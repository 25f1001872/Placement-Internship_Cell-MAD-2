import os

class Config:
    SECRET_KEY = "supersecretkey"
    Base_directory = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(Base_directory,"..","instance","placement.db")

    JWT_SECRET_KEY = "jwt-secret-key"
    REDIS_URL = "redis://localhost:6379/0"
    CELERY_BROKER_URL = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND = "redis://localhost:6379/0"