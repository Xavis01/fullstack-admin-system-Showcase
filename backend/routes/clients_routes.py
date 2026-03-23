# Rotas para clientes

from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash
from datetime import datetime
from backend.models import Client, db
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from backend.routes.admin_routes import admin_required

clients_routes = Blueprint('clients_routes', __name__)


############################## CREATE - Adicionar novo cliente ##############################
@clients_routes.route('/api/clients', methods=['POST'])
@jwt_required()
@admin_required
def create_client():
    data = request.get_json()

    nome = data.get('nome')
    telefone = data.get('telefone')

    if not nome:
        return jsonify({'error': 'Campo nome é obrigatório'}), 400

    # Client Name Uniqueness Check
    if Client.query.filter(Client.nome.ilike(nome)).first():
        return jsonify({'error': f'Já existe um cliente com o nome "{nome}".'}), 409

    client = Client(nome=nome, telefone=telefone or None)
    db.session.add(client)
    db.session.commit()

    return jsonify({'message': 'Cliente criado com sucesso', 'client': client.as_dict()}), 201
###############################################################################################


################################# READ - Obter todos os clientes ################################
@clients_routes.route('/api/clients', methods=['GET'])
@jwt_required()
@admin_required
def get_clients():
    from sqlalchemy import func
    from backend.models import Sale # Import Sale model

    name_filter = request.args.get('name')
    sort_by = request.args.get('sort_by')  # 'nome', 'total'
    order = request.args.get('order', 'asc')  # 'asc', 'desc'
    created_order = request.args.get('created_order', 'desc')  # 'asc', 'desc'

    # Query Client, Count(Sales), Sum(QuantCaixa)
    query = db.session.query(
        Client, 
        func.count(Sale.id).label('total_compras'), 
        func.coalesce(func.sum(Sale.quant_caixa_vendida), 0).label('total_caixas')
    ).outerjoin(Sale).group_by(Client.id)

    if name_filter:
        query = query.filter(Client.nome.ilike(f'%{name_filter}%'))

    # Determine sort order
    if sort_by == 'total':
        if order == 'desc':
            query = query.order_by(func.coalesce(func.sum(Sale.quant_caixa_vendida), 0).desc())
        else:
            query = query.order_by(func.coalesce(func.sum(Sale.quant_caixa_vendida), 0).asc())
    elif sort_by == 'nome':
        if order == 'desc':
            query = query.order_by(Client.nome.desc())
        else:
            query = query.order_by(Client.nome.asc())
    else:
        # Fallback to created_order
        if created_order == 'asc':
            query = query.order_by(Client.created_at.asc())
        else:
            query = query.order_by(Client.created_at.desc())

    results = query.all()

    clients_list = []
    for client, total_compras, total_caixas in results:
        clients_list.append({
            'id': client.id,
            'nome': client.nome,
            'telefone': client.telefone,
            'total_compras': total_compras,
            'total_caixas': int(total_caixas),
            'created_at': client.created_at.strftime("%Y-%m-%d %H:%M:%S") if client.created_at else None,
            'sales': [
                {
                    'num_lote': sale.num_lote,
                    'quant_caixa_vendida': sale.quant_caixa_vendida,
                    'data_venda': sale.data_venda.strftime("%Y-%m-%d") if sale.data_venda else None
                }
                for sale in sorted(client.sales, key=lambda x: x.data_venda, reverse=True)
            ]
        })

    return jsonify(clients_list), 200
##################################################################################################


################################# READ - Obter cliente pelo ID ##################################
@clients_routes.route('/api/clients/<int:client_id>', methods=['GET'])
@jwt_required()
@admin_required
def get_client(client_id):
    client = Client.query.get(client_id)
    if not client:
        return jsonify({'error': 'Cliente não encontrado'}), 404
    return jsonify(client.as_dict()), 200
##################################################################################################


############################### UPDATE - Atualizar cliente pelo ID ###############################
@clients_routes.route('/api/clients/<int:client_id>', methods=['PUT'])
@jwt_required()
@admin_required
def update_client(client_id):
    client = Client.query.get(client_id)
    if not client:
        return jsonify({'error': 'Cliente não encontrado'}), 404

    data = request.get_json()
    new_nome = data.get('nome')
    if new_nome and new_nome.lower() != client.nome.lower():
        if Client.query.filter(Client.nome.ilike(new_nome)).first():
            return jsonify({'error': f'Já existe um cliente com o nome "{new_nome}".'}), 409
    
    client.nome = new_nome if new_nome else client.nome
    
    new_telefone = data.get('telefone')
    # If key is present but empty, set to None. If key not present, keep old.
    if 'telefone' in data:
        client.telefone = new_telefone or None

    db.session.commit()
    return jsonify({'message': 'Cliente atualizado com sucesso', 'client': client.as_dict()}), 200
##################################################################################################


################################### DELETE - Excluir cliente pelo ID ##############################
@clients_routes.route('/api/clients/<int:client_id>', methods=['DELETE'])
@jwt_required()
@admin_required
def delete_client(client_id):
    client = Client.query.get(client_id)
    if not client:
        return jsonify({'error': 'Cliente não encontrado'}), 404

    try:
        db.session.delete(client)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        if 'foreign key constraint' in str(e).lower():
            return jsonify({'error': 'Não é possível excluir este cliente pois ele possui Compras registradas.'}), 409
        return jsonify({'error': 'Erro ao excluir cliente.'}), 500
    
    return jsonify({'message': 'Cliente excluído com sucesso'}), 200
##################################################################################################