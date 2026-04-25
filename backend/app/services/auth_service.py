import secrets
from ..db import db
from ..models.user import User
from ..models.settings import UserSettings

def generate_token():
    """Generate a secure random token for authentication"""
    return secrets.token_urlsafe(32)

def create_user(username):
    """Create a new user with generated token and default settings"""
    # Check if username already exists
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return None, {'error': 'Username already exists'}

    # Generate unique token
    token = generate_token()

    # Create user
    user = User(username=username, token=token)
    db.session.add(user)
    db.session.flush()

    # Create default settings for user
    settings = UserSettings(user_id=user.id)
    db.session.add(settings)

    db.session.commit()

    return user, None

def login_user(username):
    """Login user (simplified - no password, just username)"""
    user = User.query.filter_by(username=username).first()
    if not user:
        return None, {'error': 'User not found'}

    return user, None

def verify_token(token):
    """Verify user token and return user if valid"""
    user = User.query.filter_by(token=token).first()
    return user
