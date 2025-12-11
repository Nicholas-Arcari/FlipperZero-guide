# Flipper Zero – Modulo NFC

Il modulo NFC del Flipper Zero permette la lettura, emulazione, clonazione, fuzzing e analisi di una vasta gamma di tag NFC/RFID a 13.56 MHz.

È uno dei moduli più potenti del dispositivo grazie al supporto a protocolli MIFARE, NTAG, DESFire, iClass/PicoPass, T-Union e molti altri.

Questo README descrive:

- Che cos’è il modulo NFC
- Struttura delle cartelle e panoramica dei tool
- Funzione specifica di ciascun componente
- Esempi pratici su come, quando e dove usarlo

---

## Cos’è il modulo NFC

Il Flipper Zero usa un transceiver ad alta frequenza (13.56 MHz) compatibile con:

- ISO14443 A/B
- MIFARE Classic / DESFire / Plus
- NTAG / NDEF
- iClass / PicoPass
- T-Union / transport cards

Il modulo NFC permette:

- Scansione e analisi tag
- Emulazione software di card
- Fuzzing protocolli
- Sniffing di comunicazioni reader ↔ tag
- Scrittura e modifica contenuti
- Attacchi a MIFARE Classic (mfkey…)

---

### Amusement IC

Gestione di card NFC usate in parchi divertimento o sale giochi.

- Funzione: lettura, analisi e talvolta emulazione.

Esempio pratico:

- Avvicina la card alla bobina NFC
- Leggi il saldo o ID
- Salvalo per utilizzi di test


### Cyborg Detector

Rilevatore di impianti NFC sottocutanei.

- Funzione: verifica presenza di chip implantati.

Esempio pratico:

- Attiva detector
- Avvicina la zona della mano/avambraccio
- Il Flipper avvisa se rileva campo NFC attivo


### MetroFlip

Tool per card dei trasporti (metropolitane) compatibili.

- Funzione: leggere dati, storici, settore viaggio.

Esempio pratico:

- Passa la card metro sul Flipper
- Controlla ID, UID, contatori


### MFDesfire Auth

Autenticatore per MIFARE DESFire.

- Funzione: test autenticazioni AES/3DES.

Esempio pratico:

- Carica keyset
- Avvia autenticazione per verificare accessi


### MFKey

Suite per ottenere chiavi MIFARE Classic.

- Funzione: attacco alle chiavi tramite analisi sniffata.

Esempio pratico:

- Sniffa lettore <-> card
- Applica mfkey
- Recupera chiavi A/B


### Mi Band NFC

Supporto a funzioni NFC dei braccialetti Xiaomi.

Esempio pratico:

- Poggia Mi Band sul Flipper
- Leggi ID e servizi supportati


### MIFARE Classic Editor

Editor settori MIFARE Classic.

- Funzione: lettura/scrittura blocchi.

Esempio pratico:

- Recupera chiavi A/B
- Modifica un blocco dati (es. nome file o contatore)


### MIFARE Fuzzer

Fuzzer per protocolli MIFARE.

- Funzione: invio comandi non standard.

Esempio pratico:

- Seleziona modalità fuzz
- Invia handshake anomali al lettore


### MiZip Balance Editor

Editor di carte MiZip compatibili.

- Funzione: lettura bilanci.

Esempio pratico:

- Scansiona card MiZip
- Osserva valore e dati


### NFC (principale)

Hub centrale del modulo NFC.

- Funzione: lettura, emulazione, salvataggio tag.

Esempio pratico:

- Seleziona "Read"
- Avvicina un tag
- Salva file `.nfc` generato


### NFC APDU Runner

Invio manuale di comandi APDU.

- Funzione: debug ISO7816.

Esempio pratico:

- Inserisci comando APDU
- Invia e analizza risposta


### NFC Comparator

Confronto tra due file NFC.

- Funzione: verifica differenze di dati.

Esempio pratico:

