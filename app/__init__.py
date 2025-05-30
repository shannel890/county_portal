from flask import Flask
from flask_security import SQLAlchemyUserDatastore
from app.extension import db, mail, security
from app.models.user import User, Role
from flask_security import hash_password
from config import Config
import uuid
# Import necessary modules and blueprints
from app.main.views import main_bp
from app.api.routes import api_bp
from app.auth.routes import auth_bp
# / blueprint import
def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)
    mail.init_app(app)
    

    #register blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp)
    app.register_blueprint(auth_bp)
    # Import models and intialize Flask-Security
    user_datastore = SQLAlchemyUserDatastore(db, User, Role)
    security.init_app(app,user_datastore)

    
    with app.app_context():
        db.create_all()

        roles_data = [{'name': 'super_admin', 'description': 'Administrator role'},
                      {'name': 'staff', 'description': 'county staff with limited access'},
                      {'name': 'citizen', 'description': 'citizen with basic data access'},
                      {'name': 'guest', 'description': 'guest with minimal access'}]
        for role_data in roles_data:
            role = Role.query.filter_by(name=role_data['name']).first()
            if not role:
                role = Role(**role_data)
                db.session.add(role)
        db.session.commit()

        admin_role = Role.query.filter_by(name='super_admin').first()
        admin_user = User.query.filter_by(email='shannel@gmail.com').first()

        if not admin_user:
            admin_user = User(
                email='shannel@gmail.com',
                password=hash_password('shannel254'),  # Use a hashed password in production
                active=True,
                roles=[admin_role],
                fs_uniquifier=str(uuid.uuid4())
            )
            db.session.add(admin_user)
        db.session.commit()
        print("Admin user created successfully.")

    return app
    