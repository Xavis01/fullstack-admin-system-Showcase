from backend import create_app, db, bcrypt
from backend.models import User

app = create_app()

with app.app_context():
    email = "admin@escorpiao.com"
    password = "admin"
    
    existing_user = User.query.filter_by(email=email).first()
    
    if not existing_user:
        admin_user = User(
            nome="Admin User",
            primeiro_nome="Admin",
            email=email,
            password_hash=bcrypt.generate_password_hash(password).decode('utf-8'),
            is_admin=True
        )
        db.session.add(admin_user)
        db.session.commit()
        print(f"Admin user created: {email} / {password}")
    else:
        print(f"Admin user already exists: {email}")
