# Infrared - Overview

Infrared communication module for capturing, emulating, and analyzing IR signals. Covers NEC, RC5, RC6, Sony SIRC, Samsung, and Raw protocols. Includes the universal IR database for remote control of TVs, ACs, projectors, and other devices.

**LED:** TSAL6200 (940nm) | **Carrier:** 38 kHz | **Range:** 5-10m | **Protocols:** NEC, RC5, RC6, SIRC, Samsung, Raw

---

## Contents

| # | File | Description |
|---|------|-------------|
| 01 | [Technical Fundamentals](01-Technical-Fundamentals.md) | IR communication, OOK modulation, carrier frequency, line-of-sight, photodiode |
| 02 | [Hardware and Limitations](02-Hardware-and-Limitations.md) | TSAL6200, real-world range, emission angle, environmental limitations (sunlight) |
| 03 | [Protocols](03-Protocols.md) | NEC (9ms+4.5ms timing), RC5 (Manchester), RC6, Sony SIRC, Samsung, AC protocols (100+ bit), Raw capture |
| 04 | [Operational Guide](04-Operational-Guide.md) | Tool-by-tool: IR Receiver, Universal Remote, Learn New Remote, IR Scanner, Button Remapper, IR database |
| 05 | [Real-World Scenarios](05-Real-World-Scenarios.md) | Pentest scenarios: hotel TV/AC, conference room AV takeover, digital signage, universal IR database, HVAC assessment |
| 06 | [Attacks and Defenses](06-Attacks-and-Defenses.md) | IR replay, brute force power-off, AC manipulation, TV-B-Gone - attacks and countermeasures |
| 07 | [Legal Aspects](07-Legal-Aspects.md) | Italian/EU regulations for IR testing |
| 08 | [Personal Experience](08-Personal-Experience.md) | Troubleshooting, field notes, mistakes to avoid |

---

## Quick Reference - Main Protocols

| Protocol | Address | Command | Carrier | Used by |
|----------|---------|---------|---------|---------|
| NEC | 8/16 bit | 8 bit | 38 kHz | LG, older Samsung, Chinese brands |
| RC5 | 5 bit | 6 bit | 36 kHz | Philips, European brands |
| RC6 | 8 bit | 8 bit | 36 kHz | Philips, Microsoft MCE |
| Sony SIRC | 5 bit | 7 bit | 40 kHz | Sony TV, Blu-ray, PS |
| Samsung | 8 bit | 8 bit | 38 kHz | Samsung TV |
| Raw | N/A | N/A | Variable | AC, projectors, custom |

> **Personal note:** IR is often underestimated as an attack vector. In reality, unauthorized control of TVs, ACs, and projectors in corporate environments can cause significant disruption. The Flipper's universal database allows you to control most devices without even capturing the signal.

---

## Resources and Example Files

| Resource | Link | Description |
|----------|------|-------------|
| **Flipper IRDB** | [github.com/Lucaslhm/Flipper-IRDB](https://github.com/Lucaslhm/Flipper-IRDB) | Universal IR database: thousands of remotes for TVs, ACs, projectors, fans, LEDs |
| **Example files** | [examples/](../../examples/) | Example `.ir` files (NEC for TV, Raw for AC) with commented structure |
