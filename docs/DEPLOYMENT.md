# RuvScan Deployment Guide

## Production Deployment Options

### 1. Docker Compose (Recommended for Single Server)

**Best for**: Small to medium deployments, development, testing

```bash
# Production docker-compose
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

**Requirements**:
- Docker 20.10+
- Docker Compose 2.0+
- 4GB RAM minimum
- 2 CPU cores minimum

### 2. Kubernetes (Recommended for Scale)

**Best for**: Large deployments, multi-region, high availability

```bash
# Apply Kubernetes manifests
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/secrets.yaml
kubectl apply -f k8s/deployments/
kubectl apply -f k8s/services/
kubectl apply -f k8s/ingress.yaml
```

**Requirements**:
- Kubernetes 1.24+
- 8GB RAM per node
- 4 CPU cores per node
- Persistent storage (for database)

### 3. Cloud Platforms

#### AWS

**Option A: ECS (Elastic Container Service)**
```bash
# Build and push images
docker build -t ruvscan-mcp:latest -f docker/Dockerfile.python .
docker tag ruvscan-mcp:latest ${AWS_ACCOUNT}.dkr.ecr.${REGION}.amazonaws.com/ruvscan-mcp:latest
docker push ${AWS_ACCOUNT}.dkr.ecr.${REGION}.amazonaws.com/ruvscan-mcp:latest

# Deploy with ECS
aws ecs create-service \
  --cluster ruvscan-cluster \
  --service-name ruvscan-mcp \
  --task-definition ruvscan-mcp:1
```

**Option B: EKS (Elastic Kubernetes Service)**
```bash
# Create cluster
eksctl create cluster --name ruvscan --region us-west-2

# Deploy
kubectl apply -f k8s/
```

#### Google Cloud

**Option A: Cloud Run**
```bash
# Build and deploy
gcloud builds submit --tag gcr.io/${PROJECT_ID}/ruvscan-mcp
gcloud run deploy ruvscan-mcp \
  --image gcr.io/${PROJECT_ID}/ruvscan-mcp \
  --platform managed
```

**Option B: GKE (Google Kubernetes Engine)**
```bash
# Create cluster
gcloud container clusters create ruvscan \
  --num-nodes=3 \
  --machine-type=n1-standard-2

# Deploy
kubectl apply -f k8s/
```

#### Azure

**Option A: Azure Container Instances**
```bash
# Deploy container group
az container create \
  --resource-group ruvscan-rg \
  --name ruvscan-mcp \
  --image ruvscan/mcp-server:latest
```

**Option B: AKS (Azure Kubernetes Service)**
```bash
# Create cluster
az aks create \
  --resource-group ruvscan-rg \
  --name ruvscan-cluster \
  --node-count 3

# Deploy
kubectl apply -f k8s/
```

## Environment Configuration

### Required Environment Variables

```bash
# GitHub
GITHUB_TOKEN=ghp_xxxxx

# OpenAI (for embeddings)
OPENAI_API_KEY=sk-xxxxx

# Database
DATABASE_TYPE=sqlite  # or supabase
SQLITE_PATH=/data/ruvscan.db

# Server
RUVSCAN_HOST=0.0.0.0
RUVSCAN_PORT=8000

# Rust Engine
RUST_ENGINE_HOST=rust-engine
RUST_ENGINE_PORT=50051

# Go Scanner
RUVSCAN_SOURCE_TYPE=org
RUVSCAN_SOURCE_NAME=ruvnet
```

### Optional Environment Variables

```bash
# Supabase (if using cloud storage)
SUPABASE_URL=https://xxx.supabase.co
SUPABASE_KEY=xxxxx

# Anthropic (alternative LLM)
ANTHROPIC_API_KEY=sk-ant-xxxxx

# Monitoring
LOG_LEVEL=INFO
SENTRY_DSN=https://xxx@sentry.io/xxx

