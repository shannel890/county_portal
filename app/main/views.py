from flask import Blueprint

main_bp = Blueprint('main_bp',__name__)

@main_bp.route('/')
def home():
    return "Welcome to the County portal!"

@main_bp.route('/about')
def about():
    return "This is the about page of the County portal."