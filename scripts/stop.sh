#!/bin/bash
# ================================================================================================
# NOWHERE.AI Platform - Stop Script
# ================================================================================================
# Stop all services

set -e

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${YELLOW}================================================================================================${NC}"
echo -e "${YELLOW}Stopping NOWHERE.AI Platform${NC}"
echo -e "${YELLOW}================================================================================================${NC}"

# Check if using Docker
if [ -f "docker-compose.yml" ] && command -v docker-compose &> /dev/null; then
    echo -e "${YELLOW}Stopping Docker services...${NC}"
    docker-compose down
    
    echo ""
    echo -e "${GREEN}✅ All Docker services stopped${NC}"
    
elif command -v supervisorctl &> /dev/null; then
    echo -e "${YELLOW}Stopping Supervisor services...${NC}"
    sudo supervisorctl stop all
    
    echo ""
    sudo supervisorctl status
    
    echo ""
    echo -e "${GREEN}✅ All Supervisor services stopped${NC}"
    
else
    echo -e "${YELLOW}Stopping services manually...${NC}"
    
    # Stop Backend
    echo "Stopping Backend..."
    pkill -f "uvicorn server:app" || echo "Backend not running"
    
    # Stop Frontend
    echo "Stopping Frontend..."
    pkill -f "yarn start" || pkill -f "react-scripts start" || echo "Frontend not running"
    
    echo ""
    echo -e "${GREEN}✅ All services stopped${NC}"
fi

echo ""
echo -e "${GREEN}================================================================================================${NC}"
