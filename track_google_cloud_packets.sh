#!/bin/bash
# Deep Packet Analysis for Google Cloud Traffic
# Captures actual packet data to/from Google Cloud servers

OUTPUT_DIR="$HOME/windsurf_cloud_tracking"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
PCAP_FILE="$OUTPUT_DIR/cloud_packets_${TIMESTAMP}.pcap"
ANALYSIS_FILE="$OUTPUT_DIR/cloud_analysis_${TIMESTAMP}.txt"

mkdir -p "$OUTPUT_DIR"

echo "=========================================="
echo "GOOGLE CLOUD PACKET TRACKER"
echo "=========================================="
echo ""
echo "This will capture ACTUAL PACKETS to/from Google Cloud"
echo ""
echo "⚠️  WARNING: Requires sudo/admin privileges"
echo "⚠️  This captures network traffic - may contain sensitive data"
echo ""
echo "Output files:"
echo "  PCAP: $PCAP_FILE"
echo "  Analysis: $ANALYSIS_FILE"
echo ""
read -p "Continue? (yes/no): " CONFIRM

if [ "$CONFIRM" != "yes" ]; then
    echo "Cancelled."
    exit 0
fi

echo ""
echo "Starting packet capture..."
echo "Press Ctrl+C to stop"
echo ""

# Create analysis header
{
    echo "=== GOOGLE CLOUD PACKET ANALYSIS ==="
    echo "Date: $(date)"
    echo "Host: $(hostname)"
    echo ""
    echo "Target IPs:"
    echo "  - 34.49.14.144 (Google Cloud)"
    echo "  - 178.238.223.35 (Google Cloud)"
    echo ""
    echo "=== LIVE CAPTURE ==="
    echo ""
} > "$ANALYSIS_FILE"

# Start tcpdump in background
echo "Starting tcpdump (requires sudo)..."
sudo tcpdump -i any -n \
    "host 34.49.14.144 or host 178.238.223.35" \
    -w "$PCAP_FILE" \
    -v 2>&1 | tee -a "$ANALYSIS_FILE" &

TCPDUMP_PID=$!

# Monitor connections while capturing
{
    sleep 2
    echo ""
    echo "=== CONNECTION MONITORING ==="
    echo ""
    
    COUNTER=0
    while kill -0 $TCPDUMP_PID 2>/dev/null; do
        COUNTER=$((COUNTER + 1))
        echo "--- Sample #$COUNTER at $(date "+%H:%M:%S") ---"
        
        # Show active connections
        netstat -an | grep -E "(34.49.14.144|178.238.223.35)" | head -20
        
        # Show packet count
        if [ -f "$PCAP_FILE" ]; then
            SIZE=$(ls -lh "$PCAP_FILE" | awk '{print $5}')
            echo "Captured data: $SIZE"
        fi
        
        echo ""
        sleep 5
    done
} | tee -a "$ANALYSIS_FILE"

echo ""
echo "=========================================="
echo "CAPTURE COMPLETE"
echo "=========================================="
echo ""
echo "Files saved:"
echo "  PCAP: $PCAP_FILE"
echo "  Analysis: $ANALYSIS_FILE"
echo ""
echo "To analyze the PCAP file:"
echo "  tcpdump -r $PCAP_FILE -A"
echo "  tcpdump -r $PCAP_FILE -X (hex dump)"
echo "  wireshark $PCAP_FILE (GUI analysis)"
echo ""
