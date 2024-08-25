from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)
jwt = JWTManager(app)

from .routes import *

if __name__ == "__main__":
    app.run(debug=True)
