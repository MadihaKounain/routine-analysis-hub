# 🚀 Production Deployment Guide

## Pre-Deployment Checklist

### Security
- [ ] Generate strong SECRET_KEY
- [ ] Update all credentials
- [ ] Enable HTTPS/SSL
- [ ] Configure environment variables
- [ ] Review authentication logic
- [ ] Enable security headers

### Performance
- [ ] Set up caching strategy
- [ ] Configure logging
- [ ] Test under load
- [ ] Optimize database queries
- [ ] Minify static assets

### Infrastructure
- [ ] Use production WSGI server (Gunicorn)
- [ ] Set up reverse proxy (Nginx)
- [ ] Configure firewall
- [ ] Set up backup strategy
- [ ] Configure monitoring/alerting

---

## Step 1: Prepare Environment

### 1.1 Generate Secret Key
```bash
python -c "import secrets; print(secrets.token_hex(32))"
# Output: a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6a7b8c9d0e1f2
```

### 1.2 Create Production `.env` File
```bash
# On your production server, create .env with:

FLASK_ENV=production
SECRET_KEY=a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6a7b8c9d0e1f2
SESSION_COOKIE_SECURE=True
SESSION_COOKIE_HTTPONLY=True
DATABASE_PATH=/var/app/database/app.json
LOG_LEVEL=WARNING
LOG_FILE=/var/log/flask-app/app.log
HOST=0.0.0.0
PORT=8000
```

### 1.3 Set Permissions
```bash
# Create application directory
mkdir -p /var/app
mkdir -p /var/log/flask-app

# Copy application
cp -r routine-analytics-hub/* /var/app/

# Set permissions
chmod 755 /var/app
chmod 755 /var/log/flask-app
chown www-data:www-data /var/app
chown www-data:www-data /var/log/flask-app
```

---

## Step 2: Install Dependencies

### 2.1 Create Virtual Environment
```bash
cd /var/app
python3 -m venv venv
source venv/bin/activate
```

### 2.2 Install Packages
```bash
pip install -r requirements.txt
pip install gunicorn
pip install psycopg2-binary  # If using PostgreSQL
```

### 2.3 Verify Installation
```bash
python -c "from app import create_app; app = create_app('production'); print('✅ App loads successfully')"
```

---

## Step 3: Migrate Database (Optional)

### 3.1 From JSON to PostgreSQL (Recommended for Production)

**Install PostgreSQL packages:**
```bash
pip install sqlalchemy flask-sqlalchemy
```

**Create migration script** (`scripts/migrate_to_postgres.py`):
```python
import json
import os
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Text
from sqlalchemy.orm import sessionmaker, declarative_base
from datetime import datetime

# Configure PostgreSQL connection
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://user:password@localhost/analytics_db')

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
Base = declarative_base()

# Define SQLAlchemy models
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(20), default='user')
    created_at = Column(DateTime, default=datetime.utcnow)

class Task(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    priority = Column(String(20), default='medium')
    status = Column(String(20), default='pending')
    created_at = Column(DateTime, default=datetime.utcnow)

# Create tables
Base.metadata.create_all(engine)

# Load JSON data and migrate
json_path = 'app/database/app.json'
with open(json_path, 'r') as f:
    data = json.load(f)

session = Session()

# Migrate users
for user in data.get('users', []):
    new_user = User(**user)
    session.add(new_user)

# Migrate tasks
for task in data.get('tasks', []):
    new_task = Task(**task)
    session.add(new_task)

session.commit()
print("✅ Migration complete")
```

**Run migration:**
```bash
python scripts/migrate_to_postgres.py
```

---

## Step 4: Set Up Gunicorn

### 4.1 Create Gunicorn Configuration (`gunicorn_config.py`)
```python
import multiprocessing
import os

# Server configuration
bind = "0.0.0.0:8000"
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "sync"
threads = 2
timeout = 60
keepalive = 2

# Logging
accesslog = "/var/log/flask-app/access.log"
errorlog = "/var/log/flask-app/error.log"
loglevel = "warning"

# Process naming
proc_name = "routine-analytics-hub"

# Server mechanics
daemon = False
pidfile = "/tmp/gunicorn.pid"
max_requests = 1000
max_requests_jitter = 100
```

### 4.2 Create Systemd Service (`/etc/systemd/system/flask-app.service`)
```ini
[Unit]
Description=Routine Analytics Hub Flask Application
After=network.target

[Service]
Type=notify
User=www-data
WorkingDirectory=/var/app
Environment="PATH=/var/app/venv/bin"
ExecStart=/var/app/venv/bin/gunicorn --config gunicorn_config.py run:app
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### 4.3 Enable Service
```bash
sudo systemctl daemon-reload
sudo systemctl enable flask-app
sudo systemctl start flask-app
sudo systemctl status flask-app
```

---

## Step 5: Configure Nginx Reverse Proxy

### 5.1 Create Nginx Configuration (`/etc/nginx/sites-available/analytics`)
```nginx
upstream flask_app {
    server 127.0.0.1:8000;
}

server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;
    
    # Redirect HTTP to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com www.yourdomain.com;
    
    # SSL Certificate
    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;
    
    # SSL Configuration
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 10m;
    
    # Security Headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-XSS-Protection "1; mode=block" always;
    
    # Logging
    access_log /var/log/nginx/flask-app-access.log;
    error_log /var/log/nginx/flask-app-error.log;
    
    # Client limits
    client_max_body_size 16M;
    
    # Proxy configuration
    location / {
        proxy_pass http://flask_app;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
        
        # Timeouts
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }
    
    # Static files (with caching)
    location /static {
        alias /var/app/app/static;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }
}
```

### 5.2 Enable Nginx Site
```bash
sudo ln -s /etc/nginx/sites-available/analytics /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

