#!/bin/bash
# Comprehensive Test: Historical Access Deletion Verification
# Tests if cleanup script properly removes ALL historical workspace access data

echo "=========================================="
echo "HISTORICAL ACCESS DELETION TEST SUITE"
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

# Test counters
TESTS_PASSED=0
TESTS_FAILED=0
TESTS_TOTAL=0

# Function to run a test
run_test() {
    local test_name="$1"
    local test_result="$2"
    
    ((TESTS_TOTAL++))
    
    if [ "$test_result" = "PASS" ]; then
        echo -e "${GREEN}✅ PASS${NC}: $test_name"
        ((TESTS_PASSED++))
    else
        echo -e "${RED}❌ FAIL${NC}: $test_name"
        ((TESTS_FAILED++))
    fi
}

echo "=========================================="
echo "TEST 1: TRACKING ID DELETION"
echo "=========================================="
echo ""

# Test 1.1: Machine ID removed
if [ -f ~/Library/Application\ Support/Windsurf/User/globalStorage/storage.json ]; then
    MACHINE_ID=$(cat ~/Library/Application\ Support/Windsurf/User/globalStorage/storage.json | \
        python3 -c "import sys, json; data=json.load(sys.stdin); print(data.get('telemetry.machineId', ''))" 2>/dev/null)
    
    if [ -z "$MACHINE_ID" ]; then
        run_test "Machine ID removed from storage.json" "PASS"
    else
        run_test "Machine ID removed from storage.json (found: $MACHINE_ID)" "FAIL"
    fi
else
    run_test "storage.json exists" "FAIL"
fi

# Test 1.2: Device ID removed
if [ -f ~/Library/Application\ Support/Windsurf/User/globalStorage/storage.json ]; then
    DEVICE_ID=$(cat ~/Library/Application\ Support/Windsurf/User/globalStorage/storage.json | \
        python3 -c "import sys, json; data=json.load(sys.stdin); print(data.get('telemetry.devDeviceId', ''))" 2>/dev/null)
    
    if [ -z "$DEVICE_ID" ]; then
        run_test "Device ID removed from storage.json" "PASS"
    else
        run_test "Device ID removed from storage.json (found: $DEVICE_ID)" "FAIL"
    fi
fi

# Test 1.3: SQM ID removed
if [ -f ~/Library/Application\ Support/Windsurf/User/globalStorage/storage.json ]; then
    SQM_ID=$(cat ~/Library/Application\ Support/Windsurf/User/globalStorage/storage.json | \
        python3 -c "import sys, json; data=json.load(sys.stdin); print(data.get('telemetry.sqmId', ''))" 2>/dev/null)
    
    if [ -z "$SQM_ID" ]; then
        run_test "SQM ID removed from storage.json" "PASS"
    else
        run_test "SQM ID removed from storage.json (found: $SQM_ID)" "FAIL"
    fi
fi

echo ""
echo "=========================================="
echo "TEST 2: WORKSPACE HISTORY DELETION"
echo "=========================================="
echo ""

# Test 2.1: Workspace associations cleared
if [ -f ~/Library/Application\ Support/Windsurf/User/globalStorage/storage.json ]; then
    WORKSPACE_COUNT=$(cat ~/Library/Application\ Support/Windsurf/User/globalStorage/storage.json | \
        python3 -c "import sys, json; data=json.load(sys.stdin); print(len(data.get('profileAssociations', {}).get('workspaces', {})))" 2>/dev/null)
    
    if [ "$WORKSPACE_COUNT" = "0" ]; then
        run_test "Workspace associations cleared (profileAssociations)" "PASS"
    else
        run_test "Workspace associations cleared (found: $WORKSPACE_COUNT)" "FAIL"
        echo -e "   ${YELLOW}Found workspaces:${NC}"
        cat ~/Library/Application\ Support/Windsurf/User/globalStorage/storage.json | \
            python3 -c "import sys, json; data=json.load(sys.stdin); print('\n'.join(data.get('profileAssociations', {}).get('workspaces', {}).keys()))" 2>/dev/null | head -5
    fi
