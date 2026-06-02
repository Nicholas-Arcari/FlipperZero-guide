# Flipper Zero - Advanced Operational Guide

In-depth technical guide to using the Flipper Zero in cybersecurity, physical penetration testing, RF analysis, hardware reverse engineering, and security research.

This repository was born from direct field experience with the device and documents every module, protocol, and technique at an operational level - not as a superficial overview, but as a practical reference for those who work (or want to work) in offensive and defensive security.

> **Personal note:** This project collects years of real-world experimentation with the Flipper Zero. Every section includes personal experience notes, mistakes made, real limitations encountered, and workarounds discovered in the field. This is not a generic wiki - it is the operational notebook of a pentester.

---

## Ethical and Legal Disclaimer

All content in this repository is intended exclusively for:

- **Security research** on devices and systems you own
- **Authorized penetration testing** with a contract or written authorization
- **Training and study** in cybersecurity
- **Physical security audits** for organizations that request them

Using these techniques on devices, networks, or systems belonging to others without explicit authorization is **illegal** under the Italian Penal Code (Art. 615-ter, 617-quater, 617-quinquies) and European regulations.

**Possession of the Flipper Zero is legal in Italy and the EU.** Improper use of its capabilities is not.

---

## Hardware Overview

### Flipper Zero Technical Specifications

| Component | Detail |
|---|---|
| **MCU** | STM32WB55RG - ARM Cortex-M4 (64 MHz) + Cortex-M0+ for BLE |
| **Sub-GHz** | CC1101 transceiver - 300-348 MHz, 387-464 MHz, 779-928 MHz |
| **NFC** | ST25R3916 - ISO 14443A/B, ISO 15693, FeliCa, NFC-V |
| **RFID 125 kHz** | Custom LF antenna + integrated analog circuit |
| **Infrared** | TX LED TSAL6200 (940nm) + TSOP75338 receiver (38kHz) |
| **Bluetooth** | BLE 5.0 integrated in STM32WB55 |
| **GPIO** | 18 pins - 3.3V logic, 5V tolerant on some pins, UART/SPI/I2C/SWD |
| **USB** | USB-C 2.0 - CDC, HID, Mass Storage |
| **iButton** | Integrated 1-Wire pad on the back |
| **Storage** | microSD up to 256 GB (FAT32/exFAT) |
| **Battery** | LiPo 2000 mAh - ~7 days standby, ~2-4h intensive RF use |
| **Display** | Monochrome LCD 128x64 px |

### Firmware

This guide is primarily based on custom firmware **RogueMaster** and **Momentum**, which significantly extend the capabilities of the official firmware. The main differences:

- **Official Firmware:** basic features, no Sub-GHz transmission on restricted frequencies, limited protocol set
- **RogueMaster / Momentum / Unleashed:** frequency unlock, additional protocols, third-party apps, extended Sub-GHz, rolling code tools

> **Personal note:** I recommend RogueMaster or Momentum for those doing serious research. The official firmware is too limited for pentest activities. Flashing is reversible and does not void the hardware warranty.

---

## Repository Structure

```
How to use/
|-- Sub-GHz/            # RF 300-928 MHz: remotes, sensors, rolling code, TPMS, pagers
|-- NFC/                # 13.56 MHz: MIFARE, DESFire, NTAG, iClass, badges, transit cards
|-- RFID/               # 125 kHz: EM4100, HID Prox, T5577, access badges
|-- iButton/            # 1-Wire: Dallas keys, Cyfral, Metakom, intercoms
|-- Infrared/           # IR: TV/AC remotes, NEC/RC5/RC6 protocols, reverse engineering
|-- GPIO/               # External hardware: ESP32, ESP8266, NRF24, sensors, SWD/JTAG debug
|   |-- ESP32/          # WiFi/BLE: Marauder, Evil Portal, camera, wardriving
|   |-- ESP8266/        # WiFi: Deauther, scanner, IoT automation
|   |-- NRF24/          # 2.4 GHz: MouseJacker, sniffing, jamming
|   |-- Debug/          # SWD, JTAG, I2C, SPI, UART - hardware hacking
|   |-- Sensors/        # Environmental sensors, Geiger, gas, distance
|   |-- Malveke/        # Camera addon, printer, emulator
|   |-- Flipboard/      # Rapid prototyping with LEDs and buttons
|   |-- Games/          # Hardware mini-games (UART Pong, ToF Pong)
|   |-- VGM/            # Video Game Module
|   |-- Other components/ # GPS, LoRa, FM radio, automotive, security, utilities
|-- USB/                # HID attacks: BadUSB, DuckyScript, exfiltration, U2F
|   |-- Bad USB/        # Payloads, scripts, evasion, PoC
|   |-- Other components/ # Mass Storage, MIDI, U2F, controller, barcode
|-- WiFi-Marauder/      # WiFi Marauder setup and usage with ESP32
|-- Bluetooth/          # BLE: spam, sniffing, pairing, tracking, security
|-- RogueMaster/        # Custom firmware: download, comparison, installation
|
|-- examples/           # Example files for each module (.sub, .nfc, .rfid, .ibtn, .ir)
```

