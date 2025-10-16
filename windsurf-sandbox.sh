#!/bin/bash

################################################################################
# Windsurf Sandbox Script
# Purpose: Restrict Windsurf IDE file access to only the current workspace
# Author: AIMF LLC Cybersecurity Research
# Date: October 7, 2025
################################################################################

set -e

SCRIPT_NAME="Windsurf Sandbox"
VERSION="1.0.0"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Windsurf process name
WINDSURF_PROCESS="Windsurf"
WINDSURF_APP="/Applications/Windsurf.app"

# Log file
LOG_FILE="$HOME/.windsurf-sandbox.log"

################################################################################
# Functions
################################################################################

print_banner() {
    echo -e "${BLUE}"
    echo "╔════════════════════════════════════════════════════════════╗"
    echo "║           Windsurf Sandbox - File Access Control          ║"
    echo "║                    Version $VERSION                           ║"
    echo "╚════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
}

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1" | tee -a "$LOG_FILE"
}

success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1" | tee -a "$LOG_FILE"
}

warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1" | tee -a "$LOG_FILE"
}

info() {
    echo -e "${BLUE}[INFO]${NC} $1" | tee -a "$LOG_FILE"
}

check_windsurf_running() {
    if pgrep -x "$WINDSURF_PROCESS" > /dev/null; then
        return 0
    else
        return 1
    fi
}

get_windsurf_pids() {
    pgrep -x "$WINDSURF_PROCESS" || echo ""
}

create_sandbox_profile() {
    local workspace_path="$1"
    local profile_path="$2"
    
    cat > "$profile_path" << EOF
(version 1)

; Deny all file access by default
(deny file-read* file-write*)

; Allow read/write only to the specified workspace
(allow file-read* file-write*
    (subpath "$workspace_path"))

; Allow read-only access to system libraries and frameworks
(allow file-read*
    (subpath "/System")
    (subpath "/Library")
    (subpath "/usr/lib")
    (subpath "/usr/share"))

; Allow read-only access to Windsurf application itself
(allow file-read*
    (subpath "$WINDSURF_APP"))

; Allow read/write to temporary directories (needed for operation)
(allow file-read* file-write*
    (subpath "/private/tmp")
    (subpath "/private/var/tmp"))

; Allow read/write to Windsurf's own config (in user Library)
(allow file-read* file-write*
    (subpath "$HOME/Library/Application Support/Windsurf")
    (subpath "$HOME/Library/Caches/Windsurf")
    (subpath "$HOME/Library/Preferences/com.codeium.windsurf.plist"))

; Deny network access to Google Cloud IPs
(deny network-outbound
    (remote ip "2607:f8b0:4005:812::200e")
    (remote ip "2607:f8b0:4005:810::200e")
    (remote ip "2607:f8b0:4005:812::200a")
    (remote ip "2607:f8b0:4005:813::2003"))

; Log denied operations
(deny file-read* file-write* (with send-signal SIGKILL))
EOF

    success "Sandbox profile created at: $profile_path"
}

apply_sandbox() {
    local workspace_path="$1"
    local profile_path="/tmp/windsurf-sandbox-$$.sb"
    
    # Validate workspace path
    if [ ! -d "$workspace_path" ]; then
        error "Workspace path does not exist: $workspace_path"
        return 1
    fi
    
    # Convert to absolute path
    workspace_path=$(cd "$workspace_path" && pwd)
    
    info "Creating sandbox profile for workspace: $workspace_path"
    create_sandbox_profile "$workspace_path" "$profile_path"
    
    # Check if Windsurf is running
    if check_windsurf_running; then
        warning "Windsurf is currently running. You must restart it for sandbox to take effect."
        echo ""
        read -p "Do you want to quit Windsurf now? (y/n): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            info "Quitting Windsurf..."
            osascript -e 'quit app "Windsurf"' 2>/dev/null || killall Windsurf 2>/dev/null || true
            sleep 2
        else
            warning "Sandbox will not be active until you restart Windsurf manually."
            return 1
        fi
    fi
    
    # Launch Windsurf with sandbox
    info "Launching Windsurf with sandbox restrictions..."
    sandbox-exec -f "$profile_path" open -a "$WINDSURF_APP" "$workspace_path" &
    
    # Store profile path for later cleanup
    echo "$profile_path" > "$HOME/.windsurf-sandbox-profile"
    echo "$workspace_path" > "$HOME/.windsurf-sandbox-workspace"
    
    success "Windsurf launched in sandboxed mode!"
    success "File access restricted to: $workspace_path"
    
    return 0
}

