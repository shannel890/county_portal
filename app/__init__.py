from flask import Flask
from flask_security import SQLAlchemyUserDatastore
from app.extension import db, mail, security
from app.models.user import User, Role
from app.models.county import County, Department
from app.forms import ExtendedLoginForm, ExtendRegisterForm
from flask_security import hash_password
from config import Config
import uuid
# Import necessary modules and blueprints
from app.main.views import main_bp
from app.api.routes import api_bp
from app.auth.routes import auth_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)
    mail.init_app(app)
    
    # Register blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp)
    app.register_blueprint(auth_bp)
    
    # Import models and initialize Flask-Security
    user_datastore = SQLAlchemyUserDatastore(db, User, Role)
    security.init_app(app, user_datastore, register_form=ExtendRegisterForm, login_form=ExtendedLoginForm)
    
    # ******Advanced Topics*********
    # Custom user registration handler
    from flask_security.signals import user_registered

    @user_registered.connect_via(app)
    def user_registered_sighandler(sender, user, confirm_token, **extra):
        """Handle post-registration logic"""
        # Assign default 'citizen' role
        default_role = Role.query.filter_by(name='citizen').first()
        if default_role and not user.roles:
            user.roles.append(default_role)
            db.session.commit()
        print(f"New user registered: {user.email} in {user.county.name if user.county else 'No County'}")
    # ******end***********

    with app.app_context():
        db.create_all()

    # Create sample counties                                                  
        counties_data = [                                                         
            {'name': 'Bomet County', 'code': '036', 'description': 'Kipsisgis County'},                                                                       
            {'name': 'Narok County', 'code': '033', 'description': 'Maa county'},                                                                       
            {'name': 'Kericho County', 'code': '035', 'description': 'Green county'},                                                                       
        ]
        created_counties = {}                                                     
        for county_data in counties_data:                                         
            county = County.query.filter_by(code=county_data['code']).first()     
            if not county:                                                        
                county = County(**county_data)                                    
                db.session.add(county)                                            
                print(f"Created county: {county.name}")                           
            created_counties[county.code] = county                                                                                                         
        db.session.commit()

        # Create sample departments
        departments_data = [
            {'name': 'Trade & Commerce', 'code': 'TC'},
            {'name': 'Lands & Housing', 'code': 'LH'},
            {'name': 'Health Services', 'code': 'HS'},
            {'name': 'Environment & Water', 'code': 'EW'},
        ]
        for county in created_counties.values():                                  
                for dept_data in departments_data:                                    
                    dept = Department.query.filter_by(                                
                        code=dept_data['code'],                                       
                        county_id=county.id                                           
                    ).first()                                                         
                    if not dept:                                                      
                        dept = Department(                                            
                            name=dept_data['name'],                                   
                            code=dept_data['code'],                                   
                            county_id=county.id,                                      
                            description=f"{dept_data['name']} department for {county.name}"                                                                          
                        )                                                             
                        db.session.add(dept)                                         
                        print(f"Created department: {dept.name} in {county.name}")
                    db.session.commit()

        # Create roles
        roles_data = [
            {'name': 'super_admin', 'description': 'Administrator role'},
            {'name': 'staff', 'description': 'county staff with limited access'},
            {'name': 'citizen', 'description': 'citizen with basic data access'},
            {'name': 'guest', 'description': 'guest with minimal access'}
        ]
        for role_data in roles_data:
            role = Role.query.filter_by(name=role_data['name']).first()
            if not role:
                role = Role(**role_data)
                db.session.add(role)
        db.session.commit()

        # Create admin user
        admin_role = Role.query.filter_by(name='super_admin').first()
        admin_user = User.query.filter_by(email='shannel@gmail.com').first()
        if not admin_user:
            admin_user = User(
                email='shannel@gmail.com',
                password=hash_password('shannel254'),
                first_name='shannel',
                last_name='kirui',
                active=True,
                county_id=created_counties['036'].id,
                roles=[admin_role],
                fs_uniquifier=str(uuid.uuid4())
            )
            db.session.add(admin_user)
        db.session.commit()

    return app