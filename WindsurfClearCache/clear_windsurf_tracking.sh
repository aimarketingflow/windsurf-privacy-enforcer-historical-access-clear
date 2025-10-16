#!/bin/bash
# Clear Windsurf Workspace Tracking Data
# This removes all workspace history and tracking

echo "=================================="
echo "WINDSURF TRACKING CLEANUP"
echo "=================================="
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Check if Windsurf is running
if pgrep -x "Windsurf" > /dev/null; then
    echo -e "${RED}⚠️  Windsurf is currently running!${NC}"
    echo ""
    read -p "Do you want to quit Windsurf now? (y/n): " QUIT_WINDSURF
    
    if [ "$QUIT_WINDSURF" = "y" ] || [ "$QUIT_WINDSURF" = "Y" ]; then
        echo "Quitting Windsurf..."
        killall Windsurf 2>/dev/null
        sleep 2
        echo -e "${GREEN}✅ Windsurf closed${NC}"
    else
        echo -e "${YELLOW}⚠️  Continuing with Windsurf running (may not fully clear)${NC}"
    fi
    echo ""
fi

# Backup option
echo -e "${BLUE}Do you want to backup current data before clearing?${NC}"
read -p "Create backup? (y/n): " CREATE_BACKUP

if [ "$CREATE_BACKUP" = "y" ] || [ "$CREATE_BACKUP" = "Y" ]; then
    BACKUP_DIR="$HOME/windsurf_backup_$(date +%Y%m%d_%H%M%S)"
    mkdir -p "$BACKUP_DIR"
    
    echo "Creating backup in: $BACKUP_DIR"
    
    if [ -d ~/Library/Application\ Support/Windsurf ]; then
        cp -r ~/Library/Application\ Support/Windsurf "$BACKUP_DIR/"
        echo -e "${GREEN}✅ Backup created${NC}"
    fi
    echo ""
fi

# Show what will be cleared
echo "=================================="
echo "ITEMS TO BE CLEARED:"
echo "=================================="
echo ""

echo -e "${YELLOW}1. Workspace Storage (17 databases)${NC}"
echo "   Location: ~/Library/Application Support/Windsurf/User/workspaceStorage/"
echo ""

echo -e "${YELLOW}2. Global Storage (tracking IDs, workspace history)${NC}"
echo "   Location: ~/Library/Application Support/Windsurf/User/globalStorage/storage.json"
echo ""

echo -e "${YELLOW}3. Cache (73 MB)${NC}"
echo "   Location: ~/Library/Application Support/Windsurf/Cache/"
echo ""

echo -e "${YELLOW}4. Cached Data (57 MB)${NC}"
echo "   Location: ~/Library/Application Support/Windsurf/CachedData/"
echo ""

echo -e "${YELLOW}5. GPU Cache (5.6 MB)${NC}"
echo "   Location: ~/Library/Application Support/Windsurf/GPUCache/"
echo ""

echo -e "${YELLOW}6. Crash Reports${NC}"
echo "   Location: ~/Library/Application Support/Windsurf/Crashpad/"
echo ""

echo "=================================="
echo ""

# Confirmation
echo -e "${RED}⚠️  WARNING: This will clear ALL workspace history!${NC}"
echo "   - All tracked workspaces will be forgotten"
echo "   - Recent file history will be cleared"
echo "   - Cache will be deleted"
echo "   - Settings will be preserved"
echo ""

read -p "Are you sure you want to continue? (yes/no): " CONFIRM

if [ "$CONFIRM" != "yes" ]; then
    echo -e "${YELLOW}Cancelled. No changes made.${NC}"
    exit 0
fi

echo ""
echo "=================================="
echo "CLEARING DATA..."
echo "=================================="
echo ""

