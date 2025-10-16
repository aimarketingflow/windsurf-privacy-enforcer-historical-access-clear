# Visual Prompts Quick Reference Guide
**For Windsurf Security Report**

## 🎯 Quick Start

This guide provides streamlined prompts for generating visuals for the Windsurf security report. Each prompt is optimized for AI image generators (DALL-E, Midjourney, Stable Diffusion, etc.).

---

## 📋 Prompt Summary Table

| # | Visual Name | Type | Dimensions | Priority | File Name |
|---|-------------|------|------------|----------|-----------|
| 1 | Data Flow Diagram | Technical Diagram | 1920x1080 | HIGH | `windsurf_data_flow.png` |
| 2 | Investigation Timeline | Infographic | 2400x800 | HIGH | `windsurf_timeline.png` |
| 3 | Workspace Violations | Network Map | 1920x1080 | CRITICAL | `windsurf_workspace_violations.png` |
| 4 | Traffic Spike Chart | Data Visualization | 1600x900 | MEDIUM | `windsurf_traffic_spikes.png` |
| 5 | Security Toolkit | Dashboard | 1920x1080 | HIGH | `windsurf_toolkit_dashboard.png` |
| 6 | Frame 3243 Breakdown | Packet Analysis | 1200x1600 | CRITICAL | `windsurf_frame3243.png` |

---

## 🎨 Universal Style Guide

**Color Palette:**
```
Primary:    #667eea (purple-blue)
Secondary:  #764ba2 (deep purple)
Critical:   #dc3545 (red)
Warning:    #ffc107 (yellow/gold)
Success:    #28a745 (green)
Background: #2d2d2d (dark gray)
Text:       #f8f8f2 (off-white)
```

**Design Principles:**
- Modern, technical cybersecurity aesthetic
- Dark backgrounds with bright accents
- Clear hierarchy and readability
- Professional, not playful
- Data-driven and evidence-based

---

## 🚀 Copy-Paste Prompts

### Prompt 1: Data Flow Diagram ⭐ HIGH PRIORITY

```
Create a technical network diagram showing Windsurf IDE data exfiltration architecture. Dark background (#2d2d2d). Left side: MacBook with 16 folder icons labeled with security-related names (Stealthshark2, HackRFOne, AntiPineapple, etc). Center: Two process boxes labeled "language_server_macos_arm" and "Windsurf Helper" with CPU activity indicators. Right side: Data flow arrows showing Protocol Buffers serialization, loopback connections (127.0.0.1 - 106,754 packets), and external connection to Google Cloud (35.223.238.178:443). Bottom: Storage database icons showing tracking IDs. Color code: Red for sensitive data flows, yellow for tracking, blue for network. Modern cybersecurity style, technical, professional. 1920x1080 landscape.
```

**Key Elements:** MacBook, folder icons, process boxes, arrows, Google Cloud endpoint, color-coded flows

---

### Prompt 2: Investigation Timeline ⭐ HIGH PRIORITY

```
Create a horizontal timeline infographic on dark background. Timeline spans October 6-11, 2025. Key milestones: Oct 6 17:06 (network spike icon, "Initial Discovery"), Oct 6 17:50 (capture icon, "93 MB PCAP"), Oct 11 15:30 (magnifying glass, "Second Capture"), Oct 11 15:38:45 (explosion/lightbulb, "BREAKTHROUGH - Frame 3243", highlighted in gold), Oct 11 16:25 (checkmark, "85 MB Complete"), Oct 11 17:00 (shield, "Solution Toolkit"). Include packet counts and data sizes. Gradient purple-blue colors (#667eea to #764ba2). Modern, clean design. 2400x800 wide banner.
```

**Key Elements:** Timeline bar, milestone markers, icons, data annotations, breakthrough highlight

---

### Prompt 3: Workspace Violations ⭐⭐ CRITICAL

