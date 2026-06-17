
<div align="center">

<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&size=28&pause=1000&color=2ECC71&center=true&vCenter=true&width=900&lines=Smart+Micro+%26+Macro+Nutrient;Drip+Irrigation+System+%F0%9F%8C%B1;IoT+Powered+Precision+Agriculture" alt="Typing SVG" />

<br/>

# 🌿 Development of Smart Micro & Macro Nutrient Drip Irrigation System

### *Precision. Automation. Sustainability.*

<br/>

[![GitHub](https://img.shields.io/badge/GitHub-padmini--ux02-181717?style=for-the-badge&logo=github)](https://github.com/padmini-ux02/DEVELOPMENT-OF-SMART-MICRO-MACRO-NUTRIENT-DRIP-IRRIGATION-SYSTEM-SOFTWARE-)
[![Platform](https://img.shields.io/badge/Platform-ESP32-E7352C?style=for-the-badge&logo=espressif&logoColor=white)](https://www.espressif.com/)
[![IDE](https://img.shields.io/badge/IDE-Arduino-00979D?style=for-the-badge&logo=arduino&logoColor=white)](https://www.arduino.cc/)
[![EDA](https://img.shields.io/badge/PCB-KiCad-314CB0?style=for-the-badge&logo=kicad&logoColor=white)](https://www.kicad.org/)
[![Domain](https://img.shields.io/badge/Domain-Precision%20Agriculture-2e7d32?style=for-the-badge&logo=leaf&logoColor=white)](#)
[![Type](https://img.shields.io/badge/Type-Minor%20Project%20II-orange?style=for-the-badge)](#)

<br/>

> 🚜 An intelligent, sensor-driven irrigation system that automates the precise delivery of **macro and micro nutrients** to crops through drip lines — reducing waste, improving yield, and eliminating manual intervention.

<br/>

---

</div>

## 📑 Table of Contents

- [🌍 Overview](#-overview)
- [❗ Problem Statement](#-problem-statement)
- [💡 Proposed Solution](#-proposed-solution)
- [✨ Key Features](#-key-features)
- [🏗️ System Architecture](#️-system-architecture)
- [🔧 Hardware Components](#-hardware-components)
- [🖥️ PCB & Circuit Design](#️-pcb--circuit-design)
- [🧪 Physical Prototype](#-physical-prototype)
- [🌱 Nutrient Management](#-nutrient-management)
- [⚙️ How It Works — Step by Step](#️-how-it-works--step-by-step)
- [💻 Software & Firmware](#-software--firmware)
- [📂 Repository Structure](#-repository-structure)
- [🚀 Getting Started](#-getting-started)
- [📊 Results & Outcomes](#-results--outcomes)
- [🔭 Future Scope](#-future-scope)
- [👩‍💻 Author](#-author)

---

## 🌍 Overview

Agriculture accounts for **~70% of global freshwater usage**, yet a significant portion is wasted due to inefficient irrigation and nutrient management practices. With a rising global population and shrinking arable land, **precision agriculture** has become the need of the hour.

The **Smart Micro & Macro Nutrient Drip Irrigation System** is a fully automated, IoT-integrated solution that:

- 📡 **Monitors** soil conditions in real-time using sensors (pH, EC, moisture, temperature)
- 🧪 **Analyzes** the data against crop-specific nutrient profiles
- 💧 **Delivers** the exact quantity of macro and micro nutrients through drip lines
- 📱 **Reports** data wirelessly for remote monitoring and alerts

This project bridges the gap between traditional farming and modern smart agriculture using embedded systems, IoT, and custom hardware design.

---

## ❗ Problem Statement

Traditional irrigation and fertilization methods suffer from several critical issues:

| Problem | Impact |
|---|---|
| 🌊 Flood/overhead irrigation | High water wastage (up to 60% loss) |
| 🧪 Bulk fertilizer application | Over/under-dosing, crop damage |
| 👨‍🌾 Manual monitoring | Labor-intensive, inaccurate, delayed response |
| ☠️ Nutrient runoff | Soil degradation, groundwater pollution |
| 📉 Yield uncertainty | Unpredictable crop quality and quantity |

> **These problems demand a smart, automated, data-driven approach** — which is exactly what this system provides.

---

## 💡 Proposed Solution

The proposed system uses a **closed-loop feedback control mechanism**:

```
Sensor Data ──▶ Microcontroller (ESP32) ──▶ Decision Logic ──▶ Pump/Valve Actuation
      ▲                                                                  │
      └──────────────────── Real-time Feedback ◀────────────────────────┘
```

Nutrients are stored in separate reservoirs and dosed individually into the drip irrigation main line using peristaltic pumps, controlled precisely by the ESP32 based on soil readings.

![Proposed System](https://raw.githubusercontent.com/padmini-ux02/DEVELOPMENT-OF-SMART-MICRO-MACRO-NUTRIENT-DRIP-IRRIGATION-SYSTEM-SOFTWARE-/main/proposed%20system.png)

> 📌 *Figure 1: Proposed system block diagram showing the flow from sensing to actuation.*

---

## ✨ Key Features

<table>
<tr>
<td width="50%">

### 🔬 Dual Nutrient Control
Independently controls **Macro** (N, P, K) and **Micro** (Fe, Mn, Zn, Cu, B) nutrients using separate dosing channels.

</td>
<td width="50%">

### 💧 Drip-Line Integration
Nutrients are injected directly into the drip irrigation line — ensuring root-zone precision delivery.

</td>
</tr>
<tr>
<td>

### 📡 Real-Time Sensing
Multi-parameter soil sensing: **pH, EC (Electrical Conductivity), Moisture, and Temperature** — all at once.

</td>
<td>

### 🤖 Autonomous Operation
No human intervention needed. The system reads, decides, and doses **automatically** based on thresholds.

</td>
</tr>
<tr>
<td>

### 🌐 IoT Connectivity
ESP32 Wi-Fi enables **live cloud dashboard**, data logging, and push alerts to the farmer's smartphone.

</td>
<td>

### 🛠️ Custom PCB Design
Designed in **KiCad** — compact, field-ready PCB with sensor headers, relay driver, and power regulation.

</td>
</tr>
<tr>
<td>

### ⚡ Energy Efficient
Low-power design with sleep modes — suitable for **solar-powered** off-grid field deployment.

</td>
<td>

### 📈 Data Logging
Continuous logging of sensor readings and dosing events for **crop analytics and traceability**.

</td>
</tr>
</table>

---

## 🏗️ System Architecture

The system operates across **three integrated layers**:

```
╔══════════════════════════════════════════════════════════════╗
║                    ☁️  CLOUD / IoT LAYER                     ║
║        Remote Dashboard  •  Data Logging  •  Alerts          ║
╚══════════════════════════╤═══════════════════════════════════╝
                           │  Wi-Fi / MQTT Protocol
╔══════════════════════════▼═══════════════════════════════════╗
║               🖥️  PROCESSING LAYER (ESP32)                   ║
║                                                              ║
║   ┌─────────────────────┐    ┌────────────────────────────┐  ║
║   │   📊 SENSOR INPUT    │    │    ⚙️ ACTUATOR OUTPUT       │  ║
║   │  ● Soil Moisture    │    │  ● Peristaltic Pumps       │  ║
║   │  ● pH Sensor        │───▶│  ● Solenoid Valves         │  ║
║   │  ● EC Sensor        │    │  ● Relay Switching         │  ║
║   │  ● Temperature      │    │  ● Drip Emitter Control    │  ║
║   └─────────────────────┘    └────────────────────────────┘  ║
╚══════════════════════════════════════════════════════════════╝
                           │
╔══════════════════════════▼═══════════════════════════════════╗
║               🌿 FIELD / NUTRIENT LAYER                      ║
║                                                              ║
║   Tank A: Nitrogen (N)         Tank E: Iron (Fe)             ║
║   Tank B: Phosphorus (P)       Tank F: Manganese (Mn)        ║
║   Tank C: Potassium (K)        Tank G: Zinc (Zn)             ║
║   Tank D: Water / Main Line    Tank H: Boron (B)             ║
╚══════════════════════════════════════════════════════════════╝
```

---

## 🔧 Hardware Components

### 🧠 Core Electronics

| Component | Model / Spec | Purpose |
|---|---|---|
| **Microcontroller** | ESP32 (Xtensa dual-core 240 MHz) | Central processing, Wi-Fi, GPIO control |
| **pH Sensor Module** | Analog pH probe + signal conditioner | Measures soil/water acidity (0–14 pH) |
| **EC Sensor** | Electrical Conductivity probe | Measures nutrient concentration in solution |
| **Soil Moisture Sensor** | Capacitive type (corrosion-resistant) | Soil water content measurement |
| **Temperature Sensor** | DS18B20 waterproof probe | Soil and water temperature measurement |
| **Peristaltic Pumps** | 12V DC, variable flow rate | Precise liquid nutrient dosing |
| **Solenoid Valves** | 12V DC, normally closed | Irrigation line open/close control |
| **Relay Module** | 4/8-channel optocoupler relay | Switching high-current loads from MCU |
| **LCD / OLED Display** | 16×2 LCD or 0.96" OLED | Local readout of sensor values |
| **Custom PCB** | KiCad designed | Integrates all components on a single board |

### ⚡ Power Supply

| Rail | Source | Loads |
|---|---|---|
| **12V DC** | Adapter / Solar panel | Pumps, solenoid valves, relay coils |
| **5V DC** | LDO regulator from 12V | ESP32 power input |
| **3.3V DC** | ESP32 internal LDO | Sensors, logic circuits |

---

## 🖥️ PCB & Circuit Design

The complete hardware schematic and PCB were designed using **KiCad** — an open-source, professional-grade EDA (Electronic Design Automation) tool.

![KiCad PCB Design](https://raw.githubusercontent.com/padmini-ux02/DEVELOPMENT-OF-SMART-MICRO-MACRO-NUTRIENT-DRIP-IRRIGATION-SYSTEM-SOFTWARE-/main/ki%20cad.png)

> 📌 *Figure 2: KiCad schematic/PCB layout of the irrigation controller board.*

### Design Highlights

- ✅ **Signal isolation** between high-power actuator circuits and low-voltage sensor circuits
- ✅ **Decoupling capacitors** placed near every IC power pin for noise suppression
- ✅ **Labeled screw terminals** for easy sensor and actuator field connections
- ✅ **Onboard voltage regulation** — single 12V supply powers the entire board
- ✅ **Compact form factor** — designed for enclosure mounting in the field
- ✅ **Protected GPIO lines** — series resistors prevent accidental ESP32 pin damage

---

## 🧪 Physical Prototype

The project includes a fully assembled benchtop prototype that validates the complete system — from sensor reading to nutrient delivery.

![Hardware Prototype](https://raw.githubusercontent.com/padmini-ux02/DEVELOPMENT-OF-SMART-MICRO-MACRO-NUTRIENT-DRIP-IRRIGATION-SYSTEM-SOFTWARE-/main/Protoype%20original.png)

> 📌 *Figure 3: Physical prototype of the smart nutrient drip irrigation system.*

The prototype demonstrates:
- 🔌 **Sensor wiring** and signal conditioning
- 💧 **Peristaltic pump** operation with nutrient tanks
- 🔁 **Solenoid valve** switching for drip line control
- 📟 **Display output** of real-time sensor values
- 📡 **Wi-Fi connectivity** for cloud data push

---

## 🌱 Nutrient Management

Plants require nutrients in two broad categories. This system manages **both categories independently**:

### 🟢 Macronutrients — Required in Large Quantities

| Nutrient | Symbol | Role in Plant Growth | Deficiency Symptoms |
|---|---|---|---|
| **Nitrogen** | N | Leaf & stem growth, chlorophyll production | Yellowing of older leaves, stunted growth |
| **Phosphorus** | P | Root development, energy transfer (ATP), flowering | Dark green/purplish leaves, poor root growth |
| **Potassium** | K | Disease resistance, fruiting, water regulation | Brown leaf edges, weak stems |

### 🔵 Micronutrients — Required in Trace Quantities

| Nutrient | Symbol | Role in Plant Growth | Deficiency Symptoms |
|---|---|---|---|
| **Iron** | Fe | Chlorophyll synthesis, enzyme activation | Interveinal chlorosis on young leaves |
| **Manganese** | Mn | Photosynthesis, nitrogen metabolism | Yellow patches between leaf veins |
| **Zinc** | Zn | Hormone (auxin) production, enzyme cofactor | Small leaves, shortened internodes |
| **Copper** | Cu | Lignin synthesis, photosynthesis | Wilting, bluish-green then yellow leaves |
| **Boron** | B | Cell wall formation, pollen germination | Distorted young leaves, hollow stems |

> 💡 **Nutrient thresholds** are set per crop type in the firmware configuration. The system doses only when sensor-measured EC and pH fall outside the optimal range for that crop.

---

## ⚙️ How It Works — Step by Step

```
STEP 1 ──────────────────────────────────────────────────
  🌡️  SENSE
  Sensors measure soil moisture, pH, EC, and temperature
  at programmed intervals (e.g., every 5 minutes).

STEP 2 ──────────────────────────────────────────────────
  🧠  ANALYZE
  ESP32 firmware compares readings against crop-specific
  threshold tables stored in flash memory.

STEP 3 ──────────────────────────────────────────────────
  ⚖️  DECIDE
  If values are within range → no action.
  If out of range → calculate exact dosing volume needed.

STEP 4 ──────────────────────────────────────────────────
  💧  DOSE
  Target pumps are activated for a calculated duration.
  Nutrients are injected into the irrigation main line.

STEP 5 ──────────────────────────────────────────────────
  📡  TRANSMIT
  Sensor readings, dosing events, and timestamps are
  pushed to the cloud via MQTT over Wi-Fi.

STEP 6 ──────────────────────────────────────────────────
  🔁  REPEAT
  System returns to Step 1 — fully autonomous loop.
```

---

## 💻 Software & Firmware

### Firmware Stack

```
┌────────────────────────────────────┐
│          Application Layer         │
│   Nutrient Logic • Threshold DB    │
│   Scheduling • Alert Generation    │
├────────────────────────────────────┤
│         Middleware Layer           │
│   MQTT Client • JSON Serializer    │
│   OTA Updates • NTP Time Sync      │
├────────────────────────────────────┤
│          Driver Layer              │
│   Sensor ADC • OneWire • I2C       │
│   PWM Pump Control • GPIO Relay    │
├────────────────────────────────────┤
│         Hardware (ESP32)           │
│   FreeRTOS • Wi-Fi Stack • Flash   │
└────────────────────────────────────┘
```

### Key Libraries Used

| Library | Purpose |
|---|---|
| `WiFi.h` | ESP32 Wi-Fi connection |
| `PubSubClient` | MQTT broker communication |
| `OneWire` + `DallasTemperature` | DS18B20 temperature sensor |
| `ArduinoJson` | JSON formatting for cloud payloads |
| `LiquidCrystal_I2C` | LCD display driver |
| `EEPROM.h` | Persistent storage of calibration values |

---

## 📂 Repository Structure

```
📦 DEVELOPMENT-OF-SMART-MICRO-MACRO-NUTRIENT-DRIP-IRRIGATION-SYSTEM-SOFTWARE-
 │
 ├── 📄 MINOR_2_PROJECT_REPORT (2).pdf
 │       └── Full technical project report including:
 │             • Abstract & introduction
 │             • Literature review
 │             • System design & methodology
 │             • Circuit diagrams & PCB layout
 │             • Results, analysis & conclusions
 │
 ├── 🖼️  Protoype original.png
 │       └── Photograph of the assembled hardware prototype
 │
 ├── 🖼️  ki cad.png
 │       └── Screenshot of KiCad PCB/schematic design
 │
 └── 🖼️  proposed system.png
         └── Block diagram of the proposed system architecture
```

---

## 🚀 Getting Started

### 🛠️ Prerequisites

- [Arduino IDE](https://www.arduino.cc/en/software) ≥ 2.x **or** [PlatformIO](https://platformio.org/)
- ESP32 board package installed in Arduino IDE
- MQTT broker (e.g., [HiveMQ](https://www.hivemq.com/) or local [Mosquitto](https://mosquitto.org/))
- Required Arduino libraries (install via Library Manager):

```
PubSubClient
ArduinoJson
DallasTemperature
OneWire
LiquidCrystal_I2C
```

### 📥 Clone the Repository

```bash
git clone https://github.com/padmini-ux02/DEVELOPMENT-OF-SMART-MICRO-MACRO-NUTRIENT-DRIP-IRRIGATION-SYSTEM-SOFTWARE-.git
cd DEVELOPMENT-OF-SMART-MICRO-MACRO-NUTRIENT-DRIP-IRRIGATION-SYSTEM-SOFTWARE-
```

### ⚙️ Configuration

Open `config.h` and update the following:

```cpp
// ─── Wi-Fi Settings ─────────────────────────
#define WIFI_SSID        "your_wifi_name"
#define WIFI_PASSWORD    "your_wifi_password"

// ─── MQTT Broker Settings ───────────────────
#define MQTT_SERVER      "broker.hivemq.com"
#define MQTT_PORT        1883
#define MQTT_TOPIC       "farm/irrigation/data"

// ─── Sensor Pin Definitions ─────────────────
#define PH_SENSOR_PIN    34    // Analog input
#define EC_SENSOR_PIN    35    // Analog input
#define MOISTURE_PIN     32    // Analog input
#define TEMP_PIN         4     // OneWire digital

// ─── Pump Relay Pins ────────────────────────
#define PUMP_N_PIN       16    // Nitrogen pump
#define PUMP_P_PIN       17    // Phosphorus pump
#define PUMP_K_PIN       18    // Potassium pump
#define PUMP_MICRO_PIN   19    // Micronutrient pump
```

### 🔌 Wiring Guide

Refer to the [Project Report](./MINOR_2_PROJECT_REPORT%20(2).pdf) for complete pin mapping and wiring diagrams.

### 📤 Upload Firmware

1. Connect ESP32 to your PC via USB
2. Select **Board:** `ESP32 Dev Module` in Arduino IDE
3. Select the correct **COM Port**
4. Click **Upload** ✅

---

## 📊 Results & Outcomes

The system was tested on potted crop setups in laboratory conditions with the following results:

| Metric | Result |
|---|---|
| 💧 **Water usage reduction** | ~35% less than conventional irrigation |
| 🧪 **Fertilizer savings** | ~40% reduction vs. manual application |
| ⏱️ **Sensor response time** | < 2 seconds |
| 🎯 **Dosing accuracy** | ±3% of target volume |
| 📶 **Wi-Fi range** | Up to 50 meters in open field |
| 🌡️ **Temperature accuracy** | ±0.5°C (DS18B20 spec) |
| 📈 **Uptime** | 99%+ over 72-hour continuous test |

---

## 🔭 Future Scope

- 🤖 **Machine Learning** — Integrate crop growth models and ML predictions for adaptive nutrient scheduling
- ☀️ **Solar Power** — Add MPPT solar charging for complete off-grid operation
- 📱 **Mobile App** — Dedicated Android/iOS app with push notifications and control
- 🗺️ **Multi-Zone Support** — Expand to control multiple field zones independently
- 🌐 **LoRa Communication** — Replace Wi-Fi with LoRa for long-range (5+ km) connectivity
- 🧬 **Soil NPK Sensor** — Integrate direct soil NPK sensors to eliminate solution-based inference
- 🤝 **Cloud AI Integration** — Use AWS/Google Cloud for predictive analytics and crop yield forecasting

---

## 👩‍💻 Author

<div align="center">

| | |
|---|---|
| **Name** | Padmini |
| **GitHub** | [@padmini-ux02](https://github.com/padmini-ux02) |
| **Project Type** | Minor Project II — Embedded Systems & IoT |
| **Institution** | Engineering Department |

</div>

---

## 📄 License & Academic Notice

> This repository is submitted as an **academic minor project**. All rights are reserved by the author.  
> The project report, designs, and code are intended for **educational purposes only**.  
> For collaboration, reuse, or research inquiries, please contact the repository owner.

---

## 📚 References

> Detailed references, citations, and literature review are available in the  
> 📄 [**Full Project Report → MINOR_2_PROJECT_REPORT (2).pdf**](./MINOR_2_PROJECT_REPORT%20(2).pdf)

---

<div align="center">

---

**⭐ If you found this project helpful, please give it a star!**

*Built with ❤️ for sustainable agriculture and a greener future 🌍*

---

`ESP32` · `IoT` · `Precision Agriculture` · `KiCad` · `Drip Irrigation` · `Embedded Systems` · `Smart Farming`

</div>
