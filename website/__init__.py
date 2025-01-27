from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app= Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'ORANGEPIZZA'
    db.init_app(app)
    
    from .views import my_view
    app.register_blueprint(my_view)
    
    from .login import auth
    app.register_blueprint(auth)
    
    
    from .models import Todo, Auth
    with app.app_context():
        db.create_all()
        
    return app