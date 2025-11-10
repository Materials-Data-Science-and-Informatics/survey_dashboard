# Local Testing Guide - Survey Dashboard

This guide explains how to test the Docker deployment setup locally before deploying to production. This helps catch issues early and ensures a smooth production deployment.

---

## Table of Contents

1. [Why Test Locally?](#why-test-locally)
2. [What You Can Test](#what-you-can-test)
3. [What You Cannot Test](#what-you-cannot-test)
4. [Local Testing Setup](#local-testing-setup)
5. [Testing Scenarios](#testing-scenarios)
6. [Verification Steps](#verification-steps)
7. [Troubleshooting](#troubleshooting)
8. [Cleanup](#cleanup)

---

## Why Test Locally?

Testing locally allows you to:

- ✅ Verify Docker images build successfully
- ✅ Ensure all containers start without errors
- ✅ Test that the dashboard is accessible at the correct path
- ✅ Verify WebSocket connections work
- ✅ Catch configuration errors before production
- ✅ Understand the deployment process in a safe environment
- ✅ Test updates and changes without affecting production

---

## What You Can Test

### ✅ Fully Testable Locally

1. **Docker Build Process**
   - Multi-stage build completes successfully
   - No missing dependencies
   - Application code is copied correctly

2. **Container Startup**
   - All 3 containers start without errors
   - Containers communicate via Docker network
   - Port mappings work correctly

3. **Application Functionality**
   - Dashboard loads and displays correctly
   - Interactive elements work (buttons, filters, plots)
   - WebSocket connections establish successfully
   - Static files (CSS, JavaScript) load properly

4. **Path Routing**
   - Dashboard accessible at specified VIRTUAL_PATH
   - Root path returns expected response
   - nginx-proxy routing configuration works

5. **Environment Variables**
   - Variables are read correctly by containers
   - Panel receives correct --prefix argument
   - Configuration is applied as expected

---

## What You Cannot Test

### ❌ Not Testable Locally (Requires Production Domain)

1. **HTTPS/SSL Certificates**
   - Let's Encrypt requires a real domain pointing to a public IP
   - Cannot acquire valid SSL certificates for localhost
   - **Workaround:** Test with HTTP only locally

2. **DNS Resolution**
   - localhost is not a real domain
   - Cannot test DNS propagation
   - **Workaround:** Use localhost or 127.0.0.1

3. **Public Internet Access**
   - Cannot test from external networks
   - Cannot verify public firewall rules
   - **Workaround:** Test from local network only

---

## Local Testing Setup

### Prerequisites

Ensure you have installed:
- Docker Engine (v20.10+)
- Docker Compose (v2.0+)

Verify installation:
```bash
docker --version
docker-compose --version
```

### Step 1: Create Local Environment File

Create a `.env.local` file for local testing:

```bash
cp .env.example .env.local
```

### Step 2: Configure for Local Testing

Edit `.env.local`:

```bash
nano .env.local
```

**Local testing configuration:**

```env
# Project name
COMPOSE_PROJECT_NAME=survey-dashboard-local

# Application port (internal)
APP_PORT=5006

# Nginx ports (external)
NGINX_PORT=80

# Use localhost for local testing
# IMPORTANT: HTTPS will NOT work with localhost
HOST=localhost

# Path where dashboard is accessible
VIRTUAL_PATH=/2021community

# Dummy email for local testing (not used without real domain)
LETSENCRYPT_EMAIL=test@localhost

# Python configuration
PYTHONUNBUFFERED=1
```

**Key differences from production:**
- `HOST=localhost` (instead of real domain)
- `COMPOSE_PROJECT_NAME=survey-dashboard-local` (to avoid conflicts)
- LETSENCRYPT_EMAIL is dummy (won't be used)

### Step 3: Point Docker Compose to Local Environment

Use the `-f` flag or rename:

**Option A: Use environment file flag**
```bash
docker-compose --env-file .env.local up -d
```

**Option B: Temporarily rename files**
```bash
# Backup production .env if it exists
mv .env .env.production 2>/dev/null || true

# Use local env for testing
cp .env.local .env

# Run docker-compose
docker-compose up -d

# After testing, restore production .env
mv .env.production .env 2>/dev/null || true
```

I'll use **Option A** in this guide (safer, no file renaming).

---

## Testing Scenarios

### Scenario 1: Basic HTTP Deployment Test

**Goal:** Verify all containers start and dashboard is accessible via HTTP.

**Steps:**

1. **Start containers with local environment:**
   ```bash
   docker-compose --env-file .env.local up -d --build
   ```

2. **Verify containers are running:**
   ```bash
   docker-compose ps
   ```

   Expected output:
   ```
   NAME                                    STATUS
   survey-dashboard-local_dashboard_1      Up
   nginx-proxy                             Up
   acme-companion                          Up
   ```

3. **Check dashboard logs:**
   ```bash
   docker-compose logs dashboard
   ```

   Look for:
   ```
   Starting HMC Survey Dashboard in PRODUCTION mode...
   Using URL prefix: /2021community
   Dashboard will be accessible at: http://0.0.0.0:5006/2021community
   ```

4. **Check nginx-proxy logs:**
   ```bash
   docker-compose logs nginx-proxy | grep localhost
   ```

   Should show nginx-proxy detected your container.

5. **Test HTTP access:**
   ```bash
   curl -I http://localhost/2021community/
   ```

   Expected: `HTTP/1.1 200 OK` or `HTTP/1.1 302 Found` (redirect)

6. **Open in browser:**
   ```
   http://localhost/2021community/
   ```

   Dashboard should load with full functionality.

**Expected Result:** ✅ Dashboard accessible, interactive, no errors

---

### Scenario 2: Path Restriction Test

**Goal:** Verify that only the specified path is accessible, others return 404.

**Steps:**

1. **Test the correct path (should work):**
   ```bash
   curl -I http://localhost/2021community
   ```

   Expected: `HTTP/1.1 200 OK`

2. **Test root path (should fail):**
   ```bash
   curl -I http://localhost/
   ```

   Expected: `HTTP/1.1 404 Not Found` or `HTTP/1.1 503 Service Unavailable`

   (503 is also acceptable - means nginx-proxy has no backend for root path)

3. **Test wrong path (should fail):**
   ```bash
   curl -I http://localhost/wrong-path
   ```

   Expected: `HTTP/1.1 404 Not Found`

4. **Browser test:**
   - Visit `http://localhost/2021community/` → Should load ✅
   - Visit `http://localhost/` → Should show 404 or 503 ✅
   - Visit `http://localhost/other` → Should show 404 ✅

**Expected Result:** ✅ Only `/2021community/` path is accessible

---

### Scenario 3: WebSocket Connection Test

**Goal:** Verify WebSocket connections work correctly for Panel interactivity.

**Steps:**

1. **Open dashboard in browser:**
   ```
   http://localhost/2021community/
   ```

2. **Open browser DevTools (F12)**

3. **Go to Network tab**

4. **Filter by "WS" (WebSocket)**

5. **Interact with dashboard** (click filters, buttons)

**Expected Result:**
- ✅ WebSocket connection established (Status: 101 Switching Protocols)
- ✅ Messages flowing in both directions
- ✅ Interactive elements respond immediately
- ✅ No WebSocket errors in console

**If WebSocket fails:**
- Check `nginx/vhost.d/default` file exists
- Check nginx-proxy logs for errors
- Restart nginx-proxy: `docker-compose restart nginx-proxy`

---

### Scenario 4: Container Restart and Persistence Test

**Goal:** Verify containers restart properly and maintain state.

**Steps:**

1. **Stop all containers:**
   ```bash
   docker-compose --env-file .env.local down
   ```

2. **Verify containers stopped:**
   ```bash
   docker-compose ps
   ```

   Should show no running containers.

3. **Start containers again:**
   ```bash
   docker-compose --env-file .env.local up -d
   ```

4. **Verify dashboard accessible:**
   ```bash
   curl -I http://localhost/2021community
   ```

5. **Check logs for clean startup:**
   ```bash
   docker-compose logs dashboard | tail -20
   ```

**Expected Result:** ✅ Clean restart, dashboard immediately accessible

---

### Scenario 5: Build Cache and Rebuild Test

**Goal:** Test that rebuilds work correctly (for code updates).

**Steps:**

1. **Make a small change to code** (e.g., add a comment):
   ```bash
   echo "# Test change" >> survey_dashboard/scripts.py
   ```

2. **Rebuild and restart:**
   ```bash
   docker-compose --env-file .env.local up -d --build
   ```

3. **Verify change is reflected:**
   ```bash
   docker-compose exec dashboard cat /app/survey_dashboard/scripts.py | tail -5
   ```

4. **Test dashboard still works:**
   ```bash
   curl -I http://localhost/2021community
   ```

5. **Undo test change:**
   ```bash
   git checkout survey_dashboard/scripts.py
   ```

**Expected Result:** ✅ Rebuild completes, changes reflected, dashboard works

---

### Scenario 6: Different VIRTUAL_PATH Test

**Goal:** Test that changing the path works correctly.

**Steps:**

1. **Stop containers:**
   ```bash
   docker-compose --env-file .env.local down
   ```

2. **Edit .env.local to use different path:**
   ```bash
   # Change VIRTUAL_PATH=/2021community to VIRTUAL_PATH=/test-path
   sed -i 's|VIRTUAL_PATH=/2021community|VIRTUAL_PATH=/test-path|' .env.local
   ```

3. **Start with new path:**
   ```bash
   docker-compose --env-file .env.local up -d --build
   ```

4. **Test new path:**
   ```bash
   curl -I http://localhost/test-path
   ```

   Expected: `HTTP/1.1 200 OK`

5. **Test old path no longer works:**
   ```bash
   curl -I http://localhost/2021community
   ```

   Expected: `HTTP/1.1 404 Not Found`

6. **Restore original path:**
   ```bash
   sed -i 's|VIRTUAL_PATH=/test-path|VIRTUAL_PATH=/2021community|' .env.local
   docker-compose --env-file .env.local down
   ```

**Expected Result:** ✅ Path change works, old path inaccessible

---

### Scenario 7: Port Conflict Test

**Goal:** Test behavior when port 80 is already in use.

**Steps:**

1. **Check if port 80 is available:**
   ```bash
   sudo lsof -i :80
   ```

2. **If port 80 is in use, use alternative port:**

   Edit `.env.local`:
   ```env
   NGINX_PORT=8080
   ```

3. **Update docker-compose ports** (temporary test):
   ```bash
   # This requires editing docker-compose.yml temporarily
   # Change: "80:80" to "8080:80"
   ```

4. **Start containers:**
   ```bash
   docker-compose --env-file .env.local up -d
   ```

5. **Test on new port:**
   ```bash
   curl -I http://localhost:8080/2021community
   ```

**Expected Result:** ✅ Works on alternative port

**Note:** In production, you need port 80 for Let's Encrypt. This test just verifies flexibility.

---

## Verification Steps

### Complete Local Testing Checklist

Run through this checklist to ensure everything works:

- [ ] Docker images build without errors
- [ ] All 3 containers start successfully
- [ ] `docker-compose ps` shows all containers "Up"
- [ ] Dashboard logs show production mode with correct prefix
- [ ] nginx-proxy logs show configuration for localhost
- [ ] HTTP access works: `curl http://localhost/2021community/`
- [ ] Browser loads dashboard at `http://localhost/2021community/`
- [ ] Dashboard displays correctly with styling
- [ ] Interactive elements work (buttons, filters, plots)
- [ ] Browser console shows no errors (F12)
- [ ] WebSocket connection established (Network tab)
- [ ] Root path blocked: `http://localhost/` returns 404/503
- [ ] Other paths blocked: `http://localhost/other` returns 404
- [ ] Containers restart cleanly: `docker-compose down && up -d`
- [ ] Rebuild works: `docker-compose up -d --build`

If all items are checked ✅, your setup is ready for production!

---

## Troubleshooting

### Issue 1: Port 80 Already in Use

**Error:**
```
Error starting userland proxy: listen tcp4 0.0.0.0:80: bind: address already in use
```

**Cause:** Another service (Apache, nginx, etc.) is using port 80.

**Solutions:**

**Option A: Stop the conflicting service**
```bash
# Find what's using port 80
sudo lsof -i :80

# Stop Apache (example)
sudo systemctl stop apache2

# Or stop nginx
sudo systemctl stop nginx
```

**Option B: Use a different port for testing**
```bash
# Edit .env.local
NGINX_PORT=8080

# Access via: http://localhost:8080/2021community
```

### Issue 2: Dashboard Container Exits Immediately

**Check logs:**
```bash
docker-compose logs dashboard
```

**Common causes:**

1. **Python error in code:**
   - Look for Python tracebacks in logs
   - Fix syntax or import errors

2. **Missing dependencies:**
   - Rebuild: `docker-compose up -d --build`

3. **Wrong command:**
   - Check Dockerfile CMD is correct
   - Verify scripts.py is executable

### Issue 3: 502 Bad Gateway

**Cause:** nginx-proxy can't reach dashboard container.

**Steps:**

1. **Check dashboard is running:**
   ```bash
   docker-compose ps dashboard
   ```

2. **Check dashboard logs for errors:**
   ```bash
   docker-compose logs dashboard
   ```

3. **Verify containers are on same network:**
   ```bash
   docker network inspect survey-dashboard-local_default
   ```

   Should show both nginx-proxy and dashboard.

4. **Restart both containers:**
   ```bash
   docker-compose restart nginx-proxy dashboard
   ```

### Issue 4: WebSockets Not Working

**Symptoms:** Dashboard loads but buttons/filters don't work.

**Steps:**

1. **Check vhost.d/default exists:**
   ```bash
   ls -la nginx/vhost.d/default
   ```

2. **Verify WebSocket config content:**
   ```bash
   cat nginx/vhost.d/default
   ```

   Should contain:
   ```
   proxy_http_version 1.1;
   proxy_set_header Upgrade $http_upgrade;
   proxy_set_header Connection "upgrade";
   ```

3. **Restart nginx-proxy:**
   ```bash
   docker-compose restart nginx-proxy
   ```

4. **Check browser console (F12):**
   - Look for WebSocket connection errors
   - Should see successful WS connection

### Issue 5: Changes Not Reflected After Rebuild

**Cause:** Docker using cached layers.

**Solution:**

```bash
# Force complete rebuild without cache
docker-compose build --no-cache

# Or rebuild specific service
docker-compose build --no-cache dashboard

# Then restart
docker-compose up -d
```

### Issue 6: acme-companion Logs Show Errors

**This is NORMAL for local testing!**

acme-companion will show errors like:
```
ERROR: localhost is not a valid domain for Let's Encrypt
```

**Why:** Let's Encrypt requires a real domain. This is expected with `HOST=localhost`.

**Solution:** Ignore these errors during local testing. They won't occur in production with a real domain.

---

## Cleanup

### Stop and Remove Containers

```bash
# Stop containers (preserves volumes)
docker-compose --env-file .env.local down

# Stop and remove volumes (complete cleanup)
docker-compose --env-file .env.local down -v
```

### Remove Local Testing Environment File

```bash
rm .env.local
```

### Remove Docker Images (Optional)

```bash
# List images
docker images | grep survey-dashboard

# Remove specific image
docker rmi survey-dashboard-local_dashboard

# Remove all unused images
docker image prune -a
```

### Clean Up Nginx Directories

If you want to start fresh:

```bash
# Remove generated nginx files (certificates, etc.)
rm -rf nginx/certs/*
rm -rf nginx/html/*

# Keep vhost.d/default (it's part of your config)
```

---

## Key Differences: Local vs Production

| Aspect | Local Testing | Production |
|--------|---------------|------------|
| Domain | `localhost` | Real domain (e.g., `dashboard.survey.helmholtz-metadaten.de`) |
| HTTPS | ❌ Not available | ✅ Let's Encrypt SSL |
| Protocol | HTTP only | HTTPS (HTTP redirects to HTTPS) |
| Certificate | None | Valid Let's Encrypt certificate |
| Access | Only from local machine | Accessible from internet |
| DNS | Not needed | Must be configured |
| Firewall | Not needed | Ports 80, 443 must be open |
| Email | Dummy value | Real email for notifications |

---

## What to Test Before Production

### Critical Tests ✅

Run these tests locally before production deployment:

1. **Docker Build:** `docker-compose build` completes without errors
2. **Container Startup:** All 3 containers start and stay running
3. **Dashboard Access:** Dashboard loads at correct path
4. **Path Routing:** Only specified path accessible, others blocked
5. **WebSockets:** Interactive elements work (check browser DevTools)
6. **Rebuild:** Code changes reflected after rebuild
7. **Restart:** Clean restart after `down` and `up`

### Cannot Test Locally ⚠️

These can only be tested in production:

1. **SSL/HTTPS:** Requires real domain
2. **Let's Encrypt:** Certificate acquisition
3. **DNS Resolution:** Public DNS records
4. **External Access:** Access from internet
5. **Auto-renewal:** Certificate renewal after 60 days

---

## Quick Test Commands

```bash
# Start local test environment
docker-compose --env-file .env.local up -d --build

# Check status
docker-compose ps

# Test HTTP access
curl -I http://localhost/2021community/

# Test root path is blocked
curl -I http://localhost/

# View logs
docker-compose logs -f dashboard

# Stop and clean up
docker-compose --env-file .env.local down

# Complete cleanup (removes volumes too)
docker-compose --env-file .env.local down -v
```

---

## Next Steps After Successful Local Testing

Once all local tests pass:

1. ✅ Review DEPLOYMENT.md for production steps
2. ✅ Ensure you have a real domain and it points to your VM
3. ✅ Create production `.env` file with real values
4. ✅ Follow DEPLOYMENT.md step-by-step on production VM
5. ✅ Monitor Let's Encrypt certificate acquisition
6. ✅ Verify HTTPS access works in production

---

**Last Updated:** 2024-11-03
**Purpose:** Local testing before production deployment
**Environment:** Docker Compose on local development machine