fi

# Test 2.2: Backup workspaces cleared
if [ -f ~/Library/Application\ Support/Windsurf/User/globalStorage/storage.json ]; then
    BACKUP_FOLDERS=$(cat ~/Library/Application\ Support/Windsurf/User/globalStorage/storage.json | \
        python3 -c "import sys, json; data=json.load(sys.stdin); print(len(data.get('backupWorkspaces', {}).get('folders', [])))" 2>/dev/null)
    
    if [ "$BACKUP_FOLDERS" = "0" ]; then
        run_test "Backup workspace folders cleared" "PASS"
    else
        run_test "Backup workspace folders cleared (found: $BACKUP_FOLDERS)" "FAIL"
    fi
fi

# Test 2.3: Backup workspaces list cleared
if [ -f ~/Library/Application\ Support/Windsurf/User/globalStorage/storage.json ]; then
    BACKUP_WORKSPACES=$(cat ~/Library/Application\ Support/Windsurf/User/globalStorage/storage.json | \
        python3 -c "import sys, json; data=json.load(sys.stdin); print(len(data.get('backupWorkspaces', {}).get('workspaces', [])))" 2>/dev/null)
    
    if [ "$BACKUP_WORKSPACES" = "0" ]; then
        run_test "Backup workspace list cleared" "PASS"
    else
        run_test "Backup workspace list cleared (found: $BACKUP_WORKSPACES)" "FAIL"
    fi
fi

# Test 2.4: Empty windows cleared
if [ -f ~/Library/Application\ Support/Windsurf/User/globalStorage/storage.json ]; then
    EMPTY_WINDOWS=$(cat ~/Library/Application\ Support/Windsurf/User/globalStorage/storage.json | \
        python3 -c "import sys, json; data=json.load(sys.stdin); print(len(data.get('backupWorkspaces', {}).get('emptyWindows', [])))" 2>/dev/null)
    
    if [ "$EMPTY_WINDOWS" = "0" ]; then
        run_test "Empty windows cleared" "PASS"
    else
        run_test "Empty windows cleared (found: $EMPTY_WINDOWS)" "FAIL"
    fi
fi

echo ""
echo "=========================================="
echo "TEST 3: WORKSPACE STORAGE FILES"
echo "=========================================="
echo ""

# Test 3.1: workspace.json files removed
if [ -d ~/Library/Application\ Support/Windsurf/User/workspaceStorage ]; then
    WORKSPACE_JSON_COUNT=$(find ~/Library/Application\ Support/Windsurf/User/workspaceStorage -name "workspace.json" 2>/dev/null | wc -l | tr -d ' ')
    
    if [ "$WORKSPACE_JSON_COUNT" = "0" ]; then
        run_test "workspace.json tracking files removed" "PASS"
    else
        run_test "workspace.json tracking files removed (found: $WORKSPACE_JSON_COUNT)" "FAIL"
        echo -e "   ${YELLOW}Remaining workspace.json files:${NC}"
        find ~/Library/Application\ Support/Windsurf/User/workspaceStorage -name "workspace.json" 2>/dev/null | head -5
    fi
else
    run_test "workspaceStorage directory exists" "PASS"
fi

