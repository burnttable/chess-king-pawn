from flask import Blueprint, request, jsonify
from ..services.auth_service import create_user, login_user

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    """Register a new user"""
    data = request.get_json()

    if not data or 'username' not in data:
        return jsonify({'error': 'Username is required'}), 400

    username = data['username'].strip()

    if len(username) < 3 or len(username) > 20:
        return jsonify({'error': 'Username must be between 3 and 20 characters'}), 400

    user, error = create_user(username)

    if error:
        return jsonify(error), 400

    return jsonify({
        'message': 'User created successfully',
        'user': user.to_dict()
    }), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    """Login with username (simplified - no password)"""
    data = request.get_json()

    if not data or 'username' not in data:
        return jsonify({'error': 'Username is required'}), 400

    username = data['username'].strip()

    user, error = login_user(username)

    if error:
        return jsonify(error), 404

    return jsonify({
        'message': 'Login successful',
        'user': user.to_dict()
    }), 200
