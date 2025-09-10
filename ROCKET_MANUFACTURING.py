# -*- coding: utf-8 -*-
"""
Created on Thu Aug 14 20:39:39 2025

@author: samng
"""

# -*- coding: utf-8 -*-
"""
GRIMSTRE DIGITAL TOOLS - Solid Motor Manufacturing & Flight Analysis
with Advanced Propellant Formulation Tools
Python 3.9 Tkinter Version
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import math
import json
import os
from datetime import datetime

class GrimstreDigitalTools:
    def __init__(self, root):
        self.root = root
        self.root.title("Rocketry Pro MAX - GRIMSTRE DIGITAL TOOLS")
        self.root.geometry("1400x1000")
        
        # Configure default font
        default_font = ('Arial', 10)
        self.root.option_add('*Font', default_font)
        
        # Configure style
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('TFrame', padding=10, background='#f0f0f0')
        self.style.configure('TLabel', padding=5, font=default_font, background='#f0f0f0')
        self.style.configure('TButton', padding=5, font=default_font)
        self.style.configure('TCombobox', font=default_font)
        self.style.configure('TNotebook', font=default_font)
        self.style.configure('TNotebook.Tab', font=default_font, padding=[10, 5])
        self.style.configure('Header.TLabel', font=('Arial', 12, 'bold'))
        self.style.configure('Warning.TLabel', font=('Arial', 10, 'bold'), foreground='red', background='yellow')
        
        # Safety warning
        self.safety_warning = ttk.Label(
            root, 
            text="⚠️ WARNING: Rocket motors and propellants contain high-energy materials. Follow all safety protocols and regulations. ⚠️",
            style='Warning.TLabel',
            padding=10
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
        self.create_terminology_tab()
        self.create_pyrocellulose_tab()
        self.create_contact_tab()
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready - GRIMSTRE DIGITAL TOOLS v2.1")
        self.status_bar = ttk.Label(root, textvariable=self.status_var, relief=tk.SUNKEN)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Initialize variables
        self.flight_data = []
        self.current_project = None
        self.telemetry_data = []
    
    def create_terminology_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Terminology Guide")
        
        # Header
        ttk.Label(frame, text="Rocketry Terminology and Instructions", style='Header.TLabel').grid(row=0, column=0, columnspan=2, pady=10)
        
        # Create notebook for subtabs
        term_notebook = ttk.Notebook(frame)
        term_notebook.grid(row=1, column=0, columnspan=2, sticky='nsew', padx=10, pady=10)
        
        # Motor Design Terms
        motor_frame = ttk.Frame(term_notebook)
        term_notebook.add(motor_frame, text="Motor Design")
        
        motor_text = """MOTOR DESIGN TERMINOLOGY:

1. Motor Diameter: Inner diameter of the motor casing (meters)
2. Motor Length: Total length of the motor casing (meters)
3. Nozzle Throat: Narrowest part of the nozzle (meters)
4. Nozzle Exit: Diameter at nozzle exit (meters)
5. Grain Configuration: Shape of propellant grain
   - Cylindrical: Simple hollow cylinder
   - Star: Star-shaped core for progressive burn
   - Wagon Wheel: Complex core geometry
   - End Burner: Burns from one end only
6. Web Fraction: Fraction of grain that burns radially

CALCULATION NOTES:
- Calculations assume ideal gas behavior
- Performance estimates are theoretical maximums
- Real-world results may vary by 10-15%
"""
        motor_text_widget = tk.Text(motor_frame, wrap=tk.WORD, font=('Consolas', 10), padx=10, pady=10)
        motor_text_widget.insert(tk.END, motor_text)
        motor_text_widget.config(state=tk.DISABLED)
        motor_text_widget.pack(fill='both', expand=True)
        
        # Propellant Terms
        prop_frame = ttk.Frame(term_notebook)
        term_notebook.add(prop_frame, text="Propellant")
        
        prop_text = """PROPELLANT TERMINOLOGY:

1. AP (Ammonium Perchlorate): Oxidizer (70-80% typical)
2. Aluminum Powder: Fuel (15-20% typical)
3. HTPB Binder: Rubber-based fuel/binder (10-15% typical)
4. Additives: Various performance modifiers
   - Burn rate modifiers: Fe2O3, CuO, PbO
   - Stabilizers: CaCO3, MgO
   - Opacifiers: Carbon black
   - Bonding agents: MAPO, Tepanol

COMMON PROPELLANT TYPES:
1. APCP (Ammonium Perchlorate Composite Propellant):
   - AP + Al + HTPB
   - Most common in amateur rocketry
2. Black Powder:
   - KNO3 + Charcoal + Sulfur
   - Used in small motors and ejection charges
3. Double Base:
   - Nitrocellulose + Nitroglycerin
   - Used in military applications
4. Hybrid:
   - Solid fuel + Liquid oxidizer
   - Often HTPB + N2O

NITROCELLULOSE TYPES:
1. Pyrocellulose (12.0-12.6% N):
   - Used in smokeless powders
2. Gun Cotton (>12.6% N):
   - High explosive grade
"""
        prop_text_widget = tk.Text(prop_frame, wrap=tk.WORD, font=('Consolas', 10), padx=10, pady=10)
        prop_text_widget.insert(tk.END, prop_text)
        prop_text_widget.config(state=tk.DISABLED)
        prop_text_widget.pack(fill='both', expand=True)
        
        # Flight Sim Terms
        flight_frame = ttk.Frame(term_notebook)
        term_notebook.add(flight_frame, text="Flight Sim")
        
        flight_text = """FLIGHT SIMULATION TERMINOLOGY:

1. Rocket Mass: Dry mass without propellant (kg)
2. Propellant Mass: Mass of fuel/oxidizer (kg)
3. Average Thrust: Mean thrust over burn (N)
4. Burn Time: Duration of thrust phase (s)
5. Drag Coefficient: Aerodynamic drag factor
6. Rocket Diameter: Max body diameter (m)

SIMULATION NOTES:
- Uses simplified physics model
- Assumes vertical flight only
- No wind or atmospheric variations
- Drag model is approximate
"""
        flight_text_widget = tk.Text(flight_frame, wrap=tk.WORD, font=('Consolas', 10), padx=10, pady=10)
        flight_text_widget.insert(tk.END, flight_text)
        flight_text_widget.config(state=tk.DISABLED)
        flight_text_widget.pack(fill='both', expand=True)
        
        # Telemetry Guide
        tele_frame = ttk.Frame(term_notebook)
        term_notebook.add(tele_frame, text="Telemetry")
        
        tele_text = """TELEMETRY DATA INSTRUCTIONS:

1. Data Format Requirements:
   - JSON file with array of data points
   - Each point must contain:
     - time (seconds)
     - altitude (meters)
     - velocity (m/s)
     - accel (m/s²)
   
2. Example Structure:
   [
     {"time": 0.0, "altitude": 0.0, "velocity": 0.0, "accel": 9.8},
     {"time": 0.1, "altitude": 0.05, "velocity": 1.0, "accel": 15.2},
     ...
   ]

3. Loading Data:
   - Click 'Load Telemetry Data' button
   - Select your JSON file
   - Data will display in table format
   - Use 'Analyze Flight' for statistics

4. Export Options:
   - Export to TXT: Raw data with analysis
   - Export Report: Formatted flight report
