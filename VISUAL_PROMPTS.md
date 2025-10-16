# Visual Prompts for Windsurf Security Report
**AIMF LLC Cybersecurity Research**  
**Date:** October 11, 2025

---

## 1. Data Flow Diagram - Exfiltration Architecture

**Purpose:** Show complete data exfiltration pathway from user's workspace to Google Cloud

**Prompt:**
```
Create a technical network diagram showing:
- Center: User's MacBook with Windsurf IDE open
- Left side: Local workspace with 16 folders (show folder icons with security-related names)
- Middle: Windsurf processes (language_server_macos_arm, Windsurf Helper)
- Right side: Data flow arrows showing:
  * Protocol Buffers serialization
  * Loopback connections (127.0.0.1) - 106,754 packets
  * External connection to Google Cloud (35.223.238.178:443)
- Bottom: Storage showing tracking IDs and workspace databases
- Color code: Red for sensitive data, Yellow for tracking, Blue for network
- Style: Modern, technical, cybersecurity aesthetic with dark background
```

**Dimensions:** 1920x1080 (landscape)  
**File Name:** `windsurf_data_flow_diagram.png`

---

## 2. Timeline Infographic - Investigation Journey

**Purpose:** Visual timeline of the 5-day investigation from discovery to solution

**Prompt:**
```
Create a horizontal timeline infographic showing:
- Oct 6, 2025 17:06 PDT: Initial discovery (network spike icon)
- Oct 6, 2025 17:50 PDT: First PCAP capture complete (93 MB)
- Oct 11, 2025 15:30 PDT: Second capture begins
- Oct 11, 2025 15:38:45 PDT: BREAKTHROUGH - Frame 3243 discovered (explosion/lightbulb icon)
- Oct 11, 2025 16:25 PDT: Capture complete (85 MB)
- Oct 11, 2025 17:00 PDT: Solution toolkit developed (shield icon)
- Style: Clean, modern timeline with icons, gradient purple/blue colors
- Include packet counts and data sizes at each milestone
```

**Dimensions:** 2400x800 (wide banner)  
**File Name:** `windsurf_investigation_timeline.png`

---

## 3. Workspace Boundary Violation Map

**Purpose:** Visualize unauthorized access to 16 directories outside opened workspace

**Prompt:**
```
Create a visual map showing:
- Center circle: "Opened Workspace" (AIMFGuideforCybersec folder)
- Outer ring: 16 unauthorized accessed directories radiating outward
- Each directory as a node with icon:
  * Stealthshark2 (shark icon, red alert)
  * HackRFOne-SignalTesting (radio tower, red alert)
  * AntiPineapple (pineapple with X, red alert)
  * _Murus_Firewall_Optimizer (firewall icon, red alert)
  * _ToInvestigate-Offline-Attacks (folder with warning, red alert)
  * AmbientSec (security badge, red alert)
  * SunoVocalStemz (music note, yellow)
  * MidiVisualizer (waveform, yellow)
  * MidiViz (chart, yellow)
  * Staples (office, yellow)
  * _SpecialCharacterNightmare (symbols, yellow)
  * Wild*Card (wildcard symbol, yellow)
- Connecting lines showing Windsurf's unauthorized access
- Legend showing: Red = Security Research, Yellow = Personal, Blue = Media
- Style: Network graph, cybersecurity theme, dark background
```

**Dimensions:** 1920x1080 (landscape)  
**File Name:** `windsurf_workspace_violations.png`

---

## 4. Traffic Spike Analysis Chart

**Purpose:** Show data exfiltration spikes over time with volume metrics

**Prompt:**
```
Create a line/area chart showing:
- X-axis: Time (0-3337 seconds)
- Y-axis: Data rate (kBps) and Packet count
- Multiple colored spikes highlighting:
  * 480-540s: 8.7 MB spike (red, labeled "4,105 packets")
  * 2400-2460s: 4.5 MB spike (orange, labeled "4,287 packets")
  * 3240-3300s: 9.5 MB spike (red, labeled "8,932 packets")
  * 3300-3337s: 13.5 MB EXTREME spike (dark red, labeled "364 kBps - CRITICAL")
- Annotations showing what was being transmitted at each spike
- Background gradient from blue (normal) to red (critical)
- Style: Modern data visualization, professional analytics dashboard
- Include legend showing: Normal activity, High activity, Critical exfiltration
```

**Dimensions:** 1600x900 (landscape)  
**File Name:** `windsurf_traffic_spikes.png`

---

## 5. Security Toolkit Dashboard

**Purpose:** Visual overview of the 4-tool security solution

