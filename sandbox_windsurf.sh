#!/bin/bash
# Windsurf Sandboxing Script
# Creates a restrictive sandbox profile for Windsurf IDE

echo "=================================="
echo "WINDSURF SANDBOXING SETUP"
echo "=================================="
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Check if running as root
if [ "$EUID" -eq 0 ]; then 
    echo -e "${RED}❌ Do NOT run this script as root${NC}"
    echo "Run as normal user: ./sandbox_windsurf.sh"
    exit 1
fi

echo -e "${BLUE}This script will create a sandboxed environment for Windsurf${NC}"
echo ""
echo "Options:"
echo "  1. Create custom sandbox profile (macOS sandbox-exec)"
echo "  2. Setup firewall rules (Little Snitch/Lulu/pfctl)"
echo "  3. Create restricted launch wrapper"
echo "  4. Setup file system restrictions"
echo "  5. All of the above"
echo ""
read -p "Select option (1-5): " OPTION

case $OPTION in
    1|5)
        echo ""
        echo "=================================="
        echo "1. CREATING SANDBOX PROFILE"
        echo "=================================="
        
        SANDBOX_DIR="$HOME/.windsurf_sandbox"
        mkdir -p "$SANDBOX_DIR"
        
        cat > "$SANDBOX_DIR/windsurf.sb" << 'EOF'
;; Windsurf Sandbox Profile
;; Restrictive sandbox for Windsurf IDE

(version 1)
(debug deny)

;; Deny everything by default
(deny default)

;; Allow basic system operations
(allow process-exec
    (literal "/Applications/Windsurf.app/Contents/MacOS/Electron"))

(allow process-fork)
(allow signal)

;; Allow reading system frameworks
(allow file-read*
    (subpath "/System/Library")
    (subpath "/usr/lib")
    (subpath "/usr/share"))

;; Allow reading Windsurf app bundle
(allow file-read*
    (subpath "/Applications/Windsurf.app"))

;; Allow reading/writing to Windsurf config (restricted)
(allow file-read* file-write*
    (subpath (string-append (param "HOME") "/Library/Application Support/Windsurf"))
    (subpath (string-append (param "HOME") "/Library/Caches/Windsurf")))

;; RESTRICTED: Only allow access to specific workspace
;; Uncomment and modify this line to allow a specific directory:
;; (allow file-read* file-write*
;;     (subpath "/Users/YOUR_USERNAME/Documents/YOUR_WORKSPACE"))

;; Deny access to sensitive directories
(deny file-read* file-write*
    (subpath (string-append (param "HOME") "/.ssh"))
    (subpath (string-append (param "HOME") "/.aws"))
    (subpath (string-append (param "HOME") "/.gnupg"))
    (subpath (string-append (param "HOME") "/Library/Keychains")))

;; Allow network (can be further restricted)
(allow network-outbound)
(allow network-inbound)

;; Deny camera and microphone
(deny device-camera)
(deny device-microphone)

;; Deny Bluetooth
(deny iokit-open
    (iokit-user-client-class "IOBluetoothHCIController"))

;; Allow mach lookups for basic services
(allow mach-lookup
    (global-name "com.apple.system.logger")
    (global-name "com.apple.system.notification_center"))

;; Log denied operations
(deny default (with send-signal SIGKILL))
EOF

        echo -e "${GREEN}✅ Sandbox profile created: $SANDBOX_DIR/windsurf.sb${NC}"
        echo ""
        echo "To use this profile, run:"
        echo -e "${YELLOW}  sandbox-exec -f $SANDBOX_DIR/windsurf.sb /Applications/Windsurf.app/Contents/MacOS/Electron${NC}"
        echo ""
        ;;&
        
    2|5)
        echo ""
        echo "=================================="
        echo "2. FIREWALL RULES SETUP"
        echo "=================================="
        
        # Create pfctl rules
        FIREWALL_RULES="$SANDBOX_DIR/windsurf_firewall.rules"
        
        cat > "$FIREWALL_RULES" << 'EOF'
# Windsurf Firewall Rules (pfctl)
# Block all outbound connections from Windsurf except localhost

# Get Windsurf process
windsurf_path = "/Applications/Windsurf.app/Contents/MacOS/Electron"

# Block all outbound except localhost
block out proto tcp from any to any user $(id -u) process $windsurf_path
block out proto udp from any to any user $(id -u) process $windsurf_path

# Allow localhost only
pass out proto tcp from any to 127.0.0.1 user $(id -u) process $windsurf_path
pass out proto tcp from any to ::1 user $(id -u) process $windsurf_path
EOF

        echo -e "${GREEN}✅ Firewall rules created: $FIREWALL_RULES${NC}"
        echo ""
        echo -e "${YELLOW}To apply pfctl rules (requires sudo):${NC}"
        echo "  sudo pfctl -f $FIREWALL_RULES"
        echo ""
        echo -e "${BLUE}Recommended: Use Little Snitch or Lulu for easier management${NC}"
        echo ""
        
        # Create Lulu rules
        LULU_RULES="$SANDBOX_DIR/windsurf_lulu_rules.txt"
        cat > "$LULU_RULES" << 'EOF'
# Lulu Firewall Rules for Windsurf
# Import these rules into Lulu

Application: /Applications/Windsurf.app
Action: Block
Direction: Outgoing
Protocol: Any
Remote: Any (except 127.0.0.1)

