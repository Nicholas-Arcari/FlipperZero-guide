# NRF24L01+ - Overview

Modulo transceiver **NRF24L01+** a 2.4 GHz collegato via GPIO per sniffing, jamming e hijacking di periferiche wireless (mouse, tastiere, presenter). Include il celebre attacco **MouseJacker**.

**Chip:** NRF24L01+ | **Frequenza:** 2.4 GHz ISM | **Canali:** 126 (2400-2525 MHz) | **Protocollo:** Enhanced ShockBurst | **Interfaccia:** SPI via GPIO

---

## Contenuti

| # | File | Descrizione |
|---|------|-------------|
| 01 | [Fondamenti e Hardware](01-Fondamenti-e-Hardware.md) | NRF24L01+ specs, Enhanced ShockBurst, 2.4 GHz ISM, wiring GPIO, antenna |
| 02 | [MouseJacker Deep Dive](02-MouseJacker-Deep-Dive.md) | Attacco MouseJacker: dispositivi vulnerabili, Logitech Unifying, keystroke injection via mouse wireless |
| 03 | [Tool Operativi](03-Tool-Operativi.md) | Sniffing NRF24, Jamming 2.4 GHz, Channel Scan, NRF24Monitor, Scanner, Batch operations |
| 04 | [Scenari Reali](04-Scenari-Reali.md) | Scenari pentest: wireless keyboard exploitation, meeting room attack, device enumeration |
| 05 | [Attacchi e Difese](05-Attacchi-e-Difese.md) | Aspetti legali + attacchi NRF24 + contromisure + tool Flipper dettaglio operativo |
| 06 | [Esperienza Personale](06-Esperienza-Personale.md) | Note dal campo, riepilogo, raccomandazioni |

---

## Quick Reference - Attacchi NRF24

| Attacco | Target | Complessità | Impatto |
|---------|--------|-------------|---------|
| MouseJacker | Mouse/tastiere wireless non criptati | Bassa | Keystroke injection |
| Sniffing | Comunicazioni NRF24 | Media | Intercettazione dati |
| Jamming 2.4 GHz | Qualsiasi dispositivo 2.4 GHz | Bassa | DoS |
| Channel Scan | Dispositivi NRF24 | Bassa | Reconnaissance |

> **Nota personale:** MouseJacker è devastante in ambienti office dove mouse e tastiere wireless economiche sono ovunque. In un engagement ho iniettato comandi in un mouse Logitech non-Unifying dalla sala riunioni adiacente - keystroke injection attraverso il muro. Il proprietario non ha capito cosa stesse succedendo.
