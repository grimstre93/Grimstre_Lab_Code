# -----------------------------------------------------------------------------
# ROCKET ALTITUDE SIMULATION (RASP-93)
# Copyright (c) 2024 GRIMSTRE DIGITAL TOOLS
#
# This software and its source code are the property of GRIMSTRE DIGITAL TOOLS.
# Unauthorized copying, distribution, or modification of this file, via any
# medium, is strictly prohibited unless prior written permission is obtained
# from GRIMSTRE DIGITAL TOOLS.
#
# For licensing inquiries, contact: grimstredigitaltools@example.com
# -----------------------------------------------------------------------------

import tkinter as tk
from tkinter import ttk, messagebox

# Motor data: code -> (motor_mass, mass_dec, delay, [thrusts...])
MOTOR_DB = {
    "A6":   (0.0153, 0.0008536, 0.40, [5.91, 11.82, 5.91, 0]),
    "A8":   (0.0165, 0.000624, 0.5, [5.2, 10.4, 4, 3.2, 0]),
    "B4":   (0.0202, 0.000694, 1.2, [5.2, 10.4, 4, 3.2, 3.2, 3.2, 3.2, 3.2, 3.2, 0]),
    "B6":   (0.02, 0.00078, 0.8, [6.5, 13, 6, 0]),
    "C6":   (0.026, 0.000734, 1.7, [6.5, 13, 6, 5, 5, 5, 5, 5, 5, 5, 5, 0]),
    # Add more motors as needed...
}

LENGTH_UNITS = [
    ("inches", 0.0254),
    ("millimeters", 0.001),
    ("feet", 0.3048),
    ("meters", 1.0)
]

MASS_UNITS = [
    ("ounces", 0.02834952),
    ("grams", 0.001),
    ("pounds", 0.453592),
    ("kilograms", 1.0)
]

def simulate_rocket(params):
    # Unpack parameters
    empty_weight, mass_unit, bt_diameter, length_unit, cd, motor_code = params
    # Convert units
    rocket_mass = empty_weight * MASS_UNITS[mass_unit][1]
    bt_radius = (bt_diameter * LENGTH_UNITS[length_unit][1]) / 2
    cd = float(cd)
    motor_code = motor_code.upper().strip()
    if motor_code not in MOTOR_DB:
        return None, f"Motor code '{motor_code}' not found."
    motor_mass, mass_dec, delay, thrusts = MOTOR_DB[motor_code]
    # Constants
    PI = 3.14159
    RHO = 1.2062
    G_FORCE = 9.81001
    TIME_INC = 0.1
    # Initial values
    time = 0.0
    vel = 0.0
    max_vel = 0.0
    alti = 0.0
    rocket_mass_total = rocket_mass + motor_mass
    drag_val = 0.5 * RHO * PI * cd * (bt_radius ** 2)
    thrust_idx = 0
    m_force = thrusts[thrust_idx]
    results = []
    # Simulation loop
    while True:
        accel = m_force / rocket_mass_total - G_FORCE - drag_val * vel * abs(vel) / rocket_mass_total
        vel += accel * TIME_INC
        if vel < 0:
            break
        alti += vel * TIME_INC
        if m_force > 0:
            rocket_mass_total -= mass_dec
            thrust_idx += 1
            if thrust_idx < len(thrusts):
                m_force = thrusts[thrust_idx]
            else:
                m_force = 0
        if vel > max_vel:
            max_vel = vel
        results.append((round(time,2), round(alti,2), round(vel,2), round(accel,2), round(rocket_mass_total,3)))
        time += TIME_INC
    return {
        "max_altitude_m": alti,
        "max_altitude_ft": alti * 3.28084,
        "time_to_peak": time,
        "max_velocity_mps": max_vel,
        "max_velocity_fps": max_vel * 3.28084,
        "recommended_delay": delay,
        "flight_data": results
    }, None

class RocketSimApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("ROCKET ALTITUDE SIMULATION (RASP-93)")
        self.geometry("600x600")
        self.create_widgets()

    def create_widgets(self):
        frm = ttk.Frame(self)
        frm.pack(padx=10, pady=10, fill="x")

        # Empty weight
        ttk.Label(frm, text="Rocket no-engine (empty) weight:").grid(row=0, column=0, sticky="w")
        self.empty_weight = ttk.Entry(frm)
        self.empty_weight.grid(row=0, column=1)
        self.mass_unit = ttk.Combobox(frm, values=[u[0] for u in MASS_UNITS], state="readonly")
        self.mass_unit.current(1)
        self.mass_unit.grid(row=0, column=2)

        # Body tube diameter
        ttk.Label(frm, text="Rocket's maximum body tube diameter:").grid(row=1, column=0, sticky="w")
        self.bt_diameter = ttk.Entry(frm)
        self.bt_diameter.grid(row=1, column=1)
        self.length_unit = ttk.Combobox(frm, values=[u[0] for u in LENGTH_UNITS], state="readonly")
        self.length_unit.current(1)
        self.length_unit.grid(row=1, column=2)

        # Drag coefficient
        ttk.Label(frm, text="Drag Coefficient:").grid(row=2, column=0, sticky="w")
        self.cd = ttk.Entry(frm)
        self.cd.grid(row=2, column=1)

        # Motor code
        ttk.Label(frm, text="Rocket Motor type code (e.g. A6, B4, C6):").grid(row=3, column=0, sticky="w")
        self.motor_code = ttk.Entry(frm)
        self.motor_code.grid(row=3, column=1)

        # Simulate button
        self.sim_btn = ttk.Button(frm, text="Simulate", command=self.run_simulation)
        self.sim_btn.grid(row=4, column=0, columnspan=3, pady=10)

        # Results
        self.results = tk.Text(self, height=20, width=70)
        self.results.pack(padx=10, pady=10, fill="both", expand=True)

    def run_simulation(self):
        try:
            params = (
                float(self.empty_weight.get()),
                self.mass_unit.current(),
                float(self.bt_diameter.get()),
                self.length_unit.current(),
                float(self.cd.get()),
                self.motor_code.get()
            )
        except Exception as e:
            messagebox.showerror("Input Error", "Please enter valid numeric values.")
            return
        result, error = simulate_rocket(params)
        self.results.delete("1.0", tk.END)
        if error:
            self.results.insert(tk.END, error)
            return
        self.results.insert(tk.END, f"Maximum Altitude attained: {result['max_altitude_m']:.2f} meters ({result['max_altitude_ft']:.2f} feet)\n")
        self.results.insert(tk.END, f"Time to peak altitude: {result['time_to_peak']:.2f} seconds\n")
        self.results.insert(tk.END, f"Recommended delay time: {result['recommended_delay']} seconds\n")
        self.results.insert(tk.END, f"Maximum velocity attained: {result['max_velocity_mps']:.2f} m/s ({result['max_velocity_fps']:.2f} ft/s)\n\n")
        self.results.insert(tk.END, "Time\tAltitude\tVelocity\tAccel\tWeight\n")
        for row in result['flight_data']:
            self.results.insert(tk.END, f"{row[0]:.2f}\t{row[1]:.2f}\t\t{row[2]:.2f}\t\t{row[3]:.2f}\t{row[4]:.3f}\n")

if __name__ == "__main__":
    app = RocketSimApp()
    app.mainloop()

# To create an executable file, run the following command in your terminal:
# python -m PyInstaller --onefile --windowed RASP_93.py

# To install required dependencies, run the following command in your terminal:
# pip install matplotlib
