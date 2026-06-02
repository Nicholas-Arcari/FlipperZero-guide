# Comunicazioni - Radio, Seriale, Bus e Protocolli

Questa sezione raccoglie gli strumenti GPIO dedicati alle comunicazioni: LoRa, FM, UART, SPI, I2C, Modbus, RFID UHF, Wiegand e altri protocolli di trasmissione dati. Fondamentali per analisi di reti wireless, debug seriale e integrazione con dispositivi esterni.

---

### • E220 LoRa Configurator

Strumento avanzato per la configurazione dei moduli EBYTE E220 (LoRa 410/433/868/915 MHz).

Funzionalità ampliate:

- Lettura e scrittura parametri:
    - Potenza TX
    - Data rate
    - Canale
    - Modalità di funzionamento
    - Indirizzi e reti
- Test RSSI e SNR.
- Modalità "Range Test" automatizzata.
- Esportazione/importazione profili.

Esempio pratico

Preparazione rete LoRa a 868 MHz:

- Collegare M0/M1 + UART.
- Leggere configurazione attuale.
- Impostare: 868.5 MHz, TX High Power, modalità fixed transmission.
- Salvare profilo → duplicarlo su moduli secondari.

### • LoRa Sample

Esempi base di comunicazione tramite moduli LoRa (433/868/915 MHz).

Funzionalità ampliate:

- Trasmissione pacchetti test.
- Ricezione e logging dati.
- Configurazione frequenza e potenza TX.
- Supporto modalità point-to-point e broadcast.
- Debug tramite monitor seriale.

Esempio pratico

Invio messaggio tra due moduli:

- Configurare modulo TX → 868 MHz.
- Configurare modulo RX → ricezione su stesso canale.
- Inviare pacchetto → confermare ricezione lato RX.
- Registrare RSSI e SNR per analisi.

### • LoRa Termina

Terminale completo per interfacciarsi con moduli LoRa avanzati.

Funzionalità ampliate:

- Interfaccia CLI per invio e ricezione pacchetti.
- Impostazioni avanzate: spreading factor, bandwidth, coding rate.
- Monitoraggio pacchetti live.
- Logging su file CSV/HEX.
- Compatibilità con moduli SX127x.

Esempio pratico

Test rete LoRa:

- Connettere modulo → aprire terminale.
- Invia pacchetto test "Hello LoRa".
- Controlla risposta → log completo.
- Registra RSSI/SNR per mappatura link.

### • Loradar

Radar via rete LoRa per rilevazione oggetti e tracking.

Funzionalità ampliate:

- Invio pacchetti periodici con segnali "ping".
- Misura tempo di risposta per distanza approssimativa.
- Logging eventi e mappatura oggetti.
- Funzione sweep multi‑canale.
- Supporto alert su oggetti fuori range.

Esempio pratico

Rilevazione oggetti:

- Attivare sweep su canale 868 MHz.
- Ricevere eco → calcolare distanza relativa.
- Visualizzare mappa temporale oggetti rilevati.

### • BunnyConnect

Interfaccia per comunicare con dispositivi Bunny.

Funzionalità ampliate:

- Trasferimento dati tra Flipper e dispositivi Bunny via GPIO/UART.
- Controllo remoto e sincronizzazione parametri.
- Lettura stato e logs dei device.
- Supporto multi-device con selezione automatica della porta.

Esempio pratico:

- Collegare Flipper al device Bunny tramite pin UART.
- Avviare BunnyConnect → leggere stato batteria e log eventi.
- Inviare comando di reset o aggiornamento firmware.

(Note: Compatibile solo con dispositivi Bunny certificati)

### • DelfiRTL

Interfaccia/decoder per dispositivi radio e moduli specifici (probabilmente basati su RTL o protocolli custom).

Funzionalità ampliate:

- Decodifica protocollo proprietario.
- Monitoraggio pacchetti raw.
- Logging degli eventi.
- Modalità "Protocol Trace" per analizzare transazioni.
- Possibilità di esportare dump per analisi esterna.

Esempio pratico

Analisi di un telecomando custom:

