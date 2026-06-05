# WiFi Marauder - Overview

WiFi module based on **ESP32** with **Marauder** firmware for 802.11 wireless penetration testing. Enables network scanning, deauthentication, evil portal, PMKID/handshake capture, beacon spam, probe flood, and wardriving.

**Hardware:** ESP32 WiFi Devboard | **Frequency:** 2.4 GHz | **Standard:** 802.11 b/g/n | **Firmware:** ESP32 Marauder

---

## Reference Videos

Flipper Zero - Tutorial Italiano - 15 - WIFI MARAUDER ( https://www.youtube.com/watch?v=z3ft9ND-3iA )

Flipper Zero - Tutorial Italiano - 17 - WIFI MARAUDER ( https://www.youtube.com/watch?v=CP0cmj3byJE )

---

## Contents

| # | File | Description |
|---|------|-------------|
| 01 | [Technical Fundamentals](01-Fondamenti-Tecnici.md) | 802.11 frame architecture, Beacon, Probe, Authentication, Association, 4-Way Handshake WPA2, PMKID |
| 02 | [Hardware and Flash](02-Hardware-e-Limiti.md) | ESP32 devboard specs, Marauder flash procedure (Web/CLI/manual), Flipper configuration |
| 03 | [802.11 Protocols](03-Protocolli.md) | Deep dive into frame architecture, management/control/data, WPA2 key derivation, PMKID math |
| 04 | [Operational Guide](04-Guida-Operativa.md) | Tool-by-tool: Scan, Sniff (PMKID/Handshake/Raw), Deauth, Beacon Spam, Probe Flood, Evil Portal, Wardriving |
| 05 | [Real-World Scenarios](05-Scenari-Reali.md) | Pentest scenarios: corporate WiFi assessment, evil twin, WPA2 handshake capture, guest network, rogue AP detection |
| 06 | [Attacks and Defenses](06-Attacchi-e-Difese.md) | Deauth, Evil Portal, PMKID, Handshake, Beacon Spam, Wardriving - attacks and countermeasures (802.11w, WPA3, WIDS) |
| 07 | [Legal Aspects](07-Aspetti-Legali.md) | Italian/EU regulations for WiFi testing, Art. 617-quater, operational rules |
| 08 | [Personal Experience](08-Esperienza-Personale.md) | Flash/connection troubleshooting, field notes, mistakes to avoid, resources |

---

## Quick Reference - Main Marauder Commands

| Command | Function | Pentest Use |
|---------|----------|-------------|
| `scanap` | Access Point scanning | Reconnaissance |
| `scansta` | Station (client) scanning | Client enumeration |
| `sniffpmkid` | PMKID capture | WPA2 password recovery |
| `sniffraw` | 4-way handshake capture | WPA2 password recovery |
| `deauth` | Deauthentication frame | DoS / force reconnection |
| `evilportal` | Fake captive portal | Credential harvesting |
| `beaconspam` | Massive fake SSIDs | Confusion / cover |
| `probeflood` | Probe Request flood | AP DoS |
| `wardrive` | Scanning + GPS | WiFi mapping |

> **Personal note:** WiFi Marauder turns the Flipper into a portable WiFi pentest tool. It does not replace a laptop with aircrack-ng, but for quick reconnaissance, deauth testing, and evil portal it is excellent. PMKID capture works surprisingly well - during an engagement I recovered 3 PMKIDs in less than 5 minutes and cracked the WPA2 password with hashcat in 2 hours.
