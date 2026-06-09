#!/bin/bash

echo "🚀 Database Query Optimizer - Starting"
echo "========================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check Docker
echo -e "${YELLOW}[1/4]${NC} Checking Docker..."
if ! command -v docker &> /dev/null; then
    echo -e "${RED}❌ Docker is not installed${NC}"
    exit 1
fi
echo -e "${GREEN}✅ Docker found${NC}"

# Start PostgreSQL in Docker
echo -e "${YELLOW}[2/4]${NC} Starting PostgreSQL container..."
docker-compose up -d
sleep 5

# Check database connection
echo -e "${YELLOW}[3/4]${NC} Waiting for database to be ready..."
max_attempts=30
attempt=0
while ! docker-compose exec -T postgres pg_isready -U banking_user > /dev/null 2>&1; do
    attempt=$((attempt + 1))
    if [ $attempt -ge $max_attempts ]; then
        echo -e "${RED}❌ Database failed to start${NC}"
        exit 1
    fi
    sleep 1
done
echo -e "${GREEN}✅ Database is ready${NC}"

# Install Python dependencies
echo -e "${YELLOW}[4/4]${NC} Installing Python dependencies..."
cd backend
pip install -r requirements.txt
echo -e "${GREEN}✅ Dependencies installed${NC}"

# Set up environment variables
if [ ! -f .env ]; then
    cp .env.example .env
    echo -e "${YELLOW}⚠️  Please update .env with your ANTHROPIC_API_KEY${NC}"
fi

# Start Flask app
echo ""
echo -e "${GREEN}✨ Starting Flask application...${NC}"
echo -e "${GREEN}📱 Dashboard will be available at: http://localhost:5000${NC}"
echo ""

python app.py
