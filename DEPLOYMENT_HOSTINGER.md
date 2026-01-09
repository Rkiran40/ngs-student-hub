# StudentHub Deployment Guide - Hostinger VPS

## Overview
This guide provides step-by-step instructions for deploying StudentHub to Hostinger VPS with the domain `studenthub.nuhvin.com`.

**Architecture:**
- Frontend: React + Vite (served via Nginx)
- Backend: Flask + Gunicorn (reverse proxied via Nginx)
- Database: MySQL 8.0
- OS: Ubuntu 20.04+ or CentOS 8+
- Domain: studenthub.nuhvin.com

---

## Prerequisites

### 1. Hostinger VPS Access
- SSH access to your VPS
- Root or sudo privileges
- Public IP address assigned

### 2. Domain Setup
- Point `studenthub.nuhvin.com` to your VPS public IP
- Update DNS A record to your VPS IP
- Verify DNS propagation (can take up to 24 hours)

### 3. System Requirements
- Ubuntu 20.04+ or equivalent
- 2+ CPU cores
- 4+ GB RAM
- 20+ GB disk space
- Python 3.10+

---

## Deployment Steps

### Step 1: SSH into VPS

```bash
ssh root@your-vps-ip
# or
ssh your_username@your-vps-ip
```

### Step 2: Update System & Install Dependencies

```bash
# Update package manager
sudo apt update && sudo apt upgrade -y

# Install essential packages
sudo apt install -y \
    curl \
    wget \
    git \
    build-essential \
    python3 \
    python3-dev \
    python3-pip \
    python3-venv \
    mysql-server \
    nginx \
    supervisor \
    certbot \
    python3-certbot-nginx

# Verify Python version
python3 --version  # Should be 3.10+
```

### Step 3: Clone Repository

```bash
# Create app directory
sudo mkdir -p /var/www/studenthub
cd /var/www/studenthub

# Clone your repository
sudo git clone https://github.com/your-org/studenthub.git .
# Or if private:
sudo git clone https://your-token@github.com/your-org/studenthub.git .

# Set proper permissions
sudo chown -R $USER:$USER /var/www/studenthub
```

### Step 4: Setup Python Virtual Environment

```bash
cd /var/www/studenthub/backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install backend dependencies
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt

# Verify installation
python3 -c "import flask; print(flask.__version__)"
```

### Step 5: Configure Environment Variables

```bash
# Create production .env file
sudo cp /var/www/studenthub/backend/deploy/systemd/studenthub.env.example \
    /etc/studenthub.env

# Edit with production values
sudo nano /etc/studenthub.env
```

**Update these values in `/etc/studenthub.env`:**

```env
# Flask / App
FLASK_ENV=production
SECRET_KEY=your-secure-random-key-here
JWT_SECRET_KEY=your-jwt-secret-key-here

# Database (MySQL)
DATABASE_URL=mysql+pymysql://studenthub_user:db_password@localhost:3306/studenthub_db?charset=utf8mb4

# Uploads and Mail
UPLOAD_FOLDER=/var/lib/studenthub/uploads
MAIL_OUTPUT_DIR=/var/lib/studenthub/sent_emails

# SMTP Configuration
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
MAIL_USE_TLS=true
MAIL_DEFAULT_SENDER=noreply@studenthub.nuhvin.com

# Frontend
FRONTEND_URL=https://studenthub.nuhvin.com

# Optional
SENTRY_DSN=
```

**Generate secure keys:**
```bash
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

Set file permissions:
```bash
sudo chmod 600 /etc/studenthub.env
sudo chown root:root /etc/studenthub.env
```

### Step 6: Setup MySQL Database

```bash
# Connect to MySQL
sudo mysql -u root

# Create database and user
CREATE DATABASE studenthub_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'studenthub_user'@'localhost' IDENTIFIED BY 'secure_password_here';
GRANT ALL PRIVILEGES ON studenthub_db.* TO 'studenthub_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;

# Test connection
mysql -u studenthub_user -p -h localhost studenthub_db -e "SELECT 1;"
```

### Step 7: Run Database Migrations

```bash
cd /var/www/studenthub/backend
source venv/bin/activate

