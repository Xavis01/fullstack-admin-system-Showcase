from flask import Blueprint, request, jsonify
from backend import bcrypt
from datetime import datetime
from backend.models import User, db

registration_routes = Blueprint('registration_routes', __name__)

@registration_routes.route('/api/register', methods=['POST'])
def register():
    """
    Endpoint público para auto-cadastro de usuários.
    Novos usuários são criados com is_admin=False e precisam de aprovação posterior.
    """
    data = request.get_json()
    nome = data.get('nome')
    email = data.get('email')
    dt_nascimento = data.get('dt_nascimento')  # String: 'YYYY-MM-DD' (opcional)
    password = data.get('password')

    # Validações
    if not nome or not email or not password:
        return jsonify({'error': 'Campos obrigatórios: nome, email, password'}), 400

    if len(password) < 6:
        return jsonify({'error': 'A senha deve ter no mínimo 6 caracteres.'}), 400

    # Verifica se email já existe
    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'Este e-mail já está cadastrado.'}), 409

    # Cria o hash da senha
    hashed_pw = bcrypt.generate_password_hash(password).decode('utf-8')

    # Extrai primeiro nome
    primeiro_nome = nome.split()[0] if nome else ''

    # Cria o usuário (sempre como não-admin)
    user = User(
        nome=nome,
        primeiro_nome=primeiro_nome,
        email=email,
        dt_nascimento=datetime.strptime(dt_nascimento, "%Y-%m-%d") if dt_nascimento and dt_nascimento.strip() else None,
        password_hash=hashed_pw,
        is_admin=False  # Sempre False para auto-cadastro
    )
    
    db.session.add(user)
    db.session.commit()

    return jsonify({
        'message': 'Cadastro realizado com sucesso! Aguarde a aprovação de um administrador para acessar o sistema.',
        'user': user.as_dict()
    }), 201