remove_sandbox() {
    info "Removing sandbox restrictions..."
    
    if check_windsurf_running; then
        info "Quitting sandboxed Windsurf..."
        osascript -e 'quit app "Windsurf"' 2>/dev/null || killall Windsurf 2>/dev/null || true
        sleep 2
    fi
    
    # Clean up profile
    if [ -f "$HOME/.windsurf-sandbox-profile" ]; then
        local profile_path=$(cat "$HOME/.windsurf-sandbox-profile")
        rm -f "$profile_path" 2>/dev/null || true
        rm -f "$HOME/.windsurf-sandbox-profile"
    fi
    
    if [ -f "$HOME/.windsurf-sandbox-workspace" ]; then
        rm -f "$HOME/.windsurf-sandbox-workspace"
    fi
    
    success "Sandbox removed. You can now launch Windsurf normally."
}

status_sandbox() {
    echo ""
    echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
    echo -e "${BLUE}                    Sandbox Status                         ${NC}"
    echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
    echo ""
    
    if [ -f "$HOME/.windsurf-sandbox-workspace" ]; then
        local workspace=$(cat "$HOME/.windsurf-sandbox-workspace")
        echo -e "${GREEN}✓ Sandbox is ACTIVE${NC}"
        echo -e "  Workspace: ${YELLOW}$workspace${NC}"
        echo ""
        
        if check_windsurf_running; then
            echo -e "${GREEN}✓ Windsurf is running (sandboxed)${NC}"
            echo -e "  PIDs: $(get_windsurf_pids)"
        else
            echo -e "${YELLOW}⚠ Windsurf is not running${NC}"
        fi
    else
        echo -e "${RED}✗ Sandbox is NOT active${NC}"
        echo ""
        
        if check_windsurf_running; then
            echo -e "${YELLOW}⚠ Windsurf is running (UNRESTRICTED)${NC}"
            echo -e "  PIDs: $(get_windsurf_pids)"
        else
            echo -e "  Windsurf is not running"
        fi
    fi
    
    echo ""
    echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
    echo ""
}

monitor_sandbox() {
    info "Starting sandbox monitor (Press Ctrl+C to stop)..."
    echo ""
    
    while true; do
        clear
        print_banner
        status_sandbox
        
        echo -e "${BLUE}File Access Attempts:${NC}"
        echo "Monitoring system logs for denied file operations..."
        echo ""
        
        # Monitor system logs for sandbox violations
        log show --predicate 'eventMessage contains "sandbox"' --last 1m --style compact 2>/dev/null | \
            grep -i "windsurf\|deny" | tail -10 || echo "No violations detected in last minute"
        
        echo ""
        echo -e "${YELLOW}Refreshing in 5 seconds... (Ctrl+C to stop)${NC}"
        sleep 5
    done
}

show_help() {
    cat << EOF

${SCRIPT_NAME} v${VERSION}

USAGE:
    $0 [COMMAND] [OPTIONS]

COMMANDS:
    enable <workspace_path>    Enable sandbox for specified workspace
    disable                    Disable sandbox and restore normal access
    status                     Show current sandbox status
    monitor                    Monitor sandbox violations in real-time
    help                       Show this help message

EXAMPLES:
    # Enable sandbox for current directory
    $0 enable .

    # Enable sandbox for specific workspace
    $0 enable ~/Documents/MyProject

    # Check sandbox status
    $0 status

    # Monitor file access attempts
    $0 monitor

    # Disable sandbox
    $0 disable

NOTES:
    - Windsurf must be restarted for sandbox to take effect
    - Only the specified workspace will be accessible
    - Network access to Google Cloud IPs is blocked
    - System libraries remain accessible (read-only)

EOF
}

################################################################################
# Main
################################################################################

main() {
    print_banner
    
    # Check if running on macOS
    if [[ "$OSTYPE" != "darwin"* ]]; then
        error "This script only works on macOS"
        exit 1
    fi
    
    # Check if Windsurf is installed
    if [ ! -d "$WINDSURF_APP" ]; then
        error "Windsurf is not installed at: $WINDSURF_APP"
        exit 1
    fi
    
    # Parse command
    case "${1:-help}" in
        enable)
            if [ -z "$2" ]; then
                error "Please specify a workspace path"
                echo "Usage: $0 enable <workspace_path>"
                exit 1
            fi
            apply_sandbox "$2"
            echo ""
            status_sandbox
            ;;
        disable)
            remove_sandbox
            ;;
        status)
            status_sandbox
            ;;
        monitor)
            monitor_sandbox
            ;;
        help|--help|-h)
            show_help
            ;;
        *)
            error "Unknown command: $1"
            show_help
            exit 1
            ;;
    esac
}

# Run main function
main "$@"
