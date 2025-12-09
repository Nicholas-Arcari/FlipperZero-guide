# Flipper Zero - WiFi Marauder

Toolkit informativo e di supporto per utilizzare un modulo WiFi compatibile con WiFi Marauder all’interno del Flipper Zero, per attività di ricerca sulla sicurezza wireless, diagnostica e analisi del comportamento delle reti WiFi

## Disclaimer Etico e Legale

Questo progetto è destinato solo a scopi educativi, di diagnostica o di test su reti di cui si possiede l’autorizzazione esplicita

L’utilizzo improprio di tecniche o strumenti che interferiscono con reti o dispositivi di terzi è illegale e può comportare sanzioni penali

Usa il contenuto di questa repository in modo responsabile

---

## Video di riferimento

Flipper Zero - Tutorial Italiano - 15 - WIFI MARAUDER ( https://www.youtube.com/watch?v=z3ft9ND-3iA )

Flipper Zero - Tutorial Italiano - 17 - WIFI MARAUDER ( https://www.youtube.com/watch?v=CP0cmj3byJE )

---

## Hardware Necessario

Per utilizzare WiFi Marauder con il Flipper Zero sono necessari:

- Flipper Zero aggiornato all’ultima versione firmware (ufficiale o custom compatibile)
- Flipper Zero WiFi Devboard (ESP32-S2) oppure altro modulo ESP32 supportato da Marauder
- Cavo USB-C per il flash del firmware sul modulo WiFi
- (Opzionale) Computer per il flashing e la configurazione iniziale

Flipper Zero da solo non ha WiFi integrato: il supporto è fornito al 100% dal modulo ESP32 + firmware Marauder

---

## Flashware Necessario

Per windows aprire il seguente link: https://github.com/UberGuidoZ/Flipper/tree/main/Wifi_DevBoard/FZ_Marauder_Flasher

Per Linux/MacOS aprire il seguente link: https://github.com/SkeletonMan03/FZEasyMarauderFlash

---

## Installazione del Firmware WiFi Marauder

1. Metodo Web (semplice) - FZEE Flasher o tool equivalenti

- Collegare l’ESP32 al PC via USB.
- Mettere la scheda in modalità boot + reset
- Da browser scegliere la board ESP32 e selezionare il firmware Marauder
- Premere Program
- Al termine, reset del modulo → pronto all’uso

2. Metodo alternativo - ESP Web Flasher

- Scaricare il file binario corretto per la propria board
- Caricare tramite interfaccia web:
    - bootloader
    - partizioni
    - boot_app
    - bin principale Marauder
- Flashare gli slot indicati
- Reset finale

3. Metodo avanzato via script / esptool

Per utenti esperti:

- flash tramite Terminale
- comandi di esptool.py
- porta seriale UART

Alcuni OS (Windows) richiedono driver USB-UART, mentre su Linux/macOS possono servire permessi seriali

Nota: Segui sempre la documentazione ufficiale del progetto Marauder per la versione aggiornata del firmware

---

## Configurazione del Flipper Zero

1. Collegamento del Devboard al Flipper

Collegare il WiFi Devboard al Flipper tramite PIN dedicati (suggerimento: farlo quando il FlipperZero è spento)

Assicurarsi che il Flipper riconosca il modulo nel menu dedicato

2. Attivazione del Plugin WiFi Marauder

Alcuni firmware del Flipper includono un’app dedicata al controllo del devboard

In genere il percorso è simile a:

Apps → GPIO → WiFi Marauder (o similare)

Da qui il Flipper può:

- comunicare con il modulo WiFi
- visualizzare dati e output
- inviare comandi preconfigurati
- avviare modalità di analisi

---

## Funzionalità Principali

WiFi Marauder è uno strumento avanzato di diagnostica e analisi
Di seguito una panoramica, utile per capire cosa offre

1. Scansione WiFi / Discovery

Permette di:

- identificare reti vicine
- visualizzare di AP, canali, potenza del segnale, cifrature
- raccogliere informazioni utili per valutazioni di sicurezza (audit autorizzati)

Utilizzo legittimo: controllare la copertura della propria rete, verificare canali affollati, audit autorizzati

2. Packet Monitoring (Sniffer)

Il modulo può osservare attività radio su una banda WiFi, mostrando:

- frame di gestione
- beacon
- traffico non cifrato (se presente)
- pattern di segnale utili alla diagnostica

Utilizzo legittimo: analizzare interferenze, monitorare comportamento di dispositivi IoT autorizzati

3. Beacon Frame Broadcasting

Il modulo può generare beacon WiFi artificiali per scopi di:

- test sulla robustezza di device IoT
- simulazioni per verificare come un sistema reagisce a reti non affidabili

(Non utilizzare questa funzione per saturare lo spettro radio o disturbare terzi)

4. Fake Access Point (AP simulati)

Creazione di reti di test per analizzare:

- comportamento di dispositivi autorizzati
- creazione di access point fittizi
- configurazioni errate che potrebbero esporre utenti a rischi

Utilizzo legittimo: dimostrazioni educative e test controllati

5. Test di Robustezza (DoS mirati e non)

WiFi Marauder include funzioni utili a valutare la resistenza di un dispositivo a condizioni anomale, come:

- saturazione di management frames
- tentativi di disassociazione controllati
- stress test della rete

(Queste funzionalità devono essere usate solo su reti e dispositivi autorizzati e in contesti di laboratorio)

---

## Utilizzo dal Flipper Zero

Dopo aver aperto l'app WiFi Marauder sul Flipper, è possibile:

- navigare tra le modalità di analisi
- visualizzare liste di reti
- selezionare funzioni diagnostiche
- monitorare output e log in tempo reale

Il Flipper funge da interfaccia di controllo, mentre l’ESP32 esegue l’elaborazione

Note: dopo la configurazione iniziale non serve più il PC: tutto viene gestito dal Flipper

---

## Note / Avvertenze importanti

Il Flipper Zero non ha WiFi integrato: tutto funziona grazie all’ESP32

Scarica sempre il firmware corretto per il tuo tipo di ESP32

Alcune schede richiedono driver aggiuntivi su Windows

Le funzioni più invasive (sniffing, deauth, fake AP, broadcast) possono essere illegali su reti non autorizzate

Segui il principio: solo test etici e autorizzati