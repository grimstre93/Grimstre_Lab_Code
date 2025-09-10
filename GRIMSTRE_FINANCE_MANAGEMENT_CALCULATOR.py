# Copyright (c) GRIMSTRE DIGITAL TOOLS. All rights reserved.
# This software is proprietary and confidential. Unauthorized copying or distribution is prohibited.

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime
import math
import csv

# Initialize main window
root = tk.Tk()
root.title("Yearly Financial Observation Record")
root.geometry("1100x750")

# Data storage
finance_data = []
goals_data = []
log_data = []
foodstock_data = []

# --- Tab Control ---
tab_control = ttk.Notebook(root)

# --- Finance Tab ---
finance_tab = ttk.Frame(tab_control)
tab_control.add(finance_tab, text='Finance')

# --- Food Stock Tab ---
foodstock_tab = ttk.Frame(tab_control)
tab_control.add(foodstock_tab, text='Food Stock')

# --- Goals Tab ---
goals_tab = ttk.Frame(tab_control)
tab_control.add(goals_tab, text='Goals')

# --- Log Tab ---
log_tab = ttk.Frame(tab_control)
tab_control.add(log_tab, text='Log')

# --- Calculator Tab ---
calc_tab = ttk.Frame(tab_control)
tab_control.add(calc_tab, text='Test Calculator')

# --- Analysis Tab ---
analysis_tab = ttk.Frame(tab_control)
tab_control.add(analysis_tab, text='Analysis')

tab_control.pack(expand=1, fill='both')

# --- Finance Tab Widgets ---
def add_finance_record():
    compile_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    record = {
        "Date & Time": compile_date,
        "Income Generated": try_float(income_var.get()),
        "Expenditure": try_float(expenditure_var.get()),
        "Retained Profits": try_float(retained_var.get()),
        "Savings": try_float(savings_var.get()),
        "Food Quantity (90kg Bags)": try_float(food_bags_var.get()),
        "Scale of Expenditure (%)": try_float(scale_var.get())
    }
    finance_data.append(record)
    finance_tree.insert('', 'end', values=list(record.values()))
    log_entry(f"Finance record added: {record}")
    clear_finance_entries()

def clear_finance_entries():
    income_var.set('')
    expenditure_var.set('')
    retained_var.set('')
    savings_var.set('')
    food_bags_var.set('')
    scale_var.set('')

def try_float(val):
    try:
        return float(val)
    except ValueError:
        return 0.0

income_var = tk.StringVar()
expenditure_var = tk.StringVar()
retained_var = tk.StringVar()
savings_var = tk.StringVar()
food_bags_var = tk.StringVar()
scale_var = tk.StringVar()

fields = [
    ("Income Generated", income_var),
    ("Expenditure", expenditure_var),
    ("Retained Profits", retained_var),
    ("Savings", savings_var),
    ("Food Quantity (90kg Bags)", food_bags_var),
    ("Scale of Expenditure (%)", scale_var)
]

for idx, (label, var) in enumerate(fields):
    ttk.Label(finance_tab, text=label).grid(row=idx, column=0, padx=5, pady=5, sticky='e')
    ttk.Entry(finance_tab, textvariable=var).grid(row=idx, column=1, padx=5, pady=5, sticky='w')

ttk.Button(finance_tab, text="Add Record", command=add_finance_record).grid(row=len(fields), column=0, columnspan=2, pady=10)

def export_finance_data():
    if not finance_data:
        messagebox.showinfo("Export", "No finance data to export.")
        return
    file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
    if file_path:
        with open(file_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=["Date & Time"] + [f[0] for f in fields])
            writer.writeheader()
            for row in finance_data:
                writer.writerow(row)
        messagebox.showinfo("Export", f"Finance data exported to {file_path}")

ttk.Button(finance_tab, text="Export Data", command=export_finance_data).grid(row=len(fields)+1, column=0, columnspan=2, pady=5)

finance_tree = ttk.Treeview(finance_tab, columns=["Date & Time"] + [f[0] for f in fields], show='headings')
for col in ["Date & Time"] + [f[0] for f in fields]:
    finance_tree.heading(col, text=col)
    finance_tree.column(col, width=140)
