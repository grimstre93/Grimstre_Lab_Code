# To build standalone exe: 
#   pyinstaller --onefile --windowed --name ShogunFinance shogun_finance.py
import tkinter as tk
from tkinter import ttk, scrolledtext
from typing import Dict, List

# ─────────────── Core “Shogun 2”-style Metrics ───────────────

def compute_income_generated(domains: Dict[str, float]) -> float:
    return sum(domains.values())

def compute_upkeep_costs(armies: Dict[str, int],
                         upkeep_rates: Dict[str, float]) -> float:
    return sum(count * upkeep_rates.get(unit, 0.0)
               for unit, count in armies.items())

def compute_monthly_budget(income: float, upkeep: float) -> float:
    return income - upkeep

def compute_profits_retained(income: float,
                             upkeep: float,
                             other_costs: float = 0.0) -> float:
    return income - upkeep - other_costs

def compute_total_savings(prev_savings: float,
                          retained_profits: List[float]) -> float:
    return prev_savings + sum(retained_profits)

def compute_food_stock(bags: Dict[str, int],
                       kg_per_bag: float = 90.0) -> Dict[str, float]:
    return { cereal: count * kg_per_bag
             for cereal, count in bags.items() }

def compute_scale_of_finance_usage(used: float, total: float) -> float:
    if total <= 0: return 0.0
    pct = (used / total) * 100
    return max(0.0, min(100.0, pct))


# ─────────────── The Tkinter App ───────────────

class ShogunFinanceApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Shogun-2 Finance Dashboard")
        self._build_ui()
    
    def _build_ui(self):
        frm = ttk.Frame(self, padding=10)
        frm.pack(fill="both", expand=True)

        # -- Domains (Income)
        domain_lbl = ttk.Label(frm, text="Domain Incomes (gold/month)", font=("Segoe UI", 10, "underline"))
        domain_lbl.grid(row=0, column=0, sticky="w", pady=(0,5))
        self.domain_vars = {}
        for i, name in enumerate(["Yamato Plains", "Omi Province", "Iga Highlands"]):
            sv = tk.StringVar(value="0")
            ttk.Label(frm, text=name).grid(row=i+1, column=0, sticky="e")
            ttk.Entry(frm, textvariable=sv, width=10).grid(row=i+1, column=1)
            self.domain_vars[name] = sv

        # -- Armies & Upkeep
        army_lbl = ttk.Label(frm, text="Army Counts & Upkeep", font=("Segoe UI", 10, "underline"))
        army_lbl.grid(row=0, column=2, sticky="w", padx=(20,0), pady=(0,5))
        self.army_vars = {}
        self.upkeep_rates = {"Ashigaru":5.0, "Samurai":15.0, "Sohei":12.0}
        for i, unit in enumerate(self.upkeep_rates.keys()):
            sv = tk.StringVar(value="0")
            ttk.Label(frm, text=f"{unit} (#)").grid(row=i+1, column=2, sticky="e", padx=(20,0))
            ttk.Entry(frm, textvariable=sv, width=8).grid(row=i+1, column=3)
            self.army_vars[unit] = sv

        # -- Other costs & previous savings
        ttk.Label(frm, text="Other Costs:").grid(row=5, column=0, sticky="e", pady=(10,0))
        self.other_costs = tk.StringVar(value="0")
        ttk.Entry(frm, textvariable=self.other_costs, width=10).grid(row=5, column=1, pady=(10,0))
        ttk.Label(frm, text="Prev. Savings:").grid(row=5, column=2, sticky="e", padx=(20,0), pady=(10,0))
        self.prev_sav = tk.StringVar(value="0")
        ttk.Entry(frm, textvariable=self.prev_sav, width=10).grid(row=5, column=3, pady=(10,0))

        # -- Cereal bags
        cereal_lbl = ttk.Label(frm, text="Cereal Bags (# of 90kg)", font=("Segoe UI", 10, "underline"))
        cereal_lbl.grid(row=7, column=0, sticky="w", pady=(20,5))
        self.cereal_vars = {}
        for i, cereal in enumerate(["Rice", "Barley", "Millet"]):
            sv = tk.StringVar(value="0")
            ttk.Label(frm, text=cereal).grid(row=8+i, column=0, sticky="e")
            ttk.Entry(frm, textvariable=sv, width=10).grid(row=8+i, column=1)
            self.cereal_vars[cereal] = sv

        # -- Calculate button
        btn = ttk.Button(frm, text="Calculate", command=self._on_calculate)
        btn.grid(row=12, column=0, columnspan=4, pady=(20,0))

        # -- Output log
        self.log = scrolledtext.ScrolledText(frm, height=10, state="disabled")
        self.log.grid(row=13, column=0, columnspan=4, sticky="nsew", pady=(10,0))
        frm.rowconfigure(13, weight=1)
        frm.columnconfigure(3, weight=1)

    def _on_calculate(self):
        # Gather inputs
        domains = { name: float(var.get()) for name,var in self.domain_vars.items() }
        armies  = { unit: int(var.get())   for unit,var in self.army_vars.items() }
        other_costs = float(self.other_costs.get())
        prev_savings = float(self.prev_sav.get())
        bags = { cereal: int(var.get()) for cereal,var in self.cereal_vars.items() }

        # Compute metrics
        income   = compute_income_generated(domains)
        upkeep   = compute_upkeep_costs(armies, self.upkeep_rates)
        budget   = compute_monthly_budget(income, upkeep)
        profits  = compute_profits_retained(income, upkeep, other_costs)
        total_sav= compute_total_savings(prev_savings, [profits])
        food_kg  = compute_food_stock(bags)
        spent    = upkeep + other_costs
        usage_pct= compute_scale_of_finance_usage(spent, income)

        # Log to UI
        self._append_log(f"Income Generated:          {income:.2f}")
        self._append_log(f"Total Upkeep Costs:        {upkeep:.2f}")
        self._append_log(f"Net Budget (Income−Upkeep):{budget:.2f}")
        self._append_log(f"Profits Retained:          {profits:.2f}")
        self._append_log(f"New Total Savings:         {total_sav:.2f}")
        for c, kg in food_kg.items():
            self._append_log(f"Food Stock – {c}:       {kg:.1f} kg")
        self._append_log(f"Finance Usage:             {usage_pct:.1f}%")
        self._append_log("-"*40)

    def _append_log(self, text: str):
        self.log['state'] = 'normal'
        self.log.insert("end", text + "\n")
        self.log.see("end")
        self.log['state'] = 'disabled'

print("Starting…")

if __name__ == "__main__":
    app = ShogunFinanceApp()
    app.geometry("600x600")
    app.mainloop()
