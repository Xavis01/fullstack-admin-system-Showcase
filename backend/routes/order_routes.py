from flask import Blueprint, request, jsonify
from sqlalchemy.orm import joinedload
from backend.models import db, SaleOrder, OrderProduct, Sale, User, Client
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.routes.admin_routes import admin_required

order_routes = Blueprint('order_routes', __name__)


# ═══════════════════════════════════════════════════════════════════════════════
# READ - Obter todos os pedidos (com eager loading otimizado)
# ═══════════════════════════════════════════════════════════════════════════════
@order_routes.route('/api/orders', methods=['GET'])
@jwt_required()
@admin_required
def get_orders():
    try:
        query = SaleOrder.query

        # Filtros
        client_id = request.args.get('client_id')
        achieved = request.args.get('achieved')

        if client_id:
            query = query.filter_by(client_id=client_id)
        if achieved is not None:
            is_achieved = achieved.lower() == 'true'
            query = query.filter_by(achieved=is_achieved)

        # Eager load relações para evitar N+1 no as_dict()
        orders = query.options(
            joinedload(SaleOrder.client),
            joinedload(SaleOrder.user),
            joinedload(SaleOrder.products)
                .joinedload(OrderProduct.production),
            joinedload(SaleOrder.products)
                .joinedload(OrderProduct.linked_sale)
        ).order_by(SaleOrder.created_at.desc()).all()

        return jsonify([order.as_dict() for order in orders]), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ═══════════════════════════════════════════════════════════════════════════════
# CREATE - Criar novo pedido
# ═══════════════════════════════════════════════════════════════════════════════
@order_routes.route('/api/orders', methods=['POST'])
@jwt_required()
@admin_required
def create_order():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    if not user:
        return jsonify({"error": "Admin account not found"}), 404

    data = request.json
    try:
        lotes = data.get('lotes', [])
        if not lotes:
            return jsonify({"error": "Selecione pelo menos um lote"}), 400

        new_order = SaleOrder(
            client_id=data['client_id'],
            quant_caixa_solicitada=data['quant_caixa_solicitada'],
            achieved=data.get('achieved', False),
            observacao=data.get('observacao'),
            created_by=user.id
        )
        db.session.add(new_order)
        db.session.flush()

        for lote_data in lotes:
            num_lote = lote_data.get('num_lote')
            quantidade = lote_data.get('quantidade', 0)
            
            if quantidade <= 0:
                raise ValueError(f"A quantidade do lote {num_lote} deve ser maior que zero")

            op = OrderProduct(
                order_id=new_order.id,
                num_lote=num_lote,
                quantidade=quantidade
            )
            db.session.add(op)

        db.session.commit()

        return jsonify({
            "message": "Order created successfully",
            "order": new_order.as_dict()
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400


# ═══════════════════════════════════════════════════════════════════════════════
# UPDATE - Atualizar pedido (protege lotes com vendas vinculadas)
# ═══════════════════════════════════════════════════════════════════════════════
@order_routes.route('/api/orders/<int:order_id>', methods=['PUT'])
@jwt_required()
@admin_required
def update_order(order_id):
    order = SaleOrder.query.get_or_404(order_id)
    data = request.json
    try:
        if 'client_id' in data:
            order.client_id = data['client_id']
        if 'quant_caixa_solicitada' in data:
            order.quant_caixa_solicitada = data['quant_caixa_solicitada']
        if 'achieved' in data:
            order.achieved = data['achieved']
        if 'observacao' in data:
            order.observacao = data['observacao']

        # Atualizar lotes (preservando vendidos)
        if 'lotes' in data:
            # Identificar lotes com venda vinculada (JOIN para evitar N+1)
            existing_ops = (
                OrderProduct.query
                .options(joinedload(OrderProduct.linked_sale))
                .filter_by(order_id=order.id)
                .all()
            )
            sold_lotes = {}
            for op in existing_ops:
                if op.linked_sale is not None:
                    sold_lotes[str(op.num_lote)] = op

            # Verificar que lotes vendidos não foram removidos do payload
            new_lote_nums = {str(l.get('num_lote')) for l in data['lotes']}
            for num_lote, op in sold_lotes.items():
                if num_lote not in new_lote_nums:
                    raise ValueError(f"O lote #{num_lote} possui uma venda vinculada e não pode ser removido.")

            # Deletar apenas lotes sem venda
            for op in existing_ops:
                if str(op.num_lote) not in sold_lotes:
                    db.session.delete(op)

            # Adicionar novos lotes (skip vendidos)
            for lote_data in data['lotes']:
                num_lote = str(lote_data.get('num_lote'))
                quantidade = lote_data.get('quantidade', 0)

                if num_lote in sold_lotes:
                    continue

                if quantidade <= 0:
                    raise ValueError(f"A quantidade do lote {num_lote} deve ser maior que zero")

                op = OrderProduct(
                    order_id=order.id,
                    num_lote=num_lote,
                    quantidade=quantidade
                )
                db.session.add(op)

        # Auto-concluir se todos os lotes restantes foram vendidos
        if 'lotes' in data:
            db.session.flush()  # Garante que deletes/adds estão refletidos
            total_items = OrderProduct.query.filter_by(order_id=order.id).count()
            sold_items = (
                db.session.query(OrderProduct.id)
                .join(Sale, Sale.order_product_id == OrderProduct.id)
                .filter(OrderProduct.order_id == order.id)
                .count()
            )
            order.achieved = (total_items > 0 and sold_items >= total_items)

        db.session.commit()
        return jsonify({
            "message": "Order updated successfully",
            "order": order.as_dict()
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400


# ═══════════════════════════════════════════════════════════════════════════════
# DELETE - Excluir pedido (bloqueia se tiver vendas vinculadas)
# ═══════════════════════════════════════════════════════════════════════════════
@order_routes.route('/api/orders/<int:order_id>', methods=['DELETE'])
@jwt_required()
@admin_required
def delete_order(order_id):
    order = SaleOrder.query.get_or_404(order_id)
    try:
        # Verificar se algum lote tem venda vinculada
        sold_count = (
            db.session.query(OrderProduct.id)
            .join(Sale, Sale.order_product_id == OrderProduct.id)
            .filter(OrderProduct.order_id == order.id)
            .count()
        )
        if sold_count > 0:
            return jsonify({
                "error": f"Este pedido possui {sold_count} lote(s) com venda vinculada. Exclua as vendas antes de excluir o pedido."
            }), 409

        db.session.delete(order)
        db.session.commit()
        return jsonify({"message": "Order deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400


# ═══════════════════════════════════════════════════════════════════════════════
# PATCH - Toggle status "separado" (requer master)
# ═══════════════════════════════════════════════════════════════════════════════
@order_routes.route('/api/orders/<int:order_id>/toggle-separado', methods=['PATCH'])
@jwt_required()
@admin_required
def toggle_separado(order_id):
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    if not user or not user.is_master:
        return jsonify({"error": "Somente usuários master podem alterar o status de separação."}), 403

    order = SaleOrder.query.get_or_404(order_id)

    if order.achieved:
        return jsonify({"error": "Pedidos concluídos não podem ter o status de separação alterado."}), 400

    try:
        order.separado = not order.separado
        db.session.commit()
        return jsonify({
            "message": f"Pedido {'marcado como separado' if order.separado else 'retornado para pendente'}.",
            "separado": order.separado
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400
