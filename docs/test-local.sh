#!/bin/bash
# Quick local testing script for Survey Dashboard
# Tests the Docker deployment setup before production deployment

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Print colored message
print_status() {
    echo -e "${BLUE}==>${NC} $1"
}

print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

# Banner
echo ""
echo "=========================================="
echo "  Survey Dashboard - Local Testing"
echo "=========================================="
echo ""

# Check if .env.local exists
if [ ! -f .env.local ]; then
    print_warning ".env.local not found. Creating from template..."
    if [ -f .env.local.example ]; then
        cp .env.local.example .env.local
        print_success "Created .env.local from .env.local.example"
    else
        print_error ".env.local.example not found!"
        echo "Please create .env.local manually. See LOCAL_TESTING.md for details."
        exit 1
    fi
fi

# Check Docker is running
print_status "Checking Docker..."
if ! docker info > /dev/null 2>&1; then
    print_error "Docker is not running!"
    echo "Please start Docker and try again."
    exit 1
fi
print_success "Docker is running"

# Check Docker Compose is installed
print_status "Checking Docker Compose..."
if ! command -v docker-compose &> /dev/null; then
    print_error "Docker Compose is not installed!"
    echo "Please install Docker Compose and try again."
    exit 1
fi
print_success "Docker Compose is installed"

# Build and start containers
print_status "Building Docker images..."
if docker-compose --env-file .env.local build; then
    print_success "Docker images built successfully"
else
    print_error "Docker build failed!"
    exit 1
fi

print_status "Starting containers..."
if docker-compose --env-file .env.local up -d; then
    print_success "Containers started"
else
    print_error "Failed to start containers!"
    exit 1
fi

# Wait for containers to be ready
print_status "Waiting for containers to be ready..."
sleep 5

# Check container status
print_status "Checking container status..."
if docker-compose --env-file .env.local ps | grep -q "Up"; then
    print_success "Containers are running"
    docker-compose --env-file .env.local ps
else
    print_error "Some containers are not running!"
    docker-compose --env-file .env.local ps
    exit 1
fi

echo ""
print_status "Running connectivity tests..."
echo ""

# Read VIRTUAL_PATH from .env.local
VIRTUAL_PATH=$(grep VIRTUAL_PATH .env.local | cut -d= -f2)
if [ -z "$VIRTUAL_PATH" ]; then
    VIRTUAL_PATH="/"
    print_warning "VIRTUAL_PATH is empty, testing root path"
fi

# Test 1: Dashboard path should work
print_status "Test 1: Testing dashboard path (http://localhost${VIRTUAL_PATH}/)..."
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" "http://localhost${VIRTUAL_PATH}/")
if [ "$HTTP_CODE" == "200" ] || [ "$HTTP_CODE" == "302" ]; then
    print_success "Dashboard is accessible (HTTP $HTTP_CODE)"
else
    print_error "Dashboard returned HTTP $HTTP_CODE (expected 200 or 302)"
fi

# Test 2: Root path should fail (if VIRTUAL_PATH is not root)
if [ "$VIRTUAL_PATH" != "/" ]; then
    print_status "Test 2: Testing root path should be blocked (http://localhost/)..."
    HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" "http://localhost/")
    if [ "$HTTP_CODE" == "404" ] || [ "$HTTP_CODE" == "503" ]; then
        print_success "Root path is blocked (HTTP $HTTP_CODE)"
    else
        print_warning "Root path returned HTTP $HTTP_CODE (expected 404 or 503)"
    fi
fi

# Test 3: Check dashboard logs
print_status "Test 3: Checking dashboard logs..."
if docker-compose --env-file .env.local logs dashboard | grep -q "PRODUCTION mode"; then
    print_success "Dashboard started in production mode"
else
    print_warning "Could not verify production mode in logs"
fi

if docker-compose --env-file .env.local logs dashboard | grep -q "Using URL prefix"; then
    print_success "Dashboard is using URL prefix"
else
    if [ "$VIRTUAL_PATH" != "/" ]; then
        print_warning "Could not verify URL prefix in logs"
    fi
fi

# Summary
echo ""
echo "=========================================="
echo "  Test Summary"
echo "=========================================="
echo ""
print_success "Docker setup is working!"
echo ""
echo "Next steps:"
echo "  1. Open browser: http://localhost${VIRTUAL_PATH}/"
echo "  2. Verify dashboard loads and is interactive"
echo "  3. Check browser console (F12) for errors"
echo "  4. Test WebSocket connections in Network tab"
echo ""
echo "View logs:"
echo "  docker-compose --env-file .env.local logs -f"
echo ""
echo "Stop containers:"
echo "  docker-compose --env-file .env.local down"
echo ""
echo "See LOCAL_TESTING.md for detailed testing scenarios"
echo ""
