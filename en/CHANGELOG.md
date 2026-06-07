# Changelog

History of major changes to the repository.

---

## v4.0 - 2026-04-07 - Arsenal, automation, and professionalization

### Additions
- `INDEX.md` - navigable global index of all files, organized by module and by type
- `GLOSSARY.md` - technical glossary with 80+ terms (OOK, SAK, Crypto1, AMSI, LOLBin, etc.)
- `CONTRIBUTING.md` - contribution guide for the project
- `MITRE-ATTACK.md` - complete Flipper techniques → MITRE ATT&CK framework mapping with kill chain
- `REPORT-TEMPLATES.md` - report templates for 6 finding types (Sub-GHz, NFC, RFID, BadUSB, WiFi, IR)
- `WORKFLOW-DIAGRAMS.md` - 6 Mermaid diagrams (kill chain, NFC pipeline, Sub-GHz flow, BadUSB chain, WiFi Marauder, RFID decision)
- `README_EN.md` - English translation of the main README
- `scripts/setup-sd.sh` - bash script for SD card setup (structure + IR/NFC database download)
- `scripts/validate-files.py` - syntax validator for .sub/.nfc/.rfid/.ibtn/.ir files + link check
- `.github/workflows/validate.yml` - GitHub Actions CI for structure and file validation
- `payloads/` - BadUSB arsenal with 25+ payloads organized by OS and category:
  - Windows: recon (system, network, AD, security enum), reverse shell (PS, encrypted, LOLBin mshta/certutil), credential harvest (WiFi, browser, SAM, mimikatz), persistence (registry, schtask, WMI), evasion (Defender, AMSI, ETW), privilege escalation (UAC fodhelper, admin user), exfiltration (webhook, clipboard)
  - macOS: reverse shell, recon, LaunchAgent persistence
  - Linux: reverse shell, SSH key exfil, cron/bashrc persistence
  - Multi-OS: awareness demo (rickroll, wallpaper)

### Changes
- Root `README.md` updated with links to all new resources
- Obsolete RogueMaster firmware binaries removed (~1.1 GB)

---

## v3.0 - 2026-04-07 - Structural improvements

### Additions
- `CHEATSHEET.md` - printable quick reference for the field
- `LAB-SETUP.md` - guide to creating a home testing laboratory
- `CHANGELOG.md` - this file
- `examples/` folders with sample files for each module
- Cross-references between modules in multi-vector scenarios
- Example `.ir` files and links to the official IR database
- GPIO/Other components split into 7 sub-files by category

### Changes
- Root `README.md` updated to reflect the new split structure
- `USB/Altre componenti/README.md` expanded with security scenarios
- `RogueMaster/` - firmware binaries replaced with links to official releases

---

## v2.0 - 2026-04-05 - Engineering into sub-files

### Structural changes
Each main module was split into thematic sub-files:

```
Module/
├── README.md                    ← Index with links
├── 01-Fondamenti-Tecnici.md     ← Technical fundamentals
├── 02-Hardware-e-Limiti.md      ← Specifications and real-world limits
├── 03-Protocolli.md             ← Protocol deep dive
├── 04-Guida-Operativa.md        ← Tool-by-tool step-by-step
├── 05-Scenari-Reali.md          ← Pentest scenarios (EXPANDED)
├── 06-Attacchi-e-Difese.md      ← Attack vectors + countermeasures
├── 07-Aspetti-Legali.md         ← Italian/EU regulations
└── 08-Esperienza-Personale.md   ← Field notes + troubleshooting
```

### Split modules (8 files each)
- Sub-GHz, NFC, RFID, iButton, Infrared, Bluetooth, WiFi-Marauder, USB/BadUSB

### Split modules (6 files each)
- GPIO/ESP32, GPIO/NRF24, GPIO/Debug

### Expanded real-world scenarios
- Sub-GHz: from 3 to 8 scenarios
- NFC: from 3 to 7 scenarios
- RFID: from 4 to 7 scenarios

---

## v1.0 - 2026-04-04 - Low-level content expansion

### Changes
- All README.md files rewritten from high-level overviews to low-level operational guides
- Total content: from ~3,000 lines to ~17,000+ lines
- Perspective: senior cybersecurity analyst + senior penetration tester
- Added bit-level analysis for each protocol
- Added step-by-step procedures for each tool
- Added real-world penetration testing scenarios for each module
- Added legal aspects sections (Italy/EU) for each module
- Added detailed troubleshooting for each module
- Preserved all personal experience notes

### New modules
- `Bluetooth/` - BLE section created from scratch (1247 lines)
- `WiFi-Marauder/` - renamed from `Wifi-Maruder/`, rewritten (2300 lines)
- `GPIO/ESP32/` - renamed from `GPIO/EPS32/`, rewritten (1854 lines)
- `GPIO/NRF24/` - rewritten (1397 lines)
- `GPIO/Debug/` - rewritten (1410 lines)

### Structural fixes
- Fixed typo: `EPS32` → `ESP32`
- Fixed typo: `Wifi-Maruder` → `WiFi-Marauder`
- Root `README.md` rewritten as complete guide (236 lines)

---

## v0.1 - Pre-refactoring

Original version with high-level overviews (5-15 lines per tool), links to YouTube videos, firmware binaries in the repo.
