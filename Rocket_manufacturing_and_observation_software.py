# -*- coding: utf-8 -*-
"""
Rocketry Pro - Solid Motor Manufacturing & Flight Analysis
Python 3.9 Tkinter Version
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import math
import json
import os
from datetime import datetime

class RocketryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Rocketry Pro - Solid Motor Manufacturing & Flight Analysis")
        self.root.geometry("1300x950")
        
        # Configure default font
        default_font = ('Times New Roman', 10)
        self.root.option_add('*Font', default_font)
        
        # Configure style
        self.style = ttk.Style()
        self.style.configure('TFrame', padding=10)
        self.style.configure('TLabel', padding=5, font=default_font)
        self.style.configure('TButton', padding=5, font=default_font)
        self.style.configure('TCombobox', font=default_font)
        self.style.configure('TNotebook', font=default_font)
        self.style.configure('TNotebook.Tab', font=default_font)
        
        # Safety warning
        self.safety_warning = tk.Label(
            root, 
            text="⚠️ WARNING: Rocket motors contain high-energy materials. Follow all safety protocols and regulations. ⚠️",
            fg='red', 
            bg='yellow',
            font=('Times New Roman', 10, 'bold'),
            pady=10
        )
        self.safety_warning.pack(fill=tk.X)
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Create tabs
        self.create_motor_design_tab()
        self.create_propellant_calc_tab()
        self.create_flight_sim_tab()
        self.create_telemetry_tab()
        self.create_orbital_tab()
        self.create_contact_tab()
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        self.status_bar = tk.Label(root, textvariable=self.status_var, bd=1, relief=tk.SUNKEN, anchor=tk.W, font=default_font)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Initialize variables
        self.flight_data = []
        self.current_project = None
    
    def create_contact_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Contact")
        
        # Header
        ttk.Label(frame, text="Contact Information", font=('Times New Roman', 12, 'bold')).grid(row=0, column=0, columnspan=2, pady=10)
        
        # Contact details
        contact_info = """
        Rocketry Pro Software Support
        ----------------------------
        
        For technical support or questions:
        Email: Samngacha@gmail.com
        Phone: +254742859291
        
        Development Team:
        - Lead Engineer: Sam Ng (Samngacha@gmail.com)
        - Propulsion Specialist: Alex Chen (alex.chen@rocketrypro.com)
        - Flight Dynamics: Taylor Smith (taylor.smith@rocketrypro.com)
        
        Office Address:
        Rocketry Pro Inc.
        123 Aerospace Way
        Houston, TX 77058
        United States
        
        Business Hours:
        Monday-Friday: 9:00 AM - 5:00 PM CST
        """
        
        contact_label = tk.Text(frame, height=20, width=60, wrap=tk.WORD, font=('Times New Roman', 10))
        contact_label.insert(tk.END, contact_info)
        contact_label.config(state=tk.DISABLED)
        contact_label.grid(row=1, column=0, padx=10, pady=10)
        
        # Emergency contact
        emergency_frame = ttk.LabelFrame(frame, text="Emergency Contact", padding=10)
        emergency_frame.grid(row=1, column=1, padx=10, pady=10, sticky='n')
        
        ttk.Label(emergency_frame, text="For immediate safety concerns:", font=('Times New Roman', 10, 'bold')).pack()
        ttk.Label(emergency_frame, text="24/7 Safety Hotline: +1 (555) 987-6543", font=('Times New Roman', 10)).pack(pady=5)
        ttk.Label(emergency_frame, text="Email: safety@rocketrypro.com", font=('Times New Roman', 10)).pack(pady=5)
        
        # Configure grid weights
        frame.grid_rowconfigure(1, weight=1)
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(1, weight=1)

    def create_motor_design_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Motor Design")
        
        # Header
        ttk.Label(frame, text="Solid Rocket Motor Design Calculator", font=('Times New Roman', 12, 'bold')).grid(row=0, column=0, columnspan=4, pady=10)
        
        # Motor parameters
        ttk.Label(frame, text="Motor Diameter:").grid(row=1, column=0, sticky='e')
        self.diameter_var = tk.DoubleVar(value=0.1)  # meters
        ttk.Entry(frame, textvariable=self.diameter_var, width=10).grid(row=1, column=1, sticky='w')
        ttk.Label(frame, text="m").grid(row=1, column=2, sticky='w')
        
        ttk.Label(frame, text="Motor Length:").grid(row=2, column=0, sticky='e')
        self.length_var = tk.DoubleVar(value=0.5)  # meters
        ttk.Entry(frame, textvariable=self.length_var, width=10).grid(row=2, column=1, sticky='w')
        ttk.Label(frame, text="m").grid(row=2, column=2, sticky='w')
        
        ttk.Label(frame, text="Nozzle Throat Diam:").grid(row=3, column=0, sticky='e')
        self.throat_var = tk.DoubleVar(value=0.02)  # meters
        ttk.Entry(frame, textvariable=self.throat_var, width=10).grid(row=3, column=1, sticky='w')
        ttk.Label(frame, text="m").grid(row=3, column=2, sticky='w')
        
        ttk.Label(frame, text="Nozzle Exit Diam:").grid(row=4, column=0, sticky='e')
        self.exit_var = tk.DoubleVar(value=0.05)  # meters
        ttk.Entry(frame, textvariable=self.exit_var, width=10).grid(row=4, column=1, sticky='w')
        ttk.Label(frame, text="m").grid(row=4, column=2, sticky='w')
        
        # Grain configuration
        ttk.Label(frame, text="Grain Configuration:").grid(row=5, column=0, sticky='e')
        self.grain_type_var = tk.StringVar(value="Cylindrical")
        grain_types = ["Cylindrical", "Star", "Wagon Wheel", "End Burner"]
        ttk.Combobox(frame, textvariable=self.grain_type_var, values=grain_types, width=15).grid(row=5, column=1, sticky='w')
        
        ttk.Label(frame, text="Web Fraction:").grid(row=6, column=0, sticky='e')
        self.web_var = tk.DoubleVar(value=0.7)
        ttk.Entry(frame, textvariable=self.web_var, width=10).grid(row=6, column=1, sticky='w')
        
        # Calculate button
        ttk.Button(frame, text="Calculate Motor Parameters", command=self.calculate_motor).grid(row=7, column=0, columnspan=3, pady=10)
        
        # Export button
        ttk.Button(frame, text="Export to TXT", command=self.export_motor_to_txt).grid(row=7, column=3, pady=10)
        
        # Results notebook
        results_notebook = ttk.Notebook(frame)
        results_notebook.grid(row=8, column=0, columnspan=4, sticky='nsew', padx=5, pady=5)
        
        # Design tab
        design_frame = ttk.Frame(results_notebook)
        results_notebook.add(design_frame, text="Design Parameters")
        self.design_text = tk.Text(design_frame, height=15, width=90, wrap=tk.WORD)
        scrollbar = ttk.Scrollbar(design_frame, orient="vertical", command=self.design_text.yview)
        scrollbar.pack(side="right", fill="y")
        self.design_text.configure(yscrollcommand=scrollbar.set)
        self.design_text.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Performance tab
        perf_frame = ttk.Frame(results_notebook)
        results_notebook.add(perf_frame, text="Performance Estimates")
        self.perf_text = tk.Text(perf_frame, height=15, width=90, wrap=tk.WORD)
        scrollbar = ttk.Scrollbar(perf_frame, orient="vertical", command=self.perf_text.yview)
        scrollbar.pack(side="right", fill="y")
        self.perf_text.configure(yscrollcommand=scrollbar.set)
        self.perf_text.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Configure grid weights
        for i in range(9):
            frame.grid_rowconfigure(i, weight=1)
        for j in range(4):
            frame.grid_columnconfigure(j, weight=1)
    
    def export_motor_to_txt(self):
        try:
            # Get current date and time
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            # Get design and performance text
            design_text = self.design_text.get("1.0", tk.END)
            perf_text = self.perf_text.get("1.0", tk.END)
            
            # Ask for save location
            filepath = filedialog.asksaveasfilename(
                title="Save Motor Design Report",
                defaultextension=".txt",
                filetypes=(("Text Files", "*.txt"), ("All Files", "*.*"))
            )
            
            if filepath:
                with open(filepath, 'w') as f:
                    f.write("ROCKET MOTOR DESIGN REPORT\n")
                    f.write(f"Generated: {timestamp}\n\n")
                    f.write("DESIGN PARAMETERS\n")
                    f.write("================\n")
                    f.write(design_text)
                    f.write("\nPERFORMANCE ESTIMATES\n")
                    f.write("====================\n")
                    f.write(perf_text)
                
                self.status_var.set(f"Motor design exported to TXT: {os.path.basename(filepath)}")
                messagebox.showinfo("Export Complete", "Motor design exported to text file successfully")
            
        except Exception as e:
            messagebox.showerror("Export Error", f"Failed to export: {str(e)}")
            self.status_var.set("Error exporting motor design")
    
    def calculate_motor(self):
        try:
            # Get input values
            D = self.diameter_var.get()
            L = self.length_var.get()
            Dt = self.throat_var.get()
            De = self.exit_var.get()
            web = self.web_var.get()
            grain_type = self.grain_type_var.get()
            
            # Validate inputs
            if D <= 0 or L <= 0 or Dt <= 0 or De <= 0 or web <= 0:
                messagebox.showerror("Input Error", "All values must be positive numbers")
                return
            
            # Calculate areas
            At = math.pi * (Dt/2)**2  # Throat area
            Ae = math.pi * (De/2)**2  # Exit area
            epsilon = Ae / At  # Expansion ratio
            
            # Calculate grain parameters
            Vc = math.pi * (D/2)**2 * L  # Chamber volume
            Vp = Vc * web  # Propellant volume (approximate)
            
            # Calculate performance estimates (simplified)
            # Using typical values for APCP propellant
            Pc = 3.5e6  # Chamber pressure (Pa)
            gamma = 1.18  # Specific heat ratio
            Tc = 2800  # Chamber temperature (K)
            R = 320  # Gas constant (J/kg-K)
            M = 0.022  # Molecular weight (kg/mol)
            
            # Characteristic velocity
            c_star = math.sqrt(gamma * R * Tc / (M * gamma * (2/(gamma+1))**((gamma+1)/(gamma-1))))
            
            # Thrust coefficient
            Cf = math.sqrt((2*gamma**2/(gamma-1)) * (2/(gamma+1))**((gamma+1)/(gamma-1)) * \
                (1 - (Pc/3.5e6)**((gamma-1)/gamma))) + epsilon * (Pc/3.5e6 - 0.37)
            
            # Mass flow rate (simplified)
            m_dot = Pc * At / c_star
            
            # Thrust
            F = Cf * Pc * At
            
            # Specific impulse
            Isp = F / (m_dot * 9.81)
            
            # Burn time estimate (based on web thickness and burn rate)
            burn_rate = 0.008  # m/s (typical APCP burn rate)
            burn_time = (D * web) / burn_rate
            
            # Generate design parameters
            design_params = f"""MOTOR DESIGN PARAMETERS
            
