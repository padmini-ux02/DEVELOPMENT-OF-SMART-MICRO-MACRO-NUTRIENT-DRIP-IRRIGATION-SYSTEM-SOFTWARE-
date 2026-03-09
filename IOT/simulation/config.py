"""
config.py
=========
Central configuration for the Smart Plant Nutrient Doser simulation.
Edit thresholds and timing here to test different scenarios.
"""


class Config:
    # ── Simulation control ─────────────────────────────────────
    SIMULATION_STEPS: int   = 5       # Total time-steps to simulate
    STEP_DELAY_SEC: float   = 0.01     # Real-time pause between steps (seconds)
    RANDOM_SEED: int | None = None     # Set an int for reproducible runs

    # ── Soil Moisture thresholds (%) ───────────────────────────
    MOISTURE_LOW: float    = 60.0      # Below → irrigation ON
    MOISTURE_HIGH: float   = 75.0      # Above → irrigation OFF
    MOISTURE_INIT_MIN: float = 40.0    # Sensor start range (low)
    MOISTURE_INIT_MAX: float = 65.0    # Sensor start range (high)
    EVAP_RATE_MIN: float   = 0.20      # Min % lost per step (dry rate)
    EVAP_RATE_MAX: float   = 0.55      # Max % lost per step
    IRRIGATION_GAIN_MIN: float = 1.5   # Min % gained per step when pump ON
    IRRIGATION_GAIN_MAX: float = 3.0   # Max % gained per step

    # ── EC (Electrical Conductivity) thresholds (mS/cm) ───────
    EC_LOW: float          = 1.0       # Below → dose micro + macro nutrients
    EC_HIGH: float         = 3.0       # Above → stop dosing (over-fertilised)
    EC_INIT_MIN: float     = 1.2
    EC_INIT_MAX: float     = 2.0
    EC_PLANT_UPTAKE: float = 0.025     # EC decrease per step (plant consumption)
    EC_MICRO_GAIN: float   = 0.10      # EC increase per step when micro pump ON
    EC_MACRO_GAIN: float   = 0.20      # EC increase per step when macro pump ON
    EC_DILUTION: float     = 0.05      # EC decrease per step when irrigation ON

    # ── pH thresholds ──────────────────────────────────────────
    PH_LOW: float          = 5.5       # Alert below
    PH_HIGH: float         = 7.0       # Alert above
    PH_INIT_MIN: float     = 5.8
    PH_INIT_MAX: float     = 6.8

    # ── Temperature (°C) ───────────────────────────────────────
    TEMP_BASE: float       = 22.0      # Mean daily temperature
    TEMP_AMPLITUDE: float  = 8.0       # Diurnal swing ±°C
    TEMP_CYCLE_STEPS: int  = 48        # Steps per full day-night cycle

    # ── Pump timing (steps) ────────────────────────────────────
    IRRIGATION_DURATION: int = 20       # Steps irrigation stays ON per trigger
    MICRO_DOSE_DURATION: int = 30       # Steps micro-pump stays ON per trigger
    MACRO_DOSE_DURATION: int = 60       # Steps macro-pump stays ON per trigger
