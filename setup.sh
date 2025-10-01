#!/bin/bash

# Installation & Testing Script for Personal AI Guidance System
# This script installs dependencies and runs tests

echo "========================================="
echo "Personal AI Guidance System Setup"
echo "========================================="
echo ""

# Check Python version
echo "Checking Python version..."
python3 --version
echo ""

# Create virtual environment (optional but recommended)
echo "Creating virtual environment..."
python3 -m venv venv
echo "✓ Virtual environment created"
echo ""

# Activate virtual environment
echo "To activate virtual environment, run:"
echo "  source venv/bin/activate  (Linux/Mac)"
echo "  venv\\Scripts\\activate     (Windows)"
echo ""

# Install dependencies
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt
echo "✓ Dependencies installed"
echo ""

# Create database tables
echo "Setting up database..."
python3 -c "from database import Base, engine; import models; Base.metadata.create_all(bind=engine); print('✓ Database tables created')"
echo ""

# Test imports
echo "Testing imports..."
python3 -c "import fastapi, sqlalchemy, pydantic; print('✓ Core packages imported successfully')"
echo ""

echo "========================================="
echo "Setup Complete!"
echo "========================================="
echo ""
echo "Next steps:"
echo "1. Start the server: python -m uvicorn main_enhanced:app --reload"
echo "2. Run the demo: python demo_example.py"
echo "3. Visit API docs: http://localhost:8000/docs"
echo ""
