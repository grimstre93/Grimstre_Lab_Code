import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
from datetime import datetime
import json
import os
from pathlib import Path

class FinancialPsychologyToolkit:
    def __init__(self, root):
        self.root = root
        self.root.title("Psychology of Financial Planning Toolkit")
        self.root.geometry("1024x768")
        
        # Initialize components
        self.logger = AppLogger()
        self.media_handler = MediaHandler(self.logger)
        self.session_report = SessionReport(self.logger)
        
        # Build the UI
        self._setup_menu()
        self._setup_main_interface()
        
        # Initial log entry
        self.logger.log("Application started")

    def _setup_menu(self):
        menubar = tk.Menu(self.root)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="New Session", command=self._new_session)
        file_menu.add_command(label="Export Report", command=self._export_report)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        menubar.add_cascade(label="File", menu=file_menu)
        
        # View menu
        view_menu = tk.Menu(menubar, tearoff=0)
        view_menu.add_command(label="Toggle Log Panel", command=self._toggle_log_panel)
        menubar.add_cascade(label="View", menu=view_menu)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="About", command=self._show_about)
        menubar.add_cascade(label="Help", menu=help_menu)
        
        self.root.config(menu=menubar)

    def _setup_main_interface(self):
        # Main container
        main_container = ttk.Frame(self.root)
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Sidebar
        self.sidebar = ttk.Frame(main_container, width=200)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
        
        # Main content area
        self.content_area = ttk.Frame(main_container)
        self.content_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Log panel
        self.log_panel = ttk.LabelFrame(self.root, text="Session Log", height=150)
        self.log_panel.pack(fill=tk.X, padx=5, pady=5)
        
        # Build components
        self._build_sidebar()
        self._build_content_area()
        self._build_log_panel()

    def _build_sidebar(self):
        # Exercises label
        ttk.Label(self.sidebar, text="Exercises", font=('Helvetica', 12, 'bold')).pack(pady=10)
        
        # Exercise list
        self.exercise_listbox = tk.Listbox(
            self.sidebar,
            selectmode=tk.SINGLE,
            font=('Helvetica', 10),
            height=20
        )
        
        for exercise in EXERCISES:
            self.exercise_listbox.insert(tk.END, exercise['name'])
        
        self.exercise_listbox.pack(fill=tk.BOTH, expand=True)
        self.exercise_listbox.bind('<<ListboxSelect>>', self._on_exercise_select)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(self.sidebar)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.exercise_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.exercise_listbox.yview)

    def _build_content_area(self):
        # Initial placeholder
        self.current_exercise_frame = None
        self._show_welcome_message()

    def _build_log_panel(self):
        self.log_text = tk.Text(
            self.log_panel,
            state=tk.DISABLED,
            wrap=tk.WORD,
            height=6,
            font=('Courier', 10)
        )
        self.log_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        scrollbar = ttk.Scrollbar(self.log_panel)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.log_text.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.log_text.yview)

    def _show_welcome_message(self):
        if self.current_exercise_frame:
            self.current_exercise_frame.destroy()
            
        welcome_frame = ttk.Frame(self.content_area)
        welcome_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(
            welcome_frame,
            text="Welcome to the Financial Psychology Toolkit",
            font=('Helvetica', 14, 'bold')
        ).pack(pady=20)
        
        ttk.Label(
            welcome_frame,
            text="Please select an exercise from the sidebar to begin",
            font=('Helvetica', 12)
        ).pack(pady=10)
        
        self.current_exercise_frame = welcome_frame

    def _on_exercise_select(self, event):
        selection = self.exercise_listbox.curselection()
        if not selection:
            return
            
        exercise_index = selection[0]
        exercise = EXERCISES[exercise_index]
        
        # Clear current content
        if self.current_exercise_frame:
            self.current_exercise_frame.destroy()
        
        # Create new exercise frame
        self.current_exercise_frame = ExerciseFrame(
            self.content_area,
            exercise,
            self.logger,
            self.media_handler
        )
        self.current_exercise_frame.pack(fill=tk.BOTH, expand=True)
        
        self.logger.log(f"Loaded exercise: {exercise['name']}")
        self._update_log_display()

    def _new_session(self):
        # Reset the application state
        self._show_welcome_message()
        self.logger.clear()
        self.media_handler.clear_attachments()
        self.logger.log("New session started")
        self._update_log_display()

    def _export_report(self):
        filepath = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON", "*.json"), ("HTML", "*.html"), ("All Files", "*.*")]
        )
        
        if filepath:
            try:
                self.session_report.export(filepath)
                messagebox.showinfo("Export Successful", f"Report saved to:\n{filepath}")
                self.logger.log(f"Exported report to {filepath}")
            except Exception as e:
                messagebox.showerror("Export Error", f"Failed to export report:\n{str(e)}")
                self.logger.log(f"Export failed: {str(e)}")
            
            self._update_log_display()

    def _toggle_log_panel(self):
        if self.log_panel.winfo_ismapped():
            self.log_panel.pack_forget()
        else:
            self.log_panel.pack(fill=tk.X, padx=5, pady=5)

    def _show_about(self):
        about_text = (
            "Psychology of Financial Planning Toolkit\n"
            "Version 1.0\n\n"
            "A comprehensive application for financial planners\n"
            "to conduct psychological exercises with clients."
        )
        messagebox.showinfo("About", about_text)
        self.logger.log("Viewed About dialog")
        self._update_log_display()

    def _update_log_display(self):
        self.log_text.config(state=tk.NORMAL)
        self.log_text.delete(1.0, tk.END)
        
        for entry in self.logger.get_entries():
            self.log_text.insert(tk.END, entry + "\n")
        
        self.log_text.config(state=tk.DISABLED)
        self.log_text.see(tk.END)

