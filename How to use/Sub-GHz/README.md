# SUB-GHZ

Strumenti avanzati dedicati all’analisi, registrazione, trasmissione, fuzzing e studio dei dispositivi che utilizzano frequenze Sub‑GHz (300–928 MHz).

Utili in ambito domotico, sensori, telecomandi, pagers, protocolli industriali, analisi RF e ricerca sulla sicurezza.

---

### • Chief Cooker

Sistema creativo per generare segnali RF personalizzati.

Funzionalità ampliate:

- Creazione rapida di “ricette” RF da parametri grezzi.
- Configurazione ampia di modulazioni ASK/OOK.
- Esportazione e riutilizzo all’interno della cartella Sub‑GHz.
- Debug e prova rapida su dispositivi proprietari.

Esempio pratico

Creazione di una sequenza di comandi per un cancello:

- Impostare frequenza → 433.92 MHz.
- Generare pattern ASK basato su campioni ricavati.
- Trasmettere → verificare reazione del ricevitore.
- Ritoccare lunghezze impulsi e salvare ricetta finale.

### • Enhanced Sub‑GHz Chat

Sistema di comunicazione via RF tra Flipper e altri dispositivi compatibili.

Funzionalità ampliate:

- Chat bidirezionale tramite pacchetti Sub‑GHz.
- Modalità broadcast o indirizzamento specifico.
- Supporto a protocolli semplici e telegrammi corti.
- Log cronologico dei messaggi.

Esempio pratico

Comunicazione con un altro Flipper:

- Impostare stessa frequenza (es. 315 MHz).
- Avviare modalità chat → scambio messaggi.
- Test utile per verificare portata e interferenze.

### • Frequency Analyzer w/ External

Analizzatore di frequenza con antenna o modulo esterno.

Funzionalità ampliate:

- Identificazione precisa di frequenze attive.
- Supporto a LNA/antenne esterne per aumentare la sensibilità.
- Visualizzazione picchi in tempo reale.
- Log delle frequenze rilevate.

Esempio pratico

Individuare frequenza di un telecomando sconosciuto:

- Premere tasto telecomando vicino al modulo esterno.
- Annotare frequenza dominante rilevata.
- Importare valore nel tool Sub‑GHz per registrazione.

### • FRSSCAN

Scanner dedicato ai protocolli FRSky (telemetria e RC).

Funzionalità ampliate:

- Rilevamento pacchetti RC.
- Analisi telemetria base.
- Identificazione pattern di binding.
- Supporto per modelli D e X (se disponibili).

Esempio pratico

Analizzare un radiocomando per droni:

- Avviare FRSSCAN.
- Attivare telecomando RC.
- Osservare pacchetti e RSSI.
- Utilizzare dati per debug o reverse engineering.

### • Genie Door Recorder

Registratore e riproduttore di telecomandi per garage compatibili.

Funzionalità ampliate:

- Decodifica protocolli Genie.
- Registrazione pulsanti Open/Close.
- Riproduzione istantanea.
- Supporto rolling e fixed codes (nei limiti del legale).

Esempio pratico

Duplicazione controllo interno (legalmente, per proprio garage):

- Premere pulsante originale vicino al Flipper.
- Salvare registrazione.
- Trasmettere → test operativo sul garage.

### • Marmalade

Strumento creativo che trasforma file audio o tono in segnali RF.

Funzionalità ampliate:

- Convertire pattern audio → OOK Sub‑GHz.
- Salvare come telecomando RF.
- Parametrizzare modulazione e durata.

Esempio pratico

Usare un breve beep per generare un segnale RF personalizzato:

- Caricare file audio.
- Convertire in forma OOK.
- Trasmettere → osservare effetto.

### • Music to Sub‑GHz Radio

Convertitore musicale → segnale RF.

Funzionalità ampliate:

- Trasferimento pattern musicali su OOK ASK.
- Frequenza personalizzabile.
- Logging di impulsi generati.

Esempio pratico