```
Create a network graph visualization showing workspace boundary violations. Dark background. Center: Large circle labeled "Opened Workspace (AIMFGuideforCybersec)". Radiating outward: 16 nodes representing unauthorized directories. Each node has icon and label: Stealthshark2 (shark, red), HackRFOne-SignalTesting (radio tower, red), AntiPineapple (pineapple with X, red), _Murus_Firewall_Optimizer (firewall, red), SunoVocalStemz (music note, yellow), MidiVisualizer (waveform, green), etc. Connecting lines from center to each node showing Windsurf's unauthorized access. Legend: Red=Security Research (Critical), Yellow=Personal (Medium), Green=Media (Low). Cybersecurity theme, network graph style. 1920x1080 landscape.
```

**Key Elements:** Central node, 16 radiating nodes, color-coded by sensitivity, connecting lines, legend

---

### Prompt 4: Traffic Spike Analysis

```
Create a modern data visualization chart showing network traffic over time. Dark background. X-axis: Time (0-3337 seconds). Y-axis: Data rate (kBps) and packet count. Area chart with multiple colored spikes: 480-540s (8.7 MB, orange spike), 2400-2460s (4.5 MB, yellow spike), 3240-3300s (9.5 MB, red spike), 3300-3337s (13.5 MB EXTREME spike, dark red, 364 kBps, tallest). Annotations showing what was transmitted at each spike. Background gradient from blue (normal) to red (critical). Professional analytics dashboard style. 1600x900 landscape.
```

**Key Elements:** Time-series chart, multiple spikes, annotations, gradient background, data labels

---

### Prompt 5: Security Toolkit Dashboard ⭐ HIGH PRIORITY

```
Create a modern dashboard showing 4 security tools in 2x2 grid. Dark background with purple-blue gradient. Top-left: "audit_windsurf_access.sh" with magnifying glass icon, "10 checks performed", green/red status dots. Top-right: "clear_windsurf_tracking.sh" with broom icon, "16 workspaces cleared, 140 MB freed", before/after bars. Bottom-left: "sandbox_windsurf.sh" with lock/shield icon, "5 restrictions applied", icons for blocked camera/mic/network/bluetooth. Bottom-right: "verify_cleanup.sh" with checkmark icon, "8 verification tests", pass/fail indicators. Modern UI design, clean icons, professional. 1920x1080 landscape.
```

**Key Elements:** 2x2 grid, tool names, icons, metrics, status indicators, modern UI

---

### Prompt 6: Frame 3243 Packet Breakdown ⭐⭐ CRITICAL

```
Create a detailed packet visualization showing network packet layers. Dark background. Top: Header showing "Frame 3243, 637 bytes, Oct 11 2025 15:38:45 PDT". Middle: 6 protocol layers stacked vertically, each color-coded: NULL/Loopback (gray), IP (blue), TCP (green), HTTP/1.1 (purple), Protocol Buffers (orange), JSON payload (red). Each layer shows brief details. Bottom: Zoomed JSON section showing "TargetFile": "/Users/meep/.../LINKEDIN_RESPONSE_DRAFT.md" and "CodeContent": "# LinkedIn HackerOne Response..." with sensitive data highlighted in red. Wireshark-inspired style, technical, with hex dump aesthetic. Color-coded layers. 1200x1600 portrait.
```

**Key Elements:** Packet header, 6 stacked protocol layers, JSON zoom, color coding, technical style

---

## 📝 Usage Instructions

### For AI Image Generators:

1. **DALL-E 3 (ChatGPT/Bing):**
   - Copy prompt directly
   - May need to simplify complex technical terms
   - Works best with Prompts 2, 4, 5

2. **Midjourney:**
   - Add `--ar 16:9` for landscape or `--ar 3:4` for portrait
   - Add `--style raw` for technical diagrams
   - Works best with Prompts 1, 3, 6

