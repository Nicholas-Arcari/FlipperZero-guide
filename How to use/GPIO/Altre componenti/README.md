# Altre Componenti nella Cartella GPIO

Questi componenti non appartengono a una sottocartella specifica ma sono inclusi direttamente nella cartella principale GPIO.

### • Air Mouse

Tool per controllare il cursore del dispositivo o PC tramite movimenti del Flipper Zero.

Funzionalità ampliate:

- Rilevamento movimenti su 3 assi tramite accelerometro interno.
- Supporto a protocolli mouse HID via GPIO o Bluetooth.
- Sensibilità regolabile e calibrazione automatica.
- Movimento relativo e assoluto selezionabile.

Esempio pratico:

- Collegare il Flipper via USB HID.
- Attivare modalità “Mouse”.
- Muovere il dispositivo → il cursore sul PC si muove.
- Testare clic con pulsante GPIO configurato come tasto sinistro.

(Note: Alcuni PC richiedono driver HID aggiornati)

### • 7-Segment Output

Pilota display a 7 segmenti tramite GPIO.

Funzionalità ampliate:

- Controllo individuale dei segmenti a livello digitale o tramite driver esterno.
- Supporto multiplexing per display multipli.
- Possibilità di visualizzare numeri, lettere limitate e simboli personalizzati.

Esempio pratico:

- Collegare catodo comune → GPIO configurati come output.
- Impostare sequenza di numeri (0–9) per test.
- Attivare “scroll” di numeri o simboli.

(Note: Attenzione alla corrente massima dei LED: usare resistori adeguati)

### • Input Reader 2

Lettura di più input digitali contemporaneamente.

Funzionalità ampliate:

- Supporto a più canali GPIO.
- Rilevamento livelli HIGH/LOW e debounce software.
- Trigger su fronte di salita/discesa.
- Modalità polling e interrupt (se hardware compatibile).

Esempio pratico:

- Collegare 4 pulsanti a 4 pin GPIO.
- Avviare lettura multipla.-
- Premere i pulsanti → console Flipper mostra quale è stato premuto.

(Note: Evitare cavi troppo lunghi senza resistenze di pull-up/pull-down)

### • Intervalometer

Timer per fotocamere, automazione o trigger sequenziali.

Funzionalità ampliate:

- Configurabile per intervalli in secondi, minuti o ore.
- Trigger via GPIO o relè per attuatori esterni.
- Modalità singolo scatto, intervallo continuo o a conteggio.

Esempio pratico:

- Collegare modulo relè a fotocamera.
- Impostare intervallo 10 sec.
- Avviare → il Flipper attiva il relè ogni 10 secondi.

(Note: Alcuni moduli fotocamera richiedono trigger con polarità specifica)

### • Pins Reader

Lettura rapida dello stato dei pin GPIO.

Funzionalità ampliate:

- Monitoraggio multiplo dei livelli digitali.
- Lettura in tempo reale con aggiornamento frequente.
- Supporto per pull-up/pull-down interni o esterni.
- Trigger programmabili su fronte di salita/discesa.

Esempio pratico:

- Collegare 6 pin a sensori digitali.
- Avviare Pins Reader → leggere valori HIGH/LOW su tutti i pin contemporaneamente.
- Configurare alert su pin che cambiano stato.

(Note: Utile per debug hardware o test di schede custom)

### • RGB LED

Controllo LED RGB tramite PWM.

Funzionalità ampliate:

- Gestione dei colori tramite PWM su tre canali (R/G/B).
- Supporto a fade, blink e pattern personalizzati.
- Salvataggio di preset luminosità e combinazioni.

Esempio pratico:

- Collegare LED RGB comune anodo/catodo ai pin GPIO.
- Impostare PWM → visualizzare combinazioni di colori.
- Usare pattern ciclici per segnalazione visiva di stato.

(Note: Controllare corrente massima dei LED, usare resistori adeguati)

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

### • Step Counter

Contapassi basato su input digitale o sensori di movimento.

Funzionalità ampliate:

- Rilevazione passo tramite accelerometro o input esterni.
- Calcolo distanza stimata e conteggio calorie.
- Visualizzazione in tempo reale su display o via connessione a app.
- Supporto per reset manuale o automatico giornaliero.

Esempio pratico:

- Collegare sensore accelerometro ai pin GPIO.
- Avviare Step Counter → monitorare conteggio passi sul display del Flipper.
- Registrare sessione di attività → esportare dati per analisi.

