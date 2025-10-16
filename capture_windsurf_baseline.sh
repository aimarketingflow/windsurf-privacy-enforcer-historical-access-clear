#!/bin/bash

# Windsurf Baseline Capture Script
# Captures network activity, system diagnostics, and tracking data for before/after comparison

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

# Timestamp
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BASELINE_DIR="$HOME/Documents/AIMFGuideforCybersec*°·/WindsurfExploit-Oct25/baselines/baseline_$TIMESTAMP"

echo -e "${CYAN}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║     Windsurf Baseline Capture Tool                        ║${NC}"
echo -e "${CYAN}║     Capturing system state for before/after comparison    ║${NC}"
echo -e "${CYAN}╔════════════════════════════════════════════════════════════╗${NC}"
echo ""

# Create baseline directory
mkdir -p "$BASELINE_DIR"/{network,system,tracking,processes}

echo -e "${BLUE}📁 Baseline directory: $BASELINE_DIR${NC}"
echo ""

# ============================================================================
# 1. NETWORK CAPTURE
# ============================================================================
echo -e "${CYAN}═══════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}🌐 NETWORK ACTIVITY CAPTURE${NC}"
echo -e "${CYAN}═══════════════════════════════════════════════════════════${NC}"

# Check if Windsurf is running
if pgrep -x "Windsurf" > /dev/null; then
    echo -e "${GREEN}✓ Windsurf is running${NC}"
    WINDSURF_RUNNING=true
else
    echo -e "${YELLOW}⚠ Windsurf is not running${NC}"
    echo -e "${YELLOW}  Start Windsurf and run this script again for accurate capture${NC}"
    WINDSURF_RUNNING=false
fi

echo ""
echo -e "${BLUE}Capturing active connections...${NC}"

# Active connections
lsof -i -n -P | grep -i windsurf > "$BASELINE_DIR/network/active_connections.txt" 2>/dev/null
netstat -an | grep ESTABLISHED > "$BASELINE_DIR/network/established_connections.txt" 2>/dev/null

# Connection count
CONN_COUNT=$(lsof -i -n -P | grep -i windsurf | wc -l | tr -d ' ')
echo -e "${GREEN}✓ Captured $CONN_COUNT active Windsurf connections${NC}"

# DNS queries (if available)
if command -v tcpdump &> /dev/null; then
    echo -e "${BLUE}Capturing DNS queries (10 seconds)...${NC}"
    sudo tcpdump -i any -n port 53 -c 50 -w "$BASELINE_DIR/network/dns_queries.pcap" 2>/dev/null &
    TCPDUMP_PID=$!
    sleep 10
    sudo kill $TCPDUMP_PID 2>/dev/null
    echo -e "${GREEN}✓ DNS queries captured${NC}"
fi

# Network statistics
echo -e "${BLUE}Capturing network statistics...${NC}"
netstat -s > "$BASELINE_DIR/network/network_stats.txt" 2>/dev/null
ifconfig > "$BASELINE_DIR/network/interfaces.txt" 2>/dev/null
echo -e "${GREEN}✓ Network statistics captured${NC}"

echo ""

# ============================================================================
# 2. SYSTEM DIAGNOSTICS
# ============================================================================
echo -e "${CYAN}═══════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}🔧 SYSTEM DIAGNOSTICS${NC}"
echo -e "${CYAN}═══════════════════════════════════════════════════════════${NC}"

# Spindump (if Windsurf is running)
if [ "$WINDSURF_RUNNING" = true ]; then
    echo -e "${BLUE}Capturing spindump (this may take 10 seconds)...${NC}"
    WINDSURF_PID=$(pgrep -x "Windsurf" | head -1)
    sudo spindump $WINDSURF_PID 10 -file "$BASELINE_DIR/system/windsurf_spindump.txt" 2>/dev/null
    echo -e "${GREEN}✓ Spindump captured${NC}"
fi

# Process information
echo -e "${BLUE}Capturing process information...${NC}"
ps aux | grep -i windsurf > "$BASELINE_DIR/processes/windsurf_processes.txt"
top -l 1 | grep -i windsurf > "$BASELINE_DIR/processes/windsurf_top.txt"
echo -e "${GREEN}✓ Process information captured${NC}"

# Memory usage
echo -e "${BLUE}Capturing memory usage...${NC}"
vm_stat > "$BASELINE_DIR/system/memory_stats.txt"
echo -e "${GREEN}✓ Memory statistics captured${NC}"

# File descriptors
echo -e "${BLUE}Capturing file descriptors...${NC}"
if [ "$WINDSURF_RUNNING" = true ]; then
    lsof -p $WINDSURF_PID > "$BASELINE_DIR/system/file_descriptors.txt" 2>/dev/null
    echo -e "${GREEN}✓ File descriptors captured${NC}"
fi

echo ""

# ============================================================================
# 3. TRACKING DATA SNAPSHOT
# ============================================================================
echo -e "${CYAN}═══════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}🔍 TRACKING DATA SNAPSHOT${NC}"
echo -e "${CYAN}═══════════════════════════════════════════════════════════${NC}"

