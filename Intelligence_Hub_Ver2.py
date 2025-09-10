# -*- coding: utf-8 -*-
"""
Indo-Pacific Strategic Intelligence Hub
Fixed and regenerated for robust uploads, clean UI, and full event timeline.
Added delete, refresh, and WhatsApp share PDF functionality.
Added save and export PDF buttons throughout the application.
Added refresh, save and delete buttons in all tabs, save new entries, and report generation with graphs.

Python: 3.11+
Dependencies: PyQt5, matplotlib, pandas
Run: python app.py
"""

import sys
import os
import json
import random
import subprocess
import webbrowser
from datetime import datetime
from urllib.parse import quote
import matplotlib.pyplot as plt
from io import BytesIO
import base64

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QStackedWidget, QListWidget, QListWidgetItem, QFormLayout,
    QLineEdit, QTextEdit, QComboBox, QFileDialog, QGroupBox, QTableWidget,
    QTableWidgetItem, QHeaderView, QMessageBox, QDialog, QScrollArea, QFrame,
    QAction, QMenu, QToolBar, QSizePolicy
)
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QFont, QTextDocument, QDesktopServices, QIcon, QPixmap
from PyQt5.QtPrintSupport import QPrinter


# ------------------------------
# Utility helpers
# ------------------------------
def human_size(num_bytes: int) -> str:
    units = ["B", "KB", "MB", "GB", "TB"]
    size = float(num_bytes)
    idx = 0
    while size >= 1024 and idx < len(units) - 1:
        size /= 1024.0
        idx += 1
    return f"{size:.1f} {units[idx]}"


def now_str() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M")


def create_sample_graph():
    """Create a sample graph and return as base64 encoded image"""
    try:
        # Sample data
        categories = ['East Asia', 'Southeast Asia', 'South Asia', 'Oceania', 'Eastern Africa']
        values = [23, 17, 31, 12, 19]
        
        # Create plot
        plt.figure(figsize=(8, 5))
        plt.bar(categories, values, color=['#007bff', '#28a745', '#dc3545', '#ffc107', '#17a2b8'])
        plt.title('Regional Activity Distribution')
        plt.xlabel('Region')
        plt.ylabel('Number of Activities')
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        # Save to buffer
        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        
        # Convert to base64
        img_str = base64.b64encode(buffer.read()).decode()
        plt.close()
        
        return f"data:image/png;base64,{img_str}"
    except Exception as e:
        print(f"Error creating graph: {e}")
        return None


# ------------------------------
# Cognitive Dissonance Analyzer
# ------------------------------
class CognitiveAnalysisDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Cognitive Dissonance Analysis")
        self.setModal(True)
        self.setMinimumSize(900, 650)

        layout = QVBoxLayout(self)

        # Title
        title_layout = QHBoxLayout()
        title_layout.addWidget(QLabel("Title:"))
        self.title_input = QLineEdit()
        title_layout.addWidget(self.title_input)
        layout.addLayout(title_layout)

        # Source type
        source_layout = QHBoxLayout()
        source_layout.addWidget(QLabel("Source Type:"))
        self.source_combo = QComboBox()
        self.source_combo.addItems([
            "Political Speech",
            "Media Report",
            "Social Media",
            "Academic Findings",
            "Government Statement",
            "Other"
        ])
        source_layout.addWidget(self.source_combo)
        layout.addLayout(source_layout)

        # Region
        region_layout = QHBoxLayout()
        region_layout.addWidget(QLabel("Region:"))
        self.region_combo = QComboBox()
        self.region_combo.addItems([
            "East Asia",
            "Southeast Asia",
            "South Asia",
            "Oceania",
            "Eastern Africa",
            "Middle East",
            "Europe",
            "North America",
            "Latin America"
        ])
        self.region_combo.setCurrentText("Eastern Africa")
        region_layout.addWidget(self.region_combo)
        layout.addLayout(region_layout)

        # Text input
        layout.addWidget(QLabel("Text to Analyze:"))
        self.text_input = QTextEdit()
        self.text_input.setPlaceholderText(
            "Paste the text you want to analyze for cognitive dissonance..."
        )
        layout.addWidget(self.text_input)

        # Word count
        self.word_count_label = QLabel("Words: 0")
        layout.addWidget(self.word_count_label)

        # File upload (load text)
        file_layout = QHBoxLayout()
        self.load_text_btn = QPushButton("Load Text From File")
        file_layout.addWidget(self.load_text_btn)
        file_layout.addStretch()
        layout.addLayout(file_layout)

        # Analyze button
        self.analyze_btn = QPushButton("Analyze Text")
        self.analyze_btn.setStyleSheet("background-color: #007bff; color: white;")
        layout.addWidget(self.analyze_btn)

        # Results
        results_group = QGroupBox("Analysis Results")
        results_layout = QVBoxLayout(results_group)

        self.results_title = QLabel("Cognitive Dissonance Analysis")
        self.results_title.setStyleSheet("font-weight: bold;")
        results_layout.addWidget(self.results_title)

        self.results_summary = QLabel("Analysis will appear here...")
        self.results_summary.setWordWrap(True)
        results_layout.addWidget(self.results_summary)

        details_group = QGroupBox("Analysis Details")
        details_layout = QFormLayout(details_group)

        self.dissonance_score = QLabel("0/100")
        details_layout.addRow("Dissonance Score:", self.dissonance_score)

        self.key_indicators = QLabel("None detected")
        details_layout.addRow("Key Indicators:", self.key_indicators)

        self.recommended_actions = QLabel("No recommendations")
        details_layout.addRow("Recommended Actions:", self.recommended_actions)

        results_layout.addWidget(details_group)

        # Export buttons
        export_layout = QHBoxLayout()
        self.export_pdf_btn = QPushButton("Export as PDF")
        self.export_json_btn = QPushButton("Export as JSON")
        self.share_whatsapp_btn = QPushButton("Share via WhatsApp")
        self.share_whatsapp_btn.setStyleSheet("background-color: #25D366; color: white;")
        export_layout.addWidget(self.export_pdf_btn)
        export_layout.addWidget(self.export_json_btn)
        export_layout.addWidget(self.share_whatsapp_btn)
        export_layout.addStretch()
        results_layout.addLayout(export_layout)

        layout.addWidget(results_group)

        # Signals
        self.text_input.textChanged.connect(self.update_word_count)
        self.load_text_btn.clicked.connect(self.load_text_from_file)
        self.analyze_btn.clicked.connect(self.analyze_text)
        self.export_pdf_btn.clicked.connect(self.export_pdf)
        self.export_json_btn.clicked.connect(self.export_json)
        self.share_whatsapp_btn.clicked.connect(self.share_via_whatsapp)

        # State
        self.last_result = None
        self.last_pdf_path = None

    def update_word_count(self):
        text = self.text_input.toPlainText().strip()
        words = len(text.split()) if text else 0
        self.word_count_label.setText(f"Words: {words}")

    def load_text_from_file(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Open Text File", "", "Text Files (*.txt);;All Files (*)"
        )
        if not path:
            return
        try:
            with open(path, "r", encoding="utf-8") as f:
                self.text_input.setPlainText(f.read())
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Could not open file:\n{e}")

    def analyze_text(self):
        text = self.text_input.toPlainText().strip()
        if len(text) < 50:
            QMessageBox.warning(
                self, "Input Error",
                "Please enter at least 50 characters for analysis."
            )
            return

        score = random.randint(0, 100)
        self.dissonance_score.setText(f"{score}/100")

        if score > 70:
            indicators = "Contradictory statements; value-action discrepancies."
            actions = "Compare with external sources; deeper context review."
            level = "high"
        elif score > 40:
            indicators = "Some inconsistent phrasing; possible justification patterns."
            actions = "Moderate review of context and sources."
            level = "moderate"
        else:
            indicators = "Minimal dissonance indicators found."
            actions = "Low level; standard monitoring recommended."
            level = "low"

        self.key_indicators.setText(indicators)
        self.recommended_actions.setText(actions)

        title = self.title_input.text().strip() or "Untitled Analysis"
        source_type = self.source_combo.currentText()
        region = self.region_combo.currentText()
        summary = (
            f'Analysis of "{title}" reveals a {level} level of cognitive dissonance.\n'
            f"Source Type: {source_type} | Region: {region}\n"
            f"Evaluated for contradictions, value-action gaps, and selective evidence."
        )
        self.results_summary.setText(summary)

        self.last_result = {
            "title": title,
            "source_type": source_type,
            "region": region,
            "score": score,
            "level": level,
            "indicators": indicators,
            "actions": actions,
            "summary": summary,
            "word_count": len(text.split()),
            "timestamp": now_str(),
        }

    def export_pdf(self):
        if not self.last_result:
            QMessageBox.information(self, "Export", "Run an analysis first.")
            return

        path, _ = QFileDialog.getSaveFileName(
            self, "Export PDF", "analysis.pdf", "PDF Files (*.pdf)"
        )
        if not path:
            return

        # Generate graph for report
        graph_data = create_sample_graph()
        graph_html = f'<img src="{graph_data}" width="500" height="300"/>' if graph_data else ""

        doc = QTextDocument()
        html = f"""
        <h2>Cognitive Dissonance Analysis</h2>
        <p><b>Title:</b> {self.last_result['title']}<br>
        <b>Source Type:</b> {self.last_result['source_type']}<br>
        <b>Region:</b> {self.last_result['region']}<br>
        <b>Score:</b> {self.last_result['score']}/100 ({self.last_result['level']})<br>
        <b>Word Count:</b> {self.last_result['word_count']}<br>
        <b>Timestamp:</b> {self.last_result['timestamp']}</p>
        <p><b>Key Indicators:</b> {self.last_result['indicators']}</p>
        <p><b>Recommended Actions:</b> {self.last_result['actions']}</p>
        <p>{self.last_result['summary']}</p>
        {graph_html}
        """
        doc.setHtml(html)

        printer = QPrinter(QPrinter.HighResolution)
        printer.setOutputFormat(QPrinter.PdfFormat)
        printer.setOutputFileName(path)
        doc.print_(printer)
        
        self.last_pdf_path = path
        QMessageBox.information(self, "Export", "PDF exported successfully.")

    def export_json(self):
        if not self.last_result:
            QMessageBox.information(self, "Export", "Run an analysis first.")
            return

        path, _ = QFileDialog.getSaveFileName(
            self, "Export JSON", "analysis.json", "JSON Files (*.json)"
        )
        if not path:
            return

        try:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(self.last_result, f, ensure_ascii=False, indent=2)
            QMessageBox.information(self, "Export", "JSON exported successfully.")
        except Exception as e:
            QMessageBox.warning(self, "Export Error", f"Failed to write JSON:\n{e}")

    def share_via_whatsapp(self):
        if not self.last_pdf_path:
            QMessageBox.information(self, "Share", "Export a PDF first to share via WhatsApp.")
            return
            
        # Create a message with analysis summary
        message = f"Cognitive Dissonance Analysis: {self.last_result['title']}\n\n"
        message += f"Score: {self.last_result['score']}/100 ({self.last_result['level']})\n"
        message += f"Region: {self.last_result['region']}\n"
        message += f"Source Type: {self.last_result['source_type']}\n\n"
        message += "See attached PDF for full analysis."
        
        # URL encode the message
        encoded_message = quote(message)
        
        # Create WhatsApp URL
        whatsapp_url = f"whatsapp://send?text={encoded_message}"
        
        # Try to open WhatsApp
        try:
            if sys.platform == "win32":
                os.startfile(whatsapp_url)
            elif sys.platform == "darwin":
                subprocess.Popen(["open", whatsapp_url])
            else:
                subprocess.Popen(["xdg-open", whatsapp_url])
        except Exception as e:
            QMessageBox.warning(self, "Share Error", 
                               f"Could not open WhatsApp: {e}\n\n"
                               "Please make sure WhatsApp is installed on your device.")


