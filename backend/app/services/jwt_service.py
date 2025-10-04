import jwt
import os
from datetime import datetime, timedelta
from typing import Dict, Optional

class JWTService:
    """Service for handling JWT token operations"""
    
    def __init__(self):
        self.secret_key = os.getenv('JWT_SECRET_KEY', 'your-jwt-secret-key-change-in-production')
        self.algorithm = 'HS256'
        self.access_token_expire_minutes = int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES', 60))  # 1 hour default
    
    def create_access_token(self, user_data: Dict) -> str:
        """Create a JWT access token"""
        # Set expiration time
        expire = datetime.utcnow() + timedelta(minutes=self.access_token_expire_minutes)
        
        # Create payload
        payload = {
            'user_id': user_data.get('id'),
            'email': user_data.get('email'),
            'first_name': user_data.get('first_name'),
            'last_name': user_data.get('last_name'),
            'created_at': user_data.get('created_at'),
            'exp': expire,  # Expiration time
            'iat': datetime.utcnow(),  # Issued at
            'type': 'access'
        }
        
        # Generate token
        token = jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
        return token
    
    def verify_token(self, token: str) -> Optional[Dict]:
        """Verify and decode a JWT token"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except jwt.ExpiredSignatureError:
            return None  # Token has expired
        except jwt.InvalidTokenError:
            return None  # Token is invalid
    
    def extract_user_from_token(self, token: str) -> Optional[Dict]:
        """Extract user information from a valid token"""
        payload = self.verify_token(token)
        if payload:
            return {
                'id': payload.get('user_id'),
                'email': payload.get('email'),
                'first_name': payload.get('first_name'),
                'last_name': payload.get('last_name')
            }
        return None
