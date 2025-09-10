"""
Physics Toolkit - A comprehensive desktop application for physics calculations and reference
"""

import tkinter as tk
from tkinter import ttk, messagebox
import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime

class PhysicsToolkit:
    def __init__(self, root):
        self.root = root
        self.root.title("Physics Toolkit")
        self.root.geometry("1200x800")
        
        # Constants
        self.PHYSICAL_CONSTANTS = {
            "c": {"symbol": "c", "name": "Speed of light in vacuum", "value": 299792458, "unit": "m/s", "category": "Fundamental"},
            "G": {"symbol": "G", "name": "Gravitational constant", "value": 6.67430e-11, "unit": "m³/kg·s²", "category": "Fundamental"},
            "h": {"symbol": "h", "name": "Planck constant", "value": 6.62607015e-34, "unit": "J·s", "category": "Quantum"},
            "ħ": {"symbol": "ħ", "name": "Reduced Planck constant", "value": 1.054571817e-34, "unit": "J·s", "category": "Quantum"},
            "k_B": {"symbol": "k_B", "name": "Boltzmann constant", "value": 1.380649e-23, "unit": "J/K", "category": "Thermodynamics"},
            "R": {"symbol": "R", "name": "Molar gas constant", "value": 8.314462618, "unit": "J/mol·K", "category": "Thermodynamics"},
            "N_A": {"symbol": "N_A", "name": "Avogadro constant", "value": 6.02214076e23, "unit": "1/mol", "category": "Thermodynamics"},
            "e": {"symbol": "e", "name": "Elementary charge", "value": 1.602176634e-19, "unit": "C", "category": "Electromagnetism"},
            "μ_0": {"symbol": "μ_0", "name": "Vacuum permeability", "value": 1.25663706212e-6, "unit": "N/A²", "category": "Electromagnetism"},
            "ε_0": {"symbol": "ε_0", "name": "Vacuum permittivity", "value": 8.8541878128e-12, "unit": "F/m", "category": "Electromagnetism"},
            "k_e": {"symbol": "k_e", "name": "Coulomb constant", "value": 8.9875517923e9, "unit": "N·m²/C²", "category": "Electromagnetism"},
            "m_e": {"symbol": "m_e", "name": "Electron mass", "value": 9.1093837015e-31, "unit": "kg", "category": "Particle"},
            "m_p": {"symbol": "m_p", "name": "Proton mass", "value": 1.67262192369e-27, "unit": "kg", "category": "Particle"},
            "m_n": {"symbol": "m_n", "name": "Neutron mass", "value": 1.67492749804e-27, "unit": "kg", "category": "Particle"},
            "g": {"symbol": "g", "name": "Standard gravity", "value": 9.80665, "unit": "m/s²", "category": "Earth Science"}
        }
        
        # Data storage
        self.measurements = []
        self.circuit_components = []
        self.forces = []
        
        # Create tabs
        self.tab_control = ttk.Notebook(root)
        
        # Add tabs
        self.tab_constants = ttk.Frame(self.tab_control)
        self.tab_kinematics = ttk.Frame(self.tab_control)
        self.tab_dynamics = ttk.Frame(self.tab_control)
        self.tab_energy = ttk.Frame(self.tab_control)
        self.tab_waves = ttk.Frame(self.tab_control)
        self.tab_electricity = ttk.Frame(self.tab_control)
        self.tab_measurements = ttk.Frame(self.tab_control)
        self.tab_terminologies = ttk.Frame(self.tab_control)
        
        self.tab_control.add(self.tab_constants, text="Physical Constants")
        self.tab_control.add(self.tab_kinematics, text="Kinematics")
        self.tab_control.add(self.tab_dynamics, text="Dynamics")
        self.tab_control.add(self.tab_energy, text="Energy & Work")
        self.tab_control.add(self.tab_waves, text="Waves & Optics")
        self.tab_control.add(self.tab_electricity, text="Electricity")
        self.tab_control.add(self.tab_measurements, text="Measurements")
        self.tab_control.add(self.tab_terminologies, text="Terminologies")
        
        self.tab_control.pack(expand=1, fill="both")
        
        # Initialize all tabs
        self.init_constants_tab()
        self.init_kinematics_tab()
        self.init_dynamics_tab()
        self.init_energy_tab()
        self.init_waves_tab()
        self.init_electricity_tab()
        self.init_measurements_tab()
        self.init_terminologies_tab()
        
        # Set default tab
        self.tab_control.select(self.tab_constants)
    
    def init_constants_tab(self):
        # Search frame
        search_frame = ttk.LabelFrame(self.tab_constants, text="Search Constants")
        search_frame.pack(pady=10, padx=10, fill="x")
        
        ttk.Label(search_frame, text="Search:").grid(row=0, column=0, padx=5, pady=5)
        self.constant_search_entry = ttk.Entry(search_frame)
        self.constant_search_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        
        ttk.Button(search_frame, text="Search", command=self.search_constant).grid(row=0, column=2, padx=5, pady=5)
        ttk.Button(search_frame, text="Show All", command=self.show_all_constants).grid(row=0, column=3, padx=5, pady=5)
        
        # Constants table
        table_frame = ttk.Frame(self.tab_constants)
        table_frame.pack(pady=10, padx=10, fill="both", expand=True)
        
        # Create treeview with scrollbars
        scroll_y = ttk.Scrollbar(table_frame, orient="vertical")
        scroll_x = ttk.Scrollbar(table_frame, orient="horizontal")
        
        self.constants_tree = ttk.Treeview(
            table_frame, 
            columns=("symbol", "name", "value", "unit", "category"), 
            yscrollcommand=scroll_y.set, 
            xscrollcommand=scroll_x.set
        )
        
        scroll_y.config(command=self.constants_tree.yview)
        scroll_x.config(command=self.constants_tree.xview)
        
        # Define columns
        self.constants_tree.heading("#0", text="#")
        self.constants_tree.heading("symbol", text="Symbol")
        self.constants_tree.heading("name", text="Name")
        self.constants_tree.heading("value", text="Value")
        self.constants_tree.heading("unit", text="Unit")
        self.constants_tree.heading("category", text="Category")
        
        self.constants_tree.column("#0", width=50, minwidth=50)
        self.constants_tree.column("symbol", width=100, minwidth=100)
        self.constants_tree.column("name", width=250, minwidth=150)
        self.constants_tree.column("value", width=150, minwidth=100)
        self.constants_tree.column("unit", width=100, minwidth=80)
        self.constants_tree.column("category", width=150, minwidth=100)
        
        # Pack treeview and scrollbars
        self.constants_tree.grid(row=0, column=0, sticky="nsew")
        scroll_y.grid(row=0, column=1, sticky="ns")
        scroll_x.grid(row=1, column=0, sticky="ew")
        
        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)
        
        # Populate with all constants initially
        self.show_all_constants()
    
    def search_constant(self):
        query = self.constant_search_entry.get().strip().lower()
        if not query:
            self.show_all_constants()
            return
        
        found = {}
        for symbol, constant in self.PHYSICAL_CONSTANTS.items():
            if (query in symbol.lower() or 
                query in constant["name"].lower() or 
                query in constant["category"].lower()):
                found[symbol] = constant
        
        self.display_constants(found)
    
    def show_all_constants(self):
        self.constant_search_entry.delete(0, tk.END)
        self.display_constants(self.PHYSICAL_CONSTANTS)
    
    def display_constants(self, constants):
        # Clear existing items
        for item in self.constants_tree.get_children():
            self.constants_tree.delete(item)
        
        # Add new items
        for i, (symbol, constant) in enumerate(constants.items()):
            self.constants_tree.insert(
                "", "end", text=str(i+1),
                values=(
                    symbol,
                    constant["name"],
                    f"{constant['value']:.4e}",
                    constant["unit"],
                    constant["category"]
                )
            )

    def init_kinematics_tab(self):
        # Main frames
        left_frame = ttk.Frame(self.tab_kinematics)
        left_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        
        right_frame = ttk.Frame(self.tab_kinematics)
        right_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)
        
        # Equation selection
        eq_frame = ttk.LabelFrame(left_frame, text="Kinematics Equation")
        eq_frame.pack(fill="x", padx=5, pady=5)
        
        self.kinematics_eq_var = tk.StringVar()
        self.kinematics_eq_var.set("v_u_at")  # Default equation
        
        eq_options = [
            ("v = u + at", "v_u_at"),
            ("s = ut + ½at²", "s_ut_05at2"),
            ("v² = u² + 2as", "v2_u2_2as"),
            ("s = vt - ½at²", "s_vt_05at2"),
            ("s = ½(u + v)t", "s_05_u_v_t")
        ]
        
        for text, value in eq_options:
            ttk.Radiobutton(
                eq_frame, 
                text=text, 
                variable=self.kinematics_eq_var, 
                value=value,
                command=self.update_kinematics_inputs
            ).pack(anchor="w", padx=5, pady=2)
        
        # Inputs frame
        self.kinematics_inputs_frame = ttk.LabelFrame(left_frame, text="Inputs")
        self.kinematics_inputs_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Variable to find
        self.find_frame = ttk.Frame(self.kinematics_inputs_frame)
        self.find_frame.pack(fill="x", padx=5, pady=5)
        
        ttk.Label(self.find_frame, text="Find:").pack(side="left", padx=5)
        self.kinematics_var_var = tk.StringVar()
        self.kinematics_var_menu = ttk.Combobox(self.find_frame, textvariable=self.kinematics_var_var)
        self.kinematics_var_menu.pack(side="left", padx=5, fill="x", expand=True)
        
        # Input fields will be created by update_kinematics_inputs
        self.kinematics_input_fields = {}
        
        # Buttons
        button_frame = ttk.Frame(left_frame)
        button_frame.pack(fill="x", padx=5, pady=5)
        
        ttk.Button(button_frame, text="Calculate", command=self.calculate_kinematics).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Reset", command=self.reset_kinematics).pack(side="left", padx=5)
        
        # Result
        result_frame = ttk.LabelFrame(left_frame, text="Result")
        result_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        self.kinematics_result = tk.StringVar()
        self.kinematics_result.set("Result will appear here")
        ttk.Label(result_frame, textvariable=self.kinematics_result, wraplength=300).pack(padx=5, pady=5)
        
        # Visualization frame
        vis_frame = ttk.LabelFrame(right_frame, text="Motion Visualization")
        vis_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        button_frame = ttk.Frame(vis_frame)
        button_frame.pack(fill="x", padx=5, pady=5)
        
        ttk.Button(button_frame, text="Plot Motion", command=self.plot_kinematics).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Clear Plot", command=self.clear_kinematics_plot).pack(side="left", padx=5)
        
        # Matplotlib figure
        self.kinematics_fig, self.kinematics_ax = plt.subplots(figsize=(6, 4))
        self.kinematics_canvas = FigureCanvasTkAgg(self.kinematics_fig, master=vis_frame)
        self.kinematics_canvas.get_tk_widget().pack(fill="both", expand=True)
        
        # Initialize inputs
        self.update_kinematics_inputs()
    
    def update_kinematics_inputs(self):
        # Clear existing input fields (except the find frame)
        for widget in self.kinematics_inputs_frame.winfo_children():
            if widget != self.find_frame:
                widget.destroy()
        
        equation = self.kinematics_eq_var.get()
        self.kinematics_input_fields = {}
        
        # Common variables for all equations
        variables = []
        input_widgets = []
        
        if equation == "v_u_at":
            # v = u + at
            variables = ["v", "u", "a", "t"]
            
            input_widgets = [
                ("u", "Initial Velocity (u, m/s):", 0),
                ("a", "Acceleration (a, m/s²):", 0),
                ("t", "Time (t, s):", 0)
            ]
            
        elif equation == "s_ut_05at2":
            # s = ut + ½at²
            variables = ["s", "u", "a", "t"]
            
            input_widgets = [
                ("u", "Initial Velocity (u, m/s):", 0),
                ("a", "Acceleration (a, m/s²):", 0),
                ("t", "Time (t, s):", 0)
            ]
            
        elif equation == "v2_u2_2as":
            # v² = u² + 2as
            variables = ["v", "u", "a", "s"]
            
            input_widgets = [
                ("u", "Initial Velocity (u, m/s):", 0),
                ("a", "Acceleration (a, m/s²):", 0),
                ("s", "Displacement (s, m):", 0)
            ]
            
        elif equation == "s_vt_05at2":
            # s = vt - ½at²
            variables = ["s", "v", "a", "t"]
            
            input_widgets = [
                ("v", "Final Velocity (v, m/s):", 0),
                ("a", "Acceleration (a, m/s²):", 0),
                ("t", "Time (t, s):", 0)
            ]
            
        elif equation == "s_05_u_v_t":
            # s = ½(u + v)t
            variables = ["s", "u", "v", "t"]
            
            input_widgets = [
                ("u", "Initial Velocity (u, m/s):", 0),
                ("v", "Final Velocity (v, m/s):", 0),
                ("t", "Time (t, s):", 0)
            ]
        
        # Update variable selection
        self.kinematics_var_menu['values'] = variables
        self.kinematics_var_var.set(variables[0])
        
        # Create input fields
        for field_id, label_text, default_value in input_widgets:
            frame = ttk.Frame(self.kinematics_inputs_frame)
            frame.pack(fill="x", padx=5, pady=2)
            
            ttk.Label(frame, text=label_text).pack(side="left", padx=5)
            
            var = tk.DoubleVar(value=default_value)
            entry = ttk.Entry(frame, textvariable=var)
            entry.pack(side="right", padx=5, fill="x", expand=True)
            
            self.kinematics_input_fields[field_id] = var
    
    def calculate_kinematics(self):
        equation = self.kinematics_eq_var.get()
        variable = self.kinematics_var_var.get()
        
        try:
            if equation == "v_u_at":
                # v = u + at
                u = self.kinematics_input_fields["u"].get()
                a = self.kinematics_input_fields["a"].get()
                t = self.kinematics_input_fields["t"].get()
                
                if variable == "v":
                    result = u + a * t
                    self.kinematics_result.set(f"Final Velocity (v): {result:.2f} m/s")
                elif variable == "u":
                    result = -a * t  # Assuming v=0 if not provided
                    self.kinematics_result.set(f"Initial Velocity (u): {result:.2f} m/s")
                elif variable == "a":
                    result = -u / t if t != 0 else 0  # Assuming v=0 if not provided
                    self.kinematics_result.set(f"Acceleration (a): {result:.2f} m/s²")
                elif variable == "t":
                    result = -u / a if a != 0 else 0  # Assuming v=0 if not provided
                    self.kinematics_result.set(f"Time (t): {result:.2f} s")
                    
            elif equation == "s_ut_05at2":
                # s = ut + ½at²
                u = self.kinematics_input_fields["u"].get()
                a = self.kinematics_input_fields["a"].get()
                t = self.kinematics_input_fields["t"].get()
                
                if variable == "s":
                    result = u * t + 0.5 * a * t * t
                    self.kinematics_result.set(f"Displacement (s): {result:.2f} m")
                elif variable == "u":
                    s = 0  # Assuming s=0 if not provided
                    result = (s - 0.5 * a * t * t) / t if t != 0 else 0
                    self.kinematics_result.set(f"Initial Velocity (u): {result:.2f} m/s")
                elif variable == "a":
                    s = 0  # Assuming s=0 if not provided
                    result = 2 * (s - u * t) / (t * t) if t != 0 else 0
                    self.kinematics_result.set(f"Acceleration (a): {result:.2f} m/s²")
                elif variable == "t":
                    s = 0  # Assuming s=0 if not provided
                    discriminant = u * u + 2 * a * s
                    if discriminant < 0:
                        raise ValueError("No real solution exists")
                    result = (-u + math.sqrt(discriminant)) / a
                    if result < 0:
                        result = (-u - math.sqrt(discriminant)) / a
                        if result < 0:
                            raise ValueError("No positive time solution exists")
                    self.kinematics_result.set(f"Time (t): {result:.2f} s")
                    
            elif equation == "v2_u2_2as":
                # v² = u² + 2as
                u = self.kinematics_input_fields["u"].get()
                a = self.kinematics_input_fields["a"].get()
                s = self.kinematics_input_fields["s"].get()
                
                if variable == "v":
                    result = math.sqrt(u * u + 2 * a * s)
                    self.kinematics_result.set(f"Final Velocity (v): {result:.2f} m/s")
                elif variable == "u":
                    v = 0  # Assuming v=0 if not provided
                    result = math.sqrt(v * v - 2 * a * s)
                    self.kinematics_result.set(f"Initial Velocity (u): {result:.2f} m/s")
                elif variable == "a":
                    v = 0  # Assuming v=0 if not provided
                    result = (v * v - u * u) / (2 * s) if s != 0 else 0
                    self.kinematics_result.set(f"Acceleration (a): {result:.2f} m/s²")
                elif variable == "s":
                    v = 0  # Assuming v=0 if not provided
                    result = (v * v - u * u) / (2 * a) if a != 0 else 0
                    self.kinematics_result.set(f"Displacement (s): {result:.2f} m")
                    
            elif equation == "s_vt_05at2":
                # s = vt - ½at²
                v = self.kinematics_input_fields["v"].get()
                a = self.kinematics_input_fields["a"].get()
                t = self.kinematics_input_fields["t"].get()
                
                if variable == "s":
                    result = v * t - 0.5 * a * t * t
                    self.kinematics_result.set(f"Displacement (s): {result:.2f} m")
                elif variable == "v":
                    s = 0  # Assuming s=0 if not provided
                    result = (s + 0.5 * a * t * t) / t if t != 0 else 0
                    self.kinematics_result.set(f"Final Velocity (v): {result:.2f} m/s")
                elif variable == "a":
                    s = 0  # Assuming s=0 if not provided
                    result = 2 * (v * t - s) / (t * t) if t != 0 else 0
                    self.kinematics_result.set(f"Acceleration (a): {result:.2f} m/s²")
                elif variable == "t":
                    s = 0  # Assuming s=0 if not provided
                    discriminant = v * v - 2 * a * s
                    if discriminant < 0:
                        raise ValueError("No real solution exists")
                    result = (v + math.sqrt(discriminant)) / a
                    if result < 0:
                        result = (v - math.sqrt(discriminant)) / a
                        if result < 0:
                            raise ValueError("No positive time solution exists")
                    self.kinematics_result.set(f"Time (t): {result:.2f} s")
                    
            elif equation == "s_05_u_v_t":
                # s = ½(u + v)t
                u = self.kinematics_input_fields["u"].get()
                v = self.kinematics_input_fields["v"].get()
                t = self.kinematics_input_fields["t"].get()
                
                if variable == "s":
                    result = 0.5 * (u + v) * t
                    self.kinematics_result.set(f"Displacement (s): {result:.2f} m")
                elif variable == "u":
                    s = 0  # Assuming s=0 if not provided
                    result = (2 * s / t) - v if t != 0 else 0
                    self.kinematics_result.set(f"Initial Velocity (u): {result:.2f} m/s")
                elif variable == "v":
                    s = 0  # Assuming s=0 if not provided
                    result = (2 * s / t) - u if t != 0 else 0
                    self.kinematics_result.set(f"Final Velocity (v): {result:.2f} m/s")
                elif variable == "t":
                    s = 0  # Assuming s=0 if not provided
                    result = 2 * s / (u + v) if (u + v) != 0 else 0
                    self.kinematics_result.set(f"Time (t): {result:.2f} s")
                    
        except Exception as e:
            self.kinematics_result.set(f"Error: {str(e)}")
    
    def plot_kinematics(self):
        equation = self.kinematics_eq_var.get()
        
        try:
            self.kinematics_ax.clear()
            
            if equation == "v_u_at":
                # v = u + at
                u = self.kinematics_input_fields["u"].get()
                a = self.kinematics_input_fields["a"].get()
                t_max = self.kinematics_input_fields["t"].get() or 10
                
                times = np.linspace(0, t_max, 100)
                velocities = u + a * times
                
                self.kinematics_ax.plot(times, velocities, label='Velocity (m/s)')
                self.kinematics_ax.set_xlabel('Time (s)')
                self.kinematics_ax.set_ylabel('Velocity (m/s)')
                self.kinematics_ax.set_title('Velocity vs Time')
                
            elif equation == "s_ut_05at2":
                # s = ut + ½at²
                u = self.kinematics_input_fields["u"].get()
                a = self.kinematics_input_fields["a"].get()
                t_max = self.kinematics_input_fields["t"].get() or 10
                
                times = np.linspace(0, t_max, 100)
                displacements = u * times + 0.5 * a * times * times
                
                self.kinematics_ax.plot(times, displacements, label='Displacement (m)')
                self.kinematics_ax.set_xlabel('Time (s)')
                self.kinematics_ax.set_ylabel('Displacement (m)')
                self.kinematics_ax.set_title('Displacement vs Time')
                
            else:
                raise ValueError("Plotting not available for this equation")
            
            self.kinematics_ax.legend()
            self.kinematics_ax.grid(True)
            self.kinematics_canvas.draw()
            
        except Exception as e:
            self.kinematics_result.set(f"Plot Error: {str(e)}")
    
    def clear_kinematics_plot(self):
        self.kinematics_ax.clear()
        self.kinematics_canvas.draw()
    
    def reset_kinematics(self):
        self.kinematics_result.set("Result will appear here")
        self.update_kinematics_inputs()
        self.clear_kinematics_plot()

    def init_dynamics_tab(self):
        # Main frames
        left_frame = ttk.Frame(self.tab_dynamics)
        left_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        
        right_frame = ttk.Frame(self.tab_dynamics)
        right_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)
        
        # Equation selection
        eq_frame = ttk.LabelFrame(left_frame, text="Dynamics Equation")
        eq_frame.pack(fill="x", padx=5, pady=5)
        
        self.dynamics_eq_var = tk.StringVar()
        self.dynamics_eq_var.set("newton2")  # Default equation
        
        eq_options = [
            ("F = ma (Newton's Second Law)", "newton2"),
            ("Friction (F = μN)", "friction"),
            ("Centripetal Force (F = mv²/r)", "centripetal"),
            ("Gravitation (F = Gm₁m₂/r²)", "gravitation"),
            ("Momentum (p = mv)", "momentum"),
            ("Impulse (J = FΔt)", "impulse")
        ]
        
        for text, value in eq_options:
            ttk.Radiobutton(
                eq_frame, 
                text=text, 
                variable=self.dynamics_eq_var, 
                value=value,
                command=self.update_dynamics_inputs
            ).pack(anchor="w", padx=5, pady=2)
        
        # Inputs frame
        self.dynamics_inputs_frame = ttk.LabelFrame(left_frame, text="Inputs")
        self.dynamics_inputs_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Variable to find
        self.dynamics_find_frame = ttk.Frame(self.dynamics_inputs_frame)
        self.dynamics_find_frame.pack(fill="x", padx=5, pady=5)
        
        ttk.Label(self.dynamics_find_frame, text="Find:").pack(side="left", padx=5)
        self.dynamics_var_var = tk.StringVar()
        self.dynamics_var_menu = ttk.Combobox(self.dynamics_find_frame, textvariable=self.dynamics_var_var)
        self.dynamics_var_menu.pack(side="left", padx=5, fill="x", expand=True)
        
        # Input fields will be created by update_dynamics_inputs
        self.dynamics_input_fields = {}
        
        # Buttons
        button_frame = ttk.Frame(left_frame)
        button_frame.pack(fill="x", padx=5, pady=5)
        
        ttk.Button(button_frame, text="Calculate", command=self.calculate_dynamics).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Reset", command=self.reset_dynamics).pack(side="left", padx=5)
        
        # Result
        result_frame = ttk.LabelFrame(left_frame, text="Result")
        result_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        self.dynamics_result = tk.StringVar()
        self.dynamics_result.set("Result will appear here")
        ttk.Label(result_frame, textvariable=self.dynamics_result, wraplength=300).pack(padx=5, pady=5)
        
        # Free body diagram frame
        fbd_frame = ttk.LabelFrame(right_frame, text="Free Body Diagram")
        fbd_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Force table
        columns = ("name", "magnitude", "angle", "actions")
        self.forces_tree = ttk.Treeview(fbd_frame, columns=columns, show="headings", height=5)
        
        self.forces_tree.heading("name", text="Name")
        self.forces_tree.heading("magnitude", text="Magnitude (N)")
        self.forces_tree.heading("angle", text="Angle (°)")
        self.forces_tree.heading("actions", text="Actions")
        
        self.forces_tree.column("name", width=100, anchor=tk.CENTER)
        self.forces_tree.column("magnitude", width=100, anchor=tk.CENTER)
        self.forces_tree.column("angle", width=100, anchor=tk.CENTER)
        self.forces_tree.column("actions", width=100, anchor=tk.CENTER)
        
        self.forces_tree.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Buttons for force management
        force_button_frame = ttk.Frame(fbd_frame)
        force_button_frame.pack(fill="x", padx=5, pady=5)
        
        ttk.Button(force_button_frame, text="Add Force", command=self.add_force_dialog).pack(side="left", padx=5)
        ttk.Button(force_button_frame, text="Clear All", command=self.clear_forces).pack(side="left", padx=5)
        
        # Net force calculation
        net_force_frame = ttk.Frame(fbd_frame)
        net_force_frame.pack(fill="x", padx=5, pady=5)
        
        ttk.Button(net_force_frame, text="Calculate Net Force", command=self.calculate_net_force).pack(pady=5)
        
        # Net force result
        net_result_frame = ttk.LabelFrame(fbd_frame, text="Net Force Result")
        net_result_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        self.net_force_result = tk.StringVar()
        self.net_force_result.set("Net force will appear here")
        ttk.Label(net_result_frame, textvariable=self.net_force_result, wraplength=300).pack(padx=5, pady=5)
        
        # Initialize inputs
        self.update_dynamics_inputs()
    
    def update_dynamics_inputs(self):
        # Clear existing input fields (except the find frame)
        for widget in self.dynamics_inputs_frame.winfo_children():
            if widget != self.dynamics_find_frame:
                widget.destroy()
        
        equation = self.dynamics_eq_var.get()
        self.dynamics_input_fields = {}
        
        # Common variables for all equations
        variables = []
        input_widgets = []
        
        if equation == "newton2":
            # F = ma
            variables = ["F", "m", "a"]
            
            input_widgets = [
                ("F", "Force (F, N):", 0),
                ("m", "Mass (m, kg):", 0),
                ("a", "Acceleration (a, m/s²):", 0)
            ]
            
        elif equation == "friction":
            # Friction (F = μN)
            variables = ["F", "μ", "N"]
            
            input_widgets = [
                ("F", "Friction Force (F, N):", 0),
                ("μ", "Coefficient of Friction (μ):", 0),
                ("N", "Normal Force (N, N):", 0)
            ]
            
        elif equation == "centripetal":
            # Centripetal Force (F = mv²/r)
            variables = ["F", "m", "v", "r"]
            
            input_widgets = [
                ("F", "Centripetal Force (F, N):", 0),
                ("m", "Mass (m, kg):", 0),
                ("v", "Velocity (v, m/s):", 0),
                ("r", "Radius (r, m):", 0)
            ]
            
        elif equation == "gravitation":
            # Gravitation (F = Gm₁m₂/r²)
            variables = ["F", "m1", "m2", "r"]
            
            input_widgets = [
                ("F", "Gravitational Force (F, N):", 0),
                ("m1", "Mass 1 (m₁, kg):", 0),
                ("m2", "Mass 2 (m₂, kg):", 0),
                ("r", "Distance (r, m):", 0)
            ]
            
        elif equation == "momentum":
            # Momentum (p = mv)
            variables = ["p", "m", "v"]
            
            input_widgets = [
                ("p", "Momentum (p, kg·m/s):", 0),
                ("m", "Mass (m, kg):", 0),
                ("v", "Velocity (v, m/s):", 0)
            ]
            
        elif equation == "impulse":
            # Impulse (J = FΔt)
            variables = ["J", "F", "Δt"]
            
            input_widgets = [
                ("J", "Impulse (J, N·s):", 0),
                ("F", "Force (F, N):", 0),
                ("Δt", "Time Interval (Δt, s):", 0)
            ]
        
        # Update variable selection
        self.dynamics_var_menu['values'] = variables
        self.dynamics_var_var.set(variables[0])
        
        # Create input fields
        for field_id, label_text, default_value in input_widgets:
            frame = ttk.Frame(self.dynamics_inputs_frame)
            frame.pack(fill="x", padx=5, pady=2)
            
            ttk.Label(frame, text=label_text).pack(side="left", padx=5)
            
            var = tk.DoubleVar(value=default_value)
            entry = ttk.Entry(frame, textvariable=var)
            entry.pack(side="right", padx=5, fill="x", expand=True)
            
            self.dynamics_input_fields[field_id] = var
    
    def calculate_dynamics(self):
        equation = self.dynamics_eq_var.get()
        variable = self.dynamics_var_var.get()
        
        try:
            if equation == "newton2":
                # F = ma
                F = self.dynamics_input_fields["F"].get()
                m = self.dynamics_input_fields["m"].get()
                a = self.dynamics_input_fields["a"].get()
                
                if variable == "F":
                    result = m * a
                    self.dynamics_result.set(f"Force (F): {result:.2f} N")
                elif variable == "m":
                    result = F / a if a != 0 else 0
                    self.dynamics_result.set(f"Mass (m): {result:.2f} kg")
                elif variable == "a":
                    result = F / m if m != 0 else 0
                    self.dynamics_result.set(f"Acceleration (a): {result:.2f} m/s²")
                    
            elif equation == "friction":
                # Friction (F = μN)
                F = self.dynamics_input_fields["F"].get()
                μ = self.dynamics_input_fields["μ"].get()
                N = self.dynamics_input_fields["N"].get()
                
                if variable == "F":
                    result = μ * N
                    self.dynamics_result.set(f"Friction Force (F): {result:.2f} N")
                elif variable == "μ":
                    result = F / N if N != 0 else 0
                    self.dynamics_result.set(f"Coefficient of Friction (μ): {result:.2f}")
                elif variable == "N":
                    result = F / μ if μ != 0 else 0
                    self.dynamics_result.set(f"Normal Force (N): {result:.2f} N")
                    
            elif equation == "centripetal":
                # Centripetal Force (F = mv²/r)
                F = self.dynamics_input_fields["F"].get()
                m = self.dynamics_input_fields["m"].get()
                v = self.dynamics_input_fields["v"].get()
                r = self.dynamics_input_fields["r"].get()
                
                if variable == "F":
                    result = m * v * v / r if r != 0 else 0
                    self.dynamics_result.set(f"Centripetal Force (F): {result:.2f} N")
                elif variable == "m":
                    result = F * r / (v * v) if v != 0 else 0
                    self.dynamics_result.set(f"Mass (m): {result:.2f} kg")
                elif variable == "v":
                    result = math.sqrt(F * r / m) if m != 0 else 0
                    self.dynamics_result.set(f"Velocity (v): {result:.2f} m/s")
                elif variable == "r":
                    result = m * v * v / F if F != 0 else 0
                    self.dynamics_result.set(f"Radius (r): {result:.2f} m")
                    
            elif equation == "gravitation":
                # Gravitation (F = Gm₁m₂/r²)
                F = self.dynamics_input_fields["F"].get()
                m1 = self.dynamics_input_fields["m1"].get()
                m2 = self.dynamics_input_fields["m2"].get()
                r = self.dynamics_input_fields["r"].get()
                
                if variable == "F":
                    result = 6.67430e-11 * m1 * m2 / (r * r) if r != 0 else 0
                    self.dynamics_result.set(f"Gravitational Force (F): {result:.2e} N")
                elif variable == "m1":
                    result = F * r * r / (6.67430e-11 * m2) if m2 != 0 else 0
                    self.dynamics_result.set(f"Mass 1 (m₁): {result:.2f} kg")
                elif variable == "m2":
                    result = F * r * r / (6.67430e-11 * m1) if m1 != 0 else 0
                    self.dynamics_result.set(f"Mass 2 (m₂): {result:.2f} kg")
                elif variable == "r":
                    result = math.sqrt(6.67430e-11 * m1 * m2 / F) if F != 0 else 0
                    self.dynamics_result.set(f"Distance (r): {result:.2f} m")
                    
            elif equation == "momentum":
                # Momentum (p = mv)
                p = self.dynamics_input_fields["p"].get()
                m = self.dynamics_input_fields["m"].get()
                v = self.dynamics_input_fields["v"].get()
                
                if variable == "p":
                    result = m * v
                    self.dynamics_result.set(f"Momentum (p): {result:.2f} kg·m/s")
                elif variable == "m":
                    result = p / v if v != 0 else 0
                    self.dynamics_result.set(f"Mass (m): {result:.2f} kg")
                elif variable == "v":
                    result = p / m if m != 0 else 0
                    self.dynamics_result.set(f"Velocity (v): {result:.2f} m/s")
                    
            elif equation == "impulse":
                # Impulse (J = FΔt)
                J = self.dynamics_input_fields["J"].get()
                F = self.dynamics_input_fields["F"].get()
                Δt = self.dynamics_input_fields["Δt"].get()
                
                if variable == "J":
                    result = F * Δt
                    self.dynamics_result.set(f"Impulse (J): {result:.2f} N·s")
                elif variable == "F":
                    result = J / Δt if Δt != 0 else 0
                    self.dynamics_result.set(f"Force (F): {result:.2f} N")
                elif variable == "Δt":
                    result = J / F if F != 0 else 0
                    self.dynamics_result.set(f"Time Interval (Δt): {result:.2f} s")
                    
        except Exception as e:
            self.dynamics_result.set(f"Error: {str(e)}")
    
    def reset_dynamics(self):
        self.dynamics_result.set("Result will appear here")
        self.update_dynamics_inputs()
    
    def add_force_dialog(self):
        # Create a dialog to add a new force
        dialog = tk.Toplevel(self.root)
        dialog.title("Add Force")
        dialog.geometry("300x200")
        dialog.transient(self.root)
        dialog.grab_set()
        
        ttk.Label(dialog, text="Force Name:").pack(pady=5)
        name_var = tk.StringVar()
        ttk.Entry(dialog, textvariable=name_var).pack(pady=5)
        
        ttk.Label(dialog, text="Magnitude (N):").pack(pady=5)
        magnitude_var = tk.DoubleVar()
        ttk.Entry(dialog, textvariable=magnitude_var).pack(pady=5)
        
        ttk.Label(dialog, text="Angle (degrees):").pack(pady=5)
        angle_var = tk.DoubleVar()
        ttk.Entry(dialog, textvariable=angle_var).pack(pady=5)
        
        def save_force():
            self.forces.append({
                "name": name_var.get(),
                "magnitude": magnitude_var.get(),
                "angle": angle_var.get()
            })
            self.update_forces_table()
            dialog.destroy()
        
        ttk.Button(dialog, text="Save", command=save_force).pack(pady=10)
    
    def update_forces_table(self):
        # Clear existing items
        for item in self.forces_tree.get_children():
            self.forces_tree.delete(item)
        
        # Add new items
        for i, force in enumerate(self.forces):
            self.forces_tree.insert(
                "", "end", 
                values=(
                    force["name"],
                    f"{force['magnitude']:.2f}",
                    f"{force['angle']:.2f}",
                    "Delete"
                ),
                tags=(i,)
            )
        
        # Bind delete action
        self.forces_tree.bind("<ButtonRelease-1>", self.on_force_click)
    
    def on_force_click(self, event):
        region = self.forces_tree.identify("region", event.x, event.y)
        if region == "cell":
            column = self.forces_tree.identify_column(event.x)
            item = self.forces_tree.identify_row(event.y)
            
            if column == "#4":  # Actions column
                index = int(self.forces_tree.item(item, "tags")[0])
                self.forces.pop(index)
                self.update_forces_table()
    
    def clear_forces(self):
        self.forces = []
        self.update_forces_table()
    
    def calculate_net_force(self):
        if not self.forces:
            self.net_force_result.set("No forces to calculate")
            return
        
        try:
            # Calculate net force components
            fx_total = 0
            fy_total = 0
            
            for force in self.forces:
                magnitude = force["magnitude"]
                angle_rad = math.radians(force["angle"])
                fx_total += magnitude * math.cos(angle_rad)
                fy_total += magnitude * math.sin(angle_rad)
            
            # Calculate magnitude and direction
            net_magnitude = math.sqrt(fx_total**2 + fy_total**2)
            net_angle_rad = math.atan2(fy_total, fx_total)
            net_angle_deg = math.degrees(net_angle_rad)
            
            self.net_force_result.set(
                f"Net Force: {net_magnitude:.2f} N at {net_angle_deg:.2f}°\n"
                f"X-component: {fx_total:.2f} N\n"
                f"Y-component: {fy_total:.2f} N"
            )
            
        except Exception as e:
            self.net_force_result.set(f"Error: {str(e)}")

    def init_energy_tab(self):
        # Main frames
        left_frame = ttk.Frame(self.tab_energy)
        left_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        
        right_frame = ttk.Frame(self.tab_energy)
        right_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)
        
        # Equation selection
        eq_frame = ttk.LabelFrame(left_frame, text="Energy & Work Equation")
        eq_frame.pack(fill="x", padx=5, pady=5)
        
        self.energy_eq_var = tk.StringVar()
        self.energy_eq_var.set("ke")  # Default equation
        
        eq_options = [
            ("Kinetic Energy (KE = ½mv²)", "ke"),
            ("Potential Energy (PE = mgh)", "pe"),
            ("Work (W = Fd cosθ)", "work"),
            ("Power (P = W/t)", "power"),
            ("Spring Energy (E = ½kx²)", "spring"),
            ("Conservation of Energy", "conservation")
        ]
        
        for text, value in eq_options:
            ttk.Radiobutton(
                eq_frame, 
                text=text, 
                variable=self.energy_eq_var, 
                value=value,
                command=self.update_energy_inputs
            ).pack(anchor="w", padx=5, pady=2)
        
        # Inputs frame
        self.energy_inputs_frame = ttk.LabelFrame(left_frame, text="Inputs")
        self.energy_inputs_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Variable to find
        self.energy_find_frame = ttk.Frame(self.energy_inputs_frame)
        self.energy_find_frame.pack(fill="x", padx=5, pady=5)
        
        ttk.Label(self.energy_find_frame, text="Find:").pack(side="left", padx=5)
        self.energy_var_var = tk.StringVar()
        self.energy_var_menu = ttk.Combobox(self.energy_find_frame, textvariable=self.energy_var_var)
        self.energy_var_menu.pack(side="left", padx=5, fill="x", expand=True)
        
        # Input fields will be created by update_energy_inputs
        self.energy_input_fields = {}
        
        # Buttons
        button_frame = ttk.Frame(left_frame)
        button_frame.pack(fill="x", padx=5, pady=5)
        
        ttk.Button(button_frame, text="Calculate", command=self.calculate_energy).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Reset", command=self.reset_energy).pack(side="left", padx=5)
        
        # Result
        result_frame = ttk.LabelFrame(left_frame, text="Result")
        result_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        self.energy_result = tk.StringVar()
        self.energy_result.set("Result will appear here")
        ttk.Label(result_frame, textvariable=self.energy_result, wraplength=300).pack(padx=5, pady=5)
        
        # Energy conservation visualization
        vis_frame = ttk.LabelFrame(right_frame, text="Energy Visualization")
        vis_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        button_frame = ttk.Frame(vis_frame)
        button_frame.pack(fill="x", padx=5, pady=5)
        
        ttk.Button(button_frame, text="Plot Energy", command=self.plot_energy).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Clear Plot", command=self.clear_energy_plot).pack(side="left", padx=5)
        
        # Matplotlib figure
        self.energy_fig, self.energy_ax = plt.subplots(figsize=(6, 4))
        self.energy_canvas = FigureCanvasTkAgg(self.energy_fig, master=vis_frame)
        self.energy_canvas.get_tk_widget().pack(fill="both", expand=True)
        
        # Initialize inputs
        self.update_energy_inputs()
    
    def update_energy_inputs(self):
        # Clear existing input fields (except the find frame)
        for widget in self.energy_inputs_frame.winfo_children():
            if widget != self.energy_find_frame:
                widget.destroy()
        
        equation = self.energy_eq_var.get()
        self.energy_input_fields = {}
        
        # Common variables for all equations
        variables = []
        input_widgets = []
        
        if equation == "ke":
            # Kinetic Energy (KE = ½mv²)
            variables = ["KE", "m", "v"]
            
            input_widgets = [
                ("KE", "Kinetic Energy (KE, J):", 0),
                ("m", "Mass (m, kg):", 0),
                ("v", "Velocity (v, m/s):", 0)
            ]
            
        elif equation == "pe":
            # Potential Energy (PE = mgh)
            variables = ["PE", "m", "g", "h"]
            
            input_widgets = [
                ("PE", "Potential Energy (PE, J):", 0),
                ("m", "Mass (m, kg):", 0),
                ("g", "Gravity (g, m/s²):", 9.81),
                ("h", "Height (h, m):", 0)
            ]
            
        elif equation == "work":
            # Work (W = Fd cosθ)
            variables = ["W", "F", "d", "θ"]
            
            input_widgets = [
                ("W", "Work (W, J):", 0),
                ("F", "Force (F, N):", 0),
                ("d", "Distance (d, m):", 0),
                ("θ", "Angle (θ, °):", 0)
            ]
            
        elif equation == "power":
            # Power (P = W/t)
            variables = ["P", "W", "t"]
            
            input_widgets = [
                ("P", "Power (P, W):", 0),
                ("W", "Work (W, J):", 0),
                ("t", "Time (t, s):", 0)
            ]
            
        elif equation == "spring":
            # Spring Energy (E = ½kx²)
            variables = ["E", "k", "x"]
            
            input_widgets = [
                ("E", "Spring Energy (E, J):", 0),
                ("k", "Spring Constant (k, N/m):", 0),
                ("x", "Displacement (x, m):", 0)
            ]
            
        elif equation == "conservation":
            # Conservation of Energy
            variables = ["KE_i", "PE_i", "KE_f", "PE_f"]
            
            input_widgets = [
                ("KE_i", "Initial Kinetic Energy (KE_i, J):", 0),
                ("PE_i", "Initial Potential Energy (PE_i, J):", 0),
                ("KE_f", "Final Kinetic Energy (KE_f, J):", 0),
                ("PE_f", "Final Potential Energy (PE_f, J):", 0)
            ]
        
        # Update variable selection
        self.energy_var_menu['values'] = variables
        self.energy_var_var.set(variables[0])
        
        # Create input fields
        for field_id, label_text, default_value in input_widgets:
            frame = ttk.Frame(self.energy_inputs_frame)
            frame.pack(fill="x", padx=5, pady=2)
            
            ttk.Label(frame, text=label_text).pack(side="left", padx=5)
            
            var = tk.DoubleVar(value=default_value)
            entry = ttk.Entry(frame, textvariable=var)
            entry.pack(side="right", padx=5, fill="x", expand=True)
            
            self.energy_input_fields[field_id] = var
    
    def calculate_energy(self):
        equation = self.energy_eq_var.get()
        variable = self.energy_var_var.get()
        
        try:
            if equation == "ke":
                # Kinetic Energy (KE = ½mv²)
                KE = self.energy_input_fields["KE"].get()
                m = self.energy_input_fields["m"].get()
                v = self.energy_input_fields["v"].get()
                
                if variable == "KE":
                    result = 0.5 * m * v * v
                    self.energy_result.set(f"Kinetic Energy (KE): {result:.2f} J")
                elif variable == "m":
                    result = 2 * KE / (v * v) if v != 0 else 0
                    self.energy_result.set(f"Mass (m): {result:.2f} kg")
                elif variable == "v":
                    result = math.sqrt(2 * KE / m) if m != 0 else 0
                    self.energy_result.set(f"Velocity (v): {result:.2f} m/s")
                    
            elif equation == "pe":
                # Potential Energy (PE = mgh)
                PE = self.energy_input_fields["PE"].get()
                m = self.energy_input_fields["m"].get()
                g = self.energy_input_fields["g"].get()
                h = self.energy_input_fields["h"].get()
                
                if variable == "PE":
                    result = m * g * h
                    self.energy_result.set(f"Potential Energy (PE): {result:.2f} J")
                elif variable == "m":
                    result = PE / (g * h) if (g * h) != 0 else 0
                    self.energy_result.set(f"Mass (m): {result:.2f} kg")
                elif variable == "g":
                    result = PE / (m * h) if (m * h) != 0 else 0
                    self.energy_result.set(f"Gravity (g): {result:.2f} m/s²")
                elif variable == "h":
                    result = PE / (m * g) if (m * g) != 0 else 0
                    self.energy_result.set(f"Height (h): {result:.2f} m")
                    
            elif equation == "work":
                # Work (W = Fd cosθ)
                W = self.energy_input_fields["W"].get()
                F = self.energy_input_fields["F"].get()
                d = self.energy_input_fields["d"].get()
                θ = self.energy_input_fields["θ"].get()
                
                if variable == "W":
                    result = F * d * math.cos(math.radians(θ))
                    self.energy_result.set(f"Work (W): {result:.2f} J")
                elif variable == "F":
                    result = W / (d * math.cos(math.radians(θ))) if (d * math.cos(math.radians(θ))) != 0 else 0
                    self.energy_result.set(f"Force (F): {result:.2f} N")
                elif variable == "d":
                    result = W / (F * math.cos(math.radians(θ))) if (F * math.cos(math.radians(θ))) != 0 else 0
                    self.energy_result.set(f"Distance (d): {result:.2f} m")
                elif variable == "θ":
                    result = math.degrees(math.acos(W / (F * d))) if (F * d) != 0 else 0
                    self.energy_result.set(f"Angle (θ): {result:.2f} °")
                    
            elif equation == "power":
                # Power (P = W/t)
                P = self.energy_input_fields["P"].get()
                W = self.energy_input_fields["W"].get()
                t = self.energy_input_fields["t"].get()
                
                if variable == "P":
                    result = W / t if t != 0 else 0
                    self.energy_result.set(f"Power (P): {result:.2f} W")
                elif variable == "W":
                    result = P * t
                    self.energy_result.set(f"Work (W): {result:.2f} J")
                elif variable == "t":
                    result = W / P if P != 0 else 0
                    self.energy_result.set(f"Time (t): {result:.2f} s")
                    
            elif equation == "spring":
                # Spring Energy (E = ½kx²)
                E = self.energy_input_fields["E"].get()
                k = self.energy_input_fields["k"].get()
                x = self.energy_input_fields["x"].get()
                
                if variable == "E":
                    result = 0.5 * k * x * x
                    self.energy_result.set(f"Spring Energy (E): {result:.2f} J")
                elif variable == "k":
                    result = 2 * E / (x * x) if x != 0 else 0
                    self.energy_result.set(f"Spring Constant (k): {result:.2f} N/m")
                elif variable == "x":
                    result = math.sqrt(2 * E / k) if k != 0 else 0
                    self.energy_result.set(f"Displacement (x): {result:.2f} m")
                    
            elif equation == "conservation":
                # Conservation of Energy
                KE_i = self.energy_input_fields["KE_i"].get()
                PE_i = self.energy_input_fields["PE_i"].get()
                KE_f = self.energy_input_fields["KE_f"].get()
                PE_f = self.energy_input_fields["PE_f"].get()
                
                if variable == "KE_i":
                    result = (KE_f + PE_f) - PE_i
                    self.energy_result.set(f"Initial Kinetic Energy (KE_i): {result:.2f} J")
                elif variable == "PE_i":
                    result = (KE_f + PE_f) - KE_i
                    self.energy_result.set(f"Initial Potential Energy (PE_i): {result:.2f} J")
                elif variable == "KE_f":
                    result = (KE_i + PE_i) - PE_f
                    self.energy_result.set(f"Final Kinetic Energy (KE_f): {result:.2f} J")
                elif variable == "PE_f":
                    result = (KE_i + PE_i) - KE_f
                    self.energy_result.set(f"Final Potential Energy (PE_f): {result:.2f} J")
                    
        except Exception as e:
            self.energy_result.set(f"Error: {str(e)}")
    
    def plot_energy(self):
        equation = self.energy_eq_var.get()
        
        try:
            self.energy_ax.clear()
            
            if equation == "ke":
                # Kinetic Energy (KE = ½mv²)
                m = self.energy_input_fields["m"].get() or 1
                v_max = 10
                
                velocities = np.linspace(0, v_max, 100)
                energies = 0.5 * m * velocities * velocities
                
                self.energy_ax.plot(velocities, energies, label='Kinetic Energy (J)')
                self.energy_ax.set_xlabel('Velocity (m/s)')
                self.energy_ax.set_ylabel('Energy (J)')
                self.energy_ax.set_title('Kinetic Energy vs Velocity')
                
            elif equation == "pe":
                # Potential Energy (PE = mgh)
                m = self.energy_input_fields["m"].get() or 1
                g = self.energy_input_fields["g"].get() or 9.81
                h_max = 10
                
                heights = np.linspace(0, h_max, 100)
                energies = m * g * heights
                
                self.energy_ax.plot(heights, energies, label='Potential Energy (J)')
                self.energy_ax.set_xlabel('Height (m)')
                self.energy_ax.set_ylabel('Energy (J)')
                self.energy_ax.set_title('Potential Energy vs Height')
                
            elif equation == "spring":
                # Spring Energy (E = ½kx²)
                k = self.energy_input_fields["k"].get() or 1
                x_max = 5
                
                displacements = np.linspace(-x_max, x_max, 100)
                energies = 0.5 * k * displacements * displacements
                
                self.energy_ax.plot(displacements, energies, label='Spring Energy (J)')
                self.energy_ax.set_xlabel('Displacement (m)')
                self.energy_ax.set_ylabel('Energy (J)')
                self.energy_ax.set_title('Spring Energy vs Displacement')
                
            else:
                raise ValueError("Plotting not available for this equation")
            
            self.energy_ax.legend()
            self.energy_ax.grid(True)
            self.energy_canvas.draw()
            
        except Exception as e:
            self.energy_result.set(f"Plot Error: {str(e)}")
    
    def clear_energy_plot(self):
        self.energy_ax.clear()
        self.energy_canvas.draw()
    
    def reset_energy(self):
        self.energy_result.set("Result will appear here")
        self.update_energy_inputs()
        self.clear_energy_plot()

    def init_waves_tab(self):
        # Main frames
        left_frame = ttk.Frame(self.tab_waves)
        left_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        
        right_frame = ttk.Frame(self.tab_waves)
        right_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)
        
        # Equation selection
        eq_frame = ttk.LabelFrame(left_frame, text="Waves & Optics Equation")
        eq_frame.pack(fill="x", padx=5, pady=5)
        
        self.waves_eq_var = tk.StringVar()
        self.waves_eq_var.set("wave_speed")  # Default equation
        
        eq_options = [
            ("Wave Speed (v = fλ)", "wave_speed"),
            ("Frequency (f = 1/T)", "frequency"),
            ("Snell's Law (n₁sinθ₁ = n₂sinθ₂)", "snell"),
            ("Thin Lens (1/f = 1/d₀ + 1/dᵢ)", "thin_lens"),
            ("Doppler Effect", "doppler"),
            ("Interference (d sinθ = mλ)", "interference")
        ]
        
        for text, value in eq_options:
            ttk.Radiobutton(
                eq_frame, 
                text=text, 
                variable=self.waves_eq_var, 
                value=value,
                command=self.update_waves_inputs
            ).pack(anchor="w", padx=5, pady=2)
        
        # Inputs frame
        self.waves_inputs_frame = ttk.LabelFrame(left_frame, text="Inputs")
        self.waves_inputs_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Variable to find
        self.waves_find_frame = ttk.Frame(self.waves_inputs_frame)
        self.waves_find_frame.pack(fill="x", padx=5, pady=5)
        
        ttk.Label(self.waves_find_frame, text="Find:").pack(side="left", padx=5)
        self.waves_var_var = tk.StringVar()
        self.waves_var_menu = ttk.Combobox(self.waves_find_frame, textvariable=self.waves_var_var)
        self.waves_var_menu.pack(side="left", padx=5, fill="x", expand=True)
        
        # Input fields will be created by update_waves_inputs
        self.waves_input_fields = {}
        
        # Buttons
        button_frame = ttk.Frame(left_frame)
        button_frame.pack(fill="x", padx=5, pady=5)
        
        ttk.Button(button_frame, text="Calculate", command=self.calculate_waves).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Reset", command=self.reset_waves).pack(side="left", padx=5)
        
        # Result
        result_frame = ttk.LabelFrame(left_frame, text="Result")
        result_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        self.waves_result = tk.StringVar()
        self.waves_result.set("Result will appear here")
        ttk.Label(result_frame, textvariable=self.waves_result, wraplength=300).pack(padx=5, pady=5)
        
        # Wave visualization
        vis_frame = ttk.LabelFrame(right_frame, text="Wave Visualization")
        vis_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        button_frame = ttk.Frame(vis_frame)
        button_frame.pack(fill="x", padx=5, pady=5)
        
        ttk.Button(button_frame, text="Plot Wave", command=self.plot_wave).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Clear Plot", command=self.clear_wave_plot).pack(side="left", padx=5)
        
        # Matplotlib figure
        self.wave_fig, self.wave_ax = plt.subplots(figsize=(6, 4))
        self.wave_canvas = FigureCanvasTkAgg(self.wave_fig, master=vis_frame)
        self.wave_canvas.get_tk_widget().pack(fill="both", expand=True)
        
        # Initialize inputs
        self.update_waves_inputs()
    
    def update_waves_inputs(self):
        # Clear existing input fields (except the find frame)
        for widget in self.waves_inputs_frame.winfo_children():
            if widget != self.waves_find_frame:
                widget.destroy()
        
        equation = self.waves_eq_var.get()
        self.waves_input_fields = {}
        
        # Common variables for all equations
        variables = []
        input_widgets = []
        
        if equation == "wave_speed":
            # Wave Speed (v = fλ)
            variables = ["v", "f", "λ"]
            
            input_widgets = [
                ("v", "Wave Speed (v, m/s):", 0),
                ("f", "Frequency (f, Hz):", 0),
                ("λ", "Wavelength (λ, m):", 0)
            ]
            
        elif equation == "frequency":
            # Frequency (f = 1/T)
            variables = ["f", "T"]
            
            input_widgets = [
                ("f", "Frequency (f, Hz):", 0),
                ("T", "Period (T, s):", 0)
            ]
            
        elif equation == "snell":
            # Snell's Law (n₁sinθ₁ = n₂sinθ₂)
            variables = ["n1", "θ1", "n2", "θ2"]
            
            input_widgets = [
                ("n1", "Index of Refraction 1 (n₁):", 1.0),
                ("θ1", "Angle of Incidence (θ₁, °):", 0),
                ("n2", "Index of Refraction 2 (n₂):", 1.0),
                ("θ2", "Angle of Refraction (θ₂, °):", 0)
            ]
            
        elif equation == "thin_lens":
            # Thin Lens (1/f = 1/d₀ + 1/dᵢ)
            variables = ["f", "d₀", "dᵢ"]
            
            input_widgets = [
                ("f", "Focal Length (f, m):", 0),
                ("d₀", "Object Distance (d₀, m):", 0),
                ("dᵢ", "Image Distance (dᵢ, m):", 0)
            ]
            
        elif equation == "doppler":
            # Doppler Effect
            variables = ["f_observed", "f_source", "v_source", "v_observer", "v_wave"]
            
            input_widgets = [
                ("f_observed", "Observed Frequency (f_obs, Hz):", 0),
                ("f_source", "Source Frequency (f_src, Hz):", 0),
                ("v_source", "Source Velocity (v_src, m/s):", 0),
                ("v_observer", "Observer Velocity (v_obs, m/s):", 0),
                ("v_wave", "Wave Velocity (v_wave, m/s):", 343)
            ]
            
        elif equation == "interference":
            # Interference (d sinθ = mλ)
            variables = ["d", "θ", "m", "λ"]
            
            input_widgets = [
                ("d", "Slit Separation (d, m):", 0),
                ("θ", "Angle (θ, °):", 0),
                ("m", "Order (m):", 0),
                ("λ", "Wavelength (λ, m):", 0)
            ]
        
        # Update variable selection
        self.waves_var_menu['values'] = variables
        self.waves_var_var.set(variables[0])
        
        # Create input fields
        for field_id, label_text, default_value in input_widgets:
            frame = tttk.Frame(self.waves_inputs_frame)
            frame.pack(fill="x", padx=5, pady=2)
            
            ttk.Label(frame, text=label_text).pack(side="left", padx=5)
            
            var = tk.DoubleVar(value=default_value)
            entry = ttk.Entry(frame, textvariable=var)
            entry.pack(side="right", padx=5, fill="x", expand=True)
            
            self.waves_input_fields[field_id] = var
    
    def calculate_waves(self):
        equation = self.waves_eq_var.get()
        variable = self.waves_var_var.get()
        
        try:
            if equation == "wave_speed":
                # Wave Speed (v = fλ)
                v = self.waves_input_fields["v"].get()
                f = self.waves_input_fields["f"].get()
                λ = self.waves_input_fields["λ"].get()
                
                if variable == "v":
                    result = f * λ
                    self.waves_result.set(f"Wave Speed (v): {result:.2f} m/s")
                elif variable == "f":
                    result = v / λ if λ != 0 else 0
                    self.waves_result.set(f"Frequency (f): {result:.2f} Hz")
                elif variable == "λ":
                    result = v / f if f != 0 else 0
                    self.waves_result.set(f"Wavelength (λ): {result:.2f} m")
                    
            elif equation == "frequency":
                # Frequency (f = 1/T)
                f = self.waves_input_fields["f"].get()
                T = self.waves_input_fields["T"].get()
                
                if variable == "f":
                    result = 1 / T if T != 0 else 0
                    self.waves_result.set(f"Frequency (f): {result:.2f} Hz")
                elif variable == "T":
                    result = 1 / f if f != 0 else 0
                    self.waves_result.set(f"Period (T): {result:.2f} s")
                    
            elif equation == "snell":
                # Snell's Law (n₁sinθ₁ = n₂sinθ₂)
                n1 = self.waves_input_fields["n1"].get()
                θ1 = self.waves_input_fields["θ1"].get()
                n2 = self.waves_input_fields["n2"].get()
                θ2 = self.waves_input_fields["θ2"].get()
                
                if variable == "n1":
                    result = n2 * math.sin(math.radians(θ2)) / math.sin(math.radians(θ1)) if math.sin(math.radians(θ1)) != 0 else 0
                    self.waves_result.set(f"Index of Refraction 1 (n₁): {result:.2f}")
                elif variable == "θ1":
                    result = math.degrees(math.asin(n2 * math.sin(math.radians(θ2)) / n1)) if n1 != 0 else 0
                    self.waves_result.set(f"Angle of Incidence (θ₁): {result:.2f} °")
                elif variable == "n2":
                    result = n1 * math.sin(math.radians(θ1)) / math.sin(math.radians(θ2)) if math.sin(math.radians(θ2)) != 0 else 0
                    self.waves_result.set(f"Index of Refraction 2 (n₂): {result:.2f}")
                elif variable == "θ2":
                    result = math.degrees(math.asin(n1 * math.sin(math.radians(θ1)) / n2)) if n2 != 0 else 0
                    self.waves_result.set(f"Angle of Refraction (θ₂): {result:.2f} °")
                    
            elif equation == "thin_lens":
                # Thin Lens (1/f = 1/d₀ + 1/dᵢ)
                f = self.waves_input_fields["f"].get()
                d₀ = self.waves_input_fields["d₀"].get()
                dᵢ = self.waves_input_fields["dᵢ"].get()
                
                if variable == "f":
                    result = 1 / (1/d₀ + 1/dᵢ) if (d₀ != 0 and dᵢ != 0) else 0
                    self.waves_result.set(f"Focal Length (f): {result:.2f} m")
                elif variable == "d₀":
                    result = 1 / (1/f - 1/dᵢ) if (f != 0 and dᵢ != 0) else 0
                    self.waves_result.set(f"Object Distance (d₀): {result:.2f} m")
                elif variable == "dᵢ":
                    result = 1 / (1/f - 1/d₀) if (f != 0 and d₀ != 0) else 0
                    self.waves_result.set(f"Image Distance (dᵢ): {result:.2f} m")
                    
            elif equation == "doppler":
                # Doppler Effect
                f_observed = self.waves_input_fields["f_observed"].get()
                f_source = self.waves_input_fields["f_source"].get()
                v_source = self.waves_input_fields["v_source"].get()
                v_observer = self.waves_input_fields["v_observer"].get()
                v_wave = self.waves_input_fields["v_wave"].get()
                
                if variable == "f_observed":
                    result = f_source * (v_wave + v_observer) / (v_wave + v_source) if (v_wave + v_source) != 0 else 0
                    self.waves_result.set(f"Observed Frequency (f_obs): {result:.2f} Hz")
                elif variable == "f_source":
                    result = f_observed * (v_wave + v_source) / (v_wave + v_observer) if (v_wave + v_observer) != 0 else 0
                    self.waves_result.set(f"Source Frequency (f_src): {result:.2f} Hz")
                elif variable == "v_source":
                    result = (f_source * (v_wave + v_observer) / f_observed) - v_wave if f_observed != 0 else 0
                    self.waves_result.set(f"Source Velocity (v_src): {result:.2f} m/s")
                elif variable == "v_observer":
                    result = (f_observed * (v_wave + v_source) / f_source) - v_wave if f_source != 0 else 0
                    self.waves_result.set(f"Observer Velocity (v_obs): {result:.2f} m/s")
                elif variable == "v_wave":
                    result = (f_source * v_observer - f_observed * v_source) / (f_observed - f_source) if (f_observed - f_source) != 0 else 0
                    self.waves_result.set(f"Wave Velocity (v_wave): {result:.2f} m/s")
                    
            elif equation == "interference":
                # Interference (d sinθ = mλ)
                d = self.waves_input_fields["d"].get()
                θ = self.waves_input_fields["θ"].get()
                m = self.waves_input_fields["m"].get()
                λ = self.waves_input_fields["λ"].get()
                
                if variable == "d":
                    result = m * λ / math.sin(math.radians(θ)) if math.sin(math.radians(θ)) != 0 else 0
                    self.waves_result.set(f"Slit Separation (d): {result:.2e} m")
                elif variable == "θ":
                    result = math.degrees(math.asin(m * λ / d)) if d != 0 else 0
                    self.waves_result.set(f"Angle (θ): {result:.2f} °")
                elif variable == "m":
                    result = d * math.sin(math.radians(θ)) / λ if λ != 0 else 0
                    self.waves_result.set(f"Order (m): {result:.2f}")
                elif variable == "λ":
                    result = d * math.sin(math.radians(θ)) / m if m != 0 else 0
                    self.waves_result.set(f"Wavelength (λ): {result:.2e} m")
                    
        except Exception as e:
            self.waves_result.set(f"Error: {str(e)}")
    
    def plot_wave(self):
        equation = self.waves_eq_var.get()
        
        try:
            self.wave_ax.clear()
            
            if equation == "wave_speed":
                # Wave visualization
                λ = self.waves_input_fields["λ"].get() or 1
                f = self.waves_input_fields["f"].get() or 1
                amplitude = 1
                
                x = np.linspace(0, 3*λ, 1000)
                y = amplitude * np.sin(2 * np.pi * (x/λ - f * 0.1))  # Time evolution
                
                self.wave_ax.plot(x, y)
                self.wave_ax.set_xlabel('Distance (m)')
                self.wave_ax.set_ylabel('Amplitude')
                self.wave_ax.set_title(f'Wave with λ={λ:.2f}m, f={f:.2f}Hz')
                
            elif equation == "interference":
                # Interference pattern
                λ = self.waves_input_fields["λ"].get() or 500e-9
                d = self.waves_input_fields["d"].get() or 0.001
                L = 1  # Distance to screen
                
                y = np.linspace(-0.05, 0.05, 1000)
                θ = np.arctan(y/L)
                intensity = np.cos(np.pi * d * np.sin(θ) / λ)**2
                
                self.wave_ax.plot(y, intensity)
                self.wave_ax.set_xlabel('Position on Screen (m)')
                self.wave_ax.set_ylabel('Intensity')
                self.wave_ax.set_title('Interference Pattern')
                
            else:
                raise ValueError("Plotting not available for this equation")
            
            self.wave_ax.grid(True)
            self.wave_canvas.draw()
            
        except Exception as e:
            self.waves_result.set(f"Plot Error: {str(e)}")
    
    def clear_wave_plot(self):
        self.wave_ax.clear()
        self.wave_canvas.draw()
    
    def reset_waves(self):
        self.waves_result.set("Result will appear here")
        self.update_waves_inputs()
        self.clear_wave_plot()

    def init_electricity_tab(self):
        # Main frames
        left_frame = ttk.Frame(self.tab_electricity)
        left_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        
        right_frame = ttk.Frame(self.tab_electricity)
        right_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)
        
        # Equation selection
        eq_frame = ttk.LabelFrame(left_frame, text="Electricity & Magnetism Equation")
        eq_frame.pack(fill="x", padx=5, pady=5)
        
        self.electricity_eq_var = tk.StringVar()
        self.electricity_eq_var.set("ohm")  # Default equation
        
        eq_options = [
            ("Ohm's Law (V = IR)", "ohm"),
            ("Power (P = IV)", "power"),
            ("Coulomb's Law (F = kq₁q₂/r²)", "coulomb"),
            ("Electric Field (E = F/q)", "electric_field"),
            ("Capacitance (C = Q/V)", "capacitance"),
            ("Magnetic Force (F = qvB sinθ)", "magnetic_force")
        ]
        
        for text, value in eq_options:
            ttk.Radiobutton(
                eq_frame, 
                text=text, 
                variable=self.electricity_eq_var, 
                value=value,
                command=self.update_electricity_inputs
            ).pack(anchor="w", padx=5, pady=2)
        
        # Inputs frame
        self.electricity_inputs_frame = ttk.LabelFrame(left_frame, text="Inputs")
        self.electricity_inputs_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Variable to find
        self.electricity_find_frame = ttk.Frame(self.electricity_inputs_frame)
        self.electricity_find_frame.pack(fill="x", padx=5, pady=5)
        
        ttk.Label(self.electricity_find_frame, text="Find:").pack(side="left", padx=5)
        self.electricity_var_var = tk.StringVar()
        self.electricity_var_menu = ttk.Combobox(self.electricity_find_frame, textvariable=self.electricity_var_var)
        self.electricity_var_menu.pack(side="left", padx=5, fill="x", expand=True)
        
        # Input fields will be created by update_electricity_inputs
        self.electricity_input_fields = {}
        
        # Buttons
        button_frame = ttk.Frame(left_frame)
        button_frame.pack(fill="x", padx=5, pady=5)
        
        ttk.Button(button_frame, text="Calculate", command=self.calculate_electricity).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Reset", command=self.reset_electricity).pack(side="left", padx=5)
        
        # Result
        result_frame = ttk.LabelFrame(left_frame, text="Result")
        result_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        self.electricity_result = tk.StringVar()
        self.electricity_result.set("Result will appear here")
        ttk.Label(result_frame, textvariable=self.electricity_result, wraplength=300).pack(padx=5, pady=5)
        
        # Circuit visualization
        vis_frame = ttk.LabelFrame(right_frame, text="Circuit Visualization")
        vis_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Circuit components table
        self.circuit_tree = ttk.Treeview(
            vis_frame, 
            columns=("type", "value", "actions"), 
            show="headings",
            height=5
        )
        
        self.circuit_tree.heading("type", text="Component Type")
        self.circuit_tree.heading("value", text="Value")
        self.circuit_tree.heading("actions", text="Actions")
        
        self.circuit_tree.column("type", width=150, anchor=tk.CENTER)
        self.circuit_tree.column("value", width=100, anchor=tk.CENTER)
        self.circuit_tree.column("actions", width=100, anchor=tk.CENTER)
        
        self.circuit_tree.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Buttons for circuit management
        circuit_button_frame = ttk.Frame(vis_frame)
        circuit_button_frame.pack(fill="x", padx=5, pady=5)
        
        ttk.Button(circuit_button_frame, text="Add Component", command=self.add_circuit_component).pack(side="left", padx=5)
        ttk.Button(circuit_button_frame, text="Clear All", command=self.clear_circuit_components).pack(side="left", padx=5)
        ttk.Button(circuit_button_frame, text="Analyze Circuit", command=self.analyze_circuit).pack(side="left", padx=5)
        
        # Circuit analysis result
        circuit_result_frame = ttk.LabelFrame(vis_frame, text="Circuit Analysis")
        circuit_result_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        self.circuit_analysis_result = tk.StringVar()
        self.circuit_analysis_result.set("Circuit analysis will appear here")
        ttk.Label(circuit_result_frame, textvariable=self.circuit_analysis_result, wraplength=300).pack(padx=5, pady=5)
        
        # Initialize inputs
        self.update_electricity_inputs()
    
    def update_electricity_inputs(self):
        # Clear existing input fields (except the find frame)
        for widget in self.electricity_inputs_frame.winfo_children():
            if widget != self.electricity_find_frame:
                widget.destroy()
        
        equation = self.electricity_eq_var.get()
        self.electricity_input_fields = {}
        
        # Common variables for all equations
        variables = []
        input_widgets = []
        
        if equation == "ohm":
            # Ohm's Law (V = IR)
            variables = ["V", "I", "R"]
            
            input_widgets = [
                ("V", "Voltage (V, V):", 0),
                ("I", "Current (I, A):", 0),
                ("R", "Resistance (R, Ω):", 0)
            ]
            
        elif equation == "power":
            # Power (P = IV)
            variables = ["P", "I", "V"]
            
            input_widgets = [
                ("P", "Power (P, W):", 0),
                ("I", "Current (I, A):", 0),
                ("V", "Voltage (V, V):", 0)
            ]
            
        elif equation == "coulomb":
            # Coulomb's Law (F = kq₁q₂/r²)
            variables = ["F", "q1", "q2", "r"]
            
            input_widgets = [
                ("F", "Force (F, N):", 0),
                ("q1", "Charge 1 (q₁, C):", 0),
                ("q2", "Charge 2 (q₂, C):", 0),
                ("r", "Distance (r, m):", 0)
            ]
            
        elif equation == "electric_field":
            # Electric Field (E = F/q)
            variables = ["E", "F", "q"]
            
            input_widgets = [
                ("E", "Electric Field (E, N/C):", 0),
                ("F", "Force (F, N):", 0),
                ("q", "Charge (q, C):", 0)
            ]
            
        elif equation == "capacitance":
            # Capacitance (C = Q/V)
            variables = ["C", "Q", "V"]
            
            input_widgets = [
                ("C", "Capacitance (C, F):", 0),
                ("Q", "Charge (Q, C):", 0),
                ("V", "Voltage (V, V):", 0)
            ]
            
        elif equation == "magnetic_force":
            # Magnetic Force (F = qvB sinθ)
            variables = ["F", "q", "v", "B", "θ"]
            
            input_widgets = [
                ("F", "Force (F, N):", 0),
                ("q", "Charge (q, C):", 0),
                ("v", "Velocity (v, m/s):", 0),
                ("B", "Magnetic Field (B, T):", 0),
                ("θ", "Angle (θ, °):", 0)
            ]
        
        # Update variable selection
        self.electricity_var_menu['values'] = variables
        self.electricity_var_var.set(variables[0])
        
        # Create input fields
        for field_id, label_text, default_value in input_widgets:
            frame = ttk.Frame(self.electricity_inputs_frame)
            frame.pack(fill="x", padx=5, pady=2)
            
            ttk.Label(frame, text=label_text).pack(side="left", padx=5)
            
            var = tk.DoubleVar(value=default_value)
            entry = ttk.Entry(frame, textvariable=var)
            entry.pack(side="right", padx=5, fill="x", expand=True)
            
            self.electricity_input_fields[field_id] = var
    
    def calculate_electricity(self):
        equation = self.electricity_eq_var.get()
        variable = self.electricity_var_var.get()
        
        try:
            if equation == "ohm":
                # Ohm's Law (V = IR)
                V = self.electricity_input_fields["V"].get()
                I = self.electricity_input_fields["I"].get()
                R = self.electricity_input_fields["R"].get()
                
                if variable == "V":
                    result = I * R
                    self.electricity_result.set(f"Voltage (V): {result:.2f} V")
                elif variable == "I":
                    result = V / R if R != 0 else 0
                    self.electricity_result.set(f"Current (I): {result:.2f} A")
                elif variable == "R":
                    result = V / I if I != 0 else 0
                    self.electricity_result.set(f"Resistance (R): {result:.2f} Ω")
                    
            elif equation == "power":
                # Power (P = IV)
                P = self.electricity_input_fields["P"].get()
                I = self.electricity_input_fields["I"].get()
                V = self.electricity_input_fields["V"].get()
                
                if variable == "P":
                    result = I * V
                    self.electricity_result.set(f"Power (P): {result:.2f} W")
                elif variable == "I":
                    result = P / V if V != 0 else 0
                    self.electricity_result.set(f"Current (I): {result:.2f} A")
                elif variable == "V":
                    result = P / I if I != 0 else 0
                    self.electricity_result.set(f"Voltage (V): {result:.2f} V")
                    
            elif equation == "coulomb":
                # Coulomb's Law (F = kq₁q₂/r²)
                F = self.electricity_input_fields["F"].get()
                q1 = self.electricity_input_fields["q1"].get()
                q2 = self.electricity_input_fields["q2"].get()
                r = self.electricity_input_fields["r"].get()
                
                if variable == "F":
                    result = 8.9875517923e9 * q1 * q2 / (r * r) if r != 0 else 0
                    self.electricity_result.set(f"Force (F): {result:.2e} N")
                elif variable == "q1":
                    result = F * r * r / (8.9875517923e9 * q2) if q2 != 0 else 0
                    self.electricity_result.set(f"Charge 1 (q₁): {result:.2e} C")
                elif variable == "q2":
                    result = F * r * r / (8.9875517923e9 * q1) if q1 != 0 else 0
                    self.electricity_result.set(f"Charge 2 (q₂): {result:.2e} C")
                elif variable == "r":
                    result = math.sqrt(8.9875517923e9 * q1 * q2 / F) if F != 0 else 0
                    self.electricity_result.set(f"Distance (r): {result:.2f} m")
                    
            elif equation == "electric_field":
                # Electric Field (E = F/q)
                E = self.electricity_input_fields["E"].get()
                F = self.electricity_input_fields["F"].get()
                q = self.electricity_input_fields["q"].get()
                
                if variable == "E":
                    result = F / q if q != 0 else 0
                    self.electricity_result.set(f"Electric Field (E): {result:.2f} N/C")
                elif variable == "F":
                    result = E * q
                    self.electricity_result.set(f"Force (F): {result:.2f} N")
                elif variable == "q":
                    result = F / E if E != 0 else 0
                    self.electricity_result.set(f"Charge (q): {result:.2e} C")
                    
            elif equation == "capacitance":
                # Capacitance (C = Q/V)
                C = self.electricity_input_fields["C"].get()
                Q = self.electricity_input_fields["Q"].get()
                V = self.electricity_input_fields["V"].get()
                
                if variable == "C":
                    result = Q / V if V != 0 else 0
                    self.electricity_result.set(f"Capacitance (C): {result:.2e} F")
                elif variable == "Q":
                    result = C * V
                    self.electricity_result.set(f"Charge (Q): {result:.2e} C")
                elif variable == "V":
                    result = Q / C if C != 0 else 0
                    self.electricity_result.set(f"Voltage (V): {result:.2f} V")
                    
            elif equation == "magnetic_force":
                # Magnetic Force (F = qvB sinθ)
                F = self.electricity_input_fields["F"].get()
                q = self.electricity_input_fields["q"].get()
                v = self.electricity_input_fields["v"].get()
                B = self.electricity_input_fields["B"].get()
                θ = self.electricity_input_fields["θ"].get()
                
                if variable == "F":
                    result = q * v * B * math.sin(math.radians(θ))
                    self.electricity_result.set(f"Force (F): {result:.2e} N")
                elif variable == "q":
                    result = F / (v * B * math.sin(math.radians(θ))) if (v * B * math.sin(math.radians(θ))) != 0 else 0
                    self.electricity_result.set(f"Charge (q): {result:.2e} C")
                elif variable == "v":
                    result = F / (q * B * math.sin(math.radians(θ))) if (q * B * math.sin(math.radians(θ))) != 0 else 0
                    self.electricity_result.set(f"Velocity (v): {result:.2f} m/s")
                elif variable == "B":
                    result = F / (q * v * math.sin(math.radians(θ))) if (q * v * math.sin(math.radians(θ))) != 0 else 0
                    self.electricity_result.set(f"Magnetic Field (B): {result:.2f} T")
                elif variable == "θ":
                    result = math.degrees(math.asin(F / (q * v * B))) if (q * v * B) != 0 else 0
                    self.electricity_result.set(f"Angle (θ): {result:.2f} °")
                    
        except Exception as e:
            self.electricity_result.set(f"Error: {str(e)}")
    
    def reset_electricity(self):
        self.electricity_result.set("Result will appear here")
        self.update_electricity_inputs()
    
    def add_circuit_component(self):
        # Create a dialog to add a new circuit component
        dialog = tk.Toplevel(self.root)
        dialog.title("Add Circuit Component")
        dialog.geometry("300x200")
        dialog.transient(self.root)
        dialog.grab_set()
        
        ttk.Label(dialog, text="Component Type:").pack(pady=5)
        type_var = tk.StringVar()
        type_combo = ttk.Combobox(dialog, textvariable=type_var)
        type_combo['values'] = ("Resistor", "Capacitor", "Inductor", "Voltage Source", "Current Source")
        type_combo.pack(pady=5)
        
        ttk.Label(dialog, text="Value:").pack(pady=5)
        value_var = tk.DoubleVar()
        ttk.Entry(dialog, textvariable=value_var).pack(pady=5)
        
        ttk.Label(dialog, text="Unit:").pack(pady=5)
        unit_var = tk.StringVar()
        unit_combo = ttk.Combobox(dialog, textvariable=unit_var)
        unit_combo['values'] = ("Ω", "F", "H", "V", "A")
        unit_combo.pack(pady=5)
        
        def save_component():
            self.circuit_components.append({
                "type": type_var.get(),
                "value": value_var.get(),
                "unit": unit_var.get()
            })
            self.update_circuit_table()
            dialog.destroy()
        
        ttk.Button(dialog, text="Save", command=save_component).pack(pady=10)
    
    def update_circuit_table(self):
        # Clear existing items
        for item in self.circuit_tree.get_children():
            self.circuit_tree.delete(item)
        
        # Add new items
        for i, component in enumerate(self.circuit_components):
            self.circuit_tree.insert(
                "", "end", 
                values=(
                    component["type"],
                    f"{component['value']} {component['unit']}",
                    "Delete"
                ),
                tags=(i,)
            )
        
        # Bind delete action
        self.circuit_tree.bind("<ButtonRelease-1>", self.on_circuit_click)
    
    def on_circuit_click(self, event):
        region = self.circuit_tree.identify("region", event.x, event.y)
        if region == "cell":
            column = self.circuit_tree.identify_column(event.x)
            item = self.circuit_tree.identify_row(event.y)
            
            if column == "#3":  # Actions column
                index = int(self.circuit_tree.item(item, "tags")[0])
                self.circuit_components.pop(index)
                self.update_circuit_table()
    
    def clear_circuit_components(self):
        self.circuit_components = []
        self.update_circuit_table()
    
    def analyze_circuit(self):
        if not self.circuit_components:
            self.circuit_analysis_result.set("No components to analyze")
            return
        
        try:
            # Simple circuit analysis (series resistors only for this example)
            total_resistance = 0
            total_capacitance = 0
            total_inductance = 0
            voltage_sources = []
            current_sources = []
            
            for component in self.circuit_components:
                if component["type"] == "Resistor" and component["unit"] == "Ω":
                    total_resistance += component["value"]
                elif component["type"] == "Capacitor" and component["unit"] == "F":
                    total_capacitance += component["value"]
                elif component["type"] == "Inductor" and component["unit"] == "H":
                    total_inductance += component["value"]
                elif component["type"] == "Voltage Source" and component["unit"] == "V":
                    voltage_sources.append(component["value"])
                elif component["type"] == "Current Source" and component["unit"] == "A":
                    current_sources.append(component["value"])
            
            analysis_text = "Circuit Analysis:\n"
            
            if total_resistance > 0:
                analysis_text += f"Total Resistance: {total_resistance} Ω\n"
            
            if total_capacitance > 0:
                analysis_text += f"Total Capacitance: {total_capacitance} F\n"
            
            if total_inductance > 0:
                analysis_text += f"Total Inductance: {total_inductance} H\n"
            
            if voltage_sources:
                total_voltage = sum(voltage_sources)
                analysis_text += f"Total Voltage: {total_voltage} V\n"
                
                if total_resistance > 0:
                    current = total_voltage / total_resistance
                    analysis_text += f"Current: {current:.2f} A\n"
                    analysis_text += f"Power: {total_voltage * current:.2f} W\n"
            
            if current_sources:
                total_current = sum(current_sources)
                analysis_text += f"Total Current: {total_current} A\n"
                
                if total_resistance > 0:
                    voltage = total_current * total_resistance
                    analysis_text += f"Voltage: {voltage:.2f} V\n"
                    analysis_text += f"Power: {voltage * total_current:.2f} W\n"
            
            self.circuit_analysis_result.set(analysis_text)
            
        except Exception as e:
            self.circuit_analysis_result.set(f"Error: {str(e)}")

    def init_measurements_tab(self):
        # Main frames
        left_frame = ttk.Frame(self.tab_measurements)
        left_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        
        right_frame = ttk.Frame(self.tab_measurements)
        right_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)
        
        # Measurement input
        input_frame = ttk.LabelFrame(left_frame, text="Add Measurement")
        input_frame.pack(fill="x", padx=5, pady=5)
        
        ttk.Label(input_frame, text="Measurement Name:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.measurement_name_var = tk.StringVar()
        ttk.Entry(input_frame, textvariable=self.measurement_name_var).grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        
        ttk.Label(input_frame, text="Value:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.measurement_value_var = tk.DoubleVar()
        ttk.Entry(input_frame, textvariable=self.measurement_value_var).grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        
        ttk.Label(input_frame, text="Unit:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.measurement_unit_var = tk.StringVar()
        ttk.Entry(input_frame, textvariable=self.measurement_unit_var).grid(row=2, column=1, padx=5, pady=5, sticky="ew")
        
        ttk.Label(input_frame, text="Uncertainty:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.measurement_uncertainty_var = tk.DoubleVar()
        ttk.Entry(input_frame, textvariable=self.measurement_uncertainty_var).grid(row=3, column=1, padx=5, pady=5, sticky="ew")
        
        button_frame = ttk.Frame(input_frame)
        button_frame.grid(row=4, column=0, columnspan=2, pady=10)
        
        ttk.Button(button_frame, text="Add Measurement", command=self.add_measurement).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Clear All", command=self.clear_measurements).pack(side="left", padx=5)
        
        # Measurements table
        table_frame = ttk.LabelFrame(left_frame, text="Measurements")
        table_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        columns = ("name", "value", "unit", "uncertainty", "timestamp", "actions")
        self.measurements_tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=10)
        
        self.measurements_tree.heading("name", text="Name")
        self.measurements_tree.heading("value", text="Value")
        self.measurements_tree.heading("unit", text="Unit")
        self.measurements_tree.heading("uncertainty", text="Uncertainty")
        self.measurements_tree.heading("timestamp", text="Timestamp")
        self.measurements_tree.heading("actions", text="Actions")
        
        self.measurements_tree.column("name", width=100, anchor=tk.CENTER)
        self.measurements_tree.column("value", width=80, anchor=tk.CENTER)
        self.measurements_tree.column("unit", width=80, anchor=tk.CENTER)
        self.measurements_tree.column("uncertainty", width=80, anchor=tk.CENTER)
        self.measurements_tree.column("timestamp", width=120, anchor=tk.CENTER)
        self.measurements_tree.column("actions", width=80, anchor=tk.CENTER)
        
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.measurements_tree.yview)
        self.measurements_tree.configure(yscrollcommand=scrollbar.set)
        
        self.measurements_tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Bind delete action
        self.measurements_tree.bind("<ButtonRelease-1>", self.on_measurement_click)
        
        # Statistics frame
        stats_frame = ttk.LabelFrame(right_frame, text="Measurement Statistics")
        stats_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        self.stats_result = tk.StringVar()
        self.stats_result.set("Select measurements to see statistics")
        ttk.Label(stats_frame, textvariable=self.stats_result, wraplength=300).pack(padx=5, pady=5)
        
        ttk.Button(stats_frame, text="Calculate Statistics", command=self.calculate_statistics).pack(pady=10)
        
        # Plot frame
        plot_frame = ttk.LabelFrame(right_frame, text="Measurement Plot")
        plot_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        button_frame = ttk.Frame(plot_frame)
        button_frame.pack(fill="x", padx=5, pady=5)
        
        ttk.Button(button_frame, text="Plot Measurements", command=self.plot_measurements).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Clear Plot", command=self.clear_measurement_plot).pack(side="left", padx=5)
        
        # Matplotlib figure
        self.measurement_fig, self.measurement_ax = plt.subplots(figsize=(6, 4))
        self.measurement_canvas = FigureCanvasTkAgg(self.measurement_fig, master=plot_frame)
        self.measurement_canvas.get_tk_widget().pack(fill="both", expand=True)
    
    def add_measurement(self):
        name = self.measurement_name_var.get()
        value = self.measurement_value_var.get()
        unit = self.measurement_unit_var.get()
        uncertainty = self.measurement_uncertainty_var.get()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        if not name:
            messagebox.showerror("Error", "Please enter a measurement name")
            return
        
        self.measurements.append({
            "name": name,
            "value": value,
            "unit": unit,
            "uncertainty": uncertainty,
            "timestamp": timestamp
        })
        
        self.update_measurements_table()
        
        # Clear input fields
        self.measurement_name_var.set("")
        self.measurement_value_var.set(0)
        self.measurement_unit_var.set("")
        self.measurement_uncertainty_var.set(0)
    
    def update_measurements_table(self):
        # Clear existing items
        for item in self.measurements_tree.get_children():
            self.measurements_tree.delete(item)
        
        # Add new items
        for i, measurement in enumerate(self.measurements):
            self.measurements_tree.insert(
                "", "end", 
                values=(
                    measurement["name"],
                    f"{measurement['value']:.4f}",
                    measurement["unit"],
                    f"{measurement['uncertainty']:.4f}",
                    measurement["timestamp"],
                    "Delete"
                ),
                tags=(i,)
            )
    
    def on_measurement_click(self, event):
        region = self.measurements_tree.identify("region", event.x, event.y)
        if region == "cell":
            column = self.measurements_tree.identify_column(event.x)
            item = self.measurements_tree.identify_row(event.y)
            
            if column == "#6":  # Actions column
                index = int(self.measurements_tree.item(item, "tags")[0])
                self.measurements.pop(index)
                self.update_measurements_table()
    
    def clear_measurements(self):
        self.measurements = []
        self.update_measurements_table()
    
    def calculate_statistics(self):
        if not self.measurements:
            self.stats_result.set("No measurements to analyze")
            return
        
        try:
            values = [m["value"] for m in self.measurements]
            
            if not values:
                self.stats_result.set("No numeric values to analyze")
                return
            
            mean = sum(values) / len(values)
            variance = sum((x - mean) ** 2 for x in values) / len(values)
            std_dev = math.sqrt(variance)
            min_val = min(values)
            max_val = max(values)
            
            self.stats_result.set(
                f"Statistics for {len(values)} measurements:\n"
                f"Mean: {mean:.4f}\n"
                f"Standard Deviation: {std_dev:.4f}\n"
                f"Minimum: {min_val:.4f}\n"
                f"Maximum: {max_val:.4f}"
            )
            
        except Exception as e:
            self.stats_result.set(f"Error: {str(e)}")
    
    def plot_measurements(self):
        if not self.measurements:
            self.stats_result.set("No measurements to plot")
            return
        
        try:
            self.measurement_ax.clear()
            
            names = [m["name"] for m in self.measurements]
            values = [m["value"] for m in self.measurements]
            uncertainties = [m["uncertainty"] for m in self.measurements]
            
            x_pos = range(len(names))
            
            self.measurement_ax.bar(x_pos, values, yerr=uncertainties, align='center', alpha=0.7, ecolor='black', capsize=10)
            self.measurement_ax.set_xlabel('Measurements')
            self.measurement_ax.set_ylabel('Values')
            self.measurement_ax.set_title('Measurement Values with Uncertainty')
            self.measurement_ax.set_xticks(x_pos)
            self.measurement_ax.set_xticklabels(names, rotation=45, ha='right')
            self.measurement_ax.yaxis.grid(True)
            
            self.measurement_fig.tight_layout()
            self.measurement_canvas.draw()
            
        except Exception as e:
            self.stats_result.set(f"Plot Error: {str(e)}")
    
    def clear_measurement_plot(self):
        self.measurement_ax.clear()
        self.measurement_canvas.draw()

    def init_terminologies_tab(self):
        # Physics terminologies dictionary
        self.terminologies = {
            "Kinematics": {
                "Velocity": "The rate of change of an object's position with respect to time. It is a vector quantity with both magnitude and direction.",
                "Acceleration": "The rate of change of velocity with respect to time. It is a vector quantity.",
                "Displacement": "The change in position of an object. It is a vector quantity that specifies both distance and direction.",
                "Projectile Motion": "The motion of an object thrown or projected into the air, subject only to acceleration due to gravity."
            },
            "Dynamics": {
                "Force": "A push or pull upon an object resulting from its interaction with another object. Measured in Newtons (N).",
                "Newton's First Law": "An object at rest stays at rest and an object in motion stays in motion with the same speed and in the same direction unless acted upon by an unbalanced force.",
                "Newton's Second Law": "The acceleration of an object is directly proportional to the net force acting on it and inversely proportional to its mass (F = ma).",
                "Newton's Third Law": "For every action, there is an equal and opposite reaction.",
                "Friction": "The force that opposes the relative motion or tendency of such motion of two surfaces in contact."
            },
            "Energy": {
                "Kinetic Energy": "The energy possessed by an object due to its motion. KE = ½mv²",
                "Potential Energy": "The energy stored in an object due to its position or configuration. PE = mgh for gravitational potential energy.",
                "Work": "The product of the force applied to an object and the displacement of the object in the direction of the force. W = F·d",
                "Power": "The rate at which work is done or energy is transferred. P = W/t"
            },
            "Waves": {
                "Wavelength": "The distance between successive crests, troughs, or identical parts of a wave.",
                "Frequency": "The number of waves that pass a fixed point in unit time. Measured in Hertz (Hz).",
                "Amplitude": "The maximum displacement or distance moved by a point on a wave from its equilibrium position.",
                "Refraction": "The change in direction of a wave passing from one medium to another caused by its change in speed."
            },
            "Electricity": {
                "Current": "The flow of electric charge. Measured in Amperes (A).",
                "Voltage": "The electric potential difference between two points. Measured in Volts (V).",
                "Resistance": "The opposition to the flow of electric current. Measured in Ohms (Ω).",
                "Ohm's Law": "The current through a conductor between two points is directly proportional to the voltage across the two points (V = IR)."
            }
        }
        
        # Main frames
        left_frame = ttk.Frame(self.tab_terminologies)
        left_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        
        right_frame = ttk.Frame(self.tab_terminologies)
        right_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)
        
        # Category selection
        category_frame = ttk.LabelFrame(left_frame, text="Select Category")
        category_frame.pack(fill="x", padx=5, pady=5)
        
        self.terminology_category_var = tk.StringVar()
        self.terminology_category_var.set("Kinematics")
        
        category_combo = ttk.Combobox(category_frame, textvariable=self.terminology_category_var)
        category_combo['values'] = tuple(self.terminologies.keys())
        category_combo.pack(padx=5, pady=5, fill="x")
        category_combo.bind('<<ComboboxSelected>>', self.update_terminology_list)
        
        # Terminology list
        list_frame = ttk.LabelFrame(left_frame, text="Terminologies")
        list_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        self.terminology_listbox = tk.Listbox(list_frame)
        self.terminology_listbox.pack(fill="both", expand=True, padx=5, pady=5)
        self.terminology_listbox.bind('<<ListboxSelect>>', self.show_terminology_definition)
        
        # Definition display
        definition_frame = ttk.LabelFrame(right_frame, text="Definition")
        definition_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        self.definition_text = tk.Text(definition_frame, wrap="word", height=15, width=40)
        scrollbar = ttk.Scrollbar(definition_frame, orient="vertical", command=self.definition_text.yview)
        self.definition_text.configure(yscrollcommand=scrollbar.set)
        
        self.definition_text.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        scrollbar.pack(side="right", fill="y", padx=(0, 5), pady=5)
        
        # Search frame
        search_frame = ttk.LabelFrame(right_frame, text="Search Terminologies")
        search_frame.pack(fill="x", padx=5, pady=5)
        
        ttk.Label(search_frame, text="Search:").pack(side="left", padx=5, pady=5)
        self.terminology_search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=self.terminology_search_var)
        search_entry.pack(side="left", padx=5, pady=5, fill="x", expand=True)
        search_entry.bind('<KeyRelease>', self.search_terminologies)
        
        # Initialize terminology list
        self.update_terminology_list()
    
    def update_terminology_list(self, event=None):
        category = self.terminology_category_var.get()
        self.terminology_listbox.delete(0, tk.END)
        
        if category in self.terminologies:
            for term in sorted(self.terminologies[category].keys()):
                self.terminology_listbox.insert(tk.END, term)
    
    def show_terminology_definition(self, event):
        selection = self.terminology_listbox.curselection()
        if not selection:
            return
        
        category = self.terminology_category_var.get()
        term = self.terminology_listbox.get(selection[0])
        
        if category in self.terminologies and term in self.terminologies[category]:
            definition = self.terminologies[category][term]
            self.definition_text.delete(1.0, tk.END)
            self.definition_text.insert(tk.END, f"{term}:\n\n{definition}")
    
    def search_terminologies(self, event):
        query = self.terminology_search_var.get().lower()
        
        if not query:
            self.update_terminology_list()
            return
        
        self.terminology_listbox.delete(0, tk.END)
        
        for category, terms in self.terminologies.items():
            for term, definition in terms.items():
                if query in term.lower() or query in definition.lower():
                    self.terminology_listbox.insert(tk.END, f"{category}: {term}")

# Main application
if __name__ == "__main__":
    root = tk.Tk()
    app = PhysicsToolkit(root)
    root.mainloop()