Trasmissione di una melodia come test RF:

- Importare MIDI/WAV.
- Impostare 433 MHz.
- Trasmettere melodia.

Usata per verificare sensibilità ricevitori.

### • POCSAG Pager

Decoder/encoder per protocolli pager POCSAG.

Funzionalità ampliate:

- Ricezione messaggi digitali su 433–466 MHz.
- Analisi pacchetti.
- Generazione messaggi semplici (solo in modalità legale/offline).
- Esportazione log.

Esempio pratico

Analisi di un pager ospedaliero (in modalità monitor legale):

- Impostare frequenza locale.
- Monitorare canale.
- Decodificare messaggi broadcast dimostrativi.

### • Protocols Visualizer

Sistema di visualizzazione dei protocolli RF decodificati.

Funzionalità ampliate:

- Visualizzazione grafica trame.
- Identificazione header, payload, sync.
- Comparazione automatica tra protocolli.
- Esportazione grafici.

Esempio pratico

Analisi struttura di un telecomando:

- Registrare segnale Sub‑GHz.
- Aprire nel visualizer.
- Identificare bit di rolling code.

### • Radio Scanner

Scanner continuo delle frequenze Sub‑GHz.

Funzionalità ampliate:

- Scansione 300–928 MHz.
- Rilevazione picchi.
- Grafico RSSI in tempo reale.
- Salvataggio frequenze attive.

Esempio pratico

Scoprire quali frequenze usa un edificio domotico:

- Lanciare scanner.
- Controllare picchi al passare delle persone.
- Annotare e analizzare.

### • Restaurant Pager

Decoder per sistemi di chiamata nei fast‑food/ristoranti.

Funzionalità ampliate:

- Identificazione protocolli comuni dei pagers.
- Monitoraggio pacchetti.
- Decodifica ID dispositivo.
- Logging eventi.

Esempio pratico

Studiare un chiamapranzo (senza interferire):

- Impostare frequenza tipica 433/315 MHz.
- Osservare pacchetti → capire formato.

Utile per analisi e documentazione.

### • Shapshup

Trasformatore creativo di segnali RF → nuovi pattern.

Funzionalità ampliate:

- Applicazione “effetti” ai segnali registrati.
- Stretch/Compress, invert, slice.
- Testing RF creativo.

Esempio pratico

Modifica di un segnale fisso:

Registrare telecomando.

- Applicare “stretch” del 5%.
- Verificare comportamento del ricevitore target.

### • Spectrum Analyzer

Analizzatore di spettro RF.

Funzionalità ampliate:

- FFT in tempo reale.
- Visualizzazione ampiezza/frequenza.
- Filtri per ridurre rumore.
- Supporto banda 315/433/868/915 MHz.

Esempio pratico

Determinare interferenze in un garage:

- Avviare spectrum analyzer.
- Premere telecomandi vicini.
- Identificare segnali sovrapposti.

### • Sub Analyzer

Analizzatore generico dei segnali Sub‑GHz.

Funzionalità ampliate:

- Decodifica protocolli comuni.
- Visualizzatore di pacchetti.
- Riconoscimento firme protocollari.
- Log esportabile.

Esempio pratico

Studiare protocollo di una sirena wireless:

- Registrare segnale.
- Osservare bit pattern.
- Analizzare parità e payload.

### • Sub‑GHz

Il modulo principale per trasmissione e ricezione.

Funzionalità ampliate:

- Registrazione telecomandi.
- Trasmissione codici fissi.
- Analisi rolling code (solo ricerca/educational).
- Ampia lista protocolli built‑in (Nice, FAAC, Came, ecc.).
- Playlist RF.

Esempio pratico

Registrare un telecomando per uso personale:

- Avviare “Read”.
- Salvare file.
- Trasmettere → testare.

### • Sub‑GHz Bruteforcer

Ricerca automatizzata di combinazioni di telecomandi.

Funzionalità ampliate:

- Sequenze pre-settate di test.
- Invio pacchetti incrementali.
- Logging risultati.
- Controlli di sicurezza (timeout, ritmo, limiti).

Esempio pratico

Test sicurezza del proprio cancello:

- Selezionare protocollo corrispondente.
- Impostare intervallo ID.
- Avviare test → verificare robustezza sistema.

### • Sub‑GHz Playlist

Gestione liste di segnali RF.

Funzionalità ampliate:

- Raccolta multipla di telecomandi.
- Riproduzione sequenziale.
- Riordinamento e timing.
- Supporto utilizzi ripetitivi.

Esempio pratico

Test multipli su più dispositivi:

- Creare playlist con 3 telecomandi.
- Riprodurre sequenza automatica.

### • Sub‑GHz Playlist Creator

Editor avanzato per creare playlist RF.

Funzionalità ampliate:

- Editing tempi ON/OFF.
- Import di segnali registrati.
- Clonazione facile.
- Aggiunta note.

Esempio pratico

Preparare test di automazione:

- Aggiungere 10 comandi in ordine.
- Impostare intervalli personalizzati.

### • Sub‑GHz Remote

Telecomando RF universale basato su schemi pre‑esistenti.

Funzionalità ampliate:

- Gestione telecomandi per elettrodomestici.
- Pannello rapido tasti.
- Supporto protocolli semplici.
- Salvataggio rapido preset.

Esempio pratico

Creare un telecomando custom:

- Caricare codice da file.
- Impostare pulsanti su schermata.
- Usarlo come telecomando principale.

### • Sub‑GHz Rolling Flaws

Analizzatore vulnerabilità rolling code.

Funzionalità ampliate:

- Identificazione seed.
- Analisi entropia.
- Riconoscimento debolezze protocolli.
- Output dettagliato sicurezza.

Esempio pratico

Testare un vecchio modello di garage:

- Registrare due sequenze.
- Avviare analisi.
- Valutare robustezza dell’algoritmo rolling.

### • Sub‑GHz Scheduler

Automazione temporizzata di comandi RF.

Funzionalità ampliate:

- Invio programmato di segnali RF.
- Timer, ripetizione, intervalli.
- Integrazione playlist.
- Log storico.

Esempio pratico

Far partire un automatismo ogni 10 minuti:

- Impostare comando → intervallo 10 minuti.
- Attivare scheduler.
- Verificare funzionamento.

### • Sub‑GHz Test

Suite diagnostica Sub‑GHz.

Funzionalità ampliate:

- Test hardware RF.
- Test potenza di trasmissione.
- Test ricezione.
- Diagnostica antenna interna.

Esempio pratico

Verificare integrità RF del Flipper:

- Eseguire tutti i test.
- Controllare valori RSSI.
- Confermare funzionamento hardware.

### • SubGHz Toolkit

Raccolta strumenti RF in un’unica interfaccia.

Funzionalità ampliate:

- Mini-scan.
- Registrazione rapida.
- Conversione protocolli.
- Espansione funzioni base.

Esempio pratico

Utilizzo rapido quotidiano:

- Aprire Toolkit.
- Usare opzioni senza aprire moduli avanzati.

### • TPMS Reader

Reader per sensori pressione pneumatici (TPMS).

Funzionalità ampliate:

- Ricezione pacchetti TPMS auto/moto.
- Decodifica ID sensore.
- Lettura pressione e temperatura.
- Log pacchetti.

Esempio pratico

Analisi sensore TPMS:

- Attivare lettura.
- Avvicinare sensore.
- Visualizzare ID e pressione.

### • Weather Station

Decoder segnali meteo da stazioni wireless.

Funzionalità ampliate:

- Ricezione temperatura/umidità.
- Identificazione marca/protocollo.
- Log misure.
- Decodifica trame meteo comuni.

Esempio pratico

Monitorare una stazione casalinga:

- Impostare frequenza tipica (433 MHz).
- Leggere pacchetti periodici.
- Visualizzare temperatura/umidità.