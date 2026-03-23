from flask_jwt_extended import JWTManager
from datetime import timedelta

jwt = JWTManager()

def init_jwt(app):
    # Configurações recomendadas
    app.config['JWT_SECRET_KEY'] = 'sua_chave_secreta_supersegura'
    # Define expiração do token em 1 hora
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
    jwt.init_app(app)
