from flask import Flask
from app.routes import UserAccountManagement

def create_app():
    app = Flask(__name__)
    UserAccountManagement(app)
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)