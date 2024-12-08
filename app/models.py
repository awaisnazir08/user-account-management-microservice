from pymongo import MongoClient
from flask_bcrypt import Bcrypt
from datetime import datetime
import re

class UserModel:
    def __init__(self, config):
        # Extract the database name from the connection string
        import urllib.parse
        from pymongo.uri_parser import parse_uri

        # Parse the connection URI
        parsed_uri = parse_uri(config.MONGO_URI)
        database_name = parsed_uri['database'] or 'user_management'

        # Create client and specify database
        self.client = MongoClient(config.MONGO_URI)
        self.db = self.client[database_name]
        self.users_collection = self.db['users']
        self.bcrypt = Bcrypt()
        
        # Create unique indexes
        self.users_collection.create_index('email', unique=True)
        self.users_collection.create_index('username', unique=True)
    
    def create_user(self, username, email, password):
        # Validate input
        if not self._validate_username(username):
            raise ValueError("Invalid username format")
        
        if not self._validate_email(email):
            raise ValueError("Invalid email format")
        
        # Check if user already exists
        if self.users_collection.find_one({'$or': [
            {'username': username},
            {'email': email}
        ]}):
            raise ValueError("Username or email already exists")
        
        # Hash password
        hashed_password = self.bcrypt.generate_password_hash(password).decode('utf-8')
        
        user_data = {
            'username': username,
            'email': email,
            'password': hashed_password,
            'created_at': datetime.now(),
            'last_login': None,
            'is_active': True
        }
        
        return self.users_collection.insert_one(user_data)
    
    def authenticate_user(self, identifier, password):
        # Allow login with username or email
        user = self.users_collection.find_one({
            '$or': [
                {'username': identifier},
                {'email': identifier}
            ]
        })
        
        if not user:
            raise ValueError("User not found")
        
        # Verify password
        if self.bcrypt.check_password_hash(user['password'], password):
            # Update last login
            self.users_collection.update_one(
                {'_id': user['_id']},
                {'$set': {'last_login': datetime.utcnow()}}
            )
            return user
        
        raise ValueError("Invalid credentials")
    
    def _validate_username(self, username):
        # Username must be 3-20 characters, alphanumeric and underscore
        return re.match(r'^[a-zA-Z0-9_]{3,20}$', username) is not None
    
    def _validate_email(self, email):
        # Basic email validation
        return re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email) is not None