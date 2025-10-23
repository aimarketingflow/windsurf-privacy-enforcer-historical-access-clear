#!/usr/bin/env python3
"""
Windsurf Privacy Toolkit - GUI Application
Modern PyQt6 interface for privacy protection and tracking cleanup
"""

import sys
import os
import subprocess
import json
from pathlib import Path
from datetime import datetime

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QTextEdit, QProgressBar, QTabWidget,
    QGroupBox, QRadioButton, QButtonGroup, QCheckBox, QMessageBox,
    QFileDialog, QStatusBar, QFrame, QScrollArea, QGridLayout, QTableWidget,
    QTableWidgetItem, QHeaderView
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QTimer
from PyQt6.QtGui import QFont, QIcon, QPalette, QColor, QTextCursor


class WorkerThread(QThread):
    """Background worker thread for running shell scripts"""
    output_signal = pyqtSignal(str)
    finished_signal = pyqtSignal(bool, str)
    progress_signal = pyqtSignal(int)
    
    def __init__(self, script_path, args=None):
        super().__init__()
        self.script_path = script_path
        self.args = args or []
        self.process = None
        
    def run(self):
        try:
            cmd = [self.script_path] + self.args
            self.process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1
            )
            
            for line in iter(self.process.stdout.readline, ''):
                if line:
                    self.output_signal.emit(line.rstrip())
                    
            self.process.wait()
            
            if self.process.returncode == 0:
                self.finished_signal.emit(True, "Operation completed successfully!")
            elif self.process.returncode == 1:
                self.finished_signal.emit(False, "Operation cancelled by user")
            else:
                self.finished_signal.emit(False, f"Operation failed with code {self.process.returncode}")
                
        except Exception as e:
            self.finished_signal.emit(False, f"Error: {str(e)}")
            
    def stop(self):
        if self.process:
            self.process.terminate()