Each main module is organized into thematic sub-files:

| # | File | Content |
|---|------|---------|
| 01 | Technical Fundamentals | How the protocol works at a low level |
| 02 | Hardware and Limitations | Chip specs, antennas, real-world range |
| 03 | Protocols | Deep dive into each supported protocol |
| 04 | Operational Guide | Tool-by-tool step-by-step |
| 05 | Real-World Scenarios | Real pentest scenarios from the field |
| 06 | Attacks and Defenses | Attack vectors + countermeasures |
| 07 | Legal Aspects | Italian and EU regulations |
| 08 | Personal Experience | Field notes, mistakes, lessons learned |

### Additional Resources

| File | Description |
|------|-------------|
| [CHEATSHEET.md](CHEATSHEET.md) | Printable quick reference for the field (decision tree, frequencies, commands) |
| [LAB-SETUP.md](LAB-SETUP.md) | Guide to setting up a home test lab |
| [CHANGELOG.md](CHANGELOG.md) | Repository change history |

---

## Modules - Operational Overview

### Sub-GHz (300-928 MHz)

The most versatile module for a physical pentester. Covers garage remotes, gates, wireless sensors, pagers, weather stations, TPMS, and any device communicating on the ISM band. Includes rolling code analysis, replay attacks, bruteforce, and RF fuzzing.

**Real-world scenarios:** opening gates during physical pentest, home automation security analysis, hospital pager interception, vehicle TPMS study, reverse engineering proprietary remotes.

### NFC (13.56 MHz)

The critical module for access control system pentesting. Supports MIFARE Classic (with crypto1/mfkey32 attack), DESFire, NTAG, iClass/PicoPass, and transit cards. Enables cloning, emulation, relay attacks, and fuzzing.

**Real-world scenarios:** cloning corporate badges, bypassing turnstiles, hotel card analysis, contactless payment system testing, enterprise access control audits.

### RFID 125 kHz

The module for legacy access systems. Most commercial and residential buildings still use 125 kHz tags without encryption. Reading, emulation, and cloning are immediate.

**Real-world scenarios:** cloning apartment building badges, testing HID Prox readers, auditing industrial access systems, duplication onto T5577.

### iButton (1-Wire)

Contact-based access systems, very common in Eastern European and Italian intercoms. Supports DS1990A, Cyfral, and Metakom with reading, emulation, and fuzzing.

**Real-world scenarios:** cloning intercom keys, auditing building intercom systems, testing 1-Wire reader robustness.

### Infrared

Control of any device with an IR receiver. Useful for both automation and physical pentest scenarios where displays, TVs, or digital signage systems need to be controlled.

**Real-world scenarios:** turning off TVs/displays in target environments, AC control for social engineering, reverse engineering proprietary remotes, camera automation.

### GPIO - Hardware Hacking

The expansion interface that transforms the Flipper into a complete hardware hacking platform. With ESP32 it becomes an offensive WiFi tool, with NRF24 it attacks wireless peripherals, with SWD/JTAG it extracts firmware from embedded devices.

**Real-world scenarios:** WiFi deauth and evil portal with ESP32 Marauder, MouseJacker on wireless keyboards/mice, firmware dump via SWD, sniffing I2C/SPI/UART buses on IoT devices.

### USB - HID Attacks

