# Flipper Zero – Modulo Infrared

Il modulo Infrared del Flipper Zero permette di inviare, ricevere, registrare e riprodurre segnali a infrarossi (IR), gli stessi utilizzati da telecomandi TV, condizionatori, proiettori, fotocamere e molti altri dispositivi consumer.

Questo README descrive:

- Che cos’è il modulo IR
- Le cartelle principali e la funzione di ogni componente
- Descrizione specifica di ogni tool
- Esempi pratici su come, quando e dove usarlo

---

## Cos’è il modulo Infrarossi

Il Flipper Zero possiede un LED IR ad alta potenza in grado di:

- Trasmettere segnali IR (come un telecomando)
- Registrare segnali IR da altri dispositivi
- Decodificare protocolli standard (NEC, Sony, Samsung, ecc.)
- Riprodurre comandi personalizzati

Il modulo IR è utile per test, reverse engineering, automazione, prototipazione e studio dei protocolli IR.

---

### Infrared

Sezione principale per registrare, decodificare e inviare segnali IR.

- Funzione: telecomando generico, registratore e libreria IR del Flipper.

- Quando usarlo: per controllare TV, proiettori, apparecchi IR comuni.

### Cross Remote

Telecomando universale multi-vendor.

- Funzione: permette di controllare vari dispositivi senza file IR personalizzati.

- Uso tipico: hotel, uffici, dispositivi non propri.

Esempio pratico:

- Apri Cross Remote
- Seleziona il profilo (es. TV → Samsung)
- Premi Power → Verifica il controllo del dispositivo

### Fire String

Generatore di stringhe IR specifiche.

- Funzione: invio rapido di comandi IR predefiniti.

- Uso: test e analisi ripetitiva.

Esempio pratico:

- Seleziona una stringa preimpostata (es. NEC test)
- Punta il Flipper verso un ricevitore IR
- Invia ripetutamente per verificare sensibilità e risposta

### Flame RNG

Random Number Generator via IR.

- Funzione: trasmissione casuale di segnali IR.

- Uso: stress test dei ricevitori IR.

Esempio pratico:

- Avvia Flame RNG
- Il Flipper invierà pacchetti IR casuali
- Osserva quanto velocemente un ricevitore IR va in overload

### Flipper Tag

Sistema di tagging IR.

- Funzione: invia identificatori IR univoci.

- Uso: demo e interazioni tra più Flipper.

Esempio pratico:

- Imposta un ID (es. Tag 42)
- Invia il Tag verso un altro Flipper
- Il secondo Flipper mostrerà la ricezione e l’ID identificato

### Hard Hat Brigade IR

Mini‑gioco o demo basata su comunicazione IR.

- Funzione: scambio comandi IR per game/demos.

Esempio pratico:

- Avvia il gioco su due Flipper
- Posizionali frontali
- Ogni IR trigger invia "colpi" al device opposto

### Hitachi AC Remote

Telecomando IR per climatizzatori Hitachi.

- Funzione: controllo AC.

- Uso: test, sostituzione telecomando originale.

Esempio pratico:

- Seleziona Hitachi AC Remote
- Imposta temperatura e modalità
- Invia il comando verso l’unità AC

### IR Blaster

Trasmettitore IR avanzato.

- Funzione: invio continuo o massiccio di segnali IR.

- Uso: test intensivi su ricevitori.

Esempio pratico:

- Avvia IR Blaster in modalità burst
- Punta verso un sensore IR
- Verifica saturazione o comportamento in overload

### IR Decoder

Strumento per analizzare e decodificare segnali IR.

- Funzione: mostra protocollo, lunghezza, dati.

- Uso: reverse engineering, creazione di file personalizzati.

Esempio pratico:

- Premi Start decoding
- Punta un telecomando verso il Flipper
- Leggi il protocollo (NEC/Sony ecc.) e copia i dati RAW

### IR Intervalometer

Controllo remoto per fotocamere DSLR compatibili.

- Funzione: scatto intervallato tramite IR.

- Uso: time-lapse fotografici.

Esempio pratico:

- Imposta intervallo (es. 5 sec)
- Punta verso la DSLR
- Avvia e lascia che il Flipper scatti automaticamente

### IR Remote

Telecomando universale con UI semplice.

- Funzione: permette di caricare file `.ir` e inviarli.

Esempio pratico:

- Carica un file IR (es. `sony_power.ir`)
- Premi Send
- La TV risponderà come col telecomando originale

### IR Scope

Oscilloscopio IR.

- Funzione: visualizza forme d’onda IR.

- Uso: analisi tecnica del segnale.

Esempio pratico:

- Avvia IR Scope
- Punta un telecomando verso il Flipper
- Analizza waveform, duty-cycle e lunghezza burst

### IR Transfer

Sistema di invio e ricezione file via IR.

- Funzione: trasferisci dati tra Flipper.

Esempio pratico:

- Posiziona due Flipper uno di fronte all’altro
- Seleziona Send File
- Il secondo Flipper riceverà automaticamente

### LIDAR Emulator

Emulatore IR per dispositivi che leggono distanze.

- Funzione: invia pattern IR simili a sensori di prossimità.

Esempio pratico:

- Seleziona modalità LIDAR preset
- Invialo verso un robot con sensore IR
- Analizza come reagisce il robot

### Midea / Mitsubishi AC Remote

Telecomandi specifici per AC Midea e Mitsubishi.

- Funzione: controllo climatizzatori.

Esempio pratico:

- Regola temperatura e modalità
- Invia IR verso unità AC
- Verifica la risposta

### Netflix TV Remote

Telecomando IR per alcune smart TV usate da Netflix.

- Funzione: navigazione multimediale.

Esempio pratico:

- Premi Play, Pause, Back
- Controlla rapidamente app Netflix via IR

### R.O.B. Control

Controllo IR per il robot R.O.B. del Nintendo NES.

- Funzione: invia comandi al robot vintage.

Esempio pratico:

- Avvia R.O.B. Control
- Seleziona comando (es. "Raise Arms")
- Il robot eseguirà il movimento

### Xbox Control

Controllo IR per dispositivi Xbox compatibili.

Esempio pratico:

- Invia comando Guide o Power
- La console risponde come col telecomando IR originale

### XRemote

Telecomando avanzato multi-dispositivo.

- Funzione: telecomando universale potenziato.

Esempio pratico di utilizzo:

Obiettivo: controllare una TV usando il modulo IR del Flipper Zero.

1. Registrazione del segnale (opzionale)

1. Vai su Infrared → Learn New Remote
2. Punta il telecomando verso il Flipper
3. Premi un tasto e salva il file generato

2. Invio diretto di un segnale

1. Vai su Infrared → Saved Remotes
2. Seleziona il file salvato (es. `tv_power.ir`)
3. Premi Send

La TV dovrebbe rispondere come se avessi premuto il pulsante originale.

Quando usarlo:

- Test funzionalità IR
- Sostituire temporaneamente un telecomando rotto
- Automazione o prototipazione IR
- Studio di protocolli

Dove usarlo:

- Casa (TV, condizionatori, soundbar)
- Laboratori
- Uffici
- Ambienti dove sono presenti dispositivi IR