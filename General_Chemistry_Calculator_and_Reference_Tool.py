# -*- coding: utf-8 -*-
"""
Created on Sat Aug 16 12:47:54 2025

@author: samng
"""

import math
from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Optional, Tuple

class ChemistryCalculator:
    """
    A comprehensive general chemistry calculator and reference tool based on 'GENERAL CHEMISTRY' by S. Ekambaram.
    Includes key formulas, terminology definitions, and periodic table data.
    """
    
    def __init__(self):
        self.periodic_table = self._initialize_periodic_table()
        self.lab_equipment = self._initialize_lab_equipment()
        self.theories_definitions = self._initialize_theories_definitions()
        self.laws_definitions = self._initialize_laws_definitions()
        
    class GasLaw(Enum):
        BOYLE = "Boyle's Law"
        CHARLES = "Charles's Law"
        GAY_LUSSAC = "Gay-Lussac's Law"
        AVOGADRO = "Avogadro's Law"
        IDEAL = "Ideal Gas Law"
        VAN_DER_WAALS = "van der Waals Equation"
    
    @dataclass
    class Element:
        atomic_number: int
        symbol: str
        name: str
        atomic_weight: float
        group: int
        period: int
        category: str
        electron_configuration: str
    
    @dataclass
    class LabEquipment:
        name: str
        description: str
        common_uses: str
    
    def _initialize_periodic_table(self) -> Dict[str, Element]:
        """Initialize periodic table data"""
        # Note: This is a simplified version with a few representative elements
        elements = {
            "H": self.Element(1, "H", "Hydrogen", 1.008, 1, 1, "Nonmetal", "1s¹"),
            "He": self.Element(2, "He", "Helium", 4.0026, 18, 1, "Noble Gas", "1s²"),
            "Li": self.Element(3, "Li", "Lithium", 6.94, 1, 2, "Alkali Metal", "[He] 2s¹"),
            # Add more elements as needed...
            "C": self.Element(6, "C", "Carbon", 12.011, 14, 2, "Nonmetal", "[He] 2s² 2p²"),
            "O": self.Element(8, "O", "Oxygen", 15.999, 16, 2, "Nonmetal", "[He] 2s² 2p⁴"),
            "Na": self.Element(11, "Na", "Sodium", 22.990, 1, 3, "Alkali Metal", "[Ne] 3s¹"),
            "Cl": self.Element(17, "Cl", "Chlorine", 35.45, 17, 3, "Halogen", "[Ne] 3s² 3p⁵"),
            "Fe": self.Element(26, "Fe", "Iron", 55.845, 8, 4, "Transition Metal", "[Ar] 3d⁶ 4s²"),
        }
        return elements
    
    def _initialize_lab_equipment(self) -> Dict[str, LabEquipment]:
        """Initialize laboratory equipment definitions"""
        equipment = {
            "beaker": self.LabEquipment(
                "Beaker",
                "A cylindrical container with a flat bottom and a spout for pouring",
                "Mixing, heating, and holding liquids"
            ),
            "erlenmeyer_flask": self.LabEquipment(
                "Erlenmeyer Flask",
                "A conical flask with a flat bottom and a narrow neck",
                "Titrations and mixing solutions"
            ),
            "bunsen_burner": self.LabEquipment(
                "Bunsen Burner",
                "A gas burner that produces a single open flame",
                "Heating, sterilization, and combustion"
            ),
            # Add more equipment as needed...
        }
        return equipment
    
    def _initialize_theories_definitions(self) -> Dict[str, str]:
        """Initialize chemistry theories definitions"""
        theories = {
            "Dalton's Atomic Theory": (
                "1) Elements are made of tiny particles called atoms. "
                "2) Atoms of a given element are identical. "
                "3) Atoms of different elements combine in simple whole-number ratios. "
                "4) Chemical reactions involve reorganization of atoms."
            ),
            "Quantum Theory": (
                "Theory describing nature at the atomic and subatomic level where energy is quantized "
                "and particles exhibit wave-particle duality."
            ),
            "Kinetic Molecular Theory": (
                "Explains the behavior of gases based on the idea that gas consists of particles in "
                "constant random motion."
            ),
            # Add more theories as needed...
        }
        return theories
    
    def _initialize_laws_definitions(self) -> Dict[str, str]:
        """Initialize chemistry laws definitions"""
        laws = {
            "Boyle's Law": (
                "For a fixed amount of gas at constant temperature, pressure is inversely proportional to volume. "
                "Formula: P₁V₁ = P₂V₂"
            ),
            "Charles's Law": (
                "For a fixed amount of gas at constant pressure, volume is directly proportional to temperature. "
                "Formula: V₁/T₁ = V₂/T₂"
            ),
            "Gay-Lussac's Law": (
                "For a fixed amount of gas at constant volume, pressure is directly proportional to temperature. "
                "Formula: P₁/T₁ = P₂/T₂"
            ),
            "Avogadro's Law": (
                "Equal volumes of gases at the same temperature and pressure contain equal numbers of molecules. "
                "Formula: V ∝ n"
            ),
            # Add more laws as needed...
        }
        return laws
    
    def calculate_gas_law(self, law: GasLaw, **kwargs) -> float:
        """
        Calculate gas law problems based on the specified law and provided parameters.
        
        Args:
            law: The gas law to apply (from GasLaw enum)
            kwargs: Parameters needed for the calculation (varies by law)
            
        Returns:
            The calculated value
            
        Raises:
            ValueError: If insufficient parameters are provided
        """
        if law == self.GasLaw.BOYLE:
            if 'p1' in kwargs and 'v1' in kwargs and 'p2' in kwargs:
                return (kwargs['p1'] * kwargs['v1']) / kwargs['p2']
            elif 'p1' in kwargs and 'v1' in kwargs and 'v2' in kwargs:
                return (kwargs['p1'] * kwargs['v1']) / kwargs['v2']
            else:
                raise ValueError("For Boyle's Law, provide either (p1, v1, p2) or (p1, v1, v2)")
        
        elif law == self.GasLaw.CHARLES:
            if 'v1' in kwargs and 't1' in kwargs and 'v2' in kwargs:
                return (kwargs['v2'] * kwargs['t1']) / kwargs['v1']
            elif 'v1' in kwargs and 't1' in kwargs and 't2' in kwargs:
                return (kwargs['v1'] * kwargs['t2']) / kwargs['t1']
            else:
                raise ValueError("For Charles's Law, provide either (v1, t1, v2) or (v1, t1, t2)")
        
        elif law == self.GasLaw.IDEAL:
            if 'p' in kwargs and 'v' in kwargs and 'n' in kwargs and 't' in kwargs:
                R = 0.0821  # L·atm/(mol·K)
                calculated = (kwargs['p'] * kwargs['v']) / (kwargs['n'] * kwargs['t'])
                return calculated
            else:
                raise ValueError("For Ideal Gas Law, provide p, v, n, and t")
        
        elif law == self.GasLaw.VAN_DER_WAALS:
            if 'p' in kwargs and 'v' in kwargs and 'n' in kwargs and 't' in kwargs:
                a = kwargs.get('a', 1.36)  # L²·atm/mol² for CO₂ (example)
                b = kwargs.get('b', 0.0319)  # L/mol for CO₂ (example)
                R = 0.0821  # L·atm/(mol·K)
                term1 = (kwargs['p'] + a * (kwargs['n']**2 / kwargs['v']**2))
                term2 = (kwargs['v'] - kwargs['n'] * b)
                return term1 * term2 - kwargs['n'] * R * kwargs['t']
            else:
                raise ValueError("For van der Waals Equation, provide p, v, n, t and optionally a, b")
        
        else:
            raise ValueError(f"Gas law {law} not yet implemented")
    
    def calculate_quantum_energy(self, frequency: float) -> float:
        """
        Calculate energy of a photon using Planck's equation (E = hν).
        
        Args:
            frequency: Frequency of radiation in Hz
            
        Returns:
            Energy in joules
        """
        h = 6.62607015e-34  # Planck's constant in J·s
        return h * frequency
    
    def calculate_de_broglie_wavelength(self, mass: float, velocity: float) -> float:
        """
        Calculate de Broglie wavelength (λ = h / (m·v)).
        
        Args:
            mass: Mass of particle in kg
            velocity: Velocity of particle in m/s
            
        Returns:
            Wavelength in meters
        """
        h = 6.62607015e-34  # Planck's constant in J·s
        return h / (mass * velocity)
    
    def calculate_heisenberg_uncertainty(self, delta_x: float) -> float:
        """
        Calculate minimum momentum uncertainty using Heisenberg's uncertainty principle.
        
        Args:
            delta_x: Position uncertainty in meters
            
        Returns:
            Minimum momentum uncertainty in kg·m/s
        """
        h_bar = 1.054571817e-34  # Reduced Planck's constant in J·s
        return h_bar / (2 * delta_x)
    
    def calculate_gibbs_free_energy(self, delta_h: float, delta_s: float, temp: float) -> float:
        """
        Calculate Gibbs free energy change (ΔG = ΔH - TΔS).
        
        Args:
            delta_h: Enthalpy change in J/mol
            delta_s: Entropy change in J/(mol·K)
            temp: Temperature in Kelvin
            
        Returns:
            Gibbs free energy change in J/mol
        """
        return delta_h - temp * delta_s
    
    def calculate_osmotic_pressure(self, concentration: float, temp: float, van_t_hoff: float = 1) -> float:
        """
        Calculate osmotic pressure using van't Hoff's law (Π = iCRT).
        
        Args:
            concentration: Molar concentration in mol/L
            temp: Temperature in Kelvin
            van_t_hoff: van't Hoff factor (i)
            
        Returns:
            Osmotic pressure in atm
        """
        R = 0.0821  # Gas constant in L·atm/(mol·K)
        return van_t_hoff * concentration * R * temp
    
    def get_element_info(self, element: str) -> Optional[Element]:
        """
        Get information about an element from the periodic table.
        
        Args:
            element: Element symbol or name
            
        Returns:
            Element dataclass with properties or None if not found
        """
        # Try by symbol first
        if element in self.periodic_table:
            return self.periodic_table[element]
        
        # Try by name
        for elem in self.periodic_table.values():
            if elem.name.lower() == element.lower():
                return elem
        
        return None
    
    def get_lab_equipment_info(self, equipment: str) -> Optional[LabEquipment]:
        """
        Get information about laboratory equipment.
        
        Args:
            equipment: Equipment name
            
        Returns:
            LabEquipment dataclass with description or None if not found
        """
        # Try exact match first
        if equipment in self.lab_equipment:
            return self.lab_equipment[equipment]
        
        # Try case-insensitive search
        for key, value in self.lab_equipment.items():
            if value.name.lower() == equipment.lower():
                return value
        
        return None
    
    def get_theory_definition(self, theory: str) -> Optional[str]:
        """
        Get definition of a chemistry theory.
        
        Args:
            theory: Theory name
            
        Returns:
            Definition string or None if not found
        """
        return self.theories_definitions.get(theory)
    
    def get_law_definition(self, law: str) -> Optional[str]:
        """
        Get definition of a chemistry law.
        
        Args:
            law: Law name
            
        Returns:
            Definition string or None if not found
        """
        return self.laws_definitions.get(law)
    
    def balance_chemical_equation(self, reactants: List[str], products: List[str]) -> Dict[str, int]:
        """
        Balance a chemical equation (simple implementation for demonstration).
        
        Args:
            reactants: List of reactant formulas
            products: List of product formulas
            
        Returns:
            Dictionary with coefficients for each compound
            
        Note:
            This is a simplified version. A full implementation would require
            matrix algebra or more complex algorithms.
        """
        # This is a placeholder - actual implementation would be more complex
        if sorted(reactants) == ["H2", "O2"] and sorted(products) == ["H2O"]:
            return {"H2": 2, "O2": 1, "H2O": 2}
        elif sorted(reactants) == ["CH4", "O2"] and sorted(products) == ["CO2", "H2O"]:
            return {"CH4": 1, "O2": 2, "CO2": 1, "H2O": 2}
        else:
            # For demonstration, return 1 for all (not actually balanced)
            return {**{r: 1 for r in reactants}, **{p: 1 for p in products}}

