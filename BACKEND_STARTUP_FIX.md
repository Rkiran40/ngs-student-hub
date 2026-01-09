# StudentHub Backend - Startup Fix Guide

## Current Status

The Flask backend has the following issues:

1. **Virtual environment is out of disk space** - Cannot install pip packages
2. **Missing required Python packages** - Flask, SQLAlchemy, etc.
3. **Database configuration** - Configured for MySQL but not available locally

## Solutions

### Option 1: Clean up disk space and reinstall venv (Recommended)

```powershell
# Delete the virtual environment (it takes up space)
Remove-Item -Recurse -Force .venv

# Remove any cache
Remove-Item -Recurse -Force backend/__pycache__
Remove-Item -Recurse -Force .pytest_cache

# Create fresh virtual environment
python -m venv .venv

# Activate it
.venv\Scripts\Activate.ps1

# Install requirements
pip install -r backend/requirements.txt
```

### Option 2: Use Python system packages (if available)

If Flask is installed globally, run directly:

```powershell
python backend/run_test_server.py
```

### Option 3: Use Docker for isolated environment

```powershell
# Build Docker image for backend
docker build -f backend/Dockerfile -t studenthub-backend .

# Run backend in container
docker run -p 5001:5001 studenthub-backend
```

## Quick Start After Installation

Once dependencies are installed:

```powershell
# Navigate to project root
cd c:\Users\T430\Desktop\studenthub

# Run test server
python backend/run_test_server.py
```

Server will start at: **http://localhost:5001**

## Testing the Backend

Once server is running, test endpoints:

```powershell
# Test health
Invoke-WebRequest http://localhost:5001/ -Method GET

# Test auth endpoint
Invoke-WebRequest http://localhost:5001/auth/health -Method GET

# Test student endpoint
Invoke-WebRequest http://localhost:5001/student/profile -Method GET `
  -Headers @{ Authorization = "Bearer your-token" }
```

## Database Configuration

The backend is configured to:

1. Try connecting to MySQL at `127.0.0.1:3306`
2. Fall back to SQLite at `backend/dev_fallback.db` if MySQL unavailable

For local development with SQLite:
- No database setup required
- All data stored in `backend/dev_fallback.db`
- Will work for testing

For production with MySQL:
- Set `DATABASE_URL` environment variable
- Ensure MySQL server is running
- Create database and user per deployment guide

## File: config.py Changes

Updated settings:
```python
DEV_SQLITE_FALLBACK = True       # Enable SQLite fallback
AUTO_CREATE_DB = True             # Auto-create DB schema
FLASK_ENV = development           # Default environment
```

## Troubleshooting

### "ModuleNotFoundError: No module named 'flask'"
→ Install dependencies: `pip install -r backend/requirements.txt`

### "No space left on device"
→ Delete and recreate venv (Option 1 above)

### "MySQL connection refused"
→ This is OK - will fall back to SQLite. Ignore the warning.

### Port 5001 already in use
→ Change port in run_test_server.py or kill process on that port:
```powershell
Get-Process -Name python | Stop-Process -Force
```

## Next Steps

1. ✅ Fix disk space issue
2. ✅ Reinstall Python dependencies
3. ✅ Start Flask server
4. ✅ Test endpoints
5. ✅ Then ready for Hostinger deployment

## Need Help?

Check these files:
- `backend/app.py` - Flask app factory
- `backend/config.py` - Configuration
- `backend/routes/` - API endpoints
- `DEPLOYMENT_HOSTINGER.md` - Production deployment guide
