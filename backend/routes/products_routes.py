from flask import Blueprint, request, jsonify
from datetime import datetime
from backend.models import Product, db
from flask_jwt_extended import jwt_required
from backend.routes.admin_routes import admin_required

products_routes = Blueprint('products_routes', __name__)

################################ CREATE - Adicionar novo produto #################################
@products_routes.route('/api/products', methods=['POST'])
@jwt_required()
@admin_required
def create_product():
    data = request.get_json()
    nome = data.get('nome')
    unidades_por_caixa = data.get('unidades_por_caixa')
    image_path = data.get('image_path')  # opcional

    if not nome or unidades_por_caixa is None:
        return jsonify({'error': 'Campos nome e unidades_por_caixa são obrigatórios.'}), 400

    # Product Name Uniqueness Check
    if Product.query.filter(Product.nome.ilike(nome)).first():
        return jsonify({'error': f'Já existe um produto com o nome "{nome}".'}), 409

    product = Product(
        nome=nome,
        unidades_por_caixa=unidades_por_caixa,
        image_path=image_path
    )
    db.session.add(product)
    db.session.commit()

    return jsonify({'message': 'Produto criado com sucesso!', 'product': product.as_dict()}), 201
##################################################################################################


################################# READ - Obter todos os produtos #################################
@products_routes.route('/api/products', methods=['GET'])
@jwt_required()
@admin_required
def get_products():
    from sqlalchemy import func
    from backend.models import Production # Import Production model

    name_filter = request.args.get('name')
    sort_by = request.args.get('sort_by') # 'nome', 'stock'
    order = request.args.get('order', 'asc') # 'asc', 'desc'

    # Query Product and calculate total stock via Left Join
    query = db.session.query(Product, func.coalesce(func.sum(Production.estoque_lote), 0).label('total_stock')) \
        .outerjoin(Production) \
        .group_by(Product.id)

    if name_filter:
        query = query.filter(Product.nome.ilike(f'%{name_filter}%'))

    if sort_by == 'stock':
        if order == 'desc':
            query = query.order_by(func.coalesce(func.sum(Production.estoque_lote), 0).desc())
        else:
            query = query.order_by(func.coalesce(func.sum(Production.estoque_lote), 0).asc())
    elif sort_by == 'nome':
        if order == 'desc':
            query = query.order_by(Product.nome.desc())
        else:
            query = query.order_by(Product.nome.asc())
    
    results = query.all()

    # Pre-fetch usage data to avoid N+1 queries
    # Get IDs of products that are used in Productions or Sales
    from backend.models import Sale
    
    product_ids_in_production = {r[0] for r in db.session.query(Production.product_id).distinct().all()}
    product_ids_in_sales = {r[0] for r in db.session.query(Sale.product_id).distinct().all()}
    used_product_ids = product_ids_in_production.union(product_ids_in_sales)

    # Manually construct response to avoid triggering lazy loading in product.as_dict()
    products_list = []
    for product, total_stock in results:
        image_url = None
        if product.image_path:
            path = product.image_path
            if path.startswith('http'):
                image_url = path
            else:
                clean_path = path.replace('backend\\', '').replace('backend/', '').replace('\\', '/')
                if not clean_path.startswith('/'):
                    clean_path = f'/{clean_path}'
                image_url = clean_path

        products_list.append({
            'id': product.id,
            'nome': product.nome,
            'total_acumulado_caixa': int(total_stock),
            'unidades_por_caixa': product.unidades_por_caixa,
            'image_path': product.image_path,
            'image_url': image_url,
            'has_dependencies': product.id in used_product_ids,
            'created_at': product.created_at.strftime("%Y-%m-%d %H:%M:%S") if product.created_at else None
        })

    return jsonify(products_list), 200
##################################################################################################


################################# READ - Obter produto pelo ID ##################################
@products_routes.route('/api/products/<int:product_id>', methods=['GET'])
@jwt_required()
@admin_required
def get_product(product_id):
    product = Product.query.get(product_id)
    if not product:
        return jsonify({'error': 'Produto não encontrado.'}), 404
    return jsonify(product.as_dict()), 200
##################################################################################################


############################### UPDATE - Atualizar produto pelo ID ###############################
@products_routes.route('/api/products/<int:product_id>', methods=['PUT'])
@jwt_required()
@admin_required
def update_product(product_id):
    product = Product.query.get(product_id)
    if not product:
        return jsonify({'error': 'Produto não encontrado.'}), 404

    data = request.get_json()
    new_nome = data.get('nome')
    if new_nome and new_nome.lower() != product.nome.lower():
         if Product.query.filter(Product.nome.ilike(new_nome)).first():
            return jsonify({'error': f'Já existe um produto com o nome "{new_nome}".'}), 409

    product.nome = new_nome if new_nome else product.nome
    product.unidades_por_caixa = data.get('unidades_por_caixa', product.unidades_por_caixa)
    product.image_path = data.get('image_path', product.image_path)
    db.session.commit()

    return jsonify({'message': 'Produto atualizado com sucesso!', 'product': product.as_dict()}), 200
#####################################################################################################


############################### DELETE - Excluir produto ############################################
@products_routes.route('/api/products/<int:product_id>', methods=['DELETE'])
@jwt_required()
@admin_required
def delete_product(product_id):
    product = Product.query.get(product_id)
    if not product:
        return jsonify({'error': 'Produto não encontrado.'}), 404

    try:
        db.session.delete(product)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        # Catch IntegrityError (sqlalchemy.exc.IntegrityError) but generic Exception is safer for now without importing
        if 'foreign key constraint' in str(e).lower():
            return jsonify({'error': 'Não é possível excluir este produto pois ele está vinculado a Lotes ou Vendas.'}), 409
        return jsonify({'error': 'Erro ao excluir produto.'}), 500

    return jsonify({'message': 'Produto excluído com sucesso!'}), 200
#####################################################################################################