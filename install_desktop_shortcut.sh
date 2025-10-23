#!/bin/bash

# Windsurf Privacy Toolkit - Desktop Shortcut Installer
# Handles permission checks and graceful fallbacks

echo "🛡️  Windsurf Privacy Toolkit - Desktop Shortcut Installer"
echo "=========================================================="
echo ""

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
DESKTOP="$HOME/Desktop"

# Test Desktop access
echo "Checking Desktop access..."
if touch "$DESKTOP/.windsurf_test" 2>/dev/null; then
    rm "$DESKTOP/.windsurf_test"
    echo "✅ Desktop access: GRANTED"
    echo ""
else
    echo "❌ Desktop access: DENIED"
    echo ""
    echo "⚠️  macOS has restricted access to Desktop folder."
    echo ""
    echo "To grant access:"
    echo "  1. Open System Settings"
    echo "  2. Go to Privacy & Security → Files and Folders"
    echo "  3. Find Terminal (or your terminal app)"
    echo "  4. Enable 'Desktop Folder' access"
    echo ""
    echo "Alternative: I can create the shortcut in Documents instead."
    echo ""
    read -p "Create shortcut in Documents folder? (y/n): " choice
    
    if [[ "$choice" =~ ^[Yy]$ ]]; then
        DESKTOP="$HOME/Documents"
        echo "✅ Using Documents folder instead"
    else
        echo "❌ Installation cancelled"
        exit 1
    fi
fi

# Create launcher script if it doesn't exist
LAUNCHER="$SCRIPT_DIR/launch_windsurf_toolkit.command"
if [ ! -f "$LAUNCHER" ]; then
    echo "Creating launcher script..."
    cat > "$LAUNCHER" << 'LAUNCHER_SCRIPT'
#!/bin/bash

# Windsurf Privacy Toolkit Launcher
# Auto-finds toolkit location

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Navigate to script directory
cd "$SCRIPT_DIR"

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    osascript -e 'display dialog "Python 3 is required but not found. Please install Python 3." buttons {"OK"} default button "OK" with icon stop'
    exit 1
fi

# Check if GUI file exists
if [ ! -f "windsurf_privacy_gui.py" ]; then
    osascript -e 'display dialog "windsurf_privacy_gui.py not found in this directory!" buttons {"OK"} default button "OK" with icon stop'
    exit 1
fi

# Launch the GUI
python3 windsurf_privacy_gui.py

# If GUI exits with error, show message
if [ $? -ne 0 ]; then
    osascript -e 'display dialog "Error launching Windsurf Privacy Toolkit. Check terminal for details." buttons {"OK"} default button "OK" with icon caution'
fi
LAUNCHER_SCRIPT

    chmod +x "$LAUNCHER"
    echo "✅ Launcher script created"
fi

# Create app bundle
APP_NAME="Windsurf Privacy Toolkit"
APP_PATH="$DESKTOP/${APP_NAME}.app"

echo ""
echo "Creating app bundle..."

# Create app structure
mkdir -p "${APP_PATH}/Contents/MacOS"
mkdir -p "${APP_PATH}/Contents/Resources"

# Create Info.plist
cat > "${APP_PATH}/Contents/Info.plist" << 'PLIST'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleExecutable</key>
    <string>launcher</string>
    <key>CFBundleIconFile</key>
    <string>AppIcon</string>
    <key>CFBundleIdentifier</key>
    <string>com.windsurf.privacy.toolkit</string>
    <key>CFBundleName</key>
    <string>Windsurf Privacy Toolkit</string>
    <key>CFBundlePackageType</key>
    <string>APPL</string>
    <key>CFBundleShortVersionString</key>
    <string>2.0</string>
    <key>LSMinimumSystemVersion</key>
    <string>10.13</string>
</dict>
</plist>
PLIST

# Create launcher that finds toolkit automatically
cat > "${APP_PATH}/Contents/MacOS/launcher" << LAUNCHER_APP
#!/bin/bash
# Auto-finding launcher

# Try current known location first
TOOLKIT_DIR="$SCRIPT_DIR"

# If not found, search for it
if [ ! -f "\$TOOLKIT_DIR/windsurf_privacy_gui.py" ]; then
    echo "Searching for Windsurf Privacy Toolkit..."
    
    SEARCH_PATHS=(
        "$HOME/Documents"
        "$HOME/Desktop"
        "$HOME/Downloads"
        "$HOME"
    )
    
    for base_dir in "\${SEARCH_PATHS[@]}"; do
        found=\$(find "\$base_dir" -maxdepth 3 -name "windsurf_privacy_gui.py" -type f 2>/dev/null | head -1)
        if [ -n "\$found" ]; then
            TOOLKIT_DIR=\$(dirname "\$found")
            echo "Found toolkit at: \$TOOLKIT_DIR"
            break
        fi
    done
fi

# Launch if found
if [ -f "\$TOOLKIT_DIR/windsurf_privacy_gui.py" ]; then
    cd "\$TOOLKIT_DIR"
    
    if ! command -v python3 &> /dev/null; then
        osascript -e 'display dialog "Python 3 is required. Install from python.org" buttons {"OK"} default button "OK" with icon stop'
        exit 1
    fi
    
    python3 windsurf_privacy_gui.py
    
    if [ \$? -ne 0 ]; then
        osascript -e 'display dialog "Error launching toolkit. Check that all files are present." buttons {"OK"} default button "OK" with icon caution'
    fi
else
    osascript -e 'display dialog "Could not find Windsurf Privacy Toolkit!\n\nSearched in:\n• Documents\n• Desktop\n• Downloads\n\nPlease ensure windsurf_privacy_gui.py exists." buttons {"OK"} default button "OK" with icon stop'
fi
LAUNCHER_APP

chmod +x "${APP_PATH}/Contents/MacOS/launcher"

echo "✅ App bundle created"
echo ""
echo "=========================================================="
echo "✅ Installation Complete!"
echo "=========================================================="
echo ""
echo "Location: $APP_PATH"
echo ""
echo "Features:"
echo "  • Works even if you move the toolkit folder"
echo "  • Auto-searches common locations"
echo "  • Double-click to launch"
echo ""
echo "You can now close this terminal and use the app!"
