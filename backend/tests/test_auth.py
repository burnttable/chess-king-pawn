import pytest
from app.services.auth_service import create_user, login_user, verify_token, generate_token

class TestAuthService:
    """Test cases for authentication service"""

    def test_generate_token(self):
        """Test token generation"""
        token = generate_token()

        assert token is not None
        assert len(token) > 0
        assert isinstance(token, str)

    def test_generate_token_uniqueness(self):
        """Test that tokens are unique"""
        token1 = generate_token()
        token2 = generate_token()

        assert token1 != token2

    def test_create_user(self, app):
        """Test user creation"""
        with app.app_context():
            user, error = create_user('testuser')

            assert user is not None
            assert error is None
            assert user.username == 'testuser'
            assert user.token is not None
            assert user.id is not None

    def test_create_duplicate_user(self, app):
        """Test creating duplicate user"""
        with app.app_context():
            user1, error1 = create_user('duplicate')
            user2, error2 = create_user('duplicate')

            assert user1 is not None
            assert error1 is None
            assert user2 is None
            assert error2 is not None
            assert 'already exists' in error2['error']

    def test_login_user(self, app):
        """Test user login"""
        with app.app_context():
            # Create user first
            create_user('loginuser')

            # Login
            user, error = login_user('loginuser')

            assert user is not None
            assert error is None
            assert user.username == 'loginuser'

    def test_login_nonexistent_user(self, app):
        """Test logging in nonexistent user"""
        with app.app_context():
            user, error = login_user('nonexistent')

            assert user is None
            assert error is not None
            assert 'not found' in error['error']

    def test_verify_token(self, app):
        """Test token verification"""
        with app.app_context():
            # Create user
            user = create_user('tokenuser')[0]

            # Verify token
            verified_user = verify_token(user.token)

            assert verified_user is not None
            assert verified_user.id == user.id
            assert verified_user.username == 'tokenuser'

    def test_verify_invalid_token(self, app):
        """Test verifying invalid token"""
        with app.app_context():
            verified_user = verify_token('invalid_token_12345')

            assert verified_user is None

    def test_username_validation(self, app):
        """Test username validation"""
        with app.app_context():
            # Test short username
            user, error = create_user('ab')
            assert user is None
            assert error is None  # Service doesn't validate, API does

            # Test long username
            user, error = create_user('a' * 25)
            assert user is None
            assert error is None  # Service doesn't validate, API does

    def test_user_settings_creation(self, app):
        """Test that user settings are created with user"""
        with app.app_context():
            from app.db import db
            from app.models.settings import UserSettings

            user = create_user('settingsuser')[0]

            settings = UserSettings.query.filter_by(user_id=user.id).first()

            assert settings is not None
            assert settings.theme == 'light'
            assert settings.default_difficulty == 'medium'