Motor Geometry:
- Diameter: {D:.3f} m
- Length: {L:.3f} m
- Chamber Volume: {Vc:.4f} m³
- Propellant Volume: {Vp:.4f} m³ (Web Fraction: {web:.2f})

Nozzle Geometry:
- Throat Diameter: {Dt:.4f} m
- Exit Diameter: {De:.4f} m
- Throat Area: {At:.6f} m²
- Exit Area: {Ae:.6f} m²
- Expansion Ratio: {epsilon:.2f}

Grain Configuration:
- Type: {grain_type}
- Estimated Burn Time: {burn_time:.2f} s
"""
            
            # Generate performance estimates
            performance = f"""PERFORMANCE ESTIMATES
            
Theoretical Performance:
- Chamber Pressure: {Pc/1e6:.1f} MPa
- Characteristic Velocity (c*): {c_star:.0f} m/s
- Thrust Coefficient (Cf): {Cf:.2f}
- Mass Flow Rate: {m_dot:.3f} kg/s
- Thrust: {F:.1f} N ({F/9.81:.1f} kgf)
- Specific Impulse: {Isp:.1f} s

Estimated Flight Performance:
- Total Impulse: {F*burn_time:.0f} N·s
- Propellant Mass: {m_dot*burn_time:.3f} kg
- Average Thrust: {F:.1f} N
"""
            
            # Update display
            self.design_text.config(state=tk.NORMAL)
            self.design_text.delete(1.0, tk.END)
            self.design_text.insert(tk.END, design_params)
            self.design_text.config(state=tk.DISABLED)
            
            self.perf_text.config(state=tk.NORMAL)
            self.perf_text.delete(1.0, tk.END)
            self.perf_text.insert(tk.END, performance)
            self.perf_text.config(state=tk.DISABLED)
            
            self.status_var.set("Motor design calculated successfully")
            
        except Exception as e:
            self.status_var.set(f"Error in motor calculations: {str(e)}")
            messagebox.showerror("Calculation Error", f"An error occurred: {str(e)}")
    
    def create_propellant_calc_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Propellant Calc")
        
        # Header
        ttk.Label(frame, text="Propellant Formulation Calculator", font=('Times New Roman', 12, 'bold')).grid(row=0, column=0, columnspan=4, pady=10)
        
        # Propellant components
        ttk.Label(frame, text="AP (Ammonium Perchlorate):").grid(row=1, column=0, sticky='e')
        self.ap_var = tk.DoubleVar(value=70.0)
        ttk.Entry(frame, textvariable=self.ap_var, width=10).grid(row=1, column=1, sticky='w')
        ttk.Label(frame, text="%").grid(row=1, column=2, sticky='w')
        
        ttk.Label(frame, text="Aluminum Powder:").grid(row=2, column=0, sticky='e')
        self.al_var = tk.DoubleVar(value=18.0)
        ttk.Entry(frame, textvariable=self.al_var, width=10).grid(row=2, column=1, sticky='w')
        ttk.Label(frame, text="%").grid(row=2, column=2, sticky='w')
        
        ttk.Label(frame, text="HTPB Binder:").grid(row=3, column=0, sticky='e')
        self.htpb_var = tk.DoubleVar(value=12.0)
        ttk.Entry(frame, textvariable=self.htpb_var, width=10).grid(row=3, column=1, sticky='w')
        ttk.Label(frame, text="%").grid(row=3, column=2, sticky='w')
        
        # Additives
        ttk.Label(frame, text="Additives (Fe2O3, etc):").grid(row=4, column=0, sticky='e')
        self.add_var = tk.DoubleVar(value=0.0)
        ttk.Entry(frame, textvariable=self.add_var, width=10).grid(row=4, column=1, sticky='w')
        ttk.Label(frame, text="%").grid(row=4, column=2, sticky='w')
        
        # Burn rate parameters
        ttk.Label(frame, text="Burn Rate Coefficient (a):").grid(row=5, column=0, sticky='e')
        self.a_var = tk.DoubleVar(value=0.0002)
        ttk.Entry(frame, textvariable=self.a_var, width=10).grid(row=5, column=1, sticky='w')
        ttk.Label(frame, text="m/s/Pa^n").grid(row=5, column=2, sticky='w')
        
        ttk.Label(frame, text="Burn Rate Exponent (n):").grid(row=6, column=0, sticky='e')
        self.n_var = tk.DoubleVar(value=0.35)
        ttk.Entry(frame, textvariable=self.n_var, width=10).grid(row=6, column=1, sticky='w')
        
        # Calculate button
        ttk.Button(frame, text="Calculate Propellant", command=self.calculate_propellant).grid(row=7, column=0, columnspan=3, pady=10)
        
        # Export button
        ttk.Button(frame, text="Export to TXT", command=self.export_propellant_to_txt).grid(row=7, column=3, pady=10)
        
        # Results notebook
        results_notebook = ttk.Notebook(frame)
        results_notebook.grid(row=8, column=0, columnspan=4, sticky='nsew', padx=5, pady=5)
        
        # Formulation tab
        form_frame = ttk.Frame(results_notebook)
        results_notebook.add(form_frame, text="Formulation")
        self.form_text = tk.Text(form_frame, height=15, width=90, wrap=tk.WORD)
        scrollbar = ttk.Scrollbar(form_frame, orient="vertical", command=self.form_text.yview)
        scrollbar.pack(side="right", fill="y")
        self.form_text.configure(yscrollcommand=scrollbar.set)
        self.form_text.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Properties tab
        prop_frame = ttk.Frame(results_notebook)
        results_notebook.add(prop_frame, text="Properties")
        self.prop_text = tk.Text(prop_frame, height=15, width=90, wrap=tk.WORD)
        scrollbar = ttk.Scrollbar(prop_frame, orient="vertical", command=self.prop_text.yview)
        scrollbar.pack(side="right", fill="y")
        self.prop_text.configure(yscrollcommand=scrollbar.set)
        self.prop_text.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Configure grid weights
        for i in range(9):
            frame.grid_rowconfigure(i, weight=1)
        for j in range(4):
            frame.grid_columnconfigure(j, weight=1)
    
    def export_propellant_to_txt(self):
        try:
            # Get current date and time
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            # Get formulation and properties text
            form_text = self.form_text.get("1.0", tk.END)
            prop_text = self.prop_text.get("1.0", tk.END)
            
            # Ask for save location
            filepath = filedialog.asksaveasfilename(
                title="Save Propellant Report",
                defaultextension=".txt",
                filetypes=(("Text Files", "*.txt"), ("All Files", "*.*"))
            )
            
            if filepath:
                with open(filepath, 'w') as f:
                    f.write("PROPELLANT FORMULATION REPORT\n")
                    f.write(f"Generated: {timestamp}\n\n")
                    f.write("FORMULATION\n")
                    f.write("===========\n")
                    f.write(form_text)
                    f.write("\nPROPERTIES\n")
                    f.write("==========\n")
                    f.write(prop_text)
                
                self.status_var.set(f"Propellant data exported to TXT: {os.path.basename(filepath)}")
                messagebox.showinfo("Export Complete", "Propellant data exported to text file successfully")
            
        except Exception as e:
            messagebox.showerror("Export Error", f"Failed to export: {str(e)}")
            self.status_var.set("Error exporting propellant data")
    
    def calculate_propellant(self):
        try:
            # Get input values
            ap = self.ap_var.get()
            al = self.al_var.get()
            htpb = self.htpb_var.get()
            add = self.add_var.get()
            a = self.a_var.get()
            n = self.n_var.get()
            
            # Validate inputs
            total = ap + al + htpb + add
            if abs(total - 100.0) > 0.1:
                messagebox.showerror("Input Error", "Component percentages must sum to 100%")
                return
            
            if n <= 0 or n >= 1:
                messagebox.showerror("Input Error", "Burn rate exponent must be between 0 and 1")
                return
            
            # Calculate theoretical properties
            # These are simplified empirical relationships
            density = 0.01 * (ap * 1.95 + al * 2.70 + htpb * 0.92 + add * 2.5)  # g/cm³
            
            # Adiabatic flame temperature (simplified)
            T_flame = 2800 + 50 * (ap - 65) + 100 * al
            
            # Specific impulse estimate (simplified)
            Isp_vac = 250 + 0.5 * ap + 2.0 * al - 0.1 * htpb
            
            # Characteristic velocity estimate
            c_star = 1500 + 10 * ap + 20 * al - 5 * htpb
            
            # Generate formulation report
            formulation = f"""PROPELLANT FORMULATION
            
