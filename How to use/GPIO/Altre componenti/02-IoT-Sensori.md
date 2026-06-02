# IoT e Sensori - Misurazioni, Monitoraggio e Diagnostica

Questa sezione raccoglie gli strumenti GPIO dedicati a sensori, misurazioni ambientali, monitoraggio batterie, test di continuità e strumenti di diagnostica fisica. Ideali per progetti IoT, laboratorio e field testing.

---

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

### • CO2 Logger

Strumento dedicato alla misurazione e registrazione dei livelli di CO₂ da sensori compatibili (MH‑Z19, SCD30, CCS811 e simili).

Funzionalità ampliate:

- Lettura continua in tempo reale (ppm, temperatura, umidità se supportati).
- Logging interno con timestamp.
- Calibrazione automatica ABC o manuale.
- Grafico storico a breve termine.
- Esportazione log in formato CSV.
-  Funzione "Air Quality Alert" con soglie configurabili.

Esempio pratico

Monitoraggio qualità dell'aria in un ufficio:

- Collegare TX/RX (o SDA/SCL per sensori I2C).
- Attivare logging ogni 10 secondi.
- Impostare allarme a 1200 ppm.
- Analizzare CSV per verificare ventilazione insufficiente.

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

### • Continuity Tester

Tester per la continuità elettrica con visualizzazione visiva/uditiva ad alta reattività.

Funzionalità ampliate:

- Tempo di risposta < 5 ms.
- Segnale acustico con intensità proporzionale alla resistenza.
- Test resistenza (stima ohmica non calibrata).
- Modalità "Hands-Free" con latch.
- Logica anti-rimbalzo per contatti rovinati.

Esempio pratico

Verifica di piste su PCB danneggiato:

- Collegare le sonde ai pin GPIO dedicati.
- Attivare modalità acustica.
- Spostare le sonde seguendo la traccia.
- Identificare punto di interruzione in pochi secondi.

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

### • INA Meter

Misura corrente, tensione e potenza tramite sensori INA219/INA226.

Funzionalità ampliate:

- Letture mA/mV precise.
- Calcolo potenza in tempo reale.-
- Logging consumo.
- Calibrazione Shunt personalizzata.
- Modalità "Energy Counter".

Esempio pratico

Analisi di un modulo WiFi:

- Collegare alimentazione tramite INA.-
- Connettere al tool → leggere picchi consumo TX.
- Usare log per ottimizzare duty cycle.

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

### • Fencing Test Box

Strumento per la diagnosi dell'attrezzatura di scherma (fioretto, spada, sciabola), compatibile con le logiche elettriche regolamentari.

Funzionalità ampliate:

- Test continuità punta/spada con soglie regolabili.
- Simulazione box arbitro: luci "colpo valido / colpo non valido".
- Logging eventi per analisi successiva.
- Modalità "Training" per misurare tempo di reazione.
- Supporto configurazioni FIE (impedenza, tempi minimi).

Esempio pratico

Verifica di un fioretto con contatti difettosi:

- Collegare clip ai terminali arma.
- Attivare monitoraggio punta.
- Premere e rilasciare → rilevare irregolarità nel tempo di chiusura.
- Identificare contatto ossidato da sostituire.

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