finance_tree.grid(row=0, column=2, rowspan=len(fields)+2, padx=10, pady=5)

# --- Food Stock Tab Widgets ---
def add_foodstock_record():
    compile_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    record = {
        "Date & Time": compile_date,
        "Food Quantity (90kg Bags)": try_float(food_bags_fs_var.get())
    }
    foodstock_data.append(record)
    foodstock_tree.insert('', 'end', values=list(record.values()))
    log_entry(f"Food stock record added: {record}")
    clear_foodstock_entries()

def clear_foodstock_entries():
    food_bags_fs_var.set('')

food_bags_fs_var = tk.StringVar()

ttk.Label(foodstock_tab, text="Food Quantity (90kg Bags)").grid(row=0, column=0, padx=5, pady=5, sticky='e')
ttk.Entry(foodstock_tab, textvariable=food_bags_fs_var).grid(row=0, column=1, padx=5, pady=5, sticky='w')

ttk.Button(foodstock_tab, text="Add Record", command=add_foodstock_record).grid(row=1, column=0, columnspan=2, pady=10)

def export_foodstock_data():
    if not foodstock_data:
        messagebox.showinfo("Export", "No food stock data to export.")
        return
    file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
    if file_path:
        with open(file_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=["Date & Time", "Food Quantity (90kg Bags)"])
            writer.writeheader()
            for row in foodstock_data:
                writer.writerow(row)
        messagebox.showinfo("Export", f"Food stock data exported to {file_path}")

ttk.Button(foodstock_tab, text="Export Data", command=export_foodstock_data).grid(row=2, column=0, columnspan=2, pady=5)

foodstock_tree = ttk.Treeview(foodstock_tab, columns=("Date & Time", "Food Quantity (90kg Bags)"), show='headings')
for col in ("Date & Time", "Food Quantity (90kg Bags)"):
    foodstock_tree.heading(col, text=col)
    foodstock_tree.column(col, width=180)
foodstock_tree.grid(row=0, column=2, rowspan=3, padx=10, pady=5)

# --- Goals Tab Widgets ---
def add_goal_record():
    compile_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    record = {
        "Date & Time": compile_date,
        "Goal Description": goal_desc_var.get()
    }
    goals_data.append(record)
    goals_tree.insert('', 'end', values=list(record.values()))
    log_entry(f"Goal record added: {record}")
    clear_goal_entries()

def clear_goal_entries():
    goal_desc_var.set('')

goal_desc_var = tk.StringVar()

ttk.Label(goals_tab, text="Goal Description").grid(row=0, column=0, padx=5, pady=5, sticky='e')
ttk.Entry(goals_tab, textvariable=goal_desc_var, width=60).grid(row=0, column=1, padx=5, pady=5, sticky='w')

ttk.Button(goals_tab, text="Add Goal", command=add_goal_record).grid(row=1, column=0, columnspan=2, pady=10)

def export_goals_data():
    if not goals_data:
        messagebox.showinfo("Export", "No goals data to export.")
        return
    file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
    if file_path:
        with open(file_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=["Date & Time", "Goal Description"])
            writer.writeheader()
            for row in goals_data:
                writer.writerow(row)
        messagebox.showinfo("Export", f"Goals data exported to {file_path}")

ttk.Button(goals_tab, text="Export Data", command=export_goals_data).grid(row=2, column=0, columnspan=2, pady=5)

goals_tree = ttk.Treeview(goals_tab, columns=("Date & Time", "Goal Description"), show='headings')
for col in ("Date & Time", "Goal Description"):
    goals_tree.heading(col, text=col)
    goals_tree.column(col, width=300)
goals_tree.grid(row=0, column=2, rowspan=3, padx=10, pady=5)

# --- Log Tab Widgets ---
def log_entry(message):
    log_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"{log_time} - {message}"
    log_data.append(entry)
    log_listbox.insert(tk.END, entry)

log_listbox = tk.Listbox(log_tab, width=120, height=30)
log_listbox.pack(padx=10, pady=10, fill='both', expand=True)

