#!/bin/bash
# Update GCP container with latest code

set -e

echo "🔄 Pulling latest code from GitHub..."
git pull origin main

echo "🐳 Rebuilding Docker image..."
docker build -f Dockerfile.gcp -t twitter-automation .

echo "🛑 Stopping old container..."
docker stop twitter-automation || true
docker rm twitter-automation || true

echo "🚀 Starting new container with ZeroTier IP..."
docker run -d \
  --name twitter-automation \
  --network host \
  --restart=always \
  -e ANDROID_SERIAL=10.175.24.66:5555 \
  -e ANDROID_PIN=2055 \
  -e FLASK_ENV=production \
  twitter-automation

echo "⏳ Waiting for container to start..."
sleep 5

echo "📋 Container logs:"
docker logs twitter-automation

echo ""
echo "✅ Update complete!"
echo "🌐 Dashboard: http://35.212.171.248:5000"
echo ""
echo "📊 Check status with: docker logs -f twitter-automation"
