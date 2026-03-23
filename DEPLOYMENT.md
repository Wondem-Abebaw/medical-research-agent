# Deployment Guide

This guide covers deploying the Medical Research Agent to production environments.

## Table of Contents

- [Google Cloud Platform (GCP)](#google-cloud-platform-gcp)
- [AWS](#aws)
- [Docker Compose (VPS)](#docker-compose-vps)
- [Environment Variables](#environment-variables)
- [Security Considerations](#security-considerations)

## Google Cloud Platform (GCP)

### Option 1: Cloud Run (Recommended)

**Benefits**: Serverless, auto-scaling, pay-per-use

#### Backend Deployment

1. **Build and push Docker image**

```bash
cd backend

# Configure gcloud
gcloud config set project YOUR_PROJECT_ID

# Build image
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/medical-research-agent-backend

# Deploy to Cloud Run
gcloud run deploy medical-research-agent-backend \
  --image gcr.io/YOUR_PROJECT_ID/medical-research-agent-backend \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --memory 2Gi \
  --cpu 2 \
  --timeout 300 \
  --set-env-vars GOOGLE_API_KEY=your_key,PUBMED_EMAIL=your_email
```

#### Frontend Deployment

```bash
cd frontend

# Build image
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/medical-research-agent-frontend

# Deploy to Cloud Run
gcloud run deploy medical-research-agent-frontend \
  --image gcr.io/YOUR_PROJECT_ID/medical-research-agent-frontend \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars VITE_API_URL=https://backend-url.run.app
```

### Option 2: Google Kubernetes Engine (GKE)

For high-traffic production deployments.

```bash
# Create cluster
gcloud container clusters create medical-research-agent \
  --num-nodes=3 \
  --machine-type=e2-standard-2

# Deploy with Kubernetes manifests
kubectl apply -f k8s/
```

## AWS

### Option 1: ECS Fargate

```bash
# Create ECR repositories
aws ecr create-repository --repository-name medical-research-agent-backend
aws ecr create-repository --repository-name medical-research-agent-frontend

# Build and push images
docker build -t backend ./backend
docker tag backend:latest YOUR_AWS_ACCOUNT.dkr.ecr.us-east-1.amazonaws.com/medical-research-agent-backend:latest
docker push YOUR_AWS_ACCOUNT.dkr.ecr.us-east-1.amazonaws.com/medical-research-agent-backend:latest

# Create ECS task definition and service
# Use AWS Console or CLI to configure
```

### Option 2: Elastic Beanstalk

```bash
# Initialize EB
eb init -p docker medical-research-agent

# Deploy
eb create production --database
eb deploy
```

## Docker Compose (VPS)

For deployment on a VPS (DigitalOcean, Linode, etc.)

### 1. Server Setup

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

### 2. Deploy Application

```bash
# Clone repository
git clone <your-repo-url>
cd medical-research-agent

# Set up environment variables
cp backend/.env.example backend/.env
# Edit backend/.env with your production values

# Start services
docker-compose up -d

# View logs
docker-compose logs -f
```

### 3. Set up Nginx Reverse Proxy (Optional)

```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }

    location /api {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### 4. Set up SSL with Let's Encrypt

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com
```

## Environment Variables

### Production Backend (.env)

```env
# API Keys
GOOGLE_API_KEY=your_production_google_api_key
TAVILY_API_KEY=your_production_tavily_api_key

# Application
DEBUG=false
APP_NAME=Medical Research Agent API
APP_VERSION=1.0.0

# Server
HOST=0.0.0.0
PORT=8000

# CORS - Update with your frontend domain
CORS_ORIGINS=https://yourdomain.com

# PubMed
PUBMED_EMAIL=your-production-email@yourdomain.com
PUBMED_TOOL=MedicalResearchAgent

# Model Configuration
MODEL_NAME=gemini-1.5-flash
TEMPERATURE=0.7
MAX_TOKENS=2048

# Agent Configuration
AGENT_MAX_ITERATIONS=10
AGENT_TIMEOUT=300
```

### Production Frontend (.env)

```env
VITE_API_URL=https://api.yourdomain.com
```

## Security Considerations

### 1. API Keys

- **Never commit API keys to version control**
- Use environment variables or secret managers (GCP Secret Manager, AWS Secrets Manager)
- Rotate keys regularly
- Use different keys for production and development

### 2. CORS Configuration

Update `backend/.env`:
```env
CORS_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
```

### 3. Rate Limiting

Add rate limiting in production:

```python
# backend/app/main.py
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.post("/api/v1/query")
@limiter.limit("10/minute")
async def query_agent(request: Request, agent_request: AgentRequest):
    # ...
```

### 4. HTTPS

Always use HTTPS in production:
- Cloud providers: Configure SSL in load balancer
- VPS: Use Let's Encrypt with Certbot

### 5. Authentication (Optional)

For production deployments requiring authentication:

```python
# backend/app/api/auth.py
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()

async def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if credentials.credentials != os.getenv("API_TOKEN"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )
    return credentials.credentials

# Add to routes
@router.post("/query", dependencies=[Depends(verify_token)])
```

### 6. Monitoring

Set up monitoring and logging:

**GCP:**
```bash
# Cloud Logging
gcloud logging read "resource.type=cloud_run_revision"

# Cloud Monitoring
# Configure alerts in GCP Console
```

**Self-hosted:**
```bash
# Install Prometheus and Grafana
docker-compose -f monitoring/docker-compose.yml up -d
```

## Health Checks

Configure health checks for production:

**Backend**: `GET /ping` and `GET /api/v1/health`
**Frontend**: `GET /` (returns 200 if serving)

## Scaling Considerations

### Horizontal Scaling

- **Cloud Run**: Auto-scales based on traffic
- **ECS/GKE**: Configure auto-scaling groups
- **VPS**: Add more instances behind a load balancer

### Performance Optimization

1. **Caching**: Implement Redis for frequent queries
2. **Database**: Add PostgreSQL for conversation history
3. **CDN**: Serve frontend assets via CDN
4. **API Gateway**: Use API Gateway for rate limiting and caching

## Backup and Disaster Recovery

1. **Database Backups**: If using PostgreSQL, set up automated backups
2. **Docker Images**: Tag and store images in registry
3. **Environment Variables**: Document and backup securely
4. **Monitoring**: Set up alerts for downtime

## Cost Optimization

### GCP Cloud Run
- Set min instances to 0 (cold starts acceptable)
- Set max instances based on expected traffic
- Use Gemini Flash instead of Pro for lower costs

### Resource Limits
```yaml
# docker-compose.yml
services:
  backend:
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 2G
        reservations:
          cpus: '0.5'
          memory: 512M
```

## Maintenance

### Update Deployment

```bash
# Pull latest code
git pull origin main

# Rebuild and redeploy
docker-compose down
docker-compose build --no-cache
docker-compose up -d

# Or for Cloud Run
gcloud builds submit --tag gcr.io/PROJECT_ID/app:latest
gcloud run deploy app --image gcr.io/PROJECT_ID/app:latest
```

### Database Migrations

If adding a database:
```bash
# Run migrations
docker-compose exec backend alembic upgrade head
```

## Troubleshooting

### Check Logs

```bash
# Docker Compose
docker-compose logs -f backend
docker-compose logs -f frontend

# Cloud Run
gcloud run services logs read medical-research-agent-backend --limit=50
```

### Common Issues

1. **API Key errors**: Verify environment variables are set correctly
2. **CORS errors**: Check CORS_ORIGINS configuration
3. **Timeout errors**: Increase AGENT_TIMEOUT value
4. **Memory issues**: Increase container memory allocation

## Support

For deployment issues:
- Check logs first
- Review environment variables
- Verify API keys are valid
- Test health endpoints

---

**Production Checklist:**
- [ ] All API keys configured
- [ ] HTTPS enabled
- [ ] CORS properly configured
- [ ] Health checks working
- [ ] Monitoring set up
- [ ] Backups configured
- [ ] Rate limiting enabled
- [ ] Error logging enabled
- [ ] Performance tested
- [ ] Security review completed
