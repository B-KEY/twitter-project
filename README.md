# Twitter/X Automation Project

Automated Twitter engagement system with a modern web dashboard.

## Features

- 🎯 Multi-account Twitter automation via WiFi ADB
- 📊 Real-time dashboard with live status updates
- 🔒 Auto-lock device after completion
- 🎨 Professional, mobile-responsive UI
- 🐳 Docker-ready for easy deployment

## Quick Deploy to GCP

1. **SSH into your GCP instance:**
   ```bash
   ssh your-username@35.212.171.248
   ```

2. **Run the one-command deployment:**
   ```bash
   curl -sSL https://raw.githubusercontent.com/YOUR_USERNAME/twitter-automation/main/deploy-to-gcp.sh | bash
   ```

   Or manually:
   ```bash
   git clone https://github.com/YOUR_USERNAME/twitter-automation.git
   cd twitter-automation
   bash deploy-to-gcp.sh
   ```

3. **Access your dashboard:**
   - External: `http://35.212.171.248:5001`
   - Internal: `http://10.138.0.2:5001`

That's it! 🎉

## Local Development

### Web Interface (Recommended)
```powershell
# Install dependencies
pip install -r requirements.txt

# Run the web app
python src/web_app.py

# Open browser to http://localhost:5000
```

### Command Line
```powershell
# From the project root
python .\src\working_twitter_automation.py "https://x.com/...."
```

## Configuration

Set these environment variables (optional):

```bash
export ANDROID_SERIAL="192.168.0.105:35946"  # Your WiFi ADB device
export ANDROID_PIN="2055"                      # Device PIN
```

## Manual Deployment (Alternative)

```bash
# Build the Docker image
docker build -f Dockerfile.gcp -t twitter-automation:latest .

# Run the container
docker run -d \
  --name twitter-automation \
  --network my-network \
  --restart unless-stopped \
  -p 5001:5000 \
  -e ANDROID_SERIAL=192.168.0.105:35946 \
  -e ANDROID_PIN=2055 \
  twitter-automation:latest
```

## Management Commands

```bash
# View logs
docker logs -f twitter-automation

# Restart
docker restart twitter-automation

# Stop
docker stop twitter-automation

# Remove
docker rm -f twitter-automation
```

## Architecture

- **Backend:** Flask (Python 3.12)
- **Frontend:** Modern HTML/CSS/JavaScript
- **Automation:** uiautomator2 + WiFi ADB
- **Container:** Docker with health checks
- **Network:** Custom bridge network (my-network)

## Port Configuration

- Internal: 5000 (Flask app inside container)
- External: 5001 (Host port, mapped to avoid conflicts)
- Won't affect existing containers (n8n:5678, image-generator:9000)

## Mobile Support

Dashboard is fully responsive and optimized for mobile devices with:
- Touch-friendly interface
- Adaptive layouts
- Mobile-first design
- No horizontal scrolling

## Structure
- src/working_twitter_automation.py — automation script
- src/web_app.py — Flask web interface
- templates/ — HTML templates
- static/ — static assets
- scripts/run.ps1 — PowerShell runner
- tests/ — test files
- ui_dumps/ — UI dump output (ignored by git)
- requirements.txt — Python dependencies
- Dockerfile.gcp — Docker image for GCP
- docker-compose.yml — Docker compose setup
- .gitignore — ignored files

## Security

- Non-root user in container
- Health checks enabled
- Auto-lock device feature
- Environment-based configuration

## Requirements

- Docker installed on GCP instance
- WiFi ADB device accessible from network
- Python 3.12+ (containerized)

## Troubleshooting

**Container won't start:**
```bash
docker logs twitter-automation
```

**Can't access from browser:**
- Check GCP firewall rules for port 5001
- Verify container is running: `docker ps`

**Device connection issues:**
- Verify WiFi ADB is enabled: `adb connect 192.168.0.105:35946`
- Check ANDROID_SERIAL environment variable

## License

MIT
