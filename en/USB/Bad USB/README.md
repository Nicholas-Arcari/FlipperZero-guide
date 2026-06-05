# BadUSB - Overview

**USB HID** (Human Interface Device) emulation module for keystroke injection attacks. The Flipper Zero presents itself as a USB keyboard and types commands automatically. Supports DuckyScript for cross-platform payload development.

**Emulation:** USB HID (keyboard) | **Language:** DuckyScript | **VID/PID:** configurable | **Target OS:** Windows, macOS, Linux, ChromeOS, Android

---

## Contents

| # | File | Description |
|---|------|-------------|
| 01 | [Technical Fundamentals](01-Fondamenti-Tecnici.md) | USB HID protocol, descriptors, keystroke injection, USB enumeration |
| 02 | [Hardware and Limitations](02-Hardware-e-Limiti.md) | Flipper as USB HID, VID/PID spoofing, typing speed, real-world limitations |
| 03 | [DuckyScript and Payloads](03-Protocolli.md) | DuckyScript syntax, commands, ALT codes, ALTSTRING, payloads for Windows/macOS/Linux |
| 04 | [Operational Guide](04-Guida-Operativa.md) | Step-by-step BadUSB, payload execution, configuration + [Scripts and Payloads](Script/README.md) |
| 05 | [Real-World Scenarios](05-Scenari-Reali.md) | Pentest scenarios: corporate laptop compromise, kiosk exploitation, EDR bypass, physical+BadUSB combo |
| 06 | [Attacks and Defenses](06-Attacchi-e-Difese.md) | Evasion techniques (LOLBins, AMSI bypass, VID/PID spoofing) + countermeasures (USB policies, MDM) |
| 07 | [Legal Aspects](07-Aspetti-Legali.md) | Italian/EU regulations for USB HID testing |
| 08 | [Personal Experience](08-Esperienza-Personale.md) | Troubleshooting, field notes, mistakes to avoid |

---

## Quick Reference - Basic DuckyScript Commands

| Command | Function | Example |
|---------|----------|---------|
| `DELAY` | Pause (ms) | `DELAY 1000` |
| `STRING` | Type text | `STRING cmd.exe` |
| `ENTER` | Press Enter | `ENTER` |
| `GUI` | Windows/Cmd key | `GUI r` (Run) |
| `ALT` | Alt key | `ALT F4` |
| `CTRL` | Ctrl key | `CTRL c` |
| `TAB` | Tab key | `TAB` |
| `ALTSTRING` | Type via ALT codes | `ALTSTRING ciao` |

## Quick Reference - Main Payloads

| Payload | OS | Purpose | Time |
|---------|-----|---------|------|
| Reverse shell PS | Windows | Remote shell | ~5s |
| WiFi password exfil | Windows | WiFi credential exfiltration | ~8s |
| Disable Defender | Windows | AV disabling | ~3s |
| Hidden admin user | Windows | Persistence | ~4s |
| Certutil download | Windows | File download | ~5s |
| Terminal + curl | macOS/Linux | Reverse shell/download | ~4s |

> **Personal note:** BadUSB is the most impactful tool in a physical pentest. 5 seconds of physical access to an unattended laptop = remote shell. The key is preparation: tested payload, calibrated timing, credible pretext. The most common mistake is not considering the target's keyboard layout.
