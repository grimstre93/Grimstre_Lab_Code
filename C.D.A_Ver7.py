# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime, timedelta
import json
import csv
from fpdf import FPDF
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import sys
import os

class CognitiveDissonanceAnalyzer:
    def __init__(self, root):
        self.root = root
        self.root.title("Cognitive Dissonance Thought Analyzer")
        self.root.geometry("1000x800")
        
        # Set application icon if exists
        if hasattr(sys, '_MEIPASS'):
            icon_path = os.path.join(sys._MEIPASS, 'icon.ico')
        else:
            icon_path = 'icon.ico'
        
        try:
            self.root.iconbitmap(icon_path)
        except:
            pass
        
        # Data storage
        self.users = []
        self.thoughts = []
        self.current_user = None
        
        # Load data
        self.load_data()
        
        # Create UI
        self.create_widgets()
        
        # Initialize with empty fields
        self.add_consonant_field()
        self.add_dissonant_field()
        
    def load_data(self):
        try:
            with open('users.json', 'r', encoding='utf-8') as f:
                self.users = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.users = []
            
        try:
            with open('thoughts.json', 'r', encoding='utf-8') as f:
                self.thoughts = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.thoughts = []
    
    def save_data(self):
        with open('users.json', 'w', encoding='utf-8') as f:
            json.dump(self.users, f, ensure_ascii=False)
            
        with open('thoughts.json', 'w', encoding='utf-8') as f:
            json.dump(self.thoughts, f, ensure_ascii=False)
    
    def create_widgets(self):
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Create tabs
        self.create_info_tab()
        self.create_login_tab()
        self.create_analysis_tab()
        self.create_history_tab()
    
    def create_info_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Information")
        
        info_text = """Cognitive Dissonance Thought Analyzer

D* = D / (D + C)

Where:
- D* = Total magnitude of dissonance (0-1 scale)
- D = Count of dissonant elements
- C = Count of consonant elements

Examples:
- Consonant: "I exercise" and "Exercise is healthy"
- Dissonant: "I smoke" and "Smoking causes cancer\""""
        
        label = tk.Label(tab, text=info_text, justify=tk.LEFT, padx=10, pady=10)
        label.pack(anchor=tk.W)
    
    # [All other methods remain exactly the same as in the original code...]
    # Only the encoding-related changes were made to file operations
    
    def generate_pdf(self, data, file_path, selected_user):
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        
        # Title with UTF-8 support
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(0, 10, "Cognitive Dissonance Analysis Report".encode('latin-1', 'replace').decode('latin-1'), 0, 1, 'C')
        pdf.ln(5)
        
        # Report info
        pdf.set_font("Arial", size=12)
        pdf.cell(0, 10, f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", 0, 1)
        pdf.cell(0, 10, f"User: {'All users' if selected_user == 'All users' else selected_user}", 0, 1)
        pdf.ln(5)
        
        # [Rest of the PDF generation code remains the same...]
        # Ensure to use .encode('latin-1', 'replace').decode('latin-1') for any user-generated text

if __name__ == "__main__":
    # Handle high DPI displays on Windows
    if sys.platform == "win32":
        from ctypes import windll
        windll.shcore.SetProcessDpiAwareness(1)
    
    root = tk.Tk()
    app = CognitiveDissonanceAnalyzer(root)
    root.mainloop()
