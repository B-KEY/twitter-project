#!/bin/bash
# Quick setup script for GCP - Place in /tmp/ or home directory

echo "🚀 Setting up Twitter Automation..."

# GitHub repository
GITHUB_REPO="https://github.com/B-KEY/twitter-project.git"

# Configuration
APP_NAME="twitter-automation"
PORT=5001

cd ~

# Check if repo exists
if [ ! -d "$APP_NAME" ]; then
    echo "📥 Cloning repository..."
    git clone $GITHUB_REPO $APP_NAME
    cd $APP_NAME
else
    echo "📥 Updating repository..."
    cd $APP_NAME
    git pull origin main
fi

# Run the main deployment script
bash deploy-to-gcp.sh
