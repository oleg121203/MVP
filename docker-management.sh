#!/bin/bash

# Docker Management Script for Ventai App

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to display menu
define_menu() {
    clear
    echo -e "${GREEN}=== Ventai Docker Management Script ===${NC}"
    echo "1. Build Containers"
    echo "2. Clean Up Resources"
    echo "3. Manage Individual Containers"
    echo "4. Manage Ports"
    echo "5. Exit"
    echo -e "${YELLOW}Select an option [1-5]: ${NC}"
}

# Function for build menu
define_build_menu() {
    clear
    echo -e "${GREEN}=== Build Containers ===${NC}"
    echo "1. Build with Cache"
    echo "2. Build without Cache"
    echo "3. Back to Main Menu"
    echo -e "${YELLOW}Select an option [1-3]: ${NC}"
}

# Function for cleanup menu
define_cleanup_menu() {
    clear
    echo -e "${GREEN}=== Clean Up Resources ===${NC}"
    echo "1. Stop and Remove All Containers"
    echo "2. Remove All Docker Resources (Full Cleanup)"
    echo "3. Back to Main Menu"
    echo -e "${YELLOW}Select an option [1-3]: ${NC}"
}

# Function for container management menu
define_container_menu() {
    clear
    echo -e "${GREEN}=== Manage Individual Containers ===${NC}"
    echo "1. Start Specific Container"
    echo "2. Stop Specific Container"
    echo "3. Back to Main Menu"
    echo -e "${YELLOW}Select an option [1-3]: ${NC}"
}

# Function for port management menu
define_port_menu() {
    clear
    echo -e "${GREEN}=== Manage Ports ===${NC}"
    echo "1. Check Port Status"
    echo "2. Kill Processes on Specific Ports (3000, 8000, 5433, 6380)"
    echo "3. Back to Main Menu"
    echo -e "${YELLOW}Select an option [1-3]: ${NC}"
}

# Function to stop and remove containers
stop_and_remove_containers() {
    echo -e "${YELLOW}Stopping and removing all containers...${NC}"
    docker-compose -f docker-compose.dev.yml down --remove-orphans
    echo -e "${GREEN}Done.${NC}"
}

# Function for full cleanup
full_cleanup() {
    echo -e "${YELLOW}Performing full cleanup of Docker resources...${NC}"
    docker-compose -f docker-compose.dev.yml down --volumes --remove-orphans
    echo -e "${RED}WARNING: This will remove all Docker images, containers, volumes, and networks.${NC}"
    read -p "Are you sure you want to continue? (y/N): " confirm
    if [[ "$confirm" =~ ^[Yy]$ ]]; then
        docker system prune -a --volumes
        echo -e "${GREEN}Full cleanup completed.${NC}"
    else
        echo -e "${RED}Full cleanup aborted.${NC}"
    fi
}

# Function to build with cache
build_with_cache() {
    echo -e "${YELLOW}Building containers with cache...${NC}"
    docker-compose -f docker-compose.dev.yml build
    echo -e "${GREEN}Build with cache completed.${NC}"
}

# Function to build without cache
build_without_cache() {
    echo -e "${YELLOW}Building containers without cache...${NC}"
    docker-compose -f docker-compose.dev.yml build --no-cache
    echo -e "${GREEN}Build without cache completed.${NC}"
}

# Function to start specific container
start_container() {
    echo -e "${GREEN}Available containers:${NC}"
    echo "1. frontend"
    echo "2. backend"
    echo "3. db (PostgreSQL)"
    echo "4. redis"
    read -p "Select container to start [1-4]: " container_choice
    case $container_choice in
        1) container="frontend" ;;
        2) container="backend" ;;
        3) container="db" ;;
        4) container="redis" ;;
        *) echo -e "${RED}Invalid choice.${NC}"; return ;;
    esac
    echo -e "${YELLOW}Starting $container container...${NC}"
    docker-compose -f docker-compose.dev.yml up -d $container
    echo -e "${GREEN}Started $container container.${NC}"
}

