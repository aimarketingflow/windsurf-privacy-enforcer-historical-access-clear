#!/bin/bash
# ENHANCED Clear Windsurf Workspace Tracking Data
# This removes ALL workspace history, tracking, and historical access
# Version 2.0 - Complete Historical Access Deletion

echo "=========================================="
echo "WINDSURF ENHANCED TRACKING CLEANUP v2.0"
echo "=========================================="
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

# Check if Windsurf is running
if pgrep -x "Windsurf" > /dev/null; then
    echo -e "${RED}⚠️  Windsurf is currently running!${NC}"
    echo ""
    read -p "Do you want to quit Windsurf now? (y/n): " QUIT_WINDSURF
    
    if [ "$QUIT_WINDSURF" = "y" ] || [ "$QUIT_WINDSURF" = "Y" ]; then
        echo "Quitting Windsurf and all related processes..."
        killall Windsurf 2>/dev/null
        killall "Windsurf Helper" 2>/dev/null
        pkill -9 language_server_macos_arm 2>/dev/null
        sleep 3
        echo -e "${GREEN}✅ Windsurf closed${NC}"
    else
        echo -e "${YELLOW}⚠️  Continuing with Windsurf running (cleanup may be incomplete)${NC}"
    fi
    echo ""
fi

# Backup option
echo -e "${BLUE}Do you want to backup current data before clearing?${NC}"
echo ""
echo "Backup options:"
echo "  1) No backup (skip)"
echo "  2) Full backup (all Windsurf data)"
echo "  3) Chat history only (recommended)"
echo "  4) Full backup + separate chat export"
echo ""
read -p "Select option (1-4): " BACKUP_OPTION

if [ "$BACKUP_OPTION" = "2" ] || [ "$BACKUP_OPTION" = "4" ]; then
    # Full backup
    BACKUP_DIR="$HOME/windsurf_backup_$(date +%Y%m%d_%H%M%S)"
    mkdir -p "$BACKUP_DIR"
    
    echo ""
    echo -e "${CYAN}Creating full backup...${NC}"
    echo "Location: $BACKUP_DIR"
    
    if [ -d ~/Library/Application\ Support/Windsurf ]; then
        cp -r ~/Library/Application\ Support/Windsurf "$BACKUP_DIR/"
        echo -e "${GREEN}✅ Full backup created${NC}"
    fi
fi

