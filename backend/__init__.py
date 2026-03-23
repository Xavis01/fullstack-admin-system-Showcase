from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from backend.config import DevelopmentConfig, ProductionConfig
from flask_jwt_extended import JWTManager
from backend.jwt_helper import init_jwt
from flask_bcrypt import Bcrypt
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_talisman import Talisman
import os

db = SQLAlchemy()
bcrypt = Bcrypt()
limiter = Limiter(key_func=get_remote_address, default_limits=["300 per minute"])

def create_app():
    app = Flask(__name__)
    flask_env = os.getenv("FLASK_ENV", "development")
    if flask_env == "production":
        app.config.from_object(ProductionConfig)
    else:
        app.config.from_object(DevelopmentConfig)
    
    # Configurações para evitar timeout de conexão com MySQL
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        'pool_pre_ping': True,  # Testa conexão antes de usar
        'pool_recycle': 3600,   # Recicla conexões após 1 hora
        'connect_args': {
            'connect_timeout': 10,  # Timeout de conexão em segundos
        }
    }
    

    db.init_app(app)
    bcrypt.init_app(app)
    limiter.init_app(app)
    init_jwt(app)
    
    # Security Headers (Talisman)
    # Em produção force_https=True, em desenvolvimento False para não quebrar localhost
    is_production = flask_env == "production"
    
    csp = {
        'default-src': '\'self\'',
        'img-src': '*',
        'style-src': ['\'self\'', '\'unsafe-inline\''], # Permite styles inline se necessário (Vue pode precisar)
        'script-src': ['\'self\'', '\'unsafe-eval\'']   # Vue as vezes precisa de unsafe-eval em dev
    }

    Talisman(app, force_https=is_production, content_security_policy=csp)
    
    from flask_cors import CORS
    # Configuração de CORS dinâmica
    if flask_env == "production":
        allowed_origins = [
            "https://admin.sodaescorpiao.com.br"
        ]
        CORS(app, resources={r"/api/*": {"origins": allowed_origins}}, supports_credentials=True)
    else:
        # Em desenvolvimento, permite tudo para facilitar testes no celular e localhost
        CORS(app, resources={r"/api/*": {"origins": "*"}}, supports_credentials=True)

    # Importa as rotas aqui dentro da função, para evitar import circular
    from backend.routes.user_routes import user_routes
    from backend.routes.admin_routes import admin_routes
    from backend.routes.clients_routes import clients_routes
    from backend.routes.products_routes import products_routes
    from backend.routes.production_routes import production_routes
    from backend.routes.sale_routes import sale_routes
    from backend.routes.registration_routes import registration_routes
    from backend.routes.dashboard_routes import dashboard_routes
    from backend.routes.goal_routes import goal_routes
    from backend.routes.return_routes import return_routes
    from backend.routes.order_routes import order_routes
    from backend.routes.procedure_routes import procedure_routes
    
    app.register_blueprint(user_routes)
    app.register_blueprint(admin_routes)
    app.register_blueprint(clients_routes)
    app.register_blueprint(products_routes)
    app.register_blueprint(production_routes)
    app.register_blueprint(sale_routes)
    app.register_blueprint(registration_routes)
    app.register_blueprint(dashboard_routes)
    app.register_blueprint(goal_routes)
    app.register_blueprint(return_routes)
    app.register_blueprint(order_routes)
    app.register_blueprint(procedure_routes)

    return app