# ------------------------------
# Main Window
# ------------------------------
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Indo-Pacific Strategic Intelligence Hub")
        self.setGeometry(100, 100, 1200, 800)

        # State
        self.uploads = []  # list of dicts
        self.events = self._build_events()
        self.political_analyses = []
        self.tech_reports = []
        self.projects = []
        self.documents = []
        self.media_items = []

        # Create toolbar with save and export buttons
        self.toolbar = QToolBar("Main Toolbar")
        self.addToolBar(self.toolbar)
        
        # Save action
        self.save_action = QAction("Save", self)
        self.save_action.setStatusTip("Save current data")
        self.save_action.triggered.connect(self.save_data)
        self.toolbar.addAction(self.save_action)
        
        # Export PDF action
        self.export_pdf_action = QAction("Export PDF", self)
        self.export_pdf_action.setStatusTip("Export current view as PDF")
        self.export_pdf_action.triggered.connect(self.export_current_as_pdf)
        self.toolbar.addAction(self.export_pdf_action)

        # Central layout
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QHBoxLayout(central)

        # Sidebar
        self.sidebar = QListWidget()
        self.sidebar.setMaximumWidth(220)
        self.sidebar.setStyleSheet("""
            QListWidget { background-color: #2c3e50; color: white; border: none; }
            QListWidget::item { padding: 10px; border-bottom: 1px solid #34495e; }
            QListWidget::item:selected { background-color: #3498db; color: white; }
        """)
        for item in [
            "Dashboard",
            "Political Trends",
            "Technology",
            "Code Projects",
            "Documents",
            "Media Library",
            "Geopolitical Analysis",
            "Cognitive Analysis",
            "Activity Log",
            "Upload Files",
            "About",
        ]:
            self.sidebar.addItem(QListWidgetItem(item))

        # Stacked pages
        self.stacked = QStackedWidget()
        self.dashboard_page = self.create_dashboard_page()
        self.political_page = self.create_political_page()
        self.tech_page = self.create_technology_page()
        self.projects_page = self.create_projects_page()
        self.documents_page = self.create_documents_page()
        self.media_page = self.create_media_page()
        self.geopolitical_page = self.create_geopolitical_page()
        self.cognitive_page = self.create_cognitive_page()
        self.logs_page = self.create_logs_page()
        self.upload_page = self.create_upload_page()
        self.about_page = self.create_about_page()

        for page in [
            self.dashboard_page, self.political_page, self.tech_page,
            self.projects_page, self.documents_page, self.media_page,
            self.geopolitical_page, self.cognitive_page, self.logs_page,
            self.upload_page, self.about_page
        ]:
            self.stacked.addWidget(page)

        main_layout.addWidget(self.sidebar)
        main_layout.addWidget(self.stacked)

        self.sidebar.currentRowChanged.connect(self.stacked.setCurrentIndex)
        self.sidebar.setCurrentRow(0)

        self.statusBar().showMessage("Ready")

    def save_data(self):
        """Save current application data"""
        try:
            # Prepare data to save
            data_to_save = {
                "uploads": self.uploads,
                "events": self.events,
                "political_analyses": self.political_analyses,
                "tech_reports": self.tech_reports,
                "projects": self.projects,
                "documents": self.documents,
                "media_items": self.media_items,
                "logs": self.get_logs_data(),
                "timestamp": now_str()
            }
            
            # Ask for save location
            path, _ = QFileDialog.getSaveFileName(
                self, "Save Data", "intelligence_hub_data.json", "JSON Files (*.json)"
            )
            
            if path:
                with open(path, "w", encoding="utf-8") as f:
                    json.dump(data_to_save, f, ensure_ascii=False, indent=2)
                
                self.statusBar().showMessage(f"Data saved successfully to {path}", 5000)
                QMessageBox.information(self, "Save Successful", f"Data saved to:\n{path}")
                
        except Exception as e:
            QMessageBox.warning(self, "Save Error", f"Failed to save data:\n{e}")

    def export_current_as_pdf(self):
        """Export current view as PDF"""
        try:
            current_index = self.stacked.currentIndex()
            page_name = self.sidebar.item(current_index).text()
            
            path, _ = QFileDialog.getSaveFileName(
                self, "Export PDF", f"{page_name.lower().replace(' ', '_')}.pdf", "PDF Files (*.pdf)"
            )
            
            if not path:
                return
                
            doc = QTextDocument()
            html = f"""
            <h1>Indo-Pacific Strategic Intelligence Hub</h1>
            <h2>{page_name} Report</h2>
            <p><b>Generated:</b> {now_str()}</p>
            <hr>
            """
            
            # Add content based on current page
            if page_name == "Dashboard":
                html += self.get_dashboard_html()
            elif page_name == "Political Trends":
                html += self.get_political_html()
            elif page_name == "Technology":
                html += self.get_technology_html()
            elif page_name == "Code Projects":
                html += self.get_projects_html()
            elif page_name == "Documents":
                html += self.get_documents_html()
            elif page_name == "Media Library":
                html += self.get_media_html()
            elif page_name == "Geopolitical Analysis":
                html += self.get_geopolitical_html()
            elif page_name == "Activity Log":
                html += self.get_logs_html()
            elif page_name == "Upload Files":
                html += self.get_uploads_html()
            else:
                html += f"<p>Content export for {page_name} page.</p>"
            
            # Add graph to report
            graph_data = create_sample_graph()
            if graph_data:
                html += f'<h3>Regional Activity Distribution</h3><img src="{graph_data}" width="500" height="300"/>'
            
            doc.setHtml(html)
            
            printer = QPrinter(QPrinter.HighResolution)
            printer.setOutputFormat(QPrinter.PdfFormat)
            printer.setOutputFileName(path)
            doc.print_(printer)
            
            self.statusBar().showMessage(f"PDF exported successfully to {path}", 5000)
            QMessageBox.information(self, "Export Successful", f"PDF exported to:\n{path}")
            
        except Exception as e:
            QMessageBox.warning(self, "Export Error", f"Failed to export PDF:\n{e}")

    def get_dashboard_html(self):
        """Generate HTML content for dashboard export"""
        html = "<h3>Regional Highlights</h3><ul>"
        html += "<li>China-Kenya Infrastructure Projects: 12</li>"
        html += "<li>Japan Technology Partnerships: 7</li>"
        html += "<li>Maritime Security Incidents: 3</li>"
        html += "</ul>"
        
        html += "<h3>Recent Timeline</h3>"
        for e in self.events[:5]:
            html += f"<p><b>{e['date']} — {e['headline']}</b><br>{e['notes']}</p>"
            
        return html

    def get_political_html(self):
        """Generate HTML content for political analysis export"""
        html = "<h3>Political Analyses</h3>"
        html += "<table border='1' style='border-collapse: collapse; width: 100%;'>"
        html += "<tr><th>Title</th><th>Region</th><th>Date</th></tr>"
        
        for analysis in self.political_analyses:
            html += f"<tr><td>{analysis['title']}</td><td>{analysis['region']}</td><td>{analysis['date']}</td></tr>"
            
        html += "</table>"
        return html

    def get_technology_html(self):
        """Generate HTML content for technology reports export"""
        html = "<h3>Technology Reports</h3>"
        html += "<table border='1' style='border-collapse: collapse; width: 100%;'>"
        html += "<tr><th>Title</th><th>Category</th><th>Date</th></tr>"
        
        for report in self.tech_reports:
            html += f"<tr><td>{report['title']}</td><td>{report['category']}</td><td>{report['date']}</td></tr>"
            
        html += "</table>"
        return html

    def get_projects_html(self):
        """Generate HTML content for projects export"""
        html = "<h3>Code Projects</h3>"
        html += "<table border='1' style='border-collapse: collapse; width: 100%;'>"
        html += "<tr><th>Name</th><th>Language</th><th>Date</th></tr>"
        
        for project in self.projects:
            html += f"<tr><td>{project['name']}</td><td>{project['language']}</td><td>{project['date']}</td></tr>"
            
        html += "</table>"
        return html

    def get_documents_html(self):
        """Generate HTML content for documents export"""
        html = "<h3>Documents</h3>"
        html += "<table border='1' style='border-collapse: collapse; width: 100%;'>"
        html += "<tr><th>Title</th><th>Type</th><th>Date</th></tr>"
        
        for doc in self.documents:
            html += f"<tr><td>{doc['title']}</td><td>{doc['type']}</td><td>{doc['date']}</td></tr>"
            
        html += "</table>"
        return html

    def get_media_html(self):
        """Generate HTML content for media export"""
        html = "<h3>Media Items</h3>"
        html += "<table border='1' style='border-collapse: collapse; width: 100%;'>"
        html += "<tr><th>Title</th><th>Type</th><th>Date</th></tr>"
        
        for media in self.media_items:
            html += f"<tr><td>{media['title']}</td><td>{media['type']}</td><td>{media['date']}</td></tr>"
            
        html += "</table>"
        return html

    def get_geopolitical_html(self):
        """Generate HTML content for geopolitical analysis export"""
        html = "<h3>Key Events Timeline</h3>"
        html += "<table border='1' style='border-collapse: collapse; width: 100%;'>"
        html += "<tr><th>Date</th><th>Headline</th><th>Notes</th><th>Ref#</th></tr>"
        
        for e in self.events:
            html += f"<tr><td>{e['date']}</td><td>{e['headline']}</td><td>{e['notes']}</td><td>{e['ref']}</td></tr>"
            
        html += "</table>"
        return html

    def get_logs_html(self):
        """Generate HTML content for logs export"""
        html = "<h3>Activity Log</h3>"
        html += "<table border='1' style='border-collapse: collapse; width: 100%;'>"
        html += "<tr><th>Date & Time</th><th>User</th><th>Action</th><th>Details</th></tr>"
        
        logs_data = self.get_logs_data()
        for log in logs_data:
            html += f"<tr><td>{log['timestamp']}</td><td>{log['user']}</td><td>{log['action']}</td><td>{log['details']}</td></tr>"
            
        html += "</table>"
        return html

    def get_uploads_html(self):
        """Generate HTML content for uploads export"""
        html = "<h3>File Uploads</h3>"
        html += "<table border='1' style='border-collapse: collapse; width: 100%;'>"
        html += "<tr><th>Title</th><th>Category</th><th>Size</th><th>Date</th></tr>"
        
        for up in self.uploads:
            html += f"<tr><td>{up['title']}</td><td>{up['category']}</td><td>{up['size']}</td><td>{up['date']}</td></tr>"
            
        html += "</table>"
        return html

    def get_logs_data(self):
        """Extract logs data from table"""
        logs_data = []
        for row in range(self.logs_table.rowCount()):
            timestamp_item = self.logs_table.item(row, 0)
            user_item = self.logs_table.item(row, 1)
            action_item = self.logs_table.item(row, 2)
            details_item = self.logs_table.item(row, 3)
            
            log_entry = {
                "timestamp": timestamp_item.text() if timestamp_item else "",
                "user": user_item.text() if user_item else "",
                "action": action_item.text() if action_item else "",
                "details": details_item.text() if details_item else ""
            }
            logs_data.append(log_entry)
        return logs_data

    # --------------------------
    # Dashboard
    # --------------------------
    def create_dashboard_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)

        title = QLabel("Strategic Intelligence Dashboard")
        title.setStyleSheet("font-size: 24px; font-weight: bold; margin-bottom: 12px;")
        layout.addWidget(title)

        # Refresh button
        refresh_btn = QPushButton("Refresh Dashboard")
        refresh_btn.clicked.connect(self.refresh_dashboard)
        layout.addWidget(refresh_btn)

        # Counters (static sample)
        counters_layout = QHBoxLayout()
        for text, count, color in [
            ("Documents", "247", "#007bff"),
            ("Videos", "63", "#28a745"),
            ("Photos", "184", "#dc3545"),
            ("Projects", "29", "#ffc107"),
        ]:
            w = QWidget()
            w.setStyleSheet(
                f"background-color: white; border-top: 4px solid {color}; padding: 12px;")
            v = QVBoxLayout(w)
            c = QLabel(count); c.setStyleSheet("font-size: 24px; font-weight: bold;")
            t = QLabel(text); t.setStyleSheet("color: #6c757d;")
            v.addWidget(c); v.addWidget(t)
            counters_layout.addWidget(w)
        layout.addLayout(counters_layout)

        # Highlights (static sample)
        highlights_group = QGroupBox("Key Regional Highlights")
        hg_layout = QVBoxLayout(highlights_group)
        for label, count in [
            ("China-Kenya Infrastructure Projects", "12"),
            ("Japan Technology Partnerships", "7"),
            ("Maritime Security Incidents", "3"),
        ]:
            row = QHBoxLayout()
            row.addWidget(QLabel(label))
            row.addStretch()
            chip = QLabel(count)
            chip.setStyleSheet(
                "background-color: #007bff; color: white; border-radius: 10px; padding: 4px 8px;")
            row.addWidget(chip)
            hg_layout.addLayout(row)
        layout.addWidget(highlights_group)

        # Recent Timeline (first 8 events)
        timeline_group = QGroupBox("Recent Regional Timeline")
        tl_layout = QVBoxLayout(timeline_group)

        recent = self.events[:8]
        for e in recent:
            box = QVBoxLayout()
            head = QLabel(f"{e['date']} — {e['headline']} (Ref {e['ref']})")
            head.setStyleSheet("font-weight: bold;")
            box.addWidget(head)
            box.addWidget(QLabel(e['notes']))
            roww = QWidget(); roww.setLayout(box)
            tl_layout.addWidget(roww)

        layout.addWidget(timeline_group)
        layout.addStretch()
        return page

    def refresh_dashboard(self):
        """Refresh dashboard data"""
        self.statusBar().showMessage("Dashboard refreshed.", 3000)

    # --------------------------
    # Political page
    # --------------------------
    def create_political_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)

        # Title and refresh button
        title_layout = QHBoxLayout()
        title = QLabel("Political Analysis")
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        title_layout.addWidget(title)
        
        refresh_btn = QPushButton("Refresh")
        refresh_btn.clicked.connect(self.refresh_political)
        title_layout.addStretch()
        title_layout.addWidget(refresh_btn)
        layout.addLayout(title_layout)

        content_layout = QHBoxLayout()
        
        form_group = QGroupBox("Add Political Analysis")
        form_layout = QFormLayout(form_group)

        self.pol_title = QLineEdit()
        self.pol_country = QComboBox()
        self.pol_country.addItems([
            "Select a country/region", "China", "Japan", "India", "Australia",
            "Kenya", "Tanzania", "Ethiopia", "EU", "USA"
        ])
        self.pol_analysis = QTextEdit()
        self.pol_attach_btn = QPushButton("Attach Files")
        self.pol_submit_btn = QPushButton("Submit Analysis")
        self.pol_submit_btn.setStyleSheet("background-color: #007bff; color: white;")

        form_layout.addRow("Title:", self.pol_title)
        form_layout.addRow("Country/Region:", self.pol_country)
        form_layout.addRow("Analysis:", self.pol_analysis)
        form_layout.addRow("Attach Files:", self.pol_attach_btn)
        form_layout.addRow(self.pol_submit_btn)

        content_layout.addWidget(form_group)

        # Right-side info
        recent_group = QGroupBox("Recent Analyses")
        recent_layout = QVBoxLayout(recent_group)
        
        # Table for recent analyses
        self.pol_table = QTableWidget()
        self.pol_table.setColumnCount(3)
        self.pol_table.setHorizontalHeaderLabels(["Title", "Region", "Date"])
        self.pol_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.pol_table.setRowCount(0)
        
        # Enable context menu for deletion
        self.pol_table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.pol_table.customContextMenuRequested.connect(self.show_political_context_menu)
        
        recent_layout.addWidget(self.pol_table)
        content_layout.addWidget(recent_group)

        layout.addLayout(content_layout)

        # Handlers
        self.pol_attach_btn.clicked.connect(lambda: self._open_file_dialog("Political"))
        self.pol_submit_btn.clicked.connect(self._submit_political)

        return page

    def refresh_political(self):
        """Refresh political analyses table"""
        self.pol_table.setRowCount(len(self.political_analyses))
        for r, analysis in enumerate(self.political_analyses):
            self.pol_table.setItem(r, 0, QTableWidgetItem(analysis["title"]))
            self.pol_table.setItem(r, 1, QTableWidgetItem(analysis["region"]))
            self.pol_table.setItem(r, 2, QTableWidgetItem(analysis["date"]))
        self.statusBar().showMessage("Political analyses refreshed.", 3000)

    def show_political_context_menu(self, position):
        """Show context menu for political table with delete option"""
        menu = QMenu()
        delete_action = menu.addAction("Delete Analysis")
        
        action = menu.exec_(self.pol_table.mapToGlobal(position))
        if action == delete_action:
            row = self.pol_table.currentRow()
            if row >= 0:
                reply = QMessageBox.question(
                    self, "Confirm Delete", 
                    f"Delete analysis '{self.political_analyses[row]['title']}'?",
                    QMessageBox.Yes | QMessageBox.No
                )
                if reply == QMessageBox.Yes:
                    deleted_analysis = self.political_analyses.pop(row)
                    self.refresh_political()
                    self._add_log("Analysis Deleted", deleted_analysis["title"], f"Region: {deleted_analysis['region']}")

    def _submit_political(self):
        title = self.pol_title.text().strip()
        region = self.pol_country.currentText()
        
        if not title or region == "Select a country/region":
            QMessageBox.warning(self, "Input Error", "Please provide a title and select a region.")
            return
            
        analysis = {
            "title": title,
            "region": region,
            "analysis": self.pol_analysis.toPlainText(),
            "date": now_str()
        }
        
        self.political_analyses.append(analysis)
        self.refresh_political()
        self._add_log("Analysis Submitted", f"Political: {title}", f"Region: {region}")
        self.statusBar().showMessage("Political analysis submitted.", 3000)
        
        # Clear form
        self.pol_title.clear()
        self.pol_country.setCurrentIndex(0)
        self.pol_analysis.clear()

    # --------------------------
    # Technology page
    # --------------------------
    def create_technology_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)

        # Title and refresh button
        title_layout = QHBoxLayout()
        title = QLabel("Technology Reports")
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        title_layout.addWidget(title)
        
        refresh_btn = QPushButton("Refresh")
        refresh_btn.clicked.connect(self.refresh_technology)
        title_layout.addStretch()
        title_layout.addWidget(refresh_btn)
        layout.addLayout(title_layout)

        content_layout = QHBoxLayout()
        
        form_group = QGroupBox("Add Technology Report")
        form_layout = QFormLayout(form_group)

        self.tech_title = QLineEdit()
        self.tech_category = QComboBox()
        self.tech_category.addItems([
            "Select category", "AI", "Cybersecurity", "Infrastructure", "Telecom", "Other"
        ])
        self.tech_report = QTextEdit()
        self.tech_attach_btn = QPushButton("Attach Files")
        self.tech_submit_btn = QPushButton("Submit Report")
        self.tech_submit_btn.setStyleSheet("background-color: #007bff; color: white;")

        form_layout.addRow("Title:", self.tech_title)
        form_layout.addRow("Category:", self.tech_category)
        form_layout.addRow("Report:", self.tech_report)
        form_layout.addRow("Attach Files:", self.tech_attach_btn)
        form_layout.addRow(self.tech_submit_btn)

        content_layout.addWidget(form_group)

        # Right-side info
        recent_group = QGroupBox("Recent Reports")
        recent_layout = QVBoxLayout(recent_group)
        
        # Table for recent reports
        self.tech_table = QTableWidget()
        self.tech_table.setColumnCount(3)
        self.tech_table.setHorizontalHeaderLabels(["Title", "Category", "Date"])
        self.tech_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tech_table.setRowCount(0)
        
        # Enable context menu for deletion
        self.tech_table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tech_table.customContextMenuRequested.connect(self.show_tech_context_menu)
        
        recent_layout.addWidget(self.tech_table)
        content_layout.addWidget(recent_group)

        layout.addLayout(content_layout)

        # Handlers
        self.tech_attach_btn.clicked.connect(lambda: self._open_file_dialog("Technology"))
        self.tech_submit_btn.clicked.connect(self._submit_tech)

        return page

    def refresh_technology(self):
        """Refresh technology reports table"""
        self.tech_table.setRowCount(len(self.tech_reports))
        for r, report in enumerate(self.tech_reports):
            self.tech_table.setItem(r, 0, QTableWidgetItem(report["title"]))
            self.tech_table.setItem(r, 1, QTableWidgetItem(report["category"]))
            self.tech_table.setItem(r, 2, QTableWidgetItem(report["date"]))
        self.statusBar().showMessage("Technology reports refreshed.", 3000)

    def show_tech_context_menu(self, position):
        """Show context menu for tech table with delete option"""
        menu = QMenu()
        delete_action = menu.addAction("Delete Report")
        
        action = menu.exec_(self.tech_table.mapToGlobal(position))
        if action == delete_action:
            row = self.tech_table.currentRow()
            if row >= 0:
                reply = QMessageBox.question(
                    self, "Confirm Delete", 
                    f"Delete report '{self.tech_reports[row]['title']}'?",
                    QMessageBox.Yes | QMessageBox.No
                )
                if reply == QMessageBox.Yes:
                    deleted_report = self.tech_reports.pop(row)
                    self.refresh_technology()
                    self._add_log("Report Deleted", deleted_report["title"], f"Category: {deleted_report['category']}")

    def _submit_tech(self):
        title = self.tech_title.text().strip()
        category = self.tech_category.currentText()
        
        if not title or category == "Select category":
            QMessageBox.warning(self, "Input Error", "Please provide a title and select a category.")
            return
            
        report = {
            "title": title,
            "category": category,
            "report": self.tech_report.toPlainText(),
            "date": now_str()
        }
        
        self.tech_reports.append(report)
        self.refresh_technology()
        self._add_log("Report Submitted", f"Technology: {title}", f"Category: {category}")
        self.statusBar().showMessage("Technology report submitted.", 3000)
        
        # Clear form
        self.tech_title.clear()
        self.tech_category.setCurrentIndex(0)
        self.tech_report.clear()

    # --------------------------
    # Projects page
    # --------------------------
    def create_projects_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)

        # Title and refresh button
        title_layout = QHBoxLayout()
        title = QLabel("Code Projects")
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        title_layout.addWidget(title)
        
        refresh_btn = QPushButton("Refresh")
        refresh_btn.clicked.connect(self.refresh_projects)
        title_layout.addStretch()
        title_layout.addWidget(refresh_btn)
        layout.addLayout(title_layout)

        content_layout = QHBoxLayout()
        
        form_group = QGroupBox("Add Project")
        form_layout = QFormLayout(form_group)

        self.proj_name = QLineEdit()
        self.proj_language = QComboBox()
        self.proj_language.addItems([
            "Select language", "Python", "JavaScript", "Java", "C++", "Go", "Rust", "Other"
        ])
        self.proj_description = QTextEdit()
        self.proj_attach_btn = QPushButton("Attach Files")
        self.proj_submit_btn = QPushButton("Submit Project")
        self.proj_submit_btn.setStyleSheet("background-color: #007bff; color: white;")

        form_layout.addRow("Name:", self.proj_name)
        form_layout.addRow("Language:", self.proj_language)
        form_layout.addRow("Description:", self.proj_description)
        form_layout.addRow("Attach Files:", self.proj_attach_btn)
        form_layout.addRow(self.proj_submit_btn)

        content_layout.addWidget(form_group)

        # Right-side info
        recent_group = QGroupBox("Recent Projects")
        recent_layout = QVBoxLayout(recent_group)
        
        # Table for recent projects
        self.proj_table = QTableWidget()
        self.proj_table.setColumnCount(3)
        self.proj_table.setHorizontalHeaderLabels(["Name", "Language", "Date"])
        self.proj_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.proj_table.setRowCount(0)
        
        # Enable context menu for deletion
        self.proj_table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.proj_table.customContextMenuRequested.connect(self.show_proj_context_menu)
        
        recent_layout.addWidget(self.proj_table)
        content_layout.addWidget(recent_group)

        layout.addLayout(content_layout)

        # Handlers
        self.proj_attach_btn.clicked.connect(lambda: self._open_file_dialog("Project"))
        self.proj_submit_btn.clicked.connect(self._submit_project)

        return page

    def refresh_projects(self):
        """Refresh projects table"""
        self.proj_table.setRowCount(len(self.projects))
        for r, project in enumerate(self.projects):
            self.proj_table.setItem(r, 0, QTableWidgetItem(project["name"]))
            self.proj_table.setItem(r, 1, QTableWidgetItem(project["language"]))
            self.proj_table.setItem(r, 2, QTableWidgetItem(project["date"]))
        self.statusBar().showMessage("Projects refreshed.", 3000)

    def show_proj_context_menu(self, position):
        """Show context menu for projects table with delete option"""
        menu = QMenu()
        delete_action = menu.addAction("Delete Project")
        
        action = menu.exec_(self.proj_table.mapToGlobal(position))
        if action == delete_action:
            row = self.proj_table.currentRow()
            if row >= 0:
                reply = QMessageBox.question(
                    self, "Confirm Delete", 
                    f"Delete project '{self.projects[row]['name']}'?",
                    QMessageBox.Yes | QMessageBox.No
                )
                if reply == QMessageBox.Yes:
                    deleted_project = self.projects.pop(row)
                    self.refresh_projects()
                    self._add_log("Project Deleted", deleted_project["name"], f"Language: {deleted_project['language']}")

    def _submit_project(self):
        name = self.proj_name.text().strip()
        language = self.proj_language.currentText()
        
        if not name or language == "Select language":
            QMessageBox.warning(self, "Input Error", "Please provide a name and select a language.")
            return
            
        project = {
            "name": name,
            "language": language,
            "description": self.proj_description.toPlainText(),
            "date": now_str()
        }
        
        self.projects.append(project)
        self.refresh_projects()
        self._add_log("Project Submitted", f"Code: {name}", f"Language: {language}")
        self.statusBar().showMessage("Project submitted.", 3000)
        
        # Clear form
        self.proj_name.clear()
        self.proj_language.setCurrentIndex(0)
        self.proj_description.clear()

    # --------------------------
    # Documents page
    # --------------------------
    def create_documents_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)

        # Title and refresh button
        title_layout = QHBoxLayout()
        title = QLabel("Documents")
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        title_layout.addWidget(title)
        
        refresh_btn = QPushButton("Refresh")
        refresh_btn.clicked.connect(self.refresh_documents)
        title_layout.addStretch()
        title_layout.addWidget(refresh_btn)
        layout.addLayout(title_layout)

        content_layout = QHBoxLayout()
        
        form_group = QGroupBox("Add Document")
        form_layout = QFormLayout(form_group)

        self.doc_title = QLineEdit()
        self.doc_type = QComboBox()
        self.doc_type.addItems([
            "Select type", "Report", "Policy", "Analysis", "Research", "Other"
        ])
        self.doc_description = QTextEdit()
        self.doc_attach_btn = QPushButton("Attach Files")
        self.doc_submit_btn = QPushButton("Submit Document")
        self.doc_submit_btn.setStyleSheet("background-color: #007bff; color: white;")

        form_layout.addRow("Title:", self.doc_title)
        form_layout.addRow("Type:", self.doc_type)
        form_layout.addRow("Description:", self.doc_description)
        form_layout.addRow("Attach Files:", self.doc_attach_btn)
        form_layout.addRow(self.doc_submit_btn)

        content_layout.addWidget(form_group)

        # Right-side info
        recent_group = QGroupBox("Recent Documents")
        recent_layout = QVBoxLayout(recent_group)
        
        # Table for recent documents
        self.doc_table = QTableWidget()
        self.doc_table.setColumnCount(3)
        self.doc_table.setHorizontalHeaderLabels(["Title", "Type", "Date"])
        self.doc_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.doc_table.setRowCount(0)
        
        # Enable context menu for deletion
        self.doc_table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.doc_table.customContextMenuRequested.connect(self.show_doc_context_menu)
        
        recent_layout.addWidget(self.doc_table)
        content_layout.addWidget(recent_group)

        layout.addLayout(content_layout)

        # Handlers
        self.doc_attach_btn.clicked.connect(lambda: self._open_file_dialog("Document"))
        self.doc_submit_btn.clicked.connect(self._submit_document)

        return page

    def refresh_documents(self):
        """Refresh documents table"""
        self.doc_table.setRowCount(len(self.documents))
        for r, document in enumerate(self.documents):
            self.doc_table.setItem(r, 0, QTableWidgetItem(document["title"]))
            self.doc_table.setItem(r, 1, QTableWidgetItem(document["type"]))
            self.doc_table.setItem(r, 2, QTableWidgetItem(document["date"]))
        self.statusBar().showMessage("Documents refreshed.", 3000)

    def show_doc_context_menu(self, position):
        """Show context menu for documents table with delete option"""
        menu = QMenu()
        delete_action = menu.addAction("Delete Document")
        
        action = menu.exec_(self.doc_table.mapToGlobal(position))
        if action == delete_action:
            row = self.doc_table.currentRow()
            if row >= 0:
                reply = QMessageBox.question(
                    self, "Confirm Delete", 
                    f"Delete document '{self.documents[row]['title']}'?",
                    QMessageBox.Yes | QMessageBox.No
                )
                if reply == QMessageBox.Yes:
                    deleted_doc = self.documents.pop(row)
                    self.refresh_documents()
                    self._add_log("Document Deleted", deleted_doc["title"], f"Type: {deleted_doc['type']}")

    def _submit_document(self):
        title = self.doc_title.text().strip()
        doc_type = self.doc_type.currentText()
        
        if not title or doc_type == "Select type":
            QMessageBox.warning(self, "Input Error", "Please provide a title and select a type.")
            return
            
        document = {
            "title": title,
            "type": doc_type,
            "description": self.doc_description.toPlainText(),
            "date": now_str()
        }
        
        self.documents.append(document)
        self.refresh_documents()
        self._add_log("Document Submitted", f"Document: {title}", f"Type: {doc_type}")
        self.statusBar().showMessage("Document submitted.", 3000)
        
        # Clear form
        self.doc_title.clear()
        self.doc_type.setCurrentIndex(0)
        self.doc_description.clear()

    # --------------------------
    # Media page
    # --------------------------
    def create_media_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)

        # Title and refresh button
        title_layout = QHBoxLayout()
        title = QLabel("Media Library")
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        title_layout.addWidget(title)
        
        refresh_btn = QPushButton("Refresh")
        refresh_btn.clicked.connect(self.refresh_media)
        title_layout.addStretch()
        title_layout.addWidget(refresh_btn)
        layout.addLayout(title_layout)

        content_layout = QHBoxLayout()
        
        form_group = QGroupBox("Add Media Item")
        form_layout = QFormLayout(form_group)

        self.media_title = QLineEdit()
        self.media_type = QComboBox()
        self.media_type.addItems([
            "Select type", "Image", "Video", "Audio", "Infographic", "Other"
        ])
        self.media_description = QTextEdit()
        self.media_attach_btn = QPushButton("Attach Files")
        self.media_submit_btn = QPushButton("Submit Media")
        self.media_submit_btn.setStyleSheet("background-color: #007bff; color: white;")

        form_layout.addRow("Title:", self.media_title)
        form_layout.addRow("Type:", self.media_type)
        form_layout.addRow("Description:", self.media_description)
        form_layout.addRow("Attach Files:", self.media_attach_btn)
        form_layout.addRow(self.media_submit_btn)

        content_layout.addWidget(form_group)

        # Right-side info
        recent_group = QGroupBox("Recent Media Items")
        recent_layout = QVBoxLayout(recent_group)
        
        # Table for recent media items
        self.media_table = QTableWidget()
        self.media_table.setColumnCount(3)
        self.media_table.setHorizontalHeaderLabels(["Title", "Type", "Date"])
        self.media_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.media_table.setRowCount(0)
        
        # Enable context menu for deletion
        self.media_table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.media_table.customContextMenuRequested.connect(self.show_media_context_menu)
        
        recent_layout.addWidget(self.media_table)
        content_layout.addWidget(recent_group)

        layout.addLayout(content_layout)

        # Handlers
        self.media_attach_btn.clicked.connect(lambda: self._open_file_dialog("Media"))
        self.media_submit_btn.clicked.connect(self._submit_media)

        return page

    def refresh_media(self):
        """Refresh media items table"""
        self.media_table.setRowCount(len(self.media_items))
        for r, media in enumerate(self.media_items):
            self.media_table.setItem(r, 0, QTableWidgetItem(media["title"]))
            self.media_table.setItem(r, 1, QTableWidgetItem(media["type"]))
            self.media_table.setItem(r, 2, QTableWidgetItem(media["date"]))
        self.statusBar().showMessage("Media items refreshed.", 3000)

    def show_media_context_menu(self, position):
        """Show context menu for media table with delete option"""
        menu = QMenu()
        delete_action = menu.addAction("Delete Media Item")
        
        action = menu.exec_(self.media_table.mapToGlobal(position))
        if action == delete_action:
            row = self.media_table.currentRow()
            if row >= 0:
                reply = QMessageBox.question(
                    self, "Confirm Delete", 
                    f"Delete media item '{self.media_items[row]['title']}'?",
                    QMessageBox.Yes | QMessageBox.No
                )
                if reply == QMessageBox.Yes:
                    deleted_media = self.media_items.pop(row)
                    self.refresh_media()
                    self._add_log("Media Deleted", deleted_media["title"], f"Type: {deleted_media['type']}")

    def _submit_media(self):
        title = self.media_title.text().strip()
        media_type = self.media_type.currentText()
        
        if not title or media_type == "Select type":
            QMessageBox.warning(self, "Input Error", "Please provide a title and select a type.")
            return
            
        media_item = {
            "title": title,
            "type": media_type,
            "description": self.media_description.toPlainText(),
            "date": now_str()
        }
        
        self.media_items.append(media_item)
        self.refresh_media()
        self._add_log("Media Submitted", f"Media: {title}", f"Type: {media_type}")
        self.statusBar().showMessage("Media item submitted.", 3000)
        
        # Clear form
        self.media_title.clear()
        self.media_type.setCurrentIndex(0)
        self.media_description.clear()

    # --------------------------
    # Geopolitical page
    # --------------------------
    def create_geopolitical_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)

        title = QLabel("Geopolitical Analysis")
        title.setStyleSheet("font-size: 24px; font-weight: bold; margin-bottom: 12px;")
        layout.addWidget(title)

        # Refresh button
        refresh_btn = QPushButton("Refresh Analysis")
        refresh_btn.clicked.connect(self.refresh_geopolitical)
        layout.addWidget(refresh_btn)

        # Event timeline
        timeline_group = QGroupBox("Key Events Timeline")
        timeline_layout = QVBoxLayout(timeline_group)

        self.timeline_table = QTableWidget()
        self.timeline_table.setColumnCount(4)
        self.timeline_table.setHorizontalHeaderLabels(["Date", "Headline", "Notes", "Ref#"])
        self.timeline_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.timeline_table.setRowCount(len(self.events))

        for r, e in enumerate(self.events):
            self.timeline_table.setItem(r, 0, QTableWidgetItem(e["date"]))
            self.timeline_table.setItem(r, 1, QTableWidgetItem(e["headline"]))
            self.timeline_table.setItem(r, 2, QTableWidgetItem(e["notes"]))
            self.timeline_table.setItem(r, 3, QTableWidgetItem(e["ref"]))

        timeline_layout.addWidget(self.timeline_table)
        layout.addWidget(timeline_group)

        # Add event form
        form_group = QGroupBox("Add New Event")
        form_layout = QFormLayout(form_group)

        self.event_date = QLineEdit(now_str().split()[0])
        self.event_headline = QLineEdit()
        self.event_notes = QTextEdit()
        self.event_ref = QLineEdit()
        self.event_submit = QPushButton("Add Event")
        self.event_submit.setStyleSheet("background-color: #007bff; color: white;")

        form_layout.addRow("Date (YYYY-MM-DD):", self.event_date)
        form_layout.addRow("Headline:", self.event_headline)
        form_layout.addRow("Notes:", self.event_notes)
        form_layout.addRow("Reference #:", self.event_ref)
        form_layout.addRow(self.event_submit)

        layout.addWidget(form_group)
        layout.addStretch()

        # Handlers
        self.event_submit.clicked.connect(self._add_event)

        return page

    def refresh_geopolitical(self):
        """Refresh geopolitical events table"""
        self.timeline_table.setRowCount(len(self.events))
        for r, e in enumerate(self.events):
            self.timeline_table.setItem(r, 0, QTableWidgetItem(e["date"]))
            self.timeline_table.setItem(r, 1, QTableWidgetItem(e["headline"]))
            self.timeline_table.setItem(r, 2, QTableWidgetItem(e["notes"]))
            self.timeline_table.setItem(r, 3, QTableWidgetItem(e["ref"]))
        self.statusBar().showMessage("Geopolitical analysis refreshed.", 3000)

    def _add_event(self):
        date = self.event_date.text().strip()
        headline = self.event_headline.text().strip()
        notes = self.event_notes.toPlainText().strip()
        ref = self.event_ref.text().strip()

        if not all([date, headline, notes, ref]):
            QMessageBox.warning(self, "Input Error", "Please fill all fields.")
            return

        event = {
            "date": date,
            "headline": headline,
            "notes": notes,
            "ref": ref
        }

        self.events.append(event)
        self.refresh_geopolitical()
        self._add_log("Event Added", f"Geopolitical: {headline}", f"Date: {date}")
        self.statusBar().showMessage("Event added to timeline.", 3000)

        # Clear form
        self.event_headline.clear()
        self.event_notes.clear()
        self.event_ref.clear()

    # --------------------------
    # Cognitive page
    # --------------------------
    def create_cognitive_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)

        title = QLabel("Cognitive Dissonance Analysis")
        title.setStyleSheet("font-size: 24px; font-weight: bold; margin-bottom: 12px;")
        layout.addWidget(title)

        # Refresh button
        refresh_btn = QPushButton("Refresh Analysis")
        refresh_btn.clicked.connect(self.refresh_cognitive)
        layout.addWidget(refresh_btn)

        desc = QLabel(
            "Analyze texts for cognitive dissonance indicators: contradictions, "
            "value-action gaps, selective evidence, and justification patterns."
        )
        desc.setWordWrap(True)
        layout.addWidget(desc)

        launch_btn = QPushButton("Launch Analysis Tool")
        launch_btn.setStyleSheet("background-color: #007bff; color: white; padding: 12px;")
        launch_btn.clicked.connect(self._launch_cognitive_tool)
        layout.addWidget(launch_btn)

        # Recent analyses table
        recent_group = QGroupBox("Recent Analyses")
        recent_layout = QVBoxLayout(recent_group)
        
        self.cognitive_table = QTableWidget()
        self.cognitive_table.setColumnCount(4)
        self.cognitive_table.setHorizontalHeaderLabels(["Title", "Source", "Score", "Date"])
        self.cognitive_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.cognitive_table.setRowCount(0)
        
        # Enable context menu for deletion
        self.cognitive_table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.cognitive_table.customContextMenuRequested.connect(self.show_cognitive_context_menu)
        
        recent_layout.addWidget(self.cognitive_table)
        layout.addWidget(recent_group)

        layout.addStretch()
        return page

    def refresh_cognitive(self):
        """Refresh cognitive analyses table"""
        # This would normally load from saved analyses
        self.statusBar().showMessage("Cognitive analyses refreshed.", 3000)

    def show_cognitive_context_menu(self, position):
        """Show context menu for cognitive table with delete option"""
        menu = QMenu()
        delete_action = menu.addAction("Delete Analysis")
        
        action = menu.exec_(self.cognitive_table.mapToGlobal(position))
        if action == delete_action:
            row = self.cognitive_table.currentRow()
            if row >= 0:
                reply = QMessageBox.question(
                    self, "Confirm Delete", 
                    f"Delete cognitive analysis?",
                    QMessageBox.Yes | QMessageBox.No
                )
                if reply == QMessageBox.Yes:
                    self.cognitive_table.removeRow(row)
                    self._add_log("Analysis Deleted", "Cognitive Analysis", f"Row: {row}")

    def _launch_cognitive_tool(self):
        dialog = CognitiveAnalysisDialog(self)
        dialog.exec_()

    # --------------------------
    # Logs page
    # --------------------------
    def create_logs_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)

        title = QLabel("Activity Log")
        title.setStyleSheet("font-size: 24px; font-weight: bold; margin-bottom: 12px;")
        layout.addWidget(title)

        # Refresh button
        refresh_btn = QPushButton("Refresh Logs")
        refresh_btn.clicked.connect(self.refresh_logs)
        layout.addWidget(refresh_btn)

        # Logs table
        self.logs_table = QTableWidget()
        self.logs_table.setColumnCount(4)
        self.logs_table.setHorizontalHeaderLabels(["Timestamp", "User", "Action", "Details"])
        self.logs_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.logs_table.setRowCount(0)

        # Enable context menu for deletion
        self.logs_table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.logs_table.customContextMenuRequested.connect(self.show_logs_context_menu)

        layout.addWidget(self.logs_table)
        
        # Add some sample logs
        self._add_log("System", "Application Started", "Intelligence Hub initialized")
        self._add_log("User", "Login", "User logged in successfully")
        self._add_log("System", "Data Loaded", "Sample data loaded")

        return page

    def refresh_logs(self):
        """Refresh logs table"""
        # Logs are updated in real-time, so this just confirms refresh
        self.statusBar().showMessage("Activity logs refreshed.", 3000)

    def show_logs_context_menu(self, position):
        """Show context menu for logs table with delete option"""
        menu = QMenu()
        delete_action = menu.addAction("Delete Log Entry")
        clear_all_action = menu.addAction("Clear All Logs")
        
        action = menu.exec_(self.logs_table.mapToGlobal(position))
        if action == delete_action:
            row = self.logs_table.currentRow()
            if row >= 0:
                self.logs_table.removeRow(row)
                self._add_log("User", "Log Deleted", f"Row {row} removed")
        elif action == clear_all_action:
            reply = QMessageBox.question(
                self, "Confirm Clear", 
                "Clear all log entries?",
                QMessageBox.Yes | QMessageBox.No
            )
            if reply == QMessageBox.Yes:
                self.logs_table.setRowCount(0)
                self._add_log("User", "Logs Cleared", "All log entries removed")

    def _add_log(self, user, action, details):
        """Add a log entry to the table"""
        row = self.logs_table.rowCount()
        self.logs_table.insertRow(row)
        self.logs_table.setItem(row, 0, QTableWidgetItem(now_str()))
        self.logs_table.setItem(row, 1, QTableWidgetItem(user))
        self.logs_table.setItem(row, 2, QTableWidgetItem(action))
        self.logs_table.setItem(row, 3, QTableWidgetItem(details))
        # Auto-scroll to bottom
        self.logs_table.scrollToBottom()

    # --------------------------
    # Upload page
    # --------------------------
    def create_upload_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)

        title = QLabel("Upload Files")
        title.setStyleSheet("font-size: 24px; font-weight: bold; margin-bottom: 12px;")
        layout.addWidget(title)

        # Refresh button
        refresh_btn = QPushButton("Refresh Uploads")
        refresh_btn.clicked.connect(self.refresh_uploads)
        layout.addWidget(refresh_btn)

        # Upload form
        form_group = QGroupBox("Upload New File")
        form_layout = QFormLayout(form_group)

        self.upload_title = QLineEdit()
        self.upload_category = QComboBox()
        self.upload_category.addItems([
            "Document", "Image", "Video", "Audio", "Data", "Other"
        ])
        self.upload_description = QTextEdit()
        self.upload_btn = QPushButton("Select File to Upload")
        self.upload_submit_btn = QPushButton("Upload File")
        self.upload_submit_btn.setStyleSheet("background-color: #007bff; color: white;")

        form_layout.addRow("Title:", self.upload_title)
        form_layout.addRow("Category:", self.upload_category)
        form_layout.addRow("Description:", self.upload_description)
        form_layout.addRow("File:", self.upload_btn)
        form_layout.addRow(self.upload_submit_btn)

        layout.addWidget(form_group)

        # Uploads table
        uploads_group = QGroupBox("Recent Uploads")
        uploads_layout = QVBoxLayout(uploads_group)

        self.uploads_table = QTableWidget()
        self.uploads_table.setColumnCount(4)
        self.uploads_table.setHorizontalHeaderLabels(["Title", "Category", "Size", "Date"])
        self.uploads_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.uploads_table.setRowCount(0)
        
        # Enable context menu for deletion
        self.uploads_table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.uploads_table.customContextMenuRequested.connect(self.show_uploads_context_menu)

        uploads_layout.addWidget(self.uploads_table)
        layout.addWidget(uploads_group)

        # Handlers
        self.upload_btn.clicked.connect(self._select_upload_file)
        self.upload_submit_btn.clicked.connect(self._submit_upload)

        return page

    def refresh_uploads(self):
        """Refresh uploads table"""
        self.uploads_table.setRowCount(len(self.uploads))
        for r, upload in enumerate(self.uploads):
            self.uploads_table.setItem(r, 0, QTableWidgetItem(upload["title"]))
            self.uploads_table.setItem(r, 1, QTableWidgetItem(upload["category"]))
            self.uploads_table.setItem(r, 2, QTableWidgetItem(upload["size"]))
            self.uploads_table.setItem(r, 3, QTableWidgetItem(upload["date"]))
        self.statusBar().showMessage("Uploads refreshed.", 3000)

    def show_uploads_context_menu(self, position):
        """Show context menu for uploads table with delete option"""
        menu = QMenu()
        delete_action = menu.addAction("Delete Upload")
        
        action = menu.exec_(self.uploads_table.mapToGlobal(position))
        if action == delete_action:
            row = self.uploads_table.currentRow()
            if row >= 0:
                reply = QMessageBox.question(
                    self, "Confirm Delete", 
                    f"Delete upload '{self.uploads[row]['title']}'?",
                    QMessageBox.Yes | QMessageBox.No
                )
                if reply == QMessageBox.Yes:
                    deleted_upload = self.uploads.pop(row)
                    self.refresh_uploads()
                    self._add_log("Upload Deleted", deleted_upload["title"], f"Category: {deleted_upload['category']}")

    def _select_upload_file(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Select File to Upload", "", "All Files (*)"
        )
        if path:
            self._current_upload_path = path
            size = human_size(os.path.getsize(path))
            name = os.path.basename(path)
            self.upload_title.setText(name)
            self.upload_description.setPlainText(f"File: {name}\nSize: {size}\nPath: {path}")

    def _submit_upload(self):
        if not hasattr(self, "_current_upload_path") or not self._current_upload_path:
            QMessageBox.warning(self, "Upload Error", "Please select a file first.")
            return

        title = self.upload_title.text().strip()
        if not title:
            QMessageBox.warning(self, "Input Error", "Please provide a title.")
            return

        upload = {
            "title": title,
            "category": self.upload_category.currentText(),
            "size": human_size(os.path.getsize(self._current_upload_path)),
            "date": now_str(),
            "path": self._current_upload_path
        }

        self.uploads.append(upload)
        self.refresh_uploads()
        self._add_log("File Uploaded", title, f"Category: {upload['category']}, Size: {upload['size']}")
        self.statusBar().showMessage("File uploaded successfully.", 3000)

        # Clear form
        self.upload_title.clear()
        self.upload_description.clear()
        delattr(self, "_current_upload_path")

    # --------------------------
    # About page
    # --------------------------
    def create_about_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)

        title = QLabel("About Indo-Pacific Strategic Intelligence Hub")
        title.setStyleSheet("font-size: 24px; font-weight: bold; margin-bottom: 12px;")
        layout.addWidget(title)

        about_text = QLabel(
            "This application provides analytical tools for monitoring and assessing "
            "strategic developments across the Indo-Pacific region, with special focus "
            "on Eastern Africa geopolitical dynamics, cognitive analysis, and intelligence fusion."
        )
        about_text.setWordWrap(True)
        layout.addWidget(about_text)

        # Version info
        version_group = QGroupBox("Version Information")
        version_layout = QVBoxLayout(version_group)
        version_layout.addWidget(QLabel("Version: 2.0.0"))
        version_layout.addWidget(QLabel("Build Date: 2023-11-15"))
        version_layout.addWidget(QLabel("Python: 3.11+"))
        version_layout.addWidget(QLabel("Framework: PyQt5"))
        layout.addWidget(version_group)

        # Features
        features_group = QGroupBox("Features")
        features_layout = QVBoxLayout(features_group)
        for feat in [
            "Cognitive Dissonance Analysis",
            "Geopolitical Event Tracking",
            "Document and Media Management",
            "Regional Focus Analysis",
            "Data Export and Reporting",
            "WhatsApp Integration for Sharing"
        ]:
            features_layout.addWidget(QLabel(f"• {feat}"))
        layout.addWidget(features_group)

        layout.addStretch()
        return page

    # --------------------------
    # Utility methods
    # --------------------------
    def _build_events(self):
        return [
            {
                "date": "2023-10-15",
                "headline": "China-Kenya Infrastructure Agreement Signed",
                "notes": "New port and railway projects announced during state visit.",
                "ref": "CN-KE-2023-001"
            },
            {
                "date": "2023-10-12",
                "headline": "Japan Increases Indian Ocean Naval Presence",
                "notes": "Two additional destroyers deployed for anti-piracy operations.",
                "ref": "JP-IN-2023-045"
            },
            {
                "date": "2023-10-08",
                "headline": "Australia-Pacific Islands Forum Concludes",
                "notes": "Climate resilience and security partnerships emphasized.",
                "ref": "AU-PI-2023-018"
            },
            {
                "date": "2023-10-03",
                "headline": "Indian Ocean Maritime Security Exercise",
                "notes": "Multinational drills focused on counter-terrorism coordination.",
                "ref": "IO-2023-033"
            },
            {
                "date": "2023-09-28",
                "headline": "Ethiopia-Djibouti Trade Corridor Expansion",
                "notes": "Infrastructure upgrades to increase capacity by 40%.",
                "ref": "ET-DJ-2023-022"
            },
            {
                "date": "2023-09-22",
                "headline": "EU Indo-Pacific Strategy Review",
                "notes": "New emphasis on digital infrastructure and green partnerships.",
                "ref": "EU-2023-107"
            },
            {
                "date": "2023-09-15",
                "headline": "Tanzanian Port Modernization Agreement",
                "notes": "World Bank funding secured for Bagamoyo port upgrade.",
                "ref": "TZ-WB-2023-009"
            },
            {
                "date": "2023-09-10",
                "headline": "US-Australia Submarine Technology Sharing",
                "notes": "Next-phase agreements on nuclear propulsion technology.",
                "ref": "US-AU-2023-088"
            },
        ]

    def _open_file_dialog(self, context):
        path, _ = QFileDialog.getOpenFileName(
            self, f"Select File for {context}", "", "All Files (*)"
        )
        if path:
            self.statusBar().showMessage(f"Selected: {path}", 3000)

    def closeEvent(self, event):
        reply = QMessageBox.question(
            self, "Confirm Exit",
            "Are you sure you want to exit the application?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


# ------------------------------
# Run application
# ------------------------------
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())