- Carica due dump
- Identifica settori modificati


### NFC Dict Manager

Gestione dizionari chiavi MIFARE.

Esempio pratico:

- Aggiungi chiavi personalizzate
- Riprova autenticazione


### NFC E‑Ink Tags

Gestione tag NFC con display e‑ink.

Esempio pratico:

- Scrivi un testo personalizzato su un tag e‑ink


### NFC Keyboard

Simula una tastiera via NFC.

Esempio pratico:

- Programma tag con input (es. password demo)
- Toccando un reader NFC, invia input


### NFC Magic

Supporto a tag “Magic” (cambiabile UID).

Esempio pratico:

- Carica dump originale
- Scrivilo su una Magic Card
- Imposta UID identico all’originale


### NFC Maker

Generatore rapido di tag NFC.

Esempio pratico:

- Crea NDEF (URL, testo, comando)
- Scrivi su un tag


### NFC Playlist

Tool per generare playlist multimediali su tag.

Esempio pratico:

- Imposta link Spotify o YouTube
- Scrivi tag NFC da usare come "shortcut"


### NFC Relay

Relay/NFC MitM.

- Funzione: inoltra lettore <-> tag.

Esempio pratico:

- Attiva relay su due Flipper
- Posiziona uno sul lettore, uno sulla card


### NFC Sniffer

Sniffing NFC.

- Funzione: intercetta comunicazioni ISO14443.

Esempio pratico:

- Metti Flipper tra lettore e card
- Salva pacchetti raw


### NFC URL

Generatore rapido tag NDEF URL.

Esempio pratico:

- Inserisci un link
- Scrivi un tag da usare come shortcut


### NFC/RFID Detector

Rilevatore generico segnali NFC/RFID.

Esempio pratico:

- Avvicina il Flipper a dispositivi
- Verifica presenza campo RF


### Open Print Tag

Compatibile con sistemi di stampa.

Esempio pratico:

- Leggi tag stampante
- Analizza ID o contatori


### Passport Reader

Lettore NFC documenti elettronici (MRZ richiesta).

Esempio pratico:

- Inserisci MRZ del passaporto
- Tappa il passaporto sul Flipper
- Leggi dati base


### PicoPass / iClass

Gestione tag PicoPass/iClass.

Esempio pratico:

- Scansiona badge aziendale compatibile
- Salva UID


### SEADER

Analizzatore protocolli Secure Element.

Esempio pratico:

- Invia APDU
- Controlla risposte crittografiche


### SEOS Compatible

Gestione tag SEOS compatibili.

Esempio pratico:

- Scansiona badge SEOS
- Verifica compatibilità


### SLI Writer

Scrittura/tag SLI.

Esempio pratico:

- Carica file SLI
- Scrivi su tag compatibile


### T‑Union Master (China)

Supporto a card del trasporto T‑Union.

Esempio pratico:

- Leggi dati trasporto
- Verifica ID e contatori


### TuLlave

Card dei trasporti (Sud America).

Esempio pratico:

- Scansiona card
- Salva dump per analisi


### UdECard

Supporto a carte UdE.

Esempio pratico:

- Usa NFC → Read
- Identifica settori utili


### UID Brute Smarter

Bruteforce UID ottimizzato.

Esempio pratico:

- Avvia brute UID
- Usa per test su lettori compatibili


### VB Migration Assistant

Tool per migrazione da/verso sistemi VB.

Esempio pratico:

- Converte formati tag legacy


### Weebo

Tool NFC avanzati per app Weebo.

Esempio pratico:

- Leggi tag Weebo
- Analizza formati

 Esempio pratico generale – Clonazione di un tag NFC semplice (NTAG)

1. Vai in NFC → Read
2. Avvicina il tag
3. Salva il dump generato
4. Inserisci una Magic Tag compatibile
5. Apri NFC Magic → Write
6. Scrivi il dump
7. Testa su un lettore