Composition:
- Ammonium Perchlorate (AP): {ap:.1f}%
- Aluminum Powder (Al): {al:.1f}%
- HTPB Binder: {htpb:.1f}%
- Additives: {add:.1f}%
- Total: {total:.1f}%

Processing Parameters:
- Mixing Temperature: 50-60°C
- Cure Time: 5-7 days at 60°C
- Pot Life: 4-6 hours
- Viscosity: 20,000-50,000 cP
"""
            
            # Generate properties report
            properties = f"""THEORETICAL PROPERTIES
            
Physical Properties:
- Density: {density:.3f} g/cm³
- Theoretical Density: {density*1.05:.3f} g/cm³ (with processing)
- Mechanical Strength: 0.8-1.2 MPa

Combustion Properties:
- Burn Rate at 7MPa: {a * (7e6)**n * 1000:.1f} mm/s
- Burn Rate Exponent (n): {n:.3f}
- Pressure Sensitivity: {n*100:.1f}%
- Temperature Sensitivity: 0.2-0.4%/°C

Performance Properties:
- Adiabatic Flame Temp: {T_flame:.0f} K
- Specific Impulse (vac): {Isp_vac:.1f} s
- Characteristic Velocity: {c_star:.0f} m/s
- Combustion Gas MW: 28-32 g/mol
"""
            
            # Update display
            self.form_text.config(state=tk.NORMAL)
            self.form_text.delete(1.0, tk.END)
            self.form_text.insert(tk.END, formulation)
            self.form_text.config(state=tk.DISABLED)
            
            self.prop_text.config(state=tk.NORMAL)
            self.prop_text.delete(1.0, tk.END)
            self.prop_text.insert(tk.END, properties)
            self.prop_text.config(state=tk.DISABLED)
            
            self.status_var.set("Propellant calculated successfully")
            
        except Exception as e:
            self.status_var.set(f"Error in propellant calculations: {str(e)}")
            messagebox.showerror("Calculation Error", f"An error occurred: {str(e)}")
    
    def create_flight_sim_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Flight Sim")
        
        # Header
        ttk.Label(frame, text="Rocket Flight Simulation", font=('Times New Roman', 12, 'bold')).grid(row=0, column=0, columnspan=4, pady=10)
        
        # Rocket parameters
        ttk.Label(frame, text="Rocket Mass (empty):").grid(row=1, column=0, sticky='e')
        self.rocket_mass_var = tk.DoubleVar(value=10.0)
        ttk.Entry(frame, textvariable=self.rocket_mass_var, width=10).grid(row=1, column=1, sticky='w')
        ttk.Label(frame, text="kg").grid(row=1, column=2, sticky='w')
        
        ttk.Label(frame, text="Propellant Mass:").grid(row=2, column=0, sticky='e')
        self.prop_mass_var = tk.DoubleVar(value=5.0)
        ttk.Entry(frame, textvariable=self.prop_mass_var, width=10).grid(row=2, column=1, sticky='w')
        ttk.Label(frame, text="kg").grid(row=2, column=2, sticky='w')
        
        ttk.Label(frame, text="Average Thrust:").grid(row=3, column=0, sticky='e')
        self.thrust_var = tk.DoubleVar(value=500.0)
        ttk.Entry(frame, textvariable=self.thrust_var, width=10).grid(row=3, column=1, sticky='w')
        ttk.Label(frame, text="N").grid(row=3, column=2, sticky='w')
        
        ttk.Label(frame, text="Burn Time:").grid(row=4, column=0, sticky='e')
        self.burn_time_var = tk.DoubleVar(value=5.0)
        ttk.Entry(frame, textvariable=self.burn_time_var, width=10).grid(row=4, column=1, sticky='w')
        ttk.Label(frame, text="s").grid(row=4, column=2, sticky='w')
        
        ttk.Label(frame, text="Drag Coefficient:").grid(row=5, column=0, sticky='e')
        self.cd_var = tk.DoubleVar(value=0.5)
        ttk.Entry(frame, textvariable=self.cd_var, width=10).grid(row=5, column=1, sticky='w')
        
        ttk.Label(frame, text="Rocket Diameter:").grid(row=6, column=0, sticky='e')
        self.rocket_dia_var = tk.DoubleVar(value=0.1)
        ttk.Entry(frame, textvariable=self.rocket_dia_var, width=10).grid(row=6, column=1, sticky='w')
        ttk.Label(frame, text="m").grid(row=6, column=2, sticky='w')
        
        # Simulation button
        ttk.Button(frame, text="Run Flight Simulation", command=self.run_flight_sim).grid(row=7, column=0, columnspan=3, pady=10)
        
        # Export button
        ttk.Button(frame, text="Export to TXT", command=self.export_flight_to_txt).grid(row=7, column=3, pady=10)
        
        # Results notebook
        results_notebook = ttk.Notebook(frame)
        results_notebook.grid(row=8, column=0, columnspan=4, sticky='nsew', padx=5, pady=5)
        
        # Results tab
        results_frame = ttk.Frame(results_notebook)
        results_notebook.add(results_frame, text="Flight Results")
        self.results_text = tk.Text(results_frame, height=15, width=90, wrap=tk.WORD)
        scrollbar = ttk.Scrollbar(results_frame, orient="vertical", command=self.results_text.yview)
        scrollbar.pack(side="right", fill="y")
        self.results_text.configure(yscrollcommand=scrollbar.set)
        self.results_text.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Configure grid weights
        for i in range(9):
            frame.grid_rowconfigure(i, weight=1)
        for j in range(4):
            frame.grid_columnconfigure(j, weight=1)
    
    def export_flight_to_txt(self):
        try:
            # Get current date and time
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            # Get results text
            results_text = self.results_text.get("1.0", tk.END)
            
            # Ask for save location
            filepath = filedialog.asksaveasfilename(
                title="Save Flight Report",
                defaultextension=".txt",
                filetypes=(("Text Files", "*.txt"), ("All Files", "*.*"))
            )
            
            if filepath:
                with open(filepath, 'w') as f:
                    f.write("FLIGHT SIMULATION REPORT\n")
                    f.write(f"Generated: {timestamp}\n\n")
                    f.write("SIMULATION RESULTS\n")
                    f.write("=================\n")
                    f.write(results_text)
                
                self.status_var.set(f"Flight data exported to TXT: {os.path.basename(filepath)}")
                messagebox.showinfo("Export Complete", "Flight data exported to text file successfully")
            
        except Exception as e:
            messagebox.showerror("Export Error", f"Failed to export: {str(e)}")
            self.status_var.set("Error exporting flight data")
    
    def run_flight_sim(self):
        try:
            # Get input values
            m_rocket = self.rocket_mass_var.get()
            m_prop = self.prop_mass_var.get()
            F_avg = self.thrust_var.get()
            t_burn = self.burn_time_var.get()
            Cd = self.cd_var.get()
            D = self.rocket_dia_var.get()
            
            # Validate inputs
            if m_rocket <= 0 or m_prop <= 0 or F_avg <= 0 or t_burn <= 0 or Cd <= 0 or D <= 0:
                messagebox.showerror("Input Error", "All values must be positive numbers")
                return
            
            # Constants
            g = 9.81  # m/s²
            rho_air = 1.225  # kg/m³ at sea level
            A = math.pi * (D/2)**2  # Frontal area
            
            # Initial conditions
            m_total = m_rocket + m_prop
            m_dot = m_prop / t_burn  # Mass flow rate
            
            # Time array (simplified - in a real simulation we'd use smaller steps)
            times = [0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0]
            altitude = [0.0] * len(times)
            velocity = [0.0] * len(times)
            acceleration = [0.0] * len(times)
            
            # Simplified simulation (in a real app we'd use numerical integration)
            for i in range(1, len(times)):
                t = times[i]
                
                # Update mass
                if t < t_burn:
                    mass = m_total - m_dot * t
                    thrust = F_avg
                else:
                    mass = m_rocket
                    thrust = 0
                
                # Simplified physics (no real integration here)
                if i == 1:
                    # Initial acceleration
                    accel = (thrust - mass * g) / mass
                    vel = accel * (times[i] - times[i-1])
                    alt = 0.5 * accel * (times[i] - times[i-1])**2
                else:
                    # Simplified progression
                    if thrust > 0:
                        # Powered flight
                        accel = (thrust - 0.5 * rho_air * velocity[i-1]**2 * Cd * A) / mass - g
                        vel = velocity[i-1] + accel * (times[i] - times[i-1])
                        alt = altitude[i-1] + vel * (times[i] - times[i-1])
                    else:
                        # Coasting
                        accel = -g - (0.5 * rho_air * velocity[i-1]**2 * Cd * A) / mass
                        vel = velocity[i-1] + accel * (times[i] - times[i-1])
                        alt = altitude[i-1] + vel * (times[i] - times[i-1])
                
                # Don't go below ground
                if alt < 0:
                    alt = 0
                    vel = 0
                    accel = 0
                
                altitude[i] = alt
                velocity[i] = vel
                acceleration[i] = accel
            
            # Find important points
            burnout_idx = min(len(times)-1, int(t_burn))
            apogee_idx = altitude.index(max(altitude))
            
            # Generate results
            results = f"""FLIGHT SIMULATION RESULTS
            
