#!/bin/bash

# Medical Research Agent - Quick Start Script
# This script helps you set up and run the Medical Research Agent quickly

set -e

echo "🏥 Medical Research Agent - Quick Start"
echo "========================================"
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    echo "Visit: https://docs.docker.com/get-docker/"
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Check if .env file exists
if [ ! -f "backend/.env" ]; then
    echo "📝 Creating backend/.env from template..."
    cp backend/.env.example backend/.env
    echo ""
    echo "⚠️  IMPORTANT: You need to configure your API keys in backend/.env"
    echo ""
    echo "Required:"
    echo "  - GOOGLE_API_KEY (Get from: https://aistudio.google.com/app/apikey)"
    echo "  - PUBMED_EMAIL (Your email address for NCBI)"
    echo ""
    echo "Optional:"
    echo "  - TAVILY_API_KEY (Get from: https://tavily.com)"
    echo ""
    read -p "Press Enter after you've configured backend/.env with your API keys..."
fi

# Verify GOOGLE_API_KEY is set
if ! grep -q "GOOGLE_API_KEY=.*[a-zA-Z0-9]" backend/.env; then
    echo ""
    echo "❌ GOOGLE_API_KEY is not configured in backend/.env"
    echo "Please add your Google AI API key and try again."
    exit 1
fi

echo ""
echo "🚀 Starting Medical Research Agent..."
echo ""

# Build and start services
if docker compose version &> /dev/null; then
    docker compose up --build
else
    docker-compose up --build
fi
