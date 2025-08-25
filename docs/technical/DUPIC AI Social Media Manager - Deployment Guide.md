# DUPIC AI Social Media Manager - Deployment Guide

## Prerequisites

### System Requirements

- **Operating System**: Ubuntu 20.04+ or similar Linux distribution
- **Python**: 3.11 or higher
- **Node.js**: 20.x or higher
- **Database**: SQLite (development) or PostgreSQL (production)
- **Memory**: Minimum 4GB RAM (8GB+ recommended)
- **Storage**: 20GB+ available space

### Required Software

```bash
# Update system packages
sudo apt update && sudo apt upgrade -y

# Install Python and pip
sudo apt install python3.11 python3.11-pip python3.11-venv -y

# Install Node.js and npm
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt install nodejs -y

# Install Git
sudo apt install git -y

# Install additional dependencies
sudo apt install build-essential libssl-dev libffi-dev python3.11-dev -y
```

## Backend Deployment

### 1. Clone and Setup

```bash
# Clone the repository
git clone https://github.com/jonquixote/dupic.git
cd dupic/social-media-manager-app

# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Environment Configuration

Create a `.env` file in the backend directory:

```bash
# .env file
FLASK_APP=src/main.py
FLASK_ENV=production
SECRET_KEY=your-super-secret-key-here
DATABASE_URL=sqlite:///social_media_manager.db

# AI Provider API Keys (Optional - users can configure their own)
OPENAI_API_KEY=your-openai-api-key
ANTHROPIC_API_KEY=your-anthropic-api-key
GOOGLE_AI_API_KEY=your-google-ai-api-key

# Redis Configuration (if using Redis for caching)
REDIS_URL=redis://localhost:6379/0

# Email Configuration (for notifications)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
```

### 3. Database Setup

```bash
# Initialize the database
python3 -c "
from src.main import create_app
from src.models import db

app = create_app()
with app.app_context():
    db.create_all()
    print('Database initialized successfully!')
"
```

### 4. Production Server Setup

#### Using Gunicorn (Recommended)

```bash
# Install Gunicorn
pip install gunicorn

# Create Gunicorn configuration
cat > gunicorn.conf.py << EOF
bind = "0.0.0.0:5000"
workers = 4
worker_class = "sync"
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 100
timeout = 30
keepalive = 5
preload_app = True
EOF

# Start the application
gunicorn --config gunicorn.conf.py src.main:app
```

#### Using systemd Service

```bash
# Create systemd service file
sudo tee /etc/systemd/system/dupic-backend.service << EOF
[Unit]
Description=DUPIC AI Social Media Manager Backend
After=network.target

[Service]
Type=exec
User=ubuntu
Group=ubuntu
WorkingDirectory=/path/to/dupic/social-media-manager-app
Environment=PATH=/path/to/dupic/social-media-manager-app/venv/bin
ExecStart=/path/to/dupic/social-media-manager-app/venv/bin/gunicorn --config gunicorn.conf.py src.main:app
ExecReload=/bin/kill -s HUP \$MAINPID
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

# Enable and start the service
sudo systemctl daemon-reload
sudo systemctl enable dupic-backend
sudo systemctl start dupic-backend
sudo systemctl status dupic-backend
```

## Frontend Deployment

### 1. Setup and Build

```bash
# Navigate to frontend directory
cd ../dupic-frontend

# Install dependencies
npm install

# Build for production
npm run build
```

### 2. Static File Serving

#### Using Nginx (Recommended)

```bash
# Install Nginx
sudo apt install nginx -y

