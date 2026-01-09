# StudentHub Hostinger VPS Deployment Checklist
## Domain: studenthub.nuhvin.com

---

## PRE-DEPLOYMENT

- [ ] **DNS Setup**
  - [ ] Point `studenthub.nuhvin.com` A record to VPS IP
  - [ ] Point `www.studenthub.nuhvin.com` CNAME to `studenthub.nuhvin.com`
  - [ ] Verify DNS propagation (ping or nslookup)

- [ ] **VPS Preparation**
  - [ ] SSH access verified
  - [ ] Root or sudo privileges confirmed
  - [ ] Hostinger firewall settings reviewed

- [ ] **Credentials & Keys**
  - [ ] Generated `SECRET_KEY` (python3 -c "import secrets; print(secrets.token_urlsafe(32))")
  - [ ] Generated `JWT_SECRET_KEY`
  - [ ] MySQL password created
  - [ ] SMTP credentials obtained (Gmail, SendGrid, etc.)

---

## SYSTEM SETUP

- [ ] **OS Updates**
  - [ ] `sudo apt update && sudo apt upgrade -y`
  - [ ] All essential packages installed

- [ ] **Dependencies Installed**
  - [ ] Python 3.10+ (`python3 --version`)
  - [ ] MySQL Server (`mysql --version`)
  - [ ] Nginx (`nginx -v`)
  - [ ] Node.js 18+ (`node --version`)
  - [ ] Git (`git --version`)

- [ ] **Directory Structure**
  - [ ] `/var/www/studenthub` created
  - [ ] Repository cloned
  - [ ] Proper ownership set (not root)

---

## BACKEND SETUP

- [ ] **Python Environment**
  - [ ] Virtual environment created (`venv/`)
  - [ ] `pip install -r requirements.txt` successful
  - [ ] Gunicorn installed

- [ ] **Database**
  - [ ] MySQL user `studenthub_user` created
  - [ ] Database `studenthub_db` created with UTF8MB4
  - [ ] Permissions granted to user
  - [ ] Connection tested with credentials
  - [ ] Alembic migrations run (`alembic upgrade head`)
  - [ ] Tables verified in database

- [ ] **Environment File**
  - [ ] `/etc/studenthub.env` created
  - [ ] All required variables set:
    - [ ] FLASK_ENV=production
    - [ ] SECRET_KEY (generated & unique)
    - [ ] JWT_SECRET_KEY (generated & unique)
    - [ ] DATABASE_URL (correct MySQL credentials)
    - [ ] MAIL_SERVER, MAIL_PORT, MAIL_USERNAME, MAIL_PASSWORD
    - [ ] UPLOAD_FOLDER=/var/lib/studenthub/uploads
    - [ ] MAIL_OUTPUT_DIR=/var/lib/studenthub/sent_emails
    - [ ] FRONTEND_URL=https://studenthub.nuhvin.com
  - [ ] File permissions: `sudo chmod 600 /etc/studenthub.env`
  - [ ] Owner verified: `root:root`

- [ ] **Application Directories**
  - [ ] `/var/lib/studenthub/uploads` created with proper permissions
  - [ ] `/var/lib/studenthub/sent_emails` created with proper permissions
  - [ ] `/var/log/studenthub` created with proper permissions

- [ ] **Systemd Service**
  - [ ] `/etc/systemd/system/studenthub.service` created/updated
  - [ ] Paths updated to match your setup
  - [ ] Service enabled: `sudo systemctl enable studenthub.service`
  - [ ] Service started: `sudo systemctl start studenthub.service`
  - [ ] Service status verified: `sudo systemctl status studenthub.service`
  - [ ] Logs checked: `sudo journalctl -u studenthub.service -n 20`

---

## FRONTEND SETUP

- [ ] **Build**
  - [ ] Node modules installed: `npm ci`
  - [ ] Build successful: `npm run build`
  - [ ] Build output verified: `ls /var/www/studenthub/frontend/dist/`

- [ ] **Frontend Root**
  - [ ] `/var/www/studenthub/frontend/dist` directory confirmed
  - [ ] `index.html` present in dist/

---

## NGINX SETUP

- [ ] **Configuration**
  - [ ] `/etc/nginx/sites-available/studenthub.nuhvin.com` created
  - [ ] Upstream backend IP correct: `127.0.0.1:8000`
  - [ ] Root path correct: `/var/www/studenthub/frontend/dist`
  - [ ] All proxy paths configured:
    - [ ] /auth/
    - [ ] /admin/
    - [ ] /student/
    - [ ] /api/
    - [ ] /uploads/

- [ ] **Enabling Site**
  - [ ] Symlink created to `sites-enabled/`
  - [ ] Config tested: `sudo nginx -t` (returns OK)
  - [ ] Nginx reloaded: `sudo systemctl reload nginx`
  - [ ] Nginx status verified: `sudo systemctl status nginx`

---

## SSL/TLS SETUP

- [ ] **Let's Encrypt Certificate**
  - [ ] Certbot installed
  - [ ] Certificate created: `sudo certbot certonly --nginx -d studenthub.nuhvin.com -d www.studenthub.nuhvin.com`
  - [ ] Certificate files exist:
    - [ ] `/etc/letsencrypt/live/studenthub.nuhvin.com/fullchain.pem`
    - [ ] `/etc/letsencrypt/live/studenthub.nuhvin.com/privkey.pem`

- [ ] **SSL in Nginx**
  - [ ] SSL paths updated in nginx.conf
  - [ ] HTTP to HTTPS redirect configured
  - [ ] SSL ciphers and protocols configured

