from flask import Blueprint
from flask_security import login_required ,roles_required

main_bp = Blueprint('main_bp',__name__)

@main_bp.route('/')
@login_required
def home():
    return "Welcome to the County portal "


@main_bp.route('/about')
def about():
    return "This is the about page of the County portal."

@main_bp.route('/dashboard')
@roles_required('super_admin')
def dashboard():
    return "This dashboard is accessible to admins only"