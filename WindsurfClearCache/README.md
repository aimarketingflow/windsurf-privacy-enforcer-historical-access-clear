# Windsurf Clear Tracking - Desktop Shortcut

## 📦 What's in This Folder

- `clear_windsurf_tracking.sh` - The cleanup script
- `Clear Windsurf Tracking.app` - macOS app for easy launching

## 🚀 Installation Instructions

### Step 1: Copy to _Locker
```bash
cp -r ~/Documents/AIMFGuideforCybersec*°·/WindsurfExploit-Oct25/WindsurfClearCache /Users/meep/_Locker/
```

### Step 2: Create Desktop Shortcut
```bash
# Create an alias on Desktop
ln -s "/Users/meep/_Locker/WindsurfClearCache/Clear Windsurf Tracking.app" ~/Desktop/
```

**OR** manually:
1. Open Finder
2. Navigate to `/Users/meep/_Locker/WindsurfClearCache/`
3. Right-click `Clear Windsurf Tracking.app`
4. Select "Make Alias"
5. Drag the alias to your Desktop

### Step 3: Make Executable (if needed)
```bash
chmod +x "/Users/meep/_Locker/WindsurfClearCache/Clear Windsurf Tracking.app/Contents/MacOS/launcher"
chmod +x "/Users/meep/_Locker/WindsurfClearCache/clear_windsurf_tracking.sh"
```

## 🎯 How to Use

### Option 1: Double-Click the App
- Double-click `Clear Windsurf Tracking.app` (or the Desktop shortcut)
- Terminal will open and run the script
- Follow the prompts

### Option 2: Run from Terminal
```bash
cd /Users/meep/_Locker/WindsurfClearCache
./clear_windsurf_tracking.sh
```

## ✨ What It Does

**CLEARS:**
- ✓ Workspace tracking (16 directories)
- ✓ Machine/Device tracking IDs
- ✓ Cache (140 MB)
- ✓ Crash reports
- ✓ Non-auth logs

**PRESERVES:**
- ✓ Windsurf login (stays logged in)
- ✓ GitHub authentication
- ✓ Chat history with Cascade
- ✓ User settings
- ✓ Extensions
- ✓ Keybindings

## 🔧 Troubleshooting

### App won't open?
```bash
# Remove quarantine attribute
xattr -d com.apple.quarantine "/Users/meep/_Locker/WindsurfClearCache/Clear Windsurf Tracking.app"
```

### Permission denied?
```bash
# Make executable
chmod +x "/Users/meep/_Locker/WindsurfClearCache/Clear Windsurf Tracking.app/Contents/MacOS/launcher"
```

### Want to run silently?
Edit the launcher script and remove the Terminal activation, or run directly:
```bash
/Users/meep/_Locker/WindsurfClearCache/clear_windsurf_tracking.sh
```

## 📅 Recommended Schedule

Run this script:
- **Weekly** - For regular privacy maintenance
- **Monthly** - Minimum recommended
- **Before sensitive work** - Clear tracking before opening sensitive projects

## 🔐 Security Notes

- This script only clears LOCAL tracking data
- Data already sent to Windsurf servers remains there
- For complete privacy, combine with firewall rules (see sandbox_windsurf.sh)
- Always backup before running (script offers this option)

## 📞 Support

If you need to restore from backup:
```bash
# Backups are stored in:
~/windsurf_backup_[timestamp]/
```

---

**Version:** 1.0  
**Last Updated:** October 11, 2025