### • GPS

Interfaccia a moduli GPS esterni.

Funzionalità ampliate:

- Ricezione dati NMEA da moduli GPS via UART.
- Parsing di latitudine, longitudine, altitudine e velocità.
- Visualizzazione posizione corrente e tracking in tempo reale.
- Logging dati GPS su file per analisi post-viaggio.

Esempio pratico:

- Collegare modulo GPS ai pin TX/RX GPIO.
- Avviare GPS → attendere fix satellitare.
- Visualizzare coordinate sul Flipper → registrare percorso.

### • ColecoVision

Interfaccia retro-console ColecoVision.

Funzionalità ampliate:

- Connessione tramite GPIO a cartucce e controller ColecoVision.
- Emulazione segnali di input/output per giochi.
- Lettura/monitoraggio memoria RAM/ROM interna cartuccia.
- Possibilità di integrare display esterno o output via seriale per debugging.

Esempio pratico:

- Collegare Flipper ai pin cartuccia → alimentare console.
- Avviare software ColecoVision → leggere stato controller.
- Monitorare input e verificare corretto funzionamento dei tasti.

(Note: Utile per sviluppo, test e retro-engineering di giochi ColecoVision)

### • Analog Output

Uscita analogica simulata tramite PWM o DAC del Flipper Zero.

Funzionalità ampliate:

- Generazione di segnali analogici variabili.
- Controllo tensione/media su pin GPIO.
- Supporto per modulazione PWM, frequenza variabile e duty cycle programmabile.
- Compatibile con piccoli circuiti di test o attuatori analogici.

Esempio pratico:

- Collegare LED o motore a pin analogico.
- Impostare duty cycle 50% → LED a metà luminosità.
- Modificare duty cycle per variazioni graduali.

(Note: Non adatto a carichi ad alta corrente senza driver esterno)

### • Atari SIO Emulator

Emulatore di periferiche Atari via GPIO.

Funzionalità ampliate:

- Simula cartucce, floppy e dispositivi Atari SIO.
- Lettura/scrittura dati per giochi e software legacy.
- Debug interfaccia SIO per sviluppo o retro-engineering.
- Compatibile con Floppy Drive o dispositivi virtuali via GPIO.

Esempio pratico:

- Collegare Flipper al connettore SIO Atari.
- Avviare emulator → caricare ROM di test.
- Verificare corretto trasferimento dati e risposta periferica.

### • Battery Checker

Strumento per misurare lo stato della batteria del Flipper o dispositivi esterni.

Funzionalità ampliate:

- Lettura tensione in tempo reale.
- Calcolo approssimativo della capacità residua.
- Monitoraggio corrente assorbita.-
- Logging storico per analisi degrado batteria.

Esempio pratico:

- Collegare batteria esterna ai pin GPIO + GND.
- Avviare Battery Checker → leggere tensione → stimare percentuale residua.
- Registrare dati in sessioni multiple per verificare performance.

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

### • CAN Transceiver

Interfaccia al bus CAN standard (Controller Area Network).

Funzionalità ampliate:

- Lettura e scrittura pacchetti CAN.
- Monitoraggio traffico in tempo reale.
- Analisi errori di comunicazione (CRC, ACK).
- Supporto a velocità standard: 125k, 250k, 500k, 1Mbps.

Esempio pratico:

- Collegare CAN_H e CAN_L ai pin GPIO dedicati.
- Avviare CAN Transceiver → monitorare messaggi da ECU automotive.
- Inviare pacchetti test per simulare sensori.

(Note: Usare resistenze di terminazione corrette per evitare errori sul bus)

### • CANBus

Lettura e scrittura avanzata su reti CAN.

Funzionalità ampliate:

- Registrazione e analisi pacchetti CAN.
- Supporto multi-ID e filtri.
- Compatibile con CAN standard e extended.

Esempio pratico:

- Collegare CANBus ai pin GPIO.
- Avviare lettura → salvare dump dei messaggi su file.
- Analizzare traffico per diagnostica ECU o dispositivi industriali.

### • CANBus Attack

Strumenti diagnostici e di attacco sul bus CAN.

Funzionalità ampliate:

- Iniezione pacchetti CAN per test di sicurezza.
- Replay attack su messaggi memorizzati.
- Analisi vulnerabilità del network CAN.

Esempio pratico:

- Collegare Flipper al bus CAN dell’auto in test.
- Avviare replay pacchetti → osservare reazioni ECU o gateway.
- Valutare sicurezza o comportamento di fail-safe.

### • CANCommander

Terminale per invio comandi CAN manuale o scriptato.

Funzionalità ampliate:

- Interfaccia testo per invio e ricezione messaggi.
- Supporto script di test automatizzati.
- Visualizzazione live di errori e stato del bus.

Esempio pratico:

- Avviare CANCommander → digitare messaggi CAN.
- Inviare comando a ECU di test → monitorare risposta.
- Script per test ciclici di messaggi su vari ID.

(Note: Utile per debugging e sviluppo di tool automotive)

### • Canon Intervalometer

Timer dedicato per fotocamere Canon.

Funzionalità ampliate:

- Scatti programmati e intervallati.
- Modalità timelapse con impostazione frequenza.
- Controllo remoto via GPIO.
- Compatibile con molte reflex Canon via connettore remoto.

Esempio pratico:

- Collegare Flipper al connettore remoto Canon.
- Impostare intervallo 5s → avviare scatti automatici.
- Salvare immagini → analizzare timelapse.

(Note: Non tutti i modelli Canon sono supportati; verificare compatibilità)

### • CO2 Logger

Strumento dedicato alla misurazione e registrazione dei livelli di CO₂ da sensori compatibili (MH‑Z19, SCD30, CCS811 e simili).

Funzionalità ampliate:

- Lettura continua in tempo reale (ppm, temperatura, umidità se supportati).
- Logging interno con timestamp.
- Calibrazione automatica ABC o manuale.
- Grafico storico a breve termine.
- Esportazione log in formato CSV.
-  Funzione “Air Quality Alert” con soglie configurabili.

Esempio pratico

Monitoraggio qualità dell’aria in un ufficio:

- Collegare TX/RX (o SDA/SCL per sensori I2C).
- Attivare logging ogni 10 secondi.
- Impostare allarme a 1200 ppm.
- Analizzare CSV per verificare ventilazione insufficiente.

### • Coffee EEPROM

Strumento per accedere alle EEPROM presenti in macchine da caffè (DeLonghi, Nespresso, ecc.) utilizzate per memorizzare contatori, configurazioni e parametri di calibrazione.

Funzionalità ampliate:

- Identificazione automatica chip (24Cxx, 93Cxx, ecc.).
- Lettura completa della memoria.
- Backup binario.
- Editing sicuro delle aree note (volumi, cicli decalcificazione).
- Protezione “Safe Zone” per evitare corruzione firmware.

Esempio pratico

Reset contatore decalcificazione:

- Collegare SDA/SCL.
- Effettuare dump completo → salvare backup.
- Modificare byte relativo al contatore.
- Scrivere solo il settore modificato.
- Riavviare macchina e verificare reset.

### • Continuity Tester

Tester per la continuità elettrica con visualizzazione visiva/uditiva ad alta reattività.

Funzionalità ampliate:

- Tempo di risposta < 5 ms.
- Segnale acustico con intensità proporzionale alla resistenza.
- Test resistenza (stima ohmica non calibrata).
- Modalità “Hands-Free” con latch.
- Logica anti-rimbalzo per contatti rovinati.

Esempio pratico

Verifica di piste su PCB danneggiato:

- Collegare le sonde ai pin GPIO dedicati.
- Attivare modalità acustica.
- Spostare le sonde seguendo la traccia.
- Identificare punto di interruzione in pochi secondi.

### • DelfiRTL

Interfaccia/decoder per dispositivi radio e moduli specifici (probabilmente basati su RTL o protocolli custom).

Funzionalità ampliate:

- Decodifica protocollo proprietario.
- Monitoraggio pacchetti raw.
- Logging degli eventi.
- Modalità “Protocol Trace” per analizzare transazioni.
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
- Modalità “Range Test” automatizzata.
- Esportazione/importazione profili.

Esempio pratico

Preparazione rete LoRa a 868 MHz:

- Collegare M0/M1 + UART.
- Leggere configurazione attuale.
- Impostare: 868.5 MHz, TX High Power, modalità fixed transmission.
- Salvare profilo → duplicarlo su moduli secondari.

### • Encoder Reader

Tool per leggere encoder rotativi (incrementali) con alta precisione.

Funzionalità ampliate:

- Riconoscimento quadratura A/B.
- Conteggio step con filtraggio anti-rimbalzo.
- Modalità velocità (step/sec).
- Reset, zero offset, direzione invertita.
- Grafico di movimento in tempo reale.

Esempio pratico

Test di un encoder industriale 600 PPR:

- Collegare canale A/B ai GPIO.
- Avviare monitoraggio live.
- Ruotare l’albero e verificare direzione e step.
- Usare grafico per controllare stabilità e jitter.

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

### • Fencing Test Box

Strumento per la diagnosi dell’attrezzatura di scherma (fioretto, spada, sciabola), compatibile con le logiche elettriche regolamentari.

Funzionalità ampliate:

- Test continuità punta/spada con soglie regolabili.
- Simulazione box arbitro: luci “colpo valido / colpo non valido”.
- Logging eventi per analisi successiva.
- Modalità “Training” per misurare tempo di reazione.
- Supporto configurazioni FIE (impedenza, tempi minimi).

Esempio pratico

Verifica di un fioretto con contatti difettosi:

- Collegare clip ai terminali arma.
- Attivare monitoraggio punta.
- Premere e rilasciare → rilevare irregolarità nel tempo di chiusura.
- Identificare contatto ossidato da sostituire.

### • Flashlight

Trasforma il dispositivo in una torcia ad alta luminosità usando il LED integrato o un LED esterno.

Funzionalità ampliate:

- Modalità luminosità variabile.
- Strobo con frequenza regolabile.
- Funzione SOS in codice Morse.
- PWM ad alta efficienza per ridurre consumo energetico.
- Possibilità di pilotare un LED potente esterno.

Esempio pratico

Uso in ambiente buio per diagnosi PCB:

- Collegare piccolo LED su GPIO.
- Regolare intensità al massimo.
- Puntare sul PCB per verificare microfratture.

### • Flipagotchi

Mini‑gioco/mascotte virtuale interattiva con grafica minimale, basato su contatori e input sensore.

Funzionalità ampliate:

- Stati multipli della creatura (felice, stanca, affamata).
- Eventi randomizzati giornalieri.
- Salvataggio stato persistente.
- Mini‑giochi integrati.
- Interazioni via accelerometro o pulsanti esterni.

Esempio pratico

Sessione di cura:

- Avviare Flipagotchi.
- Interagire inclinando il dispositivo.
- Risolvere mini‑gioco per aumentare “felicità”.
- Stato salvato automaticamente.

### • Flipper BlackHat

Set di strumenti sperimentali e non documentati, orientati a testing, ricerca e sviluppo “deep-level”.

Funzionalità ampliate:

- Accesso diretto ai registri interni.
- Funzioni diagnostiche avanzate.
- Possibili tool di exploit/sperimentazione (varia per release).
- Logging raw a basso livello.
- Modalità “unsafe” opzionale.

Esempio pratico

Debug low-level:

- Attivare modalità avanzata.
- Monitorare registri GPIO in tempo reale.
- Individuare comportamento anomalo di un pin.

### • Flippy Temp

Strumento di misura della temperatura tramite sensori esterni (TMP102, DS18B20, termistori) oppure tramite lettura ADC.

Funzionalità ampliate:

- Supporto sensori digitali e analogici.
- Conversione automatica °C/°F.
- Logging continuo con timestamp.
- Calibrazione manuale (offset/gain).
- Allarmi temperatura alta/bassa.

Esempio pratico

Monitoraggio temperatura acqua in un progetto:

- Collegare DS18B20 su singolo filo.
- Impostare logging ogni 5 secondi.
- Avviare monitor e visualizzare grafico.
- Attivare allarme > 70°C.

### • FM Radio

Ricevitore FM basato su moduli dedicati (es. TEA5767, RDA5807).

Funzionalità ampliate:

- Sintonizzazione automatica e manuale.
- RDS (se supportato dal modulo).
- Regolazione guadagno e volume.
- Scan banda con logging dei canali rilevati.
- Modalità “Signal Strength” per misure RF base.

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
- Modalità “Beacon” per segnali brevi.

Esempio pratico

Trasmissione audio locale:

- Collegare sorgente audio (jack o microfono).
- Impostare frequenza, es. 100.1 MHz.
- Trasmettere → verificare ricezione a pochi metri.
- Regolare pre‑enfasi per chiarezza voce.

### • GPIO

Strumento generico per manipolare pin digitali in input/output.