- [ ] **Auto-Renewal**
  - [ ] Certbot timer enabled: `sudo systemctl enable certbot.timer`
  - [ ] Renewal tested: `sudo certbot renew --dry-run`

---

## FIREWALL SETUP

- [ ] **UFW (Ubuntu Firewall)**
  - [ ] UFW enabled: `sudo ufw enable`
  - [ ] SSH allowed: `sudo ufw allow 22/tcp`
  - [ ] HTTP allowed: `sudo ufw allow 80/tcp`
  - [ ] HTTPS allowed: `sudo ufw allow 443/tcp`
  - [ ] Default policies set:
    - [ ] Incoming: `deny`
    - [ ] Outgoing: `allow`
  - [ ] Status verified: `sudo ufw status`

---

## VERIFICATION & TESTING

- [ ] **Backend Health**
  - [ ] Service running: `sudo systemctl status studenthub.service`
  - [ ] Logs show no errors: `sudo journalctl -u studenthub.service -n 50`
  - [ ] Port 8000 listening: `sudo netstat -tlnp | grep 8000`

- [ ] **Frontend Load**
  - [ ] `https://studenthub.nuhvin.com` loads
  - [ ] Index.html served correctly
  - [ ] Browser console has no CORS errors
  - [ ] Assets load (CSS, JS, images)

- [ ] **API Endpoints**
  - [ ] `/auth/login` endpoint accessible
  - [ ] `/admin/` endpoint accessible with auth
  - [ ] `/student/` endpoint accessible with auth
  - [ ] `/uploads/` serves files correctly

- [ ] **Database Connectivity**
  - [ ] Backend can connect to MySQL
  - [ ] No "connection refused" errors in logs

- [ ] **Email Functionality**
  - [ ] SMTP credentials correct
  - [ ] Test email sends successfully
  - [ ] Email configuration working

- [ ] **SSL/HTTPS**
  - [ ] HTTPS works: `https://studenthub.nuhvin.com`
  - [ ] HTTP redirects to HTTPS
  - [ ] Certificate valid and shows green lock
  - [ ] No mixed content warnings

---

## SECURITY HARDENING

- [ ] **System Security**
  - [ ] SSH password login disabled (key-only auth)
  - [ ] Root login disabled via SSH
  - [ ] Fail2ban installed and configured (optional but recommended)
  - [ ] Automatic security updates enabled

- [ ] **Application Security**
  - [ ] Environment variables not in code
  - [ ] Database password strong
  - [ ] SECRET_KEY and JWT_SECRET_KEY unique
  - [ ] CORS configured correctly
  - [ ] Security headers in nginx:
    - [ ] HSTS
    - [ ] X-Frame-Options
    - [ ] X-Content-Type-Options
    - [ ] CSP (if applicable)

- [ ] **File Permissions**
  - [ ] `/etc/studenthub.env` is 600 (readable only by root)
  - [ ] Upload directory writable by www-data
  - [ ] Log directory writable by www-data
  - [ ] Backend source not world-readable

---

## BACKUPS & MONITORING

- [ ] **Database Backups**
  - [ ] Backup script created
  - [ ] Backup directory created: `/backups/studenthub`
  - [ ] Cron job scheduled for daily backups
  - [ ] Test backup created and verified

- [ ] **Log Monitoring**
  - [ ] Log files created:
    - [ ] `/var/log/studenthub/error.log`
    - [ ] `/var/log/studenthub/access.log`
    - [ ] `/var/log/nginx/studenthub_error.log`
    - [ ] `/var/log/nginx/studenthub_access.log`
  - [ ] Log rotation configured (logrotate)

- [ ] **Monitoring Setup** (optional)
  - [ ] Uptime monitoring (UptimeRobot, etc.)
  - [ ] Error tracking (Sentry, Rollbar, etc.)
  - [ ] Performance monitoring (optional)

---

## DOCUMENTATION & HANDOFF

- [ ] **Access Credentials**
  - [ ] Database credentials documented (securely)
  - [ ] Admin user created for initial login
  - [ ] SSH keys backed up

- [ ] **Runbooks Created**
  - [ ] How to restart services
  - [ ] How to view logs
  - [ ] How to restore from backup
  - [ ] How to deploy updates

- [ ] **Contact Information**
  - [ ] Support email: studenthub@nuhvin.com
  - [ ] Admin contact updated
  - [ ] Emergency contacts listed

---

## POST-DEPLOYMENT (ONGOING)

- [ ] **Daily**
  - [ ] Check service status
  - [ ] Monitor error logs
  - [ ] Verify backups completed

- [ ] **Weekly**
  - [ ] Review access logs for anomalies
  - [ ] Check disk space usage
  - [ ] Verify SSL certificate status

- [ ] **Monthly**
  - [ ] Security updates applied
  - [ ] Performance review
  - [ ] Backup integrity tested

- [ ] **Quarterly**
  - [ ] Full security audit
  - [ ] Dependency updates
  - [ ] Disaster recovery drill

---

## ROLLBACK PLAN

If deployment fails:
1. Stop studenthub service: `sudo systemctl stop studenthub.service`
2. Revert code: `git revert` or restore from backup
3. Restart service: `sudo systemctl start studenthub.service`
4. Verify: Check logs and endpoints

---

## SIGN-OFF

- [ ] **Deployed By:** _________________  
- [ ] **Date:** _________________  
- [ ] **Verified By:** _________________  
- [ ] **Date:** _________________  

**Notes:**
