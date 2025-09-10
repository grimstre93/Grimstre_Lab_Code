# -*- coding: utf-8 -*-
"""
Chemistry Toolkit GUI Application

A comprehensive chemistry toolkit with GUI interface for:
- Periodic table reference
- Chemical reaction analysis and balancing
- Stoichiometry calculations
- Physical/chemical laws calculations
- Measurement recording
- Data visualization
- Chemical terminologies and theories
"""

import sys
import csv
import math
import re
import logging
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any

import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import pandas as pd
import numpy as np
from sympy import Matrix, lcm
from PyQt5.QtWidgets import (QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QLineEdit, QPushButton, QTextEdit, QComboBox, QTableWidget,
                             QTableWidgetItem, QGroupBox, QSpinBox, QDoubleSpinBox, QFileDialog, 
                             QMessageBox, QHeaderView, QScrollArea, QDialog, QDialogButtonBox)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ====================== Core Chemistry Classes ======================
class Units(Enum):
    GRAMS = 'g'
    MOLES = 'mol'
    LITERS = 'L'
    ATMOSPHERES = 'atm'
    KELVIN = 'K'
    JOULES = 'J'

# Fundamental constants
R = 8.314462618  # J/(mol·K)
h = 6.62607015e-34  # J·s
c = 299792458  # m/s
k_B = 1.380649e-23  # J/K
hbar = 1.054571817e-34  # J·s
NA = 6.02214076e23  # Avogadro's number

@dataclass
class Element:
    symbol: str
    name: str
    atomic_number: int
    atomic_weight: float  # g/mol
    group: int
    period: int
    category: str  # 'alkali metal', 'halogen', etc.

def load_periodic_table() -> Dict[str, Element]:
    """Load periodic table data."""
    return {
        "H": Element("H", "Hydrogen", 1, 1.008, 1, 1, "nonmetal"),
        "He": Element("He", "Helium", 2, 4.0026, 18, 1, "noble gas"),
        "Li": Element("Li", "Lithium", 3, 6.94, 1, 2, "alkali metal"),
        "Be": Element("Be", "Beryllium", 4, 9.0122, 2, 2, "alkaline earth metal"),
        "B": Element("B", "Boron", 5, 10.81, 13, 2, "metalloid"),
        "C": Element("C", "Carbon", 6, 12.011, 14, 2, "nonmetal"),
        "N": Element("N", "Nitrogen", 7, 14.007, 15, 2, "nonmetal"),
        "O": Element("O", "Oxygen", 8, 15.999, 16, 2, "nonmetal"),
        "F": Element("F", "Fluorine", 9, 18.998, 17, 2, "halogen"),
        "Ne": Element("Ne", "Neon", 10, 20.180, 18, 2, "noble gas"),
        "Na": Element("Na", "Sodium", 11, 22.990, 1, 3, "alkali metal"),
        "Mg": Element("Mg", "Magnesium", 12, 24.305, 2, 3, "alkaline earth metal"),
        "Al": Element("Al", "Aluminum", 13, 26.982, 13, 3, "post-transition metal"),
        "Si": Element("Si", "Silicon", 14, 28.085, 14, 3, "metalloid"),
        "P": Element("P", "Phosphorus", 15, 30.974, 15, 3, "nonmetal"),
        "S": Element("S", "Sulfur", 16, 32.06, 16, 3, "nonmetal"),
        "Cl": Element("Cl", "Chlorine", 17, 35.45, 17, 3, "halogen"),
        "Ar": Element("Ar", "Argon", 18, 39.948, 18, 3, "noble gas"),
        "K": Element("K", "Potassium", 19, 39.098, 1, 4, "alkali metal"),
        "Ca": Element("Ca", "Calcium", 20, 40.078, 2, 4, "alkaline earth metal"),
    }

PERIODIC_TABLE = load_periodic_table()

@dataclass
class Measurement:
    timestamp: datetime
    variable: str
    value: float
    unit: str
    notes: str = ""

@dataclass
class Reaction:
    reactants: Dict[str, int]      # e.g., {"H2": 2, "O2": 1}
    products: Dict[str, int]       # e.g., {"H2O": 2}
    name: str = "Unnamed Reaction"
    conditions: Dict[str, Any] = field(default_factory=dict)  # temp, pressure, etc.
    
    def molar_mass(self, formula: str) -> float:
        """Compute molar mass by summing atomic weights."""
        mass = 0.0
        tokens = re.findall(r"([A-Z][a-z]*)(\d*)", formula)
        for sym, count in tokens:
            elem = PERIODIC_TABLE.get(sym)
            if not elem:
                raise KeyError(f"Element {sym} not in periodic table")
            mass += elem.atomic_weight * (int(count) if count else 1)
        return mass

    def stoichiometry(self, measured: Dict[str, float], measure_unit: str = "g") -> Dict[str, Tuple[float, float]]:
        """Perform stoichiometric calculations."""
        moles_avail = {}
        for spc, qty in measured.items():
            if measure_unit == "g":
                moles_avail[spc] = qty / self.molar_mass(spc)
            elif measure_unit == "mol":
                moles_avail[spc] = qty
            else:
                raise ValueError("Unit must be 'g' or 'mol'")

        ratios = {
            spc: moles_avail.get(spc, 0.0) / coeff
            for spc, coeff in self.reactants.items()
        }
        limiting = min(ratios, key=ratios.get)

        theoretical = {}
        factor = ratios[limiting]
        for prod, coeff in self.products.items():
            theoretical[prod] = coeff * factor

        return {
            **{f"{r}_avail": (moles_avail[r], self.reactants[r]) for r in self.reactants},
            "limiting_reagent": (limiting, ratios[limiting]),
            **{f"{p}_theoretical_mol": (theoretical[p], self.products[p]) for p in self.products},
        }
    
    def display_equation(self) -> str:
        """Returns a formatted chemical equation string"""
        def format_side(species: Dict[str, int]) -> str:
            return " + ".join(f"{coeff if coeff != 1 else ''}{spc}" for spc, coeff in species.items())
        
        return f"{format_side(self.reactants)} → {format_side(self.products)}"

    def balance_equation(self) -> None:
        """Balance the chemical equation using matrix methods."""
        try:
            elements = set()
            for formula in list(self.reactants.keys()) + list(self.products.keys()):
                tokens = re.findall(r"([A-Z][a-z]*)(\d*)", formula)
                for sym, _ in tokens:
                    elements.add(sym)
            
            elements = sorted(elements)
            
            matrix = []
            for elem in elements:
                row = []
                for formula, coeff in self.reactants.items():
                    tokens = re.findall(r"([A-Z][a-z]*)(\d*)", formula)
                    elem_count = 0
                    for sym, count in tokens:
                        if sym == elem:
                            elem_count = int(count) if count else 1
                    row.append(-elem_count)
                
                for formula, coeff in self.products.items():
                    tokens = re.findall(r"([A-Z][a-z]*)(\d*)", formula)
                    elem_count = 0
                    for sym, count in tokens:
                        if sym == elem:
                            elem_count = int(count) if count else 1
                    row.append(elem_count)
                
                matrix.append(row)
            
            mat = Matrix(matrix)
            solution = mat.nullspace()[0]
            
            denominators = [val.q for val in solution]
            lcm_val = 1
            for d in denominators:
                lcm_val = lcm(lcm_val, d)
            
            coeffs = [x * lcm_val for x in solution]
            
            num_reactants = len(self.reactants)
            reactants_coeffs = coeffs[:num_reactants]
            products_coeffs = coeffs[num_reactants:]
            
            self.reactants = {
                formula: int(reactants_coeffs[i]) 
                for i, formula in enumerate(self.reactants.keys())
            }
            self.products = {
                formula: int(products_coeffs[i])
                for i, formula in enumerate(self.products.keys())
            }
            
        except Exception as e:
            logger.error(f"Failed to balance equation: {e}")
            raise ValueError("Equation balancing failed. Check that the reaction is valid.")

