## 4. Tool Camera

### 4.1 Camera

**Cosa fa a livello tecnico**

Camera è il tool base per lo streaming video dall'ESP32-CAM al Flipper Zero. L'ESP32-CAM cattura frame dalla camera OV2640/OV3660, li comprime in formato JPEG e li trasmette via UART al Flipper, che li decomprime e visualizza sul suo display monocromatico 128x64 pixel.

A livello tecnico, il flusso e':
1. Il sensore camera cattura un frame RAW (YUV o RGB).
2. Il processore immagine dell'ESP32 comprime il frame in JPEG.
3. Il JPEG viene ridimensionato alla risoluzione del display Flipper.
4. I dati vengono trasmessi via UART al Flipper.
5. Il Flipper decomprime e converte in 1-bit (bianco/nero con dithering) per il display.

La latenza dipende dalla risoluzione, dalla qualità JPEG e dalla velocità UART. In modalità "Low Latency" (risoluzione ridotta, JPEG quality bassa, UART a 921600 baud) si ottiene circa 5-10 fps. In modalità alta qualità (risoluzione piena, JPEG quality alta) il frame rate scende a 1-2 fps.

**Procedura step-by-step completa**

1. Hardware: ESP32-CAM con sensore OV2640 o OV3660.
2. Flashare il firmware Camera sull'ESP32-CAM:
   - Collegare un convertitore UART-USB (es. FTDI, CP2102) all'ESP32-CAM.
   - GPIO0 a GND per entrare in boot mode.
   - Flashare il firmware.
   - Rimuovere il collegamento GPIO0-GND.
3. Collegare l'ESP32-CAM al Flipper via GPIO:
   - TX/RX come standard
   - Alimentazione: preferibilmente esterna (powerbank) per stabilità
4. Sul Flipper: Applicazioni > GPIO > Camera.
5. Lo streaming si avvia automaticamente.
6. Controlli disponibili:
   - Scatta foto (salva JPEG sulla SD del Flipper)
   - Regola parametri immagine
   - Cambia risoluzione
   - Attiva/disattiva LED flash
   - Modalità specchio (mirror)

**Parametri configurabili:**

Immagine:
- Risoluzione: QQVGA (160x120), QVGA (320x240), VGA (640x480), SVGA (800x600), XGA (1024x768)
- Qualità JPEG: 10-63 (10 = massima qualità, 63 = massima compressione)
- Luminosità: -2 a +2
- Contrasto: -2 a +2
- Saturazione: -2 a +2
- Gain: auto o manuale (0-30)
- Esposizione: auto (AE) o manuale
- Bilanciamento bianco: auto (AWB) o manuale
- Effetti speciali: nessuno, negativo, scala di grigi, seppia

Streaming:
- Modalità: MJPEG continuo o JPEG singolo (snapshot)
- Baud rate UART: 115200, 230400, 460800, 921600
- Dithering: Floyd-Steinberg, ordinato, o nessuno

**Esempio di uso reale in pentest:**

Ricognizione fisica durante un assessment:
1. Montare l'ESP32-CAM in un contenitore discreto.
2. Collegare al Flipper in tasca.
3. Usare lo streaming per verificare visivamente aree senza esporsi (es. controllare se una sala server è presidiata, leggere badge esposti, verificare la disposizione delle telecamere).
4. Scattare foto di rack, cablaggio, etichette con informazioni sensibili.

### 4.2 Camera Suite

**Cosa fa a livello tecnico**

Camera Suite è un'applicazione avanzata che estende le funzionalità base della Camera con strumenti professionali: time-lapse, visione notturna ottimizzata, filtri anti-rumore, e controllo completo del sensore. Rispetto al tool Camera base, offre un controllo granulare su ogni parametro del sensore OV2640/OV3660.

L'ottimizzazione della visione notturna funziona aumentando il gain del sensore, allungando il tempo di esposizione, e attivando il LED IR integrato nell'ESP32-CAM. Il filtro anti-rumore applica algoritmi di riduzione del rumore digitale (media tra frame successivi) per compensare l'alto gain necessario in condizioni di scarsa luce.

**Procedura step-by-step completa**

1. Flashare il firmware Camera Suite sull'ESP32-CAM.
2. Collegare al Flipper (stesso schema del tool Camera).
3. Sul Flipper: Applicazioni > GPIO > Camera Suite.
4. Menu principale:
   - Live View: streaming in tempo reale con controlli avanzati
   - Time-lapse: cattura automatica a intervalli
   - Night Vision: modalità ottimizzata per scarsa illuminazione
   - Photo: scatto singolo ad alta risoluzione
   - Settings: tutti i parametri del sensore

**Modalità Time-lapse:**
- Impostare intervallo tra scatti (1 secondo - 24 ore)
- Impostare numero totale di scatti o durata totale
- Selezionare risoluzione (maggiore = più dettaglio ma più spazio su SD)
- Avviare la cattura
- Le foto vengono salvate sulla microSD con numerazione progressiva
- Al termine, le foto possono essere assemblate in video su PC

**Modalità Night Vision:**
- Attivazione automatica LED IR (se presente)
- Gain sensore al massimo
- Tempo di esposizione esteso
- Filtro anti-rumore attivo (media mobile su N frame)
- Sharpening post-elaborazione per compensare la sfocatura del gain alto

**Parametri configurabili:**
- Tutti i parametri del tool Camera base
- Intervallo time-lapse (1s - 86400s)
- Numero frame time-lapse
- Intensità LED IR (0-255 PWM)
- Frame averaging (1-8 frame per riduzione rumore)
- Sharpening (off, basso, medio, alto)
- Formato salvataggio (JPEG, BMP)
- Prefisso nome file

**Esempio di uso reale:**

Sorveglianza time-lapse di un'area:
1. Posizionare l'ESP32-CAM con visuale sull'area di interesse.
2. Configurare time-lapse: 1 scatto ogni 30 secondi per 8 ore.
3. Alimentazione da powerbank capiente (10000+ mAh).
4. Al termine, analizzare le 960 foto per ricostruire i movimenti nell'area.

