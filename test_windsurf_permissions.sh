#!/bin/bash
# Test Windsurf Permissions - Active Detection
# Tests what Windsurf actually has access to

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

echo "=========================================="
echo "WINDSURF PERMISSIONS TEST"
echo "=========================================="
echo ""
echo "This script actively tests what permissions"
echo "Windsurf has been granted on your system."
echo ""

# Check if Windsurf is running
if pgrep "Windsurf" > /dev/null; then
    echo -e "${GREEN}✅ Windsurf is running${NC}"
    WINDSURF_PID=$(pgrep "Windsurf" | head -1)
else
    echo -e "${RED}❌ Windsurf is not running${NC}"
    echo "Please start Windsurf and run this script again."
    exit 1
fi

echo ""
echo "=========================================="
echo "1. FULL DISK ACCESS TEST"
echo "=========================================="

# Test reading protected files
PROTECTED_FILES=(
    "$HOME/Library/Safari/History.db"
    "$HOME/Library/Mail"
    "$HOME/Library/Messages"
    "$HOME/Library/Cookies"
)

FDA_GRANTED=false
for file in "${PROTECTED_FILES[@]}"; do
    if [ -e "$file" ]; then
        if [ -r "$file" ]; then
            echo -e "${RED}⚠️  Can read: $file${NC}"
            FDA_GRANTED=true
        else
            echo -e "${GREEN}✅ Cannot read: $file${NC}"
        fi
    fi
done

if [ "$FDA_GRANTED" = true ]; then
    echo ""
    echo -e "${RED}🚨 FULL DISK ACCESS: GRANTED${NC}"
    echo "Windsurf can read protected system files!"
    echo "To revoke: System Settings → Privacy & Security → Full Disk Access"
else
    echo ""
    echo -e "${GREEN}✅ FULL DISK ACCESS: NOT GRANTED${NC}"
fi

echo ""
echo "=========================================="
echo "2. FOLDER ACCESS TEST"
echo "=========================================="

# Check common directories
TEST_DIRS=(
    "$HOME/Documents"
    "$HOME/Desktop"
    "$HOME/Downloads"
    "$HOME/Pictures"
    "$HOME/Movies"
    "$HOME/Music"
)

echo "Testing access to common folders:"
for dir in "${TEST_DIRS[@]}"; do
    if [ -d "$dir" ]; then
        if [ -r "$dir" ] && [ -w "$dir" ]; then
            echo -e "  ${YELLOW}📁 $dir - Read/Write access${NC}"
        elif [ -r "$dir" ]; then
            echo -e "  ${CYAN}📁 $dir - Read-only access${NC}"
        else
            echo -e "  ${GREEN}📁 $dir - No access${NC}"
        fi
    fi
done

echo ""
echo "=========================================="
echo "3. NETWORK CONNECTIONS TEST"
echo "=========================================="

echo "Active Windsurf network connections:"
CONNECTIONS=$(lsof -i -n -P 2>/dev/null | grep Windsurf)

if [ -z "$CONNECTIONS" ]; then
    echo -e "${GREEN}✅ No active network connections${NC}"
else
    CONNECTION_COUNT=$(echo "$CONNECTIONS" | wc -l | tr -d ' ')
    echo -e "${YELLOW}⚠️  Found $CONNECTION_COUNT active connections:${NC}"
    echo ""
    
    # Extract unique remote addresses
    echo "$CONNECTIONS" | awk '{print $9}' | grep '->' | cut -d'>' -f2 | sort -u | while read addr; do
        if [ ! -z "$addr" ] && [ "$addr" != "127.0.0.1" ]; then
            echo -e "  ${CYAN}🌐 $addr${NC}"
        fi
    done
fi

echo ""
echo "=========================================="
echo "4. OPEN FILES TEST"
echo "=========================================="

echo "Files currently open by Windsurf:"
OPEN_FILES=$(lsof -p $WINDSURF_PID 2>/dev/null | grep -E "\.txt|\.md|\.py|\.js|\.json|\.sh" | wc -l | tr -d ' ')

if [ "$OPEN_FILES" -gt 0 ]; then
    echo -e "${YELLOW}⚠️  $OPEN_FILES code/text files currently open${NC}"
    
    # Show sample of open files
    echo ""
    echo "Sample of open files:"
    lsof -p $WINDSURF_PID 2>/dev/null | grep -E "\.txt|\.md|\.py|\.js|\.json|\.sh" | head -5 | awk '{print $9}' | while read file; do
        echo -e "  ${CYAN}📄 $file${NC}"
    done
else
    echo -e "${GREEN}✅ No code files currently open${NC}"
fi

echo ""
echo "=========================================="
echo "5. MACOS PRIVACY PERMISSIONS"
echo "=========================================="

echo "Checking Info.plist for requested permissions:"

PLIST_PATH="/Applications/Windsurf.app/Contents/Info.plist"