class GasLaws:
    @staticmethod
    def boyle(P1: float, V1: float, P2: float = None, V2: float = None) -> float:
        """Boyle's Law: P1*V1 = P2*V2"""
        if P2 is None and V2 is not None:
            return P1 * V1 / V2
        if V2 is None and P2 is not None:
            return P1 * V1 / P2
        raise ValueError("Provide exactly one of P2 or V2")

    @staticmethod
    def ideal_gas(P: float = None, V: float = None, 
                 n: float = None, T: float = None) -> float:
        """Ideal Gas Law: PV = nRT"""
        if P is None:
            return n * R * T / V
        if V is None:
            return n * R * T / P
        if n is None:
            return P * V / (R * T)
        if T is None:
            return P * V / (n * R)
        raise ValueError("Exactly one variable must be None")

# ====================== GUI Components ======================
class AboutDialog(QDialog):
    """Dialog showing information about the application and usage guidelines"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("About Chemistry Toolkit")
        self.setModal(True)
        self.resize(600, 500)
        
        layout = QVBoxLayout()
        
        # Title
        title = QLabel("Chemistry Toolkit")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Version
        version = QLabel("Version 1.0")
        version.setAlignment(Qt.AlignCenter)
        layout.addWidget(version)
        
        # Description
        desc = QLabel("A comprehensive chemistry toolkit for students and professionals")
        desc.setAlignment(Qt.AlignCenter)
        layout.addWidget(desc)
        
        # Usage instructions
        instructions = QTextEdit()
        instructions.setReadOnly(True)
        instructions.setHtml("""
        <h2>Usage Guide</h2>
        
        <h3>Periodic Table Tab</h3>
        <ul>
            <li>Search for elements by symbol or name</li>
            <li>Click 'Show All Elements' to display the complete table</li>
            <li>Use the 'Refresh' button to reset the view</li>
        </ul>
        
        <h3>Reaction Analysis Tab</h3>
        <ul>
            <li>Enter reactants and products with their coefficients</li>
            <li>Click 'Create Reaction' to initialize the reaction</li>
            <li>Use 'Balance Equation' to automatically balance the reaction</li>
            <li>Enter quantities for stoichiometry calculations</li>
            <li>Use 'Delete' buttons to remove reactants/products</li>
        </ul>
        
        <h3>Gas Laws Tab</h3>
        <ul>
            <li>Select the gas law you want to use</li>
            <li>Enter known values and leave one field empty to solve for it</li>
            <li>Click 'Calculate' to compute the result</li>
            <li>Use 'Refresh' to clear all inputs</li>
        </ul>
        
        <h3>Measurements Tab</h3>
        <ul>
            <li>Record experimental measurements with timestamps</li>
            <li>View and plot measurement history</li>
            <li>Export data to CSV for further analysis</li>
            <li>Use 'Delete' to remove unwanted measurements</li>
        </ul>
        
        <h3>Terminologies Tab</h3>
        <ul>
            <li>Browse chemical theories and concepts</li>
            <li>Reference guide for obtaining all elements</li>
            <li>Comprehensive chemistry resource</li>
        </ul>
        """)
        layout.addWidget(instructions)
        
        # Close button
        button_box = QDialogButtonBox(QDialogButtonBox.Ok)
        button_box.accepted.connect(self.accept)
        layout.addWidget(button_box)
        
        self.setLayout(layout)

class MplCanvas(FigureCanvas):
    """Matplotlib canvas for embedding plots in Qt"""
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super().__init__(fig)

class TerminologyTab(QWidget):
    """Tab for displaying chemical terminologies and theories"""
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Create a scroll area for the content
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        
        # Create a widget to hold the content
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        
        # Add title
        title = QLabel("Chemical Terminologies and Theories")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setAlignment(Qt.AlignCenter)
        content_layout.addWidget(title)
        
        # Add content sections
        self.add_section(content_layout, "Workflow to Obtain or Synthesize All 118 Elements", self.get_elements_content())
        self.add_section(content_layout, "Key Chemical and Atomic Theories", self.get_theories_content())
        self.add_section(content_layout, "Comprehensive Chemistry Resource", self.get_resource_content())
        
        # Set the scroll area's widget
        scroll.setWidget(content_widget)
        layout.addWidget(scroll)
        
        # Refresh button
        refresh_btn = QPushButton("Refresh")
        refresh_btn.clicked.connect(self.refresh_content)
        layout.addWidget(refresh_btn)
        
        self.setLayout(layout)
    
    def add_section(self, layout, title, content):
        """Add a section with title and content"""
        # Section title
        section_title = QLabel(title)
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        section_title.setFont(title_font)
        section_title.setStyleSheet("margin-top: 20px; margin-bottom: 10px;")
        layout.addWidget(section_title)
        
        # Section content
        content_label = QTextEdit()
        content_label.setReadOnly(True)
        content_label.setHtml(content)
        content_label.setStyleSheet("background-color: white; border: 1px solid #ccc; padding: 10px;")
        layout.addWidget(content_label)
    
    def get_elements_content(self):
        """Return HTML formatted content for elements workflow"""
        return """
        <h3>1. Prepare Your Facility and Safety Protocols</h3>
        <ul>
            <li>Establish a multi-functional chemistry lab with fume hoods, high-vacuum pumps, inert-atmosphere gloveboxes, high-temperature furnaces, electrolytic cells, and fractional distillation columns.</li>
            <li>Implement rigorous safety measures including PPE for acids, bases, cryogenics, and radiation.</li>
        </ul>
        
        <h3>2. Gases from the Atmosphere and Water</h3>
        <ul>
            <li>Hydrogen (H): Electrolyze deionized water with a proton-exchange membrane cell.</li>
            <li>Nitrogen (N), Oxygen (O), Argon (Ar), Neon (Ne), Krypton (Kr), Xenon (Xe): Fractional distillation of liquefied air.</li>
            <li>Helium (He): Commercially from natural gas wells via low-temperature separation.</li>
        </ul>
        
        <h3>3. Alkali, Alkaline-Earth, and Early Transition Metals</h3>
        <ul>
            <li>Lithium (Li), Sodium (Na), Potassium (K): Brine or ore mining and molten-salt electrolysis.</li>
            <li>Magnesium (Mg), Calcium (Ca), Strontium (Sr), Barium (Ba): Extract from seawater or minerals.</li>
        </ul>
        
        <h3>4. Post-Transition Metals, Metalloids, and Nonmetals</h3>
        <ul>
            <li>Aluminum (Al), Gallium (Ga), Indium (In), Thallium (Tl): Bauxite for Al via Bayer process.</li>
            <li>Boron (B), Silicon (Si), Germanium (Ge): Borates from evaporation ponds; quartz reduction for Si.</li>
        </ul>
        
        <h3>5. Halogens and Chalcogens</h3>
        <ul>
            <li>Fluorine (F): Electrolysis of anhydrous HF/KF.</li>
            <li>Chlorine (Cl): Chlor-alkali electrolysis.</li>
            <li>Bromine (Br): Oxidation of bromide-rich brines.</li>
        </ul>
        
        <h3>6. Lanthanides (57–71)</h3>
        <ul>
            <li>Monazite and bastnäsite ores from pegmatites.</li>
            <li>Crystallization or solvent extraction to fractionate individual lanthanides.</li>
        </ul>
        
        <h3>7. Actinides Up to Uranium (89–92)</h3>
        <ul>
            <li>Thorium (Th) and Uranium (U): Uraninite and thorite mining.</li>
            <li>Neptunium (Np), Plutonium (Pu): Produced by neutron irradiation of U-238 in reactors.</li>
        </ul>
        
        <h3>8. Transuranics and Superheavy Elements (93–118)</h3>
        <ul>
            <li>Heavy-ion fusion reactions in a particle accelerator.</li>
            <li>Rapid chemical separation in gas-phase or liquid-phase recoil separators.</li>
        </ul>
        
        <h3>9. Documentation and Verification</h3>
        <ul>
            <li>Characterize each isolate with mass spectrometry for isotope confirmation.</li>
            <li>Record in standardized report format with procurement route and yield.</li>
        </ul>
        """
    
    def get_theories_content(self):
        """Return HTML formatted content for chemical theories"""
        return """
        <h3>Dalton's Atomic Theory</h3>
        <p>John Dalton proposed that matter is composed of indivisible atoms, each element having atoms of a single unique mass and properties.</p>
        
        <h3>Thomson's Atomic Model</h3>
        <p>J.J. Thomson envisioned the atom as a uniform sphere of positive charge in which electrons are embedded like "plums in a pudding."</p>
        
        <h3>Rutherford's Atomic Model</h3>
        <p>Ernest Rutherford's gold-foil experiment revealed that most of an atom's mass and positive charge are concentrated in a tiny, dense nucleus.</p>
        
        <h3>Bohr's Quanta Concept</h3>
        <p>Niels Bohr proposed that electrons orbit the nucleus in fixed, quantized energy levels and emit or absorb photons when jumping between these levels.</p>
        
        <h3>Quantum Mechanical Approach for the Atom</h3>
        <p>This framework uses wavefunctions (ψ) governed by Schrödinger's equation to describe the probabilistic distribution of electrons around the nucleus.</p>
        
        <h3>Crystal Field Theory (CFT)</h3>
        <p>CFT models how the degenerate d-orbitals of a transition metal ion split in energy when surrounded by point charges (ligands) in a crystal lattice.</p>
        
        <h3>Molecular Orbital Theory</h3>
        <p>Molecular Orbital Theory constructs orbitals that extend over an entire molecule by combining atomic orbitals through linear combinations (LCAO).</p>
        
        <h3>Valence Bond Theory</h3>
        <p>Valence Bond Theory describes chemical bonds as the overlap of half-filled atomic orbitals on adjacent atoms.</p>
        
        <h3>Werner's Theory</h3>
        <p>Alfred Werner's coordination theory introduced the idea of primary valence (oxidation state) and secondary valence (coordination number).</p>
        
        <h3>Sidgwick's EAN Rule</h3>
        <p>The Effective Atomic Number (EAN) rule states that stable metal complexes often achieve an electron count equal to the noble gas configuration.</p>
        """
    
    def get_resource_content(self):
        """Return HTML formatted content for comprehensive chemistry resource"""
        return """
        <h3>Chemical Foundations and Quantum Chemistry</h3>
        <p>Introduces Dalton's atomic theory and the evolution of atomic models. Details the discovery and properties of subatomic particles, the organization of the periodic table.</p>
        
        <h3>Thermodynamics and Thermochemistry</h3>
        <p>Key thermodynamic concepts including internal energy, enthalpy, entropy, and Gibbs free energy with an emphasis on spontaneity and equilibrium.</p>
        
        <h3>Chemical Kinetics and Photochemistry</h3>
        <p>The study of reaction rates begins with definitions of rate laws, molecularity, and reaction order.</p>
        
        <h3>Chemical Equilibrium and Bonding</h3>
        <p>Reversible reactions and dynamic equilibrium concepts are presented with the law of mass action defining equilibrium constants.</p>
        
        <h3>Gases and Colligative Properties</h3>
        <p>Classical gas laws are unified into the ideal gas law, with Dalton's law of partial pressures and Graham's law of diffusion/effusion.</p>
        
        <h3>Phase Rule and Acid-Base Chemistry</h3>
        <p>Gibbs' phase rule provides a framework for analyzing multiphase systems, defining phases, components, and degrees of freedom.</p>
        
        <h3>Electrochemistry and Redox Reactions</h3>
        <p>Fundamentals of electrochemistry cover metallic and electrolytic conduction, Kohlrausch's law, and galvanic cells.</p>
        
        <h3>Coordination Chemistry and Inorganic Elements</h3>
        <p>Coordination compounds are described with central metal ions bonded to ligands of varying denticity.</p>
        
        <h3>Solid State Chemistry and Materials Characterization</h3>
        <p>Synthesis methods for solid materials include high-temperature and wet chemical routes.</p>
        
        <h3>Organic Chemistry: Hydrocarbons and Polymers</h3>
        <p>Hydrocarbon chemistry covers nomenclature, isomerism, and reactions of alkanes, alkenes, alkynes, and aromatic compounds.</p>
        
        <h3>Nuclear Chemistry</h3>
        <p>Nuclear chemistry introduces isotopes, nuclear stability, and decay modes including alpha, beta, positron emission, and electron capture.</p>
        """
    
    def refresh_content(self):
        """Refresh the content display"""
        # This tab is mostly static, so refresh just clears any potential user modifications
        self.init_ui()

class PeriodicTableTab(QWidget):
    """Tab for displaying periodic table information"""
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Search box
        search_layout = QHBoxLayout()
        search_layout.addWidget(QLabel("Search Element:"))
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Enter symbol or name")
        self.search_input.returnPressed.connect(self.search_element)
        search_layout.addWidget(self.search_input)
        
        self.search_button = QPushButton("Search")
        self.search_button.clicked.connect(self.search_element)
        search_layout.addWidget(self.search_button)
        
        # Add delete and refresh buttons
        self.delete_button = QPushButton("Delete Selected")
        self.delete_button.clicked.connect(self.delete_selected)
        search_layout.addWidget(self.delete_button)
        
        self.refresh_button = QPushButton("Refresh")
        self.refresh_button.clicked.connect(self.refresh_table)
        search_layout.addWidget(self.refresh_button)
        
        layout.addLayout(search_layout)
        
        # Results display
        self.results_table = QTableWidget()
        self.results_table.setColumnCount(7)
        self.results_table.setHorizontalHeaderLabels(["Symbol", "Name", "Atomic Number", 
                                                    "Atomic Weight", "Group", "Period", "Category"])
        self.results_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.results_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.results_table)
        
        # Display all elements button
        self.show_all_button = QPushButton("Show All Elements")
        self.show_all_button.clicked.connect(self.display_all_elements)
        layout.addWidget(self.show_all_button)
        
        self.setLayout(layout)
        self.display_all_elements()
    
    def search_element(self):
        query = self.search_input.text().strip().capitalize()
        if not query:
            self.display_all_elements()
            return
        
        found = []
        for symbol, element in PERIODIC_TABLE.items():
            if query.lower() in symbol.lower() or query.lower() in element.name.lower():
                found.append(element)
        
        self.display_elements(found)
    
    def display_all_elements(self):
        self.display_elements(PERIODIC_TABLE.values())
    
    def display_elements(self, elements):
        self.results_table.setRowCount(len(elements))
        for row, element in enumerate(elements):
            self.results_table.setItem(row, 0, QTableWidgetItem(element.symbol))
            self.results_table.setItem(row, 1, QTableWidgetItem(element.name))
            self.results_table.setItem(row, 2, QTableWidgetItem(str(element.atomic_number)))
            self.results_table.setItem(row, 3, QTableWidgetItem(f"{element.atomic_weight:.4f}"))
            self.results_table.setItem(row, 4, QTableWidgetItem(str(element.group)))
            self.results_table.setItem(row, 5, QTableWidgetItem(str(element.period)))
            self.results_table.setItem(row, 6, QTableWidgetItem(element.category))
        
        self.results_table.resizeColumnsToContents()
    
    def delete_selected(self):
        """Delete selected elements from the table view (does not affect actual data)"""
        selected = self.results_table.selectedItems()
        if not selected:
            return
        
        rows = {item.row() for item in selected}
        for row in sorted(rows, reverse=True):
            self.results_table.removeRow(row)
    
    def refresh_table(self):
        """Refresh the table view"""
        self.search_input.clear()
        self.display_all_elements()

class ReactionTab(QWidget):
    """Tab for chemical reaction analysis"""
    def __init__(self):
        super().__init__()
        self.current_reaction = None
        self.init_ui()
    
    def init_ui(self):
        main_layout = QHBoxLayout()
        
        # Left side - Reaction input
        left_layout = QVBoxLayout()
        
        # Reaction name
        name_layout = QHBoxLayout()
        name_layout.addWidget(QLabel("Reaction Name:"))
        self.reaction_name = QLineEdit()
        self.reaction_name.setPlaceholderText("Enter reaction name")
        name_layout.addWidget(self.reaction_name)
        left_layout.addLayout(name_layout)
        
        # Reactants input
        reactants_group = QGroupBox("Reactants")
        reactants_layout = QVBoxLayout()
        
        self.reactants_table = QTableWidget()
        self.reactants_table.setColumnCount(3)
        self.reactants_table.setHorizontalHeaderLabels(["Formula", "Coefficient", ""])
        self.reactants_table.setRowCount(3)
        
        # Add delete buttons to each row
        for row in range(self.reactants_table.rowCount()):
            self.add_delete_button(row, self.reactants_table)
        
        reactants_layout.addWidget(self.reactants_table)
        
        add_reactant_btn = QPushButton("Add Reactant")
        add_reactant_btn.clicked.connect(lambda: self.add_row_with_delete(self.reactants_table))
        reactants_layout.addWidget(add_reactant_btn)
        
        reactants_group.setLayout(reactants_layout)
        left_layout.addWidget(reactants_group)
        
        # Products input
        products_group = QGroupBox("Products")
        products_layout = QVBoxLayout()
        
        self.products_table = QTableWidget()
        self.products_table.setColumnCount(3)
        self.products_table.setHorizontalHeaderLabels(["Formula", "Coefficient", ""])
        self.products_table.setRowCount(2)
        
        # Add delete buttons to each row
        for row in range(self.products_table.rowCount()):
            self.add_delete_button(row, self.products_table)
        
        products_layout.addWidget(self.products_table)
        
        add_product_btn = QPushButton("Add Product")
        add_product_btn.clicked.connect(lambda: self.add_row_with_delete(self.products_table))
        products_layout.addWidget(add_product_btn)
        
        products_group.setLayout(products_layout)
        left_layout.addWidget(products_group)
        
        # Buttons
        button_layout = QHBoxLayout()
        self.create_reaction_btn = QPushButton("Create Reaction")
        self.create_reaction_btn.clicked.connect(self.create_reaction)
        button_layout.addWidget(self.create_reaction_btn)
        
        self.balance_btn = QPushButton("Balance Equation")
        self.balance_btn.clicked.connect(self.balance_equation)
        self.balance_btn.setEnabled(False)
        button_layout.addWidget(self.balance_btn)
        
        self.refresh_btn = QPushButton("Refresh")
        self.refresh_btn.clicked.connect(self.refresh_tables)
        button_layout.addWidget(self.refresh_btn)
        
        left_layout.addLayout(button_layout)
        
        # Right side - Results and visualization
        right_layout = QVBoxLayout()
        
        # Equation display
        self.equation_display = QTextEdit()
        self.equation_display.setReadOnly(True)
        self.equation_display.setPlaceholderText("Balanced equation will appear here")
        right_layout.addWidget(self.equation_display)
        
        # Stoichiometry section
        stoichiometry_group = QGroupBox("Stoichiometry Calculator")
        stoichiometry_layout = QVBoxLayout()
        
        # Quantity inputs
        quantities_layout = QVBoxLayout()
        self.quantities_table = QTableWidget()
        self.quantities_table.setColumnCount(4)
        self.quantities_table.setHorizontalHeaderLabels(["Species", "Amount", "Unit", ""])
        self.quantities_table.setRowCount(0)
        
        # Add delete buttons to each row
        for row in range(self.quantities_table.rowCount()):
            self.add_delete_button(row, self.quantities_table, 3)
        
        stoichiometry_layout.addWidget(self.quantities_table)
        
        # Unit selector
        unit_layout = QHBoxLayout()
        unit_layout.addWidget(QLabel("Unit:"))
        self.unit_combo = QComboBox()
        self.unit_combo.addItems(["g", "mol"])
        unit_layout.addWidget(self.unit_combo)
        stoichiometry_layout.addLayout(unit_layout)
        
        # Calculate button
        self.calculate_btn = QPushButton("Calculate Stoichiometry")
        self.calculate_btn.clicked.connect(self.calculate_stoichiometry)
        self.calculate_btn.setEnabled(False)
        stoichiometry_layout.addWidget(self.calculate_btn)
        
        # Results display
        self.stoich_results = QTextEdit()
        self.stoich_results.setReadOnly(True)
        stoichiometry_layout.addWidget(self.stoich_results)
        
        stoichiometry_group.setLayout(stoichiometry_layout)
        right_layout.addWidget(stoichiometry_group)
        
        # Plot area
        self.plot_canvas = MplCanvas(self, width=5, height=4, dpi=100)
        right_layout.addWidget(self.plot_canvas)
        
        main_layout.addLayout(left_layout)
        main_layout.addLayout(right_layout)
        
        self.setLayout(main_layout)
    
    def add_row_with_delete(self, table):
        """Add a new row with a delete button to the specified table"""
        row = table.rowCount()
        table.insertRow(row)
        self.add_delete_button(row, table)
    
    def add_delete_button(self, row, table, column=2):
        """Add a delete button to the specified row and column of the table"""
        delete_btn = QPushButton("Delete")
        delete_btn.clicked.connect(lambda: self.delete_row(row, table))
        table.setCellWidget(row, column, delete_btn)
    
    def delete_row(self, row, table):
        """Delete the specified row from the table"""
        table.removeRow(row)
        # Reassign delete button signals for remaining rows
        for r in range(row, table.rowCount()):
            btn = table.cellWidget(r, 2)
            if btn:
                btn.clicked.disconnect()
                btn.clicked.connect(lambda _, r=r: self.delete_row(r, table))
    
    def refresh_tables(self):
        """Refresh all tables and clear results"""
        self.reactants_table.setRowCount(3)
        self.products_table.setRowCount(2)
        self.quantities_table.setRowCount(0)
        self.equation_display.clear()
        self.stoich_results.clear()
        self.plot_canvas.axes.clear()
        self.plot_canvas.draw()
        self.current_reaction = None
        self.balance_btn.setEnabled(False)
        self.calculate_btn.setEnabled(False)
        
        # Re-add delete buttons
        for row in range(self.reactants_table.rowCount()):
            self.add_delete_button(row, self.reactants_table)
        
        for row in range(self.products_table.rowCount()):
            self.add_delete_button(row, self.products_table)
    
    def create_reaction(self):
        try:
            # Get reactants
            reactants = {}
            for row in range(self.reactants_table.rowCount()):
                formula_item = self.reactants_table.item(row, 0)
                coeff_item = self.reactants_table.item(row, 1)
                
                if formula_item and coeff_item:
                    formula = formula_item.text().strip()
                    try:
                        coeff = int(coeff_item.text())
                    except ValueError:
                        coeff = 1
                    
                    if formula:
                        reactants[formula] = coeff
            
            # Get products
            products = {}
            for row in range(self.products_table.rowCount()):
                formula_item = self.products_table.item(row, 0)
                coeff_item = self.products_table.item(row, 1)
                
                if formula_item and coeff_item:
                    formula = formula_item.text().strip()
                    try:
                        coeff = int(coeff_item.text())
                    except ValueError:
                        coeff = 1
                    
                    if formula:
                        products[formula] = coeff
            
            if not reactants or not products:
                raise ValueError("Must have at least one reactant and one product")
            
            # Create reaction
            name = self.reaction_name.text().strip() or "Unnamed Reaction"
            self.current_reaction = Reaction(reactants, products, name)
            
            # Update UI
            self.equation_display.setPlainText(self.current_reaction.display_equation())
            self.balance_btn.setEnabled(True)
            self.calculate_btn.setEnabled(True)
            
            # Populate quantities table
            self.quantities_table.setRowCount(len(reactants))
            for row, (formula, coeff) in enumerate(reactants.items()):
                self.quantities_table.setItem(row, 0, QTableWidgetItem(formula))
                self.quantities_table.setItem(row, 1, QTableWidgetItem("0.0"))
                self.quantities_table.setItem(row, 2, QTableWidgetItem("g"))
                self.add_delete_button(row, self.quantities_table, 3)
            
        except Exception as e:
            self.equation_display.setPlainText(f"Error: {str(e)}")
    
    def balance_equation(self):
        if self.current_reaction:
            try:
                self.current_reaction.balance_equation()
                self.equation_display.setPlainText(self.current_reaction.display_equation())
                
                # Update tables with balanced coefficients
                for row in range(self.reactants_table.rowCount()):
                    formula_item = self.reactants_table.item(row, 0)
                    if formula_item:
                        formula = formula_item.text().strip()
                        if formula in self.current_reaction.reactants:
                            coeff = self.current_reaction.reactants[formula]
                            self.reactants_table.setItem(row, 1, QTableWidgetItem(str(coeff)))
                
                for row in range(self.products_table.rowCount()):
                    formula_item = self.products_table.item(row, 0)
                    if formula_item:
                        formula = formula_item.text().strip()
                        if formula in self.current_reaction.products:
                            coeff = self.current_reaction.products[formula]
                            self.products_table.setItem(row, 1, QTableWidgetItem(str(coeff)))
                
            except Exception as e:
                self.equation_display.setPlainText(f"Error balancing equation: {str(e)}")
    
    def calculate_stoichiometry(self):
        if not self.current_reaction:
            return
        
        try:
            # Get measured quantities
            measured = {}
            for row in range(self.quantities_table.rowCount()):
                species_item = self.quantities_table.item(row, 0)
                amount_item = self.quantities_table.item(row, 1)
                unit_item = self.quantities_table.item(row, 2)
                
                if species_item and amount_item and unit_item:
                    species = species_item.text().strip()
                    try:
                        amount = float(amount_item.text())
                    except ValueError:
                        amount = 0.0
                    unit = unit_item.text().strip() or "g"
                    
                    if species:
                        measured[species] = amount
            
            unit = self.unit_combo.currentText()
            result = self.current_reaction.stoichiometry(measured, unit)
            
            # Display results
            limiting, factor = result["limiting_reagent"]
            output = [f"Limiting Reagent: {limiting} (reaction proceeds {factor:.2f} times)"]
            output.append("\nTheoretical Yields:")
            
            for key, (yield_mol, coeff) in result.items():
                if key.endswith("_theoretical_mol"):
                    product = key.replace("_theoretical_mol", "")
                    mass = yield_mol * self.current_reaction.molar_mass(product)
                    output.append(f"- {product}: {yield_mol:.2f} mol ({mass:.2f} g)")
            
            self.stoich_results.setPlainText("\n".join(output))
            
            # Plot results
            self.plot_stoichiometry(result)
            
        except Exception as e:
            self.stoich_results.setPlainText(f"Error in calculation: {str(e)}")
    
    def plot_stoichiometry(self, result):
        """Plot stoichiometry results"""
        species = [k.replace("_avail", "") for k in result if k.endswith("_avail")]
        avail = [result[f"{s}_avail"][0] for s in species]
        needed = [result[f"{s}_avail"][1] for s in species]
        
        self.plot_canvas.axes.clear()
        
        x = range(len(species))
        width = 0.35
        self.plot_canvas.axes.bar([i - width/2 for i in x], avail, width, label='Available')
        self.plot_canvas.axes.bar([i + width/2 for i in x], needed, width, label='Required')
        
        self.plot_canvas.axes.set_xlabel('Reactants')
        self.plot_canvas.axes.set_ylabel('Moles')
        self.plot_canvas.axes.set_title('Available vs. Required Mole Ratios')
        self.plot_canvas.axes.set_xticks(x)
        self.plot_canvas.axes.set_xticklabels(species)
        self.plot_canvas.axes.legend()
        
        self.plot_canvas.draw()

class GasLawsTab(QWidget):
    """Tab for gas law calculations"""
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Law selection
        law_layout = QHBoxLayout()
        law_layout.addWidget(QLabel("Gas Law:"))
        self.law_combo = QComboBox()
        self.law_combo.addItems(["Boyle's Law", "Ideal Gas Law"])
        self.law_combo.currentIndexChanged.connect(self.update_input_fields)
        law_layout.addWidget(self.law_combo)
        
        # Add refresh button
        self.refresh_button = QPushButton("Refresh")
        self.refresh_button.clicked.connect(self.refresh_inputs)
        law_layout.addWidget(self.refresh_button)
        
        layout.addLayout(law_layout)
        
        # Input fields (dynamically updated)
        self.input_group = QGroupBox("Input Parameters")
        self.input_layout = QVBoxLayout()
        self.input_group.setLayout(self.input_layout)
        layout.addWidget(self.input_group)
        
        # Result display
        self.result_display = QLabel("Result will appear here")
        self.result_display.setAlignment(Qt.AlignCenter)
        self.result_display.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(self.result_display)
        
        # Calculate button
        self.calculate_btn = QPushButton("Calculate")
        self.calculate_btn.clicked.connect(self.calculate)
        layout.addWidget(self.calculate_btn)
        
        self.setLayout(layout)
        self.update_input_fields()
    
    def update_input_fields(self):
        """Update input fields based on selected gas law"""
        # Clear existing widgets
        for i in reversed(range(self.input_layout.count())): 
            self.input_layout.itemAt(i).widget().setParent(None)
        
        law = self.law_combo.currentText()
        
        if law == "Boyle's Law":
            # Boyle's Law: P1V1 = P2V2
            self.input_layout.addWidget(QLabel("Initial Pressure (P1, atm):"))
            self.p1_input = QDoubleSpinBox()
            self.p1_input.setRange(0.01, 1000)
            self.p1_input.setValue(1.0)
            self.input_layout.addWidget(self.p1_input)
            
            self.input_layout.addWidget(QLabel("Initial Volume (V1, L):"))
            self.v1_input = QDoubleSpinBox()
            self.v1_input.setRange(0.01, 1000)
            self.v1_input.setValue(1.0)
            self.input_layout.addWidget(self.v1_input)
            
            self.input_layout.addWidget(QLabel("Find:"))
            self.variable_combo = QComboBox()
            self.variable_combo.addItems(["Final Pressure (P2)", "Final Volume (V2)"])
            self.input_layout.addWidget(self.variable_combo)
            
            self.input_layout.addWidget(QLabel("Value:"))
            self.value_input = QDoubleSpinBox()
            self.value_input.setRange(0.01, 1000)
            self.value_input.setValue(2.0)
            self.input_layout.addWidget(self.value_input)
            
        elif law == "Ideal Gas Law":
            # Ideal Gas Law: PV = nRT
            self.input_layout.addWidget(QLabel("Find:"))
            self.variable_combo = QComboBox()
            self.variable_combo.addItems(["Pressure (P)", "Volume (V)", "Moles (n)", "Temperature (T)"])
            self.input_layout.addWidget(self.variable_combo)
            
            # Other inputs will be shown/hidden based on selection
            self.p_input = QDoubleSpinBox()
            self.p_input.setRange(0.01, 1000)
            self.p_input.setValue(1.0)
            
            self.v_input = QDoubleSpinBox()
            self.v_input.setRange(0.01, 1000)
            self.v_input.setValue(22.4)
            
            self.n_input = QDoubleSpinBox()
            self.n_input.setRange(0.001, 1000)
            self.n_input.setValue(1.0)
            
            self.t_input = QDoubleSpinBox()
            self.t_input.setRange(0.01, 1000)
            self.t_input.setValue(273.15)
            
            self.input_layout.addWidget(QLabel("Pressure (P, atm):"))
            self.input_layout.addWidget(self.p_input)
            
            self.input_layout.addWidget(QLabel("Volume (V, L):"))
            self.input_layout.addWidget(self.v_input)
            
            self.input_layout.addWidget(QLabel("Moles (n, mol):"))
            self.input_layout.addWidget(self.n_input)
            
            self.input_layout.addWidget(QLabel("Temperature (T, K):"))
            self.input_layout.addWidget(self.t_input)
            
            # Hide all initially, will be shown based on selection
            self.p_input.hide()
            self.v_input.hide()
            self.n_input.hide()
            self.t_input.hide()
            
            self.variable_combo.currentIndexChanged.connect(self.update_ideal_gas_inputs)
            self.update_ideal_gas_inputs()
    
    def update_ideal_gas_inputs(self):
        """Show/hide inputs for ideal gas law based on what we're solving for"""
        variable = self.variable_combo.currentText()
        
        # Hide all first
        self.p_input.hide()
        self.v_input.hide()
        self.n_input.hide()
        self.t_input.hide()
        
        # Then show the ones we need
        if variable != "Pressure (P)":
            self.p_input.show()
        if variable != "Volume (V)":
            self.v_input.show()
        if variable != "Moles (n)":
            self.n_input.show()
        if variable != "Temperature (T)":
            self.t_input.show()
    
    def calculate(self):
        """Perform the selected gas law calculation"""
        law = self.law_combo.currentText()
        
        try:
            if law == "Boyle's Law":
                p1 = self.p1_input.value()
                v1 = self.v1_input.value()
                value = self.value_input.value()
                
                if self.variable_combo.currentText() == "Final Pressure (P2)":
                    v2 = value
                    result = GasLaws.boyle(p1, v1, V2=v2)
                    self.result_display.setText(f"Final Pressure (P2): {result:.2f} atm")
                else:
                    p2 = value
                    result = GasLaws.boyle(p1, v1, P2=p2)
                    self.result_display.setText(f"Final Volume (V2): {result:.2f} L")
            
            elif law == "Ideal Gas Law":
                variable = self.variable_combo.currentText()
                
                if variable == "Pressure (P)":
                    v = self.v_input.value()
                    n = self.n_input.value()
                    t = self.t_input.value()
                    result = GasLaws.ideal_gas(V=v, n=n, T=t)
                    self.result_display.setText(f"Pressure (P): {result:.2f} atm")
                elif variable == "Volume (V)":
                    p = self.p_input.value()
                    n = self.n_input.value()
                    t = self.t_input.value()
                    result = GasLaws.ideal_gas(P=p, n=n, T=t)
                    self.result_display.setText(f"Volume (V): {result:.2f} L")
                elif variable == "Moles (n)":
                    p = self.p_input.value()
                    v = self.v_input.value()
                    t = self.t_input.value()
                    result = GasLaws.ideal_gas(P=p, V=v, T=t)
                    self.result_display.setText(f"Moles (n): {result:.4f} mol")
                elif variable == "Temperature (T)":
                    p = self.p_input.value()
                    v = self.v_input.value()
                    n = self.n_input.value()
                    result = GasLaws.ideal_gas(P=p, V=v, n=n)
                    self.result_display.setText(f"Temperature (T): {result:.2f} K")
        
        except Exception as e:
            self.result_display.setText(f"Error: {str(e)}")
    
    def refresh_inputs(self):
        """Refresh all input fields"""
        self.update_input_fields()
        self.result_display.setText("Result will appear here")

