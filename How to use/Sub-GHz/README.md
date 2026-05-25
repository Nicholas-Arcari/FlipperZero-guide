# Sub-GHz - Overview

Modulo di comunicazione radio a frequenza inferiore a 1 GHz, basato sul chip **Texas Instruments CC1101**. Copre le bande ISM (300-348, 387-464, 779-928 MHz) utilizzate per telecomandi, sensori, allarmi, domotica, pager e sistemi industriali.

**Chip:** CC1101 | **TX Power:** +12 dBm (~16 mW) | **Modulazioni:** OOK/ASK, 2-FSK, GFSK, MSK | **Portata reale:** 5-15m indoor, 30-50m LOS

---

## Contenuti

| # | File | Descrizione |
|---|------|-------------|
| 01 | [Fondamenti Tecnici](01-Fondamenti-Tecnici.md) | Bande di frequenza, modulazioni, come funziona la comunicazione RF Sub-GHz |
| 02 | [Hardware e Limiti](02-Hardware-e-Limiti.md) | Specifiche CC1101, limiti di portata/potenza, antenna esterna, gap di frequenza |
| 03 | [Protocolli](03-Protocolli.md) | OOK/ASK/FSK deep dive, protocolli a codice fisso e rolling code, KeeLoq, tabelle complete |
| 04 | [Guida Operativa](04-Guida-Operativa.md) | Tool-by-tool completo: Read, Read RAW, Frequency Analyzer, Bruteforcer, Rolling Flaws, POCSAG, Weather Station, TPMS, Chat, Playlist, Remote, Scheduler e tutti gli altri |
| 05 | [Scenari Reali](05-Scenari-Reali.md) | 8 scenari di pentest dettagliati: bypass cancello, allarme wireless, OSINT TPMS/Pager, barriera aziendale, IoT industriale, domotica, multi-tenant, incident response |
| 06 | [Attacchi e Difese](06-Attacchi-e-Difese.md) | Replay, RollJam, Bruteforce, Jamming, Side-Channel KeeLoq - principio, procedura e contromisure |
| 07 | [Aspetti Legali](07-Aspetti-Legali.md) | Normativa italiana (c.p. art. 617-quater, 615-ter, D.Lgs. 259/2003), EU (RED, ETSI, GDPR), regole operative |
| 08 | [Esperienza Personale](08-Esperienza-Personale.md) | Troubleshooting completo, note dal campo, errori da evitare, best practice operative |

---

## Quick Reference - Frequenze Principali

| Frequenza | Uso | Regione |
|-----------|-----|---------|
| 315.00 MHz | Telecomandi USA, chiavi auto US | Nord America |
| 433.92 MHz | Cancelli, sensori, meteo, TPMS | Europa/Asia |
| 433.42 MHz | Somfy RTS (tapparelle) | Europa |
| 434.42 MHz | Variante EU alcuni produttori | Europa |
| 466.075 MHz | Pager POCSAG | Italia |
| 868.35 MHz | Domotica EU, FAAC, allarmi | Europa |
| 915.00 MHz | ISM band, LoRa US | Nord America |

---

## Quick Reference - Protocolli Comuni in Italia

| Protocollo | Tipo | Bit | Sicurezza | Diffusione |
|-----------|------|-----|-----------|------------|
| Nice FLO | Fisso | 12 | Nulla | Cancelli pre-2010 |
| Came 12-bit | Fisso | 12 | Nulla | Cancelli pre-2010 |
| Princeton | Fisso | 24 | Bassa | Cloni cinesi, generico |
| Nice FLOR/Smilo | Rolling | 52/66 | Media-Alta | Cancelli post-2012 |
| Came TOP | Rolling | 64 | Alta | Cancelli post-2012 |
| FAAC SLH | Rolling | 64 | Alta | Cancelli/garage |
| Somfy RTS | Rolling | 56 | Media | Tapparelle/tende |
| KeeLoq generico | Rolling | 66 | Media-Alta | Multi-brand |

> **Nota personale:** Il 90% del lavoro sul campo in Italia si concentra su 433.92 MHz e 868.35 MHz. La maggior parte dei cancelli residenziali pre-2010 è ancora a codice fisso e si clona in 5 secondi. Per engagement seri, porta sempre un'antenna CC1101 esterna e un HackRF come backup.
