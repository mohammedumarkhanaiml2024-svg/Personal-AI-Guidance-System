# 🚀 Quick Start - Build & Deploy

## Build Your Project in 3 Commands

```bash
# 1. Make build script executable
chmod +x build.sh

# 2. Run the build
./build.sh

# 3. Done! Your distribution is in dist/
ls -lh dist/
```

## What You Get

After running `./build.sh`:

```
dist/
├── personal-ai-guidance-system-1.0.0.tar.gz  ← Deploy this anywhere!
├── personal-ai-guidance-system-1.0.0.tar     ← Docker image (if available)
├── BUILD_INFO.txt                             ← Build details
├── install.sh                                 ← Run on target server
├── start.sh                                   ← Start your app
└── stop.sh                                    ← Stop your app
```

## Deploy to Production Server

```bash
# 1. Copy to server
scp dist/personal-ai-guidance-system-1.0.0.tar.gz user@server:/opt/

# 2. On server - extract
cd /opt
tar -xzf personal-ai-guidance-system-1.0.0.tar.gz

# 3. Install
./install.sh

# 4. Configure (add your API keys)
nano .env

# 5. Start
./start.sh

# 6. Access
# http://your-server:8080  ← Frontend
# http://your-server:8000  ← Backend API
```

## Use Docker (Even Easier!)

```bash
# Build image
make docker-build

# Run everything
make docker-run

# Done! App is running:
# Frontend: http://localhost:8080
# Backend: http://localhost:8000
```

## All Make Commands

```bash
make help          # Show all commands
make build         # Build distribution
make docker-build  # Build Docker image
make docker-run    # Run with Docker
make start         # Start app locally
make stop          # Stop app
make all           # Complete build
```

## Cloud Deployment Quick Guide

### AWS EC2
```bash
./build.sh
scp dist/*.tar.gz ubuntu@ec2-ip:~/
# SSH and run ./install.sh && ./start.sh
```

### Google Cloud Run
```bash
make docker-build
docker tag personal-ai-guidance-system:1.0.0 gcr.io/project/app:1.0.0
docker push gcr.io/project/app:1.0.0
gcloud run deploy app --image gcr.io/project/app:1.0.0
```

### Heroku
```bash
git push heroku main
```

## Troubleshooting

**Build fails?**
```bash
# Check Python
python3 --version  # Need 3.12+

# Install dependencies
pip install -r requirements.txt

# Try again
./build.sh
```

**Need help?**
- Read: `BUILD.md` - Complete build documentation
- Read: `DEPLOYMENT.md` - Deployment guide
- Run: `make help` - See all commands

## That's It! 🎉

Your app is ready to deploy anywhere:
- ✅ Local servers
- ✅ Cloud platforms (AWS, GCP, Azure)
- ✅ Docker containers
- ✅ Kubernetes
- ✅ Heroku/DigitalOcean

**Happy deploying!** 🚀
