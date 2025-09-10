import tkinter as tk
from tkinter import ttk, messagebox

class PyrocelluloseApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Pyrocellulose Production Calculator")
        self.root.geometry("1000x800")
        
        # Configure style
        self.style = ttk.Style()
        self.style.configure('TFrame', padding=10)
        self.style.configure('TLabel', padding=5)
        
        # Safety warning
        self.safety_warning = tk.Label(
            root, 
            text="⚠️ DANGER: Highly exothermic reactions! Use proper PPE (face shield, acid gloves, apron) and work in fume hood ⚠️",
            fg='red', 
            bg='yellow',
            font=('Arial', 12, 'bold'),
            pady=10
        )
        self.safety_warning.pack(fill=tk.X)
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Create tabs
        self.create_lab_tab()
        self.create_industrial_tab()
        self.create_acid_prep_tab()  # New tab for acid preparation
        self.create_gun_cotton_tab()
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        self.status_bar = tk.Label(root, textvariable=self.status_var, bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Configure grid weights for resizing
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
    
    def create_lab_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Lab Production")
        
        # Header
        ttk.Label(frame, text="Laboratory Pyrocellulose Production", font=('Arial', 14, 'bold')).grid(row=0, column=0, columnspan=4, pady=10)
        
        # Input fields with unit options
        units = {
            'weight': ['mg', 'g', 'kg', 'oz', 'lb'],
            'volume': ['μL', 'mL', 'L', 'fl oz'],
            'time': ['sec', 'min', 'hr'],
            'area': ['mm²', 'cm²', 'm²', 'in²']
        }
        
        # Cotton input
        ttk.Label(frame, text="Cellulose Amount:").grid(row=1, column=0, sticky='e')
        self.cotton_var = tk.DoubleVar(value=5.0)
        ttk.Entry(frame, textvariable=self.cotton_var, width=10).grid(row=1, column=1, sticky='w')
        self.cotton_unit = ttk.Combobox(frame, values=units['weight'], width=5)
        self.cotton_unit.current(1)  # Default to grams
        self.cotton_unit.grid(row=1, column=2)
        
        # Acid volume input
        ttk.Label(frame, text="Acid Volume:").grid(row=2, column=0, sticky='e')
        self.acid_var = tk.DoubleVar(value=150.0)
        ttk.Entry(frame, textvariable=self.acid_var, width=10).grid(row=2, column=1, sticky='w')
        self.acid_unit = ttk.Combobox(frame, values=units['volume'], width=5)
        self.acid_unit.current(1)  # Default to mL
        self.acid_unit.grid(row=2, column=2)
        
        # Time input
        ttk.Label(frame, text="Nitration Time:").grid(row=3, column=0, sticky='e')
        self.time_var = tk.DoubleVar(value=30.0)
        ttk.Entry(frame, textvariable=self.time_var, width=10).grid(row=3, column=1, sticky='w')
        self.time_unit = ttk.Combobox(frame, values=units['time'], width=5)
        self.time_unit.current(1)  # Default to minutes
        self.time_unit.grid(row=3, column=2)
        
        # Calculate button
        ttk.Button(frame, text="Calculate Process", command=self.calculate_lab).grid(row=4, column=0, columnspan=3, pady=10)
        
        # Results notebook
        results_notebook = ttk.Notebook(frame)
        results_notebook.grid(row=5, column=0, columnspan=4, sticky='nsew', padx=5, pady=5)
        
        # Process steps tab
        process_frame = ttk.Frame(results_notebook)
        results_notebook.add(process_frame, text="Process Steps")
        self.process_text = tk.Text(process_frame, height=15, width=90, wrap=tk.WORD, font=('Consolas', 10))
        self.process_text.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Calculations tab
        calc_frame = ttk.Frame(results_notebook)
        results_notebook.add(calc_frame, text="Calculated Values")
        self.calc_text = tk.Text(calc_frame, height=15, width=90, wrap=tk.WORD, font=('Consolas', 10))
        self.calc_text.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Configure grid weights
        for i in range(6):
            frame.grid_rowconfigure(i, weight=1)
        for j in range(4):
            frame.grid_columnconfigure(j, weight=1)
        
        # Initial update
        self.update_lab_process()
        
        # Bind variables to update process
        for var in [self.cotton_var, self.acid_var, self.time_var]:
            var.trace_add('write', lambda *args: self.update_lab_process())
    
    def convert_units(self, value, from_unit, to_category):
        """Convert between different unit systems"""
        conversions = {
            'weight': {
                'mg': {'g': 0.001, 'kg': 0.000001, 'oz': 0.000035274, 'lb': 0.00000220462},
                'g': {'mg': 1000, 'kg': 0.001, 'oz': 0.035274, 'lb': 0.00220462},
                'kg': {'mg': 1000000, 'g': 1000, 'oz': 35.274, 'lb': 2.20462},
                'oz': {'mg': 28349.5, 'g': 28.3495, 'kg': 0.0283495, 'lb': 0.0625},
                'lb': {'mg': 453592, 'g': 453.592, 'kg': 0.453592, 'oz': 16}
            },
            'volume': {
                'μL': {'mL': 0.001, 'L': 0.000001, 'fl oz': 0.000033814},
                'mL': {'μL': 1000, 'L': 0.001, 'fl oz': 0.033814},
                'L': {'μL': 1000000, 'mL': 1000, 'fl oz': 33.814},
                'fl oz': {'μL': 29573.5, 'mL': 29.5735, 'L': 0.0295735}
            },
            'time': {
                'sec': {'min': 1/60, 'hr': 1/3600},
                'min': {'sec': 60, 'hr': 1/60},
                'hr': {'sec': 3600, 'min': 60}
            },
            'area': {
                'mm²': {'cm²': 0.01, 'm²': 0.000001, 'in²': 0.00155},
                'cm²': {'mm²': 100, 'm²': 0.0001, 'in²': 0.155},
                'm²': {'mm²': 1000000, 'cm²': 10000, 'in²': 1550},
                'in²': {'mm²': 645.16, 'cm²': 6.4516, 'm²': 0.00064516}
            }
        }
        
        if from_unit in conversions.get(to_category, {}):
            return value, from_unit  # Already in target category
        
        for category, units in conversions.items():
            if from_unit in units:
                if to_category == category:  # Convert to first unit in category
                    target_unit = list(units[from_unit].keys())[0]
                    return value * units[from_unit][target_unit], target_unit
                else:  # Convert between categories (e.g., weight to volume - not implemented)
                    return value, from_unit
        
        return value, from_unit  # No conversion available
    
    def update_lab_process(self):
        try:
            # Convert all inputs to standard units (g, mL, min)
            cotton, cotton_std_unit = self.convert_units(self.cotton_var.get(), self.cotton_unit.get(), 'weight')
            acid, acid_std_unit = self.convert_units(self.acid_var.get(), self.acid_unit.get(), 'volume')
            time, time_std_unit = self.convert_units(self.time_var.get(), self.time_unit.get(), 'time')
            
            # Calculate acid components (60% H2SO4, 40% HNO3 by volume)
            h2so4_vol = acid * 0.6
            hno3_vol = acid * 0.4
            
            # Calculate masses (using densities: H2SO4 1.84 g/mL, HNO3 1.42 g/mL)
            h2so4_mass = h2so4_vol * 1.84
            hno3_mass = hno3_vol * 1.42
            
            # Calculate theoretical yield (assuming 40% mass increase from nitration)
            theoretical_yield = cotton * 1.4
            
            # Generate process description
            process = f"""PYROCELLULOSE LAB PRODUCTION PROTOCOL

1. ACID PREPARATION:
   - Measure {h2so4_vol:.1f} mL sulfuric acid (96-98%, d=1.84 g/mL, {h2so4_mass:.1f}g)
   - Measure {hno3_vol:.1f} mL nitric acid (68%, d=1.42 g/mL, {hno3_mass:.1f}g)
   - In fume hood, slowly add sulfuric acid to nitric acid while stirring
   - Cool mixture to 20-25°C before use

2. CELLULOSE PREPARATION:
   - Weigh {cotton:.1f}g of purified cotton (or filter paper)
   - Dry at 100-105°C for 2 hours, cool in desiccator

3. NITRATION PROCESS:
   - Immerse dried cellulose in acid mixture
   - Maintain temperature at 25-30°C for {time:.0f} minutes
   - Stir gently every 5 minutes with glass rod

4. TERMINATION & WASHING:
   - Remove cellulose with glass rod, press out excess acid
   - Immediately transfer to 2L cold distilled water
   - Rinse with running water for 30 minutes

5. PURIFICATION:
   - Boil in distilled water for 1 hour
   - Repeat boiling with fresh water (3×30 minutes)
   - Test final rinse water with litmus (pH 6-7)

6. DRYING:
   - Press out excess water between filter papers
   - Air-dry at room temperature for 48 hours
   - Final drying at 40°C for 4 hours

THEORETICAL YIELD: {theoretical_yield:.1f}g (12.0-12.4% nitrogen)
ACTUAL YIELD: {theoretical_yield*0.85:.1f}-{theoretical_yield:.1f}g (85-100% efficiency)
"""
            
            # Generate calculations
            calculations = f"""CALCULATED VALUES:

Input Parameters:
- Cellulose: {self.cotton_var.get():.2f} {self.cotton_unit.get()} → {cotton:.2f}g
- Acid Volume: {self.acid_var.get():.2f} {self.acid_unit.get()} → {acid:.2f}mL
- Nitration Time: {self.time_var.get():.2f} {self.time_unit.get()} → {time:.2f} minutes

Acid Composition:
- Sulfuric Acid (H₂SO₄): {h2so4_vol:.1f}mL ({h2so4_mass:.1f}g)
- Nitric Acid (HNO₃): {hno3_vol:.1f}mL ({hno3_mass:.1f}g)
- Total Acid Mass: {h2so4_mass + hno3_mass:.1f}g

Stoichiometry:
- Acid to Cellulose Ratio: {acid:.1f}mL : {cotton:.1f}g ({(acid/cotton):.2f} mL/g)
- H₂SO₄:HNO₃ Ratio: 3:2 by volume

Safety Parameters:
- Maximum Exotherm: ~45°C (must keep below 50°C)
- Acid Waste Generated: {acid*1.1:.1f}mL (10% excess)
"""
            
            self.process_text.config(state=tk.NORMAL)
            self.process_text.delete(1.0, tk.END)
            self.process_text.insert(tk.END, process)
            self.process_text.config(state=tk.DISABLED)
            
            self.calc_text.config(state=tk.NORMAL)
            self.calc_text.delete(1.0, tk.END)
            self.calc_text.insert(tk.END, calculations)
            self.calc_text.config(state=tk.DISABLED)
            
        except Exception as e:
            self.status_var.set(f"Error in calculations: {str(e)}")
    
    def calculate_lab(self):
        try:
            # Validate inputs
            if self.cotton_var.get() <= 0 or self.acid_var.get() <= 0 or self.time_var.get() <= 0:
                messagebox.showerror("Input Error", "All values must be positive numbers")
                return
            
            self.update_lab_process()
            self.status_var.set("Lab process calculated successfully")
            
        except tk.TclError:
            messagebox.showerror("Input Error", "Please enter valid numbers in all fields")
    
    def create_industrial_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Industrial Production")
        
        # Header
        ttk.Label(frame, text="Industrial-Scale Pyrocellulose Production", font=('Arial', 14, 'bold')).grid(row=0, column=0, columnspan=4, pady=10)
        
        # Batch size input
        ttk.Label(frame, text="Batch Size:").grid(row=1, column=0, sticky='e')
        self.batch_var = tk.DoubleVar(value=100.0)
        ttk.Entry(frame, textvariable=self.batch_var, width=10).grid(row=1, column=1, sticky='w')
        self.batch_unit = ttk.Combobox(frame, values=['kg', 'ton', 'lb'], width=5)
        self.batch_unit.current(0)
        self.batch_unit.grid(row=1, column=2)
        
        # Nitrogen content
        ttk.Label(frame, text="Nitrogen Content:").grid(row=2, column=0, sticky='e')
        self.nitro_var = tk.DoubleVar(value=12.2)
        ttk.Entry(frame, textvariable=self.nitro_var, width=10).grid(row=2, column=1, sticky='w')
        ttk.Label(frame, text="%").grid(row=2, column=2, sticky='w')
        
        # Acid concentration
        ttk.Label(frame, text="H₂SO₄ Concentration:").grid(row=3, column=0, sticky='e')
        self.h2so4_conc_var = tk.DoubleVar(value=96.0)
        ttk.Entry(frame, textvariable=self.h2so4_conc_var, width=10).grid(row=3, column=1, sticky='w')
        ttk.Label(frame, text="%").grid(row=3, column=2, sticky='w')
        
        ttk.Label(frame, text="HNO₃ Concentration:").grid(row=4, column=0, sticky='e')
        self.hno3_conc_var = tk.DoubleVar(value=68.0)
        ttk.Entry(frame, textvariable=self.hno3_conc_var, width=10).grid(row=4, column=1, sticky='w')
        ttk.Label(frame, text="%").grid(row=4, column=2, sticky='w')
        
        # Calculate button
        ttk.Button(frame, text="Calculate Industrial Process", command=self.calculate_industrial).grid(row=5, column=0, columnspan=3, pady=10)
        
        # Results notebook
        results_notebook = ttk.Notebook(frame)
        results_notebook.grid(row=6, column=0, columnspan=4, sticky='nsew', padx=5, pady=5)
        
        # Process tab
        process_frame = ttk.Frame(results_notebook)
        results_notebook.add(process_frame, text="Process Flow")
        self.industrial_process_text = tk.Text(process_frame, height=15, width=90, wrap=tk.WORD, font=('Consolas', 10))
        self.industrial_process_text.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Calculations tab
        calc_frame = ttk.Frame(results_notebook)
        results_notebook.add(calc_frame, text="Material Requirements")
        self.industrial_calc_text = tk.Text(calc_frame, height=15, width=90, wrap=tk.WORD, font=('Consolas', 10))
        self.industrial_calc_text.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Configure grid weights
        for i in range(7):
            frame.grid_rowconfigure(i, weight=1)
        for j in range(4):
            frame.grid_columnconfigure(j, weight=1)
        
        # Initial update
        self.update_industrial_process()
        
        # Bind variables
        for var in [self.batch_var, self.nitro_var, self.h2so4_conc_var, self.hno3_conc_var]:
            var.trace_add('write', lambda *args: self.update_industrial_process())
    
    def update_industrial_process(self):
        try:
            # Convert batch size to kg
            batch_size = self.batch_var.get()
            if self.batch_unit.get() == 'ton':
                batch_size *= 1000
            elif self.batch_unit.get() == 'lb':
                batch_size *= 0.453592
            
            nitro_content = self.nitro_var.get()
            h2so4_conc = self.h2so4_conc_var.get() / 100
            hno3_conc = self.hno3_conc_var.get() / 100
            
            # Calculate acid requirements (industrial ratios)
            h2so4_kg = batch_size * (10 + (nitro_content - 12.0) * 2)
            hno3_kg = batch_size * (5 + (nitro_content - 12.0) * 1)
            
            # Adjust for acid concentrations
            h2so4_vol = h2so4_kg / (1.84 * h2so4_conc)  # 1.84 g/mL density
            hno3_vol = hno3_kg / (1.42 * hno3_conc)     # 1.42 g/mL density
            
            # Calculate water requirements
            wash_water = batch_size * 50  # 50L water per kg cellulose
            
            # Generate process description
            process = f"""INDUSTRIAL PYROCELLULOSE PRODUCTION PROCESS

1. MATERIAL PREPARATION:
   - Weigh {batch_size:.1f} kg cellulose (wood pulp or cotton linters)
   - Dry to <0.5% moisture in rotary dryer at 105°C
   - Screen to remove oversize particles (>2mm)

2. ACID MIXING:
   - Prepare nitrating acid in lead-lined reactor:
     - {h2so4_vol:.1f}L sulfuric acid ({h2so4_conc*100:.1f}%, {h2so4_kg:.1f}kg)
     - {hno3_vol:.1f}L nitric acid ({hno3_conc*100:.1f}%, {hno3_kg:.1f}kg)
   - Cool to 15-20°C with jacket cooling

3. NITRATION:
   - Feed cellulose into dipper system at {batch_size/10:.1f} kg/min
   - Immerse for 30-45 minutes at 25-30°C
   - Control exotherm with cooling jacket

4. CENTRIFUGATION:
   - Separate nitrated cellulose at 2000 rpm
   - Recover >95% spent acid for regeneration
   - Immediate washing with cold water

5. STABILIZATION:
   - Boil in rotary washers with {wash_water:.0f}L water
   - 6-8 washing cycles (1 hour each)
   - Neutralize with Na₂CO₃ solution if needed

6. FINISHING:
   - Refine in beater to desired fiber length
   - Adjust moisture to 25-30%
   - Package in 100kg polyethylene-lined drums

PRODUCTION DATA:
- Target Nitrogen: {nitro_content:.1f}% ±0.2%
- Throughput: {batch_size*24:.0f} kg/day (continuous)
- Acid Consumption: {h2so4_kg + hno3_kg:.0f} kg per {batch_size:.0f}kg product
"""
            
            # Generate calculations
            calculations = f"""INDUSTRIAL PRODUCTION CALCULATIONS

Batch Parameters:
- Cellulose: {self.batch_var.get():.1f} {self.batch_unit.get()} → {batch_size:.1f} kg
- Target Nitrogen: {nitro_content:.1f}%
- H₂SO₄ Concentration: {h2so4_conc*100:.1f}%
- HNO₃ Concentration: {hno3_conc*100:.1f}%

Material Requirements:
- Sulfuric Acid: {h2so4_kg:.1f} kg ({h2so4_vol:.1f}L)
- Nitric Acid: {hno3_kg:.1f} kg ({hno3_vol:.1f}L)
- Total Acid Volume: {h2so4_vol + hno3_vol:.1f}L
- Wash Water: {wash_water:.0f}L

Process Economics:
- Acid Cost: ${(h2so4_kg*0.3 + hno3_kg*0.5):.0f} (estimated)
- Water Treatment: {wash_water*0.02:.1f} kg NaOH required
- Energy Consumption: {batch_size*5:.0f} kWh

Safety Considerations:
- Cooling Capacity Required: {batch_size*2:.0f} kW
- Ventilation: {batch_size*10:.0f} m³/min airflow
- Neutralization Capacity: {batch_size*0.5:.0f} kg Na₂CO₃
"""
            
            self.industrial_process_text.config(state=tk.NORMAL)
            self.industrial_process_text.delete(1.0, tk.END)
            self.industrial_process_text.insert(tk.END, process)
            self.industrial_process_text.config(state=tk.DISABLED)
            
            self.industrial_calc_text.config(state=tk.NORMAL)
            self.industrial_calc_text.delete(1.0, tk.END)
            self.industrial_calc_text.insert(tk.END, calculations)
            self.industrial_calc_text.config(state=tk.DISABLED)
            
        except Exception as e:
            self.status_var.set(f"Error in industrial calculations: {str(e)}")
    
    def calculate_industrial(self):
        try:
            if (self.batch_var.get() <= 0 or 
                self.nitro_var.get() < 12.0 or 
                self.nitro_var.get() > 13.5 or
                self.h2so4_conc_var.get() <= 0 or
                self.hno3_conc_var.get() <= 0):
                messagebox.showerror("Input Error", "Please enter valid parameters:\n- Batch > 0\n- Nitrogen 12.0-13.5%\n- Acid concentrations > 0%")
                return
            
            self.update_industrial_process()
            self.status_var.set("Industrial process calculated successfully")
            
        except tk.TclError:
            messagebox.showerror("Input Error", "Please enter valid numbers in all fields")
    
    def create_acid_prep_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Acid Preparation")
        
        # Header
        ttk.Label(frame, text="Acid Mixture Preparation", font=('Arial', 14, 'bold')).grid(row=0, column=0, columnspan=4, pady=10)
        
        # Acid selection
        ttk.Label(frame, text="Acid Mixture Type:").grid(row=1, column=0, sticky='e')
        self.acid_type_var = tk.StringVar(value="Standard Nitrating")
        acid_types = [
            "Standard Nitrating (60% H₂SO₄, 40% HNO₃)",
            "High-Nitrogen (50% H₂SO₄, 45% HNO₃, 5% H₃PO₄)",
            "Economy (70% H₂SO₄, 30% HNO₃)",
            "Gun Cotton (40% H₂SO₄, 55% HNO₃, 5% H₂O)"
        ]
        ttk.Combobox(frame, textvariable=self.acid_type_var, values=acid_types, width=40).grid(row=1, column=1, columnspan=3, sticky='w')
        
        # Total volume input
        ttk.Label(frame, text="Total Volume:").grid(row=2, column=0, sticky='e')
        self.total_vol_var = tk.DoubleVar(value=1000.0)
        ttk.Entry(frame, textvariable=self.total_vol_var, width=10).grid(row=2, column=1, sticky='w')
        self.total_vol_unit = ttk.Combobox(frame, values=['mL', 'L'], width=5)
        self.total_vol_unit.current(0)
        self.total_vol_unit.grid(row=2, column=2)
        
        # Temperature control
        ttk.Label(frame, text="Cooling Temperature:").grid(row=3, column=0, sticky='e')
        self.temp_var = tk.DoubleVar(value=20.0)
        ttk.Entry(frame, textvariable=self.temp_var, width=10).grid(row=3, column=1, sticky='w')
        ttk.Label(frame, text="°C").grid(row=3, column=2, sticky='w')
        
        # Calculate button
        ttk.Button(frame, text="Calculate Acid Mixture", command=self.calculate_acid_mix).grid(row=4, column=0, columnspan=4, pady=10)
        
        # Results frame
        results_frame = ttk.LabelFrame(frame, text="Acid Preparation Protocol", padding=10)
        results_frame.grid(row=5, column=0, columnspan=4, sticky='nsew', padx=5, pady=5)
        
        self.acid_text = tk.Text(results_frame, height=15, width=90, wrap=tk.WORD, font=('Consolas', 10))
        self.acid_text.pack(fill='both', expand=True)
        
        # Configure grid weights
        for i in range(6):
            frame.grid_rowconfigure(i, weight=1)
        for j in range(4):
            frame.grid_columnconfigure(j, weight=1)
        
        # Initial update
        self.update_acid_mix()
        
        # Bind variables
        for var in [self.acid_type_var, self.total_vol_var, self.temp_var]:
            var.trace_add('write', lambda *args: self.update_acid_mix())
    
    def update_acid_mix(self):
        try:
            acid_type = self.acid_type_var.get()
            total_vol = self.total_vol_var.get()
            if self.total_vol_unit.get() == 'L':
                total_vol *= 1000  # Convert to mL
            
            temp = self.temp_var.get()
            
            # Determine acid ratios based on type
            if "High-Nitrogen" in acid_type:
                ratios = {'H₂SO₄': 0.50, 'HNO₃': 0.45, 'H₃PO₄': 0.05}
            elif "Economy" in acid_type:
                ratios = {'H₂SO₄': 0.70, 'HNO₃': 0.30}
            elif "Gun Cotton" in acid_type:
                ratios = {'H₂SO₄': 0.40, 'HNO₃': 0.55, 'H₂O': 0.05}
            else:  # Standard
                ratios = {'H₂SO₄': 0.60, 'HNO₃': 0.40}
            
            # Calculate volumes
            h2so4_vol = total_vol * ratios.get('H₂SO₄', 0)
            hno3_vol = total_vol * ratios.get('HNO₃', 0)
            h3po4_vol = total_vol * ratios.get('H₃PO₄', 0)
            h2o_vol = total_vol * ratios.get('H₂O', 0)
            
            # Calculate masses (using densities)
            h2so4_mass = h2so4_vol * 1.84
            hno3_mass = hno3_vol * 1.42
            h3po4_mass = h3po4_vol * 1.88 if h3po4_vol > 0 else 0
            total_mass = h2so4_mass + hno3_mass + h3po4_mass + h2o_vol
            
            # Generate protocol
            protocol = f"""ACID MIXTURE PREPARATION PROTOCOL

Mixture Type: {acid_type}
Total Volume: {total_vol:.1f}mL ({total_vol/1000:.2f}L)
Target Temperature: {temp:.1f}°C

COMPONENTS:
- Sulfuric Acid (96% H₂SO₄): {h2so4_vol:.1f}mL ({h2so4_mass:.1f}g)
- Nitric Acid (68% HNO₃): {hno3_vol:.1f}mL ({hno3_mass:.1f}g)"""
            
            if h3po4_vol > 0:
                protocol += f"\n- Phosphoric Acid (85% H₃PO₄): {h3po4_vol:.1f}mL ({h3po4_mass:.1f}g)"
            if h2o_vol > 0:
                protocol += f"\n- Distilled Water: {h2o_vol:.1f}mL"
            
            protocol += f"""
Total Mass: {total_mass:.1f}g
Density: {total_mass/total_vol:.3f}g/mL

PREPARATION STEPS:
1. Chill nitric acid to {temp-5:.0f}°C in ice bath
2. In fume hood, place {hno3_vol:.1f}mL HNO₃ in jacketed reactor
3. Slowly add {h2so4_vol:.1f}mL H₂SO₄ with constant stirring
4. Maintain temperature below {temp+5:.0f}°C with cooling"""
            
            if h3po4_vol > 0:
                protocol += f"\n5. Add {h3po4_vol:.1f}mL H₃PO₄ dropwise"
            if h2o_vol > 0:
                protocol += f"\n6. Add {h2o_vol:.1f}mL H₂O slowly"
            
            protocol += f"""
7. Stir for 15 minutes after last addition
8. Store in glass or PTFE container at {temp:.0f}±2°C

SAFETY NOTES:
- ALWAYS add sulfuric acid to nitric acid (never reverse)
- Use borosilicate glass or PTFE equipment only
- Immediate neutralization of spills with NaHCO₃
- Exotherm may reach {temp+30:.0f}°C if uncontrolled
"""
            
            self.acid_text.config(state=tk.NORMAL)
            self.acid_text.delete(1.0, tk.END)
            self.acid_text.insert(tk.END, protocol)
            self.acid_text.config(state=tk.DISABLED)
            
        except Exception as e:
            self.status_var.set(f"Error in acid preparation: {str(e)}")
    
    def calculate_acid_mix(self):
        try:
            if self.total_vol_var.get() <= 0 or self.temp_var.get() < 0:
                messagebox.showerror("Input Error", "Volume must be positive and temperature realistic")
                return
            
            self.update_acid_mix()
            self.status_var.set("Acid mixture calculated successfully")
            
        except tk.TclError:
            messagebox.showerror("Input Error", "Please enter valid numbers in all fields")
    
    def create_gun_cotton_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Gun Cotton")
        
        # Header
        ttk.Label(frame, text="Gun Cotton (High-Nitrogen Nitrocellulose)", font=('Arial', 14, 'bold')).grid(row=0, column=0, columnspan=2, pady=10)
        
        # Process description
        process_text = """GUN COTTON PRODUCTION (13.0-13.5% Nitrogen)

SPECIAL CONSIDERATIONS:
1. ACID COMPOSITION:
   - Higher HNO₃ concentration (70-90%)
   - Reduced H₂SO₄ content (30-40%)
   - Possible addition of stabilizers (H₃PO₄, urea)

2. EXTENDED NITRATION:
   - 2-3 hour immersion time
   - Strict temperature control (15-20°C)
   - Multiple acid refresh cycles

3. INTENSIVE WASHING:
   - 12-15 boiling cycles (1 hour each)
   - Alkaline treatment between washes (Na₂CO₃)
   - Final neutralization with ammonium carbonate

4. STABILIZATION:
   - Ethanol or ether washing
   - Anti-oxidant additives (Diphenylamine)
   - Long-term aging (6-12 months)

CHARACTERISTICS:
- Nitrogen Content: 13.0-13.5%
- Ignition Temperature: 170-180°C
- Solubility: Insoluble in most solvents
- Energy Content: 3800-4000 J/g

SAFETY PROTOCOLS:
1. Small batches only (<100g per reaction)
2. Remote operation behind blast shield
3. Ground all equipment (static hazard)
4. Immediate disposal of failed batches
5. Storage in water-wet condition only

LEGAL NOTICE:
Production of gun cotton (nitrocellulose >12.6% N) requires
government authorization in most countries. This information
is provided for academic study only.
"""
        
        text = tk.Text(frame, height=25, width=90, wrap=tk.WORD, font=('Consolas', 10))
        text.insert(tk.END, process_text)
        text.config(state=tk.DISABLED)
        text.grid(row=1, column=0, columnspan=2, padx=10, pady=10)
        
        # Warning label
        warning = tk.Label(frame, 
            text="⚠️ WARNING: Gun cotton is a high explosive - Professional supervision required ⚠️",
            fg='red', 
            bg='yellow',
            font=('Arial', 12, 'bold'),
            pady=5
        )
        warning.grid(row=2, column=0, columnspan=2, sticky='ew', padx=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = PyrocelluloseApp(root)
    root.mainloop()
