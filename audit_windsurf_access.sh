#!/bin/bash
# Windsurf System Access Audit Script
# Checks all permissions and access points for Windsurf IDE

echo "=================================="
echo "WINDSURF SYSTEM ACCESS AUDIT"
echo "=================================="
echo "Date: $(date)"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if Windsurf is installed
if [ ! -d "/Applications/Windsurf.app" ]; then
    echo -e "${RED}❌ Windsurf.app not found in /Applications/${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Windsurf.app found${NC}"
echo ""

# 1. CHECK ENTITLEMENTS
echo "=================================="
echo "1. CODE SIGNING & ENTITLEMENTS"
echo "=================================="
codesign -d --entitlements - /Applications/Windsurf.app 2>&1 | grep -A1 "Key\|Value" | head -20
echo ""

# 2. CHECK INFO.PLIST PERMISSIONS
echo "=================================="
echo "2. REQUESTED PERMISSIONS (Info.plist)"
echo "=================================="
echo -e "${YELLOW}Camera:${NC}"
plutil -p /Applications/Windsurf.app/Contents/Info.plist | grep -A1 "NSCameraUsageDescription"

echo -e "${YELLOW}Microphone:${NC}"
plutil -p /Applications/Windsurf.app/Contents/Info.plist | grep -A1 "NSMicrophoneUsageDescription"

echo -e "${YELLOW}Bluetooth:${NC}"
plutil -p /Applications/Windsurf.app/Contents/Info.plist | grep -A1 "NSBluetoothAlwaysUsageDescription"

echo -e "${YELLOW}AppleScript:${NC}"
plutil -p /Applications/Windsurf.app/Contents/Info.plist | grep -A1 "NSAppleEventsUsageDescription"

echo -e "${YELLOW}Network Security:${NC}"
plutil -p /Applications/Windsurf.app/Contents/Info.plist | grep -A2 "NSAppTransportSecurity"
echo ""

# 3. CHECK TCC DATABASE (requires sudo)
echo "=================================="
echo "3. GRANTED PERMISSIONS (TCC Database)"
echo "=================================="
echo -e "${YELLOW}Note: This requires sudo access${NC}"
echo "Checking system TCC database..."

if sudo -n true 2>/dev/null; then
    sudo sqlite3 /Library/Application\ Support/com.apple.TCC/TCC.db \
        "SELECT service, client, auth_value, auth_reason FROM access WHERE client LIKE '%windsurf%' OR client LIKE '%Windsurf%';" 2>/dev/null
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ TCC database checked${NC}"
    else
        echo -e "${RED}❌ Could not read TCC database${NC}"
    fi
else
    echo -e "${YELLOW}⚠️  Skipping TCC check (requires sudo)${NC}"
    echo "Run with: sudo ./audit_windsurf_access.sh"
fi
echo ""

# 4. CHECK WORKSPACE TRACKING
echo "=================================="
echo "4. WORKSPACE TRACKING"
echo "=================================="
if [ -f ~/Library/Application\ Support/Windsurf/User/globalStorage/storage.json ]; then
    echo -e "${YELLOW}Machine Tracking IDs:${NC}"
    cat ~/Library/Application\ Support/Windsurf/User/globalStorage/storage.json | \
        python3 -c "import sys, json; data=json.load(sys.stdin); print('Machine ID:', data.get('telemetry.machineId', 'N/A')); print('Device ID:', data.get('telemetry.devDeviceId', 'N/A'))"
    
    echo ""
    echo -e "${YELLOW}Tracked Workspaces:${NC}"
    cat ~/Library/Application\ Support/Windsurf/User/globalStorage/storage.json | \
        python3 -c "import sys, json; data=json.load(sys.stdin); workspaces=data.get('profileAssociations', {}).get('workspaces', {}); [print(f'  - {k}') for k in workspaces.keys()]"
    
    echo ""
    echo -e "${YELLOW}Backup Workspaces:${NC}"
    cat ~/Library/Application\ Support/Windsurf/User/globalStorage/storage.json | \
        python3 -c "import sys, json; data=json.load(sys.stdin); folders=data.get('backupWorkspaces', {}).get('folders', []); [print(f'  - {f.get(\"folderUri\", \"\")}') for f in folders]"
else
    echo -e "${RED}❌ storage.json not found${NC}"
fi
echo ""