Funzionalità ampliate:

- Configurazione rapida pin come INPUT/OUTPUT/PU/PD.
- Pulsazione automatica (toggling) con frequenza definita.
- Modalità monitor per tracciare cambi di stato.
- Iniezione pattern digitali.
- Profilazione consumo per output.

Esempio pratico

Test di un relè:

- Impostare pin come OUTPUT.
- Attivare toggling lento (1 Hz).
- Ascoltare click relè → verificare operatività.

### • GPIO Badge

Badge elettronico con interfacce GPIO programmabili.

Funzionalità ampliate:

- Controllo LED integrati.
- Lettura pulsanti e sensori base.
- Modalità “Badge Animation” per effetti luminosi.
- API compatibile con altre estensioni GPIO.
- Possibilità di scripting rapido.

Esempio pratico

Animazione logo:

- Caricare script con pattern lampeggianti.
- Avviare sequenza LED.
- Impostare loop continuo.

### • GPIO Controller

Suite per la gestione avanzata dei pin digitali e analogici.

Funzionalità ampliate:

Dashboard completa di tutti i pin.

- Regolazioni ADC/DAC (se disponibili).
- Trigger condizionali: notifiche e automazioni.
- Integrazione con moduli esterni SPI/I2C.
- Supporto a macro e sequenze personalizzate.

Esempio pratico

Automazione semplice:

- Configurare input su sensore magnetico.
- Quando scatta → attiva output LED per 5s.
- Salvare e testare macro.

### • GPIO Explorer

Tool dedicato all’analisi di attività elettrica su pin.

Funzionalità ampliate:

- Monitoraggio multi‑pin in tempo reale.
- Timeline segnali con timestamp ad alta precisione.
- Misura durata impulsi (pulse width).
- Rilevamento frequenza e duty cycle.
- Esportazione log.

Esempio pratico

Analisi segnale pulsante anti‑rimbalzo:

- Collegare pulsante.
- Premere → osservare rimbalzo reale (bouncing).
- Ottimizzare circuito o software di debounce.

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

### • HC-11 Modem

Interfaccia per moduli seriali HC-11 (RF 433 MHz).

Funzionalità ampliate:

- Configurazione parametri AT.
- Monitor seriale dedicato.
- Controllo potenza trasmissione.
- Test di portata radio.
- Modalità “transparent link”.

Esempio pratico

Setup link seriale wireless:

- Collegare modulo.
- Impostare canale e baudrate.
- Inviare testo → verificare ricezione lato remoto.

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

### • INA Meter

Misura corrente, tensione e potenza tramite sensori INA219/INA226.

Funzionalità ampliate:

- Letture mA/mV precise.
- Calcolo potenza in tempo reale.-
- Logging consumo.
- Calibrazione Shunt personalizzata.
- Modalità “Energy Counter”.

Esempio pratico

Analisi di un modulo WiFi:

- Collegare alimentazione tramite INA.-
- Connettere al tool → leggere picchi consumo TX.
- Usare log per ottimizzare duty cycle.

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
- Modalità gioco “cat laser chase”.
- Allarmi ottici.
- Logging eventi.

Esempio pratico

Barriera laser:

- Attivare laser + sensore.
- Oggetto passa → interruzione → trigger evento.

### • Logic Analyzer

Analizzatore logico digitale via GPIO con capacità multi‑canale.

Funzionalità ampliate:

- Campionamento fino ai limiti hardware disponibili.
- Trigger su fronte di salita/discesa.
- Decodifica protocolli base (UART, I²C, SPI).
- Esportazione VCD/CSV.
- Visualizzazione onde in tempo reale.

Esempio pratico

Analisi traffico UART:

- Collegare RX su segnale.
- Impostare trigger su START bit.
- Registrare frame → decodifica testo.

### • Longwave Clock

Orologio a onde lunghe (LW) per sincronizzazione e misurazione temporale precisa.

Funzionalità ampliate:

- Ricezione segnali WWVB, DCF77 o MSF (secondo modulo).
- Aggiornamento orario automatico.
- Display ora e data in tempo reale.
- Logging timestamp su file.
- Modalità debug segnale per analisi qualità ricezione.

Esempio pratico

Sincronizzazione automatica:

- Collegare modulo ricevitore LW.
- Attivare ricezione DCF77.
- Visualizzare ora corrente → aggiornamento automatico ogni ora.
- Log frequenza del segnale per test ricezione.

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
- Invia pacchetto test “Hello LoRa”.
- Controlla risposta → log completo.
- Registra RSSI/SNR per mappatura link.

