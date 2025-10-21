#!/bin/bash
# Windsurf Privacy Toolkit - Terminal Menu
# Interactive menu for all privacy tools

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
NC='\033[0m'

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

show_banner() {
    clear
    echo -e "${CYAN}"
    echo "╔════════════════════════════════════════════════════════════╗"
    echo "║                                                            ║"
    echo "║        WINDSURF PRIVACY TOOLKIT v2.1                       ║"
    echo "║        Terminal Edition                                    ║"
    echo "║                                                            ║"
    echo "╚════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
    echo ""
}

show_menu() {
    echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
    echo -e "${YELLOW}  MAIN MENU${NC}"
    echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
    echo ""
    echo -e "${GREEN}1)${NC} 🔍 Audit Windsurf Access"
    echo -e "   ${CYAN}→ Scan for tracking data and privacy issues${NC}"
    echo ""
    echo -e "${GREEN}2)${NC} 🧹 Enhanced Cleanup"
    echo -e "   ${CYAN}→ Clear tracking data (with venv preservation)${NC}"
    echo ""
    echo -e "${GREEN}3)${NC} 💾 Export Chat History"
    echo -e "   ${CYAN}→ Backup all Cascade conversations to CSV/JSON${NC}"
    echo ""
    echo -e "${GREEN}4)${NC} 🔒 Prevent MachineID Regeneration"
    echo -e "   ${CYAN}→ Block tracking ID recreation${NC}"
    echo ""
    echo -e "${GREEN}5)${NC} 🌐 Track Google Cloud Connections"
    echo -e "   ${CYAN}→ Monitor network activity${NC}"
    echo ""
    echo -e "${GREEN}6)${NC} 📊 Launch GUI Version"
    echo -e "   ${CYAN}→ Open full graphical interface${NC}"
    echo ""
    echo -e "${GREEN}7)${NC} ℹ️  Show Documentation"
    echo -e "   ${CYAN}→ View README and guides${NC}"
    echo ""
    echo -e "${RED}0)${NC} ❌ Exit"
    echo ""
    echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
    echo ""
}

audit_windsurf() {
    show_banner
    echo -e "${CYAN}Running Windsurf Access Audit...${NC}"
    echo ""
    
    if [ -f "$SCRIPT_DIR/audit_windsurf_access.sh" ]; then
        bash "$SCRIPT_DIR/audit_windsurf_access.sh"
    else
        echo -e "${RED}Error: audit_windsurf_access.sh not found${NC}"
    fi
    
    echo ""
    read -p "Press Enter to continue..."
}

run_cleanup() {
    show_banner
    echo -e "${CYAN}Starting Enhanced Cleanup...${NC}"
    echo ""
    
    if [ -f "$SCRIPT_DIR/clear_windsurf_tracking_ENHANCED.sh" ]; then
        bash "$SCRIPT_DIR/clear_windsurf_tracking_ENHANCED.sh"
    else
        echo -e "${RED}Error: clear_windsurf_tracking_ENHANCED.sh not found${NC}"
    fi
    
    echo ""
    read -p "Press Enter to continue..."
}

export_chats() {
    show_banner
    echo -e "${CYAN}Exporting Chat History...${NC}"
    echo ""
    
    if [ -f "$SCRIPT_DIR/backup_windsurf_chat.sh" ]; then
        bash "$SCRIPT_DIR/backup_windsurf_chat.sh"
    else
        echo -e "${RED}Error: backup_windsurf_chat.sh not found${NC}"
    fi
    
    echo ""
    read -p "Press Enter to continue..."
}

prevent_machineid() {
    show_banner
    echo -e "${CYAN}Preventing MachineID Regeneration...${NC}"
    echo ""
    
    if [ -f "$SCRIPT_DIR/prevent_machineid_regeneration.sh" ]; then
        bash "$SCRIPT_DIR/prevent_machineid_regeneration.sh"
    else
        echo -e "${RED}Error: prevent_machineid_regeneration.sh not found${NC}"
    fi
    
    echo ""
    read -p "Press Enter to continue..."
}

