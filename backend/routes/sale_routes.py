from flask import Blueprint, request, jsonify
from sqlalchemy.orm import joinedload
from datetime import datetime
from backend.models import Sale, Production, OrderProduct, SaleOrder, db, registrar_movimentacao
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.routes.admin_routes import admin_required

sale_routes = Blueprint('sale_routes', __name__)


# ═══════════════════════════════════════════════════════════════════════════════
# CREATE - Adicionar nova venda
# ═══════════════════════════════════════════════════════════════════════════════
@sale_routes.route('/api/sales', methods=['POST'])
@jwt_required()
@admin_required
def create_sale():
    data = request.get_json()
    num_lote = data.get('num_lote')
    product_id = data.get('product_id')
    data_venda = data.get('data_venda')
    client_id = data.get('client_id')
    quant_caixa_vendida = data.get('quant_caixa_vendida')
    order_product_id = data.get('order_product_id')

    if not all([num_lote, product_id, data_venda, client_id, quant_caixa_vendida]):
        return jsonify({'error': 'Campos obrigatórios: num_lote, product_id, data_venda, client_id, quant_caixa_vendida'}), 400

    qty = int(quant_caixa_vendida)

    try:
        # Validar lote e estoque numa única query
        production = Production.query.get(num_lote)
        if not production:
            return jsonify({'error': 'Lote não encontrado.'}), 404
        if production.product_id != product_id:
            return jsonify({'error': 'Produto não confere com o lote.'}), 400
        if qty > production.estoque_lote:
            return jsonify({'error': f'Estoque insuficiente. Disponível: {production.estoque_lote}, Solicitado: {qty}'}), 409

        # Validar vínculo com item de expedição (se fornecido)
        order_product = None
        if order_product_id:
            order_product = OrderProduct.query.get(order_product_id)
            if not order_product:
                return jsonify({'error': 'Item de expedição não encontrado.'}), 404
            if order_product.linked_sale is not None:
                return jsonify({'error': 'Este item de expedição já possui uma venda vinculada.'}), 409
            if order_product.num_lote != num_lote:
                return jsonify({'error': 'O lote da venda não confere com o lote do item de expedição.'}), 400

        # Atualizar estoque do lote
        production.estoque_lote -= qty

        created_by = get_jwt_identity()
        sale = Sale(
            num_lote=num_lote,
            product_id=product_id,
            data_venda=datetime.strptime(data_venda, "%Y-%m-%d"),
            client_id=client_id,
            quant_caixa_vendida=qty,
            created_by=created_by,
            order_product_id=order_product_id
        )
        db.session.add(sale)
        db.session.flush()

        registrar_movimentacao(
            num_lote=num_lote,
            product_id=product_id,
            tipo='sale_created',
            quantidade=-qty,
            estoque_apos=production.estoque_lote,
            referencia_id=sale.id,
            referencia_tipo='sale',
            created_by=created_by
        )

        # Auto-concluir expedição se todos os lotes foram vendidos
        if order_product_id and order_product:
            order = SaleOrder.query.get(order_product.order_id)
            if order:
                # Query direta e scoped — conta apenas os OrderProducts DESTE pedido
                total_items = OrderProduct.query.filter_by(order_id=order.id).count()
                sold_items = (
                    db.session.query(OrderProduct.id)
                    .join(Sale, Sale.order_product_id == OrderProduct.id)
                    .filter(OrderProduct.order_id == order.id)
                    .count()
                )
                if sold_items >= total_items:
                    order.achieved = True

        db.session.commit()
        return jsonify({'message': 'Venda cadastrada com sucesso!', 'sale': sale.as_dict()}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Erro ao criar venda: {str(e)}'}), 500


# ═══════════════════════════════════════════════════════════════════════════════
# READ - Obter todas as vendas (com eager loading otimizado)
# ═══════════════════════════════════════════════════════════════════════════════
@sale_routes.route('/api/sales', methods=['GET'])
@jwt_required()
@admin_required
def get_sales():
    query = Sale.query

    # Filtros
    sale_id = request.args.get('sale_id')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    client_id = request.args.get('client_id')
    product_id = request.args.get('product_id')
    num_lote = request.args.get('num_lote')

    if sale_id:
        from sqlalchemy import cast, String
        query = query.filter(cast(Sale.id, String).ilike(f'%{sale_id}%'))
    if start_date:
        query = query.filter(Sale.data_venda >= datetime.strptime(start_date, "%Y-%m-%d"))
    if end_date:
        query = query.filter(Sale.data_venda <= datetime.strptime(end_date, "%Y-%m-%d"))
    if client_id:
        query = query.filter(Sale.client_id == client_id)
    if product_id:
        query = query.filter(Sale.product_id == product_id)
    if num_lote:
        query = query.filter(Sale.num_lote.ilike(f'%{num_lote}%'))

    # Eager load todas as relações necessárias para evitar N+1
    sales = query.options(
        joinedload(Sale.user),
        joinedload(Sale.client),
        joinedload(Sale.product),
        joinedload(Sale.production),
        joinedload(Sale.returns)
    ).order_by(Sale.data_venda.desc()).all()

    sales_list = []
    for s in sales:
        sale_dict = s.as_dict()
        
        # Campos agregados para a UI
        sale_dict['client_name'] = s.client.nome if s.client else 'Cliente Desconhecido'
        sale_dict['product_name'] = s.product.nome if s.product else 'Produto Desconhecido'
        
        # Imagem do produto — normalização de path
        image_url = None
        if s.product and s.product.image_path:
            path = s.product.image_path
            if path.startswith('http'):
                image_url = path
            else:
                clean_path = path.replace('backend\\', '').replace('backend/', '').replace('\\', '/')
                if not clean_path.startswith('/'):
                    clean_path = f'/{clean_path}'
                image_url = clean_path
        sale_dict['product_image'] = image_url

        sale_dict['remaining_stock'] = s.production.estoque_lote if s.production else 'N/A'
        
        # Resumo de devoluções (já carregado via eager load)
        total_returned = sum(r.quant_devolvida for r in s.returns)
        has_returns = total_returned > 0
        
        sale_dict['returns_info'] = {
            'has_returns': has_returns,
            'total_returned': total_returned,
            'latest_status': s.returns[-1].status if has_returns else None
        }
        
        sales_list.append(sale_dict)

    return jsonify(sales_list), 200


# ═══════════════════════════════════════════════════════════════════════════════
# READ - Obter venda pelo ID
# ═══════════════════════════════════════════════════════════════════════════════
@sale_routes.route('/api/sales/<int:sale_id>', methods=['GET'])
@jwt_required()
@admin_required
def get_sale(sale_id):
    sale = Sale.query.options(
        joinedload(Sale.user),
        joinedload(Sale.client),
        joinedload(Sale.product),
        joinedload(Sale.production)
    ).get(sale_id)
    if not sale:
        return jsonify({'error': 'Venda não encontrada.'}), 404
    return jsonify(sale.as_dict()), 200


# ═══════════════════════════════════════════════════════════════════════════════
# UPDATE - Atualizar venda pelo ID
# ═══════════════════════════════════════════════════════════════════════════════
@sale_routes.route('/api/sales/<int:sale_id>', methods=['PUT'])
@jwt_required()
@admin_required
def update_sale(sale_id):
    sale = Sale.query.get(sale_id)
    if not sale:
        return jsonify({'error': 'Venda não encontrada.'}), 404
    
    # Bloquear edição de vendas vinculadas a expedições
    if sale.order_product_id:
        return jsonify({'error': 'Vendas vinculadas a expedições não podem ser editadas. Você pode apenas excluí-la e refazer a venda.'}), 403
    
    data = request.get_json()
    
    try:
        current_user = get_jwt_identity()

        # Rollback do estoque anterior
        old_lote = sale.num_lote
        old_qty = int(sale.quant_caixa_vendida)
        old_production = Production.query.get(old_lote)
        if old_production:
            old_production.estoque_lote += old_qty
            registrar_movimentacao(
                num_lote=old_lote,
                product_id=old_production.product_id,
                tipo='sale_edit_rollback',
                quantidade=+old_qty,
                estoque_apos=old_production.estoque_lote,
                referencia_id=sale_id,
                referencia_tipo='sale',
                created_by=current_user
            )
        
        # Novos dados
        new_lote = data.get('num_lote', sale.num_lote)
        new_qty = int(data.get('quant_caixa_vendida', sale.quant_caixa_vendida))
        new_production = Production.query.get(new_lote)
        
        if not new_production:
            db.session.rollback()
            return jsonify({'error': 'Novo lote não encontrado.'}), 404
        
        # Validar novo estoque
        if new_qty > new_production.estoque_lote:
            db.session.rollback()
            return jsonify({'error': f'Estoque insuficiente. Disponível: {new_production.estoque_lote}, Solicitado: {new_qty}'}), 409

        # Subtrai do novo lote
        new_production.estoque_lote -= new_qty
        registrar_movimentacao(
            num_lote=new_lote,
            product_id=new_production.product_id,
            tipo='sale_edited',
            quantidade=-new_qty,
            estoque_apos=new_production.estoque_lote,
            referencia_id=sale_id,
            referencia_tipo='sale',
            created_by=current_user
        )
        
        # Atualiza os campos
        sale.num_lote = new_lote
        if data.get('product_id'): 
            sale.product_id = data['product_id']
        if data.get('data_venda'): 
            sale.data_venda = datetime.strptime(data['data_venda'], "%Y-%m-%d")
        if data.get('client_id'): 
            sale.client_id = data['client_id']
        sale.quant_caixa_vendida = new_qty
        
        db.session.commit()
        return jsonify({'message': 'Venda atualizada com sucesso!', 'sale': sale.as_dict()}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Erro ao atualizar venda: {str(e)}'}), 500


# ═══════════════════════════════════════════════════════════════════════════════
# DELETE - Excluir venda pelo ID
# ═══════════════════════════════════════════════════════════════════════════════
@sale_routes.route('/api/sales/<int:sale_id>', methods=['DELETE'])
@jwt_required()
@admin_required
def delete_sale(sale_id):
    sale = Sale.query.get(sale_id)
    if not sale:
        return jsonify({'error': 'Venda não encontrada.'}), 404

    try:
        current_user = get_jwt_identity()

        # Se tinha vínculo com expedição, reverter achieved
        if sale.order_product_id:
            order_product = OrderProduct.query.get(sale.order_product_id)
            if order_product:
                order = SaleOrder.query.get(order_product.order_id)
                if order and order.achieved:
                    order.achieved = False

        # Rollback do estoque do lote
        production = Production.query.get(sale.num_lote)
        if production:
            qty = int(sale.quant_caixa_vendida)
            production.estoque_lote += qty
            registrar_movimentacao(
                num_lote=sale.num_lote,
                product_id=sale.product_id,
                tipo='sale_deleted',
                quantidade=+qty,
                estoque_apos=production.estoque_lote,
                referencia_id=sale_id,
                referencia_tipo='sale',
                created_by=current_user
            )

        db.session.delete(sale)
        db.session.commit()
        return jsonify({'message': 'Venda excluída com sucesso!'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Erro ao excluir venda: {str(e)}'}), 500