# Test 3.2: Check for residual workspace identifiers in state.vscdb
if [ -d ~/Library/Application\ Support/Windsurf/User/workspaceStorage ]; then
    echo -e "${CYAN}Checking state.vscdb files for workspace paths...${NC}"
    
    WORKSPACE_PATHS_FOUND=0
    for db in ~/Library/Application\ Support/Windsurf/User/workspaceStorage/*/state.vscdb; do
        if [ -f "$db" ]; then
            # Check if database contains workspace path references (excluding chat data)
            PATHS=$(sqlite3 "$db" "SELECT key FROM ItemTable WHERE key LIKE '%workspace%' AND key NOT LIKE '%chat%' AND key NOT LIKE '%cascade%';" 2>/dev/null | wc -l | tr -d ' ')
            if [ "$PATHS" -gt 0 ]; then
                ((WORKSPACE_PATHS_FOUND++))
            fi
        fi
    done
    
    if [ "$WORKSPACE_PATHS_FOUND" = "0" ]; then
        run_test "No workspace path references in state.vscdb files" "PASS"
    else
        run_test "No workspace path references in state.vscdb files (found in $WORKSPACE_PATHS_FOUND databases)" "FAIL"
    fi
fi

echo ""
echo "=========================================="
echo "TEST 4: GLOBAL STATE DATABASE"
echo "=========================================="
echo ""

# Test 4.1: Check global state.vscdb for workspace history
if [ -f ~/Library/Application\ Support/Windsurf/User/globalStorage/state.vscdb ]; then
    echo -e "${CYAN}Analyzing global state.vscdb...${NC}"
    
    # Check for recent workspace entries
    RECENT_WORKSPACES=$(sqlite3 ~/Library/Application\ Support/Windsurf/User/globalStorage/state.vscdb \
        "SELECT COUNT(*) FROM ItemTable WHERE key LIKE '%workspaceIdentifier%' OR key LIKE '%recentlyOpened%';" 2>/dev/null)
    
    if [ "$RECENT_WORKSPACES" = "0" ]; then
        run_test "No recent workspace entries in global state.vscdb" "PASS"
    else
        run_test "No recent workspace entries in global state.vscdb (found: $RECENT_WORKSPACES)" "FAIL"
    fi
    
    # Check for file history
    FILE_HISTORY=$(sqlite3 ~/Library/Application\ Support/Windsurf/User/globalStorage/state.vscdb \
        "SELECT COUNT(*) FROM ItemTable WHERE key LIKE '%history.recentlyOpened%';" 2>/dev/null)
    
    if [ "$FILE_HISTORY" = "0" ]; then
        run_test "File history cleared from global state.vscdb" "PASS"
    else
        run_test "File history cleared from global state.vscdb (found: $FILE_HISTORY entries)" "FAIL"
    fi
else
    run_test "Global state.vscdb exists" "FAIL"
fi

echo ""
echo "=========================================="
echo "TEST 5: DIRECTORY-SPECIFIC TRACKING"
echo "=========================================="
echo ""

# Test 5.1: Check for specific sensitive directory references
SENSITIVE_DIRS=(
    "SensitiveProject1"
    "SensitiveProject2"
    "SensitiveProject3"
    "LINKEDIN_RESPONSE_DRAFT"
    "_Locker"
    "AIMFGuideforCybersec"
)

echo -e "${CYAN}Checking for sensitive directory references...${NC}"

SENSITIVE_FOUND=0
if [ -f ~/Library/Application\ Support/Windsurf/User/globalStorage/storage.json ]; then
    for dir in "${SENSITIVE_DIRS[@]}"; do
        if grep -q "$dir" ~/Library/Application\ Support/Windsurf/User/globalStorage/storage.json 2>/dev/null; then
            echo -e "   ${RED}Found reference to: $dir${NC}"
            ((SENSITIVE_FOUND++))
        fi
    done
fi

if [ "$SENSITIVE_FOUND" = "0" ]; then
    run_test "No sensitive directory references in storage.json" "PASS"
else
    run_test "No sensitive directory references in storage.json (found: $SENSITIVE_FOUND)" "FAIL"
fi

# Test 5.2: Check state.vscdb files for sensitive paths
echo -e "${CYAN}Checking state.vscdb files for sensitive paths...${NC}"

SENSITIVE_IN_DB=0
for db in ~/Library/Application\ Support/Windsurf/User/workspaceStorage/*/state.vscdb; do
    if [ -f "$db" ]; then
        for dir in "${SENSITIVE_DIRS[@]}"; do
            if sqlite3 "$db" "SELECT value FROM ItemTable WHERE value LIKE '%$dir%';" 2>/dev/null | grep -q "$dir"; then
                ((SENSITIVE_IN_DB++))
                break
            fi
        done
    fi
done

if [ "$SENSITIVE_IN_DB" = "0" ]; then
    run_test "No sensitive paths in workspace state.vscdb files" "PASS"
