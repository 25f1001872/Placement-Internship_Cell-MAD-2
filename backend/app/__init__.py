from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .config import Config
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from .extensions import db, jwt, mail, celery
from celery.schedules import crontab


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    jwt.init_app(app)
    mail.init_app(app)
    CORS(app)

    celery.conf.update(
        broker_url=app.config['CELERY_BROKER_URL'],
        result_backend=app.config['CELERY_RESULT_BACKEND'],
        beat_schedule={
        'send-interview-reminders-daily': {
            'task': 'app.tasks.jobs.send_interview_reminders',
            'schedule': crontab(hour=9, minute=0),
        },
        'monthly-placement-report': {
            'task': 'app.tasks.jobs.generate_monthly_report',
            'schedule': crontab(day_of_month=1, hour=8, minute=0),
        },
    }
    )

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask

    with app.app_context():
        from . import models
        db.create_all()

        from app.models.user import User
        from werkzeug.security import generate_password_hash
        if not User.query.filter_by(role="admin").first():
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
        from .routes.student_routes import student_bp
        from .routes.tasks_routes import tasks_bp
        app.register_blueprint(auth_bp)
        app.register_blueprint(admin_bp)
        app.register_blueprint(company_bp)
        app.register_blueprint(student_bp)
        app.register_blueprint(tasks_bp)

    return app

