# RFID 125 kHz - Overview

Module for reading, writing and emulating **125 kHz** (Low Frequency) RFID tags. Covers the EM4100, HID Prox, Indala, FDX-B protocols and supports writing to programmable T5577 tags.

**Frequency:** 125 kHz (+ 134.2 kHz for FDX-B) | **Range:** 3-8 cm | **Writing:** T5577 | **Protocols:** 20+

---

## Contents

| # | File | Description |
|---|------|-------------|
| 01 | [Technical Fundamentals](01-Technical-Fundamentals.md) | RFID LF, inductive coupling, ASK/FSK/PSK modulation, frame structure |
| 02 | [Hardware and Limitations](02-Hardware-and-Limitations.md) | Flipper LF antenna, real-world range, emulation/writing limitations |
| 03 | [Protocols](03-Protocols.md) | EM4100 (full 64-bit frame), HID Prox H10301 (26-bit), Indala, FDX-B (ISO 11784/11785), T5577 (Block 0 config word, multi-protocol emulation) |
| 04 | [Operational Guide](04-Operational-Guide.md) | Tool-by-tool: Read, Write, Emulate, Add Manually, EM4100 Key Generator, FDX-B Maker, RFID Fuzzer, T5577 MultiWriter, T5577 Raw Writer, DCF77, NFC/RFID Detector |
| 05 | [Real-World Scenarios](05-Real-World-Scenarios.md) | 7 detailed scenarios: EM4100 apartment building, corporate HID badge, reader fuzzing, hidden reader detection, multi-level parking garage, gym/anti-passback, red team building entry |
| 06 | [Attacks and Defenses](06-Attacks-and-Defenses.md) | Replay/cloning, brute force, jamming, long-range skimming, database manipulation |
| 07 | [Legal Aspects](07-Legal-Aspects.md) | Art. 615-ter/quater, 640-ter Italian Criminal Code, GDPR, legal operational procedures |
| 08 | [Personal Experience](08-Personal-Experience.md) | Complete troubleshooting, Flipper limitations, operational kit, mistakes to avoid, future of 125 kHz, references |

---

## Quick Reference - Main Protocols

| Protocol | Bits | Modulation | Security | Prevalence in Italy |
|-----------|-----|------------|-----------|-------------------|
| EM4100 | 64 (40 data) | ASK/Manchester | Zero | Apartment buildings, gyms, parking garages |
| HID H10301 | 26 | FSK2 | Zero | Offices, banks, hospitals |
| Indala | 26/29 | PSK1 | Zero | Rare (NATO buildings, USA) |
| FDX-B | 128 | ASK/NRZ | Read-only | Animal microchips (mandatory) |
| T5577 | Programmable | Any | Optional password | Universal write target |

## Quick Reference - Operational Workflow

```
RFID → Read → Identify protocol
  ├─ EM4100 → Clone to T5577 (5 seconds) → Test at reader
  ├─ HID H10301 → Note FC:CN → Clone to T5577 → Fuzz CN
  ├─ Indala → Clone to T5577 (less reliable) → Verify
  ├─ FDX-B → Read/emulate only (no real write)
  └─ Unknown → Proxmark3 for raw analysis
```

> **Personal note:** 90% of Italian apartment buildings use EM4100 with no encryption. Cloning takes less than 10 seconds. A Flipper and 10 T5577s in your pocket is all you need to demonstrate that the access control system is nothing but a security illusion.
