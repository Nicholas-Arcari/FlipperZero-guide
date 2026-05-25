# Hardware e Limiti Reali

## Il Chip ST25R3916

Il Flipper Zero usa il **ST25R3916** di STMicroelectronics:

- **Standard supportati:** ISO 14443A/B, ISO 15693, FeliCa, NFC-V
- **Frequenza:** 13.56 MHz
- **Potenza campo:** regolabile, sufficiente per tag standard
- **Distanza di lettura:** 2-5 cm (tag standard), fino a 8-10 cm in condizioni ideali
- **Data rate:** fino a 6.78 Mbit/s (NFC-A/B high speed)
- **Funzionalità:** reader, emulatore, sniffing (limitato)

---

## Limiti Reali che Devi Conoscere

**Distanza di lettura:** Il Flipper legge tag a massimo 3-5 cm nella pratica. Questo è un limite critico durante il pentest - devi avvicinarti molto al badge target. La "bobina" NFC è nella parte superiore del Flipper (sopra lo schermo).

**Emulazione imperfetta:** L'emulazione NFC del Flipper non è al livello di un Proxmark3 o ChameleonMini. Alcuni lettori rifiutano l'emulazione per differenze di timing o di livello del campo. Certi sistemi di accesso hanno filtri anti-emulazione.

**Nessun supporto EMV completo:** Il Flipper può leggere dati base di carte bancarie NFC (PAN, expiry) ma non può clonare o emulare carte di pagamento - i sistemi EMV usano crittografia asimmetrica e challenge-response che il Flipper non può replicare.

**MIFARE Classic solo:** L'attacco crypto1 funziona solo su MIFARE Classic. Tag MIFARE Plus (SL3), DESFire, SEOS, iClass SE non sono vulnerabili allo stesso attacco.

**Sniffing limitato:** Il Flipper può fare sniffing NFC ma la qualità è inferiore a un Proxmark3. Per catture affidabili di comunicazioni reader-tag, il Proxmark rimane lo standard.

> **Nota personale:** La distanza di lettura è il problema più grande nel pentest NFC. Per leggere un badge, devi avvicinarti a meno di 5 cm dalla persona che lo porta - servono tecniche di social engineering o situazioni dove il badge è appoggiato (es. sulla scrivania). Ho avuto successo leggendo badge lasciati sul tavolo in mensa durante la pausa pranzo. Mai sottovalutare la distanza fisica necessaria.

---

## Confronto con Altri Strumenti

| Caratteristica | Flipper Zero | Proxmark3 RDV4 | ChameleonMini | ACR122U |
|---|---|---|---|---|
| **Portabilità** | Eccellente | Buona | Buona | Desktop |
| **Distanza lettura** | 3-5 cm | 5-8 cm | 3-5 cm | 5-8 cm |
| **Emulazione** | Discreta | Eccellente | Eccellente | No |
| **Sniffing** | Limitato | Eccellente | Buono | No |
| **Facilità d'uso** | Alta | Bassa | Media | Media |
| **Costo** | ~170 EUR | ~300 EUR | ~50 EUR | ~30 EUR |
| **Discrezione** | Alta | Media | Alta | Nulla |

> **Nota personale:** Il Flipper è imbattibile per la discrezione - sembra un giocattolo e nessuno sospetta. Il Proxmark è superiore tecnicamente ma attira attenzione. Per il pentest sul campo, uso il Flipper per la fase di raccolta e il Proxmark in laboratorio per l'analisi approfondita.
