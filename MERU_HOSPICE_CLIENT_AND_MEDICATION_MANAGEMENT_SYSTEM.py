import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import os
from datetime import date, datetime

class MeruHospiceManager:
    def __init__(self, root):
        self.root = root
        self.root.title("MERU HOSPICE CLIENT AND MEDICATION MANAGEMENT SYSTEM")
        self.root.geometry("1200x800")
        
        # Initialize data structures
        self.clients = []
        self.supplies = []
        self.medications = []
        
        # Create notebook (tabbed interface)
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Create frames for each section
        self.client_frame = ttk.Frame(self.notebook)
        self.supplies_frame = ttk.Frame(self.notebook)
        self.about_frame = ttk.Frame(self.notebook)
        
        self.notebook.add(self.client_frame, text="Client Management")
        self.notebook.add(self.supplies_frame, text="Medication & Supplies")
        self.notebook.add(self.about_frame, text="About")
        
        # Build sections
        self.build_client_section()
        self.build_supplies_section()
        self.build_about_section()
        
        # Load existing data
        self.load_data()
    
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
        
        # Build medication section
        self.build_medication_section(med_frame)
        
        # Build supplies section
        self.build_supplies_subsection(sup_frame)
    
    def build_medication_section(self, parent):
        # Main frame
        main_frame = ttk.Frame(parent)
        main_frame.pack(fill='both', expand=True)
        
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
        columns = ('id', 'name', 'quantity', 'expiry', 'client')
        self.med_tree = ttk.Treeview(list_frame, columns=columns, show='headings')
        
        # Define headings
        self.med_tree.heading('id', text='ID')
        self.med_tree.heading('name', text='Medication Name')
        self.med_tree.heading('quantity', text='Quantity')
        self.med_tree.heading('expiry', text='Expiry Date')
        self.med_tree.heading('client', text='Assigned Client')
        
        # Define columns
        self.med_tree.column('id', width=50)
        self.med_tree.column('name', width=150)
        self.med_tree.column('quantity', width=80)
        self.med_tree.column('expiry', width=100)
        self.med_tree.column('client', width=100)
        
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
        ttk.Button(button_frame, text="Export Data", command=self.export_med_data).pack(side='right')
        
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
        
        ttk.Label(detail_frame, text="Medication Name:").grid(row=1, column=0, sticky='e', pady=2)
        self.med_name = ttk.Entry(detail_frame)
        self.med_name.grid(row=1, column=1, sticky='ew', pady=2, padx=(5, 0))
        
        ttk.Label(detail_frame, text="Quantity:").grid(row=2, column=0, sticky='e', pady=2)
        self.med_quantity = ttk.Entry(detail_frame)
        self.med_quantity.grid(row=2, column=1, sticky='ew', pady=2, padx=(5, 0))
        
        ttk.Label(detail_frame, text="Expiry Date:").grid(row=3, column=0, sticky='e', pady=2)
        self.med_expiry = ttk.Entry(detail_frame)
        self.med_expiry.grid(row=3, column=1, sticky='ew', pady=2, padx=(5, 0))
        
        ttk.Label(detail_frame, text="Assigned Client:").grid(row=4, column=0, sticky='e', pady=2)
        self.med_client = ttk.Combobox(detail_frame)
        self.med_client.grid(row=4, column=1, sticky='ew', pady=2, padx=(5, 0))
        
        ttk.Label(detail_frame, text="Dosage:").grid(row=5, column=0, sticky='e', pady=2)
        self.med_dosage = ttk.Entry(detail_frame)
        self.med_dosage.grid(row=5, column=1, sticky='ew', pady=2, padx=(5, 0))
        
        ttk.Label(detail_frame, text="Instructions:").grid(row=6, column=0, sticky='ne', pady=2)
        self.med_instructions = tk.Text(detail_frame, height=5, width=30)
        self.med_instructions.grid(row=6, column=1, sticky='ew', pady=2, padx=(5, 0))
        
        # Configure grid weights
        detail_frame.columnconfigure(1, weight=1)
        
        # Save button
        ttk.Button(right_frame, text="Save Changes", command=self.save_med_changes).pack(pady=10)
    
    def build_supplies_subsection(self, parent):
        # Main frame
        main_frame = ttk.Frame(parent)
        main_frame.pack(fill='both', expand=True)
        
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
        columns = ('id', 'name', 'quantity', 'category', 'min_stock')
        self.sup_tree = ttk.Treeview(list_frame, columns=columns, show='headings')
        
        # Define headings
        self.sup_tree.heading('id', text='ID')
        self.sup_tree.heading('name', text='Supply Name')
        self.sup_tree.heading('quantity', text='Quantity')
        self.sup_tree.heading('category', text='Category')
        self.sup_tree.heading('min_stock', text='Min Stock Level')
        
        # Define columns
        self.sup_tree.column('id', width=50)
        self.sup_tree.column('name', width=150)
        self.sup_tree.column('quantity', width=80)
        self.sup_tree.column('category', width=100)
        self.sup_tree.column('min_stock', width=100)
        
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
        ttk.Button(button_frame, text="Export Data", command=self.export_sup_data).pack(side='right')
        
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
        
        ttk.Label(detail_frame, text="Supply Name:").grid(row=1, column=0, sticky='e', pady=2)
        self.sup_name = ttk.Entry(detail_frame)
        self.sup_name.grid(row=1, column=1, sticky='ew', pady=2, padx=(5, 0))
        
        ttk.Label(detail_frame, text="Quantity:").grid(row=2, column=0, sticky='e', pady=2)
        self.sup_quantity = ttk.Entry(detail_frame)
        self.sup_quantity.grid(row=2, column=1, sticky='ew', pady=2, padx=(5, 0))
        
        ttk.Label(detail_frame, text="Category:").grid(row=3, column=0, sticky='e', pady=2)
        self.sup_category = ttk.Combobox(detail_frame, values=['Medical', 'Hygiene', 'Administrative', 'Other'])
        self.sup_category.grid(row=3, column=1, sticky='ew', pady=2, padx=(5, 0))
        
        ttk.Label(detail_frame, text="Min Stock Level:").grid(row=4, column=0, sticky='e', pady=2)
        self.sup_min_stock = ttk.Entry(detail_frame)
        self.sup_min_stock.grid(row=4, column=1, sticky='ew', pady=2, padx=(5, 0))
        
        ttk.Label(detail_frame, text="Supplier:").grid(row=5, column=0, sticky='e', pady=2)
        self.sup_supplier = ttk.Entry(detail_frame)
        self.sup_supplier.grid(row=5, column=1, sticky='ew', pady=2, padx=(5, 0))
        
        ttk.Label(detail_frame, text="Notes:").grid(row=6, column=0, sticky='ne', pady=2)
        self.sup_notes = tk.Text(detail_frame, height=5, width=30)
        self.sup_notes.grid(row=6, column=1, sticky='ew', pady=2, padx=(5, 0))
        
        # Configure grid weights
        detail_frame.columnconfigure(1, weight=1)
        
        # Save button
        ttk.Button(right_frame, text="Save Changes", command=self.save_sup_changes).pack(pady=10)
    
    def build_about_section(self):
        about_text = f"""
MERU HOSPICE CLIENT AND MEDICATION MANAGEMENT SYSTEM

Version: 1.0
Developed for: Meru Hospice Care
Developer: GRIMSTRE LAB

Description:
This system manages client information, medication inventory, 
and medical supplies for Meru Hospice Care. It provides a 
comprehensive solution for tracking patient care, medication 
dispensing, and inventory management.

Features:
- Client registration and management
- Medication inventory tracking
- Supplies management
- Reporting and analytics
- Data export/import functionality

System Requirements:
- Python 3.6+
- Tkinter library
- JSON data storage

Release Date: {date.today()}

For support contact: support@grimstrelab.com
"""
        # Use a consistent background color instead of trying to get it from the frame
        about_label = tk.Text(self.about_frame, wrap='word', height=20, width=70, 
                             font=('Arial', 10), bg='white', relief='flat')
        about_label.insert('1.0', about_text)
        about_label.configure(state='disabled')
        about_label.pack(padx=20, pady=20, fill='both', expand=True)
    
    def load_data(self):
        # Try to load client data
        try:
            if os.path.exists('clients.json'):
                with open('clients.json', 'r') as f:
                    self.clients = json.load(f)
                for client in self.clients:
                    self.client_tree.insert('', 'end', values=(
                        client['id'], client['name'], client['dob'], 
                        client['phone'], client['status']
                    ))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load client data: {str(e)}")
            self.clients = []
        
        # Try to load medication data
        try:
            if os.path.exists('medications.json'):
                with open('medications.json', 'r') as f:
                    self.medications = json.load(f)
                for med in self.medications:
                    self.med_tree.insert('', 'end', values=(
                        med['id'], med['name'], med['quantity'], 
                        med['expiry'], med['client']
                    ))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load medication data: {str(e)}")
            self.medications = []
        
        # Try to load supplies data
        try:
            if os.path.exists('supplies.json'):
                with open('supplies.json', 'r') as f:
                    self.supplies = json.load(f)
                for supply in self.supplies:
                    self.sup_tree.insert('', 'end', values=(
                        supply['id'], supply['name'], supply['quantity'], 
                        supply['category'], supply['min_stock']
                    ))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load supplies data: {str(e)}")
            self.supplies = []
        
        # Update client combobox in medication section
        client_names = [client['name'] for client in self.clients]
        self.med_client['values'] = client_names
    
    def save_data(self):
        # Save client data
        try:
            with open('clients.json', 'w') as f:
                json.dump(self.clients, f, indent=4)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save client data: {str(e)}")
        
        # Save medication data
        try:
            with open('medications.json', 'w') as f:
                json.dump(self.medications, f, indent=4)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save medication data: {str(e)}")
        
        # Save supplies data
        try:
            with open('supplies.json', 'w') as f:
                json.dump(self.supplies, f, indent=4)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save supplies data: {str(e)}")
    
    def filter_clients(self, event):
        query = self.client_search.get().lower()
        
        # Clear treeview
        for item in self.client_tree.get_children():
            self.client_tree.delete(item)
        
        # Add filtered items
        for client in self.clients:
            if (query in client['name'].lower() or 
                query in client['id'].lower() or 
                query in client['phone'].lower() or
                query in client['status'].lower()):
                self.client_tree.insert('', 'end', values=(
                    client['id'], client['name'], client['dob'], 
                    client['phone'], client['status']
                ))
    
    def filter_medications(self, event):
        query = self.med_search.get().lower()
        
        # Clear treeview
        for item in self.med_tree.get_children():
            self.med_tree.delete(item)
        
        # Add filtered items
        for med in self.medications:
            if (query in med['name'].lower() or 
                query in med['id'].lower() or 
                query in med['client'].lower()):
                self.med_tree.insert('', 'end', values=(
                    med['id'], med['name'], med['quantity'], 
                    med['expiry'], med['client']
                ))
    
    def filter_supplies(self, event):
        query = self.sup_search.get().lower()
        
        # Clear treeview
        for item in self.sup_tree.get_children():
            self.sup_tree.delete(item)
        
        # Add filtered items
        for supply in self.supplies:
            if (query in supply['name'].lower() or 
                query in supply['id'].lower() or 
                query in supply['category'].lower()):
                self.sup_tree.insert('', 'end', values=(
                    supply['id'], supply['name'], supply['quantity'], 
                    supply['category'], supply['min_stock']
                ))
    
    def on_client_select(self, event):
        selected = self.client_tree.focus()
        if not selected:
            return
        
        values = self.client_tree.item(selected, 'values')
        if not values:
            return
        
        client_id = values[0]
        client = next((c for c in self.clients if c['id'] == client_id), None)
        
        if client:
            self.client_id.config(state='normal')
            self.client_id.delete(0, 'end')
            self.client_id.insert(0, client['id'])
            self.client_id.config(state='readonly')
            
            self.client_name.delete(0, 'end')
            self.client_name.insert(0, client['name'])
            
            self.client_dob.delete(0, 'end')
            self.client_dob.insert(0, client['dob'])
            
            self.client_phone.delete(0, 'end')
            self.client_phone.insert(0, client['phone'])
            
            self.client_address.delete(0, 'end')
            self.client_address.insert(0, client.get('address', ''))
            
            self.client_condition.delete(0, 'end')
            self.client_condition.insert(0, client.get('condition', ''))
            
            self.client_status.set(client['status'])
            
            self.client_notes.delete(1.0, 'end')
            self.client_notes.insert(1.0, client.get('notes', ''))
    
    def on_med_select(self, event):
        selected = self.med_tree.focus()
        if not selected:
            return
        
        values = self.med_tree.item(selected, 'values')
        if not values:
            return
        
        med_id = values[0]
        med = next((m for m in self.medications if m['id'] == med_id), None)
        
        if med:
            self.med_id.config(state='normal')
            self.med_id.delete(0, 'end')
            self.med_id.insert(0, med['id'])
            self.med_id.config(state='readonly')
            
            self.med_name.delete(0, 'end')
            self.med_name.insert(0, med['name'])
            
            self.med_quantity.delete(0, 'end')
            self.med_quantity.insert(0, med['quantity'])
            
            self.med_expiry.delete(0, 'end')
            self.med_expiry.insert(0, med['expiry'])
            
            self.med_client.set(med['client'])
            
            self.med_dosage.delete(0, 'end')
            self.med_dosage.insert(0, med.get('dosage', ''))
            
            self.med_instructions.delete(1.0, 'end')
            self.med_instructions.insert(1.0, med.get('instructions', ''))
    
    def on_sup_select(self, event):
        selected = self.sup_tree.focus()
        if not selected:
            return
        
        values = self.sup_tree.item(selected, 'values')
        if not values:
            return
        
        sup_id = values[0]
        supply = next((s for s in self.supplies if s['id'] == sup_id), None)
        
        if supply:
            self.sup_id.config(state='normal')
            self.sup_id.delete(0, 'end')
            self.sup_id.insert(0, supply['id'])
            self.sup_id.config(state='readonly')
            
            self.sup_name.delete(0, 'end')
            self.sup_name.insert(0, supply['name'])
            
            self.sup_quantity.delete(0, 'end')
            self.sup_quantity.insert(0, supply['quantity'])
            
            self.sup_category.set(supply['category'])
            
            self.sup_min_stock.delete(0, 'end')
            self.sup_min_stock.insert(0, supply.get('min_stock', ''))
            
            self.sup_supplier.delete(0, 'end')
            self.sup_supplier.insert(0, supply.get('supplier', ''))
            
            self.sup_notes.delete(1.0, 'end')
            self.sup_notes.insert(1.0, supply.get('notes', ''))
    
    def add_client(self):
        # Generate a new ID
        if self.clients:
            new_id = str(max(int(c['id']) for c in self.clients) + 1)
        else:
            new_id = "1"
        
        # Create a new client
        new_client = {
            'id': new_id,
            'name': 'New Client',
            'dob': '',
            'phone': '',
            'address': '',
            'condition': '',
            'status': 'Active',
            'notes': ''
        }
        
        self.clients.append(new_client)
        self.client_tree.insert('', 'end', values=(
            new_client['id'], new_client['name'], new_client['dob'], 
            new_client['phone'], new_client['status']
        ))
        
        # Select the new client
        for item in self.client_tree.get_children():
            if self.client_tree.item(item, 'values')[0] == new_id:
                self.client_tree.focus(item)
                self.client_tree.selection_set(item)
                self.on_client_select(None)
                break
        
        self.save_data()
    
    def edit_client(self):
        selected = self.client_tree.focus()
        if not selected:
            messagebox.showwarning("Warning", "Please select a client to edit.")
            return
        
        self.on_client_select(None)
    
    def delete_client(self):
        selected = self.client_tree.focus()
        if not selected:
            messagebox.showwarning("Warning", "Please select a client to delete.")
            return
        
        values = self.client_tree.item(selected, 'values')
        if not values:
            return
        
        client_id = values[0]
        
        # Confirm deletion
        if not messagebox.askyesno("Confirm", f"Are you sure you want to delete client {client_id}?"):
            return
        
        # Remove from list and treeview
        self.clients = [c for c in self.clients if c['id'] != client_id]
        self.client_tree.delete(selected)
        
        # Clear form
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
        
        self.save_data()
    
    def save_client_changes(self):
        selected = self.client_tree.focus()
        if not selected:
            messagebox.showwarning("Warning", "Please select a client to save changes.")
            return
        
        values = self.client_tree.item(selected, 'values')
        if not values:
            return
        
        client_id = values[0]
        client = next((c for c in self.clients if c['id'] == client_id), None)
        
        if client:
            client['name'] = self.client_name.get()
            client['dob'] = self.client_dob.get()
            client['phone'] = self.client_phone.get()
            client['address'] = self.client_address.get()
            client['condition'] = self.client_condition.get()
            client['status'] = self.client_status.get()
            client['notes'] = self.client_notes.get(1.0, 'end-1c')
            
            # Update treeview
            self.client_tree.item(selected, values=(
                client['id'], client['name'], client['dob'], 
                client['phone'], client['status']
            ))
            
            self.save_data()
            messagebox.showinfo("Success", "Client details saved successfully.")
    
    def add_medication(self):
        # Generate a new ID
        if self.medications:
            new_id = str(max(int(m['id']) for m in self.medications) + 1)
        else:
            new_id = "1"
        
        # Create a new medication
        new_med = {
            'id': new_id,
            'name': 'New Medication',
            'quantity': '0',
            'expiry': '',
            'client': '',
            'dosage': '',
            'instructions': ''
        }
        
        self.medications.append(new_med)
        self.med_tree.insert('', 'end', values=(
            new_med['id'], new_med['name'], new_med['quantity'], 
            new_med['expiry'], new_med['client']
        ))
        
        # Select the new medication
        for item in self.med_tree.get_children():
            if self.med_tree.item(item, 'values')[0] == new_id:
                self.med_tree.focus(item)
                self.med_tree.selection_set(item)
                self.on_med_select(None)
                break
        
        self.save_data()
    
    def edit_medication(self):
        selected = self.med_tree.focus()
        if not selected:
            messagebox.showwarning("Warning", "Please select a medication to edit.")
            return
        
        self.on_med_select(None)
    
    def delete_medication(self):
        selected = self.med_tree.focus()
        if not selected:
            messagebox.showwarning("Warning", "Please select a medication to delete.")
            return
        
        values = self.med_tree.item(selected, 'values')
        if not values:
            return
        
        med_id = values[0]
        
        # Confirm deletion
        if not messagebox.askyesno("Confirm", f"Are you sure you want to delete medication {med_id}?"):
            return
        
        # Remove from list and treeview
        self.medications = [m for m in self.medications if m['id'] != med_id]
        self.med_tree.delete(selected)
        
        # Clear form
        self.med_id.config(state='normal')
        self.med_id.delete(0, 'end')
        self.med_id.config(state='readonly')
        
        self.med_name.delete(0, 'end')
        self.med_quantity.delete(0, 'end')
        self.med_expiry.delete(0, 'end')
        self.med_client.set('')
        self.med_dosage.delete(0, 'end')
        self.med_instructions.delete(1.0, 'end')
        
        self.save_data()
    
    def save_med_changes(self):
        selected = self.med_tree.focus()
        if not selected:
            messagebox.showwarning("Warning", "Please select a medication to save changes.")
            return
        
        values = self.med_tree.item(selected, 'values')
        if not values:
            return
        
        med_id = values[0]
        med = next((m for m in self.medications if m['id'] == med_id), None)
        
        if med:
            med['name'] = self.med_name.get()
            med['quantity'] = self.med_quantity.get()
            med['expiry'] = self.med_expiry.get()
            med['client'] = self.med_client.get()
            med['dosage'] = self.med_dosage.get()
            med['instructions'] = self.med_instructions.get(1.0, 'end-1c')
            
            # Update treeview
            self.med_tree.item(selected, values=(
                med['id'], med['name'], med['quantity'], 
                med['expiry'], med['client']
            ))
            
            self.save_data()
            messagebox.showinfo("Success", "Medication details saved successfully.")
    
    def add_supply(self):
        # Generate a new ID
        if self.supplies:
            new_id = str(max(int(s['id']) for s in self.supplies) + 1)
        else:
            new_id = "1"
        
        # Create a new supply
        new_supply = {
            'id': new_id,
            'name': 'New Supply',
            'quantity': '0',
            'category': 'Medical',
            'min_stock': '5',
            'supplier': '',
            'notes': ''
        }
        
        self.supplies.append(new_supply)
        self.sup_tree.insert('', 'end', values=(
            new_supply['id'], new_supply['name'], new_supply['quantity'], 
            new_supply['category'], new_supply['min_stock']
        ))
        
        # Select the new supply
        for item in self.sup_tree.get_children():
            if self.sup_tree.item(item, 'values')[0] == new_id:
                self.sup_tree.focus(item)
                self.sup_tree.selection_set(item)
                self.on_sup_select(None)
                break
        
        self.save_data()
    
    def edit_supply(self):
        selected = self.sup_tree.focus()
        if not selected:
            messagebox.showwarning("Warning", "Please select a supply to edit.")
            return
        
        self.on_sup_select(None)
    
    def delete_supply(self):
        selected = self.sup_tree.focus()
        if not selected:
            messagebox.showwarning("Warning", "Please select a supply to delete.")
            return
        
        values = self.sup_tree.item(selected, 'values')
        if not values:
            return
        
        sup_id = values[0]
        
        # Confirm deletion
        if not messagebox.askyesno("Confirm", f"Are you sure you want to delete supply {sup_id}?"):
            return
        
        # Remove from list and treeview
        self.supplies = [s for s in self.supplies if s['id'] != sup_id]
        self.sup_tree.delete(selected)
        
        # Clear form
        self.sup_id.config(state='normal')
        self.sup_id.delete(0, 'end')
        self.sup_id.config(state='readonly')
        
        self.sup_name.delete(0, 'end')
        self.sup_quantity.delete(0, 'end')
        self.sup_category.set('')
        self.sup_min_stock.delete(0, 'end')
        self.sup_supplier.delete(0, 'end')
        self.sup_notes.delete(1.0, 'end')
        
        self.save_data()
    
    def save_sup_changes(self):
        selected = self.sup_tree.focus()
        if not selected:
            messagebox.showwarning("Warning", "Please select a supply to save changes.")
            return
        
        values = self.sup_tree.item(selected, 'values')
        if not values:
            return
        
        sup_id = values[0]
        supply = next((s for s in self.supplies if s['id'] == sup_id), None)
        
        if supply:
            supply['name'] = self.sup_name.get()
            supply['quantity'] = self.sup_quantity.get()
            supply['category'] = self.sup_category.get()
            supply['min_stock'] = self.sup_min_stock.get()
            supply['supplier'] = self.sup_supplier.get()
            supply['notes'] = self.sup_notes.get(1.0, 'end-1c')
            
            # Update treeview
            self.sup_tree.item(selected, values=(
                supply['id'], supply['name'], supply['quantity'], 
                supply['category'], supply['min_stock']
            ))
            
            self.save_data()
            messagebox.showinfo("Success", "Supply details saved successfully.")
    
    def export_client_data(self):
        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            title="Export Client Data"
        )
        
        if not filename:
            return
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                # Write header
                f.write("ID,Name,Date of Birth,Phone,Address,Medical Condition,Status,Notes\n")
                
                # Write data
                for client in self.clients:
                    # Handle notes field by escaping quotes
                    notes = client.get('notes', '').replace('"', '""')
                    f.write(f'"{client["id"]}","{client["name"]}","{client["dob"]}",'
                            f'"{client["phone"]}","{client.get("address", "")}",'
                            f'"{client.get("condition", "")}","{client["status"]}",'
                            f'"{notes}"\n')
            
            messagebox.showinfo("Success", f"Client data exported to {filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export data: {str(e)}")
    
    def export_med_data(self):
        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            title="Export Medication Data"
        )
        
        if not filename:
            return
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                # Write header
                f.write("ID,Name,Quantity,Expiry Date,Assigned Client,Dosage,Instructions\n")
                
                # Write data
                for med in self.medications:
                    # Handle instructions field by escaping quotes
                    instructions = med.get('instructions', '').replace('"', '""')
                    f.write(f'"{med["id"]}","{med["name"]}","{med["quantity"]}",'
                            f'"{med["expiry"]}","{med["client"]}","{med.get("dosage", "")}",'
                            f'"{instructions}"\n')
            
            messagebox.showinfo("Success", f"Medication data exported to {filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export data: {str(e)}")
    
    def export_sup_data(self):
        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            title="Export Supplies Data"
        )
        
        if not filename:
            return
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                # Write header
                f.write("ID,Name,Quantity,Category,Min Stock Level,Supplier,Notes\n")
                
                # Write data
                for supply in self.supplies:
                    # Handle notes field by escaping quotes
                    notes = supply.get('notes', '').replace('"', '""')
                    f.write(f'"{supply["id"]}","{supply["name"]}","{supply["quantity"]}",'
                            f'"{supply["category"]}","{supply.get("min_stock", "")}",'
                            f'"{supply.get("supplier", "")}","{notes}"\n')
            
            messagebox.showinfo("Success", f"Supplies data exported to {filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export data: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = MeruHospiceManager(root)
    root.mainloop()