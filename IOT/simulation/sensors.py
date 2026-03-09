"""
sensors.py
==========
Virtual sensor models with realistic physical behaviour:
  - Moisture drops from evaporation; rises when irrigation is active.
  - EC drops from plant uptake; rises with nutrient dosing; dilutes with water.
  - pH drifts slowly with dosing activity.
  - Temperature follows a sinusoidal day/night cycle.
"""

import math
import random
from config import Config


# ──────────────────────────────────────────────────────────────
class SoilMoistureSensor:
    """
    Simulates a capacitive soil moisture sensor.
    Range: 0 – 100 %
    """

    def __init__(self, cfg: Config):
        self._cfg = cfg
        self._state = random.uniform(cfg.MOISTURE_INIT_MIN, cfg.MOISTURE_INIT_MAX)

    # ── Public ─────────────────────────────────────────────────
    def update(self, irrigation_active: bool) -> float:
        cfg = self._cfg
        if irrigation_active:
            delta = random.uniform(cfg.IRRIGATION_GAIN_MIN, cfg.IRRIGATION_GAIN_MAX)
            self._state += delta
        else:
            delta = random.uniform(cfg.EVAP_RATE_MIN, cfg.EVAP_RATE_MAX)
            self._state -= delta

        # Sensor noise  ±0.3 %
        noise = random.gauss(0, 0.3)
        self._state = float(max(0.0, min(100.0, self._state)))
        return float(max(0.0, min(100.0, self._state + noise)))

    @property
    def raw(self) -> float:
        return self._state


# ──────────────────────────────────────────────────────────────
class ECSensor:
    """
    Simulates an Electrical Conductivity sensor.
    Range: 0.0 – 5.0 mS/cm
    """

    def __init__(self, cfg: Config):
        self._cfg = cfg
        self._state = random.uniform(cfg.EC_INIT_MIN, cfg.EC_INIT_MAX)

    def update(
        self,
        micro_active: bool,
        macro_active: bool,
        irrigation_active: bool,
    ) -> float:
        cfg = self._cfg

        # Plant uptake (continuous EC drawdown)
        self._state -= random.uniform(0.01, cfg.EC_PLANT_UPTAKE)

        if micro_active:
            self._state += random.uniform(cfg.EC_MICRO_GAIN * 0.7, cfg.EC_MICRO_GAIN)
        if macro_active:
            self._state += random.uniform(cfg.EC_MACRO_GAIN * 0.7, cfg.EC_MACRO_GAIN)
        if irrigation_active:
            self._state -= random.uniform(cfg.EC_DILUTION * 0.5, cfg.EC_DILUTION)

        noise = random.gauss(0, 0.02)
        self._state = float(max(0.0, min(5.0, self._state)))
        return float(max(0.0, min(5.0, self._state + noise)))

    @property
    def raw(self) -> float:
        return self._state


# ──────────────────────────────────────────────────────────────
class PHSensor:
    """
    Simulates a pH probe.
    Range: 4.0 – 8.5
    """

    def __init__(self, cfg: Config):
        self._cfg = cfg
        self._state = random.uniform(cfg.PH_INIT_MIN, cfg.PH_INIT_MAX)

    def update(self, micro_active: bool, macro_active: bool) -> float:
        # Micro nutrients tend to acidify; macro tend to alkalinise
        if micro_active:
            self._state -= random.uniform(0.01, 0.04)
        if macro_active:
            self._state += random.uniform(0.005, 0.025)

        # Slow mean-reversion toward 6.2
        self._state += (6.2 - self._state) * 0.01

        noise = random.gauss(0, 0.02)
        self._state = float(max(4.0, min(8.5, self._state)))
        return float(max(4.0, min(8.5, self._state + noise)))

    @property
    def raw(self) -> float:
        return self._state


# ──────────────────────────────────────────────────────────────
class TemperatureSensor:
    """
    Simulates air/root-zone temperature.
    Uses a sinusoidal day-night cycle plus Gaussian noise.
    """

    def __init__(self, cfg: Config):
        self._cfg = cfg

    def update(self, step: int) -> float:
        cfg = self._cfg
        phase = 2 * math.pi * step / cfg.TEMP_CYCLE_STEPS
        base  = cfg.TEMP_BASE + cfg.TEMP_AMPLITUDE * math.sin(phase)
        noise = random.gauss(0, 0.3)
        return round(base + noise, 2)
