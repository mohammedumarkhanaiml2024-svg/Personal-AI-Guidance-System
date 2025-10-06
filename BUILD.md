# 📦 Build System Documentation

## Overview

This project includes a comprehensive build system for creating production-ready deployments of the Personal AI Guidance System.

## 🏗️ Build Files

### Core Build Files

1. **`build.sh`** - Main build script
   - Creates distribution packages
   - Builds Docker images
   - Generates deployment artifacts
   - Creates installation scripts

2. **`Makefile`** - Build automation
   - Provides convenient commands
   - Manages dependencies
   - Handles Docker operations
   - Runs tests and linting

3. **`Dockerfile`** - Container image definition
   - Multi-stage build for optimization
   - Production-ready configuration
   - Health checks included

4. **`docker-compose.yml`** - Multi-container orchestration
   - Backend service
   - Frontend service (Nginx)
   - Network configuration
   - Volume management

5. **`nginx.conf`** - Web server configuration
   - Static file serving
   - API reverse proxy
   - CORS headers
   - Caching strategy

## 🚀 Quick Start

### Using build.sh

```bash
# Make executable (first time only)
chmod +x build.sh

# Run build
./build.sh

# Build with custom version
VERSION=2.0.0 ./build.sh

# Build with registry
REGISTRY=myregistry.com ./build.sh
```

### Using Makefile

```bash
# Show all commands
make help

# Install dependencies
make install

# Build everything
make all

# Docker build
make docker-build

# Run with Docker
make docker-run
```

## 📋 Available Make Commands

| Command | Description |
|---------|-------------|
| `make help` | Show all available commands |
| `make install` | Install Python dependencies |
| `make clean` | Clean build artifacts |
| `make test` | Run tests |
| `make lint` | Lint code with flake8 |
| `make format` | Format code with black |
| `make build` | Build distribution packages |
| `make start` | Start application locally |
| `make stop` | Stop application |
| `make docker-build` | Build Docker image |
| `make docker-run` | Run with Docker Compose |
| `make docker-stop` | Stop Docker containers |
| `make docker-logs` | View Docker logs |
| `make docker-push` | Push to registry |
| `make dev` | Start development servers |
| `make deploy` | Prepare deployment |
| `make check` | Run tests and lint |
| `make all` | Complete build process |

## 📦 Build Outputs

After running `./build.sh` or `make build`, you'll get:

### In `dist/` directory:

1. **`personal-ai-guidance-system-1.0.0.tar.gz`**
   - Complete source distribution
   - All application files
   - Documentation
   - Configuration templates

2. **`personal-ai-guidance-system-1.0.0.tar`** (if Docker available)
   - Docker image export
   - Ready to load on any system

3. **`BUILD_INFO.txt`**
   - Build manifest
   - Version information
   - File listing
   - Deployment instructions

4. **`install.sh`**
   - Automated installation
   - Dependency setup
   - Directory creation

5. **`start.sh`**
   - Start the application
   - Works with both Docker and direct execution

6. **`stop.sh`**
   - Stop all services
   - Clean shutdown

## 🐳 Docker Build

### Build Image

```bash
# Using Makefile
make docker-build

# Using docker directly
docker build -t personal-ai-guidance-system:1.0.0 .

# With build args
docker build --build-arg VERSION=1.0.0 -t personal-ai-guidance-system:1.0.0 .
```

### Run Container

```bash
# Using Docker Compose (recommended)
docker-compose up -d

# Using docker run
docker run -d \
  --name ai-guidance \
  -p 8000:8000 \
  -p 8080:80 \
  -v $(pwd)/private_user_data:/app/private_user_data \
  -e GOOGLE_API_KEY=your_key \
  personal-ai-guidance-system:1.0.0
```

## 📝 Build Configuration

### Environment Variables

Configure the build with environment variables:

```bash
# Version
VERSION=1.0.0 ./build.sh

# Docker registry
REGISTRY=myregistry.com ./build.sh

# Combined
VERSION=2.0.0 REGISTRY=myregistry.com ./build.sh
```

### Build Options

Customize the build in `build.sh`:

- `PROJECT_NAME` - Project name
- `VERSION` - Version number
- `REGISTRY` - Docker registry URL

## 🔄 CI/CD Integration

### GitHub Actions

The project includes `.github/workflows/build-and-deploy.yml` for automated:

- **Testing** on every push/PR
- **Building** on main branch
- **Docker image creation** and push to GitHub Container Registry
- **Release creation** on version tags

### Trigger Release

