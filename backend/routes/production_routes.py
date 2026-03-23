from flask import Blueprint, request, jsonify
from sqlalchemy.orm import joinedload
from sqlalchemy import func
from datetime import datetime
from backend.models import Production, Goal, GoalProduction, Return, SaleOrder, OrderProduct, db, registrar_movimentacao
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.routes.admin_routes import admin_required

production_routes = Blueprint('production_routes', __name__)

################################## CREATE - Adicionar novo lote de produção #################################
@production_routes.route('/api/productions', methods=['POST'])
@jwt_required()
@admin_required
def create_production():
    data = request.get_json()
    num_lote = data.get('num_lote')
    data_producao = data.get('data_producao')
    product_id = data.get('product_id')
    quant_caixa_produzida = data.get('quant_caixa_produzida')

    if not num_lote:
        return jsonify({'error': 'Campo obrigatório hi: num_lote'}), 400
    if not data_producao:
        return jsonify({'error': 'Campo obrigatório: data_producao'}), 400
    if not product_id:
        return jsonify({'error': 'Campo obrigatório: product_id'}), 400
    if quant_caixa_produzida is None:
        return jsonify({'error': 'Campo obrigatório: quant_caixa_produzida'}), 400

    # Lote Uniqueness Check
    if Production.query.get(num_lote):
        return jsonify({'error': f'Já existe um lote com o número {num_lote}.'}), 409

    # O estoque inicial é igual à quantidade produzida
    estoque_lote = quant_caixa_produzida

    created_by = get_jwt_identity()
    obj = Production(
        num_lote=num_lote,
        data_producao=datetime.strptime(data_producao, "%Y-%m-%d"),
        product_id=product_id,
        quant_caixa_produzida=quant_caixa_produzida,
        estoque_lote=estoque_lote,
        created_by=created_by
    )
    db.session.add(obj)
    registrar_movimentacao(
        num_lote=num_lote,
        product_id=product_id,
        tipo='production_created',
        quantidade=quant_caixa_produzida,
        estoque_apos=estoque_lote,
        referencia_id=num_lote,
        referencia_tipo='production',
        created_by=created_by
    )
    db.session.commit()

    # --- Goal Linkage Logic ---
    # Find all goals that cover this production date
    matching_goals = Goal.query.filter(
        Goal.data_inicio <= obj.data_producao,
        Goal.data_fim >= obj.data_producao
    ).all()
    
    for goal in matching_goals:
        link = GoalProduction(
            goal_id=goal.id,
            num_lote=obj.num_lote,
            quant_caixa_produzida=obj.quant_caixa_produzida
        )
        db.session.add(link)
        goal.meta_atual += obj.quant_caixa_produzida
        
    db.session.commit()
    # --------------------------

    return jsonify({'message': 'Lote de produção criado com sucesso!', 'production': obj.as_dict()}), 201
##############################################################################################################


################################ READ - Obter todos os lotes de produção #####################################
@production_routes.route('/api/productions', methods=['GET'])
@jwt_required()
@admin_required
def get_productions():
    query = Production.query
    if request.args.get('available') == 'true':
        query = query.filter(Production.estoque_lote > 0)
    
    from sqlalchemy.orm import subqueryload
    productions = query.options(joinedload(Production.user), subqueryload(Production.sales)).all()

    # Calculate reserved quantities in pending orders (achieved=False)
    # Only count OrderProducts that do NOT have a linked sale yet
    from backend.models import Sale
    reserved_filter = SaleOrder.achieved == False
    exclude_order_id = request.args.get('exclude_order_id')
    if exclude_order_id:
        reserved_filter = db.and_(reserved_filter, SaleOrder.id != int(exclude_order_id))

    reserved_query = db.session.query(
        OrderProduct.num_lote,
        func.sum(OrderProduct.quantidade).label('total_reserved')
    ).join(SaleOrder, OrderProduct.order_id == SaleOrder.id).outerjoin(
        Sale, Sale.order_product_id == OrderProduct.id
    ).filter(
        reserved_filter,
        Sale.id == None  # Only items WITHOUT a linked sale
    ).group_by(OrderProduct.num_lote).all()

    reserved_map = {r.num_lote: r.total_reserved for r in reserved_query}

    # Calculate sold quantities per lot (from sales table)
    sold_query = db.session.query(
        Sale.num_lote,
        func.sum(Sale.quant_caixa_vendida).label('total_sold')
    ).group_by(Sale.num_lote).all()

    sold_map = {s.num_lote: s.total_sold for s in sold_query}

    result = []
    for p in productions:
        d = p.as_dict()
        d['reserved_in_orders'] = reserved_map.get(p.num_lote, 0)
        d['sold_quantity'] = sold_map.get(p.num_lote, 0)
        result.append(d)

    return jsonify(result), 200
###############################################################################################################


################################ READ - Obter lote pelo número do lote ########################################
@production_routes.route('/api/productions/<num_lote>', methods=['GET'])
@jwt_required()
@admin_required
def get_production(num_lote):
    production = Production.query.get(num_lote)
    if not production:
        return jsonify({'error': 'Lote não encontrado.'}), 404
    return jsonify(production.as_dict()), 200
################################################################################################################


