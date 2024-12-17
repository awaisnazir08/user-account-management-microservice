from flask import Flask
from flask_cors import CORS  # Import CORS
from app.routes import UserAccountManagement

def create_app():
    app = Flask(__name__)
    CORS(app)  # Enable CORS for all routes
    UserAccountManagement(app)
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)