"""
        tele_text_widget = tk.Text(tele_frame, wrap=tk.WORD, font=('Consolas', 10), padx=10, pady=10)
        tele_text_widget.insert(tk.END, tele_text)
        tele_text_widget.config(state=tk.DISABLED)
        tele_text_widget.pack(fill='both', expand=True)
        
        # Configure grid weights
        frame.grid_rowconfigure(1, weight=1)
        frame.grid_columnconfigure(0, weight=1)
    
    def create_motor_design_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Motor Design")
        
        # Header
        ttk.Label(frame, text="Solid Rocket Motor Design Calculator", style='Header.TLabel').grid(row=0, column=0, columnspan=4, pady=10)
        
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
        
        # Button frame
        button_frame = ttk.Frame(frame)
        button_frame.grid(row=7, column=0, columnspan=4, pady=10)
        
        ttk.Button(button_frame, text="Calculate Motor Parameters", command=self.calculate_motor).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Export to TXT", command=self.export_motor_to_txt).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Save Design", command=self.save_motor_design).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Load Design", command=self.load_motor_design).pack(side=tk.LEFT, padx=5)
        
        # Results notebook
        results_notebook = ttk.Notebook(frame)
        results_notebook.grid(row=8, column=0, columnspan=4, sticky='nsew', padx=5, pady=5)
        
        # Design tab
        design_frame = ttk.Frame(results_notebook)
        results_notebook.add(design_frame, text="Design Parameters")
        self.design_text = tk.Text(design_frame, height=15, width=90, wrap=tk.WORD, font=('Consolas', 10))
        scrollbar = ttk.Scrollbar(design_frame, orient="vertical", command=self.design_text.yview)
        scrollbar.pack(side="right", fill="y")
        self.design_text.configure(yscrollcommand=scrollbar.set)
        self.design_text.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Performance tab
        perf_frame = ttk.Frame(results_notebook)
        results_notebook.add(perf_frame, text="Performance Estimates")
        self.perf_text = tk.Text(perf_frame, height=15, width=90, wrap=tk.WORD, font=('Consolas', 10))
        scrollbar = ttk.Scrollbar(perf_frame, orient="vertical", command=self.perf_text.yview)
        scrollbar.pack(side="right", fill="y")
        self.perf_text.configure(yscrollcommand=scrollbar.set)
        self.perf_text.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Configure grid weights
        for i in range(9):
            frame.grid_rowconfigure(i, weight=1)
        for j in range(4):
            frame.grid_columnconfigure(j, weight=1)
    
    def save_motor_design(self):
        design_data = {
            'diameter': self.diameter_var.get(),
            'length': self.length_var.get(),
            'throat': self.throat_var.get(),
            'exit': self.exit_var.get(),
            'grain_type': self.grain_type_var.get(),
            'web': self.web_var.get(),
            'design_text': self.design_text.get("1.0", tk.END),
            'performance_text': self.perf_text.get("1.0", tk.END)
        }
        
        filepath = filedialog.asksaveasfilename(
            title="Save Motor Design",
            defaultextension=".json",
            filetypes=(("JSON Files", "*.json"), ("All Files", "*.*")))
        
        if filepath:
            try:
                with open(filepath, 'w') as f:
                    json.dump(design_data, f, indent=4)
                self.status_var.set(f"Motor design saved to {os.path.basename(filepath)}")
            except Exception as e:
                messagebox.showerror("Save Error", f"Failed to save design: {str(e)}")
    
    def load_motor_design(self):
        filepath = filedialog.askopenfilename(
            title="Load Motor Design",
            filetypes=(("JSON Files", "*.json"), ("All Files", "*.*")))
        
        if filepath:
            try:
                with open(filepath, 'r') as f:
                    design_data = json.load(f)
                
                self.diameter_var.set(design_data['diameter'])
                self.length_var.set(design_data['length'])
                self.throat_var.set(design_data['throat'])
                self.exit_var.set(design_data['exit'])
                self.grain_type_var.set(design_data['grain_type'])
                self.web_var.set(design_data['web'])
                
                self.design_text.config(state=tk.NORMAL)
                self.design_text.delete(1.0, tk.END)
                self.design_text.insert(tk.END, design_data['design_text'])
                self.design_text.config(state=tk.DISABLED)
                
                self.perf_text.config(state=tk.NORMAL)
                self.perf_text.delete(1.0, tk.END)
                self.perf_text.insert(tk.END, design_data['performance_text'])
                self.perf_text.config(state=tk.DISABLED)
                
                self.status_var.set(f"Motor design loaded from {os.path.basename(filepath)}")
            except Exception as e:
                messagebox.showerror("Load Error", f"Failed to load design: {str(e)}")
    
    def export_motor_to_txt(self):
        try:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            design_text = self.design_text.get("1.0", tk.END)
            perf_text = self.perf_text.get("1.0", tk.END)
            
            filepath = filedialog.asksaveasfilename(
                title="Save Motor Design Report",
                defaultextension=".txt",
                filetypes=(("Text Files", "*.txt"), ("All Files", "*.*")))
            
            if filepath:
                with open(filepath, 'w') as f:
                    f.write("ROCKET MOTOR DESIGN REPORT\n")
                    f.write(f"Generated: {timestamp}\n")
                    f.write(f"Software: GRIMSTRE DIGITAL TOOLS v2.1\n\n")
                    f.write("DESIGN PARAMETERS\n")
                    f.write("================\n")
                    f.write(design_text)
                    f.write("\nPERFORMANCE ESTIMATES\n")
                    f.write("====================\n")
                    f.write(perf_text)
                
                self.status_var.set(f"Motor design exported to TXT: {os.path.basename(filepath)}")
                messagebox.showinfo("Export Complete", "Motor design exported successfully")
            
        except Exception as e:
            messagebox.showerror("Export Error", f"Failed to export: {str(e)}")
            self.status_var.set("Error exporting motor design")
    
    def calculate_motor(self):
        try:
            D = self.diameter_var.get()
            L = self.length_var.get()
            Dt = self.throat_var.get()
            De = self.exit_var.get()
            web = self.web_var.get()
            grain_type = self.grain_type_var.get()
            
            if D <= 0 or L <= 0 or Dt <= 0 or De <= 0 or web <= 0:
                messagebox.showerror("Input Error", "All values must be positive numbers")
                return
            
            At = math.pi * (Dt/2)**2
            Ae = math.pi * (De/2)**2
            epsilon = Ae / At
            
            Vc = math.pi * (D/2)**2 * L
            Vp = Vc * web
            
            Pc = 3.5e6  # Chamber pressure in Pa
            gamma = 1.18  # Specific heat ratio
            Tc = 2800  # Chamber temperature in K
            R = 320  # Gas constant in J/(kg·K)
            M = 0.022  # Molar mass in kg/mol
            
            c_star = math.sqrt(gamma * R * Tc / (M * gamma * (2/(gamma+1))**((gamma+1)/(gamma-1))))
            
            Cf = math.sqrt((2*gamma**2/(gamma-1)) * (2/(gamma+1))**((gamma+1)/(gamma-1)) * \
                (1 - (Pc/3.5e6)**((gamma-1)/gamma))) + epsilon * (Pc/3.5e6 - 0.37)
            
            m_dot = Pc * At / c_star
            F = Cf * Pc * At
            Isp = F / (m_dot * 9.81)
            
            burn_rate = 0.008  # m/s (simplified burn rate)
            burn_time = (D * web) / burn_rate
            
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
        ttk.Label(frame, text="Advanced Propellant Formulation Calculator", style='Header.TLabel').grid(row=0, column=0, columnspan=4, pady=10)
        
        # Propellant type selection
        ttk.Label(frame, text="Propellant Type:").grid(row=1, column=0, sticky='e')
        self.prop_type_var = tk.StringVar(value="APCP")
        prop_types = ["APCP", "Black Powder", "Double Base", "Nitrocellulose"]
        ttk.Combobox(frame, textvariable=self.prop_type_var, values=prop_types, width=15).grid(row=1, column=1, sticky='w')
        
        # APCP components
        self.apcp_frame = ttk.Frame(frame)
        self.apcp_frame.grid(row=2, column=0, columnspan=4, sticky='ew')
        
        ttk.Label(self.apcp_frame, text="AP (Ammonium Perchlorate):").grid(row=0, column=0, sticky='e')
        self.ap_var = tk.DoubleVar(value=70.0)
        ttk.Entry(self.apcp_frame, textvariable=self.ap_var, width=10).grid(row=0, column=1, sticky='w')
        ttk.Label(self.apcp_frame, text="%").grid(row=0, column=2, sticky='w')
        
        ttk.Label(self.apcp_frame, text="Aluminum Powder:").grid(row=1, column=0, sticky='e')
        self.al_var = tk.DoubleVar(value=18.0)
        ttk.Entry(self.apcp_frame, textvariable=self.al_var, width=10).grid(row=1, column=1, sticky='w')
        ttk.Label(self.apcp_frame, text="%").grid(row=1, column=2, sticky='w')
        
        ttk.Label(self.apcp_frame, text="HTPB Binder:").grid(row=2, column=0, sticky='e')
        self.htpb_var = tk.DoubleVar(value=12.0)
        ttk.Entry(self.apcp_frame, textvariable=self.htpb_var, width=10).grid(row=2, column=1, sticky='w')
        ttk.Label(self.apcp_frame, text="%").grid(row=2, column=2, sticky='w')
        
        # Additives
        ttk.Label(self.apcp_frame, text="Additives:").grid(row=3, column=0, sticky='e')
        self.add_var = tk.DoubleVar(value=0.0)
        ttk.Entry(self.apcp_frame, textvariable=self.add_var, width=10).grid(row=3, column=1, sticky='w')
        ttk.Label(self.apcp_frame, text="%").grid(row=3, column=2, sticky='w')
        
        # Additive type selection
        ttk.Label(self.apcp_frame, text="Additive Type:").grid(row=4, column=0, sticky='e')
        self.add_type_var = tk.StringVar(value="None")
        add_types = ["None", "Fe2O3 (Burn rate catalyst)", "CuO (Burn rate catalyst)", 
                    "CaCO3 (Stabilizer)", "Carbon black (Opacifier)"]
        ttk.Combobox(self.apcp_frame, textvariable=self.add_type_var, values=add_types, width=25).grid(row=4, column=1, columnspan=2, sticky='w')
        
        # Black Powder components
        self.bp_frame = ttk.Frame(frame)
        self.bp_frame.grid(row=2, column=0, columnspan=4, sticky='ew')
        
        ttk.Label(self.bp_frame, text="Potassium Nitrate:").grid(row=0, column=0, sticky='e')
        self.kno3_var = tk.DoubleVar(value=75.0)
        ttk.Entry(self.bp_frame, textvariable=self.kno3_var, width=10).grid(row=0, column=1, sticky='w')
        ttk.Label(self.bp_frame, text="%").grid(row=0, column=2, sticky='w')
        
        ttk.Label(self.bp_frame, text="Charcoal:").grid(row=1, column=0, sticky='e')
        self.charcoal_var = tk.DoubleVar(value=15.0)
        ttk.Entry(self.bp_frame, textvariable=self.charcoal_var, width=10).grid(row=1, column=1, sticky='w')
        ttk.Label(self.bp_frame, text="%").grid(row=1, column=2, sticky='w')
        
        ttk.Label(self.bp_frame, text="Sulfur:").grid(row=2, column=0, sticky='e')
        self.sulfur_var = tk.DoubleVar(value=10.0)
        ttk.Entry(self.bp_frame, textvariable=self.sulfur_var, width=10).grid(row=2, column=1, sticky='w')
        ttk.Label(self.bp_frame, text="%").grid(row=2, column=2, sticky='w')
        
        # Double Base components
        self.db_frame = ttk.Frame(frame)
        self.db_frame.grid(row=2, column=0, columnspan=4, sticky='ew')
        
        ttk.Label(self.db_frame, text="Nitrocellulose:").grid(row=0, column=0, sticky='e')
        self.nc_var = tk.DoubleVar(value=55.0)
        ttk.Entry(self.db_frame, textvariable=self.nc_var, width=10).grid(row=0, column=1, sticky='w')
        ttk.Label(self.db_frame, text="%").grid(row=0, column=2, sticky='w')
        
        ttk.Label(self.db_frame, text="Nitroglycerin:").grid(row=1, column=0, sticky='e')
        self.ng_var = tk.DoubleVar(value=45.0)
        ttk.Entry(self.db_frame, textvariable=self.ng_var, width=10).grid(row=1, column=1, sticky='w')
        ttk.Label(self.db_frame, text="%").grid(row=1, column=2, sticky='w')
        
        # Nitrocellulose components
        self.nc_frame = ttk.Frame(frame)
        self.nc_frame.grid(row=2, column=0, columnspan=4, sticky='ew')
        
        ttk.Label(self.nc_frame, text="Nitrogen Content:").grid(row=0, column=0, sticky='e')
        self.n_content_var = tk.DoubleVar(value=12.2)
        ttk.Entry(self.nc_frame, textvariable=self.n_content_var, width=10).grid(row=0, column=1, sticky='w')
        ttk.Label(self.nc_frame, text="%").grid(row=0, column=2, sticky='w')
        
        ttk.Label(self.nc_frame, text="Stabilizer:").grid(row=1, column=0, sticky='e')
        self.stab_var = tk.DoubleVar(value=1.0)
        ttk.Entry(self.nc_frame, textvariable=self.stab_var, width=10).grid(row=1, column=1, sticky='w')
        ttk.Label(self.nc_frame, text="%").grid(row=1, column=2, sticky='w')
        
        ttk.Label(self.nc_frame, text="Stabilizer Type:").grid(row=2, column=0, sticky='e')
        self.stab_type_var = tk.StringVar(value="Diphenylamine")
        stab_types = ["Diphenylamine", "Ethyl Centralite", "2-Nitrodiphenylamine"]
        ttk.Combobox(self.nc_frame, textvariable=self.stab_type_var, values=stab_types, width=20).grid(row=2, column=1, columnspan=2, sticky='w')
        
        # Hide all propellant frames initially
        self.hide_all_propellant_frames()
        self.show_propellant_frame(self.apcp_frame)
        
        # Bind propellant type change
        self.prop_type_var.trace_add('write', self.on_prop_type_change)
        
        # Burn rate parameters
        ttk.Label(frame, text="Burn Rate Coefficient (a):").grid(row=3, column=0, sticky='e')
        self.a_var = tk.DoubleVar(value=0.0002)
        ttk.Entry(frame, textvariable=self.a_var, width=10).grid(row=3, column=1, sticky='w')
        ttk.Label(frame, text="m/s/Pa^n").grid(row=3, column=2, sticky='w')
        
        ttk.Label(frame, text="Burn Rate Exponent (n):").grid(row=4, column=0, sticky='e')
        self.n_var = tk.DoubleVar(value=0.35)
        ttk.Entry(frame, textvariable=self.n_var, width=10).grid(row=4, column=1, sticky='w')
        
        # Button frame
        button_frame = ttk.Frame(frame)
        button_frame.grid(row=5, column=0, columnspan=4, pady=10)
        
        ttk.Button(button_frame, text="Calculate Propellant", command=self.calculate_propellant).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Export to TXT", command=self.export_propellant_to_txt).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Save Formulation", command=self.save_propellant_formulation).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Load Formulation", command=self.load_propellant_formulation).pack(side=tk.LEFT, padx=5)
        
        # Results notebook
        results_notebook = ttk.Notebook(frame)
        results_notebook.grid(row=6, column=0, columnspan=4, sticky='nsew', padx=5, pady=5)
        
        # Formulation tab
        form_frame = ttk.Frame(results_notebook)
        results_notebook.add(form_frame, text="Formulation")
        self.form_text = tk.Text(form_frame, height=15, width=90, wrap=tk.WORD, font=('Consolas', 10))
        scrollbar = ttk.Scrollbar(form_frame, orient="vertical", command=self.form_text.yview)
        scrollbar.pack(side="right", fill="y")
        self.form_text.configure(yscrollcommand=scrollbar.set)
        self.form_text.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Properties tab
        prop_frame = ttk.Frame(results_notebook)
        results_notebook.add(prop_frame, text="Properties")
        self.prop_text = tk.Text(prop_frame, height=15, width=90, wrap=tk.WORD, font=('Consolas', 10))
        scrollbar = ttk.Scrollbar(prop_frame, orient="vertical", command=self.prop_text.yview)
        scrollbar.pack(side="right", fill="y")
        self.prop_text.configure(yscrollcommand=scrollbar.set)
        self.prop_text.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Configure grid weights
        for i in range(7):
            frame.grid_rowconfigure(i, weight=1)
        for j in range(4):
            frame.grid_columnconfigure(j, weight=1)
    
    def hide_all_propellant_frames(self):
        self.apcp_frame.grid_remove()
        self.bp_frame.grid_remove()
        self.db_frame.grid_remove()
        self.nc_frame.grid_remove()
    
    def show_propellant_frame(self, frame):
        self.hide_all_propellant_frames()
        frame.grid()
    
    def on_prop_type_change(self, *args):
        prop_type = self.prop_type_var.get()
        if prop_type == "APCP":
            self.show_propellant_frame(self.apcp_frame)
        elif prop_type == "Black Powder":
            self.show_propellant_frame(self.bp_frame)
        elif prop_type == "Double Base":
            self.show_propellant_frame(self.db_frame)
        elif prop_type == "Nitrocellulose":
            self.show_propellant_frame(self.nc_frame)
    
    def save_propellant_formulation(self):
        prop_data = {
            'prop_type': self.prop_type_var.get(),
            'ap': self.ap_var.get(),
            'al': self.al_var.get(),
            'htpb': self.htpb_var.get(),
            'add': self.add_var.get(),
            'add_type': self.add_type_var.get(),
            'kno3': self.kno3_var.get(),
            'charcoal': self.charcoal_var.get(),
            'sulfur': self.sulfur_var.get(),
            'nc': self.nc_var.get(),
            'ng': self.ng_var.get(),
            'n_content': self.n_content_var.get(),
            'stab': self.stab_var.get(),
            'stab_type': self.stab_type_var.get(),
            'a': self.a_var.get(),
            'n': self.n_var.get(),
            'form_text': self.form_text.get("1.0", tk.END),
            'prop_text': self.prop_text.get("1.0", tk.END)
        }
        
        filepath = filedialog.asksaveasfilename(
            title="Save Propellant Formulation",
            defaultextension=".json",
            filetypes=(("JSON Files", "*.json"), ("All Files", "*.*")))
        
        if filepath:
            try:
                with open(filepath, 'w') as f:
                    json.dump(prop_data, f, indent=4)
                self.status_var.set(f"Propellant formulation saved to {os.path.basename(filepath)}")
            except Exception as e:
                messagebox.showerror("Save Error", f"Failed to save formulation: {str(e)}")

    def load_propellant_formulation(self):
        filepath = filedialog.askopenfilename(
            title="Load Propellant Formulation",
            filetypes=(("JSON Files", "*.json"), ("All Files", "*.*")))
        
        if filepath:
            try:
                with open(filepath, 'r') as f:
                    prop_data = json.load(f)
                
                self.prop_type_var.set(prop_data['prop_type'])
                self.ap_var.set(prop_data['ap'])
                self.al_var.set(prop_data['al'])
                self.htpb_var.set(prop_data['htpb'])
                self.add_var.set(prop_data['add'])
                self.add_type_var.set(prop_data['add_type'])
                self.kno3_var.set(prop_data['kno3'])
                self.charcoal_var.set(prop_data['charcoal'])
                self.sulfur_var.set(prop_data['sulfur'])
                self.nc_var.set(prop_data['nc'])
                self.ng_var.set(prop_data['ng'])
                self.n_content_var.set(prop_data['n_content'])
                self.stab_var.set(prop_data['stab'])
                self.stab_type_var.set(prop_data['stab_type'])
                self.a_var.set(prop_data['a'])
                self.n_var.set(prop_data['n'])
                
                self.form_text.config(state=tk.NORMAL)
                self.form_text.delete(1.0, tk.END)
                self.form_text.insert(tk.END, prop_data['form_text'])
                self.form_text.config(state=tk.DISABLED)
                
                self.prop_text.config(state=tk.NORMAL)
                self.prop_text.delete(1.0, tk.END)
                self.prop_text.insert(tk.END, prop_data['prop_text'])
                self.prop_text.config(state=tk.DISABLED)
                
                self.status_var.set(f"Propellant formulation loaded from {os.path.basename(filepath)}")
                self.on_prop_type_change()  # Update visible frame
            except Exception as e:
                messagebox.showerror("Load Error", f"Failed to load formulation: {str(e)}")

    def export_propellant_to_txt(self):
        try:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            form_text = self.form_text.get("1.0", tk.END)
            prop_text = self.prop_text.get("1.0", tk.END)
            
            filepath = filedialog.asksaveasfilename(
                title="Save Propellant Formulation Report",
                defaultextension=".txt",
                filetypes=(("Text Files", "*.txt"), ("All Files", "*.*")))
            
            if filepath:
                with open(filepath, 'w') as f:
                    f.write("PROPELLANT FORMULATION REPORT\n")
                    f.write(f"Generated: {timestamp}\n")
                    f.write(f"Software: GRIMSTRE DIGITAL TOOLS v2.1\n\n")
                    f.write("FORMULATION\n")
                    f.write("===========\n")
                    f.write(form_text)
                    f.write("\nPROPERTIES\n")
                    f.write("==========\n")
                    f.write(prop_text)
                
                self.status_var.set(f"Propellant formulation exported to TXT: {os.path.basename(filepath)}")
                messagebox.showinfo("Export Complete", "Propellant formulation exported successfully")
            
        except Exception as e:
            messagebox.showerror("Export Error", f"Failed to export: {str(e)}")
            self.status_var.set("Error exporting propellant formulation")

    def calculate_propellant(self):
        try:
            prop_type = self.prop_type_var.get()
            
            if prop_type == "APCP":
                ap = self.ap_var.get()
                al = self.al_var.get()
                htpb = self.htpb_var.get()
                add = self.add_var.get()
                total = ap + al + htpb + add
                
                if not math.isclose(total, 100.0, abs_tol=0.1):
                    messagebox.showwarning("Composition Warning", 
                        f"APCP composition sums to {total:.1f}% (should be 100%). Adjusting values.")
                    
                    # Normalize to 100%
                    ap = ap * 100 / total
                    al = al * 100 / total
                    htpb = htpb * 100 / total
                    add = add * 100 / total
                    
                    self.ap_var.set(ap)
                    self.al_var.set(al)
                    self.htpb_var.set(htpb)
                    self.add_var.set(add)
                
                # Calculate properties
                density = 1800 * (ap/100) + 2700 * (al/100) + 920 * (htpb/100) + 1500 * (add/100)
                isp_vac = 280 * (ap/100) + 300 * (al/100) + 240 * (htpb/100) + 250 * (add/100)
                flame_temp = 3400 * (ap/100) + 3500 * (al/100) + 2900 * (htpb/100) + 3200 * (add/100)
                
                formulation = f"""APCP FORMULATION
                
