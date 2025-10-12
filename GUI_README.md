# Windsurf Privacy Toolkit - GUI Application

**Modern PyQt6 interface for complete privacy protection and historical access deletion**

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Python](https://img.shields.io/badge/python-3.8+-green)
![PyQt6](https://img.shields.io/badge/PyQt6-6.6.1-orange)
![Platform](https://img.shields.io/badge/platform-macOS-lightgrey)

---

## 🎨 Features

### 📊 Dashboard
- Real-time Windsurf status monitoring
- Tracking status overview
- Chat history backup status
- Last cleanup timestamp
- Quick action buttons

### 🔍 Security Audit
- Comprehensive 10-point security assessment
- Real-time output display
- Progress tracking
- Save reports to file
- Dark terminal-style interface

### 🧹 Enhanced Cleanup
- 4 backup options:
  1. No backup (skip)
  2. Full backup (all Windsurf data)
  3. Chat history only (recommended)
  4. Full backup + separate chat export
- Real-time progress tracking
- Step-by-step output display
- Confirmation dialogs
- Success notifications

### 💾 Chat History Backup
- Export to CSV (Excel-compatible)
- Export to JSON (programmatic access)
- Full database backups
- Automatic workspace detection
- Open backup folder directly
- Timestamped backups

---

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- macOS 14+ (Sonoma, Sequoia)
- Windsurf IDE installed

### Step 1: Install Python Dependencies
```bash
# Using pip
pip install -r requirements.txt

# Or using pip3
pip3 install -r requirements.txt
```

### Step 2: Make Scripts Executable
```bash
chmod +x audit_windsurf_access.sh
chmod +x clear_windsurf_tracking_ENHANCED.sh
chmod +x backup_windsurf_chat.sh
chmod +x test_historical_access_deletion.sh
chmod +x verify_cleanup.sh
```

### Step 3: Run the GUI
```bash
python3 windsurf_privacy_gui.py
```

---

## 🚀 Quick Start

### Launch the Application
```bash
# From the toolkit directory
python3 windsurf_privacy_gui.py
```

### First Time Setup
1. **Dashboard** - Check your current status
2. **Audit** - Run a security audit to see what's being tracked
3. **Chat Backup** - Backup your chat history (recommended)
4. **Cleanup** - Run enhanced cleanup with backup option 3
5. **Dashboard** - Verify status has changed

---

## 📖 User Guide

### Dashboard Tab

**Status Cards:**
- **Windsurf Status** - Shows if Windsurf is running
- **Tracking Status** - Shows if tracking IDs are active
- **Chat History** - Shows last backup timestamp
- **Last Cleanup** - Shows when cleanup was last run

**Quick Actions:**
- **Run Security Audit** - Opens audit tab and starts scan
- **Backup Chat History** - Opens backup tab and starts backup
- **Enhanced Cleanup** - Opens cleanup tab
- **Run Tests** - Runs comprehensive test suite

### Audit Tab

**Features:**
- Real-time output display
- Terminal-style dark interface
- Progress indicator
- Stop button for long-running audits
- Save report to file

**Usage:**
1. Click "▶️ Run Audit"
2. Watch real-time output
3. Wait for completion
4. Click "💾 Save Report" to save results

### Cleanup Tab

**Backup Options:**
1. **No backup** - Skip backup (not recommended)
2. **Full backup** - Backs up entire Windsurf directory (~200MB)
3. **Chat history only** - Backs up just chat data (recommended, ~1MB)
4. **Full + chat export** - Both full backup and readable chat export

**Usage:**
1. Select backup option (recommend option 3)
2. Click "🧹 Run Cleanup"
3. Confirm in dialog
4. Watch progress (10 steps)
5. Wait for completion notification

**What Gets Cleared:**
- ✅ Machine/Device tracking IDs
- ✅ ALL 16+ workspace associations
- ✅ Backup workspace history
- ✅ Recent file history
- ✅ 26.2 MB tracking data

**What Gets Preserved:**
- ✅ User settings
- ✅ Extensions
- ✅ Keybindings
- ✅ Chat history with Cascade
- ✅ GitHub/Windsurf authentication

### Chat Backup Tab

**Features:**
- Exports all chat histories
- Creates CSV files (Excel-compatible)
- Creates JSON files (programmatic)
- Full database backups
- Opens backup folder automatically

**Usage:**
1. Click "💾 Backup Chat History"
2. Wait for completion
3. Click "📂 Open Backup Folder" to view

**Output Location:**
```
~/WindsurfChatBackup_YYYYMMDD_HHMMSS/
├── README.txt
├── workspace_1/
│   ├── chat_data.csv
│   ├── chat_data.json
│   └── state.vscdb.backup
├── workspace_2/
│   ├── chat_data.csv
│   ├── chat_data.json
│   └── state.vscdb.backup
...
```

---

## 🎨 Screenshots

### Dashboard
```
┌─────────────────────────────────────────────────────┐
│  Windsurf Privacy Toolkit                          │
│  Complete Privacy Protection & Historical Access    │
│                                                     │
│  ┌──────────────┐  ┌──────────────┐               │
│  │ Windsurf     │  │ Tracking     │               │
│  │ Status       │  │ Status       │               │
│  │ Running      │  │ Cleared      │               │
│  └──────────────┘  └──────────────┘               │
│                                                     │
│  ┌──────────────┐  ┌──────────────┐               │
│  │ Chat History │  │ Last Cleanup │               │
│  │ Last: 9:35PM │  │ Today 9:32PM │               │
│  └──────────────┘  └──────────────┘               │
│                                                     │
│  Quick Actions                                      │
│  ┌─────────────────────────────────────────────┐  │
│  │ 🔍 Run Security Audit                       │  │
│  │ 💾 Backup Chat History                      │  │
│  │ 🧹 Enhanced Cleanup                         │  │
│  │ 🧪 Run Tests                                │  │
│  └─────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────┘
```

---

## 🛠️ Technical Details

### Architecture
- **Frontend**: PyQt6 (modern Qt6 bindings)
- **Backend**: Shell scripts (bash)
- **Threading**: QThread for non-blocking operations
- **IPC**: subprocess for script execution

### File Structure
```
windsurf-privacy-toolkit/
├── windsurf_privacy_gui.py          # Main GUI application
├── requirements.txt                  # Python dependencies
├── GUI_README.md                     # This file
├── audit_windsurf_access.sh         # Audit script
├── clear_windsurf_tracking_ENHANCED.sh  # Cleanup script
├── backup_windsurf_chat.sh          # Backup script
├── test_historical_access_deletion.sh   # Test script
└── verify_cleanup.sh                # Verification script
```

### Classes
- **MainWindow** - Main application window with tabs
- **DashboardWidget** - Status overview and quick actions
- **AuditWidget** - Security audit interface
- **CleanupWidget** - Enhanced cleanup interface
- **ChatBackupWidget** - Chat backup interface
- **WorkerThread** - Background thread for script execution

---

## 🔧 Troubleshooting

### GUI Won't Start
```bash
# Check Python version
python3 --version  # Should be 3.8+

# Reinstall dependencies
pip3 install --upgrade -r requirements.txt

# Check PyQt6 installation
python3 -c "from PyQt6.QtWidgets import QApplication"
```

### Scripts Not Found
```bash
# Ensure you're in the correct directory
pwd
# Should show: .../WindsurfExploit-Oct25

# Make scripts executable
chmod +x *.sh
```

### Permission Denied
```bash
# Scripts need execute permission
chmod +x audit_windsurf_access.sh
chmod +x clear_windsurf_tracking_ENHANCED.sh
chmod +x backup_windsurf_chat.sh
```

### Dark Theme Not Applied
- Restart the application
- Check if your OS has dark mode enabled
- Try running with: `python3 windsurf_privacy_gui.py --style Fusion`

---

## 🎯 Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Cmd+Q` | Quit application |
| `Cmd+W` | Close window |
| `Cmd+Tab` | Switch between tabs |
| `Cmd+S` | Save report (in Audit tab) |

---

## 🚀 Advanced Usage

### Running from Command Line
```bash
# Launch GUI
python3 windsurf_privacy_gui.py

# With specific tab
python3 windsurf_privacy_gui.py --tab audit

# With debug output
python3 windsurf_privacy_gui.py --debug
```

### Customizing the Theme
Edit the `apply_dark_theme()` method in `windsurf_privacy_gui.py`:
```python
def apply_dark_theme(self):
    dark_stylesheet = """
        /* Customize colors here */
        QMainWindow {
            background-color: #your-color;
        }
    """
    self.setStyleSheet(dark_stylesheet)
```

---

## 📊 Performance

- **Memory Usage**: ~50-100 MB
- **CPU Usage**: <5% idle, <20% during operations
- **Startup Time**: <2 seconds
- **Script Execution**: Real-time output streaming

---

## 🔒 Security

### Data Handling
- All operations run locally
- No network connections from GUI
- Scripts execute with user permissions
- Backup data stored locally

### Sensitive Information
- GUI does not log sensitive data
- Output can be cleared
- Reports saved to user-specified location

---

## 🐛 Known Issues

1. **Interactive Prompts**: Some scripts have interactive prompts that need modification for GUI use
2. **Progress Tracking**: Progress bar is based on text output parsing
3. **macOS Only**: Currently only supports macOS (Linux/Windows coming)

---

## 🔮 Planned Features

- [ ] Linux support
- [ ] Windows support
- [ ] Scheduled cleanup
- [ ] Real-time monitoring dashboard
- [ ] Export to PDF
- [ ] Email notifications
- [ ] Cloud backup integration
- [ ] Multi-language support

---

## 📝 License

MIT License - See main repository for details

---

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Test thoroughly
4. Submit a pull request

---

## 📧 Support

- **Issues**: GitHub Issues
- **Discussions**: GitHub Discussions
- **Email**: hana.omori@aimarketingflow.com

---

## 🙏 Acknowledgments

- PyQt6 team for excellent Qt bindings
- Windsurf IDE for the platform
- Security research community

---

**Version**: 1.0.0  
**Last Updated**: October 11, 2025  
**Platform**: macOS 14+  
**Python**: 3.8+
