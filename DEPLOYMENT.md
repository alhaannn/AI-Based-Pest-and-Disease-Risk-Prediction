# 🚀 Deployment Guide - AI-Based Pest and Disease Risk Prediction System

This guide covers deploying the application to production environments.

## Table of Contents

1. [Pre-Deployment Checklist](#pre-deployment-checklist)
2. [Environment Setup](#environment-setup)
3. [Database Configuration](#database-configuration)
4. [Static Files](#static-files)
5. [WSGI Server Setup](#wsgi-server-setup)
6. [Web Server Configuration](#web-server-configuration)
7. [SSL/HTTPS Setup](#sslhttps-setup)
8. [Environment Variables](#environment-variables)
9. [Deployment Platforms](#deployment-platforms)
10. [Post-Deployment](#post-deployment)
11. [Monitoring & Maintenance](#monitoring--maintenance)

---

## ✅ Pre-Deployment Checklist

Before deploying to production, ensure:

- [ ] All tests pass locally
- [ ] Database migrations are up to date
- [ ] Static files are collected
- [ ] Environment variables are configured
- [ ] DEBUG is set to False
- [ ] SECRET_KEY is secure and unique
- [ ] ALLOWED_HOSTS is configured
- [ ] Database backups are set up
- [ ] SSL certificate is obtained
- [ ] Monitoring is configured

---

## 🔧 Environment Setup

### 1. Production Settings

Create `pest_prediction/settings_production.py`:

```python
from .settings import *

# Security Settings
DEBUG = False
SECRET_KEY = os.environ.get('SECRET_KEY')
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        'PORT': os.environ.get('DB_PORT', '5432'),
    }
}

# Static Files
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'

# Media Files
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# Security
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# HTTPS
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Email (for future notifications)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.environ.get('EMAIL_HOST')
EMAIL_PORT = int(os.environ.get('EMAIL_PORT', 587))
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get('EMAIL_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_PASSWORD')

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': '/var/log/django/error.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}
```

### 2. Update manage.py

```python
#!/usr/bin/env python
import os
import sys

if __name__ == '__main__':
    # Use production settings in production
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 
                          'pest_prediction.settings_production')
    
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
```

---

## 🗄️ Database Configuration

### PostgreSQL Setup (Recommended)

**1. Install PostgreSQL:**

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install postgresql postgresql-contrib

# Start PostgreSQL
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

**2. Create Database and User:**

```bash
sudo -u postgres psql

# In PostgreSQL shell:
CREATE DATABASE pest_prediction_db;
CREATE USER pest_user WITH PASSWORD 'your_secure_password';
ALTER ROLE pest_user SET client_encoding TO 'utf8';
ALTER ROLE pest_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE pest_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE pest_prediction_db TO pest_user;
\q
```

**3. Install psycopg2:**

```bash
pip install psycopg2-binary
```

**4. Run Migrations:**

```bash
python manage.py migrate
python manage.py createsuperuser
```

### MySQL Setup (Alternative)

```bash
# Install MySQL
sudo apt install mysql-server

# Create database
sudo mysql -u root -p

CREATE DATABASE pest_prediction_db CHARACTER SET utf8mb4;
CREATE USER 'pest_user'@'localhost' IDENTIFIED BY 'your_secure_password';
GRANT ALL PRIVILEGES ON pest_prediction_db.* TO 'pest_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;

# Install MySQL client
pip install mysqlclient
```

Update settings:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'pest_prediction_db',
        'USER': 'pest_user',
        'PASSWORD': 'your_secure_password',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

---

## 📦 Static Files

### 1. Collect Static Files

```bash
python manage.py collectstatic --noinput
```

### 2. Configure Static File Serving

**Option A: WhiteNoise (Simple)**

```bash
pip install whitenoise
```

Add to `settings_production.py`:
```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Add this
    # ... other middleware
]

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
```

**Option B: Nginx (Recommended for production)**

See [Web Server Configuration](#web-server-configuration)

---

## 🖥️ WSGI Server Setup

### Gunicorn (Recommended)

**1. Install Gunicorn:**

```bash
pip install gunicorn
```

**2. Create Gunicorn Configuration:**

Create `gunicorn_config.py`:

```python
import multiprocessing

bind = "127.0.0.1:8000"
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "sync"
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 50
timeout = 30
keepalive = 2

# Logging
accesslog = "/var/log/gunicorn/access.log"
errorlog = "/var/log/gunicorn/error.log"
loglevel = "info"
```

**3. Create Systemd Service:**

Create `/etc/systemd/system/pest-prediction.service`:

```ini
[Unit]
Description=Pest Prediction Gunicorn Daemon
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/pest-prediction
Environment="PATH=/var/www/pest-prediction/venv/bin"
ExecStart=/var/www/pest-prediction/venv/bin/gunicorn \
          --config /var/www/pest-prediction/gunicorn_config.py \
          pest_prediction.wsgi:application

[Install]
WantedBy=multi-user.target
```

**4. Start Service:**

```bash
sudo systemctl start pest-prediction
sudo systemctl enable pest-prediction
sudo systemctl status pest-prediction
```

### uWSGI (Alternative)

```bash
pip install uwsgi

# Create uwsgi.ini
[uwsgi]
chdir = /var/www/pest-prediction
module = pest_prediction.wsgi:application
master = true
processes = 4
socket = /var/www/pest-prediction/pest-prediction.sock
chmod-socket = 666
vacuum = true
die-on-term = true
```

---

## 🌐 Web Server Configuration

### Nginx (Recommended)

**1. Install Nginx:**

```bash
sudo apt install nginx
```

**2. Create Nginx Configuration:**

Create `/etc/nginx/sites-available/pest-prediction`:

```nginx
upstream pest_prediction {
    server 127.0.0.1:8000;
}

server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;
    
    # Redirect to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com www.yourdomain.com;
    
    # SSL Configuration
    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    
    # Logging
    access_log /var/log/nginx/pest-prediction-access.log;
    error_log /var/log/nginx/pest-prediction-error.log;
    
    # Max upload size
    client_max_body_size 10M;
    
    # Static files
    location /static/ {
        alias /var/www/pest-prediction/staticfiles/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }
    
    # Media files
    location /media/ {
        alias /var/www/pest-prediction/media/;
        expires 7d;
    }
    
    # Django application
    location / {
        proxy_pass http://pest_prediction;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
    }
}
```

**3. Enable Site:**

```bash
sudo ln -s /etc/nginx/sites-available/pest-prediction /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### Apache (Alternative)

```bash
sudo apt install apache2 libapache2-mod-wsgi-py3

# Enable modules
sudo a2enmod wsgi
sudo a2enmod ssl
sudo a2enmod rewrite
```

Create `/etc/apache2/sites-available/pest-prediction.conf`:

```apache
<VirtualHost *:80>
    ServerName yourdomain.com
    Redirect permanent / https://yourdomain.com/
</VirtualHost>

<VirtualHost *:443>
    ServerName yourdomain.com
    
    SSLEngine on
    SSLCertificateFile /etc/letsencrypt/live/yourdomain.com/fullchain.pem
    SSLCertificateKeyFile /etc/letsencrypt/live/yourdomain.com/privkey.pem
    
    Alias /static /var/www/pest-prediction/staticfiles
    Alias /media /var/www/pest-prediction/media
    
    <Directory /var/www/pest-prediction/staticfiles>
        Require all granted
    </Directory>
    
    <Directory /var/www/pest-prediction/media>
        Require all granted
    </Directory>
    
    WSGIDaemonProcess pest_prediction python-path=/var/www/pest-prediction python-home=/var/www/pest-prediction/venv
    WSGIProcessGroup pest_prediction
    WSGIScriptAlias / /var/www/pest-prediction/pest_prediction/wsgi.py
    
    <Directory /var/www/pest-prediction/pest_prediction>
        <Files wsgi.py>
            Require all granted
        </Files>
    </Directory>
</VirtualHost>
```

---

## 🔒 SSL/HTTPS Setup

### Let's Encrypt (Free SSL)

**1. Install Certbot:**

```bash
sudo apt install certbot python3-certbot-nginx
```

**2. Obtain Certificate:**

```bash
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

**3. Auto-Renewal:**

```bash
# Test renewal
sudo certbot renew --dry-run

# Certbot automatically sets up cron job
# Verify with:
sudo systemctl status certbot.timer
```

---

## 🔐 Environment Variables

### 1. Create .env File

Create `/var/www/pest-prediction/.env`:

```bash
# Django
SECRET_KEY=your-very-long-random-secret-key-here
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# Database
DB_NAME=pest_prediction_db
DB_USER=pest_user
DB_PASSWORD=your_secure_password
DB_HOST=localhost
DB_PORT=5432

# Email (for future notifications)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USER=your-email@gmail.com
EMAIL_PASSWORD=your-app-password

# Optional
DJANGO_SETTINGS_MODULE=pest_prediction.settings_production
```

### 2. Load Environment Variables

Install python-decouple:

```bash
pip install python-decouple
```

Update `settings_production.py`:

```python
from decouple import config

SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS').split(',')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT'),
    }
}
```

---

## ☁️ Deployment Platforms

### Heroku

**1. Install Heroku CLI:**

```bash
curl https://cli-assets.heroku.com/install.sh | sh
```

**2. Create Procfile:**

```
web: gunicorn pest_prediction.wsgi --log-file -
release: python manage.py migrate
```

**3. Create runtime.txt:**

```
python-3.10.12
```

**4. Deploy:**

```bash
heroku login
heroku create your-app-name
heroku addons:create heroku-postgresql:hobby-dev
git push heroku main
heroku run python manage.py createsuperuser
heroku open
```

### DigitalOcean

**1. Create Droplet** (Ubuntu 22.04)

**2. SSH into Droplet:**

```bash
ssh root@your-droplet-ip
```

**3. Follow standard deployment steps above**

**4. Configure Firewall:**

```bash
sudo ufw allow 22
sudo ufw allow 80
sudo ufw allow 443
sudo ufw enable
```

### AWS EC2

**1. Launch EC2 Instance** (Ubuntu 22.04)

**2. Configure Security Group:**
- SSH (22)
- HTTP (80)
- HTTPS (443)

**3. Connect and Deploy:**

```bash
ssh -i your-key.pem ubuntu@ec2-ip-address
# Follow standard deployment steps
```

### Docker Deployment

**Create Dockerfile:**

```dockerfile
FROM python:3.10-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "pest_prediction.wsgi:application"]
```

**Create docker-compose.yml:**

```yaml
version: '3.8'

services:
  db:
    image: postgres:14
    environment:
      POSTGRES_DB: pest_prediction_db
      POSTGRES_USER: pest_user
      POSTGRES_PASSWORD: your_password
    volumes:
      - postgres_data:/var/lib/postgresql/data

  web:
    build: .
    command: gunicorn pest_prediction.wsgi:application --bind 0.0.0.0:8000
    volumes:
      - .:/app
      - static_volume:/app/staticfiles
      - media_volume:/app/media
    ports:
      - "8000:8000"
    env_file:
      - .env
    depends_on:
      - db

  nginx:
    image: nginx:alpine
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - static_volume:/app/staticfiles
      - media_volume:/app/media
    ports:
      - "80:80"
      - "443:443"
    depends_on:
      - web

volumes:
  postgres_data:
  static_volume:
  media_volume:
```

**Deploy:**

```bash
docker-compose up -d
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
```

---

## ✅ Post-Deployment

### 1. Verify Deployment

```bash
# Check services
sudo systemctl status pest-prediction
sudo systemctl status nginx

# Check logs
sudo tail -f /var/log/gunicorn/error.log
sudo tail -f /var/log/nginx/error.log

# Test application
curl https://yourdomain.com
```

### 2. Create Superuser

```bash
python manage.py createsuperuser
```

### 3. Load Initial Data

```bash
# If you have fixtures
python manage.py loaddata initial_data.json

# Or manually add preventive measures via admin panel
```

### 4. Set Up Backups

**Database Backup Script** (`backup.sh`):

```bash
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/var/backups/pest-prediction"
DB_NAME="pest_prediction_db"

mkdir -p $BACKUP_DIR

# Database backup
pg_dump -U pest_user $DB_NAME > $BACKUP_DIR/db_$DATE.sql

# Media files backup
tar -czf $BACKUP_DIR/media_$DATE.tar.gz /var/www/pest-prediction/media

# Keep only last 30 days
find $BACKUP_DIR -type f -mtime +30 -delete

echo "Backup completed: $DATE"
```

**Add to crontab:**

```bash
sudo crontab -e

# Daily backup at 2 AM
0 2 * * * /var/www/pest-prediction/backup.sh
```

---

## 📊 Monitoring & Maintenance

### 1. Set Up Monitoring

**Install monitoring tools:**

```bash
# System monitoring
sudo apt install htop

# Application monitoring
pip install django-prometheus
```

### 2. Log Rotation

Create `/etc/logrotate.d/pest-prediction`:

```
/var/log/gunicorn/*.log {
    daily
    rotate 30
    compress
    delaycompress
    notifempty
    create 0640 www-data www-data
    sharedscripts
    postrotate
        systemctl reload pest-prediction
    endscript
}
```

### 3. Performance Optimization

**Enable caching:**

```python
# settings_production.py
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
    }
}
```

**Database optimization:**

```bash
# PostgreSQL
sudo -u postgres psql pest_prediction_db

VACUUM ANALYZE;
REINDEX DATABASE pest_prediction_db;
```

### 4. Regular Maintenance Tasks

**Weekly:**
- Check error logs
- Review disk space
- Monitor database size

**Monthly:**
- Update dependencies
- Review security patches
- Test backups
- Clean old data

**Quarterly:**
- Performance audit
- Security audit
- Update documentation

---

## 🆘 Troubleshooting

### Common Issues

**Issue: 502 Bad Gateway**
```bash
# Check Gunicorn
sudo systemctl status pest-prediction
sudo journalctl -u pest-prediction -n 50

# Check Nginx
sudo nginx -t
sudo systemctl status nginx
```

**Issue: Static files not loading**
```bash
# Recollect static files
python manage.py collectstatic --clear --noinput

# Check permissions
sudo chown -R www-data:www-data /var/www/pest-prediction/staticfiles
```

**Issue: Database connection errors**
```bash
# Check PostgreSQL
sudo systemctl status postgresql
sudo -u postgres psql -c "SELECT 1"

# Verify credentials in .env
```

---

## 📞 Support

For deployment issues:
- Check logs: `/var/log/gunicorn/`, `/var/log/nginx/`
- Review Django documentation
- Consult platform-specific guides

---

**Deployment Complete! 🎉**

Your AI-Based Pest and Disease Risk Prediction System is now live and ready to help farmers!
