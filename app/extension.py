from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_security import Security
from flask_mail import Mail

db = SQLAlchemy()
migrate = Migrate()
security = Security()
mail = Mail()