# Storage.json
echo -e "${BLUE}Capturing storage.json...${NC}"
if [ -f ~/Library/Application\ Support/Windsurf/User/globalStorage/storage.json ]; then
    cp ~/Library/Application\ Support/Windsurf/User/globalStorage/storage.json "$BASELINE_DIR/tracking/storage.json"
    
    # Extract key tracking IDs
    cat "$BASELINE_DIR/tracking/storage.json" | python3 -m json.tool > "$BASELINE_DIR/tracking/storage_pretty.json" 2>/dev/null
    
    # Count tracked items
    MACHINE_ID=$(grep -o '"telemetry.machineId"[^,]*' "$BASELINE_DIR/tracking/storage.json" | cut -d'"' -f4)
    WORKSPACE_COUNT=$(grep -o '"workspaces"' "$BASELINE_DIR/tracking/storage.json" | wc -l | tr -d ' ')
    
    echo -e "${GREEN}✓ Storage.json captured${NC}"
    echo -e "  Machine ID: ${MACHINE_ID:0:20}..."
    echo -e "  Tracked workspaces: $WORKSPACE_COUNT"
else
    echo -e "${YELLOW}⚠ storage.json not found${NC}"
fi

# Workspace storage
echo -e "${BLUE}Capturing workspace storage info...${NC}"
if [ -d ~/Library/Application\ Support/Windsurf/User/workspaceStorage ]; then
    ls -la ~/Library/Application\ Support/Windsurf/User/workspaceStorage > "$BASELINE_DIR/tracking/workspace_list.txt"
    WORKSPACE_DIRS=$(ls ~/Library/Application\ Support/Windsurf/User/workspaceStorage | wc -l | tr -d ' ')
    echo -e "${GREEN}✓ Found $WORKSPACE_DIRS workspace directories${NC}"
fi

# Cache size
echo -e "${BLUE}Calculating cache sizes...${NC}"
CACHE_SIZE=$(du -sh ~/Library/Application\ Support/Windsurf 2>/dev/null | cut -f1)
echo -e "${GREEN}✓ Total Windsurf data: $CACHE_SIZE${NC}"

echo ""

# ============================================================================
# 4. GENERATE SUMMARY REPORT
# ============================================================================
echo -e "${CYAN}═══════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}📊 GENERATING SUMMARY REPORT${NC}"
echo -e "${CYAN}═══════════════════════════════════════════════════════════${NC}"

cat > "$BASELINE_DIR/BASELINE_SUMMARY.txt" << EOF
Windsurf Baseline Capture Summary
==================================
Capture Date: $(date)
Timestamp: $TIMESTAMP

SYSTEM STATUS
-------------
Windsurf Running: $WINDSURF_RUNNING
Windsurf PID: ${WINDSURF_PID:-N/A}

NETWORK ACTIVITY
----------------
Active Connections: $CONN_COUNT
DNS Queries: Captured (10 seconds)
Network Stats: Captured

TRACKING DATA
-------------
Machine ID: ${MACHINE_ID:-Not found}
Tracked Workspaces: ${WORKSPACE_COUNT:-0}
Workspace Directories: ${WORKSPACE_DIRS:-0}
Total Data Size: ${CACHE_SIZE:-Unknown}

FILES CAPTURED
--------------
Network:
  - active_connections.txt
  - established_connections.txt
  - dns_queries.pcap
  - network_stats.txt
  - interfaces.txt

System:
  - windsurf_spindump.txt
  - memory_stats.txt
  - file_descriptors.txt

Processes:
  - windsurf_processes.txt
  - windsurf_top.txt

Tracking:
  - storage.json
  - storage_pretty.json
  - workspace_list.txt

BASELINE LOCATION
-----------------
$BASELINE_DIR

NEXT STEPS
----------
1. Run cleanup: ./clear_windsurf_tracking_ENHANCED.sh
2. Wait 24 hours of normal usage
3. Run this script again to capture "after" baseline
4. Compare baselines using: ./compare_baselines.sh

EOF

echo -e "${GREEN}✓ Summary report generated${NC}"
echo ""

# ============================================================================
# 5. DISPLAY SUMMARY
# ============================================================================
echo -e "${CYAN}═══════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}✅ BASELINE CAPTURE COMPLETE${NC}"
echo -e "${CYAN}═══════════════════════════════════════════════════════════${NC}"
echo ""
echo -e "${BLUE}📊 Quick Stats:${NC}"
echo -e "  Windsurf Running: $WINDSURF_RUNNING"
echo -e "  Active Connections: $CONN_COUNT"
echo -e "  Tracked Workspaces: ${WORKSPACE_COUNT:-0}"
echo -e "  Total Data Size: ${CACHE_SIZE:-Unknown}"
echo ""
echo -e "${BLUE}📁 Baseline saved to:${NC}"
echo -e "  $BASELINE_DIR"
echo ""
echo -e "${YELLOW}📝 Next Steps:${NC}"
echo -e "  1. Review baseline: cat $BASELINE_DIR/BASELINE_SUMMARY.txt"
echo -e "  2. Run cleanup (if this is 'before' baseline)"
echo -e "  3. Wait 24 hours"
echo -e "  4. Run this script again for 'after' baseline"
echo -e "  5. Compare: ./compare_baselines.sh"
echo ""
echo -e "${GREEN}Done!${NC}"
