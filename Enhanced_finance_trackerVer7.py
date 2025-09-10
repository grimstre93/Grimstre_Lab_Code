# -*- coding: utf-8 -*-
""" Created on Wed Aug  6 13:06:12 2025

@author: samng
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import csv
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from matplotlib.figure import Figure
from matplotlib import cm

class PersonalFinanceTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Enhanced Personal Finance Tracker with Graphs")
        self.root.geometry("1200x800")

        # Configure style
        self.style = ttk.Style()
        self.style.configure('TFrame', background='#f0f0f0')
        self.style.configure('TButton', font=('Times New Roman', 10), padding=5)
        self.style.configure('Title.TLabel', font=('Times New Roman', 14, 'bold'), background='#f0f0f0')
        self.style.configure('Subtitle.TLabel', font=('Times New Roman', 12), background='#f0f0f0')
        self.style.configure('Alert.TLabel', font=('Times New Roman', 10, 'bold'), foreground='red')

        # Constants
        self.MIN_UPKEEP = 5000
        self.MIN_SAVINGS = 18000
        self.LONG_TERM_SAVINGS = 15000
        self.SHORT_TERM_SAVINGS = 3000
        self.SAVINGS_TARGET = 4000000
        self.INVESTMENT_PERCENT = 10
        self.EMERGENCY_PERCENT = 10
        self.CONFIDENCE_LEVEL = 0.95

        # Food prices
        self.food_prices = {
            "maize": {"buy": 2500, "sell": 2200},
            "rice": {"buy": 6000, "sell": 5500},
            "beans": {"buy": 8000, "sell": 7500},
            "wheat": {"buy": 3500, "sell": 3200},
            "sorghum": {"buy": 2000, "sell": 1800}
        }

        # Initialize UI state variables after root is created
        self.food_price_vars = {}
        self.food_qty_vars = {}
        
        # Application state
        self.state = {
            "current_month": {},
            "history": [],
            "total_savings": 472000,
            "short_term_savings": 0,
            "food_inventory": {food: 0 for food in self.food_prices},
            "current_screen": "month_selector"
        }

        # Load data
        self.load_data()

        # Create menu bar
        self.create_menu_bar()

        # Create main container
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Create all screens
        self.create_month_selector_screen()
        self.create_income_screen()
        self.create_expenditure_screen()
        self.create_results_screen()
        self.create_history_screen()

        # Show initial screen
        self.show_screen("month_selector")

    def create_menu_bar(self):
        menubar = tk.Menu(self.root)

        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="New Month", command=lambda: self.show_screen("month_selector"))
        file_menu.add_command(label="Income", command=lambda: self.show_screen("income"))
        file_menu.add_command(label="Expenses", command=lambda: self.show_screen("expenditure"))
        file_menu.add_command(label="Results", command=lambda: self.show_screen("results"))
        file_menu.add_command(label="History", command=lambda: self.show_screen("history"))
        file_menu.add_separator()
        file_menu.add_command(label="Export to CSV", command=self.export_to_csv)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        menubar.add_cascade(label="File", menu=file_menu)

        # Tools menu
        tools_menu = tk.Menu(menubar, tearoff=0)
        tools_menu.add_command(label="Refresh Data", command=self.refresh_data)
        tools_menu.add_command(label="Clear All Data", command=self.clear_all_data)
        menubar.add_cascade(label="Tools", menu=tools_menu)

        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="Help", command=self.show_help)
        help_menu.add_command(label="About", command=self.show_about)
        menubar.add_cascade(label="Help", menu=help_menu)

        self.root.config(menu=menubar)

    def show_help(self):
        help_text = "For assistance, please contact:\n\n"
        help_text += "Email: samngacha@gmail.com\n"
        help_text += "Phone: +254742859291\n\n"
        help_text += "This software helps you track your personal finances, including income, expenses, and savings.\n"
        help_text += "Key Features:\n"
        help_text += "- Track monthly income and expenses\n"
        help_text += "- Manage food inventory and transactions\n"
        help_text += "- Visualize financial data with charts\n"
        help_text += "- Analyze budget variances\n"
        help_text += "- Track progress toward savings goals"
        messagebox.showinfo("Help", help_text)

    def show_about(self):
        about_text = "Personal Finance Tracker\n"
        about_text += "Version 3.0\n\n"
        about_text += "Developed by Sam Ngacha\n"
        about_text += "© 2023 All Rights Reserved"
        messagebox.showinfo("About", about_text)

    def load_data(self):
        try:
            with open('finance_data.json', 'r') as f:
                data = json.load(f)
                self.state["history"] = data.get("history", [])
                self.state["total_savings"] = data.get("total_savings", 442000)
                self.state["short_term_savings"] = data.get("short_term_savings", 0)
                self.state["food_inventory"] = data.get("food_inventory", {food: 0 for food in self.food_prices})
                # Update food prices if they exist in saved data
                saved_prices = data.get("food_prices", {})
                for food in saved_prices:
                    if food in self.food_prices:
                        self.food_prices[food] = saved_prices[food]
        except (FileNotFoundError, json.JSONDecodeError):
            pass

    def save_data(self):
        # Remove any StringVar references before saving
        food_prices_serializable = {}
        for food, prices in self.food_prices.items():
            food_prices_serializable[food] = {
                "buy": prices.get("buy", 0),
                "sell": prices.get("sell", 0)
            }
        data = {
            "history": self.state["history"],
            "total_savings": self.state["total_savings"],
            "short_term_savings": self.state["short_term_savings"],
            "food_inventory": self.state["food_inventory"],
            "food_prices": food_prices_serializable
        }
        with open('finance_data.json', 'w') as f:
            json.dump(data, f)

    def show_screen(self, screen_name):
        for screen in [self.month_selector_frame, self.income_frame,
                      self.expenditure_frame, self.results_frame, self.history_frame]:
            if hasattr(self, screen_name.split('.')[0] + '_frame'):
                screen.pack_forget()

        self.state["current_screen"] = screen_name

        if screen_name == "month_selector":
            self.update_month_selector_screen()
            self.month_selector_frame.pack(fill=tk.BOTH, expand=True)
        elif screen_name == "income":
            self.update_income_screen()
            self.income_frame.pack(fill=tk.BOTH, expand=True)
        elif screen_name == "expenditure":
            self.update_expenditure_screen()
            self.expenditure_frame.pack(fill=tk.BOTH, expand=True)
        elif screen_name == "results":
            self.update_results_screen()
            self.results_frame.pack(fill=tk.BOTH, expand=True)
        elif screen_name == "history":
            self.update_history_screen()
            self.history_frame.pack(fill=tk.BOTH, expand=True)

    def create_month_selector_screen(self):
        self.month_selector_frame = ttk.Frame(self.main_frame)

        # Title
        title_label = ttk.Label(self.month_selector_frame, text="Select Month", style='Title.TLabel')
        title_label.pack(pady=10)

        # Month selection
        month_frame = ttk.Frame(self.month_selector_frame)
        month_frame.pack(pady=5)
        ttk.Label(month_frame, text="Month:").pack(side=tk.LEFT)
        self.month_entry = ttk.Entry(month_frame)
        self.month_entry.pack(side=tk.LEFT, padx=5)
        now = datetime.now()
        current_month = f"{now.year}-{now.month:02d}"
        self.month_entry.insert(0, current_month)

        # Action selection
        action_frame = ttk.Frame(self.month_selector_frame)
        action_frame.pack(pady=5)
        ttk.Label(action_frame, text="Action:").pack(anchor=tk.N)
        self.month_action = tk.StringVar(value="new")
        ttk.Radiobutton(action_frame, text="Create New Month", variable=self.month_action, value="new").pack(anchor=tk.N)
        self.view_radio = ttk.Radiobutton(action_frame, text="View Existing Month", variable=self.month_action, value="view")
        self.view_radio.pack(anchor=tk.N)

        # Recent months with loan status
        recent_label = ttk.Label(self.month_selector_frame, text="Recent Months (with Loan Status)")
        recent_label.pack(pady=5)
        self.recent_months_frame = ttk.Frame(self.month_selector_frame)
        self.recent_months_frame.pack(fill=tk.X, pady=5)

        # Contact information (always visible)
        contact_frame = ttk.Frame(self.month_selector_frame, relief=tk.RIDGE, borderwidth=2)
        contact_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=10)
        ttk.Label(contact_frame, text="Contact Support: samngacha@gmail.com | +254742859291", style='Subtitle.TLabel').pack()

        # Navigation buttons
        button_frame = ttk.Frame(self.month_selector_frame)
        button_frame.pack(pady=10)
        ttk.Button(button_frame, text="Refresh", command=self.refresh_data).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Clear All Data", command=self.clear_all_data).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Continue", command=self.process_month_selection).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Exit", command=self.root.quit).pack(side=tk.LEFT, padx=5)

    def update_month_selector_screen(self):
        for widget in self.recent_months_frame.winfo_children():
            widget.destroy()

        # Show last 10 months with loan status
        sorted_months = sorted([item for item in self.state["history"]], key=lambda x: x["month"], reverse=True)
        if not sorted_months:
            ttk.Label(self.recent_months_frame, text="No historical data available").pack()
            return

        # Create a treeview for better display
        columns = ("month", "income", "expenses", "savings", "loan_status")
        tree = ttk.Treeview(self.recent_months_frame, columns=columns, show="headings", height=min(10, len(sorted_months)))

        # Define headings
        tree.heading("month", text="Month")
        tree.heading("income", text="Income (KES)")
        tree.heading("expenses", text="Expenses (KES)")
        tree.heading("savings", text="Savings (KES)")
        tree.heading("loan_status", text="Loan Status")

        # Define columns
        tree.column("month", width=100)
        tree.column("income", width=120, anchor=tk.E)
        tree.column("expenses", width=120, anchor=tk.E)
        tree.column("savings", width=120, anchor=tk.E)
        tree.column("loan_status", width=150)

        # Add data
        for month_data in sorted_months:
            expenses = (
                sum(month_data.get("expenditures", {}).values()) +
                sum(item["cost"] for item in month_data.get("food_purchases", [])) -
                sum(item["income"] for item in month_data.get("food_sales", []))
            )
            loan_status = "Yes (KES {:.2f})".format(month_data.get("loan", {}).get("total", 0)) if month_data.get("loan", {}).get("needed", False) else "No"
            tree.insert("", tk.END, values=(
                month_data["month"],
                "{:.2f}".format(month_data.get("income", 0)),
                "{:.2f}".format(expenses),
                "{:.2f}".format(month_data.get("savings", {}).get("total", 0)),
                loan_status
            ))
        tree.pack(fill=tk.BOTH, expand=True)

        # Add button to view selected month
        def view_selected_month():
            selected_item = tree.focus()
            if selected_item:
                month_data = tree.item(selected_item)["values"][0]
                self.load_month(month_data)

        view_btn = tk.Button(self.recent_months_frame, text="View Selected Month", command=view_selected_month)
        view_btn.pack(pady=5)

        self.view_radio['state'] = 'disabled' if not self.state["history"] else 'normal'

    def load_month(self, month):
        month_data = next((item for item in self.state["history"] if item["month"] == month), None)
        if month_data:
            self.state["current_month"] = month_data.copy()
            self.show_screen("results")
        else:
            messagebox.showerror("Error", f"No data found for month {month}")

    def process_month_selection(self):
        month = self.month_entry.get()
        if not month:
            messagebox.showerror("Error", "Please select a month")
            return

        action = self.month_action.get()
        if action == "new":
            self.state["current_month"] = {
                "month": month,
                "income": 0,
                "savings_reserve": 0,
                "available_budget": 0,
                "expenditures": {
                    "upkeep": 0,
                    "transport": 0,
                    "utilities": 0,
                    "entertainment": 0,
                    "rent": 0
                },
                "food_purchases": [],
                "food_sales": [],
                "investments": 0,
                "emergency_fund": 0,
                "loan": {"needed": False},
                "savings": {
                    "long_term": 0,
                    "short_term": 0,
                    "total": 0
                },
                "budget_analysis": {
                    "planned": {},
                    "actual": {},
                    "variance": {},
                    "variance_amounts": {},
                    "significant": False,
                    "statistical_analysis": {}
                }
            }
            self.show_screen("income")
        else:
            self.load_month(month)

    def create_income_screen(self):
        self.income_frame = ttk.Frame(self.main_frame)

        # Title
        title_label = ttk.Label(self.income_frame, text="Enter Income", style='Title.TLabel')
        title_label.pack(pady=10)

        # Income entry
        income_frame = ttk.Frame(self.income_frame)
        income_frame.pack(pady=5)
        ttk.Label(income_frame, text="Income (KES):").pack(side=tk.LEFT)
        self.income_entry = ttk.Entry(income_frame)
        self.income_entry.pack(side=tk.LEFT, padx=5)

        # Note
        note_label = ttk.Label(self.income_frame,
                            text="Note: Minimum of 18,000 KES will be reserved for savings (15,000 long-term + 3,000 short-term)")
        note_label.pack(pady=5)

        # Projected loan information (if available from previous months)
        loan_frame = ttk.Frame(self.income_frame, relief=tk.GROOVE, borderwidth=2)
        loan_frame.pack(pady=10, fill=tk.X, padx=10)

        # Get average expenses from last 3 months
        if len(self.state["history"]) >= 1:
            last_months = sorted(self.state["history"], key=lambda x: x["month"], reverse=True)[:3]
            avg_expenses = sum(
                sum(month.get("expenditures", {}).values()) +
                sum(item["cost"] for item in month.get("food_purchases", [])) -
                sum(item["income"] for item in month.get("food_sales", []))
                for month in last_months
            ) / len(last_months)

            loan_text = "Based on your last {} months, average expenses: KES {:,.2f}\n".format(len(last_months), avg_expenses)
            loan_text += "With this income, you might need a loan of approximately KES {:,.2f}".format(
                max(avg_expenses - float(self.income_entry.get()) if self.income_entry.get() else 0, 0)
            )
            ttk.Label(loan_frame, text="Projected Loan Information", style='Subtitle.TLabel').pack()
            ttk.Label(loan_frame, text=loan_text).pack()
        else:
            ttk.Label(loan_frame, text="No enough data for loan projection (need at least 1 previous month)").pack()

        # Navigation buttons
        button_frame = ttk.Frame(self.income_frame)
        button_frame.pack(pady=10)
        ttk.Button(button_frame, text="Refresh", command=self.refresh_data).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Clear All Data", command=self.clear_all_data).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Calculate", command=self.process_income).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Back", command=lambda: self.show_screen("month_selector")).pack(side=tk.LEFT, padx=5)

    def update_income_screen(self):
        self.income_entry.delete(0, tk.END)
        if "income" in self.state["current_month"]:
            self.income_entry.insert(0, str(self.state["current_month"]["income"]))

    def process_income(self):
        try:
            income = float(self.income_entry.get())
            if income < 0:
                messagebox.showerror("Error", "Income cannot be negative")
                return
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid income amount")
            return

        self.state["current_month"]["income"] = income
        self.state["current_month"]["savings_reserve"] = max(income * 0.3, self.MIN_SAVINGS)
        self.state["current_month"]["investments"] = income * (self.INVESTMENT_PERCENT / 100)
        self.state["current_month"]["emergency_fund"] = income * (self.EMERGENCY_PERCENT / 100)
        self.state["current_month"]["available_budget"] = income - (
            self.state["current_month"]["savings_reserve"] +
            self.state["current_month"]["investments"] +
            self.state["current_month"]["emergency_fund"]
        )
        self.show_screen("expenditure")

    def create_expenditure_screen(self):
        self.expenditure_frame = ttk.Frame(self.main_frame)

        # Notebook for tabs
        self.expenditure_notebook = ttk.Notebook(self.expenditure_frame)
        self.expenditure_notebook.pack(fill=tk.BOTH, expand=True)

        # Budget Information Tab
        self.budget_info_tab = ttk.Frame(self.expenditure_notebook)
        self.expenditure_notebook.add(self.budget_info_tab, text="Budget Information")
        self.budget_info_text = tk.Text(self.budget_info_tab, wrap=tk.WORD, height=10)
        self.budget_info_text.pack(fill=tk.BOTH, expand=True)

        # Regular Expenses Tab
        self.regular_expenses_tab = ttk.Frame(self.expenditure_notebook)
        self.expenditure_notebook.add(self.regular_expenses_tab, text="Regular Expenditures")

        ttk.Label(self.regular_expenses_tab, text="Upkeep (KES):").pack(anchor=tk.W)
        self.upkeep_entry = ttk.Entry(self.regular_expenses_tab)
        self.upkeep_entry.pack(fill=tk.X, padx=5, pady=2)
        ttk.Label(self.regular_expenses_tab, text=f"Minimum: {self.MIN_UPKEEP} KES").pack(anchor=tk.W)

        ttk.Label(self.regular_expenses_tab, text="Transport (KES):").pack(anchor=tk.W)
        self.transport_entry = ttk.Entry(self.regular_expenses_tab)
        self.transport_entry.pack(fill=tk.X, padx=5, pady=2)

        ttk.Label(self.regular_expenses_tab, text="Utilities (KES):").pack(anchor=tk.W)
        self.utilities_entry = ttk.Entry(self.regular_expenses_tab)
        self.utilities_entry.pack(fill=tk.X, padx=5, pady=2)

        ttk.Label(self.regular_expenses_tab, text="Entertainment (KES):").pack(anchor=tk.W)
        self.entertainment_entry = ttk.Entry(self.regular_expenses_tab)
        self.entertainment_entry.pack(fill=tk.X, padx=5, pady=2)

        ttk.Label(self.regular_expenses_tab, text="Rent (KES):").pack(anchor=tk.W)
        self.rent_entry = ttk.Entry(self.regular_expenses_tab)
        self.rent_entry.pack(fill=tk.X, padx=5, pady=2)

        # Food Stock Management Tab
        self.food_stock_tab = ttk.Frame(self.expenditure_notebook)
        self.expenditure_notebook.add(self.food_stock_tab, text="Food Stock Management")

        self.inventory_text = tk.Text(self.food_stock_tab, wrap=tk.WORD, height=5)
        self.inventory_text.pack(fill=tk.X, pady=5)

        ttk.Label(self.food_stock_tab, text="Food Price Configuration", font=('Arial', 10, 'bold')).pack()
        self.food_prices_frame = ttk.Frame(self.food_stock_tab)
        self.food_prices_frame.pack(fill=tk.X, pady=5)

        ttk.Label(self.food_stock_tab, text="Food Transactions", font=('Arial', 10, 'bold')).pack()
        ttk.Label(self.food_stock_tab, text="Note: Positive numbers for purchase, negative for sale").pack()

        self.food_transactions_frame = ttk.Frame(self.food_stock_tab)
        self.food_transactions_frame.pack(fill=tk.X, pady=5)

        # Loan projection information
        self.loan_projection_frame = ttk.Frame(self.expenditure_frame, relief=tk.GROOVE, borderwidth=2)
        self.loan_projection_frame.pack(fill=tk.X, padx=10, pady=5)
        self.loan_projection_label = ttk.Label(self.loan_projection_frame, text="Loan Projection: ")
        self.loan_projection_label.pack()

        # Navigation buttons
        button_frame = ttk.Frame(self.expenditure_frame)
        button_frame.pack(pady=10)
        ttk.Button(button_frame, text="Refresh", command=self.refresh_data).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Clear All Data", command=self.clear_all_data).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Calculate Budget", command=self.process_expenditure).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Back", command=lambda: self.show_screen("income")).pack(side=tk.LEFT, padx=5)

    def update_expenditure_screen(self):
        budget_info = (
            f"Available Budget: {self.state['current_month'].get('available_budget', 0):.2f} KES\n"
            f"Savings Reserve: {self.state['current_month'].get('savings_reserve', 0):.2f} KES (15,000 long-term + 3,000 short-term)\n"
            f"Investments: {self.state['current_month'].get('investments', 0):.2f} KES\n"
            f"Emergency Fund: {self.state['current_month'].get('emergency_fund', 0):.2f} KES\n"
            f"Note: Minimum upkeep requirement is {self.MIN_UPKEEP:.2f} KES"
        )
        self.budget_info_text.delete(1.0, tk.END)
        self.budget_info_text.insert(tk.END, budget_info)

        # Get upkeep value or use minimum if not set
        upkeep_value = self.state["current_month"].get("expenditures", {}).get("upkeep", self.MIN_UPKEEP)
        self.upkeep_entry.delete(0, tk.END)
        self.upkeep_entry.insert(0, str(upkeep_value))

        self.transport_entry.delete(0, tk.END)
        self.transport_entry.insert(0, str(self.state["current_month"].get("expenditures", {}).get("transport", 0)))

        self.utilities_entry.delete(0, tk.END)
        self.utilities_entry.insert(0, str(self.state["current_month"].get("expenditures", {}).get("utilities", 0)))

        self.entertainment_entry.delete(0, tk.END)
        self.entertainment_entry.insert(0, str(self.state["current_month"].get("expenditures", {}).get("entertainment", 0)))

        self.rent_entry.delete(0, tk.END)
        self.rent_entry.insert(0, str(self.state["current_month"].get("expenditures", {}).get("rent", 0)))

        inventory_text = "Current Inventory:\n"
        for food, quantity in self.state["food_inventory"].items():
            inventory_text += f"{self.capitalize(food)}: {quantity} bags\n"
        self.inventory_text.delete(1.0, tk.END)
        self.inventory_text.insert(tk.END, inventory_text)

        # Clear previous widgets
        for widget in self.food_prices_frame.winfo_children():
            widget.destroy()

        ttk.Label(self.food_prices_frame, text="Food", width=15).grid(row=0, column=0)
        ttk.Label(self.food_prices_frame, text="Buy Price").grid(row=0, column=1)
        ttk.Label(self.food_prices_frame, text="Sell Price").grid(row=0, column=2)

        # Initialize food_price variables if they don't exist
        for i, food in enumerate(self.food_prices, 1):
            ttk.Label(self.food_prices_frame, text=self.capitalize(food)).grid(row=i, column=0)

            # Create StringVar if it doesn't exist
            if food not in self.food_price_vars:
                self.food_price_vars[food] = {
                    "buy_var": tk.StringVar(value=str(self.food_prices[food]['buy'])),
                    "sell_var": tk.StringVar(value=str(self.food_prices[food]['sell']))
                }

            ttk.Entry(self.food_prices_frame, textvariable=self.food_price_vars[food]["buy_var"]).grid(row=i, column=1)
            ttk.Entry(self.food_prices_frame, textvariable=self.food_price_vars[food]["sell_var"]).grid(row=i, column=2)

        for widget in self.food_transactions_frame.winfo_children():
            widget.destroy()

        ttk.Label(self.food_transactions_frame, text="Food", width=15).grid(row=0, column=0)
        ttk.Label(self.food_transactions_frame, text="Quantity (bags)").grid(row=0, column=1)

        # Initialize food quantity variables if they don't exist
        for i, food in enumerate(self.food_prices, 1):
            ttk.Label(self.food_transactions_frame, text=self.capitalize(food)).grid(row=i, column=0)
            # Create StringVar if it doesn't exist
            if food not in self.food_qty_vars:
                self.food_qty_vars[food] = tk.StringVar(value="0")

            ttk.Entry(self.food_transactions_frame, textvariable=self.food_qty_vars[food]).grid(row=i, column=1)

        # Update loan projection
        try:
            upkeep = float(self.upkeep_entry.get()) if self.upkeep_entry.get() else self.MIN_UPKEEP
            transport = float(self.transport_entry.get()) if self.transport_entry.get() else 0
            utilities = float(self.utilities_entry.get()) if self.utilities_entry.get() else 0
            entertainment = float(self.entertainment_entry.get()) if self.entertainment_entry.get() else 0
            rent = float(self.rent_entry.get()) if self.rent_entry.get() else 0

            total_expenses = upkeep + transport + utilities + entertainment + rent
            projected_loan = max(total_expenses - self.state["current_month"].get("available_budget", 0), 0)

            if projected_loan > 0:
                interest_rate = 0.2 if projected_loan <= 49999 else 0.12
                total_loan = projected_loan * (1 + interest_rate)
                self.loan_projection_label.config(
                    text=f"Loan Projection: Based on current entries, you may need a loan of KES {projected_loan:.2f}\n"
                         f"(Total repayment: KES {total_loan:.2f} at {interest_rate*100:.0f}% interest)",
                    style='Alert.TLabel'
                )
            else:
                self.loan_projection_label.config(
                    text="Loan Projection: Based on current entries, you should not need a loan",
                    style='Subtitle.TLabel'
                )
        except ValueError:
            self.loan_projection_label.config(
                text="Loan Projection: Enter valid amounts to calculate loan projection",
                style='Alert.TLabel'
            )

    def process_expenditure(self):
        for food in self.food_prices:
            try:
                self.food_prices[food]["buy"] = float(self.food_price_vars[food]["buy_var"].get())
                self.food_prices[food]["sell"] = float(self.food_price_vars[food]["sell_var"].get())
            except ValueError:
                messagebox.showerror("Error", f"Please enter valid prices for {food}")
                return

        try:
            # Ensure upkeep is at least MIN_UPKEEP
            upkeep = float(self.upkeep_entry.get())
            self.state["current_month"]["expenditures"]["upkeep"] = upkeep if upkeep >= self.MIN_UPKEEP else self.MIN_UPKEEP
            self.state["current_month"]["expenditures"]["transport"] = max(float(self.transport_entry.get()), 0)
            self.state["current_month"]["expenditures"]["utilities"] = max(float(self.utilities_entry.get()), 0)
            self.state["current_month"]["expenditures"]["entertainment"] = max(float(self.entertainment_entry.get()), 0)
            self.state["current_month"]["expenditures"]["rent"] = max(float(self.rent_entry.get()), 0)
        except ValueError:
            messagebox.showerror("Error", "Please enter valid amounts for all expenditures")
            return

        food_purchases = []
        food_sales = []
        food_net_cost = 0

        for food in self.food_prices:
            try:
                qty = float(self.food_qty_vars[food].get())
            except ValueError:
                messagebox.showerror("Error", f"Please enter a valid quantity for {food}")
                return

            if qty > 0:
                cost = qty * self.food_prices[food]["buy"]
                food_purchases.append({"food": food, "bags": qty, "cost": cost})
                food_net_cost += cost
                self.state["food_inventory"][food] = self.state["food_inventory"].get(food, 0) + qty
            elif qty < 0:
                bags_sold = abs(qty)
                if bags_sold > self.state["food_inventory"].get(food, 0):
                    messagebox.showerror("Error", f"Cannot sell more {food} than in inventory")
                    return
                income = bags_sold * self.food_prices[food]["sell"]
                food_sales.append({"food": food, "bags": bags_sold, "income": income})
                food_net_cost -= income
                self.state["food_inventory"][food] = self.state["food_inventory"].get(food, 0) - bags_sold

        self.state["current_month"]["food_purchases"] = food_purchases
        self.state["current_month"]["food_sales"] = food_sales

        total_exp = (
            sum(self.state["current_month"]["expenditures"].values()) +
            food_net_cost
        )

        loan_amount = max(total_exp - self.state["current_month"]['available_budget'], 0)
        if loan_amount > 0:
            loan_interest = loan_amount * (0.2 if loan_amount <= 49999 else 0.12)
            total_loan = loan_amount + loan_interest
            self.state["current_month"]['loan'] = {
                "amount": loan_amount,
                "interest": loan_interest,
                "total": total_loan,
                "needed": True
            }
        else:
            self.state["current_month"]['loan'] = {"needed": False}

        additional_savings = max(self.state["current_month"]['available_budget'] - total_exp, 0)
        self.state["current_month"]['savings'] = {
            "long_term": self.LONG_TERM_SAVINGS,
            "short_term": self.SHORT_TERM_SAVINGS + additional_savings,
            "total": self.LONG_TERM_SAVINGS + self.SHORT_TERM_SAVINGS + additional_savings
        }

        self.state["total_savings"] += self.LONG_TERM_SAVINGS
        self.state["short_term_savings"] += self.SHORT_TERM_SAVINGS + additional_savings

        self.perform_budget_analysis()

        existing_index = next((i for i, item in enumerate(self.state["history"]) if item["month"] == self.state["current_month"]["month"]), None)
        if existing_index is not None:
            self.state["history"][existing_index] = self.state["current_month"].copy()
        else:
            self.state["history"].append(self.state["current_month"].copy())

        self.save_data()
        self.show_screen("results")

    def perform_budget_analysis(self):
        planned = {
            "essentials": self.state["current_month"]["income"] * 0.5,
            "savings": self.state["current_month"]["savings_reserve"],
            "investments": self.state["current_month"]["investments"],
            "discretionary": self.state["current_month"]["income"] * 0.1
        }

        actual = {
            "essentials": (
                self.state["current_month"]["expenditures"]["upkeep"] +
                self.state["current_month"]["expenditures"]["rent"] +
                sum(item["cost"] for item in self.state["current_month"].get("food_purchases", []))
            ),
            "savings": self.state["current_month"]["savings"]["total"],
            "investments": self.state["current_month"]["investments"],
            "discretionary": (
                self.state["current_month"]["expenditures"]["transport"] +
                self.state["current_month"]["expenditures"]["utilities"] +
                self.state["current_month"]["expenditures"]["entertainment"]
            )
        }

        variance = {}
        variance_amounts = {}
        for category in planned:
            variance_amounts[category] = actual[category] - planned[category]
            if planned[category] > 0:
                variance[category] = (variance_amounts[category] / planned[category]) * 100
            else:
                variance[category] = 0

        self.state["current_month"]["budget_analysis"] = {
            "planned": planned,
            "actual": actual,
            "variance": variance,
            "variance_amounts": variance_amounts,
            "significant": any(abs(v) > 10 for v in variance.values()),
            "statistical_analysis": {
                "message": "Basic analysis completed"
            }
        }

    def create_results_screen(self):
        self.results_frame = ttk.Frame(self.main_frame)

        # Notebook for tabs
        self.results_notebook = ttk.Notebook(self.results_frame)
        self.results_notebook.pack(fill=tk.BOTH, expand=True)

        # Summary Tab
        self.summary_tab = ttk.Frame(self.results_notebook)
        self.results_notebook.add(self.summary_tab, text="Summary")

        summary_container = ttk.Frame(self.summary_tab)
        summary_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.summary_text = tk.Text(summary_container, wrap=tk.WORD)
        self.summary_text.pack(fill=tk.BOTH, expand=True)

        # Budget Analysis Tab
        self.budget_analysis_tab = ttk.Frame(self.results_notebook)
        self.results_notebook.add(self.budget_analysis_tab, text="Budget Analysis")
        analysis_container = ttk.Frame(self.budget_analysis_tab)
        analysis_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.budget_analysis_text = tk.Text(analysis_container, wrap=tk.WORD)
        self.budget_analysis_text.pack(fill=tk.BOTH, expand=True)

        # Graphs Tab
        self.graphs_tab = ttk.Frame(self.results_notebook)
        self.results_notebook.add(self.graphs_tab, text="Visualizations")
        self.create_graphs_tab()

        # Loan repayment schedule tab (new)
        self.loan_tab = ttk.Frame(self.results_notebook)
        self.results_notebook.add(self.loan_tab, text="Loan Details")
        self.create_loan_tab()

        # Common buttons for all tabs
        button_frame = ttk.Frame(self.results_frame)
        button_frame.pack(pady=10, fill=tk.X)
        ttk.Button(button_frame, text="Refresh", command=self.refresh_data).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="View History", command=lambda: self.show_screen("history")).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Track New Month", command=lambda: self.show_screen("month_selector")).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Back", command=lambda: self.show_screen("expenditure")).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Export to CSV", command=self.export_to_csv).pack(side=tk.LEFT, padx=5)

    def create_loan_tab(self):
        # Clean previous widgets
        for widget in self.loan_tab.winfo_children():
            widget.destroy()

        # Create text widget for loan details
        self.loan_text = tk.Text(self.loan_tab, wrap=tk.WORD)
        self.loan_text.pack(fill=tk.BOTH, expand=True)

        # Add contact information
        contact_frame = ttk.Frame(self.loan_tab, relief=tk.RIDGE, borderwidth=2)
        contact_frame.pack(fill=tk.X, pady=5)
        ttk.Label(contact_frame, text="For loan assistance, contact: samngacha@gmail.com | +254742859291").pack()

    def update_loan_tab(self):
        self.loan_text.delete(1.0, tk.END)
        if self.state["current_month"].get("loan", {}).get("needed", False):
            loan = self.state["current_month"]["loan"]
            loan_text = "=== LOAN DETAILS ===\n\n"
            loan_text += f"Loan Amount: {loan['amount']:.2f} KES\n"
            loan_text += f"Interest Rate: {15 if loan['amount'] <= 49999 else 10}%\n"
            loan_text += f"Interest Amount: {loan['interest']:.2f} KES\n"
            loan_text += f"Total Repayment: {loan['total']:.2f} KES\n\n"
            loan_text += "=== REPAYMENT SCHEDULE ===\n\n"
            loan_text += "You can repay this loan in installments:\n"

            # 3-month repayment option
            monthly_3 = loan['total'] / 3
            loan_text += f"1. 3 months: {monthly_3:.2f} KES per month\n"

            # 6-month repayment option
            monthly_6 = loan['total'] / 6
            loan_text += f"2. 6 months: {monthly_6:.2f} KES per month\n"

            # 12-month repayment option
            monthly_12 = loan['total'] / 12
            loan_text += f"3. 12 months: {monthly_12:.2f} KES per month\n\n"

            loan_text += "Note: Early repayment will reduce total interest paid."
        else:
            loan_text = "No loan needed for this month.\n\n"
            loan_text += "Your expenses are within your available budget."

        self.loan_text.insert(tk.END, loan_text)

    def create_graphs_tab(self):
        # Clear previous graphs if they exist
        for widget in self.graphs_tab.winfo_children():
            widget.destroy()

        # Create a frame for the graphs
        graph_frame = ttk.Frame(self.graphs_tab)
        graph_frame.pack(fill=tk.BOTH, expand=True)

        # Create a figure with subplots
        fig = Figure(figsize=(12, 10), dpi=100)
        gs = fig.add_gridspec(3, 2, hspace=0.5, wspace=0.3)
        ax1 = fig.add_subplot(gs[0, 0]) # Budget Allocation
        ax2 = fig.add_subplot(gs[0, 1]) # Expense Breakdown
        ax3 = fig.add_subplot(gs[1, 0]) # Savings Progress
        ax4 = fig.add_subplot(gs[1, 1]) # Budget Variance
        ax5 = fig.add_subplot(gs[2, :]) # Historical Trends

        # Set figure background color
        fig.patch.set_facecolor('#f0f0f0')

        # Plot 1: Budget Allocation Sunburst Chart
        if "income" in self.state["current_month"]:
            income = self.state["current_month"]['income']
            categories = {
                'Savings': self.state["current_month"]['savings_reserve'],
                'Investments': self.state["current_month"]['investments'],
                'Emergency Fund': self.state["current_month"]['emergency_fund'],
                'Expenses': sum(self.state["current_month"]['expenditures'].values()) +
                            sum(item["cost"] for item in self.state["current_month"].get("food_purchases", [])) -
                            sum(item["income"] for item in self.state["current_month"].get("food_sales", [])),
                'Loan': self.state["current_month"].get("loan", {}).get("total", 0)
            }

            # Remove zero values and sort by amount
            categories = {k: v for k, v in sorted(categories.items(), key=lambda item: item[1], reverse=True) if v > 0}

            if categories:
                # Create sunburst chart
                sizes = list(categories.values())
                labels = [f"{k}\n{v:.0f} KES" for k, v in categories.items()]
                colors = plt.cm.Pastel1(np.linspace(0, 1, len(categories)))

                wedges, texts = ax1.pie(sizes, labels=labels, colors=colors, startangle=90, wedgeprops=dict(width=0.5))

                for w in wedges:
                    w.set_linewidth(1)
                    w.set_edgecolor('gray')

                ax1.set_title('Budget Allocation (Sunburst Chart)', pad=20)
                ax1.axis('equal')

        # Plot 2: Expense Breakdown Horizontal Bar Chart
        if "expenditures" in self.state["current_month"]:
            expenses = self.state["current_month"]['expenditures']
            food_expense = sum(item["cost"] for item in self.state["current_month"].get("food_purchases", [])) - \
                          sum(item["income"] for item in self.state["current_month"].get("food_sales", []))
            loan_expense = self.state["current_month"].get("loan", {}).get("total", 0)
            expense_categories = {
                'Upkeep': expenses.get("upkeep", 0),
                'Transport': expenses.get("transport", 0),
                'Utilities': expenses.get("utilities", 0),
                'Entertainment': expenses.get("entertainment", 0),
                'Rent': expenses.get("rent", 0),
                'Food': food_expense,
                'Loan': loan_expense
            }

            # Remove zero values and sort by amount
            expense_categories = {k: v for k, v in sorted(expense_categories.items(), key=lambda item: item[1], reverse=True) if v > 0}

            if expense_categories:
                y_pos = np.arange(len(expense_categories))
                colors = plt.cm.viridis(np.linspace(0.2, 0.8, len(expense_categories)))

                bars = ax2.barh(y_pos, list(expense_categories.values()), color=colors)
                ax2.set_yticks(y_pos)
                ax2.set_yticklabels(list(expense_categories.keys()))
                ax2.set_title('Expense Breakdown (KES)')
                ax2.grid(axis='x', linestyle='--', alpha=0.7)

                # Add value labels
                for bar in bars:
                    width = bar.get_width()
                    ax2.text(width + max(expense_categories.values())*0.02, bar.get_y() + bar.get_height()/2,
                            f"{width:.0f}", ha='left', va='center')

        # Plot 3: Savings Progress Gauge Chart
        progress = (self.state["total_savings"] / self.SAVINGS_TARGET) * 100
        remaining = max(self.SAVINGS_TARGET - self.state["total_savings"], 0)

        # Create gauge chart
        ax3.set_title(f'Savings Progress ({progress:.1f}%)', pad=20)

        # Draw the filled part
        filled_angle = 180 * (progress / 100)
        ax3.pie([progress, 100-progress], startangle=90, counterclock=False,
                colors=['#4CAF50', '#E0E0E0'], wedgeprops=dict(width=0.3),
                radius=1.3, center=(0, 0))

        # Add center text
        ax3.text(0, 0, f"{progress:.1f}%\n{self.state['total_savings']:,.0f} KES",
                ha='center', va='center', fontsize=12)

        # Add target text
        ax3.text(0, -1.5, f"Target: {self.SAVINGS_TARGET:,.0f} KES",
                ha='center', va='center', fontsize=10)

        ax3.axis('equal')
        ax3.set_xlim(-1.5, 1.5)
        ax3.set_ylim(-1.5, 1.5)

        # Plot 4: Budget Variance Bar Chart
        if "budget_analysis" in self.state["current_month"]:
            analysis = self.state["current_month"]["budget_analysis"]
            categories = list(analysis["planned"].keys())
            planned = [analysis["planned"][cat] for cat in categories]
            actual = [analysis["actual"].get(cat, 0) for cat in categories]
            variance = [analysis["variance"].get(cat, 0) for cat in categories]

            x = np.arange(len(categories))
            width = 0.35

            bars1 = ax4.bar(x - width/2, planned, width, label='Planned', color="#2196F3")
            bars2 = ax4.bar(x + width/2, actual, width, label='Actual', color="#FF9800")

            # Add variance percentages
            for i, (p, a) in enumerate(zip(planned, actual)):
                if p > 0 or a > 0:
                    var_pct = ((a - p) / p) * 100 if p > 0 else 0
                    ax4.text(i, max(p, a) + max(planned)*0.05, f"{var_pct:.1f}%",
                            ha='center', va='bottom', fontsize=9)

            ax4.set_xticks(x)
            ax4.set_xticklabels([self.capitalize(cat) for cat in categories])
            ax4.set_title('Budget Variance Analysis')
            ax4.legend()
            ax4.grid(axis='y', linestyle='--', alpha=0.7)
            ax4.tick_params(axis='x', rotation=45)

        # Plot 5: Historical Trends (if enough data)
        if len(self.state["history"]) >= 2:
            sorted_history = sorted(self.state["history"], key=lambda x: x["month"])
            months = [item["month"] for item in sorted_history]
            incomes = [item.get("income", 0) for item in sorted_history]
            expenses = [
                sum(item.get("expenditures", {}).values()) +
                sum(p["cost"] for p in item.get("food_purchases", [])) -
                sum(s["income"] for s in item.get("food_sales", []))
                for item in sorted_history
            ]
            savings = [item.get("savings", {}).get("total", 0) for item in sorted_history]
            loans = [item.get("loan", {}).get("total", 0) for item in sorted_history]

            ax5.plot(months, incomes, marker='o', label='Income', color='#4CAF50')
            ax5.plot(months, expenses, marker='o', label='Expenses', color='#F44336')
            ax5.plot(months, savings, marker='o', label='Savings', color='#2196F3')

            # Add loan data if any loans exist
            if any(loans):
                ax5.plot(months, loans, marker='o', label='Loans', color='#9C27B0')

            ax5.set_title('Historical Trends')
            ax5.legend()
            ax5.grid(True, linestyle='-', alpha=0.7)
            ax5.tick_params(axis='x', rotation=45)

            # Format y-axis labels with thousands separator
            ax5.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"{x:,.0f}"))

            # Add data labels for the last point
            for y, label in zip([incomes[-1], expenses[-1], savings[-1]], ['Income', 'Expenses', 'Savings']):
                ax5.text(len(months)-1, y, f" {label}: {y:,.0f}", va='center')

        # Adjust layout
        try:
            fig.tight_layout()
        except:
            pass

        # Embed the figure in the Tkinter window
        canvas = FigureCanvasTkAgg(fig, master=graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def update_results_screen(self):
        summary_text = "=== INCOME ===\n"
        summary_text += f"Income: {self.state['current_month'].get('income', 0):,.2f} KES\n\n"

        summary_text += "=== SAVINGS PROGRESS ===\n"
        progress = (self.state["total_savings"] / self.SAVINGS_TARGET) * 100
        summary_text += f"Current Total Savings: {self.state['total_savings']:,.2f} KES (Long-term: {self.state['total_savings'] - self.state['short_term_savings']:,.2f}, Short-term: {self.state['short_term_savings']:,.2f})\n"
        summary_text += f"Savings Target: {self.SAVINGS_TARGET:,.2f} KES\n"
        summary_text += f"Progress: {progress:.1f}% of target\n"
        summary_text += f"Remaining: {self.SAVINGS_TARGET - self.state['total_savings']:,.2f} KES\n\n"

        summary_text += "=== REGULAR EXPENDITURES ===\n"
        for category, amount in self.state["current_month"].get("expenditures", {}).items():
            summary_text += f"{self.capitalize(category)}: {amount:,.2f} KES\n"
        summary_text += "\n"

        summary_text += "=== FOOD STOCK TRANSACTIONS ===\n"
        if self.state["current_month"].get("food_purchases"):
            summary_text += "Purchases:\n"
            for data in self.state["current_month"]['food_purchases']:
                food = data['food']
                summary_text += (
                    f"{self.capitalize(food)}: {data['bags']} bags @ "
                    f"{self.food_prices[food]['buy']:,.2f} KES/bag = {data['cost']:,.2f} KES\n"
                )
        if self.state["current_month"].get("food_sales"):
            summary_text += "\nSales:\n"
            for data in self.state["current_month"]['food_sales']:
                food = data['food']
                summary_text += (
                    f"{self.capitalize(food)}: {data['bags']} bags @ "
                    f"{self.food_prices[food]['sell']:,.2f} KES/bag = {data['income']:,.2f} KES\n"
                )
        summary_text += "\nCurrent Inventory:\n"
        for food, quantity in self.state["food_inventory"].items():
            summary_text += f"{self.capitalize(food)}: {quantity} bags\n"
        summary_text += "\n"

        summary_text += "=== INVESTMENTS AND EMERGENCY FUND ===\n"
        summary_text += f"Investments: {self.state['current_month'].get('investments', 0):,.2f} KES\n"
        summary_text += f"Emergency Fund: {self.state['current_month'].get('emergency_fund', 0):,.2f} KES\n\n"

        if self.state["current_month"].get("loan", {}).get("needed", False):
            summary_text += "=== LOAN INFORMATION ===\n"
            summary_text += f"Loan Amount: {self.state['current_month']['loan']['amount']:,.2f} KES\n"
            summary_text += (
                f"Loan Interest: {self.state['current_month']['loan']['interest']:,.2f} KES "
                f"({15 if self.state['current_month']['loan']['amount'] <= 49999 else 10}% rate)\n"
            )
            summary_text += f"Total Loan Repayment: {self.state['current_month']['loan']['total']:,.2f} KES\n\n"
            summary_text += "You have exceeded your budget and need a loan. Consider reducing expenses.\n\n"

        total_exp = (
            sum(self.state["current_month"].get("expenditures", {}).values()) +
            sum(item["cost"] for item in self.state["current_month"].get("food_purchases", [])) -
            sum(item["income"] for item in self.state["current_month"].get("food_sales", []))
        )

        summary_text += "=== SAVINGS ===\n"
        income = self.state["current_month"].get("income", 1)
        savings_total = self.state["current_month"].get("savings", {}).get("total", 0)
        savings_rate = (savings_total / income) * 100 if income else 0
        summary_text += f"Total Savings: {savings_total:,.2f} KES ({savings_rate:.1f}% of income)\n"
        summary_text += "From Savings Reserve: 18,000.00 KES (15,000 long-term + 3,000 short-term)\n"
        if self.state["current_month"].get("loan", {}).get("needed", False):
            summary_text += f"Additional Savings: -{total_exp - self.state['current_month']['available_budget']:,.2f} KES (deducted from short-term savings)\n"
        else:
            additional_savings = self.state["current_month"]['available_budget'] - total_exp
            summary_text += f"Additional Savings: {additional_savings:,.2f} KES (added to short-term savings)\n"

        self.summary_text.delete(1.0, tk.END)
        self.summary_text.insert(tk.END, summary_text)

        # Budget Analysis Tab
        analysis_text = "=== BUDGET VARIANCE ANALYSIS ===\n\n"
        analysis_text += "Category".ljust(20) + "Planned (KES)".ljust(15) + "Actual (KES)".ljust(15) + "Variance (KES)".ljust(15) + "Variance %".ljust(15) + "\n"
        analysis_text += "-" * 80 + "\n"

        budget_analysis = self.state["current_month"].get("budget_analysis", {})
        planned = budget_analysis.get("planned", {})
        actual = budget_analysis.get("actual", {})
        variance_amounts = budget_analysis.get("variance_amounts", {})
        variance = budget_analysis.get("variance", {})

        for category in planned:
            analysis_text += (
                f"{self.capitalize(category).ljust(20)}"
                f"{planned[category]:15,.2f}"
                f"{actual.get(category, 0):15,.2f}"
                f"{variance_amounts.get(category, 0):15,.2f}"
                f"{variance.get(category, 0):15.1f}%\n"
            )

        analysis_text += "\n=== STATISTICAL ANALYSIS ===\n"
        significant = budget_analysis.get("significant", False)
        analysis_text += f"Significant variance: {'Yes' if significant else 'No'}\n"
        analysis_text += budget_analysis.get("statistical_analysis", {}).get("message", "")
        self.budget_analysis_text.delete(1.0, tk.END)
        self.budget_analysis_text.insert(tk.END, analysis_text)

        # Update loan tab
        self.update_loan_tab()

        # Update graphs
        self.create_graphs_tab()

    def create_history_screen(self):
        self.history_frame = ttk.Frame(self.main_frame)

        title_label = ttk.Label(self.history_frame, text="Financial History", style="Title.TLabel")
        title_label.pack(pady=10)

        # Add contact information
        contact_frame = ttk.Frame(self.history_frame, relief=tk.RIDGE, borderwidth=2)
        contact_frame.pack(fill=tk.X, pady=5)
        ttk.Label(contact_frame, text="For assistance, contact: samngacha@gmail.com | +254742859291").pack()

        # Add tabs for different views
        self.history_notebook = ttk.Notebook(self.history_frame)
        self.history_notebook.pack(fill=tk.BOTH, expand=True)

        # Monthly summary tab
        self.monthly_summary_tab = ttk.Frame(self.history_notebook)
        self.history_notebook.add(self.monthly_summary_tab, text="Monthly Summary")

        # Create container for text and graph
        monthly_summary_container = ttk.Frame(self.monthly_summary_tab)
        monthly_summary_container.pack(fill=tk.BOTH, expand=True)

        # Text portion
        self.monthly_summary_text = tk.Text(monthly_summary_container, wrap=tk.WORD, height=10)
        self.monthly_summary_text.pack(fill=tk.BOTH, expand=True)

        # Graph portion
        self.monthly_summary_graph_frame = ttk.Frame(monthly_summary_container)
        self.monthly_summary_graph_frame.pack(fill=tk.BOTH, expand=True)

        # Loans history tab
        self.loans_history_tab = ttk.Frame(self.history_notebook)
        self.history_notebook.add(self.loans_history_tab, text="Loans History")

        # Create container for text and graph
        loans_history_container = ttk.Frame(self.loans_history_tab)
        loans_history_container.pack(fill=tk.BOTH, expand=True)

        # Text portion
        self.loans_history_text = tk.Text(loans_history_container, wrap=tk.WORD, height=10)
        self.loans_history_text.pack(fill=tk.BOTH, expand=True)

        # Graph portion
        self.loans_history_graph_frame = ttk.Frame(loans_history_container)
        self.loans_history_graph_frame.pack(fill=tk.BOTH, expand=True)

        button_frame = ttk.Frame(self.history_frame)
        button_frame.pack(pady=10)
        ttk.Button(button_frame, text="Refresh", command=self.refresh_data).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Clear All Data", command=self.clear_all_data).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Track New Month", command=lambda: self.show_screen("month_selector")).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Back", command=lambda: self.show_screen("results")).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Export to CSV", command=self.export_to_csv).pack(side=tk.LEFT, padx=5)

    def update_history_screen(self):
        self.monthly_summary_text.delete(1.0, tk.END)
        self.loans_history_text.delete(1.0, tk.END)

        # Clear previous graphs
        for widget in self.monthly_summary_graph_frame.winfo_children():
            widget.destroy()
        for widget in self.loans_history_graph_frame.winfo_children():
            widget.destroy()

        if not self.state["history"]:
            self.monthly_summary_text.insert(tk.END, "No historical data available yet.\n")
            self.loans_history_text.insert(tk.END, "No loan history available yet.\n")
            return

        progress = (self.state["total_savings"] / self.SAVINGS_TARGET) * 100
        self.monthly_summary_text.insert(tk.END, "=== TOTAL SAVINGS PROGRESS ===\n")
        self.monthly_summary_text.insert(tk.END, f"Current Total Savings: {self.state['total_savings']:,.2f} KES\n")
        self.monthly_summary_text.insert(tk.END, f"Short-term Savings: {self.state['short_term_savings']:,.2f} KES\n")
        self.monthly_summary_text.insert(tk.END, f"Savings Target: {self.SAVINGS_TARGET:,.2f} KES\n")
        self.monthly_summary_text.insert(tk.END, f"Progress: {progress:.1f}% of target\n\n")

        self.monthly_summary_text.insert(tk.END, "=== FINANCIAL HISTORY ===\n")
        self.monthly_summary_text.insert(tk.END, "Month".ljust(12) + "Income (KES)".ljust(15) + "Expenses (KES)".ljust(15) + "Savings %".ljust(10) + "Budget Aligned".ljust(15) + "Loans".ljust(15) + "\n")
        self.monthly_summary_text.insert(tk.END, "-" * 100 + "\n")

        # Prepare loans history
        loans_history = []
        loans_history_text = "=== LOAN HISTORY ===\n\n"

        sorted_history = sorted(self.state["history"], key=lambda x: x["month"])
        for month_data in sorted_history:
            try:
                expenses = (
                    sum(month_data.get("expenditures", {}).values()) +
                    sum(item["cost"] for item in month_data.get("food_purchases", [])) -
                    sum(item["income"] for item in month_data.get("food_sales", []))
                )
                income = month_data.get("income", 1)
                savings_total = month_data.get("savings", {}).get("total", 0)
                savings_pct = (savings_total / income) * 100 if income else 0
                budget_analysis = month_data.get("budget_analysis", {})
                budget_aligned = "Needs Review" if budget_analysis.get("significant", False) else "Aligned"
                loan = month_data.get("loan", {})
                loan_needed = f"Yes ({loan.get('total', 0):.2f})" if loan.get("needed", False) else "No"

                self.monthly_summary_text.insert(tk.END,
                    f"{month_data.get('month', ''):12} {income:15,.2f} {expenses:15,.2f} "
                    f"{savings_total:15,.2f} {savings_pct:10.1f}% "
                    f"{budget_aligned:15} {loan_needed:15}\n"
                )

                # Collect loan information
                if loan.get("needed", False):
                    loans_history.append({
                        "month": month_data.get("month", ""),
                        "amount": loan.get("amount", 0),
                        "interest": loan.get("interest", 0),
                        "total": loan.get("total", 0),
                        "rate": 15 if loan.get("amount", 0) <= 49999 else 10
                    })
            except Exception as e:
                self.monthly_summary_text.insert(tk.END, f"Error displaying month {month_data.get('month', '')}: {str(e)}\n")

        self.monthly_summary_text.insert(tk.END, "\n=== TREND ANALYSIS ===\n")
        if len(self.state["history"]) >= 3:
            incomes = [month.get("income", 0) for month in sorted_history]
            income_trend = "Increasing" if incomes[-1] > incomes[0] else "Decreasing" if incomes[-1] < incomes[0] else "Stable"
            savings = [
                (month.get("savings", {}).get("total", 0)) / month.get("income", 1) * 100 if month.get("income", 0) > 0 else 0
                for month in sorted_history
            ]
            savings_trend = "Increasing" if savings[-1] > savings[0] else "Decreasing" if savings[-1] < savings[0] else "Stable"

            self.monthly_summary_text.insert(tk.END, f"Income Trend: {income_trend}\n")
            self.monthly_summary_text.insert(tk.END, f"Savings Rate Trend: {savings_trend}\n")
        else:
            self.monthly_summary_text.insert(tk.END, "Insufficient data for meaningful trend analysis\n")

        # Display loans history
        if loans_history:
            loans_history_text += "Month".ljust(12) + "Amount (KES)".ljust(15) + "Interest (KES)".ljust(15) + "Total (KES)".ljust(15) + "Rate %".ljust(10) + "\n"
            loans_history_text += "-" * 70 + "\n"
            for loan in loans_history:
                loans_history_text += (
                    f"{loan['month']:12} {loan['amount']:15,.2f} {loan['interest']:15,.2f} "
                    f"{loan['total']:15,.2f} {loan['rate']:10.1f}%\n"
                )

            total_loans = sum(loan['amount'] for loan in loans_history)
            total_interest = sum(loan['interest'] for loan in loans_history)
            loans_history_text += "\n=== TOTALS ===\n"
            loans_history_text += f"Total loans: {total_loans:,.2f} KES\n"
            loans_history_text += f"Total Interest Paid: {total_interest:,.2f} KES\n"
            loans_history_text += f"Average Interest Rate: {total_interest / total_loans * 100 if total_loans > 0 else 0:.1f}%\n"
        else:
            loans_history_text += "No loan history found in the recorded months.\n"
        self.loans_history_text.insert(tk.END, loans_history_text)

        # Create monthly summary graph
        if len(self.state["history"]) >= 2:
            fig = Figure(figsize=(10, 5), dpi=100)
            ax = fig.add_subplot(111)

            months = [item["month"] for item in sorted_history]
            incomes = [item.get("income", 0) for item in sorted_history]
            expenses = [
                sum(item.get("expenditures", {}).values()) +
                sum(item["cost"] for item in item.get("food_purchases", [])) -
                sum(item["income"] for item in item.get("food_sales", []))
                for item in sorted_history
            ]
            savings = [item.get("savings", {}).get("total", 0) for item in sorted_history]

            ax.plot(months, incomes, marker='o', label='Income', color='#4CAF50')
            ax.plot(months, expenses, marker='o', label='Expenses', color='#F44336')
            ax.plot(months, savings, marker='o', label='Savings', color='#2196F3')

            ax.set_title('Monthly Financial Summary')
            ax.legend()
            ax.grid(True, linestyle='--', alpha=0.7)
            ax.tick_params(axis='x', rotation=45)
            ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"{x:,.0f}"))

            canvas = FigureCanvasTkAgg(fig, master=self.monthly_summary_graph_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Create loans history graph
        if loans_history:
            fig = Figure(figsize=(10, 5), dpi=100)
            ax = fig.add_subplot(111)

            loan_months = [loan["month"] for loan in loans_history]
            loan_amounts = [loan["amount"] for loan in loans_history]
            loan_interests = [loan["interest"] for loan in loans_history]

            x = np.arange(len(loan_months))
            width = 0.35

            bars1 = ax.bar(x - width/2, loan_amounts, width, label='Principal', color='#2196F3')
            bars2 = ax.bar(x + width/2, loan_interests, width, label='Interest', color='#FF9800')

            ax.set_xticks(x)
            ax.set_xticklabels(loan_months)
            ax.set_title('Loan History')
            ax.legend()
            ax.grid(axis='y', linestyle='--', alpha=0.7)
            ax.tick_params(axis='x', rotation=45)
            ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"{x:,.0f}"))

            # Add value labels
            for bars in [bars1, bars2]:
                for bar in bars:
                    height = bar.get_height()
                    ax.text(bar.get_x() + bar.get_width()/2., height,
                            f"{height:,.0f}",
                            ha='center', va='bottom')

            canvas = FigureCanvasTkAgg(fig, master=self.loans_history_graph_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def export_to_csv(self):
        if not self.state["current_month"]:
            messagebox.showerror("Error", "No current month data to export")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")],
            initialfile=f"finance_report_{self.state['current_month'].get('month', 'report')}.csv"
        )
        if not file_path:
            return

        try:
            progress = (self.state["total_savings"] / self.SAVINGS_TARGET) * 100
            with open(file_path, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['Category', 'Amount (KES)', 'Details'])
                writer.writerow(['Income', self.state["current_month"].get("income", 0), ''])
                writer.writerow(['Total Long-term Savings', self.state["total_savings"], f"Target: {self.SAVINGS_TARGET:,.0f} KES"])
                writer.writerow(['Short-term Savings', self.state["short_term_savings"], ''])
                writer.writerow(['Savings Progress', f"{self.state['total_savings']}/{self.SAVINGS_TARGET:,.0f} KES ({progress:.1f}%)", ''])

                for category, amount in self.state["current_month"].get("expenditures", {}).items():
                    writer.writerow([self.capitalize(category), amount, ''])

                for data in self.state["current_month"].get("food_purchases", []):
                    writer.writerow([
                        f"Food Purchase {self.capitalize(data['food'])}",
                        data["cost"],
                        f"{data['bags']} bags @ {self.food_prices[data['food']]['buy']:.2f} KES/bag"
                    ])

                for data in self.state["current_month"].get("food_sales", []):
                    writer.writerow([
                        f"Food Sale {self.capitalize(data['food'])}",
                        data["income"],
                        f"{data['bags']} bags @ {self.food_prices[data['food']]['sell']:.2f} KES/bag"
                    ])

                writer.writerow(['Investments', self.state["current_month"].get("investments", 0), ''])
                writer.writerow(['Emergency Fund', self.state["current_month"].get("emergency_fund", 0), ''])
                writer.writerow(['Savings Reserve', self.state["current_month"].get("savings_reserve", 0), ''])
                writer.writerow(['From Savings Reserve', 18000.00, "15,000 long-term + 3,000 short-term"])

                total_exp = (
                    sum(self.state["current_month"].get("expenditures", {}).values()) +
                    sum(item["cost"] for item in self.state["current_month"].get("food_purchases", [])) -
                    sum(item["income"] for item in self.state["current_month"].get("food_sales", []))
                )

                if self.state["current_month"].get("loan", {}).get("needed", False):
                    writer.writerow(['Additional Savings', -(total_exp - self.state["current_month"]['available_budget']), 'Deducted from short-term savings'])
                else:
                    writer.writerow(['Additional Savings', self.state["current_month"]['available_budget'] - total_exp, 'Added to short-term savings'])

                writer.writerow([
                    "Total Savings",
                    self.state["current_month"].get("savings", {}).get("total", 0),
                    f"{self.state['current_month'].get('savings', {}).get('total', 0)/self.state['current_month'].get('income', 1)*100:.1f}% of income"
                ])

                if self.state["current_month"].get("loan", {}).get("needed", False):
                    writer.writerow(['Loan Amount', self.state["current_month"]['loan']['amount'], ''])
                    writer.writerow([
                        "Loan Interest",
                        self.state["current_month"]['loan']['interest'],
                        f"{15 if self.state['current_month']['loan']['amount'] <= 49999 else 10}% rate"
                    ])
                    writer.writerow(['Total Loan Repayment', self.state["current_month"]['loan']['total'], ''])

                budget_analysis = self.state["current_month"].get("budget_analysis", {})
                writer.writerow([
                    "Budget Alignment",
                    "Needs Review" if budget_analysis.get("significant", False) else "Aligned",
                    ""
                ])

                for category, var_pct in budget_analysis.get("variance", {}).items():
                    writer.writerow([f"{self.capitalize(category)} Variance", f"{var_pct:.1f}%", ""])

            messagebox.showinfo("Success", "Data exported to CSV successfully")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export data: {str(e)}")

    def clear_all_data(self):
        if messagebox.askyesno("Confirm", "Are you sure you want to delete all your financial data?"):
            self.state = {
                "current_month": {},
                "history": [],
                "total_savings": 442000,
                "short_term_savings": 0,
                "food_inventory": {food: 0 for food in self.food_prices},
                "current_screen": "month_selector"
            }

            self.save_data()
            self.show_screen("month_selector")
            messagebox.showinfo("Success", "All data has been cleared")

    def refresh_data(self):
        self.load_data()
        self.show_screen(self.state["current_screen"])

    def capitalize(self, text):
        return text[0].upper() + text[1:]

if __name__ == "__main__":
    root = tk.Tk()
    app = PersonalFinanceTracker(root)
    root.mainloop()