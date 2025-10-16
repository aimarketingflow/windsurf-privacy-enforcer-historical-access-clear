#!/bin/bash
# Verify Windsurf Tracking Cleanup & Exfiltration Status

echo "=================================="
echo "WINDSURF CLEANUP VERIFICATION"
echo "=================================="
echo "Date: $(date)"
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# 1. CHECK TRACKING IDS
echo "=================================="
echo "1. TRACKING IDS STATUS"
echo "=================================="

if [ -f ~/Library/Application\ Support/Windsurf/User/globalStorage/storage.json ]; then
    echo -e "${YELLOW}Checking Machine/Device IDs...${NC}"
    
    MACHINE_ID=$(cat ~/Library/Application\ Support/Windsurf/User/globalStorage/storage.json | \
        python3 -c "import sys, json; data=json.load(sys.stdin); print(data.get('telemetry.machineId', 'NOT FOUND'))" 2>/dev/null)
    
    DEVICE_ID=$(cat ~/Library/Application\ Support/Windsurf/User/globalStorage/storage.json | \
        python3 -c "import sys, json; data=json.load(sys.stdin); print(data.get('telemetry.devDeviceId', 'NOT FOUND'))" 2>/dev/null)
    
    if [ "$MACHINE_ID" = "" ] || [ "$MACHINE_ID" = "NOT FOUND" ]; then
        echo -e "${GREEN}✅ Machine ID: CLEARED${NC}"
    else
        echo -e "${RED}❌ Machine ID still present: ${MACHINE_ID}${NC}"
    fi
    
    if [ "$DEVICE_ID" = "" ] || [ "$DEVICE_ID" = "NOT FOUND" ]; then
        echo -e "${GREEN}✅ Device ID: CLEARED${NC}"
    else
        echo -e "${RED}❌ Device ID still present: ${DEVICE_ID}${NC}"
    fi
else
    echo -e "${RED}❌ storage.json not found${NC}"
fi
echo ""

# 2. CHECK WORKSPACE TRACKING
echo "=================================="
echo "2. WORKSPACE TRACKING STATUS"
echo "=================================="

if [ -f ~/Library/Application\ Support/Windsurf/User/globalStorage/storage.json ]; then
    WORKSPACE_COUNT=$(cat ~/Library/Application\ Support/Windsurf/User/globalStorage/storage.json | \
        python3 -c "import sys, json; data=json.load(sys.stdin); print(len(data.get('profileAssociations', {}).get('workspaces', {})))" 2>/dev/null)
    
    BACKUP_COUNT=$(cat ~/Library/Application\ Support/Windsurf/User/globalStorage/storage.json | \
        python3 -c "import sys, json; data=json.load(sys.stdin); print(len(data.get('backupWorkspaces', {}).get('folders', [])))" 2>/dev/null)
    
    if [ "$WORKSPACE_COUNT" = "0" ]; then
        echo -e "${GREEN}✅ Tracked workspaces: 0 (CLEARED)${NC}"
    else
        echo -e "${RED}❌ Tracked workspaces: ${WORKSPACE_COUNT}${NC}"
        echo "   Run cleanup script again!"
    fi
    
    if [ "$BACKUP_COUNT" = "0" ]; then
        echo -e "${GREEN}✅ Backup workspaces: 0 (CLEARED)${NC}"
    else
        echo -e "${RED}❌ Backup workspaces: ${BACKUP_COUNT}${NC}"
    fi
else
    echo -e "${RED}❌ Cannot verify workspace tracking${NC}"
fi
echo ""

# 3. CHECK ACTIVE NETWORK CONNECTIONS
echo "=================================="
echo "3. ACTIVE NETWORK CONNECTIONS"
echo "=================================="

