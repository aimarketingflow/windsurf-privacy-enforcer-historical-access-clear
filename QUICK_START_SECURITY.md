# Windsurf Security Quick Start Guide

## 🚀 Three-Step Security Setup

### Step 1: Revoke Permissions (5 minutes)

**Go to System Settings → Privacy & Security**

1. **Camera** → Find "Windsurf" → Toggle OFF
2. **Microphone** → Find "Windsurf" → Toggle OFF  
3. **Bluetooth** → Find "Windsurf" → Toggle OFF
4. **Files and Folders** → Find "Windsurf" → Revoke all
5. **Full Disk Access** → Find "Windsurf" → Toggle OFF (CRITICAL!)
6. **Automation** → Find "Windsurf" → Revoke all

---

### Step 2: Run Audit Script (2 minutes)

```bash
cd ~/Documents/AIMFGuideforCybersec*°·/WindsurfExploit-Oct25/
./audit_windsurf_access.sh
```

**What it checks:**
- ✅ Code signing & entitlements
- ✅ Requested permissions
- ✅ Granted permissions (requires sudo)
- ✅ Workspace tracking
- ✅ Active network connections
- ✅ Running processes
- ✅ Storage usage

**Review the output** and note any concerning findings.

---

### Step 3: Setup Sandboxing (10 minutes)

```bash
./sandbox_windsurf.sh
```

**Select option 5** (All of the above) to:
1. Create custom sandbox profile
2. Setup firewall rules
3. Create restricted launch wrapper
4. Setup file system restrictions

**Then apply the restrictions:**

```bash
# Apply file restrictions
~/.windsurf_sandbox/setup_acls.sh

# Test restricted launch
~/.windsurf_sandbox/windsurf_restricted.sh
```

---

## 📋 Quick Commands Reference

### Audit Windsurf Access
```bash
./audit_windsurf_access.sh | tee windsurf_audit_$(date +%Y%m%d).log
```

### Launch Windsurf Sandboxed
```bash
~/.windsurf_sandbox/windsurf_restricted.sh
```

### Check Active Connections
```bash
lsof -i -n -P | grep -i windsurf
```

### Clear Workspace History
```bash
rm -rf ~/Library/Application\ Support/Windsurf/User/workspaceStorage/
rm ~/Library/Application\ Support/Windsurf/User/globalStorage/storage.json
```

### Monitor Network Traffic
```bash
sudo tcpdump -i any -n host $(hostname) and port 443 -w windsurf_traffic.pcap
```

---

## 🔥 Nuclear Option: Complete Removal

If you decide Windsurf is too risky:

```bash
# 1. Quit Windsurf
killall Windsurf 2>/dev/null

# 2. Remove application
sudo rm -rf /Applications/Windsurf.app

# 3. Remove all data
rm -rf ~/Library/Application\ Support/Windsurf
rm -rf ~/Library/Caches/Windsurf
rm -rf ~/Library/Saved\ Application\ State/com.exafunction.windsurf.savedState
rm -rf ~/Library/Preferences/com.exafunction.windsurf.plist

# 4. Clear TCC permissions (requires reboot)
# Go to System Settings → Privacy & Security
# Manually remove all Windsurf entries

# 5. Verify removal
find ~ -name "*windsurf*" -o -name "*Windsurf*" 2>/dev/null
```

---

## 🛡️ Firewall Setup Options

### Option A: Little Snitch (Paid, Recommended)
1. Install Little Snitch
2. Import rules from: `~/.windsurf_sandbox/windsurf_lulu_rules.txt`
3. Block all Windsurf connections except localhost

### Option B: Lulu (Free)
1. Install Lulu from Objective-See
2. Manually create rules:
   - Block: `/Applications/Windsurf.app` → Any (except 127.0.0.1)
   - Allow: `/Applications/Windsurf.app` → 127.0.0.1, ::1

### Option C: pfctl (Built-in, Advanced)
```bash
sudo pfctl -f ~/.windsurf_sandbox/windsurf_firewall.rules
sudo pfctl -e  # Enable pfctl
```

---

## 📊 Monitoring Checklist

**Daily:**
- [ ] Check for unexpected network connections
- [ ] Review workspace tracking in storage.json

**Weekly:**
- [ ] Run audit script
- [ ] Check packet captures for data exfiltration
- [ ] Review System Settings permissions

**Monthly:**
- [ ] Clear workspace history
- [ ] Update sandbox rules
- [ ] Review firewall logs

---

## ⚠️ Known Limitations

**Sandboxing will break:**
- ✅ AI features (requires network)
- ✅ Extension marketplace
- ✅ Auto-updates
- ✅ Telemetry (good!)
- ✅ Cloud sync

**Sandboxing will NOT prevent:**
- ❌ Data already collected
- ❌ Access to files you explicitly open
- ❌ Workspace indexing (happens locally)

---

## 🎯 Recommended Workflow

**For Sensitive Work:**
1. Use VS Code with local-only extensions
2. Work in air-gapped VM
3. Never open sensitive directories in Windsurf

**For General Work:**
1. Use sandboxed Windsurf launcher
2. Monitor with audit script weekly
3. Clear workspace history monthly

**For Maximum Security:**
1. Remove Windsurf completely
2. Use Vim/Emacs/VS Code (local only)
3. Work offline

---

## 📞 Support

**Issues with scripts:**
- Check permissions: `ls -l *.sh`
- Make executable: `chmod +x *.sh`
- Run with bash: `bash script_name.sh`

**Sandbox not working:**
- Check macOS version (sandbox-exec deprecated in newer versions)
- Try firewall-only approach
- Consider VM isolation instead

**Need help:**
- Review ANALYSIS_10-11-25_SPIKE.md for technical details
- Check WINDSURF_EXFILTRATION_ANALYSIS.md for background
- Consult WINDSURF_PRIVACY_OVERREACH_CASE_STUDY.md for context

---

## 🔐 Security Best Practices

1. **Never grant Full Disk Access** to any IDE
2. **Revoke camera/microphone** unless actively needed
3. **Monitor network traffic** regularly
4. **Clear workspace history** frequently
5. **Use separate user account** for sensitive work
6. **Enable FileVault** for disk encryption
7. **Use firewall** to block unnecessary connections
8. **Audit permissions** monthly

---

**Last Updated:** October 11, 2025  
**Scripts Version:** 1.0  
**Compatibility:** macOS 13.0+
