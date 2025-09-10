# -----------------------------------------------------------------------------
# Copyright (c) 2025 GRIMSTRE DIGITAL TOOLS
# All rights reserved.
#
# This software is provided for educational and non-commercial use only.
# Unauthorized copying, distribution, or modification of this file,
# via any medium is strictly prohibited.
# -----------------------------------------------------------------------------

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime

class RocketCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Rocket Motor Calculator & Log")
        
        # Conversion factors
        self.conversions = {
            # Weight
            'g': {'kg': 0.001, 'lb': 0.00220462},
            'kg': {'g': 1000, 'lb': 2.20462},
            'lb': {'g': 453.592, 'kg': 0.453592},
            'oz': {'g': 28.3495},
            
            # Area
            'm2': {'cm2': 10000, 'in2': 1550},
            'cm2': {'m2': 0.0001, 'in2': 0.155},
            'in2': {'m2': 0.00064516, 'cm2': 6.4516},
            
            # Force
            'N': {'lbf': 0.224809},
            'lbf': {'N': 4.44822},
            
            # Velocity
            'm/s': {'km/h': 3.6, 'mph': 2.23694},
            'km/h': {'m/s': 0.277778, 'mph': 0.621371},
            'mph': {'m/s': 0.44704, 'km/h': 1.60934},
            
            # Volume
            'mL': {'fl oz': 0.033814},
            'fl oz': {'mL': 29.5735}
        }
        
        # Data storage
        self.entries = []
        self.motor_logs = []
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill='both', expand=True)
        
        # Create frames for each section
        self.create_thrust_calculator_tab()
        self.create_chemical_procedures_tab()
        self.create_motor_log_tab()
        
    def convert(self, value, from_unit, to_unit):
        if from_unit == to_unit:
            return value
        if from_unit not in self.conversions or to_unit not in self.conversions[from_unit]:
            return value
        return value * self.conversions[from_unit][to_unit]
    
    def create_thrust_calculator_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Thrust Calculator")
        
        # Input fields
        ttk.Label(frame, text="Weight:").grid(row=0, column=0, sticky='e')
        self.weight_var = tk.DoubleVar()
        ttk.Entry(frame, textvariable=self.weight_var, width=10).grid(row=0, column=1)
        self.weight_unit = ttk.Combobox(frame, values=['g', 'kg', 'lb'], width=5)
        self.weight_unit.current(0)
        self.weight_unit.grid(row=0, column=2)
        
        ttk.Label(frame, text="Thrust:").grid(row=1, column=0, sticky='e')
        self.thrust_var = tk.DoubleVar()
        ttk.Entry(frame, textvariable=self.thrust_var, width=10).grid(row=1, column=1)
        self.thrust_unit = ttk.Combobox(frame, values=['N', 'lbf'], width=5)
        self.thrust_unit.current(0)
        self.thrust_unit.grid(row=1, column=2)
        
        ttk.Label(frame, text="Area:").grid(row=2, column=0, sticky='e')
        self.area_var = tk.DoubleVar()
        ttk.Entry(frame, textvariable=self.area_var, width=10).grid(row=2, column=1)
        self.area_unit = ttk.Combobox(frame, values=['m2', 'cm2', 'in2'], width=5)
        self.area_unit.current(0)
        self.area_unit.grid(row=2, column=2)
        
        ttk.Label(frame, text="Velocity:").grid(row=3, column=0, sticky='e')
        self.velocity_var = tk.DoubleVar()
        ttk.Entry(frame, textvariable=self.velocity_var, width=10).grid(row=3, column=1)
        self.velocity_unit = ttk.Combobox(frame, values=['m/s', 'km/h', 'mph'], width=5)
        self.velocity_unit.current(0)
        self.velocity_unit.grid(row=3, column=2)
        
        # Buttons
        ttk.Button(frame, text="Add Entry", command=self.add_entry).grid(row=4, column=0, columnspan=2)
        ttk.Button(frame, text="Clear Entries", command=self.clear_entries).grid(row=4, column=2)
        
        # Entries table
        columns = ("Time", "Weight (g)", "Thrust (N)", "Area (m²)", "Velocity (m/s)", "Cd")
        self.entries_tree = ttk.Treeview(frame, columns=columns, show="headings", height=5)
        for col in columns:
            self.entries_tree.heading(col, text=col)
            self.entries_tree.column(col, width=80)
        self.entries_tree.grid(row=5, column=0, columnspan=3, sticky='nsew')
        
        # Configure grid weights for resizing
        for i in range(6):
            frame.grid_rowconfigure(i, weight=1)
        for j in range(3):
            frame.grid_columnconfigure(j, weight=1)
    
    def create_chemical_procedures_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Chemical Procedures")
        
        # Black Powder
        ttk.Label(frame, text="Black Powder (6:1:1)").grid(row=0, column=0, sticky='w')
        
        ttk.Label(frame, text="Total Weight:").grid(row=1, column=0, sticky='e')
        self.bp_weight_var = tk.DoubleVar()
        ttk.Entry(frame, textvariable=self.bp_weight_var, width=10).grid(row=1, column=1)
        self.bp_weight_unit = ttk.Combobox(frame, values=['g', 'oz'], width=5)
        self.bp_weight_unit.current(0)
        self.bp_weight_unit.grid(row=1, column=2)
        ttk.Button(frame, text="Calculate", command=self.calculate_bp).grid(row=1, column=3)
        
        self.bp_result_var = tk.StringVar()
        ttk.Label(frame, textvariable=self.bp_result_var, wraplength=300).grid(row=2, column=0, columnspan=4, sticky='w')
        
        # Nitrocellulose
        ttk.Label(frame, text="Nitrocellulose").grid(row=3, column=0, sticky='w')
        
        ttk.Label(frame, text="Sugar:").grid(row=4, column=0, sticky='e')
        self.nc_sugar_var = tk.DoubleVar()
        ttk.Entry(frame, textvariable=self.nc_sugar_var, width=10).grid(row=4, column=1)
        self.nc_sugar_unit = ttk.Combobox(frame, values=['g', 'oz'], width=5)
        self.nc_sugar_unit.current(0)
        self.nc_sugar_unit.grid(row=4, column=2)
        
        ttk.Label(frame, text="Acid Volume:").grid(row=5, column=0, sticky='e')
        self.nc_acid_var = tk.DoubleVar()
        ttk.Entry(frame, textvariable=self.nc_acid_var, width=10).grid(row=5, column=1)
        self.nc_acid_unit = ttk.Combobox(frame, values=['mL', 'fl oz'], width=5)
        self.nc_acid_unit.current(0)
        self.nc_acid_unit.grid(row=5, column=2)
        ttk.Button(frame, text="Calculate", command=self.calculate_nc).grid(row=5, column=3)
        
        self.nc_result_var = tk.StringVar()
        ttk.Label(frame, textvariable=self.nc_result_var, wraplength=300).grid(row=6, column=0, columnspan=4, sticky='w')
        
        # Configure grid weights
        for i in range(7):
            frame.grid_rowconfigure(i, weight=1)
        for j in range(4):
            frame.grid_columnconfigure(j, weight=1)
    
    def create_motor_log_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Motor Log")
        
        # Input fields
        ttk.Label(frame, text="Motor ID:").grid(row=0, column=0, sticky='e')
        self.motor_id_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.motor_id_var, width=15).grid(row=0, column=1)
        
        ttk.Label(frame, text="Type:").grid(row=0, column=2, sticky='e')
        self.motor_type_var = tk.StringVar()
        ttk.Combobox(frame, textvariable=self.motor_type_var, values=['BP', 'NC'], width=5).grid(row=0, column=3)
        
        ttk.Label(frame, text="Weight:").grid(row=1, column=0, sticky='e')
        self.motor_weight_var = tk.DoubleVar()
        ttk.Entry(frame, textvariable=self.motor_weight_var, width=10).grid(row=1, column=1)
        self.motor_weight_unit = ttk.Combobox(frame, values=['g', 'oz'], width=5)
        self.motor_weight_unit.current(0)
        self.motor_weight_unit.grid(row=1, column=2)
        
        ttk.Label(frame, text="Thrust:").grid(row=1, column=3, sticky='e')
        self.motor_thrust_var = tk.DoubleVar()
        ttk.Entry(frame, textvariable=self.motor_thrust_var, width=10).grid(row=1, column=4)
        self.motor_thrust_unit = ttk.Combobox(frame, values=['N', 'lbf'], width=5)
        self.motor_thrust_unit.current(0)
        self.motor_thrust_unit.grid(row=1, column=5)
        
        ttk.Label(frame, text="Cd (optional):").grid(row=2, column=0, sticky='e')
        self.motor_cd_var = tk.DoubleVar()
        ttk.Entry(frame, textvariable=self.motor_cd_var, width=10).grid(row=2, column=1)
        
        ttk.Label(frame, text="Notes:").grid(row=2, column=2, sticky='e')
        self.motor_notes_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.motor_notes_var, width=20).grid(row=2, column=3, columnspan=3)
        
        # Buttons
        ttk.Button(frame, text="Log Motor", command=self.log_motor).grid(row=3, column=0, columnspan=2)
        ttk.Button(frame, text="View Logs", command=self.view_logs).grid(row=3, column=2, columnspan=2)
        ttk.Button(frame, text="Export Logs", command=self.export_logs).grid(row=3, column=4, columnspan=2)
        
        # Logs table
        columns = ("Timestamp", "MotorID", "Type", "Weight (g)", "Thrust (N)", "Cd", "Notes")
        self.logs_tree = ttk.Treeview(frame, columns=columns, show="headings", height=10)
        for col in columns:
            self.logs_tree.heading(col, text=col)
            self.logs_tree.column(col, width=80)
        self.logs_tree.grid(row=4, column=0, columnspan=6, sticky='nsew')
        
        # Configure grid weights
        for i in range(5):
            frame.grid_rowconfigure(i, weight=1)
        for j in range(6):
            frame.grid_columnconfigure(j, weight=1)
    
    def calculate_drag_coefficient(self, thrust_N, weight_g, area_m2, velocity_ms):
        air_density = 1.225  # kg/m³
        try:
            weight_kg = weight_g / 1000
            cd = (2 * weight_kg) / (air_density * area_m2 * (velocity_ms ** 2))
            return round(cd, 4)
        except:
            return None
    
    def add_entry(self):
        if len(self.entries) >= 5:
            messagebox.showwarning("Limit Reached", "Maximum of 5 entries allowed.")
            return
        
        try:
            weight = self.weight_var.get()
            weight_unit = self.weight_unit.get()
            thrust = self.thrust_var.get()
            thrust_unit = self.thrust_unit.get()
            area = self.area_var.get()
            area_unit = self.area_unit.get()
            velocity = self.velocity_var.get()
            velocity_unit = self.velocity_unit.get()
        except tk.TclError:
            messagebox.showerror("Input Error", "Please enter valid numbers.")
            return
        
        # Convert to standard units
        weight_g = self.convert(weight, weight_unit, 'g')
        thrust_N = self.convert(thrust, thrust_unit, 'N')
        area_m2 = self.convert(area, area_unit, 'm2')
        velocity_ms = self.convert(velocity, velocity_unit, 'm/s')
        
        cd = self.calculate_drag_coefficient(thrust_N, weight_g, area_m2, velocity_ms)
        if cd is None:
            messagebox.showerror("Error", "Invalid input for drag coefficient calculation.")
            return
        
        entry = {
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "weight": round(weight_g, 2),
            "thrust": round(thrust_N, 2),
            "area": round(area_m2, 6),
            "velocity": round(velocity_ms, 2),
            "cd": cd
        }
        
        self.entries.append(entry)
        self.update_entries_table()
    
    def clear_entries(self):
        self.entries = []
        self.update_entries_table()
    
    def update_entries_table(self):
        for item in self.entries_tree.get_children():
            self.entries_tree.delete(item)
        
        for entry in self.entries:
            self.entries_tree.insert("", "end", values=(
                entry["time"],
                entry["weight"],
                entry["thrust"],
                entry["area"],
                entry["velocity"],
                entry["cd"]
            ))
    
    def calculate_bp(self):
        try:
            total_weight = self.bp_weight_var.get()
            weight_unit = self.bp_weight_unit.get()
        except tk.TclError:
            self.bp_result_var.set("Invalid input")
            return
        
        if total_weight <= 0:
            self.bp_result_var.set("Weight must be positive")
            return
        
        # Convert to grams
        total_weight_g = self.convert(total_weight, weight_unit, 'g')
        
        kn = round(total_weight_g * 6 / 8, 2)
        s = round(total_weight_g * 1 / 8, 2)
        c = round(total_weight_g * 1 / 8, 2)
        
        self.bp_result_var.set(
            f"Black Powder Composition:\n"
            f"Potassium Nitrate (KN): {kn}g\n"
            f"Sulfur (S): {s}g\n"
            f"Charcoal (C): {c}g"
        )
    
    def calculate_nc(self):
        try:
            sugar = self.nc_sugar_var.get()
            sugar_unit = self.nc_sugar_unit.get()
            acid = self.nc_acid_var.get()
            acid_unit = self.nc_acid_unit.get()
        except tk.TclError:
            self.nc_result_var.set("Invalid input")
            return
        
        if sugar <= 0 or acid <= 0:
            self.nc_result_var.set("Values must be positive")
            return
        
        # Convert to standard units
        sugar_g = self.convert(sugar, sugar_unit, 'g')
        acid_mL = self.convert(acid, acid_unit, 'mL')
        
        self.nc_result_var.set(
            f"Nitrocellulose Preparation:\n"
            f"1. Mix {sugar_g}g sugar with {acid_mL}mL acid mixture (1:2 HNO₃:H₂SO₄)\n"
            f"2. Cool to 0°C and stir to form paste\n"
            f"3. Wash with boiling water until acid-free\n"
            f"4. Dry at low temperature (<50°C)\n"
            f"Warning: Highly flammable!"
        )
    
    def log_motor(self):
        try:
            motor_id = self.motor_id_var.get()
            motor_type = self.motor_type_var.get()
            weight = self.motor_weight_var.get()
            weight_unit = self.motor_weight_unit.get()
            thrust = self.motor_thrust_var.get()
            thrust_unit = self.motor_thrust_unit.get()
            cd = self.motor_cd_var.get() if self.motor_cd_var.get() != 0 else 0
            notes = self.motor_notes_var.get()
        except tk.TclError:
            messagebox.showerror("Input Error", "Please enter valid values.")
            return
        
        if not motor_id or motor_type not in ['BP', 'NC'] or weight <= 0 or thrust <= 0:
            messagebox.showerror("Input Error", "Please fill required fields with valid values.")
            return
        
        # Convert to standard units
        weight_g = self.convert(weight, weight_unit, 'g')
        thrust_N = self.convert(thrust, thrust_unit, 'N')
        
        log_entry = {
            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "MotorID": motor_id,
            "Type": motor_type,
            "Weight (g)": round(weight_g, 2),
            "Thrust (N)": round(thrust_N, 2),
            "Cd": round(cd, 4) if cd else 0,
            "Notes": notes
        }
        
        self.motor_logs.append(log_entry)
        self.update_logs_table()
        
        # Clear fields
        self.motor_id_var.set("")
        self.motor_weight_var.set(0)
        self.motor_thrust_var.set(0)
        self.motor_cd_var.set(0)
        self.motor_notes_var.set("")
        
        messagebox.showinfo("Success", f"Motor {motor_id} logged successfully.")
    
    def view_logs(self):
        self.update_logs_table()
    
    def update_logs_table(self):
        for item in self.logs_tree.get_children():
            self.logs_tree.delete(item)
        
        for log in self.motor_logs:
            self.logs_tree.insert("", "end", values=(
                log["Timestamp"],
                log["MotorID"],
                log["Type"],
                log["Weight (g)"],
                log["Thrust (N)"],
                log["Cd"],
                log["Notes"]
            ))
    
    def export_logs(self):
        if not self.motor_logs:
            messagebox.showwarning("No Data", "No motor logs to export.")
            return
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")],
            title="Save Motor Logs"
        )
        
        if not file_path:
            return
        
        try:
            with open(file_path, 'w') as f:
                # Write header
                f.write("Timestamp,MotorID,Type,Weight (g),Thrust (N),Cd,Notes\n")
                
                # Write data
                for log in self.motor_logs:
                    f.write(
                        f"{log['Timestamp']},"
                        f"{log['MotorID']},"
                        f"{log['Type']},"
                        f"{log['Weight (g)']},"
                        f"{log['Thrust (N']},"
                        f"{log['Cd']},"
                        f'"{log["Notes"]}"\n'
                    )
            
            messagebox.showinfo("Success", f"Logs exported to {file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export logs:\n{str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = RocketCalculator(root)
    root.mainloop()