# Performance
MAX_WORKERS=4
REQUEST_TIMEOUT=30
```

## Database Setup

### SQLite (Default)

```bash
# Auto-initialized on first run
# Data stored in: /data/ruvscan.db
```

### Supabase (Cloud)

1. Create Supabase project
2. Run migrations:
```sql
-- Run SQL from src/mcp/storage/migrations/
```
3. Set environment variables:
```bash
SUPABASE_URL=https://xxx.supabase.co
SUPABASE_KEY=your_anon_key
```

### PostgreSQL (Self-hosted)

```bash
# docker-compose.postgres.yml
docker-compose -f docker-compose.yml -f docker-compose.postgres.yml up -d
```

## SSL/TLS Configuration

### Let's Encrypt with Nginx

```nginx
server {
    listen 443 ssl http2;
    server_name api.ruvscan.io;

    ssl_certificate /etc/letsencrypt/live/api.ruvscan.io/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/api.ruvscan.io/privkey.pem;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### Traefik (Docker)

```yaml
labels:
  - "traefik.enable=true"
  - "traefik.http.routers.ruvscan.rule=Host(`api.ruvscan.io`)"
  - "traefik.http.routers.ruvscan.tls=true"
  - "traefik.http.routers.ruvscan.tls.certresolver=letsencrypt"
```

## Scaling

### Horizontal Scaling

**Python MCP Server**:
```bash
# Docker Compose
docker-compose up --scale mcp-server=3

# Kubernetes
kubectl scale deployment ruvscan-mcp --replicas=3
```

**Rust Engine**:
```bash
# Stateless - scale freely
kubectl scale deployment ruvscan-rust --replicas=5
```

**Go Scanners**:
```bash
# Run as jobs or cron
kubectl create job scanner-job --from=cronjob/ruvscan-scanner
```

### Load Balancing

**Nginx**:
```nginx
upstream ruvscan_backend {
    least_conn;
    server 127.0.0.1:8001;
    server 127.0.0.1:8002;
    server 127.0.0.1:8003;
}

server {
    location / {
        proxy_pass http://ruvscan_backend;
    }
}
```

**Kubernetes**:
```yaml
apiVersion: v1
kind: Service
metadata:
  name: ruvscan-mcp
spec:
  type: LoadBalancer
  selector:
    app: ruvscan-mcp
  ports:
    - port: 80
      targetPort: 8000
```

## Monitoring

### Prometheus Metrics

```yaml
# prometheus.yml
scrape_configs:
  - job_name: 'ruvscan'
    static_configs:
      - targets: ['localhost:8000']
```

### Grafana Dashboards

Import dashboard from `monitoring/grafana/ruvscan-dashboard.json`

### Log Aggregation

**Loki**:
```yaml
# promtail-config.yml
clients:
  - url: http://loki:3100/loki/api/v1/push
```

**ELK Stack**:
```bash
# filebeat.yml
filebeat.inputs:
  - type: container
    paths:
      - '/var/lib/docker/containers/*/*.log'
```

## Backup

### Database Backup

```bash
# SQLite
sqlite3 /data/ruvscan.db ".backup /backups/ruvscan-$(date +%Y%m%d).db"

# Automated with cron
0 2 * * * sqlite3 /data/ruvscan.db ".backup /backups/ruvscan-$(date +%Y%m%d).db"
```

### Configuration Backup

```bash
# Backup environment and configs
tar -czf config-backup-$(date +%Y%m%d).tar.gz \
  .env \
  config/ \
  docker-compose*.yml
```

## Security Checklist

- [ ] Change default passwords
- [ ] Enable SSL/TLS
- [ ] Configure firewall rules
- [ ] Set up API rate limiting
- [ ] Enable authentication (API keys)
- [ ] Scan images for vulnerabilities
- [ ] Set up secret management (Vault/AWS Secrets Manager)
- [ ] Enable audit logging
- [ ] Configure CORS properly
- [ ] Keep dependencies updated

## Health Checks

### Kubernetes Liveness/Readiness

```yaml
livenessProbe:
  httpGet:
    path: /health
    port: 8000
  initialDelaySeconds: 30
  periodSeconds: 10

readinessProbe:
  httpGet:
    path: /health
    port: 8000
  initialDelaySeconds: 5
  periodSeconds: 5
```

### Docker Healthcheck

```dockerfile
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1
```

## Troubleshooting

### Container Won't Start

```bash
# Check logs
docker-compose logs -f mcp-server

# Check resource usage
docker stats

# Verify environment
docker-compose config
```

### High Memory Usage

```bash
# Check Python memory
docker exec -it ruvscan-mcp ps aux

# Adjust workers
# In docker-compose.yml:
environment:
  MAX_WORKERS: 2
```

### Slow Queries

```bash
# Check database size
ls -lh /data/ruvscan.db

# Analyze slow queries
sqlite3 /data/ruvscan.db "EXPLAIN QUERY PLAN SELECT * FROM repos;"

# Add indexes if needed
```

## Performance Tuning

### Python

```yaml
environment:
  WORKERS: 4
  WORKER_CLASS: uvicorn.workers.UvicornWorker
  WORKER_CONNECTIONS: 1000
```

### Rust

```toml
[profile.release]
opt-level = 3
lto = true
codegen-units = 1
```

### Database

```bash
# SQLite optimizations
PRAGMA journal_mode = WAL;
PRAGMA synchronous = NORMAL;
PRAGMA cache_size = 10000;
```

## Rollback Procedure

```bash
# Docker Compose
docker-compose down
docker-compose pull
docker-compose up -d

# Kubernetes
kubectl rollout undo deployment/ruvscan-mcp
kubectl rollout status deployment/ruvscan-mcp
```

## Cost Optimization

### Cloud Provider Tips

1. **Use spot instances** for non-critical workloads
2. **Enable auto-scaling** to match demand
3. **Use cloud storage** (S3/GCS) for backups
4. **Set up budget alerts**
5. **Review logs retention** policies

### Resource Limits

```yaml
resources:
  limits:
    cpu: "1"
    memory: "512Mi"
  requests:
    cpu: "250m"
    memory: "256Mi"
```

## Support

For deployment issues:
- GitHub Issues: https://github.com/ruvnet/ruvscan/issues
- Documentation: `/docs`
- Community: Discord