class DashboardWidget(QWidget):
    """Main dashboard showing system status"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        self.init_ui()
        
    def init_ui(self):
        # Create scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        
        # Create content widget
        content = QWidget()
        layout = QVBoxLayout()
        content.setLayout(layout)
        
        # Title
        title = QLabel("Windsurf Privacy Toolkit")
        title.setFont(QFont("Arial", 24, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        # Subtitle
        subtitle = QLabel("Complete Privacy Protection & Historical Access Deletion")
        subtitle.setFont(QFont("Arial", 12))
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setStyleSheet("color: #888;")
        layout.addWidget(subtitle)
        
        layout.addSpacing(30)
        
        # Status Grid
        status_grid = QGridLayout()
        
        # Windsurf Status
        self.windsurf_status = self.create_status_card(
            "Windsurf Status",
            "Checking...",
            "#3498db"
        )
        status_grid.addWidget(self.windsurf_status, 0, 0)
        
        # Tracking Status
        self.tracking_status = self.create_status_card(
            "Tracking Status",
            "Unknown",
            "#e74c3c"
        )
        status_grid.addWidget(self.tracking_status, 0, 1)
        
        # Chat History
        self.chat_status = self.create_status_card(
            "Chat History",
            "Not Backed Up",
            "#f39c12"
        )
        status_grid.addWidget(self.chat_status, 1, 0)
        
        # Last Cleanup
        self.cleanup_status = self.create_status_card(
            "Last Cleanup",
            "Never",
            "#95a5a6"
        )
        status_grid.addWidget(self.cleanup_status, 1, 1)
        
        layout.addLayout(status_grid)
        
        layout.addSpacing(30)
        
        # Recommendations
        self.recommendations_group = QGroupBox("📋 Recommendations")
        recommendations_layout = QVBoxLayout()
        
        self.recommendations_text = QLabel("Analyzing system...")
        self.recommendations_text.setWordWrap(True)
        self.recommendations_text.setStyleSheet("""
            QLabel {
                padding: 15px;
                background-color: #1e1e1e;
                border-radius: 5px;
                line-height: 1.6;
            }
        """)
        recommendations_layout.addWidget(self.recommendations_text)
        
        self.recommendations_group.setLayout(recommendations_layout)
        layout.addWidget(self.recommendations_group)
        
        layout.addSpacing(20)
        
        # Quick Actions
        actions_group = QGroupBox("Quick Actions")
        actions_layout = QGridLayout()
        
        self.btn_audit = QPushButton("🔍 Run Security Audit")
        self.btn_audit.setMinimumHeight(60)
        self.btn_audit.setStyleSheet(self.get_button_style("#3498db"))
        self.btn_audit.clicked.connect(self.switch_to_audit)
        actions_layout.addWidget(self.btn_audit, 0, 0)
        
        self.btn_backup = QPushButton("💾 Backup Chat History")
        self.btn_backup.setMinimumHeight(60)
        self.btn_backup.setStyleSheet(self.get_button_style("#2ecc71"))
        self.btn_backup.clicked.connect(self.switch_to_backup)
        actions_layout.addWidget(self.btn_backup, 0, 1)
        
        self.btn_cleanup = QPushButton("🧹 Enhanced Cleanup")
        self.btn_cleanup.setMinimumHeight(60)
        self.btn_cleanup.setStyleSheet(self.get_button_style("#e67e22"))
        self.btn_cleanup.clicked.connect(self.switch_to_cleanup)
        actions_layout.addWidget(self.btn_cleanup, 1, 0)
        
        self.btn_test = QPushButton("🧪 Run Tests")
        self.btn_test.setMinimumHeight(60)
        self.btn_test.setStyleSheet(self.get_button_style("#9b59b6"))
        self.btn_test.clicked.connect(self.run_tests)
        actions_layout.addWidget(self.btn_test, 1, 1)
        
        actions_group.setLayout(actions_layout)
        layout.addWidget(actions_group)
        
        layout.addStretch()
        
        # Set scroll area
        scroll.setWidget(content)
        main_layout = QVBoxLayout()
        main_layout.addWidget(scroll)
        self.setLayout(main_layout)
        
        # Update status
        self.update_status()
        
    def create_status_card(self, title, value, color):
        """Create a status card widget"""
        card = QFrame()
        card.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Raised)
        card.setLineWidth(2)
        
        card_layout = QVBoxLayout()
        
        title_label = QLabel(title)
        title_label.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        title_label.setStyleSheet(f"color: {color};")
        card_layout.addWidget(title_label)
        
        value_label = QLabel(value)
        value_label.setFont(QFont("Arial", 14))
        value_label.setWordWrap(True)
        card_layout.addWidget(value_label)
        
        card.setLayout(card_layout)
        card.setMinimumHeight(100)
        
        # Store value label for updates
        card.value_label = value_label
        
        return card
        
    def get_button_style(self, color):
        """Get button stylesheet"""
        return f"""
            QPushButton {{
                background-color: {color};
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px;
                font-size: 14px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {self.lighten_color(color)};
            }}
            QPushButton:pressed {{
                background-color: {self.darken_color(color)};
            }}
        """
        
    def lighten_color(self, hex_color):
        """Lighten a hex color"""
        # Simple lightening - increase RGB values
        return hex_color  # Simplified for now
        
    def darken_color(self, hex_color):
        """Darken a hex color"""
        return hex_color  # Simplified for now
        
    def update_status(self):
        """Update dashboard status"""
        # Check if Windsurf is running
        try:
            result = subprocess.run(
                ['pgrep', '-x', 'Windsurf'],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                self.windsurf_status.value_label.setText("Running")
                self.windsurf_status.value_label.setStyleSheet("color: #2ecc71;")
            else:
                self.windsurf_status.value_label.setText("Not Running")
                self.windsurf_status.value_label.setStyleSheet("color: #95a5a6;")
        except:
            self.windsurf_status.value_label.setText("Unknown")
            
        # Check tracking status
        storage_json = Path.home() / "Library/Application Support/Windsurf/User/globalStorage/storage.json"
        if storage_json.exists():
            try:
                with open(storage_json) as f:
                    data = json.load(f)
                    machine_id = data.get('telemetry.machineId', '')
                    if machine_id:
                        self.tracking_status.value_label.setText("Active")
                        self.tracking_status.value_label.setStyleSheet("color: #e74c3c;")
                    else:
                        self.tracking_status.value_label.setText("Cleared")
                        self.tracking_status.value_label.setStyleSheet("color: #2ecc71;")
            except:
                self.tracking_status.value_label.setText("Unknown")
        
        # Check chat backups
        backup_dir = Path.home() / "WindsurfChatBackup_*"
        backups = list(Path.home().glob("WindsurfChatBackup_*"))
        if backups:
            latest = max(backups, key=lambda p: p.stat().st_mtime)
            backup_time = datetime.fromtimestamp(latest.stat().st_mtime)
            self.chat_status.value_label.setText(f"Last: {backup_time.strftime('%Y-%m-%d %H:%M')}")
            self.chat_status.value_label.setStyleSheet("color: #2ecc71;")
        else:
            self.chat_status.value_label.setText("Not Backed Up")
            self.chat_status.value_label.setStyleSheet("color: #f39c12;")
        
        # Check last cleanup - look for backup folders and backup files in storage.json
        cleanup_files = list(Path.home().glob("windsurf_backup_*"))
        cleanup_files.extend(list(Path.home().glob("WindsurfBackups/*")))
        
        # Also check storage.json backup timestamp
        storage_backup = Path.home() / "Library/Application Support/Windsurf/User/globalStorage/storage.json.backup"
        if storage_backup.exists():
            cleanup_files.append(storage_backup)
        
        if cleanup_files:
            latest = max(cleanup_files, key=lambda p: p.stat().st_mtime)
            cleanup_time = datetime.fromtimestamp(latest.stat().st_mtime)
            self.cleanup_status.value_label.setText(f"{cleanup_time.strftime('%Y-%m-%d %H:%M')}")
            self.cleanup_status.value_label.setStyleSheet("color: #2ecc71;")
        else:
            self.cleanup_status.value_label.setText("Never")
            self.cleanup_status.value_label.setStyleSheet("color: #95a5a6;")
        
        # Update recommendations
        self.update_recommendations()
    
    def update_recommendations(self):
        """Generate intelligent recommendations based on system state"""
        recommendations = []
        priority_level = "low"
        
        # Check tracking status
        storage_json = Path.home() / "Library/Application Support/Windsurf/User/globalStorage/storage.json"
        has_tracking = False
        workspace_count = 0
        
        if storage_json.exists():
            try:
                with open(storage_json) as f:
                    data = json.load(f)
                    machine_id = data.get('telemetry.machineId', '')
                    if machine_id:
                        has_tracking = True
                        priority_level = "high"
                    
                    # Count tracked workspaces
                    profile_assoc = data.get('profileAssociations', {})
                    workspaces = profile_assoc.get('workspaces', {})
                    workspace_count = len(workspaces)
            except:
                pass
        
        # Check last cleanup
        last_cleanup_time = None
        cleanup_files = list(Path.home().glob("windsurf_backup_*"))
        if cleanup_files:
            latest = max(cleanup_files, key=lambda p: p.stat().st_mtime)
            last_cleanup_time = datetime.fromtimestamp(latest.stat().st_mtime)
        
        # Check chat backup
        chat_backups = list(Path.home().glob("WindsurfChatBackup_*"))
        last_chat_backup = None
        if chat_backups:
            latest = max(chat_backups, key=lambda p: p.stat().st_mtime)
            last_chat_backup = datetime.fromtimestamp(latest.stat().st_mtime)
        
        # Generate recommendations
        if has_tracking and workspace_count > 10:
            recommendations.append(
                f"🔴 <b>HIGH PRIORITY:</b> Tracking is active with {workspace_count} workspaces being monitored. "
                "We strongly recommend running Enhanced Cleanup to clear historical access."
            )
            priority_level = "critical"
        elif has_tracking:
            recommendations.append(
                f"🟡 <b>RECOMMENDED:</b> Tracking IDs are active. "
                "Consider running Enhanced Cleanup to remove tracking data."
            )
            priority_level = "medium"
        else:
            recommendations.append(
                "✅ <b>GOOD:</b> No active tracking IDs detected. Your privacy is protected."
            )
        
        # Last cleanup recommendation
        if last_cleanup_time:
            days_since = (datetime.now() - last_cleanup_time).days
            if days_since > 30:
                recommendations.append(
                    f"🟡 <b>MAINTENANCE:</b> Last cleanup was {days_since} days ago. "
                    "For active security research, we recommend monthly cleanups."
                )
                if priority_level == "low":
                    priority_level = "medium"
            elif days_since > 7:
                recommendations.append(
                    f"ℹ️ Last cleanup was {days_since} days ago. "
                    "Consider running cleanup if you've been working on sensitive projects."
                )
        else:
            recommendations.append(
                "🟡 <b>FIRST TIME:</b> No cleanup detected. "
                "Run your first security audit to understand your exposure."
            )
            if priority_level == "low":
                priority_level = "medium"
        
        # Chat backup recommendation
        if not chat_backups:
            recommendations.append(
                "💾 <b>BACKUP:</b> No chat history backups found. "
                "We recommend backing up your Cascade conversations before cleanup."
            )
        elif last_chat_backup:
            days_since = (datetime.now() - last_chat_backup).days
            if days_since > 7:
                recommendations.append(
                    f"💾 Chat history last backed up {days_since} days ago. "
                    "Consider creating a fresh backup."
                )
        
        # Device switching scenario
        if has_tracking and not last_cleanup_time:
            recommendations.append(
                "🔄 <b>NEW DEVICE?</b> If you're switching to a new device, "
                "run Enhanced Cleanup on your old device before migration."
            )
        
        # Sensitive work scenario
        if workspace_count > 15:
            recommendations.append(
                f"🔒 <b>PRIVACY TIP:</b> You have {workspace_count} tracked workspaces. "
                "Consider using sandboxing for sensitive security research."
            )
        
        # Format recommendations
        if recommendations:
            rec_html = "<br><br>".join(recommendations)
            
            # Add color based on priority
            if priority_level == "critical":
                self.recommendations_group.setStyleSheet("QGroupBox { color: #e74c3c; font-weight: bold; }")
            elif priority_level == "high":
                self.recommendations_group.setStyleSheet("QGroupBox { color: #e67e22; font-weight: bold; }")
            elif priority_level == "medium":
                self.recommendations_group.setStyleSheet("QGroupBox { color: #f39c12; }")
            else:
                self.recommendations_group.setStyleSheet("QGroupBox { color: #2ecc71; }")
            
            self.recommendations_text.setText(rec_html)
        else:
            self.recommendations_text.setText("✅ All systems normal. No immediate actions required.")
    
    def switch_to_audit(self):
        """Switch to audit tab"""
        if self.parent_window:
            self.parent_window.tabs.setCurrentIndex(1)
    
    def switch_to_cleanup(self):
        """Switch to cleanup tab"""
        if self.parent_window:
            self.parent_window.tabs.setCurrentIndex(2)
    
    def switch_to_backup(self):
        """Switch to backup tab"""
        if self.parent_window:
            self.parent_window.tabs.setCurrentIndex(3)
    
    def run_tests(self):
        """Run test suite"""
        script_path = Path(__file__).parent / "test_historical_access_deletion.sh"
        if script_path.exists():
            # Switch to audit tab and run tests there
            if self.parent_window:
                self.parent_window.tabs.setCurrentIndex(1)
                # Could trigger test run here
        else:
            QMessageBox.warning(self, "Error", f"Test script not found: {script_path}")


class AuditWidget(QWidget):
    """Security audit tab"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.worker = None
        self.init_ui()
        
    def init_ui(self):
        # Create scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        
        # Create content widget
        content = QWidget()
        layout = QVBoxLayout()
        content.setLayout(layout)
        
        # Title
        title = QLabel("Security Audit")
        title.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        layout.addWidget(title)
        
        # Description
        desc = QLabel("Comprehensive 10-point security assessment of Windsurf IDE")
        desc.setStyleSheet("color: #888;")
        layout.addWidget(desc)
        
        layout.addSpacing(20)
        
        # Control buttons
        btn_layout = QHBoxLayout()
        
        self.btn_run = QPushButton("▶️ Run Audit")
        self.btn_run.setMinimumHeight(40)
        self.btn_run.clicked.connect(self.run_audit)
        btn_layout.addWidget(self.btn_run)
        
        self.btn_stop = QPushButton("⏹️ Stop")
        self.btn_stop.setMinimumHeight(40)
        self.btn_stop.setEnabled(False)
        self.btn_stop.clicked.connect(self.stop_audit)
        btn_layout.addWidget(self.btn_stop)
        
        self.btn_save = QPushButton("💾 Save Report")
        self.btn_save.setMinimumHeight(40)
        self.btn_save.clicked.connect(self.save_report)
        btn_layout.addWidget(self.btn_save)
        
        layout.addLayout(btn_layout)
        
        # Progress bar
        self.progress = QProgressBar()
        self.progress.setVisible(False)
        layout.addWidget(self.progress)
        
        # Output text
        self.output = QTextEdit()
        self.output.setReadOnly(True)
        self.output.setFont(QFont("Courier", 10))
        self.output.setStyleSheet("""
            QTextEdit {
                background-color: #1e1e1e;
                color: #d4d4d4;
                border: 1px solid #3e3e3e;
                border-radius: 5px;
                padding: 10px;
            }
        """)
        layout.addWidget(self.output)
        
        # Set scroll area
        scroll.setWidget(content)
        main_layout = QVBoxLayout()
        main_layout.addWidget(scroll)
        self.setLayout(main_layout)
        
    def run_audit(self):
        """Run security audit"""
        script_path = Path(__file__).parent / "audit_windsurf_access.sh"
        
        if not script_path.exists():
            QMessageBox.warning(self, "Error", f"Audit script not found: {script_path}")
            return
            
        self.output.clear()
        self.output.append("Starting security audit...\n")
        
        self.btn_run.setEnabled(False)
        self.btn_stop.setEnabled(True)
        self.progress.setVisible(True)
        self.progress.setRange(0, 0)  # Indeterminate
        
        self.worker = WorkerThread(str(script_path))
        self.worker.output_signal.connect(self.append_output)
        self.worker.finished_signal.connect(self.audit_finished)
        self.worker.start()
        
    def stop_audit(self):
        """Stop running audit"""
        if self.worker:
            self.worker.stop()
            self.output.append("\n[Audit stopped by user]")
            
    def append_output(self, text):
        """Append text to output"""
        self.output.append(text)
        # Auto-scroll to bottom
        self.output.moveCursor(QTextCursor.MoveOperation.End)
        
    def audit_finished(self, success, message):
        """Audit completed"""
        self.btn_run.setEnabled(True)
        self.btn_stop.setEnabled(False)
        self.progress.setVisible(False)
        
        if success:
            self.output.append(f"\n✅ {message}")
        else:
            self.output.append(f"\n❌ {message}")
            
    def save_report(self):
        """Save audit report to file"""
        filename, _ = QFileDialog.getSaveFileName(
            self,
            "Save Audit Report",
            str(Path.home() / f"windsurf_audit_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"),
            "Text Files (*.txt);;All Files (*)"
        )
        
        if filename:
            try:
                with open(filename, 'w') as f:
                    f.write(self.output.toPlainText())
                QMessageBox.information(self, "Success", f"Report saved to:\n{filename}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to save report:\n{str(e)}")


