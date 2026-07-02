from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .config import Config
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from .extensions import db, jwt



def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    jwt.init_app(app)
    CORS(app)

    with app.app_context():
        from . import models
        db.create_all()

        from app.models.user import User
        from werkzeug.security import generate_password_hash

        existing_admin = User.query.filter_by(role = "admin").first()

        if not existing_admin:
            admin = User(
                name="Admin",
                email="admin@gmail.com",
                password_hash=generate_password_hash("admin@2005"),
                role="admin"
            )
            db.session.add(admin)
            db.session.commit()


        from .routes.auth_routes import auth_bp
        from .routes.admin_routes import admin_bp
        from .routes.company_routes import company_bp
        app.register_blueprint(auth_bp)
        app.register_blueprint(admin_bp)
        app.register_blueprint(company_bp)

    return app

