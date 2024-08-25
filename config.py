import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql://username:password@localhost/task_management_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.urandom(24)
    JWT_SECRET_KEY = 'your_jwt_secret_key'

config = Config()
