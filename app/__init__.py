from flask import Flask
from app.extension import db
from config import Config
from flask_migrate import Migrate
from app.main.views import main_bp
from app.api.routes import api_bp
# / blueprint import
def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)
    migrate = Migrate(app, db)

    #register blueprints
    app.register_blueprint(main_bp)

    #register blueprints
    app.register_blueprint(api_bp)



    
    with app.app_context():
        db.create_all()
    return app
    