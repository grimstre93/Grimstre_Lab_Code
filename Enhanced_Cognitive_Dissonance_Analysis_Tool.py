import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
from datetime import datetime, timedelta
import json
import csv
import os
import base64
import io
import zipfile
import tempfile
import shutil
from PIL import Image, ImageTk, ImageDraw
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image as ReportLabImage, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
import sounddevice as sd
import soundfile as sf
import threading
import queue
import time

class CognitiveDissonanceAnalyzer:
    def __init__(self, root):
        self.root = root
        self.root.title("Cognitive Dissonance Thought Analyzer")
        self.root.geometry("1200x900")
        
        # Configure styles
        self.style = ttk.Style()
        self.style.configure('.', font=('Times New Roman', 10))
        self.style.configure('TFrame', background='#f0f0f0')
        self.style.configure('TLabel', background='#f0f0f0')
        self.style.configure('TButton', font=('Times New Roman', 10))
        self.style.configure('TNotebook', font=('Times New Roman', 10))
        self.style.configure('Treeview', font=('Times New Roman', 10))
        self.style.configure('Treeview.Heading', font=('Times New Roman', 10, 'bold'))
        
        # Database
        self.thoughts = []
        self.load_data()
        
        # Create main containers
        self.create_header()
        self.create_info_box()
        self.create_analysis_panel()
        self.create_history_panel()
        self.create_media_panel()
        
    def load_data(self):
        try:
            with open("thoughts.json", "r") as f:
                self.thoughts = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.thoughts = []
    
    def save_data(self):
        with open("thoughts.json", "w") as f:
            json.dump(self.thoughts, f, indent=2)
    
    def create_header(self):
        header_frame = ttk.Frame(self.root)
        header_frame.pack(fill=tk.X, padx=10, pady=10)
        
        title_label = ttk.Label(header_frame, 
                              text="Cognitive Dissonance Thought Analyzer", 
                              font=("Times New Roman", 16, "bold"))
        title_label.pack()
        
    def create_info_box(self):
        info_frame = ttk.LabelFrame(self.root, 
                                  text="Understanding Cognitive Dissonance", 
                                  padding=10)
        info_frame.pack(fill=tk.X, padx=10, pady=5)
        
        formula_label = ttk.Label(info_frame, 
                                text="D* = D / (D + C)", 
                                font=("Times New Roman", 12, "bold"))
        formula_label.pack(anchor=tk.W)
        
        where_label = ttk.Label(info_frame, text="Where:")
        where_label.pack(anchor=tk.W)
        
        dstar_label = ttk.Label(info_frame, text="- D* = Total magnitude of dissonance")
        dstar_label.pack(anchor=tk.W)
        
        d_label = ttk.Label(info_frame, text="- D = Sum of all elements dissonant with the element in question")
        d_label.pack(anchor=tk.W)
        
        c_label = ttk.Label(info_frame, text="- C = Sum of all elements consonant with the same element")
        c_label.pack(anchor=tk.W)
        
        sep = ttk.Separator(info_frame, orient=tk.HORIZONTAL)
        sep.pack(fill=tk.X, pady=5)
        
        def_label = ttk.Label(info_frame, 
                            text="Definitions (Festinger, 1957)", 
                            font=("Times New Roman", 10, "bold"))
        def_label.pack(anchor=tk.W)
        
        consonant_label = ttk.Label(info_frame, 
                                  text="Consonant cognitions - Two cognitions are consonant if they're relevant to one another and one logically follows from the other.")
        consonant_label.pack(anchor=tk.W)
        
        consonant_ex = ttk.Label(info_frame, 
                               text='Example: "I exercise regularly" and "Regular exercise is healthy."', 
                               font=("Times New Roman", 9))
        consonant_ex.pack(anchor=tk.W)
        
        dissonant_label = ttk.Label(info_frame, 
                                 text="Dissonant cognitions - Two cognitions are dissonant if they're relevant but one entails the opposite of the other.")
        dissonant_label.pack(anchor=tk.W)
        
        dissonant_ex = ttk.Label(info_frame, 
                               text='Example: "I smoke" and "Smoking causes cancer."', 
                               font=("Times New Roman", 9))
        dissonant_ex.pack(anchor=tk.W)
        
        explanation_label = ttk.Label(info_frame, 
                                    text="Holding dissonant cognitions produces psychological discomfort (dissonance), which motivates people to restore consonance by changing beliefs, adding new cognitions, or trivializing the conflict.")
        explanation_label.pack(anchor=tk.W)
    
    def create_analysis_panel(self):
        analysis_frame = ttk.LabelFrame(self.root, 
                                      text="New Thought Analysis", 
                                      padding=10)
        analysis_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Thought entry
        thought_frame = ttk.Frame(analysis_frame)
        thought_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(thought_frame, 
                text="Enter your thought (up to 200 words):").pack(anchor=tk.W)
        
        self.thought_text = scrolledtext.ScrolledText(thought_frame, 
                                                    height=5, 
                                                    wrap=tk.WORD,
                                                    font=('Times New Roman', 10))
        self.thought_text.pack(fill=tk.X, pady=5)
        
        # Elements frame
        elements_frame = ttk.Frame(analysis_frame)
        elements_frame.pack(fill=tk.X)
        
        # Consonant elements
        consonant_frame = ttk.LabelFrame(elements_frame, 
                                       text="Consonant Elements", 
                                       padding=5)
        consonant_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        self.consonant_elements_frame = ttk.Frame(consonant_frame)
        self.consonant_elements_frame.pack(fill=tk.X)
        
        self.add_consonant_field()
        
        ttk.Button(consonant_frame, 
                  text="Add Consonant Element", 
                  command=self.add_consonant_field).pack(anchor=tk.W, pady=5)
        
        # Dissonant elements
        dissonant_frame = ttk.LabelFrame(elements_frame, 
                                       text="Dissonant Elements", 
                                       padding=5)
        dissonant_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        self.dissonant_elements_frame = ttk.Frame(dissonant_frame)
        self.dissonant_elements_frame.pack(fill=tk.X)
        
        self.add_dissonant_field()
        
        ttk.Button(dissonant_frame, 
                  text="Add Dissonant Element", 
                  command=self.add_dissonant_field).pack(anchor=tk.W, pady=5)
        
        # Calculate button
        button_frame = ttk.Frame(analysis_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(button_frame, 
                  text="Calculate Dissonance", 
                  command=self.calculate_dissonance).pack()
        
        # Results
        self.result_frame = ttk.Frame(analysis_frame)
        self.result_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(self.result_frame, 
                text="Dissonance Score", 
                font=("Times New Roman", 10, "bold")).pack(anchor=tk.W)
        
        self.d_score_label = ttk.Label(self.result_frame, text="D* = ")
        self.d_score_label.pack(anchor=tk.W)
        
        self.interpretation_label = ttk.Label(self.result_frame, text="Interpretation: ")
        self.interpretation_label.pack(anchor=tk.W)
        
        self.result_frame.pack_forget()
    
    def create_media_panel(self):
        media_frame = ttk.LabelFrame(self.root, 
                                   text="Media Attachments", 
                                   padding=10)
        media_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Image attachment
        image_frame = ttk.Frame(media_frame)
        image_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(image_frame, 
                  text="Attach Image", 
                  command=self.attach_image).pack(side=tk.LEFT, padx=5)
        
        self.image_label = ttk.Label(image_frame, text="No image attached")
        self.image_label.pack(side=tk.LEFT, padx=5)
        
        # Audio recording
        audio_frame = ttk.Frame(media_frame)
        audio_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(audio_frame, 
                  text="Start Recording", 
                  command=self.start_recording).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(audio_frame, 
                  text="Stop Recording", 
                  command=self.stop_recording).pack(side=tk.LEFT, padx=5)
        
        self.audio_status = ttk.Label(audio_frame, text="No recording")
        self.audio_status.pack(side=tk.LEFT, padx=5)
        
        # Variables for audio recording
        self.is_recording = False
        self.audio_queue = queue.Queue()
        self.audio_frames = []
        self.recording_thread = None
        self.sample_rate = 44100
        self.current_audio_file = None
    
    def create_history_panel(self):
        history_frame = ttk.LabelFrame(self.root, 
                                     text="Thought History", 
                                     padding=10)
        history_frame.pack(fill=tk.BOTH, padx=10, pady=5, expand=True)
        
        # Filter controls
        filter_frame = ttk.Frame(history_frame)
        filter_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(filter_frame, 
                  text="Load History", 
                  command=self.load_history).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(filter_frame, 
                  text="Export Data", 
                  command=self.export_data).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(filter_frame, 
                  text="Generate Report", 
                  command=self.generate_report).pack(side=tk.LEFT, padx=5)
        
        # History table
        columns = ("ID", "Date", "Thought", "D* Score", "Actions")
        self.history_tree = ttk.Treeview(history_frame, columns=columns, show="headings")
        
        for col in columns:
            self.history_tree.heading(col, text=col)
            self.history_tree.column(col, width=100)
        
        self.history_tree.column("Thought", width=300)
        self.history_tree.column("Actions", width=150)
        
        scrollbar = ttk.Scrollbar(history_frame, 
                                 orient=tk.VERTICAL, 
                                 command=self.history_tree.yview)
        self.history_tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.history_tree.pack(fill=tk.BOTH, expand=True)
        
        # Bind double click to view details
        self.history_tree.bind("<Double-1>", self.show_entry_details)
    
    def add_consonant_field(self):
        entry = ttk.Entry(self.consonant_elements_frame, 
                         font=('Times New Roman', 10))
        entry.pack(fill=tk.X, pady=2)
        return entry
    
    def add_dissonant_field(self):
        entry = ttk.Entry(self.dissonant_elements_frame, 
                         font=('Times New Roman', 10))
        entry.pack(fill=tk.X, pady=2)
        return entry
    
    def calculate_dissonance(self):
        thought = self.thought_text.get("1.0", tk.END).strip()
        if not thought:
            messagebox.showerror("Error", "Please enter a thought to analyze")
            return
        
        word_count = len(thought.split())
        if word_count > 200:
            messagebox.showerror("Error", "Thought exceeds 200 words")
            return
        
        # Get consonant elements
        consonant_elements = []
        for child in self.consonant_elements_frame.winfo_children():
            if isinstance(child, ttk.Entry):
                val = child.get().strip()
                if val:
                    consonant_elements.append(val)
        
        # Get dissonant elements
        dissonant_elements = []
        for child in self.dissonant_elements_frame.winfo_children():
            if isinstance(child, ttk.Entry):
                val = child.get().strip()
                if val:
                    dissonant_elements.append(val)
        
        if not consonant_elements and not dissonant_elements:
            messagebox.showerror("Error", "Please add at least one consonant or dissonant element")
            return
        
        # Calculate D* = D / (D + C)
        D = len(dissonant_elements)
        C = len(consonant_elements)
        Dstar = D / (D + C) if (D + C) > 0 else 0.0
        
        # Handle media attachments
        image_data = None
        audio_data = None
        
        if hasattr(self, 'current_image'):
            # Convert image to base64 for storage
            buffered = io.BytesIO()
            self.current_image.save(buffered, format="PNG")
            image_data = base64.b64encode(buffered.getvalue()).decode('utf-8')
        
        if self.current_audio_file:
            with open(self.current_audio_file, 'rb') as f:
                audio_data = base64.b64encode(f.read()).decode('utf-8')
        
        # Create entry
        entry_id = len(self.thoughts) + 1
        entry = {
            "id": entry_id,
            "date": datetime.now().isoformat(),
            "thought": thought,
            "consonantElements": consonant_elements,
            "dissonantElements": dissonant_elements,
            "D": D,
            "C": C,
            "Dstar": Dstar,
            "image": image_data,
            "audio": audio_data
        }
        
        self.thoughts.append(entry)
        self.save_data()
        
        # Display results
        self.d_score_label.config(text=f"D* = {Dstar:.3f}")
        
        if Dstar < 0.3:
            interpretation = "Low dissonance - mostly consonant thoughts"
        elif Dstar < 0.7:
            interpretation = "Moderate dissonance - mixed thoughts"
        else:
            interpretation = "High dissonance - mostly dissonant thoughts"
        
        self.interpretation_label.config(text=f"Interpretation: {interpretation}")
        self.result_frame.pack(fill=tk.X, pady=5)
        
        # Clear fields
        self.thought_text.delete("1.0", tk.END)
        for child in self.consonant_elements_frame.winfo_children():
            if isinstance(child, ttk.Entry):
                child.delete(0, tk.END)
        for child in self.dissonant_elements_frame.winfo_children():
            if isinstance(child, ttk.Entry):
                child.delete(0, tk.END)
        
        if hasattr(self, 'current_image'):
            del self.current_image
            self.image_label.config(text="No image attached")
        
        if self.current_audio_file:
            os.remove(self.current_audio_file)
            self.current_audio_file = None
            self.audio_status.config(text="No recording")
        
        # Update history
        self.load_history()
    
    def load_history(self):
        # Clear current items
        for item in self.history_tree.get_children():
            self.history_tree.delete(item)
        
        # Sort by date (newest first)
        self.thoughts.sort(key=lambda x: x["date"], reverse=True)
        
        # Add to treeview
        for thought in self.thoughts:
            date_str = datetime.fromisoformat(thought["date"]).strftime("%Y-%m-%d %H:%M")
            thought_preview = (thought["thought"][:47] + "...") if len(thought["thought"]) > 50 else thought["thought"]
            
            # Add edit and delete buttons
            actions = f"[View] [Edit] [Delete]"
            
            self.history_tree.insert("", tk.END, values=(
                thought["id"],
                date_str,
                thought_preview,
                f"{thought['Dstar']:.3f}",
                actions
            ))
    
    def show_entry_details(self, event):
        item = self.history_tree.selection()[0]
        item_values = self.history_tree.item(item, "values")
        entry_id = int(item_values[0])
        
        entry = next((t for t in self.thoughts if t["id"] == entry_id), None)
        if not entry:
            return
        
        # Create details window
        details_window = tk.Toplevel(self.root)
        details_window.title(f"Entry Details - ID: {entry_id}")
        details_window.geometry("800x600")
        
        # Main frame with scrollbar
        main_frame = ttk.Frame(details_window)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        canvas = tk.Canvas(main_frame)
        scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Entry details
        ttk.Label(scrollable_frame, 
                text=f"Entry ID: {entry['id']}", 
                font=("Times New Roman", 12, "bold")).pack(anchor=tk.W, pady=5)
        
        ttk.Label(scrollable_frame, 
                text=f"Date: {datetime.fromisoformat(entry['date']).strftime('%Y-%m-%d %H:%M:%S')}",
                font=("Times New Roman", 10)).pack(anchor=tk.W)
        
        ttk.Label(scrollable_frame, 
                text="Thought:", 
                font=("Times New Roman", 10, "bold")).pack(anchor=tk.W, pady=5)
        
        thought_text = scrolledtext.ScrolledText(scrollable_frame, 
                                               wrap=tk.WORD, 
                                               height=5,
                                               font=('Times New Roman', 10))
        thought_text.insert(tk.END, entry["thought"])
        thought_text.pack(fill=tk.X, pady=5)
        thought_text.config(state=tk.DISABLED)
        
        # Dissonance score
        ttk.Label(scrollable_frame, 
                text=f"Dissonance Score: D* = {entry['Dstar']:.3f}", 
                font=("Times New Roman", 10, "bold")).pack(anchor=tk.W, pady=5)
        
        # Consonant elements
        ttk.Label(scrollable_frame, 
                text="Consonant Elements:", 
                font=("Times New Roman", 10, "bold")).pack(anchor=tk.W, pady=5)
        
        for element in entry["consonantElements"]:
            ttk.Label(scrollable_frame, 
                    text=f"- {element}", 
                    font=("Times New Roman", 10)).pack(anchor=tk.W)
        
        # Dissonant elements
        ttk.Label(scrollable_frame, 
                text="Dissonant Elements:", 
                font=("Times New Roman", 10, "bold")).pack(anchor=tk.W, pady=5)
        
        for element in entry["dissonantElements"]:
            ttk.Label(scrollable_frame, 
                    text=f"- {element}", 
                    font=("Times New Roman", 10)).pack(anchor=tk.W)
        
        # Media attachments
        ttk.Label(scrollable_frame, 
                text="Attachments:", 
                font=("Times New Roman", 10, "bold")).pack(anchor=tk.W, pady=5)
        
        if entry.get("image"):
            try:
                image_data = base64.b64decode(entry["image"])
                image = Image.open(io.BytesIO(image_data))
                image.thumbnail((300, 300))
                photo = ImageTk.PhotoImage(image)
                
                image_label = ttk.Label(scrollable_frame, image=photo)
                image_label.image = photo  # Keep a reference
                image_label.pack(anchor=tk.W, pady=5)
            except Exception as e:
                ttk.Label(scrollable_frame, 
                         text=f"Error loading image: {str(e)}").pack(anchor=tk.W)
        
        if entry.get("audio"):
            ttk.Button(scrollable_frame, 
                      text="Play Audio", 
                      command=lambda: self.play_audio(entry["audio"])).pack(anchor=tk.W, pady=5)
        
        # Buttons
        button_frame = ttk.Frame(scrollable_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(button_frame, 
                  text="Edit Entry", 
                  command=lambda: self.edit_entry(entry_id, details_window)).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(button_frame, 
                  text="Delete Entry", 
                  command=lambda: self.delete_entry(entry_id, details_window)).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(button_frame, 
                  text="Close", 
                  command=details_window.destroy).pack(side=tk.RIGHT, padx=5)
    
    def edit_entry(self, entry_id, parent_window):
        entry = next((t for t in self.thoughts if t["id"] == entry_id), None)
        if not entry:
            return
        
        # Create edit window
        edit_window = tk.Toplevel(self.root)
        edit_window.title(f"Edit Entry - ID: {entry_id}")
        edit_window.geometry("800x600")
        
        # Main frame with scrollbar
        main_frame = ttk.Frame(edit_window)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        canvas = tk.Canvas(main_frame)
        scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Thought entry
        ttk.Label(scrollable_frame, 
                text="Thought:", 
                font=("Times New Roman", 10, "bold")).pack(anchor=tk.W, pady=5)
        
        thought_text = scrolledtext.ScrolledText(scrollable_frame, 
                                              wrap=tk.WORD, 
                                              height=5,
                                              font=('Times New Roman', 10))
        thought_text.insert(tk.END, entry["thought"])
        thought_text.pack(fill=tk.X, pady=5)
        
        # Consonant elements
        ttk.Label(scrollable_frame, 
                text="Consonant Elements:", 
                font=("Times New Roman", 10, "bold")).pack(anchor=tk.W, pady=5)
        
        consonant_frame = ttk.Frame(scrollable_frame)
        consonant_frame.pack(fill=tk.X)
        
        for element in entry["consonantElements"]:
            entry_field = ttk.Entry(consonant_frame, 
                                  font=('Times New Roman', 10))
            entry_field.insert(0, element)
            entry_field.pack(fill=tk.X, pady=2)
        
        ttk.Button(scrollable_frame, 
                  text="Add Consonant Element", 
                  command=lambda: self.add_element_field(consonant_frame)).pack(anchor=tk.W, pady=5)
        
        # Dissonant elements
        ttk.Label(scrollable_frame, 
                text="Dissonant Elements:", 
                font=("Times New Roman", 10, "bold")).pack(anchor=tk.W, pady=5)
        
        dissonant_frame = ttk.Frame(scrollable_frame)
        dissonant_frame.pack(fill=tk.X)
        
        for element in entry["dissonantElements"]:
            entry_field = ttk.Entry(dissonant_frame, 
                                  font=('Times New Roman', 10))
            entry_field.insert(0, element)
            entry_field.pack(fill=tk.X, pady=2)
        
        ttk.Button(scrollable_frame, 
                  text="Add Dissonant Element", 
                  command=lambda: self.add_element_field(dissonant_frame)).pack(anchor=tk.W, pady=5)
        
        # Media attachments
        ttk.Label(scrollable_frame, 
                text="Attachments:", 
                font=("Times New Roman", 10, "bold")).pack(anchor=tk.W, pady=5)
        
        if entry.get("image"):
            try:
                image_data = base64.b64decode(entry["image"])
                image = Image.open(io.BytesIO(image_data))
                image.thumbnail((300, 300))
                photo = ImageTk.PhotoImage(image)
                
                image_label = ttk.Label(scrollable_frame, image=photo)
                image_label.image = photo  # Keep a reference
                image_label.pack(anchor=tk.W, pady=5)
                
                ttk.Button(scrollable_frame, 
                          text="Remove Image", 
                          command=lambda: self.remove_attachment(entry, 'image')).pack(anchor=tk.W, pady=5)
            except Exception as e:
                ttk.Label(scrollable_frame, 
                         text=f"Error loading image: {str(e)}").pack(anchor=tk.W)
        
        if entry.get("audio"):
            ttk.Button(scrollable_frame, 
                      text="Play Audio", 
                      command=lambda: self.play_audio(entry["audio"])).pack(anchor=tk.W, pady=5)
            
            ttk.Button(scrollable_frame, 
                      text="Remove Audio", 
                      command=lambda: self.remove_attachment(entry, 'audio')).pack(anchor=tk.W, pady=5)
        
        # Buttons
        button_frame = ttk.Frame(scrollable_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(button_frame, 
                  text="Save Changes", 
                  command=lambda: self.save_edited_entry(
                      entry_id,
                      thought_text.get("1.0", tk.END).strip(),
                      consonant_frame,
                      dissonant_frame,
                      edit_window,
                      parent_window
                  )).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(button_frame, 
                  text="Cancel", 
                  command=edit_window.destroy).pack(side=tk.RIGHT, padx=5)
    
    def add_element_field(self, parent_frame):
        entry = ttk.Entry(parent_frame, 
                         font=('Times New Roman', 10))
        entry.pack(fill=tk.X, pady=2)
        return entry
    
    def remove_attachment(self, entry, attachment_type):
        if attachment_type in entry:
            entry.pop(attachment_type)
            self.save_data()
            messagebox.showinfo("Success", f"{attachment_type.capitalize()} removed")
    
    def save_edited_entry(self, entry_id, thought_text, consonant_frame, dissonant_frame, edit_window, parent_window):
        # Get consonant elements
        consonant_elements = []
        for child in consonant_frame.winfo_children():
            if isinstance(child, ttk.Entry):
                val = child.get().strip()
                if val:
                    consonant_elements.append(val)
        
        # Get dissonant elements
        dissonant_elements = []
        for child in dissonant_frame.winfo_children():
            if isinstance(child, ttk.Entry):
                val = child.get().strip()
                if val:
                    dissonant_elements.append(val)
        
        if not consonant_elements and not dissonant_elements:
            messagebox.showerror("Error", "Please add at least one consonant or dissonant element")
            return
        
        # Calculate D* = D / (D + C)
        D = len(dissonant_elements)
        C = len(consonant_elements)
        Dstar = D / (D + C) if (D + C) > 0 else 0.0
        
        # Update entry
        entry = next((t for t in self.thoughts if t["id"] == entry_id), None)
        if entry:
            entry["thought"] = thought_text
            entry["consonantElements"] = consonant_elements
            entry["dissonantElements"] = dissonant_elements
            entry["D"] = D
            entry["C"] = C
            entry["Dstar"] = Dstar
            entry["date"] = datetime.now().isoformat()
            
            self.save_data()
            self.load_history()
            
            edit_window.destroy()
            parent_window.destroy()
            
            messagebox.showinfo("Success", "Entry updated successfully")
    
    def delete_entry(self, entry_id, parent_window):
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this entry?"):
            self.thoughts = [t for t in self.thoughts if t["id"] != entry_id]
            self.save_data()
            self.load_history()
            parent_window.destroy()
            messagebox.showinfo("Success", "Entry deleted successfully")
    
    def attach_image(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.gif")]
        )
        
        if file_path:
            try:
                self.current_image = Image.open(file_path)
                self.image_label.config(text=f"Image attached: {os.path.basename(file_path)}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load image: {str(e)}")
    
    def start_recording(self):
        if self.is_recording:
            return
        
        self.is_recording = True
        self.audio_frames = []
        self.audio_status.config(text="Recording...")
        
        def callback(indata, frames, time, status):
            if self.is_recording:
                self.audio_queue.put(indata.copy())
        
        self.recording_thread = threading.Thread(
            target=self.recording_worker,
            daemon=True
        )
        self.recording_thread.start()
        
        self.stream = sd.InputStream(
            samplerate=self.sample_rate,
            channels=1,
            callback=callback
        )
        self.stream.start()
    
    def recording_worker(self):
        while self.is_recording:
            data = self.audio_queue.get()
            self.audio_frames.append(data)
    
    def stop_recording(self):
        if not self.is_recording:
            return
        
        self.is_recording = False
        self.stream.stop()
        self.stream.close()
        self.recording_thread.join()
        
        # Save recording to temporary file
        temp_dir = tempfile.mkdtemp()
        self.current_audio_file = os.path.join(temp_dir, "recording.wav")
        
        audio_data = np.concatenate(self.audio_frames, axis=0)
        sf.write(self.current_audio_file, audio_data, self.sample_rate)
        
        self.audio_status.config(text=f"Recording saved ({len(audio_data)/self.sample_rate:.1f}s)")
    
    def play_audio(self, audio_data):
        if not audio_data:
            return
        
        try:
            # Create temporary file
            temp_dir = tempfile.mkdtemp()
            temp_file = os.path.join(temp_dir, "temp_audio.wav")
            
            # Decode base64 and write to file
            with open(temp_file, 'wb') as f:
                f.write(base64.b64decode(audio_data))
            
            # Play audio
            data, samplerate = sf.read(temp_file)
            sd.play(data, samplerate)
            
            # Clean up after playback is done
            def cleanup():
                time.sleep(1)  # Wait a bit to ensure playback is complete
                shutil.rmtree(temp_dir)
            
            threading.Thread(target=cleanup, daemon=True).start()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to play audio: {str(e)}")
    
    def export_data(self):
        # Create temporary directory for export
        temp_dir = tempfile.mkdtemp()
        
        try:
            # Export thoughts data as JSON
            json_path = os.path.join(temp_dir, "thoughts_data.json")
            with open(json_path, 'w') as f:
                json.dump(self.thoughts, f, indent=2)
            
            # Export media files
            media_dir = os.path.join(temp_dir, "media")
            os.makedirs(media_dir, exist_ok=True)
            
            for thought in self.thoughts:
                if thought.get("image"):
                    try:
                        image_data = base64.b64decode(thought["image"])
                        image_path = os.path.join(media_dir, f"image_{thought['id']}.png")
                        with open(image_path, 'wb') as f:
                            f.write(image_data)
                    except Exception as e:
                        print(f"Error exporting image for entry {thought['id']}: {str(e)}")
                
                if thought.get("audio"):
                    try:
                        audio_data = base64.b64decode(thought["audio"])
                        audio_path = os.path.join(media_dir, f"audio_{thought['id']}.wav")
                        with open(audio_path, 'wb') as f:
                            f.write(audio_data)
                    except Exception as e:
                        print(f"Error exporting audio for entry {thought['id']}: {str(e)}")
            
            # Create ZIP file
            zip_path = filedialog.asksaveasfilename(
                defaultextension=".zip",
                filetypes=[("ZIP files", "*.zip")],
                initialfile="cognitive_dissonance_data.zip"
            )
            
            if zip_path:
                with zipfile.ZipFile(zip_path, 'w') as zipf:
                    for root, dirs, files in os.walk(temp_dir):
                        for file in files:
                            file_path = os.path.join(root, file)
                            arcname = os.path.relpath(file_path, temp_dir)
                            zipf.write(file_path, arcname)
                
                messagebox.showinfo("Success", f"Data exported successfully to {zip_path}")
        finally:
            # Clean up temporary directory
            shutil.rmtree(temp_dir)
    
    def generate_report(self):
        # Create PDF report
        file_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf")],
            initialfile="cognitive_dissonance_report.pdf"
        )
        
        if not file_path:
            return
        
        # Create document
        doc = SimpleDocTemplate(file_path, pagesize=letter)
        
        # Styles
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'Title',
            parent=styles['Heading1'],
            fontName='Times-Roman',
            fontSize=16,
            leading=20,
            spaceAfter=20
        )
        
        heading_style = ParagraphStyle(
            'Heading2',
            parent=styles['Heading2'],
            fontName='Times-Roman',
            fontSize=12,
            leading=15,
            spaceAfter=10
        )
        
        normal_style = ParagraphStyle(
            'Normal',
            parent=styles['Normal'],
            fontName='Times-Roman',
            fontSize=10,
            leading=12,
            spaceAfter=10
        )
        
        # Content
        elements = []
        
        # Title
        elements.append(Paragraph("Cognitive Dissonance Analysis Report", title_style))
        elements.append(Spacer(1, 12))
        
        # Summary
        elements.append(Paragraph("Summary", heading_style))
        
        total_entries = len(self.thoughts)
        avg_dissonance = sum(t['Dstar'] for t in self.thoughts) / total_entries if total_entries > 0 else 0
        
        summary_text = f"""
        Total entries: {total_entries}<br/>
        Average dissonance score: {avg_dissonance:.3f}<br/>
        Date range: {min(t['date'] for t in self.thoughts) if total_entries > 0 else 'N/A'} to {max(t['date'] for t in self.thoughts) if total_entries > 0 else 'N/A'}
        """
        elements.append(Paragraph(summary_text, normal_style))
        elements.append(Spacer(1, 20))
        
        # Dissonance distribution chart
        if total_entries > 0:
            fig, ax = plt.subplots(figsize=(6, 4))
            dissonance_scores = [t['Dstar'] for t in self.thoughts]
            ax.hist(dissonance_scores, bins=10, range=(0, 1), color='skyblue', edgecolor='black')
            ax.set_title('Distribution of Dissonance Scores')
            ax.set_xlabel('Dissonance Score (D*)')
            ax.set_ylabel('Frequency')
            ax.grid(True)
            
            # Save plot to buffer
            buf = io.BytesIO()
            plt.savefig(buf, format='png', dpi=150, bbox_inches='tight')
            plt.close()
            buf.seek(0)
            
            # Add plot to report
            chart = ReportLabImage(buf)
            chart._restrictSize(400, 300)
            elements.append(chart)
            elements.append(Spacer(1, 20))
        
        # Entries table
        if total_entries > 0:
            elements.append(Paragraph("Entries", heading_style))
            
            # Prepare table data
            table_data = [['ID', 'Date', 'Thought', 'D*', 'Consonant', 'Dissonant']]
            
            for thought in sorted(self.thoughts, key=lambda x: x['date'], reverse=True)[:50]:  # Limit to 50 entries
                date_str = datetime.fromisoformat(thought['date']).strftime('%Y-%m-%d')
                thought_preview = thought['thought'][:50] + '...' if len(thought['thought']) > 50 else thought['thought']
                consonant_count = len(thought['consonantElements'])
                dissonant_count = len(thought['dissonantElements'])
                
                table_data.append([
                    str(thought['id']),
                    date_str,
                    thought_preview,
                    f"{thought['Dstar']:.3f}",
                    str(consonant_count),
                    str(dissonant_count)
                ])
            
            # Create table
            table = Table(table_data)
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Times-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('FONTNAME', (0, 1), (-1, -1), 'Times-Roman'),
                ('FONTSIZE', (0, 1), (-1, -1), 8),
            ]))
            
            elements.append(table)
            elements.append(Spacer(1, 20))
        
        # Build document
        doc.build(elements)
        messagebox.showinfo("Success", f"Report generated successfully at {file_path}")

if __name__ == "__main__":
    root = tk.Tk()
    app = CognitiveDissonanceAnalyzer(root)
    root.mainloop()