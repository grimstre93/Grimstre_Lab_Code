# -*- coding: utf-8 -*-
"""
Chemistry Toolkit with Explosives Manufacturing Module
Created on Tue Aug 20 2025
@author: Samuel
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import math
import re
from sympy import Matrix, lcm
from datetime import datetime
import csv
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import pandas as pd

# Configure matplotlib to use Tkinter backend
plt.rcParams['font.family'] = 'Times New Roman'

class ChemistryToolkit:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Chemistry Toolkit with Explosives Manufacturing")
        self.root.geometry("1400x900")
        
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
        
        # Initialize data FIRST to avoid AttributeError
        self.periodic_table = self.load_periodic_table()
        self.measurements = []
        self.explosives_data = self.load_explosives_data()
        
        # Create tabs
        self.notebook = ttk.Notebook(root)
        
        # Create frames for each tab
        self.periodic_table_frame = ttk.Frame(self.notebook, padding="10")
        self.reaction_frame = ttk.Frame(self.notebook, padding="10")
        self.explosives_frame = ttk.Frame(self.notebook, padding="10")
        self.gas_laws_frame = ttk.Frame(self.notebook, padding="10")
        self.measurements_frame = ttk.Frame(self.notebook, padding="10")
        self.terminology_frame = ttk.Frame(self.notebook, padding="10")
        self.about_frame = ttk.Frame(self.notebook, padding="10")
        
        # Add tabs to notebook
        self.notebook.add(self.periodic_table_frame, text="Periodic Table")
        self.notebook.add(self.reaction_frame, text="Reaction Analysis")
        self.notebook.add(self.explosives_frame, text="Explosives Manufacturing")
        self.notebook.add(self.gas_laws_frame, text="Gas Laws")
        self.notebook.add(self.measurements_frame, text="Measurements")
        self.notebook.add(self.terminology_frame, text="Terminologies")
        self.notebook.add(self.about_frame, text="About")
        
        self.notebook.pack(expand=1, fill="both")
        
        # Initialize components
        self.setup_periodic_table_tab()
        self.setup_reaction_tab()
        self.setup_explosives_tab()
        self.setup_gas_laws_tab()
        self.setup_measurements_tab()
        self.setup_terminology_tab()
        self.setup_about_tab()
    
    def load_periodic_table(self):
        """Load periodic table data with all 118 elements"""
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
            "Sc": {"name": "Scandium", "atomic_number": 21, "atomic_weight": 44.956, "group": 3, "period": 4, "category": "transition metal", "state": "solid"},
            "Ti": {"name": "Titanium", "atomic_number": 22, "atomic_weight": 47.867, "group": 4, "period": 4, "category": "transition metal", "state": "solid"},
            "V": {"name": "Vanadium", "atomic_number": 23, "atomic_weight": 50.942, "group": 5, "period": 4, "category": "transition metal", "state": "solid"},
            "Cr": {"name": "Chromium", "atomic_number": 24, "atomic_weight": 51.996, "group": 6, "period": 4, "category": "transition metal", "state": "solid"},
            "Mn": {"name": "Manganese", "atomic_number": 25, "atomic_weight": 54.938, "group": 7, "period": 4, "category": "transition metal", "state": "solid"},
            "Fe": {"name": "Iron", "atomic_number": 26, "atomic_weight": 55.845, "group": 8, "period": 4, "category": "transition metal", "state": "solid"},
            "Co": {"name": "Cobalt", "atomic_number": 27, "atomic_weight": 58.933, "group": 9, "period": 4, "category": "transition metal", "state": "solid"},
            "Ni": {"name": "Nickel", "atomic_number": 28, "atomic_weight": 58.693, "group": 10, "period": 4, "category": "transition metal", "state": "solid"},
            "Cu": {"name": "Copper", "atomic_number": 29, "atomic_weight": 63.546, "group": 11, "period": 4, "category": "transition metal", "state": "solid"},
            "Zn": {"name": "Zinc", "atomic_number": 30, "atomic_weight": 65.38, "group": 12, "period": 4, "category": "transition metal", "state": "solid"},
            "Ga": {"name": "Gallium", "atomic_number": 31, "atomic_weight": 69.723, "group": 13, "period": 4, "category": "post-transition metal", "state": "solid"},
            "Ge": {"name": "Germanium", "atomic_number": 32, "atomic_weight": 72.630, "group": 14, "period": 4, "category": "metalloid", "state": "solid"},
            "As": {"name": "Arsenic", "atomic_number": 33, "atomic_weight": 74.922, "group": 15, "period": 4, "category": "metalloid", "state": "solid"},
            "Se": {"name": "Selenium", "atomic_number": 34, "atomic_weight": 78.971, "group": 16, "period": 4, "category": "nonmetal", "state": "solid"},
            "Br": {"name": "Bromine", "atomic_number": 35, "atomic_weight": 79.904, "group": 17, "period": 4, "category": "halogen", "state": "liquid"},
            "Kr": {"name": "Krypton", "atomic_number": 36, "atomic_weight": 83.798, "group": 18, "period": 4, "category": "noble gas", "state": "gas"},
            "Rb": {"name": "Rubidium", "atomic_number": 37, "atomic_weight": 85.468, "group": 1, "period": 5, "category": "alkali metal", "state": "solid"},
            "Sr": {"name": "Strontium", "atomic_number": 38, "atomic_weight": 87.62, "group": 2, "period": 5, "category": "alkaline earth metal", "state": "solid"},
            "Y": {"name": "Yttrium", "atomic_number": 39, "atomic_weight": 88.906, "group": 3, "period": 5, "category": "transition metal", "state": "solid"},
            "Zr": {"name": "Zirconium", "atomic_number": 40, "atomic_weight": 91.224, "group": 4, "period": 5, "category": "transition metal", "state": "solid"},
            "Nb": {"name": "Niobium", "atomic_number": 41, "atomic_weight": 92.906, "group": 5, "period": 5, "category": "transition metal", "state": "solid"},
            "Mo": {"name": "Molybdenum", "atomic_number": 42, "atomic_weight": 95.95, "group": 6, "period": 5, "category": "transition metal", "state": "solid"},
            "Tc": {"name": "Technetium", "atomic_number": 43, "atomic_weight": 98.0, "group": 7, "period": 5, "category": "transition metal", "state": "solid"},
            "Ru": {"name": "Ruthenium", "atomic_number": 44, "atomic_weight": 101.07, "group": 8, "period": 5, "category": "transition metal", "state": "solid"},
            "Rh": {"name": "Rhodium", "atomic_number": 45, "atomic_weight": 102.91, "group": 9, "period": 5, "category": "transition metal", "state": "solid"},
            "Pd": {"name": "Palladium", "atomic_number": 46, "atomic_weight": 106.42, "group": 10, "period": 5, "category": "transition metal", "state": "solid"},
            "Ag": {"name": "Silver", "atomic_number": 47, "atomic_weight": 107.87, "group": 11, "period": 5, "category": "transition metal", "state": "solid"},
            "Cd": {"name": "Cadmium", "atomic_number": 48, "atomic_weight": 112.41, "group": 12, "period": 5, "category": "transition metal", "state": "solid"},
            "In": {"name": "Indium", "atomic_number": 49, "atomic_weight": 114.82, "group": 13, "period": 5, "category": "post-transition metal", "state": "solid"},
            "Sn": {"name": "Tin", "atomic_number": 50, "atomic_weight": 118.71, "group": 14, "period": 5, "category": "post-transition metal", "state": "solid"},
            "Sb": {"name": "Antimony", "atomic_number": 51, "atomic_weight": 121.76, "group": 15, "period": 5, "category": "metalloid", "state": "solid"},
            "Te": {"name": "Tellurium", "atomic_number": 52, "atomic_weight": 127.60, "group": 16, "period": 5, "category": "metalloid", "state": "solid"},
            "I": {"name": "Iodine", "atomic_number": 53, "atomic_weight": 126.90, "group": 17, "period": 5, "category": "halogen", "state": "solid"},
            "Xe": {"name": "Xenon", "atomic_number": 54, "atomic_weight": 131.29, "group": 18, "period": 5, "category": "noble gas", "state": "gas"},
            "Cs": {"name": "Cesium", "atomic_number": 55, "atomic_weight": 132.91, "group": 1, "period": 6, "category": "alkali metal", "state": "solid"},
            "Ba": {"name": "Barium", "atomic_number": 56, "atomic_weight": 137.33, "group": 2, "period": 6, "category": "alkaline earth metal", "state": "solid"},
            "La": {"name": "Lanthanum", "atomic_number": 57, "atomic_weight": 138.91, "group": 3, "period": 6, "category": "lanthanide", "state": "solid"},
            "Ce": {"name": "Cerium", "atomic_number": 58, "atomic_weight": 140.12, "group": 3, "period": 6, "category": "lanthanide", "state": "solid"},
            "Pr": {"name": "Praseodymium", "atomic_number": 59, "atomic_weight": 140.91, "group": 3, "period": 6, "category": "lanthanide", "state": "solid"},
            "Nd": {"name": "Neodymium", "atomic_number": 60, "atomic_weight": 144.24, "group": 3, "period": 6, "category": "lanthanide", "state": "solid"},
            "Pm": {"name": "Promethium", "atomic_number": 61, "atomic_weight": 145.0, "group": 3, "period": 6, "category": "lanthanide", "state": "solid"},
            "Sm": {"name": "Samarium", "atomic_number": 62, "atomic_weight": 150.36, "group": 3, "period": 6, "category": "lanthanide", "state": "solid"},
            "Eu": {"name": "Europium", "atomic_number": 63, "atomic_weight": 151.96, "group": 3, "period": 6, "category": "lanthanide", "state": "solid"},
            "Gd": {"name": "Gadolinium", "atomic_number": 64, "atomic_weight": 157.25, "group": 3, "period": 6, "category": "lanthanide", "state": "solid"},
            "Tb": {"name": "Terbium", "atomic_number": 65, "atomic_weight": 158.93, "group": 3, "period": 6, "category": "lanthanide", "state": "solid"},
            "Dy": {"name": "Dysprosium", "atomic_number": 66, "atomic_weight": 162.50, "group": 3, "period": 6, "category": "lanthanide", "state": "solid"},
            "Ho": {"name": "Holmium", "atomic_number": 67, "atomic_weight": 164.93, "group": 3, "period": 6, "category": "lanthanide", "state": "solid"},
            "Er": {"name": "Erbium", "atomic_number": 68, "atomic_weight": 167.26, "group": 3, "period": 6, "category": "lanthanide", "state": "solid"},
            "Tm": {"name": "Thulium", "atomic_number": 69, "atomic_weight": 168.93, "group": 3, "period": 6, "category": "lanthanide", "state": "solid"},
            "Yb": {"name": "Ytterbium", "atomic_number": 70, "atomic_weight": 173.05, "group": 3, "period": 6, "category": "lanthanide", "state": "solid"},
            "Lu": {"name": "Lutetium", "atomic_number": 71, "atomic_weight": 174.97, "group": 3, "period": 6, "category": "lanthanide", "state": "solid"},
            "Hf": {"name": "Hafnium", "atomic_number": 72, "atomic_weight": 178.49, "group": 4, "period": 6, "category": "transition metal", "state": "solid"},
            "Ta": {"name": "Tantalum", "atomic_number": 73, "atomic_weight": 180.95, "group": 5, "period": 6, "category": "transition metal", "state": "solid"},
            "W": {"name": "Tungsten", "atomic_number": 74, "atomic_weight": 183.84, "group": 6, "period": 6, "category": "transition metal", "state": "solid"},
            "Re": {"name": "Rhenium", "atomic_number": 75, "atomic_weight": 186.21, "group": 7, "period": 6, "category": "transition metal", "state": "solid"},
            "Os": {"name": "Osmium", "atomic_number": 76, "atomic_weight": 190.23, "group": 8, "period": 6, "category": "transition metal", "state": "solid"},
            "Ir": {"name": "Iridium", "atomic_number": 77, "atomic_weight": 192.22, "group": 9, "period": 6, "category": "transition metal", "state": "solid"},
            "Pt": {"name": "Platinum", "atomic_number": 78, "atomic_weight": 195.08, "group": 10, "period": 6, "category": "transition metal", "state": "solid"},
            "Au": {"name": "Gold", "atomic_number": 79, "atomic_weight": 196.97, "group": 11, "period": 6, "category": "transition metal", "state": "solid"},
            "Hg": {"name": "Mercury", "atomic_number": 80, "atomic_weight": 200.59, "group": 12, "period": 6, "category": "transition metal", "state": "liquid"},
            "Tl": {"name": "Thallium", "atomic_number": 81, "atomic_weight": 204.38, "group": 13, "period": 6, "category": "post-transition metal", "state": "solid"},
            "Pb": {"name": "Lead", "atomic_number": 82, "atomic_weight": 207.2, "group": 14, "period": 6, "category": "post-transition metal", "state": "solid"},
            "Bi": {"name": "Bismuth", "atomic_number": 83, "atomic_weight": 208.98, "group": 15, "period": 6, "category": "post-transition metal", "state": "solid"},
            "Po": {"name": "Polonium", "atomic_number": 84, "atomic_weight": 209.0, "group": 16, "period": 6, "category": "metalloid", "state": "solid"},
            "At": {"name": "Astatine", "atomic_number": 85, "atomic_weight": 210.0, "group": 17, "period": 6, "category": "halogen", "state": "solid"},
            "Rn": {"name": "Radon", "atomic_number": 86, "atomic_weight": 222.0, "group": 18, "period": 6, "category": "noble gas", "state": "gas"},
            "Fr": {"name": "Francium", "atomic_number": 87, "atomic_weight": 223.0, "group": 1, "period": 7, "category": "alkali metal", "state": "solid"},
            "Ra": {"name": "Radium", "atomic_number": 88, "atomic_weight": 226.0, "group": 2, "period": 7, "category": "alkaline earth metal", "state": "solid"},
            "Ac": {"name": "Actinium", "atomic_number": 89, "atomic_weight": 227.0, "group": 3, "period": 7, "category": "actinide", "state": "solid"},
            "Th": {"name": "Thorium", "atomic_number": 90, "atomic_weight": 232.04, "group": 3, "period": 7, "category": "actinide", "state": "solid"},
            "Pa": {"name": "Protactinium", "atomic_number": 91, "atomic_weight": 231.04, "group": 3, "period": 7, "category": "actinide", "state": "solid"},
            "U": {"name": "Uranium", "atomic_number": 92, "atomic_weight": 238.03, "group": 3, "period": 7, "category": "actinide", "state": "solid"},
            "Np": {"name": "Neptunium", "atomic_number": 93, "atomic_weight": 237.0, "group": 3, "period": 7, "category": "actinide", "state": "solid"},
            "Pu": {"name": "Plutonium", "atomic_number": 94, "atomic_weight": 244.0, "group": 3, "period": 7, "category": "actinide", "state": "solid"},
            "Am": {"name": "Americium", "atomic_number": 95, "atomic_weight": 243.0, "group": 3, "period": 7, "category": "actinide", "state": "solid"},
            "Cm": {"name": "Curium", "atomic_number": 96, "atomic_weight": 247.0, "group": 3, "period": 7, "category": "actinide", "state": "solid"},
            "Bk": {"name": "Berkelium", "atomic_number": 97, "atomic_weight": 247.0, "group": 3, "period": 7, "category": "actinide", "state": "solid"},
            "Cf": {"name": "Californium", "atomic_number": 98, "atomic_weight": 251.0, "group": 3, "period": 7, "category": "actinide", "state": "solid"},
            "Es": {"name": "Einsteinium", "atomic_number": 99, "atomic_weight": 252.0, "group": 3, "period": 7, "category": "actinide", "state": "solid"},
            "Fm": {"name": "Fermium", "atomic_number": 100, "atomic_weight": 257.0, "group": 3, "period": 7, "category": "actinide", "state": "solid"},
            "Md": {"name": "Mendelevium", "atomic_number": 101, "atomic_weight": 258.0, "group": 3, "period": 7, "category": "actinide", "state": "solid"},
            "No": {"name": "Nobelium", "atomic_number": 102, "atomic_weight": 259.0, "group": 3, "period": 7, "category": "actinide", "state": "solid"},
            "Lr": {"name": "Lawrencium", "atomic_number": 103, "atomic_weight": 262.0, "group": 3, "period": 7, "category": "actinide", "state": "solid"},
            "Rf": {"name": "Rutherfordium", "atomic_number": 104, "atomic_weight": 267.0, "group": 4, "period": 7, "category": "transition metal", "state": "solid"},
            "Db": {"name": "Dubnium", "atomic_number": 105, "atomic_weight": 268.0, "group": 5, "period": 7, "category": "transition metal", "state": "solid"},
            "Sg": {"name": "Seaborgium", "atomic_number": 106, "atomic_weight": 269.0, "group": 6, "period": 7, "category": "transition metal", "state": "solid"},
            "Bh": {"name": "Bohrium", "atomic_number": 107, "atomic_weight": 270.0, "group": 7, "period": 7, "category": "transition metal", "state": "solid"},
            "Hs": {"name": "Hassium", "atomic_number": 108, "atomic_weight": 277.0, "group": 8, "period": 7, "category": "transition metal", "state": "solid"},
            "Mt": {"name": "Meitnerium", "atomic_number": 109, "atomic_weight": 278.0, "group": 9, "period": 7, "category": "transition metal", "state": "solid"},
            "Ds": {"name": "Darmstadtium", "atomic_number": 110, "atomic_weight": 281.0, "group": 10, "period": 7, "category": "transition metal", "state": "solid"},
            "Rg": {"name": "Roentgenium", "atomic_number": 111, "atomic_weight": 282.0, "group": 11, "period": 7, "category": "transition metal", "state": "solid"},
            "Cn": {"name": "Copernicium", "atomic_number": 112, "atomic_weight": 285.0, "group": 12, "period": 7, "category": "transition metal", "state": "solid"},
            "Nh": {"name": "Nihonium", "atomic_number": 113, "atomic_weight": 286.0, "group": 13, "period": 7, "category": "post-transition metal", "state": "solid"},
            "Fl": {"name": "Flerovium", "atomic_number": 114, "atomic_weight": 289.0, "group": 14, "period": 7, "category": "post-transition metal", "state": "solid"},
            "Mc": {"name": "Moscovium", "atomic_number": 115, "atomic_weight": 290.0, "group": 15, "period": 7, "category": "post-transition metal", "state": "solid"},
            "Lv": {"name": "Livermorium", "atomic_number": 116, "atomic_weight": 293.0, "group": 16, "period": 7, "category": "post-transition metal", "state": "solid"},
            "Ts": {"name": "Tennessine", "atomic_number": 117, "atomic_weight": 294.0, "group": 17, "period": 7, "category": "halogen", "state": "solid"},
            "Og": {"name": "Oganesson", "atomic_number": 118, "atomic_weight": 294.0, "group": 18, "period": 7, "category": "noble gas", "state": "solid"}
        }
    
    def load_explosives_data(self):
        """Load explosives data from research document"""
        return {
            "Dynamite": {
                "types": {
                    "Guhr Dynamite": {"composition": "75% NG, 25% kieselguhr", "VOD": "5600-6800 m/s", "sensitivity": "Moderate", "water_resistance": "Poor"},
                    "Straight Dynamite": {"composition": "20-60% NG, wood pulp, nitrate", "VOD": "4500-6250 m/s", "sensitivity": "Moderate", "water_resistance": "Poor-good"},
                    "Ammonia Dynamite": {"composition": "20-50% AN, 20-40% NG", "VOD": "2500-4000 m/s", "sensitivity": "Low", "water_resistance": "Moderate"}
                },
                "history": "Invented by Alfred Nobel in 1867 by stabilizing nitroglycerin with kieselguhr"
            },
            "Blasting Gelatin": {
                "composition": "92% NG, 8% nitrocellulose",
                "VOD": "7800-8000 m/s",
                "density": "1.53-1.63 g/cm3",
                "water_resistance": "Excellent",
                "history": "Nobel's 1875 breakthrough discovering nitrocellulose dissolved in NG forms a tough gelatin"
            },
            "ANFO": {
                "composition": "94% AN, 6% fuel oil",
                "VOD": "2500-4500 m/s",
                "sensitivity": "Low",
                "water_resistance": "Poor",
                "history": "Became dominant in 20th century for bulk mining applications"
            },
            "Potassium Picrate": {
                "composition": "C6H2KN3O7",
                "formula": "2C6H3N3O7 + K2CO3 → 2C6H2KN3O7 + CO2 + H2O",
                "MW": 267.21,
                "sensitivity": "Very high",
                "appearance": "Yellow crystalline solid",
                "density": "1.83 g/cm³"
            }
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
        
        refresh_btn = ttk.Button(search_frame, text="Refresh", command=self.refresh_periodic_table)
        refresh_btn.pack(side="left", padx=5)
        
        # Results table with scrollbars
        table_frame = ttk.Frame(self.periodic_table_frame)
        table_frame.pack(fill="both", expand=True, pady=5)
        
        columns = ("Symbol", "Name", "Atomic Number", "Atomic Weight", "Group", "Period", "Category", "State")
        self.pt_table = ttk.Treeview(table_frame, columns=columns, show="headings", height=15)
        
        for col in columns:
            self.pt_table.heading(col, text=col)
            self.pt_table.column(col, width=100)
        
        # Add scrollbars
        v_scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.pt_table.yview)
        h_scrollbar = ttk.Scrollbar(table_frame, orient="horizontal", command=self.pt_table.xview)
        self.pt_table.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        self.pt_table.pack(side="left", fill="both", expand=True)
        v_scrollbar.pack(side="right", fill="y")
        h_scrollbar.pack(side="bottom", fill="x")
        
        # Button frame for delete operations
        button_frame = ttk.Frame(self.periodic_table_frame)
        button_frame.pack(fill="x", pady=5)
        
        delete_btn = ttk.Button(button_frame, text="Delete Selected", command=self.delete_selected_element)
        delete_btn.pack(side="left", padx=5)
        
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
    
    def refresh_periodic_table(self):
        """Refresh the periodic table view"""
        self.search_entry.delete(0, tk.END)
        self.show_all_elements()
    
    def delete_selected_element(self):
        """Delete selected element from view (not from actual data)"""
        selected = self.pt_table.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select an element to delete from view")
            return
        
        for item in selected:
            self.pt_table.delete(item)
    
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
    
    def setup_explosives_tab(self):
        """Set up the explosives manufacturing tab"""
        # Create notebook for different explosives
        explosives_notebook = ttk.Notebook(self.explosives_frame)
        explosives_notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Potassium Picrate tab
        k_picrate_frame = ttk.Frame(explosives_notebook)
        explosives_notebook.add(k_picrate_frame, text="Potassium Picrate")
        
        # Dynamite tab
        dynamite_frame = ttk.Frame(explosives_notebook)
        explosives_notebook.add(dynamite_frame, text="Dynamite")
        
        # ANFO tab
        anfo_frame = ttk.Frame(explosives_notebook)
        explosives_notebook.add(anfo_frame, text="ANFO")
        
        # Blasting Gelatin tab
        gelatin_frame = ttk.Frame(explosives_notebook)
        explosives_notebook.add(gelatin_frame, text="Blasting Gelatin")
        
        # Setup each tab
        self.setup_potassium_picrate_tab(k_picrate_frame)
        self.setup_dynamite_tab(dynamite_frame)
        self.setup_anfo_tab(anfo_frame)
        self.setup_gelatin_tab(gelatin_frame)
    
    def setup_potassium_picrate_tab(self, parent_frame):
        """Set up potassium picrate manufacturing calculator"""
        # Warning label
        warning_frame = ttk.LabelFrame(parent_frame, text="WARNING")
        warning_frame.pack(fill='x', padx=10, pady=5)
        
        warning_text = ("Potassium picrate is a sensitive explosive compound. This calculator is for educational purposes only. "
                       "Only trained professionals with proper safety equipment and facilities should attempt to handle or synthesize this compound.")
        warning_label = ttk.Label(warning_frame, text=warning_text, wraplength=1000, foreground='red')
        warning_label.pack(padx=10, pady=10)
        
        # Main content frame
        content_frame = ttk.Frame(parent_frame)
        content_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Left frame for inputs
        left_frame = ttk.LabelFrame(content_frame, text="Manufacturing Parameters")
        left_frame.pack(side='left', fill='both', expand=True, padx=(0, 5))
        
        # Molecular weights
        self.MW_PICRIC_ACID = 229.11  # g/mol
        self.MW_K2CO3 = 138.21  # g/mol
        self.MW_POTASSIUM_PICRATE = 267.21  # g/mol
        
        # Input fields
        inputs = [
            ("Desired Potassium Picrate Amount (g)", "target_amount", 50.0),
            ("Potassium Carbonate Purity (%)", "k2co3_purity", 95),
            ("Picric Acid Purity (%)", "picric_purity", 98),
            ("Reaction Temperature (°C)", "reaction_temp", 95),
            ("Water Volume per gram of Picric Acid (ml)", "water_ratio", 2.0)
        ]
        
        self.kp_input_vars = {}
        for i, (label, name, default) in enumerate(inputs):
            frame = ttk.Frame(left_frame)
            frame.pack(fill='x', pady=5)
            
            ttk.Label(frame, text=label).pack(side='left')
            var = tk.DoubleVar(value=default)
            entry = ttk.Entry(frame, textvariable=var, width=15)
            entry.pack(side='right')
            self.kp_input_vars[name] = var
        
        # Calculate button
        calculate_btn = ttk.Button(left_frame, text="Calculate Manufacturing Parameters", command=self.calculate_potassium_picrate)
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
        self.kp_results_frame = ttk.LabelFrame(right_frame, text="Calculation Results")
        self.kp_results_frame.pack(fill='both', expand=True)
        
        # Required materials table
        materials_frame = ttk.LabelFrame(self.kp_results_frame, text="Required Materials")
        materials_frame.pack(fill='x', padx=10, pady=5)
        
        self.kp_materials_tree = ttk.Treeview(materials_frame, columns=('amount'), show='tree headings', height=3)
        self.kp_materials_tree.heading('#0', text='Material')
        self.kp_materials_tree.heading('amount', text='Amount')
        self.kp_materials_tree.column('#0', width=200)
        self.kp_materials_tree.column('amount', width=100)
        self.kp_materials_tree.pack(fill='x', padx=5, pady=5)
        
        # Reaction information table
        reaction_frame = ttk.LabelFrame(self.kp_results_frame, text="Reaction Information")
        reaction_frame.pack(fill='x', padx=10, pady=5)
        
        self.kp_reaction_tree = ttk.Treeview(reaction_frame, columns=('value'), show='tree headings', height=4)
        self.kp_reaction_tree.heading('#0', text='Parameter')
        self.kp_reaction_tree.heading('value', text='Value')
        self.kp_reaction_tree.column('#0', width=150)
        self.kp_reaction_tree.column('value', width=100)
        self.kp_reaction_tree.pack(fill='x', padx=5, pady=5)
        
        # Procedure output
        procedure_frame = ttk.LabelFrame(parent_frame, text="Manufacturing Procedure")
        procedure_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.kp_procedure_text = scrolledtext.ScrolledText(procedure_frame, wrap=tk.WORD, width=100, height=15)
        self.kp_procedure_text.pack(fill='both', expand=True, padx=10, pady=10)
        self.kp_procedure_text.insert(tk.END, "Procedure will be generated here after calculation.")
        self.kp_procedure_text.config(state=tk.DISABLED)
        
        # Perform initial calculation
        self.calculate_potassium_picrate()
    
    def calculate_potassium_picrate(self):
        """Calculate potassium picrate manufacturing parameters"""
        # Get input values
        target_amount = self.kp_input_vars['target_amount'].get()
        k2co3_purity = self.kp_input_vars['k2co3_purity'].get() / 100
        picric_purity = self.kp_input_vars['picric_purity'].get() / 100
        reaction_temp = self.kp_input_vars['reaction_temp'].get()
        water_ratio = self.kp_input_vars['water_ratio'].get()
        
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
        for item in self.kp_materials_tree.get_children():
            self.kp_materials_tree.delete(item)
            
        self.kp_materials_tree.insert('', 'end', text='Potassium Carbonate (K₂CO₃)', 
                                  values=(f"{k2co3_required:.2f} g",))
        self.kp_materials_tree.insert('', 'end', text='Picric Acid', 
                                  values=(f"{picric_acid_required:.2f} g",))
        self.kp_materials_tree.insert('', 'end', text='Water', 
                                  values=(f"{water_required:.2f} ml",))
        
        # Update reaction information table
        for item in self.kp_reaction_tree.get_children():
            self.kp_reaction_tree.delete(item)
            
        self.kp_reaction_tree.insert('', 'end', text='Theoretical Yield', 
                                 values=(f"{theoretical_yield:.2f} g",))
        self.kp_reaction_tree.insert('', 'end', text='Expected Actual Yield', 
                                 values=(f"{actual_yield:.2f} g",))
        self.kp_reaction_tree.insert('', 'end', text='Yield Percentage', 
                                 values=(f"{yield_percentage:.1f}%",))
        self.kp_reaction_tree.insert('', 'end', text='Limiting Reagent', 
                                 values=(limiting_reagent,))
        
        # Generate and display procedure
        self.generate_potassium_picrate_procedure(target_amount, k2co3_required, picric_acid_required, 
                               water_required, reaction_temp, actual_yield, 
                               yield_percentage, limiting_reagent)
    
    def generate_potassium_picrate_procedure(self, target_amount, k2co3, picric, water, temp, 
                          actual_yield, yield_percentage, limiting_reagent):
        """Generate manufacturing procedure for potassium picrate"""
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
        
        self.kp_procedure_text.config(state=tk.NORMAL)
        self.kp_procedure_text.delete(1.0, tk.END)
        self.kp_procedure_text.insert(tk.END, procedure)
        self.kp_procedure_text.config(state=tk.DISABLED)
    
    def setup_dynamite_tab(self, parent_frame):
        """Set up dynamite manufacturing information with calculator"""
        content_frame = ttk.Frame(parent_frame)
        content_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Warning label
        warning_frame = ttk.LabelFrame(content_frame, text="WARNING")
        warning_frame.pack(fill='x', pady=5)
        
        warning_text = ("Dynamite is a high explosive. Manufacturing requires specialized training, equipment, "
                       "and legal authorization. This information is for educational purposes only.")
        warning_label = ttk.Label(warning_frame, text=warning_text, wraplength=1000, foreground='red')
        warning_label.pack(padx=10, pady=10)
        
        # Dynamite calculator frame
        calculator_frame = ttk.LabelFrame(content_frame, text="Dynamite Manufacturing Calculator")
        calculator_frame.pack(fill='x', pady=5)
        
        # Input fields
        input_frame = ttk.Frame(calculator_frame)
        input_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Label(input_frame, text="Desired Dynamite Amount (kg):").grid(row=0, column=0, sticky="w", padx=5, pady=2)
        self.dynamite_amount_var = tk.DoubleVar(value=10.0)
        ttk.Entry(input_frame, textvariable=self.dynamite_amount_var, width=10).grid(row=0, column=1, padx=5, pady=2)
        
        ttk.Label(input_frame, text="Dynamite Type:").grid(row=1, column=0, sticky="w", padx=5, pady=2)
        self.dynamite_type_var = tk.StringVar(value="Guhr Dynamite")
        dynamite_types = ["Guhr Dynamite", "Straight Dynamite", "Ammonia Dynamite"]
        ttk.Combobox(input_frame, textvariable=self.dynamite_type_var, values=dynamite_types, state="readonly", width=15).grid(row=1, column=1, padx=5, pady=2)
        
        ttk.Label(input_frame, text="NG Purity (%):").grid(row=2, column=0, sticky="w", padx=5, pady=2)
        self.ng_purity_var = tk.DoubleVar(value=98.0)
        ttk.Entry(input_frame, textvariable=self.ng_purity_var, width=10).grid(row=2, column=1, padx=5, pady=2)
        
        # Calculate button
        ttk.Button(input_frame, text="Calculate", command=self.calculate_dynamite).grid(row=3, column=0, columnspan=2, pady=5)
        
        # Results frame
        results_frame = ttk.Frame(calculator_frame)
        results_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Label(results_frame, text="Nitroglycerin Required:").grid(row=0, column=0, sticky="w", padx=5, pady=2)
        self.ng_result_var = tk.StringVar(value="0 kg")
        ttk.Label(results_frame, textvariable=self.ng_result_var).grid(row=0, column=1, sticky="w", padx=5, pady=2)
        
        ttk.Label(results_frame, text="Absorbent Required:").grid(row=1, column=0, sticky="w", padx=5, pady=2)
        self.absorbent_result_var = tk.StringVar(value="0 kg")
        ttk.Label(results_frame, textvariable=self.absorbent_result_var).grid(row=1, column=1, sticky="w", padx=5, pady=2)
        
        # Dynamite types information
        types_frame = ttk.LabelFrame(content_frame, text="Dynamite Types")
        types_frame.pack(fill='x', pady=5)
        
        dynamite_info = """
        Dynamite was invented by Alfred Nobel in 1867. Key types include:
        
        1. Guhr Dynamite (Nobel's Original):
           - Composition: 75% nitroglycerin, 25% kieselguhr (diatomaceous earth)
           - Properties: First commercially practical high explosive, stable but poor water resistance
        
        2. Straight Dynamite:
           - Composition: 20-60% NG with wood pulp and sodium nitrate
           - Properties: More powerful than guhr dynamite, better oxygen balance
        
        3. Ammonia Dynamite:
           - Composition: 20-50% ammonium nitrate, 20-40% NG
           - Properties: Safer, cooler explosion, better for mining applications
        
        Manufacturing typically involves carefully mixing nitroglycerin with absorbents and stabilizers
        in specialized facilities with extensive safety measures.
        """
        
        info_label = ttk.Label(types_frame, text=dynamite_info, justify=tk.LEFT)
        info_label.pack(padx=10, pady=10)
        
        # Properties table
        properties_frame = ttk.LabelFrame(content_frame, text="Dynamite Properties")
        properties_frame.pack(fill='x', pady=5)
        
        properties_tree = ttk.Treeview(properties_frame, columns=('value'), show='tree headings', height=4)
        properties_tree.heading('#0', text='Property')
        properties_tree.heading('value', text='Value')
        properties_tree.column('#0', width=150)
        properties_tree.column('value', width=200)
        properties_tree.pack(fill='x', padx=5, pady=5)
        
        properties_data = [
            ("Detonation Velocity", "4500-6800 m/s (depending on type)"),
            ("Sensitivity", "Moderate (requires blasting cap for initiation)"),
            ("Water Resistance", "Poor to Moderate"),
            ("Storage Stability", "Good (but can exude NG in warm conditions)")
        ]
        
        for prop, value in properties_data:
            properties_tree.insert('', 'end', text=prop, values=(value,))
        
        # Perform initial calculation
        self.calculate_dynamite()
    
    def calculate_dynamite(self):
        """Calculate dynamite manufacturing parameters"""
        try:
            total_amount = self.dynamite_amount_var.get()
            dynamite_type = self.dynamite_type_var.get()
            ng_purity = self.ng_purity_var.get() / 100
            
            if dynamite_type == "Guhr Dynamite":
                ng_percentage = 0.75
                absorbent_percentage = 0.25
                absorbent_name = "Kieselguhr"
            elif dynamite_type == "Straight Dynamite":
                ng_percentage = 0.40  # Average value
                absorbent_percentage = 0.60
                absorbent_name = "Wood pulp + Sodium nitrate"
            else:  # Ammonia Dynamite
                ng_percentage = 0.30  # Average value
                absorbent_percentage = 0.70
                absorbent_name = "Ammonium nitrate + Absorbents"
            
            ng_required = total_amount * ng_percentage / ng_purity
            absorbent_required = total_amount * absorbent_percentage
            
            self.ng_result_var.set(f"{ng_required:.2f} kg")
            self.absorbent_result_var.set(f"{absorbent_required:.2f} kg ({absorbent_name})")
        except:
            self.ng_result_var.set("Error")
            self.absorbent_result_var.set("Error")
    
    def setup_anfo_tab(self, parent_frame):
        """Set up ANFO manufacturing information with calculator"""
        content_frame = ttk.Frame(parent_frame)
        content_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # ANFO calculator
        calculator_frame = ttk.LabelFrame(content_frame, text="ANFO Manufacturing Calculator")
        calculator_frame.pack(fill='x', pady=5)
        
        # Input fields
        input_frame = ttk.Frame(calculator_frame)
        input_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Label(input_frame, text="Desired ANFO Amount (kg):").grid(row=0, column=0, sticky="w", padx=5, pady=2)
        self.anfo_amount_var = tk.DoubleVar(value=100.0)
        ttk.Entry(input_frame, textvariable=self.anfo_amount_var, width=10).grid(row=0, column=1, padx=5, pady=2)
        
        ttk.Label(input_frame, text="Fuel Oil Percentage (%):").grid(row=1, column=0, sticky="w", padx=5, pady=2)
        self.fuel_oil_percent_var = tk.DoubleVar(value=6.0)
        ttk.Entry(input_frame, textvariable=self.fuel_oil_percent_var, width=10).grid(row=1, column=1, padx=5, pady=2)
        
        ttk.Label(input_frame, text="AN Purity (%):").grid(row=2, column=0, sticky="w", padx=5, pady=2)
        self.an_purity_var = tk.DoubleVar(value=95.0)
        ttk.Entry(input_frame, textvariable=self.an_purity_var, width=10).grid(row=2, column=1, padx=5, pady=2)
        
        # Calculate button
        ttk.Button(input_frame, text="Calculate", command=self.calculate_anfo).grid(row=3, column=0, columnspan=2, pady=5)
        
        # Results
        results_frame = ttk.Frame(calculator_frame)
        results_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Label(results_frame, text="Ammonium Nitrate Required:").grid(row=0, column=0, sticky="w", padx=5, pady=2)
        self.an_result_var = tk.StringVar(value="0 kg")
        ttk.Label(results_frame, textvariable=self.an_result_var).grid(row=0, column=1, sticky="w", padx=5, pady=2)
        
        ttk.Label(results_frame, text="Fuel Oil Required:").grid(row=1, column=0, sticky="w", padx=5, pady=2)
        self.fo_result_var = tk.StringVar(value="0 L")
        ttk.Label(results_frame, textvariable=self.fo_result_var).grid(row=1, column=1, sticky="w", padx=5, pady=2)
        
        # ANFO information
        info_frame = ttk.LabelFrame(content_frame, text="ANFO (Ammonium Nitrate/Fuel Oil)")
        info_frame.pack(fill='x', pady=5)
        
        anfo_info = """
        ANFO is the most widely used industrial explosive, consisting of approximately:
        - 94% Ammonium Nitrate (oxidizer)
        - 6% Fuel Oil (typically diesel)
        
        Advantages:
        - Low cost and easy to manufacture
        - Relatively safe to handle (not cap-sensitive)
        - Good gas production for heaving action
        
        Limitations:
        - Poor water resistance
        - Requires large diameter charges for reliable detonation
        - Lower velocity of detonation compared to NG-based explosives
        
        Manufacturing Process:
        1. Use porous ammonium nitrate prills (special formulation for explosives)
        2. Mix with correct proportion of fuel oil (typically 5.7-6.2%)
        3. Allow time for oil absorption (typically 15-30 minutes)
        4. Load into boreholes using pneumatic loading equipment
        """
        
        info_label = ttk.Label(info_frame, text=anfo_info, justify=tk.LEFT)
        info_label.pack(padx=10, pady=10)
        
        # Perform initial calculation
        self.calculate_anfo()
    
    def calculate_anfo(self):
        """Calculate ANFO mixture components"""
        try:
            total_amount = self.anfo_amount_var.get()
            fuel_percent = self.fuel_oil_percent_var.get() / 100
            an_purity = self.an_purity_var.get() / 100
            
            an_amount = total_amount * (1 - fuel_percent) / an_purity
            fo_amount = total_amount * fuel_percent
            
            # Assume fuel oil density of approximately 0.85 kg/L
            fo_volume = fo_amount / 0.85
            
            self.an_result_var.set(f"{an_amount:.2f} kg")
            self.fo_result_var.set(f"{fo_volume:.2f} L ({fo_amount:.2f} kg)")
        except:
            self.an_result_var.set("Error")
            self.fo_result_var.set("Error")
    
    def setup_gelatin_tab(self, parent_frame):
        """Set up blasting gelatin information with calculator"""
        content_frame = ttk.Frame(parent_frame)
        content_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Warning label
        warning_frame = ttk.LabelFrame(content_frame, text="EXTREME HAZARD")
        warning_frame.pack(fill='x', pady=5)
        
        warning_text = ("Blasting gelatin is one of the most powerful commercial explosives. "
                       "It is extremely sensitive and requires specialized handling. "
                       "This information is for educational purposes only.")
        warning_label = ttk.Label(warning_frame, text=warning_text, wraplength=1000, foreground='red')
        warning_label.pack(padx=10, pady=10)
        
        # Gelatin calculator
        calculator_frame = ttk.LabelFrame(content_frame, text="Blasting Gelatin Manufacturing Calculator")
        calculator_frame.pack(fill='x', pady=5)
        
        # Input fields
        input_frame = ttk.Frame(calculator_frame)
        input_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Label(input_frame, text="Desired Gelatin Amount (kg):").grid(row=0, column=0, sticky="w", padx=5, pady=2)
        self.gelatin_amount_var = tk.DoubleVar(value=5.0)
        ttk.Entry(input_frame, textvariable=self.gelatin_amount_var, width=10).grid(row=0, column=1, padx=5, pady=2)
        
        ttk.Label(input_frame, text="NG Purity (%):").grid(row=1, column=0, sticky="w", padx=5, pady=2)
        self.gel_ng_purity_var = tk.DoubleVar(value=98.0)
        ttk.Entry(input_frame, textvariable=self.gel_ng_purity_var, width=10).grid(row=1, column=1, padx=5, pady=2)
        
        ttk.Label(input_frame, text="NC Purity (%):").grid(row=2, column=0, sticky="w", padx=5, pady=2)
        self.gel_nc_purity_var = tk.DoubleVar(value=95.0)
        ttk.Entry(input_frame, textvariable=self.gel_nc_purity_var, width=10).grid(row=2, column=1, padx=5, pady=2)
        
        # Calculate button
        ttk.Button(input_frame, text="Calculate", command=self.calculate_gelatin).grid(row=3, column=0, columnspan=2, pady=5)
        
        # Results
        results_frame = ttk.Frame(calculator_frame)
        results_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Label(results_frame, text="Nitroglycerin Required:").grid(row=0, column=0, sticky="w", padx=5, pady=2)
        self.gel_ng_result_var = tk.StringVar(value="0 kg")
        ttk.Label(results_frame, textvariable=self.gel_ng_result_var).grid(row=0, column=1, sticky="w", padx=5, pady=2)
        
        ttk.Label(results_frame, text="Nitrocellulose Required:").grid(row=1, column=0, sticky="w", padx=5, pady=2)
        self.gel_nc_result_var = tk.StringVar(value="0 kg")
        ttk.Label(results_frame, textvariable=self.gel_nc_result_var).grid(row=1, column=1, sticky="w", padx=5, pady=2)
        
        # Gelatin information
        info_frame = ttk.LabelFrame(content_frame, text="Blasting Gelatin")
        info_frame.pack(fill='x', pady=5)
        
        gelatin_info = """
        Blasting gelatin was discovered by Alfred Nobel in 1875 when he found that
        nitrocellulose dissolves in nitroglycerin to form a stable, rubbery mass.
        
        Composition:
        - 92-93% Nitroglycerin
        - 7-8% Nitrocellulose (collodion cotton)
        
        Properties:
        - Very high detonation velocity (7800-8000 m/s)
        - Excellent water resistance
        - High density (1.53-1.63 g/cm³)
        - Can be molded to fill boreholes completely
        
        Manufacturing involves carefully dissolving specially prepared nitrocellulose
        in nitroglycerin under controlled conditions. This process is extremely hazardous
        and requires specialized equipment and facilities.
        """
        
        info_label = ttk.Label(info_frame, text=gelatin_info, justify=tk.LEFT)
        info_label.pack(padx=10, pady=10)
        
        # Properties table
        properties_frame = ttk.LabelFrame(content_frame, text="Blasting Gelatin Properties")
        properties_frame.pack(fill='x', pady=5)
        
        properties_tree = ttk.Treeview(properties_frame, columns=('value'), show='tree headings', height=5)
        properties_tree.heading('#0', text='Property')
        properties_tree.heading('value', text='Value')
        properties_tree.column('#0', width=150)
        properties_tree.column('value', width=200)
        properties_tree.pack(fill='x', padx=5, pady=5)
        
        properties_data = [
            ("Detonation Velocity", "7800-8000 m/s"),
            ("Density", "1.53-1.63 g/cm³"),
            ("Water Resistance", "Excellent (can be used underwater)"),
            ("Lead Block Test", "Approx. 600 cc expansion"),
            ("Sensitivity", "High (requires careful handling)")
        ]
        
        for prop, value in properties_data:
            properties_tree.insert('', 'end', text=prop, values=(value,))
        
        # Perform initial calculation
        self.calculate_gelatin()
    
    def calculate_gelatin(self):
        """Calculate blasting gelatin manufacturing parameters"""
        try:
            total_amount = self.gelatin_amount_var.get()
            ng_purity = self.gel_ng_purity_var.get() / 100
            nc_purity = self.gel_nc_purity_var.get() / 100
            
            ng_percentage = 0.92  # 92% NG
            nc_percentage = 0.08  # 8% NC
            
            ng_required = total_amount * ng_percentage / ng_purity
            nc_required = total_amount * nc_percentage / nc_purity
            
            self.gel_ng_result_var.set(f"{ng_required:.2f} kg")
            self.gel_nc_result_var.set(f"{nc_required:.2f} kg")
        except:
            self.gel_ng_result_var.set("Error")
            self.gel_nc_result_var.set("Error")
    
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
        
        refresh_btn = ttk.Button(button_frame, text="Refresh", command=self.refresh_measurements)
        refresh_btn.pack(side="left", padx=5)
        
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
    
    def refresh_measurements(self):
        """Refresh the measurements table"""
        self.update_measurements_table()
    
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
        - Note: Temperature must in Kelvin
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
        
        # Explosives chemistry tab
        explosives_frame = ttk.Frame(term_notebook, padding="10")
        term_notebook.add(explosives_frame, text="Explosives Chemistry")
        
        explosives_text = scrolledtext.ScrolledText(explosives_frame, font=self.custom_font)
        explosives_text.pack(fill="both", expand=True)
        
        explosives_content = """
        EXPLOSIVES CHEMISTRY AND MANUFACTURING PRINCIPLES

        High explosives are characterized by their ability to undergo rapid, self-sustaining 
        decomposition known as detonation, which produces a shock wave and large volumes of gas.

        Key Concepts:

        1. Oxygen Balance
        - The ratio of oxygen content to the amount needed to fully oxidize the fuel components
        - Positive balance: Excess oxygen (produces NOx gases)
        - Negative balance: Insufficient oxygen (produces CO and soot)
        - Zero balance: Optimal (produces CO2, H2O, N2)

        2. Velocity of Detonation (VOD)
        - Speed at which the detonation wave travels through the explosive
        - Ranges from 2,000 m/s (ANFO) to 8,000+ m/s (high-performance explosives)
        - Higher VOD generally means greater brisance (shattering power)

        3. Brisance
        - The shattering capability of an explosive
        - Related to the speed of detonation and the pressure of the detonation wave
        - Measured by the lead block test or sand crush test

        4. Sensitivity
        - The ease with which an explosive can be initiated
        - Types: impact, friction, electrostatic, thermal
        - Primary explosives: Very sensitive (used in detonators)
        - Secondary explosives: Less sensitive (require a detonator)

        Major Explosive Families:

        1. Nitroaromatics (TNT, Tetryl, Picric Acid)
        - Contain nitro groups attached to aromatic rings
        - Generally stable and insensitive
        - Good thermal stability

        2. Nitramines (RDX, HMX)
        - Contain N-NO2 groups
        - High energy content and detonation velocity
        - Used in military applications

        3. Nitrate Esters (Nitroglycerin, PETN, Nitrocellulose)
        - Contain O-NO2 groups
        - Range from very sensitive to moderately sensitive
        - Often plasticized or phlegmatized for safety

        4. Composite Explosives (ANFO, Emulsions, Slurries)
        - Mixtures of oxidizer and fuel
        - Generally less sensitive and lower performance
        - Dominant in commercial mining applications

        Safety Considerations:
        - Always use smallest practical quantities
        - Work behind blast shields with remote handling
        - Avoid friction, impact, and electrostatic discharge
        - Store explosives properly (often under water for sensitive materials)
        - Have emergency plans and equipment readily available
        """
        explosives_text.insert(1.0, explosives_content)
        explosives_text.config(state="disabled")
    
    def setup_about_tab(self):
        """Set up the about tab"""
        about_text = f"""
        ADVANCED CHEMISTRY TOOLKIT WITH EXPLOSIVES MANUFACTURING MODULE
        
        A comprehensive software tool for chemical calculations, reference, and education.
        Includes specialized modules for explosives chemistry based on historical and modern formulations.
        
        FEATURES:
        - Periodic table reference with detailed element information
        - Chemical reaction balancing and stoichiometry calculations
        - Explosives manufacturing calculators (Potassium Picrate, ANFO, etc.)
        - Gas law calculations with step-by-step solutions
        - Measurement recording with timestamp logging
        - Comprehensive chemical terminology and theory reference
        - Data visualization and export capabilities
        
        SAFETY NOTICE:
        This software includes information about explosives and hazardous chemicals
        for educational purposes only. Actual synthesis and handling of these materials
        requires specialized training, equipment, and legal authorization. Always follow
        proper safety protocols when working with chemicals.
        
        CONTACT INFORMATION:
        Email: Samngacha@gmail.com
        Phone: +254742859291
        
        VERSION: 2.0 (Explosives Edition)
        RELEASE DATE: {datetime.now().strftime('%Y-%m-%d')}
        
        This application is designed for educational and research purposes.
        
        © 2025 Chemistry Toolkit. All rights reserved.
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
           - Use 'Refresh' to reset the view
           - Use 'Delete Selected' to remove elements from view
        
        2. REACTION ANALYSIS TAB:
           - Enter reactants and products with coefficients
           - Use 'Create Reaction' to initialize the reaction
           - Use 'Balance Equation' to automatically balance the reaction
           - Enter quantities for stoichiometry calculations
        
        3. EXPLOSIVES MANUFACTURING TAB:
           - Select from various explosive types (Potassium Picrate, Dynamite, ANFO, etc.)
           - Calculate required materials and manufacturing procedures
           - View safety information and properties for each explosive
        
        4. GAS LAWS TAB:
           - Select the gas law you want to use
           - Enter known values and leave one field empty to solve for it
           - Click 'Calculate' to compute the result with detailed steps
        
        5. MEASUREMENTS TAB:
           - Record experimental measurements with timestamps
           - View and plot measurement history
           - Export data to CSV for further analysis
           - Use 'Refresh' to update the table view
           - Use 'Delete Selected' to remove measurements
        
        6. TERMINOLOGIES TAB:
           - Reference guide for element reproduction procedures
           - Methods for measuring atomic weights
           - Complete gas laws with formulas and explanations
           - Key chemical and atomic theories
           - Explosives chemistry and manufacturing principles
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