# 5. CHECK WORKSPACE STORAGE
echo "=================================="
echo "5. WORKSPACE STORAGE DATABASES"
echo "=================================="
WORKSPACE_COUNT=$(find ~/Library/Application\ Support/Windsurf/User/workspaceStorage -name "workspace.json" 2>/dev/null | wc -l | tr -d ' ')
echo -e "${YELLOW}Total workspace databases: ${WORKSPACE_COUNT}${NC}"

if [ $WORKSPACE_COUNT -gt 0 ]; then
    echo "Recent workspaces:"
    find ~/Library/Application\ Support/Windsurf/User/workspaceStorage -name "workspace.json" 2>/dev/null | \
        head -5 | while read file; do
            echo "  - $(dirname "$file" | xargs basename)"
        done
    
    if [ $WORKSPACE_COUNT -gt 5 ]; then
        echo "  ... and $((WORKSPACE_COUNT - 5)) more"
    fi
fi
echo ""

# 6. CHECK NETWORK CONNECTIONS
echo "=================================="
echo "6. ACTIVE NETWORK CONNECTIONS"
echo "=================================="
echo -e "${YELLOW}Checking for active Windsurf connections...${NC}"
CONNECTIONS=$(lsof -i -n -P 2>/dev/null | grep -i windsurf | wc -l | tr -d ' ')
if [ $CONNECTIONS -gt 0 ]; then
    echo -e "${RED}⚠️  Found ${CONNECTIONS} active network connections:${NC}"
    lsof -i -n -P 2>/dev/null | grep -i windsurf | head -10
else
    echo -e "${GREEN}✅ No active connections (Windsurf not running)${NC}"
fi
echo ""

# 7. CHECK RUNNING PROCESSES
echo "=================================="
echo "7. RUNNING PROCESSES"
echo "=================================="
PROCESSES=$(ps aux | grep -i windsurf | grep -v grep | wc -l | tr -d ' ')
if [ $PROCESSES -gt 0 ]; then
    echo -e "${YELLOW}Found ${PROCESSES} Windsurf processes:${NC}"
    ps aux | grep -i windsurf | grep -v grep | awk '{print "  PID:", $2, "- Command:", $11, $12, $13}'
else
    echo -e "${GREEN}✅ No Windsurf processes running${NC}"
fi
echo ""

# 8. CHECK FILE ACCESS LOGS
echo "=================================="
echo "8. RECENT FILE ACCESS (Last 24h)"
echo "=================================="
echo -e "${YELLOW}Checking system logs for Windsurf file access...${NC}"
if command -v log &> /dev/null; then
    log show --predicate 'process == "Windsurf"' --last 24h --style compact 2>/dev/null | \
        grep -i "file\|access\|permission" | head -5
    
    if [ $? -ne 0 ]; then
        echo -e "${YELLOW}⚠️  No recent file access logs found${NC}"
    fi
else
    echo -e "${YELLOW}⚠️  'log' command not available${NC}"
fi
echo ""

# 9. CHECK CACHE AND DATA SIZE
echo "=================================="
echo "9. STORAGE USAGE"
echo "=================================="
if [ -d ~/Library/Application\ Support/Windsurf ]; then
    SIZE=$(du -sh ~/Library/Application\ Support/Windsurf 2>/dev/null | awk '{print $1}')
    echo -e "${YELLOW}Windsurf data size: ${SIZE}${NC}"
    
    echo "Breakdown:"
    du -sh ~/Library/Application\ Support/Windsurf/* 2>/dev/null | sort -hr | head -5
else
    echo -e "${RED}❌ Windsurf data directory not found${NC}"
fi
echo ""

# 10. SUMMARY
echo "=================================="
echo "10. SECURITY RECOMMENDATIONS"
echo "=================================="
echo -e "${RED}🚨 HIGH PRIORITY:${NC}"
echo "  1. Revoke Full Disk Access (if granted)"
echo "  2. Revoke Camera/Microphone access (if not needed)"
echo "  3. Review tracked workspaces and clear history"
echo ""
echo -e "${YELLOW}⚠️  MEDIUM PRIORITY:${NC}"
echo "  4. Disable telemetry in Windsurf settings"
echo "  5. Use firewall to block Windsurf network access"
echo "  6. Consider sandboxing with custom profile"
echo ""
echo -e "${GREEN}✅ LOW PRIORITY:${NC}"
echo "  7. Regularly audit workspace tracking"
echo "  8. Monitor network traffic with packet capture"
echo ""

echo "=================================="
echo "AUDIT COMPLETE"
echo "=================================="
echo "Report saved to: windsurf_audit_$(date +%Y%m%d_%H%M%S).log"
echo ""
