# FLIPBOARD - Operational Guide

Modular addon with physical buttons, RGB LEDs, and integrated traces, designed as an intelligent breadboard for rapid prototyping and I/O interaction with the Flipper Zero.

---

## Hardware

The Flipboard connects to the Flipper's GPIO header and provides:
- **4 physical buttons** mapped to GPIO pins
- **4 RGB LEDs** controllable via PWM
- **Connection traces** for external components
- **Prototyping area** for quick soldering

---

## Tools

### Flipboard Blinky

Direct control of the integrated LEDs.

**Features:**
- Individual on/off control of the 4 LEDs
- Customizable blinking patterns (frequency, duty cycle)
- RGB color control via PWM on three channels
- Quick test of GPIO -> LED pinout

**Practical usage:**
- Verification of the Flipper <-> Flipboard connection
- Visual debugging: assign an LED to an event (e.g., red LED = error, green = success)
- Status indicator during automated GPIO scripts

### Flipboard Keyboard

Transforms the Flipboard buttons into a programmable macro pad.

**Features:**
- Mapping of each button to an action (UART send, GPIO command, LED toggle)
- "Macro" mode: predefined sequences for each key
- Support for combinations and multi-step sequences

**Usage in pentesting:**
- Macro pad for frequent actions during an engagement
- Button 1: start WiFi scan, Button 2: capture Sub-GHz, Button 3: toggle status LED, Button 4: save log
- Quick automation without navigating menus

### Flipboard Signal

Electrical signal monitoring on Flipboard pins.

**Features:**
- Real-time digital HIGH/LOW reading
- Logic level analysis with display visualization
- Low-speed input signal detection
- LED indication of logic level

**Usage:** diagnostics of sensors, external buttons, relays, transistors. Useful for verifying that a circuit works before connecting it to the Flipper.

### Flipboard Simon

"Simon Says" game with LEDs and buttons -- color sequences to memorize.

**Educational value:** demonstrates full GPIO I/O usage (button input + LED output + game logic). Excellent example for understanding how interrupts, debounce, and timing work on GPIO.

> **Personal note:** The Flipboard is more of a maker tool than a pentester tool, but I've used it as a macro pad during long engagements. Having 4 physical buttons mapped to frequent actions speeds up the work when you spend hours capturing RF signals or testing NFC badges.
