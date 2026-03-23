#!/bin/bash

# Medical Research Agent - Development Setup Script
# Sets up local development environment without Docker

set -e

echo "🏥 Medical Research Agent - Development Setup"
echo "=============================================="
echo ""

# Check Python version
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.11+ first."
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
echo "✓ Python version: $PYTHON_VERSION"

# Check Node.js version
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 20+ first."
    exit 1
fi

NODE_VERSION=$(node --version)
echo "✓ Node.js version: $NODE_VERSION"
echo ""

# Backend setup
echo "🔧 Setting up Backend..."
echo "------------------------"

cd backend

# Create .env if it doesn't exist
if [ ! -f ".env" ]; then
    echo "Creating .env from template..."
    cp .env.example .env
    echo ""
    echo "⚠️  Please configure backend/.env with your API keys:"
    echo "  - GOOGLE_API_KEY (Required)"
    echo "  - TAVILY_API_KEY (Optional)"
    echo "  - PUBMED_EMAIL (Required)"
    echo ""
    read -p "Press Enter after configuring .env..."
fi

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "✓ Backend setup complete!"
echo ""

cd ..

# Frontend setup
echo "🔧 Setting up Frontend..."
echo "------------------------"

cd frontend

# Install dependencies
echo "Installing Node.js dependencies..."
npm install

echo "✓ Frontend setup complete!"
echo ""

cd ..

# Final instructions
echo "✅ Development Environment Ready!"
echo "================================"
echo ""
echo "To start the application:"
echo ""
echo "1. Backend (Terminal 1):"
echo "   cd backend"
echo "   source venv/bin/activate"
echo "   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"
echo ""
echo "2. Frontend (Terminal 2):"
echo "   cd frontend"
echo "   npm run dev"
echo ""
echo "3. Open http://localhost:5173 in your browser"
echo ""
echo "Or use the provided run-dev.sh script to start both services."