Composition:
- Ammonium Perchlorate (AP): {ap:.1f}%
- Aluminum Powder: {al:.1f}%
- HTPB Binder: {htpb:.1f}%
- Additives ({self.add_type_var.get()}): {add:.1f}%
"""
                
                properties = f"""PHYSICAL PROPERTIES
                
- Theoretical Density: {density:.0f} kg/m³
- Estimated Isp (vac): {isp_vac:.0f} s
- Flame Temperature: {flame_temp:.0f} K
- Burn Rate: r = {self.a_var.get():.5f} * P^{self.n_var.get():.3f} m/s
"""
                
            elif prop_type == "Black Powder":
                kno3 = self.kno3_var.get()
                charcoal = self.charcoal_var.get()
                sulfur = self.sulfur_var.get()
                total = kno3 + charcoal + sulfur
                
                if not math.isclose(total, 100.0, abs_tol=0.1):
                    messagebox.showwarning("Composition Warning", 
                        f"Black powder composition sums to {total:.1f}% (should be 100%). Adjusting values.")
                    
                    # Normalize to 100%
                    kno3 = kno3 * 100 / total
                    charcoal = charcoal * 100 / total
                    sulfur = sulfur * 100 / total
                    
                    self.kno3_var.set(kno3)
                    self.charcoal_var.set(charcoal)
                    self.sulfur_var.set(sulfur)
                
                # Calculate properties
                density = 1900 * (kno3/100) + 500 * (charcoal/100) + 2000 * (sulfur/100)
                isp_vac = 80 * (kno3/100) + 60 * (charcoal/100) + 70 * (sulfur/100)
                flame_temp = 2300 * (kno3/100) + 1800 * (charcoal/100) + 2000 * (sulfur/100)
                
                formulation = f"""BLACK POWDER FORMULATION
                
