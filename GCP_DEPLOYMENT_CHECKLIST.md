# GCP Deployment Checklist

## Pre-Deployment Checklist

### ☐ Prerequisites
- [ ] GCP Account created (free tier available)
- [ ] gcloud CLI installed (`gcloud --version`)
- [ ] gcloud authenticated (`gcloud auth login`)
- [ ] Project created in GCP
- [ ] Project ID noted down
- [ ] Billing enabled on GCP account
- [ ] Docker installed locally (for testing)

### ☐ Local Testing
- [ ] Code verified locally
- [ ] `docker build -f Dockerfile.gcp -t test .` works
- [ ] `docker run -p 5000:5000 test` runs without errors
- [ ] Dashboard loads at `http://localhost:5000`
- [ ] All environment variables verified

### ☐ Configuration Review
- [ ] `ANDROID_SERIAL=192.168.0.105:35587` is correct
- [ ] `ANDROID_PIN` is set correctly
- [ ] `FLASK_ENV=production` confirmed
- [ ] Port 5000 is available
- [ ] No sensitive data in Dockerfile

---

## Cloud Run Deployment (RECOMMENDED)

### ☐ Setup Phase
- [ ] Navigate to project directory: `cd /path/to/automation`
- [ ] GCP project set: `gcloud config set project YOUR_PROJECT_ID`
- [ ] Verify project: `gcloud config list`
- [ ] Cloud Run API enabled: `gcloud services enable run.googleapis.com`

### ☐ Build Phase
- [ ] Build command ready:
  ```bash
  gcloud run deploy twitter-automation \
      --source . \
      --dockerfile Dockerfile.gcp \
      --platform managed \
      --region us-central1 \
      --port 5000 \
      --memory 512Mi \
      --timeout 600 \
      --set-env-vars "FLASK_ENV=production,ANDROID_SERIAL=192.168.0.105:35587" \
      --allow-unauthenticated
  ```
- [ ] Copy deploy command
- [ ] Execute deploy command
- [ ] Wait for build to complete (2-3 minutes)

### ☐ Post-Deployment
- [ ] Deployment successful message shown
- [ ] Service URL obtained: `https://twitter-automation-xxxxx.run.app`
- [ ] URL copied to clipboard
- [ ] Test URL in browser
- [ ] Dashboard loads successfully
- [ ] All UI elements visible
- [ ] Network info shows correct endpoint

### ☐ Verify Functionality
- [ ] Dashboard accessible
- [ ] Job queue visible
- [ ] API endpoints respond
- [ ] CORS headers present
- [ ] No console errors in browser

### ☐ Monitor Initial Deployment
- [ ] Check Cloud Run console
- [ ] Verify no errors in recent requests
- [ ] Check CPU/Memory metrics
- [ ] Confirm instance count (should be 1)
- [ ] Check logs for any warnings

---

## Compute Engine Deployment (FULL AUTOMATION)

### ☐ VM Setup Phase
- [ ] VM creation command ready
- [ ] Machine type selected (e2-small recommended)
- [ ] Zone selected (us-central1-a)
- [ ] Startup script prepared
- [ ] Firewall rules planned

### ☐ VM Creation
- [ ] Create VM with startup script
- [ ] Wait for VM to boot (2-3 minutes)
- [ ] Verify VM created in GCP Console
- [ ] Note down VM external IP address
- [ ] Check VM status is "running"

### ☐ Post-VM Creation
- [ ] SSH access verified
- [ ] Docker installed on VM
- [ ] Docker service running
- [ ] User added to docker group
- [ ] Repository cloned on VM

### ☐ Docker Deployment on VM
- [ ] docker-compose.gcp.yml uploaded/present
- [ ] Environment variables configured
- [ ] Volumes mounted correctly
- [ ] `docker-compose -f docker-compose.gcp.yml up -d` executed
- [ ] Containers running: `docker ps`
- [ ] No errors in container logs

### ☐ Network Configuration
- [ ] Firewall rule created for port 5000
- [ ] Rule allows incoming TCP traffic
- [ ] Source IP ranges appropriate
- [ ] VPN configured (if using local device)
- [ ] Network connectivity tested

### ☐ Verify VM Deployment
- [ ] Dashboard accessible at `http://vm-ip:5000`
- [ ] All UI elements loading
- [ ] No connection errors
- [ ] Logs look clean
- [ ] Resource usage reasonable

---

## Local Automation Setup (HYBRID)

### ☐ Configuration
- [ ] `ANDROID_SERIAL` in script: `192.168.0.105:35587`
- [ ] `ANDROID_PIN` environment variable set
- [ ] Device IP address correct
- [ ] Device ADB port correct (35587)
- [ ] WiFi connection to device available

### ☐ Testing
- [ ] Test ADB connection: `adb connect 192.168.0.105:35587`
- [ ] Device shows in `adb devices`
- [ ] Test automation locally: `python src/working_twitter_automation.py "test_url"`
- [ ] Job completes successfully
- [ ] Output is readable

### ☐ Integration
- [ ] Local automation can reach cloud dashboard
- [ ] Dashboard API endpoints accessible
- [ ] Job queue updates visible
- [ ] Status polling works
- [ ] Output logging functional

---

## Post-Deployment Verification

