from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path

db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    from flask_login import LoginManager

    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'abcdcewvewv'

    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'    
    db.init_app(app)


    

    
    from .views import views
    from .auth import auth


    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Notes
    
    
    with app.app_context():
        db.create_all()

    
    LoginManager = LoginManager()
    LoginManager.login_view = 'auth.login' #when not logged in
    LoginManager.init_app(app)

    @LoginManager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    
    return app



    
    