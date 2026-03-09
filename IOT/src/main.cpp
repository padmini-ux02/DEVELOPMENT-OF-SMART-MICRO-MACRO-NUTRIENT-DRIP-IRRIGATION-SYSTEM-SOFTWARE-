/*
 * ================================================================
 *  Smart Plant Micro-Macro Nutrient Doser – Drip Irrigation
 *  ----------------------------------------------------------------
 *  Platform  : Wokwi Simulator – ESP32 Dev Module
 *  Framework : Arduino (PlatformIO)
 *  Date      : 2026
 * ================================================================
 *
 *  PIN MAP
 *  -------
 *  GPIO 34  → Potentiometer wiper  (Soil Moisture – ADC1 ch.6)
 *  GPIO  4  → DS18B20 Data line    (1-Wire, 4.7 kΩ pull-up → 3.3 V)
 *  GPIO 27  → YF-S201 signal       (Simulated by "Flow Sim" button)
 *  GPIO 25  → Manual dose button   (Active-LOW, internal pull-up)
 *  GPIO 26  → Pump / LED           (HIGH = pump ON)
 * ================================================================
 */

#include <Arduino.h>
#include <DallasTemperature.h>
#include <OneWire.h>

// ── Pin definitions ────────────────────────────────────────────
#define MOISTURE_PIN 34 // Analogue – potentiometer wiper
#define ONE_WIRE_PIN 4  // DS18B20 data
#define FLOW_PIN 27     // YF-S201 pulse (simulated by button)
#define BUTTON_PIN 25   // Manual dose  (active-LOW)
#define PUMP_PIN 26     // Pump / LED output

// ── Tuning constants ───────────────────────────────────────────
#define MOISTURE_THRESHOLD 40   // % moisture – auto-pump below this
#define FLOW_K_FACTOR 7.5f      // YF-S201: pulses-per-second per L/min
#define SAMPLE_PERIOD_MS 2000UL // Serial print interval (ms)
#define DEBOUNCE_MS 50UL        // Button de-bounce window (ms)

// ── OneWire / DallasTemperature ────────────────────────────────
OneWire oneWire(ONE_WIRE_PIN);
DallasTemperature tempSensor(&oneWire);

// ── ISR state ─────────────────────────────────────────────────
volatile uint32_t flowPulses = 0; // incremented by ISR

// ── Runtime state ──────────────────────────────────────────────
bool pumpOn = false;
bool manualRequested = false;
uint32_t lastSample = 0;
uint32_t lastFlowReset = 0;
uint32_t lastDebounce = 0;

// ── Flow-sensor ISR ────────────────────────────────────────────
void IRAM_ATTR onFlowPulse() { flowPulses++; }

// ──────────────────────────────────────────────────────────────
//  readMoisture()  – returns 0-100 %
//  ADC reads 0-4095; potentiometer at max (4095 = dry, 0 = wet).
//  Inverted: 0 % adc → 100 % moist, 4095 adc → 0 % moist.
// ──────────────────────────────────────────────────────────────
float readMoisture() {
  int raw = analogRead(MOISTURE_PIN);
  float pct = 100.0f - (raw / 4095.0f * 100.0f);
  return constrain(pct, 0.0f, 100.0f);
}

// ──────────────────────────────────────────────────────────────
//  readTemperature()  – returns °C; returns -127 on error
// ──────────────────────────────────────────────────────────────
float readTemperature() {
  tempSensor.requestTemperatures();
  float t = tempSensor.getTempCByIndex(0);
  return t;
}

// ──────────────────────────────────────────────────────────────
//  getFlowRate()  – returns L/min
//  Captures pulse count since last call, computes frequency.
// ──────────────────────────────────────────────────────────────
float getFlowRate(uint32_t nowMs) {
  noInterrupts();
  uint32_t pulses = flowPulses;
  flowPulses = 0;
  interrupts();

  float elapsedSec = (nowMs - lastFlowReset) / 1000.0f;
  lastFlowReset = nowMs;

  if (elapsedSec <= 0.0f)
    return 0.0f;
  float hz = pulses / elapsedSec; // pulses per second
  return hz / FLOW_K_FACTOR;      // L / min
}

