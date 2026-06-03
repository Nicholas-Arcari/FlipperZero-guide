# Sub-GHz - Overview

Radio communication module operating at frequencies below 1 GHz, based on the **Texas Instruments CC1101** chip. It covers the ISM bands (300-348, 387-464, 779-928 MHz) used for remote controls, sensors, alarms, home automation, pagers, and industrial systems.

**Chip:** CC1101 | **TX Power:** +12 dBm (~16 mW) | **Modulations:** OOK/ASK, 2-FSK, GFSK, MSK | **Real-world range:** 5-15m indoor, 30-50m LOS

---

## Contents

| # | File | Description |
|---|------|-------------|
| 01 | [Technical Fundamentals](01-Fondamenti-Tecnici.md) | Frequency bands, modulations, how Sub-GHz RF communication works |
| 02 | [Hardware and Limitations](02-Hardware-e-Limiti.md) | CC1101 specifications, range/power limitations, external antenna, frequency gaps |
| 03 | [Protocols](03-Protocolli.md) | OOK/ASK/FSK deep dive, fixed code and rolling code protocols, KeeLoq, complete tables |
| 04 | [Operational Guide](04-Guida-Operativa.md) | Complete tool-by-tool guide: Read, Read RAW, Frequency Analyzer, Bruteforcer, Rolling Flaws, POCSAG, Weather Station, TPMS, Chat, Playlist, Remote, Scheduler, and all the others |
| 05 | [Real-World Scenarios](05-Scenari-Reali.md) | 8 detailed pentest scenarios: gate bypass, wireless alarm, TPMS/Pager OSINT, corporate barrier, industrial IoT, home automation, multi-tenant, incident response |
| 06 | [Attacks and Defenses](06-Attacchi-e-Difese.md) | Replay, RollJam, Bruteforce, Jamming, Side-Channel KeeLoq - principle, procedure, and countermeasures |
| 07 | [Legal Aspects](07-Aspetti-Legali.md) | Italian regulations (Criminal Code art. 617-quater, 615-ter, D.Lgs. 259/2003), EU (RED, ETSI, GDPR), operational rules |
| 08 | [Personal Experience](08-Esperienza-Personale.md) | Complete troubleshooting, field notes, mistakes to avoid, operational best practices |

---

## Quick Reference - Main Frequencies

| Frequency | Use | Region |
|-----------|-----|--------|
| 315.00 MHz | US remote controls, US car keys | North America |
| 433.92 MHz | Gates, sensors, weather, TPMS | Europe/Asia |
| 433.42 MHz | Somfy RTS (roller shutters) | Europe |
| 434.42 MHz | EU variant from some manufacturers | Europe |
| 466.075 MHz | POCSAG pagers | Italy |
| 868.35 MHz | EU home automation, FAAC, alarms | Europe |
| 915.00 MHz | ISM band, LoRa US | North America |

---

## Quick Reference - Common Protocols in Italy

| Protocol | Type | Bits | Security | Prevalence |
|-----------|------|-----|-----------|------------|
| Nice FLO | Fixed | 12 | None | Gates pre-2010 |
| Came 12-bit | Fixed | 12 | None | Gates pre-2010 |
| Princeton | Fixed | 24 | Low | Chinese clones, generic |
| Nice FLOR/Smilo | Rolling | 52/66 | Medium-High | Gates post-2012 |
| Came TOP | Rolling | 64 | High | Gates post-2012 |
| FAAC SLH | Rolling | 64 | High | Gates/garages |
| Somfy RTS | Rolling | 56 | Medium | Roller shutters/awnings |
| KeeLoq generic | Rolling | 66 | Medium-High | Multi-brand |

> **Personal note:** 90% of field work in Italy is focused on 433.92 MHz and 868.35 MHz. The majority of pre-2010 residential gates still use fixed code and can be cloned in 5 seconds. For serious engagements, always bring an external CC1101 antenna and a HackRF as backup.
