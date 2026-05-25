# ESP32 - Overview

Modulo **ESP32** come coprocessore WiFi/BLE collegato via GPIO al Flipper Zero. Supporta WiFi offensivo (Marauder, Evil Portal), camera, tool di rete, BLE auditing e utility varie.

**SoC:** ESP32-WROOM-32 / ESP32-S2 | **WiFi:** 802.11 b/g/n | **BLE:** 4.2 | **Flash:** 4-16 MB | **Interfaccia:** UART via GPIO

---

## Contenuti

| # | File | Descrizione |
|---|------|-------------|
| 01 | [Fondamenti e Hardware](01-Fondamenti-e-Hardware.md) | ESP32 specs, confronto ESP32 vs ESP8266, flash firmware (Marauder, Evil Portal, Blackmagic), wiring GPIO |
| 02 | [Tool WiFi Offensivi](02-Tool-WiFi-Offensivi.md) | Scan AP/Station, Deauth, Evil Portal, Sniff PMKID/Handshake, Beacon Spam, Probe Flood, Wardrive |
| 03 | [Tool Network e BLE](03-Tool-Network-e-BLE.md) | Camera tools, packet/signal monitor, BLE scan/spam, tool vari (GPS, temperature, LED) |
| 04 | [Scenari Reali](04-Scenari-Reali.md) | Scenari pentest WiFi con ESP32: corporate assessment, evil portal engagement, handshake capture |
| 06 | [Esperienza Personale](06-Esperienza-Personale.md) | Note dal campo, troubleshooting flash, consigli operativi |

---

## Quick Reference - Firmware Disponibili

| Firmware | Funzione Principale | Flash Tool |
|----------|-------------------|------------|
| ESP32 Marauder | WiFi offensive (deauth, evil portal, sniff) | Web Flasher / esptool |
| Blackmagic | Debug probe (GDB) | esptool |
| Camera | Streaming video via WiFi | esptool |
| Evil Portal standalone | Captive portal phishing | esptool |

> **Nota personale:** L'ESP32 trasforma il Flipper in un tool WiFi completo. Il firmware Marauder è il più versatile - copre il 90% delle esigenze di un WiFi pentest. Per engagement specifici, flasho firmware dedicati (es. Evil Portal per credential harvesting mirato).
