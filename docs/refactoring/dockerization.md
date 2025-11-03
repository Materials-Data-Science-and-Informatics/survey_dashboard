# Dockerization Documentation

This document explains how the Survey Dashboard application is dockerized for production deployment with nginx as a reverse proxy.

## Table of Contents
1. [Architecture Overview](#architecture-overview)
2. [Component Breakdown](#component-breakdown)
3. [Request Flow](#request-flow)
4. [File Structure](#file-structure)
5. [Configuration Details](#configuration-details)
6. [Deployment Guide](#deployment-guide)

---

## Architecture Overview

### High-Level Schematic

```
┌─────────────────────────────────────────────────────────────┐
│                         PRODUCTION                          │
│                                                             │
│  ┌───────────┐         ┌──────────────┐                   │
│  │  Internet │────────▶│    Nginx     │                   │
│  │   User    │         │  Container   │                   │
│  └───────────┘         │  (Port 80)   │                   │
│       │                └──────┬───────┘                   │
│       │                       │                            │
│       │                  Reverse Proxy                     │
│       │                  WebSocket Support                 │
│       │                       │                            │
│       │                ┌──────▼───────┐                   │
│       └───────────────▶│    Panel     │                   │
│                        │ App Container│                   │
│                        │  (Port 5006) │                   │
│                        └──────────────┘                   │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐  │
│  │         Docker Compose Network                       │  │
│  │  - nginx and app containers can communicate         │  │
│  │  - Isolated from host network                        │  │
│  └─────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘

vs.

┌─────────────────────────────────────────────────────────────┐
│                        DEVELOPMENT                          │
│                                                             │
│  ┌───────────┐         ┌──────────────┐                   │
│  │ Developer │────────▶│  Panel App   │                   │
│  │  Browser  │         │ (localhost)  │                   │
│  └───────────┘         │  Port 5006   │                   │
│                        └──────────────┘                   │
│                                                             │
│  - No nginx (direct access)                                │
│  - No Docker (runs locally)                                │
│  - Auto-opens browser with --show flag                     │
└─────────────────────────────────────────────────────────────┘
```

---

## Component Breakdown

### 1. Docker Image vs. Configuration Files

#### Why We Need Both:

```
┌──────────────────────────────────────────────────────────────┐
│                    NGINX SETUP                               │
│                                                              │
│  ┌─────────────────────┐      ┌─────────────────────┐      │
│  │   Nginx Docker      │      │  Custom Config      │      │
│  │      Image          │  +   │     Files           │  =   │
│  │                     │      │                     │      │
│  │ - nginx software    │      │ - Proxy settings    │      │
│  │ - Linux base        │      │ - WebSocket setup   │      │
│  │ - Default configs   │      │ - Your app routing  │      │
│  └─────────────────────┘      └─────────────────────┘      │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │         Working Nginx Server                         │  │
│  │  Knows how to forward requests to Panel app          │  │
│  └──────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────┘
```

**Key Concept:** The Docker image provides the software, the config files tell it what to do.

### 2. Multi-Stage Docker Build

```
┌────────────────────────────────────────────────────────────┐
│                   DOCKERFILE STAGES                        │
│                                                            │
│  Stage 1: BUILDER                                          │
│  ┌──────────────────────────────────────────────┐         │
│  │ FROM python:3.12-slim                        │         │
│  │ - Install Poetry                             │         │
│  │ - Copy pyproject.toml & poetry.lock          │         │
│  │ - Install dependencies                       │         │
│  │                                              │         │
│  │ Result: All Python packages installed        │         │
│  └──────────────────────────────────────────────┘         │
│                        │                                   │
│                        │ Copy only installed packages      │
│                        ▼                                   │
│  Stage 2: FINAL                                            │
│  ┌──────────────────────────────────────────────┐         │
│  │ FROM python:3.12-slim (fresh image)          │         │
│  │ - Copy packages from builder                 │         │
│  │ - Copy application code                      │         │
│  │ - Create non-root user                       │         │
│  │ - Set CMD to run app                         │         │
│  │                                              │         │
│  │ Result: Lean production image                │         │
│  │ (No Poetry, no build tools, no cache)        │         │
│  └──────────────────────────────────────────────┘         │
│                                                            │
│  Benefits:                                                 │
│  - Smaller final image size                               │
│  - Faster deployment                                       │
│  - No unnecessary build tools in production               │
└────────────────────────────────────────────────────────────┘
```

### 3. Production vs Development Mode

The updated `scripts.py` supports both modes:

```python
# Development Mode (default)
$ survey-dashboard
→ Runs on localhost
→ Opens browser automatically (--show flag)
→ Only accessible from your machine

# Production Mode (Docker)
$ survey-dashboard --production --host 0.0.0.0
→ Binds to 0.0.0.0 (all network interfaces)
→ Allows WebSocket connections from anywhere
→ No browser opening (runs as service)
→ Accessible from external networks
```

**Key Changes Made to scripts.py:**
1. Added `argparse` for command-line arguments
2. Added `--production` flag
3. Added `--host` and `--port` parameters
4. Conditional logic for `--show` flag (dev only)
5. Conditional `--allow-websocket-origin` (production only)

---

## Request Flow

### How a User Request Travels Through the System

```
1. User visits https://yourdomain.com
   │
   ├─▶ DNS resolves to your server IP
   │
   ▼
2. Request hits server on port 80/443
   │
   ├─▶ Nginx container receives request
   │
   ▼
3. Nginx processes request
   │
   ├─▶ Checks nginx/conf.d/default.conf
   ├─▶ Sees proxy_pass directive
   ├─▶ Forwards to http://dashboard:5006
   │
   ▼
4. Request reaches Panel app container
   │
   ├─▶ Panel app running on port 5006
   ├─▶ Generates HTML/JavaScript response
   │
   ▼
5. Response travels back through nginx
   │
   ├─▶ Nginx adds headers
   ├─▶ Handles WebSocket upgrades
   │
   ▼
6. User sees the dashboard in browser
   │
   ├─▶ JavaScript connects via WebSocket
   ├─▶ Real-time interactivity works
   │
   ▼
7. User interacts with dashboard
   │
   └─▶ WebSocket messages flow through nginx
       to Panel app and back
```

### WebSocket Handling (Critical for Panel/Bokeh)

```
Regular HTTP Request:
Browser ────HTTP GET────▶ Nginx ────▶ Panel App
       ◀────HTML────────       ◀────

WebSocket Upgrade (for interactivity):
Browser ────Upgrade: websocket────▶ Nginx
                                     │
                                     ├─ Detects "Upgrade" header
                                     ├─ Uses proxy_http_version 1.1
                                     ├─ Sets Connection "upgrade"
                                     ▼
                                  Panel App
       ◀────────Persistent WebSocket Connection────────▶

Now when you click a button:
Browser ────WS Message────▶ Nginx ────▶ Panel App
       ◀────WS Response───       ◀────
```

**Why This Matters:** Without proper WebSocket configuration, the dashboard would load but be completely non-interactive.

---

## File Structure

```
survey_dashboard/
├── Dockerfile                      # Multi-stage build definition
├── docker-compose.yml              # Orchestrates nginx + app containers
├── .dockerignore                   # Files to exclude from Docker build
├── .env.example                    # Template for environment variables
│
├── nginx/                          # Nginx configuration
│   └── conf.d/
│       └── default.conf            # Reverse proxy configuration
│
├── survey_dashboard/
│   ├── app.py                      # Main Panel application
│   ├── scripts.py                  # Entry point (now with --production flag)
│   └── ...                         # Other app files
│
├── pyproject.toml                  # Poetry dependencies
├── poetry.lock                     # Locked dependency versions
│
└── docs/
    └── refactoring/
        └── dockerization.md        # This document
```

---

## Configuration Details

### 1. Dockerfile Explained

```dockerfile
# STAGE 1: BUILDER
FROM python:3.12-slim as builder
# Why: Matches pyproject.toml requirement (python = "^3.12.3")
# Why slim: Smaller base image (~100MB vs ~900MB for full Python)

RUN pip install --no-cache-dir poetry==1.8.2
# Why: Poetry is the dependency manager (poetry.lock exists)
# Why --no-cache-dir: Reduces image size by not caching pip files

COPY pyproject.toml poetry.lock ./
# Why copy first: Docker layer caching - if dependencies don't change,
#                 this layer is reused on rebuilds

RUN poetry config virtualenvs.create false
# Why: In containers, we don't need virtual environments
#      The container itself provides isolation

RUN poetry install --no-dev --no-interaction --no-ansi
# Why --no-dev: Skip pytest, pre-commit, pdoc (not needed in production)
# Why --no-interaction: Non-interactive mode for automated builds

# STAGE 2: FINAL
FROM python:3.12-slim
# Why fresh image: Don't include Poetry, build tools, pip cache

COPY --from=builder /usr/local/lib/python3.12/site-packages ...
# Why: Only copy installed packages, not Poetry or build artifacts

USER appuser
# Why: Security best practice - don't run as root
#      If container is compromised, attacker has limited permissions
```

### 2. docker-compose.yml Structure

```yaml
services:
  nginx:
    image: nginx:latest              # Official nginx Docker image
    ports:
      - "80:80"                       # Host:Container port mapping
    volumes:
      - ./nginx/conf.d:/etc/nginx/conf.d  # Mount our config
    depends_on:
      - dashboard                     # Start dashboard first

  dashboard:
    build: .                          # Build from ./Dockerfile
    expose:
      - "5006"                        # Internal port (not published to host)
    command: ["survey-dashboard", "--production", "--host", "0.0.0.0"]
```

**Key Concepts:**
- `ports` vs `expose`: `ports` publishes to host, `expose` only within Docker network
- `volumes`: Mounts local files into container (changes reflect without rebuild)
- `depends_on`: Ensures startup order

### 3. Nginx Configuration (nginx/conf.d/default.conf)

```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location / {
        proxy_pass http://dashboard:5006;
        # Why 'dashboard': Docker Compose creates DNS entry for service name

        # WebSocket support
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        # Why: Panel/Bokeh requires WebSocket for interactivity

        # Timeouts
        proxy_read_timeout 86400;
        # Why: Panel apps can have long-lived WebSocket connections
    }
}
```

---

## Deployment Guide

### Local Development (No Docker)

```bash
# Install dependencies
poetry install

# Run in development mode
survey-dashboard
# OR
python -m survey_dashboard.scripts

# App opens automatically in browser at http://localhost:5006
```

### Docker Development Testing

```bash
# Build and start containers
docker-compose up --build

# Access at http://localhost
# Nginx forwards to Panel app

# Stop containers
docker-compose down
```

### Production Deployment

```bash
# 1. Clone repository on server
git clone <repo-url>
cd survey_dashboard

# 2. Copy and configure environment
cp .env.example .env
nano .env  # Set HOST=yourdomain.com

# 3. Update nginx config with your domain
nano nginx/conf.d/default.conf

# 4. Start services
docker-compose up -d

# 5. View logs
docker-compose logs -f

# 6. Stop services
docker-compose down
```

### Updating the Application

```bash
# Pull latest changes
git pull

# Rebuild and restart
docker-compose up -d --build

# Old containers are automatically replaced
```

---

## Key Takeaways

### Why Dockerize?

1. **Consistency**: "Works on my machine" → "Works everywhere"
2. **Isolation**: Dependencies don't conflict with host system
3. **Scalability**: Easy to run multiple instances
4. **Reproducibility**: Exact same environment every time

### Why Nginx?

1. **Reverse Proxy**: Single entry point for multiple services
2. **SSL/TLS**: Easy to add HTTPS with Let's Encrypt
3. **Load Balancing**: Can distribute traffic across multiple app instances
4. **Static Files**: Efficiently serve CSS/JS/images
5. **WebSocket**: Proper handling of long-lived connections

### Why Multi-Stage Build?

1. **Smaller Images**: ~200MB vs ~1GB
2. **Faster Deployments**: Less data to transfer
3. **Security**: Fewer tools = smaller attack surface
4. **Cost**: Smaller images save storage/bandwidth costs

---

## Troubleshooting

### Common Issues

**Issue:** Dashboard loads but filters/buttons don't work
- **Cause:** WebSocket connection failing
- **Fix:** Check nginx WebSocket config (Upgrade headers)

**Issue:** "Connection refused" errors
- **Cause:** Panel app not ready when nginx starts
- **Fix:** Add health check or restart policy in docker-compose.yml

**Issue:** Changes to code not reflected
- **Cause:** Using cached Docker layers
- **Fix:** Rebuild with `docker-compose up --build`

**Issue:** Permission errors in container
- **Cause:** Files owned by root
- **Fix:** Check USER directive in Dockerfile (should be appuser)

---

## Future Enhancements

1. **HTTPS/SSL**: Add Let's Encrypt for SSL certificates
2. **Health Checks**: Add container health monitoring
3. **Scaling**: Add multiple Panel app instances with load balancing
4. **Logging**: Centralized logging with ELK/Prometheus
5. **CI/CD**: Automated builds and deployments
6. **Secrets Management**: Use Docker secrets for sensitive data
