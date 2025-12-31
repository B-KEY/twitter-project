# ✅ Pre-Deployment Checklist

Before pushing to GitHub, complete these steps:

## 1. Update GitHub Username

- [ ] Open `deploy-to-gcp.sh`
  - Line 10: Replace `YOUR_USERNAME` with your actual GitHub username
  
- [ ] Open `quick-setup.sh`
  - Line 6: Replace `YOUR_USERNAME` with your actual GitHub username
  
- [ ] Open `README.md`
  - Search for `YOUR_USERNAME` (appears ~6 times)
  - Replace all with your actual GitHub username

## 2. Verify Files Exist

- [ ] `deploy-to-gcp.sh` ✅
- [ ] `quick-setup.sh` ✅
- [ ] `update-app.sh` ✅
- [ ] `Dockerfile.gcp` ✅
- [ ] `requirements.txt` ✅
- [ ] `src/web_app.py` ✅
- [ ] `src/working_twitter_automation.py` ✅
- [ ] `templates/index.html` ✅ (mobile-responsive)
- [ ] `static/` directory ✅
- [ ] `README.md` ✅
- [ ] `DEPLOYMENT.md` ✅
- [ ] `QUICK_START.md` ✅
- [ ] `.gitignore` ✅

## 3. Test Locally (Optional)

```powershell
# Test web app locally
python src\web_app.py

# Open browser: http://localhost:5000
# Verify mobile responsiveness (press F12, toggle device toolbar)
```

## 4. Push to GitHub

```powershell
# Initialize git (if not done)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit: Twitter automation with GCP deployment"

# Create repository on GitHub
# Go to: https://github.com/new
# Repository name: twitter-automation
# Public or Private: Your choice
# Don't initialize with README (we already have one)

# Add remote (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/twitter-automation.git

# Push
git branch -M main
git push -u origin main
```

## 5. Deploy to GCP

```bash
# SSH to GCP
ssh your-username@35.212.171.248

# One-line deployment
curl -sSL https://raw.githubusercontent.com/YOUR_USERNAME/twitter-automation/main/deploy-to-gcp.sh | bash
```

## 6. Configure Firewall (If Needed)

If you can't access the dashboard from browser:

```bash
gcloud compute firewall-rules create twitter-automation-port \
    --allow tcp:5001 \
    --source-ranges 0.0.0.0/0 \
    --description "Allow Twitter Automation Dashboard"
```

Or use GCP Console → VPC Network → Firewall → Create Rule

## 7. Verify Deployment

- [ ] Container is running: `docker ps | grep twitter-automation`
- [ ] No errors in logs: `docker logs twitter-automation`
- [ ] Dashboard accessible: http://35.212.171.248:5001
- [ ] Mobile responsive: Test on phone
- [ ] Existing containers still running: `docker ps`

## 8. Test Functionality

- [ ] Submit a tweet URL
- [ ] Monitor real-time logs
- [ ] Check session info updates
- [ ] Verify actions display correctly
- [ ] Test on mobile device

## Success! 🎉

Your Twitter automation is now deployed and running on GCP!

---

## Quick Reference

**Dashboard:** http://35.212.171.248:5001  
**Logs:** `docker logs -f twitter-automation`  
**Restart:** `docker restart twitter-automation`  
**Update:** `cd twitter-automation && bash update-app.sh`  

**Port Allocation:**
- n8n: 5678 ✅
- image-generator: 9000 ✅
- twitter-automation: 5001 ⭐ NEW

No conflicts, all running together on `my-network`!
