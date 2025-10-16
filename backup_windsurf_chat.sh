#!/bin/bash
# Backup Windsurf Chat Histories
# Exports all chat data from workspace databases to a readable format

BACKUP_DIR="$HOME/WindsurfChatBackup_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR"

echo "=========================================="
echo "WINDSURF CHAT HISTORY BACKUP"
echo "=========================================="
echo "Date: $(date)"
echo "Backup Location: $BACKUP_DIR"
echo ""

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

TOTAL_CHATS=0
TOTAL_WORKSPACES=0

# Backup workspace chat data
if [ -d ~/Library/Application\ Support/Windsurf/User/workspaceStorage ]; then
    echo -e "${CYAN}Backing up workspace chat histories...${NC}"
    echo ""
    
    for workspace in ~/Library/Application\ Support/Windsurf/User/workspaceStorage/*/; do
        if [ -f "$workspace/state.vscdb" ]; then
            WORKSPACE_ID=$(basename "$workspace")
            
            # Check if this workspace has chat data
            CHAT_COUNT=$(sqlite3 "$workspace/state.vscdb" \
                "SELECT COUNT(*) FROM ItemTable WHERE key LIKE '%chat%' OR key LIKE '%cascade%';" 2>/dev/null)
            
            if [ "$CHAT_COUNT" -gt 0 ]; then
                ((TOTAL_WORKSPACES++))
                TOTAL_CHATS=$((TOTAL_CHATS + CHAT_COUNT))
                
                echo -e "${BLUE}Workspace: ${WORKSPACE_ID}${NC}"
                echo "  Chat entries: $CHAT_COUNT"
                
                # Create workspace backup directory
                WORKSPACE_BACKUP="$BACKUP_DIR/$WORKSPACE_ID"
                mkdir -p "$WORKSPACE_BACKUP"
                
                # Export chat data to JSON
                echo -e "${CYAN}  Exporting chat data...${NC}"
                sqlite3 "$workspace/state.vscdb" <<EOF > "$WORKSPACE_BACKUP/chat_data.json"
.mode json
SELECT key, value FROM ItemTable 
WHERE key LIKE '%chat%' OR key LIKE '%cascade%'
ORDER BY key;
EOF
                
                # Export chat data to CSV (more readable)
                sqlite3 "$workspace/state.vscdb" <<EOF > "$WORKSPACE_BACKUP/chat_data.csv"
.mode csv
.headers on
SELECT key, value FROM ItemTable 
WHERE key LIKE '%chat%' OR key LIKE '%cascade%'
ORDER BY key;
EOF
                
                # Export full database as backup
                cp "$workspace/state.vscdb" "$WORKSPACE_BACKUP/state.vscdb.backup"
                
                # Create a readable summary
                cat > "$WORKSPACE_BACKUP/README.txt" << SUMMARY
Workspace Chat Backup
=====================
Workspace ID: $WORKSPACE_ID
Backup Date: $(date)
Chat Entries: $CHAT_COUNT

Files in this backup:
- chat_data.json: Chat data in JSON format
- chat_data.csv: Chat data in CSV format (open in Excel/Numbers)
- state.vscdb.backup: Full database backup

To restore:
Copy state.vscdb.backup back to:
~/Library/Application Support/Windsurf/User/workspaceStorage/$WORKSPACE_ID/state.vscdb
SUMMARY
                
                echo -e "${GREEN}  ✅ Backed up to: $WORKSPACE_BACKUP${NC}"
                echo ""
            fi
        fi
    done
    
    if [ "$TOTAL_WORKSPACES" -gt 0 ]; then
        echo ""
        echo -e "${GREEN}=========================================="
        echo "BACKUP COMPLETE"
        echo "==========================================${NC}"
        echo ""
        echo "Summary:"
        echo "  Workspaces backed up: $TOTAL_WORKSPACES"
        echo "  Total chat entries: $TOTAL_CHATS"
        echo "  Backup location: $BACKUP_DIR"
        echo ""
        echo "Files created per workspace:"
        echo "  • chat_data.json - JSON format"
        echo "  • chat_data.csv - CSV format (readable in Excel)"
        echo "  • state.vscdb.backup - Full database"
        echo "  • README.txt - Backup information"
        echo ""
        echo -e "${CYAN}To view your chats:${NC}"
        echo "  1. Open chat_data.csv in Excel/Numbers/Google Sheets"
        echo "  2. Or open chat_data.json in a text editor"
        echo ""
        echo -e "${CYAN}To restore:${NC}"
        echo "  1. Close Windsurf"
        echo "  2. Copy state.vscdb.backup to the original location"
        echo "  3. Rename to state.vscdb"
        echo ""
        
        # Create master index
        cat > "$BACKUP_DIR/MASTER_INDEX.txt" << INDEX
Windsurf Chat History Backup
=============================
Backup Date: $(date)
Total Workspaces: $TOTAL_WORKSPACES
Total Chat Entries: $TOTAL_CHATS

Workspace Directories:
$(ls -1 "$BACKUP_DIR" | grep -v "MASTER_INDEX.txt" | grep -v "backup_script.sh")

Each workspace directory contains:
- chat_data.json: JSON format
- chat_data.csv: CSV format (open in Excel)
- state.vscdb.backup: Full database backup
- README.txt: Workspace-specific info

To browse your chats:
Open any chat_data.csv file in Excel, Numbers, or Google Sheets.
The 'value' column contains the actual chat content.
INDEX
        
        echo -e "${GREEN}Master index created: $BACKUP_DIR/MASTER_INDEX.txt${NC}"
        echo ""
        echo -e "${CYAN}Opening backup location...${NC}"
        open "$BACKUP_DIR"
        
    else
        echo -e "${CYAN}No chat history found to backup.${NC}"
        rmdir "$BACKUP_DIR" 2>/dev/null
    fi
else
    echo "Windsurf workspace storage not found."
fi

echo ""
echo "Backup script complete: $(date)"
echo ""
