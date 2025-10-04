from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class User:
    """User model for database operations"""
    id: Optional[str] = None
    email: str = ""
    first_name: str = ""
    last_name: str = ""
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    is_active: bool = True
    
    def to_dict(self) -> dict:
        """Convert user to dictionary for database operations"""
        return {
            'id': self.id,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'is_active': self.is_active
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'User':
        """Create User instance from dictionary"""
        return cls(
            id=data.get('id'),
            email=data.get('email', ''),
            first_name=data.get('first_name', ''),
            last_name=data.get('last_name', ''),
            created_at=datetime.fromisoformat(data['created_at']) if data.get('created_at') else None,
            updated_at=datetime.fromisoformat(data['updated_at']) if data.get('updated_at') else None,
            is_active=data.get('is_active', True)
        )
