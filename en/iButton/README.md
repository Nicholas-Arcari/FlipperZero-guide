# iButton - Overview

Module for reading, writing, emulating, and analyzing **iButton** keys (1-Wire contact keys). Supports Dallas/Maxim DS1990A, Cyfral, and Metakom protocols, with write capability on RW1990 rewritable keys.

**Interface:** 1-Wire (contact) | **Protocols:** DS1990A, Cyfral, Metakom | **Write:** RW1990 | **ID:** 64 bit (8 byte)

---

## Contents

| # | File | Description |
|---|------|-------------|
| 01 | [Technical Fundamentals](01-Fondamenti-Tecnici.md) | 1-Wire protocol, bus electrical characteristics, timing, ROM commands, topology |
| 02 | [Hardware and Limitations](02-Hardware-e-Limiti.md) | Flipper's iButton interface, GPIO contact, range, physical limitations |
| 03 | [Protocols](03-Protocolli.md) | DS1990A (64-bit ROM, family code), Cyfral (pulse-based), Metakom, programmable RW1990 |
| 04 | [Operational Guide](04-Guida-Operativa.md) | Tool-by-tool: Read, Write, Emulate, Add Manually, Converter, Fuzzer |
| 05 | [Real-World Scenarios](05-Scenari-Reali.md) | Pentest scenarios: DS1990A apartment building, Cyfral/Metakom building, building assessment, industrial intercom, Italian city case studies |
| 06 | [Attacks and Defenses](06-Attacchi-e-Difese.md) | Cloning, bruteforce, fuzzing, bypass - attacks and countermeasures |
| 07 | [Legal Considerations](07-Aspetti-Legali.md) | Italian/EU regulations for iButton testing |
| 08 | [Personal Experience](08-Esperienza-Personale.md) | Troubleshooting, Flipper limitations, operational kit, mistakes to avoid, references |

---

## Quick Reference - Protocols

| Protocol | ID | Prevalence in Italy | Security | Clonable |
|-----------|-----|-------------------|-----------|-----------|
| DS1990A | 64 bit (8 byte) | Very high (apartment buildings) | Zero | Yes (RW1990) |
| Cyfral | Variable | Medium (older intercoms) | Zero | Yes (emulation) |
| Metakom | Variable | Medium (older intercoms) | Zero | Yes (emulation) |

## Quick Reference - Workflow

```
iButton → Read (contact with key) → Identify protocol
  ├─ DS1990A → Clone to RW1990 (3 seconds) → Test on intercom
  ├─ Cyfral → Emulation (not writable) → Test on intercom
  ├─ Metakom → Emulation (not writable) → Test on intercom
  └─ Not recognized → Check contact, retry with different angle
```

> **Personal note:** iButton DS1990A is still ubiquitous in Italian apartment buildings, especially in Rome, Milan, Turin, and Bologna. Cloning onto an RW1990 takes 3 seconds and costs 0.50 EUR per key. No encryption, no protection whatsoever.
