from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from flask_cors import CORS

db = SQLAlchemy()
DB_NAME = 'database.db'

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config['SECRET_KEY'] = 'Gene'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix = "/")
    app.register_blueprint(auth, url_prefix = "/")

    from .models import User

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(id)

    with app.app_context():
        #Unhash this and run if you are adding new things to database
        #db.drop_all()
        db.create_all()

    return app 
