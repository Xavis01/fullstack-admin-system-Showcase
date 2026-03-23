# Rotas para funcionalidades exclusivas de administradores

from flask import Blueprint, request, jsonify
from backend import bcrypt
from datetime import datetime
from backend.models import User, db
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from functools import wraps
from sqlalchemy import inspect, text

admin_routes = Blueprint('admin_routes', __name__)


#################### Middleware simples para checar se  é admin ###########################
def admin_required(fn):

    @wraps(fn)
    def wrapper(*args, **kwargs):
        claims = get_jwt()
        if not claims.get('is_admin'):
            return jsonify({'error': 'Acesso restrito a administradores.'}), 403
        return fn(*args, **kwargs)

    return wrapper
##########################################################################################


############################## Rota de CREATE usuário #######################################
@admin_routes.route('/api/users', methods=['POST'])
@jwt_required()
@admin_required
def create_user():
    data = request.get_json()
    nome = data.get('nome')
    email = data.get('email')
    dt_nascimento = data.get('dt_nascimento')  # String: 'YYYY-MM-DD'
    password = data.get('password')
    is_admin = data.get('is_admin', False)
    is_master = data.get('is_master', False)

    if not nome or not email or not password:
        return jsonify({'error': 'Campos obrigatórios: nome, email, password'}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'Email já cadastrado!'}), 409

    hashed_pw = bcrypt.generate_password_hash(password).decode('utf-8')

    primeiro_nome = nome.split()[0] if nome else ''

    user = User(
        nome=nome,
        primeiro_nome=primeiro_nome,
        email=email,
        dt_nascimento=datetime.strptime(dt_nascimento, "%Y-%m-%d") if dt_nascimento and dt_nascimento.strip() else None,
        password_hash=hashed_pw,
        is_admin=is_admin,
        is_master=is_master
    )
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'Administrador cadastrado!', 'user': user.as_dict()}), 201
##############################################################################################


###################################### Rota de READ de usuário ######################################
@admin_routes.route('/api/users', methods=['GET'])
@jwt_required()
@admin_required
def get_users():
    users = User.query.all()
    users_list = [user.as_dict() for user in users]
    return jsonify(users_list), 200
#######################################################################################################


##################################### Rota para READ de um usuário ######################################
@admin_routes.route('/api/users/<int:user_id>', methods=['GET'])
@jwt_required()
@admin_required
def get_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "Usuário não encontrado."}), 404
    return jsonify(user.as_dict()), 200
##########################################################################################################


###################################### Rota para UPDATE de usuário ######################################
@admin_routes.route('/api/users/<int:user_id>', methods=['PUT'])
@jwt_required()
@admin_required
def update_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "Usuário não encontrado."}), 404
    
    data = request.get_json()
    
    novo_nome = data.get('nome', user.nome)
    user.nome = novo_nome
    user.primeiro_nome = novo_nome.split()[0] if novo_nome else user.primeiro_nome

    user.email = data.get('email', user.email)
    
    dt_nasc = data.get('dt_nascimento')
    if dt_nasc and dt_nasc.strip():
        user.dt_nascimento = datetime.strptime(dt_nasc, "%Y-%m-%d")
    
    if data.get('password'):
        user.password_hash = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    
    user.is_admin = data.get('is_admin', user.is_admin)
    user.is_master = data.get('is_master', user.is_master)
    
    db.session.commit()
    
    return jsonify({'message': 'Usuário atualizado com sucesso.', 'user': user.as_dict()}), 200
######################################################################################################


###################################### Rota de DELETE de usuário ######################################
@admin_routes.route('/api/users/<int:user_id>', methods=['DELETE'])
@jwt_required()
@admin_required
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "Usuário não encontrado."}), 404
    
    db.session.delete(user)
    db.session.commit()

    return jsonify({"message": f"Usuário {user.nome} excluído com sucesso."}), 200
######################################################################################################


######################### Rota para SINCRONIZAR o banco de dados #####################################
@admin_routes.route('/api/admin/sync-database', methods=['POST'])
@jwt_required()
@admin_required
def sync_database():
    try:
        # 1) Cria tabelas novas que ainda não existem
        db.create_all()

        # 2) Detecta colunas faltantes em tabelas existentes e adiciona via ALTER TABLE
        inspector = inspect(db.engine)
        existing_tables = inspector.get_table_names()
        added_columns = []

        for table in db.metadata.sorted_tables:
            if table.name not in existing_tables:
                continue  # tabela nova, já foi criada pelo create_all()

            # Colunas que existem no banco
            db_columns = {col['name'] for col in inspector.get_columns(table.name)}

            # Colunas definidas no model
            for column in table.columns:
                if column.name not in db_columns:
                    # Montar o tipo SQL
                    col_type = column.type.compile(dialect=db.engine.dialect)
                    nullable = "NULL" if column.nullable else "NOT NULL"
                    
                    default_clause = ""
                    if column.default is not None:
                        default_val = column.default.arg
                        if isinstance(default_val, bool):
                            default_clause = f"DEFAULT {1 if default_val else 0}"
                        elif isinstance(default_val, (int, float)):
                            default_clause = f"DEFAULT {default_val}"
                        elif isinstance(default_val, str):
                            default_clause = f"DEFAULT '{default_val}'"
                    
                    sql = f"ALTER TABLE `{table.name}` ADD COLUMN `{column.name}` {col_type} {nullable} {default_clause}"
                    db.session.execute(text(sql))
                    added_columns.append(f"{table.name}.{column.name}")

        db.session.commit()

        if added_columns:
            msg = f"Sincronizado! Colunas adicionadas: {', '.join(added_columns)}"
        else:
            msg = "Banco de dados já está sincronizado. Nenhuma alteração necessária."

        return jsonify({'message': msg, 'added_columns': added_columns}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Erro ao sincronizar: {str(e)}'}), 500
######################################################################################################