class AppLogger:
    def __init__(self):
        self.entries = []

    def log(self, message):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = f"[{timestamp}] {message}"
        self.entries.append(entry)

    def get_entries(self):
        return self.entries.copy()

    def clear(self):
        self.entries = []

class MediaHandler:
    def __init__(self, logger):
        self.logger = logger
        self.photo_references = []
        self.attachments = []

    def attach_photo(self):
        try:
            initial_dir = str(Path.home() / "Pictures")
            if not os.path.exists(initial_dir):
                initial_dir = str(Path.home())
                
            filepath = filedialog.askopenfilename(
                title="Select Photo",
                initialdir=initial_dir,
                filetypes=[
                    ("Image Files", "*.png;*.jpg;*.jpeg"),
                    ("All Files", "*.*")
                ]
            )
            
            if not filepath:
                return None
                
            self.logger.log(f"Attached photo: {os.path.basename(filepath)}")
            
            # Open and resize image
            img = Image.open(filepath)
            img.thumbnail((400, 400))
            
            # Convert to PhotoImage
            photo = ImageTk.PhotoImage(img)
            self.photo_references.append(photo)  # Keep reference
            
            # Store attachment info
            self.attachments.append({
                "path": filepath,
                "timestamp": datetime.now().isoformat(),
                "type": "photo"
            })
            
            return photo
            
        except Exception as e:
            self.logger.log(f"Error attaching photo: {str(e)}")
            return None

    def clear_attachments(self):
        self.photo_references = []
        self.attachments = []

