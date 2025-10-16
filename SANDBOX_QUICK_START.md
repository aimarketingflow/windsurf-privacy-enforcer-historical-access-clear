# Windsurf Sandbox - Quick Start Guide

## What It Does

The **Windsurf Sandbox** restricts Windsurf IDE to only access files in your current workspace. It prevents:

- ✅ Access to files outside the workspace folder
- ✅ Network connections to Google Cloud IPs
- ✅ Scanning your entire Documents folder
- ✅ Transmitting data from other projects

## Quick Start

### 1. Enable Sandbox for Current Project

```bash
cd /path/to/your/project
./windsurf-sandbox.sh enable .
```

This will:
- Quit Windsurf if running
- Create a sandbox profile
- Relaunch Windsurf with restrictions
- Only allow access to the current folder

### 2. Check Status

```bash
./windsurf-sandbox.sh status
```

Shows:
- Whether sandbox is active
- Which workspace is allowed
- If Windsurf is running

### 3. Monitor File Access Attempts

```bash
./windsurf-sandbox.sh monitor
```

Real-time monitoring of:
- Denied file access attempts
- Blocked network connections
- Sandbox violations

### 4. Disable Sandbox

```bash
./windsurf-sandbox.sh disable
```

Removes all restrictions and returns to normal operation.

---

## Example Workflow

### Scenario: Working on Sensitive Security Research

```bash
# Navigate to your sensitive project
cd ~/Documents/AIMFGuideforCybersec*°·/LinkedInExploit

# Enable sandbox (restricts Windsurf to ONLY this folder)
../WindsurfExploit-Oct25/windsurf-sandbox.sh enable .

# Windsurf will restart and can ONLY access LinkedInExploit folder
# It CANNOT see:
#   - WindsurfExploit-Oct25/
#   - Spotify_Attack_Data/
#   - Any other folders in Documents/

# Work on your files safely
# ...

# When done, disable sandbox
../WindsurfExploit-Oct25/windsurf-sandbox.sh disable
```

---

## What Gets Blocked

### File Access
- ❌ **Blocked:** All folders outside workspace
- ❌ **Blocked:** Parent directories
- ❌ **Blocked:** Other projects in Documents/
- ✅ **Allowed:** Current workspace only
- ✅ **Allowed:** System libraries (read-only)
- ✅ **Allowed:** Windsurf's own config files

### Network Access
- ❌ **Blocked:** Google Cloud IPs (2607:f8b0:4005::/48)
- ✅ **Allowed:** DNS, Apple services, Cloudflare CDN

---

## Advanced Usage

### Enable Sandbox for Specific Folder

```bash
./windsurf-sandbox.sh enable ~/Documents/MyProject
```

### Monitor in Background

```bash
./windsurf-sandbox.sh monitor > sandbox-log.txt 2>&1 &
```

### Check Logs

```bash
tail -f ~/.windsurf-sandbox.log
```

---

## Technical Details

### How It Works

1. **macOS Sandbox Profile:** Uses Apple's `sandbox-exec` to create a security profile
2. **File Access Control:** Restricts read/write to specified workspace only
3. **Network Filtering:** Blocks outbound connections to Google Cloud IPs
4. **Process Isolation:** Windsurf runs in a restricted environment

### Sandbox Profile Location

```
/tmp/windsurf-sandbox-<pid>.sb
```

### Configuration Files

```
~/.windsurf-sandbox-profile    # Current sandbox profile path
~/.windsurf-sandbox-workspace  # Current allowed workspace
~/.windsurf-sandbox.log        # Activity log
```

---

## Limitations

### What Sandbox CANNOT Prevent

1. **Windsurf's Config Access:** Windsurf can still read/write its own settings
2. **System Libraries:** Read-only access to /System, /Library (required for operation)
3. **Temporary Files:** Access to /tmp (required for IPC)

### Known Issues

- **First Launch:** May take 5-10 seconds to start
- **Extensions:** Some Windsurf extensions may not work if they need external file access
- **Git Operations:** Git repos outside workspace won't be accessible

---

## Troubleshooting

### Windsurf Won't Start

```bash
# Check if sandbox profile is valid
cat ~/.windsurf-sandbox-profile

# Remove sandbox and try again
./windsurf-sandbox.sh disable
```

### "Permission Denied" Errors

```bash
# Make sure script is executable
chmod +x windsurf-sandbox.sh

# Check workspace path exists
ls -la /path/to/workspace
```

### Sandbox Not Working

```bash
# Verify macOS version (requires 10.14+)
sw_vers

# Check if sandbox-exec is available
which sandbox-exec

# View system logs
./windsurf-sandbox.sh monitor
```

---

## Security Notes

### What This Protects Against

✅ **Workspace-wide scanning** - Windsurf can't index other folders  
✅ **File path leakage** - Other project names won't be transmitted  
✅ **Cross-project contamination** - Evidence files stay isolated  
✅ **Google Cloud exfiltration** - Network to GCP is blocked  

### What This DOESN'T Protect Against

❌ **Clipboard access** - Windsurf can still read clipboard  
❌ **Keyboard logging** - Keystrokes within workspace are still sent  
❌ **Local model inference** - If using local AI, no network needed  

---

## Comparison: Before vs. After

### Before Sandbox

```
Windsurf has access to:
├── Documents/
│   ├── AIMFGuideforCybersec/
│   │   ├── LinkedInExploit/          ← Can scan
│   │   ├── WindsurfExploit-Oct25/    ← Can scan
│   │   ├── Spotify_Attack_Data/      ← Can scan
│   │   └── ALL OTHER FOLDERS         ← Can scan
│   └── Other sensitive projects/     ← Can scan
└── Network: Google Cloud (unrestricted)
```

### After Sandbox

```
Windsurf has access to:
├── Documents/
│   ├── AIMFGuideforCybersec/
│   │   ├── LinkedInExploit/          ← ONLY THIS
│   │   ├── WindsurfExploit-Oct25/    ← BLOCKED
│   │   ├── Spotify_Attack_Data/      ← BLOCKED
│   │   └── ALL OTHER FOLDERS         ← BLOCKED
│   └── Other sensitive projects/     ← BLOCKED
└── Network: Google Cloud (BLOCKED)
```

---

## Recommended Workflow

### For Security Research

1. **Create isolated workspace** for each investigation
2. **Enable sandbox** before opening Windsurf
3. **Work on evidence** knowing other projects are protected
4. **Monitor activity** with `./windsurf-sandbox.sh monitor`
5. **Disable sandbox** when switching projects

### For General Development

1. **Enable sandbox** for client projects under NDA
2. **Enable sandbox** for personal projects with sensitive data
3. **Disable sandbox** for open-source work (less concern)

---

## FAQ

**Q: Will this slow down Windsurf?**  
A: Minimal impact. Sandbox checks are fast.

**Q: Can I have multiple workspaces?**  
A: No, only one workspace at a time. Disable and re-enable for different folders.

**Q: Does this work with Windsurf updates?**  
A: Yes, sandbox is applied at runtime, not to the app itself.

**Q: Can Windsurf bypass this?**  
A: No, macOS sandbox is kernel-level enforcement.

**Q: What if I need to access a file outside workspace?**  
A: Disable sandbox temporarily, or copy the file into workspace.

---

## Support

For issues or questions:
- Check logs: `cat ~/.windsurf-sandbox.log`
- View status: `./windsurf-sandbox.sh status`
- Monitor violations: `./windsurf-sandbox.sh monitor`

---

**Created:** October 7, 2025  
**Version:** 1.0.0  
**Author:** AIMF LLC Cybersecurity Research
