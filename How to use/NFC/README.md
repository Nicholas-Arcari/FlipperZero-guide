# NFC - Overview

Modulo di comunicazione contactless a **13.56 MHz** basato sul chip **ST25R3916** per la lettura, scrittura, emulazione e analisi di tag e card NFC. Copre ISO 14443A/B, MIFARE Classic/Ultralight/DESFire, iClass/PicoPass, e card bancarie EMV.

**Chip:** ST25R3916 | **Frequenza:** 13.56 MHz | **Portata:** 3-5 cm | **Standard:** ISO 14443A/B, ISO 15693

---

## Contenuti

| # | File | Descrizione |
|---|------|-------------|
| 01 | [Fondamenti Tecnici](01-Fondamenti-Tecnici.md) | NFC vs RFID, ISO 14443, campo RF, accoppiamento induttivo, anti-collisione |
| 02 | [Hardware e Limiti](02-Hardware-e-Limiti.md) | ST25R3916, limiti di portata, energia, posizionamento bobina |
| 03 | [Protocolli](03-Protocolli.md) | Tipi di tag (MIFARE Classic/UL/DESFire, iClass, NTAG), SAK/ATQA identification, struttura memoria, Crypto-1 |
| 04 | [Guida Operativa](04-Guida-Operativa.md) | Tool-by-tool: Read, Detect Reader, Emulate, MFKey32, Dictionary Attack, MIFARE Editor, Fuzzer, APDU Runner, Comparator, Magic, Sniffer, Relay, PicoPass |
| 05 | [Scenari Reali](05-Scenari-Reali.md) | 7 scenari dettagliati: badge aziendale, card hotel, relay attack, multi-piano privilege escalation, mensa/credito, trasporto pubblico, red team datacenter |
| 06 | [Attacchi e Difese](06-Attacchi-e-Difese.md) | Magic Card (Gen1-4), Crypto-1 recovery, dictionary attack, clone-and-replay, UID-only bypass, relay attack |
| 07 | [Aspetti Legali](07-Aspetti-Legali.md) | Art. 615-ter, 640-ter c.p., GDPR, gestione Magic Card e dump |
| 08 | [Esperienza Personale](08-Esperienza-Personale.md) | Troubleshooting completo, note dal campo, errori da evitare, best practice |

---

## Quick Reference - Identificazione Tag per SAK

| SAK | Tipo | Vulnerabilità | Approccio |
|-----|------|---------------|-----------|
| 0x08 | MIFARE Classic 1K | Crypto-1 | Dict → MFKey32 → Clone |
| 0x18 | MIFARE Classic 4K | Crypto-1 | Dict → MFKey32 → Clone |
| 0x04 | MIFARE Ultralight | Nessuna crypto | Read diretto |
| 0x44 | MIFARE Ultralight C | 3DES | Password attack |
| 0x20 | MIFARE DESFire | AES (forte) | Molto difficile |
| 0x20 | NTAG 21x | Password 32-bit | Bruteforce (lento) |
| N/A | iClass Legacy | DES debole | PicoPass tools |
| N/A | iClass SE | AES (forte) | Non praticabile |

## Quick Reference - Workflow Operativo

```
NFC → Read → Identifica SAK
  ├─ SAK 0x08/0x18 (MIFARE Classic) → Dictionary Attack
  │   ├─ Tutte le chiavi trovate → Dump completo → Clone su Magic Card
  │   └─ Chiavi mancanti → Detect Reader → MFKey32 → Ri-leggi → Clone
  ├─ SAK 0x04 (Ultralight) → Read diretto → Emulate/Clone
  ├─ SAK 0x20 (DESFire) → Documenta nel report come "sicuro"
  └─ Non riconosciuto → Read RAW → Analisi manuale
```

> **Nota personale:** Il 60% degli uffici italiani usa ancora MIFARE Classic 1K. La clonazione richiede meno di 30 secondi. Porta sempre almeno 10 Magic Card Gen4 - l'emulazione fallisce nel 40% dei casi in campo.