BadUSB turns the Flipper into a malicious keyboard that executes automated payloads. It is the equivalent of a Rubber Ducky with the advantage of being field-programmable.

**Real-world scenarios:** drop attacks during physical pentest, WiFi credential exfiltration, privilege escalation, reverse shell deployment, kiosk evasion.

### WiFi (via ESP32 Marauder)

The Flipper Zero has no native WiFi - everything goes through the ESP32. With Marauder firmware it becomes a WiFi scanner, deauther, beacon spammer, and handshake sniffer.

**Real-world scenarios:** wireless reconnaissance during an engagement, deauth to force reconnections, evil portal for credential harvesting, wardriving.

### Bluetooth (BLE 5.0)

The integrated BLE module enables advertisement packet spam, analysis of nearby BLE devices, and integration with companion apps.

**Real-world scenarios:** BLE spam for disruption, device tracking, wearable security analysis, BLE service fuzzing.

---

## Methodology for Use in an Engagement

In a physical penetration test, the Flipper Zero fits into several phases:

### 1. Reconnaissance

- **Sub-GHz Frequency Analyzer** to identify RF devices in the target area
- **Radio Scanner** to map the active frequencies of a building
- **WiFi Scanner** (ESP32) to enumerate networks and clients
- **NFC/RFID Detector** to locate hidden badge readers
- **BLE Scanner** to identify IoT devices and wearables

### 2. Analysis

- **Sub-GHz Read** to capture and decode signals from remotes and sensors
- **NFC Read** to identify badge type and security
- **RFID Read** to classify 125 kHz tags
- **IR Decoder** to reverse engineer remotes
- **Spectrum Analyzer** to study the environment's RF spectrum

### 3. Exploitation

- **Sub-GHz Replay/Bruteforce** to test opening systems
- **NFC Emulate/Magic Write** to clone badges
- **RFID Emulate** to gain access with cloned badges
- **BadUSB** to execute payloads on workstations
- **Evil Portal** (ESP32) for WiFi credential harvesting
- **MouseJacker** (NRF24) for wireless peripheral hijacking

### 4. Post-Exploitation

- **BadUSB** for data exfiltration
- **Sub-GHz Scheduler** for persistence on RF systems
- **NFC Relay** to maintain access to badge systems

### 5. Reporting

- Logs of all detected frequencies
- Dumps of cloned badges (with hashes, not cleartext data)
- Screenshots of vulnerabilities found
- Mitigation recommendations for each finding

---

## Quick Reference - Useful Commands and Paths

### SD Card Paths

```
/ext/subghz/         - Recorded .sub files
/ext/nfc/            - Saved .nfc dumps
/ext/lfrfid/         - 125 kHz RFID files
/ext/ibutton/        - .ibtn files
/ext/infrared/       - .ir files and universal databases
/ext/badusb/         - DuckyScript / BadUSB scripts
/ext/apps/           - Installed applications
/ext/apps_data/      - Application data
/ext/subghz/assets/  - Frequency and protocol database
/ext/nfc/assets/     - MIFARE key dictionaries
```

### Important Configuration Files

```
/ext/subghz/assets/setting_user    - Custom Sub-GHz frequencies
/ext/nfc/assets/mf_classic_dict_user.nfc - Custom MIFARE keys
/ext/infrared/assets/tv.ir         - Universal IR database
```

---

## Useful External Resources

- **RogueMaster Firmware:** main GitHub repository for the custom firmware used in this guide
- **Flipper Zero Docs:** official documentation for API and hardware reference
- **MIFARE Classic Tool (Android):** companion app for NFC field analysis
- **Proxmark3:** reference for comparison with professional NFC/RFID tools
- **HackRF / RTL-SDR:** for advanced RF analysis beyond the capabilities of the CC1101
- **Wireshark:** for analysis of captured packet dumps

---

## About the Author

This guide is the result of daily hands-on experience with the Flipper Zero in the following contexts:

- Physical penetration testing on commercial and industrial buildings
- Access control system audits (NFC, RFID, iButton)
- Security research on consumer and industrial RF protocols
- Hardware hacking and reverse engineering of IoT devices
- Physical security training and awareness

Each section contains `> Personal note:` blocks that document real experiences, successes, failures, and lessons learned in the field.
