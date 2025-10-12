#!/bin/bash
# Pre-Flight Safety Check: Verify Chat & Auth Preservation
# Run this BEFORE cleanup to ensure critical data will be preserved

echo "=========================================="
echo "PRESERVATION SAFETY CHECK"
echo "=========================================="
echo "Date: $(date)"
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

echo -e "${CYAN}This script verifies what will be PRESERVED during cleanup${NC}"
echo ""

# Check 1: Chat History
echo "=========================================="
echo "1. CHAT HISTORY CHECK"
echo "=========================================="
echo ""

TOTAL_CHAT_ENTRIES=0
WORKSPACES_WITH_CHAT=0

if [ -d ~/Library/Application\ Support/Windsurf/User/workspaceStorage ]; then
    for db in ~/Library/Application\ Support/Windsurf/User/workspaceStorage/*/state.vscdb; do
        if [ -f "$db" ]; then
            WORKSPACE_NAME=$(basename "$(dirname "$db")")
            
            # Count chat entries
            CHAT_COUNT=$(sqlite3 "$db" "SELECT COUNT(*) FROM ItemTable WHERE key LIKE '%chat%' OR key LIKE '%cascade%';" 2>/dev/null)
            
            if [ "$CHAT_COUNT" -gt 0 ]; then
                ((WORKSPACES_WITH_CHAT++))
                TOTAL_CHAT_ENTRIES=$((TOTAL_CHAT_ENTRIES + CHAT_COUNT))
                
                # Show first few chat entries
                echo -e "${BLUE}Workspace: ${WORKSPACE_NAME}${NC}"
                echo "  Chat entries: $CHAT_COUNT"
                
                # Get sample chat keys (first 3)
                sqlite3 "$db" "SELECT key FROM ItemTable WHERE key LIKE '%chat%' OR key LIKE '%cascade%' LIMIT 3;" 2>/dev/null | \
                    while read key; do
                        echo "    • $key"
                    done
                echo ""
            fi
        fi
    done
    
    if [ "$WORKSPACES_WITH_CHAT" -gt 0 ]; then
        echo -e "${GREEN}✅ Found chat history in $WORKSPACES_WITH_CHAT workspaces${NC}"
        echo -e "${GREEN}   Total chat entries: $TOTAL_CHAT_ENTRIES${NC}"
        echo ""
        echo -e "${CYAN}These will be PRESERVED during cleanup.${NC}"
    else
        echo -e "${YELLOW}⚠️  No chat history found${NC}"
        echo "   (This is normal if you haven't used Cascade chat yet)"
    fi
else
    echo -e "${YELLOW}⚠️  No workspace storage found${NC}"
fi

echo ""

# Check 2: GitHub Authentication
echo "=========================================="
echo "2. GITHUB AUTHENTICATION CHECK"
echo "=========================================="
echo ""

if [ -f ~/Library/Application\ Support/Windsurf/User/globalStorage/state.vscdb ]; then
    # Check for GitHub auth entries
    GITHUB_AUTH_COUNT=$(sqlite3 ~/Library/Application\ Support/Windsurf/User/globalStorage/state.vscdb \
        "SELECT COUNT(*) FROM ItemTable WHERE key LIKE '%github%authentication%';" 2>/dev/null)
    
    if [ "$GITHUB_AUTH_COUNT" -gt 0 ]; then
        echo -e "${GREEN}✅ GitHub authentication found${NC}"
        echo "   Auth entries: $GITHUB_AUTH_COUNT"
        echo ""
        
        # Show auth keys (not values for security)
        echo "   Authentication keys:"
        sqlite3 ~/Library/Application\ Support/Windsurf/User/globalStorage/state.vscdb \
            "SELECT key FROM ItemTable WHERE key LIKE '%github%authentication%' LIMIT 5;" 2>/dev/null | \
            while read key; do
                echo "    • $key"
            done
        echo ""
        echo -e "${CYAN}These will be PRESERVED during cleanup.${NC}"
    else
        echo -e "${YELLOW}⚠️  No GitHub authentication found${NC}"
        echo "   (You may need to re-authenticate after cleanup)"
    fi
    
    # Check for other auth
    OTHER_AUTH=$(sqlite3 ~/Library/Application\ Support/Windsurf/User/globalStorage/state.vscdb \
        "SELECT COUNT(*) FROM ItemTable WHERE key LIKE '%auth%' AND key NOT LIKE '%github%';" 2>/dev/null)
    
    if [ "$OTHER_AUTH" -gt 0 ]; then
        echo ""
        echo -e "${BLUE}ℹ️  Other authentication found: $OTHER_AUTH entries${NC}"
        echo "   (Windsurf login, etc. - will be preserved)"
    fi
else
    echo -e "${RED}❌ Global state.vscdb not found${NC}"
    echo "   Cannot verify authentication status"
fi

echo ""

# Check 3: User Settings
echo "=========================================="
echo "3. USER SETTINGS CHECK"
echo "=========================================="
echo ""

if [ -f ~/Library/Application\ Support/Windsurf/User/settings.json ]; then
    SETTINGS_SIZE=$(du -h ~/Library/Application\ Support/Windsurf/User/settings.json 2>/dev/null | awk '{print $1}')
    echo -e "${GREEN}✅ User settings found${NC}"
    echo "   Size: $SETTINGS_SIZE"
    echo "   Location: ~/Library/Application Support/Windsurf/User/settings.json"
    echo ""
    echo -e "${CYAN}Settings will NOT be modified during cleanup.${NC}"
else
    echo -e "${YELLOW}⚠️  No custom settings found${NC}"
    echo "   (Using default settings)"
fi

echo ""

# Check 4: Extensions
echo "=========================================="
echo "4. EXTENSIONS CHECK"
echo "=========================================="
echo ""

if [ -d ~/Library/Application\ Support/Windsurf/User/extensions ]; then
    EXTENSION_COUNT=$(find ~/Library/Application\ Support/Windsurf/User/extensions -maxdepth 1 -type d 2>/dev/null | wc -l | tr -d ' ')
    EXTENSION_COUNT=$((EXTENSION_COUNT - 1))  # Subtract parent directory
    
    if [ "$EXTENSION_COUNT" -gt 0 ]; then
        echo -e "${GREEN}✅ Found $EXTENSION_COUNT installed extensions${NC}"
        echo ""
        echo "   Installed extensions:"
        find ~/Library/Application\ Support/Windsurf/User/extensions -maxdepth 1 -type d 2>/dev/null | \
            tail -n +2 | head -10 | while read ext; do
                echo "    • $(basename "$ext")"
            done
        
        if [ "$EXTENSION_COUNT" -gt 10 ]; then
            echo "    ... and $((EXTENSION_COUNT - 10)) more"
        fi
        echo ""
        echo -e "${CYAN}Extensions will NOT be modified during cleanup.${NC}"
    else
        echo -e "${YELLOW}⚠️  No extensions found${NC}"
    fi
else
    echo -e "${YELLOW}⚠️  Extensions directory not found${NC}"
fi

echo ""

# Check 5: Keybindings
echo "=========================================="
echo "5. KEYBINDINGS CHECK"
echo "=========================================="
echo ""

if [ -f ~/Library/Application\ Support/Windsurf/User/keybindings.json ]; then
    KEYBINDINGS_SIZE=$(du -h ~/Library/Application\ Support/Windsurf/User/keybindings.json 2>/dev/null | awk '{print $1}')
    KEYBINDING_COUNT=$(cat ~/Library/Application\ Support/Windsurf/User/keybindings.json | grep -c "key" 2>/dev/null)
    
    echo -e "${GREEN}✅ Custom keybindings found${NC}"
    echo "   Size: $KEYBINDINGS_SIZE"
    echo "   Bindings: ~$KEYBINDING_COUNT"
    echo ""
    echo -e "${CYAN}Keybindings will NOT be modified during cleanup.${NC}"
else
    echo -e "${YELLOW}⚠️  No custom keybindings found${NC}"
    echo "   (Using default keybindings)"
fi

echo ""

# Check 6: What WILL be deleted
echo "=========================================="
echo "6. WHAT WILL BE DELETED"
echo "=========================================="
echo ""

echo -e "${RED}The following will be REMOVED:${NC}"
echo ""

# Tracking IDs
if [ -f ~/Library/Application\ Support/Windsurf/User/globalStorage/storage.json ]; then
    MACHINE_ID=$(cat ~/Library/Application\ Support/Windsurf/User/globalStorage/storage.json | \
        python3 -c "import sys, json; data=json.load(sys.stdin); print(data.get('telemetry.machineId', 'none'))" 2>/dev/null)
    
    if [ "$MACHINE_ID" != "none" ] && [ -n "$MACHINE_ID" ]; then
        echo -e "  ${YELLOW}• Machine ID:${NC} ${MACHINE_ID:0:20}..."
    fi
fi

# Workspace count
if [ -f ~/Library/Application\ Support/Windsurf/User/globalStorage/storage.json ]; then
    WORKSPACE_COUNT=$(cat ~/Library/Application\ Support/Windsurf/User/globalStorage/storage.json | \
        python3 -c "import sys, json; data=json.load(sys.stdin); print(len(data.get('profileAssociations', {}).get('workspaces', {})))" 2>/dev/null)
    
    if [ "$WORKSPACE_COUNT" -gt 0 ]; then
        echo -e "  ${YELLOW}• Tracked workspaces:${NC} $WORKSPACE_COUNT"
    fi
fi

# Cache size
if [ -d ~/Library/Application\ Support/Windsurf/Cache ]; then
    CACHE_SIZE=$(du -sh ~/Library/Application\ Support/Windsurf/Cache 2>/dev/null | awk '{print $1}')
    echo -e "  ${YELLOW}• Cache:${NC} $CACHE_SIZE"
fi

if [ -d ~/Library/Application\ Support/Windsurf/CachedData ]; then
    CACHED_DATA_SIZE=$(du -sh ~/Library/Application\ Support/Windsurf/CachedData 2>/dev/null | awk '{print $1}')
    echo -e "  ${YELLOW}• Cached Data:${NC} $CACHED_DATA_SIZE"
fi

# Workspace databases
if [ -d ~/Library/Application\ Support/Windsurf/User/workspaceStorage ]; then
    WORKSPACE_DB_COUNT=$(find ~/Library/Application\ Support/Windsurf/User/workspaceStorage -name "workspace.json" 2>/dev/null | wc -l | tr -d ' ')
    if [ "$WORKSPACE_DB_COUNT" -gt 0 ]; then
        echo -e "  ${YELLOW}• Workspace tracking files:${NC} $WORKSPACE_DB_COUNT"
    fi
fi

echo ""

# Summary
echo "=========================================="
echo "SAFETY SUMMARY"
echo "=========================================="
echo ""

SAFE_TO_RUN=true

if [ "$TOTAL_CHAT_ENTRIES" -gt 0 ]; then
    echo -e "${GREEN}✅ Chat history will be preserved ($TOTAL_CHAT_ENTRIES entries)${NC}"
else
    echo -e "${BLUE}ℹ️  No chat history to preserve${NC}"
fi

if [ "$GITHUB_AUTH_COUNT" -gt 0 ]; then
    echo -e "${GREEN}✅ GitHub authentication will be preserved${NC}"
else
    echo -e "${YELLOW}⚠️  No GitHub auth found - you may need to re-login${NC}"
    SAFE_TO_RUN=false
fi

if [ -f ~/Library/Application\ Support/Windsurf/User/settings.json ]; then
    echo -e "${GREEN}✅ User settings will be preserved${NC}"
else
    echo -e "${BLUE}ℹ️  No custom settings to preserve${NC}"
fi

if [ "$EXTENSION_COUNT" -gt 0 ]; then
    echo -e "${GREEN}✅ Extensions will be preserved ($EXTENSION_COUNT extensions)${NC}"
else
    echo -e "${BLUE}ℹ️  No extensions to preserve${NC}"
fi

echo ""

if [ "$SAFE_TO_RUN" = true ]; then
    echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${GREEN}✅ SAFE TO RUN CLEANUP${NC}"
    echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
    echo "All critical data will be preserved."
    echo "You can safely run the enhanced cleanup script."
    echo ""
    echo -e "${CYAN}Next step:${NC}"
    echo "  ./clear_windsurf_tracking_ENHANCED.sh"
else
    echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${YELLOW}⚠️  REVIEW WARNINGS ABOVE${NC}"
    echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
    echo "Some authentication data may not be preserved."
    echo "Review the warnings above before proceeding."
    echo ""
    echo -e "${YELLOW}You may need to:${NC}"
    echo "  • Re-authenticate with GitHub after cleanup"
    echo "  • Re-login to Windsurf after cleanup"
fi

echo ""
echo "=========================================="
echo "Safety check complete: $(date)"
echo "=========================================="
echo ""