Composition:
- Potassium Nitrate (KNO3): {kno3:.1f}%
- Charcoal: {charcoal:.1f}%
- Sulfur: {sulfur:.1f}%
"""
                
                properties = f"""PHYSICAL PROPERTIES
                
- Theoretical Density: {density:.0f} kg/m³
- Estimated Isp (vac): {isp_vac:.0f} s
- Flame Temperature: {flame_temp:.0f} K
- Burn Rate: r = {self.a_var.get():.5f} * P^{self.n_var.get():.3f} m/s
"""
            
            elif prop_type == "Double Base":
                nc = self.nc_var.get()
                ng = self.ng_var.get()
                total = nc + ng
                
                if not math.isclose(total, 100.0, abs_tol=0.1):
                    messagebox.showwarning("Composition Warning", 
                        f"Double base composition sums to {total:.1f}% (should be 100%). Adjusting values.")
                    
                    # Normalize to 100%
                    nc = nc * 100 / total
                    ng = ng * 100 / total
                    
                    self.nc_var.set(nc)
                    self.ng_var.set(ng)
                
                # Calculate properties
                density = 1600 * (nc/100) + 1500 * (ng/100)
                isp_vac = 220 * (nc/100) + 240 * (ng/100)
                flame_temp = 2800 * (nc/100) + 3000 * (ng/100)
                
                formulation = f"""DOUBLE BASE FORMULATION
                
Composition:
- Nitrocellulose: {nc:.1f}%
- Nitroglycerin: {ng:.1f}%
"""
                
                properties = f"""PHYSICAL PROPERTIES
                
- Theoretical Density: {density:.0f} kg/m³
- Estimated Isp (vac): {isp_vac:.0f} s
- Flame Temperature: {flame_temp:.0f} K
- Burn Rate: r = {self.a_var.get():.5f} * P^{self.n_var.get():.3f} m/s
"""
            
            elif prop_type == "Nitrocellulose":
                n_content = self.n_content_var.get()
                stab = self.stab_var.get()
                
                if n_content < 12.0 or n_content > 13.5:
                    messagebox.showwarning("Nitrogen Warning",
                        f"Nitrocellulose with {n_content:.1f}% N may be unstable or impractical")
                
                # Calculate properties
                density = 1500 + (n_content - 12.0) * 50
                isp_vac = 200 + (n_content - 12.0) * 10
                flame_temp = 2500 + (n_content - 12.0) * 100
                
                formulation = f"""NITROCELLULOSE FORMULATION
                
Composition:
- Nitrogen Content: {n_content:.1f}%
- {self.stab_type_var.get()} Stabilizer: {stab:.1f}%
"""
                
                properties = f"""PHYSICAL PROPERTIES
                
