import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
from datetime import datetime

class CognitiveDissonanceAnalyzer:
    def __init__(self, root):
        self.root = root
        self.root.title("Cognitive Dissonance Thought Analyzer")
        self.root.geometry("1000x800")
        
        # Database
        self.users = []
        self.thoughts = []
        self.current_user = None
        
        self.load_data()
        
        # Create main containers
        self.create_header()
        self.create_info_box()
        self.create_user_panel()
        self.create_analysis_panel()
        self.create_history_panel()
        
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
        with open("users.json", "w") as f:
            json.dump(self.users, f)
            
        with open("thoughts.json", "w") as f:
            json.dump(self.thoughts, f)
    
    def create_header(self):
        header_frame = ttk.Frame(self.root)
        header_frame.pack(fill=tk.X, padx=10, pady=10)
        
        title_label = ttk.Label(header_frame, text="Cognitive Dissonance Thought Analyzer", 
                              font=("Arial", 16, "bold"))
        title_label.pack()
        
    def create_info_box(self):
        info_frame = ttk.LabelFrame(self.root, text="Understanding Cognitive Dissonance", padding=10)
        info_frame.pack(fill=tk.X, padx=10, pady=5)
        
        formula_label = ttk.Label(info_frame, text="D* = D / (D + C)", font=("Arial", 12, "bold"))
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
        
        def_label = ttk.Label(info_frame, text="Definitions (Festinger, 1957)", font=("Arial", 10, "bold"))
        def_label.pack(anchor=tk.W)
        
        consonant_label = ttk.Label(info_frame, text="Consonant cognitions - Two cognitions are consonant if they're relevant to one another and one logically follows from the other.")
        consonant_label.pack(anchor=tk.W)
        
        consonant_ex = ttk.Label(info_frame, text='Example: "I exercise regularly" and "Regular exercise is healthy."', font=("Arial", 9))
        consonant_ex.pack(anchor=tk.W)
        
        dissonant_label = ttk.Label(info_frame, text="Dissonant cognitions - Two cognitions are dissonant if they're relevant but one entails the opposite of the other.")
        dissonant_label.pack(anchor=tk.W)
        
        dissonant_ex = ttk.Label(info_frame, text='Example: "I smoke" and "Smoking causes cancer."', font=("Arial", 9))
        dissonant_ex.pack(anchor=tk.W)
        
        explanation_label = ttk.Label(info_frame, text="Holding dissonant cognitions produces psychological discomfort (dissonance), which motivates people to restore consonance by changing beliefs, adding new cognitions, or trivializing the conflict.")
        explanation_label.pack(anchor=tk.W)
    
    def create_user_panel(self):
        user_frame = ttk.LabelFrame(self.root, text="User Registration", padding=10)
        user_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Login section
        self.login_frame = ttk.Frame(user_frame)
        self.login_frame.pack(fill=tk.X)
        
        ttk.Label(self.login_frame, text="Username:").grid(row=0, column=0, sticky=tk.W)
        self.username_entry = ttk.Entry(self.login_frame)
        self.username_entry.grid(row=0, column=1, sticky=tk.EW, padx=5, pady=2)
        
        ttk.Label(self.login_frame, text="Password:").grid(row=1, column=0, sticky=tk.W)
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
        analysis_frame = ttk.LabelFrame(self.root, text="New Thought Analysis", padding=10)
        analysis_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(analysis_frame, text="Enter your thought (up to 200 words):").pack(anchor=tk.W)
        self.thought_text = tk.Text(analysis_frame, height=5, wrap=tk.WORD)
        self.thought_text.pack(fill=tk.X, pady=5)
        
        # Consonant elements
        consonant_frame = ttk.Frame(analysis_frame)
        consonant_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(consonant_frame, text="Consonant Elements").pack(anchor=tk.W)
        self.consonant_elements_frame = ttk.Frame(consonant_frame)
        self.consonant_elements_frame.pack(fill=tk.X)
        
        self.add_consonant_field()
        
        ttk.Button(consonant_frame, text="Add Consonant Element", command=self.add_consonant_field).pack(anchor=tk.W)
        
        # Dissonant elements
        dissonant_frame = ttk.Frame(analysis_frame)
        dissonant_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(dissonant_frame, text="Dissonant Elements").pack(anchor=tk.W)
        self.dissonant_elements_frame = ttk.Frame(dissonant_frame)
        self.dissonant_elements_frame.pack(fill=tk.X)
        
        self.add_dissonant_field()
        
        ttk.Button(dissonant_frame, text="Add Dissonant Element", command=self.add_dissonant_field).pack(anchor=tk.W)
        
        # Calculate button
        ttk.Button(analysis_frame, text="Calculate Dissonance", command=self.calculate_dissonance).pack(pady=10)
        
        # Results
        self.result_frame = ttk.Frame(analysis_frame)
        self.result_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(self.result_frame, text="Dissonance Score", font=("Arial", 10, "bold")).pack(anchor=tk.W)
        self.d_score_label = ttk.Label(self.result_frame, text="D* = ")
        self.d_score_label.pack(anchor=tk.W)
        
        self.interpretation_label = ttk.Label(self.result_frame, text="Interpretation: ")
        self.interpretation_label.pack(anchor=tk.W)
        
        self.result_frame.pack_forget()
    
    def create_history_panel(self):
        history_frame = ttk.LabelFrame(self.root, text="Thought History", padding=10)
        history_frame.pack(fill=tk.BOTH, padx=10, pady=5, expand=True)
        
        # Filter controls
        filter_frame = ttk.Frame(history_frame)
        filter_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(filter_frame, text="Filter by user:").pack(side=tk.LEFT)
        self.user_filter = ttk.Combobox(filter_frame, values=["all"] + [user["username"] for user in self.users])
        self.user_filter.set("all")
        self.user_filter.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(filter_frame, text="Load History", command=self.load_history).pack(side=tk.LEFT, padx=5)
        ttk.Button(filter_frame, text="Export Data", command=self.export_data).pack(side=tk.LEFT)
        
        # History table
        columns = ("Date", "User", "Thought", "D* Score")
        self.history_tree = ttk.Treeview(history_frame, columns=columns, show="headings")
        
        for col in columns:
            self.history_tree.heading(col, text=col)
            self.history_tree.column(col, width=100)
        
        self.history_tree.column("Thought", width=300)
        
        scrollbar = ttk.Scrollbar(history_frame, orient=tk.VERTICAL, command=self.history_tree.yview)
        self.history_tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.history_tree.pack(fill=tk.BOTH, expand=True)
    
    def add_consonant_field(self):
        entry = ttk.Entry(self.consonant_elements_frame)
        entry.pack(fill=tk.X, pady=2)
        return entry
    
    def add_dissonant_field(self):
        entry = ttk.Entry(self.dissonant_elements_frame)
        entry.pack(fill=tk.X, pady=2)
        return entry
    
    def register_user(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        if not username or not password:
            messagebox.showerror("Error", "Please enter both username and password")
            return
        
        if any(user["username"] == username for user in self.users):
            messagebox.showerror("Error", "Username already exists")
            return
        
        self.users.append({"username": username, "password": password})
        self.save_data()
        
        messagebox.showinfo("Success", "Registration successful! Please login.")
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
        
        # Update user filter dropdown
        self.user_filter["values"] = ["all"] + [user["username"] for user in self.users]
    
    def login_user(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        user = next((u for u in self.users if u["username"] == username and u["password"] == password), None)
        
        if user:
            self.current_user = username
            self.user_info_label.config(text=f"Logged in as: {username}")
            
            self.login_frame.pack_forget()
            self.user_info_frame.pack(fill=tk.X)
            
            self.username_entry.delete(0, tk.END)
            self.password_entry.delete(0, tk.END)
        else:
            messagebox.showerror("Error", "Invalid username or password")
    
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
        
        # Save to history
        entry = {
            "date": datetime.now().isoformat(),
            "user": self.current_user,
            "thought": thought,
            "consonantElements": consonant_elements,
            "dissonantElements": dissonant_elements,
            "D": D,
            "C": C,
            "Dstar": Dstar
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
        
        # Update history
        self.load_history()
    
    def load_history(self):
        selected_user = self.user_filter.get()
        
        # Clear current items
        for item in self.history_tree.get_children():
            self.history_tree.delete(item)
        
        # Filter thoughts
        filtered_thoughts = self.thoughts
        if selected_user != "all":
            filtered_thoughts = [t for t in self.thoughts if t["user"] == selected_user]
        
        # Sort by date (newest first)
        filtered_thoughts.sort(key=lambda x: x["date"], reverse=True)
        
        # Add to treeview
        for thought in filtered_thoughts:
            date_str = datetime.fromisoformat(thought["date"]).strftime("%Y-%m-%d %H:%M")
            thought_preview = (thought["thought"][:47] + "...") if len(thought["thought"]) > 50 else thought["thought"]
            self.history_tree.insert("", tk.END, values=(
                date_str,
                thought["user"],
                thought_preview,
                f"{thought['Dstar']:.3f}"
            ))
    
    def export_data(self):
        selected_user = self.user_filter.get()
        data_to_export = self.thoughts
        
        if selected_user != "all":
            data_to_export = [t for t in self.thoughts if t["user"] == selected_user]
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json")],
            initialfile=f"dissonance-data-{'all-users' if selected_user == 'all' else selected_user}.json"
        )
        
        if file_path:
            with open(file_path, "w") as f:
                json.dump(data_to_export, f, indent=2)
            messagebox.showinfo("Success", "Data exported successfully")

if __name__ == "__main__":
    root = tk.Tk()
    app = CognitiveDissonanceAnalyzer(root)
    root.mainloop()
