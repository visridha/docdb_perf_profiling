#!/bin/bash
# Quick start script for running DocumentDB performance tests with Locust

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}DocumentDB Performance Testing with Locust${NC}"
echo "=============================================="
echo ""

# Check if .env file exists
if [ ! -f .env ]; then
    echo -e "${YELLOW}Warning: .env file not found${NC}"
    echo "Creating .env from template..."
    cp config/.env.example .env
    echo -e "${YELLOW}Please edit .env with your DocumentDB credentials before running tests${NC}"
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -q -r ../requirements.txt

# Parse command line arguments
SCENARIO="locustfile.py"
MODE="web"
USERS=10
SPAWN_RATE=1
RUN_TIME="5m"

while [[ $# -gt 0 ]]; do
    case $1 in
        --scenario)
            SCENARIO="$2"
            shift 2
            ;;
        --headless)
            MODE="headless"
            shift
            ;;
        --users)
            USERS="$2"
            shift 2
            ;;
        --spawn-rate)
            SPAWN_RATE="$2"
            shift 2
            ;;
        --run-time)
            RUN_TIME="$2"
            shift 2
            ;;
        --help)
            echo "Usage: $0 [OPTIONS]"
            echo ""
            echo "Options:"
            echo "  --scenario SCENARIO     Scenario to run (locustfile.py, scenarios/read_heavy.py, etc.)"
            echo "  --headless              Run in headless mode (no web UI)"
            echo "  --users N               Number of concurrent users (default: 10)"
            echo "  --spawn-rate N          User spawn rate per second (default: 1)"
            echo "  --run-time DURATION     Test duration (default: 5m)"
            echo "  --help                  Show this help message"
            echo ""
            echo "Examples:"
            echo "  $0                                      # Run with web UI"
            echo "  $0 --scenario scenarios/read_heavy.py   # Run read-heavy scenario"
            echo "  $0 --headless --users 50 --run-time 10m # Headless mode with 50 users for 10 minutes"
            exit 0
            ;;
        *)
            echo -e "${RED}Unknown option: $1${NC}"
            echo "Use --help for usage information"
            exit 1
            ;;
    esac
done

# Load environment variables
set -a
source .env
set +a

echo ""
echo "Test Configuration:"
echo "  Scenario: $SCENARIO"
echo "  Mode: $MODE"
echo "  Users: $USERS"
echo "  Spawn Rate: $SPAWN_RATE"
echo "  Run Time: $RUN_TIME"
echo "  Host: $DOCDB_HOST"
echo ""

# Run Locust
if [ "$MODE" = "web" ]; then
    echo -e "${GREEN}Starting Locust web UI...${NC}"
    echo "Open http://localhost:8089 in your browser"
    echo ""
    locust -f "$SCENARIO"
else
    echo -e "${GREEN}Starting Locust in headless mode...${NC}"
    echo ""
    locust -f "$SCENARIO" --headless --users "$USERS" --spawn-rate "$SPAWN_RATE" --run-time "$RUN_TIME" --html report.html
    echo ""
    echo -e "${GREEN}Test completed! Report saved to report.html${NC}"
fi
