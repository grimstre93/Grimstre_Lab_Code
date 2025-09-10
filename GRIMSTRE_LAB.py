# -*- coding: utf-8 -*-
"""
Created on Sun Aug 17 11:13:34 2025

@author: samng
"""
# -*- coding: utf-8 -*-
"""
Cognitive Behavioral & R&D Tools Manager
Copyright (c) GRIMSTRE DIGITAL TOOLS. All rights reserved.
Font: Times New Roman
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime
import json
import csv
from enum import Enum
import os

# ------------------------------
# Enums and Data Classes
# ------------------------------
class ActivityType(Enum):
    SOCIAL = "Social"
    PROJECT = "Project"
    RND = "R&D"

class ToolCategory(Enum):
    ELECTRICAL = "Electrical"
    MECHANICAL = "Mechanical"
    SOFTWARE = "Software"

class CognitiveActivity:
    def __init__(self, name, description, activity_type, time_spent, investment, project_profile):
        self.name = name
        self.description = description
        self.activity_type = activity_type
        self.time_spent = time_spent
        self.investment = investment
        self.project_profile = project_profile
        self.timestamp = datetime.now().isoformat()

    def to_dict(self):
        return {
            "name": self.name,
            "description": self.description,
            "type": self.activity_type.value,
            "time_spent": self.time_spent,
            "investment": self.investment,
            "project_profile": self.project_profile,
            "timestamp": self.timestamp
        }

class Tool:
    def __init__(self, name, category, quantity, description):
        self.name = name
        self.category = category
        self.quantity = quantity
        self.description = description
    
    def to_dict(self):
        return {
            "name": self.name,
            "category": self.category.value,
            "quantity": self.quantity,
            "description": self.description
        }

# ------------------------------
# Main Application
# ------------------------------
class GrimstreApp:
    def __init__(self, root):
        self.root = root
        self.root.title("GRIMSTRE DIGITAL TOOLS - Cognitive & R&D Manager")
        self.root.geometry("1000x700")
        
        # Configure styles
        self.configure_styles()
        
        # Initialize data stores
        self.activities = []
        self.tools = []
        
        # Create notebook (tabs)
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Create tabs
        self.create_activity_tab()
        self.create_tools_tab()
        self.create_reports_tab()
        
    def configure_styles(self):
        style = ttk.Style()
        style.configure('TNotebook.Tab', font=('Times New Roman', 10, 'bold'))
        style.configure('TLabel', font=('Times New Roman', 10))
        style.configure('TButton', font=('Times New Roman', 10))
        style.configure('TEntry', font=('Times New Roman', 10))
        
    def create_activity_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Cognitive Activities")
        
        # Activity Entry Frame
        entry_frame = ttk.LabelFrame(tab, text="Log New Activity", padding=10)
        entry_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(entry_frame, text="Activity Name:").grid(row=0, column=0, sticky=tk.W)
        self.act_name = ttk.Entry(entry_frame, width=40)
        self.act_name.grid(row=0, column=1, padx=5, pady=2)
        
        ttk.Label(entry_frame, text="Description:").grid(row=1, column=0, sticky=tk.W)
        self.act_desc = ttk.Entry(entry_frame, width=40)
        self.act_desc.grid(row=1, column=1, padx=5, pady=2)
        
        ttk.Label(entry_frame, text="Type:").grid(row=2, column=0, sticky=tk.W)
        self.act_type = ttk.Combobox(entry_frame, values=[t.value for t in ActivityType], state="readonly")
        self.act_type.grid(row=2, column=1, padx=5, pady=2, sticky=tk.W)
        
        ttk.Label(entry_frame, text="Time Spent (hours):").grid(row=3, column=0, sticky=tk.W)
        self.act_time = ttk.Entry(entry_frame, width=10)
        self.act_time.grid(row=3, column=1, padx=5, pady=2, sticky=tk.W)
        
        ttk.Label(entry_frame, text="Investment ($):").grid(row=4, column=0, sticky=tk.W)
        self.act_invest = ttk.Entry(entry_frame, width=10)
        self.act_invest.grid(row=4, column=1, padx=5, pady=2, sticky=tk.W)
        
        ttk.Label(entry_frame, text="Project Profile:").grid(row=5, column=0, sticky=tk.W)
        self.act_profile = ttk.Entry(entry_frame, width=40)
        self.act_profile.grid(row=5, column=1, padx=5, pady=2)
        
        ttk.Button(entry_frame, text="Add Activity", command=self.add_activity).grid(row=6, column=1, pady=10, sticky=tk.E)
        
        # Activity Display Frame
        display_frame = ttk.LabelFrame(tab, text="Activity Log", padding=10)
        display_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        columns = ("Name", "Description", "Type", "Time", "Investment", "Profile", "Timestamp")
        self.activity_tree = ttk.Treeview(display_frame, columns=columns, show="headings", height=10)
        
        for col in columns:
            self.activity_tree.heading(col, text=col)
            self.activity_tree.column(col, width=100, anchor=tk.W)
        
        self.activity_tree.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(display_frame, orient=tk.VERTICAL, command=self.activity_tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.activity_tree.configure(yscrollcommand=scrollbar.set)
        
    def create_tools_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="R&D Tools")
        
        # Tools Entry Frame
        entry_frame = ttk.LabelFrame(tab, text="Log New Tool", padding=10)
        entry_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(entry_frame, text="Tool Name:").grid(row=0, column=0, sticky=tk.W)
        self.tool_name = ttk.Entry(entry_frame, width=40)
        self.tool_name.grid(row=0, column=1, padx=5, pady=2)
        
        ttk.Label(entry_frame, text="Category:").grid(row=1, column=0, sticky=tk.W)
        self.tool_cat = ttk.Combobox(entry_frame, values=[c.value for c in ToolCategory], state="readonly")
        self.tool_cat.grid(row=1, column=1, padx=5, pady=2, sticky=tk.W)
        
        ttk.Label(entry_frame, text="Quantity:").grid(row=2, column=0, sticky=tk.W)
        self.tool_qty = ttk.Entry(entry_frame, width=10)
        self.tool_qty.grid(row=2, column=1, padx=5, pady=2, sticky=tk.W)
        
        ttk.Label(entry_frame, text="Description:").grid(row=3, column=0, sticky=tk.W)
        self.tool_desc = ttk.Entry(entry_frame, width=40)
        self.tool_desc.grid(row=3, column=1, padx=5, pady=2)
        
        ttk.Button(entry_frame, text="Add Tool", command=self.add_tool).grid(row=4, column=1, pady=10, sticky=tk.E)
        
        # Tools Display Frame
        display_frame = ttk.LabelFrame(tab, text="Tools Inventory", padding=10)
        display_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        columns = ("Name", "Category", "Quantity", "Description")
        self.tools_tree = ttk.Treeview(display_frame, columns=columns, show="headings", height=10)
        
        for col in columns:
            self.tools_tree.heading(col, text=col)
            self.tools_tree.column(col, width=120, anchor=tk.W)
        
        self.tools_tree.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(display_frame, orient=tk.VERTICAL, command=self.tools_tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tools_tree.configure(yscrollcommand=scrollbar.set)
        
    def create_reports_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Reports & Export")
        
        # Reports Frame
        reports_frame = ttk.LabelFrame(tab, text="Export Data", padding=20)
        reports_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        ttk.Button(reports_frame, text="Export Activities to CSV", 
                  command=self.export_activities).pack(pady=10, fill=tk.X)
        
        ttk.Button(reports_frame, text="Export Tools to JSON", 
                  command=self.export_tools).pack(pady=10, fill=tk.X)
        
        ttk.Button(reports_frame, text="Generate Combined Report", 
                  command=self.generate_report).pack(pady=10, fill=tk.X)
        
        # Status Bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        ttk.Label(tab, textvariable=self.status_var, relief=tk.SUNKEN, 
                 anchor=tk.W, font=('Times New Roman', 9)).pack(fill=tk.X, side=tk.BOTTOM)
    
    # ------------------------------
    # Core Functions
    # ------------------------------
    def add_activity(self):
        try:
            activity = CognitiveActivity(
                name=self.act_name.get(),
                description=self.act_desc.get(),
                activity_type=ActivityType(self.act_type.get()),
                time_spent=float(self.act_time.get()),
                investment=float(self.act_invest.get()),
                project_profile=self.act_profile.get()
            )
            
            self.activities.append(activity)
            self.update_activity_tree()
            self.clear_activity_fields()
            self.status_var.set("Activity added successfully")
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid input: {str(e)}")
    
    def add_tool(self):
        try:
            tool = Tool(
                name=self.tool_name.get(),
                category=ToolCategory(self.tool_cat.get()),
                quantity=int(self.tool_qty.get()),
                description=self.tool_desc.get()
            )
            
            self.tools.append(tool)
            self.update_tools_tree()
            self.clear_tool_fields()
            self.status_var.set("Tool added successfully")
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid input: {str(e)}")
    
    def update_activity_tree(self):
        self.activity_tree.delete(*self.activity_tree.get_children())
        for activity in self.activities:
            self.activity_tree.insert("", tk.END, values=(
                activity.name,
                activity.description,
                activity.activity_type.value,
                activity.time_spent,
                activity.investment,
                activity.project_profile,
                activity.timestamp
            ))
    
    def update_tools_tree(self):
        self.tools_tree.delete(*self.tools_tree.get_children())
        for tool in self.tools:
            self.tools_tree.insert("", tk.END, values=(
                tool.name,
                tool.category.value,
                tool.quantity,
                tool.description
            ))
    
    def clear_activity_fields(self):
        self.act_name.delete(0, tk.END)
        self.act_desc.delete(0, tk.END)
        self.act_type.set('')
        self.act_time.delete(0, tk.END)
        self.act_invest.delete(0, tk.END)
        self.act_profile.delete(0, tk.END)
    
    def clear_tool_fields(self):
        self.tool_name.delete(0, tk.END)
        self.tool_cat.set('')
        self.tool_qty.delete(0, tk.END)
        self.tool_desc.delete(0, tk.END)
    
    def export_activities(self):
        if not self.activities:
            messagebox.showwarning("Warning", "No activities to export")
            return
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV Files", "*.csv")],
            title="Save Activities CSV"
        )
        
        if file_path:
            try:
                with open(file_path, 'w', newline='') as f:
                    writer = csv.DictWriter(f, fieldnames=[
                        'name', 'description', 'type', 'time_spent', 
                        'investment', 'project_profile', 'timestamp'
                    ])
                    writer.writeheader()
                    for activity in self.activities:
                        writer.writerow(activity.to_dict())
                self.status_var.set(f"Activities exported to {os.path.basename(file_path)}")
            except Exception as e:
                messagebox.showerror("Error", f"Export failed: {str(e)}")
    
    def export_tools(self):
        if not self.tools:
            messagebox.showwarning("Warning", "No tools to export")
            return
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON Files", "*.json")],
            title="Save Tools JSON"
        )
        
        if file_path:
            try:
                with open(file_path, 'w') as f:
                    json.dump([tool.to_dict() for tool in self.tools], f, indent=4)
                self.status_var.set(f"Tools exported to {os.path.basename(file_path)}")
            except Exception as e:
                messagebox.showerror("Error", f"Export failed: {str(e)}")
    
    def generate_report(self):
        if not self.activities and not self.tools:
            messagebox.showwarning("Warning", "No data to generate report")
            return
        
        report = "GRIMSTRE DIGITAL TOOLS - Cognitive & R&D Report\n\n"
        report += f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        
        report += "=== Cognitive Activities ===\n"
        if self.activities:
            for activity in self.activities:
                report += (
                    f"Name: {activity.name}\n"
                    f"Type: {activity.activity_type.value}\n"
                    f"Time: {activity.time_spent} hours | Investment: ${activity.investment}\n"
                    f"Profile: {activity.project_profile}\n"
                    f"Description: {activity.description}\n"
                    f"Timestamp: {activity.timestamp}\n\n"
                )
        else:
            report += "No activities recorded\n\n"
        
        report += "=== R&D Tools Inventory ===\n"
        if self.tools:
            for tool in self.tools:
                report += (
                    f"Name: {tool.name}\n"
                    f"Category: {tool.category.value}\n"
                    f"Quantity: {tool.quantity}\n"
                    f"Description: {tool.description}\n\n"
                )
        else:
            report += "No tools recorded\n\n"
        
        # Show report in a new window
        report_window = tk.Toplevel(self.root)
        report_window.title("GRIMSTRE Report")
        report_window.geometry("600x700")
        
        text_frame = ttk.Frame(report_window)
        text_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        text_widget = tk.Text(text_frame, wrap=tk.WORD, font=('Times New Roman', 10))
        text_widget.insert(tk.END, report)
        text_widget.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
        
        scrollbar = ttk.Scrollbar(text_frame, orient=tk.VERTICAL, command=text_widget.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        text_widget.configure(yscrollcommand=scrollbar.set)
        
        ttk.Button(report_window, text="Save Report", 
                  command=lambda: self.save_text_report(report)).pack(pady=10)
    
    def save_text_report(self, report):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt")],
            title="Save Report"
        )
        
        if file_path:
            try:
                with open(file_path, 'w') as f:
                    f.write(report)
                self.status_var.set(f"Report saved to {os.path.basename(file_path)}")
            except Exception as e:
                messagebox.showerror("Error", f"Save failed: {str(e)}")

# ------------------------------
# Run Application
# ------------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = GrimstreApp(root)
    
    # Copyright notice
    copyright_label = ttk.Label(
        root, 
        text="© 2023 GRIMSTRE DIGITAL TOOLS. All rights reserved.", 
        font=('Times New Roman', 8),
        foreground="gray"
    )
    copyright_label.pack(side=tk.BOTTOM, fill=tk.X)
    
    root.mainloop()