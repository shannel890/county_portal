from app.extension import db
from flask_security import UserMixin, RoleMixin
import uuid

#many to many relationship between users and roles
#This is an association table that links users and roles
roles_users = db.Table('roles_users',
                        db.Column('user_id',db.Integer, db.ForeignKey('users.id')),
                        db.Column('role_id', db.Integer, db.ForeignKey('roles.id'))
                )
class Role(db.Model, RoleMixin):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(255), nullable=True)

class User(db.Model,UserMixin):
    __tablename__ = 'users'
    #Basic identity fields that come with Flask-security

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)

    #profile information
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    phone = db.Column(db.String(20))

    #account status fields
    active = db.Column(db.Boolean(), default=True)
    confirmed_at = db.Column(db.DateTime())
    created_at = db.Column(db.DateTime(), nullable=False, default=db.func.current_timestamp())


    # Flask security required field for tokens,session,password management
    fs_uniquifier = db.Column(db.String(64), unique=True, nullable=True, default=lambda: str(uuid.uuid4()))
    

    #county and department relationship 
    county_id = db.Column(db.Integer,db.ForeignKey('counties.id'))
    department_id = db.Column(db.Integer,db.ForeignKey('departments.id'))
    #Tracking fields
    last_login_at = db.Column(db.DateTime())
    current_login_at = db.Column(db.DateTime())
    last_login_ip = db.Column(db.String(45))
    current_login_ip = db.Column(db.String(45))
    login_count = db.Column(db.Integer, default=0)

    #relationships
    roles = db.relationship('Role', secondary=roles_users, backref=db.backref('users', lazy='dynamic'))

    def __repr__(self):
        return f"user {self.email} {self.roles}"
    
    def full_name(self):
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.email.split('@')[0]
    
    def has_role(self, role_name):
        return any(role.name == role_name for role in self.roles)
    
    def __repr__(self):
        return f'role:{self.name}'