if pgrep -x "Windsurf" > /dev/null; then
    echo -e "${YELLOW}Windsurf is running. Checking connections...${NC}"
    
    # Check for external connections (not localhost)
    EXTERNAL_CONNS=$(lsof -i -n -P 2>/dev/null | grep -i windsurf | grep -v "127.0.0.1" | grep -v "::1" | grep ESTABLISHED)
    
    if [ -z "$EXTERNAL_CONNS" ]; then
        echo -e "${GREEN}✅ No external connections (GOOD)${NC}"
    else
        echo -e "${RED}❌ Active external connections detected:${NC}"
        echo "$EXTERNAL_CONNS" | while read line; do
            echo "   $line"
        done
        echo ""
        echo -e "${YELLOW}⚠️  Windsurf is still sending data to external servers!${NC}"
    fi
    
    # Count localhost connections
    LOCAL_CONNS=$(lsof -i -n -P 2>/dev/null | grep -i windsurf | grep -E "127.0.0.1|::1" | wc -l | tr -d ' ')
    echo -e "${BLUE}ℹ️  Localhost connections: ${LOCAL_CONNS} (internal IPC - normal)${NC}"
else
    echo -e "${GREEN}✅ Windsurf is not running${NC}"
fi
echo ""

# 4. CHECK CACHE SIZE
echo "=================================="
echo "4. CACHE STATUS"
echo "=================================="

if [ -d ~/Library/Application\ Support/Windsurf/Cache ]; then
    CACHE_SIZE=$(du -sh ~/Library/Application\ Support/Windsurf/Cache 2>/dev/null | awk '{print $1}')
    CACHE_FILES=$(find ~/Library/Application\ Support/Windsurf/Cache -type f 2>/dev/null | wc -l | tr -d ' ')
    
    if [ "$CACHE_FILES" = "0" ]; then
        echo -e "${GREEN}✅ Cache: Empty (0 files)${NC}"
    else
        echo -e "${YELLOW}⚠️  Cache: ${CACHE_SIZE} (${CACHE_FILES} files)${NC}"
        echo "   Cache rebuilds during use - this is normal"
    fi
else
    echo -e "${GREEN}✅ Cache directory not found or empty${NC}"
fi
echo ""

# 5. CHECK WORKSPACE DATABASES
echo "=================================="
echo "5. WORKSPACE DATABASES"
echo "=================================="

if [ -d ~/Library/Application\ Support/Windsurf/User/workspaceStorage ]; then
    DB_COUNT=$(find ~/Library/Application\ Support/Windsurf/User/workspaceStorage -name "workspace.json" 2>/dev/null | wc -l | tr -d ' ')
    
    if [ "$DB_COUNT" = "0" ]; then
        echo -e "${GREEN}✅ Workspace tracking files: 0 (CLEARED)${NC}"
    else
        echo -e "${YELLOW}⚠️  Workspace tracking files: ${DB_COUNT}${NC}"
        echo "   (May rebuild if you open workspaces)"
    fi
    
    # Check if chat history is preserved
    CHAT_DBS=$(find ~/Library/Application\ Support/Windsurf/User/workspaceStorage -name "state.vscdb" 2>/dev/null | wc -l | tr -d ' ')
    echo -e "${BLUE}ℹ️  Chat history databases: ${CHAT_DBS} (preserved)${NC}"
else
    echo -e "${GREEN}✅ No workspace storage${NC}"
fi
echo ""

# 6. MONITOR LIVE TRAFFIC (5 seconds)
echo "=================================="
echo "6. LIVE TRAFFIC MONITORING (5 sec)"
echo "=================================="

if pgrep -x "Windsurf" > /dev/null; then
    echo -e "${YELLOW}Monitoring Windsurf network activity...${NC}"
    
    # Capture traffic for 5 seconds
    TEMP_PCAP="/tmp/windsurf_verify_$$.pcap"
    
    timeout 5 tcpdump -i any -n "host not 127.0.0.1 and host not ::1" -w "$TEMP_PCAP" 2>/dev/null &
    TCPDUMP_PID=$!
    
    sleep 5
    wait $TCPDUMP_PID 2>/dev/null
    
    if [ -f "$TEMP_PCAP" ]; then
        PACKET_COUNT=$(tcpdump -r "$TEMP_PCAP" 2>/dev/null | wc -l | tr -d ' ')
        
        if [ "$PACKET_COUNT" = "0" ]; then
            echo -e "${GREEN}✅ No external traffic in 5 seconds (GOOD)${NC}"
        else
            echo -e "${RED}❌ Detected ${PACKET_COUNT} external packets${NC}"
            echo ""
            echo "Top destinations:"
            tcpdump -r "$TEMP_PCAP" -n 2>/dev/null | awk '{print $3}' | sort | uniq -c | sort -rn | head -5
        fi
        
        rm -f "$TEMP_PCAP"
    else
        echo -e "${YELLOW}⚠️  Could not capture traffic (may need sudo)${NC}"
    fi
