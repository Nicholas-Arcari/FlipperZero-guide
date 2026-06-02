# Creativi e Utility - Strumenti GPIO, Analisi Segnali e Automazione

Questa sezione raccoglie gli strumenti GPIO di uso generale: controllo LED, output analogici, lettura pin, encoder, oscilloscopi, analizzatori logici, generatori di segnale, servo tester e altri tool di utilità quotidiana per maker, tester e sviluppatori hardware.

---

### • Air Mouse

Tool per controllare il cursore del dispositivo o PC tramite movimenti del Flipper Zero.

Funzionalità ampliate:

- Rilevamento movimenti su 3 assi tramite accelerometro interno.
- Supporto a protocolli mouse HID via GPIO o Bluetooth.
- Sensibilità regolabile e calibrazione automatica.
- Movimento relativo e assoluto selezionabile.

Esempio pratico:

- Collegare il Flipper via USB HID.
- Attivare modalità "Mouse".
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
- Attivare "scroll" di numeri o simboli.

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
- Ruotare l'albero e verificare direzione e step.
- Usare grafico per controllare stabilità e jitter.

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
- Modalità "Badge Animation" per effetti luminosi.
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

Tool dedicato all'analisi di attività elettrica su pin.

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

### • Oscilloscope

Oscilloscopio digitale via GPIO.

Funzionalità ampliate:

- Visualizzazione forme d'onda analogiche.
- Multi‑channel fino ai limiti del hardware.
- Trigger su salita/discesa.
- Misura frequenza, duty cycle, ampiezza.
- Esportazione dati in CSV o VCD.

Esempio pratico

Analisi segnale PWM:

- Collegare pin → ingresso oscilloscope.
- Visualizzare onda → misurare duty cycle.
- Esportare dati per report.

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