- Theoretical Density: {density:.0f} kg/m³
- Estimated Isp (vac): {isp_vac:.0f} s
- Flame Temperature: {flame_temp:.0f} K
- Burn Rate: r = {self.a_var.get():.5f} * P^{self.n_var.get():.3f} m/s
"""
            
            self.form_text.config(state=tk.NORMAL)
            self.form_text.delete(1.0, tk.END)
            self.form_text.insert(tk.END, formulation)
            self.form_text.config(state=tk.DISABLED)
            
            self.prop_text.config(state=tk.NORMAL)
            self.prop_text.delete(1.0, tk.END)
            self.prop_text.insert(tk.END, properties)
            self.prop_text.config(state=tk.DISABLED)
            
            self.status_var.set(f"{prop_type} propellant calculated successfully")
            
        except Exception as e:
            self.status_var.set(f"Error in propellant calculations: {str(e)}")
            messagebox.showerror("Calculation Error", f"An error occurred: {str(e)}")

    def create_flight_sim_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Flight Sim")
        
        # Header
        ttk.Label(frame, text="Rocket Flight Simulation", style='Header.TLabel').grid(row=0, column=0, columnspan=4, pady=10)
        
        # Rocket parameters
        ttk.Label(frame, text="Rocket Mass (dry):").grid(row=1, column=0, sticky='e')
        self.rocket_mass_var = tk.DoubleVar(value=10.0)  # kg
        ttk.Entry(frame, textvariable=self.rocket_mass_var, width=10).grid(row=1, column=1, sticky='w')
        ttk.Label(frame, text="kg").grid(row=1, column=2, sticky='w')
        
        ttk.Label(frame, text="Propellant Mass:").grid(row=2, column=0, sticky='e')
        self.prop_mass_var = tk.DoubleVar(value=5.0)  # kg
        ttk.Entry(frame, textvariable=self.prop_mass_var, width=10).grid(row=2, column=1, sticky='w')
        ttk.Label(frame, text="kg").grid(row=2, column=2, sticky='w')
        
        ttk.Label(frame, text="Average Thrust:").grid(row=3, column=0, sticky='e')
        self.thrust_var = tk.DoubleVar(value=1000.0)  # N
        ttk.Entry(frame, textvariable=self.thrust_var, width=10).grid(row=3, column=1, sticky='w')
        ttk.Label(frame, text="N").grid(row=3, column=2, sticky='w')
        
        ttk.Label(frame, text="Burn Time:").grid(row=4, column=0, sticky='e')
        self.burn_time_var = tk.DoubleVar(value=5.0)  # s
        ttk.Entry(frame, textvariable=self.burn_time_var, width=10).grid(row=4, column=1, sticky='w')
        ttk.Label(frame, text="s").grid(row=4, column=2, sticky='w')
        
        ttk.Label(frame, text="Drag Coefficient:").grid(row=5, column=0, sticky='e')
        self.cd_var = tk.DoubleVar(value=0.5)
        ttk.Entry(frame, textvariable=self.cd_var, width=10).grid(row=5, column=1, sticky='w')
        
        ttk.Label(frame, text="Rocket Diameter:").grid(row=6, column=0, sticky='e')
        self.rocket_diam_var = tk.DoubleVar(value=0.15)  # m
        ttk.Entry(frame, textvariable=self.rocket_diam_var, width=10).grid(row=6, column=1, sticky='w')
        ttk.Label(frame, text="m").grid(row=6, column=2, sticky='w')
        
        # Button frame
        button_frame = ttk.Frame(frame)
        button_frame.grid(row=7, column=0, columnspan=4, pady=10)
        
        ttk.Button(button_frame, text="Run Simulation", command=self.run_flight_simulation).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Export Data", command=self.export_flight_data).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Save Parameters", command=self.save_flight_params).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Load Parameters", command=self.load_flight_params).pack(side=tk.LEFT, padx=5)
        
        # Results notebook
        results_notebook = ttk.Notebook(frame)
        results_notebook.grid(row=8, column=0, columnspan=4, sticky='nsew', padx=5, pady=5)
        
        # Data tab
        data_frame = ttk.Frame(results_notebook)
        results_notebook.add(data_frame, text="Flight Data")
        
        # Create treeview for data display
        columns = ("time", "altitude", "velocity", "acceleration", "mass")
        self.flight_tree = ttk.Treeview(data_frame, columns=columns, show="headings", height=15)
        
        # Configure columns
        self.flight_tree.heading("time", text="Time (s)")
        self.flight_tree.heading("altitude", text="Altitude (m)")
        self.flight_tree.heading("velocity", text="Velocity (m/s)")
        self.flight_tree.heading("acceleration", text="Acceleration (m/s²)")
        self.flight_tree.heading("mass", text="Mass (kg)")
        
        # Set column widths
        self.flight_tree.column("time", width=100, anchor='e')
        self.flight_tree.column("altitude", width=100, anchor='e')
        self.flight_tree.column("velocity", width=100, anchor='e')
        self.flight_tree.column("acceleration", width=100, anchor='e')
        self.flight_tree.column("mass", width=100, anchor='e')
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(data_frame, orient="vertical", command=self.flight_tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.flight_tree.configure(yscrollcommand=scrollbar.set)
        self.flight_tree.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Analysis tab
        analysis_frame = ttk.Frame(results_notebook)
        results_notebook.add(analysis_frame, text="Flight Analysis")
        self.analysis_text = tk.Text(analysis_frame, height=15, width=90, wrap=tk.WORD, font=('Consolas', 10))
        scrollbar = ttk.Scrollbar(analysis_frame, orient="vertical", command=self.analysis_text.yview)
        scrollbar.pack(side="right", fill="y")
        self.analysis_text.configure(yscrollcommand=scrollbar.set)
        self.analysis_text.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Configure grid weights
        for i in range(9):
            frame.grid_rowconfigure(i, weight=1)
        for j in range(4):
            frame.grid_columnconfigure(j, weight=1)

    def save_flight_params(self):
        flight_data = {
            'rocket_mass': self.rocket_mass_var.get(),
            'prop_mass': self.prop_mass_var.get(),
            'thrust': self.thrust_var.get(),
            'burn_time': self.burn_time_var.get(),
            'cd': self.cd_var.get(),
            'rocket_diam': self.rocket_diam_var.get(),
            'analysis_text': self.analysis_text.get("1.0", tk.END)
        }
        
        filepath = filedialog.asksaveasfilename(
            title="Save Flight Parameters",
            defaultextension=".json",
            filetypes=(("JSON Files", "*.json"), ("All Files", "*.*")))
        
        if filepath:
            try:
                with open(filepath, 'w') as f:
                    json.dump(flight_data, f, indent=4)
                self.status_var.set(f"Flight parameters saved to {os.path.basename(filepath)}")
            except Exception as e:
                messagebox.showerror("Save Error", f"Failed to save parameters: {str(e)}")

    def load_flight_params(self):
        filepath = filedialog.askopenfilename(
            title="Load Flight Parameters",
            filetypes=(("JSON Files", "*.json"), ("All Files", "*.*")))
        
        if filepath:
            try:
                with open(filepath, 'r') as f:
                    flight_data = json.load(f)
                
                self.rocket_mass_var.set(flight_data['rocket_mass'])
                self.prop_mass_var.set(flight_data['prop_mass'])
                self.thrust_var.set(flight_data['thrust'])
                self.burn_time_var.set(flight_data['burn_time'])
                self.cd_var.set(flight_data['cd'])
                self.rocket_diam_var.set(flight_data['rocket_diam'])
                
                self.analysis_text.config(state=tk.NORMAL)
                self.analysis_text.delete(1.0, tk.END)
                self.analysis_text.insert(tk.END, flight_data['analysis_text'])
                self.analysis_text.config(state=tk.DISABLED)
                
                self.status_var.set(f"Flight parameters loaded from {os.path.basename(filepath)}")
            except Exception as e:
                messagebox.showerror("Load Error", f"Failed to load parameters: {str(e)}")

    def export_flight_data(self):
        try:
            if not self.flight_data:
                messagebox.showwarning("No Data", "No flight data to export. Run simulation first.")
                return
            
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            filepath = filedialog.asksaveasfilename(
                title="Export Flight Data",
                defaultextension=".json",
                filetypes=(("JSON Files", "*.json"), ("Text Files", "*.txt"), ("All Files", "*.*")))
            
            if filepath:
                if filepath.endswith('.txt'):
                    with open(filepath, 'w') as f:
                        f.write("FLIGHT DATA REPORT\n")
                        f.write(f"Generated: {timestamp}\n")
                        f.write(f"Software: GRIMSTRE DIGITAL TOOLS v2.1\n\n")
                        f.write("Time(s)\tAltitude(m)\tVelocity(m/s)\tAccel(m/s²)\tMass(kg)\n")
                        for point in self.flight_data:
                            f.write(f"{point['time']:.2f}\t{point['altitude']:.2f}\t{point['velocity']:.2f}\t{point['accel']:.2f}\t{point['mass']:.2f}\n")
                else:
                    with open(filepath, 'w') as f:
                        json.dump(self.flight_data, f, indent=4)
                
                self.status_var.set(f"Flight data exported to {os.path.basename(filepath)}")
                messagebox.showinfo("Export Complete", "Flight data exported successfully")
            
        except Exception as e:
            messagebox.showerror("Export Error", f"Failed to export: {str(e)}")
            self.status_var.set("Error exporting flight data")

    def run_flight_simulation(self):
        try:
            # Get input parameters
            dry_mass = self.rocket_mass_var.get()  # kg
            prop_mass = self.prop_mass_var.get()  # kg
            thrust = self.thrust_var.get()  # N
            burn_time = self.burn_time_var.get()  # s
            cd = self.cd_var.get()
            diameter = self.rocket_diam_var.get()  # m
            
            if dry_mass <= 0 or prop_mass <= 0 or thrust <= 0 or burn_time <= 0 or diameter <= 0:
                messagebox.showerror("Input Error", "All values must be positive numbers")
                return
            
            # Constants
            g = 9.80665  # m/s²
            rho = 1.225  # kg/m³ (air density at sea level)
            dt = 0.1  # s (time step)
            
            # Initial conditions
            time = 0.0
            altitude = 0.0
            velocity = 0.0
            mass = dry_mass + prop_mass 
            area = math.pi * (diameter/2)**2  # m²
            
            # Clear previous data
            self.flight_data = []
            for item in self.flight_tree.get_children():
                self.flight_tree.delete(item)
            
            # Simulation loop
            max_altitude = 0.0
            max_velocity = 0.0
            max_accel = 0.0
            burnout_time = 0.0
            apogee_time = 0.0
            
            while altitude >= 0:
                # Calculate forces
                if time <= burn_time:
                    # Thrust phase
                    thrust_force = thrust
                    mass_flow = prop_mass / burn_time
                    mass = dry_mass + prop_mass - mass_flow * time
                else:
                    # Coast phase
                    thrust_force = 0.0
                    mass = dry_mass
                
                # Record burnout time
                if time >= burn_time and burnout_time == 0:
                    burnout_time = time
                
                # Calculate drag (simplified model)
                drag = 0.5 * rho * velocity**2 * cd * area
                if velocity < 0:
                    drag = -drag  # Drag always opposes motion
                
                # Calculate acceleration
                weight = mass * g
                net_force = thrust_force - weight - drag
                acceleration = net_force / mass
                
                # Update max values
                if altitude > max_altitude:
                    max_altitude = altitude
                    apogee_time = time
                if abs(velocity) > max_velocity:
                    max_velocity = abs(velocity)
                if abs(acceleration) > max_accel:
                    max_accel = abs(acceleration)
                
                # Store data point
                point = {
                    'time': time,
                    'altitude': altitude,
                    'velocity': velocity,
                    'accel': acceleration,
                    'mass': mass
                }
                self.flight_data.append(point)
                
                # Update display every 10 points
                if len(self.flight_data) % 10 == 0:
                    self.flight_tree.insert("", "end", values=(
                        f"{time:.2f}",
                        f"{altitude:.2f}",
                        f"{velocity:.2f}",
                        f"{acceleration:.2f}",
                        f"{mass:.2f}"
                    ))
                
                # Update state (Euler integration)
                velocity += acceleration * dt
                altitude += velocity * dt
                time += dt
                
                # Stop if we've been falling for a while
                if time > burn_time + 30 and velocity < -100:
                    break
            
            # Add final data points
            for point in self.flight_data[-10:]:
                self.flight_tree.insert("", "end", values=(
                    f"{point['time']:.2f}",
                    f"{point['altitude']:.2f}",
                    f"{point['velocity']:.2f}",
                    f"{point['accel']:.2f}",
                    f"{point['mass']:.2f}"
                ))
            
            # Generate analysis report
            analysis = f"""FLIGHT ANALYSIS REPORT
            
Launch Parameters:
- Rocket Mass (dry): {dry_mass:.2f} kg
- Propellant Mass: {prop_mass:.2f} kg
- Average Thrust: {thrust:.1f} N
- Burn Time: {burn_time:.2f} s
- Drag Coefficient: {cd:.2f}
- Rocket Diameter: {diameter:.3f} m

