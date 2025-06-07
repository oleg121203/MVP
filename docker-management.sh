#!/bin/bash

# Docker Management Script for VentAI App
# This script provides an interactive menu to manage Docker containers for both production and development environments.

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to display the main menu
main_menu() {
    clear
    echo -e "${GREEN}=== VentAI Docker Management Script ===${NC}"
    echo "1. Build Containers"
    echo "2. Clean Up Docker Resources"
    echo "3. Manage Production Containers"
    echo "4. Manage Development Containers"
    echo "5. Manage Ports"
    echo "6. Exit"
    echo -e -n "${YELLOW}Select an option (1-6): ${NC}"
    read choice
    case $choice in
        1) build_menu ;;
        2) cleanup_menu ;;
        3) production_menu ;;
        4) development_menu ;;
        5) port_menu ;;
        6) exit 0 ;;
        *) echo -e "${RED}Invalid option. Please try again.${NC}" ; sleep 2 ; main_menu ;;
    esac
}

# Function to display the build menu
build_menu() {
    clear
    echo -e "${GREEN}=== Build Containers ===${NC}"
    echo "1. Build Production Containers (with cache)"
    echo "2. Build Production Containers (no cache)"
    echo "3. Build Development Containers (with cache)"
    echo "4. Build Development Containers (no cache)"
    echo "5. Back to Main Menu"
    echo -e -n "${YELLOW}Select an option (1-5): ${NC}"
    read choice
    case $choice in
        1) echo -e "${YELLOW}Building production containers with cache...${NC}" ; docker-compose -f docker-compose.yml build ; echo -e "${GREEN}Done.${NC}" ; sleep 2 ; build_menu ;;
        2) echo -e "${YELLOW}Building production containers without cache...${NC}" ; docker-compose -f docker-compose.yml build --no-cache ; echo -e "${GREEN}Done.${NC}" ; sleep 2 ; build_menu ;;
        3) echo -e "${YELLOW}Building development containers with cache...${NC}" ; docker-compose -f docker-compose.dev.yml build ; echo -e "${GREEN}Done.${NC}" ; sleep 2 ; build_menu ;;
        4) echo -e "${YELLOW}Building development containers without cache...${NC}" ; docker-compose -f docker-compose.dev.yml build --no-cache ; echo -e "${GREEN}Done.${NC}" ; sleep 2 ; build_menu ;;
        5) main_menu ;;
        *) echo -e "${RED}Invalid option. Please try again.${NC}" ; sleep 2 ; build_menu ;;
    esac
}

# Function to display the cleanup menu
cleanup_menu() {
    clear
    echo -e "${GREEN}=== Clean Up Docker Resources ===${NC}"
    echo "1. Stop and Remove All Production Containers"
    echo "2. Stop and Remove All Development Containers"
    echo "3. Full Cleanup (Images, Networks, Volumes)"
    echo "4. Back to Main Menu"
    echo -e -n "${YELLOW}Select an option (1-4): ${NC}"
    read choice
    case $choice in
        1) echo -e "${YELLOW}Stopping and removing all production containers...${NC}" ; docker-compose -f docker-compose.yml down ; echo -e "${GREEN}Done.${NC}" ; sleep 2 ; cleanup_menu ;;
        2) echo -e "${YELLOW}Stopping and removing all development containers...${NC}" ; docker-compose -f docker-compose.dev.yml down ; echo -e "${GREEN}Done.${NC}" ; sleep 2 ; cleanup_menu ;;
        3) echo -e "${YELLOW}Performing full cleanup...${NC}" ; docker-compose -f docker-compose.yml down --rmi all --volumes ; docker-compose -f docker-compose.dev.yml down --rmi all --volumes ; echo -e "${GREEN}Done.${NC}" ; sleep 2 ; cleanup_menu ;;
        4) main_menu ;;
        *) echo -e "${RED}Invalid option. Please try again.${NC}" ; sleep 2 ; cleanup_menu ;;
    esac
}

