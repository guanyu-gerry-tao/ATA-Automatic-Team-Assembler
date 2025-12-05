#!/bin/bash
# Connect to the console container for interactive CLI access

set -e

# Check if the console container is running
if ! docker ps | grep -q ata-console; then
    echo "❌ Console container is not running. Please run './start-dev.sh' first."
    exit 1
fi

echo "🔗 Connecting to Console..."
echo "----------------------------------------"
docker exec -it ata-console python3 -m ATA.main


