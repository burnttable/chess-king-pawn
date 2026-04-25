"""
WSGI configuration for production deployment
"""
import os
from app import create_app

# Get environment from environment variable
env = os.getenv('FLASK_ENV', 'production')

# Create Flask application
app = create_app(env)

if __name__ == '__main__':
    # For development only
    app.run(debug=False, host='0.0.0.0', port=5000)