Initial Conditions:
- Total Mass: {m_total:.2f} kg
- Propellant Mass: {m_prop:.2f} kg
- Average Thrust: {F_avg:.1f} N
- Burn Time: {t_burn:.1f} s
- Drag Coefficient: {Cd:.2f}
- Diameter: {D:.3f} m

Flight Performance:
- Burnout Altitude: {altitude[burnout_idx]:.1f} m
- Burnout Velocity: {velocity[burnout_idx]:.1f} m/s
- Apogee: {max(altitude):.1f} m
- Time to Apogee: {times[apogee_idx]:.1f} s
- Maximum Acceleration: {max(acceleration)/g:.1f} g
- Maximum Velocity: {max(velocity):.1f} m/s
- Maximum Dynamic Pressure: {0.5*1.225*max(velocity)**2/1000:.1f} kPa

Time History:
Time(s)  Alt(m)  Vel(m/s)  Accel(m/s²)
------------------------------------"""
            
            for i in range(len(times)):
                results += f"\n{times[i]:6.1f}  {altitude[i]:6.1f}  {velocity[i]:7.1f}  {acceleration[i]:9.1f}"
            
            # Update display
            self.results_text.config(state=tk.NORMAL)
            self.results_text.delete(1.0, tk.END)
            self.results_text.insert(tk.END, results)
            self.results_text.config(state=tk.DISABLED)
            
            self.status_var.set("Flight simulation completed successfully")
            
        except Exception as e:
            self.status_var.set(f"Error in flight simulation: {str(e)}")
            messagebox.showerror("Simulation Error", f"An error occurred: {str(e)}")
    
    def create_telemetry_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Telemetry")
        
        # Header
        ttk.Label(frame, text="Rocket Telemetry Analysis", font=('Times New Roman', 12, 'bold')).grid(row=0, column=0, columnspan=4, pady=10)
        
        # Data controls
        ttk.Button(frame, text="Load Telemetry Data", command=self.load_telemetry).grid(row=1, column=0, pady=5)
        ttk.Button(frame, text="Analyze Flight", command=self.analyze_telemetry).grid(row=1, column=1, pady=5)
        ttk.Button(frame, text="Export Report", command=self.export_report).grid(row=1, column=2, pady=5)
        ttk.Button(frame, text="Export to TXT", command=self.export_telemetry_to_txt).grid(row=1, column=3, pady=5)
        
        # Data display
        self.telemetry_text = tk.Text(frame, height=25, width=90, wrap=tk.WORD)
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=self.telemetry_text.yview)
        scrollbar.grid(row=2, column=4, sticky='ns')
        self.telemetry_text.configure(yscrollcommand=scrollbar.set)
        self.telemetry_text.grid(row=2, column=0, columnspan=4, padx=5, pady=5)
        
        # Configure grid weights
        for i in range(3):
            frame.grid_rowconfigure(i, weight=1)
        for j in range(4):
            frame.grid_columnconfigure(j, weight=1)
    
    def export_telemetry_to_txt(self):
        if not self.flight_data:
            messagebox.showwarning("No Data", "No telemetry data to export")
            return
        
        try:
            # Get current date and time
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            # Get telemetry text
            telemetry_text = self.telemetry_text.get("1.0", tk.END)
            
            # Ask for save location
            filepath = filedialog.asksaveasfilename(
                title="Save Telemetry Report",
                defaultextension=".txt",
                filetypes=(("Text Files", "*.txt"), ("All Files", "*.*"))
            )
            
            if filepath:
                with open(filepath, 'w') as f:
                    f.write("TELEMETRY ANALYSIS REPORT\n")
                    f.write(f"Generated: {timestamp}\n\n")
                    f.write(telemetry_text)
                
                self.status_var.set(f"Telemetry data exported to TXT: {os.path.basename(filepath)}")
                messagebox.showinfo("Export Complete", "Telemetry data exported to text file successfully")
            
        except Exception as e:
            messagebox.showerror("Export Error", f"Failed to export: {str(e)}")
            self.status_var.set("Error exporting telemetry data")
    
    def load_telemetry(self):
        filepath = filedialog.askopenfilename(
            title="Select Telemetry File",
            filetypes=(("JSON Files", "*.json"), ("All Files", "*.*"))
        )
        
        if filepath:
            try:
                with open(filepath, 'r') as f:
                    self.flight_data = json.load(f)
                
                self.telemetry_text.config(state=tk.NORMAL)
                self.telemetry_text.delete(1.0, tk.END)
                self.telemetry_text.insert(tk.END, f"Loaded telemetry data from: {filepath}\n\n")
                self.telemetry_text.insert(tk.END, "Time(s)  Alt(m)  Vel(m/s)  Accel(m/s²)\n")
                self.telemetry_text.insert(tk.END, "------------------------------------\n")
                
                for point in self.flight_data:
                    self.telemetry_text.insert(tk.END, 
                        f"{point['time']:6.2f}  {point['altitude']:6.1f}  {point['velocity']:7.1f}  {point['accel']:9.1f}\n")
                
                self.telemetry_text.config(state=tk.DISABLED)
                self.status_var.set(f"Telemetry data loaded from {os.path.basename(filepath)}")
                
            except Exception as e:
                messagebox.showerror("Load Error", f"Failed to load telemetry data: {str(e)}")
                self.status_var.set("Error loading telemetry data")
    
    def analyze_telemetry(self):
        if not self.flight_data:
            messagebox.showwarning("No Data", "Please load telemetry data first")
            return
        
        try:
            # Extract data
            times = [p['time'] for p in self.flight_data]
            altitudes = [p['altitude'] for p in self.flight_data]
            velocities = [p['velocity'] for p in self.flight_data]
            accelerations = [p['accel'] for p in self.flight_data]
            
            # Calculate statistics
            max_alt = max(altitudes)
            max_vel = max(velocities)
            max_accel = max(accelerations)
            burn_time = times[velocities.index(max_vel)]  # Approximate burnout
            apogee_time = times[altitudes.index(max_alt)]
            
            # Generate analysis
            analysis = f"""TELEMETRY ANALYSIS RESULTS
            
