#!/bin/bash
set -e

echo "🚀 Building Personal AI Guidance System..."

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
PROJECT_NAME="personal-ai-guidance-system"
VERSION="${VERSION:-1.0.0}"
REGISTRY="${REGISTRY:-}"

echo -e "${BLUE}=====================================${NC}"
echo -e "${BLUE}  Personal AI Guidance System Build ${NC}"
echo -e "${BLUE}  Version: ${VERSION}${NC}"
echo -e "${BLUE}=====================================${NC}"
echo ""

# Function to print section headers
print_section() {
    echo -e "\n${GREEN}▶ $1${NC}"
}

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check prerequisites
print_section "Checking prerequisites..."

if ! command_exists python3; then
    echo "❌ Python 3 is required but not installed."
    exit 1
fi
echo "✅ Python 3 found"

if ! command_exists pip; then
    echo "❌ pip is required but not installed."
    exit 1
fi
echo "✅ pip found"

# Check for Docker (optional)
if command_exists docker; then
    echo "✅ Docker found"
    DOCKER_AVAILABLE=true
else
    echo "⚠️  Docker not found (optional for containerized deployment)"
    DOCKER_AVAILABLE=false
fi

# Create build directory
print_section "Creating build directory..."
BUILD_DIR="build"
DIST_DIR="dist"
rm -rf "$BUILD_DIR" "$DIST_DIR"
mkdir -p "$BUILD_DIR" "$DIST_DIR"
echo "✅ Build directories created"

# Install/Update Python dependencies
print_section "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt
echo "✅ Dependencies installed"

# Run tests (if test file exists)
if [ -f "tests/test_main.py" ]; then
    print_section "Running tests..."
    python -m pytest tests/ -v
    echo "✅ Tests passed"
else
    echo "⚠️  No tests found, skipping..."
fi

# Lint code (if flake8 is available)
if command_exists flake8; then
    print_section "Linting code..."
    flake8 --max-line-length=120 --exclude=__pycache__,venv,build,dist *.py || true
    echo "✅ Linting complete"
fi

# Copy application files to build directory
print_section "Copying application files..."

# Backend files
cp main_enhanced.py "$BUILD_DIR/"
cp auth.py "$BUILD_DIR/"
cp models.py "$BUILD_DIR/"
cp schemas.py "$BUILD_DIR/"
cp database.py "$BUILD_DIR/"
cp utils.py "$BUILD_DIR/"
cp ai_service.py "$BUILD_DIR/"
cp google_ai_service.py "$BUILD_DIR/"
cp brain_service.py "$BUILD_DIR/"
cp private_data_store.py "$BUILD_DIR/"
cp data_privacy_service.py "$BUILD_DIR/"
cp requirements.txt "$BUILD_DIR/"

# Frontend files
cp *.html "$BUILD_DIR/" 2>/dev/null || true
cp *.css "$BUILD_DIR/" 2>/dev/null || true
cp *.js "$BUILD_DIR/" 2>/dev/null || true

# Configuration files
cp Dockerfile "$BUILD_DIR/" 2>/dev/null || true
cp docker-compose.yml "$BUILD_DIR/" 2>/dev/null || true
cp nginx.conf "$BUILD_DIR/" 2>/dev/null || true

# Documentation
cp README.md "$BUILD_DIR/" 2>/dev/null || true
cp *.md "$BUILD_DIR/" 2>/dev/null || true

echo "✅ Files copied to build directory"

# Create necessary directories in build
print_section "Creating application directories..."
mkdir -p "$BUILD_DIR/private_user_data"
mkdir -p "$BUILD_DIR/user_brains"
mkdir -p "$BUILD_DIR/logs"
echo "✅ Directories created"

# Create .env.example file
print_section "Creating environment configuration..."
cat > "$BUILD_DIR/.env.example" << EOF
# Personal AI Guidance System - Environment Configuration

# Application Settings
ENVIRONMENT=production
DEBUG=false

# Database
DATABASE_URL=sqlite:///./app.db

