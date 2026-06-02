# Esempi - File di Riferimento per Ogni Modulo

Questa cartella contiene file di esempio per ogni modulo del Flipper Zero. Sono utili per:

- Capire la struttura dei file salvati dal Flipper
- Testare import/export senza un dispositivo fisico
- Usarli come template per creare file personalizzati
- Verificare che il firmware legga correttamente i formati

> **Nota:** Questi sono file di esempio/didattici. Non contengono dati reali di dispositivi altrui.

---

## Contenuti

| File | Modulo | Descrizione |
|------|--------|-------------|
| [esempio_subghz.sub](esempio_subghz.sub) | Sub-GHz | Segnale 433.92 MHz OOK (Princeton, codice fisso) |
| [esempio_subghz_raw.sub](esempio_subghz_raw.sub) | Sub-GHz | Cattura RAW di un segnale 433 MHz |
| [esempio_nfc_mifare.nfc](esempio_nfc_mifare.nfc) | NFC | Dump MIFARE Classic 1K (chiavi di default) |
| [esempio_nfc_ntag.nfc](esempio_nfc_ntag.nfc) | NFC | Tag NTAG215 con URL |
| [esempio_rfid.rfid](esempio_rfid.rfid) | RFID | Tag EM4100 125 kHz |
| [esempio_ibutton.ibtn](esempio_ibutton.ibtn) | iButton | Chiave DS1990A |
| [esempio_ir_tv.ir](esempio_ir_tv.ir) | Infrared | Telecomando TV (NEC protocol) |
| [esempio_ir_ac.ir](esempio_ir_ac.ir) | Infrared | Telecomando condizionatore (raw) |
| [esempio_badusb.txt](esempio_badusb.txt) | BadUSB | Script DuckyScript base |

---

## Dove Copiare i File sul Flipper

```
esempio_subghz.sub      → /ext/subghz/
esempio_subghz_raw.sub  → /ext/subghz/
esempio_nfc_*.nfc       → /ext/nfc/
esempio_rfid.rfid       → /ext/lfrfid/
esempio_ibutton.ibtn    → /ext/ibutton/
esempio_ir_*.ir         → /ext/infrared/
esempio_badusb.txt      → /ext/badusb/
```

## Risorse Esterne - Database Ufficiali

| Risorsa | Link | Contenuto |
|---------|------|-----------|
| **Flipper IRDB** | [github.com/Lucaslhm/Flipper-IRDB](https://github.com/Lucaslhm/Flipper-IRDB) | Database IR universale: migliaia di telecomandi TV, AC, proiettori, ventilatori |
| **UberGuidoZ IRDB** | [github.com/UberGuidoZ/Flipper-IRDB](https://github.com/UberGuidoZ/Flipper-IRDB) | Fork con contributi aggiuntivi |
| **Flipper Sub-GHz DB** | [github.com/UberGuidoZ/Flipper](https://github.com/UberGuidoZ/Flipper) | Database Sub-GHz, BadUSB, NFC e altro |
| **Bad USB Payloads** | [github.com/UberGuidoZ/Flipper/tree/main/BadUSB](https://github.com/UberGuidoZ/Flipper/tree/main/BadUSB) | Raccolta payload DuckyScript |
