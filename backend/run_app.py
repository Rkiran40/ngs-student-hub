#!/usr/bin/env python
import sys
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

print("Starting Flask...", flush=True)
from app import create_app

print("Creating app...", flush=True)
app = create_app()

print("Running app...", flush=True)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=False)