// ──────────────────────────────────────────────────────────────
//  setPump()  – drive LED / relay and track state
// ──────────────────────────────────────────────────────────────
void setPump(bool on) {
  if (pumpOn != on) {
    pumpOn = on;
    digitalWrite(PUMP_PIN, on ? HIGH : LOW);
  }
}

// ──────────────────────────────────────────────────────────────
//  printHeader()  – one-time startup banner
// ──────────────────────────────────────────────────────────────
void printHeader() {
  Serial.println();
  Serial.println(F("================================================"));
  Serial.println(F("  Smart Plant Nutrient Doser – Drip Irrigation  "));
  Serial.println(F("  ESP32 Dev Module | Wokwi Simulation            "));
  Serial.println(F("================================================"));
  Serial.println();
  Serial.println(F("  Controls:"));
  Serial.println(F("  • Rotate potentiometer  → change soil moisture"));
  Serial.println(F("  • Press BLUE  button    → manual nutrient dose "));
  Serial.println(F("  • Press GREEN button    → simulate water flow  "));
  Serial.println();
  Serial.println(F("  Auto-pump activates when moisture < 40 %       "));
  Serial.println(F("================================================"));
  Serial.println();
}

// ──────────────────────────────────────────────────────────────
//  setup()
// ──────────────────────────────────────────────────────────────
void setup() {
  Serial.begin(115200);
  delay(300);

  // GPIO configuration
  pinMode(PUMP_PIN, OUTPUT);
  digitalWrite(PUMP_PIN, LOW);

  pinMode(BUTTON_PIN, INPUT_PULLUP); // manual dose  – active LOW
  pinMode(FLOW_PIN, INPUT_PULLUP);   // flow pulses  – active LOW

  // Rising edge on flow pin = one pulse from YF-S201
  attachInterrupt(digitalPinToInterrupt(FLOW_PIN), onFlowPulse, RISING);

  // Start temperature sensor
  tempSensor.begin();

  // Initialise timers
  uint32_t now = millis();
  lastSample = now;
  lastFlowReset = now;

  printHeader();
}

// ──────────────────────────────────────────────────────────────
//  loop()
// ──────────────────────────────────────────────────────────────
void loop() {
  uint32_t now = millis();

  // ── 1. Manual button – debounced ──────────────────────────
  if (digitalRead(BUTTON_PIN) == LOW) {
    if ((now - lastDebounce) > DEBOUNCE_MS) {
      lastDebounce = now;
      manualRequested = true;
    }
  }

  // ── 2. Periodic sampling & output ─────────────────────────
  if ((now - lastSample) >= SAMPLE_PERIOD_MS) {
    lastSample = now;

    // ---- Sensor reads ----
    float moisture = readMoisture();
    float tempC = readTemperature();
    float flowRate = getFlowRate(now);

    // ---- Pump decision ----
    bool autoTrigger = (moisture < (float)MOISTURE_THRESHOLD);

    if (manualRequested) {
      setPump(true);
      manualRequested = false;
    } else {
      setPump(autoTrigger);
    }

    // ---- Serial Monitor output ----
    Serial.println(F("┌─────────────────────────────────────────┐"));

    Serial.print(F("│  Uptime       : "));
    uint32_t secs = now / 1000;
    Serial.print(secs / 60);
    Serial.print(F(" min "));
    Serial.print(secs % 60);
    Serial.println(F(" sec              │"));

    Serial.print(F("│  Soil Moisture: "));
    Serial.print(moisture, 1);
    Serial.print(F(" %"));
    if (autoTrigger) {
      Serial.print(F("  [LOW – auto pump]  "));
    } else {
      Serial.print(F("               "));
    }
    Serial.println(F("│"));

    Serial.print(F("│  Temperature  : "));
    if (tempC <= DEVICE_DISCONNECTED_C) {
      Serial.println(F("-- Sensor not found --        │"));
    } else {
      Serial.print(tempC, 2);
      Serial.println(F(" °C                     │"));
    }

    Serial.print(F("│  Flow Rate    : "));
    Serial.print(flowRate, 3);
    Serial.println(F(" L/min                  │"));

    Serial.print(F("│  Pump Status  : "));
    if (pumpOn) {
      Serial.println(F("[ON]  ★ Dosing nutrients         │"));
    } else {
      Serial.println(F("[OFF] – Standby                  │"));
    }

    Serial.println(F("└─────────────────────────────────────────┘"));
    Serial.println();
  }
}