Flight Performance:
- Maximum Altitude: {max_altitude:.0f} m
- Apogee Time: {apogee_time:.2f} s
- Maximum Velocity: {max_velocity:.1f} m/s
- Maximum Acceleration: {max_accel:.1f} m/s² ({max_accel/g:.1f} g)
- Burnout Time: {burnout_time:.2f} s
- Burnout Altitude: {next(p['altitude'] for p in self.flight_data if p['time'] >= burnout_time):.0f} m
- Burnout Velocity: {next(p['velocity'] for p in self.flight_data if p['time'] >= burnout_time):.1f} m/s
- Total Flight Time: {time:.2f} s
"""
            
            self.analysis_text.config(state=tk.NORMAL)
            self.analysis_text.delete(1.0, tk.END)
            self.analysis_text.insert(tk.END, analysis)
            self.analysis_text.config(state=tk.DISABLED)
            
            self.status_var.set(f"Flight simulation completed. Apogee: {max_altitude:.0f} m")
            
        except Exception as e:
            self.status_var.set(f"Error in flight simulation: {str(e)}")
            messagebox.showerror("Simulation Error", f"An error occurred: {str(e)}")

    def create_telemetry_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Telemetry")
        
        # Header
        ttk.Label(frame, text="Flight Telemetry Analysis", style='Header.TLabel').grid(row=0, column=0, columnspan=4, pady=10)
        
        # Button frame
        button_frame = ttk.Frame(frame)
        button_frame.grid(row=1, column=0, columnspan=4, pady=10)
        
        ttk.Button(button_frame, text="Load Telemetry Data", command=self.load_telemetry_data).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Analyze Flight", command=self.analyze_telemetry_data).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Export Data", command=self.export_telemetry_data).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Generate Report", command=self.generate_telemetry_report).pack(side=tk.LEFT, padx=5)
        
        # Data display
        columns = ("time", "altitude", "velocity", "acceleration")
        self.telemetry_tree = ttk.Treeview(frame, columns=columns, show="headings", height=15)
        
        # Configure columns
        self.telemetry_tree.heading("time", text="Time (s)")
        self.telemetry_tree.heading("altitude", text="Altitude (m)")
        self.telemetry_tree.heading("velocity", text="Velocity (m/s)")
        self.telemetry_tree.heading("acceleration", text="Acceleration (m/s²)")
        
        # Set column widths
        self.telemetry_tree.column("time", width=100, anchor='e')
        self.telemetry_tree.column("altitude", width=100, anchor='e')
        self.telemetry_tree.column("velocity", width=100, anchor='e')
        self.telemetry_tree.column("acceleration", width=100, anchor='e')
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=self.telemetry_tree.yview)
        scrollbar.grid(row=2, column=4, sticky='ns')
        self.telemetry_tree.configure(yscrollcommand=scrollbar.set)
        self.telemetry_tree.grid(row=2, column=0, columnspan=4, sticky='nsew', padx=5, pady=5)
        
        # Analysis frame
        self.telemetry_analysis = tk.Text(frame, height=15, width=90, wrap=tk.WORD, font=('Consolas', 10))
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=self.telemetry_analysis.yview)
        scrollbar.grid(row=3, column=4, sticky='ns')
        self.telemetry_analysis.configure(yscrollcommand=scrollbar.set)
        self.telemetry_analysis.grid(row=3, column=0, columnspan=4, sticky='nsew', padx=5, pady=5)
        
        # Configure grid weights
        frame.grid_rowconfigure(2, weight=1)
        frame.grid_rowconfigure(3, weight=1)
        frame.grid_columnconfigure(0, weight=1)

    def load_telemetry_data(self):
        filepath = filedialog.askopenfilename(
            title="Load Telemetry Data",
            filetypes=(("JSON Files", "*.json"), ("Text Files", "*.txt"), ("All Files", "*.*")))
        
        if filepath:
            try:
                with open(filepath, 'r') as f:
                    if filepath.endswith('.json'):
                        self.telemetry_data = json.load(f)
                    else:
                        # Try to parse as text file
                        self.telemetry_data = []
                        for line in f.readlines()[1:]:  # Skip header
                            parts = line.strip().split()
                            if len(parts) >= 4:
                                self.telemetry_data.append({
                                    'time': float(parts[0]),
                                    'altitude': float(parts[1]),
                                    'velocity': float(parts[2]),
                                    'accel': float(parts[3])
                                })
                
                # Clear previous data
                for item in self.telemetry_tree.get_children():
                    self.telemetry_tree.delete(item)
                
                # Load first 100 points
                for point in self.telemetry_data[:100]:
                    self.telemetry_tree.insert("", "end", values=(
                        f"{point.get('time', 0):.2f}",
                        f"{point.get('altitude', 0):.2f}",
                        f"{point.get('velocity', 0):.2f}",
                        f"{point.get('accel', 0):.2f}"
                    ))
                
                self.status_var.set(f"Loaded {len(self.telemetry_data)} telemetry points from {os.path.basename(filepath)}")
            
            except Exception as e:
                messagebox.showerror("Load Error", f"Failed to load telemetry data: {str(e)}")
                self.status_var.set("Error loading telemetry data")

    def analyze_telemetry_data(self):
        if not hasattr(self, 'telemetry_data') or not self.telemetry_data:
            messagebox.showwarning("No Data", "No telemetry data to analyze. Load data first.")
            return
        
        try:
            # Find key flight parameters
            max_alt = max(p['altitude'] for p in self.telemetry_data)
            max_vel = max(abs(p['velocity']) for p in self.telemetry_data)
            max_accel = max(abs(p['accel']) for p in self.telemetry_data)
            
            # Find burnout time (when acceleration drops near 1g)
            burnout_time = next((p['time'] for p in self.telemetry_data 
                              if p['time'] > 0.5 and abs(p['accel']) < 10.5), 0)
            
            # Find apogee time
            apogee_time = next(p['time'] for p in self.telemetry_data 
                             if p['altitude'] == max_alt)
            
            # Generate analysis
            analysis = f"""TELEMETRY ANALYSIS
            
Flight Summary:
- Maximum Altitude: {max_alt:.0f} m
- Maximum Velocity: {max_vel:.1f} m/s
- Maximum Acceleration: {max_accel:.1f} m/s² ({max_accel/9.8:.1f} g)
- Burnout Time: {burnout_time:.2f} s
- Apogee Time: {apogee_time:.2f} s
- Total Flight Time: {self.telemetry_data[-1]['time']:.2f} s

