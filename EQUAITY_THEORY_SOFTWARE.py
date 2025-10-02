from dataclasses import dataclass, asdict
from typing import Dict, List, Tuple, Optional, Any
import math
import json
import datetime
from datetime import datetime
import os

@dataclass
class BehavioralObservation:
    """Represents a behavioral observation with timestamp and impact."""
    id: str
    partner_id: str
    timestamp: datetime
    description: str
    category: str
    impact_type: str  # 'input' or 'outcome'
    impact_value: float
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert observation to dictionary for serialization."""
        return {
            'id': self.id,
            'partner_id': self.partner_id,
            'timestamp': self.timestamp.isoformat(),
            'description': self.description,
            'category': self.category,
            'impact_type': self.impact_type,
            'impact_value': self.impact_value
        }

@dataclass
class Partner:
    """Represents a relational partner with inputs and outcomes."""
    id: str
    name: str
    inputs: float
    outcomes: float

class EquityTheorySoftware:
    """
    Comprehensive Equity Theory Interpersonal Relations Management System
    with behavioral tracking and 10,000-word limit per observation.
    """
    
    # Behavioral categories for comprehensive analysis
    BEHAVIORAL_CATEGORIES = {
        'emotional_support': ['listening', 'empathy', 'comfort', 'encouragement', 'validation'],
        'practical_support': ['chores', 'errands', 'financial_help', 'transportation', 'technical_help'],
        'social_investment': ['time_together', 'shared_activities', 'social_events', 'family_interaction'],
        'communication': ['initiating_contact', 'conflict_resolution', 'deep_conversations', 'daily_checkins'],
        'personal_growth': ['career_support', 'skill_development', 'health_encouragement', 'goal_support'],
        'intimacy': ['physical_affection', 'emotional_vulnerability', 'trust_displays', 'personal_sharing']
    }
    
    def __init__(self):
        self.partners: List[Partner] = []
        self.observations: List[BehavioralObservation] = []
        self.data_file = "equity_theory_data.json"
        self.load_data()
    
    def generate_id(self) -> str:
        """Generate a unique ID for partners and observations."""
        return str(datetime.now().timestamp()).replace('.', '')
    
    def count_words(self, text: str) -> int:
        """Count words in a text string."""
        return len(text.split()) if text.strip() else 0
    
    def save_data(self):
        """Save all data to JSON file."""
        data = {
            'partners': [asdict(partner) for partner in self.partners],
            'observations': [obs.to_dict() for obs in self.observations]
        }
        with open(self.data_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def load_data(self):
        """Load data from JSON file."""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    data = json.load(f)
                
                # Load partners
                self.partners = [Partner(**partner_data) for partner_data in data.get('partners', [])]
                
                # Load observations
                self.observations = []
                for obs_data in data.get('observations', []):
                    # Convert timestamp string back to datetime object
                    obs_data['timestamp'] = datetime.fromisoformat(obs_data['timestamp'])
                    self.observations.append(BehavioralObservation(**obs_data))
                    
            except Exception as e:
                print(f"Error loading data: {e}")
    
    def add_partner(self, name: str, inputs: float, outcomes: float) -> Partner:
        """Add a new partner to the analysis."""
        partner = Partner(
            id=self.generate_id(),
            name=name,
            inputs=inputs,
            outcomes=outcomes
        )
        self.partners.append(partner)
        self.save_data()
        return partner
    
    def remove_partner(self, partner_id: str):
        """Remove a partner and all their observations."""
        self.partners = [p for p in self.partners if p.id != partner_id]
        self.observations = [obs for obs in self.observations if obs.partner_id != partner_id]
        self.save_data()
    
    def add_observation(self, partner_id: str, description: str, category: str, 
                       impact_type: str, impact_value: float) -> BehavioralObservation:
        """
        Add a behavioral observation with 10,000 word limit check.
        """
        # Check word count limit
        word_count = self.count_words(description)
        if word_count > 10000:
            raise ValueError(f"Observation description exceeds 10,000 word limit. Current: {word_count} words")
        
        observation = BehavioralObservation(
            id=self.generate_id(),
            partner_id=partner_id,
            timestamp=datetime.now(),
            description=description,
            category=category,
            impact_type=impact_type,
            impact_value=impact_value
        )
        self.observations.append(observation)
        self.save_data()
        return observation
    
    def remove_observation(self, observation_id: str):
        """Remove an observation."""
        self.observations = [obs for obs in self.observations if obs.id != observation_id]
        self.save_data()
    
    def get_partner_observations(self, partner_id: str) -> List[BehavioralObservation]:
        """Get all observations for a specific partner."""
        return [obs for obs in self.observations if obs.partner_id == partner_id]
    
    def calculate_equity_ratio(self, partner: Partner) -> float:
        """Compute the outcome/input ratio."""
        return partner.outcomes / partner.inputs if partner.inputs != 0 else float('inf')
    
    def calculate_from_observations(self, partner: Partner) -> Dict[str, Any]:
        """
        Calculate inputs and outcomes from behavioral observations.
        """
        partner_observations = self.get_partner_observations(partner.id)
        
        total_inputs = partner.inputs
        total_outcomes = partner.outcomes
        input_breakdown = {}
        outcome_breakdown = {}
        
        for obs in partner_observations:
            if obs.impact_type == 'input':
                total_inputs += obs.impact_value
                input_breakdown[obs.category] = input_breakdown.get(obs.category, 0) + obs.impact_value
            elif obs.impact_type == 'outcome':
                total_outcomes += obs.impact_value
                outcome_breakdown[obs.category] = outcome_breakdown.get(obs.category, 0) + obs.impact_value
        
        return {
            'total_inputs': total_inputs,
            'total_outcomes': total_outcomes,
            'calculated_ratio': total_outcomes / total_inputs if total_inputs != 0 else float('inf'),
            'input_breakdown': input_breakdown,
            'outcome_breakdown': outcome_breakdown
        }
    
    def equity_formula_calculation(self, a: Partner, b: Partner) -> Dict[str, float]:
        """
        Calculate equity using Walster & Walster (1975) formula.
        """
        diff_a = a.outcomes - a.inputs
        diff_b = b.outcomes - b.inputs
        
        k_a = 1 if diff_a >= 0 else -1
        k_b = 1 if diff_b >= 0 else -1
        
        denom_a = abs(a.inputs) ** k_a if a.inputs != 0 else float('inf')
        denom_b = abs(b.inputs) ** k_b if b.inputs != 0 else float('inf')
        
        left_side = diff_a / denom_a if denom_a != float('inf') else float('inf')
        right_side = diff_b / denom_b if denom_b != float('inf') else float('inf')
        
        return {
            "left_side": left_side,
            "right_side": right_side,
            "equitable": math.isclose(left_side, right_side, rel_tol=1e-6, abs_tol=1e-6),
            "k_a": k_a,
            "k_b": k_b,
            "difference_a": diff_a,
            "difference_b": diff_b
        }
    
    def adams_inequity_index(self, a: Partner, b: Partner) -> Dict[str, float]:
        """
        Adams (1965) Inequity Index calculation.
        """
        ratio_a = self.calculate_equity_ratio(a)
        ratio_b = self.calculate_equity_ratio(b)
        
        if ratio_b == 0 or ratio_a == float('inf') or ratio_b == float('inf'):
            inequity_index = float('inf')
        else:
            inequity_index = abs(ratio_a / ratio_b - 1)
        
        return {
            "inequity_index": inequity_index,
            "ratio_a": ratio_a,
            "ratio_b": ratio_b,
            "equity_status": "Equitable" if inequity_index < 0.1 else "Inequitable"
        }
    
    def hatfield_global_measure(self, partners: List[Partner]) -> Dict[str, Any]:
        """
        Hatfield's Global Equity Measure (Hatfield et al., 1979).
        """
        if len(partners) != 2:
            raise ValueError("Hatfield measure requires exactly 2 partners")
        
        a, b = partners[0], partners[1]
        ratio_a = self.calculate_equity_ratio(a)
        ratio_b = self.calculate_equity_ratio(b)
        
        if ratio_b == 0 or ratio_a == float('inf') or ratio_b == float('inf'):
            hatfield_score = 0
        else:
            relative_ratio = ratio_a / ratio_b
            
            if relative_ratio > 1.5:
                hatfield_score = -3  # I am getting much better deal
            elif relative_ratio > 1.2:
                hatfield_score = -2  # I am getting somewhat better deal
            elif relative_ratio > 1.05:
                hatfield_score = -1  # I am getting slightly better deal
            elif relative_ratio >= 0.95:
                hatfield_score = 0   # Equally good or bad deal
            elif relative_ratio > 0.8:
                hatfield_score = 1   # Partner getting slightly better deal
            elif relative_ratio > 0.67:
                hatfield_score = 2   # Partner getting somewhat better deal
            else:
                hatfield_score = 3   # Partner getting much better deal
        
        interpretations = {
            -3: "You are getting a MUCH BETTER deal",
            -2: "You are getting a SOMEWHAT BETTER deal", 
            -1: "You are getting a SLIGHTLY BETTER deal",
            0: "You are getting an EQUALLY GOOD or BAD deal",
            1: "Partner is getting a SLIGHTLY BETTER deal",
            2: "Partner is getting a SOMEWHAT BETTER deal",
            3: "Partner is getting a MUCH BETTER deal"
        }
        
        return {
            "hatfield_score": hatfield_score,
            "interpretation": interpretations.get(hatfield_score, "Unable to interpret")
        }
    
    def huseman_equity_sensitivity(self, partners: List[Partner]) -> Dict[str, Any]:
        """
        Equity Sensitivity Analysis based on Huseman et al. (1987).
        """
        if len(partners) < 2:
            raise ValueError("Need at least 2 partners for sensitivity analysis")
        
        ratios = [self.calculate_equity_ratio(p) for p in partners]
        valid_ratios = [r for r in ratios if r != float('inf')]
        mean_ratio = sum(valid_ratios) / len(valid_ratios) if valid_ratios else 1.0
        
        categories = []
        for i, (partner, ratio) in enumerate(zip(partners, ratios)):
            if ratio == float('inf'):
                category = "Undefined (Zero Inputs)"
                sensitivity_score = 0
            elif ratio < mean_ratio * 0.8:
                category = "Benevolent"
                sensitivity_score = -1
            elif ratio > mean_ratio * 1.2:
                category = "Entitled" 
                sensitivity_score = 1
            else:
                category = "Equity Sensitive"
                sensitivity_score = 0
            
            descriptions = {
                "Benevolent": "Prefers giving more than receiving, tolerant of underbenefit",
                "Equity Sensitive": "Prefers balanced exchange, follows traditional equity norms", 
                "Entitled": "Prefers receiving more than giving, seeks overbenefit",
                "Undefined (Zero Inputs)": "Cannot calculate due to zero inputs"
            }
            
            categories.append({
                "partner": partner.name,
                "ratio": ratio,
                "category": category,
                "sensitivity_score": sensitivity_score,
                "description": descriptions.get(category, "Unknown category")
            })
        
        return {
            "sensitivity_analysis": categories,
            "mean_reference_ratio": mean_ratio
        }
    
    def distributive_justice_index(self, partners: List[Partner]) -> Dict[str, float]:
        """
        Calculate Distributive Justice Index based on Deutsch (1985).
        """
        ratios = [self.calculate_equity_ratio(p) for p in partners]
        valid_ratios = [r for r in ratios if r != float('inf')]
        
        if not valid_ratios:
            return {"justice_index": 0, "status": "Undefined", "std_deviation": 0, "mean_ratio": 0}
        
        mean_ratio = sum(valid_ratios) / len(valid_ratios)
        variance = sum((r - mean_ratio) ** 2 for r in valid_ratios) / len(valid_ratios)
        std_dev = math.sqrt(variance)
        
        justice_index = 1.0 / (1.0 + std_dev)
        
        if justice_index > 0.9:
            status = "High Justice"
        elif justice_index > 0.7:
            status = "Moderate Justice" 
        elif justice_index > 0.5:
            status = "Low Justice"
        else:
            status = "Severe Injustice"
        
        return {
            "justice_index": justice_index,
            "status": status,
            "std_deviation": std_dev,
            "mean_ratio": mean_ratio
        }
    
    def relational_maintenance_predictor(self, partners: List[Partner]) -> Dict[str, Any]:
        """
        Predict relational maintenance based on equity (Canary & Stafford, 1992).
        """
        if len(partners) != 2:
            raise ValueError("This predictor requires exactly 2 partners")
        
        equity_result = self.equity_formula_calculation(partners[0], partners[1])
        hatfield_result = self.hatfield_global_measure(partners)
        
        if equity_result["equitable"]:
            maintenance_score = 90
            prediction = "High Maintenance Likely"
        else:
            hatfield_abs = abs(hatfield_result["hatfield_score"])
            maintenance_score = max(20, 80 - (hatfield_abs * 20))
            
            if maintenance_score > 70:
                prediction = "Moderate-High Maintenance"
            elif maintenance_score > 50:
                prediction = "Moderate Maintenance" 
            else:
                prediction = "Low Maintenance Likely"
        
        return {
            "maintenance_score": maintenance_score,
            "prediction": prediction,
            "equitable": equity_result["equitable"],
            "hatfield_score": hatfield_result["hatfield_score"]
        }
    
    def behavioral_analysis_report(self, partner: Partner = None) -> Dict[str, Any]:
        """
        Generate comprehensive behavioral analysis with timestamps.
        """
        report = {
            'generated_at': datetime.now().isoformat(),
            'behavioral_categories': self.BEHAVIORAL_CATEGORIES,
            'partner_analyses': []
        }
        
        partners_to_analyze = [partner] if partner else self.partners
        
        for partner in partners_to_analyze:
            partner_observations = self.get_partner_observations(partner.id)
            obs_calculation = self.calculate_from_observations(partner)
            
            category_summary = {}
            for obs in partner_observations:
                if obs.category not in category_summary:
                    category_summary[obs.category] = {'inputs': 0, 'outcomes': 0, 'count': 0}
                
                category_summary[obs.category][obs.impact_type + 's'] += obs.impact_value
                category_summary[obs.category]['count'] += 1
            
            recent_cutoff = datetime.now() - datetime.timedelta(days=30)
            recent_observations = [
                obs for obs in partner_observations 
                if obs.timestamp > recent_cutoff
            ]
            
            partner_analysis = {
                'name': partner.name,
                'base_inputs': partner.inputs,
                'base_outcomes': partner.outcomes,
                'calculated_from_observations': obs_calculation,
                'observation_count': len(partner_observations),
                'recent_observations_count': len(recent_observations),
                'category_breakdown': category_summary,
                'observations_timeline': [
                    {
                        'timestamp': obs.timestamp.isoformat(),
                        'description': obs.description,
                        'impact': f"{obs.impact_type}: {obs.impact_value}",
                        'category': obs.category,
                        'word_count': self.count_words(obs.description)
                    }
                    for obs in sorted(partner_observations, key=lambda x: x.timestamp, reverse=True)
                ]
            }
            
            report['partner_analyses'].append(partner_analysis)
        
        return report
    
    def comprehensive_analysis(self) -> Dict[str, Any]:
        """Run comprehensive equity analysis using all major models."""
        if len(self.partners) < 2:
            raise ValueError("Need at least 2 partners for analysis")
        
        results = {}
        
        results["individual_ratios"] = {
            p.name: self.calculate_equity_ratio(p) for p in self.partners
        }
        
        results["behavioral_analysis"] = self.behavioral_analysis_report()
        
        if len(self.partners) == 2:
            results["walster_formula"] = self.equity_formula_calculation(self.partners[0], self.partners[1])
            results["adams_inequity"] = self.adams_inequity_index(self.partners[0], self.partners[1])
            results["hatfield_measure"] = self.hatfield_global_measure(self.partners)
            results["maintenance_prediction"] = self.relational_maintenance_predictor(self.partners)
        
        results["huseman_sensitivity"] = self.huseman_equity_sensitivity(self.partners)
        results["distributive_justice"] = self.distributive_justice_index(self.partners)
        
        justice_index = results["distributive_justice"]["justice_index"]
        if justice_index > 0.8:
            overall = "Highly Equitable Relationship"
        elif justice_index > 0.6:
            overall = "Moderately Equitable Relationship"
        elif justice_index > 0.4:
            overall = "Somewhat Inequitable Relationship" 
        else:
            overall = "Highly Inequitable Relationship"
        
        results["overall_assessment"] = overall
        
        return results

# Command Line Interface
class EquityTheoryCLI:
    """Command Line Interface for the Equity Theory Software."""
    
    def __init__(self):
        self.software = EquityTheorySoftware()
        self.running = True
    
    def display_header(self):
        """Display application header."""
        print("=" * 70)
        print("EQUITY THEORY INTERPERSONAL RELATIONS MANAGEMENT SYSTEM")
        print("With Comprehensive Behavioral Observation Tracking")
        print("=" * 70)
    
    def display_menu(self):
        """Display main menu."""
        print("\nMAIN MENU:")
        print("1. Add Partner")
        print("2. View Partners")
        print("3. Add Behavioral Observation")
        print("4. View Observations")
        print("5. Run Comprehensive Analysis")
        print("6. Run Specific Calculation")
        print("7. Behavioral Analysis Report")
        print("8. Theory Summary")
        print("9. Exit")
    
    def add_partner(self):
        """Add a new partner."""
        print("\nADD NEW PARTNER:")
        name = input("Enter partner name: ").strip()
        
        try:
            inputs = float(input("Enter inputs (contributions): "))
            outcomes = float(input("Enter outcomes (rewards): "))
        except ValueError:
            print("Invalid input! Please enter numeric values.")
            return
        
        partner = self.software.add_partner(name, inputs, outcomes)
        print(f"✓ Added {name}: Inputs={inputs}, Outcomes={outcomes}")
        
        if input("Add behavioral observations now? (y/n): ").lower() == 'y':
            self.add_observation(partner.id)
    
    def view_partners(self):
        """Display all partners."""
        if not self.software.partners:
            print("No partners available.")
            return
        
        print("\nCURRENT PARTNERS:")
        print("-" * 50)
        for i, partner in enumerate(self.software.partners, 1):
            ratio = self.software.calculate_equity_ratio(partner)
            obs_count = len(self.software.get_partner_observations(partner.id))
            print(f"{i}. {partner.name}: Inputs={partner.inputs}, Outcomes={partner.outcomes}, Ratio={ratio:.3f}")
            print(f"   Observations: {obs_count} behavioral records")
            
            if obs_count > 0:
                recent_cutoff = datetime.now() - datetime.timedelta(days=30)
                recent_obs = [
                    obs for obs in self.software.get_partner_observations(partner.id)
                    if obs.timestamp > recent_cutoff
                ]
                print(f"   Recent (30 days): {len(recent_obs)} observations")
        
        if input("\nRemove a partner? (y/n): ").lower() == 'y':
            try:
                partner_idx = int(input("Enter partner number to remove: ")) - 1
                if 0 <= partner_idx < len(self.software.partners):
                    partner = self.software.partners[partner_idx]
                    if input(f"Are you sure you want to remove {partner.name}? (y/n): ").lower() == 'y':
                        self.software.remove_partner(partner.id)
                        print(f"✓ Removed {partner.name}")
            except (ValueError, IndexError):
                print("Invalid selection!")
    
    def add_observation(self, partner_id: str = None):
        """Add a behavioral observation."""
        if not self.software.partners:
            print("No partners available. Please add partners first.")
            return
        
        if partner_id is None:
            self.view_partners()
            try:
                partner_idx = int(input("Select partner number: ")) - 1
                partner_id = self.software.partners[partner_idx].id
            except (ValueError, IndexError):
                print("Invalid selection!")
                return
        
        print("\nADD BEHAVIORAL OBSERVATION:")
        print("Available categories:")
        for i, category in enumerate(self.software.BEHAVIORAL_CATEGORIES.keys(), 1):
            print(f"{i}. {category.replace('_', ' ').title()}")
        
        description = input("Observation description: ").strip()
        
        # Check word count
        word_count = self.software.count_words(description)
        print(f"Word count: {word_count}/10000")
        if word_count > 10000:
            print("Error: Observation exceeds 10,000 word limit!")
            return
        
        try:
            cat_choice = int(input("Category number: "))
            categories = list(self.software.BEHAVIORAL_CATEGORIES.keys())
            category = categories[cat_choice - 1] if 1 <= cat_choice <= len(categories) else "general"
        except (ValueError, IndexError):
            category = "general"
        
        impact_type = input("Impact type (input/outcome): ").strip().lower()
        if impact_type not in ['input', 'outcome']:
            impact_type = 'input'
        
        try:
            impact_value = float(input("Impact value (numeric): "))
        except ValueError:
            impact_value = 1.0
        
        try:
            observation = self.software.add_observation(partner_id, description, category, impact_type, impact_value)
            print(f"✓ Added observation for {self.software.partners[0].name}")
        except ValueError as e:
            print(f"Error: {e}")
    
    def view_observations(self):
        """Display all observations."""
        if not self.software.observations:
            print("No observations available.")
            return
        
        print("\nRECENT OBSERVATIONS:")
        print("-" * 60)
        
        sorted_obs = sorted(self.software.observations, key=lambda x: x.timestamp, reverse=True)
        
        for i, obs in enumerate(sorted_obs, 1):
            partner = next((p for p in self.software.partners if p.id == obs.partner_id), None)
            if not partner:
                continue
            
            date_str = obs.timestamp.strftime("%Y-%m-%d %H:%M")
            word_count = self.software.count_words(obs.description)
            
            print(f"{i}. [{date_str}] {partner.name} - {obs.category.replace('_', ' ').title()}")
            print(f"   {obs.description[:100]}{'...' if len(obs.description) > 100 else ''}")
            print(f"   Impact: {obs.impact_type} ({obs.impact_value}) | Words: {word_count}")
            print()
        
        if input("Remove an observation? (y/n): ").lower() == 'y':
            try:
                obs_idx = int(input("Enter observation number to remove: ")) - 1
                if 0 <= obs_idx < len(sorted_obs):
                    obs = sorted_obs[obs_idx]
                    if input("Are you sure? (y/n): ").lower() == 'y':
                        self.software.remove_observation(obs.id)
                        print("✓ Observation removed")
            except (ValueError, IndexError):
                print("Invalid selection!")
    
    def run_comprehensive_analysis(self):
        """Run comprehensive equity analysis."""
        try:
            results = self.software.comprehensive_analysis()
            
            print("\nCOMPREHENSIVE EQUITY ANALYSIS")
            print("=" * 50)
            
            print("\nINDIVIDUAL EQUITY RATIOS:")
            for name, ratio in results["individual_ratios"].items():
                print(f"  {name}: {ratio:.3f}")
            
            if len(self.software.partners) == 2:
                print("\nWALSTER FORMULA ANALYSIS:")
                formula = results["walster_formula"]
                print(f"  Left Side: {formula['left_side']:.3f}")
                print(f"  Right Side: {formula['right_side']:.3f}")
                print(f"  Equitable: {formula['equitable']}")
                
                print("\nADAMS INEQUITY INDEX:")
                adams = results["adams_inequity"]
                print(f"  Inequity Index: {adams['inequity_index']:.3f}")
                print(f"  Status: {adams['equity_status']}")
                
                print("\nHATFIELD GLOBAL MEASURE:")
                hatfield = results["hatfield_measure"]
                print(f"  Score: {hatfield['hatfield_score']}")
                print(f"  Interpretation: {hatfield['interpretation']}")
                
                print("\nRELATIONAL MAINTENANCE PREDICTION:")
                maintenance = results["maintenance_prediction"]
                print(f"  Score: {maintenance['maintenance_score']:.1f}/100")
                print(f"  Prediction: {maintenance['prediction']}")
            
            print("\nHUSEMAN EQUITY SENSITIVITY:")
            sensitivity = results["huseman_sensitivity"]
            for analysis in sensitivity["sensitivity_analysis"]:
                print(f"  {analysis['partner']}: {analysis['category']} - {analysis['description']}")
            
            print("\nDISTRIBUTIVE JUSTICE ANALYSIS:")
            justice = results["distributive_justice"]
            print(f"  Justice Index: {justice['justice_index']:.3f}")
            print(f"  Status: {justice['status']}")
            print(f"  Standard Deviation: {justice['std_deviation']:.3f}")
            
            print(f"\nOVERALL ASSESSMENT: {results['overall_assessment']}")
            
        except ValueError as e:
            print(f"Error: {e}")
    
    def run_specific_calculation(self):
        """Run a specific equity theory calculation."""
        if len(self.software.partners) < 2:
            print("Need at least 2 partners!")
            return
        
        print("\nSPECIFIC CALCULATIONS:")
        print("1. Walster Formula Calculator")
        print("2. Adams Inequity Index") 
        print("3. Hatfield Global Measure")
        print("4. Huseman Sensitivity Analysis")
        print("5. Distributive Justice Index")
        print("6. Relational Maintenance Predictor")
        
        try:
            choice = int(input("Select calculation (1-6): "))
        except ValueError:
            print("Invalid choice!")
            return
        
        partner_a, partner_b = self.software.partners[0], self.software.partners[1]
        
        if choice == 1:
            result = self.software.equity_formula_calculation(partner_a, partner_b)
            print(f"\nWALSTER FORMULA RESULTS:")
            print(f"Left Side (A): {result['left_side']:.3f}")
            print(f"Right Side (B): {result['right_side']:.3f}")
            print(f"Equitable: {result['equitable']}")
            print(f"k Values: A={result['k_a']}, B={result['k_b']}")
            
        elif choice == 2:
            result = self.software.adams_inequity_index(partner_a, partner_b)
            print(f"\nADAMS INEQUITY INDEX:")
            print(f"Inequity Index: {result['inequity_index']:.3f}")
            print(f"Ratio A: {result['ratio_a']:.3f}")
            print(f"Ratio B: {result['ratio_b']:.3f}") 
            print(f"Status: {result['equity_status']}")
            
        elif choice == 3:
            result = self.software.hatfield_global_measure([partner_a, partner_b])
            print(f"\nHATFIELD GLOBAL MEASURE:")
            print(f"Score: {result['hatfield_score']}")
            print(f"Interpretation: {result['interpretation']}")
            
        elif choice == 4:
            result = self.software.huseman_equity_sensitivity(self.software.partners)
            print(f"\nHUSEMAN EQUITY SENSITIVITY:")
            for analysis in result["sensitivity_analysis"]:
                print(f"{analysis['partner']}: {analysis['category']} (Ratio: {analysis['ratio']:.3f})")
                print(f"  Description: {analysis['description']}")
                
        elif choice == 5:
            result = self.software.distributive_justice_index(self.software.partners)
            print(f"\nDISTRIBUTIVE JUSTICE INDEX:")
            print(f"Justice Index: {result['justice_index']:.3f}")
            print(f"Status: {result['status']}")
            print(f"Standard Deviation: {result['std_deviation']:.3f}")
            
        elif choice == 6:
            result = self.software.relational_maintenance_predictor([partner_a, partner_b])
            print(f"\nRELATIONAL MAINTENANCE PREDICTION:")
            print(f"Maintenance Score: {result['maintenance_score']:.1f}/100")
            print(f"Prediction: {result['prediction']}")
            print(f"Equitable: {result['equitable']}")
            
        else:
            print("Invalid choice!")
    
    def behavioral_analysis_report(self):
        """Generate behavioral analysis report."""
        if not self.software.partners:
            print("No partners available.")
            return
        
        report = self.software.behavioral_analysis_report()
        
        print("\nBEHAVIORAL ANALYSIS REPORT:")
        print(f"Generated: {report['generated_at']}")
        
        for analysis in report['partner_analyses']:
            print(f"\n{analysis['name']}:")
            print(f"  Observations: {analysis['observation_count']} total, {analysis['recent_observations_count']} recent")
            calc = analysis['calculated_from_observations']
            print(f"  Calculated: Inputs={calc['total_inputs']:.1f}, Outcomes={calc['total_outcomes']:.1f}")
            print(f"  Categories: {', '.join(analysis['category_breakdown'].keys())}")
            
            if input(f"\nShow detailed observations for {analysis['name']}? (y/n): ").lower() == 'y':
                for obs in analysis['observations_timeline'][:5]:  # Show last 5 observations
                    print(f"    [{obs['timestamp']}] {obs['category']}: {obs['description'][:50]}...")
    
    def display_theory_summary(self):
        """Display summary of equity theory concepts."""
        print("\nKEY EQUITY THEORY MODELS IMPLEMENTED:")
        print("-" * 50)
        theories = [
            ("Adams (1965)", "Original Inequity Theory", "Inequity Index"),
            ("Walster & Walster (1975)", "Mathematical Formula", "O-I/|I|^k Equation"),
            ("Hatfield et al. (1979)", "Global Measure", "-3 to +3 Scale"),
            ("Huseman et al. (1987)", "Equity Sensitivity", "Benevolent/Sensitive/Entitled"),
            ("Deutsch (1985)", "Distributive Justice", "Justice Index"),
            ("Canary & Stafford (1992)", "Relational Maintenance", "Maintenance Prediction")
        ]
        
        for theorist, concept, metric in theories:
            print(f"• {theorist:<25} {concept:<30} {metric}")
        
        print("\nBEHAVIORAL CATEGORIES TRACKED:")
        for category, behaviors in self.software.BEHAVIORAL_CATEGORIES.items():
            print(f"• {category.replace('_', ' ').title()}: {', '.join(behaviors[:3])}...")
    
    def run(self):
        """Main application loop."""
        self.display_header()
        
        while self.running:
            self.display_menu()
            
            try:
                choice = int(input("Select option (1-9): "))
            except ValueError:
                print("Invalid input! Please enter a number.")
                continue
            
            if choice == 1:
                self.add_partner()
            elif choice == 2:
                self.view_partners()
            elif choice == 3:
                self.add_observation()
            elif choice == 4:
                self.view_observations()
            elif choice == 5:
                self.run_comprehensive_analysis()
            elif choice == 6:
                self.run_specific_calculation()
            elif choice == 7:
                self.behavioral_analysis_report()
            elif choice == 8:
                self.display_theory_summary()
            elif choice == 9:
                print("Thank you for using Equity Theory Software!")
                self.running = False
            else:
                print("Invalid choice! Please select 1-9.")

def main():
    """Main application entry point."""
    cli = EquityTheoryCLI()
    cli.run()

if __name__ == "__main__":
    main()