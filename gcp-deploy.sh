#!/bin/bash

# GCP Deployment Script for Twitter Automation
# This script helps you deploy to Google Cloud Platform

set -e

echo "========================================="
echo "  X Automation - GCP Deployment Script"
echo "========================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_step() {
    echo -e "${BLUE}→${NC} $1"
}

print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

# Check prerequisites
check_prerequisites() {
    print_step "Checking prerequisites..."
    
    if ! command -v gcloud &> /dev/null; then
        print_error "gcloud CLI not found. Install it from: https://cloud.google.com/sdk/docs/install"
        exit 1
    fi
    print_success "gcloud CLI found"
    
    if ! command -v docker &> /dev/null; then
        print_error "Docker not found. Install from: https://www.docker.com/products/docker-desktop"
        exit 1
    fi
    print_success "Docker found"
}

# Get GCP project info
get_project_info() {
    print_step "Getting GCP project information..."
    
    PROJECT_ID=$(gcloud config get-value project)
    if [ -z "$PROJECT_ID" ]; then
        print_error "No GCP project set. Run: gcloud config set project YOUR_PROJECT_ID"
        exit 1
    fi
    print_success "Project ID: $PROJECT_ID"
    
    REGION=${1:-us-central1}
    print_success "Region: $REGION"
}

# Deploy to Cloud Run
deploy_cloud_run() {
    print_step "Deploying to Cloud Run..."
    print_warning "Note: Cloud Run works for Dashboard only (no ADB automation)"
    
    SERVICE_NAME="twitter-automation"
    IMAGE_NAME="gcr.io/$PROJECT_ID/$SERVICE_NAME"
    
    # Build and push image
    print_step "Building and pushing Docker image..."
    docker build -f Dockerfile.gcp -t $IMAGE_NAME .
    docker push $IMAGE_NAME
    print_success "Image pushed to Container Registry"
    
    # Deploy to Cloud Run
    print_step "Deploying to Cloud Run..."
    gcloud run deploy $SERVICE_NAME \
        --image $IMAGE_NAME \
        --platform managed \
        --region $REGION \
        --port 5000 \
        --allow-unauthenticated \
        --memory 512Mi \
        --cpu 1 \
        --set-env-vars "FLASK_ENV=production,ANDROID_SERIAL=192.168.0.105:5555"
    
    print_success "Cloud Run deployment complete!"
    
    # Get the URL
    SERVICE_URL=$(gcloud run services describe $SERVICE_NAME --region $REGION --format 'value(status.url)')
    print_success "Dashboard URL: $SERVICE_URL"
}

# Deploy to Compute Engine
deploy_compute_engine() {
    print_step "Deploying to Compute Engine..."
    print_warning "Note: Compute Engine supports full automation with ADB"
    
    read -p "Enter VM name [twitter-automation]: " VM_NAME
    VM_NAME=${VM_NAME:-twitter-automation}
    
    read -p "Enter machine type [e2-small]: " MACHINE_TYPE
    MACHINE_TYPE=${MACHINE_TYPE:-e2-small}
    
    # Create VM
    print_step "Creating Compute Engine VM..."
    gcloud compute instances create $VM_NAME \
        --image-family=debian-11 \
        --image-project=debian-cloud \
        --machine-type=$MACHINE_TYPE \
        --zone=${REGION}-a \
        --scopes=https://www.googleapis.com/auth/cloud-platform \
        --metadata-from-file startup-script=gcp-vm-startup.sh
    
    print_success "VM created: $VM_NAME"
    
    VM_IP=$(gcloud compute instances describe $VM_NAME \
        --zone=${REGION}-a \
        --format='get(networkInterfaces[0].accessConfigs[0].natIP)')
    
    print_success "VM IP: $VM_IP"
    print_success "Access dashboard at: http://$VM_IP:5000"
    
    echo ""
    echo "Next steps:"
    echo "1. Wait 2-3 minutes for VM startup script to complete"
    echo "2. SSH into the VM:"
    echo "   gcloud compute ssh $VM_NAME --zone=${REGION}-a"
    echo "3. Check Docker status:"
    echo "   docker ps"
}

# Create startup script for VM
create_startup_script() {
    print_step "Creating VM startup script..."
    
    cat > gcp-vm-startup.sh << 'EOF'
#!/bin/bash

# Update system
apt-get update
apt-get install -y \
    curl \
    git \
    docker.io

# Start Docker
systemctl start docker
systemctl enable docker

# Add current user to docker group
usermod -aG docker $USER

# Create app directory
mkdir -p /home/automation
cd /home/automation

# Clone repository
git clone https://github.com/your-username/automation.git .

# Build and start containers
docker-compose -f docker-compose.gcp.yml up -d

# Print status
echo "Deployment complete at $(date)" > /var/log/automation-startup.log
EOF
    
    chmod +x gcp-vm-startup.sh
    print_success "Startup script created"
}

# Setup firewall rules
setup_firewall() {
    print_step "Setting up firewall rules..."
    
    RULE_NAME="allow-flask-$RANDOM"
    gcloud compute firewall-rules create $RULE_NAME \
        --allow=tcp:5000 \
        --source-ranges=0.0.0.0/0 \
        --description="Allow Flask dashboard access"
    
    print_success "Firewall rule created: $RULE_NAME"
}

# Main menu
show_menu() {
    echo ""
    echo "Choose deployment option:"
    echo ""
    echo "1) Deploy to Cloud Run (Dashboard only, cheapest)"
    echo "2) Deploy to Compute Engine (Full automation support)"
    echo "3) Setup everything"
    echo "4) Exit"
    echo ""
    read -p "Enter your choice (1-4): " choice
    
    case $choice in
        1)
            deploy_cloud_run
            ;;
        2)
            create_startup_script
            setup_firewall
            deploy_compute_engine
            ;;
        3)
            print_warning "This will setup both Cloud Run and Compute Engine"
            deploy_cloud_run
            echo ""
            create_startup_script
            setup_firewall
            deploy_compute_engine
            ;;
        4)
            print_success "Exiting..."
            exit 0
            ;;
        *)
            print_error "Invalid choice"
            show_menu
            ;;
    esac
}

# Main execution
main() {
    check_prerequisites
    get_project_info $1
    show_menu
    
    echo ""
    print_success "Deployment script completed!"
    echo ""
    echo "Documentation:"
    echo "- GCP_DEPLOYMENT.md - Detailed deployment guide"
    echo "- README.md - Project overview"
    echo ""
}

main "$@"