class ExerciseFrame(ttk.Frame):
    def __init__(self, parent, exercise, logger, media_handler):
        super().__init__(parent)
        self.exercise = exercise
        self.logger = logger
        self.media_handler = media_handler
        
        self._build_ui()

    def _build_ui(self):
        # Header
        header = ttk.Frame(self)
        header.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(
            header,
            text=self.exercise['name'],
            font=('Helvetica', 12, 'bold')
        ).pack(side=tk.LEFT)
        
        # Attach photo button
        ttk.Button(
            header,
            text="Attach Photo",
            command=self._attach_photo
        ).pack(side=tk.RIGHT)
        
        # Description
        ttk.Label(
            self,
            text=self.exercise['description'],
            wraplength=600
        ).pack(fill=tk.X, pady=(0, 15))
        
        # Content area
        self._build_exercise_content()

    def _build_exercise_content(self):
        if self.exercise['id'] == "values_goals":
            self._build_values_goals()
        elif self.exercise['id'] == "money_scripts":
            self._build_money_scripts()
        else:
            self._build_generic_exercise()

    def _build_values_goals(self):
        notebook = ttk.Notebook(self)
        notebook.pack(fill=tk.BOTH, expand=True)
        
        # Values tab
        values_frame = ttk.Frame(notebook)
        ttk.Label(values_frame, text="Rank your top 5 values (1 = most important):").pack(pady=5)
        
        self.values_vars = []
        common_values = [
            "Security", "Family", "Freedom", "Achievement",
            "Growth", "Community", "Health", "Legacy"
        ]
        
        for i, value in enumerate(common_values):
            row = ttk.Frame(values_frame)
            row.pack(fill=tk.X, pady=2)
            
            ttk.Label(row, text=f"{i+1}. {value}", width=15).pack(side=tk.LEFT)
            var = tk.StringVar()
            ttk.Combobox(
                row,
                textvariable=var,
                values=[str(x) for x in range(1, 6)],
                state="readonly",
                width=5
            ).pack(side=tk.LEFT, padx=5)
            self.values_vars.append((value, var))
        
        notebook.add(values_frame, text="Core Values")
        
        # Goals tab
        goals_frame = ttk.Frame(notebook)
        ttk.Label(goals_frame, text="Describe your financial goals:").pack(pady=5)
        
        self.goals_text = tk.Text(goals_frame, height=10, wrap=tk.WORD)
        scrollbar = ttk.Scrollbar(goals_frame, command=self.goals_text.yview)
        self.goals_text.config(yscrollcommand=scrollbar.set)
        
        self.goals_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        notebook.add(goals_frame, text="Financial Goals")
        
        # Save button
        ttk.Button(
            self,
            text="Save Responses",
            command=self._save_values_goals
        ).pack(pady=10)

    def _save_values_goals(self):
        values_ranking = {}
        for value, var in self.values_vars:
            if var.get():
                values_ranking[value] = int(var.get())
        
        goals_text = self.goals_text.get("1.0", tk.END)
        self.logger.log("Saved Values & Goals responses")

    def _build_money_scripts(self):
        questions = [
            "Money is the root of all evil.",
            "More money will make me happier.",
            "I don't deserve to be wealthy.",
            "Rich people are greedy.",
            "You have to work hard to earn money."
        ]
        
        self.script_vars = []
        
        for i, question in enumerate(questions):
            frame = ttk.Frame(self)
            frame.pack(fill=tk.X, pady=5)
            
            ttk.Label(frame, text=f"{i+1}. {question}", wraplength=550).pack(side=tk.LEFT, anchor="w")
            
            var = tk.IntVar()
            ttk.Radiobutton(frame, text="Strongly Agree", variable=var, value=5).pack(side=tk.LEFT, padx=5)
            ttk.Radiobutton(frame, text="Agree", variable=var, value=4).pack(side=tk.LEFT, padx=5)
            ttk.Radiobutton(frame, text="Neutral", variable=var, value=3).pack(side=tk.LEFT, padx=5)
            ttk.Radiobutton(frame, text="Disagree", variable=var, value=2).pack(side=tk.LEFT, padx=5)
            ttk.Radiobutton(frame, text="Strongly Disagree", variable=var, value=1).pack(side=tk.LEFT, padx=5)
            
            self.script_vars.append((question, var))
        
        ttk.Button(
            self,
            text="Analyze Money Scripts",
            command=self._analyze_money_scripts
        ).pack(pady=10)

    def _analyze_money_scripts(self):
        scores = []
        for question, var in self.script_vars:
            scores.append(var.get())
        
        average_score = sum(scores) / len(scores) if scores else 0
        self.logger.log(f"Money Scripts analyzed. Average score: {average_score:.1f}")

    def _build_generic_exercise(self):
        ttk.Label(
            self,
            text="This exercise is not yet fully implemented.",
            font=('Helvetica', 11, 'italic')
        ).pack(pady=20)
        
        ttk.Label(
            self,
            text="Use the 'Attach Photo' button to capture worksheet results.",
            font=('Helvetica', 10)
        ).pack(pady=10)

    def _attach_photo(self):
        photo = self.media_handler.attach_photo()
        if photo:
            # Create a frame for the photo and its label
            photo_frame = ttk.Frame(self)
            photo_frame.pack(pady=10, fill=tk.X)
            
            # Display the photo
            lbl = ttk.Label(photo_frame, image=photo)
            lbl.image = photo  # Keep reference
            lbl.pack(side=tk.LEFT, padx=5)
            
            # Add a remove button
            ttk.Button(
                photo_frame,
                text="Remove",
                command=lambda: self._remove_photo(photo_frame)
            ).pack(side=tk.LEFT, padx=5)

    def _remove_photo(self, frame):
        frame.destroy()
        self.logger.log("Removed attached photo")

