"""
pumps.py
=========
Virtual pump models for:
  - Micro-nutrient dosing  (Fe, Mn, Zn, Cu, B, Mo)
  - Macro-nutrient dosing  (N, P, K, Ca, Mg, S)
  - Irrigation water pump
"""

from dataclasses import dataclass, field


# ──────────────────────────────────────────────────────────────
@dataclass
class PumpStats:
    total_activations: int = 0
    total_active_steps: int = 0


# ──────────────────────────────────────────────────────────────
class Pump:
    """Base class for all virtual pumps."""

    def __init__(self, name: str, icon: str, unit: str = "mL/dose", dose: float = 10.0):
        self.name     = name
        self.icon     = icon
        self.unit     = unit
        self.dose_per_activation = dose
        self.active   = False
        self._stats   = PumpStats()

    # ── State changes ──────────────────────────────────────────
    def turn_on(self, reason: str = "") -> str | None:
        """Activate pump. Returns log message or None if already on."""
        if not self.active:
            self.active = True
            self._stats.total_activations += 1
            return f"{self.icon}  {self.name} → ON   ({reason})"
        return None

    def turn_off(self) -> str | None:
        """Deactivate pump. Returns log message or None if already off."""
        if self.active:
            self.active = False
            return f"⏹   {self.name} → OFF"
        return None

    def tick(self) -> None:
        """Call once per simulation step to accumulate runtime."""
        if self.active:
            self._stats.total_active_steps += 1

    # ── Properties ─────────────────────────────────────────────
    @property
    def stats(self) -> PumpStats:
        return self._stats

    @property
    def status_str(self) -> str:
        return "ON " if self.active else "OFF"


# ──────────────────────────────────────────────────────────────
class MicroNutrientPump(Pump):
    """
    Doses micro-nutrients: Fe, Mn, Zn, Cu, B, Mo.
    Small dose volume; high frequency when EC is low.
    """

    def __init__(self):
        super().__init__(
            name="Micro-Nutrient Pump",
            icon="🧪",
            unit="mL/dose",
            dose=5.0,
        )


# ──────────────────────────────────────────────────────────────
class MacroNutrientPump(Pump):
    """
    Doses macro-nutrients: N, P, K, Ca, Mg, S.
    Larger volume; primary EC builder.
    """

    def __init__(self):
        super().__init__(
            name="Macro-Nutrient Pump",
            icon="🌿",
            unit="mL/dose",
            dose=15.0,
        )


# ──────────────────────────────────────────────────────────────
class IrrigationPump(Pump):
    """
    Drives the drip-irrigation water loop.
    Also dilutes EC when running.
    """

    def __init__(self):
        super().__init__(
            name="Irrigation Water Pump",
            icon="💧",
            unit="L/h",
            dose=2.5,
        )
