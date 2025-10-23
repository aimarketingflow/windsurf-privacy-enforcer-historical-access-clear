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
    QTableWidgetItem, QHeaderView, QDialog
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


class PermissionsWidget(QWidget):
    """System permissions tab - Camera, Microphone, Full Disk Access, etc."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Title
        title = QLabel("System Permissions")
        title.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        layout.addWidget(title)
        
        desc = QLabel(
            "View macOS system permissions granted to Windsurf. "
            "This includes Camera, Microphone, Full Disk Access, Bluetooth, and other system-level permissions."
        )
        desc.setWordWrap(True)
        desc.setStyleSheet("color: #95a5a6; margin-bottom: 15px;")
        layout.addWidget(desc)
        
        # Refresh button
        btn_layout = QHBoxLayout()
        self.btn_refresh = QPushButton("🔄 Refresh Permissions")
        self.btn_refresh.clicked.connect(self.load_permissions)
        btn_layout.addWidget(self.btn_refresh)
        btn_layout.addStretch()
        layout.addLayout(btn_layout)
        
        # Scroll area for permissions
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; }")
        
        content = QWidget()
        self.content_layout = QVBoxLayout()
        content.setLayout(self.content_layout)
        scroll.setWidget(content)
        
        layout.addWidget(scroll)
        self.setLayout(layout)
        
        # Load permissions on init
        self.load_permissions()
        
    def load_permissions(self):
        """Load and display all permissions"""
        # Clear existing content
        while self.content_layout.count():
            child = self.content_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        
        self.content_layout.addWidget(QLabel("Loading permissions..."))
        QApplication.processEvents()
        
        # Clear loading message
        while self.content_layout.count():
            child = self.content_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        
        # Add permission sections (system permissions only)
        self.add_macos_permissions()
        self.add_full_disk_access()
        self.add_network_permissions()
        
        self.content_layout.addStretch()
        
    def add_macos_permissions(self):
        """Add macOS privacy permissions section"""
        group = QGroupBox("🔐 macOS Privacy Permissions")
        layout = QVBoxLayout()
        
        try:
            import subprocess
            result = subprocess.run(
                ['defaults', 'read', '/Applications/Windsurf.app/Contents/Info.plist'],
                capture_output=True,
                text=True
            )
            
            plist_content = result.stdout
            permissions = []
            
            if 'NSCameraUsageDescription' in plist_content:
                permissions.append(("📷 Camera", "Requested", "#e67e22"))
            if 'NSMicrophoneUsageDescription' in plist_content:
                permissions.append(("🎤 Microphone", "Requested", "#e67e22"))
            if 'NSBluetoothAlwaysUsageDescription' in plist_content:
                permissions.append(("📡 Bluetooth", "Requested", "#e67e22"))
            if 'NSAppleEventsUsageDescription' in plist_content:
                permissions.append(("⚡ AppleScript/Automation", "Requested", "#e67e22"))
            
            if permissions:
                for name, status, color in permissions:
                    perm_label = QLabel(f"{name}: <b style='color: {color};'>{status}</b>")
                    layout.addWidget(perm_label)
            else:
                layout.addWidget(QLabel("✅ No special permissions requested"))
                
        except Exception as e:
            layout.addWidget(QLabel(f"❌ Error reading permissions: {str(e)}"))
        
        info = QLabel(
            "\n💡 <b>To check actual granted permissions:</b>\n"
            "System Settings → Privacy & Security → [Permission Type]\n"
            "Look for 'Windsurf' in the list"
        )
        info.setWordWrap(True)
        info.setStyleSheet("color: #3498db; font-size: 11px; margin-top: 10px;")
        layout.addWidget(info)
        
        group.setLayout(layout)
        self.content_layout.addWidget(group)
        
    def add_full_disk_access(self):
        """Add Full Disk Access section"""
        group = QGroupBox("💾 Full Disk Access")
        layout = QVBoxLayout()
        
        try:
            import os
            test_path = os.path.expanduser("~/Library/Safari/History.db")
            has_fda = os.access(test_path, os.R_OK) if os.path.exists(test_path) else False
            
            if has_fda:
                status_label = QLabel("⚠️ <b style='color: #e74c3c;'>GRANTED</b> - Windsurf has Full Disk Access")
                layout.addWidget(status_label)
                
                warning = QLabel(
                    "This means Windsurf can read:\n"
                    "• All files on your system\n"
                    "• Browser history and cookies\n"
                    "• Mail and messages\n"
                    "• Any protected data\n\n"
                    "⚠️ Consider revoking if not needed!"
                )
                warning.setStyleSheet("color: #e74c3c; margin-left: 20px;")
                warning.setWordWrap(True)
                layout.addWidget(warning)
            else:
                status_label = QLabel("✅ <b style='color: #2ecc71;'>NOT GRANTED</b> - Limited access only")
                layout.addWidget(status_label)
                
        except Exception as e:
            layout.addWidget(QLabel(f"❓ Unable to determine FDA status: {str(e)}"))
        
        info = QLabel(
            "\n💡 <b>To check/revoke Full Disk Access:</b>\n"
            "System Settings → Privacy & Security → Full Disk Access\n"
            "Uncheck 'Windsurf' if present"
        )
        info.setWordWrap(True)
        info.setStyleSheet("color: #3498db; font-size: 11px; margin-top: 10px;")
        layout.addWidget(info)
        
        group.setLayout(layout)
        self.content_layout.addWidget(group)
        
    def add_network_permissions(self):
        """Add network permissions section"""
        group = QGroupBox("🌐 Network Access")
        layout = QVBoxLayout()
        
        layout.addWidget(QLabel("<b>Network Permissions:</b>"))
        layout.addWidget(QLabel("  ✅ Outgoing connections: <b>Allowed</b> (default for all apps)"))
        
        try:
            import subprocess
            result = subprocess.run(['lsof', '-i', '-n', '-P'], capture_output=True, text=True)
            windsurf_connections = [line for line in result.stdout.split('\n') if 'Windsurf' in line]
            
            if windsurf_connections:
                layout.addWidget(QLabel(f"\n<b>Active Connections:</b> {len(windsurf_connections)}"))
        except:
            pass
        
        info = QLabel(
            "\n💡 <b>To manage network access:</b>\n"
            "System Settings → Network → Firewall\n"
            "Or use the Network Monitor tab for real-time tracking"
        )
        info.setWordWrap(True)
        info.setStyleSheet("color: #3498db; font-size: 11px; margin-top: 10px;")
        layout.addWidget(info)
        
        group.setLayout(layout)
        self.content_layout.addWidget(group)


class GlobalAccessWidget(QWidget):
    """Global folder access analysis tab"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Title
        title = QLabel("Global Folder Access Analysis")
        title.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        layout.addWidget(title)
        
        desc = QLabel(
            "Analyze which top-level system folders Windsurf has accessed. "
            "Identify if sensitive locations like Desktop, Downloads, or Library have been accessed."
        )
        desc.setWordWrap(True)
        desc.setStyleSheet("color: #95a5a6; margin-bottom: 15px;")
        layout.addWidget(desc)
        
        # Scan button
        btn_layout = QHBoxLayout()
        self.btn_scan = QPushButton("🔍 Scan Global Access")
        self.btn_scan.clicked.connect(self.scan_global_access)
        self.btn_scan.setStyleSheet("background-color: #3498db;")
        btn_layout.addWidget(self.btn_scan)
        
        self.btn_lock_documents = QPushButton("🔒 Lock to Documents Only")
        self.btn_lock_documents.clicked.connect(self.lock_to_documents)
        self.btn_lock_documents.setStyleSheet("background-color: #27ae60;")
        self.btn_lock_documents.setVisible(False)
        btn_layout.addWidget(self.btn_lock_documents)
        
        self.btn_view_log = QPushButton("📋 View Change Log")
        self.btn_view_log.clicked.connect(self.view_change_log)
        self.btn_view_log.setStyleSheet("background-color: #95a5a6;")
        btn_layout.addWidget(self.btn_view_log)
        
        btn_layout.addStretch()
        layout.addLayout(btn_layout)
        
        # Summary label
        self.summary_label = QLabel("Click 'Scan Global Access' to analyze...")
        self.summary_label.setStyleSheet("color: #95a5a6; padding: 10px; font-size: 14px;")
        layout.addWidget(self.summary_label)
        
        # Results table
        self.results_table = QTableWidget()
        self.results_table.setColumnCount(4)
        self.results_table.setHorizontalHeaderLabels(["Location", "Folder Count", "Examples (click to expand)", "Status"])
        self.results_table.horizontalHeader().setStretchLastSection(True)
        self.results_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.results_table.setSortingEnabled(True)
        self.results_table.setAlternatingRowColors(True)
        self.results_table.cellClicked.connect(self.on_cell_clicked)  # Add click handler
        self.expanded_rows = {}  # Track expanded state
        self.results_table.setStyleSheet("""
            QTableWidget {
                background-color: #1e1e1e;
                alternate-background-color: #2d2d2d;
                color: #ffffff;
                gridline-color: #3d3d3d;
                border: 1px solid #3d3d3d;
            }
            QTableWidget::item {
                padding: 5px;
            }
            QTableWidget::item:selected {
                background-color: #3498db;
            }
            QHeaderView::section {
                background-color: #2c3e50;
                color: #ffffff;
                padding: 8px;
                border: 1px solid #34495e;
                font-weight: bold;
            }
            QHeaderView::section:hover {
                background-color: #34495e;
            }
        """)
        self.results_table.setVisible(False)
        layout.addWidget(self.results_table)
        
        # Remove button
        self.btn_remove = QPushButton("🗑️ Remove All Access to Selected Location")
        self.btn_remove.clicked.connect(self.remove_location_access)
        self.btn_remove.setStyleSheet("background-color: #e74c3c;")
        self.btn_remove.setVisible(False)
        layout.addWidget(self.btn_remove)
        
        self.setLayout(layout)
        
    def scan_global_access(self):
        """Scan and display global folder access"""
        import os
        import sqlite3
        import json
        import urllib.parse
        from collections import defaultdict
        
        # Show table and buttons
        self.results_table.setVisible(True)
        self.btn_remove.setVisible(True)
        self.results_table.setRowCount(0)
        self.expanded_rows = {}  # Reset expanded state
        self.folder_data = {}  # Store full folder lists
        self.current_locations = []  # Track current locations for lock button
        
        try:
            global_db = os.path.expanduser("~/Library/Application Support/Windsurf/User/globalStorage/state.vscdb")
            
            conn = sqlite3.connect(global_db)
            cursor = conn.cursor()
            cursor.execute("SELECT value FROM ItemTable WHERE key = 'history.recentlyOpenedPathsList' LIMIT 1")
            row = cursor.fetchone()
            
            if row and row[0]:
                data = json.loads(row[0])
                entries = data.get('entries', [])
                
                # Analyze by top-level directory
                global_access = defaultdict(list)
                
                for entry in entries:
                    folder_uri = entry.get('folderUri')
                    if folder_uri:
                        folder_path = urllib.parse.unquote(folder_uri.replace('file://', ''))
                        
                        if folder_path.startswith('/Users/meep/Documents'):
                            global_access['📄 Documents'].append(folder_path)
                        elif folder_path.startswith('/Users/meep/Desktop'):
                            global_access['🖥️ Desktop'].append(folder_path)
                        elif folder_path.startswith('/Users/meep/Downloads'):
                            global_access['⬇️ Downloads'].append(folder_path)
                        elif folder_path.startswith('/Users/meep/Library'):
                            global_access['📚 Library'].append(folder_path)
                        elif folder_path.startswith('/Users/meep/Pictures'):
                            global_access['🖼️ Pictures'].append(folder_path)
                        elif folder_path.startswith('/Users/meep/Movies'):
                            global_access['🎬 Movies'].append(folder_path)
                        elif folder_path.startswith('/Users/meep/Music'):
                            global_access['🎵 Music'].append(folder_path)
                
                # Populate table
                total_folders = sum(len(paths) for paths in global_access.values())
                
                # Update summary
                if len(global_access) == 1 and '📄 Documents' in global_access:
                    assessment = "<span style='color: #2ecc71;'><b>✅ EXCELLENT</b> - Access limited to Documents only</span>"
                elif '📚 Library' in global_access:
                    assessment = "<span style='color: #e74c3c;'><b>⚠️ HIGH RISK</b> - Library access detected (Full Disk Access?)</span>"
                elif '🖥️ Desktop' in global_access or '⬇️ Downloads' in global_access:
                    assessment = "<span style='color: #e67e22;'><b>⚠️ MODERATE RISK</b> - Sensitive locations accessed</span>"
                else:
                    assessment = "<span style='color: #2ecc71;'><b>✅ GOOD</b> - No sensitive folders accessed</span>"
                
                self.summary_label.setText(f"<b>Total Folders Tracked:</b> {total_folders} | {assessment}")
                
                # Store current locations and show lock button if needed
                self.current_locations = list(global_access.keys())
                if len(global_access) > 1 or (len(global_access) == 1 and '📄 Documents' not in global_access):
                    self.btn_lock_documents.setVisible(True)
                else:
                    self.btn_lock_documents.setVisible(False)
                
                # Populate table rows
                self.results_table.setRowCount(len(global_access))
                for row, (location, paths) in enumerate(sorted(global_access.items(), key=lambda x: len(x[1]), reverse=True)):
                    count = len(paths)
                    
                    # Store full folder list for this location
                    self.folder_data[location] = paths
                    
                    # Location
                    self.results_table.setItem(row, 0, QTableWidgetItem(location))
                    
                    # Count
                    self.results_table.setItem(row, 1, QTableWidgetItem(str(count)))
                    
                    # Examples (first 3) with click hint
                    examples = ", ".join([os.path.basename(p) for p in paths[:3]])
                    if len(paths) > 3:
                        examples += f" ... 🔽 click to show all {len(paths)} folders"
                    examples_item = QTableWidgetItem(examples)
                    examples_item.setForeground(QColor("#3498db"))  # Blue to indicate clickable
                    self.results_table.setItem(row, 2, examples_item)
                    
                    # Status
                    if count > 10:
                        status = "🔴 High Access"
                    elif count > 5:
                        status = "🟠 Medium Access"
                    else:
                        status = "🟢 Low Access"
                    self.results_table.setItem(row, 3, QTableWidgetItem(status))
                
                self.results_table.resizeColumnsToContents()
            
            conn.close()
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to scan:\n{str(e)}")
    
    def on_cell_clicked(self, row, column):
        """Handle cell click to expand/collapse folder list"""
        import os
        
        # Only handle clicks on Examples column (column 2)
        if column != 2:
            return
        
        location = self.results_table.item(row, 0).text()
        
        # Check if this location has folders to expand
        if location not in self.folder_data:
            return
        
        paths = self.folder_data[location]
        if len(paths) <= 3:
            return  # Nothing to expand
        
        # Toggle expanded state
        if location in self.expanded_rows and self.expanded_rows[location]:
            # Collapse - show summary
            self.expanded_rows[location] = False
            examples = ", ".join([os.path.basename(p) for p in paths[:3]])
            examples += f" ... 🔽 click to show all {len(paths)} folders"
            examples_item = QTableWidgetItem(examples)
            examples_item.setForeground(QColor("#3498db"))
            self.results_table.setItem(row, 2, examples_item)
        else:
            # Expand - show all folders
            self.expanded_rows[location] = True
            all_folders = "\n".join([f"  • {os.path.basename(p)}" for p in paths])
            all_folders = f"🔼 click to collapse\n{all_folders}"
            examples_item = QTableWidgetItem(all_folders)
            examples_item.setForeground(QColor("#2ecc71"))
            self.results_table.setItem(row, 2, examples_item)
            
            # Adjust row height to fit content
            self.results_table.resizeRowToContents(row)
    
    def remove_location_access(self):
        """Remove all folders from selected location"""
        import os
        import sqlite3
        import json
        import urllib.parse
        
        # Get selected row
        selected_rows = self.results_table.selectionModel().selectedRows()
        if not selected_rows:
            QMessageBox.warning(self, "No Selection", "Please select a location to remove.")
            return
        
        row = selected_rows[0].row()
        location = self.results_table.item(row, 0).text()
        count = self.results_table.item(row, 1).text()
        
        # Confirmation
        reply = QMessageBox.question(
            self,
            "Remove Location Access",
            f"Remove all {count} folders from {location}?\n\n"
            "This will remove tracking for all folders in this location.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply != QMessageBox.StandardButton.Yes:
            return
        
        try:
            global_db = os.path.expanduser("~/Library/Application Support/Windsurf/User/globalStorage/state.vscdb")
            
            conn = sqlite3.connect(global_db)
            cursor = conn.cursor()
            cursor.execute("SELECT value FROM ItemTable WHERE key = 'history.recentlyOpenedPathsList' LIMIT 1")
            row_data = cursor.fetchone()
            
            if row_data and row_data[0]:
                data = json.loads(row_data[0])
                entries = data.get('entries', [])
                
                # Determine path prefix based on location
                location_map = {
                    '📄 Documents': '/Users/meep/Documents',
                    '🖥️ Desktop': '/Users/meep/Desktop',
                    '⬇️ Downloads': '/Users/meep/Downloads',
                    '📚 Library': '/Users/meep/Library',
                    '🖼️ Pictures': '/Users/meep/Pictures',
                    '🎬 Movies': '/Users/meep/Movies',
                    '🎵 Music': '/Users/meep/Music',
                }
                
                path_prefix = location_map.get(location)
                if not path_prefix:
                    QMessageBox.warning(self, "Error", "Unknown location")
                    return
                
                # Remove entries matching this location
                new_entries = []
                removed_count = 0
                for entry in entries:
                    folder_uri = entry.get('folderUri', '')
                    folder_path = urllib.parse.unquote(folder_uri.replace('file://', ''))
                    
                    if not folder_path.startswith(path_prefix):
                        new_entries.append(entry)
                    else:
                        removed_count += 1
                
                data['entries'] = new_entries
                cursor.execute("UPDATE ItemTable SET value = ? WHERE key = 'history.recentlyOpenedPathsList'", (json.dumps(data),))
                conn.commit()
                
                # Remove from table
                self.results_table.removeRow(row)
                
                # Update summary
                remaining = sum(int(self.results_table.item(r, 1).text()) for r in range(self.results_table.rowCount()))
                self.summary_label.setText(f"<b>Total Folders Tracked:</b> {remaining} | <span style='color: #2ecc71;'><b>✅ {location} access removed!</b></span>")
                
                QMessageBox.information(
                    self,
                    "Success",
                    f"Removed {removed_count} folders from {location}"
                )
            
            conn.close()
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to remove access:\n{str(e)}")
    
    def lock_to_documents(self):
        """Lock Windsurf access to Documents folder only"""
        import os
        import sqlite3
        import json
        import urllib.parse
        
        # Show what will be removed
        non_documents = [loc for loc in self.current_locations if loc != '📄 Documents']
        
        if not non_documents:
            QMessageBox.information(self, "Already Locked", "Access is already limited to Documents only!")
            return
        
        # Confirmation dialog
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Icon.Warning)
        msg.setWindowTitle("Lock to Documents Only")
        msg.setText("<b>🔒 Restrict Windsurf to Documents folder only?</b>")
        
        locations_text = "<br>".join([f"  • {loc}" for loc in non_documents])
        msg.setInformativeText(
            f"<b>This will remove access to:</b><br>{locations_text}<br><br>"
            "<b>Only Documents folder will remain tracked.</b><br><br>"
            "This change will be logged with timestamp."
        )
        msg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        msg.setDefaultButton(QMessageBox.StandardButton.No)
        reply = msg.exec()
        
        if reply != QMessageBox.StandardButton.Yes:
            return
        
        try:
            global_db = os.path.expanduser("~/Library/Application Support/Windsurf/User/globalStorage/state.vscdb")
            
            conn = sqlite3.connect(global_db)
            cursor = conn.cursor()
            cursor.execute("SELECT value FROM ItemTable WHERE key = 'history.recentlyOpenedPathsList' LIMIT 1")
            row_data = cursor.fetchone()
            
            if row_data and row_data[0]:
                data = json.loads(row_data[0])
                entries = data.get('entries', [])
                
                # Keep only Documents folders
                new_entries = []
                removed_count = 0
                removed_locations = []
                
                for entry in entries:
                    folder_uri = entry.get('folderUri', '')
                    folder_path = urllib.parse.unquote(folder_uri.replace('file://', ''))
                    
                    if folder_path.startswith('/Users/meep/Documents'):
                        new_entries.append(entry)
                    else:
                        removed_count += 1
                        # Track which location this was from
                        if folder_path.startswith('/Users/meep/Desktop'):
                            if '🖥️ Desktop' not in removed_locations:
                                removed_locations.append('🖥️ Desktop')
                        elif folder_path.startswith('/Users/meep/Downloads'):
                            if '⬇️ Downloads' not in removed_locations:
                                removed_locations.append('⬇️ Downloads')
                        elif folder_path.startswith('/Users/meep/Library'):
                            if '📚 Library' not in removed_locations:
                                removed_locations.append('📚 Library')
                
                data['entries'] = new_entries
                cursor.execute("UPDATE ItemTable SET value = ? WHERE key = 'history.recentlyOpenedPathsList'", (json.dumps(data),))
                conn.commit()
                
                # Log the change
                self.log_access_change("LOCKED_TO_DOCUMENTS", removed_locations, removed_count)
                
                # Update UI
                self.btn_lock_documents.setVisible(False)
                self.scan_global_access()  # Refresh
                
                QMessageBox.information(
                    self,
                    "✅ Locked to Documents",
                    f"<b>Successfully locked to Documents only!</b><br><br>"
                    f"Removed {removed_count} folders from:<br>" +
                    "<br>".join([f"  • {loc}" for loc in removed_locations]) +
                    "<br><br>This change has been logged."
                )
            
            conn.close()
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to lock access:\n{str(e)}")
    
    def log_access_change(self, action, locations, count):
        """Log access changes to a file"""
        import os
        from datetime import datetime
        
        log_file = os.path.expanduser("~/Library/Application Support/Windsurf/User/globalStorage/access_change_log.txt")
        
        try:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            with open(log_file, 'a') as f:
                f.write(f"\n{'='*60}\n")
                f.write(f"Timestamp: {timestamp}\n")
                f.write(f"Action: {action}\n")
                f.write(f"Locations Affected: {', '.join(locations)}\n")
                f.write(f"Folders Removed: {count}\n")
                f.write(f"{'='*60}\n")
        except Exception as e:
            print(f"Failed to log change: {e}")
    
    def view_change_log(self):
        """View the access change log"""
        import os
        
        log_file = os.path.expanduser("~/Library/Application Support/Windsurf/User/globalStorage/access_change_log.txt")
        
        if not os.path.exists(log_file):
            QMessageBox.information(
                self,
                "No Changes Logged",
                "No access changes have been logged yet.\n\n"
                "Changes will be logged when you:\n"
                "• Lock to Documents only\n"
                "• Remove location access\n"
                "• Make other access modifications"
            )
            return
        
        try:
            with open(log_file, 'r') as f:
                log_content = f.read()
            
            # Create dialog to show log
            dialog = QDialog(self)
            dialog.setWindowTitle("Access Change Log")
            dialog.setGeometry(100, 100, 700, 500)
            
            layout = QVBoxLayout()
            
            # Log content
            log_text = QTextEdit()
            log_text.setReadOnly(True)
            log_text.setPlainText(log_content)
            log_text.setStyleSheet("background-color: #1e1e1e; color: #d4d4d4; font-family: monospace;")
            layout.addWidget(log_text)
            
            # Buttons
            btn_layout = QHBoxLayout()
            
            clear_btn = QPushButton("🗑️ Clear Log")
            clear_btn.clicked.connect(lambda: self.clear_log(dialog, log_file))
            clear_btn.setStyleSheet("background-color: #e74c3c;")
            btn_layout.addWidget(clear_btn)
            
            close_btn = QPushButton("Close")
            close_btn.clicked.connect(dialog.close)
            btn_layout.addWidget(close_btn)
            
            layout.addLayout(btn_layout)
            
            dialog.setLayout(layout)
            dialog.exec()
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to read log:\n{str(e)}")
    
    def clear_log(self, dialog, log_file):
        """Clear the change log"""
        reply = QMessageBox.question(
            self,
            "Clear Log",
            "Are you sure you want to clear the access change log?\n\n"
            "This cannot be undone.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                import os
                os.remove(log_file)
                QMessageBox.information(self, "Log Cleared", "Access change log has been cleared.")
                dialog.close()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to clear log:\n{str(e)}")


class FolderAccessWidget(QWidget):
    """Folder access management tab"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Title
        title = QLabel("Folder Access Management")
        title.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        layout.addWidget(title)
        
        desc = QLabel(
            "View and manage all folders that Windsurf has accessed. "
            "Export chat histories, remove folder tracking, and control workspace access."
        )
        desc.setWordWrap(True)
        desc.setStyleSheet("color: #95a5a6; margin-bottom: 15px;")
        layout.addWidget(desc)
        
        # Global folder access summary
        self.global_access_group = QGroupBox("🌍 Global Folder Access Summary")
        global_layout = QVBoxLayout()
        self.global_access_label = QLabel("Click 'Scan Folder Access' to see global access analysis...")
        self.global_access_label.setWordWrap(True)
        self.global_access_label.setStyleSheet("color: #95a5a6; padding: 10px;")
        global_layout.addWidget(self.global_access_label)
        self.global_access_group.setLayout(global_layout)
        layout.addWidget(self.global_access_group)
        
        # Buttons
        btn_layout = QHBoxLayout()
        
        self.btn_test = QPushButton("🧪 Scan Folder Access")
        self.btn_test.clicked.connect(self.run_permission_test)
        self.btn_test.setStyleSheet("background-color: #e67e22;")
        btn_layout.addWidget(self.btn_test)
        
        self.btn_export_chats = QPushButton("💾 Export Current Workspace Chats")
        self.btn_export_chats.clicked.connect(self.export_current_chats)
        self.btn_export_chats.setStyleSheet("background-color: #2ecc71;")
        btn_layout.addWidget(self.btn_export_chats)
        
        btn_layout.addStretch()
        layout.addLayout(btn_layout)
        
        # Results table
        self.results_table = QTableWidget()
        self.results_table.setColumnCount(4)
        self.results_table.setHorizontalHeaderLabels(["Folder Path", "Last Access", "Parent Architecture", "Status"])
        self.results_table.horizontalHeader().setStretchLastSection(True)
        self.results_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.results_table.setSortingEnabled(True)  # Enable sorting
        self.results_table.setAlternatingRowColors(True)  # Alternating row colors
        self.results_table.setStyleSheet("""
            QTableWidget {
                background-color: #1e1e1e;
                alternate-background-color: #2d2d2d;
                color: #ffffff;
                gridline-color: #3d3d3d;
                border: 1px solid #3d3d3d;
            }
            QTableWidget::item {
                padding: 5px;
            }
            QTableWidget::item:selected {
                background-color: #3498db;
            }
            QHeaderView::section {
                background-color: #2c3e50;
                color: #ffffff;
                padding: 8px;
                border: 1px solid #34495e;
                font-weight: bold;
            }
            QHeaderView::section:hover {
                background-color: #34495e;
            }
        """)
        self.results_table.setVisible(False)
        layout.addWidget(self.results_table)
        
        # Remove buttons
        remove_btn_layout = QHBoxLayout()
        
        self.btn_remove = QPushButton("🗑️ Remove Access to Selected Folder")
        self.btn_remove.clicked.connect(self.remove_folder_access)
        self.btn_remove.setStyleSheet("background-color: #e74c3c;")
        self.btn_remove.setVisible(False)
        remove_btn_layout.addWidget(self.btn_remove)
        
        self.btn_remove_not_found = QPushButton("🧹 Remove All 'Not Found' Folders")
        self.btn_remove_not_found.clicked.connect(self.remove_not_found_folders)
        self.btn_remove_not_found.setStyleSheet("background-color: #e67e22;")
        self.btn_remove_not_found.setVisible(False)
        remove_btn_layout.addWidget(self.btn_remove_not_found)
        
        layout.addLayout(remove_btn_layout)
        
        self.setLayout(layout)
        
    def run_permission_test(self):
        """Run active permissions test script"""
        import os
        import sqlite3
        import json
        import urllib.parse
        
        # Show table and remove buttons
        self.results_table.setVisible(True)
        self.btn_remove.setVisible(True)
        self.btn_remove_not_found.setVisible(True)
        self.results_table.setRowCount(0)
        
        # Get folder access data from global state database
        try:
            global_db = os.path.expanduser("~/Library/Application Support/Windsurf/User/globalStorage/state.vscdb")
            
            if not os.path.exists(global_db):
                QMessageBox.warning(self, "No Data", "Global state database not found.")
                return
            
            folders = []
            
            conn = sqlite3.connect(global_db)
            cursor = conn.cursor()
            
            # Get recently opened paths
            cursor.execute("SELECT value FROM ItemTable WHERE key = 'history.recentlyOpenedPathsList' LIMIT 1")
            row = cursor.fetchone()
            
            if row and row[0]:
                data = json.loads(row[0])
                entries = data.get('entries', [])
                
                # Analyze global folder access
                from collections import defaultdict
                global_access = defaultdict(int)
                
                for entry in entries:
                    folder_uri = entry.get('folderUri')
                    if folder_uri:
                        # Decode URI
                        folder_path = urllib.parse.unquote(folder_uri.replace('file://', ''))
                        
                        # Categorize by top-level directory
                        if folder_path.startswith('/Users/meep/Documents'):
                            global_access['📄 Documents'] += 1
                        elif folder_path.startswith('/Users/meep/Desktop'):
                            global_access['🖥️ Desktop'] += 1
                        elif folder_path.startswith('/Users/meep/Downloads'):
                            global_access['⬇️ Downloads'] += 1
                        elif folder_path.startswith('/Users/meep/Library'):
                            global_access['📚 Library'] += 1
                        elif folder_path.startswith('/Users/meep/Pictures'):
                            global_access['🖼️ Pictures'] += 1
                        elif folder_path.startswith('/Users/meep/'):
                            global_access['🏠 Home Directory'] += 1
                        
                        # Get last access time
                        try:
                            stat_info = os.stat(folder_path)
                            last_access = datetime.fromtimestamp(stat_info.st_atime).strftime('%Y-%m-%d %H:%M:%S')
                        except:
                            last_access = "Unknown"
                        
                        # Get parent directory
                        parent = os.path.dirname(folder_path)
                        
                        # Determine status
                        if os.path.exists(folder_path):
                            if os.access(folder_path, os.R_OK | os.W_OK):
                                status = "✅ Read/Write"
                            elif os.access(folder_path, os.R_OK):
                                status = "📖 Read Only"
                            else:
                                status = "🔒 No Access"
                        else:
                            status = "❌ Not Found"
                        
                        folders.append((folder_path, last_access, parent, status))
            
            conn.close()
            
            # Populate table
            self.results_table.setRowCount(len(folders))
            for row, (path, access, parent, status) in enumerate(folders):
                self.results_table.setItem(row, 0, QTableWidgetItem(path))
                self.results_table.setItem(row, 1, QTableWidgetItem(access))
                self.results_table.setItem(row, 2, QTableWidgetItem(parent))
                self.results_table.setItem(row, 3, QTableWidgetItem(status))
            
            # Resize columns
            self.results_table.resizeColumnsToContents()
            
            # Update global access summary
            if global_access:
                summary_text = "<b>Windsurf has accessed folders in:</b><br><br>"
                for location, count in sorted(global_access.items(), key=lambda x: x[1], reverse=True):
                    color = "#e74c3c" if count > 5 else "#e67e22" if count > 2 else "#2ecc71"
                    summary_text += f"<span style='color: {color};'>• {location}: <b>{count} folders</b></span><br>"
                
                summary_text += "<br><b>Recommendations:</b><br>"
                if global_access.get('📚 Library', 0) > 0:
                    summary_text += "<span style='color: #e74c3c;'>⚠️ Library access detected - may indicate Full Disk Access</span><br>"
                if global_access.get('🖥️ Desktop', 0) > 0:
                    summary_text += "<span style='color: #e67e22;'>⚠️ Desktop access detected</span><br>"
                if len(global_access) == 1 and '📄 Documents' in global_access:
                    summary_text += "<span style='color: #2ecc71;'>✅ Access limited to Documents folder only</span><br>"
                
                self.global_access_label.setText(summary_text)
            
            QMessageBox.information(self, "Test Complete", 
                f"Found {len(folders)} folders with access.\n"
                f"Results displayed in table below.")
                
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to run test:\n{str(e)}")
    
    def export_current_chats(self):
        """Export current workspace chats to _Chatlogs folder"""
        import os
        import sqlite3
        import json
        
        try:
            # Get current workspace folder
            global_db = os.path.expanduser("~/Library/Application Support/Windsurf/User/globalStorage/state.vscdb")
            workspace_storage = os.path.expanduser("~/Library/Application Support/Windsurf/User/workspaceStorage")
            
            if not os.path.exists(global_db):
                QMessageBox.warning(self, "Error", "Global state database not found.")
                return
            
            # Get most recent workspace
            conn = sqlite3.connect(global_db)
            cursor = conn.cursor()
            cursor.execute("SELECT value FROM ItemTable WHERE key = 'history.recentlyOpenedPathsList' LIMIT 1")
            row = cursor.fetchone()
            
            if not row or not row[0]:
                QMessageBox.warning(self, "No Workspace", "No recent workspace found.")
                conn.close()
                return
            
            data = json.loads(row[0])
            entries = data.get('entries', [])
            
            if not entries:
                QMessageBox.warning(self, "No Workspace", "No workspace entries found.")
                conn.close()
                return
            
            # Get first folder entry (most recent)
            import urllib.parse
            current_folder = None
            for entry in entries:
                if 'folderUri' in entry:
                    current_folder = urllib.parse.unquote(entry['folderUri'].replace('file://', ''))
                    break
            
            if not current_folder:
                QMessageBox.warning(self, "No Folder", "Could not determine current workspace folder.")
                conn.close()
                return
            
            # Find workspace ID for this folder
            workspace_id = None
            workspace_path = None
            
            for ws_dir in os.listdir(workspace_storage):
                ws_path = os.path.join(workspace_storage, ws_dir)
                if os.path.isdir(ws_path):
                    state_db = os.path.join(ws_path, "state.vscdb")
                    if os.path.exists(state_db):
                        try:
                            ws_conn = sqlite3.connect(state_db)
                            ws_cursor = ws_conn.cursor()
                            ws_cursor.execute("SELECT value FROM ItemTable WHERE key = 'workspace.folderURIStr' LIMIT 1")
                            ws_row = ws_cursor.fetchone()
                            if ws_row and ws_row[0]:
                                ws_folder = urllib.parse.unquote(ws_row[0].replace('file://', ''))
                                if ws_folder == current_folder:
                                    workspace_id = ws_dir
                                    workspace_path = state_db
                                    ws_conn.close()
                                    break
                            ws_conn.close()
                        except:
                            pass
            
            conn.close()
            
            if not workspace_id or not workspace_path:
                QMessageBox.warning(self, "No Workspace", 
                    f"Could not find workspace database for:\n{current_folder}\n\n"
                    "This might mean no chats exist for this folder yet.")
                return
            
            # Export chats
            ws_conn = sqlite3.connect(workspace_path)
            ws_cursor = ws_conn.cursor()
            ws_cursor.execute("SELECT key, value FROM ItemTable WHERE key LIKE '%chat%' OR key LIKE '%cascade%'")
            chat_rows = ws_cursor.fetchall()
            ws_conn.close()
            
            if not chat_rows:
                QMessageBox.information(self, "No Chats", 
                    f"No chat history found for:\n{current_folder}")
                return
            
            # Create _Chatlogs folder
            chatlog_dir = os.path.join(current_folder, "_Chatlogs")
            os.makedirs(chatlog_dir, exist_ok=True)
            
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            
            # Export as Markdown
            md_file = os.path.join(chatlog_dir, f"chat_export_{timestamp}.md")
            with open(md_file, 'w') as f:
                f.write(f"# Chat History Export\n\n")
                f.write(f"**Workspace Folder:** {current_folder}\n")
                f.write(f"**Export Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"**Workspace ID:** {workspace_id}\n")
                f.write(f"**Total Chat Entries:** {len(chat_rows)}\n\n")
                f.write("---\n\n")
                
                for i, (key, value) in enumerate(chat_rows, 1):
                    f.write(f"## Entry {i}: {key}\n\n")
                    
                    # Try to parse JSON for better formatting
                    try:
                        parsed = json.loads(value)
                        f.write("```json\n")
                        f.write(json.dumps(parsed, indent=2))
                        f.write("\n```\n\n")
                    except:
                        # If not JSON, just write as code block
                        f.write("```\n")
                        f.write(str(value))
                        f.write("\n```\n\n")
            
            # Export as JSON
            json_file = os.path.join(chatlog_dir, f"chat_export_{timestamp}.json")
            with open(json_file, 'w') as f:
                json.dump([{"key": k, "value": v} for k, v in chat_rows], f, indent=2)
            
            # Export as CSV
            csv_file = os.path.join(chatlog_dir, f"chat_export_{timestamp}.csv")
            with open(csv_file, 'w') as f:
                f.write("key,value\n")
                for key, value in chat_rows:
                    # Escape quotes in CSV
                    escaped_value = str(value).replace('"', '""')
                    f.write(f'"{key}","{escaped_value}"\n')
            
            # Create README
            readme_file = os.path.join(chatlog_dir, "README.txt")
            with open(readme_file, 'w') as f:
                f.write("Chat History Export\n")
                f.write("===================\n\n")
                f.write(f"Workspace: {current_folder}\n")
                f.write(f"Export Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Total Entries: {len(chat_rows)}\n\n")
                f.write("Files:\n")
                f.write(f"- chat_export_{timestamp}.md   (Markdown - easy to read)\n")
                f.write(f"- chat_export_{timestamp}.json (JSON - machine readable)\n")
                f.write(f"- chat_export_{timestamp}.csv  (CSV - Excel compatible)\n\n")
                f.write("These chats are preserved locally in this folder.\n")
                f.write("You can reference them anytime, even after cleanup!\n")
            
            # Success message
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Icon.Information)
            msg.setWindowTitle("Chats Exported Successfully")
            msg.setText(f"<b>Exported {len(chat_rows)} chat entries!</b>")
            msg.setInformativeText(
                f"<b>Workspace:</b> {current_folder}<br><br>"
                f"<b>Saved to:</b><br>{chatlog_dir}<br><br>"
                f"<b>Files created:</b><br>"
                f"• chat_export_{timestamp}.md<br>"
                f"• chat_export_{timestamp}.json<br>"
                f"• chat_export_{timestamp}.csv<br>"
                f"• README.txt<br><br>"
                "You can now reference these chats anytime!"
            )
            msg.setStandardButtons(QMessageBox.StandardButton.Ok)
            
            # Add button to open folder
            open_btn = msg.addButton("📂 Open Folder", QMessageBox.ButtonRole.ActionRole)
            msg.exec()
            
            if msg.clickedButton() == open_btn:
                import subprocess
                subprocess.run(['open', chatlog_dir])
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to export chats:\n{str(e)}")
    
    def remove_folder_access(self):
        """Remove access to selected folder and export chats"""
        import os
        import sqlite3
        import json
        import urllib.parse
        import shutil
        
        # Get selected row
        selected_rows = self.results_table.selectionModel().selectedRows()
        if not selected_rows:
            QMessageBox.warning(self, "No Selection", "Please select a folder to remove access from.")
            return
        
        row = selected_rows[0].row()
        folder_path = self.results_table.item(row, 0).text()
        
        # Confirmation dialog
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Icon.Warning)
        msg.setWindowTitle("Remove Folder Access")
        msg.setText(f"<b>Remove access to this folder?</b>")
        msg.setInformativeText(
            f"<b>Folder:</b> {folder_path}<br><br>"
            "<b>This will:</b><br>"
            f"✅ Export chat conversations to:<br>"
            f"   {folder_path}/_Chatlogs/<br><br>"
            "❌ Remove workspace tracking<br>"
            "❌ Delete workspace storage database<br><br>"
            "<b>Chat files will be saved as:</b><br>"
            "• chat_export.md (Markdown - easy to read)<br>"
            "• chat_export.json (JSON - machine readable)<br>"
            "• chat_export.csv (CSV - Excel compatible)<br><br>"
            "You can reference these chats later if you re-open the folder!"
        )
        msg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        msg.setDefaultButton(QMessageBox.StandardButton.No)
        reply = msg.exec()
        
        if reply != QMessageBox.StandardButton.Yes:
            return
        
        try:
            # Step 1: Find workspace ID
            global_db = os.path.expanduser("~/Library/Application Support/Windsurf/User/globalStorage/state.vscdb")
            workspace_storage = os.path.expanduser("~/Library/Application Support/Windsurf/User/workspaceStorage")
            
            conn = sqlite3.connect(global_db)
            cursor = conn.cursor()
            
            # Get recently opened paths
            cursor.execute("SELECT value FROM ItemTable WHERE key = 'history.recentlyOpenedPathsList' LIMIT 1")
            row_data = cursor.fetchone()
            
            workspace_ids = []
            if row_data and row_data[0]:
                data = json.loads(row_data[0])
                entries = data.get('entries', [])
                
                # Find matching workspace IDs
                for ws_dir in os.listdir(workspace_storage):
                    ws_path = os.path.join(workspace_storage, ws_dir)
                    if os.path.isdir(ws_path):
                        state_db = os.path.join(ws_path, "state.vscdb")
                        if os.path.exists(state_db):
                            try:
                                ws_conn = sqlite3.connect(state_db)
                                ws_cursor = ws_conn.cursor()
                                ws_cursor.execute("SELECT value FROM ItemTable WHERE key = 'workspace.folderURIStr' LIMIT 1")
                                ws_row = ws_cursor.fetchone()
                                if ws_row and ws_row[0]:
                                    ws_folder = urllib.parse.unquote(ws_row[0].replace('file://', ''))
                                    if ws_folder == folder_path:
                                        workspace_ids.append((ws_dir, ws_path, state_db))
                                ws_conn.close()
                            except:
                                pass
            
            # Step 2: Export chats
            chatlog_dir = os.path.join(folder_path, "_Chatlogs")
            os.makedirs(chatlog_dir, exist_ok=True)
            
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            total_messages = 0
            
            for ws_id, ws_path, state_db in workspace_ids:
                try:
                    ws_conn = sqlite3.connect(state_db)
                    ws_cursor = ws_conn.cursor()
                    ws_cursor.execute("SELECT key, value FROM ItemTable WHERE key LIKE '%chat%' OR key LIKE '%cascade%'")
                    chat_rows = ws_cursor.fetchall()
                    
                    if chat_rows:
                        # Export as Markdown
                        md_file = os.path.join(chatlog_dir, f"chat_export_{timestamp}.md")
                        with open(md_file, 'w') as f:
                            f.write(f"# Chat History Export\n")
                            f.write(f"**Folder:** {folder_path}\n")
                            f.write(f"**Export Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                            f.write(f"**Workspace ID:** {ws_id}\n")
                            f.write(f"**Total Entries:** {len(chat_rows)}\n\n")
                            f.write("---\n\n")
                            
                            for key, value in chat_rows:
                                f.write(f"## {key}\n\n")
                                f.write(f"```\n{value}\n```\n\n")
                                total_messages += 1
                        
                        # Export as JSON
                        json_file = os.path.join(chatlog_dir, f"chat_export_{timestamp}.json")
                        with open(json_file, 'w') as f:
                            json.dump([{"key": k, "value": v} for k, v in chat_rows], f, indent=2)
                        
                        # Export as CSV
                        csv_file = os.path.join(chatlog_dir, f"chat_export_{timestamp}.csv")
                        with open(csv_file, 'w') as f:
                            f.write("key,value\n")
                            for key, value in chat_rows:
                                f.write(f'"{key}","{value.replace(chr(34), chr(34)+chr(34))}"\n')
                        
                        # Create README
                        readme_file = os.path.join(chatlog_dir, "README.txt")
                        with open(readme_file, 'w') as f:
                            f.write(f"Chat History Export\n")
                            f.write(f"===================\n\n")
                            f.write(f"Folder: {folder_path}\n")
                            f.write(f"Export Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                            f.write(f"Total Messages: {total_messages}\n\n")
                            f.write(f"Files:\n")
                            f.write(f"- chat_export_{timestamp}.md  (Markdown - easy to read)\n")
                            f.write(f"- chat_export_{timestamp}.json (JSON - machine readable)\n")
                            f.write(f"- chat_export_{timestamp}.csv (CSV - Excel compatible)\n\n")
                            f.write(f"These chats are preserved locally.\n")
                            f.write(f"If you re-open this folder in Windsurf, you can reference these files!\n")
                    
                    ws_conn.close()
                except Exception as e:
                    print(f"Error exporting chats: {e}")
            
            # Step 3: Remove tracking
            # Remove from history
            if row_data and row_data[0]:
                data = json.loads(row_data[0])
                entries = data.get('entries', [])
                new_entries = [e for e in entries if urllib.parse.unquote(e.get('folderUri', '').replace('file://', '')) != folder_path]
                data['entries'] = new_entries
                cursor.execute("UPDATE ItemTable SET value = ? WHERE key = 'history.recentlyOpenedPathsList'", (json.dumps(data),))
                conn.commit()
            
            # Delete workspace storage
            for ws_id, ws_path, state_db in workspace_ids:
                try:
                    shutil.rmtree(ws_path)
                except Exception as e:
                    print(f"Error deleting workspace: {e}")
            
            conn.close()
            
            # Remove from table
            self.results_table.removeRow(row)
            
            # Success message
            QMessageBox.information(
                self,
                "Access Removed Successfully",
                f"<b>Folder:</b> {folder_path}<br><br>"
                f"✅ Exported {total_messages} chat entries to:<br>"
                f"   {chatlog_dir}<br><br>"
                f"✅ Removed workspace tracking<br>"
                f"✅ Deleted {len(workspace_ids)} workspace storage folder(s)<br><br>"
                f"The folder is no longer tracked by Windsurf.<br>"
                f"Chat history has been preserved in _Chatlogs/"
            )
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to remove access:\n{str(e)}")
    
    def remove_not_found_folders(self):
        """Remove all folders that don't exist (Not Found status)"""
        import os
        import sqlite3
        import json
        import urllib.parse
        
        # Count "Not Found" folders
        not_found_folders = []
        for row in range(self.results_table.rowCount()):
            status = self.results_table.item(row, 3).text()
            if "Not Found" in status:
                folder_path = self.results_table.item(row, 0).text()
                not_found_folders.append(folder_path)
        
        if not not_found_folders:
            QMessageBox.information(self, "No Action Needed", "No 'Not Found' folders to remove.")
            return
        
        # Confirmation
        reply = QMessageBox.question(
            self,
            "Remove Not Found Folders",
            f"Remove {len(not_found_folders)} folders that no longer exist?\n\n"
            "This will clean up stale tracking entries.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply != QMessageBox.StandardButton.Yes:
            return
        
        try:
            global_db = os.path.expanduser("~/Library/Application Support/Windsurf/User/globalStorage/state.vscdb")
            
            conn = sqlite3.connect(global_db)
            cursor = conn.cursor()
            cursor.execute("SELECT value FROM ItemTable WHERE key = 'history.recentlyOpenedPathsList' LIMIT 1")
            row_data = cursor.fetchone()
            
            if row_data and row_data[0]:
                data = json.loads(row_data[0])
                entries = data.get('entries', [])
                
                # Remove entries for folders that don't exist
                new_entries = []
                removed_count = 0
                for entry in entries:
                    folder_uri = entry.get('folderUri', '')
                    folder_path = urllib.parse.unquote(folder_uri.replace('file://', ''))
                    
                    if folder_path not in not_found_folders:
                        new_entries.append(entry)
                    else:
                        removed_count += 1
                
                data['entries'] = new_entries
                cursor.execute("UPDATE ItemTable SET value = ? WHERE key = 'history.recentlyOpenedPathsList'", (json.dumps(data),))
                conn.commit()
                
                # Remove rows from table (in reverse order to avoid index issues)
                rows_to_remove = []
                for row in range(self.results_table.rowCount()):
                    status = self.results_table.item(row, 3).text()
                    if "Not Found" in status:
                        rows_to_remove.append(row)
                
                for row in reversed(rows_to_remove):
                    self.results_table.removeRow(row)
                
                QMessageBox.information(
                    self,
                    "Success",
                    f"Removed {removed_count} 'Not Found' folders from tracking.\n\n"
                    f"Your folder list is now clean!"
                )
            
            conn.close()
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to remove folders:\n{str(e)}")


class MainWindow(QMainWindow):
    """Main application window"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle("Windsurf Privacy Toolkit")
        self.setGeometry(100, 100, 1250, 700)  # 25% wider (1000 * 1.25 = 1250)
        
        # Central widget with tabs
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout()
        central_widget.setLayout(layout)
        
        # Tab widget
        self.tabs = QTabWidget()
        
        # Add tabs with visual separators
        self.tabs.addTab(DashboardWidget(self), "🏠 Dashboard")
        self.tabs.addTab(AuditWidget(), "│ 🔍 Audit")
        self.tabs.addTab(CleanupWidget(), "🧹 Cleanup")
        self.tabs.addTab(BackupsWidget(), "💾 Backups")
        self.tabs.addTab(PermissionsWidget(), "│ 🔒 Permissions")
        self.tabs.addTab(GlobalAccessWidget(), "🌍 Global Access")
        self.tabs.addTab(FolderAccessWidget(), "📁 Folder Access")
        self.tabs.addTab(NetworkMonitorWidget(), "│ 🌐 Network Monitor")
        
        # Style tabs with better spacing
        self.tabs.setStyleSheet("""
            QTabBar::tab {
                padding: 8px 16px;
                margin: 2px;
                color: white;
                font-weight: bold;
            }
            QTabWidget::pane {
                border: 1px solid #3d3d3d;
            }
        """)
        
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
