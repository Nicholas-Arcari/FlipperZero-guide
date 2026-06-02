# Sicurezza - Exploitation, Forensics e Strumenti Offensivi

Questa sezione raccoglie gli strumenti GPIO orientati alla sicurezza: emulazione carte magnetiche, controllo casseforti, moduli di exploitation, suite forensic e strumenti di sorveglianza ottica. Utilizzabili in contesti di penetration testing e ricerca di vulnerabilità.

---

### • Sentry Safe

Interfaccia con casseforti Sentry tramite protocolli di controllo.

Funzionalità ampliate:

- Apertura e chiusura digitale tramite sequenze GPIO.
- Supporto a modelli con input analogico/digitale.
- Possibilità di registrare combinazioni per test o automazioni.
- Monitoraggio stato serratura e feedback LED interno.

Esempio pratico:

- Collegare pin GPIO alla scheda di controllo della cassaforte.
- Attivare sequenza di apertura → verificare LED di stato.
- Test combinazioni multiple per verifica correttezza.

### • Evil BW16 Controller

Strumento di controllo avanzato per moduli BW16 / Ameba RTL utilizzati in automazioni e exploitation.

Funzionalità ampliate:

- Comunicazione UART/SPI/I²C con BW16.
- Programmazione firmware.
- Lettura log di debug.
- Interazione diretta con GPIO del modulo.
- Script personalizzabili per automazioni rapide.
- Monitor seriale con parsing automatico.

Esempio pratico

Flash e monitoraggio realtime:

- Collegare UART e tenere premuto il tasto BOOT del modulo.
- Caricare firmware binario → scriverlo.
- Aprire monitor seriale → verificare sequenza di boot.
- Usare comandi script per pilotare GPIO.

### • MagSpoof

Emulazione banda magnetica per test di carte e sistemi POS.

Funzionalità ampliate:

- Emulazione bande ISO 7811.
- Registrazione e replay di tracce magnetiche.
- Test sicurezza sistemi di lettura.
- Supporto a più card type (credit, hotel, access).
- Visualizzazione dati raw.

Esempio pratico

Test lettore badge:

- Collega MagSpoof → seleziona traccia.
- Esegui swipe → verifica risposta lettore.
- Analizza dati raw per debugging.

### • Flipper BlackHat

Set di strumenti sperimentali e non documentati, orientati a testing, ricerca e sviluppo "deep-level".

Funzionalità ampliate:

- Accesso diretto ai registri interni.
- Funzioni diagnostiche avanzate.
- Possibili tool di exploit/sperimentazione (varia per release).
- Logging raw a basso livello.
- Modalità "unsafe" opzionale.

Esempio pratico

Debug low-level:

- Attivare modalità avanzata.
- Monitorare registri GPIO in tempo reale.
- Individuare comportamento anomalo di un pin.

### • LAB401 DigiLab

Suite digital forensics/hardware test (dipende dai moduli supportati).

Funzionalità ampliate:

- Visualizzazione segnali digitali.
- Strumenti di cattura rapida.
- Funzioni di replay input.
- Analisi pattern protocollo.
- Esportazione dati raw.

Esempio pratico

Verifica protocollo custom:

- Collegare linee dati.
- Registrare pattern ripetitivo.
- Confrontare con documentazione interna.

### • LAB401 Light Messenger

Sistema di comunicazione ottica tramite LED e fotodiodo.

Funzionalità ampliate:

- Trasmissione ottica testo/bit.
- Modalità beacon.
- Regolazione velocità di modulazione.
- Rilevamento livello luce in ingresso.
- Codifica/decodifica automatica.

Esempio pratico

Invio messaggio su fascio di luce:

- Puntare LED e fotodiodo allineati.
- Scrivere messaggio.
- Decodifica automatica lato ricezione.

### • Lasercat

Controllo laser + rilevamento movimento del fascio.

Funzionalità ampliate:

- Accensione laser controllata.
- Rilevamento interruzione raggio.
- Modalità gioco "cat laser chase".
- Allarmi ottici.
- Logging eventi.

Esempio pratico

Barriera laser:

- Attivare laser + sensore.
- Oggetto passa → interruzione → trigger evento.
