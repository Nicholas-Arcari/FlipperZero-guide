# NFC - Overview

Contactless communication module operating at **13.56 MHz** based on the **ST25R3916** chip for reading, writing, emulating, and analyzing NFC tags and cards. Covers ISO 14443A/B, MIFARE Classic/Ultralight/DESFire, iClass/PicoPass, and EMV payment cards.

**Chip:** ST25R3916 | **Frequency:** 13.56 MHz | **Range:** 3-5 cm | **Standards:** ISO 14443A/B, ISO 15693

---

## Contents

| # | File | Description |
|---|------|-------------|
| 01 | [Technical Fundamentals](01-Fondamenti-Tecnici.md) | NFC vs RFID, ISO 14443, RF field, inductive coupling, anti-collision |
| 02 | [Hardware and Limitations](02-Hardware-e-Limiti.md) | ST25R3916, range limitations, power, coil positioning |
| 03 | [Protocols](03-Protocolli.md) | Tag types (MIFARE Classic/UL/DESFire, iClass, NTAG), SAK/ATQA identification, memory structure, Crypto-1 |
| 04 | [Operational Guide](04-Guida-Operativa.md) | Tool-by-tool: Read, Detect Reader, Emulate, MFKey32, Dictionary Attack, MIFARE Editor, Fuzzer, APDU Runner, Comparator, Magic, Sniffer, Relay, PicoPass |
| 05 | [Real-World Scenarios](05-Scenari-Reali.md) | 7 detailed scenarios: corporate badge, hotel card, relay attack, multi-floor privilege escalation, cafeteria/credit, public transit, red team datacenter |
| 06 | [Attacks and Defenses](06-Attacchi-e-Difese.md) | Magic Card (Gen1-4), Crypto-1 recovery, dictionary attack, clone-and-replay, UID-only bypass, relay attack |
| 07 | [Legal Aspects](07-Aspetti-Legali.md) | Art. 615-ter, 640-ter Italian Criminal Code, GDPR, Magic Card and dump handling |
| 08 | [Personal Experience](08-Esperienza-Personale.md) | Complete troubleshooting, field notes, mistakes to avoid, best practices |

---

## Quick Reference - Tag Identification by SAK

| SAK | Type | Vulnerability | Approach |
|-----|------|---------------|-----------|
| 0x08 | MIFARE Classic 1K | Crypto-1 | Dict → MFKey32 → Clone |
| 0x18 | MIFARE Classic 4K | Crypto-1 | Dict → MFKey32 → Clone |
| 0x04 | MIFARE Ultralight | No crypto | Direct Read |
| 0x44 | MIFARE Ultralight C | 3DES | Password attack |
| 0x20 | MIFARE DESFire | AES (strong) | Very difficult |
| 0x20 | NTAG 21x | 32-bit password | Bruteforce (slow) |
| N/A | iClass Legacy | Weak DES | PicoPass tools |
| N/A | iClass SE | AES (strong) | Not feasible |

## Quick Reference - Operational Workflow

```
NFC → Read → Identify SAK
  ├─ SAK 0x08/0x18 (MIFARE Classic) → Dictionary Attack
  │   ├─ All keys found → Full dump → Clone to Magic Card
  │   └─ Missing keys → Detect Reader → MFKey32 → Re-read → Clone
  ├─ SAK 0x04 (Ultralight) → Direct Read → Emulate/Clone
  ├─ SAK 0x20 (DESFire) → Document in report as "secure"
  └─ Unrecognized → Read RAW → Manual analysis
```

> **Personal note:** 60% of Italian offices still use MIFARE Classic 1K. Cloning takes less than 30 seconds. Always carry at least 10 Gen4 Magic Cards - emulation fails in 40% of field cases.