---

## Step 6: Set Up SSL Certificate

### 6.1 Using Let's Encrypt (Free)
```bash
sudo apt-get install certbot python3-certbot-nginx
sudo certbot certonly --nginx -d yourdomain.com -d www.yourdomain.com
```

### 6.2 Auto-Renewal
```bash
sudo systemctl enable certbot.timer
sudo systemctl start certbot.timer
```

---

## Step 7: Configure Logging and Backups

### 7.1 Set Up Log Rotation (`/etc/logrotate.d/flask-app`)
```
/var/log/flask-app/*.log {
    daily
    rotate 14
    compress
    delaycompress
    notifempty
    create 0640 www-data www-data
    sharedscripts
    postrotate
        systemctl reload flask-app > /dev/null 2>&1 || true
    endscript
}
```

### 7.2 Backup Database Script (`scripts/backup_db.sh`)
```bash
#!/bin/bash

BACKUP_DIR="/var/backups/analytics-db"
DB_FILE="/var/app/database/app.json"
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p $BACKUP_DIR

# Create backup
cp $DB_FILE $BACKUP_DIR/app_$DATE.json

# Keep only last 30 days
find $BACKUP_DIR -name "app_*.json" -mtime +30 -delete

echo "✅ Backup created: app_$DATE.json"
```

### 7.3 Schedule Backups (Crontab)
```bash
# Daily backup at 2 AM
0 2 * * * /var/app/scripts/backup_db.sh

# Weekly backup to external storage
0 3 * * 0 rsync -av /var/backups/analytics-db/ /mnt/external-drive/backups/
```

---

## Step 8: Monitoring and Alerting

### 8.1 Monitor Application Health
```bash
# Check service status
sudo systemctl status flask-app

# View application logs
tail -f /var/log/flask-app/app.log

# Check Nginx status
sudo systemctl status nginx
```

### 8.2 Set Up Monitoring Tools

**Option 1: Using Prometheus (Advanced)**
```yaml
# /etc/prometheus/prometheus.yml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'flask-app'
    static_configs:
      - targets: ['localhost:8000']
```

**Option 2: Simple Health Check Script**
```bash
#!/bin/bash
# scripts/health_check.sh

URL="https://yourdomain.com"
RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" $URL)

if [ $RESPONSE -eq 200 ]; then
    echo "✅ Application is healthy"
else
    echo "❌ Application returned HTTP $RESPONSE"
    # Send alert email
    mail -s "Analytics App Error" admin@example.com <<< "HTTP $RESPONSE"
fi
```

---

## Step 9: Performance Optimization

### 9.1 Enable Caching
```bash
pip install redis flask-caching
```

### 9.2 Configure Connection Pooling
In your database module, enable connection pooling if using SQL database.

### 9.3 Compress Static Assets
```bash
# Install compression tools
sudo apt-get install brotli

# Create compressed versions
for file in app/static/css/*.css app/static/js/*.js; do
    gzip -9 -k $file
    brotli -9 -k $file
done
```

---

## Deployment Verification

### Check Application
```bash
# Test health endpoint
curl https://yourdomain.com/

# Check logs for errors
grep -i error /var/log/flask-app/app.log

# Verify SSL certificate
curl -I https://yourdomain.com/
```

### Load Testing
```bash
pip install locust

# Create locustfile.py and run
locust -f locustfile.py -u 100 -r 10 -t 1m
```

---

## Troubleshooting

### Service won't start
```bash
# Check logs
sudo journalctl -u flask-app -n 50

# Check permissions
ls -la /var/app
ls -la /var/log/flask-app
```

### Connection refused
```bash
# Check if Gunicorn is running
ps aux | grep gunicorn

# Check port binding
netstat -tlnp | grep 8000
```

### Database issues
```bash
# Verify database exists
ls -la /var/app/database/

# Check ownership
ls -la /var/app/database/app.json
```

---

## Security Hardening

✅ Implemented in production config:
- HTTPS/SSL required
- Secure cookies (HttpOnly, Secure, SameSite)
- Strong SECRET_KEY
- Minimal logging (no sensitive data)
- CORS headers configured
- Rate limiting recommended

Still to implement (optional):
```bash
# Add rate limiting
pip install flask-limiter

# Add CSRF protection if forms added
pip install flask-wtf

# Add security headers middleware
pip install flask-talisman
```

---

## Maintenance

### Monthly Tasks
- [ ] Review logs for errors
- [ ] Check SSL certificate expiration
- [ ] Review backup status
- [ ] Update dependencies (`pip install --upgrade -r requirements.txt`)

### Quarterly Tasks
- [ ] Security audit
- [ ] Performance review
- [ ] Database optimization/cleanup

### Annually
- [ ] Full security assessment
- [ ] Disaster recovery test

---

## Rollback Plan

If deployment fails:
```bash
# Stop current version
sudo systemctl stop flask-app

# Remove new version
rm -rf /var/app/*

# Restore from backup
git checkout <previous-commit>
# or restore from backup storage

# Restart service
sudo systemctl start flask-app
```

---

## Support

For issues during deployment:
1. Check the troubleshooting section
2. Review application logs: `/var/log/flask-app/app.log`
3. Review Nginx logs: `/var/log/nginx/flask-app-error.log`
4. Check system resources: `top`, `df -h`

