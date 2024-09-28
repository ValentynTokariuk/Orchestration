#!/bin/bash

# Ensure Docker Desktop is started - Check Docker Desktop status on macOS
open -a Docker

# Wait for Docker to start
while ! docker system info > /dev/null 2>&1; do
  echo "Waiting for Docker to start..."
  sleep 1
done
echo "Docker is running."

# Start Minikube
echo "Starting Minikube..."
minikube start

# Set Docker environment to use Minikube's Docker daemon
echo "Setting Docker environment to use Minikube's..."
eval $(minikube docker-env)

# Build Docker images locally
echo "Building Docker images..."
docker build -t markvellaum/university:v0.0.1 -f Dockerfile .
docker pull postgres:latest

# Enable Kubernetes dashboard
echo "Enabling Kubernetes dashboard..."
minikube dashboard &

# Apply Kubernetes configurations
echo "Deploying Kubernetes configurations..."
kubectl apply -f app-config.yaml
kubectl apply -f db-credentials.yaml
kubectl apply -f postgres-pv.yaml
kubectl apply -f postgres-pvc.yaml
kubectl apply -f enrollments-deployment.yaml
kubectl apply -f enrollments-service.yaml
# Include grades app if needed
# kubectl apply -f grades-deployment.yaml
# kubectl apply -f grades-service.yaml

# Run the deploy.py script to start Docker containers
echo "Running deploy.py to start Docker containers..."
python3 deploy.py 

# Check if Docker containers are running
echo "Checking Docker containers..."
docker ps

# Get the URL to access the enrollments-app service
echo "Getting URL to access the enrollments-app service..."
minikube service enrollments-app --url

# Output the URL for accessing the FastAPI documentation
enrollments_url=$(minikube service enrollments-app --url)
echo "Access your application at: $enrollments_url/docs"

echo "Deployments and services applied and running."