else
    echo -e "${BLUE}ℹ️  Windsurf not running - no traffic to monitor${NC}"
fi
echo ""

# 7. CHECK FOR RECENT EXFILTRATION
echo "=================================="
echo "7. RECENT EXFILTRATION CHECK"
echo "=================================="

echo -e "${YELLOW}Checking for recent large data transfers...${NC}"

if command -v nettop &> /dev/null; then
    # Check network stats (requires sudo for detailed info)
    echo "   (Detailed stats require sudo - skipping)"
fi

# Check if language server is running
LANG_SERVER=$(ps aux | grep language_server_macos_arm | grep -v grep | wc -l | tr -d ' ')

if [ "$LANG_SERVER" -gt 0 ]; then
    echo -e "${YELLOW}⚠️  Language server is running (${LANG_SERVER} processes)${NC}"
    echo "   This is the process that sends data to Windsurf servers"
    
    # Check its connections
    LANG_CONNS=$(lsof -i -n -P 2>/dev/null | grep language_server | grep -v "127.0.0.1" | grep ESTABLISHED | wc -l | tr -d ' ')
    
    if [ "$LANG_CONNS" -gt 0 ]; then
        echo -e "${RED}❌ Language server has ${LANG_CONNS} external connections${NC}"
        lsof -i -n -P 2>/dev/null | grep language_server | grep -v "127.0.0.1" | grep ESTABLISHED
    else
        echo -e "${GREEN}✅ Language server has no external connections${NC}"
    fi
else
    echo -e "${GREEN}✅ Language server not running${NC}"
fi
echo ""

# 8. SUMMARY & RECOMMENDATIONS
echo "=================================="
echo "8. SUMMARY & RECOMMENDATIONS"
echo "=================================="
echo ""

# Calculate overall status
ISSUES=0

# Check critical items
if [ "$MACHINE_ID" != "" ] && [ "$MACHINE_ID" != "NOT FOUND" ]; then
    ((ISSUES++))
fi

if [ "$WORKSPACE_COUNT" != "0" ]; then
    ((ISSUES++))
fi

if [ -n "$EXTERNAL_CONNS" ]; then
    ((ISSUES++))
fi

if [ "$LANG_CONNS" -gt 0 ]; then
    ((ISSUES++))
fi

# Overall status
if [ $ISSUES -eq 0 ]; then
    echo -e "${GREEN}✅ CLEANUP SUCCESSFUL!${NC}"
    echo ""
    echo "All tracking has been cleared:"
    echo "  ✓ Machine/Device IDs removed"
    echo "  ✓ Workspace tracking cleared"
    echo "  ✓ No active exfiltration detected"
    echo ""
    echo -e "${BLUE}📋 Next Steps:${NC}"
    echo "  1. Continue monitoring with this script"
    echo "  2. Run cleanup monthly to maintain privacy"
    echo "  3. Consider firewall rules for complete blocking"
else
    echo -e "${RED}⚠️  ISSUES DETECTED (${ISSUES} problems)${NC}"
    echo ""
    echo -e "${YELLOW}Recommended Actions:${NC}"
    
    if [ "$MACHINE_ID" != "" ] && [ "$MACHINE_ID" != "NOT FOUND" ]; then
        echo "  1. Re-run cleanup script (tracking IDs still present)"
    fi
    
    if [ "$WORKSPACE_COUNT" != "0" ]; then
        echo "  2. Clear workspace tracking again"
    fi
    
    if [ -n "$EXTERNAL_CONNS" ] || [ "$LANG_CONNS" -gt 0 ]; then
        echo "  3. Quit Windsurf and restart to stop active connections"
        echo "  4. Consider using firewall to block external connections"
    fi
fi

echo ""
echo "=================================="
echo "VERIFICATION COMPLETE"
echo "=================================="
echo ""
echo "To monitor continuously, run:"
echo "  watch -n 60 ./verify_cleanup.sh"
echo ""
