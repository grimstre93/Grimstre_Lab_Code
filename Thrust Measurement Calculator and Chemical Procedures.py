import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
import os

# Constants
POUND_TO_NEWTON = 4.45
LOG_FILE = "motor_production_log.csv"

# Global storage
entries = []
motor_logs = []

# Initialize log file if it doesn't exist
if not os.path.exists(LOG_FILE):
    pd.DataFrame(columns=["Timestamp", "MotorID", "Type", "Weight (g)", "Thrust (N)", "Cd", "Notes"]).to_csv(LOG_FILE, index=False)

# --- Thrust/Drag Calculations ---
def calculate_drag_coefficient(thrust, weight, area, velocity):
    air_density = 1.225
    try:
        cd = (2 * float(weight)) / (air_density * float(area) * float(velocity) ** 2)
        return round(cd, 4)
    except Exception:
        return None

def add_entry():
    if len(entries) >= 5:
        messagebox.showwarning("Limit Reached", "Maximum of 5 entries allowed.")
        return
    try:
        weight = float(weight_var.get())
        thrust = float(thrust_var.get())
        area = float(area_var.get())
        velocity = float(velocity_var.get())
    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numbers.")
        return

    cd = calculate_drag_coefficient(thrust, weight, area, velocity)
    if cd is None:
        messagebox.showerror("Error", "Invalid input for Cd calculation.")
        return

    entry = {
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "weight": weight,
        "thrust": thrust,
        "area": area,
        "velocity": velocity,
        "cd": cd
    }
    entries.append(entry)
    update_table()
    plot_graph()

# --- Chemical Procedures ---
def calculate_black_powder():
    try:
        total_weight = float(bp_weight_var.get())
        kn = total_weight * 6 / 8
        s = total_weight * 1 / 8
        c = total_weight * 1 / 8
        bp_result_var.set(f"KN: {kn:.2f}g, S: {s:.2f}g, C: {c:.2f}g")
    except ValueError:
        bp_result_var.set("Invalid input")

def calculate_nitrocellulose():
    try:
        sugar = float(nc_sugar_var.get())
        acid_volume = float(nc_acid_var.get())
        nc_result_var.set(f"Use {sugar}g sugar + {acid_volume}mL acid mix (1:2 HNO3:H2SO4).\nWash with boiling water, dry at <50°C.")
    except ValueError:
        nc_result_var.set("Invalid input")

# --- Motor Production Log ---
def log_motor():
    try:
        motor_id = motor_id_var.get()
        motor_type = motor_type_var.get()
        weight = float(motor_weight_var.get())
        thrust = float(motor_thrust_var.get())
        cd = float(motor_cd_var.get()) if motor_cd_var.get() else 0
        notes = motor_notes_var.get()

        log_entry = {
            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "MotorID": motor_id,
            "Type": motor_type,
            "Weight (g)": weight,
            "Thrust (N)": thrust,
            "Cd": cd,
            "Notes": notes
        }
        motor_logs.append(log_entry)
        
        # Save to CSV
        pd.DataFrame(motor_logs).to_csv(LOG_FILE, mode='a', header=not os.path.exists(LOG_FILE), index=False)
        messagebox.showinfo("Success", f"Motor {motor_id} logged to {LOG_FILE}.")
    except ValueError:
        messagebox.showerror("Error", "Invalid input for motor log.")

def view_logs():
    try:
        logs = pd.read_csv(LOG_FILE)
        messagebox.showinfo("Motor Logs", logs.to_string(index=False))
    except Exception as e:
        messagebox.showerror("Error", f"Could not load logs:\n{e}")

# --- GUI Setup ---
root = tk.Tk()
root.title("Rocket Motor Calculator & Log")

# Thrust Calculator Frame
thrust_frame = ttk.LabelFrame(root, text="Thrust & Drag Calculator")
thrust_frame.pack(padx=10, pady=5, fill="x")

ttk.Label(thrust_frame, text="Weight (g):").grid(row=0, column=0)
weight_var = tk.StringVar()
ttk.Entry(thrust_frame, textvariable=weight_var).grid(row=0, column=1)

ttk.Label(thrust_frame, text="Thrust (N):").grid(row=1, column=0)
thrust_var = tk.StringVar()
ttk.Entry(thrust_frame, textvariable=thrust_var).grid(row=1, column=1)

ttk.Label(thrust_frame, text="Area (m²):").grid(row=2, column=0)
area_var = tk.StringVar()
ttk.Entry(thrust_frame, textvariable=area_var).grid(row=2, column=1)

