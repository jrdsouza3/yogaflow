#!/usr/bin/env python3
"""
YogaFlow Backend Application Entry Point
"""

import os
from app import create_app

# Create the Flask application
app = create_app()

if __name__ == '__main__':
    # Get configuration from environment variables
    host = os.getenv('FLASK_HOST', '0.0.0.0')
    port = int(os.getenv('FLASK_PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    
    print(f"🧘‍♀️ Starting YogaFlow Backend on http://{host}:{port}")
    print(f"📊 Debug mode: {debug}")
    print(f"🔗 API endpoints:")
    print(f"   - Flow test: http://{host}:{port}/api/flow/test")
    print(f"   - Auth test: http://{host}:{port}/api/auth/test")
    print(f"   - Signup: POST http://{host}:{port}/api/auth/signup")
    print(f"   - Login: POST http://{host}:{port}/api/auth/login")
    
    app.run(host=host, port=port, debug=debug)
