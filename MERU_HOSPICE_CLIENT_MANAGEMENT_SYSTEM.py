# -*- coding: utf-8 -*-
"""
Created on Mon Aug 25 10:48:58 2025

@author: samng
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import os
from datetime import date, datetime
import hashlib
import socket
import threading
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
import numpy as np

# Set default font to Times New Roman
def set_times_new_roman(font_size=10, weight="normal"):
    return ("Times New Roman", font_size, weight)

class LoginWindow:
    def __init__(self, root, main_app_callback):
        self.root = root
        self.root.title("MERU HOSPICE - Login")
        self.root.geometry("400x300")
        self.root.resizable(False, False)
        
        # Set Times New Roman font for all widgets
        self.style = ttk.Style()
        self.style.configure('TLabel', font=set_times_new_roman(10))
        self.style.configure('TButton', font=set_times_new_roman(10))
        self.style.configure('TEntry', font=set_times_new_roman(10))
        
        self.main_app_callback = main_app_callback
        
        # Center the window
        self.root.eval('tk::PlaceWindow . center')
        
        # Create login frame
        login_frame = ttk.Frame(self.root, padding="20")
        login_frame.pack(fill='both', expand=True)
        
        # Title
        ttk.Label(login_frame, text="MERU HOSPICE SYSTEM", font=set_times_new_roman(16, "bold")).grid(row=0, column=0, columnspan=2, pady=20)
        ttk.Label(login_frame, text="Please login to continue", font=set_times_new_roman(10)).grid(row=1, column=0, columnspan=2, pady=(0, 20))
        
        # Username
        ttk.Label(login_frame, text="Username:").grid(row=2, column=0, sticky='e', pady=5)
        self.username = ttk.Entry(login_frame, width=25)
        self.username.grid(row=2, column=1, sticky='w', pady=5, padx=(10, 0))
        
        # Password
        ttk.Label(login_frame, text="Password:").grid(row=3, column=0, sticky='e', pady=5)
        self.password = ttk.Entry(login_frame, width=25, show="*")
        self.password.grid(row=3, column=1, sticky='w', pady=5, padx=(10, 0))
        
        # Login button
        self.login_btn = ttk.Button(login_frame, text="Login", command=self.authenticate)
        self.login_btn.grid(row=4, column=0, columnspan=2, pady=20)
        
        # Bind Enter key to login
        self.root.bind('<Return>', lambda event: self.authenticate())
        
        # Load users
        self.users = self.load_users()
        
        # Pre-fill with working credentials
        self.username.insert(0, 'admin')
        self.password.insert(0, 'admin123')
        
    def load_users(self):
        try:
            if os.path.exists('users.json'):
                with open('users.json', 'r') as f:
                    return json.load(f)
            else:
                # Create default admin user if file doesn't exist
                default_users = [{
                    'username': 'admin',
                    'password': self.hash_password('admin123'),
                    'role': 'admin',
                    'full_name': 'System Administrator'
                }]
                # Save the default user
                with open('users.json', 'w') as f:
                    json.dump(default_users, f, indent=4)
                return default_users
        except Exception as e:
            print(f"Error loading users: {e}")
            # Default admin user if file doesn't exist or error reading
            return [{
                'username': 'admin',
                'password': self.hash_password('admin123'),
                'role': 'admin',
                'full_name': 'System Administrator'
            }]
    
    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()
    
    def authenticate(self):
        username = self.username.get().strip()
        password = self.password.get().strip()
        
        if not username or not password:
            messagebox.showerror("Error", "Please enter both username and password")
            return
            
        hashed_password = self.hash_password(password)
        
        # Check credentials
        user = None
        for u in self.users:
            if u['username'] == username and u['password'] == hashed_password:
                user = u
                break
                
        if user:
            self.root.destroy()
            self.main_app_callback(user)
        else:
            messagebox.showerror("Error", "Invalid username or password")

class MeruHospiceManager:
    def __init__(self, user):
        self.user = user
        self.root = tk.Tk()
        self.root.title(f"MERU HOSPICE CLIENT AND MEDICATION MANAGEMENT SYSTEM - Welcome {user['full_name']}")
        self.root.geometry("1200x800")
        
        # Set Times New Roman font for all widgets
        self.style = ttk.Style()
        self.style.configure('TLabel', font=set_times_new_roman(10))
        self.style.configure('TButton', font=set_times_new_roman(10))
        self.style.configure('TEntry', font=set_times_new_roman(10))
        self.style.configure('Treeview', font=set_times_new_roman(10))
        self.style.configure('Treeview.Heading', font=set_times_new_roman(10, "bold"))
        
        # Initialize data structures
        self.clients = []
        self.supplies = []
        self.medications = []
        
        # Create menu bar
        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)
        
        # File menu
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0, font=set_times_new_roman(10))
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="Export All Data", command=self.export_all_data)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.root.quit)
        
        # Reports menu
        self.reports_menu = tk.Menu(self.menu_bar, tearoff=0, font=set_times_new_roman(10))
        self.menu_bar.add_cascade(label="Reports", menu=self.reports_menu)
        self.reports_menu.add_command(label="Client Report", command=lambda: self.generate_report('client'))
        self.reports_menu.add_command(label="Medication Report", command=lambda: self.generate_report('medication'))
        self.reports_menu.add_command(label="Supplies Report", command=lambda: self.generate_report('supplies'))
        self.reports_menu.add_command(label="Stock Alert Report", command=self.generate_stock_alert_report)
        
        # Network menu
        self.network_menu = tk.Menu(self.menu_bar, tearoff=0, font=set_times_new_roman(10))
        self.menu_bar.add_cascade(label="Network", menu=self.network_menu)
        self.network_menu.add_command(label="Configure Network Reporting", command=self.configure_network)
        self.network_menu.add_command(label="Send Report to Network", command=self.send_network_report)
        
        # Admin menu (only for admin users)
        if self.user['role'] == 'admin':
            self.admin_menu = tk.Menu(self.menu_bar, tearoff=0, font=set_times_new_roman(10))
            self.menu_bar.add_cascade(label="Admin", menu=self.admin_menu)
            self.admin_menu.add_command(label="User Management", command=self.manage_users)
        
        # Create notebook (tabbed interface)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Create frames for each section
        self.client_frame = ttk.Frame(self.notebook)
        self.supplies_frame = ttk.Frame(self.notebook)
        self.dashboard_frame = ttk.Frame(self.notebook)
        self.about_frame = ttk.Frame(self.notebook)
        
        self.notebook.add(self.client_frame, text="Client Management")
        self.notebook.add(self.supplies_frame, text="Medication & Supplies")
        self.notebook.add(self.dashboard_frame, text="Dashboard")
        self.notebook.add(self.about_frame, text="About")
        
        # Build sections
        self.build_client_section()
        self.build_supplies_section()
        self.build_dashboard_section()
        self.build_about_section()
        
        # Load existing data
        self.load_data()
        
        # Network configuration
        self.network_config = self.load_network_config()
        
    def load_network_config(self):
        try:
            if os.path.exists('network_config.json'):
                with open('network_config.json', 'r') as f:
                    return json.load(f)
        except:
            return {
                'enabled': False,
                'ip_address': '127.0.0.1',
                'port': 5000,
                'auto_send': False
            }
    
    def save_network_config(self):
        try:
            with open('network_config.json', 'w') as f:
                json.dump(self.network_config, f, indent=4)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save network config: {str(e)}")
    
    def configure_network(self):
        config_window = tk.Toplevel(self.root)
        config_window.title("Network Configuration")
        config_window.geometry("400x300")
        config_window.resizable(False, False)
        
        # Set font for config window
        for widget in config_window.winfo_children():
            if isinstance(widget, (ttk.Label, ttk.Button, ttk.Entry)):
                widget.configure(font=set_times_new_roman(10))
        
        ttk.Label(config_window, text="Network Reporting Configuration", font=set_times_new_roman(12, "bold")).pack(pady=10)
        
        frame = ttk.Frame(config_window, padding=10)
        frame.pack(fill='both', expand=True)
        
        # Enable network reporting
        self.network_enabled = tk.BooleanVar(value=self.network_config['enabled'])
        ttk.Checkbutton(frame, text="Enable Network Reporting", variable=self.network_enabled).grid(row=0, column=0, columnspan=2, sticky='w', pady=5)
        
        # IP Address
        ttk.Label(frame, text="IP Address:").grid(row=1, column=0, sticky='e', pady=5)
        ip_entry = ttk.Entry(frame)
        ip_entry.insert(0, self.network_config['ip_address'])
        ip_entry.grid(row=1, column=1, sticky='w', pady=5, padx=(10, 0))
        
        # Port
        ttk.Label(frame, text="Port:").grid(row=2, column=0, sticky='e', pady=5)
        port_entry = ttk.Entry(frame)
        port_entry.insert(0, str(self.network_config['port']))
        port_entry.grid(row=2, column=1, sticky='w', pady=5, padx=(10, 0))
        
        # Auto send
        self.auto_send = tk.BooleanVar(value=self.network_config['auto_send'])
        ttk.Checkbutton(frame, text="Auto Send Reports", variable=self.auto_send).grid(row=3, column=0, columnspan=2, sticky='w', pady=5)
        
        # Buttons
        btn_frame = ttk.Frame(frame)
        btn_frame.grid(row=4, column=0, columnspan=2, pady=20)
        
        def save_config():
            self.network_config['enabled'] = self.network_enabled.get()
            self.network_config['ip_address'] = ip_entry.get()
            self.network_config['port'] = int(port_entry.get())
            self.network_config['auto_send'] = self.auto_send.get()
            self.save_network_config()
            config_window.destroy()
            messagebox.showinfo("Success", "Network configuration saved successfully")
        
        ttk.Button(btn_frame, text="Save", command=save_config).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Cancel", command=config_window.destroy).pack(side='left', padx=5)
    
    def send_network_report(self):
        if not self.network_config['enabled']:
            messagebox.showwarning("Warning", "Network reporting is not enabled. Please configure it first.")
            return
            
        try:
            # Create a simple report
            report = {
                'type': 'full_report',
                'timestamp': datetime.now().isoformat(),
                'clients_count': len(self.clients),
                'medications_count': len(self.medications),
                'supplies_count': len(self.supplies),
                'low_stock_items': self.get_low_stock_items()
            }
            
            # Convert to JSON
            report_json = json.dumps(report)
            
            # Send over network
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((self.network_config['ip_address'], self.network_config['port']))
                s.sendall(report_json.encode())
                
            messagebox.showinfo("Success", "Report sent successfully over network")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to send network report: {str(e)}")
    
    def manage_users(self):
        user_window = tk.Toplevel(self.root)
        user_window.title("User Management")
        user_window.geometry("600x400")
        
        # Set font for user window
        for widget in user_window.winfo_children():
            if isinstance(widget, (ttk.Label, ttk.Button, ttk.Entry)):
                widget.configure(font=set_times_new_roman(10))
        
        # Create frames
        list_frame = ttk.Frame(user_window)
        list_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Treeview for users
        columns = ('username', 'full_name', 'role')
        user_tree = ttk.Treeview(list_frame, columns=columns, show='headings')
        
        user_tree.heading('username', text='Username')
        user_tree.heading('full_name', text='Full Name')
        user_tree.heading('role', text='Role')
        
        user_tree.column('username', width=100)
        user_tree.column('full_name', width=200)
        user_tree.column('role', width=100)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient='vertical', command=user_tree.yview)
        user_tree.configure(yscrollcommand=scrollbar.set)
        
        user_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Load users
        users = self.load_users()
        for user in users:
            user_tree.insert('', 'end', values=(user['username'], user['full_name'], user['role']))
        
        # Button frame
        btn_frame = ttk.Frame(user_window)
        btn_frame.pack(fill='x', padx=10, pady=10)
        
        ttk.Button(btn_frame, text="Add User", command=lambda: self.add_user(user_tree)).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Edit User", command=lambda: self.edit_user(user_tree)).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Delete User", command=lambda: self.delete_user(user_tree)).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Close", command=user_window.destroy).pack(side='right', padx=5)
    
    def load_users(self):
        try:
            if os.path.exists('users.json'):
                with open('users.json', 'r') as f:
                    return json.load(f)
            else:
                # Create default admin user if file doesn't exist
                default_users = [{
                    'username': 'admin',
                    'password': hashlib.sha256('admin123'.encode()).hexdigest(),
                    'role': 'admin',
                    'full_name': 'System Administrator'
                }]
                # Save the default user
                with open('users.json', 'w') as f:
                    json.dump(default_users, f, indent=4)
                return default_users
        except Exception as e:
            print(f"Error loading users: {e}")
            return []
    
    def save_users(self, users):
        try:
            with open('users.json', 'w') as f:
                json.dump(users, f, indent=4)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save users: {str(e)}")
    
    def add_user(self, tree):
        add_window = tk.Toplevel(self.root)
        add_window.title("Add User")
        add_window.geometry("300x300")
        add_window.resizable(False, False)
        
        # Set font for add window
        for widget in add_window.winfo_children():
            if isinstance(widget, (ttk.Label, ttk.Button, ttk.Entry)):
                widget.configure(font=set_times_new_roman(10))
        
        frame = ttk.Frame(add_window, padding=10)
        frame.pack(fill='both', expand=True)
        
        ttk.Label(frame, text="Username:").grid(row=0, column=0, sticky='e', pady=5)
        username_entry = ttk.Entry(frame)
        username_entry.grid(row=0, column=1, sticky='w', pady=5, padx=(10, 0))
        
        ttk.Label(frame, text="Full Name:").grid(row=1, column=0, sticky='e', pady=5)
        fullname_entry = ttk.Entry(frame)
        fullname_entry.grid(row=1, column=1, sticky='w', pady=5, padx=(10, 0))
        
        ttk.Label(frame, text="Password:").grid(row=2, column=0, sticky='e', pady=5)
        password_entry = ttk.Entry(frame, show="*")
        password_entry.grid(row=2, column=1, sticky='w', pady=5, padx=(10, 0))
        
        ttk.Label(frame, text="Confirm Password:").grid(row=3, column=0, sticky='e', pady=5)
        confirm_entry = ttk.Entry(frame, show="*")
        confirm_entry.grid(row=3, column=1, sticky='w', pady=5, padx=(10, 0))
        
        ttk.Label(frame, text="Role:").grid(row=4, column=0, sticky='e', pady=5)
        role_var = tk.StringVar(value='user')
        role_combo = ttk.Combobox(frame, textvariable=role_var, values=['admin', 'user'], state='readonly')
        role_combo.grid(row=4, column=1, sticky='w', pady=5, padx=(10, 0))
        
        def save_user():
            username = username_entry.get().strip()
            full_name = fullname_entry.get().strip()
            password = password_entry.get().strip()
            confirm = confirm_entry.get().strip()
            role = role_var.get()
            
            if not username or not full_name or not password:
                messagebox.showerror("Error", "All fields are required")
                return
                
            if password != confirm:
                messagebox.showerror("Error", "Passwords do not match")
                return
                
            users = self.load_users()
            
            # Check if username already exists
            if any(u['username'] == username for u in users):
                messagebox.showerror("Error", "Username already exists")
                return
                
            # Hash password
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            
            # Add user
            users.append({
                'username': username,
                'full_name': full_name,
                'password': hashed_password,
                'role': role
            })
            
            self.save_users(users)
            
            # Update treeview
            tree.insert('', 'end', values=(username, full_name, role))
            
            add_window.destroy()
            messagebox.showinfo("Success", "User added successfully")
        
        ttk.Button(frame, text="Save", command=save_user).grid(row=5, column=0, columnspan=2, pady=20)
    
    def edit_user(self, tree):
        selected = tree.focus()
        if not selected:
            messagebox.showwarning("Warning", "Please select a user to edit")
            return
            
        values = tree.item(selected, 'values')
        if not values:
            return
            
        username = values[0]
        
        users = self.load_users()
        user = next((u for u in users if u['username'] == username), None)
        if not user:
            messagebox.showerror("Error", "User not found")
            return
            
        edit_window = tk.Toplevel(self.root)
        edit_window.title("Edit User")
        edit_window.geometry("300x350")
        edit_window.resizable(False, False)
        
        # Set font for edit window
        for widget in edit_window.winfo_children():
            if isinstance(widget, (ttk.Label, ttk.Button, ttk.Entry)):
                widget.configure(font=set_times_new_roman(10))
        
        frame = ttk.Frame(edit_window, padding=10)
        frame.pack(fill='both', expand=True)
        
        ttk.Label(frame, text="Username:").grid(row=0, column=0, sticky='e', pady=5)
        username_entry = ttk.Entry(frame)
        username_entry.insert(0, user['username'])
        username_entry.config(state='readonly')
        username_entry.grid(row=0, column=1, sticky='w', pady=5, padx=(10, 0))
        
        ttk.Label(frame, text="Full Name:").grid(row=1, column=0, sticky='e', pady=5)
        fullname_entry = ttk.Entry(frame)
        fullname_entry.insert(0, user['full_name'])
        fullname_entry.grid(row=1, column=1, sticky='w', pady=5, padx=(10, 0))
        
        ttk.Label(frame, text="New Password:").grid(row=2, column=0, sticky='e', pady=5)
        password_entry = ttk.Entry(frame, show="*")
        password_entry.grid(row=2, column=1, sticky='w', pady=5, padx=(10, 0))
        
        ttk.Label(frame, text="Confirm Password:").grid(row=3, column=0, sticky='e', pady=5)
        confirm_entry = ttk.Entry(frame, show="*")
        confirm_entry.grid(row=3, column=1, sticky='w', pady=5, padx=(10, 0))
        
        ttk.Label(frame, text="Role:").grid(row=4, column=0, sticky='e', pady=5)
        role_var = tk.StringVar(value=user['role'])
        role_combo = ttk.Combobox(frame, textvariable=role_var, values=['admin', 'user'], state='readonly')
        role_combo.grid(row=4, column=1, sticky='w', pady=5, padx=(10, 0))
        
        def save_changes():
            full_name = fullname_entry.get().strip()
            password = password_entry.get().strip()
            confirm = confirm_entry.get().strip()
            role = role_var.get()
            
            if not full_name:
                messagebox.showerror("Error", "Full name is required")
                return
                
            if password and password != confirm:
                messagebox.showerror("Error", "Passwords do not match")
                return
                
            # Update user
            user['full_name'] = full_name
            user['role'] = role
            
            if password:
                user['password'] = hashlib.sha256(password.encode()).hexdigest()
            
            self.save_users(users)
            
            # Update treeview
            tree.item(selected, values=(user['username'], user['full_name'], user['role']))
            
            edit_window.destroy()
            messagebox.showinfo("Success", "User updated successfully")
        
        ttk.Button(frame, text="Save Changes", command=save_changes).grid(row=5, column=0, columnspan=2, pady=20)
    
    def delete_user(self, tree):
        selected = tree.focus()
        if not selected:
            messagebox.showwarning("Warning", "Please select a user to delete")
            return
            
        values = tree.item(selected, 'values')
        if not values:
            return
            
        username = values[0]
        
        if username == self.user['username']:
            messagebox.showerror("Error", "You cannot delete your own account")
            return
            
        if not messagebox.askyesno("Confirm", f"Are you sure you want to delete user {username}?"):
            return
            
        users = self.load_users()
        users = [u for u in users if u['username'] != username]
        self.save_users(users)
        
        tree.delete(selected)
        messagebox.showinfo("Success", "User deleted successfully")
    
    def build_client_section(self):
        # Main frame for client section
        main_frame = ttk.Frame(self.client_frame)
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Left frame for client list
        left_frame = ttk.Frame(main_frame)
        left_frame.pack(side='left', fill='both', expand=True, padx=(0, 10))
        
        # Client list with scrollbar
        list_frame = ttk.Frame(left_frame)
        list_frame.pack(fill='both', expand=True)
        
        # Search frame
        search_frame = ttk.Frame(list_frame)
        search_frame.pack(fill='x', pady=(0, 5))
        
        ttk.Label(search_frame, text="Search:").pack(side='left')
        self.client_search = ttk.Entry(search_frame)
        self.client_search.pack(side='left', fill='x', expand=True, padx=(5, 0))
        self.client_search.bind('<KeyRelease>', self.filter_clients)
        
        # Treeview for clients
        columns = ('id', 'name', 'dob', 'phone', 'status')
        self.client_tree = ttk.Treeview(list_frame, columns=columns, show='headings')
        
        # Define headings
        self.client_tree.heading('id', text='ID')
        self.client_tree.heading('name', text='Name')
        self.client_tree.heading('dob', text='Date of Birth')
        self.client_tree.heading('phone', text='Phone')
        self.client_tree.heading('status', text='Status')
        
        # Define columns
        self.client_tree.column('id', width=50)
        self.client_tree.column('name', width=150)
        self.client_tree.column('dob', width=100)
        self.client_tree.column('phone', width=100)
        self.client_tree.column('status', width=100)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient='vertical', command=self.client_tree.yview)
        self.client_tree.configure(yscrollcommand=scrollbar.set)
        
        self.client_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Bind selection
        self.client_tree.bind('<<TreeviewSelect>>', self.on_client_select)
        
        # Button frame
        button_frame = ttk.Frame(left_frame)
        button_frame.pack(fill='x', pady=(5, 0))
        
        ttk.Button(button_frame, text="Add Client", command=self.add_client).pack(side='left', padx=(0, 5))
        ttk.Button(button_frame, text="Edit Client", command=self.edit_client).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Delete Client", command=self.delete_client).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Export Data", command=self.export_client_data).pack(side='right')
        
        # Right frame for client details
        right_frame = ttk.LabelFrame(main_frame, text="Client Details")
        right_frame.pack(side='right', fill='both', expand=False, padx=(10, 0))
        
        # Client details form
        detail_frame = ttk.Frame(right_frame)
        detail_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Form fields
        ttk.Label(detail_frame, text="Client ID:").grid(row=0, column=0, sticky='e', pady=2)
        self.client_id = ttk.Entry(detail_frame, state='readonly')
        self.client_id.grid(row=0, column=1, sticky='ew', pady=2, padx=(5, 0))
        
        ttk.Label(detail_frame, text="Full Name:").grid(row=1, column=0, sticky='e', pady=2)
        self.client_name = ttk.Entry(detail_frame)
        self.client_name.grid(row=1, column=1, sticky='ew', pady=2, padx=(5, 0))
        
        ttk.Label(detail_frame, text="Date of Birth:").grid(row=2, column=0, sticky='e', pady=2)
        self.client_dob = ttk.Entry(detail_frame)
        self.client_dob.grid(row=2, column=1, sticky='ew', pady=2, padx=(5, 0))
        
        ttk.Label(detail_frame, text="Phone:").grid(row=3, column=0, sticky='e', pady=2)
        self.client_phone = ttk.Entry(detail_frame)
        self.client_phone.grid(row=3, column=1, sticky='ew', pady=2, padx=(5, 0))
        
        ttk.Label(detail_frame, text="Address:").grid(row=4, column=0, sticky='e', pady=2)
        self.client_address = ttk.Entry(detail_frame)
        self.client_address.grid(row=4, column=1, sticky='ew', pady=2, padx=(5, 0))
        
        ttk.Label(detail_frame, text="Medical Condition:").grid(row=5, column=0, sticky='e', pady=2)
        self.client_condition = ttk.Entry(detail_frame)
        self.client_condition.grid(row=5, column=1, sticky='ew', pady=2, padx=(5, 0))
        
        ttk.Label(detail_frame, text="Status:").grid(row=6, column=0, sticky='e', pady=2)
        self.client_status = ttk.Combobox(detail_frame, values=['Active', 'Inactive', 'Deceased'])
        self.client_status.grid(row=6, column=1, sticky='ew', pady=2, padx=(5, 0))
        
        ttk.Label(detail_frame, text="Notes:").grid(row=7, column=0, sticky='ne', pady=2)
        self.client_notes = tk.Text(detail_frame, height=5, width=30)
        self.client_notes.grid(row=7, column=1, sticky='ew', pady=2, padx=(5, 0))
        
        # Configure grid weights
        detail_frame.columnconfigure(1, weight=1)
        
        # Save button
        ttk.Button(right_frame, text="Save Changes", command=self.save_client_changes).pack(pady=10)
    
    def build_supplies_section(self):
        # Create notebook for medication and supplies
        supplies_notebook = ttk.Notebook(self.supplies_frame)
        supplies_notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Medication frame
        med_frame = ttk.Frame(supplies_notebook)
        supplies_notebook.add(med_frame, text="Medications")
        
        # Supplies frame
        sup_frame = ttk.Frame(supplies_notebook)
        supplies_notebook.add(sup_frame, text="Supplies")
        
        # Stock correlation frame
        stock_frame = ttk.Frame(supplies_notebook)
        supplies_notebook.add(stock_frame, text="Stock Correlation")
        
        # Build medication section
        self.build_medication_section(med_frame)
        
        # Build supplies section
        self.build_supplies_subsection(sup_frame)
        
        # Build stock correlation section
        self.build_stock_correlation_section(stock_frame)
    
    def build_stock_correlation_section(self, parent):
        # Main frame
        main_frame = ttk.Frame(parent)
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Left frame for medication list
        left_frame = ttk.Frame(main_frame)
        left_frame.pack(side='left', fill='both', expand=True, padx=(0, 10))
        
        ttk.Label(left_frame, text="Medication Stock Levels", font=set_times_new_roman(12, "bold")).pack(pady=(0, 10))
        
        # Create a frame for the medication chart
        med_chart_frame = ttk.Frame(left_frame)
        med_chart_frame.pack(fill='both', expand=True)
        
        # Right frame for supplies list
        right_frame = ttk.Frame(main_frame)
        right_frame.pack(side='right', fill='both', expand=True, padx=(10, 0))
        
        ttk.Label(right_frame, text="Supply Stock Levels", font=set_times_new_roman(12, "bold")).pack(pady=(0, 10))
        
        # Create a frame for the supplies chart
        sup_chart_frame = ttk.Frame(right_frame)
        sup_chart_frame.pack(fill='both', expand=True)
        
        # Generate the charts
        self.update_stock_charts(med_chart_frame, sup_chart_frame)
        
        # Button to refresh charts
        ttk.Button(main_frame, text="Refresh Charts", command=lambda: self.update_stock_charts(med_chart_frame, sup_chart_frame)).pack(pady=10)
    
    def update_stock_charts(self, med_frame, sup_frame):
        # Clear existing frames
        for widget in med_frame.winfo_children():
            widget.destroy()
        for widget in sup_frame.winfo_children():
            widget.destroy()
        
        # Create medication chart
        med_fig, med_ax = plt.subplots(figsize=(6, 4))
        med_names = [med['name'] for med in self.medications]
        med_quantities = [int(med['quantity']) for med in self.medications]
        
        if med_names and med_quantities:
            med_ax.bar(med_names, med_quantities)
            med_ax.set_title('Medication Stock Levels', fontname='Times New Roman')
            med_ax.set_ylabel('Quantity', fontname='Times New Roman')
            med_ax.tick_params(axis='x', rotation=45)
            
            # Set Times New Roman font for tick labels
            for label in med_ax.get_xticklabels():
                label.set_fontname('Times New Roman')
            for label in med_ax.get_yticklabels():
                label.set_fontname('Times New Roman')
                
            med_fig.tight_layout()
            
            # Embed in tkinter
            med_canvas = FigureCanvasTkAgg(med_fig, med_frame)
            med_canvas.draw()
            med_canvas.get_tk_widget().pack(fill='both', expand=True)
        else:
            ttk.Label(med_frame, text="No medication data available").pack()
        
        # Create supplies chart
        sup_fig, sup_ax = plt.subplots(figsize=(6, 4))
        sup_names = [sup['name'] for sup in self.supplies]
        sup_quantities = [int(sup['quantity']) for sup in self.supplies]
        
        if sup_names and sup_quantities:
            sup_ax.bar(sup_names, sup_quantities)
            sup_ax.set_title('Supply Stock Levels', fontname='Times New Roman')
            sup_ax.set_ylabel('Quantity', fontname='Times New Roman')
            sup_ax.tick_params(axis='x', rotation=45)
            
            # Set Times New Roman font for tick labels
            for label in sup_ax.get_xticklabels():
                label.set_fontname('Times New Roman')
            for label in sup_ax.get_yticklabels():
                label.set_fontname('Times New Roman')
                
            sup_fig.tight_layout()
            
            # Embed in tkinter
            sup_canvas = FigureCanvasTkAgg(sup_fig, sup_frame)
            sup_canvas.draw()
            sup_canvas.get_tk_widget().pack(fill='both', expand=True)
        else:
            ttk.Label(sup_frame, text="No supply data available").pack()
    
    def build_medication_section(self, parent):
        # Main frame for medication
        main_frame = ttk.Frame(parent)
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Left frame for medication list
        left_frame = ttk.Frame(main_frame)
        left_frame.pack(side='left', fill='both', expand=True, padx=(0, 10))
        
        # Medication list with scrollbar
        list_frame = ttk.Frame(left_frame)
        list_frame.pack(fill='both', expand=True)
        
        # Search frame
        search_frame = ttk.Frame(list_frame)
        search_frame.pack(fill='x', pady=(0, 5))
        
        ttk.Label(search_frame, text="Search:").pack(side='left')
        self.med_search = ttk.Entry(search_frame)
        self.med_search.pack(side='left', fill='x', expand=True, padx=(5, 0))
        self.med_search.bind('<KeyRelease>', self.filter_medications)
        
        # Treeview for medications
        columns = ('id', 'name', 'quantity', 'min_stock', 'last_restocked')
        self.med_tree = ttk.Treeview(list_frame, columns=columns, show='headings')
        
        # Define headings
        self.med_tree.heading('id', text='ID')
        self.med_tree.heading('name', text='Name')
        self.med_tree.heading('quantity', text='Quantity')
        self.med_tree.heading('min_stock', text='Min Stock')
        self.med_tree.heading('last_restocked', text='Last Restocked')
        
        # Define columns
        self.med_tree.column('id', width=50)
        self.med_tree.column('name', width=150)
        self.med_tree.column('quantity', width=80)
        self.med_tree.column('min_stock', width=80)
        self.med_tree.column('last_restocked', width=100)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient='vertical', command=self.med_tree.yview)
        self.med_tree.configure(yscrollcommand=scrollbar.set)
        
        self.med_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Bind selection
        self.med_tree.bind('<<TreeviewSelect>>', self.on_med_select)
        
        # Button frame
        button_frame = ttk.Frame(left_frame)
        button_frame.pack(fill='x', pady=(5, 0))
        
        ttk.Button(button_frame, text="Add Medication", command=self.add_medication).pack(side='left', padx=(0, 5))
        ttk.Button(button_frame, text="Edit Medication", command=self.edit_medication).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Delete Medication", command=self.delete_medication).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Restock Medication", command=self.restock_medication).pack(side='left', padx=5)
        
        # Right frame for medication details
        right_frame = ttk.LabelFrame(main_frame, text="Medication Details")
        right_frame.pack(side='right', fill='both', expand=False, padx=(10, 0))
        
        # Medication details form
        detail_frame = ttk.Frame(right_frame)
        detail_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Form fields
        ttk.Label(detail_frame, text="Medication ID:").grid(row=0, column=0, sticky='e', pady=2)
        self.med_id = ttk.Entry(detail_frame, state='readonly')
        self.med_id.grid(row=0, column=1, sticky='ew', pady=2, padx=(5, 0))
        
        ttk.Label(detail_frame, text="Name:").grid(row=1, column=0, sticky='e', pady=2)
        self.med_name = ttk.Entry(detail_frame)
        self.med_name.grid(row=1, column=1, sticky='ew', pady=2, padx=(5, 0))
        
        ttk.Label(detail_frame, text="Description:").grid(row=2, column=0, sticky='e', pady=2)
        self.med_desc = ttk.Entry(detail_frame)
        self.med_desc.grid(row=2, column=1, sticky='ew', pady=2, padx=(5, 0))
        
        ttk.Label(detail_frame, text="Quantity:").grid(row=3, column=0, sticky='e', pady=2)
        self.med_quantity = ttk.Entry(detail_frame)
        self.med_quantity.grid(row=3, column=1, sticky='ew', pady=2, padx=(5, 0))
        
        ttk.Label(detail_frame, text="Min Stock Level:").grid(row=4, column=0, sticky='e', pady=2)
        self.med_min_stock = ttk.Entry(detail_frame)
        self.med_min_stock.grid(row=4, column=1, sticky='ew', pady=2, padx=(5, 0))
        
        ttk.Label(detail_frame, text="Last Restocked:").grid(row=5, column=0, sticky='e', pady=2)
        self.med_last_restocked = ttk.Entry(detail_frame)
        self.med_last_restocked.grid(row=5, column=1, sticky='ew', pady=2, padx=(5, 0))
        
        # Configure grid weights
        detail_frame.columnconfigure(1, weight=1)
        
        # Save button
        ttk.Button(right_frame, text="Save Changes", command=self.save_medication_changes).pack(pady=10)
    
    def build_supplies_subsection(self, parent):
        # Main frame for supplies
        main_frame = ttk.Frame(parent)
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Left frame for supplies list
        left_frame = ttk.Frame(main_frame)
        left_frame.pack(side='left', fill='both', expand=True, padx=(0, 10))
        
        # Supplies list with scrollbar
        list_frame = ttk.Frame(left_frame)
        list_frame.pack(fill='both', expand=True)
        
        # Search frame
        search_frame = ttk.Frame(list_frame)
        search_frame.pack(fill='x', pady=(0, 5))
        
        ttk.Label(search_frame, text="Search:").pack(side='left')
        self.sup_search = ttk.Entry(search_frame)
        self.sup_search.pack(side='left', fill='x', expand=True, padx=(5, 0))
        self.sup_search.bind('<KeyRelease>', self.filter_supplies)
        
        # Treeview for supplies
        columns = ('id', 'name', 'quantity', 'min_stock', 'last_restocked')
        self.sup_tree = ttk.Treeview(list_frame, columns=columns, show='headings')
        
        # Define headings
        self.sup_tree.heading('id', text='ID')
        self.sup_tree.heading('name', text='Name')
        self.sup_tree.heading('quantity', text='Quantity')
        self.sup_tree.heading('min_stock', text='Min Stock')
        self.sup_tree.heading('last_restocked', text='Last Restocked')
        
        # Define columns
        self.sup_tree.column('id', width=50)
        self.sup_tree.column('name', width=150)
        self.sup_tree.column('quantity', width=80)
        self.sup_tree.column('min_stock', width=80)
        self.sup_tree.column('last_restocked', width=100)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient='vertical', command=self.sup_tree.yview)
        self.sup_tree.configure(yscrollcommand=scrollbar.set)
        
        self.sup_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Bind selection
        self.sup_tree.bind('<<TreeviewSelect>>', self.on_sup_select)
        
        # Button frame
        button_frame = ttk.Frame(left_frame)
        button_frame.pack(fill='x', pady=(5, 0))
        
        ttk.Button(button_frame, text="Add Supply", command=self.add_supply).pack(side='left', padx=(0, 5))
        ttk.Button(button_frame, text="Edit Supply", command=self.edit_supply).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Delete Supply", command=self.delete_supply).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Restock Supply", command=self.restock_supply).pack(side='left', padx=5)
        
        # Right frame for supply details
        right_frame = ttk.LabelFrame(main_frame, text="Supply Details")
        right_frame.pack(side='right', fill='both', expand=False, padx=(10, 0))
        
        # Supply details form
        detail_frame = ttk.Frame(right_frame)
        detail_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Form fields
        ttk.Label(detail_frame, text="Supply ID:").grid(row=0, column=0, sticky='e', pady=2)
        self.sup_id = ttk.Entry(detail_frame, state='readonly')
        self.sup_id.grid(row=0, column=1, sticky='ew', pady=2, padx=(5, 0))
        
        ttk.Label(detail_frame, text="Name:").grid(row=1, column=0, sticky='e', pady=2)
        self.sup_name = ttk.Entry(detail_frame)
        self.sup_name.grid(row=1, column=1, sticky='ew', pady=2, padx=(5, 0))
        
        ttk.Label(detail_frame, text="Description:").grid(row=2, column=0, sticky='e', pady=2)
        self.sup_desc = ttk.Entry(detail_frame)
        self.sup_desc.grid(row=2, column=1, sticky='ew', pady=2, padx=(5, 0))
        
        ttk.Label(detail_frame, text="Quantity:").grid(row=3, column=0, sticky='e', pady=2)
        self.sup_quantity = ttk.Entry(detail_frame)
        self.sup_quantity.grid(row=3, column=1, sticky='ew', pady=2, padx=(5, 0))
        
        ttk.Label(detail_frame, text="Min Stock Level:").grid(row=4, column=0, sticky='e', pady=2)
        self.sup_min_stock = ttk.Entry(detail_frame)
        self.sup_min_stock.grid(row=4, column=1, sticky='ew', pady=2, padx=(5, 0))
        
        ttk.Label(detail_frame, text="Last Restocked:").grid(row=5, column=0, sticky='e', pady=2)
        self.sup_last_restocked = ttk.Entry(detail_frame)
        self.sup_last_restocked.grid(row=5, column=1, sticky='ew', pady=2, padx=(5, 0))
        
        # Configure grid weights
        detail_frame.columnconfigure(1, weight=1)
        
        # Save button
        ttk.Button(right_frame, text="Save Changes", command=self.save_supply_changes).pack(pady=10)
    
    def build_dashboard_section(self):
        # Main frame for dashboard
        main_frame = ttk.Frame(self.dashboard_frame)
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Summary frame
        summary_frame = ttk.LabelFrame(main_frame, text="Summary")
        summary_frame.pack(fill='x', pady=(0, 10))
        
        # Summary metrics
        metrics_frame = ttk.Frame(summary_frame)
        metrics_frame.pack(fill='x', padx=10, pady=10)
        
        # Client metrics
        ttk.Label(metrics_frame, text="Total Clients:", font=set_times_new_roman(10, "bold")).grid(row=0, column=0, sticky='w', padx=(0, 20))
        self.total_clients = ttk.Label(metrics_frame, text="0", font=set_times_new_roman(10))
        self.total_clients.grid(row=0, column=1, sticky='w', padx=(0, 40))
        
        ttk.Label(metrics_frame, text="Active Clients:", font=set_times_new_roman(10, "bold")).grid(row=0, column=2, sticky='w', padx=(0, 20))
        self.active_clients = ttk.Label(metrics_frame, text="0", font=set_times_new_roman(10))
        self.active_clients.grid(row=0, column=3, sticky='w', padx=(0, 40))
        
        # Medication metrics
        ttk.Label(metrics_frame, text="Medication Types:", font=set_times_new_roman(10, "bold")).grid(row=1, column=0, sticky='w', padx=(0, 20))
        self.total_meds = ttk.Label(metrics_frame, text="0", font=set_times_new_roman(10))
        self.total_meds.grid(row=1, column=1, sticky='w', padx=(0, 40))
        
        ttk.Label(metrics_frame, text="Low Stock Medications:", font=set_times_new_roman(10, "bold")).grid(row=1, column=2, sticky='w', padx=(0, 20))
        self.low_stock_meds = ttk.Label(metrics_frame, text="0", font=set_times_new_roman(10))
        self.low_stock_meds.grid(row=1, column=3, sticky='w', padx=(0, 40))
        
        # Supply metrics
        ttk.Label(metrics_frame, text="Supply Types:", font=set_times_new_roman(10, "bold")).grid(row=2, column=0, sticky='w', padx=(0, 20))
        self.total_supplies = ttk.Label(metrics_frame, text="0", font=set_times_new_roman(10))
        self.total_supplies.grid(row=2, column=1, sticky='w', padx=(0, 40))
        
        ttk.Label(metrics_frame, text="Low Stock Supplies:", font=set_times_new_roman(10, "bold")).grid(row=2, column=2, sticky='w', padx=(0, 20))
        self.low_stock_supplies = ttk.Label(metrics_frame, text="0", font=set_times_new_roman(10))
        self.low_stock_supplies.grid(row=2, column=3, sticky='w', padx=(0, 40))
        
        # Charts frame
        charts_frame = ttk.Frame(main_frame)
        charts_frame.pack(fill='both', expand=True)
        
        # Left chart (client status)
        left_chart_frame = ttk.Frame(charts_frame)
        left_chart_frame.pack(side='left', fill='both', expand=True, padx=(0, 5))
        
        ttk.Label(left_chart_frame, text="Client Status Distribution", font=set_times_new_roman(12, "bold")).pack()
        
        self.client_chart_canvas = tk.Canvas(left_chart_frame, bg='white')
        self.client_chart_canvas.pack(fill='both', expand=True)
        
        # Right chart (stock levels)
        right_chart_frame = ttk.Frame(charts_frame)
        right_chart_frame.pack(side='right', fill='both', expand=True, padx=(5, 0))
        
        ttk.Label(right_chart_frame, text="Stock Status", font=set_times_new_roman(12, "bold")).pack()
        
        self.stock_chart_canvas = tk.Canvas(right_chart_frame, bg='white')
        self.stock_chart_canvas.pack(fill='both', expand=True)
        
        # Update dashboard
        self.update_dashboard()
    
    def build_about_section(self):
        # Main frame for about section
        main_frame = ttk.Frame(self.about_frame)
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Title
        ttk.Label(main_frame, text="MERU HOSPICE CLIENT AND MEDICATION MANAGEMENT SYSTEM", 
                 font=set_times_new_roman(16, "bold")).pack(pady=20)
        
        # Description
        description = """
        This system is designed to manage client information, medication inventory, 
        and medical supplies for Meru Hospice. It provides comprehensive tools for:
        
        • Client registration and management
        • Medication inventory tracking with stock alerts
        • Medical supplies management
        • Reporting and data export capabilities
        • Network reporting for multi-location coordination
        
        The system ensures efficient management of hospice operations with 
        user-friendly interfaces and robust data management capabilities.
        """
        
        ttk.Label(main_frame, text=description, justify='center', 
                 font=set_times_new_roman(11)).pack(pady=10)
        
        # Version info
        ttk.Label(main_frame, text="Version 2.0", 
                 font=set_times_new_roman(10, "italic")).pack(pady=20)
        
        # Developer info
        ttk.Label(main_frame, text="Developed by Meru Hospice IT Department", 
                 font=set_times_new_roman(10)).pack(pady=5)
        
        # Copyright
        ttk.Label(main_frame, text=f"© {datetime.now().year} Meru Hospice. All rights reserved.", 
                 font=set_times_new_roman(9)).pack(pady=5)
    
    def update_dashboard(self):
        # Update summary metrics
        self.total_clients.config(text=str(len(self.clients)))
        active_count = sum(1 for client in self.clients if client.get('status') == 'Active')
        self.active_clients.config(text=str(active_count))
        
        self.total_meds.config(text=str(len(self.medications)))
        low_med_count = sum(1 for med in self.medications if int(med.get('quantity', 0)) <= int(med.get('min_stock', 0)))
        self.low_stock_meds.config(text=str(low_med_count))
        
        self.total_supplies.config(text=str(len(self.supplies)))
        low_sup_count = sum(1 for sup in self.supplies if int(sup.get('quantity', 0)) <= int(sup.get('min_stock', 0)))
        self.low_stock_supplies.config(text=str(low_sup_count))
        
        # Update charts
        self.update_client_chart()
        self.update_stock_chart()
    
    def update_client_chart(self):
        # Clear canvas
        self.client_chart_canvas.delete('all')
        
        # Count client statuses
        status_count = {'Active': 0, 'Inactive': 0, 'Deceased': 0}
        for client in self.clients:
            status = client.get('status', 'Active')
            if status in status_count:
                status_count[status] += 1
        
        # Draw pie chart
        width = self.client_chart_canvas.winfo_width()
        height = self.client_chart_canvas.winfo_height()
        center_x = width // 2
        center_y = height // 2
        radius = min(center_x, center_y) - 20
        
        if sum(status_count.values()) > 0:
            colors = ['green', 'orange', 'red']
            start_angle = 0
            
            for i, (status, count) in enumerate(status_count.items()):
                if count > 0:
                    angle = 360 * count / sum(status_count.values())
                    self.client_chart_canvas.create_arc(
                        center_x - radius, center_y - radius,
                        center_x + radius, center_y + radius,
                        start=start_angle, extent=angle,
                        fill=colors[i], outline='black'
                    )
                    
                    # Draw legend
                    self.client_chart_canvas.create_rectangle(
                        10, 10 + i * 20, 30, 30 + i * 20,
                        fill=colors[i], outline='black'
                    )
                    self.client_chart_canvas.create_text(
                        40, 20 + i * 20,
                        text=f"{status}: {count}",
                        anchor='w', font=set_times_new_roman(9)
                    )
                    
                    start_angle += angle
        else:
            self.client_chart_canvas.create_text(
                center_x, center_y,
                text="No client data available",
                font=set_times_new_roman(10)
            )
    
    def update_stock_chart(self):
        # Clear canvas
        self.stock_chart_canvas.delete('all')
        
        # Count stock status
        stock_status = {'Normal': 0, 'Low': 0, 'Critical': 0}
        
        for item in self.medications + self.supplies:
            quantity = int(item.get('quantity', 0))
            min_stock = int(item.get('min_stock', 0))
            
            if quantity <= min_stock * 0.3:
                stock_status['Critical'] += 1
            elif quantity <= min_stock:
                stock_status['Low'] += 1
            else:
                stock_status['Normal'] += 1
        
        # Draw bar chart
        width = self.stock_chart_canvas.winfo_width()
        height = self.stock_chart_canvas.winfo_height()
        
        if sum(stock_status.values()) > 0:
            max_value = max(stock_status.values())
            bar_width = 40
            spacing = 20
            chart_width = 3 * bar_width + 2 * spacing
            chart_height = height - 60
            start_x = (width - chart_width) // 2
            
            colors = ['green', 'orange', 'red']
            
            for i, (status, count) in enumerate(stock_status.items()):
                bar_height = (count / max_value) * chart_height if max_value > 0 else 0
                x0 = start_x + i * (bar_width + spacing)
                x1 = x0 + bar_width
                y0 = height - 30 - bar_height
                y1 = height - 30
                
                self.stock_chart_canvas.create_rectangle(x0, y0, x1, y1, fill=colors[i], outline='black')
                self.stock_chart_canvas.create_text(x0 + bar_width // 2, y0 - 10, text=str(count), font=set_times_new_roman(9))
                self.stock_chart_canvas.create_text(x0 + bar_width // 2, height - 15, text=status, font=set_times_new_roman(9))
                
                # Draw legend
                self.stock_chart_canvas.create_rectangle(10, 10 + i * 20, 30, 30 + i * 20, fill=colors[i], outline='black')
                self.stock_chart_canvas.create_text(40, 20 + i * 20, text=f"{status}: {count}", anchor='w', font=set_times_new_roman(9))
        else:
            self.stock_chart_canvas.create_text(
                width // 2, height // 2,
                text="No stock data available",
                font=set_times_new_roman(10)
            )
    
    def load_data(self):
        # Load clients
        try:
            if os.path.exists('clients.json'):
                with open('clients.json', 'r') as f:
                    self.clients = json.load(f)
                    self.populate_client_tree()
        except:
            self.clients = []
        
        # Load medications
        try:
            if os.path.exists('medications.json'):
                with open('medications.json', 'r') as f:
                    self.medications = json.load(f)
                    self.populate_med_tree()
        except:
            self.medications = []
        
        # Load supplies
        try:
            if os.path.exists('supplies.json'):
                with open('supplies.json', 'r') as f:
                    self.supplies = json.load(f)
                    self.populate_sup_tree()
        except:
            self.supplies = []
        
        # Update dashboard
        self.update_dashboard()
    
    def save_data(self):
        # Save clients
        with open('clients.json', 'w') as f:
            json.dump(self.clients, f, indent=4)
        
        # Save medications
        with open('medications.json', 'w') as f:
            json.dump(self.medications, f, indent=4)
        
        # Save supplies
        with open('supplies.json', 'w') as f:
            json.dump(self.supplies, f, indent=4)
    
    def populate_client_tree(self):
        # Clear existing items
        for item in self.client_tree.get_children():
            self.client_tree.delete(item)
        
        # Add clients to treeview
        for client in self.clients:
            self.client_tree.insert('', 'end', values=(
                client.get('id', ''),
                client.get('name', ''),
                client.get('dob', ''),
                client.get('phone', ''),
                client.get('status', 'Active')
            ))
    
    def populate_med_tree(self):
        # Clear existing items
        for item in self.med_tree.get_children():
            self.med_tree.delete(item)
        
        # Add medications to treeview
        for med in self.medications:
            self.med_tree.insert('', 'end', values=(
                med.get('id', ''),
                med.get('name', ''),
                med.get('quantity', ''),
                med.get('min_stock', ''),
                med.get('last_restocked', '')
            ))
    
    def populate_sup_tree(self):
        # Clear existing items
        for item in self.sup_tree.get_children():
            self.sup_tree.delete(item)
        
        # Add supplies to treeview
        for sup in self.supplies:
            self.sup_tree.insert('', 'end', values=(
                sup.get('id', ''),
                sup.get('name', ''),
                sup.get('quantity', ''),
                sup.get('min_stock', ''),
                sup.get('last_restocked', '')
            ))
    
    def filter_clients(self, event):
        query = self.client_search.get().lower()
        
        # Clear existing items
        for item in self.client_tree.get_children():
            self.client_tree.delete(item)
        
        # Add filtered clients to treeview
        for client in self.clients:
            if (query in client.get('id', '').lower() or 
                query in client.get('name', '').lower() or 
                query in client.get('phone', '').lower() or
                query in client.get('status', '').lower()):
                
                self.client_tree.insert('', 'end', values=(
                    client.get('id', ''),
                    client.get('name', ''),
                    client.get('dob', ''),
                    client.get('phone', ''),
                    client.get('status', 'Active')
                ))
    
    def filter_medications(self, event):
        query = self.med_search.get().lower()
        
        # Clear existing items
        for item in self.med_tree.get_children():
            self.med_tree.delete(item)
        
        # Add filtered medications to treeview
        for med in self.medications:
            if (query in med.get('id', '').lower() or 
                query in med.get('name', '').lower()):
                
                self.med_tree.insert('', 'end', values=(
                    med.get('id', ''),
                    med.get('name', ''),
                    med.get('quantity', ''),
                    med.get('min_stock', ''),
                    med.get('last_restocked', '')
                ))
    
    def filter_supplies(self, event):
        query = self.sup_search.get().lower()
        
        # Clear existing items
        for item in self.sup_tree.get_children():
            self.sup_tree.delete(item)
        
        # Add filtered supplies to treeview
        for sup in self.supplies:
            if (query in sup.get('id', '').lower() or 
                query in sup.get('name', '').lower()):
                
                self.sup_tree.insert('', 'end', values=(
                    sup.get('id', ''),
                    sup.get('name', ''),
                    sup.get('quantity', ''),
                    sup.get('min_stock', ''),
                    sup.get('last_restocked', '')
                ))
    
    def on_client_select(self, event):
        selected = self.client_tree.focus()
        if not selected:
            return
            
        values = self.client_tree.item(selected, 'values')
        if not values:
            return
            
        # Find client in list
        client_id = values[0]
        client = next((c for c in self.clients if c.get('id') == client_id), None)
        
        if client:
            # Populate form fields
            self.client_id.config(state='normal')
            self.client_id.delete(0, 'end')
            self.client_id.insert(0, client.get('id', ''))
            self.client_id.config(state='readonly')
            
            self.client_name.delete(0, 'end')
            self.client_name.insert(0, client.get('name', ''))
            
            self.client_dob.delete(0, 'end')
            self.client_dob.insert(0, client.get('dob', ''))
            
            self.client_phone.delete(0, 'end')
            self.client_phone.insert(0, client.get('phone', ''))
            
            self.client_address.delete(0, 'end')
            self.client_address.insert(0, client.get('address', ''))
            
            self.client_condition.delete(0, 'end')
            self.client_condition.insert(0, client.get('condition', ''))
            
            self.client_status.set(client.get('status', 'Active'))
            
            self.client_notes.delete(1.0, 'end')
            self.client_notes.insert(1.0, client.get('notes', ''))
    
    def on_med_select(self, event):
        selected = self.med_tree.focus()
        if not selected:
            return
            
        values = self.med_tree.item(selected, 'values')
        if not values:
            return
            
        # Find medication in list
        med_id = values[0]
        med = next((m for m in self.medications if m.get('id') == med_id), None)
        
        if med:
            # Populate form fields
            self.med_id.config(state='normal')
            self.med_id.delete(0, 'end')
            self.med_id.insert(0, med.get('id', ''))
            self.med_id.config(state='readonly')
            
            self.med_name.delete(0, 'end')
            self.med_name.insert(0, med.get('name', ''))
            
            self.med_desc.delete(0, 'end')
            self.med_desc.insert(0, med.get('description', ''))
            
            self.med_quantity.delete(0, 'end')
            self.med_quantity.insert(0, med.get('quantity', ''))
            
            self.med_min_stock.delete(0, 'end')
            self.med_min_stock.insert(0, med.get('min_stock', ''))
            
            self.med_last_restocked.delete(0, 'end')
            self.med_last_restocked.insert(0, med.get('last_restocked', ''))
    
    def on_sup_select(self, event):
        selected = self.sup_tree.focus()
        if not selected:
            return
            
        values = self.sup_tree.item(selected, 'values')
        if not values:
            return
            
        # Find supply in list
        sup_id = values[0]
        sup = next((s for s in self.supplies if s.get('id') == sup_id), None)
        
        if sup:
            # Populate form fields
            self.sup_id.config(state='normal')
            self.sup_id.delete(0, 'end')
            self.sup_id.insert(0, sup.get('id', ''))
            self.sup_id.config(state='readonly')
            
            self.sup_name.delete(0, 'end')
            self.sup_name.insert(0, sup.get('name', ''))
            
            self.sup_desc.delete(0, 'end')
            self.sup_desc.insert(0, sup.get('description', ''))
            
            self.sup_quantity.delete(0, 'end')
            self.sup_quantity.insert(0, sup.get('quantity', ''))
            
            self.sup_min_stock.delete(0, 'end')
            self.sup_min_stock.insert(0, sup.get('min_stock', ''))
            
            self.sup_last_restocked.delete(0, 'end')
            self.sup_last_restocked.insert(0, sup.get('last_restocked', ''))
    
    def add_client(self):
        # Generate new ID
        if self.clients:
            new_id = str(max(int(c.get('id', '0')) for c in self.clients) + 1)
        else:
            new_id = '1'
        
        # Create new client
        new_client = {
            'id': new_id,
            'name': '',
            'dob': '',
            'phone': '',
            'address': '',
            'condition': '',
            'status': 'Active',
            'notes': ''
        }
        
        self.clients.append(new_client)
        self.populate_client_tree()
        
        # Select the new client
        for item in self.client_tree.get_children():
            if self.client_tree.item(item, 'values')[0] == new_id:
                self.client_tree.focus(item)
                self.client_tree.selection_set(item)
                self.on_client_select(None)
                break
    
    def edit_client(self):
        selected = self.client_tree.focus()
        if not selected:
            messagebox.showwarning("Warning", "Please select a client to edit")
            return
            
        self.on_client_select(None)
    
    def delete_client(self):
        selected = self.client_tree.focus()
        if not selected:
            messagebox.showwarning("Warning", "Please select a client to delete")
            return
            
        values = self.client_tree.item(selected, 'values')
        if not values:
            return
            
        client_id = values[0]
        
        if not messagebox.askyesno("Confirm", f"Are you sure you want to delete client {values[1]}?"):
            return
            
        # Remove client from list
        self.clients = [c for c in self.clients if c.get('id') != client_id]
        self.populate_client_tree()
        self.clear_client_form()
        self.save_data()
        self.update_dashboard()
    
    def clear_client_form(self):
        self.client_id.config(state='normal')
        self.client_id.delete(0, 'end')
        self.client_id.config(state='readonly')
        
        self.client_name.delete(0, 'end')
        self.client_dob.delete(0, 'end')
        self.client_phone.delete(0, 'end')
        self.client_address.delete(0, 'end')
        self.client_condition.delete(0, 'end')
        self.client_status.set('')
        self.client_notes.delete(1.0, 'end')
    
    def save_client_changes(self):
        # Get current client ID
        client_id = self.client_id.get()
        if not client_id:
            return
            
        # Find client in list
        client = next((c for c in self.clients if c.get('id') == client_id), None)
        if not client:
            return
            
        # Update client data
        client['name'] = self.client_name.get()
        client['dob'] = self.client_dob.get()
        client['phone'] = self.client_phone.get()
        client['address'] = self.client_address.get()
        client['condition'] = self.client_condition.get()
        client['status'] = self.client_status.get()
        client['notes'] = self.client_notes.get(1.0, 'end-1c')
        
        # Update treeview
        self.populate_client_tree()
        self.save_data()
        self.update_dashboard()
        
        messagebox.showinfo("Success", "Client data saved successfully")
    
    def add_medication(self):
        # Generate new ID
        if self.medications:
            new_id = str(max(int(m.get('id', '0')) for m in self.medications) + 1)
        else:
            new_id = '1'
        
        # Create new medication
        new_med = {
            'id': new_id,
            'name': '',
            'description': '',
            'quantity': '0',
            'min_stock': '10',
            'last_restocked': date.today().isoformat()
        }
        
        self.medications.append(new_med)
        self.populate_med_tree()
        
        # Select the new medication
        for item in self.med_tree.get_children():
            if self.med_tree.item(item, 'values')[0] == new_id:
                self.med_tree.focus(item)
                self.med_tree.selection_set(item)
                self.on_med_select(None)
                break
    
    def edit_medication(self):
        selected = self.med_tree.focus()
        if not selected:
            messagebox.showwarning("Warning", "Please select a medication to edit")
            return
            
        self.on_med_select(None)
    
    def delete_medication(self):
        selected = self.med_tree.focus()
        if not selected:
            messagebox.showwarning("Warning", "Please select a medication to delete")
            return
            
        values = self.med_tree.item(selected, 'values')
        if not values:
            return
            
        med_id = values[0]
        
        if not messagebox.askyesno("Confirm", f"Are you sure you want to delete medication {values[1]}?"):
            return
            
        # Remove medication from list
        self.medications = [m for m in self.medications if m.get('id') != med_id]
        self.populate_med_tree()
        self.clear_med_form()
        self.save_data()
        self.update_dashboard()
    
    def clear_med_form(self):
        self.med_id.config(state='normal')
        self.med_id.delete(0, 'end')
        self.med_id.config(state='readonly')
        
        self.med_name.delete(0, 'end')
        self.med_desc.delete(0, 'end')
        self.med_quantity.delete(0, 'end')
        self.med_min_stock.delete(0, 'end')
        self.med_last_restocked.delete(0, 'end')
    
    def save_medication_changes(self):
        # Get current medication ID
        med_id = self.med_id.get()
        if not med_id:
            return
            
        # Find medication in list
        med = next((m for m in self.medications if m.get('id') == med_id), None)
        if not med:
            return
            
        # Update medication data
        med['name'] = self.med_name.get()
        med['description'] = self.med_desc.get()
        med['quantity'] = self.med_quantity.get()
        med['min_stock'] = self.med_min_stock.get()
        med['last_restocked'] = self.med_last_restocked.get()
        
        # Update treeview
        self.populate_med_tree()
        self.save_data()
        self.update_dashboard()
        
        messagebox.showinfo("Success", "Medication data saved successfully")
    
    def restock_medication(self):
        selected = self.med_tree.focus()
        if not selected:
            messagebox.showwarning("Warning", "Please select a medication to restock")
            return
            
        values = self.med_tree.item(selected, 'values')
        if not values:
            return
            
        med_id = values[0]
        
        # Find medication in list
        med = next((m for m in self.medications if m.get('id') == med_id), None)
        if not med:
            return
            
        # Ask for restock quantity
        quantity = tk.simpledialog.askinteger("Restock", f"Enter restock quantity for {med['name']}:", minvalue=1)
        if quantity is None:
            return
            
        # Update medication
        med['quantity'] = str(int(med.get('quantity', 0)) + quantity)
        med['last_restocked'] = date.today().isoformat()
        
        # Update treeview
        self.populate_med_tree()
        self.save_data()
        self.update_dashboard()
        
        messagebox.showinfo("Success", f"Restocked {quantity} units of {med['name']}")
    
    def add_supply(self):
        # Generate new ID
        if self.supplies:
            new_id = str(max(int(s.get('id', '0')) for s in self.supplies) + 1)
        else:
            new_id = '1'
        
        # Create new supply
        new_sup = {
            'id': new_id,
            'name': '',
            'description': '',
            'quantity': '0',
            'min_stock': '10',
            'last_restocked': date.today().isoformat()
        }
        
        self.supplies.append(new_sup)
        self.populate_sup_tree()
        
        # Select the new supply
        for item in self.sup_tree.get_children():
            if self.sup_tree.item(item, 'values')[0] == new_id:
                self.sup_tree.focus(item)
                self.sup_tree.selection_set(item)
                self.on_sup_select(None)
                break
    
    def edit_supply(self):
        selected = self.sup_tree.focus()
        if not selected:
            messagebox.showwarning("Warning", "Please select a supply to edit")
            return
            
        self.on_sup_select(None)
    
    def delete_supply(self):
        selected = self.sup_tree.focus()
        if not selected:
            messagebox.showwarning("Warning", "Please select a supply to delete")
            return
            
        values = self.sup_tree.item(selected, 'values')
        if not values:
            return
            
        sup_id = values[0]
        
        if not messagebox.askyesno("Confirm", f"Are you sure you want to delete supply {values[1]}?"):
            return
            
        # Remove supply from list
        self.supplies = [s for s in self.supplies if s.get('id') != sup_id]
        self.populate_sup_tree()
        self.clear_sup_form()
        self.save_data()
        self.update_dashboard()
    
    def clear_sup_form(self):
        self.sup_id.config(state='normal')
        self.sup_id.delete(0, 'end')
        self.sup_id.config(state='readonly')
        
        self.sup_name.delete(0, 'end')
        self.sup_desc.delete(0, 'end')
        self.sup_quantity.delete(0, 'end')
        self.sup_min_stock.delete(0, 'end')
        self.sup_last_restocked.delete(0, 'end')
    
    def save_supply_changes(self):
        # Get current supply ID
        sup_id = self.sup_id.get()
        if not sup_id:
            return
            
        # Find supply in list
        sup = next((s for s in self.supplies if s.get('id') == sup_id), None)
        if not sup:
            return
            
        # Update supply data
        sup['name'] = self.sup_name.get()
        sup['description'] = self.sup_desc.get()
        sup['quantity'] = self.sup_quantity.get()
        sup['min_stock'] = self.sup_min_stock.get()
        sup['last_restocked'] = self.sup_last_restocked.get()
        
        # Update treeview
        self.populate_sup_tree()
        self.save_data()
        self.update_dashboard()
        
        messagebox.showinfo("Success", "Supply data saved successfully")
    
    def restock_supply(self):
        selected = self.sup_tree.focus()
        if not selected:
            messagebox.showwarning("Warning", "Please select a supply to restock")
            return
            
        values = self.sup_tree.item(selected, 'values')
        if not values:
            return
            
        sup_id = values[0]
        
        # Find supply in list
        sup = next((s for s in self.supplies if s.get('id') == sup_id), None)
        if not sup:
            return
            
        # Ask for restock quantity
        quantity = tk.simpledialog.askinteger("Restock", f"Enter restock quantity for {sup['name']}:", minvalue=1)
        if quantity is None:
            return
            
        # Update supply
        sup['quantity'] = str(int(sup.get('quantity', 0)) + quantity)
        sup['last_restocked'] = date.today().isoformat()
        
        # Update treeview
        self.populate_sup_tree()
        self.save_data()
        self.update_dashboard()
        
        messagebox.showinfo("Success", f"Restocked {quantity} units of {sup['name']}")
    
    def generate_report(self, report_type):
        if report_type == 'client':
            data = self.clients
            filename = f"client_report_{date.today().isoformat()}.csv"
        elif report_type == 'medication':
            data = self.medications
            filename = f"medication_report_{date.today().isoformat()}.csv"
        elif report_type == 'supplies':
            data = self.supplies
            filename = f"supplies_report_{date.today().isoformat()}.csv"
        else:
            return
            
        if not data:
            messagebox.showwarning("Warning", f"No {report_type} data available to generate report")
            return
            
        # Ask for save location
        filepath = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            initialfile=filename
        )
        
        if not filepath:
            return
            
        try:
            # Convert to DataFrame and save as CSV
            df = pd.DataFrame(data)
            df.to_csv(filepath, index=False)
            messagebox.showinfo("Success", f"Report saved as {filepath}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate report: {str(e)}")
    
    def generate_stock_alert_report(self):
        # Get low stock items
        low_stock_meds = [m for m in self.medications if int(m.get('quantity', 0)) <= int(m.get('min_stock', 0))]
        low_stock_supplies = [s for s in self.supplies if int(s.get('quantity', 0)) <= int(s.get('min_stock', 0))]
        
        if not low_stock_meds and not low_stock_supplies:
            messagebox.showinfo("Info", "No low stock items found")
            return
            
        # Combine low stock items
        low_stock_items = low_stock_meds + low_stock_supplies
        
        # Ask for save location
        filename = f"stock_alert_report_{date.today().isoformat()}.csv"
        filepath = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            initialfile=filename
        )
        
        if not filepath:
            return
            
        try:
            # Convert to DataFrame and save as CSV
            df = pd.DataFrame(low_stock_items)
            df.to_csv(filepath, index=False)
            messagebox.showinfo("Success", f"Stock alert report saved as {filepath}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate stock alert report: {str(e)}")
    
    def get_low_stock_items(self):
        low_stock_meds = [m for m in self.medications if int(m.get('quantity', 0)) <= int(m.get('min_stock', 0))]
        low_stock_supplies = [s for s in self.supplies if int(s.get('quantity', 0)) <= int(s.get('min_stock', 0))]
        return low_stock_meds + low_stock_supplies
    
    def export_all_data(self):
        # Create a dictionary with all data
        all_data = {
            'clients': self.clients,
            'medications': self.medications,
            'supplies': self.supplies,
            'export_date': datetime.now().isoformat(),
            'exported_by': self.user['username']
        }
        
        # Ask for save location
        filename = f"meru_hospice_export_{date.today().isoformat()}.json"
        filepath = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            initialfile=filename
        )
        
        if not filepath:
            return
            
        try:
            with open(filepath, 'w') as f:
                json.dump(all_data, f, indent=4)
            messagebox.showinfo("Success", f"All data exported to {filepath}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export data: {str(e)}")
    
    def export_client_data(self):
        if not self.clients:
            messagebox.showwarning("Warning", "No client data available to export")
            return
            
        # Ask for save location
        filename = f"client_data_export_{date.today().isoformat()}.json"
        filepath = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            initialfile=filename
        )
        
        if not filepath:
            return
            
        try:
            with open(filepath, 'w') as f:
                json.dump(self.clients, f, indent=4)
            messagebox.showinfo("Success", f"Client data exported to {filepath}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export client data: {str(e)}")
    
    def run(self):
        self.root.mainloop()

def main():
    # Create login window
    login_root = tk.Tk()
    
    def start_main_app(user):
        # Start main application
        app = MeruHospiceManager(user)
        app.run()
    
    login_app = LoginWindow(login_root, start_main_app)
    login_root.mainloop()

if __name__ == "__main__":
    main()