### 4.3 Motion Detection

**Cosa fa a livello tecnico**

Motion Detection utilizza la camera ESP32-CAM per rilevare movimenti nell'inquadratura mediante confronto differenziale tra frame successivi. L'algoritmo funziona cosi':

1. Cattura frame di riferimento (background).
2. Cattura frame corrente.
3. Calcola la differenza pixel per pixel tra i due frame (in scala di grigi).
4. Se la differenza supera una soglia configurabile su un'area sufficientemente ampia, viene dichiarato un "movimento".
5. Viene scattata una foto e generato un evento (notifica sul Flipper, log su SD).
6. Il frame di riferimento viene aggiornato periodicamente per adattarsi ai cambiamenti graduali di illuminazione.

Non è un sistema basato su AI o riconoscimento oggetti -- è puramente basato sulla differenza tra frame. Questo significa che può generare falsi positivi per cambiamenti di illuminazione, ombre, animali, ecc. La sensibilità va calibrata attentamente.

**Procedura step-by-step completa**

1. Flashare il firmware Motion Detection sull'ESP32-CAM.
2. Collegare al Flipper.
3. Sul Flipper: Applicazioni > GPIO > Motion Detection.
4. Posizionare la camera con inquadratura stabile (essenziale per ridurre i falsi positivi -- anche una vibrazione minima causa trigger).
5. Configurare la sensibilità:
   - Soglia di differenza pixel (0-255, default 30)
   - Percentuale minima di pixel cambiati (default 5%)
   - Area di interesse (ROI - Region of Interest) se supportato
6. Avviare il monitoraggio.
7. Il display mostra:
   - Stato: "Monitoring..." o "MOTION DETECTED"
   - Contatore eventi
   - Ultimo evento: timestamp e foto
8. Ogni evento viene loggato con timestamp e foto sulla microSD.

**Parametri configurabili:**
- Soglia di differenza pixel (0-255)
- Percentuale area minima di cambiamento (1-100%)
- Intervallo di aggiornamento background (secondi)
- Cooldown tra eventi (evitare trigger ripetuti per lo stesso movimento)
- Risoluzione di cattura
- Salvataggio: solo log, log + foto, log + foto + notifica
- ROI (Region of Interest): limitare il rilevamento a una zona dell'inquadratura

**Esempio di uso reale in pentest:**

Monitoraggio accesso fisico durante un assessment:
1. Posizionare l'ESP32-CAM con vista sulla porta della sala server.
2. Sensibilità media per evitare falsi positivi ma rilevare persone.
3. Monitorare per l'intera durata del test.
4. Log degli accessi: chi entra, quando, frequenza.
5. Utile per valutare la sicurezza fisica e il controllo accessi.

### 4.4 Nanny Cam

**Cosa fa a livello tecnico**

Nanny Cam trasforma l'ESP32-CAM in un sistema di sorveglianza remota continuo, ottimizzato per il monitoraggio prolungato. A differenza del tool Camera che è progettato per uso interattivo, Nanny Cam è progettato per funzionare in modo autonomo per lunghi periodi con minima interazione.