Flight Statistics:
- Maximum Altitude: {max_alt:.1f} m
- Maximum Velocity: {max_vel:.1f} m/s
- Maximum Acceleration: {max_accel:.1f} m/s² ({max_accel/9.81:.1f} g)
- Burnout Time: {burn_time:.2f} s
- Apogee Time: {apogee_time:.2f} s
- Descent Rate: {-velocities[-1]:.1f} m/s (at landing)

Performance Metrics:
- Average Velocity: {sum(velocities)/len(velocities):.1f} m/s
- Average Acceleration: {sum(accelerations)/len(accelerations):.1f} m/s²
- Flight Duration: {times[-1]:.1f} s
"""
            
            self.telemetry_text.config(state=tk.NORMAL)
            self.telemetry_text.insert(tk.END, "\n\n" + analysis)
            self.telemetry_text.config(state=tk.DISABLED)
            
            self.status_var.set("Telemetry data analyzed successfully")
            
        except Exception as e:
            messagebox.showerror("Analysis Error", f"Failed to analyze telemetry: {str(e)}")
            self.status_var.set("Error analyzing telemetry data")
    
    def export_report(self):
        if not self.flight_data:
            messagebox.showwarning("No Data", "No telemetry data to export")
            return
        
        filepath = filedialog.asksaveasfilename(
            title="Save Report As",
            defaultextension=".txt",
            filetypes=(("Text Files", "*.txt"), ("All Files", "*.*"))
        )
        
        if filepath:
            try:
                with open(filepath, 'w') as f:
                    f.write("ROCKET FLIGHT REPORT\n")
                    f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                    
                    # Write telemetry data
                    f.write("TELEMETRY DATA\n")
                    f.write("Time(s)  Alt(m)  Vel(m/s)  Accel(m/s²)\n")
                    f.write("------------------------------------\n")
                    
                    for point in self.flight_data:
                        f.write(f"{point['time']:6.2f}  {point['altitude']:6.1f}  {point['velocity']:7.1f}  {point['accel']:9.1f}\n")
                    
                    # Write analysis
                    f.write("\n\nANALYSIS\n")
                    analysis_text = self.telemetry_text.get("1.0", tk.END)
                    if "TELEMETRY ANALYSIS RESULTS" in analysis_text:
                        f.write(analysis_text.split("TELEMETRY ANALYSIS RESULTS")[1])
                
                self.status_var.set(f"Report saved to {os.path.basename(filepath)}")
                messagebox.showinfo("Export Complete", "Flight report exported successfully")
                
            except Exception as e:
                messagebox.showerror("Export Error", f"Failed to export report: {str(e)}")
                self.status_var.set("Error exporting report")
    
    def create_orbital_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Orbital Mechanics")
        
        # Header
        ttk.Label(frame, text="Orbital Mechanics Calculator", font=('Times New Roman', 12, 'bold')).grid(row=0, column=0, columnspan=4, pady=10)
        
        # Orbit parameters
        ttk.Label(frame, text="Semi-major Axis:").grid(row=1, column=0, sticky='e')
        self.sma_var = tk.DoubleVar(value=7000.0)  # km
        ttk.Entry(frame, textvariable=self.sma_var, width=10).grid(row=1, column=1, sticky='w')
        ttk.Label(frame, text="km").grid(row=1, column=2, sticky='w')
        
        ttk.Label(frame, text="Eccentricity:").grid(row=2, column=0, sticky='e')
        self.ecc_var = tk.DoubleVar(value=0.0)
        ttk.Entry(frame, textvariable=self.ecc_var, width=10).grid(row=2, column=1, sticky='w')
        
        ttk.Label(frame, text="Inclination:").grid(row=3, column=0, sticky='e')
        self.inc_var = tk.DoubleVar(value=30.0)
        ttk.Entry(frame, textvariable=self.inc_var, width=10).grid(row=3, column=1, sticky='w')
        ttk.Label(frame, text="deg").grid(row=3, column=2, sticky='w')
        
        ttk.Label(frame, text="Satellite Mass:").grid(row=4, column=0, sticky='e')
        self.sat_mass_var = tk.DoubleVar(value=1000.0)
        ttk.Entry(frame, textvariable=self.sat_mass_var, width=10).grid(row=4, column=1, sticky='w')
        ttk.Label(frame, text="kg").grid(row=4, column=2, sticky='w')
        
        # Calculate button
        ttk.Button(frame, text="Calculate Orbit", command=self.calculate_orbit).grid(row=5, column=0, columnspan=3, pady=10)
        
        # Export button
        ttk.Button(frame, text="Export to TXT", command=self.export_orbit_to_txt).grid(row=5, column=3, pady=10)
        
        # Results notebook
        results_notebook = ttk.Notebook(frame)
        results_notebook.grid(row=6, column=0, columnspan=4, sticky='nsew', padx=5, pady=5)
        
        # Parameters tab
        param_frame = ttk.Frame(results_notebook)
        results_notebook.add(param_frame, text="Orbit Parameters")
        self.param_text = tk.Text(param_frame, height=15, width=90, wrap=tk.WORD)
        scrollbar = ttk.Scrollbar(param_frame, orient="vertical", command=self.param_text.yview)
        scrollbar.pack(side="right", fill="y")
        self.param_text.configure(yscrollcommand=scrollbar.set)
        self.param_text.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Configure grid weights
        for i in range(7):
            frame.grid_rowconfigure(i, weight=1)
        for j in range(4):
            frame.grid_columnconfigure(j, weight=1)
    
    def export_orbit_to_txt(self):
        try:
            # Get current date and time
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            # Get parameters text
            param_text = self.param_text.get("1.0", tk.END)
            
            # Ask for save location
            filepath = filedialog.asksaveasfilename(
                title="Save Orbit Report",
                defaultextension=".txt",
                filetypes=(("Text Files", "*.txt"), ("All Files", "*.*"))
            )
            
            if filepath:
                with open(filepath, 'w') as f:
                    f.write("ORBITAL MECHANICS REPORT\n")
                    f.write(f"Generated: {timestamp}\n\n")
                    f.write("ORBITAL PARAMETERS\n")
                    f.write("=================\n")
                    f.write(param_text)
                
                self.status_var.set(f"Orbit data exported to TXT: {os.path.basename(filepath)}")
                messagebox.showinfo("Export Complete", "Orbit data exported to text file successfully")
            
        except Exception as e:
            messagebox.showerror("Export Error", f"Failed to export: {str(e)}")
            self.status_var.set("Error exporting orbit data")
    
    def calculate_orbit(self):
        try:
            # Constants
            mu_earth = 3.986e5  # km³/s²
            R_earth = 6378  # km
            
            # Get input values
            a = self.sma_var.get()  # km
            e = self.ecc_var.get()
            i = self.inc_var.get()  # deg
            m = self.sat_mass_var.get()  # kg
            
            # Validate inputs
            if a <= R_earth:
                messagebox.showerror("Input Error", "Semi-major axis must be > Earth radius (6378 km)")
                return
            
            if e < 0 or e >= 1:
                messagebox.showerror("Input Error", "Eccentricity must be 0 ≤ e < 1")
                return
            
            # Calculate orbital parameters
            rp = a * (1 - e)  # Perigee radius (km)
            ra = a * (1 + e)  # Apogee radius (km)
            p = a * (1 - e**2)  # Semi-latus rectum (km)
            
            # Calculate orbital velocities
            vp = math.sqrt(mu_earth * (2/rp - 1/a))  # Perigee velocity (km/s)
            va = math.sqrt(mu_earth * (2/ra - 1/a))  # Apogee velocity (km/s)
            
            # Calculate orbital period
            T = 2 * math.pi * math.sqrt(a**3 / mu_earth)  # Seconds
            T_hours = T / 3600  # Hours
            
            # Calculate energies
            E = -mu_earth / (2 * a)  # Specific energy (km²/s²)
            KE_perigee = 0.5 * vp**2  # Specific kinetic energy at perigee
            PE_perigee = -mu_earth / rp  # Specific potential energy at perigee
            
            # Generate orbit parameters
            params = f"""ORBITAL PARAMETERS
            
