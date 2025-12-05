#!/bin/bash
# Start the development environment with API and console services

set -e

echo "🚀 Starting development environment..."

# Stop existing containers (if any)
echo "📦 Stopping existing containers..."
docker-compose down 2>/dev/null || true

# Start API service in the background
echo "🔧 Starting API service in background..."
docker-compose up -d --build api

# Wait for API service to be ready
echo "⏳ Waiting for API to be ready..."
sleep 2

# Run the console using docker-compose (interactive, can accept user input)
echo "----------------------------------------"
echo "💻 Starting Console (interactive mode)..."
echo "💡 This will create a new console container"
echo "----------------------------------------"
docker-compose run --rm console