```bash
# Create and push a version tag
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin v1.0.0

# GitHub Actions will automatically:
# 1. Run tests
# 2. Build distribution
# 3. Create Docker image
# 4. Create GitHub release
```

## 📊 Build Process

### Step-by-Step

1. **Prerequisites Check**
   - Verify Python installation
   - Check for Docker (optional)
   - Validate dependencies

2. **Dependency Installation**
   - Update pip
   - Install requirements.txt

3. **Code Quality**
   - Run tests (if available)
   - Lint code (if flake8 available)

4. **File Preparation**
   - Copy application files
   - Copy frontend files
   - Copy documentation

5. **Directory Structure**
   - Create data directories
   - Set up logs folder
   - Configure permissions

6. **Configuration**
   - Generate .env.example
   - Create deployment scripts

7. **Docker Build** (if available)
   - Build container image
   - Export to tar file
   - Tag versions

8. **Distribution Archive**
   - Create tar.gz package
   - Include all files
   - Generate manifest

9. **Deployment Scripts**
   - Create install.sh
   - Create start.sh
   - Create stop.sh

## 🎯 Deployment Scenarios

### Scenario 1: Simple Deployment

```bash
# Build
./build.sh

# Copy to server
scp dist/personal-ai-guidance-system-1.0.0.tar.gz user@server:/opt/

# On server
cd /opt
tar -xzf personal-ai-guidance-system-1.0.0.tar.gz
./install.sh
./start.sh
```

### Scenario 2: Docker Deployment

```bash
# Build and load
./build.sh
docker load -i dist/personal-ai-guidance-system-1.0.0.tar

# Run
docker-compose up -d
```

### Scenario 3: Cloud Deployment

```bash
# Build and push
make docker-build
make docker-push REGISTRY=gcr.io/my-project

# Deploy to cloud
gcloud run deploy ai-guidance --image gcr.io/my-project/personal-ai-guidance-system:1.0.0
```

## 🛠️ Customization

### Modify Build Script

Edit `build.sh` to customize:

```bash
# Change project name
PROJECT_NAME="my-custom-name"

# Change default version
VERSION="${VERSION:-2.0.0}"

# Add custom build steps
# ... your custom code ...
```

### Modify Dockerfile

Edit `Dockerfile` to customize:

```dockerfile
# Change base image
FROM python:3.11-slim

# Add additional dependencies
RUN apt-get install -y additional-package

# Modify entry point
CMD ["custom-command"]
```

### Modify docker-compose.yml

Edit `docker-compose.yml` to customize:

```yaml
services:
  backend:
    environment:
      - CUSTOM_ENV=value
    ports:
      - "9000:8000"  # Custom port
```

## 📈 Performance Optimization

### Multi-stage Build

The Dockerfile uses multi-stage builds:

```dockerfile
# Stage 1: Builder
FROM python:3.12-slim as builder
# ... install dependencies ...

# Stage 2: Production
FROM python:3.12-slim
COPY --from=builder /root/.local /root/.local
# ... smaller final image ...
```

### Caching

Docker build uses caching:

- Requirements installed first (cached)
- Application files copied last
- Faster rebuilds

## 🔍 Troubleshooting

### Build Fails

**Check Python version:**
```bash
python3 --version  # Should be 3.12+
```

**Check permissions:**
```bash
chmod +x build.sh
```

**Check disk space:**
```bash
df -h
```

### Docker Build Fails

**Check Docker:**
```bash
docker --version
docker info
```

**Clean Docker cache:**
```bash
docker system prune -a
```

### Tests Fail

**Install test dependencies:**
```bash
pip install pytest
```

**Run tests manually:**
```bash
python -m pytest tests/ -v
```

## 📚 Additional Resources

- **DEPLOYMENT.md** - Complete deployment guide
- **README.md** - Project documentation
- **requirements.txt** - Python dependencies
- **.github/workflows/** - CI/CD configuration

## ✅ Build Checklist

Before deployment:

- [ ] Update VERSION in build.sh
- [ ] Update requirements.txt
- [ ] Run tests: `make test`
- [ ] Lint code: `make lint`
- [ ] Build locally: `make build`
- [ ] Test Docker build: `make docker-build`
- [ ] Test Docker run: `make docker-run`
- [ ] Review BUILD_INFO.txt
- [ ] Test installation on clean system
- [ ] Update documentation
- [ ] Create git tag for release

## 🎉 Success!

Your build system is now ready to create production deployments!

For questions or issues, check:
1. Build logs in the terminal
2. Docker logs: `docker-compose logs`
3. Application logs in `logs/` directory
4. DEPLOYMENT.md for detailed instructions
