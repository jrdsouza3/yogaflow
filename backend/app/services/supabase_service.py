from supabase import create_client, Client
import os
from typing import Optional, Dict, Any
from ..models.user import User

class SupabaseService:
    """Service for interacting with Supabase database"""
    
    def __init__(self):
        self.supabase_url = os.getenv('SUPABASE_URL')
        self.supabase_key = os.getenv('SUPABASE_ANON_KEY')
        
        if not self.supabase_url or not self.supabase_key:
            print("⚠️  WARNING: Supabase URL and Key not set. Auth features will not work.")
            self.client = None
        else:
            self.client: Client = create_client(self.supabase_url, self.supabase_key)
    
    def create_user(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new user in the database"""
        if not self.client:
            return {
                'success': False,
                'message': 'Supabase not configured',
                'error': 'Database connection not available'
            }
        
        try:
            # Insert user data into the users table
            result = self.client.table('users').insert(user_data).execute()
            
            if result.data:
                return {
                    'success': True,
                    'user': result.data[0],
                    'message': 'User created successfully'
                }
            else:
                return {
                    'success': False,
                    'message': 'Failed to create user',
                    'error': 'No data returned from insert'
                }
        except Exception as e:
            return {
                'success': False,
                'message': 'Error creating user',
                'error': str(e)
            }
    
    def get_user_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """Get user by email address"""
        if not self.client:
            return None
        
        try:
            result = self.client.table('users').select('*').eq('email', email).execute()
            
            if result.data:
                return result.data[0]
            return None
        except Exception as e:
            print(f"Error getting user by email: {e}")
            return None
    
    def get_user_by_id(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get user by ID"""
        if not self.client:
            return None
        
        try:
            result = self.client.table('users').select('*').eq('id', user_id).execute()
            
            if result.data:
                return result.data[0]
            return None
        except Exception as e:
            print(f"Error getting user by ID: {e}")
            return None
    
    def update_user(self, user_id: str, update_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update user information"""
        if not self.client:
            return {
                'success': False,
                'message': 'Supabase not configured',
                'error': 'Database connection not available'
            }
        
        try:
            result = self.client.table('users').update(update_data).eq('id', user_id).execute()
            
            if result.data:
                return {
                    'success': True,
                    'user': result.data[0],
                    'message': 'User updated successfully'
                }
            else:
                return {
                    'success': False,
                    'message': 'Failed to update user'
                }
        except Exception as e:
            return {
                'success': False,
                'message': 'Error updating user',
                'error': str(e)
            }
    
    def verify_password(self, password: str, stored_hash: str) -> bool:
        """Verify a password against its stored hash"""
        import hashlib
        try:
            salt, stored_password_hash = stored_hash.split(':')
            password_hash = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000)
            return password_hash.hex() == stored_password_hash
        except:
            return False