class MeasurementTab(QWidget):
    """Tab for recording and visualizing measurements"""
    def __init__(self):
        super().__init__()
        self.measurements = []
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Measurement input section
        input_group = QGroupBox("Record Measurement")
        input_layout = QVBoxLayout()
        
        # Variable name
        var_layout = QHBoxLayout()
        var_layout.addWidget(QLabel("Variable:"))
        self.var_input = QLineEdit()
        self.var_input.setPlaceholderText("e.g., Temperature, Pressure")
        var_layout.addWidget(self.var_input)
        input_layout.addLayout(var_layout)
        
        # Value and unit
        value_layout = QHBoxLayout()
        value_layout.addWidget(QLabel("Value:"))
        self.value_input = QDoubleSpinBox()
        self.value_input.setRange(-10000, 10000)
        value_layout.addWidget(self.value_input)
        
        value_layout.addWidget(QLabel("Unit:"))
        self.unit_input = QLineEdit()
        self.unit_input.setPlaceholderText("e.g., K, atm")
        value_layout.addWidget(self.unit_input)
        input_layout.addLayout(value_layout)
        
        # Notes
        notes_layout = QHBoxLayout()
        notes_layout.addWidget(QLabel("Notes:"))
        self.notes_input = QLineEdit()
        self.notes_input.setPlaceholderText("Optional notes")
        notes_layout.addWidget(self.notes_input)
        input_layout.addLayout(notes_layout)
        
        # Record button
        self.record_btn = QPushButton("Record Measurement")
        self.record_btn.clicked.connect(self.record_measurement)
        input_layout.addWidget(self.record_btn)
        
        input_group.setLayout(input_layout)
        layout.addWidget(input_group)
        
        # Measurements table
        self.measurements_table = QTableWidget()
        self.measurements_table.setColumnCount(6)
        self.measurements_table.setHorizontalHeaderLabels(["", "Timestamp", "Variable", "Value", "Unit", "Notes"])
        self.measurements_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.measurements_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.measurements_table)
        
        # Button controls
        button_controls = QHBoxLayout()
        
        # Delete selected button
        self.delete_btn = QPushButton("Delete Selected")
        self.delete_btn.clicked.connect(self.delete_selected_measurements)
        button_controls.addWidget(self.delete_btn)
        
        # Refresh button
        self.refresh_btn = QPushButton("Refresh")
        self.refresh_btn.clicked.connect(self.refresh_measurements)
        button_controls.addWidget(self.refresh_btn)
        
        layout.addLayout(button_controls)
        
        # Plot controls
        plot_controls = QHBoxLayout()
        
        # Variable selection for plotting
        plot_controls.addWidget(QLabel("Plot Variable:"))
        self.plot_var_combo = QComboBox()
        plot_controls.addWidget(self.plot_var_combo)
        
        # Plot button
        self.plot_btn = QPushButton("Plot Data")
        self.plot_btn.clicked.connect(self.plot_measurements)
        plot_controls.addWidget(self.plot_btn)
        
        # Export button
        self.export_btn = QPushButton("Export Data")
        self.export_btn.clicked.connect(self.export_data)
        plot_controls.addWidget(self.export_btn)
        
        layout.addLayout(plot_controls)
        
        # Plot area
        self.plot_canvas = MplCanvas(self, width=5, height=4, dpi=100)
        layout.addWidget(self.plot_canvas)
        
        self.setLayout(layout)
    
    def record_measurement(self):
        """Record a new measurement"""
        try:
            variable = self.var_input.text().strip()
            value = self.value_input.value()
            unit = self.unit_input.text().strip()
            notes = self.notes_input.text().strip()
            
            if not variable:
                raise ValueError("Variable name is required")
            if not unit:
                raise ValueError("Unit is required")
            
            measurement = Measurement(
                timestamp=datetime.now(),
                variable=variable,
                value=value,
                unit=unit,
                notes=notes
            )
            
            self.measurements.append(measurement)
            self.update_measurements_table()
            self.update_plot_variables()
            
            # Clear inputs
            self.var_input.clear()
            self.value_input.setValue(0.0)
            self.unit_input.clear()
            self.notes_input.clear()
            
        except Exception as e:
            QMessageBox.warning(self, "Error", str(e))
    
    def update_measurements_table(self):
        """Update the measurements table with current data"""
        self.measurements_table.setRowCount(len(self.measurements))
        
        for row, m in enumerate(self.measurements):
            # Add delete checkbox
            chk = QTableWidgetItem()
            chk.setCheckState(Qt.Unchecked)
            self.measurements_table.setItem(row, 0, chk)
            
            self.measurements_table.setItem(row, 1, QTableWidgetItem(m.timestamp.strftime("%Y-%m-%d %H:%M:%S")))
            self.measurements_table.setItem(row, 2, QTableWidgetItem(m.variable))
            self.measurements_table.setItem(row, 3, QTableWidgetItem(f"{m.value:.4f}"))
            self.measurements_table.setItem(row, 4, QTableWidgetItem(m.unit))
            self.measurements_table.setItem(row, 5, QTableWidgetItem(m.notes))
    
    def update_plot_variables(self):
        """Update the plot variable combo box with available variables"""
        current_var = self.plot_var_combo.currentText()
        variables = sorted({m.variable for m in self.measurements})
        
        self.plot_var_combo.clear()
        self.plot_var_combo.addItems(variables)
        
        # Try to restore previous selection
        if current_var in variables:
            self.plot_var_combo.setCurrentText(current_var)
    
    def delete_selected_measurements(self):
        """Delete measurements that are checked in the table"""
        rows_to_delete = []
        for row in range(self.measurements_table.rowCount()):
            if self.measurements_table.item(row, 0).checkState() == Qt.Checked:
                rows_to_delete.append(row)
        
        # Delete from highest to lowest to maintain correct indices
        for row in sorted(rows_to_delete, reverse=True):
            if row < len(self.measurements):
                del self.measurements[row]
        
        self.update_measurements_table()
        self.update_plot_variables()
    
    def refresh_measurements(self):
        """Refresh the measurements display"""
        self.update_measurements_table()
        self.plot_canvas.axes.clear()
        self.plot_canvas.draw()
    
    def plot_measurements(self):
        """Plot the selected measurement data"""
        variable = self.plot_var_combo.currentText()
        if not variable:
            return
        
        # Filter measurements for the selected variable
        data = [(m.timestamp, m.value) for m in self.measurements if m.variable == variable]
        if not data:
            return
        
        timestamps, values = zip(*sorted(data))
        
        self.plot_canvas.axes.clear()
        self.plot_canvas.axes.plot(timestamps, values, 'o-')
        self.plot_canvas.axes.set_xlabel('Time')
        self.plot_canvas.axes.set_ylabel(f"{variable} ({self.measurements[0].unit})")
        self.plot_canvas.axes.set_title(f"Time Series of {variable}")
        self.plot_canvas.axes.grid(True)
        
        # Rotate x-axis labels for better readability
        for label in self.plot_canvas.axes.get_xticklabels():
            label.set_rotation(45)
            label.set_ha('right')
        
        self.plot_canvas.draw()
    
    def export_data(self):
        """Export measurement data to CSV file"""
        if not self.measurements:
            QMessageBox.warning(self, "Error", "No data to export")
            return
        
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(
            self, "Save Measurements", "", "CSV Files (*.csv)", options=options)
        
        if file_name:
            try:
                with open(file_name, 'w', newline='') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(["Timestamp", "Variable", "Value", "Unit", "Notes"])
                    
                    for m in self.measurements:
                        writer.writerow([
                            m.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                            m.variable,
                            m.value,
                            m.unit,
                            m.notes
                        ])
                
                QMessageBox.information(self, "Success", "Data exported successfully")
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Failed to export data: {str(e)}")

class MainWindow(QMainWindow):
    """Main application window with tabs"""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Chemistry Toolkit")
        self.setGeometry(100, 100, 1200, 800)
        
        # Create menu bar
        self.create_menu()
        
        # Create tabs
        self.tabs = QTabWidget()
        self.tabs.addTab(PeriodicTableTab(), "Periodic Table")
        self.tabs.addTab(ReactionTab(), "Reaction Analysis")
        self.tabs.addTab(GasLawsTab(), "Gas Laws")
        self.tabs.addTab(MeasurementTab(), "Measurements")
        self.tabs.addTab(TerminologyTab(), "Terminologies")
        
        self.setCentralWidget(self.tabs)
    
    def create_menu(self):
        """Create the menu bar with About action"""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu('File')
        
        exit_action = file_menu.addAction('Exit')
        exit_action.setShortcut('Ctrl+Q')
        exit_action.triggered.connect(self.close)
        
        # Help menu
        help_menu = menubar.addMenu('Help')
        
        about_action = help_menu.addAction('About')
        about_action.triggered.connect(self.show_about)
    
    def show_about(self):
        """Show the about dialog"""
        dialog = AboutDialog(self)
        dialog.exec_()

# ====================== Application Entry Point ======================
def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()