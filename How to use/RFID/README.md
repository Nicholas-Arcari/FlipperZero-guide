# RFID 125 kHz - Overview

Modulo di lettura, scrittura ed emulazione di tag RFID a **125 kHz** (Low Frequency). Copre i protocolli EM4100, HID Prox, Indala, FDX-B e supporta la scrittura su tag programmabili T5577.

**Frequenza:** 125 kHz (+ 134.2 kHz per FDX-B) | **Portata:** 3-8 cm | **Scrittura:** T5577 | **Protocolli:** 20+

---

## Contenuti

| # | File | Descrizione |
|---|------|-------------|
| 01 | [Fondamenti Tecnici](01-Fondamenti-Tecnici.md) | RFID LF, accoppiamento induttivo, modulazione ASK/FSK/PSK, struttura dei frame |
| 02 | [Hardware e Limiti](02-Hardware-e-Limiti.md) | Antenna LF del Flipper, portata reale, limiti di emulazione/scrittura |
| 03 | [Protocolli](03-Protocolli.md) | EM4100 (frame 64-bit completo), HID Prox H10301 (26-bit), Indala, FDX-B (ISO 11784/11785), T5577 (Block 0 config word, emulazione multi-protocollo) |
| 04 | [Guida Operativa](04-Guida-Operativa.md) | Tool-by-tool: Read, Write, Emulate, Add Manually, EM4100 Key Generator, FDX-B Maker, RFID Fuzzer, T5577 MultiWriter, T5577 Raw Writer, DCF77, NFC/RFID Detector |
| 05 | [Scenari Reali](05-Scenari-Reali.md) | 7 scenari dettagliati: condominio EM4100, badge HID aziendale, fuzzing lettore, rilevamento lettori nascosti, parcheggio multipiano, palestra/anti-passback, red team building |
| 06 | [Attacchi e Difese](06-Attacchi-e-Difese.md) | Replay/clonazione, bruteforce, jamming, skimming a distanza, manipolazione database |
| 07 | [Aspetti Legali](07-Aspetti-Legali.md) | Art. 615-ter/quater, 640-ter c.p., GDPR, procedure operative legali |
| 08 | [Esperienza Personale](08-Esperienza-Personale.md) | Troubleshooting completo, limiti del Flipper, kit operativo, errori da evitare, futuro del 125 kHz, riferimenti |

---

## Quick Reference - Protocolli Principali

| Protocollo | Bit | Modulazione | Sicurezza | Diffusione Italia |
|-----------|-----|------------|-----------|-------------------|
| EM4100 | 64 (40 dati) | ASK/Manchester | Zero | Condomini, palestre, parcheggi |
| HID H10301 | 26 | FSK2 | Zero | Uffici, banche, ospedali |
| Indala | 26/29 | PSK1 | Zero | Raro (edifici NATO, USA) |
| FDX-B | 128 | ASK/NRZ | Read-only | Microchip animali (obbligatorio) |
| T5577 | Programmabile | Qualsiasi | Password opzionale | Target di scrittura universale |

## Quick Reference - Workflow Operativo

```
RFID → Read → Identifica protocollo
  ├─ EM4100 → Clone su T5577 (5 secondi) → Test al lettore
  ├─ HID H10301 → Annota FC:CN → Clone su T5577 → Fuzzing su CN
  ├─ Indala → Clone su T5577 (meno affidabile) → Verifica
  ├─ FDX-B → Solo lettura/emulazione (no write reale)
  └─ Unknown → Proxmark3 per analisi raw
```

> **Nota personale:** Il 90% dei condomini italiani usa EM4100 senza crittografia. La clonazione richiede meno di 10 secondi. Un Flipper e 10 T5577 in tasca sono tutto cio' che serve per dimostrare che il sistema di accesso è un'illusione di sicurezza.
