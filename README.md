# Windsurf Privacy Enforcer & Historical Access Clear

**Complete Security Toolkit for Windsurf IDE Privacy Protection**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Platform: macOS](https://img.shields.io/badge/Platform-macOS-blue.svg)](https://www.apple.com/macos/)
[![Shell: Bash](https://img.shields.io/badge/Shell-Bash-green.svg)](https://www.gnu.org/software/bash/)

> **⚠️ IMPORTANT UPDATE: Chat Backup Feature Status**  
> As of the latest Windsurf updates, chat conversations are now stored on Codeium's cloud servers rather than locally. The `backup_windsurf_chat.sh` script and related chat backup features **no longer work** as intended. We are actively working on an alternative solution that may involve API-based backups or local conversation logging. Stay tuned for updates.

> **🎨 NEW: PyQt6 GUI Available!**  
> We've added a modern graphical interface (`windsurf_privacy_gui.py`) for easier use. **Note:** The GUI is currently in active development and may contain bugs. Please report any issues you encounter via [GitHub Issues](https://github.com/aimarketingflow/windsurf-privacy-enforcer-historical-access-clear/issues). See [GUI_README.md](GUI_README.md) for details.

## 🚨 Overview

This toolkit provides comprehensive privacy protection for Windsurf IDE users. Based on extensive security research documenting **active data exfiltration** and **workspace boundary violations**, these tools help you:

- **Audit** Windsurf's system access and network activity
- **Clear** tracking data and persistent identifiers
- **Sandbox** Windsurf to restrict excessive permissions
- **Verify** cleanup effectiveness and monitor ongoing activity

### Key Findings from Security Research

- **178 MB** of data transmitted during normal usage
- **16+ directories** tracked outside opened workspace
- **110 active network connections** including Google Cloud
- **Complete file contents** transmitted via Protocol Buffers
- **Persistent tracking IDs** for cross-session profiling

## 📦 Toolkit Components

### 🎨 NEW: `windsurf_privacy_gui.py` - GUI Application
**Modern PyQt6 graphical interface (BETA)**

⚠️ **Development Status:** This GUI is in active development and may contain bugs. We appreciate bug reports via GitHub Issues!

**Features:**
- 🏠 **Dashboard** - Real-time status monitoring with intelligent recommendations
- 🔍 **Audit** - Run security audits with live output
- 🧹 **Cleanup** - Enhanced cleanup with 4 backup options
- 💾 **Backups** - Comprehensive backup management (Chat, Audit Reports, Full Backups, Export/Import)

**Quick Start:**
```bash
# Install PyQt6
pip install PyQt6

# Run GUI
python3 windsurf_privacy_gui.py
```

**Known Limitations:**
- macOS only (Linux/Windows support coming)
- Some interactive script prompts need manual handling
- Export/Import features are experimental

**See [GUI_README.md](GUI_README.md) for complete documentation.**

---

### 1. `audit_windsurf_access.sh` 🔍
**Comprehensive security assessment tool**

Performs 10 security checks:
- Active network connections analysis
- System permissions audit
- Tracking database inspection
- Process monitoring
- File system access patterns
- Workspace boundary violations
- Persistent identifier detection
- Cache and storage analysis

**Usage:**
```bash
./audit_windsurf_access.sh > audit_report.txt
```

### 2. `clear_windsurf_tracking.sh` 🧹
**Privacy cleanup script (Original)**

Removes:
- Machine/Device tracking IDs
- Workspace tracking (16+ directories)
- 153 MB of tracking data
- Telemetry cache
- Crash reports

Preserves:
- Login credentials
- GitHub authentication
- Chat history
- User settings
- Extensions

**Usage:**
```bash
./clear_windsurf_tracking.sh
```

### 2b. `clear_windsurf_tracking_ENHANCED.sh` 🧹✨
**Enhanced cleanup script (Recommended)**

**NEW:** Complete historical access deletion with 10-step process:
1. Workspace storage cleanup (preserves chat)
2. Global storage.json complete rewrite
3. Global state.vscdb workspace history removal
4. Cache clearing
5. CachedData clearing
6. GPUCache clearing
7. Crash reports removal
8. Log cleanup (preserves auth logs)
9. Old backup file removal
10. Database optimization

**Test Results:** 82% pass rate (19/23 tests), 100% on critical tests

Removes:
- ALL tracking IDs (Machine, Device, SQM)
- ALL 16+ workspace associations
- ALL sensitive directory references
- 26.2 MB tracking data
- Historical access records

Preserves:
- 100% GitHub authentication
- 100% Chat history (51 entries)
- 100% User settings
- All extensions

**Usage:**
```bash
./clear_windsurf_tracking_ENHANCED.sh
```

### 2c. `verify_preservation_safety.sh` 🛡️
**Pre-flight safety check (NEW)**

Run BEFORE cleanup to verify what will be preserved:
- Chat history count and location
- GitHub authentication status
- User settings presence
- What will be deleted

**Usage:**
```bash
./verify_preservation_safety.sh
```

### 2d. `test_historical_access_deletion.sh` 🧪
**Comprehensive test suite (NEW)**

23-point verification after cleanup:
- Tracking ID deletion (3 tests)
- Workspace history deletion (4 tests)
- Database cleanup (4 tests)
- Cache cleanup (3 tests)
- Authentication preservation (2 tests)
- Deep forensic scans (7 tests)

**Usage:**
```bash
./test_historical_access_deletion.sh
```

### 2e. `backup_windsurf_chat.sh` 💾 ⚠️ **DEPRECATED**
**Chat history backup tool (NO LONGER FUNCTIONAL)**

> **⚠️ DEPRECATION NOTICE:**  
> This tool is **no longer functional** as of the latest Windsurf updates. Windsurf now stores chat conversations on Codeium's cloud servers rather than in local databases. The script will run but will find no chat data to backup.
>
> **Status:** We are working on an alternative solution that may include:
> - API-based cloud backup (if Codeium provides an API)
> - Local conversation logging during sessions
> - Export functionality through Windsurf's UI (if available)
>
> **For now:** Chat history is only accessible through the Windsurf interface and stored on Codeium's servers.

~~Exports all Windsurf/Cascade chat histories to readable formats:~~
- ~~**CSV format** - Open in Excel/Numbers/Google Sheets~~
- ~~**JSON format** - For programmatic access~~
- ~~**Full database backup** - For complete restoration~~

**Previous Features (No longer working):**
- ~~Backs up all workspaces automatically~~
- ~~Creates readable CSV files for each workspace~~
- ~~Includes restoration instructions~~
- ~~Preserves all chat metadata~~

**Note:** The enhanced cleanup script's chat backup options are also affected by this change.

### 3. `sandbox_windsurf.sh` 🔒
**Interactive sandboxing wizard**

Restricts:
- Camera access
- Microphone access
- Bluetooth access
- Network connections (localhost only option)
- File system access (workspace-only option)

**Usage:**
```bash
./sandbox_windsurf.sh
```

### 4. `verify_cleanup.sh` ✅
**Verification and monitoring tool**

Performs 8 verification tests:
- Tracking IDs removed
- Workspace tracking cleared
- Network connections status
- Cache size check
- Database file count
- Live traffic monitoring
- Language server status
- External connection check

**Usage:**
```bash
./verify_cleanup.sh

# Continuous monitoring
watch -n 60 ./verify_cleanup.sh
```

### 5. `Clear Windsurf Tracking.app` 🖥️
**macOS desktop application**

One-click privacy cleanup with GUI convenience.

## 🚀 Quick Start

### Installation

1. **Clone the repository:**
```bash
git clone https://github.com/aimarketingflow/windsurf-privacy-enforcer-historical-access-clear.git
cd windsurf-privacy-enforcer-historical-access-clear
```

2. **Make scripts executable:**
```bash
chmod +x *.sh
```

3. **Run initial audit:**
```bash
./audit_windsurf_access.sh
```

### Recommended Workflow (Enhanced)

**Step 1: Audit** - Understand your current exposure
```bash
./audit_windsurf_access.sh > audit_report.txt
```

**Step 2: Safety Check** - Verify what will be preserved (NEW)
```bash
./verify_preservation_safety.sh
```

**Step 3: Close Windsurf** - Stop all processes
```bash
pkill -9 Windsurf
pkill -9 language_server_macos_arm
```

**Step 4: Enhanced Clean** - Complete historical access deletion (RECOMMENDED)
```bash
./clear_windsurf_tracking_ENHANCED.sh
```

**Step 5: Test** - Comprehensive verification (NEW)
```bash
./test_historical_access_deletion.sh
```

**Step 6: Sandbox** - Restrict permissions
```bash
./sandbox_windsurf.sh
```

**Step 7: Verify** - Confirm effectiveness
```bash
./verify_cleanup.sh
```

**Step 8: Monitor** - Ongoing surveillance
```bash
watch -n 60 ./verify_cleanup.sh
```

### Alternative: Original Workflow

For the original cleanup process (without enhanced features):
```bash
# Step 1: Audit
./audit_windsurf_access.sh

# Step 2: Close Windsurf
pkill -9 Windsurf

# Step 3: Clean (original)
./clear_windsurf_tracking.sh

# Step 4: Sandbox
./sandbox_windsurf.sh

# Step 5: Verify
./verify_cleanup.sh
```

## 🖥️ Desktop App Installation (macOS)

### Step 1: Copy to Secure Location
```bash
# Create a secure directory outside Windsurf's reach
mkdir -p ~/PrivacyTools
cp -r "Clear Windsurf Tracking.app" ~/PrivacyTools/
```

### Step 2: Create Desktop Shortcut
```bash
# Create an alias on Desktop
ln -s ~/PrivacyTools/"Clear Windsurf Tracking.app" ~/Desktop/
```

**OR** manually:
1. Open Finder
2. Navigate to `~/PrivacyTools/`
3. Right-click `Clear Windsurf Tracking.app`
4. Select "Make Alias"
5. Drag the alias to your Desktop

### Step 3: Make Executable
```bash
chmod +x ~/PrivacyTools/"Clear Windsurf Tracking.app/Contents/MacOS/launcher"
```

### Step 4: Remove Quarantine (if needed)
```bash
xattr -d com.apple.quarantine ~/PrivacyTools/"Clear Windsurf Tracking.app"
```

## 📊 What Gets Cleared vs Preserved

### ✅ Cleared (Privacy Data)
- Machine/Device tracking IDs
- Workspace tracking (16+ directories)
- 153 MB of tracking databases
- Telemetry cache
- Crash reports
- Non-authentication logs
- File access history
- Cross-workspace activity data

### 🔒 Preserved (User Data)
- Windsurf login credentials
- GitHub authentication
- Chat history with Cascade
- User settings and preferences
- Installed extensions
- Custom keybindings
- Workspace configurations

## 🔧 Troubleshooting

### Scripts won't execute
```bash
# Make all scripts executable
chmod +x *.sh
```

### "Permission denied" errors
```bash
# Run with sudo for system-level operations
sudo ./sandbox_windsurf.sh
```

### Desktop app won't open
```bash
# Remove macOS quarantine
xattr -d com.apple.quarantine ~/PrivacyTools/"Clear Windsurf Tracking.app"

# Verify executable permissions
chmod +x ~/PrivacyTools/"Clear Windsurf Tracking.app/Contents/MacOS/launcher"
```

### Windsurf still tracking after cleanup
```bash
# Ensure Windsurf is fully closed
pkill -9 Windsurf
pkill -9 language_server_macos_arm

# Re-run cleanup
./clear_windsurf_tracking.sh

# Verify with monitoring
./verify_cleanup.sh
```

### Want to restore from backup?
```bash
# Backups are stored in:
~/windsurf_backup_[timestamp]/

# To restore:
cp -r ~/windsurf_backup_[timestamp]/* ~/Library/Application\ Support/Windsurf/
```

## 📅 Recommended Usage Schedule

### Regular Maintenance
- **Weekly** - For active Windsurf users
- **Monthly** - Minimum recommended frequency
- **Before sensitive work** - Always clear before security research
- **After Windsurf updates** - Re-apply sandboxing after updates

### Monitoring
- **Continuous** - Use `watch -n 60 ./verify_cleanup.sh` during sensitive sessions
- **Daily** - Quick verification check
- **After cleanup** - Always verify effectiveness

## 🔐 Security Considerations

### Important Limitations
- ⚠️ **Local data only**: This toolkit clears LOCAL tracking data. Data already transmitted to Windsurf servers cannot be removed.
- ⚠️ **Network monitoring**: Consider using Little Snitch or Lulu firewall for real-time network blocking.
- ⚠️ **Backup first**: Always create backups before running cleanup scripts.

### Enhanced Protection
1. **Combine with firewall**: Use `sandbox_windsurf.sh` + network firewall
2. **Dedicated workspace**: Use separate directories for sensitive projects
3. **Air-gapped systems**: For critical security research, use offline systems
4. **Regular audits**: Run `audit_windsurf_access.sh` weekly

### For Security Researchers
- Use isolated VMs for vulnerability research
- Monitor network traffic with Wireshark/tcpdump
- Consider alternative IDEs (VS Code, Neovim) for sensitive work
- Never open 0-day research in Windsurf

## 📚 Background & Research

This toolkit is based on comprehensive security research conducted October 6-11, 2025, which documented:

- **Active data exfiltration**: 178 MB transmitted during normal usage
- **Workspace violations**: 16+ directories tracked outside opened workspace
- **Network activity**: 110 active connections including Google Cloud (35.223.238.178)
- **File content transmission**: Complete files sent via Protocol Buffers
- **Persistent tracking**: Unique machine/device IDs for user profiling

For detailed findings, see the complete security report (available separately).

## 🤝 Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Test thoroughly on macOS
4. Submit a pull request

### Areas for Contribution
- Linux/Windows support
- Additional verification tests
- Network monitoring integration
- GUI application improvements
- Documentation translations

## 📄 License

MIT License - See LICENSE file for details

## ⚠️ Disclaimer

This toolkit is provided for educational and privacy protection purposes. Users are responsible for:
- Compliance with Windsurf's Terms of Service
- Backing up data before running scripts
- Understanding the implications of sandboxing
- Verifying script behavior in their environment

The authors are not responsible for any data loss, system issues, or Terms of Service violations resulting from use of this toolkit.

## 📞 Support & Contact

- **Issues**: Open a GitHub issue
- **Security concerns**: Contact via GitHub security advisory
- **General questions**: Use GitHub discussions

## 🙏 Acknowledgments

- Security research conducted by AIMF LLC
- Community feedback and testing
- Open source security tools community

---

**Version:** 1.0  
**Last Updated:** October 11, 2025  
**Platform:** macOS (Linux/Windows support planned)  
**Tested on:** macOS 14+ (Sonoma, Sequoia)