Il sistema supporta:
- Streaming continuo a basso consumo (risoluzione ridotta, frame rate basso)
- LED IR per visione notturna (se il modulo ESP32-CAM è dotato di LED IR)
- Audio opzionale (richiede microfono I2S collegato all'ESP32)
- Registrazione automatica su microSD del modulo ESP32-CAM
- Rilevamento automatico giorno/notte per switch IR

**Procedura step-by-step completa**

1. Hardware: ESP32-CAM con LED IR (modelli AI-Thinker con IR built-in sono ideali).
2. Flashare il firmware Nanny Cam.
3. Collegare al Flipper.
4. Sul Flipper: Applicazioni > GPIO > Nanny Cam.
5. Configurazione iniziale:
   - Risoluzione: bassa per streaming continuo, alta per registrazione
   - Modalità IR: auto (sensore luce), manuale on, manuale off
   - Registrazione: continua, solo su movimento, programmata
   - Audio: on/off (se hardware supportato)
6. Avviare il monitoraggio.
7. Il Flipper mostra lo streaming live e lo stato del sistema.
8. Le registrazioni vengono salvate sulla microSD dell'ESP32-CAM.

**Parametri configurabili:**
- Risoluzione streaming vs registrazione (possono essere diverse)
- Frame rate (1-25 fps)
- Modalità IR: auto, on, off
- Soglia sensore luce per switch IR automatico
- Registrazione: continua, su movimento, programmata (orari)
- Durata massima file registrazione (segmentazione automatica)
- Compressione JPEG (qualità)
- Audio: on/off, gain microfono

**Esempio di uso reale:**

Monitoraggio durante test di sicurezza fisica:
1. Installare l'ESP32-CAM in posizione discreta con vista sull'area target.
2. Alimentazione da presa elettrica (per funzionamento prolungato).
3. Modalità: registrazione su movimento + IR auto.
4. Dopo 24-48 ore, recuperare la microSD e analizzare le registrazioni.
5. Documentare pattern di accesso, orari, personale.

### 4.5 QR Code

**Cosa fa a livello tecnico**

QR Code utilizza la camera ESP32-CAM per acquisire immagini e decodificare QR code e altri codici bidimensionali. L'ESP32 esegue la decodifica internamente utilizzando una libreria di riconoscimento QR (tipicamente basata su quirc o ZBar portata per ESP-IDF).

Il processo tecnico:
1. Cattura frame dalla camera a risoluzione QVGA o VGA.
2. Conversione in scala di grigi.
3. Rilevamento pattern finder del QR (i tre quadrati negli angoli).
4. Decodifica della matrice di dati.
5. Interpretazione del contenuto in base al tipo: URL, testo, WiFi (SSID+password), vCard, geolocalizzazione, email.
6. Trasmissione del risultato al Flipper via UART.

L'autofocus è digitale (software-based) poichè l'OV2640 ha un obiettivo a fuoco fisso: l'algoritmo varia i parametri di esposizione e contrasto per ottimizzare la leggibilità del QR.

**Procedura step-by-step completa**

1. Collegare ESP32-CAM al Flipper.
2. Sul Flipper: Applicazioni > GPIO > QR Code.
3. Puntare la camera verso il QR code.
4. Mantenere il QR nell'inquadratura a circa 10-20cm di distanza.
5. La decodifica avviene automaticamente quando il QR viene riconosciuto.
6. Il Flipper mostra il contenuto decodificato:
   - URL: mostra l'URL con opzione di apertura (tramite Postman/Web Crawler)
   - WiFi: mostra SSID, password e tipo di autenticazione
   - Testo: mostra il testo completo
   - vCard: mostra il contatto
7. Opzione di salvataggio del contenuto sulla microSD.

**Parametri configurabili:**
- Risoluzione di cattura (più alta = QR più piccoli leggibili)
- Modalità autofocus: continuo o singolo
- LED flash: auto (in condizioni di scarsa luce), on, off
- Formato di salvataggio risultati
- Azione automatica post-decodifica (es. apri URL, connetti WiFi)

**Esempio di uso reale in pentest:**

Analisi di QR code esposti in un ambiente target:
1. QR code sono ovunque: badge, poster, adesivi, schermi.
2. Scansionare tutti i QR visibili nell'area target.
3. Verificare dove puntano: spesso contengono URL interni, credenziali WiFi, link a sistemi interni.
4. Documentare: "QR code nella hall principale contiene credenziali WiFi guest in chiaro".
5. Raccomandazione: non esporre credenziali via QR code in aree accessibili al pubblico.

> Nota personale: i QR code sono una miniera d'oro sottovalutata nel pentest fisico. Ho trovato QR code in sale riunioni che contenevano credenziali WiFi della rete corporate (non guest), link a portali interni con sessioni pre-autenticate, e persino credenziali di sistemi di building automation. Sempre scansionare tutti i QR visibili durante un assessment fisico.

---

## 5. Tool di Rete

### 5.1 FlipWiFi

**Cosa fa a livello tecnico**

FlipWiFi è un gestore WiFi completo che permette al Flipper Zero di connettersi a reti WiFi tramite l'ESP32 e di eseguire operazioni di rete. L'ESP32 funge da modem WiFi, stabilendo la connessione e fornendo al Flipper accesso alla rete attraverso la comunicazione UART.

Funzionalità di rete implementate:
- Scansione AP dettagliata con tutti i parametri (SSID, BSSID, canale, RSSI, crittografia, vendor dal MAC OUI)
- Connessione a reti aperte, WPA2-PSK, WPA3-SAE (se firmware supporta)
- Gestione profili WiFi salvati (SSID + password)
- Test di connettività: ping ICMP, traceroute, DNS resolution
- Informazioni connessione: IP locale, gateway, DNS, subnet mask
- Velocità di connessione e qualità del segnale in tempo reale

**Procedura step-by-step completa**

1. Collegare ESP32 al Flipper via GPIO.
2. Sul Flipper: Applicazioni > GPIO > FlipWiFi.
3. Menu principale:
   - Scan Networks: scansione reti disponibili
   - Saved Networks: connessione rapida a reti salvate
   - Connect: connessione manuale (SSID + password)
   - Tools: ping, traceroute, DNS lookup
   - Status: informazioni connessione attuale
4. Per connettersi:
   - Scan -> selezionare rete -> inserire password -> Connect.
   - Oppure: Saved Networks -> selezionare profilo -> Connect.
5. Una volta connessi, gli altri tool di rete (Postman, Web Crawler, FlipDownloader) possono operare.

**Parametri configurabili:**
- Timeout connessione
- DNS personalizzato (default: 8.8.8.8)
- IP statico vs DHCP
- Profili WiFi salvati (max dipende dalla memoria)
- Intervallo ping per test di connettività
- Numero hop massimo per traceroute

**Esempio di uso reale in pentest:**

Verifica della segmentazione di rete:
1. Connettersi alla rete guest con FlipWiFi.
2. Eseguire ping verso host sulla rete corporate.
3. Se raggiungibili -> segmentazione di rete insufficiente.
4. Traceroute per identificare il percorso e i dispositivi di rete intermedi.
5. DNS lookup per risolvere nomi interni dalla rete guest.

### 5.2 FlipMap

**Cosa fa a livello tecnico**

FlipMap è uno strumento di mappatura delle reti WiFi che si concentra sulla catalogazione dettagliata degli access point rilevati, con informazioni tecniche complete. A differenza di WiFi Mapping (che crea heatmap di copertura), FlipMap crea un catalogo strutturato delle reti con metadati avanzati.

L'ESP32 scansiona le reti e per ogni AP rileva:
- SSID e BSSID (MAC address)
- Canale e larghezza di banda
- RSSI (potenza del segnale)
- Tipo di crittografia e dettagli (WPA2-PSK, WPA2-Enterprise, WPA3, ecc.)
- Vendor dell'AP (dal prefisso MAC OUI)
- Beacon interval
- Supporto 802.11 features (WMM, HT, VHT)
- Numero di client associati (se rilevabile)

**Procedura step-by-step completa**

1. Collegare ESP32 al Flipper.
2. Sul Flipper: Applicazioni > GPIO > FlipMap.
3. Avviare la scansione.
4. I risultati vengono mostrati in lista ordinabile per:
   - RSSI (segnale più forte prima)
   - Canale
   - Crittografia
   - Vendor
5. Per ogni AP, selezionare per vedere i dettagli completi.
6. Esportare la mappa delle reti in formato CSV/JSON.

**Parametri configurabili:**
- Durata scansione per ciclo
- Canali da scansionare
- Ordinamento risultati
- Filtri (per RSSI, crittografia, vendor)
- Formato export
- Aggiornamento continuo o singolo snapshot

**Esempio di uso reale in pentest:**

Inventario wireless di un'organizzazione:
1. Scansione completa con FlipMap da più posizioni nell'edificio.
2. Identificare tutti gli AP: aziendali, guest, rogue (non autorizzati).
3. Verificare la crittografia: AP con WEP o Open sono critici.
4. Identificare AP di vendor diversi da quello aziendale (potenziali rogue AP).
5. Report: inventario completo con raccomandazioni per ogni anomalia trovata.

### 5.3 FlipRPI

**Cosa fa a livello tecnico**

FlipRPI permette il controllo remoto di un Raspberry Pi attraverso la connessione WiFi dell'ESP32. L'ESP32 si connette alla rete locale, stabilisce una connessione con il Raspberry Pi (tipicamente via HTTP API o comandi SSH tunnelizzati) e trasmette i comandi dal Flipper.

L'architettura e':
- Flipper Zero -> UART -> ESP32 -> WiFi -> Rete locale -> Raspberry Pi
- I comandi vengono inviati come richieste HTTP a un server API in esecuzione sul Pi
- Le risposte vengono trasmesse indietro al Flipper per la visualizzazione

Funzionalità principali:
- Invio di comandi preconfigurati (riavvio, spegnimento, update)
- Monitoraggio risorse: CPU, RAM, temperatura, spazio disco
- Esecuzione di script personalizzati
- Lettura file da directory predefinite
- Gestione servizi (start/stop)

**Procedura step-by-step completa**

1. Sul Raspberry Pi:
   - Installare il server API companion (script Python/Node)
   - Configurare l'autenticazione (token API)
   - Avviare il servizio
2. Sull'ESP32:
   - Flashare firmware con supporto FlipRPI
   - Configurare la rete WiFi (SSID + password)
   - Configurare l'IP del Raspberry Pi e il token API
3. Sul Flipper: Applicazioni > GPIO > FlipRPI.
4. Menu principale:
   - Status: mostra CPU/RAM/temp del Pi
   - Commands: lista comandi preconfigurati
   - Custom: invio comando personalizzato
   - Files: browser directory note
   - Services: gestione servizi

**Parametri configurabili:**
- IP/hostname del Raspberry Pi
- Porta del server API
- Token di autenticazione
- Lista comandi preconfigurati
- Directory accessibili per il file browser
- Intervallo di polling per lo status
- Timeout connessione

**Esempio di uso reale in pentest:**

Drop box management:
1. Il Raspberry Pi è configurato come drop box (dispositivo nascosto nella rete target).
2. FlipRPI permette di controllarlo dal Flipper senza laptop.
3. Comandi tipici: avvia scan nmap, controlla risultati, scarica file, riavvia servizi.
4. Utile quando si ha accesso fisico limitato e serve controllare il drop box rapidamente.

### 5.4 Postman

**Cosa fa a livello tecnico**

Postman è un client HTTP/HTTPS integrato che permette di inviare richieste API direttamente dal Flipper tramite l'ESP32. L'ESP32 gestisce la connessione WiFi, il TCP/IP stack, il TLS handshake (per HTTPS) e l'invio/ricezione delle richieste HTTP. I risultati vengono trasmessi al Flipper via UART.

Metodi HTTP supportati:
- GET: richiesta di risorse
- POST: invio dati (body JSON, form-encoded)
- PUT: aggiornamento risorse
- DELETE: eliminazione risorse

La limitazione principale è la memoria dell'ESP32: risposte molto grandi (> 50-100KB) possono causare problemi. Le risposte vengono troncate se eccedono la capacità.

**Procedura step-by-step completa**

1. Connettere l'ESP32 a una rete WiFi (tramite FlipWiFi o configurazione firmware).
2. Sul Flipper: Applicazioni > GPIO > Postman.
3. Configurare la richiesta:
   - Metodo: GET, POST, PUT, DELETE
   - URL: endpoint completo (http:// o https://)
   - Headers: chiave-valore (es. Authorization: Bearer token)
   - Body: testo JSON o form-encoded (per POST/PUT)
4. Inviare la richiesta.
5. Visualizzare la risposta:
   - Status code (200, 404, 500, ecc.)
   - Headers di risposta
   - Body (JSON parsed o testo raw)
6. Salvare la richiesta per uso futuro.
7. Salvare la risposta sulla microSD.

**Parametri configurabili:**
- Metodo HTTP
- URL
- Headers (multipli)
- Body (JSON, form-encoded, raw text)
- Timeout richiesta (secondi)
- Follow redirect (on/off)
- Verifica certificato SSL (on/off -- disabilitare per self-signed)
- Richieste salvate (libreria)

**Esempio di uso reale in pentest:**

Test di API esposte:
1. Durante un assessment, si scopre un endpoint API esposto.
2. Con Postman, testare rapidamente l'endpoint senza laptop.
3. GET /api/users -> verifica se ritorna dati senza autenticazione.
4. POST /api/login con credenziali di test.
5. PUT /api/users/1 -> tentativo di modifica dati senza autorizzazione.
6. Documentare le risposte per il report.

> Nota personale: Postman sul Flipper è limitato ma sorprendentemente utile per test rapidi. Lo uso quando non posso tirare fuori il laptop -- ad esempio durante walkthrough fisici quando trovo un pannello di amministrazione web e voglio fare un test veloce. La limitazione principale è l'input: scrivere URL e JSON sulla tastiera virtuale del Flipper è tedioso. Prepara le richieste come template salvati prima dell'assessment.

### 5.5 Web Crawler

**Cosa fa a livello tecnico**

Web Crawler è un mini spider web che scarica pagine HTML e ne estrae informazioni. L'ESP32 effettua richieste HTTP/HTTPS, scarica il contenuto HTML, esegue un parsing base per estrarre link, testo, metadati, e opzionalmente segue i link trovati fino a una profondità configurabile.

Il processo tecnico:
1. Richiesta HTTP GET alla URL iniziale.
2. Download del contenuto HTML (troncato se supera il limite di memoria).
3. Parsing HTML: estrazione tag `<a href>`, `<meta>`, `<title>`, `<img>`, testo visibile.
4. Se configurato per il follow dei link: aggiunta degli URL trovati alla coda.
5. Ripetizione del processo per ogni URL nella coda (fino al limite di profondità).
6. Raccolta dei risultati: lista URL, testi estratti, metadati.
7. Trasmissione risultati al Flipper e/o salvataggio su microSD.

Le limitazioni sono significative: nessun supporto JavaScript (quindi niente SPA), memoria limitata (pagine grandi vengono troncate), nessun supporto cookie/sessioni avanzate, velocità limitata dalla connessione UART.

**Procedura step-by-step completa**

1. Connettere l'ESP32 a una rete WiFi.
2. Sul Flipper: Applicazioni > GPIO > Web Crawler.
3. Inserire l'URL di partenza.
4. Configurare:
   - Profondità di crawling (0 = solo la pagina, 1 = pagina + link diretti, ecc.)
   - Limite di pagine da scaricare
   - Filtro URL (restare nello stesso dominio, o seguire link esterni)
   - Contenuto da estrarre (testo, link, meta, tutto)
5. Avviare il crawling.
6. Il display mostra il progresso: pagine scaricate, link trovati, errori.
7. Al termine, visualizzare i risultati o esportare su SD.

**Parametri configurabili:**
- URL di partenza
- Profondità di crawling (0-5, oltre diventa troppo lento/pesante)
- Numero massimo di pagine
- Filtro dominio (same-domain, any)
- Tipo di contenuto da estrarre
- Timeout per pagina
- User-Agent personalizzato
- Follow redirect

**Esempio di uso reale in pentest:**

Ricognizione di applicazioni web interne:
1. Connettere l'ESP32 alla rete target.
2. Crawlare il sito intranet aziendale.
3. Estrarre: struttura delle pagine, link a sistemi interni, metadati (versioni software, commenti HTML).
4. Identificare pagine di login, pannelli di amministrazione, file esposti.
5. I risultati alimentano la fase di enumerazione più dettagliata.

### 5.6 FlipDownloader

**Cosa fa a livello tecnico**

FlipDownloader è un download manager che utilizza l'ESP32 per scaricare file da Internet e salvarli sulla microSD del Flipper. L'ESP32 gestisce la connessione HTTP/HTTPS, il download del file e la trasmissione al Flipper via UART per il salvataggio su SD.

Funzionalità tecniche:
- Download HTTP e HTTPS
- Supporto redirect (follow 301/302)
- Ripristino del download interrotto (resume, se il server supporta Range header)
- Verifica hash del file scaricato (MD5, SHA256)
- Progress bar con velocità e tempo stimato
- Browser di file remoti (directory listing HTTP)

La velocità massima di download è limitata dalla UART (a 921600 baud, circa 90KB/s teorici) e dalla memoria dell'ESP32 (buffer di download limitato).

**Procedura step-by-step completa**

1. Connettere l'ESP32 a una rete WiFi.
2. Sul Flipper: Applicazioni > GPIO > FlipDownloader.
3. Opzioni:
   - Download URL: inserire URL diretto del file
   - Browse: navigare directory listing HTTP (se disponibile)
   - Resume: riprendere download interrotto
4. Per il download:
   - Inserire l'URL del file.
   - Selezionare la cartella di destinazione sulla microSD.
   - Opzionale: inserire hash atteso per verifica.
   - Avviare il download.
5. Progress bar mostra: percentuale, velocità, tempo rimanente.
6. Al termine, verifica hash (se configurato) e notifica.

**Parametri configurabili:**
- URL di download
- Cartella destinazione su SD
- Hash atteso (MD5/SHA256) per verifica integrità
- Timeout connessione
- Numero tentativi in caso di errore
- Verifica certificato SSL

**Esempio di uso reale in pentest:**

Aggiornamento tool sul campo:
1. Durante un assessment prolungato, serve un firmware aggiornato per l'ESP32 o un nuovo file per Evil Portal.
2. Connettere l'ESP32 a una rete disponibile (hotspot telefono).
3. Scaricare il file direttamente sulla SD del Flipper.
4. Flashare il nuovo firmware o caricare il nuovo file senza tornare al PC.

---

## 6. Tool BLE

### 6.1 BLE Killer

**Cosa fa a livello tecnico**

BLE Killer è una suite di auditing per dispositivi Bluetooth Low Energy. L'ESP32 opera come scanner BLE e analizzatore di protocollo, permettendo di scoprire dispositivi, enumerare servizi e caratteristiche, e testare la sicurezza delle connessioni BLE nell'area.

A livello tecnico, il BLE opera su tre layer:
- GAP (Generic Access Profile): gestisce discovery e connessione. BLE Killer scansiona gli advertising packet per rilevare dispositivi.
- GATT (Generic Attribute Profile): definisce la struttura dei servizi esposti. BLE Killer enumera servizi, caratteristiche e descriptor.
- L2CAP (Logical Link Control and Adaptation Protocol): gestisce il trasporto dati. BLE Killer può testare la robustezza del layer L2CAP.

Gli advertising packet BLE contengono informazioni preziose:
- MAC address del dispositivo (spesso randomizzato ma non sempre)
- Nome del dispositivo (se broadcast)
- UUID dei servizi esposti
- Dati manufacturer-specific (contengono spesso informazioni sensibili)
- TX power level (per stima distanza)
- Flag di connettibilità

**Procedura step-by-step completa**

1. Flashare il firmware con supporto BLE Killer sull'ESP32-WROOM (necessario modulo con Bluetooth, non funziona su ESP32-S2).
2. Collegare l'ESP32 al Flipper via GPIO.
3. Sul Flipper: Applicazioni > GPIO > BLE Killer.
4. Menu principale:
   - Scan: scansione dispositivi BLE
   - Inspect: dettagli di un dispositivo selezionato
   - Services: enumerazione servizi GATT
   - Monitor: monitoraggio advertising continuo
   - Attack: test di sicurezza BLE

**Modalità Scan:**
- Scansione passiva: solo ascolto advertising (nessuna trasmissione)
- Scansione attiva: invio scan request per ottenere scan response con dati aggiuntivi
- Per ogni dispositivo:
  - MAC address (public o random)
  - Nome (se disponibile)
  - RSSI (potenza segnale)
  - Tipo di advertising (connectable, non-connectable, scannable)
  - Manufacturer data

**Modalità Inspect (post-connessione):**
- Connessione al dispositivo selezionato
- Enumerazione di tutti i servizi GATT:
  - UUID del servizio (standard o custom)
  - Caratteristiche: UUID, proprietà (read, write, notify, indicate), valore
  - Descriptor: UUID, valore
- Lettura valori delle caratteristiche leggibili
- Identificazione servizi noti: Battery Service, Device Information, Heart Rate, ecc.

**Modalità Monitor:**
- Monitoraggio continuo degli advertising packet
- Tracking dei dispositivi: apparizione, scomparsa, variazione RSSI
- Utile per contare persone/dispositivi in un'area nel tempo

**Modalità Attack (test di sicurezza):**
- Spoofing MAC: tentativo di clonare il MAC address di un dispositivo BLE
- Advertising flood: invio massivo di advertising packet per saturare gli scanner
- Monitoraggio pacchetti pubblicitari per analisi dei dati esposti

**Parametri configurabili:**
- Tipo di scansione (passiva/attiva)
- Durata scansione
- Filtro per RSSI minimo
- Filtro per nome dispositivo (regex)
- Filtro per UUID servizio
- Timeout connessione
- Formato export risultati

**Esempio di uso reale in pentest:**

Auditing dispositivi IoT BLE:
1. Scan BLE nell'area target: identificare tutti i dispositivi.
2. Filtrare per dispositivi connectable.
3. Per ogni dispositivo di interesse, eseguire Inspect:
   - Verificare se i servizi espongono dati sensibili senza autenticazione.
   - Verificare se le caratteristiche writable permettono modifiche non autorizzate.
   - Verificare la presenza di servizi custom non documentati.
4. Comune trovare: serrature smart con pin leggibile, sensori medici con dati paziente esposti, beacon con configurazione modificabile.
5. Documentare ogni vulnerabilità nel report con l'UUID del servizio e il valore esposto.

> Nota personale: il BLE è il protocollo più trascurato in ambito sicurezza IoT. La maggior parte dei dispositivi BLE consumer non implementa alcuna autenticazione a livello GATT -- chiunque può connettersi e leggere/scrivere. Ho trovato serrature smart configurabili via BLE senza PIN, termostati con scheduling modificabile, e fitness tracker che espongono dati biometrici. BLE Killer è essenziale per il pentest IoT.

---

## 7. Tool Vari

### 7.1 ESP Flasher

**Cosa fa a livello tecnico**

ESP Flasher permette di flashare firmware sugli ESP32 collegati direttamente dal Flipper Zero, senza necessità di un PC. Il Flipper comunica con il bootloader dell'ESP32 via UART, inviando i dati del firmware precedentemente copiato sulla microSD.

Il processo tecnico è identico a esptool ma implementato nel firmware del Flipper:
1. Reset dell'ESP32 in boot mode (GPIO0 basso durante il reset).
2. Sincronizzazione con il bootloader ESP32 via UART.
3. Identificazione del chip (ESP32, ESP32-S2, ESP32-S3).
4. Opzionale: erase della flash.
5. Scrittura del firmware agli offset specificati.
6. Verifica del checksum.
7. Reset dell'ESP32 per avvio normale.

**Procedura step-by-step completa**

1. Copiare i file firmware (.bin) sulla microSD del Flipper:
   - `SD:/apps_data/esp_flasher/` o directory dedicata
   - Servono tipicamente: bootloader.bin, partitions.bin, firmware.bin
2. Collegare l'ESP32 al Flipper con i pin di flash:
   - TX, RX, GND, 3.3V (standard)
   - GPIO0 per boot mode
   - EN per reset
3. Sul Flipper: Applicazioni > GPIO > ESP Flasher.
4. Configurare:
   - Tipo chip: ESP32, ESP32-S2, ESP32-S3
   - Baud rate: 115200, 230400, 460800, 921600
   - File firmware e offset
5. Mettere l'ESP32 in boot mode (se non automatico).
6. Avviare il flash.
7. Attendere il completamento (progress bar).
8. Verifica checksum automatica.
9. Reset automatico dell'ESP32.

**Parametri configurabili:**
- Tipo chip target
- Baud rate di flash
- File firmware (multipli con offset)
- Erase flash prima del flash (si/no)
- Flash mode: DIO, QIO, DOUT, QOUT
- Flash frequency: 40MHz, 80MHz
- Flash size: 2MB, 4MB, 8MB, 16MB
- Verifica post-flash (si/no)

**Esempio di uso reale:**

Cambio rapido firmware sul campo:
1. Durante un assessment, serve passare da Marauder a Evil Portal sull'ESP32.
2. I firmware sono già sulla microSD.
3. Con ESP Flasher, flashare il nuovo firmware in 2-3 minuti senza PC.
4. Ricollegare l'ESP32 e avviare il tool desiderato.

> Nota personale: ESP Flasher è lento rispetto al flash da PC (la UART del Flipper non è velocissima) ma è salvavita quando sei sul campo senza laptop. Tieni sempre sulla SD i firmware principali (Marauder, Evil Portal, Camera) pronti per il flash. Il flash completo impiega circa 3-5 minuti a 115200 baud, 1-2 minuti a 921600 se il collegamento è stabile.

### 7.2 FlipLibrary

**Cosa fa a livello tecnico**

FlipLibrary è un client per repository remoti di risorse, script e moduli per il Flipper Zero. Attraverso l'ESP32 connesso a Internet, permette di navigare un catalogo online, scaricare nuovi tool, aggiornamenti firmware e risorse direttamente sul Flipper.

Il sistema funziona come un package manager semplificato:
1. L'ESP32 si connette al server del repository via HTTPS.
2. Scarica l'indice delle risorse disponibili (JSON con metadati).
3. L'utente naviga il catalogo sul display del Flipper.
4. Seleziona la risorsa da scaricare.
5. L'ESP32 scarica il file e lo trasmette al Flipper per il salvataggio su SD.

**Procedura step-by-step completa**

1. Connettere l'ESP32 a una rete WiFi.
2. Sul Flipper: Applicazioni > GPIO > FlipLibrary.
3. Il catalogo viene scaricato automaticamente.
4. Navigare per categorie:
   - Firmware ESP32
   - Script
   - Risorse (pagine HTML per Evil Portal, wordlist, ecc.)
   - Tool aggiuntivi
5. Selezionare la risorsa desiderata.
6. Visualizzare descrizione, dimensione, versione.
7. Scaricare -> il file viene salvato sulla microSD nella directory appropriata.
8. Installazione automatica se supportata.

**Parametri configurabili:**
- URL del repository (default o custom)
- Directory di download
- Aggiornamento automatico catalogo (si/no)
- Filtri per categoria, tag, data

### 7.3 FlipSocial

**Cosa fa a livello tecnico**

FlipSocial è un'interfaccia per reti social che utilizza l'ESP32 per comunicare con API di piattaforme social tramite un proxy/server intermedio. Il Flipper non comunica direttamente con le API delle piattaforme (che richiederebbero OAuth complesso) ma con un server bridge che gestisce l'autenticazione.

L'architettura:
- Flipper -> UART -> ESP32 -> WiFi -> Server proxy -> API social platform
- Il server proxy gestisce i token OAuth e le sessioni
- Il Flipper invia/riceve solo messaggi semplificati

**Procedura step-by-step completa**

1. Configurare il server proxy (se self-hosted) o registrarsi al servizio.
2. Ottenere il token API.
3. Configurare l'ESP32 con SSID WiFi e token API.
4. Sul Flipper: Applicazioni > GPIO > FlipSocial.
5. Funzionalità:
   - Visualizzare notifiche/feed
   - Inviare messaggi brevi
   - Leggere messaggi ricevuti
6. L'interazione è limitata dal display e dall'input del Flipper.

**Parametri configurabili:**
- Token API
- Piattaforma social target
- Frequenza aggiornamento feed
- Numero messaggi da visualizzare
- Lunghezza massima messaggio

### 7.4 FlipTrader

**Cosa fa a livello tecnico**

FlipTrader accede a dati di mercato crypto e finanziari tramite API pubbliche. L'ESP32 effettua richieste HTTP periodiche alle API (es. CoinGecko, CoinMarketCap, Yahoo Finance) e trasmette i dati al Flipper per la visualizzazione.

**Procedura step-by-step completa**

1. Connettere l'ESP32 a una rete WiFi.
2. Sul Flipper: Applicazioni > GPIO > FlipTrader.
3. Configurare:
   - Ticker da monitorare (es. BTC, ETH, SOL)
   - Valuta di riferimento (USD, EUR)
   - Intervallo di aggiornamento
   - Alert di prezzo (target alto/basso)
4. Il display mostra:
   - Prezzo attuale
   - Variazione 24h (percentuale)
   - Volume
   - Grafico semplificato (sparkline)
5. Alert sonoro/vibrazione al raggiungimento del target price.

**Parametri configurabili:**
- Lista ticker monitorati
- Valuta di riferimento
- Intervallo aggiornamento (secondi)
- Target price alto e basso per alert
- API key (se richiesta dalla fonte dati)
- Fonte dati (CoinGecko, CMC, custom)

### 7.5 FlipWeather

**Cosa fa a livello tecnico**

FlipWeather recupera dati meteorologici da API online (tipicamente OpenWeatherMap) e li visualizza sul Flipper. L'ESP32 effettua richieste HTTP all'API meteo, parsa la risposta JSON e trasmette i dati formattati al Flipper.

**Procedura step-by-step completa**

1. Ottenere una API key gratuita da OpenWeatherMap (o servizio simile).
2. Configurare l'ESP32 con SSID WiFi e API key.
3. Sul Flipper: Applicazioni > GPIO > FlipWeather.
4. Configurare la città (nome o coordinate GPS).
5. Il display mostra:
   - Temperatura attuale
   - Condizioni (sereno, nuvoloso, pioggia, ecc.)
   - Umidità
   - Velocità e direzione vento
   - Pressione atmosferica
   - Previsioni 1-3 giorni
6. Alert per condizioni critiche (temporali, temperature estreme).

**Parametri configurabili:**
- API key
- Città o coordinate
- Unità di misura (Celsius/Fahrenheit, km/h o mph)
- Intervallo aggiornamento
- Lingua delle descrizioni
- Alert condizioni critiche

### 7.6 FlipWorld

**Cosa fa a livello tecnico**

FlipWorld fornisce informazioni globali e geolocalizzate tramite varie API. L'ESP32 interroga servizi online per ottenere dati su paesi, valute, fusi orari, e geolocalizzazione IP.

**Procedura step-by-step completa**

1. Connettere l'ESP32 a una rete WiFi.
2. Sul Flipper: Applicazioni > GPIO > FlipWorld.
3. Funzionalità:
   - Country Info: inserire nome paese -> dati completi (capitale, popolazione, lingua, valuta, fuso orario, codice telefonico)
   - IP Geolocation: risolvere IP -> posizione geografica, ISP, ASN
   - Currency Converter: conversione valutaria in tempo reale
   - Timezone: fuso orario corrente per qualsiasi città
4. I risultati vengono mostrati sul display e salvabili su SD.

**Parametri configurabili:**
- Lingua delle informazioni
- Formato data/ora
- Valuta base per conversioni
- Fonte dati per geolocalizzazione IP

**Esempio di uso reale in pentest:**

IP geolocation durante reconnaissance:
1. Ottenere una lista di IP del target (da DNS, scan, ecc.).
2. Con FlipWorld, geolocalizzare gli IP per identificare: datacenter, CDN, posizioni uffici.
3. Utile per capire l'infrastruttura geografica del target senza laptop.

### 7.7 Gemini IA

**Cosa fa a livello tecnico**

Gemini IA è un'interfaccia al modello di intelligenza artificiale Google Gemini tramite l'ESP32. L'ESP32 invia richieste HTTP all'API di Google Gemini con il prompt dell'utente e riceve la risposta testuale, che viene trasmessa al Flipper per la visualizzazione.

Il flusso tecnico:
1. L'utente scrive un prompt sul Flipper (tastiera virtuale).
2. Il prompt viene trasmesso via UART all'ESP32.
3. L'ESP32 costruisce la richiesta HTTP POST all'API Gemini con il prompt e il token API.
4. L'API risponde con il testo generato (JSON).
5. L'ESP32 parsa la risposta e la trasmette al Flipper.
6. Il Flipper visualizza la risposta (scrollabile se lunga).

**Procedura step-by-step completa**

1. Ottenere una API key per Google Gemini.
2. Configurare l'ESP32 con SSID WiFi e API key Gemini.
3. Sul Flipper: Applicazioni > GPIO > Gemini IA.
4. Scrivere il prompt.
5. Inviare -> attendere la risposta (pochi secondi).
6. Leggere la risposta sul display.
7. Possibilità di continuare la conversazione (la cronologia viene mantenuta).

**Parametri configurabili:**
- API key Google Gemini
- Modello (gemini-pro, gemini-pro-vision se supportato)
- Temperatura (0-1, controlla la creatività della risposta)
- Max tokens di risposta
- Modalità conversazione (singola domanda o chat)
- System prompt personalizzato

**Esempio di uso reale in pentest:**

Assistente rapido durante un assessment:
1. Domande veloci: "Qual è la porta di default per il servizio X?"
2. Generazione payload: "Genera un payload XSS per un campo input"
3. Analisi rapida: "Spiega cosa fa questo script Base64: [incolla]"
4. Limitazione: la tastiera del Flipper rende l'input lento, utile solo per domande brevi.

### 7.8 Gravity

**Cosa fa a livello tecnico**

Gravity è un tool per la lettura e visualizzazione di dati da sensori fisici collegati all'ESP32 via I2C o SPI. Supporta accelerometri, giroscopi, magnetometri, sensori di temperatura/umidità/pressione, e altri sensori compatibili.

L'ESP32 legge i dati dai sensori collegati ai pin I2C (SDA/SCL) o SPI, li elabora e li trasmette al Flipper per la visualizzazione sotto forma di grafici in tempo reale e valori numerici.

Sensori supportati tipici:
- IMU (Inertial Measurement Unit): MPU6050, MPU9250, LSM6DS3
- Barometro: BMP280, BME280
- Magnetometro: HMC5883L, QMC5883L
- Temperatura/Umidità: DHT22, SHT31, BME280

**Procedura step-by-step completa**

1. Collegare il sensore all'ESP32:
   - I2C: SDA -> GPIO21, SCL -> GPIO22 (default ESP32)
   - Alimentazione: 3.3V, GND
2. Flashare il firmware Gravity sull'ESP32.
3. Collegare l'ESP32 al Flipper via GPIO.
4. Sul Flipper: Applicazioni > GPIO > Gravity.
5. Il tool rileva automaticamente i sensori collegati.
6. Selezionare il sensore da visualizzare.
7. Il display mostra:
   - Valori numerici in tempo reale
   - Grafico temporale (asse X = tempo, asse Y = valore)
   - Unità di misura appropriate
8. Logging su SD per analisi successiva.

**Parametri configurabili:**
- Sensore attivo
- Frequenza di campionamento (Hz)
- Scala asse grafico (auto o manuale)
- Durata finestra grafico
- Formato logging
- Unità di misura
- Calibrazione sensore

### 7.9 Morse Flash

**Cosa fa a livello tecnico**

Morse Flash utilizza il LED ad alta potenza dell'ESP32-CAM come trasmettitore di codice Morse ottico. Il Flipper converte il testo in codice Morse (punti e linee) e controlla il LED dell'ESP32-CAM per trasmetterlo visivamente.

La codifica segue lo standard internazionale:
- Punto (dit): LED acceso per 1 unità di tempo
- Linea (dah): LED acceso per 3 unità di tempo
- Pausa tra elementi dello stesso carattere: 1 unità
- Pausa tra caratteri: 3 unità
- Pausa tra parole: 7 unità

La durata dell'unità di tempo dipende dalla velocità in WPM (Words Per Minute). La parola di riferimento è "PARIS" (50 unità): a 20 WPM, un'unità dura 60ms.

**Procedura step-by-step completa**

1. Collegare ESP32-CAM al Flipper.
2. Sul Flipper: Applicazioni > GPIO > Morse Flash.
3. Inserire il testo da trasmettere.
4. Configurare:
   - Velocità (WPM)
   - Modalità: singolo o loop
   - Luminosità LED
5. Avviare la trasmissione.
6. Il LED dell'ESP32-CAM trasmette il messaggio in Morse.
7. In modalità loop, il messaggio si ripete indefinitamente.

**Parametri configurabili:**
- Velocità (WPM: 5-40, default 20)
- Modalità: singolo invio, loop continuo, burst (N ripetizioni)
- Luminosità LED (0-255 PWM)
- Messaggi predefiniti salvati
- Codifica: internazionale, estensioni per caratteri speciali

**Esempio di uso reale:**

Comunicazione ottica a lunga distanza:
1. Il LED flash dell'ESP32-CAM è molto potente (tipicamente 600-700mA).
2. In condizioni di buio, il segnale Morse è visibile a centinaia di metri.
3. Utile per comunicazione semplice quando radio e cellulare non sono opzioni.
4. Applicazione in CTF o esercitazioni: trasmissione di flag/codici via Morse.

---