# Run Alembic migrations
alembic upgrade head

# Verify database schema
python3 -c "from db import db; from app import create_app; app = create_app(); print('DB connection OK')"
```

### Step 8: Create Application Directories

```bash
# Create necessary directories
sudo mkdir -p /var/lib/studenthub/uploads
sudo mkdir -p /var/lib/studenthub/sent_emails
sudo mkdir -p /var/log/studenthub

# Set permissions
sudo chown -R nobody:nogroup /var/lib/studenthub
sudo chmod 755 /var/lib/studenthub/uploads
sudo chmod 755 /var/lib/studenthub/sent_emails
sudo chown -R nobody:nogroup /var/log/studenthub
```

### Step 9: Setup Systemd Service

```bash
# Copy and enable service file
sudo cp /var/www/studenthub/backend/deploy/systemd/studenthub.service.example \
    /etc/systemd/system/studenthub.service

# Edit the service file
sudo nano /etc/systemd/system/studenthub.service
```

**Update paths in studenthub.service:**
- `User=www-data`
- `Group=www-data`
- `WorkingDirectory=/var/www/studenthub/backend`
- `EnvironmentFile=/etc/studenthub.env`
- `ExecStart=/var/www/studenthub/backend/venv/bin/gunicorn -c /var/www/studenthub/backend/gunicorn_config.py wsgi:app`

Then enable and start:
```bash
sudo systemctl daemon-reload
sudo systemctl enable studenthub.service
sudo systemctl start studenthub.service
sudo systemctl status studenthub.service
```

### Step 10: Build Frontend

```bash
cd /var/www/studenthub/frontend

# Install Node dependencies
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install -y nodejs

# Install and build
npm ci
npm run build

# Verify build output
ls -la dist/
```

### Step 11: Configure Nginx

Create `/etc/nginx/sites-available/studenthub.nuhvin.com`:

```bash
sudo nano /etc/nginx/sites-available/studenthub.nuhvin.com
```

**Content:**

```nginx
upstream studenthub_backend {
    server 127.0.0.1:8000;
    keepalive 32;
}

