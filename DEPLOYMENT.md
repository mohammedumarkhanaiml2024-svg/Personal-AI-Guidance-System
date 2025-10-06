# Personal AI Guidance System - Deployment Guide

## 📦 Build & Deployment Options

This project supports multiple deployment methods:

1. **Direct Python Deployment** - Run directly with Python and uvicorn
2. **Docker Deployment** - Containerized deployment with Docker
3. **Docker Compose** - Multi-container orchestration
4. **Cloud Deployment** - Deploy to cloud platforms (AWS, GCP, Azure, etc.)

---

## 🚀 Quick Start

### Option 1: Using Build Script (Recommended)

```bash
# Make build script executable (first time only)
chmod +x build.sh

# Run the build
./build.sh

# Navigate to dist directory
cd dist/

# Extract the distribution
tar -xzf personal-ai-guidance-system-1.0.0.tar.gz

# Install
./install.sh

# Configure (edit .env file with your settings)
nano .env

# Start the application
./start.sh
```

### Option 2: Using Makefile

```bash
# Show all available commands
make help

# Run complete build
make all

# Or run individual commands
make install    # Install dependencies
make build      # Create distribution
make deploy     # Prepare deployment package
```

---

## 🔨 Build Commands

### Using build.sh

```bash
# Basic build
./build.sh

# Build with custom version
VERSION=2.0.0 ./build.sh

# Build with Docker registry
REGISTRY=myregistry.com VERSION=1.0.0 ./build.sh
```

### Using Makefile

```bash
make help           # Show all commands
make install        # Install Python dependencies
make clean          # Clean build artifacts
make test           # Run tests
make lint           # Lint code
make build          # Build distribution
make docker-build   # Build Docker image
make docker-run     # Run with Docker Compose
make deploy         # Prepare deployment package
make all            # Complete build process
```

---

## 🐳 Docker Deployment

### Build Docker Image

```bash
# Using Makefile
make docker-build

# Or using Docker directly
docker build -t personal-ai-guidance-system:1.0.0 .
```

### Run with Docker Compose

```bash
# Start services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Run Docker Container Manually

```bash
# Run backend container
docker run -d \
  --name ai-guidance-backend \
  -p 8000:8000 \
  -v $(pwd)/private_user_data:/app/private_user_data \
  -v $(pwd)/app.db:/app/app.db \
  -e GOOGLE_API_KEY=your_key_here \
  personal-ai-guidance-system:1.0.0
```

---

## ☁️ Cloud Deployment

### AWS EC2

```bash
# 1. SSH into your EC2 instance
ssh -i your-key.pem ubuntu@your-ec2-ip

# 2. Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# 3. Copy your distribution file
scp -i your-key.pem dist/personal-ai-guidance-system-1.0.0.tar.gz ubuntu@your-ec2-ip:~/

# 4. Load and run Docker image
docker load -i personal-ai-guidance-system-1.0.0.tar
docker-compose up -d

# 5. Configure security group to allow ports 8000 and 8080
```

### AWS ECS (Elastic Container Service)

```bash
# 1. Build and push to ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin your-account.dkr.ecr.us-east-1.amazonaws.com

docker tag personal-ai-guidance-system:1.0.0 your-account.dkr.ecr.us-east-1.amazonaws.com/ai-guidance:1.0.0
docker push your-account.dkr.ecr.us-east-1.amazonaws.com/ai-guidance:1.0.0

# 2. Create ECS task definition and service using AWS Console or CLI
```

### Google Cloud Run

```bash
# 1. Build and push to GCR
gcloud auth configure-docker
docker tag personal-ai-guidance-system:1.0.0 gcr.io/your-project/ai-guidance:1.0.0
docker push gcr.io/your-project/ai-guidance:1.0.0

# 2. Deploy to Cloud Run
gcloud run deploy ai-guidance \
  --image gcr.io/your-project/ai-guidance:1.0.0 \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --port 8000
```

### Azure Container Instances

```bash
# 1. Login to Azure
az login

# 2. Create container registry
az acr create --resource-group myResourceGroup --name myregistry --sku Basic

# 3. Push image
az acr login --name myregistry
docker tag personal-ai-guidance-system:1.0.0 myregistry.azurecr.io/ai-guidance:1.0.0
docker push myregistry.azurecr.io/ai-guidance:1.0.0

# 4. Deploy container
az container create \
  --resource-group myResourceGroup \
  --name ai-guidance \
  --image myregistry.azurecr.io/ai-guidance:1.0.0 \
  --cpu 1 --memory 1 \
  --port 8000 \
  --dns-name-label ai-guidance-app
```

### Heroku

```bash
# 1. Create Procfile
echo "web: uvicorn main_enhanced:app --host 0.0.0.0 --port \$PORT" > Procfile

# 2. Initialize git and deploy
git init
git add .
git commit -m "Initial commit"

# 3. Create Heroku app
heroku create your-app-name