if [ -f "$PLIST_PATH" ]; then
    # Camera
    if defaults read "$PLIST_PATH" NSCameraUsageDescription &>/dev/null; then
        echo -e "${YELLOW}📷 Camera: REQUESTED${NC}"
        echo "   Reason: $(defaults read "$PLIST_PATH" NSCameraUsageDescription 2>/dev/null)"
    else
        echo -e "${GREEN}📷 Camera: Not requested${NC}"
    fi
    
    # Microphone
    if defaults read "$PLIST_PATH" NSMicrophoneUsageDescription &>/dev/null; then
        echo -e "${YELLOW}🎤 Microphone: REQUESTED${NC}"
        echo "   Reason: $(defaults read "$PLIST_PATH" NSMicrophoneUsageDescription 2>/dev/null)"
    else
        echo -e "${GREEN}🎤 Microphone: Not requested${NC}"
    fi
    
    # Bluetooth
    if defaults read "$PLIST_PATH" NSBluetoothAlwaysUsageDescription &>/dev/null; then
        echo -e "${YELLOW}📡 Bluetooth: REQUESTED${NC}"
    else
        echo -e "${GREEN}📡 Bluetooth: Not requested${NC}"
    fi
    
    # AppleScript
    if defaults read "$PLIST_PATH" NSAppleEventsUsageDescription &>/dev/null; then
        echo -e "${YELLOW}⚡ AppleScript: REQUESTED${NC}"
    else
        echo -e "${GREEN}⚡ AppleScript: Not requested${NC}"
    fi
    
    # Location
    if defaults read "$PLIST_PATH" NSLocationWhenInUseUsageDescription &>/dev/null; then
        echo -e "${YELLOW}📍 Location: REQUESTED${NC}"
    else
        echo -e "${GREEN}📍 Location: Not requested${NC}"
    fi
else
    echo -e "${RED}❌ Cannot read Info.plist${NC}"
fi

echo ""
echo "=========================================="
echo "6. TCC DATABASE CHECK (requires sudo)"
echo "=========================================="

echo "Checking TCC (Transparency, Consent, and Control) database..."
echo "This shows actual GRANTED permissions (not just requested)"
echo ""

# Try to read TCC database
TCC_DB="/Library/Application Support/com.apple.TCC/TCC.db"

if [ -r "$TCC_DB" ]; then
    echo "Checking for Windsurf entries in TCC database:"
    sqlite3 "$TCC_DB" "SELECT service, client, auth_value FROM access WHERE client LIKE '%Windsurf%';" 2>/dev/null | while read line; do
        echo -e "${YELLOW}  $line${NC}"
    done
else
    echo -e "${CYAN}ℹ️  TCC database requires sudo access${NC}"
    echo "Run with sudo to see granted permissions:"
    echo "  sudo sqlite3 '$TCC_DB' \"SELECT service, client, auth_value FROM access WHERE client LIKE '%Windsurf%';\""
fi

echo ""
echo "=========================================="
echo "7. WORKSPACE TRACKING"
echo "=========================================="

STORAGE_JSON="$HOME/Library/Application Support/Windsurf/User/globalStorage/storage.json"

if [ -f "$STORAGE_JSON" ]; then
    # Count workspace references
    WORKSPACE_COUNT=$(grep -o "file://" "$STORAGE_JSON" 2>/dev/null | wc -l | tr -d ' ')
    
    if [ "$WORKSPACE_COUNT" -gt 0 ]; then
        echo -e "${YELLOW}⚠️  Found $WORKSPACE_COUNT workspace references${NC}"
        echo ""
        echo "Recently accessed folders:"
        
        # Extract unique folder paths
        python3 << 'EOF'
import json
import sys
try:
    with open('/Users/meep/Library/Application Support/Windsurf/User/globalStorage/storage.json', 'r') as f:
        data = json.load(f)
    
    folders = set()
    for key, value in data.items():
        if isinstance(value, str) and value.startswith('file://'):
            folder = value.replace('file://', '').replace('%20', ' ')
            folders.add(folder)
    
    for folder in sorted(folders)[:10]:
        print(f"  📂 {folder}")
    
    if len(folders) > 10:
        print(f"  ... and {len(folders) - 10} more")
except Exception as e:
    print(f"Error: {e}")
EOF
    else
        echo -e "${GREEN}✅ No workspace tracking found${NC}"
    fi
else
    echo -e "${GREEN}✅ Storage file not found${NC}"
fi

echo ""
echo "=========================================="
echo "8. PROCESS CAPABILITIES"
echo "=========================================="

echo "Windsurf process information:"
ps aux | grep Windsurf | grep -v grep | head -5 | while read line; do
    echo "  $line"
done

echo ""
echo "Memory usage:"
ps aux | grep Windsurf | grep -v grep | awk '{sum+=$6} END {print "  Total: " sum/1024 " MB"}'

echo ""
echo "=========================================="
echo "SUMMARY"
echo "=========================================="
echo ""

# Generate summary
ISSUES=0

if [ "$FDA_GRANTED" = true ]; then
    echo -e "${RED}🚨 Full Disk Access is GRANTED - High Risk${NC}"
    ((ISSUES++))
fi

if [ "$CONNECTION_COUNT" -gt 20 ]; then
    echo -e "${YELLOW}⚠️  Many network connections ($CONNECTION_COUNT) - Monitor activity${NC}"
    ((ISSUES++))
fi

if [ "$WORKSPACE_COUNT" -gt 10 ]; then
    echo -e "${YELLOW}⚠️  Many workspaces tracked ($WORKSPACE_COUNT) - Consider cleanup${NC}"
    ((ISSUES++))
fi

if [ "$ISSUES" -eq 0 ]; then
    echo -e "${GREEN}✅ No major permission issues detected${NC}"
    echo ""
    echo "Privacy Status: GOOD"
else
    echo ""
    echo -e "${YELLOW}Privacy Status: REVIEW RECOMMENDED${NC}"
    echo ""
    echo "Recommendations:"
    [ "$FDA_GRANTED" = true ] && echo "  1. Revoke Full Disk Access if not needed"
    [ "$CONNECTION_COUNT" -gt 20 ] && echo "  2. Monitor network activity with Network Monitor tab"
    [ "$WORKSPACE_COUNT" -gt 10 ] && echo "  3. Run Enhanced Cleanup to clear workspace tracking"
fi

echo ""
echo "=========================================="
echo "Test complete: $(date)"
echo "=========================================="
echo ""
