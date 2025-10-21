# Windsurf Privacy Toolkit - Terminal Menu Guide

## 🎯 Overview

The **Terminal Menu** provides an interactive command-line interface to access all Windsurf Privacy Toolkit features without needing the GUI.

## 🚀 Quick Start

### Launch the Menu

```bash
./windsurf_privacy_menu.sh
```

## 📋 Menu Options

### 1️⃣ Audit Windsurf Access
**What it does:**
- Scans all Windsurf databases for tracking data
- Identifies workspace associations
- Counts file path references
- Shows privacy score

**Use when:**
- You want to see what data Windsurf has collected
- Before running cleanup to know what will be removed
- Regular privacy checkups

**Output:**
- Detailed report of tracking data
- Privacy score (0-10)
- Recommendations

---

### 2️⃣ Enhanced Cleanup
**What it does:**
- Clears all tracking data and workspace history
- Preserves Python virtual environments (optional)
- Offers backup options
- Shows progress through 10 steps

**Features:**
- ✅ Python venv preservation (NEW!)
- ✅ Multiple backup options
- ✅ Chat history preservation
- ✅ Auth token preservation
- ✅ Interactive prompts

**Prompts:**
1. Quit Windsurf? (y/n)
2. Preserve Python environments? (y/n)
3. Backup option (1-4)
4. Final confirmation (yes/no)

**Backup Options:**
- **1)** No backup (skip)
- **2)** Full backup (all data)
- **3)** Chat history only (recommended)
- **4)** Full + chat export

---

### 3️⃣ Export Chat History ⭐ NEW!
**What it does:**
- Exports all Cascade chat conversations
- Creates multiple formats (JSON, CSV, database)
- Organizes by workspace
- Opens backup folder when done

**Output Files:**
```
WindsurfChatBackup_YYYYMMDD_HHMMSS/
├── MASTER_INDEX.txt
├── workspace_id_1/
│   ├── chat_data.json       # JSON format
│   ├── chat_data.csv         # Excel-compatible
│   ├── state.vscdb.backup    # Full database
│   └── README.txt            # Workspace info
├── workspace_id_2/
│   └── ...
└── workspace_id_3/
    └── ...
```

**How to View:**
1. **CSV files:** Open in Excel, Numbers, or Google Sheets
2. **JSON files:** Open in any text editor
3. **Database:** Use SQLite browser or restore to Windsurf

**Use Cases:**
- 📝 Archive important conversations
- 🔍 Search through old chats
- 💾 Backup before cleanup
- 📊 Analyze chat patterns
- 🔄 Transfer chats to another machine

**No Cleanup Required:**
- This is a **read-only** operation
- Your chats remain in Windsurf
- Safe to run anytime
- No confirmation needed

---

### 4️⃣ Prevent MachineID Regeneration
**What it does:**
- Blocks Windsurf from recreating tracking IDs
- Uses file permissions to prevent writes
- Maintains privacy after cleanup

**How it works:**
1. Clears existing MachineID
2. Creates empty placeholder
3. Sets read-only permissions
4. Prevents regeneration

**Status Check:**
- Shows if protection is active
- Displays current permissions
- Verifies MachineID is empty

---

### 5️⃣ Track Google Cloud Connections
**What it does:**
- Monitors Windsurf's network activity
- Tracks connections to Google Cloud
- Identifies data exfiltration

**Two Methods:**

**Method 1: Connection Tracking (lsof)**
- No sudo required
- Shows active connections
- Real-time monitoring
- Lightweight

**Method 2: Packet Capture (tcpdump)**
- Requires sudo
- Captures actual packets
- Detailed analysis
- Saves to .pcapng file

**Use Cases:**
- Verify what data is being sent
- Monitor during active coding
- Analyze privacy implications
- Document tracking behavior

---

### 6️⃣ Launch GUI Version
**What it does:**
- Launches the full graphical interface
- Runs in background
- All features available

**GUI Features:**
- 🏠 Dashboard - System overview
- 🔍 Audit - Detailed scanning
- 🧹 Cleanup - Visual cleanup with progress
- 💾 Backups - Chat history management
- 🌐 Network Monitor - Real-time connections

---

### 7️⃣ Show Documentation
**What it does:**
- Lists all available documentation
- Opens docs in terminal viewer (less)
- Easy navigation

**Available Docs:**
1. Main README
2. GUI User Guide
3. Virtual Environment Preservation
4. Google Cloud Tracking
5. Historical Access Deletion
6. Desktop Launcher Guide

**Navigation:**
- Arrow keys to scroll
- `/` to search
- `q` to quit
- Space for next page

---

### 0️⃣ Exit
Closes the menu and returns to terminal.

---

## 💡 Usage Examples

### Example 1: First Time Setup

```bash
./windsurf_privacy_menu.sh

# Select: 1 (Audit)
# Review what data exists

# Select: 3 (Export Chats)
# Backup conversations

# Select: 2 (Cleanup)
# Choose: Preserve venvs (y)
# Choose: Chat backup (3)
# Confirm: yes

# Select: 4 (Prevent MachineID)
# Block tracking ID regeneration
```

### Example 2: Regular Maintenance

```bash
./windsurf_privacy_menu.sh

# Select: 1 (Audit)
# Check current status

# Select: 2 (Cleanup)
# Quick cleanup with venv preservation
```