# Function to display the production container management menu
production_menu() {
    clear
    echo -e "${GREEN}=== Manage Production Containers ===${NC}"
    echo "1. Start All Production Containers"
    echo "2. Stop All Production Containers"
    echo "3. Start Frontend Container"
    echo "4. Stop Frontend Container"
    echo "5. Start Backend Container"
    echo "6. Stop Backend Container"
    echo "7. Start DB Container"
    echo "8. Stop DB Container"
    echo "9. Start Redis Container"
    echo "10. Stop Redis Container"
    echo "11. View Logs for Containers"
    echo "12. Back to Main Menu"
    echo -e -n "${YELLOW}Select an option (1-12): ${NC}"
    read choice
    case $choice in
        1) echo -e "${YELLOW}Starting all production containers...${NC}" ; docker-compose -f docker-compose.yml up -d ; echo -e "${GREEN}Done.${NC}" ; sleep 2 ; production_menu ;;
        2) echo -e "${YELLOW}Stopping all production containers...${NC}" ; docker-compose -f docker-compose.yml stop ; echo -e "${GREEN}Done.${NC}" ; sleep 2 ; production_menu ;;
        3) echo -e "${YELLOW}Starting production frontend container...${NC}" ; docker-compose -f docker-compose.yml start frontend ; echo -e "${GREEN}Done.${NC}" ; sleep 2 ; production_menu ;;
        4) echo -e "${YELLOW}Stopping production frontend container...${NC}" ; docker-compose -f docker-compose.yml stop frontend ; echo -e "${GREEN}Done.${NC}" ; sleep 2 ; production_menu ;;
        5) echo -e "${YELLOW}Starting production backend container...${NC}" ; docker-compose -f docker-compose.yml start backend ; echo -e "${GREEN}Done.${NC}" ; sleep 2 ; production_menu ;;
        6) echo -e "${YELLOW}Stopping production backend container...${NC}" ; docker-compose -f docker-compose.yml stop backend ; echo -e "${GREEN}Done.${NC}" ; sleep 2 ; production_menu ;;
        7) echo -e "${YELLOW}Starting production DB container...${NC}" ; docker-compose -f docker-compose.yml start db ; echo -e "${GREEN}Done.${NC}" ; sleep 2 ; production_menu ;;
        8) echo -e "${YELLOW}Stopping production DB container...${NC}" ; docker-compose -f docker-compose.yml stop db ; echo -e "${GREEN}Done.${NC}" ; sleep 2 ; production_menu ;;
        9) echo -e "${YELLOW}Starting production Redis container...${NC}" ; docker-compose -f docker-compose.yml start redis ; echo -e "${GREEN}Done.${NC}" ; sleep 2 ; production_menu ;;
        10) echo -e "${YELLOW}Stopping production Redis container...${NC}" ; docker-compose -f docker-compose.yml stop redis ; echo -e "${GREEN}Done.${NC}" ; sleep 2 ; production_menu ;;
        11) production_logs_menu ;;
        12) main_menu ;;
        *) echo -e "${RED}Invalid option. Please try again.${NC}" ; sleep 2 ; production_menu ;;
    esac
}

# Function to display logs menu for production containers
production_logs_menu() {
    clear
    echo -e "${GREEN}=== View Production Container Logs ===${NC}"
    echo "1. View Frontend Logs"
    echo "2. View Backend Logs"
    echo "3. View DB Logs"
    echo "4. View Redis Logs"
    echo "5. Back to Production Menu"
    echo -e -n "${YELLOW}Select an option (1-5): ${NC}"
    read choice
    case $choice in
        1) echo -e "${YELLOW}Showing logs for frontend container...${NC}" ; docker-compose -f docker-compose.yml logs frontend ; read -p "Press Enter to continue..." ; production_logs_menu ;;
        2) echo -e "${YELLOW}Showing logs for backend container...${NC}" ; docker-compose -f docker-compose.yml logs backend ; read -p "Press Enter to continue..." ; production_logs_menu ;;
        3) echo -e "${YELLOW}Showing logs for db container...${NC}" ; docker-compose -f docker-compose.yml logs db ; read -p "Press Enter to continue..." ; production_logs_menu ;;
        4) echo -e "${YELLOW}Showing logs for redis container...${NC}" ; docker-compose -f docker-compose.yml logs redis ; read -p "Press Enter to continue..." ; production_logs_menu ;;
        5) production_menu ;;
        *) echo -e "${RED}Invalid option. Please try again.${NC}" ; sleep 2 ; production_logs_menu ;;
    esac
}

# Function to display the development container management menu
development_menu() {
    clear
    echo -e "${GREEN}=== Manage Development Containers ===${NC}"
    echo "1. Start All Development Containers"
    echo "2. Stop All Development Containers"
    echo "3. Start Frontend Container"
    echo "4. Stop Frontend Container"
    echo "5. Start Backend Container"
    echo "6. Stop Backend Container"
    echo "7. Start DB Container"
    echo "8. Stop DB Container"
    echo "9. Start Redis Container"
    echo "10. Stop Redis Container"
    echo "11. View Logs for Containers"
    echo "12. Back to Main Menu"
    echo -e -n "${YELLOW}Select an option (1-12): ${NC}"
    read choice
    case $choice in
        1) echo -e "${YELLOW}Starting all development containers...${NC}" ; docker-compose -f docker-compose.dev.yml up -d ; echo -e "${GREEN}Done.${NC}" ; sleep 2 ; development_menu ;;
        2) echo -e "${YELLOW}Stopping all development containers...${NC}" ; docker-compose -f docker-compose.dev.yml stop ; echo -e "${GREEN}Done.${NC}" ; sleep 2 ; development_menu ;;
        3) echo -e "${YELLOW}Starting development frontend container...${NC}" ; docker-compose -f docker-compose.dev.yml start frontend ; echo -e "${GREEN}Done.${NC}" ; sleep 2 ; development_menu ;;
        4) echo -e "${YELLOW}Stopping development frontend container...${NC}" ; docker-compose -f docker-compose.dev.yml stop frontend ; echo -e "${GREEN}Done.${NC}" ; sleep 2 ; development_menu ;;
        5) echo -e "${YELLOW}Starting development backend container...${NC}" ; docker-compose -f docker-compose.dev.yml start backend ; echo -e "${GREEN}Done.${NC}" ; sleep 2 ; development_menu ;;
        6) echo -e "${YELLOW}Stopping development backend container...${NC}" ; docker-compose -f docker-compose.dev.yml stop backend ; echo -e "${GREEN}Done.${NC}" ; sleep 2 ; development_menu ;;
        7) echo -e "${YELLOW}Starting development DB container...${NC}" ; docker-compose -f docker-compose.dev.yml start db ; echo -e "${GREEN}Done.${NC}" ; sleep 2 ; development_menu ;;
        8) echo -e "${YELLOW}Stopping development DB container...${NC}" ; docker-compose -f docker-compose.dev.yml stop db ; echo -e "${GREEN}Done.${NC}" ; sleep 2 ; development_menu ;;
        9) echo -e "${YELLOW}Starting development Redis container...${NC}" ; docker-compose -f docker-compose.dev.yml start redis ; echo -e "${GREEN}Done.${NC}" ; sleep 2 ; development_menu ;;
        10) echo -e "${YELLOW}Stopping development Redis container...${NC}" ; docker-compose -f docker-compose.dev.yml stop redis ; echo -e "${GREEN}Done.${NC}" ; sleep 2 ; development_menu ;;
        11) development_logs_menu ;;
        12) main_menu ;;
        *) echo -e "${RED}Invalid option. Please try again.${NC}" ; sleep 2 ; development_menu ;;
    esac
}

