from flask import Blueprint, request, jsonify
from ..db import db
from ..models.user import User
from ..models.settings import UserSettings
from ..services.auth_service import verify_token

settings_bp = Blueprint('settings', __name__)

def get_user_from_token():
    """Get user from Authorization header token"""
    auth_header = request.headers.get('Authorization')

    if not auth_header or not auth_header.startswith('Bearer '):
        return None

    token = auth_header.split(' ')[1]
    return verify_token(token)

@settings_bp.route('/', methods=['GET'])
def get_settings():
    """Get user settings"""
    user = get_user_from_token()

    if not user:
        return jsonify({'error': 'Invalid or missing token'}), 401

    settings = UserSettings.query.filter_by(user_id=user.id).first()

    if not settings:
        return jsonify({'error': 'Settings not found'}), 404

    return jsonify(settings.to_dict()), 200

@settings_bp.route('/', methods=['PUT'])
def update_settings():
    """Update user settings"""
    user = get_user_from_token()

    if not user:
        return jsonify({'error': 'Invalid or missing token'}), 401

    data = request.get_json()

    settings = UserSettings.query.filter_by(user_id=user.id).first()

    if not settings:
        return jsonify({'error': 'Settings not found'}), 404

    # Update settings if provided
    if 'theme' in data:
        if data['theme'] not in ['light', 'dark']:
            return jsonify({'error': 'Invalid theme. Must be light or dark'}), 400
        settings.theme = data['theme']

    if 'default_difficulty' in data:
        if data['default_difficulty'] not in ['easy', 'medium', 'hard']:
            return jsonify({'error': 'Invalid difficulty. Must be easy, medium, or hard'}), 400
        settings.default_difficulty = data['default_difficulty']

    if 'timer_enabled' in data:
        settings.timer_enabled = bool(data['timer_enabled'])

    if 'default_timer_duration' in data:
        duration = int(data['default_timer_duration'])
        if duration < 60 or duration > 3600:
            return jsonify({'error': 'Timer duration must be between 60 and 3600 seconds'}), 400
        settings.default_timer_duration = duration

    db.session.commit()

    return jsonify({
        'message': 'Settings updated successfully',
        'settings': settings.to_dict()
    }), 200
