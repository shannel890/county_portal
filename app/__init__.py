from flask import Flask
from flask_security import SQLAlchemyUserDatastore
from app.extension import db,migrate,mail,security
from app.models.user import User, Role
from config import Config
from flask_migrate import Migrate
from app.main.views import main_bp
from app.api.routes import api_bp
# / blueprint import
def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)
    
    migrate.init_app(app,db)
    mail.init_app(app)
    

    #register blueprints
    app.register_blueprint(main_bp)

    #register blueprints
    app.register_blueprint(api_bp)

    # Import models and intialize Flask-Security
    user_datastore = SQLAlchemyUserDatastore(db, User, Role)
    security.init_app(app,user_datastore)

    
    with app.app_context():
        db.create_all()
    return app
    