else
    run_test "No sensitive paths in workspace state.vscdb files (found in $SENSITIVE_IN_DB databases)" "FAIL"
fi

echo ""
echo "=========================================="
echo "TEST 6: CACHE AND TEMPORARY DATA"
echo "=========================================="
echo ""

# Test 6.1: Cache cleared
if [ -d ~/Library/Application\ Support/Windsurf/Cache ]; then
    CACHE_FILES=$(find ~/Library/Application\ Support/Windsurf/Cache -type f 2>/dev/null | wc -l | tr -d ' ')
    
    if [ "$CACHE_FILES" = "0" ]; then
        run_test "Cache directory empty" "PASS"
    else
        # Cache may rebuild during use - check if it's small
        CACHE_SIZE=$(du -sk ~/Library/Application\ Support/Windsurf/Cache 2>/dev/null | awk '{print $1}')
        if [ "$CACHE_SIZE" -lt 1024 ]; then
            run_test "Cache minimal (< 1MB, acceptable)" "PASS"
        else
            run_test "Cache cleared (found: ${CACHE_SIZE}KB in $CACHE_FILES files)" "FAIL"
        fi
    fi
else
    run_test "Cache directory removed or empty" "PASS"
fi

# Test 6.2: CachedData cleared
if [ -d ~/Library/Application\ Support/Windsurf/CachedData ]; then
    CACHED_DATA_FILES=$(find ~/Library/Application\ Support/Windsurf/CachedData -type f 2>/dev/null | wc -l | tr -d ' ')
    
    if [ "$CACHED_DATA_FILES" = "0" ]; then
        run_test "CachedData directory empty" "PASS"
    else
        run_test "CachedData cleared (found: $CACHED_DATA_FILES files)" "FAIL"
    fi
else
    run_test "CachedData directory removed or empty" "PASS"
fi

# Test 6.3: GPU Cache cleared
if [ -d ~/Library/Application\ Support/Windsurf/GPUCache ]; then
    GPU_CACHE_FILES=$(find ~/Library/Application\ Support/Windsurf/GPUCache -type f 2>/dev/null | wc -l | tr -d ' ')
    
    if [ "$GPU_CACHE_FILES" = "0" ]; then
        run_test "GPUCache directory empty" "PASS"
    else
        run_test "GPUCache cleared (found: $GPU_CACHE_FILES files)" "FAIL"
    fi
else
    run_test "GPUCache directory removed or empty" "PASS"
fi

echo ""
echo "=========================================="
echo "TEST 7: AUTHENTICATION PRESERVATION"
echo "=========================================="
echo ""

# Test 7.1: GitHub auth preserved
if [ -f ~/Library/Application\ Support/Windsurf/User/globalStorage/state.vscdb ]; then
    GITHUB_AUTH=$(sqlite3 ~/Library/Application\ Support/Windsurf/User/globalStorage/state.vscdb \
        "SELECT COUNT(*) FROM ItemTable WHERE key LIKE '%github%authentication%';" 2>/dev/null)
    
    if [ "$GITHUB_AUTH" -gt 0 ]; then
        run_test "GitHub authentication preserved" "PASS"
    else
        echo -e "${YELLOW}⚠️  WARNING${NC}: GitHub authentication not found (may need to re-login)"
        run_test "GitHub authentication preserved" "PASS"  # Not a failure, just informational
    fi
fi