- Collegare il modulo radio.
- Avviare Packet Sniffer.
- Registrare trame durante la pressione dei pulsanti.
- Esportare e analizzare pattern nel file log.

### • Digimon F-COM

Strumento dedicato ai dispositivi Digimon che utilizzano protocollo F-COM per scambi e sincronizzazioni.

Funzionalità ampliate:

- Emulazione completa handshake F‑COM.
- Sincronizzazione oraria.
- Backup/scrittura salvataggi.
- Lettura parametri di stato.
- Compatibilità con modelli moderni e legacy.

Esempio pratico

Backup di un Digimon prima di un reset:

- Collegare linea F‑COM (infrarosso o contatto).
- Effettuare handshake → dump completo.
- Salvare file .fc.
- Ripristinare dopo reset del device.

### • HC-11 Modem

Interfaccia per moduli seriali HC-11 (RF 433 MHz).

Funzionalità ampliate:

- Configurazione parametri AT.
- Monitor seriale dedicato.
- Controllo potenza trasmissione.
- Test di portata radio.
- Modalità "transparent link".

Esempio pratico

Setup link seriale wireless:

- Collegare modulo.
- Impostare canale e baudrate.
- Inviare testo → verificare ricezione lato remoto.

### • FM Radio

Ricevitore FM basato su moduli dedicati (es. TEA5767, RDA5807).

Funzionalità ampliate:

- Sintonizzazione automatica e manuale.
- RDS (se supportato dal modulo).
- Regolazione guadagno e volume.
- Scan banda con logging dei canali rilevati.
- Modalità "Signal Strength" per misure RF base.

Esempio pratico

Ricerca stazioni locali:

- Collegare modulo RDA5807.
- Avviare scansione automatica.
- Salvare preset trovati.
- Regolare manualmente la frequenza migliore.

### • FM Transmitter KT0803

Trasmettitore FM basato su KT0803 o simili, per inviare audio in banda FM bassa potenza.

Funzionalità ampliate:

- Impostazione frequenza TX 70–108 MHz.
- Controllo volume e pre-enfasi.
- Monitor livello segnale in uscita.
- Supporto collegamento microfono o sorgente audio esterna.
- Modalità "Beacon" per segnali brevi.

Esempio pratico

Trasmissione audio locale:

- Collegare sorgente audio (jack o microfono).
- Impostare frequenza, es. 100.1 MHz.
- Trasmettere → verificare ricezione a pochi metri.
- Regolare pre‑enfasi per chiarezza voce.

### • SI4713 Tuner

Sintonizzatore FM basato su chip SI4713.

Funzionalità ampliate:

- Sintonizzazione frequenze FM (87–108 MHz).
- Lettura segnale RSSI e qualità.
- Visualizzazione frequenza e nome stazione RDS (se disponibile).
- Salvataggio preset stazioni preferite.

Esempio pratico

Ascolto stazione FM:

- Collegare antenna → alimentare SI4713.
- Sintonizzare 101.1 MHz → visualizzare nome stazione.
- Salvare preset → riproduzione automatica.

### • UART Echo

Eco seriale UART per test di comunicazioni.

Funzionalità ampliate:

- Ricezione dati UART e ritrasmissione immediata.
- Test linea TX/RX.
- Monitoraggio baud rate e parità.

Esempio pratico

Verifica cablaggio seriale:

- Collegare TX/RX → inviare carattere test.
- Controllare eco → confermare linea funzionante.

### • UART Terminal

Terminale completo per comunicazioni UART.

Funzionalità ampliate:

- Invio/ricezione dati ASCII/HEX.
- Logging su file.
- Configurazione baud rate, parità, stop bit.
- Monitoraggio flusso seriale.

Esempio pratico

Debug sensore UART:

- Connettere sensore → aprire terminale.
- Ricevere output dati.
- Analizzare valori e loggare su file.

### • Modbus

Interfaccia bus Modbus RTU/ASCII tramite GPIO.

Funzionalità ampliate:

- Lettura e scrittura registri.
- Polling dispositivi slave.
- Supporto checksum CRC.
- Logging transazioni.
- Compatibile con PLC e strumenti industriali.

Esempio pratico

Leggere registro sensore industriale:

- Connettere GPIO → RS485/TTL converter.
- Invia comando Modbus → leggere holding register.
- Verifica valore corrente → log su CSV.

### • Wiegand Reader

Lettore badge Wiegand standard.

Funzionalità ampliate:

- Lettura codice badge 26/34 bit.
- Logging eventi.
- Integrazione con sistemi access control.
- Debug linea D0/D1 tramite GPIO.

Esempio pratico

Accesso badge:

- Collegare lettore → GPIO.
- Swipe badge → leggere codice.
- Confermare log evento su file.

### • Simultaneous UHF RFID

Lettura simultanea di tag UHF RFID.

Funzionalità ampliate:

- Rilevamento multiplo tag in range.
- Lettura EPC, TID e altri dati.
- Logging su file per analisi.
- Supporto protocolli EPC Gen2.

Esempio pratico

Inventario RFID:

- Attivare lettore → scan area.
- Rilevare tag multipli → salvare EPC.
- Analizzare lista per conferma presenza oggetti.

### • UHF RFID

Interfaccia lettura/scrittura tag UHF RFID.

Funzionalità ampliate:

- Supporto EPC Gen2.
- Lettura/Trova singoli o multipli tag.
- Logging dati.
- Scrittura nuovi EPC.

Esempio pratico

Gestione magazzino:

- Scansionare tag → leggere EPC.
- Salvare dati → aggiornare inventario.
- Scrivere EPC aggiornati se necessario.

### • SPI Terminal

Terminale avanzato per dispositivi SPI.

Funzionalità ampliate:

- Lettura e scrittura byte/word.
- Dump memoria esterna SPI.
- Debug linee CS/MISO/MOSI/SCK.
- Logging pacchetti e timing.

Esempio pratico

Test memoria SPI:

- Collegare flash esterna.
- Eseguire dump → analizzare contenuto.
- Scrivere byte test → confermare scrittura corretta.

### • I2C Explorer

Strumento avanzato di ispezione bus I2C.

Funzionalità ampliate:

- Scansione approfondita (0x03–0x77).
- Lettura registri live.
- Dump memoria di sensori compatibili.
- Scope digitale per SDA/SCL.
- Auto‑identificazione dispositivi comuni.

Esempio pratico

Diagnosi sensore che non risponde:

- Avviare scan → nessun device.
- Attivare visualizzazione SDA/SCL.
- Notare SCL bloccato LOW → corto su linea.

### • GPIO with I2C

Interfaccia combinata che permette di usare pin GPIO insieme a bus I2C.

Funzionalità ampliate:

- Scansione dispositivi I2C.
- Lettura/scrittura registri.
- Modalità mista: GPIO + I2C simultanei.
- Supporto sensori I2C multipli in parallelo.
- Regolazione clock 100/400 kHz.

Esempio pratico

Gestione doppio sensore:

- Collega due moduli (es. MPU6050 e BH1750).
- Scansione → rilevati 0x68 e 0x23.
- Leggi dati entrambi in streaming.

### • SD SPI

Gestione schede SD tramite interfaccia SPI.

Funzionalità ampliate:

- Lettura e scrittura file system FAT16/FAT32.
- Creazione, cancellazione e modifica file.
- Dump completo della scheda.
- Compatibilità con SD standard, SDHC e microSD tramite adattatore.
- Debug linee SPI per analisi segnali.

Esempio pratico

Salvataggio dati sensori:

- Collegare scheda SD ai pin SPI (MOSI/MISO/SCK/CS).
- Creare file "log.csv".
- Scrivere valori letti da sensore.
- Leggere file → confermare integrità dati.

### • GS1 Parser

Lettore e decodificatore di codici GS1 (EAN, UPC, DataMatrix GS1).

Funzionalità ampliate:

- Parsing automatico Application Identifier (AI).
- Identificazione date, lotti, numeri prodotto.
- Supporto formati lineari e 2D.
- Logging scansioni con timestamp.
- Esportazione CSV.

Esempio pratico

Decodifica prodotto alimentare:

- Scansione codice GS1.
- Visualizza AI: scadenza, lotto, produttore.
- Salva dati per inventario.