# Function to display logs menu for development containers
development_logs_menu() {
    clear
    echo -e "${GREEN}=== View Development Container Logs ===${NC}"
    echo "1. View Frontend Logs"
    echo "2. View Backend Logs"
    echo "3. View DB Logs"
    echo "4. View Redis Logs"
    echo "5. Back to Development Menu"
    echo -e -n "${YELLOW}Select an option (1-5): ${NC}"
    read choice
    case $choice in
        1) echo -e "${YELLOW}Showing logs for frontend container...${NC}" ; docker-compose -f docker-compose.dev.yml logs frontend ; read -p "Press Enter to continue..." ; development_logs_menu ;;
        2) echo -e "${YELLOW}Showing logs for backend container...${NC}" ; docker-compose -f docker-compose.dev.yml logs backend ; read -p "Press Enter to continue..." ; development_logs_menu ;;
        3) echo -e "${YELLOW}Showing logs for db container...${NC}" ; docker-compose -f docker-compose.dev.yml logs db ; read -p "Press Enter to continue..." ; development_logs_menu ;;
        4) echo -e "${YELLOW}Showing logs for redis container...${NC}" ; docker-compose -f docker-compose.dev.yml logs redis ; read -p "Press Enter to continue..." ; development_logs_menu ;;
        5) development_menu ;;
        *) echo -e "${RED}Invalid option. Please try again.${NC}" ; sleep 2 ; development_logs_menu ;;
    esac
}

# Function to display the port management menu
port_menu() {
    clear
    echo -e "${GREEN}=== Manage Ports ===${NC}"
    echo "1. Check Port 3000 (Frontend)"
    echo "2. Kill Process on Port 3000"
    echo "3. Check Port 8000 (Backend)"
    echo "4. Kill Process on Port 8000"
    echo "5. Check Port 5433 (DB)"
    echo "6. Kill Process on Port 5433"
    echo "7. Check Port 6380 (Redis)"
    echo "8. Kill Process on Port 6380"
    echo "9. Back to Main Menu"
    echo -e -n "${YELLOW}Select an option (1-9): ${NC}"
    read choice
    case $choice in
        1) check_port 3000 ; port_menu ;;
        2) kill_port 3000 ; port_menu ;;
        3) check_port 8000 ; port_menu ;;
        4) kill_port 8000 ; port_menu ;;
        5) check_port 5433 ; port_menu ;;
        6) kill_port 5433 ; port_menu ;;
        7) check_port 6380 ; port_menu ;;
        8) kill_port 6380 ; port_menu ;;
        9) main_menu ;;
        *) echo -e "${RED}Invalid option. Please try again.${NC}" ; sleep 2 ; port_menu ;;
    esac
}

# Function to check if a port is in use
check_port() {
    local port=$1
    if lsof -i :$port > /dev/null; then
        echo -e "${RED}Port $port is in use.${NC}"
        lsof -i :$port
    else
        echo -e "${GREEN}Port $port is free.${NC}"
    fi
    read -p "Press Enter to continue..."
}

# Function to kill process on a port
kill_port() {
    local port=$1
    if lsof -i :$port > /dev/null; then
        echo -e "${YELLOW}Killing process on port $port...${NC}"
        kill -9 $(lsof -t -i :$port)
        echo -e "${GREEN}Done.${NC}"
    else
        echo -e "${GREEN}No process found on port $port.${NC}"
    fi
    read -p "Press Enter to continue..."
}

# Start the script by showing the main menu
main_menu