def export_log_data():
    if not log_data:
        messagebox.showinfo("Export", "No log data to export.")
        return
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
    if file_path:
        with open(file_path, mode='w', encoding='utf-8') as file:
            for entry in log_data:
                file.write(entry + "\n")
        messagebox.showinfo("Export", f"Log data exported to {file_path}")

ttk.Button(log_tab, text="Export Log", command=export_log_data).pack(pady=5)

# --- Calculator Tab Widgets ---
def calculate_expression():
    expr = calc_entry.get()
    try:
        allowed = "0123456789+-*/(). "
        if not all(c in allowed for c in expr):
            raise ValueError("Invalid characters in expression.")
        result = eval(expr, {"__builtins__": {}})
        calc_result_var.set(str(result))
        log_entry(f"Calculator: {expr} = {result}")
        calc_history_tree.insert('', 'end', values=(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), expr, result))
    except Exception as e:
        calc_result_var.set(f"Error: {e}")
        log_entry(f"Calculator error: {expr} ({e})")

calc_entry = tk.Entry(calc_tab, width=40)
calc_entry.grid(row=0, column=0, padx=10, pady=10, sticky='w')
ttk.Button(calc_tab, text="Calculate", command=calculate_expression).grid(row=0, column=1, padx=5, pady=10, sticky='w')
calc_result_var = tk.StringVar()
tk.Label(calc_tab, textvariable=calc_result_var, width=40, anchor='w').grid(row=1, column=0, columnspan=2, padx=10, pady=5, sticky='w')

calc_history_tree = ttk.Treeview(calc_tab, columns=("Time", "Expression", "Result"), show='headings')
for col in ("Time", "Expression", "Result"):
    calc_history_tree.heading(col, text=col)
    calc_history_tree.column(col, width=150)
calc_history_tree.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky='nsew')

def export_calc_history():
    items = calc_history_tree.get_children()
    if not items:
        messagebox.showinfo("Export", "No calculator history to export.")
        return
    file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
    if file_path:
        with open(file_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["Time", "Expression", "Result"])
            for item in items:
                writer.writerow(calc_history_tree.item(item)['values'])
        messagebox.showinfo("Export", f"Calculator history exported to {file_path}")

ttk.Button(calc_tab, text="Export History", command=export_calc_history).grid(row=3, column=0, columnspan=2, pady=5)

# --- Analysis Tab Widgets ---
def mean(values):
    return sum(values) / len(values) if values else 0

def variance(values):
    m = mean(values)
    return sum((x - m) ** 2 for x in values) / (len(values) - 1) if len(values) > 1 else 0

def stddev(values):
    return math.sqrt(variance(values))

def chi_square_test(observed, expected):
    if len(observed) != len(expected) or not observed:
        return None
    return sum((o - e) ** 2 / e if e != 0 else 0 for o, e in zip(observed, expected))

def analyse_finance():
    if not finance_data:
        messagebox.showinfo("No Data", "No finance data to analyze.")
        return
    expenditures = [rec["Expenditure"] for rec in finance_data]
    incomes = [rec["Income Generated"] for rec in finance_data]
    exp_mean = mean(expenditures)
    exp_std = stddev(expenditures)
    inc_mean = mean(incomes)
    inc_std = stddev(incomes)
    chi_sq = chi_square_test(expenditures, incomes) if len(expenditures) == len(incomes) else "N/A"
    result = (
        f"Expenditure Mean: {exp_mean:.2f}\n"
        f"Expenditure Std Dev: {exp_std:.2f}\n"
        f"Income Mean: {inc_mean:.2f}\n"
        f"Income Std Dev: {inc_std:.2f}\n"
        f"Chi-Square (Expenditure vs Income): {chi_sq if isinstance(chi_sq, str) else f'{chi_sq:.2f}'}"
    )
    messagebox.showinfo("Finance Analysis", result)
    log_entry("Finance data analyzed.")

ttk.Button(analysis_tab, text="Analyze Finance Data", command=analyse_finance).pack(pady=20)

# --- Mainloop ---
root.mainloop()