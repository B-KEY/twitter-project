# 🚀 One-Command GCP Deployment Guide

## Prerequisites
- GCP instance running (35.212.171.248)
- Docker installed on GCP
- SSH access to GCP instance
- GitHub account

## Step 1: Push to GitHub

### On your local Windows machine:

```powershell
# Navigate to your project
cd C:\Users\yongs\OneDrive\Desktop\CV\automation

# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit: Twitter automation with Docker support"

# Create a new repository on GitHub (https://github.com/new)
# Then add the remote (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/twitter-automation.git

# Push to GitHub
git branch -M main
git push -u origin main
```

## Step 2: Update Deployment Scripts

**IMPORTANT:** Before pushing to GitHub, update these files:

### 1. Edit `deploy-to-gcp.sh` (line 10):
```bash
GITHUB_REPO="https://github.com/YOUR_USERNAME/twitter-automation.git"
```
Change `YOUR_USERNAME` to your actual GitHub username.

### 2. Edit `README.md`:
Update all URLs with `YOUR_USERNAME` replaced.

### 3. Edit `quick-setup.sh` (line 6):
```bash
GITHUB_REPO="https://github.com/YOUR_USERNAME/twitter-automation.git"
```

## Step 3: Deploy to GCP

### SSH into your GCP instance:
```bash
ssh your-username@35.212.171.248
```

### One-Command Deployment (Choose ONE):

**Option A - Direct download and run:**
```bash
curl -sSL https://raw.githubusercontent.com/YOUR_USERNAME/twitter-automation/main/deploy-to-gcp.sh | bash
```

**Option B - Clone and run:**
```bash
git clone https://github.com/YOUR_USERNAME/twitter-automation.git
cd twitter-automation
bash deploy-to-gcp.sh
```

**Option C - Super quick setup:**
```bash
curl -sSL https://raw.githubusercontent.com/YOUR_USERNAME/twitter-automation/main/quick-setup.sh | bash
```

## Step 4: Access Your Dashboard

After deployment completes, access your app:

- **External URL:** http://35.212.171.248:5001
- **Internal URL:** http://10.138.0.2:5001

## What Happens Automatically

The deployment script will:
1. ✅ Check for existing containers (won't affect n8n or image-generator)
2. ✅ Clone/update code from GitHub
3. ✅ Build Docker image with all dependencies
4. ✅ Start container on port 5001 (internal: 5000)
5. ✅ Connect to your existing `my-network`
6. ✅ Set restart policy to `unless-stopped`
7. ✅ Configure environment variables

## Verify Deployment

```bash
# Check if container is running
docker ps | grep twitter-automation

# View logs
docker logs -f twitter-automation

# Check all containers (should see n8n, image-generator, twitter-automation)
docker ps --format "table {{.Names}}\t{{.Ports}}\t{{.Status}}"
```

## Firewall Configuration (If Needed)

If you can't access from browser, configure GCP firewall:

```bash
gcloud compute firewall-rules create twitter-automation-port \
    --allow tcp:5001 \
    --source-ranges 0.0.0.0/0 \
    --description "Allow Twitter Automation Dashboard"
```

Or use GCP Console:
1. Go to VPC Network → Firewall
2. Create Firewall Rule
3. Name: `twitter-automation-port`
4. Targets: All instances
5. Source IP ranges: `0.0.0.0/0`
6. Protocols: TCP - port 5001
7. Create

## Management Commands

```bash
# View real-time logs
docker logs -f twitter-automation

# Restart the app
docker restart twitter-automation

# Stop the app
docker stop twitter-automation

# Remove the app
docker rm -f twitter-automation

# Rebuild and restart (after code changes)
cd twitter-automation
git pull origin main
docker build -f Dockerfile.gcp -t twitter-automation:latest .
docker stop twitter-automation
docker rm twitter-automation
bash deploy-to-gcp.sh
```

## Update Application (After Changes)

When you make changes and push to GitHub:

```bash
# SSH into GCP
ssh your-username@35.212.171.248

# Navigate to app directory
cd twitter-automation

# Pull latest changes
git pull origin main

# Stop old container
docker stop twitter-automation
docker rm twitter-automation

# Rebuild image
docker build -f Dockerfile.gcp -t twitter-automation:latest .

# Start new container
docker run -d \
    --name twitter-automation \
    --network my-network \
    --restart unless-stopped \
    -p 5001:5000 \
    -e ANDROID_SERIAL=192.168.0.105:35946 \
    -e ANDROID_PIN=2055 \
    twitter-automation:latest
```

Or simply run:
```bash
cd twitter-automation
bash deploy-to-gcp.sh
```

## Mobile Access

The dashboard is fully mobile-responsive! Access from your phone:
- http://35.212.171.248:5001

Features:
- ✅ Touch-friendly interface
- ✅ Adaptive layouts
- ✅ Mobile-optimized controls
- ✅ No horizontal scrolling
- ✅ Works on all screen sizes

## Troubleshooting

### Container won't start:
```bash
docker logs twitter-automation
```

### Can't access from browser:
1. Check container is running: `docker ps`
2. Check firewall rules: `gcloud compute firewall-rules list`
3. Try internal IP if on same network: http://10.138.0.2:5001

### Device connection issues:
```bash
# Test ADB connection
docker exec -it twitter-automation adb devices

# Check environment variable
docker exec -it twitter-automation printenv ANDROID_SERIAL
```

### Port conflict:
If port 5001 is taken, edit `deploy-to-gcp.sh` and change:
```bash
PORT=5002  # Or any available port
```

## Architecture Overview

```
┌─────────────────────────────────────────────┐
│  GCP Instance (35.212.171.248)              │
│                                             │
│  ┌────────────────────────────────────┐    │
│  │  Docker Network: my-network         │    │
│  │                                     │    │
│  │  ┌──────────────┐  Port 5678       │    │
│  │  │     n8n      ├──────────────────┼────┤→ External
│  │  └──────────────┘                   │    │
│  │                                     │    │
│  │  ┌──────────────┐  Port 9000       │    │
│  │  │image-        ├──────────────────┼────┤→ External
│  │  │generator     │                   │    │
│  │  └──────────────┘                   │    │
│  │                                     │    │
│  │  ┌──────────────┐  Port 5001       │    │
│  │  │twitter-      ├──────────────────┼────┤→ External
│  │  │automation    │                   │    │
│  │  └──────┬───────┘                   │    │
│  │         │                           │    │
│  │         └──WiFi ADB─────────────────┼────┤→ 192.168.0.105:35946
│  └────────────────────────────────────┘    │
└─────────────────────────────────────────────┘
```

## Support

If you encounter issues:
1. Check logs: `docker logs twitter-automation`
2. Verify network: `docker network inspect my-network`
3. Test connectivity: `docker exec -it twitter-automation ping 192.168.0.105`
4. Check container health: `docker inspect twitter-automation | grep Health -A 10`

## Next Steps

After deployment:
1. ✅ Test the dashboard (http://35.212.171.248:5001)
2. ✅ Try submitting a tweet URL
3. ✅ Monitor real-time logs
4. ✅ Test on mobile device
5. ✅ Set up monitoring/alerts (optional)

Enjoy your automated Twitter engagement! 🎉
