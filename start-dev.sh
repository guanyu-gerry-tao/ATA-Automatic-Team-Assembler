#!/bin/bash
set -e

echo "🚀 Starting development environment..."

# 停止旧容器（如果存在）
echo "📦 Stopping existing containers..."
docker-compose down 2>/dev/null || true

# 启动 API 服务（后台运行）
echo "🔧 Starting API service in background..."
docker-compose up -d --build api

# 等待 API 服务启动
echo "⏳ Waiting for API to be ready..."
sleep 2

# 使用 docker-compose run 来运行 Console（交互式，可以输入）
echo "----------------------------------------"
echo "💻 Starting Console (interactive mode)..."
echo "💡 This will create a new console container"
echo "----------------------------------------"
docker-compose run --rm console
