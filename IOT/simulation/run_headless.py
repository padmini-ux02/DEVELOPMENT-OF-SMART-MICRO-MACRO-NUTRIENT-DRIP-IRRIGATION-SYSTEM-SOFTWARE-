"""
run_headless.py
===============
Runs the Nutrient Doser simulation without a terminal UI for 
maximum compatibility in headless/automated environments.
Generates 'headless_report.png'.
"""

import os
from config import Config
from sensors import SoilMoistureSensor, ECSensor, PHSensor, TemperatureSensor
from pumps import MicroNutrientPump, MacroNutrientPump, IrrigationPump
from controller import NutrientController
from plotter import plot_simulation

def run():
    cfg = Config()
    cfg.SIMULATION_STEPS = 100  # Longer run
    
    # Components
    moist_s = SoilMoistureSensor(cfg)
    ec_s    = ECSensor(cfg)
    ph_s    = PHSensor(cfg)
    temp_s  = TemperatureSensor(cfg)
    
    micro_p = MicroNutrientPump()
    macro_p = MacroNutrientPump()
    irr_p   = IrrigationPump()
    
    ctrl    = NutrientController(cfg)
    
    history = []
    
    print(f"--- Starting Headless Simulation ({cfg.SIMULATION_STEPS} steps) ---")
    
    for step in range(1, cfg.SIMULATION_STEPS + 1):
        # Update sensors
        m = moist_s.update(irr_p.active)
        e = ec_s.update(micro_p.active, macro_p.active, irr_p.active)
        p = ph_s.update(micro_p.active, macro_p.active)
        t = temp_s.update(step)
        
        # Controller decides
        events = ctrl.decide(m, e, p, t, micro_p, macro_p, irr_p)
        
        for pmp in (micro_p, macro_p, irr_p):
            pmp.tick()
        
        for ev in events:
            print(f"[Step {step:03d}] {ev}")
            
        # Log state
        history.append({
            "step":     step,
            "moisture": m,
            "ec":       e,
            "ph":       p,
            "temp":     t,
            "irr":      irr_p.active,
            "micro":    micro_p.active,
            "macro":    macro_p.active,
        })
    
    print("--- Simulation Complete ---")
    print(f"Total Irrigation: {irr_p.stats.total_activations} times")
    print(f"Total Nutrient Doses: {micro_p.stats.total_activations} times")
    
    # Generate plot
    report_path = os.path.join(os.path.dirname(__file__), "headless_report.png")
    plot_simulation(history, report_path)
    print(f"Report saved to: {report_path}")

if __name__ == "__main__":
    run()