Data Statistics:
- Data Points: {len(self.telemetry_data)}
- Time Interval: {self.telemetry_data[1]['time'] - self.telemetry_data[0]['time']:.3f} s
- First Data Point: t={self.telemetry_data[0]['time']:.2f}s, h={self.telemetry_data[0]['altitude']:.1f}m
- Last Data Point: t={self.telemetry_data[-1]['time']:.2f}s, h={self.telemetry_data[-1]['altitude']:.1f}m
"""
            
            self.telemetry_analysis.config(state=tk.NORMAL)
            self.telemetry_analysis.delete(1.0, tk.END)
            self.telemetry_analysis.insert(tk.END, analysis)
            self.telemetry_analysis.config(state=tk.DISABLED)
            
            self.status_var.set(f"Telemetry analysis complete. Max altitude: {max_alt:.0f} m")
        
        except Exception as e:
            messagebox.showerror("Analysis Error", f"Failed to analyze telemetry data: {str(e)}")
            self.status_var.set("Error analyzing telemetry data")

    def export_telemetry_data(self):
        if not hasattr(self, 'telemetry_data') or not self.telemetry_data:
            messagebox.showwarning("No Data", "No telemetry data to export. Load data first.")
            return
        
        try:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            filepath = filedialog.asksaveasfilename(
                title="Export Telemetry Data",
                defaultextension=".json",
                filetypes=(("JSON Files", "*.json"), ("Text Files", "*.txt"), ("All Files", "*.*")))
            
            if filepath:
                if filepath.endswith('.txt'):
                    with open(filepath, 'w') as f:
                        f.write("TELEMETRY DATA REPORT\n")
                        f.write(f"Generated: {timestamp}\n")
                        f.write(f"Software: GRIMSTRE DIGITAL TOOLS v2.1\n\n")
                        f.write("TIME(s)\tALTITUDE(m)\tVELOCITY(m/s)\tACCELERATION(m/s²)\n")
                        for point in self.telemetry_data:
                            f.write(f"{point['time']:.3f}\t{point['altitude']:.2f}\t{point['velocity']:.2f}\t{point['accel']:.2f}\n")
                else:
                    with open(filepath, 'w') as f:
                        json.dump(self.telemetry_data, f, indent=4)
                
                self.status_var.set(f"Telemetry data exported to {os.path.basename(filepath)}")
                messagebox.showinfo("Export Complete", "Telemetry data exported successfully")
            
        except Exception as e:
            messagebox.showerror("Export Error", f"Failed to export: {str(e)}")
            self.status_var.set("Error exporting telemetry data")

    def generate_telemetry_report(self):
        if not hasattr(self, 'telemetry_data') or not self.telemetry_data:
            messagebox.showwarning("No Data", "No telemetry data to report. Load data first.")
            return
        
        try:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            filepath = filedialog.asksaveasfilename(
                title="Save Telemetry Report",
                defaultextension=".txt",
                filetypes=(("Text Files", "*.txt"), ("All Files", "*.*")))
            
            if filepath:
                with open(filepath, 'w') as f:
                    f.write("FLIGHT TELEMETRY REPORT\n")
                    f.write(f"Generated: {timestamp}\n")
                    f.write(f"Software: GRIMSTRE DIGITAL TOOLS v2.1\n\n")
                    
                    # Write analysis
                    f.write(self.telemetry_analysis.get("1.0", tk.END))
                    f.write("\n\n")
                    
                    # Write data header
                    f.write("TIME(s)\tALTITUDE(m)\tVELOCITY(m/s)\tACCELERATION(m/s²)\n")
                    
                    # Write data points (limited to 1000 to prevent huge files)
                    for point in self.telemetry_data[:1000]:
                        f.write(f"{point['time']:.3f}\t{point['altitude']:.2f}\t{point['velocity']:.2f}\t{point['accel']:.2f}\n")
                
                self.status_var.set(f"Telemetry report saved to {os.path.basename(filepath)}")
                messagebox.showinfo("Report Complete", "Telemetry report generated successfully")
            
        except Exception as e:
            messagebox.showerror("Report Error", f"Failed to generate report: {str(e)}")
            self.status_var.set("Error generating telemetry report")

    def create_orbital_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Orbital Mechanics")
        
        # Header
        ttk.Label(frame, text="Orbital Mechanics Calculator", style='Header.TLabel').grid(row=0, column=0, columnspan=4, pady=10)
        
        # Input parameters
        ttk.Label(frame, text="Initial Altitude:").grid(row=1, column=0, sticky='e')
        self.altitude_var = tk.DoubleVar(value=200)  # km
        ttk.Entry(frame, textvariable=self.altitude_var, width=10).grid(row=1, column=1, sticky='w')
        ttk.Label(frame, text="km").grid(row=1, column=2, sticky='w')
        
        ttk.Label(frame, text="Required ΔV:").grid(row=2, column=0, sticky='e')
        self.dv_var = tk.DoubleVar(value=0.0)
        ttk.Entry(frame, textvariable=self.dv_var, width=10, state='readonly').grid(row=2, column=1, sticky='w')
        ttk.Label(frame, text="m/s").grid(row=2, column=2, sticky='w')
        
        ttk.Label(frame, text="Target Altitude:").grid(row=3, column=0, sticky='e')
        self.target_alt_var = tk.DoubleVar(value=500)  # km
        ttk.Entry(frame, textvariable=self.target_alt_var, width=10).grid(row=3, column=1, sticky='w')
        ttk.Label(frame, text="km").grid(row=3, column=2, sticky='w')
        
        ttk.Label(frame, text="Orbital Period:").grid(row=4, column=0, sticky='e')
        self.period_var = tk.StringVar(value="N/A")
        ttk.Entry(frame, textvariable=self.period_var, width=10, state='readonly').grid(row=4, column=1, sticky='w')
        ttk.Label(frame, text="minutes").grid(row=4, column=2, sticky='w')
        
        ttk.Label(frame, text="Escape Velocity:").grid(row=5, column=0, sticky='e')
        self.escape_var = tk.StringVar(value="N/A")
        ttk.Entry(frame, textvariable=self.escape_var, width=10, state='readonly').grid(row=5, column=1, sticky='w')
        ttk.Label(frame, text="km/s").grid(row=5, column=2, sticky='w')
        
        # Button frame
        button_frame = ttk.Frame(frame)
        button_frame.grid(row=6, column=0, columnspan=4, pady=10)
        
        ttk.Button(button_frame, text="Calculate Orbit", command=self.calculate_orbit).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Calculate Transfer", command=self.calculate_transfer).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Calculate Escape", command=self.calculate_escape).pack(side=tk.LEFT, padx=5)
        
        # Results text
        self.orbit_text = tk.Text(frame, height=15, width=90, wrap=tk.WORD, font=('Consolas', 10))
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=self.orbit_text.yview)
        scrollbar.grid(row=7, column=4, sticky='ns')
        self.orbit_text.configure(yscrollcommand=scrollbar.set)
        self.orbit_text.grid(row=7, column=0, columnspan=4, sticky='nsew', padx=5, pady=5)
        
        # Configure grid weights
        frame.grid_rowconfigure(7, weight=1)
        frame.grid_columnconfigure(0, weight=1)

    def calculate_orbit(self):
        try:
            altitude = self.altitude_var.get()  # km
            if altitude <= 0:
                messagebox.showerror("Input Error", "Altitude must be positive")
                return
            
            # Constants
            R_earth = 6371  # km (Earth radius)
            mu = 3.986e5  # km³/s² (standard gravitational parameter)
            
            # Calculate orbital parameters
            r = R_earth + altitude
            v = math.sqrt(mu / r)  # km/s (circular orbit velocity)
            period = 2 * math.pi * math.sqrt(r**3 / mu)  # seconds
            escape_v = math.sqrt(2 * mu / r)  # km/s (escape velocity)
            
            # Update display
            self.period_var.set(f"{period/60:.1f}")
            self.escape_var.set(f"{escape_v:.2f}")
            
            result = f"""ORBITAL PARAMETERS AT {altitude:.0f} KM
            
Circular Orbit:
- Orbital Velocity: {v:.3f} km/s
- Orbital Period: {period/60:.1f} minutes
- Escape Velocity: {escape_v:.3f} km/s

Notes:
- Assumes circular orbit
- Earth radius: 6,371 km
- Standard gravitational parameter (μ): 3.986 × 10⁵ km³/s²
"""
            
            self.orbit_text.config(state=tk.NORMAL)
            self.orbit_text.delete(1.0, tk.END)
            self.orbit_text.insert(tk.END, result)
            self.orbit_text.config(state=tk.DISABLED)
            
            self.status_var.set(f"Calculated orbital parameters at {altitude:.0f} km altitude")
        
        except Exception as e:
            messagebox.showerror("Calculation Error", f"Failed to calculate orbit: {str(e)}")
            self.status_var.set("Error calculating orbital parameters")

    def calculate_transfer(self):
        try:
            alt1 = self.altitude_var.get()  # km
            alt2 = self.target_alt_var.get()  # km
            
            if alt1 <= 0 or alt2 <= 0:
                messagebox.showerror("Input Error", "Altitudes must be positive")
                return
            if alt1 >= alt2:
                messagebox.showerror("Input Error", "Target altitude must be higher than initial altitude")
                return
            
            # Constants
            R_earth = 6371  # km
            mu = 3.986e5  # km³/s²
            
            # Calculate Hohmann transfer
            r1 = R_earth + alt1
            r2 = R_earth + alt2
            
            # Transfer orbit velocities
            v1 = math.sqrt(mu / r1)
            v2 = math.sqrt(mu / r2)
            
            # Delta-V calculations
            dv1 = math.sqrt(mu / r1) * (math.sqrt(2 * r2 / (r1 + r2)) - 1)
            dv2 = math.sqrt(mu / r2) * (1 - math.sqrt(2 * r1 / (r1 + r2)))
            total_dv = dv1 + dv2
            
            # Transfer time
            transfer_time = math.pi * math.sqrt((r1 + r2)**3 / (8 * mu))
            
            # Update display
            self.dv_var.set(f"{total_dv*1000:.1f}")
            
            result = f"""HOHMANN TRANSFER FROM {alt1:.0f} KM TO {alt2:.0f} KM
            
Transfer Parameters:
- Initial circular orbit velocity: {v1:.3f} km/s
- Final circular orbit velocity: {v2:.3f} km/s
- First burn ΔV: {dv1*1000:.1f} m/s
- Second burn ΔV: {dv2*1000:.1f} m/s
- Total ΔV required: {total_dv*1000:.1f} m/s
- Transfer time: {transfer_time/60:.1f} minutes

Notes:
- Assumes coplanar circular orbits
- Earth radius: 6,371 km
- Standard gravitational parameter (μ): 3.986 × 10⁵ km³/s²
"""
            
            self.orbit_text.config(state=tk.NORMAL)
            self.orbit_text.delete(1.0, tk.END)
            self.orbit_text.insert(tk.END, result)
            self.orbit_text.config(state=tk.DISABLED)
            
            self.status_var.set(f"Calculated Hohmann transfer from {alt1:.0f} km to {alt2:.0f} km")
        
        except Exception as e:
            messagebox.showerror("Calculation Error", f"Failed to calculate transfer: {str(e)}")
            self.status_var.set("Error calculating orbital transfer")

    def calculate_escape(self):
        try:
            altitude = self.altitude_var.get()  # km
            if altitude <= 0:
                messagebox.showerror("Input Error", "Altitude must be positive")
                return
            
            # Constants
            R_earth = 6371  # km
            mu = 3.986e5  # km³/s²
            
            # Calculate escape velocity
            r = R_earth + altitude
            v_circ = math.sqrt(mu / r)
            v_esc = math.sqrt(2 * mu / r)
            dv_esc = v_esc - v_circ
            
            # Update display
            self.dv_var.set(f"{dv_esc*1000:.1f}")
            self.escape_var.set(f"{v_esc:.3f}")
            
            result = f"""ESCAPE VELOCITY FROM {altitude:.0f} KM ALTITUDE
            
Parameters:
- Circular orbit velocity: {v_circ:.3f} km/s
- Escape velocity: {v_esc:.3f} km/s
- Required ΔV from orbit: {dv_esc*1000:.1f} m/s

