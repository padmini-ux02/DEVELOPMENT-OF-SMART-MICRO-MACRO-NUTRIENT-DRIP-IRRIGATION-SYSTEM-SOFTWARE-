"""
controller.py
=============
Rule-based nutrient dosing and irrigation controller.

Decision logic:
  ┌─────────────────────────────────────────────────────────┐
  │ IRRIGATION                                               │
  │   moisture < LOW  → turn ON  (for IRRIGATION_DURATION)  │
  │   moisture > HIGH → turn OFF                             │
  │                                                          │
  │ MICRO-NUTRIENT PUMP                                      │
  │   EC < EC_LOW     → dose for MICRO_DOSE_DURATION steps  │
  │   EC > EC_HIGH    → force OFF                            │
  │                                                          │
  │ MACRO-NUTRIENT PUMP                                      │
  │   EC < EC_LOW     → dose for MACRO_DOSE_DURATION steps  │
  │   EC > EC_HIGH    → force OFF                            │
  └─────────────────────────────────────────────────────────┘

All pumps have individual countdown timers so they run for a
fixed number of steps before the controller reassesses.
"""

from config import Config
from pumps import MicroNutrientPump, MacroNutrientPump, IrrigationPump


class NutrientController:
    def __init__(self, cfg: Config):
        self._cfg = cfg
        self._irr_cd   = 0   # irrigation countdown (steps remaining)
        self._micro_cd = 0   # micro-pump countdown
        self._macro_cd = 0   # macro-pump countdown

    # ── Main decision method ───────────────────────────────────
    def decide(
        self,
        moisture: float,
        ec: float,
        ph: float,
        temp: float,
        micro_pump: MicroNutrientPump,
        macro_pump: MacroNutrientPump,
        irr_pump:   IrrigationPump,
    ) -> list[str]:
        """
        Evaluate sensor readings and control pumps.
        Returns a list of event log strings (may be empty).
        """
        cfg    = self._cfg
        events: list[str] = []

        # ── Tick countdowns ────────────────────────────────────
        if self._irr_cd   > 0: self._irr_cd   -= 1
        if self._micro_cd > 0: self._micro_cd -= 1
        if self._macro_cd > 0: self._macro_cd -= 1

        # ── Irrigation logic ───────────────────────────────────
        if moisture < cfg.MOISTURE_LOW and self._irr_cd == 0:
            msg = irr_pump.turn_on(
                f"Moisture {moisture:.1f}% < {cfg.MOISTURE_LOW:.0f}%"
            )
            if msg:
                events.append(msg)
                self._irr_cd = cfg.IRRIGATION_DURATION

        elif moisture >= cfg.MOISTURE_HIGH or (
            self._irr_cd == 0 and moisture >= cfg.MOISTURE_LOW
        ):
            msg = irr_pump.turn_off()
            if msg:
                events.append(msg)

        # ── EC / Nutrient logic ────────────────────────────────
        if ec > cfg.EC_HIGH:
            # Over-fertilised – halt all dosing
            for pump in (micro_pump, macro_pump):
                msg = pump.turn_off()
                if msg:
                    events.append(f"⚠  EC={ec:.2f} HIGH – {msg}")
        elif ec < cfg.EC_LOW:
            # Under-fertilised – dose both
            if self._micro_cd == 0:
                msg = micro_pump.turn_on(
                    f"EC {ec:.2f} < {cfg.EC_LOW:.1f} mS/cm"
                )
                if msg:
                    events.append(msg)
                    self._micro_cd = cfg.MICRO_DOSE_DURATION

            if self._macro_cd == 0:
                msg = macro_pump.turn_on(
                    f"EC {ec:.2f} < {cfg.EC_LOW:.1f} mS/cm"
                )
                if msg:
                    events.append(msg)
                    self._macro_cd = cfg.MACRO_DOSE_DURATION
        else:
            # EC is in optimal range – stop pumps when their timers expire
            if self._micro_cd == 0:
                msg = micro_pump.turn_off()
                if msg:
                    events.append(msg)
            if self._macro_cd == 0:
                msg = macro_pump.turn_off()
                if msg:
                    events.append(msg)

        # ── pH alerts (no automatic action – for logging only) ─
        if ph < cfg.PH_LOW:
            events.append(
                f"⚠  pH={ph:.2f} ACIDIC  (< {cfg.PH_LOW}) – check buffer solution"
            )
        elif ph > cfg.PH_HIGH:
            events.append(
                f"⚠  pH={ph:.2f} ALKALINE (> {cfg.PH_HIGH}) – check acid dosing"
            )

        return events

    # ── Countdown accessors ────────────────────────────────────
    @property
    def irrigation_remaining(self) -> int:
        return self._irr_cd

    @property
    def micro_remaining(self) -> int:
        return self._micro_cd

    @property
    def macro_remaining(self) -> int:
        return self._macro_cd
