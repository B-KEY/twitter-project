#!/bin/bash
# One-command deployment script for GCP Docker
# Usage: bash deploy-to-gcp.sh

set -e

echo "🚀 Starting Twitter Automation Deployment to GCP Docker..."
echo "=================================================="

# Configuration
APP_NAME="twitter-automation"
GITHUB_REPO="https://github.com/B-KEY/twitter-project.git"
PORT=5001  # Using 5001 to avoid conflicts with existing containers
INTERNAL_PORT=5000

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}📦 Step 1: Checking for existing container...${NC}"
if docker ps -a | grep -q $APP_NAME; then
    echo -e "${YELLOW}Found existing container. Stopping and removing...${NC}"
    docker stop $APP_NAME 2>/dev/null || true
    docker rm $APP_NAME 2>/dev/null || true
fi

echo -e "${BLUE}📥 Step 2: Pulling latest code from GitHub...${NC}"
if [ -d "$APP_NAME" ]; then
    cd $APP_NAME
    git pull origin main
    cd ..
else
    git clone $GITHUB_REPO $APP_NAME
fi

echo -e "${BLUE}🔨 Step 3: Building Docker image...${NC}"
cd $APP_NAME
docker build -f Dockerfile.gcp -t $APP_NAME:latest .

echo -e "${BLUE}🌐 Step 4: Starting container...${NC}"
docker run -d \
    --name $APP_NAME \
    --network my-network \
    --restart unless-stopped \
    -p $PORT:$INTERNAL_PORT \
    -e FLASK_ENV=production \
    -e ANDROID_SERIAL=192.168.0.105:35946 \
    -e ANDROID_PIN=2055 \
    $APP_NAME:latest

echo -e "${GREEN}✅ Deployment Complete!${NC}"
echo "=================================================="
echo -e "${GREEN}🎉 Your application is now running!${NC}"
echo ""
echo "📍 Access your app at:"
echo "   External: http://35.212.171.248:$PORT"
echo "   Internal: http://10.138.0.2:$PORT"
echo ""
echo "📊 Container info:"
docker ps | grep $APP_NAME
echo ""
echo "📝 View logs: docker logs -f $APP_NAME"
echo "🛑 Stop app: docker stop $APP_NAME"
echo "🔄 Restart: docker restart $APP_NAME"
echo ""
echo -e "${BLUE}Existing containers are still running:${NC}"
docker ps --format "table {{.Names}}\t{{.Ports}}\t{{.Status}}"