Notes:
- Assumes prograde burn from circular orbit
- Earth radius: 6,371 km
- Standard gravitational parameter (μ): 3.986 × 10⁵ km³/s²
"""
            
            self.orbit_text.config(state=tk.NORMAL)
            self.orbit_text.delete(1.0, tk.END)
            self.orbit_text.insert(tk.END, result)
            self.orbit_text.config(state=tk.DISABLED)
            
            self.status_var.set(f"Calculated escape velocity from {altitude:.0f} km altitude")
        
        except Exception as e:
            messagebox.showerror("Calculation Error", f"Failed to calculate escape velocity: {str(e)}")
            self.status_var.set("Error calculating escape velocity")

    def create_pyrocellulose_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Pyrocellulose")
        
        # Header
        ttk.Label(frame, text="Pyrocellulose Formulation Calculator", style='Header.TLabel').grid(row=0, column=0, columnspan=4, pady=10)
        
        # Input parameters
        ttk.Label(frame, text="Nitrogen Content:").grid(row=1, column=0, sticky='e')
        self.pyro_n_var = tk.DoubleVar(value=12.6)
        ttk.Entry(frame, textvariable=self.pyro_n_var, width=10).grid(row=1, column=1, sticky='w')
        ttk.Label(frame, text="%").grid(row=1, column=2, sticky='w')
        
        ttk.Label(frame, text="Stabilizer:").grid(row=2, column=0, sticky='e')
        self.pyro_stab_var = tk.DoubleVar(value=1.0)
        ttk.Entry(frame, textvariable=self.pyro_stab_var, width=10).grid(row=2, column=1, sticky='w')
        ttk.Label(frame, text="%").grid(row=2, column=2, sticky='w')
        
        ttk.Label(frame, text="Stabilizer Type:").grid(row=3, column=0, sticky='e')
        self.pyro_stab_type_var = tk.StringVar(value="Diphenylamine")
        stab_types = ["Diphenylamine", "Ethyl Centralite", "2-Nitrodiphenylamine"]
        ttk.Combobox(frame, textvariable=self.pyro_stab_type_var, values=stab_types, width=20).grid(row=3, column=1, columnspan=2, sticky='w')
        
        ttk.Label(frame, text="Solvent Content:").grid(row=4, column=0, sticky='e')
        self.pyro_solvent_var = tk.DoubleVar(value=5.0)
        ttk.Entry(frame, textvariable=self.pyro_solvent_var, width=10).grid(row=4, column=1, sticky='w')
        ttk.Label(frame, text="%").grid(row=4, column=2, sticky='w')
        
        ttk.Label(frame, text="Moisture Content:").grid(row=5, column=0, sticky='e')
        self.pyro_moisture_var = tk.DoubleVar(value=0.5)
        ttk.Entry(frame, textvariable=self.pyro_moisture_var, width=10).grid(row=5, column=1, sticky='w')
        ttk.Label(frame, text="%").grid(row=5, column=2, sticky='w')
        
        # Button frame
        button_frame = ttk.Frame(frame)
        button_frame.grid(row=6, column=0, columnspan=4, pady=10)
        
        ttk.Button(button_frame, text="Calculate", command=self.calculate_pyrocellulose).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Save Formulation", command=self.save_pyro_formulation).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Load Formulation", command=self.load_pyro_formulation).pack(side=tk.LEFT, padx=5)
        
        # Results text
        self.pyro_text = tk.Text(frame, height=15, width=90, wrap=tk.WORD, font=('Consolas', 10))
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=self.pyro_text.yview)
        scrollbar.grid(row=7, column=4, sticky='ns')
        self.pyro_text.configure(yscrollcommand=scrollbar.set)
        self.pyro_text.grid(row=7, column=0, columnspan=4, sticky='nsew', padx=5, pady=5)
        
        # Configure grid weights
        frame.grid_rowconfigure(7, weight=1)
        frame.grid_columnconfigure(0, weight=1)

    def calculate_pyrocellulose(self):
        try:
            n_content = self.pyro_n_var.get()
            stab = self.pyro_stab_var.get()
            solvent = self.pyro_solvent_var.get()
            moisture = self.pyro_moisture_var.get()
            total = stab + solvent + moisture
            
            if total > 15:
                messagebox.showwarning("Composition Warning", 
                    f"Additives sum to {total:.1f}% (recommended <15%). Adjust values.")
            
            if n_content < 12.0 or n_content > 13.5:
                messagebox.showwarning("Nitrogen Warning",
                    f"Nitrocellulose with {n_content:.1f}% N may be unstable or impractical")
            
            # Calculate properties
            density = 1.25 + (n_content - 12.0) * 0.05
            burn_rate = 0.5 + (n_content - 12.0) * 0.3
            energy = 3000 + (n_content - 12.0) * 500
            
            result = f"""PYROCELLULOSE FORMULATION
            
Composition:
- Nitrogen Content: {n_content:.1f}%
- {self.pyro_stab_type_var.get()} Stabilizer: {stab:.1f}%
- Solvent Content: {solvent:.1f}%
- Moisture Content: {moisture:.1f}%

Properties:
- Theoretical Density: {density:.3f} g/cm³
- Estimated Burn Rate: {burn_rate:.2f} cm/s at STP
- Energy Content: {energy:.0f} J/g
- Stability Index: {stab/0.5:.1f} (1.0 = standard)

Safety Notes:
- Pyrocellulose with >12.6% N is classified as gun cotton
- Maximum safe processing temperature: 50°C
- Store in cool, dry place away from sparks
"""
            
            self.pyro_text.config(state=tk.NORMAL)
            self.pyro_text.delete(1.0, tk.END)
            self.pyro_text.insert(tk.END, result)
            self.pyro_text.config(state=tk.DISABLED)
            
            self.status_var.set(f"Pyrocellulose formulation calculated (N={n_content:.1f}%)")
        
        except Exception as e:
            messagebox.showerror("Calculation Error", f"Failed to calculate formulation: {str(e)}")
            self.status_var.set("Error calculating pyrocellulose formulation")

    def save_pyro_formulation(self):
        pyro_data = {
            'n_content': self.pyro_n_var.get(),
            'stab': self.pyro_stab_var.get(),
            'stab_type': self.pyro_stab_type_var.get(),
            'solvent': self.pyro_solvent_var.get(),
            'moisture': self.pyro_moisture_var.get(),
            'formulation_text': self.pyro_text.get("1.0", tk.END)
        }
        
        filepath = filedialog.asksaveasfilename(
            title="Save Pyrocellulose Formulation",
            defaultextension=".json",
            filetypes=(("JSON Files", "*.json"), ("All Files", "*.*")))
        
        if filepath:
            try:
                with open(filepath, 'w') as f:
                    json.dump(pyro_data, f, indent=4)
                self.status_var.set(f"Pyrocellulose formulation saved to {os.path.basename(filepath)}")
            except Exception as e:
                messagebox.showerror("Save Error", f"Failed to save formulation: {str(e)}")

    def load_pyro_formulation(self):
        filepath = filedialog.askopenfilename(
            title="Load Pyrocellulose Formulation",
            filetypes=(("JSON Files", "*.json"), ("All Files", "*.*")))
        
        if filepath:
            try:
                with open(filepath, 'r') as f:
                    pyro_data = json.load(f)
                
                self.pyro_n_var.set(pyro_data['n_content'])
                self.pyro_stab_var.set(pyro_data['stab'])
                self.pyro_stab_type_var.set(pyro_data['stab_type'])
                self.pyro_solvent_var.set(pyro_data['solvent'])
                self.pyro_moisture_var.set(pyro_data['moisture'])
                
                self.pyro_text.config(state=tk.NORMAL)
                self.pyro_text.delete(1.0, tk.END)
                self.pyro_text.insert(tk.END, pyro_data['formulation_text'])
                self.pyro_text.config(state=tk.DISABLED)
                
                self.status_var.set(f"Pyrocellulose formulation loaded from {os.path.basename(filepath)}")
            except Exception as e:
                messagebox.showerror("Load Error", f"Failed to load formulation: {str(e)}")

    def create_contact_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="About & Contact")
        
        # Header
        ttk.Label(frame, text="About GRIMSTRE DIGITAL TOOLS", style='Header.TLabel').grid(row=0, column=0, columnspan=2, pady=10)
        
        # About text
        about_text = """GRIMSTRE DIGITAL TOOLS - Solid Motor Manufacturing & Flight Analysis
with Advanced Propellant Formulation Tools

Version 2.1 (Python 3.9 Tkinter Version)
Release Date: August 2023

This software is designed for educational and research purposes only.
All calculations are theoretical and should be verified experimentally.

DISCLAIMER:
The developers are not responsible for any misuse of this software.
Rocketry and propellant manufacturing involve dangerous materials and processes.
Always follow all applicable laws and safety regulations.
"""
        about_label = ttk.Label(frame, text=about_text, justify=tk.LEFT)
        about_label.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky='w')
        
        # Contact info
        ttk.Label(frame, text="Contact Information:", style='Header.TLabel').grid(row=2, column=0, columnspan=2, pady=10)
        
        contact_text = """For support, questions, or feature requests:
Email: support@grimstre.com
Website: www.grimstre.com

Development Team:
- Lead Engineer: A. Grimstre
- Propulsion Specialist: J. Kerman
- Software Developer: M. Valentina
"""
        contact_label = ttk.Label(frame, text=contact_text, justify=tk.LEFT)
        contact_label.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky='w')
        
        # License info
        ttk.Label(frame, text="License Information:", style='Header.TLabel').grid(row=4, column=0, columnspan=2, pady=10)
        
        license_text = """This software is provided under the GRIMSTRE EDUCATIONAL LICENSE:
- Free for personal and educational use
- Commercial use requires permission
- No warranty of any kind
- Not for military applications
"""
        license_label = ttk.Label(frame, text=license_text, justify=tk.LEFT)
        license_label.grid(row=5, column=0, columnspan=2, padx=10, pady=10, sticky='w')

# Main application entry point
if __name__ == "__main__":
    root = tk.Tk()
    app = GrimstreDigitalTools(root)
    root.mainloop()