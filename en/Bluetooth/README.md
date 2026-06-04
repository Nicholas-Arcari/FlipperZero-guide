# Bluetooth Low Energy (BLE) - Overview

BLE 5.0 module integrated into the Flipper Zero's **STM32WB55RG** MCU. Used for BLE Spam (advertising PDU spoofing), BLE HID (BadBT keyboard/mouse), device scanner, companion app, and serial communication.

**Chip:** STM32WB55 (BLE 5.0) | **Range:** 10-30m | **Bands:** 2.4 GHz ISM | **ADV Channels:** 37, 38, 39

---

## Contents

| # | File | Description |
|---|------|-------------|
| 01 | [Technical Fundamentals](01-Fondamenti-Tecnici.md) | BLE 5.0 stack, advertising PDU, connection architecture, GATT, GAP, pairing |
| 02 | [Hardware and Limitations](02-Hardware-e-Limiti.md) | STM32WB55 BLE capabilities, TX power, real-world range, Flipper limitations |
| 03 | [Protocols and Features](03-Protocolli.md) | BLE HID, Serial CLI, Companion App, Remote Control, BLE Scanner |
| 04 | [Operational Guide - BLE Spam](04-Guida-Operativa.md) | BLE Spam deep dive: Apple (AirPods, AirTag, Handoff), Samsung (Galaxy, SmartTag), Google Fast Pair, Windows Swift Pair, crafting PDU |
| 05 | [Real-World Scenarios](05-Scenari-Reali.md) | Pentest scenarios: BLE spam in corporate environments, device enumeration, BLE HID injection, disruption assessment |
| 06 | [Attacks and Defenses](06-Attacchi-e-Difese.md) | BLE spam, MITM, eavesdropping, replay, downgrade - attacks and countermeasures |
| 07 | [Legal Aspects](07-Aspetti-Legali.md) | Italian/EU regulations for BLE testing |
| 08 | [Personal Experience](08-Esperienza-Personale.md) | Troubleshooting, field notes, limitations, resources |

---

## Quick Reference - BLE Features

| Feature | Description | Pentest Use |
|----------|-------------|-------------|
| BLE Spam | Advertising PDU spoofing (Apple/Samsung/Google/Windows) | Disruption, awareness testing |
| BLE HID (BadBT) | Wireless Bluetooth keyboard/mouse | Wireless keystroke injection |
| BLE Scanner | Scanning nearby BLE devices | Reconnaissance, device enumeration |
| Companion App | Remote Flipper control via smartphone | Remote management |
| Serial CLI | Serial console over BLE | Debug, scripting |

> **Personal note:** BLE Spam is the most visually impressive tool on the Flipper - it generates notifications on every iPhone/Samsung/Android in the room. In a pentest it's useful to demonstrate how easily fake notifications can be generated. BLE HID (BadBT) is more operationally useful - it's a wireless BadUSB that works up to 10-15 meters away.