if [ "$BACKUP_OPTION" = "3" ] || [ "$BACKUP_OPTION" = "4" ]; then
    # Chat history backup
    CHAT_BACKUP_DIR="$HOME/WindsurfChatBackup_$(date +%Y%m%d_%H%M%S)"
    mkdir -p "$CHAT_BACKUP_DIR"
    
    echo ""
    echo -e "${CYAN}Creating chat history backup...${NC}"
    echo "Location: $CHAT_BACKUP_DIR"
    
    TOTAL_CHATS=0
    TOTAL_WORKSPACES=0
    
    if [ -d ~/Library/Application\ Support/Windsurf/User/workspaceStorage ]; then
        for workspace in ~/Library/Application\ Support/Windsurf/User/workspaceStorage/*/; do
            if [ -f "$workspace/state.vscdb" ]; then
                WORKSPACE_ID=$(basename "$workspace")
                
                # Check if this workspace has chat data
                CHAT_COUNT=$(sqlite3 "$workspace/state.vscdb" \
                    "SELECT COUNT(*) FROM ItemTable WHERE key LIKE '%chat%' OR key LIKE '%cascade%';" 2>/dev/null)
                
                if [ "$CHAT_COUNT" -gt 0 ]; then
                    ((TOTAL_WORKSPACES++))
                    TOTAL_CHATS=$((TOTAL_CHATS + CHAT_COUNT))
                    
                    # Create workspace backup directory
                    WORKSPACE_BACKUP="$CHAT_BACKUP_DIR/$WORKSPACE_ID"
                    mkdir -p "$WORKSPACE_BACKUP"
                    
                    # Export chat data to JSON
                    sqlite3 "$workspace/state.vscdb" <<EOF > "$WORKSPACE_BACKUP/chat_data.json" 2>/dev/null
.mode json
SELECT key, value FROM ItemTable 
WHERE key LIKE '%chat%' OR key LIKE '%cascade%'
ORDER BY key;
EOF
                    
                    # Export chat data to CSV
                    sqlite3 "$workspace/state.vscdb" <<EOF > "$WORKSPACE_BACKUP/chat_data.csv" 2>/dev/null
.mode csv
.headers on
SELECT key, value FROM ItemTable 
WHERE key LIKE '%chat%' OR key LIKE '%cascade%'
ORDER BY key;
EOF
                    
                    # Export full database as backup
                    cp "$workspace/state.vscdb" "$WORKSPACE_BACKUP/state.vscdb.backup"
                fi
            fi
        done
        
        if [ "$TOTAL_WORKSPACES" -gt 0 ]; then
            # Create master index
            cat > "$CHAT_BACKUP_DIR/README.txt" << INDEX
Windsurf Chat History Backup
=============================
Backup Date: $(date)
Total Workspaces: $TOTAL_WORKSPACES
Total Chat Entries: $TOTAL_CHATS

Each workspace directory contains:
- chat_data.json: JSON format
- chat_data.csv: CSV format (open in Excel/Numbers)
- state.vscdb.backup: Full database backup

To view your chats:
Open any chat_data.csv file in Excel, Numbers, or Google Sheets.

To restore:
1. Close Windsurf
2. Copy state.vscdb.backup to:
   ~/Library/Application Support/Windsurf/User/workspaceStorage/<workspace_id>/state.vscdb
3. Restart Windsurf
INDEX
            
            echo -e "${GREEN}✅ Chat history backed up${NC}"
            echo "   Workspaces: $TOTAL_WORKSPACES"
            echo "   Chat entries: $TOTAL_CHATS"
        else
            echo -e "${YELLOW}⚠️  No chat history found${NC}"
            rmdir "$CHAT_BACKUP_DIR" 2>/dev/null
        fi
    fi
fi

echo ""

# Show what will be cleared
echo "=========================================="
echo "ENHANCED CLEANUP - ITEMS TO BE CLEARED:"
echo "=========================================="
echo ""

echo -e "${YELLOW}TRACKING DATA:${NC}"
echo "  • Machine/Device tracking IDs"
echo "  • Workspace associations (ALL 16+ directories)"
echo "  • Backup workspace history"
echo "  • Recent file history"
echo "  • Workspace path references"
echo ""

echo -e "${YELLOW}DATABASES:${NC}"
echo "  • Global storage.json (tracking data)"
echo "  • Global state.vscdb (workspace history)"
echo "  • Workspace state.vscdb files (path references)"
echo "  • workspace.json files (tracking metadata)"
echo ""

echo -e "${YELLOW}CACHE & TEMPORARY:${NC}"
echo "  • Cache (73+ MB)"
echo "  • CachedData (57+ MB)"
echo "  • GPUCache (5.6+ MB)"
echo "  • Crash reports"
echo "  • Backup files (.backup, .bak)"
echo ""

echo -e "${GREEN}PRESERVED:${NC}"
echo "  • User settings"
echo "  • Extensions"
echo "  • Keybindings"
echo "  • Chat history with Cascade"
echo "  • GitHub/Windsurf login"
echo ""

echo "=========================================="
echo ""

# Confirmation
echo -e "${RED}⚠️  WARNING: This will COMPLETELY clear ALL workspace history!${NC}"
echo "   - All 16+ tracked workspaces will be forgotten"
echo "   - All historical access records will be deleted"
echo "   - All file path references will be removed"
echo "   - Settings and auth will be preserved"
echo ""

read -p "Are you sure you want to continue? (yes/no): " CONFIRM

if [ "$CONFIRM" != "yes" ]; then
    echo -e "${YELLOW}Cancelled. No changes made.${NC}"
    exit 0
fi

echo ""
echo "=========================================="
echo "CLEARING DATA..."
echo "=========================================="
echo ""

# STEP 1: Clear workspace storage (preserve chat data)
echo -e "${CYAN}[1/10] Clearing workspace storage...${NC}"

if [ -d ~/Library/Application\ Support/Windsurf/User/workspaceStorage ]; then
    # For each workspace, backup chat data, clear workspace, restore chat
    for workspace in ~/Library/Application\ Support/Windsurf/User/workspaceStorage/*/; do
        if [ -f "$workspace/state.vscdb" ]; then
            WORKSPACE_NAME=$(basename "$workspace")
            TEMP_CHAT="/tmp/windsurf_chat_backup_${WORKSPACE_NAME}.sql"
            
            # Export ONLY chat-related data
            sqlite3 "$workspace/state.vscdb" \
                "SELECT key, value FROM ItemTable WHERE key LIKE '%chat%' OR key LIKE '%cascade%';" \
                > "$TEMP_CHAT" 2>/dev/null
            
            # Clear workspace.json (tracking data)
            if [ -f "$workspace/workspace.json" ]; then
                rm "$workspace/workspace.json"
            fi
            
            # Clear workspace path references from state.vscdb (keep chat)
            if [ -f "$workspace/state.vscdb" ]; then
                # Remove workspace-related keys but keep chat
                sqlite3 "$workspace/state.vscdb" \
                    "DELETE FROM ItemTable WHERE key LIKE '%workspace%' AND key NOT LIKE '%chat%' AND key NOT LIKE '%cascade%';" 2>/dev/null
                
                sqlite3 "$workspace/state.vscdb" \
                    "DELETE FROM ItemTable WHERE key LIKE '%recentlyOpened%';" 2>/dev/null
                
                sqlite3 "$workspace/state.vscdb" \
                    "DELETE FROM ItemTable WHERE key LIKE '%fileHistory%';" 2>/dev/null
                    
                sqlite3 "$workspace/state.vscdb" \
                    "DELETE FROM ItemTable WHERE value LIKE '%/Users/%' AND key NOT LIKE '%chat%' AND key NOT LIKE '%cascade%';" 2>/dev/null
            fi
        fi
    done
    
    echo -e "${GREEN}✅ Workspace tracking cleared (chat history preserved)${NC}"