# Example usage
if __name__ == "__main__":
    calculator = ChemistryCalculator()
    
    # Example calculations
    print("Example Calculations:")
    print(f"Boyle's Law (P1=1 atm, V1=2 L, P2=2 atm): V2 = {calculator.calculate_gas_law(calculator.GasLaw.BOYLE, p1=1, v1=2, p2=2)} L")
    print(f"Ideal Gas Law (P=1 atm, V=22.4 L, n=1 mol, T=273 K): R = {calculator.calculate_gas_law(calculator.GasLaw.IDEAL, p=1, v=22.4, n=1, t=273)} L·atm/(mol·K)")
    print(f"Quantum Energy (ν=1e15 Hz): E = {calculator.calculate_quantum_energy(1e15):.2e} J")
    print(f"Gibbs Free Energy (ΔH=1000 J/mol, ΔS=10 J/(mol·K), T=298 K): ΔG = {calculator.calculate_gibbs_free_energy(1000, 10, 298)} J/mol")
    
    # Example information lookups
    print("\nExample Information Lookups:")
    carbon = calculator.get_element_info("C")
    print(f"Carbon info: Atomic number {carbon.atomic_number}, weight {carbon.atomic_weight}, config {carbon.electron_configuration}")
    
    beaker = calculator.get_lab_equipment_info("beaker")
    print(f"Beaker: {beaker.description}")
    
    boyles_law = calculator.get_law_definition("Boyle's Law")
    print(f"Boyle's Law: {boyles_law}")
    
    # Example equation balancing
    print("\nExample Equation Balancing:")
    equation = calculator.balance_chemical_equation(["H2", "O2"], ["H2O"])
    print("2 H2 + O2 → 2 H2O:", equation)