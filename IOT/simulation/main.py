"""
main.py
=======
Entry point for the Smart Plant Nutrient Doser simulation.

Run:
    python main.py

Controls:
    Ctrl-C  – abort early; the chart is still saved for steps completed.
"""

import sys
import time
import random
import os

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.layout import Layout
from rich.live import Live
from rich.text import Text
from rich.align import Align
from rich.columns import Columns
from rich import box

from config import Config
from sensors import SoilMoistureSensor, ECSensor, PHSensor, TemperatureSensor
from pumps import MicroNutrientPump, MacroNutrientPump, IrrigationPump
from controller import NutrientController
from plotter import plot_simulation

# ── Console ────────────────────────────────────────────────────
console = Console()

# ── Colour helpers ─────────────────────────────────────────────
def moisture_color(v: float) -> str:
    if v < 35:   return "bold red"
    if v < 50:   return "yellow"
    if v < 75:   return "bold green"
    return "cyan"

def ec_color(v: float) -> str:
    if v < 1.0:  return "bold red"
    if v > 3.0:  return "bold magenta"
    return "bold green"

def ph_color(v: float) -> str:
    if v < 5.5 or v > 7.0: return "bold red"
    return "bold green"

def pump_badge(active: bool) -> Text:
    return (
        Text(" ON  ", style="bold black on green")
        if active
        else Text(" OFF ", style="bold white on grey23")
    )

# ── Sensor reading table ───────────────────────────────────────
def build_sensor_table(step, total, moisture, ec, ph, temp) -> Table:
    t = Table(
        title=f"[bold cyan]Step {step}/{total}[/]",
        box=box.ROUNDED,
        border_style="bright_blue",
        show_header=True,
        header_style="bold magenta",
        expand=True,
    )
    t.add_column("Sensor",   style="bold white", justify="left")
    t.add_column("Reading",  justify="right")
    t.add_column("Unit",     justify="left")
    t.add_column("Status",   justify="center")

    def moisture_status(v):
        if v < 35:   return "[bold red]DRY – irrigating[/]"
        if v > 75:   return "[cyan]SATURATED[/]"
        return "[bold green]OPTIMAL[/]"

    def ec_status(v):
        if v < 1.0:  return "[bold red]LOW – dosing[/]"
        if v > 3.0:  return "[bold magenta]HIGH – stop dose[/]"
        return "[bold green]OPTIMAL[/]"

    def ph_status(v):
        if v < 5.5:  return "[bold red]ACIDIC[/]"
        if v > 7.0:  return "[bold red]ALKALINE[/]"
        return "[bold green]OK[/]"

    def temp_status(v):
        if v < 15:   return "[cyan]COOL[/]"
        if v > 32:   return "[red]HOT[/]"
        return "[green]NORMAL[/]"

    t.add_row(
        "[yellow]🌱 Soil Moisture[/]",
        f"[{moisture_color(moisture)}]{moisture:6.1f}[/]", "%",
        moisture_status(moisture),
    )
    t.add_row(
        "[yellow]⚡ EC Level[/]",
        f"[{ec_color(ec)}]{ec:6.3f}[/]", "mS/cm",
        ec_status(ec),
    )
    t.add_row(
        "[yellow]🔬 pH Level[/]",
        f"[{ph_color(ph)}]{ph:6.2f}[/]", "pH",
        ph_status(ph),
    )
    t.add_row(
        "[yellow]🌡  Temperature[/]",
        f"[{('bold red' if temp > 32 else 'bold blue' if temp < 15 else 'white')}]{temp:6.1f}[/]",
        "°C",
        temp_status(temp),
    )
    return t

# ── Pump status table ──────────────────────────────────────────
def build_pump_table(irr_pump, micro_pump, macro_pump,
                     irr_cd, micro_cd, macro_cd) -> Table:
    t = Table(
        title="[bold cyan]Pump Status[/]",
        box=box.ROUNDED,
        border_style="bright_blue",
        show_header=True,
        header_style="bold magenta",
        expand=True,
    )
    t.add_column("Pump",         style="bold white", justify="left")
    t.add_column("State",        justify="center")
    t.add_column("Steps left",   justify="center")
    t.add_column("Activations",  justify="center")
    t.add_column("Runtime (steps)", justify="center")

    rows = [
        (irr_pump,   irr_cd,   "[cyan]💧 Irrigation[/]"),
        (micro_pump, micro_cd, "[yellow]🧪 Micro-Nutrient[/]"),
        (macro_pump, macro_cd, "[green]🌿 Macro-Nutrient[/]"),
    ]
    for pump, cd, label in rows:
        t.add_row(
            label,
            pump_badge(pump.active),
            str(cd) if pump.active else "—",
            str(pump.stats.total_activations),
            str(pump.stats.total_active_steps),
        )
    return t

# ── Event log panel ────────────────────────────────────────────
def build_event_panel(event_log: list[str]) -> Panel:
    max_lines = 10
    shown = event_log[-max_lines:]
    lines = "\n".join(
        f"[dim white]{i+1:>3}.[/] {e}" for i, e in enumerate(
            event_log[-len(shown):], start=max(0, len(event_log) - max_lines)
        )
    )
    return Panel(
        lines or "[dim]No events yet[/]",
        title="[bold cyan]📋 Event Log (last 10)[/]",
        border_style="bright_blue",
        padding=(0, 1),
    )

