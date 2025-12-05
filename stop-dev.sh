#!/bin/bash
# Stop all Docker containers for the development environment

set -e

echo "🛑 Stopping development environment..."
docker-compose down
echo "✅ All services stopped."
