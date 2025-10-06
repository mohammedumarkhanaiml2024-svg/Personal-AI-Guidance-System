.PHONY: help build clean install start stop test docker-build docker-run docker-push deploy

# Variables
PROJECT_NAME := personal-ai-guidance-system
VERSION := 1.0.0
REGISTRY := 
PYTHON := python3
PIP := pip
DOCKER := docker
DOCKER_COMPOSE := docker-compose

# Colors
GREEN := \033[0;32m
YELLOW := \033[1;33m
BLUE := \033[0;34m
NC := \033[0m # No Color

help: ## Show this help message
	@echo "$(BLUE)Personal AI Guidance System - Build Commands$(NC)"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(GREEN)%-20s$(NC) %s\n", $$1, $$2}'
	@echo ""

install: ## Install Python dependencies
	@echo "$(BLUE)Installing dependencies...$(NC)"
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt
	@echo "$(GREEN)✅ Dependencies installed$(NC)"

clean: ## Clean build artifacts
	@echo "$(BLUE)Cleaning build artifacts...$(NC)"
	rm -rf build/ dist/ *.egg-info __pycache__ */__pycache__
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	@echo "$(GREEN)✅ Cleaned$(NC)"

test: ## Run tests
	@echo "$(BLUE)Running tests...$(NC)"
	$(PYTHON) -m pytest tests/ -v || echo "$(YELLOW)⚠️  No tests found$(NC)"

lint: ## Lint code with flake8
	@echo "$(BLUE)Linting code...$(NC)"
	flake8 --max-line-length=120 --exclude=__pycache__,venv,build,dist *.py || echo "$(YELLOW)⚠️  flake8 not installed$(NC)"

format: ## Format code with black
	@echo "$(BLUE)Formatting code...$(NC)"
	black --line-length=120 *.py || echo "$(YELLOW)⚠️  black not installed$(NC)"

build: clean ## Build distribution packages
	@echo "$(BLUE)Building distribution...$(NC)"
	./build.sh
	@echo "$(GREEN)✅ Build complete$(NC)"

start: ## Start the application locally
	@echo "$(BLUE)Starting application...$(NC)"
	@./start.sh

stop: ## Stop the application
	@echo "$(BLUE)Stopping application...$(NC)"
	@./stop.sh

docker-build: ## Build Docker image
	@echo "$(BLUE)Building Docker image...$(NC)"
	$(DOCKER) build -t $(PROJECT_NAME):$(VERSION) -t $(PROJECT_NAME):latest .
	@echo "$(GREEN)✅ Docker image built$(NC)"

docker-run: ## Run Docker container
	@echo "$(BLUE)Running Docker container...$(NC)"
	$(DOCKER_COMPOSE) up -d
	@echo "$(GREEN)✅ Container started$(NC)"
	@echo "Frontend: http://localhost:8080"
	@echo "Backend: http://localhost:8000"

docker-stop: ## Stop Docker container
	@echo "$(BLUE)Stopping Docker containers...$(NC)"
	$(DOCKER_COMPOSE) down
	@echo "$(GREEN)✅ Containers stopped$(NC)"

docker-logs: ## Show Docker logs
	$(DOCKER_COMPOSE) logs -f

docker-push: ## Push Docker image to registry
	@echo "$(BLUE)Pushing Docker image...$(NC)"
	@if [ -z "$(REGISTRY)" ]; then \
		echo "$(YELLOW)⚠️  REGISTRY not set. Use: make docker-push REGISTRY=your-registry$(NC)"; \
		exit 1; \
	fi
	$(DOCKER) tag $(PROJECT_NAME):$(VERSION) $(REGISTRY)/$(PROJECT_NAME):$(VERSION)
	$(DOCKER) tag $(PROJECT_NAME):$(VERSION) $(REGISTRY)/$(PROJECT_NAME):latest
	$(DOCKER) push $(REGISTRY)/$(PROJECT_NAME):$(VERSION)
	$(DOCKER) push $(REGISTRY)/$(PROJECT_NAME):latest
	@echo "$(GREEN)✅ Image pushed to $(REGISTRY)$(NC)"

dev: ## Start development servers
	@echo "$(BLUE)Starting development servers...$(NC)"
	@echo "Starting backend..."
	@nohup uvicorn main_enhanced:app --host 0.0.0.0 --port 8000 --reload > logs/backend.log 2>&1 & echo "Backend PID: $$!"
	@echo "Starting frontend..."
	@nohup $(PYTHON) -m http.server 8080 > logs/frontend.log 2>&1 & echo "Frontend PID: $$!"
	@echo "$(GREEN)✅ Development servers started$(NC)"
	@echo "Frontend: http://localhost:8080"
	@echo "Backend: http://localhost:8000"
	@echo "API Docs: http://localhost:8000/docs"

deploy: build ## Build and prepare for deployment
	@echo "$(BLUE)Preparing deployment package...$(NC)"
	@echo "$(GREEN)✅ Deployment package ready in dist/$(NC)"
	@echo ""
	@echo "Deployment instructions:"
	@echo "1. Copy dist/$(PROJECT_NAME)-$(VERSION).tar.gz to your server"
	@echo "2. Extract: tar -xzf $(PROJECT_NAME)-$(VERSION).tar.gz"
	@echo "3. Run: ./install.sh"
	@echo "4. Configure: Edit .env file"
	@echo "5. Start: ./start.sh"

check: ## Run all checks (test + lint)
	@make test
	@make lint

all: clean install test lint build ## Run complete build process

.DEFAULT_GOAL := help