Basic Parameters:
- Semi-major Axis: {a:.1f} km
- Eccentricity: {e:.3f}
- Inclination: {i:.1f}°
- Perigee Altitude: {rp - R_earth:.1f} km
- Apogee Altitude: {ra - R_earth:.1f} km

Orbital Mechanics:
- Orbital Period: {T:.1f} s ({T_hours:.2f} hours)
- Perigee Velocity: {vp:.3f} km/s
- Apogee Velocity: {va:.3f} km/s
- Specific Orbital Energy: {E:.3f} km²/s²

Satellite Properties:
- Mass: {m:.1f} kg
- Kinetic Energy at Perigee: {0.5 * m * vp**2 * 1e6:.3e} J
- Potential Energy at Perigee: {-mu_earth * m * 1e6 / rp:.3e} J
- Total Energy: {E * m * 1e6:.3e} J
"""
            
            # Update display
            self.param_text.config(state=tk.NORMAL)
            self.param_text.delete(1.0, tk.END)
            self.param_text.insert(tk.END, params)
            self.param_text.config(state=tk.DISABLED)
            
            self.status_var.set("Orbit calculated successfully")
            
        except Exception as e:
            self.status_var.set(f"Error in orbit calculations: {str(e)}")
            messagebox.showerror("Calculation Error", f"An error occurred: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = RocketryApp(root)
    root.mainloop()