### ☐ Dashboard Testing
- [ ] Home page loads
- [ ] All stats display
- [ ] Accounts section shows 7 accounts
- [ ] Network address visible
- [ ] Responsive on mobile

### ☐ API Testing
- [ ] GET `/api/network-info` returns data
- [ ] GET `/api/jobs` returns data
- [ ] Can submit test job
- [ ] Job status updates
- [ ] Output displays in console

### ☐ Security Check
- [ ] CORS headers present
- [ ] No sensitive data exposed
- [ ] Error messages are vague (not revealing internals)
- [ ] Authentication considered (if needed)
- [ ] Firewall rules restrictive

### ☐ Performance Check
- [ ] Dashboard loads in <2 seconds
- [ ] No memory leaks
- [ ] CPU usage reasonable
- [ ] Network bandwidth acceptable
- [ ] Scale limits understood

### ☐ Logging & Monitoring
- [ ] Logs are accessible
- [ ] Error logs are clean
- [ ] Performance metrics visible
- [ ] Alerts can be configured
- [ ] Cost tracking enabled

---

## Integration Checklist

### ☐ Cloud + Local Connection
- [ ] Dashboard sends API calls to local automation
- [ ] Local automation responds to API calls
- [ ] Job queue syncs between cloud and local
- [ ] Status updates visible on dashboard
- [ ] Output logs transferring correctly

### ☐ Device Connection
- [ ] Device reachable from local automation
- [ ] ADB commands execute successfully
- [ ] Device responds to automation
- [ ] Status updates visible
- [ ] No latency issues

### ☐ End-to-End Test
- [ ] Access cloud dashboard
- [ ] Submit job via cloud interface
- [ ] Local automation picks up job
- [ ] Device executes automation
- [ ] Results display on dashboard
- [ ] Everything completes successfully

---

## Troubleshooting Checklist

### ☐ If Dashboard Won't Load
- [ ] Check Cloud Run status: `gcloud run services describe twitter-automation`
- [ ] Check service logs: `gcloud logs read --limit 50`
- [ ] Verify URL is correct
- [ ] Check browser console for errors
- [ ] Try incognito mode
- [ ] Clear browser cache

### ☐ If Automation Won't Run
- [ ] Verify local PC is on
- [ ] Check automation script is running
- [ ] Test ADB connection: `adb devices`
- [ ] Verify device is reachable
- [ ] Check network connectivity
- [ ] Review automation logs

### ☐ If Device Won't Connect
- [ ] Restart device WiFi
- [ ] Verify IP address: `adb shell ip addr`
- [ ] Check device has WiFi enabled
- [ ] Restart ADB: `adb kill-server && adb start-server`
- [ ] Try connecting again: `adb connect 192.168.0.105:35587`

### ☐ If Costs Are High
- [ ] Check Cloud Run metrics
- [ ] Review Compute Engine instance type
- [ ] Consider auto-scaling policies
- [ ] Check for failed requests
- [ ] Review timeout settings
- [ ] Optimize image size

---

## Cleanup Checklist (If Removing)

### ☐ Cloud Run Cleanup
- [ ] Delete Cloud Run service: `gcloud run services delete twitter-automation`
- [ ] Delete container images: `gcloud container images delete gcr.io/PROJECT/twitter-automation`
- [ ] Verify deletion in console

### ☐ Compute Engine Cleanup
- [ ] Stop VM: `gcloud compute instances stop twitter-automation`
- [ ] Delete VM: `gcloud compute instances delete twitter-automation`
- [ ] Delete firewall rules: `gcloud compute firewall-rules delete allow-flask-xxxx`
- [ ] Verify deletion in console

### ☐ GCP Project Cleanup
- [ ] Disable Cloud Run API
- [ ] Disable Compute Engine API
- [ ] Remove billing alerts
- [ ] Review for unused resources
- [ ] Final cost review

---

## Documentation Checklist

### ☐ Before Deployment
- [ ] Read GCP_QUICK_REFERENCE.md
- [ ] Review GCP_ARCHITECTURE_DIAGRAMS.md
- [ ] Review GCP_COMPLETE_GUIDE.md

### ☐ After Deployment
- [ ] Document deployed URL
- [ ] Document VM IP (if used)
- [ ] Document access credentials (if any)
- [ ] Document deployment date
- [ ] Document configuration used
- [ ] Update team on availability

---

## Success Criteria

✅ **Deployment is successful when:**
1. Dashboard is accessible from cloud URL
2. Dashboard displays all UI elements
3. Local automation can reach cloud API
4. Jobs can be queued from cloud dashboard
5. Local automation executes queued jobs
6. Device receives ADB commands
7. Results display on cloud dashboard
8. No errors in logs
9. Performance is acceptable
10. Cost is within expectations

---

## Timeline Estimate

| Step | Time | Total |
|------|------|-------|
| Pre-deployment setup | 5 min | 5 min |
| Local testing | 5 min | 10 min |
| Cloud Run deployment | 5 min | 15 min |
| Deployment waiting | 3 min | 18 min |
| Verification | 5 min | 23 min |
| Integration test | 10 min | 33 min |
| **TOTAL** | | **~35 minutes** |

---

**Ready to deploy?** Start with the checklist items in order and check them off as you go.

Good luck! 🚀
