# -*- coding: utf-8 -*-
"""
Created on Wed Aug 20 13:17:28 2025

@author: samng
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import pandas as pd
from datetime import datetime
import csv
import re
from sympy import Matrix, lcm
import math

# Configure matplotlib to use Tkinter backend
plt.rcParams['font.family'] = 'Times New Roman'

class ChemistryToolkit:
    def __init__(self, root):
        self.root = root
        self.root.title("Chemistry Toolkit")
        self.root.geometry("1200x800")
        
        # Set Times New Roman font
        self.custom_font = ("Times New Roman", 10)
        self.title_font = ("Times New Roman", 14, "bold")
        self.heading_font = ("Times New Roman", 12, "bold")
        
        # Configure style
        self.style = ttk.Style()
        self.style.configure('TNotebook', font=self.custom_font)
        self.style.configure('TFrame', font=self.custom_font)
        self.style.configure('TLabel', font=self.custom_font)
        self.style.configure('TButton', font=self.custom_font)
        self.style.configure('TEntry', font=self.custom_font)
        
        # Create tabs
        self.notebook = ttk.Notebook(root)
        
        # Create frames for each tab
        self.periodic_table_frame = ttk.Frame(self.notebook, padding="10")
        self.reaction_frame = ttk.Frame(self.notebook, padding="10")
        self.gas_laws_frame = ttk.Frame(self.notebook, padding="10")
        self.measurements_frame = ttk.Frame(self.notebook, padding="10")
        self.terminology_frame = ttk.Frame(self.notebook, padding="10")
        self.about_frame = ttk.Frame(self.notebook, padding="10")
        
        # Add tabs to notebook
        self.notebook.add(self.periodic_table_frame, text="Periodic Table")
        self.notebook.add(self.reaction_frame, text="Reaction Analysis")
        self.notebook.add(self.gas_laws_frame, text="Gas Laws")
        self.notebook.add(self.measurements_frame, text="Measurements")
        self.notebook.add(self.terminology_frame, text="Terminologies")
        self.notebook.add(self.about_frame, text="About")
        
        self.notebook.pack(expand=1, fill="both")
        
        # Initialize components
        self.setup_periodic_table_tab()
        self.setup_reaction_tab()
        self.setup_gas_laws_tab()
        self.setup_measurements_tab()
        self.setup_terminology_tab()
        self.setup_about_tab()
        
        # Initialize data
        self.periodic_table = self.load_periodic_table()
        self.measurements = []
    
    def load_periodic_table(self):
        """Load periodic table data"""
        return {
            "H": {"name": "Hydrogen", "atomic_number": 1, "atomic_weight": 1.008, "group": 1, "period": 1, "category": "nonmetal", "state": "gas"},
            "He": {"name": "Helium", "atomic_number": 2, "atomic_weight": 4.0026, "group": 18, "period": 1, "category": "noble gas", "state": "gas"},
            "Li": {"name": "Lithium", "atomic_number": 3, "atomic_weight": 6.94, "group": 1, "period": 2, "category": "alkali metal", "state": "solid"},
            "Be": {"name": "Beryllium", "atomic_number": 4, "atomic_weight": 9.0122, "group": 2, "period": 2, "category": "alkaline earth metal", "state": "solid"},
            "B": {"name": "Boron", "atomic_number": 5, "atomic_weight": 10.81, "group": 13, "period": 2, "category": "metalloid", "state": "solid"},
            "C": {"name": "Carbon", "atomic_number": 6, "atomic_weight": 12.011, "group": 14, "period": 2, "category": "nonmetal", "state": "solid"},
            "N": {"name": "Nitrogen", "atomic_number": 7, "atomic_weight": 14.007, "group": 15, "period": 2, "category": "nonmetal", "state": "gas"},
            "O": {"name": "Oxygen", "atomic_number": 8, "atomic_weight": 15.999, "group": 16, "period": 2, "category": "nonmetal", "state": "gas"},
            "F": {"name": "Fluorine", "atomic_number": 9, "atomic_weight": 18.998, "group": 17, "period": 2, "category": "halogen", "state": "gas"},
            "Ne": {"name": "Neon", "atomic_number": 10, "atomic_weight": 20.180, "group": 18, "period": 2, "category": "noble gas", "state": "gas"},
            "Na": {"name": "Sodium", "atomic_number": 11, "atomic_weight": 22.990, "group": 1, "period": 3, "category": "alkali metal", "state": "solid"},
            "Mg": {"name": "Magnesium", "atomic_number": 12, "atomic_weight": 24.305, "group": 2, "period": 3, "category": "alkaline earth metal", "state": "solid"},
            "Al": {"name": "Aluminum", "atomic_number": 13, "atomic_weight": 26.982, "group": 13, "period": 3, "category": "post-transition metal", "state": "solid"},
            "Si": {"name": "Silicon", "atomic_number": 14, "atomic_weight": 28.085, "group": 14, "period": 3, "category": "metalloid", "state": "solid"},
            "P": {"name": "Phosphorus", "atomic_number": 15, "atomic_weight": 30.974, "group": 15, "period": 3, "category": "nonmetal", "state": "solid"},
            "S": {"name": "Sulfur", "atomic_number": 16, "atomic_weight": 32.06, "group": 16, "period": 3, "category": "nonmetal", "state": "solid"},
            "Cl": {"name": "Chlorine", "atomic_number": 17, "atomic_weight": 35.45, "group": 17, "period": 3, "category": "halogen", "state": "gas"},
            "Ar": {"name": "Argon", "atomic_number": 18, "atomic_weight": 39.948, "group": 18, "period": 3, "category": "noble gas", "state": "gas"},
            "K": {"name": "Potassium", "atomic_number": 19, "atomic_weight": 39.098, "group": 1, "period": 4, "category": "alkali metal", "state": "solid"},
            "Ca": {"name": "Calcium", "atomic_number": 20, "atomic_weight": 40.078, "group": 2, "period": 4, "category": "alkaline earth metal", "state": "solid"},
        }
    
    def setup_periodic_table_tab(self):
        """Set up the periodic table tab"""
        # Search frame
        search_frame = ttk.Frame(self.periodic_table_frame)
        search_frame.pack(fill="x", pady=5)
        
        ttk.Label(search_frame, text="Search Element:", font=self.custom_font).pack(side="left", padx=5)
        self.search_entry = ttk.Entry(search_frame, width=20, font=self.custom_font)
        self.search_entry.pack(side="left", padx=5)
        
        search_btn = ttk.Button(search_frame, text="Search", command=self.search_element)
        search_btn.pack(side="left", padx=5)
        
        show_all_btn = ttk.Button(search_frame, text="Show All", command=self.show_all_elements)
        show_all_btn.pack(side="left", padx=5)
        
        # Results table
        columns = ("Symbol", "Name", "Atomic Number", "Atomic Weight", "Group", "Period", "Category", "State")
        self.pt_table = ttk.Treeview(self.periodic_table_frame, columns=columns, show="headings", height=15)
        
        for col in columns:
            self.pt_table.heading(col, text=col)
            self.pt_table.column(col, width=100)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(self.periodic_table_frame, orient="vertical", command=self.pt_table.yview)
        self.pt_table.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.pt_table.pack(fill="both", expand=True, pady=5)
        
        # Populate with all elements initially
        self.show_all_elements()
    
    def search_element(self):
        """Search for an element in the periodic table"""
        query = self.search_entry.get().strip().capitalize()
        if not query:
            self.show_all_elements()
            return
        
        # Clear table
        for item in self.pt_table.get_children():
            self.pt_table.delete(item)
        
        # Search for matching elements
        for symbol, data in self.periodic_table.items():
            if query.lower() in symbol.lower() or query.lower() in data["name"].lower():
                self.pt_table.insert("", "end", values=(
                    symbol, data["name"], data["atomic_number"], 
                    data["atomic_weight"], data["group"], data["period"], 
                    data["category"], data["state"]
                ))
    
    def show_all_elements(self):
        """Display all elements in the periodic table"""
        # Clear table
        for item in self.pt_table.get_children():
            self.pt_table.delete(item)
        
        # Add all elements
        for symbol, data in self.periodic_table.items():
            self.pt_table.insert("", "end", values=(
                symbol, data["name"], data["atomic_number"], 
                data["atomic_weight"], data["group"], data["period"], 
                data["category"], data["state"]
            ))
    
    def setup_reaction_tab(self):
        """Set up the reaction analysis tab"""
        # Main frames
        input_frame = ttk.Frame(self.reaction_frame)
        input_frame.pack(fill="x", pady=5)
        
        results_frame = ttk.Frame(self.reaction_frame)
        results_frame.pack(fill="both", expand=True, pady=5)
        
        # Reaction name
        name_frame = ttk.Frame(input_frame)
        name_frame.pack(fill="x", pady=5)
        
        ttk.Label(name_frame, text="Reaction Name:", font=self.custom_font).pack(side="left", padx=5)
        self.reaction_name = ttk.Entry(name_frame, width=30, font=self.custom_font)
        self.reaction_name.pack(side="left", padx=5)
        
        # Reactants and products frames
        reactants_frame = ttk.LabelFrame(input_frame, text="Reactants", padding="5")
        reactants_frame.pack(side="left", fill="both", expand=True, padx=5)
        
        products_frame = ttk.LabelFrame(input_frame, text="Products", padding="5")
        products_frame.pack(side="right", fill="both", expand=True, padx=5)
        
        # Reactants inputs
        ttk.Label(reactants_frame, text="Formula", font=self.heading_font).grid(row=0, column=0, padx=5)
        ttk.Label(reactants_frame, text="Coefficient", font=self.heading_font).grid(row=0, column=1, padx=5)
        
        self.reactant_entries = []
        for i in range(3):
            formula_entry = ttk.Entry(reactants_frame, width=15, font=self.custom_font)
            formula_entry.grid(row=i+1, column=0, padx=5, pady=2)
            
            coeff_entry = ttk.Entry(reactants_frame, width=5, font=self.custom_font)
            coeff_entry.insert(0, "1")
            coeff_entry.grid(row=i+1, column=1, padx=5, pady=2)
            
            self.reactant_entries.append((formula_entry, coeff_entry))
        
        # Products inputs
        ttk.Label(products_frame, text="Formula", font=self.heading_font).grid(row=0, column=0, padx=5)
        ttk.Label(products_frame, text="Coefficient", font=self.heading_font).grid(row=0, column=1, padx=5)
        
        self.product_entries = []
        for i in range(2):
            formula_entry = ttk.Entry(products_frame, width=15, font=self.custom_font)
            formula_entry.grid(row=i+1, column=0, padx=5, pady=2)
            
            coeff_entry = ttk.Entry(products_frame, width=5, font=self.custom_font)
            coeff_entry.insert(0, "1")
            coeff_entry.grid(row=i+1, column=1, padx=5, pady=2)
            
            self.product_entries.append((formula_entry, coeff_entry))
        
        # Buttons
        button_frame = ttk.Frame(input_frame)
        button_frame.pack(fill="x", pady=10)
        
        create_btn = ttk.Button(button_frame, text="Create Reaction", command=self.create_reaction)
        create_btn.pack(side="left", padx=5)
        
        balance_btn = ttk.Button(button_frame, text="Balance Equation", command=self.balance_equation)
        balance_btn.pack(side="left", padx=5)
        
        # Results display
        ttk.Label(results_frame, text="Balanced Equation:", font=self.heading_font).pack(anchor="w")
        self.equation_display = scrolledtext.ScrolledText(results_frame, height=3, font=self.custom_font)
        self.equation_display.pack(fill="x", pady=5)
        
        # Stoichiometry section
        stoichiometry_frame = ttk.LabelFrame(results_frame, text="Stoichiometry Calculator", padding="5")
        stoichiometry_frame.pack(fill="both", expand=True, pady=5)
        
        # Quantity inputs
        quantity_inputs = ttk.Frame(stoichiometry_frame)
        quantity_inputs.pack(fill="x", pady=5)
        
        ttk.Label(quantity_inputs, text="Species", font=self.heading_font).grid(row=0, column=0, padx=5)
        ttk.Label(quantity_inputs, text="Amount", font=self.heading_font).grid(row=0, column=1, padx=5)
        ttk.Label(quantity_inputs, text="Unit", font=self.heading_font).grid(row=0, column=2, padx=5)
        
        self.quantity_entries = []
        for i in range(2):
            species_entry = ttk.Entry(quantity_inputs, width=15, font=self.custom_font)
            species_entry.grid(row=i+1, column=0, padx=5, pady=2)
            
            amount_entry = ttk.Entry(quantity_inputs, width=10, font=self.custom_font)
            amount_entry.grid(row=i+1, column=1, padx=5, pady=2)
            
            unit_combo = ttk.Combobox(quantity_inputs, width=5, values=["g", "mol"], state="readonly", font=self.custom_font)
            unit_combo.set("g")
            unit_combo.grid(row=i+1, column=2, padx=5, pady=2)
            
            self.quantity_entries.append((species_entry, amount_entry, unit_combo))
        
        calculate_btn = ttk.Button(stoichiometry_frame, text="Calculate", command=self.calculate_stoichiometry)
        calculate_btn.pack(pady=5)
        
        ttk.Label(stoichiometry_frame, text="Results:", font=self.heading_font).pack(anchor="w")
        self.stoich_results = scrolledtext.ScrolledText(stoichiometry_frame, height=5, font=self.custom_font)
        self.stoich_results.pack(fill="both", expand=True, pady=5)
    
    def create_reaction(self):
        """Create a reaction object from the input fields"""
        try:
            reactants = {}
            for formula_entry, coeff_entry in self.reactant_entries:
                formula = formula_entry.get().strip()
                coeff = coeff_entry.get().strip()
                if formula:
                    reactants[formula] = int(coeff) if coeff else 1
            
            products = {}
            for formula_entry, coeff_entry in self.product_entries:
                formula = formula_entry.get().strip()
                coeff = coeff_entry.get().strip()
                if formula:
                    products[formula] = int(coeff) if coeff else 1
            
            if not reactants or not products:
                messagebox.showerror("Error", "Must have at least one reactant and one product")
                return
            
            name = self.reaction_name.get().strip() or "Unnamed Reaction"
            self.current_reaction = {
                "reactants": reactants,
                "products": products,
                "name": name
            }
            
            # Display the equation
            equation = self.format_equation(reactants, products)
            self.equation_display.delete(1.0, tk.END)
            self.equation_display.insert(1.0, equation)
            
            messagebox.showinfo("Success", "Reaction created successfully")
            
        except ValueError:
            messagebox.showerror("Error", "Invalid coefficient value")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create reaction: {str(e)}")
    
    def format_equation(self, reactants, products):
        """Format a chemical equation string"""
        def format_side(species):
            return " + ".join(f"{coeff if coeff != 1 else ''}{formula}" for formula, coeff in species.items())
        
        return f"{format_side(reactants)} → {format_side(products)}"
    
    def balance_equation(self):
        """Balance the chemical equation"""
        if not hasattr(self, 'current_reaction'):
            messagebox.showerror("Error", "Create a reaction first")
            return
        
        try:
            reactants = self.current_reaction["reactants"]
            products = self.current_reaction["products"]
            
            # Get all elements
            elements = set()
            for formula in list(reactants.keys()) + list(products.keys()):
                tokens = re.findall(r"([A-Z][a-z]*)(\d*)", formula)
                for sym, _ in tokens:
                    elements.add(sym)
            
            elements = sorted(elements)
            
            # Build matrix for equation balancing
            matrix = []
            for elem in elements:
                row = []
                for formula, coeff in reactants.items():
                    tokens = re.findall(r"([A-Z][a-z]*)(\d*)", formula)
                    elem_count = 0
                    for sym, count in tokens:
                        if sym == elem:
                            elem_count = int(count) if count else 1
                    row.append(-elem_count * coeff)
                
                for formula, coeff in products.items():
                    tokens = re.findall(r"([A-Z][a-z]*)(\d*)", formula)
                    elem_count = 0
                    for sym, count in tokens:
                        if sym == elem:
                            elem_count = int(count) if count else 1
                    row.append(elem_count * coeff)
                
                matrix.append(row)
            
            # Solve the system using matrix methods
            mat = Matrix(matrix)
            solution = mat.nullspace()[0]
            
            denominators = [val.q for val in solution]
            lcm_val = 1
            for d in denominators:
                lcm_val = lcm(lcm_val, d)
            
            coeffs = [x * lcm_val for x in solution]
            
            num_reactants = len(reactants)
            reactants_coeffs = coeffs[:num_reactants]
            products_coeffs = coeffs[num_reactants:]
            
            # Update coefficients
            new_reactants = {}
            for i, (formula, _) in enumerate(reactants.items()):
                new_reactants[formula] = int(reactants_coeffs[i])
            
            new_products = {}
            for i, (formula, _) in enumerate(products.items()):
                new_products[formula] = int(products_coeffs[i])
            
            # Update the reaction
            self.current_reaction["reactants"] = new_reactants
            self.current_reaction["products"] = new_products
            
            # Update the display
            equation = self.format_equation(new_reactants, new_products)
            self.equation_display.delete(1.0, tk.END)
            self.equation_display.insert(1.0, equation)
            
            # Update input fields
            for i, (formula, coeff) in enumerate(new_reactants.items()):
                if i < len(self.reactant_entries):
                    self.reactant_entries[i][0].delete(0, tk.END)
                    self.reactant_entries[i][0].insert(0, formula)
                    self.reactant_entries[i][1].delete(0, tk.END)
                    self.reactant_entries[i][1].insert(0, str(coeff))
            
            for i, (formula, coeff) in enumerate(new_products.items()):
                if i < len(self.product_entries):
                    self.product_entries[i][0].delete(0, tk.END)
                    self.product_entries[i][0].insert(0, formula)
                    self.product_entries[i][1].delete(0, tk.END)
                    self.product_entries[i][1].insert(0, str(coeff))
            
            messagebox.showinfo("Success", "Equation balanced successfully")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to balance equation: {str(e)}")
    
    def calculate_stoichiometry(self):
        """Perform stoichiometry calculations"""
        if not hasattr(self, 'current_reaction'):
            messagebox.showerror("Error", "Create a reaction first")
            return
        
        try:
            # Get measured quantities
            measured = {}
            units = {}
            for species_entry, amount_entry, unit_combo in self.quantity_entries:
                species = species_entry.get().strip()
                amount = amount_entry.get().strip()
                unit = unit_combo.get().strip()
                
                if species and amount:
                    measured[species] = float(amount)
                    units[species] = unit
            
            if not measured:
                messagebox.showerror("Error", "Enter at least one quantity")
                return
            
            # Calculate molar masses
            molar_masses = {}
            for formula in self.current_reaction["reactants"]:
                molar_masses[formula] = self.calculate_molar_mass(formula)
            
            # Convert to moles if necessary
            moles_avail = {}
            for species, amount in measured.items():
                if units[species] == "g":
                    moles_avail[species] = amount / molar_masses[species]
                else:  # mol
                    moles_avail[species] = amount
            
            # Find limiting reagent
            reactants = self.current_reaction["reactants"]
            ratios = {}
            for species, coeff in reactants.items():
                if species in moles_avail:
                    ratios[species] = moles_avail[species] / coeff
                else:
                    ratios[species] = 0
            
            limiting_reagent = min(ratios, key=ratios.get)
            factor = ratios[limiting_reagent]
            
            # Calculate theoretical yields
            theoretical_yields = {}
            for species, coeff in self.current_reaction["products"].items():
                theoretical_yields[species] = coeff * factor
            
            # Display results
            result_text = f"Limiting Reagent: {limiting_reagent}\n"
            result_text += f"Reaction Proceeds: {factor:.4f} times\n\n"
            result_text += "Theoretical Yields:\n"
            
            for species, moles in theoretical_yields.items():
                mass = moles * self.calculate_molar_mass(species)
                result_text += f"- {species}: {moles:.4f} mol ({mass:.4f} g)\n"
            
            self.stoich_results.delete(1.0, tk.END)
            self.stoich_results.insert(1.0, result_text)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to calculate stoichiometry: {str(e)}")
    
    def calculate_molar_mass(self, formula):
        """Calculate molar mass of a compound"""
        mass = 0.0
        tokens = re.findall(r"([A-Z][a-z]*)(\d*)", formula)
        for sym, count in tokens:
            if sym in self.periodic_table:
                elem_mass = self.periodic_table[sym]["atomic_weight"]
                multiplier = int(count) if count else 1
                mass += elem_mass * multiplier
        return mass
    
    def setup_gas_laws_tab(self):
        """Set up the gas laws tab"""
        # Law selection
        law_frame = ttk.Frame(self.gas_laws_frame)
        law_frame.pack(fill="x", pady=5)
        
        ttk.Label(law_frame, text="Select Gas Law:", font=self.custom_font).pack(side="left", padx=5)
        self.gas_law_var = tk.StringVar()
        gas_laws = ["Boyle's Law", "Charles's Law", "Gay-Lussac's Law", "Combined Gas Law", "Ideal Gas Law"]
        law_combo = ttk.Combobox(law_frame, textvariable=self.gas_law_var, values=gas_laws, state="readonly", font=self.custom_font)
        law_combo.set("Boyle's Law")
        law_combo.pack(side="left", padx=5)
        law_combo.bind("<<ComboboxSelected>>", self.update_gas_law_inputs)
        
        # Input frame
        self.input_frame = ttk.Frame(self.gas_laws_frame)
        self.input_frame.pack(fill="x", pady=5)
        
        # Result display
        self.gas_result = scrolledtext.ScrolledText(self.gas_laws_frame, height=5, font=self.custom_font)
        self.gas_result.pack(fill="both", expand=True, pady=5)
        
        # Calculate button
        calculate_btn = ttk.Button(self.gas_laws_frame, text="Calculate", command=self.calculate_gas_law)
        calculate_btn.pack(pady=5)
        
        # Initialize inputs
        self.update_gas_law_inputs()
    
    def update_gas_law_inputs(self, event=None):
        """Update input fields based on selected gas law"""
        # Clear existing widgets
        for widget in self.input_frame.winfo_children():
            widget.destroy()
        
        law = self.gas_law_var.get()
        
        if law == "Boyle's Law":
            ttk.Label(self.input_frame, text="P₁ (initial pressure, atm):", font=self.custom_font).grid(row=0, column=0, padx=5, pady=2, sticky="w")
            self.p1_entry = ttk.Entry(self.input_frame, width=10, font=self.custom_font)
            self.p1_entry.grid(row=0, column=1, padx=5, pady=2)
            
            ttk.Label(self.input_frame, text="V₁ (initial volume, L):", font=self.custom_font).grid(row=1, column=0, padx=5, pady=2, sticky="w")
            self.v1_entry = ttk.Entry(self.input_frame, width=10, font=self.custom_font)
            self.v1_entry.grid(row=1, column=1, padx=5, pady=2)
            
            ttk.Label(self.input_frame, text="Find:", font=self.custom_font).grid(row=2, column=0, padx=5, pady=2, sticky="w")
            self.find_var = tk.StringVar(value="P₂")
            find_combo = ttk.Combobox(self.input_frame, textvariable=self.find_var, values=["P₂", "V₂"], state="readonly", width=5, font=self.custom_font)
            find_combo.grid(row=2, column=1, padx=5, pady=2)
            
            ttk.Label(self.input_frame, text="Value:", font=self.custom_font).grid(row=3, column=0, padx=5, pady=2, sticky="w")
            self.value_entry = ttk.Entry(self.input_frame, width=10, font=self.custom_font)
            self.value_entry.grid(row=3, column=1, padx=5, pady=2)
        
        elif law == "Charles's Law":
            ttk.Label(self.input_frame, text="V₁ (initial volume, L):", font=self.custom_font).grid(row=0, column=0, padx=5, pady=2, sticky="w")
            self.v1_entry = ttk.Entry(self.input_frame, width=10, font=self.custom_font)
            self.v1_entry.grid(row=0, column=1, padx=5, pady=2)
            
            ttk.Label(self.input_frame, text="T₁ (initial temperature, K):", font=self.custom_font).grid(row=1, column=0, padx=5, pady=2, sticky="w")
            self.t1_entry = ttk.Entry(self.input_frame, width=10, font=self.custom_font)
            self.t1_entry.grid(row=1, column=1, padx=5, pady=2)
            
            ttk.Label(self.input_frame, text="Find:", font=self.custom_font).grid(row=2, column=0, padx=5, pady=2, sticky="w")
            self.find_var = tk.StringVar(value="V₂")
            find_combo = ttk.Combobox(self.input_frame, textvariable=self.find_var, values=["V₂", "T₂"], state="readonly", width=5, font=self.custom_font)
            find_combo.grid(row=2, column=1, padx=5, pady=2)
            
            ttk.Label(self.input_frame, text="Value:", font=self.custom_font).grid(row=3, column=0, padx=5, pady=2, sticky="w")
            self.value_entry = ttk.Entry(self.input_frame, width=10, font=self.custom_font)
            self.value_entry.grid(row=3, column=1, padx=5, pady=2)
        
        elif law == "Gay-Lussac's Law":
            ttk.Label(self.input_frame, text="P₁ (initial pressure, atm):", font=self.custom_font).grid(row=0, column=0, padx=5, pady=2, sticky="w")
            self.p1_entry = ttk.Entry(self.input_frame, width=10, font=self.custom_font)
            self.p1_entry.grid(row=0, column=1, padx=5, pady=2)
            
            ttk.Label(self.input_frame, text="T₁ (initial temperature, K):", font=self.custom_font).grid(row=1, column=0, padx=5, pady=2, sticky="w")
            self.t1_entry = ttk.Entry(self.input_frame, width=10, font=self.custom_font)
            self.t1_entry.grid(row=1, column=1, padx=5, pady=2)
            
            ttk.Label(self.input_frame, text="Find:", font=self.custom_font).grid(row=2, column=0, padx=5, pady=2, sticky="w")
            self.find_var = tk.StringVar(value="P₂")
            find_combo = ttk.Combobox(self.input_frame, textvariable=self.find_var, values=["P₂", "T₂"], state="readonly", width=5, font=self.custom_font)
            find_combo.grid(row=2, column=1, padx=5, pady=2)
            
            ttk.Label(self.input_frame, text="Value:", font=self.custom_font).grid(row=3, column=0, padx=5, pady=2, sticky="w")
            self.value_entry = ttk.Entry(self.input_frame, width=10, font=self.custom_font)
            self.value_entry.grid(row=3, column=1, padx=5, pady=2)
        
        elif law == "Combined Gas Law":
            ttk.Label(self.input_frame, text="P₁ (initial pressure, atm):", font=self.custom_font).grid(row=0, column=0, padx=5, pady=2, sticky="w")
            self.p1_entry = ttk.Entry(self.input_frame, width=10, font=self.custom_font)
            self.p1_entry.grid(row=0, column=1, padx=5, pady=2)
            
            ttk.Label(self.input_frame, text="V₁ (initial volume, L):", font=self.custom_font).grid(row=1, column=0, padx=5, pady=2, sticky="w")
            self.v1_entry = ttk.Entry(self.input_frame, width=10, font=self.custom_font)
            self.v1_entry.grid(row=1, column=1, padx=5, pady=2)
            
            ttk.Label(self.input_frame, text="T₁ (initial temperature, K):", font=self.custom_font).grid(row=2, column=0, padx=5, pady=2, sticky="w")
            self.t1_entry = ttk.Entry(self.input_frame, width=10, font=self.custom_font)
            self.t1_entry.grid(row=2, column=1, padx=5, pady=2)
            
            ttk.Label(self.input_frame, text="Find:", font=self.custom_font).grid(row=3, column=0, padx=5, pady=2, sticky="w")
            self.find_var = tk.StringVar(value="P₂")
            find_combo = ttk.Combobox(self.input_frame, textvariable=self.find_var, values=["P₂", "V₂", "T₂"], state="readonly", width=5, font=self.custom_font)
            find_combo.grid(row=3, column=1, padx=5, pady=2)
            
            ttk.Label(self.input_frame, text="Value 1:", font=self.custom_font).grid(row=4, column=0, padx=5, pady=2, sticky="w")
            self.value1_entry = ttk.Entry(self.input_frame, width=10, font=self.custom_font)
            self.value1_entry.grid(row=4, column=1, padx=5, pady=2)
            
            ttk.Label(self.input_frame, text="Value 2:", font=self.custom_font).grid(row=5, column=0, padx=5, pady=2, sticky="w")
            self.value2_entry = ttk.Entry(self.input_frame, width=10, font=self.custom_font)
            self.value2_entry.grid(row=5, column=1, padx=5, pady=2)
        
        elif law == "Ideal Gas Law":
            ttk.Label(self.input_frame, text="Find:", font=self.custom_font).grid(row=0, column=0, padx=5, pady=2, sticky="w")
            self.find_var = tk.StringVar(value="P")
            find_combo = ttk.Combobox(self.input_frame, textvariable=self.find_var, values=["P", "V", "n", "T"], state="readonly", width=5, font=self.custom_font)
            find_combo.grid(row=0, column=1, padx=5, pady=2)
            
            ttk.Label(self.input_frame, text="P (pressure, atm):", font=self.custom_font).grid(row=1, column=0, padx=5, pady=2, sticky="w")
            self.p_entry = ttk.Entry(self.input_frame, width=10, font=self.custom_font)
            self.p_entry.grid(row=1, column=1, padx=5, pady=2)
            
            ttk.Label(self.input_frame, text="V (volume, L):", font=self.custom_font).grid(row=2, column=0, padx=5, pady=2, sticky="w")
            self.v_entry = ttk.Entry(self.input_frame, width=10, font=self.custom_font)
            self.v_entry.grid(row=2, column=1, padx=5, pady=2)
            
            ttk.Label(self.input_frame, text="n (moles, mol):", font=self.custom_font).grid(row=3, column=0, padx=5, pady=2, sticky="w")
            self.n_entry = ttk.Entry(self.input_frame, width=10, font=self.custom_font)
            self.n_entry.grid(row=3, column=1, padx=5, pady=2)
            
            ttk.Label(self.input_frame, text="T (temperature, K):", font=self.custom_font).grid(row=4, column=0, padx=5, pady=2, sticky="w")
            self.t_entry = ttk.Entry(self.input_frame, width=10, font=self.custom_font)
            self.t_entry.grid(row=4, column=1, padx=5, pady=2)
    
    def calculate_gas_law(self):
        """Calculate the selected gas law"""
        law = self.gas_law_var.get()
        result_text = ""
        
        try:
            if law == "Boyle's Law":
                p1 = float(self.p1_entry.get())
                v1 = float(self.v1_entry.get())
                value = float(self.value_entry.get())
                
                if self.find_var.get() == "P₂":
                    v2 = value
                    p2 = p1 * v1 / v2
                    result_text = f"P₂ = {p2:.4f} atm\n\nBoyle's Law: P₁V₁ = P₂V₂\n{p1} × {v1} = P₂ × {v2}\nP₂ = {p1} × {v1} / {v2} = {p2:.4f} atm"
                else:
                    p2 = value
                    v2 = p1 * v1 / p2
                    result_text = f"V₂ = {v2:.4f} L\n\nBoyle's Law: P₁V₁ = P₂V₂\n{p1} × {v1} = {p2} × V₂\nV₂ = {p1} × {v1} / {p2} = {v2:.4f} L"
            
            elif law == "Charles's Law":
                v1 = float(self.v1_entry.get())
                t1 = float(self.t1_entry.get())
                value = float(self.value_entry.get())
                
                if self.find_var.get() == "V₂":
                    t2 = value
                    v2 = v1 * t2 / t1
                    result_text = f"V₂ = {v2:.4f} L\n\nCharles's Law: V₁/T₁ = V₂/T₂\n{v1}/{t1} = V₂/{t2}\nV₂ = {v1} × {t2} / {t1} = {v2:.4f} L"
                else:
                    v2 = value
                    t2 = v2 * t1 / v1
                    result_text = f"T₂ = {t2:.4f} K\n\nCharles's Law: V₁/T₁ = V₂/T₂\n{v1}/{t1} = {v2}/T₂\nT₂ = {v2} × {t1} / {v1} = {t2:.4f} K"
            
            elif law == "Gay-Lussac's Law":
                p1 = float(self.p1_entry.get())
                t1 = float(self.t1_entry.get())
                value = float(self.value_entry.get())
                
                if self.find_var.get() == "P₂":
                    t2 = value
                    p2 = p1 * t2 / t1
                    result_text = f"P₂ = {p2:.4f} atm\n\nGay-Lussac's Law: P₁/T₁ = P₂/T₂\n{p1}/{t1} = P₂/{t2}\nP₂ = {p1} × {t2} / {t1} = {p2:.4f} atm"
                else:
                    p2 = value
                    t2 = p2 * t1 / p1
                    result_text = f"T₂ = {t2:.4f} K\n\nGay-Lussac's Law: P₁/T₁ = P₂/T₂\n{p1}/{t1} = {p2}/T₂\nT₂ = {p2} × {t1} / {p1} = {t2:.4f} K"
            
            elif law == "Combined Gas Law":
                p1 = float(self.p1_entry.get())
                v1 = float(self.v1_entry.get())
                t1 = float(self.t1_entry.get())
                value1 = float(self.value1_entry.get())
                value2 = float(self.value2_entry.get())
                
                if self.find_var.get() == "P₂":
                    v2 = value1
                    t2 = value2
                    p2 = p1 * v1 * t2 / (v2 * t1)
                    result_text = f"P₂ = {p2:.4f} atm\n\nCombined Gas Law: P₁V₁/T₁ = P₂V₂/T₂\n{p1}×{v1}/{t1} = P₂×{v2}/{t2}\nP₂ = {p1}×{v1}×{t2}/({v2}×{t1}) = {p2:.4f} atm"
                elif self.find_var.get() == "V₂":
                    p2 = value1
                    t2 = value2
                    v2 = p1 * v1 * t2 / (p2 * t1)
                    result_text = f"V₂ = {v2:.4f} L\n\nCombined Gas Law: P₁V₁/T₁ = P₂V₂/T₂\n{p1}×{v1}/{t1} = {p2}×V₂/{t2}\nV₂ = {p1}×{v1}×{t2}/({p2}×{t1}) = {v2:.4f} L"
                else:
                    p2 = value1
                    v2 = value2
                    t2 = p2 * v2 * t1 / (p1 * v1)
                    result_text = f"T₂ = {t2:.4f} K\n\nCombined Gas Law: P₁V₁/T₁ = P₂V₂/T₂\n{p1}×{v1}/{t1} = {p2}×{v2}/T₂\nT₂ = {p2}×{v2}×{t1}/({p1}×{v1}) = {t2:.4f} K"
            
            elif law == "Ideal Gas Law":
                R = 0.0821  # L·atm/(mol·K)
                
                if self.find_var.get() == "P":
                    v = float(self.v_entry.get())
                    n = float(self.n_entry.get())
                    t = float(self.t_entry.get())
                    p = n * R * t / v
                    result_text = f"P = {p:.4f} atm\n\nIdeal Gas Law: PV = nRT\nP × {v} = {n} × {R} × {t}\nP = {n} × {R} × {t} / {v} = {p:.4f} atm"
                elif self.find_var.get() == "V":
                    p = float(self.p_entry.get())
                    n = float(self.n_entry.get())
                    t = float(self.t_entry.get())
                    v = n * R * t / p
                    result_text = f"V = {v:.4f} L\n\nIdeal Gas Law: PV = nRT\n{p} × V = {n} × {R} × {t}\nV = {n} × {R} × {t} / {p} = {v:.4f} L"
                elif self.find_var.get() == "n":
                    p = float(self.p_entry.get())
                    v = float(self.v_entry.get())
                    t = float(self.t_entry.get())
                    n = p * v / (R * t)
                    result_text = f"n = {n:.4f} mol\n\nIdeal Gas Law: PV = nRT\n{p} × {v} = n × {R} × {t}\nn = {p} × {v} / ({R} × {t}) = {n:.4f} mol"
                else:
                    p = float(self.p_entry.get())
                    v = float(self.v_entry.get())
                    n = float(self.n_entry.get())
                    t = p * v / (n * R)
                    result_text = f"T = {t:.4f} K\n\nIdeal Gas Law: PV = nRT\n{p} × {v} = {n} × {R} × T\nT = {p} × {v} / ({n} × {R}) = {t:.4f} K"
            
            # Add timestamp
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            result_text = f"Calculation performed at: {timestamp}\n\n" + result_text
            
            self.gas_result.delete(1.0, tk.END)
            self.gas_result.insert(1.0, result_text)
            
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numeric values")
        except Exception as e:
            messagebox.showerror("Error", f"Calculation failed: {str(e)}")
    
    def setup_measurements_tab(self):
        """Set up the measurements tab"""
        # Input frame
        input_frame = ttk.LabelFrame(self.measurements_frame, text="Record Measurement", padding="10")
        input_frame.pack(fill="x", pady=5)
        
        # Variable name
        var_frame = ttk.Frame(input_frame)
        var_frame.pack(fill="x", pady=5)
        ttk.Label(var_frame, text="Variable:", font=self.custom_font).pack(side="left", padx=5)
        self.measure_var = ttk.Entry(var_frame, width=20, font=self.custom_font)
        self.measure_var.pack(side="left", padx=5)
        
        # Value and unit
        value_frame = ttk.Frame(input_frame)
        value_frame.pack(fill="x", pady=5)
        ttk.Label(value_frame, text="Value:", font=self.custom_font).pack(side="left", padx=5)
        self.measure_value = ttk.Entry(value_frame, width=10, font=self.custom_font)
        self.measure_value.pack(side="left", padx=5)
        
        ttk.Label(value_frame, text="Unit:", font=self.custom_font).pack(side="left", padx=5)
        self.measure_unit = ttk.Entry(value_frame, width=10, font=self.custom_font)
        self.measure_unit.pack(side="left", padx=5)
        
        # Notes
        notes_frame = ttk.Frame(input_frame)
        notes_frame.pack(fill="x", pady=5)
        ttk.Label(notes_frame, text="Notes:", font=self.custom_font).pack(side="left", padx=5)
        self.measure_notes = ttk.Entry(notes_frame, width=30, font=self.custom_font)
        self.measure_notes.pack(side="left", padx=5)
        
        # Record button
        record_btn = ttk.Button(input_frame, text="Record Measurement", command=self.record_measurement)
        record_btn.pack(pady=5)
        
        # Measurements table
        table_frame = ttk.Frame(self.measurements_frame)
        table_frame.pack(fill="both", expand=True, pady=5)
        
        columns = ("Timestamp", "Variable", "Value", "Unit", "Notes")
        self.measure_table = ttk.Treeview(table_frame, columns=columns, show="headings", height=10)
        
        for col in columns:
            self.measure_table.heading(col, text=col)
            self.measure_table.column(col, width=120)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.measure_table.yview)
        self.measure_table.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.measure_table.pack(fill="both", expand=True)
        
        # Button controls
        button_frame = ttk.Frame(self.measurements_frame)
        button_frame.pack(fill="x", pady=5)
        
        delete_btn = ttk.Button(button_frame, text="Delete Selected", command=self.delete_measurement)
        delete_btn.pack(side="left", padx=5)
        
        export_btn = ttk.Button(button_frame, text="Export to CSV", command=self.export_measurements)
        export_btn.pack(side="left", padx=5)
        
        # Plot controls
        plot_frame = ttk.Frame(self.measurements_frame)
        plot_frame.pack(fill="x", pady=5)
        
        ttk.Label(plot_frame, text="Plot Variable:", font=self.custom_font).pack(side="left", padx=5)
        self.plot_var = ttk.Combobox(plot_frame, width=15, state="readonly", font=self.custom_font)
        self.plot_var.pack(side="left", padx=5)
        
        plot_btn = ttk.Button(plot_frame, text="Plot Data", command=self.plot_measurements)
        plot_btn.pack(side="left", padx=5)
        
        # Plot area
        self.plot_frame = ttk.Frame(self.measurements_frame)
        self.plot_frame.pack(fill="both", expand=True, pady=5)
    
    def record_measurement(self):
        """Record a new measurement"""
        try:
            variable = self.measure_var.get().strip()
            value = float(self.measure_value.get())
            unit = self.measure_unit.get().strip()
            notes = self.measure_notes.get().strip()
            
            if not variable or not unit:
                messagebox.showerror("Error", "Variable and unit are required")
                return
            
            timestamp = datetime.now()
            measurement = {
                "timestamp": timestamp,
                "variable": variable,
                "value": value,
                "unit": unit,
                "notes": notes
            }
            
            self.measurements.append(measurement)
            self.update_measurements_table()
            
            # Clear inputs
            self.measure_var.delete(0, tk.END)
            self.measure_value.delete(0, tk.END)
            self.measure_unit.delete(0, tk.END)
            self.measure_notes.delete(0, tk.END)
            
            messagebox.showinfo("Success", "Measurement recorded successfully")
            
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid numeric value")
    
    def update_measurements_table(self):
        """Update the measurements table"""
        # Clear table
        for item in self.measure_table.get_children():
            self.measure_table.delete(item)
        
        # Add measurements
        for measurement in self.measurements:
            self.measure_table.insert("", "end", values=(
                measurement["timestamp"].strftime("%Y-%m-%d %H:%M:%S"),
                measurement["variable"],
                f"{measurement['value']:.4f}",
                measurement["unit"],
                measurement["notes"]
            ))
        
        # Update plot variables
        variables = sorted({m["variable"] for m in self.measurements})
        self.plot_var["values"] = variables
        if variables:
            self.plot_var.set(variables[0])
    
    def delete_measurement(self):
        """Delete selected measurement"""
        selected = self.measure_table.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a measurement to delete")
            return
        
        # Confirm deletion
        if messagebox.askyesno("Confirm", "Are you sure you want to delete the selected measurement?"):
            # Delete from highest index to lowest to avoid index issues
            for item in sorted(selected, reverse=True):
                index = self.measure_table.index(item)
                if 0 <= index < len(self.measurements):
                    del self.measurements[index]
            
            self.update_measurements_table()
    
    def export_measurements(self):
        """Export measurements to CSV file"""
        if not self.measurements:
            messagebox.showerror("Error", "No measurements to export")
            return
        
        try:
            filename = f"measurements_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            with open(filename, 'w', newline='') as csvfile:
                fieldnames = ["timestamp", "variable", "value", "unit", "notes"]
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                
                writer.writeheader()
                for measurement in self.measurements:
                    writer.writerow({
                        "timestamp": measurement["timestamp"].strftime("%Y-%m-%d %H:%M:%S"),
                        "variable": measurement["variable"],
                        "value": measurement["value"],
                        "unit": measurement["unit"],
                        "notes": measurement["notes"]
                    })
            
            messagebox.showinfo("Success", f"Measurements exported to {filename}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export measurements: {str(e)}")
    
    def plot_measurements(self):
        """Plot measurements"""
        variable = self.plot_var.get()
        if not variable:
            messagebox.showerror("Error", "Please select a variable to plot")
            return
        
        # Filter measurements for the selected variable
        data = [m for m in self.measurements if m["variable"] == variable]
        if not data:
            messagebox.showerror("Error", f"No measurements found for {variable}")
            return
        
        # Sort by timestamp
        data.sort(key=lambda x: x["timestamp"])
        
        # Extract timestamps and values
        timestamps = [m["timestamp"] for m in data]
        values = [m["value"] for m in data]
        unit = data[0]["unit"]
        
        # Clear previous plot
        for widget in self.plot_frame.winfo_children():
            widget.destroy()
        
        # Create plot
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.plot(timestamps, values, 'o-')
        ax.set_xlabel('Time')
        ax.set_ylabel(f"{variable} ({unit})")
        ax.set_title(f"Time Series of {variable}")
        ax.grid(True)
        
        # Format x-axis labels
        fig.autofmt_xdate()
        
        # Embed plot in Tkinter
        canvas = FigureCanvasTkAgg(fig, self.plot_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
    
    def setup_terminology_tab(self):
        """Set up the terminology tab"""
        # Create notebook for terminology sections
        term_notebook = ttk.Notebook(self.terminology_frame)
        term_notebook.pack(fill="both", expand=True)
        
        # Element reproduction tab
        element_frame = ttk.Frame(term_notebook, padding="10")
        term_notebook.add(element_frame, text="Element Reproduction")
        
        element_text = scrolledtext.ScrolledText(element_frame, font=self.custom_font)
        element_text.pack(fill="both", expand=True)
        
        element_content = """
        WORKFLOW TO OBTAIN OR SYNTHESIZE ALL 118 ELEMENTS

        1. Prepare Your Facility and Safety Protocols
        - Establish a multi-functional chemistry lab with fume hoods, high-vacuum pumps, 
          inert-atmosphere gloveboxes, high-temperature furnaces, electrolytic cells, 
          and fractional distillation columns.
        - Implement rigorous safety measures including PPE for acids, bases, cryogenics, 
          and radiation.

        2. Gases from the Atmosphere and Water
        - Hydrogen (H): Electrolyze deionized water with a proton-exchange membrane cell.
        - Nitrogen (N), Oxygen (O), Argon (Ar), Neon (Ne), Krypton (Kr), Xenon (Xe): 
          Fractional distillation of liquefied air.
        - Helium (He): Commercially from natural gas wells via low-temperature separation.

        3. Alkali, Alkaline-Earth, and Early Transition Metals
        - Lithium (Li), Sodium (Na), Potassium (K): Brine or ore mining and molten-salt electrolysis.
        - Magnesium (Mg), Calcium (Ca), Strontium (Sr), Barium (Ba): Extract from seawater or minerals.

        4. Post-Transition Metals, Metalloids, and Nonmetals
        - Aluminum (Al), Gallium (Ga), Indium (In), Thallium (Tl): Bauxite for Al via Bayer process.
        - Boron (B), Silicon (Si), Germanium (Ge): Borates from evaporation ponds; quartz reduction for Si.

        5. Halogens and Chalcogens
        - Fluorine (F): Electrolysis of anhydrous HF/KF.
        - Chlorine (Cl): Chlor-alkali electrolysis.
        - Bromine (Br): Oxidation of bromide-rich brines.

        6. Lanthanides (57–71)
        - Monazite and bastnäsite ores from pegmatites.
        - Crystallization or solvent extraction to fractionate individual lanthanides.

        7. Actinides Up to Uranium (89–92)
        - Thorium (Th) and Uranium (U): Uraninite and thorite mining.
        - Neptunium (Np), Plutonium (Pu): Produced by neutron irradiation of U-238 in reactors.

        8. Transuranics and Superheavy Elements (93–118)
        - Heavy-ion fusion reactions in a particle accelerator.
        - Rapid chemical separation in gas-phase or liquid-phase recoil separators.

        9. Documentation and Verification
        - Characterize each isolate with mass spectrometry for isotope confirmation.
        - Record in standardized report format with procurement route and yield.
        """
        element_text.insert(1.0, element_content)
        element_text.config(state="disabled")
        
        # Atomic weight measurement tab
        atomic_frame = ttk.Frame(term_notebook, padding="10")
        term_notebook.add(atomic_frame, text="Atomic Weight Measurement")
        
        atomic_text = scrolledtext.ScrolledText(atomic_frame, font=self.custom_font)
        atomic_text.pack(fill="both", expand=True)
        
        atomic_content = """
        HOW TO MEASURE ATOMIC WEIGHT

        1. Mass Spectrometry Method
        - Principle: Atoms are ionized and accelerated through a magnetic field where they 
          are deflected based on their mass-to-charge ratio.
        - Procedure:
          a. Vaporize the sample
          b. Ionize the atoms using electron bombardment
          c. Accelerate ions through an electric field
          d. Separate ions based on mass-to-charge ratio in a magnetic field
          e. Detect ions and measure their relative abundances
        - Calculation: Atomic weight = Σ(isotope mass × fractional abundance)

        2. Chemical Combination Method
        - Principle: Measure the proportions in which elements combine to form compounds.
        - Example: To find atomic weight of oxygen:
          a. Form water (H₂O) from hydrogen and oxygen
          b. Measure mass of hydrogen consumed and oxygen consumed
          c. Find the ratio: mass oxygen / mass hydrogen = 8 (approximately)
          d. Since water contains 2 H atoms per O atom: atomic weight O = 16

        3. Electrolysis Method
        - Principle: Use Faraday's laws of electrolysis to determine equivalent weights.
        - Procedure:
          a. Pass known electric current through electrolyte for known time
          b. Measure mass of element deposited at electrode
          c. Calculate equivalent weight = (mass × 96500) / (current × time)
          d. Atomic weight = equivalent weight × valency

        4. Gas Density Method
        - Principle: For gaseous elements, measure density and use ideal gas law.
        - Procedure:
          a. Measure mass of known volume of gas at known T and P
          b. Calculate molar mass = (mass × R × T) / (P × V)
          c. For elements, atomic weight = molar mass

        5. X-ray Crystallography Method
        - Principle: Measure distances between atoms in crystals to calculate atomic masses.
        - Procedure:
          a. Grow single crystal of element or compound
          b. Collect X-ray diffraction data
          c. Solve crystal structure
          d. Calculate atomic masses from known relationships

        MODERN STANDARD
        - Today, atomic weights are determined by international agreement based on 
          extensive mass spectrometry data.
        - Carbon-12 is defined as exactly 12 atomic mass units.
        - Most elements have atomic weights measured to at least 4 decimal places.
        """
        atomic_text.insert(1.0, atomic_content)
        atomic_text.config(state="disabled")
        
        # Gas laws tab
        gas_laws_frame = ttk.Frame(term_notebook, padding="10")
        term_notebook.add(gas_laws_frame, text="Gas Laws")
        
        gas_laws_text = scrolledtext.ScrolledText(gas_laws_frame, font=self.custom_font)
        gas_laws_text.pack(fill="both", expand=True)
        
        gas_laws_content = """
        COMPLETE GAS LAWS WITH FORMULAS AND EXPLANATIONS

        1. Boyle's Law (1662)
        - Formula: P₁V₁ = P₂V₂ or PV = k (constant)
        - Statement: For a fixed amount of gas at constant temperature, the volume 
          is inversely proportional to the pressure.
        - Mathematical expression: V ∝ 1/P
        - Example: If pressure doubles, volume halves (at constant temperature)

        2. Charles's Law (1787)
        - Formula: V₁/T₁ = V₂/T₂ or V/T = k (constant)
        - Statement: For a fixed amount of gas at constant pressure, the volume 
          is directly proportional to the absolute temperature.
        - Mathematical expression: V ∝ T
        - Note: Temperature must be in Kelvin
        - Example: If temperature doubles, volume doubles (at constant pressure)

        3. Gay-Lussac's Law (1802)
        - Formula: P₁/T₁ = P₂/T₂ or P/T = k (constant)
        - Statement: For a fixed amount of gas at constant volume, the pressure 
          is directly proportional to the absolute temperature.
        - Mathematical expression: P ∝ T
        - Note: Temperature must be in Kelvin
        - Example: If temperature doubles, pressure doubles (at constant volume)

        4. Avogadro's Law (1811)
        - Formula: V₁/n₁ = V₂/n₂ or V/n = k (constant)
        - Statement: Equal volumes of gases at the same temperature and pressure 
          contain equal numbers of molecules.
        - Mathematical expression: V ∝ n
        - Example: If moles double, volume doubles (at constant T and P)

        5. Combined Gas Law
        - Formula: P₁V₁/T₁ = P₂V₂/T₂ or PV/T = k (constant)
        - Statement: Combines Boyle's, Charles's, and Gay-Lussac's laws
        - Used when pressure, volume, and temperature all change

        6. Ideal Gas Law
        - Formula: PV = nRT
        - Where:
          P = pressure (atm)
          V = volume (L)
          n = number of moles
          R = gas constant (0.0821 L·atm/(mol·K))
          T = temperature (K)
        - Statement: Describes the behavior of ideal gases
        - Derived from the combination of all the above laws

        7. Dalton's Law of Partial Pressures (1801)
        - Formula: P_total = P₁ + P₂ + P₃ + ...
        - Statement: The total pressure of a mixture of gases is equal to the 
          sum of the partial pressures of the individual gases.

        8. Graham's Law of Effusion (1848)
        - Formula: Rate₁/Rate₂ = √(M₂/M₁)
        - Statement: The rate of effusion of a gas is inversely proportional 
          to the square root of its molar mass.

        PRACTICAL APPLICATIONS
        - Scuba diving: Gas laws determine safe diving depths and decompression schedules
        - Weather balloons: Charles's law explains why balloons expand as they rise
        - Automotive tires: Pressure changes with temperature (Gay-Lussac's law)
        - Air conditioning: Combined gas law principles in refrigeration cycles
        """
        gas_laws_text.insert(1.0, gas_laws_content)
        gas_laws_text.config(state="disabled")
        
        # Chemical theories tab
        theories_frame = ttk.Frame(term_notebook, padding="10")
        term_notebook.add(theories_frame, text="Chemical Theories")
        
        theories_text = scrolledtext.ScrolledText(theories_frame, font=self.custom_font)
        theories_text.pack(fill="both", expand=True)
        
        theories_content = """
        KEY CHEMICAL AND ATOMIC THEORIES

        1. Dalton's Atomic Theory (1803)
        - Matter is composed of extremely small particles called atoms
        - Atoms of a given element are identical in size, mass, and other properties
        - Atoms cannot be subdivided, created, or destroyed
        - Atoms of different elements combine in simple whole-number ratios to form compounds
        - In chemical reactions, atoms are combined, separated, or rearranged

        2. Thomson's Plum Pudding Model (1897)
        - Atoms are composed of electrons embedded in a sphere of positive charge
        - Discovered the electron using cathode ray tubes
        - The model was later disproved by Rutherford's gold foil experiment

        3. Rutherford's Nuclear Model (1911)
        - Atoms have a small, dense, positively charged nucleus
        - Electrons orbit the nucleus at relatively large distances
        - Most of the atom is empty space
        - Based on the gold foil experiment where alpha particles were deflected

        4. Bohr's Model (1913)
        - Electrons orbit the nucleus in specific energy levels or shells
        - Electrons can jump between energy levels by absorbing or emitting photons
        - Each energy level has a fixed energy value
        - Successfully explained the hydrogen spectrum but failed for multi-electron atoms

        5. Quantum Mechanical Model (1926)
        - Electrons do not follow fixed orbits but exist in orbitals (probability clouds)
        - Described by wave functions and Schrödinger's equation
        - Uses quantum numbers to describe electron properties:
          * Principal quantum number (n) - energy level
          * Angular momentum quantum number (l) - orbital shape
          * Magnetic quantum number (m) - orbital orientation
          * Spin quantum number (s) - electron spin

        6. Molecular Orbital Theory
        - Atomic orbitals combine to form molecular orbitals that extend over the entire molecule
        - Electrons are delocalized over the whole molecule
        - Better explains magnetic properties and bond energies than valence bond theory

        7. Valence Bond Theory
        - Chemical bonds form when atomic orbitals overlap
        - Bonds are localized between two atoms
        - Explains molecular geometry through hybridization

        8. VSEPR Theory (Valence Shell Electron Pair Repulsion)
        - Electron pairs around a central atom arrange themselves to minimize repulsion
        - Predicts molecular shapes based on the number of bonding and lone pairs

        9. Kinetic Molecular Theory of Gases
        - Gases consist of large numbers of tiny particles that are far apart
        - Collisions between gas particles and container walls are elastic
        - Gas particles are in continuous, random motion
        - There are no forces of attraction or repulsion between gas particles
        - The average kinetic energy of gas particles depends on the temperature
        """
        theories_text.insert(1.0, theories_content)
        theories_text.config(state="disabled")
    
    def setup_about_tab(self):
        """Set up the about tab"""
        about_text = f"""
        CHEMISTRY TOOLKIT APPLICATION
        
        A comprehensive software tool for chemical calculations, reference, and education.
        
        FEATURES:
        - Periodic table reference with detailed element information
        - Chemical reaction balancing and stoichiometry calculations
        - Gas law calculations with step-by-step solutions
        - Measurement recording with timestamp logging
        - Comprehensive chemical terminology and theory reference
        - Data visualization and export capabilities
        
        CONTACT INFORMATION:
        Email: Samngacha@gmail.com
        Phone: +254742859291
        
        VERSION: 1.0
        RELEASE DATE: {datetime.now().strftime('%Y-%m-%d')}
        
        This application is designed for educational and research purposes.
        Always follow proper safety protocols when working with chemicals.
        
        © 2023 Chemistry Toolkit. All rights reserved.
        """
        
        about_label = tk.Label(self.about_frame, text=about_text, font=self.custom_font, justify="left")
        about_label.pack(pady=20)
        
        # Add a separator
        separator = ttk.Separator(self.about_frame, orient="horizontal")
        separator.pack(fill="x", pady=10)
        
        # Add usage instructions
        instructions = """
        USAGE INSTRUCTIONS:
        
        1. PERIODIC TABLE TAB:
           - Search for elements by symbol or name
           - View detailed information about each element
           - Use 'Show All' to display the complete table
        
        2. REACTION ANALYSIS TAB:
           - Enter reactants and products with coefficients
           - Use 'Create Reaction' to initialize the reaction
           - Use 'Balance Equation' to automatically balance the reaction
           - Enter quantities for stoichiometry calculations
        
        3. GAS LAWS TAB:
           - Select the gas law you want to use
           - Enter known values and leave one field empty to solve for it
           - Click 'Calculate' to compute the result with detailed steps
        
        4. MEASUREMENTS TAB:
           - Record experimental measurements with timestamps
           - View and plot measurement history
           - Export data to CSV for further analysis
        
        5. TERMINOLOGIES TAB:
           - Reference guide for element reproduction procedures
           - Methods for measuring atomic weights
           - Complete gas laws with formulas and explanations
           - Key chemical and atomic theories
        """
        
        instructions_label = tk.Label(self.about_frame, text=instructions, font=self.custom_font, justify="left")
        instructions_label.pack(pady=10)

def main():
    """Main function to run the application"""
    root = tk.Tk()
    app = ChemistryToolkit(root)
    root.mainloop()

if __name__ == "__main__":
    main()