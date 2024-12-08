from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from .models import UserModel
from .config import Config
from flask_jwt_extended import JWTManager
from bson import ObjectId

user_routes = Blueprint('user_routes', __name__)

class UserAccountManagement:
    def __init__(self, app):
        self.user_model = UserModel(Config)
        
        # JWT Setup
        app.config['JWT_SECRET_KEY'] = Config.JWT_SECRET_KEY
        self.jwt = JWTManager(app)
        
        # Register routes
        self._register_routes(app)
    
    def _register_routes(self, app):
        @app.route('/api/users/register', methods=['POST'])
        def register():
            data = request.get_json()
            try:
                result = self.user_model.create_user(
                    data['username'], 
                    data['email'], 
                    data['password']
                )
                return jsonify({
                    'message': 'User created successfully', 
                    'user_id': str(result.inserted_id)
                }), 201
            except ValueError as e:
                return jsonify({'error': str(e)}), 400
        
        @app.route('/api/users/login', methods=['POST'])
        def login():
            data = request.get_json()
            try:
                user = self.user_model.authenticate_user(
                    data['identifier'], 
                    data['password']
                )
                
                # Generate JWT Token
                access_token = create_access_token(identity=str(user['_id']))
                return jsonify({
                    'access_token': access_token,
                    'username': user['username']
                }), 200
            except ValueError as e:
                return jsonify({'error': str(e)}), 401
        
        @app.route('/api/users/profile', methods=['GET'])
        @jwt_required()
        def get_profile():
            current_user_id = get_jwt_identity()
            user = self.user_model.users_collection.find_one(
                {'_id': ObjectId(current_user_id)}, 
                {'password': 0}
            )
            
            if not user:
                return jsonify({'error': 'User not found'}), 404
            
            user['_id'] = str(user['_id'])
            return jsonify(user), 200