track_connections() {
    show_banner
    echo -e "${CYAN}Tracking Google Cloud Connections...${NC}"
    echo ""
    echo "Choose tracking method:"
    echo "  1) Connection tracking (lsof)"
    echo "  2) Packet capture (tcpdump - requires sudo)"
    echo ""
    read -p "Select option (1-2): " TRACK_OPTION
    
    case $TRACK_OPTION in
        1)
            if [ -f "$SCRIPT_DIR/track_google_cloud_connections.sh" ]; then
                bash "$SCRIPT_DIR/track_google_cloud_connections.sh"
            else
                echo -e "${RED}Error: track_google_cloud_connections.sh not found${NC}"
            fi
            ;;
        2)
            if [ -f "$SCRIPT_DIR/track_google_cloud_packets.sh" ]; then
                bash "$SCRIPT_DIR/track_google_cloud_packets.sh"
            else
                echo -e "${RED}Error: track_google_cloud_packets.sh not found${NC}"
            fi
            ;;
        *)
            echo -e "${RED}Invalid option${NC}"
            ;;
    esac
    
    echo ""
    read -p "Press Enter to continue..."
}

launch_gui() {
    show_banner
    echo -e "${CYAN}Launching GUI...${NC}"
    echo ""
    
    if [ -f "$SCRIPT_DIR/windsurf_privacy_gui.py" ]; then
        python3 "$SCRIPT_DIR/windsurf_privacy_gui.py" &
        echo -e "${GREEN}✅ GUI launched in background${NC}"
        sleep 2
    else
        echo -e "${RED}Error: windsurf_privacy_gui.py not found${NC}"
    fi
    
    echo ""
    read -p "Press Enter to continue..."
}

show_docs() {
    show_banner
    echo -e "${CYAN}Available Documentation:${NC}"
    echo ""
    
    docs=(
        "README.md:Main README"
        "GUI_README.md:GUI User Guide"
        "VENV_PRESERVATION_FEATURE.md:Virtual Environment Preservation"
        "GOOGLE_CLOUD_TRACKING_GUIDE.md:Google Cloud Tracking"
        "HISTORICAL_ACCESS_DELETION_GUIDE.md:Historical Access Deletion"
        "APP_LAUNCHER_README.md:Desktop Launcher Guide"
    )
    
    for i in "${!docs[@]}"; do
        IFS=':' read -r file desc <<< "${docs[$i]}"
        if [ -f "$SCRIPT_DIR/$file" ]; then
            echo -e "${GREEN}$((i+1)))${NC} $desc"
            echo -e "   ${CYAN}→ $file${NC}"
        fi
    done
    
    echo ""
    echo -e "${GREEN}0)${NC} Back to main menu"
    echo ""
    read -p "Select document to view (0-${#docs[@]}): " DOC_CHOICE
    
    if [ "$DOC_CHOICE" -gt 0 ] && [ "$DOC_CHOICE" -le "${#docs[@]}" ]; then
        IFS=':' read -r file desc <<< "${docs[$((DOC_CHOICE-1))]}"
        if [ -f "$SCRIPT_DIR/$file" ]; then
            clear
            echo -e "${CYAN}═══════════════════════════════════════════════════════════${NC}"
            echo -e "${YELLOW}  $desc${NC}"
            echo -e "${CYAN}═══════════════════════════════════════════════════════════${NC}"
            echo ""
            cat "$SCRIPT_DIR/$file" | less -R
        fi
    fi
}

# Main loop
while true; do
    show_banner
    show_menu
    read -p "Select option (0-7): " CHOICE
    
    case $CHOICE in
        1)
            audit_windsurf
            ;;
        2)
            run_cleanup
            ;;
        3)
            export_chats
            ;;
        4)
            prevent_machineid
            ;;
        5)
            track_connections
            ;;
        6)
            launch_gui
            ;;
        7)
            show_docs
            ;;
        0)
            clear
            echo -e "${GREEN}Thank you for using Windsurf Privacy Toolkit!${NC}"
            echo ""
            exit 0
            ;;
        *)
            echo -e "${RED}Invalid option. Please try again.${NC}"
            sleep 2
            ;;
    esac
done
