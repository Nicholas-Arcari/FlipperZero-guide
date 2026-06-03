# Sub-GHz - Technical Fundamentals

## What is Sub-GHz

The term "Sub-GHz" refers to any radio communication at frequencies below 1 GHz. In the context of the Flipper Zero, it covers the ISM (Industrial, Scientific, Medical) bands used globally for:

- **Remote controls** for gates, garages, barriers, roller shutters
- **Wireless sensors** for alarms, weather stations, smoke detectors
- **Home automation systems** (Somfy, Nice, FAAC, Came, Beninca, etc.)
- **Pagers** (POCSAG on 466 MHz in Italy)
- **TPMS** (tire pressure monitoring sensors, 433.92 MHz)
- **Car keys** (315/433 MHz - analysis only, not unlocking)
- **Industrial devices** (telemetry, legacy wireless SCADA)
- **Analog walkie-talkies** (PMR446, FRS)
- **Drone remote controls** (FrSky, ELRS protocols on 868/915 MHz)

## How RF Communication Works

A Sub-GHz signal is a modulated electromagnetic wave that carries digital information. The basic process:

1. **The transmitter** (remote control) encodes a binary message
2. **Modulation** converts the bits into variations of the radio signal (amplitude, frequency, or phase)
3. **The signal travels** through the air at the speed of light
4. **The receiver** (gate control unit) demodulates the signal and verifies the code
5. **If the code is valid**, the receiver performs the action (opens the gate)

## Frequency Bands

The Flipper Zero covers these bands through the CC1101 chip:

| Band | Range | Typical Use | Region |
|---|---|---|---|
| **300-348 MHz** | 300.00 - 348.00 MHz | Legacy remote controls, industrial sensors | Global |
| **387-464 MHz** | 387.00 - 464.00 MHz | Garage remotes (433.92), pagers, TPMS, weather | EU/Asia |
| **779-928 MHz** | 779.00 - 928.00 MHz | US remotes (315), LoRa (868/915), sensors | US/EU |

The most commonly used frequencies in daily practice:

- **315.00 MHz** - US remote controls, American market car keys
- **433.92 MHz** - The most common in Europe: gates, sensors, weather, TPMS
- **434.42 MHz** - Variant used by some EU manufacturers
- **868.35 MHz** - EU home automation (Somfy, EnOcean), alarms
- **915.00 MHz** - American ISM band, LoRa US

> **Personal note:** 90% of field work in Italy is focused on 433.92 MHz and 868.35 MHz. I have rarely needed other frequencies in European engagements. 315 MHz is only needed when working with hardware imported from the US.
