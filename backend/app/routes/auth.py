from flask import Blueprint, request, jsonify
from ..services.supabase_service import SupabaseService
from ..services.jwt_service import JWTService
from ..models.user import User
import hashlib
import secrets
from datetime import datetime

auth_bp = Blueprint('auth', __name__)

def validate_signup_data(data):
    """Validate signup form data"""
    required_fields = ['email', 'password', 'firstName', 'lastName']
    errors = []
    
    # Check required fields
    for field in required_fields:
        if not data.get(field):
            errors.append(f"{field} is required")
    
    # Validate email format
    email = data.get('email', '')
    if email and '@' not in email:
        errors.append("Invalid email format")
    
    # Validate password length
    password = data.get('password', '')
    if password and len(password) < 6:
        errors.append("Password must be at least 6 characters long")
    
    return errors

def hash_password(password: str) -> str:
    """Simple password hashing (you might want to use bcrypt in production)"""
    salt = secrets.token_hex(16)
    password_hash = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000)
    return f"{salt}:{password_hash.hex()}"

@auth_bp.route('/auth/signup', methods=['POST'])
def signup():
    """User signup endpoint"""
    try:
        # Get request data
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'message': 'No data provided',
                'errors': ['Request body is required']
            }), 400
        
        # Validate input data
        errors = validate_signup_data(data)
        if errors:
            return jsonify({
                'success': False,
                'message': 'Validation failed',
                'errors': errors
            }), 400
        
        # Initialize Supabase service
        supabase_service = SupabaseService()
        
        # Check if user already exists
        existing_user = supabase_service.get_user_by_email(data['email'])
        if existing_user:
            return jsonify({
                'success': False,
                'message': 'User already exists',
                'errors': ['Email address is already registered']
            }), 409
        
        # Hash password
        hashed_password = hash_password(data['password'])
        
        # Prepare user data for database
        user_data = {
            'email': data['email'].lower().strip(),
            'first_name': data['firstName'].strip(),
            'last_name': data['lastName'].strip(),
            'password_hash': hashed_password,
            'created_at': datetime.utcnow().isoformat(),
            'updated_at': datetime.utcnow().isoformat(),
            'is_active': True
        }
        
        # Create user in database
        result = supabase_service.create_user(user_data)
        
        if result['success']:
            # Remove password hash from response
            user_response = result['user'].copy()
            user_response.pop('password_hash', None)
            
            return jsonify({
                'success': True,
                'message': 'User created successfully',
                'user': user_response
            }), 201
        else:
            return jsonify({
                'success': False,
                'message': 'Failed to create user',
                'errors': [result.get('error', 'Unknown error')]
            }), 500
            
    except Exception as e:
            return jsonify({
                'success': False,
                'message': 'Internal server error',
                'errors': [str(e)]
            }), 500

@auth_bp.route('/auth/login', methods=['POST'])
def login():
    """User login endpoint"""
    try:
        # Get request data
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'message': 'No data provided',
                'errors': ['Request body is required']
            }), 400
        
        # Validate required fields
        if not data.get('email') or not data.get('password'):
            return jsonify({
                'success': False,
                'message': 'Validation failed',
                'errors': ['Email and password are required']
            }), 400
        
        # Initialize services
        supabase_service = SupabaseService()
        jwt_service = JWTService()
        
        # Get user from database
        user_data = supabase_service.get_user_by_email(data['email'])
        
        if not user_data:
            return jsonify({
                'success': False,
                'message': 'Invalid credentials',
                'errors': ['Email or password is incorrect']
            }), 401
        
        # Verify password
        if not supabase_service.verify_password(data['password'], user_data['password_hash']):
            return jsonify({
                'success': False,
                'message': 'Invalid credentials',
                'errors': ['Email or password is incorrect']
            }), 401
        
        # Check if user is active
        if not user_data.get('is_active', True):
            return jsonify({
                'success': False,
                'message': 'Account deactivated',
                'errors': ['Your account has been deactivated']
            }), 403
        
        # Create JWT token
        access_token = jwt_service.create_access_token(user_data)
        
        # Prepare user response (remove sensitive data)
        user_response = {
            'id': user_data['id'],
            'email': user_data['email'],
            'first_name': user_data['first_name'],
            'last_name': user_data['last_name'],
            'created_at': user_data['created_at']
        }
        
        return jsonify({
            'success': True,
            'message': 'Login successful',
            'user': user_response,
            'access_token': access_token,
            'token_type': 'Bearer'
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Internal server error',
            'errors': [str(e)]
        }), 500

@auth_bp.route('/auth/test', methods=['GET'])
def auth_test():
    """Test endpoint for auth routes"""
    return jsonify({
        'message': 'Auth endpoints are working! 🔐',
        'status': 'success',
        'endpoint': '/api/auth/test',
        'available_endpoints': {
            'signup': 'POST /api/auth/signup',
            'login': 'POST /api/auth/login'
        }
    })
