# Rotas para login de usuários comuns

from flask import Blueprint, request, jsonify
from backend import bcrypt, limiter
from werkzeug.security import check_password_hash as werkzeug_check_password_hash
from flask_jwt_extended import create_access_token
from datetime import datetime
from backend.models import User, db

user_routes = Blueprint('user_routes', __name__)

################################# Rota de login de usuário #################################
@user_routes.route('/api/login', methods=['POST'])
@limiter.limit("10 per minute")
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"error": "Email e senha obrigatórios."}), 400

    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({"error": "Credenciais inválidas."}), 401

    # 1. Tenta validar com Bcrypt (novo padrão)
    try:
        if bcrypt.check_password_hash(user.password_hash, password):
            pass # Senha ok
            return jsonify({
                "message": "Login realizado com sucesso.",
                "access_token": create_access_token(identity=str(user.id), additional_claims={"is_admin": user.is_admin}),
                "user": user.as_dict()
            }), 200
    except ValueError:
        pass # Formato inválido para bcrypt, continua para tentar legado

    # 2. Se falhar (ou der erro), tenta validar com Werkzeug (padrão antigo)
    try:
        if werkzeug_check_password_hash(user.password_hash, password):
            # Senha antiga válida! Vamos atualizar para Bcrypt automaticamente.
            new_hash = bcrypt.generate_password_hash(password).decode('utf-8')
            user.password_hash = new_hash
            db.session.commit()
            # Log ou print para debug
            print(f"Usuário {user.email} migrado para Bcrypt com sucesso.")
        else:
            return jsonify({"error": "Credenciais inválidas."}), 401
    except (ValueError, Exception):
        return jsonify({"error": "Credenciais inválidas."}), 401

    # Para incluir informações no token:
    access_token = create_access_token(
        identity=str(user.id), 
        additional_claims={"is_admin": user.is_admin}
    )


    return jsonify({
        "message": "Login realizado com sucesso.",
        "access_token": access_token,
        "user": user.as_dict()
    }), 200
##############################################################################################