3. **Stable Diffusion:**
   - Use with technical/diagram-focused models
   - May need negative prompts: "cartoon, anime, unrealistic, blurry"
   - Works best with all prompts

4. **Manual Design (Figma/Illustrator):**
   - Use prompts as design specifications
   - Follow color palette exactly
   - Refer to detailed version in VISUAL_PROMPTS.md

### Integration Steps:

1. Generate images using prompts above
2. Save with specified filenames
3. Create `/visuals/` directory in project root
4. Place images in `/visuals/` folder
5. Update HTML report image references:

```html
<img src="visuals/windsurf_data_flow.png" alt="Data Flow Diagram" style="width: 100%; border-radius: 8px; margin: 20px 0;">
```

---

## 🎯 Priority Order

**Start with these 3 (Critical):**
1. ✅ Prompt 3: Workspace Violations (shows privacy breach)
2. ✅ Prompt 6: Frame 3243 (smoking gun evidence)
3. ✅ Prompt 2: Timeline (tells the story)

**Then add these (High value):**
4. ✅ Prompt 1: Data Flow (technical architecture)
5. ✅ Prompt 5: Toolkit Dashboard (solution)

**Optional (Nice to have):**
6. ✅ Prompt 4: Traffic Spikes (supporting data)

---

## 🔧 Customization Tips

### Adjust for Your Tool:

**If using DALL-E:**
- Simplify technical jargon
- Focus on visual metaphors
- Example: "network diagram" instead of "Protocol Buffers serialization"

**If using Midjourney:**
- Add style parameters: `--style raw --quality 2`
- Use aspect ratio flags: `--ar 16:9`
- Reference style: "in the style of technical documentation"

**If using Designer/Figma:**
- Use prompts as wireframe specifications
- Follow exact color codes provided
- Refer to detailed VISUAL_PROMPTS.md for element lists

### Quick Modifications:

**Make it lighter:** Change background to `#f8f9fa`, text to `#1a1a1a`
**More dramatic:** Increase red usage, add glow effects
**More corporate:** Use blues instead of purples, remove dark background
**Print-friendly:** Use white background, high contrast colors

---

## 📦 Deliverables Checklist

- [ ] Generate 6 images using prompts
- [ ] Save with correct filenames
- [ ] Create `/visuals/` directory
- [ ] Place images in directory
- [ ] Update HTML report with `<img>` tags
- [ ] Test HTML report rendering
- [ ] Verify all images display correctly
- [ ] Export final report as PDF

---

## 🆘 Troubleshooting

**Image generator refuses prompt:**
- Remove "hacking" or "exploit" terms
- Use "security research" instead
- Focus on abstract diagrams

**Colors don't match:**
- Use exact hex codes provided
- Post-process in image editor
- Adjust in CSS if needed

**Wrong dimensions:**
- Resize in image editor
- Use CSS to constrain: `max-width: 100%; height: auto;`

**Text not readable:**
- Increase font sizes in prompt
- Add "large, readable text" to prompt
- Post-process to add text overlays

---

## 📚 Additional Resources

- **Full Prompts:** See `VISUAL_PROMPTS.md` for detailed versions
- **HTML Report:** `Windsurf_Complete_Security_Report.html`
- **Analysis Summary:** `COMPLETE_WINDSURF_ANALYSIS_SUMMARY.md`
- **Evidence Files:** See `/RecentPCAPs/` directory

---

## ✅ Quick Validation

After generating images, verify:
- [ ] Colors match palette (#667eea, #764ba2, #dc3545, etc.)
- [ ] Dimensions are correct (check table above)
- [ ] Text is readable at intended size
- [ ] Style matches cybersecurity/technical theme
- [ ] All key elements present (check prompt descriptions)
- [ ] Files named correctly
- [ ] Images integrate well with HTML report

---

**Last Updated:** October 11, 2025  
**Version:** 1.0  
**For:** Windsurf IDE Complete Security Analysis Report