# Create Nginx configuration
sudo tee /etc/nginx/sites-available/dupic << EOF
server {
    listen 80;
    server_name your-domain.com;
    root /path/to/dupic/dupic-frontend/dist;
    index index.html;

    # Gzip compression
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_types text/plain text/css text/xml text/javascript application/javascript application/xml+rss application/json;

    # Handle React Router
    location / {
        try_files \$uri \$uri/ /index.html;
    }

    # API proxy to backend
    location /api/ {
        proxy_pass http://localhost:5000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }

    # Cache static assets
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
EOF

# Enable the site
sudo ln -s /etc/nginx/sites-available/dupic /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 3. SSL Certificate (Production)

```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx -y

# Obtain SSL certificate
sudo certbot --nginx -d your-domain.com

# Auto-renewal
sudo crontab -e
# Add this line:
# 0 12 * * * /usr/bin/certbot renew --quiet
```

## Database Configuration (Production)

### PostgreSQL Setup

```bash
# Install PostgreSQL
sudo apt install postgresql postgresql-contrib -y

# Create database and user
sudo -u postgres psql << EOF
CREATE DATABASE dupic_social_media;
CREATE USER dupic_user WITH PASSWORD 'secure_password_here';
GRANT ALL PRIVILEGES ON DATABASE dupic_social_media TO dupic_user;
\q
EOF

# Update .env file
DATABASE_URL=postgresql://dupic_user:secure_password_here@localhost/dupic_social_media
```

### Database Migration

```bash
# Install Flask-Migrate if not already installed
pip install Flask-Migrate

# Initialize migrations
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

## Redis Setup (Optional but Recommended)

```bash
# Install Redis
sudo apt install redis-server -y

# Configure Redis
sudo tee -a /etc/redis/redis.conf << EOF
maxmemory 256mb
maxmemory-policy allkeys-lru
EOF

# Start Redis
sudo systemctl restart redis-server
sudo systemctl enable redis-server
```

## Monitoring and Logging

### Application Logs

```bash
# Create log directory
sudo mkdir -p /var/log/dupic
sudo chown ubuntu:ubuntu /var/log/dupic

# Update Gunicorn config for logging
cat >> gunicorn.conf.py << EOF
accesslog = "/var/log/dupic/access.log"
errorlog = "/var/log/dupic/error.log"
loglevel = "info"
EOF
```

### System Monitoring

```bash
# Install htop for system monitoring
sudo apt install htop -y

# Install and configure fail2ban
sudo apt install fail2ban -y

# Create fail2ban configuration for Nginx
sudo tee /etc/fail2ban/jail.local << EOF
[nginx-http-auth]
enabled = true
port = http,https
logpath = /var/log/nginx/error.log

[nginx-noscript]
enabled = true
port = http,https
logpath = /var/log/nginx/access.log
maxretry = 6
EOF

sudo systemctl restart fail2ban
```

## Backup Strategy

### Database Backup

```bash
# Create backup script
cat > /home/ubuntu/backup_db.sh << EOF
#!/bin/bash
BACKUP_DIR="/home/ubuntu/backups"
DATE=\$(date +%Y%m%d_%H%M%S)

mkdir -p \$BACKUP_DIR

# SQLite backup
if [ -f "/path/to/dupic/social-media-manager-app/social_media_manager.db" ]; then
    cp "/path/to/dupic/social-media-manager-app/social_media_manager.db" "\$BACKUP_DIR/db_backup_\$DATE.db"
fi

# PostgreSQL backup (if using PostgreSQL)
# pg_dump -U dupic_user -h localhost dupic_social_media > "\$BACKUP_DIR/db_backup_\$DATE.sql"

# Keep only last 7 days of backups
find \$BACKUP_DIR -name "db_backup_*.db" -mtime +7 -delete
find \$BACKUP_DIR -name "db_backup_*.sql" -mtime +7 -delete

echo "Backup completed: \$DATE"
EOF

chmod +x /home/ubuntu/backup_db.sh

# Schedule daily backups
crontab -e
# Add this line:
# 0 2 * * * /home/ubuntu/backup_db.sh
```

## Security Hardening

### Firewall Configuration

```bash
# Install and configure UFW
sudo ufw enable
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow ssh
sudo ufw allow 'Nginx Full'
sudo ufw status
```

### Application Security

```bash
# Update system packages regularly
sudo apt update && sudo apt upgrade -y

# Set proper file permissions
chmod 600 /path/to/dupic/social-media-manager-app/.env
chmod -R 755 /path/to/dupic/dupic-frontend/dist
```

## Performance Optimization

### Backend Optimization

```bash
# Install and configure Redis for caching
pip install redis flask-caching

# Add to your Flask app configuration
CACHE_TYPE = "RedisCache"
CACHE_REDIS_URL = "redis://localhost:6379/0"
```

### Frontend Optimization

```bash
# Enable Nginx gzip compression (already included in config above)
# Configure browser caching (already included in config above)

# Optional: Use a CDN for static assets
# Configure your CDN to point to your domain/static files
```

## Troubleshooting

### Common Issues

1. **Port Already in Use**
   ```bash
   sudo lsof -i :5000
   sudo kill -9 <PID>
   ```

2. **Permission Denied**
   ```bash
   sudo chown -R ubuntu:ubuntu /path/to/dupic
   chmod +x /path/to/dupic/social-media-manager-app/venv/bin/activate
   ```

3. **Database Connection Issues**
   ```bash
   # Check database status
   sudo systemctl status postgresql
   
   # Test connection
   psql -U dupic_user -h localhost -d dupic_social_media
   ```

4. **Nginx Configuration Issues**
   ```bash
   sudo nginx -t
   sudo systemctl status nginx
   sudo tail -f /var/log/nginx/error.log
   ```

### Log Locations

- **Application Logs**: `/var/log/dupic/`
- **Nginx Logs**: `/var/log/nginx/`
- **System Logs**: `/var/log/syslog`
- **PostgreSQL Logs**: `/var/log/postgresql/`

## Maintenance

### Regular Tasks

1. **Weekly**
   - Check system logs for errors
   - Monitor disk space usage
   - Review application performance

2. **Monthly**
   - Update system packages
   - Review and rotate logs
   - Check SSL certificate expiry

3. **Quarterly**
   - Review security configurations
   - Update application dependencies
   - Performance optimization review

### Update Procedure

```bash
# 1. Backup current version
cp -r /path/to/dupic /path/to/dupic_backup_$(date +%Y%m%d)

# 2. Pull latest changes
cd /path/to/dupic
git pull origin main

# 3. Update backend dependencies
cd social-media-manager-app
source venv/bin/activate
pip install -r requirements.txt

# 4. Run database migrations
flask db upgrade

# 5. Update frontend
cd ../dupic-frontend
npm install
npm run build

# 6. Restart services
sudo systemctl restart dupic-backend
sudo systemctl restart nginx
```

## Support and Documentation

### Getting Help

- **GitHub Issues**: Report bugs and feature requests
- **Documentation**: Check the README files in each directory
- **Logs**: Always check application logs first

### Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

---

*Last Updated: August 23, 2025*
*Version: 2.0.0*

