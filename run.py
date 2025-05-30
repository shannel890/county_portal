from app import create_app
from app.extension import db

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)