**Prompt:**
```
Create a dashboard-style visual showing 4 tools in a 2x2 grid:

Top left: audit_windsurf_access.sh (magnifying glass icon)
  * Title: "System Audit"
  * Shows: "10 checks performed"
  * Status indicators: green/red dots for each check
  * Metrics: "110 connections found, 16 workspaces tracked"

Top right: clear_windsurf_tracking.sh (broom/trash icon)
  * Title: "Privacy Cleanup"
  * Shows: "16 workspaces cleared, 140 MB freed"
  * Before/After comparison bars
  * Status: "Tracking IDs removed"

Bottom left: sandbox_windsurf.sh (lock/shield icon)
  * Title: "Sandboxing"
  * Shows: "5 restrictions applied"
  * Icons for blocked: camera, mic, network, bluetooth, files
  * Status: "Isolation active"

Bottom right: verify_cleanup.sh (checkmark icon)
  * Title: "Verification"
  * Shows: "8 verification tests"
  * Pass/Fail indicators (green checkmarks, red X's)
  * Overall status: "CLEANUP SUCCESSFUL"

- Style: Modern UI dashboard, purple/blue gradient, clean icons
- Each tool box has rounded corners, subtle shadow
- Include terminal-style code snippets for each tool
```

**Dimensions:** 1920x1080 (landscape)  
**File Name:** `windsurf_security_toolkit.png`

---

## 6. Frame 3243 Packet Breakdown

**Purpose:** Detailed technical visualization of the smoking gun packet

**Prompt:**
```
Create a detailed packet visualization showing:

Top section: Packet header
  * Frame 3243
  * 637 bytes
  * Timestamp: Oct 11, 2025 15:38:45.665710 PDT
  * Interface: lo0 (Loopback)

Middle section: Protocol layers breakdown (OSI model style):
  * Layer 1: NULL/Loopback (gray)
  * Layer 2: IPv4 (blue)
  * Layer 3: TCP (green)
  * Layer 4: HTTP/1.1 200 OK (yellow)
  * Layer 5: Content-Type: application/proto (orange)
  * Layer 6: Protocol Buffers (purple)
  * Layer 7: JSON payload (red)

Bottom section: Zoomed view of JSON showing:
  * "TargetFile": "/Users/meep/Documents/AIMFGuideforCybersec*°·/LinkedInExploit/LINKEDIN_RESPONSE_DRAFT.md"
  * "CodeContent": "# LinkedIn HackerOne Response - Draft\n\n## Response to \"Not Realistic\" Dismissal..."

Side panel: Hex dump view showing:
  * Actual hex bytes from packet
  * ASCII representation
  * Highlighted sections showing JSON structure

- Highlight sensitive data in red
- Style: Wireshark-inspired, technical, with hex dump aesthetic
- Color code each protocol layer
- Include arrows showing data flow through layers
```

**Dimensions:** 1200x1600 (portrait)  
**File Name:** `windsurf_frame_3243_breakdown.png`

---

## Color Palette Reference

### Primary Colors
- **Purple-Blue:** `#667eea` (Windsurf brand color)
- **Deep Purple:** `#764ba2` (Secondary accent)

### Alert Colors
- **Critical/Red:** `#dc3545` (Sensitive data, security alerts)
- **Warning/Yellow:** `#ffc107` (Caution, tracking)
- **Success/Green:** `#28a745` (Verified, safe)
- **Info/Blue:** `#17a2b8` (Information, network)

### Background Colors
- **Dark Gray:** `#2d2d2d` (Main background)
- **Off-White:** `#f8f8f2` (Text on dark)
- **Light Gray:** `#f8f9fa` (Light backgrounds)

### Gradients
- **Primary Gradient:** `linear-gradient(135deg, #667eea 0%, #764ba2 100%)`
- **Alert Gradient:** `linear-gradient(135deg, #dc3545 0%, #c82333 100%)`

---

## File Organization

Save all generated images to:
```
/Users/meep/Documents/AIMFGuideforCybersec*°·/WindsurfExploit-Oct25/visuals/
```

### Naming Convention
- `windsurf_data_flow_diagram.png`
- `windsurf_investigation_timeline.png`
- `windsurf_workspace_violations.png`
- `windsurf_traffic_spikes.png`
- `windsurf_security_toolkit.png`
- `windsurf_frame_3243_breakdown.png`

---

## Usage in Report

### HTML Integration
```html
<img src="visuals/windsurf_data_flow_diagram.png" alt="Data Flow Diagram" style="width: 100%; max-width: 1200px; margin: 30px 0;">
```

### Markdown Integration
```markdown
![Data Flow Diagram](visuals/windsurf_data_flow_diagram.png)
```

---

## Additional Visual Ideas (Optional)

### 7. System Permissions Matrix
- Grid showing requested vs granted permissions
- Icons for Camera, Mic, Bluetooth, Files, Network
- Red/Green indicators

### 8. Before/After Comparison
- Split screen showing:
  - Left: 16 tracked workspaces, 110 connections, tracking IDs
  - Right: 0 tracked workspaces, 0 connections, IDs cleared

### 9. Risk Assessment Heatmap
- Matrix of file types vs sensitivity levels
- Color-coded by exposure risk

---

**Notes:**
- All visuals should maintain consistent branding (purple/blue theme)
- Use modern, professional cybersecurity aesthetic
- Include AIMF LLC branding where appropriate
- Ensure text is readable at presentation size
- Export in high resolution (300 DPI for print, 72 DPI for web)
