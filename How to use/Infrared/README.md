# Infrared - Overview

Modulo di comunicazione a infrarossi per la cattura, emulazione e analisi di segnali IR. Copre i protocolli NEC, RC5, RC6, Sony SIRC, Samsung e Raw. Include il database IR universale per il controllo remoto di TV, AC, proiettori e altri dispositivi.

**LED:** TSAL6200 (940nm) | **Carrier:** 38 kHz | **Portata:** 5-10m | **Protocolli:** NEC, RC5, RC6, SIRC, Samsung, Raw

---

## Contenuti

| # | File | Descrizione |
|---|------|-------------|
| 01 | [Fondamenti Tecnici](01-Fondamenti-Tecnici.md) | Comunicazione IR, modulazione OOK, carrier frequency, line-of-sight, foto-diodo |
| 02 | [Hardware e Limiti](02-Hardware-e-Limiti.md) | TSAL6200, portata reale, angolo di emissione, limiti ambientali (luce solare) |
| 03 | [Protocolli](03-Protocolli.md) | NEC (timing 9ms+4.5ms), RC5 (Manchester), RC6, Sony SIRC, Samsung, protocolli AC (100+ bit), Raw capture |
| 04 | [Guida Operativa](04-Guida-Operativa.md) | Tool-by-tool: IR Receiver, Universal Remote, Learn New Remote, IR Scanner, Button Remapper, database IR |
| 05 | [Scenari Reali](05-Scenari-Reali.md) | Scenari pentest: hotel TV/AC, conference room AV takeover, digital signage, database IR universale, HVAC assessment |
| 06 | [Attacchi e Difese](06-Attacchi-e-Difese.md) | Replay IR, brute force power-off, AC manipulation, TV-B-Gone - attacchi e contromisure |
| 07 | [Aspetti Legali](07-Aspetti-Legali.md) | Normativa italiana/EU per IR testing |
| 08 | [Esperienza Personale](08-Esperienza-Personale.md) | Troubleshooting, note dal campo, errori da evitare |

---

## Quick Reference - Protocolli Principali

| Protocollo | Address | Command | Carrier | Usato da |
|-----------|---------|---------|---------|----------|
| NEC | 8/16 bit | 8 bit | 38 kHz | LG, Samsung vecchi, cinesi |
| RC5 | 5 bit | 6 bit | 36 kHz | Philips, europei |
| RC6 | 8 bit | 8 bit | 36 kHz | Philips, Microsoft MCE |
| Sony SIRC | 5 bit | 7 bit | 40 kHz | Sony TV, Blu-ray, PS |
| Samsung | 8 bit | 8 bit | 38 kHz | Samsung TV |
| Raw | N/A | N/A | Variabile | AC, proiettori, custom |

> **Nota personale:** L'IR è spesso sottovalutato come vettore di attacco. In realtà il controllo non autorizzato di TV, AC e proiettori in ambienti corporate può causare disruption significativa. Il database universale del Flipper permette di controllare la maggior parte dei dispositivi senza neanche catturare il segnale.

---

## Risorse e File di Esempio

| Risorsa | Link | Descrizione |
|---------|------|-------------|
| **Flipper IRDB** | [github.com/Lucaslhm/Flipper-IRDB](https://github.com/Lucaslhm/Flipper-IRDB) | Database IR universale: migliaia di telecomandi per TV, AC, proiettori, ventilatori, LED |
| **File di esempio** | [examples/](../../examples/) | File `.ir` di esempio (NEC per TV, Raw per AC) con struttura commentata |