class CleanupWidget(QWidget):
    """Enhanced cleanup tab"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.worker = None
        self.init_ui()
        
    def init_ui(self):
        # Create scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        
        # Create content widget
        content = QWidget()
        layout = QVBoxLayout()
        content.setLayout(layout)
        
        # Title
        title = QLabel("Enhanced Cleanup")
        title.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        layout.addWidget(title)
        
        # Description
        desc = QLabel("Complete historical access deletion with backup options")
        desc.setStyleSheet("color: #888;")
        layout.addWidget(desc)
        
        layout.addSpacing(20)
        
        # Backup options
        backup_group = QGroupBox("Backup Options")
        backup_layout = QVBoxLayout()
        
        self.backup_group = QButtonGroup()
        
        # Option 1: No backup
        self.radio_no_backup = QRadioButton("1) No backup (skip)")
        self.backup_group.addButton(self.radio_no_backup, 1)
        backup_layout.addWidget(self.radio_no_backup)
        
        no_backup_desc = QLabel("   ⚠️  Not recommended - no recovery possible")
        no_backup_desc.setStyleSheet("color: #e74c3c; font-size: 11px; margin-left: 20px;")
        backup_layout.addWidget(no_backup_desc)
        
        # Option 2: Full backup
        self.radio_full_backup = QRadioButton("2) Full backup (all Windsurf data)")
        self.backup_group.addButton(self.radio_full_backup, 2)
        backup_layout.addWidget(self.radio_full_backup)
        
        full_backup_desc = QLabel(
            "   Includes: Settings, extensions, workspaces, cache, logs (~200 MB)\n"
            "   Complete copy of entire Windsurf directory"
        )
        full_backup_desc.setStyleSheet("color: #888; font-size: 11px; margin-left: 20px;")
        full_backup_desc.setWordWrap(True)
        backup_layout.addWidget(full_backup_desc)
        
        # Option 3: Chat only
        self.radio_chat_only = QRadioButton("3) Chat history only (recommended)")
        self.radio_chat_only.setChecked(True)
        self.backup_group.addButton(self.radio_chat_only, 3)
        backup_layout.addWidget(self.radio_chat_only)
        
        chat_only_desc = QLabel(
            "   Includes: All Cascade conversations exported to CSV/JSON (~1 MB)\n"
            "   ✅ Fast, lightweight, easy to view in Excel"
        )
        chat_only_desc.setStyleSheet("color: #2ecc71; font-size: 11px; margin-left: 20px;")
        chat_only_desc.setWordWrap(True)
        backup_layout.addWidget(chat_only_desc)
        
        # Option 4: Full + Chat export
        self.radio_full_plus_chat = QRadioButton("4) Full backup + separate chat export")
        self.backup_group.addButton(self.radio_full_plus_chat, 4)
        backup_layout.addWidget(self.radio_full_plus_chat)
        
        full_plus_desc = QLabel(
            "   Includes: Everything from option 2 (~200 MB)\n"
            "   PLUS: Readable chat exports in CSV/JSON format\n"
            "   Best for: Maximum safety + easy chat viewing"
        )
        full_plus_desc.setStyleSheet("color: #3498db; font-size: 11px; margin-left: 20px;")
        full_plus_desc.setWordWrap(True)
        backup_layout.addWidget(full_plus_desc)
        
        backup_group.setLayout(backup_layout)
        layout.addWidget(backup_group)
        
        # Python environment preservation option
        preserve_group = QGroupBox("Python Environment Preservation")
        preserve_layout = QVBoxLayout()
        
        self.preserve_venv = QCheckBox("Preserve Python virtual environments")
        self.preserve_venv.setChecked(True)  # Default to preserving
        preserve_layout.addWidget(self.preserve_venv)
        
        preserve_desc = QLabel(
            "   This will protect:\n"
            "   • venv/ directories\n"
            "   • .venv/ directories\n"
            "   • env/ directories\n"
            "   • requirements.txt files\n"
            "   • Python interpreter settings\n\n"
            "   ✅ Recommended: Keep checked to avoid reinstalling packages"
        )
        preserve_desc.setStyleSheet("color: #2ecc71; font-size: 11px; margin-left: 20px;")
        preserve_desc.setWordWrap(True)
        preserve_layout.addWidget(preserve_desc)
        
        preserve_group.setLayout(preserve_layout)
        layout.addWidget(preserve_group)
        
        # MachineID prevention option
        machineid_group = QGroupBox("MachineID Regeneration Prevention")
        machineid_layout = QVBoxLayout()

        self.prevent_machineid = QCheckBox("Prevent MachineID regeneration after cleanup")
        self.prevent_machineid.setChecked(True)  # Default to preventing
        machineid_layout.addWidget(self.prevent_machineid)

        machineid_desc = QLabel(
            "   This will protect:\n"
            "   • Makes storage.json read-only\n"
            "   • Prevents Windsurf from recreating tracking IDs\n"
            "   • Maintains privacy after cleanup\n"
            "   • Can be reversed if needed\n\n"
            "   ✅ Recommended: Keep checked for maximum privacy"
        )
        machineid_desc.setStyleSheet("color: #e74c3c; font-size: 11px; margin-left: 20px;")
        machineid_desc.setWordWrap(True)
        machineid_layout.addWidget(machineid_desc)

        machineid_group.setLayout(machineid_layout)
        layout.addWidget(machineid_group)
        
        # Warning
        warning = QLabel(
            "⚠️  <b>WARNING: This will COMPLETELY clear ALL workspace history!</b><br><br>"
            "<b>What gets DELETED:</b><br>"
            "• Machine/Device tracking IDs (cross-session profiling)<br>"
            "• ALL 16+ workspace associations (directory tracking)<br>"
            "• Backup workspace history<br>"
            "• Recent file history<br>"
            "• ~26 MB of tracking data and cache<br><br>"
            "<b>What gets PRESERVED:</b><br>"
            "✅ User settings and preferences<br>"
            "✅ Installed extensions<br>"
            "✅ Custom keybindings<br>"
            "✅ Chat history with Cascade<br>"
            "✅ GitHub/Windsurf authentication (no re-login needed)"
        )
        warning.setStyleSheet("""
            QLabel {
                color: #e74c3c; 
                font-weight: bold; 
                padding: 15px; 
                background-color: #2c1e1e; 
                border-radius: 5px;
                border: 2px solid #e74c3c;
                line-height: 1.6;
            }
        """)
        warning.setWordWrap(True)
        layout.addWidget(warning)
        
        # Control buttons
        btn_layout = QHBoxLayout()
        
        self.btn_run = QPushButton("🧹 Run Cleanup")
        self.btn_run.setMinimumHeight(40)
        self.btn_run.clicked.connect(self.run_cleanup)
        btn_layout.addWidget(self.btn_run)
        
        self.btn_stop = QPushButton("⏹️ Stop")
        self.btn_stop.setMinimumHeight(40)
        self.btn_stop.setEnabled(False)
        btn_layout.addWidget(self.btn_stop)
        
        layout.addLayout(btn_layout)
        
        # Progress bar
        self.progress = QProgressBar()
        self.progress.setVisible(False)
        layout.addWidget(self.progress)
        
        # Output text
        self.output = QTextEdit()
        self.output.setReadOnly(True)
        self.output.setFont(QFont("Courier", 10))
        self.output.setStyleSheet("""
            QTextEdit {
                background-color: #1e1e1e;
                color: #d4d4d4;
                border: 1px solid #3e3e3e;
                border-radius: 5px;
                padding: 10px;
            }
        """)
        layout.addWidget(self.output)
        
        # Set scroll area
        scroll.setWidget(content)
        main_layout = QVBoxLayout()
        main_layout.addWidget(scroll)
        self.setLayout(main_layout)
        
    def run_cleanup(self):
        """Run enhanced cleanup"""
        # Get selected backup option
        backup_option = self.backup_group.checkedId()
        backup_text = {
            1: "No backup",
            2: "Full backup",
            3: "Chat history only",
            4: "Full backup + chat export"
        }.get(backup_option, "Unknown")
        
        # Get venv preservation option
        preserve_venv = self.preserve_venv.isChecked()
        preserve_text = "y" if preserve_venv else "n"
        
        # Get MachineID prevention option
        prevent_machineid = self.prevent_machineid.isChecked()
        
        # Confirmation dialog
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Icon.Warning)
        msg.setWindowTitle("Confirm Enhanced Cleanup")
        msg.setText("<b>Are you sure you want to run the enhanced cleanup?</b>")
        
        preserved_items = (
            "✅ User settings<br>"
            "✅ Extensions<br>"
            "✅ Keybindings<br>"
            "✅ Chat history with Cascade<br>"
            "✅ GitHub/Windsurf authentication"
        )
        
        if preserve_venv:
            preserved_items += (
                "<br>✅ Python virtual environments (venv/, .venv/, env/)<br>"
                "✅ requirements.txt files<br>"
                "✅ Python interpreter settings"
            )
        
        msg.setInformativeText(
            f"<b>Backup Option:</b> {backup_text}<br>"
            f"<b>Preserve Python Environments:</b> {'Yes' if preserve_venv else 'No'}<br>"
            f"<b>Prevent MachineID Regeneration:</b> {'Yes' if prevent_machineid else 'No'}<br><br>"
            "<b>What will be DELETED:</b><br>"
            "• Machine/Device tracking IDs<br>"
            "• ALL workspace associations (16+ directories)<br>"
            "• Backup workspace history<br>"
            "• Recent file history<br>"
            "• ~26 MB tracking data and cache<br><br>"
            f"<b>What will be PRESERVED:</b><br>"
            f"{preserved_items}<br><br>"
            "<b>This action cannot be undone without a backup!</b>"
        )
        msg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        msg.setDefaultButton(QMessageBox.StandardButton.No)
        reply = msg.exec()
        
        if reply != QMessageBox.StandardButton.Yes:
            return
            
        script_path = Path(__file__).parent / "clear_windsurf_tracking_ENHANCED.sh"
        
        if not script_path.exists():
            QMessageBox.warning(self, "Error", f"Cleanup script not found: {script_path}")
            return
            
        self.output.clear()
        self.output.append("Starting enhanced cleanup...\n")
        self.output.append(f"Backup option: {backup_option} ({backup_text})\n")
        self.output.append(f"Preserve Python environments: {'Yes' if preserve_venv else 'No'}\n")
        self.output.append(f"Prevent MachineID regeneration: {'Yes' if prevent_machineid else 'No'}\n")
        self.output.append("Creating wrapper script to handle interactive prompts...\n")
        
        # Create a wrapper script that auto-answers the prompts
        wrapper_script = Path(__file__).parent / "cleanup_wrapper_gui.sh"
        prevent_script = Path(__file__).parent / "prevent_machineid_regeneration.sh"
        wrapper_content = f"""#!/bin/bash
