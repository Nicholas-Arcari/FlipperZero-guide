## Attacchi e Contromisure

### Replay / Clonazione

**L'attacco:**
1. L'attaccante legge il badge della vittima (3-8 cm di distanza, meno di 1 secondo)
2. Clona l'ID su un T5577 (5 secondi)
3. Usa il clone per accedere

**Fattibilità:** Banale. Nessuna competenza tecnica richiesta. Il Flipper Zero rende il processo alla portata di chiunque.

**Scenari di acquisizione:**
- In fila alla macchinetta del caffè (il badge è appeso al collo)
- Al ristorante (il badge è nella borsa/giacca sulla sedia accanto)
- In ascensore (spazi ristretti, vicinanza forzata)
- Badge lasciato sulla scrivania
- Badge nella tasca posteriore dei pantaloni (facile da avvicinare)

**Contromisure:**
- **Migrazione a NFC con crittografia** (MIFARE DESFire EV2/EV3, HID SEOS)
- **Multi-fattore:** badge + PIN, badge + biometrico
- **Custodie schermanti** (Faraday sleeve) - efficacia limitata, scomoda
- **Policy:** badge sempre nascosto, mai lasciato incustodito
- **Monitoraggio:** log degli accessi con alert su anomalie (stesso badge in due luoghi diversi)

### Brute Force

**L'attacco:**
1. L'attaccante conosce il tipo di badge (es. HID 26-bit) e il Facility Code
2. Usa il RFID Fuzzer per provare Card Number sequenziali
3. Con 65536 possibilità a 3-5 ID/secondo: ~4-6 ore per lo spazio completo
4. In pratica molto meno, perchè i CN sono spesso in range limitati

**Fattibilità:** Media. Richiede ore di accesso fisico al lettore (poco discreto) ma tecnicamente semplice.

**Contromisure:**
- **Rate limiting:** il lettore blocca dopo N tentativi falliti in T secondi
- **Allarme:** notifica al centro di sicurezza dopo tentativi anomali
- **Logging:** registrazione di ogni tentativo (anche fallito) con timestamp
- **Anti-tamper:** rilevamento di manomissione fisica del lettore
- **Card Number non sequenziali:** usare numeri casuali rende il brute force meno efficiente

### Jamming

**L'attacco:**
1. L'attaccante genera un forte segnale a 125 kHz che "copre" il segnale del badge legittimo
2. Il lettore non riesce a leggere nessun badge
3. Usato come DoS (Denial of Service) o per forzare l'apertura manuale della porta

**Fattibilità:** Il Flipper Zero NON è uno jammer efficace (potenza troppo bassa). Serve hardware dedicato. Ma il concetto è importante da conoscere.

**Contromisure:**
- **Rilevamento RF:** sensori che rilevano campi anomali a 125 kHz
- **Failsafe policy:** se il lettore non funziona, la porta rimane chiusa (fail-closed) - MAI fail-open
- **Backup:** sistema di accesso secondario (PIN pad, chiave meccanica)
- **Monitoraggio:** alert quando un lettore non legge badge per un periodo anomalo

### Skimming a Distanza

**L'attacco:**
1. L'attaccante costruisce un lettore RFID con antenna amplificata
2. Lo nasconde in un punto dove i badge passano vicino (sotto un tappetino, dentro un tavolino)
3. Il lettore cattura gli ID dei badge senza che i proprietari se ne accorgano
4. Gli ID vengono salvati e clonati successivamente

**Fattibilità:** Media-alta per un attaccante motivato. Richiede hardware custom ma i componenti sono economici e le guide sono disponibili online. Con un'antenna ben progettata, la distanza di lettura può arrivare a 30-50 cm (molto più del Flipper).

**Contromisure:**
- **Custodie schermanti** per i badge
- **Crittografia** (rende l'ID catturato inutile senza la chiave)
- **Ispezione fisica** regolare delle aree sensibili
- **Policy:** badge in custodia schermata quando non in uso

### Manipolazione del Database

**L'attacco:**
1. L'attaccante compromette il sistema di gestione degli accessi (spesso un PC Windows con software proprietario)
2. Aggiunge il proprio ID al database degli autorizzati
3. Oppure disabilita il controllo e mette il sistema in "pass-through"

**Fattibilità:** Richiede accesso alla rete o al PC del controller. È un attacco cyber, non fisico, ma spesso più devastante della clonazione.

**Contromisure:**
- **Segregazione della rete** del sistema di accesso (VLAN dedicata)
- **Hardening** del server/PC del controller
- **Audit log** con integridad protetta
- **Monitoraggio** delle modifiche al database

---