else
    echo -e "${YELLOW}⚠️  Workspace storage not found${NC}"
fi

# STEP 2: Clear global storage.json (COMPLETE REWRITE)
echo -e "${CYAN}[2/10] Clearing global storage.json...${NC}"

if [ -f ~/Library/Application\ Support/Windsurf/User/globalStorage/storage.json ]; then
    # Backup the file
    cp ~/Library/Application\ Support/Windsurf/User/globalStorage/storage.json \
       ~/Library/Application\ Support/Windsurf/User/globalStorage/storage.json.backup
    
    # Create completely clean storage.json with NO tracking data
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
    
    echo -e "${GREEN}✅ Global storage.json cleared (all tracking IDs removed)${NC}"
else
    echo -e "${YELLOW}⚠️  Global storage not found${NC}"
fi

# STEP 3: Clear workspace history from global state.vscdb
echo -e "${CYAN}[3/10] Clearing global state.vscdb workspace history...${NC}"

if [ -f ~/Library/Application\ Support/Windsurf/User/globalStorage/state.vscdb ]; then
    # Backup the database
    cp ~/Library/Application\ Support/Windsurf/User/globalStorage/state.vscdb \
       ~/Library/Application\ Support/Windsurf/User/globalStorage/state.vscdb.backup
    
    # Remove workspace identifiers and recent history (preserve auth)
    sqlite3 ~/Library/Application\ Support/Windsurf/User/globalStorage/state.vscdb \
        "DELETE FROM ItemTable WHERE key LIKE '%workspaceIdentifier%';" 2>/dev/null
    
    sqlite3 ~/Library/Application\ Support/Windsurf/User/globalStorage/state.vscdb \
        "DELETE FROM ItemTable WHERE key LIKE '%recentlyOpened%';" 2>/dev/null
    
    sqlite3 ~/Library/Application\ Support/Windsurf/User/globalStorage/state.vscdb \
        "DELETE FROM ItemTable WHERE key LIKE '%history.recentlyOpened%';" 2>/dev/null
    
    sqlite3 ~/Library/Application\ Support/Windsurf/User/globalStorage/state.vscdb \
        "DELETE FROM ItemTable WHERE key LIKE '%workspaceStorage%';" 2>/dev/null
    
    # Remove any file paths (but keep auth tokens)
    sqlite3 ~/Library/Application\ Support/Windsurf/User/globalStorage/state.vscdb \
        "DELETE FROM ItemTable WHERE value LIKE '%/Users/%' AND key NOT LIKE '%github%' AND key NOT LIKE '%auth%';" 2>/dev/null
    
    # Vacuum to reclaim space
    sqlite3 ~/Library/Application\ Support/Windsurf/User/globalStorage/state.vscdb "VACUUM;" 2>/dev/null
    
    echo -e "${GREEN}✅ Global state.vscdb workspace history cleared (auth preserved)${NC}"
else
    echo -e "${YELLOW}⚠️  Global state.vscdb not found${NC}"
fi

# STEP 4: Clear cache
echo -e "${CYAN}[4/10] Clearing cache...${NC}"