# 4. Set environment variables
heroku config:set GOOGLE_API_KEY=your_key_here

# 5. Deploy
git push heroku main
```

### DigitalOcean App Platform

```bash
# 1. Create app.yaml
cat > app.yaml << EOF
name: personal-ai-guidance
services:
- name: backend
  github:
    repo: your-username/your-repo
    branch: main
  build_command: pip install -r requirements.txt
  run_command: uvicorn main_enhanced:app --host 0.0.0.0 --port 8080
  envs:
  - key: GOOGLE_API_KEY
    value: your_key_here
  http_port: 8080
EOF

# 2. Deploy using DigitalOcean CLI
doctl apps create --spec app.yaml
```

---

## 🔧 Production Configuration

### Environment Variables

Create a `.env` file with the following configuration:

```bash
# Application
ENVIRONMENT=production
DEBUG=false

# Database
DATABASE_URL=sqlite:///./app.db

# Google AI
GOOGLE_API_KEY=your_google_api_key_here

# Security
SECRET_KEY=your_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Server
HOST=0.0.0.0
PORT=8000

# CORS
CORS_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
```

### Nginx Reverse Proxy (Production)

```nginx
server {
    listen 80;
    server_name yourdomain.com;

    # Redirect to HTTPS
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com;

    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;

    # Frontend
    location / {
        proxy_pass http://localhost:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    # Backend API
    location /api/ {
        proxy_pass http://localhost:8000/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### SSL Certificate (Let's Encrypt)

```bash
# Install certbot
sudo apt-get install certbot python3-certbot-nginx

# Obtain certificate
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com

# Auto-renewal (add to crontab)
0 0 * * * certbot renew --quiet
```

---

## 📊 Monitoring & Logging

### Application Logs

```bash
# View backend logs
tail -f logs/backend.log

# View frontend logs
tail -f logs/frontend.log

# Docker logs
docker-compose logs -f backend
```

### Health Checks

```bash
# Check backend health
curl http://localhost:8000/health

# Check with Docker
docker exec ai-guidance-backend curl -f http://localhost:8000/health
```

---

## 🔄 Updates & Maintenance

### Update Application

```bash
# 1. Build new version
VERSION=1.1.0 ./build.sh

# 2. Stop current version
./stop.sh  # or: docker-compose down

# 3. Deploy new version
tar -xzf dist/personal-ai-guidance-system-1.1.0.tar.gz
./install.sh
./start.sh  # or: docker-compose up -d
```

### Database Migrations

```bash
# Backup current database
cp app.db app.db.backup

# Run migrations (if using Alembic)
alembic upgrade head
```

---

## 🛡️ Security Checklist

- [ ] Change default SECRET_KEY in .env
- [ ] Set strong GOOGLE_API_KEY
- [ ] Configure CORS_ORIGINS for production domains
- [ ] Enable HTTPS with SSL certificate
- [ ] Set up firewall (allow only 80, 443, 22)
- [ ] Regular security updates: `apt-get update && apt-get upgrade`
- [ ] Backup database regularly
- [ ] Monitor logs for suspicious activity
- [ ] Use strong passwords for user accounts
- [ ] Enable rate limiting (if needed)

---

## 📦 Build Artifacts

After running `./build.sh`, you'll find in `dist/`:

1. **personal-ai-guidance-system-1.0.0.tar.gz** - Source distribution
2. **personal-ai-guidance-system-1.0.0.tar** - Docker image (if Docker available)
3. **BUILD_INFO.txt** - Build manifest
4. **install.sh** - Installation script
5. **start.sh** - Start script
6. **stop.sh** - Stop script

---

## 🆘 Troubleshooting

### Build Issues

**Problem:** `Python 3 is required but not installed`
```bash
# Ubuntu/Debian
sudo apt-get install python3 python3-pip

# macOS
brew install python3
```

**Problem:** `Docker not found`
```bash
# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
```

### Runtime Issues

**Problem:** `Port 8000 already in use`
```bash
# Find and kill process
lsof -ti:8000 | xargs kill -9
```

**Problem:** `Permission denied`
```bash
# Make scripts executable
chmod +x build.sh start.sh stop.sh install.sh
```

**Problem:** `Database locked`
```bash
# Stop all processes
./stop.sh

# Remove lock file
rm -f app.db-journal

# Restart
./start.sh
```

---

## 📞 Support

For issues and questions:
1. Check logs: `tail -f logs/backend.log`
2. Review BUILD_INFO.txt
3. Check health endpoint: `curl http://localhost:8000/health`
4. Review documentation files in the repository

---

## 🎉 Success!

Your Personal AI Guidance System is now ready for deployment!

**Access Points:**
- Frontend: `http://your-domain:8080` or `http://localhost:8080`
- Backend API: `http://your-domain:8000` or `http://localhost:8000`
- API Docs: `http://your-domain:8000/docs`
- Health Check: `http://your-domain:8000/health`