### • Loradar

Radar via rete LoRa per rilevazione oggetti e tracking.

Funzionalità ampliate:

- Invio pacchetti periodici con segnali “ping”.
- Misura tempo di risposta per distanza approssimativa.
- Logging eventi e mappatura oggetti.
- Funzione sweep multi‑canale.
- Supporto alert su oggetti fuori range.

Esempio pratico

Rilevazione oggetti:

- Attivare sweep su canale 868 MHz.
- Ricevere eco → calcolare distanza relativa.
- Visualizzare mappa temporale oggetti rilevati.

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

### • Notel LRF Sampler

Laser Range Finder via GPIO per misurazioni precise.

Funzionalità ampliate:

- Trigger singolo o continuo.
- Misura distanza fino a limite hardware (es. 40 m).
- Logging su file CSV.
- Conversione unità (m, cm, ft).
- Modalità debug segnali trigger/echo.

Esempio pratico

Misura distanza stanza:

- Puntare sensore verso parete.
- Attivare trigger singolo.
- Lettura distanza → registrazione in log.
- Ripetere test in più punti per mappatura.

### • Oscilloscope

Oscilloscopio digitale via GPIO.

Funzionalità ampliate:

- Visualizzazione forme d’onda analogiche.
- Multi‑channel fino ai limiti del hardware.
- Trigger su salita/discesa.
- Misura frequenza, duty cycle, ampiezza.
- Esportazione dati in CSV o VCD.

Esempio pratico

Analisi segnale PWM:

- Collegare pin → ingresso oscilloscope.
- Visualizzare onda → misurare duty cycle.
- Esportare dati per report.

### • Pokemon Trading

Interfaccia per scambi Pokémon tra device compatibili.

Funzionalità ampliate:

- Simulazione protocolli di connessione link cable.
- Emulazione scambio sicuro tra due sistemi.
- Visualizzazione Pokémon presenti e statistiche.
- Logging transazioni.
- Supporto a backup automatico.

Esempio pratico

Scambio Pokémon:

- Collegare due dispositivi → attivare modalità trading.
- Selezionare Pokémon da scambiare.
- Confermare → trasferimento dati.
- Log conferma scambio e aggiornamento database.

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
- Creare file “log.csv”.
- Scrivere valori letti da sensore.
- Leggere file → confermare integrità dati.

### • Serma CAN-FD-HS

Interfaccia bus CAN-FD ad alta velocità tramite GPIO.

Funzionalità ampliate:

- Lettura e scrittura pacchetti CAN e CAN-FD.
- Analisi bus con timestamp.
- Filtraggio ID messaggi.
- Supporto a bus automotive e industriali.
- Logging e debug avanzato.

Esempio pratico

Monitoraggio ECU auto:

- Collegare CAN_H / CAN_L.
- Avviare logging pacchetti.
- Analizzare segnali per diagnostica ECU.
- Inviare messaggi test per verifica controlli.

### • Servo Tester 2

Tester avanzato per servo analogici e digitali.

Funzionalità ampliate:

- Controllo angolo 0°–180° (o più per modelli continui).
- PWM regolabile in frequenza e duty cycle.
- Supporto per servo digitali con segnale PPM.
- Modalità sweep continua per calibrazione.
- Visualizzazione valori su display integrato (se presente).

Esempio pratico

Test servo motore:

- Collegare servo a pin GPIO + alimentazione.
- Impostare sweep da 0° a 180°.
- Osservare movimento → verificare reattività.
- Eventuale regolazione frequenza PWM.

### • ServoTester

Tester base per servo analogici.

Funzionalità ampliate:

- Controllo manuale angolo servo.
- Alimentazione servomotore tramite GPIO esterno.
- Test rapido funzionale prima di integrazione in progetti.

Esempio pratico

Verifica servo:

- Collegare servo.
- Ruotare manualmente cursore angolo.
- Controllare risposta e range movimento.

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

### • Signal Generator

Generatore di segnali via GPIO.

Funzionalità ampliate:

- Creazione onde: sinusoidale, quadrata, triangolare.
- Frequenza regolabile.
- Ampiezza regolabile secondo capacità hardware.
- Modalità sweep e burst.
- Test e calibrazione circuiti elettronici.