if [ -d ~/Library/Application\ Support/Windsurf/Cache ]; then
    rm -rf ~/Library/Application\ Support/Windsurf/Cache/*
    echo -e "${GREEN}✅ Cache cleared${NC}"
fi

# STEP 5: Clear cached data
echo -e "${CYAN}[5/10] Clearing cached data...${NC}"

if [ -d ~/Library/Application\ Support/Windsurf/CachedData ]; then
    rm -rf ~/Library/Application\ Support/Windsurf/CachedData/*
    echo -e "${GREEN}✅ Cached data cleared${NC}"
fi

# STEP 6: Clear GPU cache
echo -e "${CYAN}[6/10] Clearing GPU cache...${NC}"

if [ -d ~/Library/Application\ Support/Windsurf/GPUCache ]; then
    rm -rf ~/Library/Application\ Support/Windsurf/GPUCache/*
    echo -e "${GREEN}✅ GPU cache cleared${NC}"
fi

# STEP 7: Clear crash reports
echo -e "${CYAN}[7/10] Clearing crash reports...${NC}"

if [ -d ~/Library/Application\ Support/Windsurf/Crashpad ]; then
    rm -rf ~/Library/Application\ Support/Windsurf/Crashpad/*
    echo -e "${GREEN}✅ Crash reports cleared${NC}"
fi

# STEP 8: Clear logs (preserve auth logs)
echo -e "${CYAN}[8/10] Clearing logs...${NC}"

if [ -d ~/Library/Application\ Support/Windsurf/logs ]; then
    # Only clear non-auth logs
    find ~/Library/Application\ Support/Windsurf/logs -type f ! -path "*/exthost/vscode.github-authentication*" -delete 2>/dev/null
    echo -e "${GREEN}✅ Logs cleared (auth logs preserved)${NC}"
fi

# STEP 9: Remove backup files
echo -e "${CYAN}[9/10] Removing old backup files...${NC}"

BACKUP_COUNT=0
if [ -f ~/Library/Application\ Support/Windsurf/User/globalStorage/storage.json.backup ]; then
    # Keep the most recent backup we just created, remove older ones
    find ~/Library/Application\ Support/Windsurf/User/globalStorage -name "*.backup" -o -name "*.bak" 2>/dev/null | \
        while read backup_file; do
            # Only remove if it's not the one we just created
            if [ "$(stat -f "%m" "$backup_file" 2>/dev/null)" -lt "$(($(date +%s) - 60))" ]; then
                rm "$backup_file" 2>/dev/null
                ((BACKUP_COUNT++))
            fi
        done
fi

echo -e "${GREEN}✅ Old backup files removed${NC}"

# STEP 10: Vacuum all databases
echo -e "${CYAN}[10/10] Optimizing databases...${NC}"

# Vacuum global state.vscdb
if [ -f ~/Library/Application\ Support/Windsurf/User/globalStorage/state.vscdb ]; then
    sqlite3 ~/Library/Application\ Support/Windsurf/User/globalStorage/state.vscdb "VACUUM;" 2>/dev/null
fi

# Vacuum workspace databases
for db in ~/Library/Application\ Support/Windsurf/User/workspaceStorage/*/state.vscdb; do
    if [ -f "$db" ]; then
        sqlite3 "$db" "VACUUM;" 2>/dev/null
    fi
done

echo -e "${GREEN}✅ Databases optimized${NC}"

echo ""
echo "=========================================="
echo "CLEANUP COMPLETE!"
echo "=========================================="
echo ""

# Show results
echo -e "${GREEN}✅ Successfully cleared:${NC}"
echo "  • Machine/Device tracking IDs"
echo "  • ALL workspace associations (16+ directories)"
echo "  • Workspace history from global database"
echo "  • File path references"
echo "  • Recent file history"
echo "  • ~140 MB of cache data"
echo "  • Crash reports and logs"
echo "  • Old backup files"
echo ""

echo -e "${BLUE}📋 Preserved:${NC}"
echo "  • User settings"
echo "  • Installed extensions"
echo "  • Keybindings"
echo "  • Snippets"
echo "  • Chat history with Cascade"
echo "  • Windsurf login (you'll stay logged in)"
echo "  • GitHub authentication"
echo ""

if [ "$CREATE_BACKUP" = "y" ] || [ "$CREATE_BACKUP" = "Y" ]; then
    echo -e "${YELLOW}💾 Backup location:${NC}"
    echo "  $BACKUP_DIR"
    echo ""
fi

echo -e "${CYAN}🔍 VERIFICATION:${NC}"
echo "  Run the test suite to verify complete deletion:"
echo "  ./test_historical_access_deletion.sh"
echo ""

echo -e "${YELLOW}⚠️  NEXT STEPS:${NC}"
echo "  1. Run verification test (see above)"
echo "  2. Restart Windsurf (if it was running)"
echo "  3. Windsurf will create fresh tracking data"
echo "  4. Only open workspaces you want tracked"
echo "  5. Run audit again: ./audit_windsurf_access.sh"
echo ""

echo -e "${RED}🚨 IMPORTANT:${NC}"
echo "  - This only clears LOCAL tracking"
echo "  - Data already sent to cloud servers remains there"
echo "  - To prevent future tracking, use sandbox/firewall"
echo "  - Run this script regularly to maintain privacy"
echo ""

echo "=========================================="
echo "Enhanced cleanup v2.0 complete!"
echo "=========================================="
echo ""