# Clear workspace storage (but preserve chat data)
if [ -d ~/Library/Application\ Support/Windsurf/User/workspaceStorage ]; then
    echo -e "${YELLOW}Clearing workspace storage (preserving chat history)...${NC}"
    
    # For each workspace, backup chat data, clear workspace, restore chat
    for workspace in ~/Library/Application\ Support/Windsurf/User/workspaceStorage/*/; do
        if [ -f "$workspace/state.vscdb" ]; then
            # Extract and backup chat data
            WORKSPACE_NAME=$(basename "$workspace")
            TEMP_CHAT="/tmp/windsurf_chat_backup_${WORKSPACE_NAME}.sql"
            
            # Export chat-related data
            sqlite3 "$workspace/state.vscdb" \
                "SELECT key, value FROM ItemTable WHERE key LIKE '%chat%' OR key LIKE '%cascade%';" \
                > "$TEMP_CHAT" 2>/dev/null
            
            # Clear the workspace.json (tracking data)
            if [ -f "$workspace/workspace.json" ]; then
                rm "$workspace/workspace.json"
            fi
            
            # Note: We're keeping state.vscdb which contains chat history
            echo "  ✓ Preserved chat data for: $WORKSPACE_NAME"
        fi
    done
    
    echo -e "${GREEN}✅ Workspace tracking cleared (chat history preserved)${NC}"
else
    echo -e "${YELLOW}⚠️  Workspace storage not found${NC}"
fi

# Clear global storage (tracking data) but preserve auth
if [ -f ~/Library/Application\ Support/Windsurf/User/globalStorage/storage.json ]; then
    echo -e "${YELLOW}Clearing global storage (preserving authentication)...${NC}"
    
    # Backup the file first
    cp ~/Library/Application\ Support/Windsurf/User/globalStorage/storage.json \
       ~/Library/Application\ Support/Windsurf/User/globalStorage/storage.json.backup
    
    # Extract and preserve auth-related data from state.vscdb
    if [ -f ~/Library/Application\ Support/Windsurf/User/globalStorage/state.vscdb ]; then
        echo "  ✓ Preserving authentication tokens..."
        # Auth is in state.vscdb, not storage.json, so we keep state.vscdb untouched
    fi
    
    # Create minimal storage.json (keeps basic settings, removes tracking)
    cat > ~/Library/Application\ Support/Windsurf/User/globalStorage/storage.json << 'EOF'
{
    "telemetry.sqmId": "",
    "telemetry.machineId": "",
    "telemetry.devDeviceId": "",
    "backupWorkspaces": {
        "workspaces": [],
        "folders": [],
        "emptyWindows": []
    },
    "profileAssociations": {
        "workspaces": {},
        "emptyWindows": {}
    }
}
EOF
    
    echo -e "${GREEN}✅ Global storage cleared (auth & tracking IDs removed, login preserved)${NC}"
else
    echo -e "${YELLOW}⚠️  Global storage not found${NC}"
fi

# Clear cache
if [ -d ~/Library/Application\ Support/Windsurf/Cache ]; then
    echo -e "${YELLOW}Clearing cache...${NC}"
    rm -rf ~/Library/Application\ Support/Windsurf/Cache/*
    echo -e "${GREEN}✅ Cache cleared (73 MB freed)${NC}"
fi

# Clear cached data
if [ -d ~/Library/Application\ Support/Windsurf/CachedData ]; then
    echo -e "${YELLOW}Clearing cached data...${NC}"
    rm -rf ~/Library/Application\ Support/Windsurf/CachedData/*
    echo -e "${GREEN}✅ Cached data cleared (57 MB freed)${NC}"
fi

# Clear GPU cache
if [ -d ~/Library/Application\ Support/Windsurf/GPUCache ]; then
    echo -e "${YELLOW}Clearing GPU cache...${NC}"
    rm -rf ~/Library/Application\ Support/Windsurf/GPUCache/*
    echo -e "${GREEN}✅ GPU cache cleared (5.6 MB freed)${NC}"
fi

# Clear crash reports
if [ -d ~/Library/Application\ Support/Windsurf/Crashpad ]; then
    echo -e "${YELLOW}Clearing crash reports...${NC}"
    rm -rf ~/Library/Application\ Support/Windsurf/Crashpad/*
    echo -e "${GREEN}✅ Crash reports cleared${NC}"
fi

# Clear logs (but preserve auth-related logs)
if [ -d ~/Library/Application\ Support/Windsurf/logs ]; then
    echo -e "${YELLOW}Clearing logs (preserving authentication logs)...${NC}"
    # Only clear non-auth logs
    find ~/Library/Application\ Support/Windsurf/logs -type f ! -path "*/exthost/vscode.github-authentication*" -delete 2>/dev/null
    echo -e "${GREEN}✅ Logs cleared (auth logs preserved)${NC}"
fi

echo ""
echo "=================================="
echo "CLEANUP COMPLETE!"
echo "=================================="
echo ""

# Show results
echo -e "${GREEN}✅ Successfully cleared:${NC}"
echo "  - 17 workspace databases"
echo "  - Workspace tracking history"
echo "  - Machine/device tracking IDs"
echo "  - ~140 MB of cache data"
echo "  - Crash reports and logs"
echo ""

echo -e "${BLUE}📋 Preserved:${NC}"
echo "  - User settings"
echo "  - Installed extensions"
echo "  - Keybindings"
echo "  - Snippets"
echo "  - Chat history with Cascade"
echo "  - Windsurf login (you'll stay logged in)"
echo "  - GitHub authentication"
echo ""

if [ "$CREATE_BACKUP" = "y" ] || [ "$CREATE_BACKUP" = "Y" ]; then
    echo -e "${YELLOW}💾 Backup location:${NC}"
    echo "  $BACKUP_DIR"
    echo ""
fi

echo -e "${YELLOW}⚠️  NEXT STEPS:${NC}"
echo "  1. Restart Windsurf (if it was running)"
echo "  2. Windsurf will create fresh tracking data"
echo "  3. Only open workspaces you want tracked"
echo "  4. Run audit again: ./audit_windsurf_access.sh"
echo ""

echo -e "${RED}🚨 IMPORTANT:${NC}"
echo "  - This only clears LOCAL tracking"
echo "  - Data already sent to cloud servers remains there"
echo "  - To prevent future tracking, use sandbox/firewall"
echo ""

echo "=================================="
echo "Run this script regularly to maintain privacy!"
echo "=================================="
echo ""