Esempio pratico

Test ingresso analogico:

- Collegare pin generatore → ingresso ADC.
- Impostare onda quadrata 1 kHz.
- Misurare risposta circuito → verificare linearità.

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

### • Spotify Remote

Controllo remoto di Spotify tramite GPIO + ESP/Internet.

Funzionalità ampliate:

- Play/Pause, next/previous track.
- Volume control.
- Gestione playlist tramite interfaccia GPIO + rete.
- Feedback LED su stato riproduzione.

Esempio pratico

Riproduzione musicale:

- Collegare pulsanti → Play/Pause.
- Collegare LED → indicazione stato.
- Test controllo → riproduzione corretta su device remoto.

### • Strobometer

Strobo per misure rotative o frequenze.

Funzionalità ampliate:

- Frequenza lampeggio regolabile.
- Sincronizzazione con eventi esterni.
- Misura RPM di oggetti rotanti tramite LED.
- Logging su file CSV.

Esempio pratico

Misura velocità motore:

- Puntare strobo → luci lampeggiano ad intervalli.
- Contare cicli → calcolare RPM.
- Regolare frequenza → verifica accuratezza.

### • U-Blox GPS

Interfaccia moduli GPS U-Blox tramite GPIO/UART.

Funzionalità ampliate:

- Lettura dati NMEA/GNSS.
- Posizione, velocità, tempo UTC.
- Logging tracce GPS.
- Supporto WAAS/EGNOS.
- Debug via terminale seriale.

Esempio pratico

Tracciamento percorso:

- Collegare modulo → alimentare.
- Ricevere posizione in tempo reale.
- Salvare log → visualizzazione su mappa.

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

### • WAV Recorder

Registratore audio digitale in formato WAV.

Funzionalità ampliate:

- Campionamento a 8/16/24 bit.
- Frequenza 8–48 kHz (hardware dipendente).
- Salvataggio su SD o memoria interna.
- Trigger registrazione tramite GPIO o timer.

Esempio pratico

Registrazione ambientale:

- Attivare trigger → inizio registrazione.
- Salvare file su SD.
- Riprodurre WAV per verifica qualità audio.

### • WHC SWIO Flasher

Flasher per moduli SWIO tramite GPIO.

Funzionalità ampliate:

- Lettura e scrittura firmware SWIO.
- Backup completo modulo.
- Verifica checksum post-flash.
- Compatibile con diversi microcontroller compatibili SWIO.

Esempio pratico

Aggiornamento firmware:

- Collegare SWIO → alimentare target.
- Caricare firmware → flash.
- Verificare checksum → test funzionalità.

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

### • Wii EC Analyzer

Analizzatore bus Wii/console per debugging elettronico.

Funzionalità ampliate:

- Lettura/decodifica comunicazioni tra MCU Wii.
- Debug sensori e controller.
- Logging pacchetti.
- Analisi timing e sequenze comandi.

Esempio pratico

Debug controller Wii:

- Collegare bus → avviare lettura.
- Visualizzare sequenze input.
- Analizzare dati per sviluppo custom firmware.

### • Wire Tester

Tester cablaggi e continuità GPIO.

Funzionalità ampliate:

- Verifica continuità tra pin.
- Segnalazione corto circuito.
- Test singolo o multiplo.
- Compatibilità con segnali digitali 3.3V/5V.

Esempio pratico

Verifica flat cable:

- Collegare fili → test continuità.
- Segnalazione pass/fail.
- Annotare eventuali corti o interruzioni.

### • WA2812B LED Tester

Tester LED indirizzabili WS2812/APA102 via GPIO.

Funzionalità ampliate:

- Controllo colore e brightness.
- Test sequenze animate.
- Debug linee dati e alimentazione.
- Supporto strisce singole o multiple.

Esempio pratico

Test striscia LED:

- Collegare striscia → avviare sequenza colori.
- Controllare LED difettosi → correggere connessioni.

### • Yuricable Pro Max

Strumento diagnostico avanzato multiuso.

Funzionalità ampliate:

- Test cavi e connessioni multiprotocollo.
- Misure tensione, continuità e segnali digitali.
- Logging test per documentazione.
- Supporto moduli esterni e alimentazione opzionale.

Esempio pratico

Diagnostica rete sensori:

- Collegare cavi → eseguire test continuità e tensione.
- Identificare linee malfunzionanti.
- Registrare log per manutenzione.