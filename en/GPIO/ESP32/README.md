# ESP32 - Overview

**ESP32** module as a WiFi/BLE coprocessor connected via GPIO to the Flipper Zero. Supports offensive WiFi (Marauder, Evil Portal), camera, network tools, BLE auditing, and various utilities.

**SoC:** ESP32-WROOM-32 / ESP32-S2 | **WiFi:** 802.11 b/g/n | **BLE:** 4.2 | **Flash:** 4-16 MB | **Interface:** UART via GPIO

---

## Contents

| # | File | Description |
|---|------|-------------|
| 01 | [Fundamentals and Hardware](01-Fondamenti-e-Hardware.md) | ESP32 specs, ESP32 vs ESP8266 comparison, firmware flash (Marauder, Evil Portal, Blackmagic), GPIO wiring |
| 02 | [Offensive WiFi Tools](02-Tool-WiFi-Offensivi.md) | AP/Station Scan, Deauth, Evil Portal, PMKID/Handshake Sniff, Beacon Spam, Probe Flood, Wardrive |
| 03 | [Network and BLE Tools](03-Tool-Network-e-BLE.md) | Camera tools, packet/signal monitor, BLE scan/spam, various tools (GPS, temperature, LED) |
| 04 | [Real-World Scenarios](04-Scenari-Reali.md) | WiFi pentest scenarios with ESP32: corporate assessment, evil portal engagement, handshake capture |
| 06 | [Personal Experience](06-Esperienza-Personale.md) | Field notes, flash troubleshooting, operational tips |

---

## Quick Reference - Available Firmware

| Firmware | Primary Function | Flash Tool |
|----------|-------------------|------------|
| ESP32 Marauder | Offensive WiFi (deauth, evil portal, sniff) | Web Flasher / esptool |
| Blackmagic | Debug probe (GDB) | esptool |
| Camera | Video streaming via WiFi | esptool |
| Evil Portal standalone | Captive portal phishing | esptool |

> **Personal note:** The ESP32 transforms the Flipper into a complete WiFi tool. The Marauder firmware is the most versatile -- it covers 90% of WiFi pentest needs. For specific engagements, I flash dedicated firmware (e.g., Evil Portal for targeted credential harvesting).