server {
    listen 80;
    server_name studenthub.nuhvin.com www.studenthub.nuhvin.com;

    # Redirect HTTP to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name studenthub.nuhvin.com www.studenthub.nuhvin.com;

    # SSL Certificates (will be created by Certbot)
    ssl_certificate /etc/letsencrypt/live/studenthub.nuhvin.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/studenthub.nuhvin.com/privkey.pem;

    # SSL Configuration
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;
    ssl_session_timeout 1d;
    ssl_session_cache shared:SSL:50m;
    ssl_stapling on;
    ssl_stapling_verify on;

    # Security Headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;

    # Root directory for frontend
    root /var/www/studenthub/frontend/dist;
    index index.html;

    # Gzip compression
    gzip on;
    gzip_types text/plain text/css text/xml text/javascript application/x-javascript application/xml+rss;
    gzip_disable "msie6";

    # Frontend SPA routing
    location / {
        try_files $uri $uri/ /index.html;
        expires 1d;
    }

    # Static assets with long caching
    location ~* \.(js|css|png|jpg|jpeg|gif|svg|ico|woff|woff2|ttf|eot)$ {
        expires 365d;
        add_header Cache-Control "public, immutable";
    }

    # API proxy to Flask backend
    location /api/ {
        proxy_pass http://studenthub_backend/;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
    }

    # Auth endpoints
    location /auth/ {
        proxy_pass http://studenthub_backend/auth/;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Admin endpoints
    location /admin/ {
        proxy_pass http://studenthub_backend/admin/;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Student endpoints
    location /student/ {
        proxy_pass http://studenthub_backend/student/;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Uploads directory
    location /uploads/ {
        alias /var/lib/studenthub/uploads/;
        expires 30d;
    }

    # Deny access to hidden files
    location ~ /\. {
        deny all;
    }

    # Logs
    access_log /var/log/nginx/studenthub_access.log combined;
    error_log /var/log/nginx/studenthub_error.log warn;
}
```

Enable the site:
```bash
sudo ln -s /etc/nginx/sites-available/studenthub.nuhvin.com \
    /etc/nginx/sites-enabled/studenthub.nuhvin.com

# Test Nginx configuration
sudo nginx -t

# Reload Nginx
sudo systemctl reload nginx
```

### Step 12: Setup SSL Certificate (Let's Encrypt)

```bash
# Generate SSL certificate
sudo certbot certonly --nginx -d studenthub.nuhvin.com -d www.studenthub.nuhvin.com

# Auto-renewal setup
sudo systemctl enable certbot.timer
sudo systemctl start certbot.timer

# Test auto-renewal
sudo certbot renew --dry-run
```

### Step 13: Firewall Configuration

```bash
# Enable UFW (if not already enabled)
sudo ufw enable

# Allow SSH
sudo ufw allow 22/tcp

# Allow HTTP and HTTPS
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# Deny everything else by default
sudo ufw default deny incoming
sudo ufw default allow outgoing

# Status
sudo ufw status
```

### Step 14: Verify Deployment

```bash
# Check backend service
sudo systemctl status studenthub.service

# Check Nginx
sudo systemctl status nginx

# Check logs
tail -f /var/log/studenthub/studenthub.log
tail -f /var/log/nginx/studenthub_error.log

# Test API endpoint
curl https://studenthub.nuhvin.com/auth/health

# Test frontend
curl https://studenthub.nuhvin.com/
```

---

## Post-Deployment

### 1. Monitor Logs
```bash
# Backend logs
sudo journalctl -u studenthub.service -f

# Nginx access logs
sudo tail -f /var/log/nginx/studenthub_access.log

# Nginx error logs
sudo tail -f /var/log/nginx/studenthub_error.log
```

### 2. Database Backups
```bash
# Create backup directory
sudo mkdir -p /backups/studenthub
sudo chmod 700 /backups/studenthub

# Backup script
#!/bin/bash
BACKUP_FILE="/backups/studenthub/studenthub_$(date +%Y%m%d_%H%M%S).sql"
mysqldump -u studenthub_user -p -h localhost studenthub_db > $BACKUP_FILE
gzip $BACKUP_FILE

# Add to crontab for daily backups
# 0 2 * * * /path/to/backup_script.sh
```

### 3. Update Application

```bash
cd /var/www/studenthub
git pull origin main

# Backend updates
cd backend
source venv/bin/activate
pip install -r requirements.txt
alembic upgrade head
sudo systemctl restart studenthub.service

# Frontend updates
cd ../frontend
npm ci
npm run build
sudo systemctl reload nginx
```

### 4. Security Hardening

- [ ] Change MySQL root password
- [ ] Disable root SSH login
- [ ] Setup SSH key authentication
- [ ] Enable fail2ban for brute-force protection
- [ ] Setup monitoring (uptimerobot, Sentry)
- [ ] Enable database encryption at rest
- [ ] Regular security updates: `sudo apt update && sudo apt upgrade`

### 5. Email Configuration

For production email delivery:
- Use transactional email service (SendGrid, Mailgun, AWS SES)
- Or configure SMTP with your email provider
- Update MAIL_SERVER and credentials in `/etc/studenthub.env`
- Restart service: `sudo systemctl restart studenthub.service`

---

## Troubleshooting

### Backend not starting
```bash
sudo systemctl status studenthub.service
sudo journalctl -u studenthub.service -n 50
```

### Database connection error
```bash
mysql -u studenthub_user -p -h localhost studenthub_db
# Check DATABASE_URL in /etc/studenthub.env
```

### Frontend not loading
```bash
# Verify build exists
ls -la /var/www/studenthub/frontend/dist/

# Check Nginx config
sudo nginx -t

# Check logs
tail -f /var/log/nginx/studenthub_error.log
```

### SSL certificate issues
```bash
# Check certificate status
sudo certbot certificates

# Renew manually
sudo certbot renew --force-renewal
```

---

## Support & Maintenance

- Monitor: `https://studenthub.nuhvin.com/`
- Backend health: Check systemd service status
- Database: Regular backups and monitoring
- SSL: Auto-renewal via certbot
- Updates: Monthly security patches

For issues, check logs in:
- `/var/log/studenthub/`
- `/var/log/nginx/`
- `sudo journalctl -u studenthub.service`
