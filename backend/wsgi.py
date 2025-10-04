#!/usr/bin/env python3
"""
WSGI entry point for production deployment
"""

import os
import sys
from app import create_app

try:
    # Create the Flask application
    app = create_app(os.getenv('FLASK_ENV', 'production'))
    print("✅ Flask app created successfully")
except Exception as e:
    print(f"❌ Error creating Flask app: {e}")
    sys.exit(1)

if __name__ == '__main__':
    # This is for development only
    port = int(os.getenv('PORT', 5000))
    print(f"🚀 Starting Flask app on port {port}")
    app.run(host='0.0.0.0', port=port)
