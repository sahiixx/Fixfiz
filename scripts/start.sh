#!/bin/bash
# ================================================================================================
# NOWHERE.AI Platform - Start Script
# ================================================================================================
# Start all services

set -e

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${GREEN}================================================================================================${NC}"
echo -e "${GREEN}Starting NOWHERE.AI Platform${NC}"
echo -e "${GREEN}================================================================================================${NC}"

# Check if using Docker
if [ -f "docker-compose.yml" ] && command -v docker-compose &> /dev/null; then
    echo -e "${YELLOW}Starting with Docker Compose...${NC}"
    docker-compose up -d
    
    echo ""
    echo -e "${YELLOW}Waiting for services to be healthy...${NC}"
    sleep 10
    
    docker-compose ps
    
    echo ""
    echo -e "${GREEN}✅ All services started${NC}"
    echo ""
    echo "Frontend: http://localhost:3000"
    echo "Backend: http://localhost:8001"
    echo "API Docs: http://localhost:8001/docs"
    
elif command -v supervisorctl &> /dev/null; then
    echo -e "${YELLOW}Starting with Supervisor...${NC}"
    sudo supervisorctl restart all
    
    echo ""
    sleep 3
    sudo supervisorctl status
    
    echo ""
    echo -e "${GREEN}✅ All services started${NC}"
    
else
    echo -e "${YELLOW}Starting services manually...${NC}"
    
    # Start MongoDB
    if ! pgrep -x "mongod" > /dev/null; then
        echo "Starting MongoDB..."
        sudo systemctl start mongod
    fi
    
    # Start Backend
    echo "Starting Backend..."
    cd backend
    source venv/bin/activate 2>/dev/null || true
    nohup uvicorn server:app --host 0.0.0.0 --port 8001 > ../logs/backend.log 2>&1 &
    cd ..
    
    # Start Frontend
    echo "Starting Frontend..."
    cd frontend
    nohup yarn start > ../logs/frontend.log 2>&1 &
    cd ..
    
    echo ""
    echo -e "${GREEN}✅ All services started${NC}"
fi

echo ""
echo -e "${GREEN}================================================================================================${NC}"
