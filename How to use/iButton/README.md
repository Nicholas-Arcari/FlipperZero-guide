# iButton - Overview

Modulo per lettura, scrittura, emulazione e analisi di chiavi **iButton** (1-Wire contact keys). Supporta i protocolli Dallas/Maxim DS1990A, Cyfral e Metakom, con capacità di scrittura su chiavi riscrivibili RW1990.

**Interfaccia:** 1-Wire (contatto) | **Protocolli:** DS1990A, Cyfral, Metakom | **Scrittura:** RW1990 | **ID:** 64 bit (8 byte)

---

## Contenuti

| # | File | Descrizione |
|---|------|-------------|
| 01 | [Fondamenti Tecnici](01-Fondamenti-Tecnici.md) | Protocollo 1-Wire, elettrica del bus, timing, ROM commands, topologia |
| 02 | [Hardware e Limiti](02-Hardware-e-Limiti.md) | Interfaccia iButton del Flipper, contatto GPIO, portata, limiti fisici |
| 03 | [Protocolli](03-Protocolli.md) | DS1990A (64-bit ROM, family code), Cyfral (impulsi), Metakom, RW1990 programmabile |
| 04 | [Guida Operativa](04-Guida-Operativa.md) | Tool-by-tool: Read, Write, Emulate, Add Manually, Converter, Fuzzer |
| 05 | [Scenari Reali](05-Scenari-Reali.md) | Scenari pentest: condominio DS1990A, palazzo Cyfral/Metakom, building assessment, citofono industriale, casi città italiane |
| 06 | [Attacchi e Difese](06-Attacchi-e-Difese.md) | Clonazione, bruteforce, fuzzing, bypass - attacchi e contromisure |
| 07 | [Aspetti Legali](07-Aspetti-Legali.md) | Normativa italiana/EU per iButton testing |
| 08 | [Esperienza Personale](08-Esperienza-Personale.md) | Troubleshooting, limiti Flipper, kit operativo, errori da evitare, riferimenti |

---

## Quick Reference - Protocolli

| Protocollo | ID | Diffusione Italia | Sicurezza | Clonabile |
|-----------|-----|-------------------|-----------|-----------|
| DS1990A | 64 bit (8 byte) | Molto alta (condomini) | Zero | Si' (RW1990) |
| Cyfral | Variabile | Media (vecchi citofoni) | Zero | Si' (emulazione) |
| Metakom | Variabile | Media (vecchi citofoni) | Zero | Si' (emulazione) |

## Quick Reference - Workflow

```
iButton → Read (contatto con chiave) → Identifica protocollo
  ├─ DS1990A → Clone su RW1990 (3 secondi) → Test al citofono
  ├─ Cyfral → Emulazione (non scrivibile) → Test al citofono
  ├─ Metakom → Emulazione (non scrivibile) → Test al citofono
  └─ Non riconosciuto → Verifica contatto, riprova con angolazione diversa
```

> **Nota personale:** iButton DS1990A è ancora onnipresente nei condomini italiani, specialmente a Roma, Milano, Torino e Bologna. La clonazione su RW1990 richiede 3 secondi e costa 0.50 EUR a chiave. Nessuna crittografia, nessuna protezione.
