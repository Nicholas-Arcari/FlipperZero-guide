# Flipper Zero – Modulo RFID (125 kHz)

Il modulo RFID 125 kHz del Flipper Zero consente di leggere, emulare, analizzare, clonare e generare tag RFID a bassa frequenza, come EM4100, HID, FDX-B e T5577.

È utilizzato in sistemi di accesso, identificazione animale, controllo presenze e automazione.

Questo README descrive:

- Cos’è il modulo RFID
- Le cartelle e i tool inclusi
- Funzione di ogni componente
- Esempi pratici su come, quando e dove usarlo

---

## Cos’è il modulo RFID 125 kHz

Il Flipper Zero integra un’antenna e un lettore/scrittore per tag a bassa frequenza:

- Lettura di tag EM4100, HID Prox, FDX-B e simili
- Emulazione diretta per aprire porte o attivare sistemi
- Scrittura su tag programmabili (T5577)
- Analisi e fuzzing dei protocolli LF

È ideale per reverse engineering, test di sicurezza e compatibilità.

---

### RFID 125 kHz (cartella principale)

Lettura, salvataggio, emulazione, scrittura e gestione tag LF.

- Funzione: gestione principale dei badge 125 kHz.

- Quando usarlo: porte d’accesso, sistemi di registrazione, cancelli.

### DCF77 Clock Sync

Sincronizzazione oraria tramite protocollo DCF77 (radio-orologio europeo).

- Funzione: decodifica segnale orario standard.

- Uso: ricerca, test, studio protocolli temporali.

### DCF77 Transmitter

Generatore di segnale DCF77 artificiale.

- Funzione: emula un segnale orario radio.

- Uso: test orologi radiocontrollati.

### EM4100 Key Generator

Generatore di tag EM4100.

- Funzione: crea codici EM4100 validi per test.

- Uso: ricerca e compatibilità.

### FDX-B Maker

Creazione di tag per sistemi animali ISO 11784/11785.

- Funzione: genera ID compatibili con microchip animali.

- Uso: ricerca, studio standard FDX-B.

### NFC/RFID Detector

Rilevatore di campi NFC e RFID.

- Funzione: mostra se un lettore è attivo.

- Uso: test di ambienti e sicurezza fisica.

### RFID Fuzzer

Strumento per fuzzing protocolli LF.

- Funzione: invio frame non standard.

- Uso: test robustezza sistemi RFID.

### T5577 MultiWriter

Scrittura semplificata per tag T5577.

- Funzione: copia automatica da un tag letto.

- Uso: duplicazione veloce.

### T5577 Raw Writer

Scrittura avanzata con comandi raw.

- Funzione: scrittura settori specifici del T5577.

- Uso: ricerca e configurazioni particolari.

---

## Esempi pratici di utilizzo

### 1. Clonare un badge 125 kHz su un T5577

1. Vai su RFID 125 kHz → Read
2. Avvicina il badge originale → salva il file
3. Inserisci un tag T5577
4. Apri T5577 MultiWriter → “Write from saved file”
5. Testa l’emulazione o il tag fisico

Quando usarlo: badge d’accesso danneggiati o test ricerca.

### 2. Generare un tag EM4100 personalizzato

1. Apri EM4100 Key Generator
2. Inserisci un ID o generane uno casuale
3. Scrivi su T5577 → testalo nel lettore

Dove usarlo: laboratori, test compatibilità.

### 3. Analizzare un sistema sospetto con NFC/RFID Detector

1. Avvia NFC/RFID Detector
2. Passa vicino a porte, scrivanie, terminali
3. Se rileva campo attivo, significa che è presente un lettore

Utilità: mappatura sicurezza fisica.

### 4. Trasmettere un segnale DCF77 artificiale

1. Apri DCF77 Transmitter
2. Scegli ora corrente o personalizzata
3. Attiva la trasmissione vicino a un orologio radiocontrollato

Uso: test protocolli orari.

### 5. Fuzzing di un lettore RFID

1. Apri RFID Fuzzer
2. Seleziona tipo di frame
3. Invia → osserva comportamento del lettore

Obiettivo: scoprire errori di implementazione.

---

## Dove si usa l’RFID 125 kHz

- Sistemi d’accesso industriali
- Condomini, uffici, hotel
- Control board e macchinette
- Sistemi legacy a bassa frequenza
- Ricerca e pentesting hardware