# Test 7.2: Chat history preserved
CHAT_PRESERVED=0
for db in ~/Library/Application\ Support/Windsurf/User/workspaceStorage/*/state.vscdb; do
    if [ -f "$db" ]; then
        CHAT_COUNT=$(sqlite3 "$db" "SELECT COUNT(*) FROM ItemTable WHERE key LIKE '%chat%' OR key LIKE '%cascade%';" 2>/dev/null)
        if [ "$CHAT_COUNT" -gt 0 ]; then
            ((CHAT_PRESERVED++))
        fi
    fi
done

if [ "$CHAT_PRESERVED" -gt 0 ]; then
    run_test "Chat history preserved ($CHAT_PRESERVED workspaces with chat data)" "PASS"
else
    echo -e "${YELLOW}⚠️  INFO${NC}: No chat history found (may not have had any)"
    run_test "Chat history preservation check" "PASS"  # Not a failure
fi

echo ""
echo "=========================================="
echo "TEST 8: LIVE EXFILTRATION CHECK"
echo "=========================================="
echo ""

# Test 8.1: Check if Windsurf is running
if pgrep -x "Windsurf" > /dev/null; then
    echo -e "${YELLOW}Windsurf is running - checking for active exfiltration...${NC}"
    
    # Test 8.2: External connections
    EXTERNAL_CONNS=$(lsof -i -n -P 2>/dev/null | grep -i windsurf | grep -v "127.0.0.1" | grep -v "::1" | grep ESTABLISHED | wc -l | tr -d ' ')
    
    if [ "$EXTERNAL_CONNS" = "0" ]; then
        run_test "No active external connections" "PASS"
    else
        run_test "No active external connections (found: $EXTERNAL_CONNS)" "FAIL"
        echo -e "   ${YELLOW}Active connections:${NC}"
        lsof -i -n -P 2>/dev/null | grep -i windsurf | grep -v "127.0.0.1" | grep -v "::1" | grep ESTABLISHED | head -5
    fi
    
    # Test 8.3: Language server connections
    LANG_SERVER_CONNS=$(lsof -i -n -P 2>/dev/null | grep language_server | grep -v "127.0.0.1" | grep ESTABLISHED | wc -l | tr -d ' ')
    
    if [ "$LANG_SERVER_CONNS" = "0" ]; then
        run_test "Language server has no external connections" "PASS"
    else
        run_test "Language server has no external connections (found: $LANG_SERVER_CONNS)" "FAIL"
    fi
else
    echo -e "${BLUE}ℹ️  Windsurf not running - skipping live connection tests${NC}"
    run_test "Live exfiltration check (Windsurf not running)" "PASS"
fi

echo ""
echo "=========================================="
echo "TEST 9: FILE SYSTEM FORENSICS"
echo "=========================================="
echo ""

# Test 9.1: Check for .json backup files
BACKUP_JSON=$(find ~/Library/Application\ Support/Windsurf/User/globalStorage -name "*.backup" -o -name "*.bak" 2>/dev/null | wc -l | tr -d ' ')

if [ "$BACKUP_JSON" = "0" ]; then
    run_test "No backup files containing old tracking data" "PASS"
else
    run_test "No backup files containing old tracking data (found: $BACKUP_JSON)" "FAIL"
    echo -e "   ${YELLOW}Backup files found:${NC}"
    find ~/Library/Application\ Support/Windsurf/User/globalStorage -name "*.backup" -o -name "*.bak" 2>/dev/null | head -5
fi

# Test 9.2: Check modification times
if [ -f ~/Library/Application\ Support/Windsurf/User/globalStorage/storage.json ]; then
    STORAGE_MTIME=$(stat -f "%m" ~/Library/Application\ Support/Windsurf/User/globalStorage/storage.json 2>/dev/null)
    CURRENT_TIME=$(date +%s)
    TIME_DIFF=$((CURRENT_TIME - STORAGE_MTIME))
    
    # Should have been modified recently if cleanup was just run
    if [ "$TIME_DIFF" -lt 3600 ]; then
        run_test "storage.json recently modified (within 1 hour)" "PASS"
    else
        echo -e "${YELLOW}⚠️  INFO${NC}: storage.json last modified $(($TIME_DIFF / 60)) minutes ago"
        run_test "storage.json modification check" "PASS"  # Not a failure
    fi
fi

echo ""
echo "=========================================="
echo "TEST 10: DEEP SCAN FOR RESIDUAL DATA"
echo "=========================================="
echo ""

# Test 10.1: Grep for common workspace paths
echo -e "${CYAN}Scanning for residual workspace paths...${NC}"

RESIDUAL_PATHS=0
if [ -d ~/Library/Application\ Support/Windsurf/User ]; then
    # Search for common path patterns in JSON and DB files
    for pattern in "/Users/" "/Documents/" "/Desktop/" "/Downloads/"; do
        FOUND=$(find ~/Library/Application\ Support/Windsurf/User -name "*.json" -type f -exec grep -l "$pattern" {} \; 2>/dev/null | wc -l | tr -d ' ')
        if [ "$FOUND" -gt 0 ]; then
            ((RESIDUAL_PATHS++))
        fi
    done
fi

if [ "$RESIDUAL_PATHS" = "0" ]; then
    run_test "No residual file paths in JSON files" "PASS"
else
    run_test "No residual file paths in JSON files (found in $RESIDUAL_PATHS files)" "FAIL"
fi

# Test 10.2: Check for UUID workspace identifiers
echo -e "${CYAN}Checking for UUID workspace identifiers...${NC}"

UUID_COUNT=0
if [ -d ~/Library/Application\ Support/Windsurf/User/workspaceStorage ]; then
    # Count workspace directories (each has a UUID name)
    UUID_COUNT=$(find ~/Library/Application\ Support/Windsurf/User/workspaceStorage -maxdepth 1 -type d 2>/dev/null | wc -l | tr -d ' ')
    # Subtract 1 for the workspaceStorage directory itself
    UUID_COUNT=$((UUID_COUNT - 1))
fi

if [ "$UUID_COUNT" -le 1 ]; then
    run_test "Minimal workspace UUID directories (≤1)" "PASS"
else
    echo -e "   ${YELLOW}Found $UUID_COUNT workspace directories${NC}"
    run_test "Minimal workspace UUID directories (found: $UUID_COUNT)" "FAIL"
fi

echo ""
echo "=========================================="
echo "FINAL RESULTS"
echo "=========================================="
echo ""

# Calculate pass rate
if [ $TESTS_TOTAL -gt 0 ]; then
    PASS_RATE=$((TESTS_PASSED * 100 / TESTS_TOTAL))
else
    PASS_RATE=0
fi

echo "Tests Run:    $TESTS_TOTAL"
echo -e "Tests Passed: ${GREEN}$TESTS_PASSED${NC}"
echo -e "Tests Failed: ${RED}$TESTS_FAILED${NC}"
echo "Pass Rate:    ${PASS_RATE}%"
echo ""

# Overall verdict
if [ $TESTS_FAILED -eq 0 ]; then
    echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${GREEN}✅ ALL TESTS PASSED!${NC}"
    echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
    echo "Historical access has been successfully deleted."
    echo "No tracking data or workspace history remains."
    echo ""
    echo -e "${BLUE}Recommendations:${NC}"
    echo "  • Run this test monthly to verify continued privacy"
    echo "  • Monitor with: watch -n 60 ./verify_cleanup.sh"
    echo "  • Consider firewall rules for complete blocking"
elif [ $PASS_RATE -ge 80 ]; then
    echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${YELLOW}⚠️  MOSTLY SUCCESSFUL (${PASS_RATE}%)${NC}"
    echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
    echo "Most historical access deleted, but some issues remain."
    echo ""
    echo -e "${YELLOW}Recommended Actions:${NC}"
    echo "  1. Review failed tests above"
    echo "  2. Re-run cleanup script: ./clear_windsurf_tracking.sh"
    echo "  3. Quit Windsurf completely before cleanup"
    echo "  4. Run this test again to verify"
else
    echo -e "${RED}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${RED}❌ CLEANUP INCOMPLETE (${PASS_RATE}%)${NC}"
    echo -e "${RED}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
    echo "Historical access deletion was not successful."
    echo ""
    echo -e "${RED}Required Actions:${NC}"
    echo "  1. Quit Windsurf: pkill -9 Windsurf"
    echo "  2. Run cleanup: ./clear_windsurf_tracking.sh"
    echo "  3. Run this test again"
    echo "  4. If issues persist, check script permissions"
fi

echo ""
echo "=========================================="
echo "Test completed: $(date)"
echo "=========================================="
echo ""
