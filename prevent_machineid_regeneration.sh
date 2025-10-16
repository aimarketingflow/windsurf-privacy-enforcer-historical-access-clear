#!/bin/bash
# Prevent MachineID Regeneration
# This script makes storage.json read-only to prevent Windsurf from regenerating tracking IDs

STORAGE_FILE="$HOME/Library/Application Support/Windsurf/User/globalStorage/storage.json"

echo "=========================================="
echo "PREVENT MACHINEID REGENERATION"
echo "=========================================="
echo ""

if [ ! -f "$STORAGE_FILE" ]; then
    echo "❌ storage.json not found. Run cleanup first."
    exit 1
fi

# Check current machineId
MACHINE_ID=$(cat "$STORAGE_FILE" | python3 -c "import sys, json; print(json.load(sys.stdin).get('telemetry.machineId', 'NOT_FOUND'))")

echo "Current machineId: $MACHINE_ID"
echo ""

if [ "$MACHINE_ID" != "" ] && [ "$MACHINE_ID" != "NOT_FOUND" ]; then
    echo "⚠️  MachineID is present. Clearing it first..."
    
    # Clear the machineId
    python3 << 'EOF'
import json
import os

storage_file = os.path.expanduser("~/Library/Application Support/Windsurf/User/globalStorage/storage.json")

with open(storage_file, 'r') as f:
    data = json.load(f)

# Clear all tracking IDs
data['telemetry.machineId'] = ""
data['telemetry.sqmId'] = ""
data['telemetry.devDeviceId'] = ""

with open(storage_file, 'w') as f:
    json.dump(data, f, indent=4)

print("✅ Tracking IDs cleared")
EOF
fi

echo ""
echo "Making storage.json read-only to prevent regeneration..."

# Make file read-only
chmod 444 "$STORAGE_FILE"

# Verify
if [ ! -w "$STORAGE_FILE" ]; then
    echo "✅ storage.json is now READ-ONLY"
    echo ""
    echo "Windsurf will NOT be able to regenerate tracking IDs!"
    echo ""
    echo "To restore write access:"
    echo "  chmod 644 '$STORAGE_FILE'"
else
    echo "❌ Failed to make file read-only"
    exit 1
fi

echo ""
echo "=========================================="
echo "PROTECTION ENABLED"
echo "=========================================="
echo ""
echo "⚠️  Note: This may cause Windsurf to show errors about"
echo "    being unable to write to storage.json"
echo ""
echo "To disable protection and restore normal operation:"
echo "  chmod 644 '$STORAGE_FILE'"
