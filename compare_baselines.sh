#!/bin/bash

# Windsurf Baseline Comparison Script
# Compares before/after baselines to show cleanup effectiveness

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

BASELINES_DIR="$HOME/Documents/AIMFGuideforCybersec*°·/WindsurfExploit-Oct25/baselines"

echo -e "${CYAN}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║     Windsurf Baseline Comparison Tool                     ║${NC}"
echo -e "${CYAN}║     Before/After Cleanup Analysis                          ║${NC}"
echo -e "${CYAN}╚════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Find available baselines
if [ ! -d "$BASELINES_DIR" ]; then
    echo -e "${RED}❌ No baselines directory found${NC}"
    echo -e "${YELLOW}Run ./capture_windsurf_baseline.sh first${NC}"
    exit 1
fi

BASELINES=($(ls -d "$BASELINES_DIR"/baseline_* 2>/dev/null | sort))

if [ ${#BASELINES[@]} -lt 2 ]; then
    echo -e "${YELLOW}⚠ Need at least 2 baselines to compare${NC}"
    echo -e "${BLUE}Available baselines: ${#BASELINES[@]}${NC}"
    echo ""
    echo -e "${YELLOW}To create baselines:${NC}"
    echo -e "  1. Run: ./capture_windsurf_baseline.sh  (before cleanup)"
    echo -e "  2. Run: ./clear_windsurf_tracking_ENHANCED.sh"
    echo -e "  3. Wait 24 hours"
    echo -e "  4. Run: ./capture_windsurf_baseline.sh  (after cleanup)"
    echo -e "  5. Run: ./compare_baselines.sh"
    exit 1
fi

# List available baselines
echo -e "${BLUE}Available Baselines:${NC}"
for i in "${!BASELINES[@]}"; do
    BASENAME=$(basename "${BASELINES[$i]}")
    TIMESTAMP=$(echo "$BASENAME" | sed 's/baseline_//')
    DATE=$(echo "$TIMESTAMP" | sed 's/\([0-9]\{4\}\)\([0-9]\{2\}\)\([0-9]\{2\}\)_\([0-9]\{2\}\)\([0-9]\{2\}\)\([0-9]\{2\}\)/\1-\2-\3 \4:\5:\6/')
    echo -e "  $((i+1)). $DATE"
done

echo ""
echo -e "${YELLOW}Select BEFORE baseline (number):${NC} "
read BEFORE_NUM

echo -e "${YELLOW}Select AFTER baseline (number):${NC} "
read AFTER_NUM

BEFORE="${BASELINES[$((BEFORE_NUM-1))]}"
AFTER="${BASELINES[$((AFTER_NUM-1))]}"

if [ ! -d "$BEFORE" ] || [ ! -d "$AFTER" ]; then
    echo -e "${RED}❌ Invalid selection${NC}"
    exit 1
fi

echo ""
echo -e "${GREEN}Comparing:${NC}"
echo -e "  BEFORE: $(basename "$BEFORE")"
echo -e "  AFTER:  $(basename "$AFTER")"
echo ""

# Create comparison report
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
REPORT_DIR="$BASELINES_DIR/comparison_$TIMESTAMP"
mkdir -p "$REPORT_DIR"

REPORT="$REPORT_DIR/COMPARISON_REPORT.txt"

# ============================================================================
# GENERATE COMPARISON REPORT
# ============================================================================

cat > "$REPORT" << EOF
Windsurf Baseline Comparison Report
====================================
Generated: $(date)

BASELINES COMPARED
------------------
BEFORE: $(basename "$BEFORE")
AFTER:  $(basename "$AFTER")

EOF

echo -e "${CYAN}═══════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}📊 ANALYZING DIFFERENCES${NC}"
echo -e "${CYAN}═══════════════════════════════════════════════════════════${NC}"
echo ""

# ============================================================================
# 1. NETWORK CONNECTIONS
# ============================================================================
echo -e "${BLUE}🌐 Network Connections...${NC}"

BEFORE_CONN=$(wc -l < "$BEFORE/network/active_connections.txt" 2>/dev/null || echo "0")
AFTER_CONN=$(wc -l < "$AFTER/network/active_connections.txt" 2>/dev/null || echo "0")
CONN_DIFF=$((BEFORE_CONN - AFTER_CONN))

cat >> "$REPORT" << EOF

NETWORK CONNECTIONS
-------------------
Before Cleanup: $BEFORE_CONN connections
After Cleanup:  $AFTER_CONN connections
Difference:     $CONN_DIFF connections $([ $CONN_DIFF -gt 0 ] && echo "REDUCED ✓" || echo "")

EOF

if [ $CONN_DIFF -gt 0 ]; then
    echo -e "${GREEN}✓ Reduced by $CONN_DIFF connections${NC}"
else
    echo -e "${YELLOW}⚠ No significant change${NC}"
fi

# ============================================================================
# 2. TRACKING DATA
# ============================================================================
echo -e "${BLUE}🔍 Tracking Data...${NC}"

# Machine ID
BEFORE_MACHINE_ID=""
AFTER_MACHINE_ID=""

if [ -f "$BEFORE/tracking/storage.json" ]; then
    BEFORE_MACHINE_ID=$(grep -o '"telemetry.machineId"[^,]*' "$BEFORE/tracking/storage.json" | cut -d'"' -f4)
fi

if [ -f "$AFTER/tracking/storage.json" ]; then
    AFTER_MACHINE_ID=$(grep -o '"telemetry.machineId"[^,]*' "$AFTER/tracking/storage.json" | cut -d'"' -f4)
fi

cat >> "$REPORT" << EOF

TRACKING IDENTIFIERS
--------------------
Machine ID Before: ${BEFORE_MACHINE_ID:-Not found}
Machine ID After:  ${AFTER_MACHINE_ID:-Not found}
Status: $([ "$BEFORE_MACHINE_ID" != "$AFTER_MACHINE_ID" ] && echo "CHANGED ✓" || echo "UNCHANGED")

EOF

if [ "$BEFORE_MACHINE_ID" != "$AFTER_MACHINE_ID" ]; then
    echo -e "${GREEN}✓ Machine ID changed (tracking reset)${NC}"
else
    echo -e "${YELLOW}⚠ Machine ID unchanged${NC}"
fi

# Workspace count
BEFORE_WORKSPACES=$(grep -o '"workspaces"' "$BEFORE/tracking/storage.json" 2>/dev/null | wc -l | tr -d ' ')
AFTER_WORKSPACES=$(grep -o '"workspaces"' "$AFTER/tracking/storage.json" 2>/dev/null | wc -l | tr -d ' ')
WORKSPACE_DIFF=$((BEFORE_WORKSPACES - AFTER_WORKSPACES))

cat >> "$REPORT" << EOF

TRACKED WORKSPACES
------------------
Before Cleanup: $BEFORE_WORKSPACES workspaces
After Cleanup:  $AFTER_WORKSPACES workspaces
Difference:     $WORKSPACE_DIFF workspaces $([ $WORKSPACE_DIFF -gt 0 ] && echo "REDUCED ✓" || echo "")

EOF

if [ $WORKSPACE_DIFF -gt 0 ]; then
    echo -e "${GREEN}✓ Reduced by $WORKSPACE_DIFF tracked workspaces${NC}"
else
    echo -e "${YELLOW}⚠ No change in workspace tracking${NC}"
fi

# ============================================================================
# 3. DATA SIZE
# ============================================================================
echo -e "${BLUE}💾 Data Size...${NC}"

# Extract sizes from summary files
BEFORE_SIZE=$(grep "Total Data Size:" "$BEFORE/BASELINE_SUMMARY.txt" 2>/dev/null | cut -d: -f2 | tr -d ' ')
AFTER_SIZE=$(grep "Total Data Size:" "$AFTER/BASELINE_SUMMARY.txt" 2>/dev/null | cut -d: -f2 | tr -d ' ')

cat >> "$REPORT" << EOF

DATA SIZE
---------
Before Cleanup: $BEFORE_SIZE
After Cleanup:  $AFTER_SIZE

EOF

echo -e "  Before: $BEFORE_SIZE"
echo -e "  After:  $AFTER_SIZE"

# ============================================================================
# 4. PROCESS ANALYSIS
# ============================================================================
echo -e "${BLUE}⚙️  Process Analysis...${NC}"

BEFORE_PROCS=$(wc -l < "$BEFORE/processes/windsurf_processes.txt" 2>/dev/null || echo "0")
AFTER_PROCS=$(wc -l < "$AFTER/processes/windsurf_processes.txt" 2>/dev/null || echo "0")

cat >> "$REPORT" << EOF

PROCESS COUNT
-------------
Before Cleanup: $BEFORE_PROCS processes
After Cleanup:  $AFTER_PROCS processes

EOF

echo -e "  Before: $BEFORE_PROCS processes"
echo -e "  After:  $AFTER_PROCS processes"

# ============================================================================
# 5. FILE DESCRIPTOR ANALYSIS
# ============================================================================
echo -e "${BLUE}📂 File Descriptors...${NC}"

if [ -f "$BEFORE/system/file_descriptors.txt" ] && [ -f "$AFTER/system/file_descriptors.txt" ]; then
    BEFORE_FDS=$(wc -l < "$BEFORE/system/file_descriptors.txt")
    AFTER_FDS=$(wc -l < "$AFTER/system/file_descriptors.txt")
    FD_DIFF=$((BEFORE_FDS - AFTER_FDS))
    
    cat >> "$REPORT" << EOF

FILE DESCRIPTORS
----------------
Before Cleanup: $BEFORE_FDS open files
After Cleanup:  $AFTER_FDS open files
Difference:     $FD_DIFF $([ $FD_DIFF -gt 0 ] && echo "REDUCED ✓" || echo "")

EOF

    if [ $FD_DIFF -gt 0 ]; then
        echo -e "${GREEN}✓ Reduced by $FD_DIFF open files${NC}"
    else
        echo -e "${YELLOW}⚠ No significant change${NC}"
    fi
fi

# ============================================================================
# 6. EFFECTIVENESS SCORE
# ============================================================================
echo ""
echo -e "${CYAN}═══════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}📈 EFFECTIVENESS SCORE${NC}"
echo -e "${CYAN}═══════════════════════════════════════════════════════════${NC}"

SCORE=0
MAX_SCORE=5

# Machine ID changed?
if [ "$BEFORE_MACHINE_ID" != "$AFTER_MACHINE_ID" ] && [ -n "$AFTER_MACHINE_ID" ]; then
    SCORE=$((SCORE + 1))
    echo -e "${GREEN}✓ Machine ID reset${NC}"
else
    echo -e "${RED}✗ Machine ID not reset${NC}"
fi

# Workspaces reduced?
if [ $WORKSPACE_DIFF -gt 0 ]; then
    SCORE=$((SCORE + 1))
    echo -e "${GREEN}✓ Workspace tracking reduced${NC}"
else
    echo -e "${RED}✗ Workspace tracking not reduced${NC}"
fi

# Connections reduced?
if [ $CONN_DIFF -gt 0 ]; then
    SCORE=$((SCORE + 1))
    echo -e "${GREEN}✓ Network connections reduced${NC}"
else
    echo -e "${YELLOW}⚠ Network connections unchanged${NC}"
fi

# File descriptors reduced?
if [ ${FD_DIFF:-0} -gt 0 ]; then
    SCORE=$((SCORE + 1))
    echo -e "${GREEN}✓ Open files reduced${NC}"
else
    echo -e "${YELLOW}⚠ Open files unchanged${NC}"
fi

# Windsurf still functional?
if [ -f "$AFTER/processes/windsurf_processes.txt" ] && [ $AFTER_PROCS -gt 0 ]; then
    SCORE=$((SCORE + 1))
    echo -e "${GREEN}✓ Windsurf still functional${NC}"
else
    echo -e "${RED}✗ Windsurf not running after cleanup${NC}"
fi

PERCENTAGE=$((SCORE * 100 / MAX_SCORE))

cat >> "$REPORT" << EOF

EFFECTIVENESS SCORE
-------------------
Score: $SCORE / $MAX_SCORE ($PERCENTAGE%)

Criteria:
- Machine ID reset: $([ "$BEFORE_MACHINE_ID" != "$AFTER_MACHINE_ID" ] && echo "✓" || echo "✗")
- Workspace tracking reduced: $([ $WORKSPACE_DIFF -gt 0 ] && echo "✓" || echo "✗")
- Network connections reduced: $([ $CONN_DIFF -gt 0 ] && echo "✓" || echo "✗")
- Open files reduced: $([ ${FD_DIFF:-0} -gt 0 ] && echo "✓" || echo "✗")
- Windsurf functional: $([ $AFTER_PROCS -gt 0 ] && echo "✓" || echo "✗")

CONCLUSION
----------
EOF

echo ""
echo -e "${CYAN}═══════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}🎯 OVERALL EFFECTIVENESS: $PERCENTAGE%${NC}"
echo -e "${CYAN}═══════════════════════════════════════════════════════════${NC}"

if [ $PERCENTAGE -ge 80 ]; then
    echo -e "${GREEN}✅ EXCELLENT - Cleanup highly effective${NC}"
    cat >> "$REPORT" << EOF
✅ EXCELLENT - Cleanup highly effective
The cleanup successfully reduced tracking data while maintaining functionality.
EOF
elif [ $PERCENTAGE -ge 60 ]; then
    echo -e "${YELLOW}⚠ GOOD - Cleanup moderately effective${NC}"
    cat >> "$REPORT" << EOF
⚠ GOOD - Cleanup moderately effective
Most tracking data was reduced, but some areas need attention.
EOF
else
    echo -e "${RED}❌ NEEDS IMPROVEMENT - Cleanup less effective${NC}"
    cat >> "$REPORT" << EOF
❌ NEEDS IMPROVEMENT - Cleanup less effective
Consider running cleanup again or checking for issues.
EOF
fi

echo ""
echo -e "${BLUE}📄 Full report saved to:${NC}"
echo -e "  $REPORT"
echo ""
echo -e "${YELLOW}To view full report:${NC}"
echo -e "  cat $REPORT"
echo ""
echo -e "${GREEN}Done!${NC}"