# Google AI (Gemini)
GOOGLE_API_KEY=your_google_api_key_here

# Security
SECRET_KEY=your_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Server
HOST=0.0.0.0
PORT=8000

# CORS
CORS_ORIGINS=*

# Logging
LOG_LEVEL=INFO
EOF
echo "✅ Environment template created"

# Build Docker image if Docker is available
if [ "$DOCKER_AVAILABLE" = true ]; then
    print_section "Building Docker image..."
    
    cd "$BUILD_DIR"
    
    if [ -n "$REGISTRY" ]; then
        IMAGE_TAG="${REGISTRY}/${PROJECT_NAME}:${VERSION}"
        IMAGE_LATEST="${REGISTRY}/${PROJECT_NAME}:latest"
    else
        IMAGE_TAG="${PROJECT_NAME}:${VERSION}"
        IMAGE_LATEST="${PROJECT_NAME}:latest"
    fi
    
    docker build -t "$IMAGE_TAG" -t "$IMAGE_LATEST" .
    
    echo "✅ Docker image built: $IMAGE_TAG"
    
    # Save Docker image to tar file
    print_section "Exporting Docker image..."
    docker save "$IMAGE_TAG" -o "../$DIST_DIR/${PROJECT_NAME}-${VERSION}.tar"
    echo "✅ Docker image exported to dist/${PROJECT_NAME}-${VERSION}.tar"
    
    cd ..
fi

# Create distribution archive
print_section "Creating distribution archive..."
tar -czf "$DIST_DIR/${PROJECT_NAME}-${VERSION}.tar.gz" -C "$BUILD_DIR" .
echo "✅ Distribution archive created: dist/${PROJECT_NAME}-${VERSION}.tar.gz"

# Create deployment scripts
print_section "Creating deployment scripts..."

# Start script
cat > "$DIST_DIR/start.sh" << 'EOF'
#!/bin/bash
echo "🚀 Starting Personal AI Guidance System..."

# Check if running with Docker
if [ -f "docker-compose.yml" ] && command -v docker-compose >/dev/null 2>&1; then
    echo "Starting with Docker Compose..."
    docker-compose up -d
    echo "✅ Application started with Docker"
    echo "   Frontend: http://localhost:8080"
    echo "   Backend API: http://localhost:8000"
    echo "   API Docs: http://localhost:8000/docs"
else
    echo "Starting with direct execution..."
    
    # Start backend
    nohup uvicorn main_enhanced:app --host 0.0.0.0 --port 8000 > logs/backend.log 2>&1 &
    BACKEND_PID=$!
    echo "Backend started with PID: $BACKEND_PID"
    
    # Start frontend
    nohup python3 -m http.server 8080 > logs/frontend.log 2>&1 &
    FRONTEND_PID=$!
    echo "Frontend started with PID: $FRONTEND_PID"
    
    echo "✅ Application started"
    echo "   Frontend: http://localhost:8080"
    echo "   Backend API: http://localhost:8000"
    echo "   API Docs: http://localhost:8000/docs"
fi
EOF

chmod +x "$DIST_DIR/start.sh"

# Stop script
cat > "$DIST_DIR/stop.sh" << 'EOF'
#!/bin/bash
echo "🛑 Stopping Personal AI Guidance System..."

# Check if running with Docker
if [ -f "docker-compose.yml" ] && command -v docker-compose >/dev/null 2>&1; then
    echo "Stopping Docker containers..."
    docker-compose down
    echo "✅ Docker containers stopped"
else
    echo "Stopping processes..."
    pkill -f "uvicorn main_enhanced:app"
    pkill -f "python.*http.server 8080"
    echo "✅ Processes stopped"
fi
EOF

chmod +x "$DIST_DIR/stop.sh"

# Installation script
cat > "$DIST_DIR/install.sh" << 'EOF'
#!/bin/bash
set -e

echo "📦 Installing Personal AI Guidance System..."

