#!/usr/bin/env python3
"""
StudentHub Backend - Minimal Test Server
This is a simplified version for testing without full dependencies
"""

import os
import sys
from pathlib import Path

# Ensure we can import from backend
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

print("=" * 60)
print("StudentHub Backend - Startup Test")
print("=" * 60)

# Check environment
print("\n[1] Environment Check")
print(f"  - Project Root: {project_root}")
print(f"  - Python Version: {sys.version}")
print(f"  - Python Executable: {sys.executable}")

# Check required modules
print("\n[2] Module Check")
required_modules = [
    'flask',
    'flask_cors',
    'flask_jwt_extended',
    'flask_sqlalchemy',
    'sqlalchemy',
    'dotenv',
]

missing = []
for module in required_modules:
    try:
        __import__(module)
        print(f"  ✓ {module}")
    except ImportError:
        print(f"  ✗ {module} (MISSING)")
        missing.append(module)

if missing:
    print(f"\n⚠ Missing modules: {', '.join(missing)}")
    print("\nTo fix, run:")
    print("  pip install flask flask-cors flask-jwt-extended flask-sqlalchemy python-dotenv")
    sys.exit(1)

# Try to import and create app
print("\n[3] Flask App Creation")
try:
    os.environ['FLASK_ENV'] = 'development'
    os.environ['DEV_SQLITE_FALLBACK'] = 'true'
    
    from backend.app import create_app
    app = create_app()
    
    print(f"  ✓ App created: {app.name}")
    print(f"  ✓ Database: {app.config.get('SQLALCHEMY_DATABASE_URI', 'not configured')[:50]}...")
    print(f"  ✓ Debug mode: {app.debug}")
    
except Exception as e:
    print(f"  ✗ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# List routes
print("\n[4] Registered Routes")
try:
    routes = []
    for rule in app.url_map.iter_rules():
        if rule.endpoint != 'static':
            routes.append(f"  {rule.rule:40} -> {rule.endpoint}")
    
    if routes:
        for route in sorted(routes)[:20]:
            print(route)
        if len(routes) > 20:
            print(f"  ... and {len(routes) - 20} more routes")
    else:
        print("  No routes registered")
        
except Exception as e:
    print(f"  ✗ Error listing routes: {e}")

# Try to start server
print("\n[5] Server Startup Test")
try:
    print("  Starting development server on http://localhost:5001...")
    print("  (Press Ctrl+C to stop)")
    print("\n" + "=" * 60)
    app.run(host='127.0.0.1', port=5001, debug=True, use_reloader=False)
    
except KeyboardInterrupt:
    print("\n\n✓ Server stopped by user")
except Exception as e:
    print(f"  ✗ Server error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
