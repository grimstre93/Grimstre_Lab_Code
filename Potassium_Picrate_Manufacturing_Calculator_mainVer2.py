# -*- coding: utf-8 -*-
"""
Created on Tue Aug 19 17:25:58 2025

@author: samng
"""

import tkinter as tk
from tkinter import ttk, scrolledtext
import math

class PotassiumPicrateCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Potassium Picrate Manufacturing Calculator")
        self.root.geometry("1200x800")
        
        # Molecular weights
        self.MW_PICRIC_ACID = 229.11  # g/mol
        self.MW_K2CO3 = 138.21  # g/mol
        self.MW_POTASSIUM_PICRATE = 267.21  # g/mol
        
        self.setup_ui()
        
    def setup_ui(self):
        # Create notebook (tabbed interface)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Create frames for each tab
        self.calculator_frame = ttk.Frame(self.notebook)
        self.precursors_frame = ttk.Frame(self.notebook)
        self.properties_frame = ttk.Frame(self.notebook)
        self.safety_frame = ttk.Frame(self.notebook)
        
        self.notebook.add(self.calculator_frame, text='Manufacturing Calculator')
        self.notebook.add(self.precursors_frame, text='Precursor Manufacturing')
        self.notebook.add(self.properties_frame, text='Properties')
        self.notebook.add(self.safety_frame, text='Safety Procedures')
        
        self.setup_calculator_tab()
        self.setup_precursors_tab()
        self.setup_properties_tab()
        self.setup_safety_tab()
        
    def setup_calculator_tab(self):
        # Warning label
        warning_frame = ttk.LabelFrame(self.calculator_frame, text="WARNING")
        warning_frame.pack(fill='x', padx=10, pady=5)
        
        warning_text = ("Potassium picrate is a sensitive explosive compound. This calculator is for educational purposes only. "
                       "Only trained professionals with proper safety equipment and facilities should attempt to handle or synthesize this compound.")
        warning_label = ttk.Label(warning_frame, text=warning_text, wraplength=1000, foreground='red')
        warning_label.pack(padx=10, pady=10)
        
        # Main content frame
        content_frame = ttk.Frame(self.calculator_frame)
        content_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Left frame for inputs
        left_frame = ttk.LabelFrame(content_frame, text="Manufacturing Parameters")
        left_frame.pack(side='left', fill='both', expand=True, padx=(0, 5))
        
        # Input fields
        inputs = [
            ("Desired Potassium Picrate Amount (g)", "target_amount", 50.0),
            ("Potassium Carbonate Purity (%)", "k2co3_purity", 95),
            ("Picric Acid Purity (%)", "picric_purity", 98),
            ("Reaction Temperature (°C)", "reaction_temp", 95),
            ("Water Volume per gram of Picric Acid (ml)", "water_ratio", 2.0)
        ]
        
        self.input_vars = {}
        for i, (label, name, default) in enumerate(inputs):
            frame = ttk.Frame(left_frame)
            frame.pack(fill='x', pady=5)
            
            ttk.Label(frame, text=label).pack(side='left')
            var = tk.DoubleVar(value=default)
            entry = ttk.Entry(frame, textvariable=var, width=15)
            entry.pack(side='right')
            self.input_vars[name] = var
        
        # Calculate button
        calculate_btn = ttk.Button(left_frame, text="Calculate Manufacturing Parameters", command=self.calculate)
        calculate_btn.pack(pady=10)
        
        # Notes frame
        notes_frame = ttk.LabelFrame(left_frame, text="Calculation Notes")
        notes_frame.pack(fill='x', pady=10)
        
        notes_text = (
            "• Based on the reaction: 2C₆H₃N₃O₇ + K₂CO₃ → 2C₆H₂KN₃O₇ + CO₂ + H₂O\n"
            "• Molecular weights: Picric Acid = 229.11 g/mol, K₂CO₃ = 138.21 g/mol, Potassium Picrate = 267.21 g/mol\n"
            "• Yield percentage is estimated based on reaction temperature and purity"
        )
        notes_label = ttk.Label(notes_frame, text=notes_text, wraplength=400)
        notes_label.pack(padx=10, pady=10)
        
        # Right frame for results
        right_frame = ttk.Frame(content_frame)
        right_frame.pack(side='right', fill='both', expand=True, padx=(5, 0))
        
        # Results frame
        self.results_frame = ttk.LabelFrame(right_frame, text="Calculation Results")
        self.results_frame.pack(fill='both', expand=True)
        
        # Required materials table
        materials_frame = ttk.LabelFrame(self.results_frame, text="Required Materials")
        materials_frame.pack(fill='x', padx=10, pady=5)
        
        self.materials_tree = ttk.Treeview(materials_frame, columns=('amount'), show='tree headings', height=3)
        self.materials_tree.heading('#0', text='Material')
        self.materials_tree.heading('amount', text='Amount')
        self.materials_tree.column('#0', width=200)
        self.materials_tree.column('amount', width=100)
        self.materials_tree.pack(fill='x', padx=5, pady=5)
        
        # Reaction information table
        reaction_frame = ttk.LabelFrame(self.results_frame, text="Reaction Information")
        reaction_frame.pack(fill='x', padx=10, pady=5)
        
        self.reaction_tree = ttk.Treeview(reaction_frame, columns=('value'), show='tree headings', height=4)
        self.reaction_tree.heading('#0', text='Parameter')
        self.reaction_tree.heading('value', text='Value')
        self.reaction_tree.column('#0', width=150)
        self.reaction_tree.column('value', width=100)
        self.reaction_tree.pack(fill='x', padx=5, pady=5)
        
        # Procedure output
        procedure_frame = ttk.LabelFrame(self.calculator_frame, text="Manufacturing Procedure")
        procedure_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.procedure_text = scrolledtext.ScrolledText(procedure_frame, wrap=tk.WORD, width=100, height=15)
        self.procedure_text.pack(fill='both', expand=True, padx=10, pady=10)
        self.procedure_text.insert(tk.END, "Procedure will be generated here after calculation.")
        self.procedure_text.config(state=tk.DISABLED)
        
        # Perform initial calculation
        self.calculate()
        
    def setup_precursors_tab(self):
        # Warning label
        warning_frame = ttk.LabelFrame(self.precursors_frame, text="WARNING")
        warning_frame.pack(fill='x', padx=10, pady=5)
        
        warning_text = "These procedures involve hazardous chemicals. Proper safety equipment and training are required."
        warning_label = ttk.Label(warning_frame, text=warning_text, wraplength=1000, foreground='orange')
        warning_label.pack(padx=10, pady=10)
        
        # Create notebook for precursor tabs
        precursor_notebook = ttk.Notebook(self.precursors_frame)
        precursor_notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Potassium carbonate tab
        k2co3_frame = ttk.Frame(precursor_notebook)
        precursor_notebook.add(k2co3_frame, text='Potassium Carbonate')
        
        k2co3_text = scrolledtext.ScrolledText(k2co3_frame, wrap=tk.WORD, width=100, height=25)
        k2co3_text.pack(fill='both', expand=True, padx=10, pady=10)
        k2co3_text.insert(tk.END, self.get_k2co3_content())
        k2co3_text.config(state=tk.DISABLED)
        
        # Picric acid tab
        picric_frame = ttk.Frame(precursor_notebook)
        precursor_notebook.add(picric_frame, text='Picric Acid')
        
        picric_text = scrolledtext.ScrolledText(picric_frame, wrap=tk.WORD, width=100, height=25)
        picric_text.pack(fill='both', expand=True, padx=10, pady=10)
        picric_text.insert(tk.END, self.get_picric_content())
        picric_text.config(state=tk.DISABLED)
        
        # TNT tab
        tnt_frame = ttk.Frame(precursor_notebook)
        precursor_notebook.add(tnt_frame, text='TNT')
        
        tnt_text = scrolledtext.ScrolledText(tnt_frame, wrap=tk.WORD, width=100, height=25)
        tnt_text.pack(fill='both', expand=True, padx=10, pady=10)
        tnt_text.insert(tk.END, self.get_tnt_content())
        tnt_text.config(state=tk.DISABLED)
        
    def setup_properties_tab(self):
        # Create paned window for split view
        paned_window = ttk.PanedWindow(self.properties_frame, orient=tk.HORIZONTAL)
        paned_window.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Physical properties frame
        physical_frame = ttk.LabelFrame(paned_window, text="Physical Properties")
        paned_window.add(physical_frame, weight=1)
        
        physical_tree = ttk.Treeview(physical_frame, columns=('value'), show='tree headings', height=7)
        physical_tree.heading('#0', text='Property')
        physical_tree.heading('value', text='Value')
        physical_tree.column('#0', width=150)
        physical_tree.column('value', width=150)
        physical_tree.pack(fill='both', expand=True, padx=10, pady=10)
        
        physical_data = [
            ("Chemical Formula", "C6H2KN3O7"),
            ("Molecular Weight", "267.21 g/mol"),
            ("Appearance", "Yellow crystalline solid"),
            ("Density", "1.83 g/cm³"),
            ("Melting Point", "Decomposes explosively"),
            ("Solubility in Water", "1.4 g/100 mL (20°C)"),
            ("Crystal Structure", "Monoclinic")
        ]
        
        for prop, value in physical_data:
            physical_tree.insert('', 'end', text=prop, values=(value,))
        
        # Chemical properties frame
        chemical_frame = ttk.LabelFrame(paned_window, text="Chemical Properties")
        paned_window.add(chemical_frame, weight=1)
        
        chemical_tree = ttk.Treeview(chemical_frame, columns=('value'), show='tree headings', height=7)
        chemical_tree.heading('#0', text='Property')
        chemical_tree.heading('value', text='Description')
        chemical_tree.column('#0', width=150)
        chemical_tree.column('value', width=150)
        chemical_tree.pack(fill='both', expand=True, padx=10, pady=10)
        
        chemical_data = [
            ("Stability", "Unstable - sensitive to impact, friction, heat"),
            ("Explosive Velocity", "Approx. 7,200 m/s (density 1.8)"),
            ("Impact Sensitivity", "Very high - < 1 J"),
            ("Friction Sensitivity", "Very high"),
            ("Electrostatic Sensitivity", "High"),
            ("Reactivity", "Forms sensitive salts with metals"),
            ("Decomposition", "Explosive decomposition when heated")
        ]
        
        for prop, value in chemical_data:
            chemical_tree.insert('', 'end', text=prop, values=(value,))
        
        # Comparative sensitivity
        sensitivity_frame = ttk.LabelFrame(self.properties_frame, text="Comparative Sensitivity")
        sensitivity_frame.pack(fill='x', padx=10, pady=10)
        
        sensitivity_text = (
            "Potassium picrate is significantly more sensitive than many common explosives:\n\n"
            "• More sensitive than TNT (trinitrotoluene)\n"
            "• More sensitive than RDX (cyclotrimethylenetrinitramine)\n"
            "• More sensitive than PETN (pentaerythritol tetranitrate)\n"
            "• Approaching the sensitivity of lead azide (a primary explosive)\n\n"
            "Thermal Decomposition: Potassium picrate decomposes explosively when heated to approximately 300°C. "
            "The decomposition products include carbon monoxide, carbon dioxide, nitrogen oxides, and potassium carbonate."
        )
        
        sensitivity_label = ttk.Label(sensitivity_frame, text=sensitivity_text, wraplength=1000, justify=tk.LEFT)
        sensitivity_label.pack(padx=10, pady=10)
        
    def setup_safety_tab(self):
        # Warning label
        warning_frame = ttk.LabelFrame(self.safety_frame, text="EXTREME HAZARD")
        warning_frame.pack(fill='x', padx=10, pady=5)
        
        warning_text = (
            "Potassium picrate is one of the most sensitive explosive compounds known. "
            "It can detonate from minimal impact, friction, or temperature change. "
            "Handling requires specialized training and equipment."
        )
        warning_label = ttk.Label(warning_frame, text=warning_text, wraplength=1000, foreground='red')
        warning_label.pack(padx=10, pady=10)
        
        # Main content frame
        content_frame = ttk.Frame(self.safety_frame)
        content_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Left frame for PPE and Engineering Controls
        left_frame = ttk.Frame(content_frame)
        left_frame.pack(side='left', fill='both', expand=True, padx=(0, 5))
        
        # PPE frame
        ppe_frame = ttk.LabelFrame(left_frame, text="Personal Protective Equipment (PPE)")
        ppe_frame.pack(fill='both', expand=True, pady=(0, 10))
        
        ppe_items = [
            "Blast-resistant face shield",
            "Leather gloves with Kevlar lining",
            "Flame-resistant lab coat",
            "Hearing protection",
            "Safety shoes with metatarsal guards"
        ]
        
        for item in ppe_items:
            ttk.Label(ppe_frame, text=f"• {item}").pack(anchor='w', padx=10, pady=2)
        
        # Engineering Controls frame
        engineering_frame = ttk.LabelFrame(left_frame, text="Engineering Controls")
        engineering_frame.pack(fill='both', expand=True)
        
        engineering_items = [
            "Work behind a certified blast shield",
            "Use a fume hood with the sash lowered",
            "Anti-static flooring and work surfaces",
            "Remote handling tools",
            "Explosion-proof electrical equipment"
        ]
        
        for item in engineering_items:
            ttk.Label(engineering_frame, text=f"• {item}").pack(anchor='w', padx=10, pady=2)
        
        # Right frame for Emergency Procedures and First Aid
        right_frame = ttk.Frame(content_frame)
        right_frame.pack(side='right', fill='both', expand=True, padx=(5, 0))
        
        # Emergency Procedures frame
        emergency_frame = ttk.LabelFrame(right_frame, text="Emergency Procedures")
        emergency_frame.pack(fill='both', expand=True, pady=(0, 10))
        
        emergency_items = [
            "Establish evacuation routes and assembly points",
            "Have fire extinguishers (Class D) readily available",
            "Maintain emergency shower and eye wash stations",
            "Establish communication protocols",
            "Train all personnel on emergency response"
        ]
        
        for item in emergency_items:
            ttk.Label(emergency_frame, text=f"• {item}").pack(anchor='w', padx=10, pady=2)
        
        # First Aid frame
        first_aid_frame = ttk.LabelFrame(right_frame, text="First Aid Measures")
        first_aid_frame.pack(fill='both', expand=True)
        
        first_aid_items = [
            ("Inhalation", "Move to fresh air, seek medical attention"),
            ("Skin contact", "Wash with soap and water, remove contaminated clothing"),
            ("Eye contact", "Flush with water for 15 minutes, seek medical attention"),
            ("Ingestion", "Do not induce vomiting, seek immediate medical attention")
        ]
        
        for injury, treatment in first_aid_items:
            frame = ttk.Frame(first_aid_frame)
            frame.pack(fill='x', padx=10, pady=2)
            ttk.Label(frame, text=f"{injury}:", font=('TkDefaultFont', 9, 'bold')).pack(side='left')
            ttk.Label(frame, text=treatment).pack(side='left', padx=(5, 0))
        
        # Spill and Fire Procedures
        procedures_frame = ttk.LabelFrame(self.safety_frame, text="Spill and Fire Procedures")
        procedures_frame.pack(fill='x', padx=10, pady=10)
        
        spill_text = (
            "Spill and Leak Procedures:\n"
            "1. Evacuate the area immediately\n"
            "2. Restrict access to trained personnel only\n"
            "3. Use remote tools to contain the spill if possible\n"
            "4. Keep the spilled material wet at all times\n"
            "5. Contact explosive disposal experts for cleanup\n"
            "6. Never use metal tools or containers for cleanup\n\n"
            "Fire Fighting Measures:\n"
            "• Evacuate immediately if potassium picrate is involved in fire\n"
            "• Do not attempt to fight the fire - the compound may explode\n"
            "• Use water from a safe distance to keep surrounding areas cool\n"
            "• Class D fire extinguishers may be used by trained personnel"
        )
        
        procedures_label = ttk.Label(procedures_frame, text=spill_text, justify=tk.LEFT)
        procedures_label.pack(padx=10, pady=10)
        
    def calculate(self):
        # Get input values
        target_amount = self.input_vars['target_amount'].get()
        k2co3_purity = self.input_vars['k2co3_purity'].get() / 100
        picric_purity = self.input_vars['picric_purity'].get() / 100
        reaction_temp = self.input_vars['reaction_temp'].get()
        water_ratio = self.input_vars['water_ratio'].get()
        
        # Validate input
        if target_amount <= 0:
            return
        
        # Calculate stoichiometry
        # 2C6H3N3O7 + K2CO3 → 2C6H2KN3O7 + CO2 + H2O
        moles_potassium_picrate = target_amount / self.MW_POTASSIUM_PICRATE
        
        # Calculate required picric acid (with 5% excess)
        moles_picric_acid = moles_potassium_picrate * 1.05  # 5% excess
        picric_acid_required = moles_picric_acid * self.MW_PICRIC_ACID / picric_purity
        
        # Calculate required K2CO3 (with 5% excess)
        moles_k2co3 = moles_potassium_picrate / 2 * 1.05  # 5% excess
        k2co3_required = moles_k2co3 * self.MW_K2CO3 / k2co3_purity
        
        # Calculate water required
        water_required = picric_acid_required * water_ratio
        
        # Calculate theoretical yield
        theoretical_yield = target_amount
        
        # Calculate actual yield based on temperature and purity
        yield_percentage = min(85, 90 - (100 - reaction_temp))
        actual_yield = theoretical_yield * yield_percentage / 100
        
        # Determine limiting reagent
        limiting_reagent = "Potassium Carbonate" if (
            k2co3_required / (self.MW_K2CO3 / k2co3_purity) < 
            picric_acid_required / (self.MW_PICRIC_ACID / picric_purity)
        ) else "Picric Acid"
        
        # Update materials table
        for item in self.materials_tree.get_children():
            self.materials_tree.delete(item)
            
        self.materials_tree.insert('', 'end', text='Potassium Carbonate (K₂CO₃)', 
                                  values=(f"{k2co3_required:.2f} g",))
        self.materials_tree.insert('', 'end', text='Picric Acid', 
                                  values=(f"{picric_acid_required:.2f} g",))
        self.materials_tree.insert('', 'end', text='Water', 
                                  values=(f"{water_required:.2f} ml",))
        
        # Update reaction information table
        for item in self.reaction_tree.get_children():
            self.reaction_tree.delete(item)
            
        self.reaction_tree.insert('', 'end', text='Theoretical Yield', 
                                 values=(f"{theoretical_yield:.2f} g",))
        self.reaction_tree.insert('', 'end', text='Expected Actual Yield', 
                                 values=(f"{actual_yield:.2f} g",))
        self.reaction_tree.insert('', 'end', text='Yield Percentage', 
                                 values=(f"{yield_percentage:.1f}%",))
        self.reaction_tree.insert('', 'end', text='Limiting Reagent', 
                                 values=(limiting_reagent,))
        
        # Generate and display procedure
        self.generate_procedure(target_amount, k2co3_required, picric_acid_required, 
                               water_required, reaction_temp, actual_yield, 
                               yield_percentage, limiting_reagent)
        
    def generate_procedure(self, target_amount, k2co3, picric, water, temp, 
                          actual_yield, yield_percentage, limiting_reagent):
        procedure = f"""POTASSIUM PICRATE MANUFACTURING PROCEDURE

Materials:
- Potassium carbonate: {k2co3:.1f} g
- Picric acid: {picric:.1f} g
- Distilled water: {water:.1f} ml
- Heating equipment (temperature-controlled)
- Crystallization dish
- Filter paper and funnel
- Drying trays

Step-by-Step Procedure:
1. Dissolve {k2co3:.1f} g of potassium carbonate in {water:.1f} ml of distilled water in a heat-resistant glass container.

2. Warm the solution to {temp}°C, maintaining temperature with constant stirring.

3. Slowly add {picric:.1f} g of picric acid in small portions (1-2 g at a time). 
   CAUTION: Addition will cause effervescence (CO2 release). Add slowly to avoid excessive foaming.

4. Continue adding picric acid until no more dissolves or effervescence stops.

5. Allow the solution to cool slowly to room temperature, then further cool in an ice bath to maximize crystallization.

6. Collect the yellow crystals by filtration using a Büchner funnel or filter paper.

7. Wash crystals with a small amount of ice-cold water to remove impurities.

8. Dry the crystals by exposure to air in a well-ventilated area away from direct sunlight.

9. For safety, store quantities larger than 5 grams under water in a sealed container.

Yield Information:
- Theoretical yield: {target_amount:.1f} g
- Expected actual yield: {actual_yield:.1f} g ({yield_percentage:.1f}%)
- Limiting reagent: {limiting_reagent}

SAFETY PRECAUTIONS:
- Work in a fume hood with proper ventilation
- Wear appropriate PPE: safety goggles, face shield, gloves, and lab coat
- Keep emergency water source nearby
- Avoid friction, impact, and heat sources
- Store final product under water"""
        
        self.procedure_text.config(state=tk.NORMAL)
        self.procedure_text.delete(1.0, tk.END)
        self.procedure_text.insert(tk.END, procedure)
        self.procedure_text.config(state=tk.DISABLED)
    
    def get_k2co3_content(self):
        return """FROM WOOD ASHES (TRADITIONAL METHOD):

1. Collect hardwood ashes (oak, beech, or maple preferred)
2. Leach ashes with water in a wooden barrel with a false bottom
3. Collect the lye solution (potassium hydroxide)
4. Evaporate the solution in iron kettles to concentrate
5. Calcinate the residue in a furnace to convert hydroxide to carbonate
6. Dissolve in water and filter to remove impurities
7. Recrystallize to purify

FROM POTASSIUM CHLORIDE (MODERN LABORATORY METHOD):

1. Electrolyze potassium chloride solution to form potassium hydroxide
2. Carbonate with carbon dioxide: 2KOH + CO₂ → K₂CO₃ + H₂O
3. Evaporate solution and crystallize
4. Dry crystals at 200°C

ALTERNATIVE METHOD FROM POTASSIUM HYDROXIDE AND CARBON DIOXIDE:

Materials:
- Potassium hydroxide (KOH)
- Carbon dioxide source (dry ice or CO₂ tank)
- Distilled water
- Crystallization dish

Procedure:
1. Dissolve KOH in distilled water to make a saturated solution
2. Bubble CO₂ gas through the solution until pH drops to 8-9
3. The reaction is: 2KOH + CO₂ → K₂CO₃ + H₂O
4. Evaporate solution to crystallize potassium carbonate
5. Collect crystals by filtration
6. Dry at 100-150°C

PURITY REQUIREMENTS FOR POTASSIUM PICRATE:
- Minimum purity: 95%
- Should be free of chloride ions
- Should be anhydrous"""
    
    def get_picric_content(self):
        return """FROM PHENOL (LABORATORY METHOD):

Materials:
- Phenol
- Concentrated sulfuric acid
- Concentrated nitric acid
- Ice bath
- Glassware with cooling

Procedure:
1. Sulfonation: 
   - Add 10g phenol to 50ml concentrated sulfuric acid
   - Heat at 100°C for 2 hours with stirring
   - Cool to room temperature

2. Nitration:
   - Slowly add 50ml concentrated nitric acid while keeping temperature below 50°C
   - After addition, heat to 100°C for 30 minutes
   - Pour reaction mixture onto crushed ice
   - Collect yellow precipitate by filtration

3. Purification:
   - Recrystallize from ethanol/water mixture
   - Dry in a desiccator

SAFETY NOTES:
- Picric acid is explosive when dry
- Store wet (with at least 10% water content)
- Avoid contact with metals (forms sensitive metal picrates)
- Work with small quantities (<50g)

ALTERNATIVE FROM ASPIRIN:
1. Hydrolyze aspirin to salicylic acid
2. Convert to phenol via decarboxylation
3. Proceed with sulfonation and nitration as above

STORAGE:
- Keep under water in plastic containers
- Label clearly as explosive
- Store away from heat and metals"""
    
    def get_tnt_content(self):
        return """TRINITROTOLUENE (TNT) PRODUCTION

Materials:
- Toluene
- Concentrated nitric acid
- Concentrated sulfuric acid
- Ice bath
- Separatory funnel

Procedure:
1. First nitration (mononitrotoluene):
   - Mix 50ml concentrated sulfuric acid and 50ml concentrated nitric acid
   - Slowly add 25ml toluene with cooling (keep below 30°C)
   - Stir for 2 hours at room temperature
   - Separate the organic layer

2. Second nitration (dinitrotoluene):
   - Mix 50ml concentrated sulfuric acid and 50ml concentrated nitric acid
   - Add mononitrotoluene slowly with cooling
   - Heat to 60°C for 1 hour
   - Pour onto ice, filter precipitate

3. Third nitration (trinitrotoluene):
   - Mix 50ml oleum (20% SO₃) and 50ml concentrated nitric acid
   - Add dinitrotoluene slowly with cooling
   - Heat to 100°C for 2 hours
   - Pour onto ice, filter yellow precipitate

4. Purification:
   - Recrystallize from ethanol
   - Wash with sodium bicarbonate solution to remove acidic impurities

Properties:
- Melting point: 80°C
- Detonation velocity: 6,900 m/s
- Sensitivity: Relatively insensitive to shock and friction

Storage:
- Store in cool, dry place
- Compatible with metals (unlike picric acid)
- Stable long-term storage"""

if __name__ == "__main__":
    root = tk.Tk()
    app = PotassiumPicrateCalculator(root)
    root.mainloop()