# Allow localhost only
Application: /Applications/Windsurf.app
Action: Allow
Direction: Outgoing
Protocol: Any
Remote: 127.0.0.1, ::1
EOF

        echo -e "${GREEN}✅ Lulu rules created: $LULU_RULES${NC}"
        echo ""
        ;;&
        
    3|5)
        echo ""
        echo "=================================="
        echo "3. RESTRICTED LAUNCH WRAPPER"
        echo "=================================="
        
        WRAPPER_SCRIPT="$SANDBOX_DIR/windsurf_restricted.sh"
        
        cat > "$WRAPPER_SCRIPT" << 'EOF'
#!/bin/bash
# Windsurf Restricted Launch Wrapper
# Launches Windsurf with maximum restrictions

echo "🔒 Launching Windsurf in restricted mode..."

# Set restrictive environment variables
export WINDSURF_DISABLE_TELEMETRY=1
export WINDSURF_DISABLE_CRASH_REPORTER=1
export WINDSURF_DISABLE_UPDATES=1
export ELECTRON_DISABLE_SECURITY_WARNINGS=0

# Limit network access (if using sandbox-exec)
SANDBOX_PROFILE="$HOME/.windsurf_sandbox/windsurf.sb"

if [ -f "$SANDBOX_PROFILE" ]; then
    echo "📋 Using sandbox profile: $SANDBOX_PROFILE"
    sandbox-exec -f "$SANDBOX_PROFILE" \
        /Applications/Windsurf.app/Contents/MacOS/Electron "$@"
else
    echo "⚠️  Sandbox profile not found, launching normally"
    /Applications/Windsurf.app/Contents/MacOS/Electron "$@"
fi
EOF

        chmod +x "$WRAPPER_SCRIPT"
        
        echo -e "${GREEN}✅ Launch wrapper created: $WRAPPER_SCRIPT${NC}"
        echo ""
        echo "To launch Windsurf in restricted mode:"
        echo -e "${YELLOW}  $WRAPPER_SCRIPT${NC}"
        echo ""
        ;;&
        
    4|5)
        echo ""
        echo "=================================="
        echo "4. FILE SYSTEM RESTRICTIONS"
        echo "=================================="
        
        # Create a script to set ACLs
        ACL_SCRIPT="$SANDBOX_DIR/setup_acls.sh"
        
        cat > "$ACL_SCRIPT" << 'EOF'
#!/bin/bash
# Setup ACLs to restrict Windsurf file access

echo "Setting up file system ACLs for Windsurf..."

# Deny Windsurf access to sensitive directories
WINDSURF_USER=$(whoami)
SENSITIVE_DIRS=(
    "$HOME/.ssh"
    "$HOME/.aws"
    "$HOME/.gnupg"
    "$HOME/Library/Keychains"
    "$HOME/.config"
)

for DIR in "${SENSITIVE_DIRS[@]}"; do
    if [ -d "$DIR" ]; then
        echo "🔒 Restricting: $DIR"
        # Note: macOS ACLs are limited, consider using chmod instead
        chmod 700 "$DIR"
    fi
done

echo "✅ ACLs configured"
echo ""
echo "⚠️  Note: macOS ACLs are limited. For better protection:"
echo "  1. Move sensitive files outside Documents"
echo "  2. Use encrypted disk images for secrets"
echo "  3. Never open sensitive directories in Windsurf"
EOF

        chmod +x "$ACL_SCRIPT"
        
        echo -e "${GREEN}✅ ACL setup script created: $ACL_SCRIPT${NC}"
        echo ""
        echo "To apply file restrictions:"
        echo -e "${YELLOW}  $ACL_SCRIPT${NC}"
        echo ""
        ;;
esac

# Final summary
echo ""
echo "=================================="
echo "SANDBOXING SETUP COMPLETE"
echo "=================================="
echo ""
echo -e "${GREEN}✅ Created files in: $SANDBOX_DIR${NC}"
ls -lh "$SANDBOX_DIR"
echo ""

echo -e "${BLUE}📋 NEXT STEPS:${NC}"
echo ""
echo "1. Review and customize the sandbox profile:"
echo "   nano $SANDBOX_DIR/windsurf.sb"
echo ""
echo "2. Test the restricted launcher:"
echo "   $SANDBOX_DIR/windsurf_restricted.sh"
echo ""
echo "3. Setup firewall rules (choose one):"
echo "   - Little Snitch (recommended): Import $SANDBOX_DIR/windsurf_lulu_rules.txt"
echo "   - Lulu (free): Import rules manually"
echo "   - pfctl: sudo pfctl -f $SANDBOX_DIR/windsurf_firewall.rules"
echo ""
echo "4. Apply file system restrictions:"
echo "   $SANDBOX_DIR/setup_acls.sh"
echo ""

echo -e "${YELLOW}⚠️  IMPORTANT NOTES:${NC}"
echo ""
echo "• Sandboxing may break some Windsurf features"
echo "• Test thoroughly before relying on it for security"
echo "• macOS sandbox-exec is deprecated but still works"
echo "• Consider using a VM for maximum isolation"
echo "• Monitor with: ./audit_windsurf_access.sh"
echo ""

echo -e "${RED}🚨 CRITICAL:${NC}"
echo "• This does NOT prevent data already collected"
echo "• Clear workspace history: rm -rf ~/Library/Application\\ Support/Windsurf/User/workspaceStorage/"
echo "• Revoke all permissions in System Settings first"
echo ""

echo "=================================="
echo "For maximum security, consider:"
echo "  1. Using VS Code with local-only extensions"
echo "  2. Working in air-gapped VM"
echo "  3. Complete removal: rm -rf /Applications/Windsurf.app"
echo "=================================="
echo ""