# ──────────────────────────────────────────────────────────────
def print_banner() -> None:
    banner = """
[bold cyan]╔══════════════════════════════════════════════════════════╗[/]
[bold cyan]║[/]  [bold white]Smart Plant Micro-Macro Nutrient Doser – Simulation[/]  [bold cyan]║[/]
[bold cyan]║[/]  [dim]Drip Irrigation Control System  |  Python 3.12[/]         [bold cyan]║[/]
[bold cyan]╚══════════════════════════════════════════════════════════╝[/]
"""
    console.print(banner)


# ──────────────────────────────────────────────────────────────
def run() -> None:
    cfg = Config()

    # Optional reproducible seed
    if cfg.RANDOM_SEED is not None:
        random.seed(cfg.RANDOM_SEED)

    # ── Instantiate components ─────────────────────────────────
    moisture_sensor = SoilMoistureSensor(cfg)
    ec_sensor       = ECSensor(cfg)
    ph_sensor       = PHSensor(cfg)
    temp_sensor     = TemperatureSensor(cfg)

    micro_pump  = MicroNutrientPump()
    macro_pump  = MacroNutrientPump()
    irr_pump    = IrrigationPump()

    controller  = NutrientController(cfg)

    history: list[dict] = []
    event_log: list[str] = []

    print_banner()
    console.print(
        f"[bold white]Simulation:[/] [cyan]{cfg.SIMULATION_STEPS}[/] steps  |  "
        f"[bold white]Step delay:[/] [cyan]{cfg.STEP_DELAY_SEC}s[/]  |  "
        f"[bold white]Moisture threshold:[/] [red]{cfg.MOISTURE_LOW}%[/] – "
        f"[green]{cfg.MOISTURE_HIGH}%[/]  |  "
        f"[bold white]EC threshold:[/] [red]{cfg.EC_LOW}[/] – "
        f"[green]{cfg.EC_HIGH}[/] mS/cm\n"
    )

    try:
        with Live(console=console, refresh_per_second=4) as live:
            for step in range(1, cfg.SIMULATION_STEPS + 1):

                # ── Read sensors ───────────────────────────────
                moisture = moisture_sensor.update(irr_pump.active)
                ec       = ec_sensor.update(micro_pump.active,
                                            macro_pump.active,
                                            irr_pump.active)
                ph       = ph_sensor.update(micro_pump.active, macro_pump.active)
                temp     = temp_sensor.update(step)

                # ── Controller decision ────────────────────────
                events = controller.decide(
                    moisture, ec, ph, temp,
                    micro_pump, macro_pump, irr_pump,
                )

                # Tick runtime counters
                for p in (micro_pump, macro_pump, irr_pump):
                    p.tick()

                # ── Record events ──────────────────────────────
                for e in events:
                    event_log.append(f"[Step {step:03d}] {e}")

                # ── History for plot ───────────────────────────
                history.append({
                    "step":     step,
                    "moisture": moisture,
                    "ec":       ec,
                    "ph":       ph,
                    "temp":     temp,
                    "irr":      irr_pump.active,
                    "micro":    micro_pump.active,
                    "macro":    macro_pump.active,
                })

                # ── Build live layout ──────────────────────────
                sensor_tbl = build_sensor_table(
                    step, cfg.SIMULATION_STEPS, moisture, ec, ph, temp
                )
                pump_tbl = build_pump_table(
                    irr_pump, micro_pump, macro_pump,
                    controller.irrigation_remaining,
                    controller.micro_remaining,
                    controller.macro_remaining,
                )
                event_panel = build_event_panel(event_log)

                # Stack vertically
                from rich.console import Group
                renderable = Group(sensor_tbl, pump_tbl, event_panel)
                live.update(renderable)

                time.sleep(cfg.STEP_DELAY_SEC)

    except KeyboardInterrupt:
        console.print("\n[yellow]Simulation interrupted by user.[/]")

    # ── Summary ────────────────────────────────────────────────
    console.print("\n[bold cyan]── Simulation Complete ──────────────────────────────[/]")
    console.print(f"  Steps run          : [white]{len(history)}[/]")
    console.print(f"  Irrigation pump    : [cyan]{irr_pump.stats.total_activations}[/] activations, "
                  f"[cyan]{irr_pump.stats.total_active_steps}[/] active steps")
    console.print(f"  Micro-nutrient pump: [yellow]{micro_pump.stats.total_activations}[/] activations, "
                  f"[yellow]{micro_pump.stats.total_active_steps}[/] active steps")
    console.print(f"  Macro-nutrient pump: [green]{macro_pump.stats.total_activations}[/] activations, "
                  f"[green]{macro_pump.stats.total_active_steps}[/] active steps")

    # ── Generate chart ─────────────────────────────────────────
    if history:
        console.print("\n[bold white]Generating dashboard chart…[/]")
        try:
            out_dir  = os.path.dirname(os.path.abspath(__file__))
            out_path = os.path.join(out_dir, "simulation_report.png")
            saved    = plot_simulation(history, out_path)
            console.print(f"[bold green]✔  Chart saved → {saved}[/]")
        except Exception as ex:
            console.print(f"[red]Chart generation failed: {ex}[/]")


# ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    run()
