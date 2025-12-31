from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import subprocess
import os
import threading

# Get WiFi IP from environment or use default
WIFI_IP = os.getenv("ANDROID_SERIAL", "192.168.0.105:35946")

app = Flask(__name__, template_folder='../templates', static_folder='../static')
CORS(app)

# Store job status
jobs = {}
job_counter = 0

def run_automation(job_id, tweet_url):
    """Run the automation script in a separate thread with real-time output streaming."""
    global jobs
    try:
        jobs[job_id]['status'] = 'running'
        jobs[job_id]['output'] = ''
        print(f"\n{'='*60}")
        print(f"[JOB {job_id}] Starting automation for: {tweet_url}")
        print(f"{'='*60}\n")
        
        # Get the Python executable path
        script_path = os.path.join(os.path.dirname(__file__), 'working_twitter_automation.py')
        
        # Prefer WiFi ADB device to avoid multi-device ambiguity
        env = os.environ.copy()
        env.setdefault('ANDROID_SERIAL', WIFI_IP)

        # Start the process with streaming output
        process = subprocess.Popen(
            ['python', script_path, tweet_url],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding='utf-8',
            errors='replace',
            bufsize=1,  # Line buffered
            universal_newlines=True,
            env=env
        )
        
        # Stream output line by line
        for line in iter(process.stdout.readline, ''):
            if line:
                # Append to job output in real-time
                jobs[job_id]['output'] += line
                # Also print to server console
                print(f"[JOB {job_id}] {line}", end='')
        
        # Wait for process to complete
        process.wait()
        
        if process.returncode == 0:
            jobs[job_id]['status'] = 'completed'
            print(f"\n[JOB {job_id}] ✓ Completed successfully\n")
        else:
            jobs[job_id]['status'] = 'failed'
            jobs[job_id]['error'] = f"Process exited with code {process.returncode}"
            print(f"\n[JOB {job_id}] ✗ Failed with return code {process.returncode}\n")
            
    except Exception as e:
        jobs[job_id]['status'] = 'failed'
        jobs[job_id]['error'] = str(e)
        print(f"\n[JOB {job_id}] ✗ Exception: {e}\n")

@app.route('/')
def index():
    """Render the main page."""
    return render_template('index.html', wifi_ip=WIFI_IP)

@app.route('/api/run', methods=['POST'])
def run_automation_api():
    """API endpoint to trigger automation."""
    global job_counter, jobs
    
    data = request.json
    tweet_url = data.get('tweet_url', '').strip()
    
    if not tweet_url:
        return jsonify({'error': 'Tweet URL is required'}), 400
    
    if not (tweet_url.startswith('https://x.com/') or tweet_url.startswith('https://twitter.com/')):
        return jsonify({'error': 'Invalid Twitter/X URL'}), 400
    
    # Create a new job
    job_counter += 1
    job_id = job_counter
    
    jobs[job_id] = {
        'status': 'queued',
        'tweet_url': tweet_url,
        'output': '',
        'error': ''
    }
    
    # Start automation in a background thread
    thread = threading.Thread(target=run_automation, args=(job_id, tweet_url))
    thread.daemon = True
    thread.start()
    
    return jsonify({
        'success': True,
        'job_id': job_id,
        'message': 'Automation started'
    })

@app.route('/api/status/<int:job_id>')
def get_job_status(job_id):
    """Get the status of a specific job."""
    job = jobs.get(job_id)
    
    if not job:
        return jsonify({'error': 'Job not found'}), 404
    
    return jsonify(job)

@app.route('/api/jobs')
def list_jobs():
    """List all jobs."""
    return jsonify(jobs)

if __name__ == '__main__':
    # Run on all interfaces so it can be accessed from network
    app.run(host='0.0.0.0', port=5000, debug=True)
