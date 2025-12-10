# ESP32

Integrazione con moduli ESP32 per WiFi, BLE, camera e automazione.

### **• Camera**

Visualizzazione streaming da moduli ESP32-CAM.

Funzionalità ampliate:

- Supporto sensori OV2640/OV3660.
- Streaming MJPEG o JPEG snapshot.
- Regolazione parametri immagine: luminosità, contrasto, saturazione, gain, AE.
- Possibilità di scattare foto a risoluzione massima.
- Salvataggio locale o invio via rete.
- Modalità “Low Latency” per ridurre lag video.

Esempio pratico:

- Alimentare l’ESP32-CAM.
- Collegare GPIO → UART per configurazione iniziale.
- Avviare streaming → monitorare flusso video in tempo reale.
- Utilizzare la visione remota per sorveglianza o progetti robotici.

### **• Marauder**

Suite avanzata di attacchi WiFi (porting ESP32 Marauder).

Funzionalità ampliate:

- Deauthentication, Beacon Spam, Probe Monitor.
- Scansione reti 2.4 GHz.
- Analisi client e AP in prossimità.
- Logging pacchetti base (senza injection estesa).
- Interfaccia ottimizzata per Flipper Zero.
- Funzioni stealth (scan passivi).

Esempio pratico:

- Selezionare Canal Scan → individuare AP attivi.
- Avviare Deauth su una rete non protetta previa autorizzazione.
- Monitorare disassociazione client per test di sicurezza.

### **• Morse Flash**

Utilizza il LED dell’ESP32-CAM come trasmettitore Morse.

Funzionalità ampliate:

- Supporto codifica internazionale Morse.
- Velocità personalizzabile (WPM).
- Modalità looping o messaggio singolo.
- Salvataggio messaggi predefiniti.

Esempio pratico:

- Inserire testo → converti in Morse.
- LED trasmette punti e linee → comunicazione ottica semplice.
- Utile per segnali a distanza o test luminosi.

### **• Motion Detection**

Rilevazione movimento tramite fotocamera ESP32-CAM.

Funzionalità ampliate:

- Confronto frame differenziali.
- Sensibilità configurabile.
- Snapshot automatico su trigger.
- Logging data/ora degli eventi.

Esempio pratico:

- Posizionare ESP32-CAM in un punto fisso.
- Attivare Motion Detection → monitorare ambiente.
- Ogni movimento genera foto e notifica sul Flipper.

### **• Nanny Cam**

Sistema di monitoraggio remoto video basato su ESP32-CAM.

Funzionalità ampliate:

- Streaming continuo.
- Modalità IR (se modulo dotato di LED IR).
- Audio opzionale (se hardware supportato).
- Registrazione automatica su microSD del modulo.

Esempio pratico:

- Installare ESP32-CAM in stanza.
- Accedere allo streaming dal Flipper.
- Verificare attività in tempo reale.

### **• QR Code**

Utilizza la camera ESP32-CAM per leggere QR Code.

Funzionalità ampliate:

- Decodifica QR ad alta risoluzione.
- Modalità autofocus digitale via software.
- Interpretazione contenuti: URL, testo, WiFi, vCard.
- Esportazione dati sul Flipper.

Esempio pratico:

- Puntare la fotocamera su un QR.
- Acquisire immagine → decodifica automatica.
- URL letto → apertura tramite strumenti ESP (Postman, Downloader).

### **• BLE Killer**

Suite di attacco BLE per auditing e test.

Funzionalità ampliate:

- Scan dispositivi BLE e BLE-Low Energy.
- Identificazione servizi e caratteristiche.
- Tentativi di spoofing MAC (se supportato).
- Monitoraggio pacchetti pubblicitari.

Esempio pratico:

- Scansione dispositivi indossabili.
- Identificazione UUID.
- Analisi traffico BLE per valutare sicurezza della connessione.

### **• Camera Suite**

Suite estesa per ESP32-CAM con opzioni avanzate.

Funzionalità ampliate:

- Controllo completo sensore camera.
- Time-lapse automatico.
- Visione notturna ottimizzata.
- Filtro antirumore e sharpening.

