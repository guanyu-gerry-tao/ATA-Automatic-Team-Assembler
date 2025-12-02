#!/bin/bash
set -e

# 检查容器是否在运行
if ! docker ps | grep -q ata-console; then
    echo "❌ Console container is not running. Please run './start-dev.sh' first."
    exit 1
fi

echo "🔗 Connecting to Console..."
echo "----------------------------------------"
docker exec -it ata-console python3 -m ATA.main