# Function to stop specific container
stop_container() {
    echo -e "${GREEN}Available containers:${NC}"
    echo "1. frontend"
    echo "2. backend"
    echo "3. db (PostgreSQL)"
    echo "4. redis"
    read -p "Select container to stop [1-4]: " container_choice
    case $container_choice in
        1) container="frontend" ;;
        2) container="backend" ;;
        3) container="db" ;;
        4) container="redis" ;;
        *) echo -e "${RED}Invalid choice.${NC}"; return ;;
    esac
    echo -e "${YELLOW}Stopping $container container...${NC}"
    docker-compose -f docker-compose.dev.yml stop $container
    echo -e "${GREEN}Stopped $container container.${NC}"
}

# Function to check port status
check_port_status() {
    echo -e "${YELLOW}Checking status of ports 3000, 8000, 5433, and 6380...${NC}"
    for port in 3000 8000 5433 6380; do
        if lsof -i :$port >/dev/null; then
            echo -e "${RED}Port $port is in use.${NC}"
            lsof -i :$port
        else
            echo -e "${GREEN}Port $port is free.${NC}"
        fi
    done
}

# Function to kill processes on specific ports
kill_port_processes() {
    echo -e "${YELLOW}Killing processes on ports 3000, 8000, 5433, and 6380...${NC}"
    for port in 3000 8000 5433 6380; do
        if lsof -i :$port >/dev/null; then
            echo -e "${RED}Killing processes on port $port...${NC}"
            lsof -t -i :$port | xargs kill -9
            echo -e "${GREEN}Processes on port $port terminated.${NC}"
        else
            echo -e "${GREEN}No processes found on port $port.${NC}"
        fi
    done
}

# Main loop
while true; do
    define_menu
    read choice
    case $choice in
        1)
            while true; do
                define_build_menu
                read build_choice
                case $build_choice in
                    1) build_with_cache ; read -p "Press Enter to continue..." ;;
                    2) build_without_cache ; read -p "Press Enter to continue..." ;;
                    3) break ;;
                    *) echo -e "${RED}Invalid choice. Please select 1, 2, or 3.${NC}" ; read -p "Press Enter to continue..." ;;
                esac
            done
            ;;
        2)
            while true; do
                define_cleanup_menu
                read cleanup_choice
                case $cleanup_choice in
                    1) stop_and_remove_containers ; read -p "Press Enter to continue..." ;;
                    2) full_cleanup ; read -p "Press Enter to continue..." ;;
                    3) break ;;
                    *) echo -e "${RED}Invalid choice. Please select 1, 2, or 3.${NC}" ; read -p "Press Enter to continue..." ;;
                esac
            done
            ;;
        3)
            while true; do
                define_container_menu
                read container_choice
                case $container_choice in
                    1) start_container ; read -p "Press Enter to continue..." ;;
                    2) stop_container ; read -p "Press Enter to continue..." ;;
                    3) break ;;
                    *) echo -e "${RED}Invalid choice. Please select 1, 2, or 3.${NC}" ; read -p "Press Enter to continue..." ;;
                esac
            done
            ;;
        4)
            while true; do
                define_port_menu
                read port_choice
                case $port_choice in
                    1) check_port_status ; read -p "Press Enter to continue..." ;;
                    2) kill_port_processes ; read -p "Press Enter to continue..." ;;
                    3) break ;;
                    *) echo -e "${RED}Invalid choice. Please select 1, 2, or 3.${NC}" ; read -p "Press Enter to continue..." ;;
                esac
            done
            ;;
        5)
            echo -e "${GREEN}Exiting script. Goodbye!${NC}"
            exit 0
            ;;
        *)
            echo -e "${RED}Invalid choice. Please select a number between 1 and 5.${NC}"
            read -p "Press Enter to continue..."
            ;;
    esac
done