ttk.Label(thrust_frame, text="Velocity (m/s):").grid(row=3, column=0)
velocity_var = tk.StringVar()
ttk.Entry(thrust_frame, textvariable=velocity_var).grid(row=3, column=1)

ttk.Button(thrust_frame, text="Add Entry", command=add_entry).grid(row=4, column=0, columnspan=2)

# Chemical Calculator Frame
chem_frame = ttk.LabelFrame(root, text="Chemical Procedures")
chem_frame.pack(padx=10, pady=5, fill="x")

# Black Powder
ttk.Label(chem_frame, text="Black Powder (6:1:1) Total Weight (g):").grid(row=0, column=0)
bp_weight_var = tk.StringVar()
ttk.Entry(chem_frame, textvariable=bp_weight_var).grid(row=0, column=1)
ttk.Button(chem_frame, text="Calculate", command=calculate_black_powder).grid(row=0, column=2)
bp_result_var = tk.StringVar()
ttk.Label(chem_frame, textvariable=bp_result_var).grid(row=0, column=3)

# Nitrocellulose
ttk.Label(chem_frame, text="Nitrocellulose - Sugar (g):").grid(row=1, column=0)
nc_sugar_var = tk.StringVar()
ttk.Entry(chem_frame, textvariable=nc_sugar_var).grid(row=1, column=1)
ttk.Label(chem_frame, text="Acid Mix Volume (mL):").grid(row=1, column=2)
nc_acid_var = tk.StringVar()
ttk.Entry(chem_frame, textvariable=nc_acid_var).grid(row=1, column=3)
ttk.Button(chem_frame, text="Calculate", command=calculate_nitrocellulose).grid(row=1, column=4)
nc_result_var = tk.StringVar()
ttk.Label(chem_frame, textvariable=nc_result_var).grid(row=2, column=0, columnspan=5)

# Motor Log Frame
log_frame = ttk.LabelFrame(root, text="Motor Production Log")
log_frame.pack(padx=10, pady=5, fill="x")

ttk.Label(log_frame, text="Motor ID:").grid(row=0, column=0)
motor_id_var = tk.StringVar()
ttk.Entry(log_frame, textvariable=motor_id_var).grid(row=0, column=1)

ttk.Label(log_frame, text="Type (BP/NC):").grid(row=0, column=2)
motor_type_var = tk.StringVar()
ttk.Entry(log_frame, textvariable=motor_type_var).grid(row=0, column=3)

ttk.Label(log_frame, text="Weight (g):").grid(row=1, column=0)
motor_weight_var = tk.StringVar()
ttk.Entry(log_frame, textvariable=motor_weight_var).grid(row=1, column=1)

ttk.Label(log_frame, text="Thrust (N):").grid(row=1, column=2)
motor_thrust_var = tk.StringVar()
ttk.Entry(log_frame, textvariable=motor_thrust_var).grid(row=1, column=3)

ttk.Label(log_frame, text="Cd (optional):").grid(row=2, column=0)
motor_cd_var = tk.StringVar()
ttk.Entry(log_frame, textvariable=motor_cd_var).grid(row=2, column=1)

ttk.Label(log_frame, text="Notes:").grid(row=2, column=2)
motor_notes_var = tk.StringVar()
ttk.Entry(log_frame, textvariable=motor_notes_var).grid(row=2, column=3)

ttk.Button(log_frame, text="Log Motor", command=log_motor).grid(row=3, column=0, columnspan=2)
ttk.Button(log_frame, text="View Logs", command=view_logs).grid(row=3, column=2, columnspan=2)

# Table and Graph (for thrust calculator)
columns = ("Time", "Weight (g)", "Thrust (N)", "Area (m²)", "Velocity (m/s)", "Cd")
tree = ttk.Treeview(root, columns=columns, show="headings", height=5)
for col in columns:
    tree.heading(col, text=col)
tree.pack(padx=10, pady=10)

fig = plt.Figure(figsize=(5, 3))
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack()

def update_table():
    for row in tree.get_children():
        tree.delete(row)
    for entry in entries:
        tree.insert("", "end", values=(
            entry["time"], entry["weight"], entry["thrust"],
            entry["area"], entry["velocity"], entry["cd"]
        ))

def plot_graph():
    if not entries:
        return
    fig.clear()
    ax = fig.add_subplot(111)
    weights = [e["weight"] for e in entries]
    cds = [e["cd"] for e in entries]
    ax.plot(weights, cds, marker='o', label="Cd vs Weight")
    ax.set_xlabel("Weight (g)")
    ax.set_ylabel("Drag Coefficient (Cd)")
    ax.legend()
    canvas.draw()

root.mainloop()