Esempio pratico:

- Impostare intervallo time-lapse.
- Salvare foto su SD.
- Creare sequenze video da frame raccolti.

### **• ESP Flasher**

Flasher per firmware ESP32/ESP32-CAM/ESP32-S2/S3.

Funzionalità ampliate:

- Flash via UART a 115200/921600 baud.
- Supporto file BIN multipli (bootloader, partitions, app).
- Auto-reset tramite GPIO.
- Identificazione chip tramite esptool integrato.

Esempio pratico:

- Collegare ESP32 a GPIO (TX/RX/EN/GND).
- Caricare firmware.bin.
- Flash → verifica checksum.
- Riavvio automatico.

### **• Evil Portal**

Crea hotspot con captive portal personalizzabile.

Funzionalità ampliate:

- Pagina HTML/CSS custom.
- Logging tentativi accesso.
- Reindirizzamento forzato tramite DNS spoofing.
- Supporto funzioni interattive (moduli, pulsanti, input).

Esempio pratico:

- Creare AP “FreeWiFi”.
- Caricare pagina personalizzata.
- Ogni client connesso vede il portale captive.

### **• FlipDownloader**

Download manager tramite ESP e rete WiFi.

Funzionalità ampliate:

- Download HTTP/HTTPS.
- Ripristino trasferimento in caso di errore.
- Browser file remoto.
- Verifica hash dei file scaricati.

Esempio pratico:

- Inserire URL → scarica firmware remoto.
- Salvare file direttamente su SD del Flipper.

### **• FlipLibrary**

Accesso a repository remoto di moduli/risorse.

Funzionalità ampliate:

- Catalogo online di file/script.
- Aggiornamento OTA.
- Categorie, tag e ricerca rapida.

Esempio pratico:

- Connettersi alla libreria.
- Scaricare nuovi moduli GPIO/ESP.
- Installazione diretta sul Flipper.

### **• FlipMap**

Mappatura reti WiFi con ESP32.

Funzionalità ampliate:

- Scansione dettagliata AP.
- Segnale RSSI in tempo reale.
- Mappa grafica (heatmap semplificata).
- Logging risultati.

Esempio pratico:

- Camminare nell’edificio con Flipper+ESP.
- Raccogliere RSSI → esportare dati.
- Ottenere mappa della copertura.

### **• FlipRPI**

Controllo remoto di Raspberry Pi.

Funzionalità ampliate:

- Invio comandi SSH preconfigurati.
- Monitoraggio CPU/RAM Pi.
- Spegnimento/riavvio remoto.
- Lettura file da directory note.

Esempio pratico:

- Collegare ESP → rete domestica.
- Flipper invia comando per riavviare RPI.
- Conferma stato in tempo reale.

### **• FlipSocial**

Interfaccia a reti social via ESP (API lato server).

Funzionalità ampliate:

- Visualizzazione notifiche social.
- Invio micro-messaggi.
- Gestione token API.
- Supporto a piattaforme selezionate (in base a proxy).

Esempio pratico:

- Autenticazione con API key.
- Invio messaggio semplice (es. tweet/testo).
- Lettura feed aggiornato.

### **• FlipTrader**

Accesso a dati crypto/finanziari.

Funzionalità ampliate:

- Quotazioni in tempo reale via API.
- Valutazione portafoglio.
- Alert configurabili (target price).
- Storico grafico semplificato.

Esempio pratico:

- Impostare ticker BTC/ETH.
- Ricevere aggiornamento live.
- Notifica raggiungimento target.

### **• FlipWeather**

Lettura dati meteo online.

Funzionalità ampliate:

- API OpenWeather o simili.
- Meteo attuale, umidità, vento, pressione.
- Previsioni brevi (1–3 giorni).
- Alert condizioni meteo critiche.

Esempio pratico:

- Impostare città.
- Visualizzare condizioni meteo attuali.
- Controllare previsione prima di uscire.

### **• FlipWiFi**

Gestione avanzata WiFi tramite ESP.

Funzionalità ampliate:

- Scan AP dettagliati.
- Connessione/disconnessione.
- Salvataggio profili WiFi.
- Test ping, traceroute.

