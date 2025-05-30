from flask import Blueprint

api_bp = Blueprint('api_bp',__name__,url_prefix='/api')

@api_bp.route('/users', methods=['GET'])
def user_list():
    return [{"name": "Mark","email": "mark@gmail.com"}]