# Check Python
if ! command -v python3 >/dev/null 2>&1; then
    echo "❌ Python 3 is required but not installed."
    exit 1
fi

# Install dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Create directories
echo "Creating application directories..."
mkdir -p private_user_data user_brains logs

# Copy environment file
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo "⚠️  Please edit .env file with your configuration"
fi

echo "✅ Installation complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env file with your API keys and configuration"
echo "2. Run ./start.sh to start the application"
EOF

chmod +x "$DIST_DIR/install.sh"

echo "✅ Deployment scripts created"

# Generate build manifest
print_section "Generating build manifest..."
cat > "$DIST_DIR/BUILD_INFO.txt" << EOF
Personal AI Guidance System - Build Information
================================================

Version: ${VERSION}
Build Date: $(date '+%Y-%m-%d %H:%M:%S')
Build Host: $(hostname)
Git Commit: $(git rev-parse --short HEAD 2>/dev/null || echo "N/A")
Git Branch: $(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "N/A")

Files Included:
--------------
Backend:
- main_enhanced.py (FastAPI application)
- auth.py (Authentication)
- models.py (Database models)
- schemas.py (Pydantic schemas)
- database.py (Database configuration)
- utils.py (Utilities)
- ai_service.py (AI service)
- google_ai_service.py (Google Gemini integration)
- brain_service.py (Personal brain service)
- private_data_store.py (Data privacy)
- data_privacy_service.py (Privacy service)

Frontend:
- index.html (Login page)
- register.html (Registration page)
- overview.html (Dashboard)
- track.html (Habit tracking)
- analytics.html (Analytics)
- brain.html (AI Brain)
- chat.html (AI Chat)
- shared.css (Shared styles)
- shared.js (Shared JavaScript)

Configuration:
- Dockerfile (Container image)
- docker-compose.yml (Docker Compose)
- nginx.conf (Nginx configuration)
- requirements.txt (Python dependencies)
- .env.example (Environment template)

Scripts:
- install.sh (Installation script)
- start.sh (Start script)
- stop.sh (Stop script)

Documentation:
- README.md
- All markdown documentation files

Build Artifacts:
---------------
1. ${PROJECT_NAME}-${VERSION}.tar.gz (Source distribution)
2. ${PROJECT_NAME}-${VERSION}.tar (Docker image - if Docker available)

Installation:
------------
1. Extract: tar -xzf ${PROJECT_NAME}-${VERSION}.tar.gz
2. Run: ./install.sh
3. Configure: Edit .env file
4. Start: ./start.sh

Docker Deployment:
-----------------
1. Load image: docker load -i ${PROJECT_NAME}-${VERSION}.tar
2. Run: docker-compose up -d

Health Check:
------------
Frontend: http://localhost:8080
Backend API: http://localhost:8000
API Docs: http://localhost:8000/docs
Health: http://localhost:8000/health

EOF

echo "✅ Build manifest generated"

# Print summary
print_section "Build Summary"
echo ""
echo -e "${GREEN}✅ Build completed successfully!${NC}"
echo ""
echo "Build artifacts in dist/:"
echo "  📦 ${PROJECT_NAME}-${VERSION}.tar.gz (Source distribution)"
if [ "$DOCKER_AVAILABLE" = true ]; then
    echo "  🐳 ${PROJECT_NAME}-${VERSION}.tar (Docker image)"
fi
echo "  📄 BUILD_INFO.txt (Build manifest)"
echo "  🚀 install.sh (Installation script)"
echo "  ▶️  start.sh (Start script)"
echo "  ⏹️  stop.sh (Stop script)"
echo ""
echo -e "${YELLOW}Next steps:${NC}"
echo "1. cd dist/"
echo "2. Extract: tar -xzf ${PROJECT_NAME}-${VERSION}.tar.gz"
echo "3. Run: ./install.sh"
echo "4. Configure: Edit .env file"
echo "5. Start: ./start.sh"
echo ""
echo -e "${GREEN}Build complete! 🎉${NC}"