class SessionReport:
    def __init__(self, logger):
        self.logger = logger
        self.report_data = {
            "metadata": {
                "created": datetime.now().isoformat(),
                "tool": "Financial Psychology Toolkit",
                "version": "1.0"
            },
            "content": {}
        }

    def export(self, path):
        try:
            self.report_data["content"]["session_log"] = self.logger.get_entries()
            self.report_data["metadata"]["exported"] = datetime.now().isoformat()
            
            path = Path(path)
            
            if path.suffix.lower() == ".html":
                self._export_html(path)
            else:
                self._export_json(path)
                
        except Exception as e:
            raise Exception(f"Export failed: {str(e)}")

    def _export_html(self, path):
        html_template = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Financial Psychology Report</title>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; }}
                h1 {{ color: #2c3e50; }}
                .log-entry {{ margin-bottom: 5px; }}
                .timestamp {{ color: #7f8c8d; font-size: 0.9em; }}
            </style>
        </head>
        <body>
            <h1>Financial Psychology Session Report</h1>
            <p>Generated on {self.report_data['metadata']['exported']}</p>
            
            <h2>Session Log</h2>
            <div id="log-entries">
                {self._generate_log_html()}
            </div>
        </body>
        </html>
        """
        
        with open(path, "w", encoding="utf-8") as f:
            f.write(html_template)

    def _generate_log_html(self):
        html = []
        for entry in self.report_data["content"]["session_log"]:
            if "]" in entry:
                timestamp, message = entry.split("]", 1)
                timestamp = timestamp[1:] + "]"
                html.append(
                    f'<div class="log-entry">'
                    f'<span class="timestamp">{timestamp}</span>'
                    f'<span class="message">{message.strip()}</span>'
                    f'</div>'
                )
            else:
                html.append(f'<div class="log-entry">{entry}</div>')
        return "\n".join(html)

    def _export_json(self, path):
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.report_data, f, indent=2, ensure_ascii=False)

# Exercise data
EXERCISES = [
    {
        "name": "Values & Goals Assessment",
        "id": "values_goals",
        "description": "Identify client's core values and financial goals alignment."
    },
    {
        "name": "Money Scripts Revealer",
        "id": "money_scripts",
        "description": "Uncover unconscious beliefs about money."
    },
    {
        "name": "Financial Flashpoints",
        "id": "flashpoints",
        "description": "Explore pivotal money-related life events."
    },
    {
        "name": "Risk Tolerance Scale",
        "id": "risk_tolerance",
        "description": "Measure comfort with financial uncertainty."
    },
    {
        "name": "Spender/Saver Profile",
        "id": "spender_saver",
        "description": "Assess money management personality type."
    }
]

if __name__ == "__main__":
    root = tk.Tk()
    app = FinancialPsychologyToolkit(root)
    root.mainloop()