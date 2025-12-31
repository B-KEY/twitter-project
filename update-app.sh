#!/bin/bash
# Update script for running container
# Run this on GCP after pushing changes to GitHub

set -e

APP_NAME="twitter-automation"

echo "🔄 Updating Twitter Automation..."
echo "================================="

# Pull latest code
echo "📥 Pulling latest changes from GitHub..."
git pull origin main

# Stop and remove old container
echo "🛑 Stopping old container..."
docker stop $APP_NAME 2>/dev/null || true
docker rm $APP_NAME 2>/dev/null || true

# Rebuild image
echo "🔨 Building new Docker image..."
docker build -f Dockerfile.gcp -t $APP_NAME:latest .

# Start new container
echo "🚀 Starting updated container..."
docker run -d \
    --name $APP_NAME \
    --network my-network \
    --restart unless-stopped \
    -p 5001:5000 \
    -e FLASK_ENV=production \
    -e ANDROID_SERIAL=192.168.0.105:35946 \
    -e ANDROID_PIN=2055 \
    $APP_NAME:latest

echo ""
echo "✅ Update complete!"
echo "📊 Container status:"
docker ps | grep $APP_NAME

echo ""
echo "📝 View logs: docker logs -f $APP_NAME"
echo "🌐 Dashboard: http://35.212.171.248:5001"