# Auto-generated wrapper for GUI cleanup
# Automatically answers prompts for non-interactive execution

# Auto-answer: quit Windsurf (y), preserve venv ({preserve_text}), backup option ({backup_option}), confirm (yes)
echo "y
{preserve_text}
{backup_option}
yes" | "{script_path}"

# Run MachineID prevention if requested
if [ "{'true' if prevent_machineid else 'false'}" = "true" ]; then
    echo ""
    echo "Running MachineID prevention..."
    "{prevent_script}"
fi
"""
        
        try:
            with open(wrapper_script, 'w') as f:
                f.write(wrapper_content)
            wrapper_script.chmod(0o755)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to create wrapper script:\n{str(e)}")
            return
        
        self.btn_run.setEnabled(False)
        self.btn_stop.setEnabled(True)
        self.progress.setVisible(True)
        self.progress.setRange(0, 10)
        self.progress.setValue(0)
        
        self.worker = WorkerThread(str(wrapper_script))
        self.worker.output_signal.connect(self.append_output)
        self.worker.finished_signal.connect(self.cleanup_finished)
        self.worker.progress_signal.connect(self.progress.setValue)
        self.worker.start()
        
    def append_output(self, text):
        """Append text to output"""
        self.output.append(text)
        self.output.moveCursor(QTextCursor.MoveOperation.End)
        
        # Update progress based on output
        if "[1/10]" in text or "Step 1/" in text:
            self.progress.setValue(1)
        elif "[2/10]" in text or "Step 2/" in text:
            self.progress.setValue(2)
        elif "[3/10]" in text or "Step 3/" in text:
            self.progress.setValue(3)
        elif "[4/10]" in text or "Step 4/" in text:
            self.progress.setValue(4)
        elif "[5/10]" in text or "Step 5/" in text:
            self.progress.setValue(5)
        elif "[6/10]" in text or "Step 6/" in text:
            self.progress.setValue(6)
        elif "[7/10]" in text or "Step 7/" in text:
            self.progress.setValue(7)
        elif "[8/10]" in text or "Step 8/" in text:
            self.progress.setValue(8)
        elif "[9/10]" in text or "Step 9/" in text:
            self.progress.setValue(9)
        elif "[10/10]" in text or "Step 10/" in text or "COMPLETE" in text or "✅ All done" in text:
            self.progress.setValue(10)
            
    def cleanup_finished(self, success, message):
        """Cleanup completed"""
        self.btn_run.setEnabled(True)
        self.btn_stop.setEnabled(False)
        self.progress.setValue(10)  # Ensure progress reaches 100%
        
        if success:
            self.output.append(f"\n✅ {message}")
            QMessageBox.information(self, "Success", "Cleanup completed successfully!")
        else:
            self.output.append(f"\n❌ {message}")
            QMessageBox.warning(self, "Error", f"Cleanup failed:\n{message}")


class BackupsWidget(QWidget):
    """Comprehensive backups management tab"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.worker = None
        self.backup_base_dir = Path.home() / "WindsurfBackups"
        self.backup_base_dir.mkdir(exist_ok=True)
        self.init_ui()
        
    def init_ui(self):
        # Create scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        
        # Create content widget
        content = QWidget()
        layout = QVBoxLayout()
        content.setLayout(layout)
        
        # Title
        title = QLabel("Backups & Exports")
        title.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        layout.addWidget(title)
        
        # Description
        desc = QLabel("Manage all Windsurf backups, exports, and audit reports")
        desc.setStyleSheet("color: #888;")
        layout.addWidget(desc)
        
        layout.addSpacing(20)
        
        # Backup type selector
        type_group = QGroupBox("Backup Type")
        type_layout = QGridLayout()
        
        # Chat History Backup
        self.btn_chat = QPushButton("💬 Chat History")
        self.btn_chat.setMinimumHeight(50)
        self.btn_chat.setStyleSheet(self.get_button_style("#2ecc71"))
        self.btn_chat.clicked.connect(self.backup_chat)
        type_layout.addWidget(self.btn_chat, 0, 0)
        
        chat_desc = QLabel("Export conversations\nCSV/JSON (~1 MB)")
        chat_desc.setStyleSheet("color: #888; font-size: 10px;")
        chat_desc.setAlignment(Qt.AlignmentFlag.AlignCenter)
        type_layout.addWidget(chat_desc, 1, 0)
        
        # Audit Report
        self.btn_audit = QPushButton("🔍 Audit Report")
        self.btn_audit.setMinimumHeight(50)
        self.btn_audit.setStyleSheet(self.get_button_style("#3498db"))
        self.btn_audit.clicked.connect(self.save_audit)
        type_layout.addWidget(self.btn_audit, 0, 1)
        
        audit_desc = QLabel("Save security audit\nText/JSON format")
        audit_desc.setStyleSheet("color: #888; font-size: 10px;")
        audit_desc.setAlignment(Qt.AlignmentFlag.AlignCenter)
        type_layout.addWidget(audit_desc, 1, 1)
        
        # Full Backup
        self.btn_full = QPushButton("📦 Full Backup")
        self.btn_full.setMinimumHeight(50)
        self.btn_full.setStyleSheet(self.get_button_style("#9b59b6"))
        self.btn_full.clicked.connect(self.backup_full)
        type_layout.addWidget(self.btn_full, 0, 2)
        
        full_desc = QLabel("Complete backup\nAll data (~200 MB)")
        full_desc.setStyleSheet("color: #888; font-size: 10px;")
        full_desc.setAlignment(Qt.AlignmentFlag.AlignCenter)
        type_layout.addWidget(full_desc, 1, 2)
        
        type_group.setLayout(type_layout)
        layout.addWidget(type_group)
        
        # Export/Import section
        export_group = QGroupBox("Export & Import")
        export_layout = QHBoxLayout()
        
        self.btn_export = QPushButton("📤 Export Package")
        self.btn_export.setMinimumHeight(40)
        self.btn_export.setToolTip("Create importable package for another Windsurf instance")
        self.btn_export.clicked.connect(self.export_package)
        export_layout.addWidget(self.btn_export)
        
        self.btn_import = QPushButton("📥 Import Package")
        self.btn_import.setMinimumHeight(40)
        self.btn_import.setToolTip("Import settings and data from another instance")
        self.btn_import.clicked.connect(self.import_package)
        export_layout.addWidget(self.btn_import)
        
        export_group.setLayout(export_layout)
        layout.addWidget(export_group)
        
        # Backup browser
        browser_group = QGroupBox("Backup History")
        browser_layout = QVBoxLayout()
        
        # Control buttons
        btn_layout = QHBoxLayout()
        
        self.btn_open = QPushButton("📂 Open Backup Folder")
        self.btn_open.setMinimumHeight(35)
        self.btn_open.clicked.connect(self.open_backup_folder)
        btn_layout.addWidget(self.btn_open)
        
        self.btn_refresh = QPushButton("🔄 Refresh")
        self.btn_refresh.setMinimumHeight(35)
        self.btn_refresh.clicked.connect(self.refresh_backup_list)
        btn_layout.addWidget(self.btn_refresh)
        
        browser_layout.addLayout(btn_layout)
        
        # Backup list
        self.backup_list = QTextEdit()
        self.backup_list.setReadOnly(True)
        self.backup_list.setMaximumHeight(150)
        self.backup_list.setFont(QFont("Courier", 10))
        self.backup_list.setStyleSheet("""
            QTextEdit {
                background-color: #1e1e1e;
                color: #d4d4d4;
                border: 1px solid #3e3e3e;
                border-radius: 5px;
                padding: 10px;
            }
        """)
        browser_layout.addWidget(self.backup_list)
        
        browser_group.setLayout(browser_layout)
        layout.addWidget(browser_group)
        
        # Progress bar
        self.progress = QProgressBar()
        self.progress.setVisible(False)
        layout.addWidget(self.progress)
        
        # Output text
        self.output = QTextEdit()
        self.output.setReadOnly(True)
        self.output.setFont(QFont("Courier", 10))
        self.output.setStyleSheet("""
            QTextEdit {
                background-color: #1e1e1e;
                color: #d4d4d4;
                border: 1px solid #3e3e3e;
                border-radius: 5px;
                padding: 10px;
            }
        """)
        layout.addWidget(self.output)
        
        # Set scroll area
        scroll.setWidget(content)
        main_layout = QVBoxLayout()
        main_layout.addWidget(scroll)
        self.setLayout(main_layout)
        
        # Initial refresh
        self.refresh_backup_list()
    
    def get_button_style(self, color):
        """Get button stylesheet"""
        return f"""
            QPushButton {{
                background-color: {color};
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px;
                font-size: 12px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                opacity: 0.8;
            }}
        """
    
    def backup_chat(self):
        """Backup chat history"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_dir = self.backup_base_dir / "ChatHistory" / f"chat_{timestamp}"
        backup_dir.mkdir(parents=True, exist_ok=True)
        
        script_path = Path(__file__).parent / "backup_windsurf_chat.sh"
        
        if not script_path.exists():
            QMessageBox.warning(self, "Error", f"Backup script not found: {script_path}")
            return
            
        self.output.clear()
        self.output.append(f"Starting chat history backup...\nSaving to: {backup_dir}\n")
        
        self.progress.setVisible(True)
        self.progress.setRange(0, 0)
        
        self.worker = WorkerThread(str(script_path))
        self.worker.output_signal.connect(self.append_output)
        self.worker.finished_signal.connect(lambda s, m: self.backup_finished(s, m, "Chat History"))
        self.worker.start()
    
    def save_audit(self):
        """Save audit report"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        audit_dir = self.backup_base_dir / "AuditReports"
        audit_dir.mkdir(parents=True, exist_ok=True)
        
        script_path = Path(__file__).parent / "audit_windsurf_access.sh"
        
        if not script_path.exists():
            QMessageBox.warning(self, "Error", f"Audit script not found: {script_path}")
            return
        
        self.output.clear()
        self.output.append(f"Running security audit...\nSaving to: {audit_dir}\n")
        
        self.progress.setVisible(True)
        self.progress.setRange(0, 0)
        
        # Run audit and save output
        self.worker = WorkerThread(str(script_path))
        self.worker.output_signal.connect(self.append_output)
        self.worker.finished_signal.connect(lambda s, m: self.save_audit_finished(s, m, audit_dir, timestamp))
        self.worker.start()
    
    def save_audit_finished(self, success, message, audit_dir, timestamp):
        """Save audit output to file"""
        self.progress.setVisible(False)
        
        if success:
            # Save the output
            audit_file = audit_dir / f"audit_{timestamp}.txt"
            try:
                with open(audit_file, 'w') as f:
                    f.write(self.output.toPlainText())
                
                self.output.append(f"\n✅ Audit report saved: {audit_file}")
                self.refresh_backup_list()
                QMessageBox.information(self, "Success", f"Audit report saved to:\n{audit_file}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to save audit:\n{str(e)}")
        else:
            self.output.append(f"\n❌ {message}")
    
    def backup_full(self):
        """Create full backup"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_dir = self.backup_base_dir / "FullBackups" / f"full_{timestamp}"
        backup_dir.mkdir(parents=True, exist_ok=True)
        
        self.output.clear()
        self.output.append(f"Creating full backup...\nSaving to: {backup_dir}\n")
        
        self.progress.setVisible(True)
        self.progress.setRange(0, 100)
        self.progress.setValue(0)
        
        # Copy entire Windsurf directory
        source = Path.home() / "Library/Application Support/Windsurf"
        
        if not source.exists():
            QMessageBox.warning(self, "Error", "Windsurf directory not found")
            self.progress.setVisible(False)
            return
        
        try:
            import shutil
            self.output.append("Copying Windsurf directory...\n")
            self.progress.setValue(25)
            
            shutil.copytree(source, backup_dir / "Windsurf", dirs_exist_ok=True)
            
            self.progress.setValue(100)
            self.output.append(f"\n✅ Full backup completed: {backup_dir}")
            self.refresh_backup_list()
            QMessageBox.information(self, "Success", f"Full backup saved to:\n{backup_dir}")
        except Exception as e:
            self.output.append(f"\n❌ Error: {str(e)}")
            QMessageBox.critical(self, "Error", f"Backup failed:\n{str(e)}")
        finally:
            self.progress.setVisible(False)
    
    def export_package(self):
        """Export package for import to another instance"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        export_dir = self.backup_base_dir / "ExportPackages"
        export_dir.mkdir(parents=True, exist_ok=True)
        
        package_file = export_dir / f"windsurf_export_{timestamp}.tar.gz"
        
        # Create package with settings, extensions, and chat
        source = Path.home() / "Library/Application Support/Windsurf"
        
        if not source.exists():
            QMessageBox.warning(self, "Error", "Windsurf directory not found")
            return
        
        self.output.clear()
        self.output.append(f"Creating export package...\n")
        self.progress.setVisible(True)
        self.progress.setRange(0, 0)
        
        try:
            import tarfile
            
            with tarfile.open(package_file, "w:gz") as tar:
                # Add settings
                settings = source / "User/settings.json"
                if settings.exists():
                    tar.add(settings, arcname="settings.json")
                    self.output.append("✓ Added settings.json\n")
                
                # Add keybindings
                keybindings = source / "User/keybindings.json"
                if keybindings.exists():
                    tar.add(keybindings, arcname="keybindings.json")
                    self.output.append("✓ Added keybindings.json\n")
                
                # Add chat history
                workspace_storage = source / "User/workspaceStorage"
                if workspace_storage.exists():
                    for workspace in workspace_storage.iterdir():
                        if workspace.is_dir():
                            state_db = workspace / "state.vscdb"
                            if state_db.exists():
                                tar.add(state_db, arcname=f"workspaces/{workspace.name}/state.vscdb")
                    self.output.append("✓ Added chat history\n")
                
                # Add manifest
                manifest = {
                    "export_date": timestamp,
                    "version": "1.0",
                    "contents": ["settings", "keybindings", "chat_history"]
                }
                import json
                manifest_path = export_dir / "manifest.json"
                with open(manifest_path, 'w') as f:
                    json.dump(manifest, f, indent=2)
                tar.add(manifest_path, arcname="manifest.json")
                manifest_path.unlink()
                self.output.append("✓ Added manifest\n")
            
            self.output.append(f"\n✅ Export package created: {package_file}")
            self.refresh_backup_list()
            QMessageBox.information(
                self,
                "Success",
                f"Export package created!\n\n{package_file}\n\n"
                "You can import this on another Windsurf instance."
            )
        except Exception as e:
            self.output.append(f"\n❌ Error: {str(e)}")
            QMessageBox.critical(self, "Error", f"Export failed:\n{str(e)}")
        finally:
            self.progress.setVisible(False)
    
    def import_package(self):
        """Import package from another instance"""
        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Select Export Package",
            str(self.backup_base_dir / "ExportPackages"),
            "Tar Archives (*.tar.gz);;All Files (*)"
        )
        
        if not filename:
            return
        
        # Confirm import
        reply = QMessageBox.question(
            self,
            "Confirm Import",
            "This will import settings and data from another Windsurf instance.\n\n"
            "Current settings may be overwritten.\n\n"
            "Continue?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply != QMessageBox.StandardButton.Yes:
            return
        
        self.output.clear()
        self.output.append(f"Importing package: {filename}\n")
        self.progress.setVisible(True)
        self.progress.setRange(0, 0)
        
        try:
            import tarfile
            import shutil
            
            dest = Path.home() / "Library/Application Support/Windsurf"
            
            with tarfile.open(filename, "r:gz") as tar:
                # Extract manifest
                manifest_member = tar.getmember("manifest.json")
                manifest_file = tar.extractfile(manifest_member)
                import json
                manifest = json.load(manifest_file)
                
                self.output.append(f"Package version: {manifest.get('version')}\n")
                self.output.append(f"Export date: {manifest.get('export_date')}\n\n")
                
                # Extract settings
                if "settings.json" in tar.getnames():
                    tar.extract("settings.json", path="/tmp")
                    shutil.copy("/tmp/settings.json", dest / "User/settings.json")
                    self.output.append("✓ Imported settings.json\n")
                
                # Extract keybindings
                if "keybindings.json" in tar.getnames():
                    tar.extract("keybindings.json", path="/tmp")
                    shutil.copy("/tmp/keybindings.json", dest / "User/keybindings.json")
                    self.output.append("✓ Imported keybindings.json\n")
                
                # Extract workspaces
                workspace_members = [m for m in tar.getmembers() if m.name.startswith("workspaces/")]
                for member in workspace_members:
                    tar.extract(member, path="/tmp")
                    workspace_id = member.name.split("/")[1]
                    workspace_dir = dest / "User/workspaceStorage" / workspace_id
                    workspace_dir.mkdir(parents=True, exist_ok=True)
                    shutil.copy(f"/tmp/{member.name}", workspace_dir / "state.vscdb")
                
                if workspace_members:
                    self.output.append(f"✓ Imported {len(workspace_members)} workspace(s)\n")
            
            self.output.append("\n✅ Import completed successfully!")
            QMessageBox.information(
                self,
                "Success",
                "Import completed!\n\nRestart Windsurf to apply changes."
            )
        except Exception as e:
            self.output.append(f"\n❌ Error: {str(e)}")
            QMessageBox.critical(self, "Error", f"Import failed:\n{str(e)}")
        finally:
            self.progress.setVisible(False)
    
    def refresh_backup_list(self):
        """Refresh the backup list"""
        self.backup_list.clear()
        self.backup_list.append("📁 Available Backups:\n")
        self.backup_list.append("=" * 60 + "\n\n")
        
        # Chat backups
        chat_dir = self.backup_base_dir / "ChatHistory"
        if chat_dir.exists():
            chats = sorted(chat_dir.glob("chat_*"), reverse=True)
            if chats:
                self.backup_list.append("💬 Chat History Backups:\n")
                for chat in chats[:5]:  # Show last 5
                    size = sum(f.stat().st_size for f in chat.rglob('*') if f.is_file()) / 1024 / 1024
                    mtime = datetime.fromtimestamp(chat.stat().st_mtime)
                    self.backup_list.append(f"  • {chat.name} ({size:.1f} MB) - {mtime.strftime('%Y-%m-%d %H:%M')}\n")
                self.backup_list.append("\n")
        
        # Audit reports
        audit_dir = self.backup_base_dir / "AuditReports"
        if audit_dir.exists():
            audits = sorted(audit_dir.glob("audit_*"), reverse=True)
            if audits:
                self.backup_list.append("🔍 Audit Reports:\n")
                for audit in audits[:5]:
                    size = audit.stat().st_size / 1024
                    mtime = datetime.fromtimestamp(audit.stat().st_mtime)
                    self.backup_list.append(f"  • {audit.name} ({size:.1f} KB) - {mtime.strftime('%Y-%m-%d %H:%M')}\n")
                self.backup_list.append("\n")
        
        # Full backups
        full_dir = self.backup_base_dir / "FullBackups"
        if full_dir.exists():
            fulls = sorted(full_dir.glob("full_*"), reverse=True)
            if fulls:
                self.backup_list.append("📦 Full Backups:\n")
                for full in fulls[:3]:
                    size = sum(f.stat().st_size for f in full.rglob('*') if f.is_file()) / 1024 / 1024
                    mtime = datetime.fromtimestamp(full.stat().st_mtime)
                    self.backup_list.append(f"  • {full.name} ({size:.1f} MB) - {mtime.strftime('%Y-%m-%d %H:%M')}\n")
                self.backup_list.append("\n")
        
        # Export packages
        export_dir = self.backup_base_dir / "ExportPackages"
        if export_dir.exists():
            exports = sorted(export_dir.glob("windsurf_export_*"), reverse=True)
            if exports:
                self.backup_list.append("📤 Export Packages:\n")
                for export in exports[:3]:
                    size = export.stat().st_size / 1024 / 1024
                    mtime = datetime.fromtimestamp(export.stat().st_mtime)
                    self.backup_list.append(f"  • {export.name} ({size:.1f} MB) - {mtime.strftime('%Y-%m-%d %H:%M')}\n")
        
        if not any([
            (self.backup_base_dir / "ChatHistory").exists(),
            (self.backup_base_dir / "AuditReports").exists(),
            (self.backup_base_dir / "FullBackups").exists(),
            (self.backup_base_dir / "ExportPackages").exists()
        ]):
            self.backup_list.append("No backups found. Create your first backup above!")
        
        self.backup_list.moveCursor(QTextCursor.MoveOperation.Start)
    
    def append_output(self, text):
        """Append text to output"""
        self.output.append(text)
        self.output.moveCursor(QTextCursor.MoveOperation.End)
    
    def backup_finished(self, success, message, backup_type):
        """Backup completed"""
        self.progress.setVisible(False)
        
        if success:
            self.output.append(f"\n✅ {backup_type} backup completed!")
            self.refresh_backup_list()
        else:
            self.output.append(f"\n❌ {message}")
    
    def open_backup_folder(self):
        """Open the backup base folder"""
        subprocess.run(['open', str(self.backup_base_dir)])


class NetworkMonitorWidget(QWidget):
    """Network monitoring and blocking tab"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.timer = None
        self.init_ui()
        
    def init_ui(self):
        # Create scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        
        # Create content widget
        content = QWidget()
        layout = QVBoxLayout()
        content.setLayout(layout)
        
        # Title
        title = QLabel("Network Monitor & Firewall")
        title.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        layout.addWidget(title)
        
        # Description
        desc = QLabel("Monitor Windsurf connections and block tracking servers")
        desc.setStyleSheet("color: #888;")
        layout.addWidget(desc)
        
        layout.addSpacing(20)
        
        # Control buttons
        btn_layout = QHBoxLayout()
        
        self.btn_refresh = QPushButton("🔄 Refresh Now")
        self.btn_refresh.setMinimumHeight(40)
        self.btn_refresh.clicked.connect(self.refresh_connections)
        btn_layout.addWidget(self.btn_refresh)
        
        self.btn_auto = QPushButton("⏱️ Auto-Refresh (5s)")
        self.btn_auto.setMinimumHeight(40)
        self.btn_auto.setCheckable(True)
        self.btn_auto.clicked.connect(self.toggle_auto_refresh)
        btn_layout.addWidget(self.btn_auto)
        
        self.btn_track = QPushButton("🔍 Track Google Cloud")
        self.btn_track.setMinimumHeight(40)
        self.btn_track.setStyleSheet("""
            QPushButton {
                background-color: #f39c12;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px;
                font-size: 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #e67e22;
            }
        """)
        self.btn_track.clicked.connect(self.track_google_cloud)
        btn_layout.addWidget(self.btn_track)
        
        self.btn_block = QPushButton("🚫 Block Google Cloud")
        self.btn_block.setMinimumHeight(40)
        self.btn_block.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px;
                font-size: 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        self.btn_block.clicked.connect(self.block_google_cloud)
        btn_layout.addWidget(self.btn_block)
        
        layout.addLayout(btn_layout)
        
        # Stats
        stats_group = QGroupBox("Connection Statistics")
        stats_layout = QGridLayout()
        
        self.stat_total = QLabel("0")
        self.stat_total.setFont(QFont("Arial", 24, QFont.Weight.Bold))
        self.stat_total.setStyleSheet("color: #3498db;")
        stats_layout.addWidget(QLabel("Total Connections:"), 0, 0)
        stats_layout.addWidget(self.stat_total, 0, 1)
        
        self.stat_external = QLabel("0")
        self.stat_external.setFont(QFont("Arial", 24, QFont.Weight.Bold))
        self.stat_external.setStyleSheet("color: #e74c3c;")
        stats_layout.addWidget(QLabel("External Connections:"), 0, 2)
        stats_layout.addWidget(self.stat_external, 0, 3)
        
        self.stat_language = QLabel("0")
        self.stat_language.setFont(QFont("Arial", 24, QFont.Weight.Bold))
        self.stat_language.setStyleSheet("color: #f39c12;")
        stats_layout.addWidget(QLabel("Language Server:"), 1, 0)
        stats_layout.addWidget(self.stat_language, 1, 1)
        
        self.stat_google = QLabel("0")
        self.stat_google.setFont(QFont("Arial", 24, QFont.Weight.Bold))
        self.stat_google.setStyleSheet("color: #e67e22;")
        stats_layout.addWidget(QLabel("Google Cloud:"), 1, 2)
        stats_layout.addWidget(self.stat_google, 1, 3)
        
        stats_group.setLayout(stats_layout)
        layout.addWidget(stats_group)
        
        # Connection table
        table_group = QGroupBox("Active Connections")
        table_layout = QVBoxLayout()
        
        self.connection_table = QTableWidget()
        self.connection_table.setColumnCount(5)
        self.connection_table.setHorizontalHeaderLabels(["PID", "Type", "Local", "Remote", "Status"])
        self.connection_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.connection_table.setStyleSheet("""
            QTableWidget {
                background-color: #1e1e1e;
                color: #d4d4d4;
                border: 1px solid #3e3e3e;
                border-radius: 5px;
            }
            QHeaderView::section {
                background-color: #2b2b2b;
                color: #ffffff;
                padding: 5px;
                border: 1px solid #3e3e3e;
            }
        """)
        table_layout.addWidget(self.connection_table)
        
        table_group.setLayout(table_layout)
        layout.addWidget(table_group)
        
        # Language Server Details
        lang_group = QGroupBox("Language Server Connections")
        lang_layout = QVBoxLayout()
        
        self.lang_output = QTextEdit()
        self.lang_output.setReadOnly(True)
        self.lang_output.setMaximumHeight(150)
        self.lang_output.setFont(QFont("Courier", 10))
        self.lang_output.setStyleSheet("""
            QTextEdit {
                background-color: #1e1e1e;
                color: #d4d4d4;
                border: 1px solid #3e3e3e;
                border-radius: 5px;
                padding: 10px;
            }
        """)
        lang_layout.addWidget(self.lang_output)
        
        lang_group.setLayout(lang_layout)
        layout.addWidget(lang_group)
        
        # Set scroll area
        scroll.setWidget(content)
        main_layout = QVBoxLayout()
        main_layout.addWidget(scroll)
        self.setLayout(main_layout)
        
        # Initial refresh
        self.refresh_connections()
    
    def refresh_connections(self):
        """Refresh connection list"""
        try:
            # Get Windsurf connections
            result = subprocess.run(
                ['lsof', '-i', '-n', '-P'],
                capture_output=True,
                text=True
            )
            
            lines = result.stdout.split('\n')
            windsurf_connections = [line for line in lines if 'Windsurf' in line or 'language_server' in line]
            
            # Parse connections
            total = len(windsurf_connections)
            external = 0
            language_server = 0
            google_cloud = 0
            
            self.connection_table.setRowCount(0)
            
            for line in windsurf_connections:
                if not line.strip():
                    continue
                    
                parts = line.split()
                if len(parts) < 8:
                    continue
                
                command = parts[0]
                pid = parts[1]
                conn_type = parts[4] if len(parts) > 4 else ""
                
                # Find the connection info (look for ->)
                local = ""
                remote = ""
                status = ""
                
                for i, part in enumerate(parts):
                    if '->' in part:
                        local = parts[i-1] if i > 0 else ""
                        remote = part.split('->')[1] if '->' in part else ""
                        status = parts[i+1] if i+1 < len(parts) else ""
                        break
                
                # Count specific types
                if 'language_server' in command or 'language_server' in line.lower():
                    language_server += 1
                
                # Check for Google Cloud in the entire line
                if '34.49.14.144' in line or '178.238.223.35' in line or 'googleusercontent.com' in line:
                    google_cloud += 1
                    external += 1
                elif remote and '127.0.0.1' not in remote and 'localhost' not in remote and remote != '*:*':
                    external += 1
                
                # Add to table (limit to 50 rows)
                if self.connection_table.rowCount() < 50:
                    row = self.connection_table.rowCount()
                    self.connection_table.insertRow(row)
                    self.connection_table.setItem(row, 0, QTableWidgetItem(pid))
                    self.connection_table.setItem(row, 1, QTableWidgetItem(conn_type))
                    self.connection_table.setItem(row, 2, QTableWidgetItem(local))
                    self.connection_table.setItem(row, 3, QTableWidgetItem(remote))
                    self.connection_table.setItem(row, 4, QTableWidgetItem(status))
                    
                    # Highlight external connections
                    if '127.0.0.1' not in remote and 'localhost' not in remote:
                        for col in range(5):
                            item = self.connection_table.item(row, col)
                            if item:
                                item.setBackground(QColor("#3e2723"))
            
            # Update stats
            self.stat_total.setText(str(total))
            self.stat_external.setText(str(external))
            self.stat_language.setText(str(language_server))
            self.stat_google.setText(str(google_cloud))
            
            # Update language server details
            self.update_language_server_details()
            
        except Exception as e:
            self.lang_output.setText(f"Error refreshing connections: {str(e)}")
    
    def update_language_server_details(self):
        """Update language server connection details"""
        try:
            result = subprocess.run(
                ['lsof', '-i', '-n', '-P'],
                capture_output=True,
                text=True
            )
            
            # Look for language_server in process name or connections
            lang_connections = [line for line in result.stdout.split('\n') 
                              if 'language_server' in line.lower() or 
                              ('Windsurf' in line and ('60983' in line or '58041' in line))]
            
            self.lang_output.clear()
            self.lang_output.append(f"Language Server Connections: {len(lang_connections)}\n")
            self.lang_output.append("=" * 60 + "\n")
            
            if lang_connections:
                for line in lang_connections[:20]:  # Show first 20
                    if line.strip():
                        self.lang_output.append(line + "\n")
            else:
                self.lang_output.append("No language server connections detected.\n")
                self.lang_output.append("\nNote: Language server typically uses ports:\n")
                self.lang_output.append("  - 60983 (common)\n")
                self.lang_output.append("  - 58041 (common)\n")
                    
        except Exception as e:
            self.lang_output.append(f"Error: {str(e)}")
    
    def toggle_auto_refresh(self, checked):
        """Toggle auto-refresh"""
        if checked:
            self.timer = QTimer()
            self.timer.timeout.connect(self.refresh_connections)
            self.timer.start(5000)  # 5 seconds
            self.btn_auto.setText("⏹️ Stop Auto-Refresh")
        else:
            if self.timer:
                self.timer.stop()
                self.timer = None
            self.btn_auto.setText("⏱️ Auto-Refresh (5s)")
    
    def track_google_cloud(self):
        """Start tracking Google Cloud connections"""
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Icon.Information)
        msg.setWindowTitle("Track Google Cloud Connections")
        msg.setText("<b>Start detailed connection tracking?</b>")
        msg.setInformativeText(
            "This will monitor all traffic to:\n\n"
            "• 34.49.14.144 (Google Cloud)\n"
            "• 178.238.223.35 (Google Cloud)\n"
            "• *.googleusercontent.com\n\n"
            "Tracking includes:\n"
            "• Connection timestamps\n"
            "• Process IDs\n"
            "• Destination IPs\n"
            "• Connection counts\n\n"
            "Logs saved to: ~/windsurf_cloud_tracking/\n\n"
            "For deep packet analysis (requires sudo):\n"
            "Run: ./track_google_cloud_packets.sh"
        )
        msg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        reply = msg.exec()
        
        if reply == QMessageBox.StandardButton.Yes:
            script_path = Path(__file__).parent / "track_google_cloud_connections.sh"
            
            if not script_path.exists():
                QMessageBox.warning(self, "Error", f"Tracking script not found: {script_path}")
                return
            
            # Run in terminal so user can see output and stop it
            subprocess.Popen([
                'open', '-a', 'Terminal',
                str(script_path)
            ])
            
            QMessageBox.information(
                self,
                "Tracking Started",
                "Google Cloud connection tracking started in Terminal.\n\n"
                "Press Ctrl+C in the Terminal to stop tracking.\n\n"
                "Logs will be saved to:\n"
                "~/windsurf_cloud_tracking/"
            )
    
    def block_google_cloud(self):
        """Block Google Cloud connections"""
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Icon.Warning)
        msg.setWindowTitle("Block Google Cloud Connections")
        msg.setText("<b>Block telemetry to Google Cloud servers?</b>")
        msg.setInformativeText(
            "This will add firewall rules to block:\n\n"
            "• *.googleusercontent.com\n"
            "• 34.49.14.144 (Google Cloud)\n"
            "• 178.238.223.35 (Google Cloud)\n\n"
            "Requires admin password.\n\n"
            "Note: This may affect some Windsurf features."
        )
        msg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        reply = msg.exec()
        
        if reply == QMessageBox.StandardButton.Yes:
            # Create firewall rules
            script = """#!/bin/bash
# Block Google Cloud telemetry
echo "Adding firewall rules..."

# Block specific IPs
sudo pfctl -t windsurf_block -T add 34.49.14.144 2>/dev/null
sudo pfctl -t windsurf_block -T add 178.238.223.35 2>/dev/null

echo "Firewall rules added!"
echo "To remove: sudo pfctl -t windsurf_block -T flush"
"""
            
            QMessageBox.information(
                self,
                "Firewall Script",
                f"Firewall blocking requires manual setup.\n\n"
                f"Run this script with sudo:\n\n{script}\n\n"
                f"Or use the sandbox_windsurf.sh script for complete isolation."
            )


class MainWindow(QMainWindow):
    """Main application window"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle("Windsurf Privacy Toolkit")
        self.setGeometry(100, 100, 1000, 700)
        
        # Central widget with tabs
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout()
        central_widget.setLayout(layout)
        
        # Tab widget
        self.tabs = QTabWidget()
        
        # Add tabs (pass self as parent so dashboard can access tabs)
        self.tabs.addTab(DashboardWidget(self), "🏠 Dashboard")
        self.tabs.addTab(AuditWidget(), "🔍 Audit")
        self.tabs.addTab(CleanupWidget(), "🧹 Cleanup")
        self.tabs.addTab(BackupsWidget(), "💾 Backups")
        self.tabs.addTab(NetworkMonitorWidget(), "🌐 Network Monitor")
        
        layout.addWidget(self.tabs)
        
        # Status bar
        self.statusBar().showMessage("Ready")
        
        # Apply dark theme
        self.apply_dark_theme()
        
    def apply_dark_theme(self):
        """Apply dark theme to application"""
        dark_stylesheet = """
            QMainWindow {
                background-color: #2b2b2b;
            }
            QWidget {
                background-color: #2b2b2b;
                color: #ffffff;
            }
            QTabWidget::pane {
                border: 1px solid #3e3e3e;
                background-color: #2b2b2b;
            }
            QTabBar::tab {
                background-color: #3e3e3e;
                color: #ffffff;
                padding: 10px 20px;
                margin-right: 2px;
            }
            QTabBar::tab:selected {
                background-color: #4e4e4e;
            }
            QGroupBox {
                border: 2px solid #3e3e3e;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
                font-weight: bold;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #5dade2;
            }
            QPushButton:pressed {
                background-color: #2980b9;
            }
            QPushButton:disabled {
                background-color: #555;
                color: #888;
            }
            QRadioButton {
                spacing: 5px;
                padding: 5px;
            }
            QRadioButton::indicator {
                width: 15px;
                height: 15px;
            }
            QProgressBar {
                border: 1px solid #3e3e3e;
                border-radius: 5px;
                text-align: center;
                background-color: #1e1e1e;
            }
            QProgressBar::chunk {
                background-color: #3498db;
                border-radius: 5px;
            }
            QStatusBar {
                background-color: #1e1e1e;
                color: #888;
            }
        """
        self.setStyleSheet(dark_stylesheet)


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Windsurf Privacy Toolkit")
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
