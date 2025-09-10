import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
from datetime import datetime

class CognitiveDissonanceAnalyzer:
    def __init__(self, root):
        self.root = root
        self.root.title("Cognitive Dissonance Thought Analyzer")
        self.root.geometry("1100x800")
        self.root.minsize(900, 600)
        
        # Database initialization
        self.users = []
        self.thoughts = []
        self.current_user = None
        
        self.load_data()
        
        # Main container with scrollbar
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        self.canvas = tk.Canvas(self.main_frame)
        self.scrollbar = ttk.Scrollbar(self.main_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        
        # Bind mousewheel for scrolling
        self.canvas.bind_all("<MouseWheel>", self.on_mousewheel)
        
        # Create UI components
        self.create_header()
        self.create_info_box()
        self.create_user_panel()
        self.create_analysis_panel()
        self.create_history_panel()
        
    def on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    
    def load_data(self):
        try:
            with open("users.json", "r") as f:
                self.users = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.users = []
            
        try:
            with open("thoughts.json", "r") as f:
                self.thoughts = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.thoughts = []
    
    def save_data(self):
        try:
            with open("users.json", "w") as f:
                json.dump(self.users, f)
            
            with open("thoughts.json", "w") as f:
                json.dump(self.thoughts, f)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save data: {str(e)}")
    
    def create_header(self):
        header_frame = ttk.Frame(self.scrollable_frame)
        header_frame.pack(fill=tk.X, padx=10, pady=10)
        
        title_label = ttk.Label(header_frame, text="Cognitive Dissonance Thought Analyzer", 
                              font=("Arial", 16, "bold"))
        title_label.pack()
    
    def create_info_box(self):
        info_frame = ttk.LabelFrame(self.scrollable_frame, text="Understanding Cognitive Dissonance", padding=10)
        info_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Formula explanation
        formula_frame = ttk.Frame(info_frame)
        formula_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(formula_frame, text="D* = D / (D + C)", font=("Arial", 12, "bold")).pack(anchor=tk.W)
        
        # Definitions
        def_frame = ttk.Frame(info_frame)
        def_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(def_frame, text="Where:").pack(anchor=tk.W)
        ttk.Label(def_frame, text="- D* = Total magnitude of dissonance (0-1 scale)").pack(anchor=tk.W)
        ttk.Label(def_frame, text="- D = Count of dissonant elements").pack(anchor=tk.W)
        ttk.Label(def_frame, text="- C = Count of consonant elements").pack(anchor=tk.W)
        
        # Examples
        examples_frame = ttk.Frame(info_frame)
        examples_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(examples_frame, text="Examples:", font=("Arial", 10, "bold")).pack(anchor=tk.W)
        ttk.Label(examples_frame, text='Consonant: "I exercise" and "Exercise is healthy"').pack(anchor=tk.W)
        ttk.Label(examples_frame, text='Dissonant: "I smoke" and "Smoking causes cancer"').pack(anchor=tk.W)
    
    def create_user_panel(self):
        user_frame = ttk.LabelFrame(self.scrollable_frame, text="User Management", padding=10)
        user_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Login section
        self.login_frame = ttk.Frame(user_frame)
        self.login_frame.pack(fill=tk.X)
        
        ttk.Label(self.login_frame, text="Username:").grid(row=0, column=0, sticky=tk.W, padx=5)
        self.username_entry = ttk.Entry(self.login_frame)
        self.username_entry.grid(row=0, column=1, sticky=tk.EW, padx=5, pady=2)
        
        ttk.Label(self.login_frame, text="Password:").grid(row=1, column=0, sticky=tk.W, padx=5)
        self.password_entry = ttk.Entry(self.login_frame, show="*")
        self.password_entry.grid(row=1, column=1, sticky=tk.EW, padx=5, pady=2)
        
        button_frame = ttk.Frame(self.login_frame)
        button_frame.grid(row=2, column=0, columnspan=2, pady=5)
        
        ttk.Button(button_frame, text="Register", command=self.register_user).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Login", command=self.login_user).pack(side=tk.LEFT, padx=5)
        
        # User info section
        self.user_info_frame = ttk.Frame(user_frame)
        self.user_info_label = ttk.Label(self.user_info_frame, text="")
        self.user_info_label.pack(side=tk.LEFT)
        
        ttk.Button(self.user_info_frame, text="Logout", command=self.logout_user).pack(side=tk.LEFT, padx=10)
        self.user_info_frame.pack_forget()
    
    def create_analysis_panel(self):
        analysis_frame = ttk.LabelFrame(self.scrollable_frame, text="Thought Analysis", padding=10)
        analysis_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Thought entry
        thought_frame = ttk.Frame(analysis_frame)
        thought_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(thought_frame, text="Enter your thought (up to 10,000 words):").pack(anchor=tk.W)
        
        text_frame = ttk.Frame(thought_frame)
        text_frame.pack(fill=tk.X)
        
        self.thought_text = tk.Text(text_frame, height=8, wrap=tk.WORD)
        text_scroll = ttk.Scrollbar(text_frame, command=self.thought_text.yview)
        self.thought_text.configure(yscrollcommand=text_scroll.set)
        
        self.thought_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        text_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Word counter
        self.word_count_label = ttk.Label(thought_frame, text="Word count: 0/10000")
        self.word_count_label.pack(anchor=tk.E)
        self.thought_text.bind("<KeyRelease>", self.update_word_count)
        
        # Elements frame
        elements_frame = ttk.Frame(analysis_frame)
        elements_frame.pack(fill=tk.X, pady=5)
        
        # Consonant elements
        consonant_frame = ttk.LabelFrame(elements_frame, text="Consonant Elements", padding=5)
        consonant_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        self.consonant_entries = []
        self.add_consonant_field()
        ttk.Button(consonant_frame, text="+ Add", command=self.add_consonant_field).pack(fill=tk.X, pady=2)
        
        # Dissonant elements
        dissonant_frame = ttk.LabelFrame(elements_frame, text="Dissonant Elements", padding=5)
        dissonant_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        self.dissonant_entries = []
        self.add_dissonant_field()
        ttk.Button(dissonant_frame, text="+ Add", command=self.add_dissonant_field).pack(fill=tk.X, pady=2)
        
        # Calculate button
        ttk.Button(analysis_frame, text="Analyze Dissonance", command=self.calculate_dissonance).pack(pady=10)
        
        # Results
        self.result_frame = ttk.LabelFrame(analysis_frame, text="Results", padding=10)
        self.result_frame.pack(fill=tk.X, pady=5)
        
        results_grid = ttk.Frame(self.result_frame)
        results_grid.pack(fill=tk.X)
        
        # Scores
        score_frame = ttk.Frame(results_grid)
        score_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        ttk.Label(score_frame, text="Dissonance Score:", font=("Arial", 10, "bold")).pack(anchor=tk.W)
        self.d_score_label = ttk.Label(score_frame, text="D* = ")
        self.d_score_label.pack(anchor=tk.W)
        
        ttk.Label(score_frame, text="Element Counts:", font=("Arial", 10, "bold")).pack(anchor=tk.W, pady=(5,0))
        self.d_label = ttk.Label(score_frame, text="D (Dissonant): 0")
        self.d_label.pack(anchor=tk.W)
        self.c_label = ttk.Label(score_frame, text="C (Consonant): 0")
        self.c_label.pack(anchor=tk.W)
        
        # Interpretation
        interpret_frame = ttk.Frame(results_grid)
        interpret_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        ttk.Label(interpret_frame, text="Interpretation:", font=("Arial", 10, "bold")).pack(anchor=tk.W)
        self.interpretation_label = ttk.Label(interpret_frame, text="", wraplength=400, justify=tk.LEFT)
        self.interpretation_label.pack(anchor=tk.W)
        
        self.result_frame.pack_forget()
    
    def create_history_panel(self):
        history_frame = ttk.LabelFrame(self.scrollable_frame, text="Analysis History", padding=10)
        history_frame.pack(fill=tk.BOTH, padx=10, pady=5, expand=True)
        
        # Filter controls
        filter_frame = ttk.Frame(history_frame)
        filter_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(filter_frame, text="Filter:").pack(side=tk.LEFT)
        self.user_filter = ttk.Combobox(filter_frame, values=["All users"] + [user["username"] for user in self.users])
        self.user_filter.set("All users")
        self.user_filter.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(filter_frame, text="Refresh", command=self.load_history).pack(side=tk.LEFT, padx=5)
        ttk.Button(filter_frame, text="Export", command=self.export_data).pack(side=tk.LEFT)
        
        # History table
        columns = ("Date", "User", "Thought", "Score", "D", "C")
        self.history_tree = ttk.Treeview(history_frame, columns=columns, show="headings", selectmode="extended")
        
        for col in columns:
            self.history_tree.heading(col, text=col)
            self.history_tree.column(col, width=100, stretch=False)
        
        self.history_tree.column("Date", width=120)
        self.history_tree.column("Thought", width=250, stretch=True)
        self.history_tree.column("Score", width=80)
        
        scrollbar = ttk.Scrollbar(history_frame, orient=tk.VERTICAL, command=self.history_tree.yview)
        self.history_tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.history_tree.pack(fill=tk.BOTH, expand=True)
    
    def update_word_count(self, event=None):
        text = self.thought_text.get("1.0", tk.END)
        words = [word for word in text.split() if word.strip()]
        count = len(words)
        self.word_count_label.config(text=f"Words: {count}/10000")
        
        if count > 8000:
            self.word_count_label.config(foreground="red")
        elif count > 5000:
            self.word_count_label.config(foreground="orange")
        else:
            self.word_count_label.config(foreground="black")
    
    def add_consonant_field(self):
        entry_frame = ttk.Frame(self.consonant_entries_frame if hasattr(self, 'consonant_entries_frame') else self.scrollable_frame)
        entry_frame.pack(fill=tk.X, pady=2)
        
        entry = ttk.Entry(entry_frame)
        entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0,5))
        
        remove_btn = ttk.Button(entry_frame, text="×", width=2, command=lambda: entry_frame.destroy())
        remove_btn.pack(side=tk.RIGHT)
        
        if not hasattr(self, 'consonant_entries_frame'):
            self.consonant_entries_frame = ttk.Frame(self.scrollable_frame)
            self.consonant_entries_frame.pack(fill=tk.X)
        
        entry_frame.pack(in_=self.consonant_entries_frame, fill=tk.X, pady=2)
        self.consonant_entries.append(entry)
        return entry
    
    def add_dissonant_field(self):
        entry_frame = ttk.Frame(self.dissonant_entries_frame if hasattr(self, 'dissonant_entries_frame') else self.scrollable_frame)
        entry_frame.pack(fill=tk.X, pady=2)
        
        entry = ttk.Entry(entry_frame)
        entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0,5))
        
        remove_btn = ttk.Button(entry_frame, text="×", width=2, command=lambda: entry_frame.destroy())
        remove_btn.pack(side=tk.RIGHT)
        
        if not hasattr(self, 'dissonant_entries_frame'):
            self.dissonant_entries_frame = ttk.Frame(self.scrollable_frame)
            self.dissonant_entries_frame.pack(fill=tk.X)
        
        entry_frame.pack(in_=self.dissonant_entries_frame, fill=tk.X, pady=2)
        self.dissonant_entries.append(entry)
        return entry
    
    def register_user(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        
        if not username or not password:
            messagebox.showerror("Error", "Username and password are required")
            return
        
        if any(user["username"].lower() == username.lower() for user in self.users):
            messagebox.showerror("Error", "Username already exists")
            return
        
        self.users.append({"username": username, "password": password})
        self.save_data()
        
        messagebox.showinfo("Success", "Registration successful")
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
        self.user_filter["values"] = ["All users"] + [user["username"] for user in self.users]
    
    def login_user(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        
        user = next((u for u in self.users if u["username"].lower() == username.lower() and u["password"] == password), None)
        
        if user:
            self.current_user = username
            self.user_info_label.config(text=f"User: {username}")
            self.login_frame.pack_forget()
            self.user_info_frame.pack(fill=tk.X)
            self.username_entry.delete(0, tk.END)
            self.password_entry.delete(0, tk.END)
        else:
            messagebox.showerror("Error", "Invalid credentials")
    
    def logout_user(self):
        self.current_user = None
        self.user_info_frame.pack_forget()
        self.login_frame.pack(fill=tk.X)
        self.result_frame.pack_forget()
    
    def calculate_dissonance(self):
        if not self.current_user:
            messagebox.showerror("Error", "Please login first")
            return
        
        thought = self.thought_text.get("1.0", tk.END).strip()
        if not thought:
            messagebox.showerror("Error", "Please enter a thought to analyze")
            return
        
        word_count = len([word for word in thought.split() if word.strip()])
        if word_count > 10000:
            messagebox.showerror("Error", "Thought exceeds 10,000 words")
            return
        
        # Get elements
        consonant_elements = []
        for entry in self.consonant_entries:
            if entry.winfo_exists():
                val = entry.get().strip()
                if val:
                    consonant_elements.append(val)
        
        dissonant_elements = []
        for entry in self.dissonant_entries:
            if entry.winfo_exists():
                val = entry.get().strip()
                if val:
                    dissonant_elements.append(val)
        
        if not consonant_elements and not dissonant_elements:
            messagebox.showerror("Error", "Please add at least one element")
            return
        
        # Calculate dissonance
        D = len(dissonant_elements)
        C = len(consonant_elements)
        total = D + C
        Dstar = D / total if total > 0 else 0.0
        
        # Save analysis
        analysis = {
            "date": datetime.now().isoformat(),
            "user": self.current_user,
            "thought": thought,
            "consonant": consonant_elements,
            "dissonant": dissonant_elements,
            "D": D,
            "C": C,
            "Dstar": Dstar,
            "words": word_count
        }
        
        self.thoughts.append(analysis)
        self.save_data()
        
        # Display results
        self.d_score_label.config(text=f"D* = {Dstar:.3f}")
        self.d_label.config(text=f"D (Dissonant): {D}")
        self.c_label.config(text=f"C (Consonant): {C}")
        
        # Interpretation
        if Dstar == 0:
            interpretation = "Complete consonance - no dissonance detected"
        elif Dstar < 0.3:
            interpretation = "Low dissonance - mostly consonant thoughts"
        elif Dstar < 0.6:
            interpretation = "Moderate dissonance - mixed thoughts"
        elif Dstar < 0.9:
            interpretation = "High dissonance - mostly conflicting thoughts"
        else:
            interpretation = "Very high dissonance - strong conflict"
        
        self.interpretation_label.config(text=interpretation)
        self.result_frame.pack(fill=tk.X, pady=5)
        self.load_history()
    
    def load_history(self):
        selected_user = self.user_filter.get()
        
        for item in self.history_tree.get_children():
            self.history_tree.delete(item)
        
        analyses = self.thoughts
        if selected_user != "All users":
            analyses = [a for a in self.thoughts if a["user"] == selected_user]
        
        analyses.sort(key=lambda x: x["date"], reverse=True)
        
        for analysis in analyses:
            date = datetime.fromisoformat(analysis["date"]).strftime("%Y-%m-%d %H:%M")
            preview = (analysis["thought"][:50] + "...") if len(analysis["thought"]) > 50 else analysis["thought"]
            self.history_tree.insert("", tk.END, values=(
                date,
                analysis["user"],
                preview,
                f"{analysis['Dstar']:.3f}",
                analysis["D"],
                analysis["C"]
            ))
    
    def export_data(self):
        selected_user = self.user_filter.get()
        data = self.thoughts if selected_user == "All users" else [a for a in self.thoughts if a["user"] == selected_user]
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON", "*.json"), ("CSV", "*.csv")],
            title="Export Analysis Data"
        )
        
        if not file_path:
            return
        
        try:
            if file_path.endswith(".csv"):
                import csv
                with open(file_path, "w", newline="") as f:
                    writer = csv.writer(f)
                    writer.writerow(["Date", "User", "Thought", "D*", "D", "C", "Words"])
                    for item in data:
                        writer.writerow([
                            item["date"],
                            item["user"],
                            item["thought"],
                            item["Dstar"],
                            item["D"],
                            item["C"],
                            item["words"]
                        ])
            else:
                with open(file_path, "w") as f:
                    json.dump(data, f, indent=2)
            
            messagebox.showinfo("Success", "Data exported successfully")
        except Exception as e:
            messagebox.showerror("Error", f"Export failed: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = CognitiveDissonanceAnalyzer(root)
    root.mainloop()