############################### UPDATE - Atualizar lote de produção pelo número do lote ##########################
@production_routes.route('/api/productions/<num_lote>', methods=['PUT'])
@jwt_required()
@admin_required
def update_production(num_lote):
    production = Production.query.get(num_lote)
    if not production:
        return jsonify({'error': 'Lote não encontrado.'}), 404
    data = request.get_json()
    if data.get('data_producao'):
        production.data_producao = datetime.strptime(data['data_producao'], "%Y-%m-%d")
    if data.get('product_id'):
        production.product_id = data['product_id']
    
    if data.get('quant_caixa_produzida'):
        new_quantity = int(data['quant_caixa_produzida'])
        old_quantity = production.quant_caixa_produzida
        delta = new_quantity - old_quantity
        
        # Apply delta to stock
        production.estoque_lote += delta
        
        # Ensure stock doesn't go negative (though usually shouldn't if validation is good, but safety net)
        if production.estoque_lote < 0:
             return jsonify({'error': f'A alteração de quantidade resultaria em estoque negativo ({production.estoque_lote}).'}), 400

        production.quant_caixa_produzida = new_quantity

        if delta != 0:
            registrar_movimentacao(
                num_lote=num_lote,
                product_id=production.product_id,
                tipo='production_edited',
                quantidade=delta,
                estoque_apos=production.estoque_lote,
                referencia_id=num_lote,
                referencia_tipo='production',
                created_by=get_jwt_identity()
            )

    # If stock is explicitly sent, we generally ignore it if quantity is changing to avoid overwrite
    # Or, we only allow explicit stock update if quantity is NOT changing (e.g. inventory adjustment)
    # For now, let's assume quantity change dictates stock change. 
    # But if users want to manually adjust stock without changing production qty, we should allow that?
    # The requirement is specifically about production quantity update failing to update stock.
    # So the above block handles that.
    
    # If a user sends explicit 'estoque_lote' BUT NOT 'quant_caixa_produzida', maybe they want to adjust stock manually?
    # The current frontend sends both. If we process quantity first, stock is already updated.
    # If we allow 'estoque_lote' in payload to overwrite, we re-introduce the bug because frontend sends OLD stock.
    # So we MUST ignore 'estoque_lote' from payload IF 'quant_caixa_produzida' is present.
    
    if data.get('estoque_lote') is not None and not data.get('quant_caixa_produzida'):
        # Only allow manual stock update if NOT updating production quantity
        production.estoque_lote = data['estoque_lote']
        
    db.session.commit()
    
    # --- Goal Linkage Logic (Update) ---
    # Simplified approach: Remove all links for this production and re-evaluate.
    affected_goals = set()

    # 1. Find existing links to know which goals to decrement
    existing_links = GoalProduction.query.filter_by(num_lote=num_lote).all()
    for link in existing_links:
        # Decrement from old goal
        if link.goal:
            link.goal.meta_atual -= link.quant_caixa_produzida
            affected_goals.add(link.goal)
        db.session.delete(link)
    
    # 2. Flush to apply deletions
    db.session.flush()
    
    # 3. Find matching goals for the NEW state (new date, new quantity)
    # Reload production to be safe (or use updated fields)
    if production.estoque_lote >= 0: # Only if valid? well production exists.
        matching_goals = Goal.query.filter(
            Goal.data_inicio <= production.data_producao,
            Goal.data_fim >= production.data_producao
        ).all()
        
        for goal in matching_goals:
            new_link = GoalProduction(
                goal_id=goal.id,
                num_lote=production.num_lote,
                quant_caixa_produzida=production.quant_caixa_produzida
            )
            db.session.add(new_link)
            goal.meta_atual += production.quant_caixa_produzida
            affected_goals.add(goal)
            
    # 4. Check status regression
    for goal in affected_goals:
        if goal.achieved and goal.meta_atual < goal.meta_final:
            goal.achieved = False

    db.session.commit()
    # -----------------------------------

    return jsonify({'message': 'Lote atualizado com sucesso!', 'production': production.as_dict()}), 200
################################################################################################################


############################# DELETE - Excluir lote de produção pelo número do lote ##############################
@production_routes.route('/api/productions/<num_lote>', methods=['DELETE'])
@jwt_required()
@admin_required
def delete_production(num_lote):
    production = Production.query.get(num_lote)
    if not production:
        return jsonify({'error': 'Lote não encontrado.'}), 404
    try:
        # --- Goal Linkage Logic (Delete) ---
        # 1. Remove links FIRST to avoid FK violation (since goal_productions has FK to production)
        existing_links = GoalProduction.query.filter_by(num_lote=num_lote).all()
        for link in existing_links:
            # We must update the goal's meta_atual first!
            if link.goal:
                link.goal.meta_atual -= link.quant_caixa_produzida
                if link.goal.achieved and link.goal.meta_atual < link.goal.meta_final:
                    link.goal.achieved = False
            db.session.delete(link)
        # -----------------------------------
        
        # 2. Revert linked Returns (Auto-revert status)
        linked_returns = Return.query.filter_by(novo_lote_id=num_lote).all()
        for ret in linked_returns:
            ret.novo_lote_id = None
            ret.status = 'Retornada'
            # Optional: Add observation explaining why ? 
            # ret.observacao = (ret.observacao or '') + f" [Lote {num_lote} excluído em {datetime.now().strftime('%d/%m/%Y')}]"

        # 3. Now safe to delete production
        db.session.delete(production)

        db.session.commit()
    except Exception as e:
        db.session.rollback()
        if 'foreign key constraint' in str(e).lower():
            return jsonify({'error': 'Não é possível excluir este lote pois existem Vendas vinculadas a ele.'}), 409
        return jsonify({'error': 'Erro ao excluir lote.'}), 500
    
    return jsonify({'message': 'Lote de produção excluído com sucesso!'}), 200
##################################################################################################################