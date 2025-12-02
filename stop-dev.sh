#!/bin/bash
set -e

echo "🛑 Stopping development environment..."
docker-compose down
echo "✅ All services stopped."