### Example 3: Export Chats Only

```bash
./windsurf_privacy_menu.sh

# Select: 3 (Export Chats)
# Backup opens automatically
# View CSV files in Excel
```

### Example 4: Monitor Network Activity

```bash
./windsurf_privacy_menu.sh

# Select: 5 (Track Connections)
# Choose: 1 (Connection tracking)
# Watch real-time connections
```

## 🎨 Menu Features

### Visual Design
- ✅ Color-coded options
- ✅ Clear descriptions
- ✅ Emoji icons for easy recognition
- ✅ Organized layout

### User Experience
- ✅ Interactive prompts
- ✅ Error handling
- ✅ Progress indicators
- ✅ Confirmation dialogs
- ✅ "Press Enter to continue" pauses

### Navigation
- ✅ Number-based selection
- ✅ Back to menu after each action
- ✅ Clear screen between operations
- ✅ Exit anytime with 0

## 🔧 Technical Details

### Requirements
- Bash shell
- macOS (tested on macOS 14+)
- Python 3 (for GUI launch)
- SQLite3 (for chat export)

### File Locations
- Menu script: `windsurf_privacy_menu.sh`
- Chat export: `backup_windsurf_chat.sh`
- Cleanup: `clear_windsurf_tracking_ENHANCED.sh`
- Audit: `audit_windsurf_access.sh`
- GUI: `windsurf_privacy_gui.py`

### Permissions
All scripts are executable:
```bash
chmod +x *.sh
```

## 🆕 What's New in v2.1

### Chat Export Feature
- ✅ Standalone menu option (Option 3)
- ✅ No cleanup required
- ✅ Multiple export formats
- ✅ Automatic folder opening
- ✅ Workspace organization

### Enhanced Cleanup
- ✅ Python venv preservation prompt
- ✅ Improved backup options
- ✅ Better progress tracking

### Menu Improvements
- ✅ Better organization
- ✅ Clearer descriptions
- ✅ Color-coded interface
- ✅ Documentation viewer

## 📊 Comparison: Terminal vs GUI

| Feature | Terminal Menu | GUI |
|---------|--------------|-----|
| **Audit** | ✅ Full report | ✅ Visual dashboard |
| **Cleanup** | ✅ Interactive | ✅ Progress bar |
| **Chat Export** | ✅ Standalone | ✅ Integrated |
| **Network Monitor** | ✅ Scripts | ✅ Real-time tabs |
| **Documentation** | ✅ Built-in viewer | ❌ External |
| **Resource Usage** | 🟢 Lightweight | 🟡 Moderate |
| **Remote Access** | ✅ SSH-friendly | ❌ Requires display |
| **Automation** | ✅ Scriptable | ❌ Manual |

### When to Use Terminal Menu
- ✅ SSH/remote access
- ✅ Scripting/automation
- ✅ Minimal resource usage
- ✅ Quick operations
- ✅ Server environments

### When to Use GUI
- ✅ Visual preference
- ✅ Real-time monitoring
- ✅ Multiple operations
- ✅ Dashboard overview
- ✅ Desktop environment

## 🎯 Tips & Tricks

### Tip 1: Regular Exports
Export chats weekly to maintain archive:
```bash
# Add to crontab for weekly export
0 0 * * 0 /path/to/windsurf_privacy_menu.sh <<< "3"
```

### Tip 2: Quick Audit
Check privacy status quickly:
```bash
./windsurf_privacy_menu.sh <<< "1"
```

### Tip 3: Automated Cleanup
Run cleanup with defaults:
```bash
echo -e "y\ny\n3\nyes" | ./clear_windsurf_tracking_ENHANCED.sh
```

### Tip 4: Export Before Cleanup
Always export chats before major cleanup:
```bash
./windsurf_privacy_menu.sh
# Option 3 first, then Option 2
```

## 🐛 Troubleshooting

### Menu Won't Launch
```bash
# Make executable
chmod +x windsurf_privacy_menu.sh

# Run directly
bash windsurf_privacy_menu.sh
```

### Chat Export Fails
```bash
# Check SQLite
which sqlite3

# Check workspace storage
ls ~/Library/Application\ Support/Windsurf/User/workspaceStorage/
```

### Scripts Not Found
```bash
# Run from correct directory
cd /path/to/WindsurfExploit-Oct25
./windsurf_privacy_menu.sh
```

## 📝 Version History

### v2.1 (October 20, 2025)
- ✅ Added standalone chat export option
- ✅ Created interactive terminal menu
- ✅ Integrated all toolkit features
- ✅ Added documentation viewer

### v2.0 (October 16, 2025)
- Network monitoring features
- Enhanced cleanup with venv preservation
- GUI improvements

## 🔗 Related Documentation

- [Main README](./README.md)
- [GUI User Guide](./GUI_README.md)
- [Chat Export Script](./backup_windsurf_chat.sh)
- [Enhanced Cleanup](./clear_windsurf_tracking_ENHANCED.sh)
- [Venv Preservation](./VENV_PRESERVATION_FEATURE.md)

---

**Status:** ✅ Complete and ready to use  
**Version:** 2.1  
**Last Updated:** October 20, 2025

**Quick Start:**
```bash
./windsurf_privacy_menu.sh
```

Enjoy the new terminal menu! 🎉