Esempio pratico:

- Connettersi a rete domestica.
- Testare latenza → analizzare qualità connessione.

### **• FlipWorld**

Informazioni globali e geolocalizzate.

Funzionalità ampliate:

- Info Paesi, valute, fusi orari.
- Ricerca geolocalizzata IP.
- Conversioni valutarie rapide.

Esempio pratico:

- Inserire paese → ottenere dati.
- Controllare valuta e fuso locale prima di viaggi.

### **• Free Roam**

Strumento avanzato per esplorazione di segnali WiFi/BLE.

Funzionalità ampliate:

- Scan simultaneo WiFi+BLe.
- Logging continuo.
- Identificazione dispositivi mobili.
- Export CSV/JSON.

Esempio pratico:

- Attivare roaming mode.
- Mappare dispositivi in un’area affollata (autorizzato).

### **• Gemini IA**

Interfaccia a modelli Google Gemini tramite ESP.

Funzionalità ampliate:

- Invio prompt testuali.
- Lettura risposte dal modello remoto.
- Token limit manager per API.
- Modalità interattiva.

Esempio pratico:

- Scrivere domanda sul Flipper.
- ESP invia prompt → riceve risposta IA.

### **• Ghost EPS**

Funzioni stealth su WiFi/BLE.

Funzionalità ampliate:

- Scan passivo non rilevabile.
- MAC randomization.
- Analisi dispositivi senza trasmissione attiva.
- Profiling segnale.

Esempio pratico:

- Monitorare rete senza inviare pacchetti.
- Identificare AP e client attivi.

### **• Gravity**

Esperimenti fisici tramite sensori collegati via ESP.

Funzionalità ampliate:

- Lettura accelerometri, giroscopi, sensori vari.
- Dashboard sul Flipper.
- Logging dati scientifici.
- Modalità laboratorio didattico.

Esempio pratico:

- Collegare IMU → registrare accel/gyro.
- Verificare andamento oscillazioni su grafico.

### **• Postman**

Client API integrato.

Funzionalità ampliate:

-GET, POST, PUT, DELETE.
- Headers personalizzati.
- Parsing JSON automatico.
- Salvataggio richieste predefinite.

Esempio pratico:

- Inserire endpoint API.
- Inviare GET → visualizzare risposta JSON.

### **• Wardriver**

Scanner WiFi mobile con logging GPS.

Funzionalità ampliate:

- Rilevamento AP + coordinate GPS.
- Logging su file wardrive standard.
- Compatibile con Wigle CSV.
- Statistiche reti trovate.

Esempio pratico:

- Camminare/viaggiare con ESP+GPS.
- Generare report wardriving completo.

### **• Web Crawler**

Mini spider via ESP.

Funzionalità ampliate:

- Download HTML pagine.
- Follow link limitati.
- Estrazione testi e metadati.
- Lista URL visitati.

Esempio pratico:

- Inserire URL → scaricare contenuti.
- Esportare testo della pagina su Flipper.

### **• Wendigo BT+BLE+WiFi Monitor**

Monitor tri-protocollo.

Funzionalità ampliate:

- Scansione simultanea BT, BLE e WiFi.
- Identificazione dispositivi.
- Filtri per tipo protocollo.
- Logging combinato.

Esempio pratico:

- Analisi area con dispositivi multiprotocollo.
- Creazione profilo completo segnali circostanti.

### **• WiFi Mapping**

Creazione mappe segnale WiFi.

Funzionalità ampliate:

- Rilevamento RSSI continuo.
- Associazione a coordinate.
- Heatmap esportabile.
- Storico punti misurati.

Esempio pratico:

- Camminare in casa/ufficio.
- Creare mappa segnale → identificare zone morte.

### **• WiFi Marauder**

Versione espansa del Marauder classico.

Funzionalità ampliate:

- Attacchi aggiuntivi.
- Migliore gestione pacchetti.
- Interfaccia migliorata.
- Logging dettagliato attacchi.

Esempio pratico:

- Avviare tool.
- Eseguire analisi avanzata reti.