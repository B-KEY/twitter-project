# Automation

Twitter/X automation using uiautomator2. This project organizes your existing script without modifying its content.

## Structure
- src/working_twitter_automation.py — your original script (content unchanged)
- scripts/run.ps1 — convenience PowerShell runner
- tests/ — placeholder for future tests
- ui_dumps/ — local UI dump output (ignored by git)
- requirements.txt — Python dependencies
- Dockerfile — Docker image configuration
- docker-compose.yml — Docker compose setup
- .gitignore — ignores typical Python artifacts and `ui_dumps/`

## Quick Start

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

### Docker Usage
```bash
# Build and run web interface with docker-compose
docker-compose build
docker-compose up

# Access at http://localhost:5000

# Or run CLI automation
docker-compose run --rm twitter-automation python src/working_twitter_automation.py "https://x.com/..."
```

**Note**: Docker setup requires USB device access for ADB connection to Android devices. On Windows, you may need to use WSL2 and USB/IP forwarding.

## Optional: Runner
Use `scripts/run.ps1` for a simpler command.
