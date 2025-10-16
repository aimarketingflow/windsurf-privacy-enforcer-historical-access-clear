#!/bin/bash
# Track Google Cloud Connections in High Detail
# Monitors all traffic to Google Cloud servers from Windsurf

OUTPUT_DIR="$HOME/windsurf_cloud_tracking"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
LOG_FILE="$OUTPUT_DIR/cloud_tracking_${TIMESTAMP}.log"

mkdir -p "$OUTPUT_DIR"

echo "=========================================="
echo "GOOGLE CLOUD CONNECTION TRACKER"
echo "=========================================="
echo ""
echo "Tracking Windsurf → Google Cloud connections"
echo "Output: $LOG_FILE"
echo ""
echo "Press Ctrl+C to stop tracking"
echo ""
echo "=========================================="
echo ""

# Start logging
{
    echo "=== TRACKING SESSION START ==="
    echo "Date: $(date)"
    echo "Host: $(hostname)"
    echo ""
    
    # Initial snapshot
    echo "=== INITIAL CONNECTION SNAPSHOT ==="
    echo ""
    lsof -i -n -P | grep -E "(Windsurf|language_server)" | grep -E "(34.49.14.144|178.238.223.35|googleusercontent.com)"
    echo ""
    
    # Continuous monitoring
    echo "=== CONTINUOUS MONITORING (10 second intervals) ==="
    echo ""
    
    COUNTER=0
    while true; do
        COUNTER=$((COUNTER + 1))
        CURRENT_TIME=$(date "+%Y-%m-%d %H:%M:%S")
        
        echo "--- Sample #$COUNTER at $CURRENT_TIME ---"
        
        # Get all Google Cloud connections
        CONNECTIONS=$(lsof -i -n -P 2>/dev/null | grep -E "(Windsurf|language_server)" | grep -E "(34.49.14.144|178.238.223.35|googleusercontent.com)")
        
        if [ -n "$CONNECTIONS" ]; then
            echo "$CONNECTIONS"
            
            # Count connections
            CONN_COUNT=$(echo "$CONNECTIONS" | wc -l | tr -d ' ')
            echo ""
            echo "Active Google Cloud connections: $CONN_COUNT"
            
            # Extract unique IPs
            echo "Unique destination IPs:"
            echo "$CONNECTIONS" | awk '{print $9}' | grep -oE '[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+' | sort -u
            
            # Extract PIDs
            echo ""
            echo "Process IDs involved:"
            echo "$CONNECTIONS" | awk '{print $2}' | sort -u
            
            # Get process details
            echo ""
            echo "Process details:"
            for PID in $(echo "$CONNECTIONS" | awk '{print $2}' | sort -u); do
                ps -p $PID -o pid,comm,args 2>/dev/null | tail -n +2
            done
            
        else
            echo "No active Google Cloud connections detected"
        fi
        
        echo ""
        echo "---"
        echo ""
        
        sleep 10
    done
    
} | tee "$LOG_FILE"
