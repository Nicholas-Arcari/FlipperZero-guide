## 3. Tool WiFi Offensivi

### 3.1 Marauder

**Cosa fa a livello tecnico**

ESP32 Marauder è una suite completa di attacchi e analisi WiFi 802.11 che sfrutta le capacità dell'ESP32 di operare in modalità promiscua e di iniettare frame 802.11 raw. Il firmware trasforma l'ESP32 in un analizzatore di rete e strumento offensivo controllato interamente dal Flipper Zero.

A livello di protocollo, Marauder opera manipolando i frame di gestione WiFi (management frames) che, nello standard 802.11, non sono autenticati nè cifrati (a meno che non sia attivo 802.11w/PMF). Questo permette di:

- Inviare frame di deautenticazione (tipo 0xC0) spoofando il BSSID dell'access point, causando la disconnessione dei client.
- Generare beacon frame (tipo 0x80) con SSID arbitrari, creando reti fantasma visibili dai dispositivi nelle vicinanze.
- Catturare probe request (tipo 0x40) per identificare i dispositivi nelle vicinanze e le reti che cercano.
- Monitorare tutto il traffico WiFi in modalità promiscua per analisi passiva.

**Procedura step-by-step completa**

1. Flashare il firmware Marauder sull'ESP32 (vedi sezione 2).
2. Collegare l'ESP32 al Flipper via GPIO (TX, RX, 3.3V, GND).
3. Sul Flipper: Applicazioni > GPIO > [ESP32] WiFi Marauder.
4. Il Flipper stabilisce la connessione UART con l'ESP32.
5. Si apre il menu principale con le opzioni disponibili.

**Comandi e funzionalità principali:**

`Scan WiFi (APs)` - Avvia una scansione attiva degli access point sui 14 canali della banda 2.4GHz. Per ogni AP rilevato mostra: SSID, BSSID (MAC), canale, RSSI (potenza segnale in dBm), tipo di crittografia (Open/WEP/WPA/WPA2/WPA3), e numero di client associati. La scansione cicla tra i canali con un dwell time configurabile.

`Scan WiFi (Stations)` - Scansione dei dispositivi client (stazioni) nell'area. Cattura i probe request inviati dai dispositivi per rivelare: MAC address del client, SSID delle reti cercate (probe request), potenza del segnale. Utile per il fingerprinting dei dispositivi.

`Deauth` - Attacco di deautenticazione. Invia frame deauth spoofati dall'AP verso i client connessi, causando la disconnessione. Parametri:
- Target: singolo AP, tutti gli AP rilevati, o specifico client
- Durata: continuo o burst limitato
- Reason code: codice di deautenticazione (default 7 = "Class 3 frame received from non-associated station")
- Channel: canale su cui operare

`Beacon Spam` - Genera centinaia di beacon frame con SSID casuali o da lista predefinita, inondando la lista reti WiFi dei dispositivi vicini. Modalità:
- Random: SSID generati casualmente
- List: SSID da file sulla SD del Flipper
- Rickroll: classica lista di SSID che formano il testo di "Never Gonna Give You Up"
- Target: clona i beacon di un AP specifico con variazioni

`Probe Flood` - Invia probe request massivi su tutti i canali, simulando centinaia di dispositivi che cercano reti. Utile per stressare AP e IDS.

`PMKID Capture` - Tenta la cattura del PMKID (Pairwise Master Key Identifier) dagli AP WPA2. Il PMKID è contenuto nel primo messaggio dell'handshake EAPOL e può essere crackato offline senza necessità di catturare l'handshake completo a 4 vie. I PMKID catturati vengono salvati in formato hashcat sulla SD.

`Packet Monitor` - Visualizza in tempo reale il traffico WiFi sul canale selezionato con grafico della densità dei pacchetti. Utile per identificare canali congestionati e attività anomale.

`Channel Hop` - Scansione continua ciclando tra i canali con visualizzazione dell'attività per canale. Il dwell time (tempo su ogni canale) è configurabile.

**Parametri configurabili:**
- Canale di operazione: 1-14 (o auto-hop)
- Potenza TX: configurabile nei limiti dell'hardware ESP32
- Filtri MAC: whitelist/blacklist per target specifici
- Dwell time per channel hopping
- Formato log: PCAP, CSV, raw
- Interfaccia: verbose o minimalista

**Esempio di uso reale in pentest:**

Durante un assessment wireless autorizzato, la procedura tipica e':
1. Scan AP per mappare tutte le reti nell'ambito del test.
2. Scan Stations per identificare i client connessi.
3. Deauth mirato su un client specifico per forzare la riassociazione.
4. Cattura PMKID durante la riassociazione.
5. Export dei file sulla SD per cracking offline con hashcat (`hashcat -m 22000`).

> Nota personale: Marauder è lo strumento che uso di più in assoluto con l'ESP32. Per il pentest wireless è fondamentale come strumento di ricognizione rapida -- lo scan AP+Stations in 30 secondi ti da un quadro completo della superficie wireless del target. Il deauth lo uso solo quando ho autorizzazione scritta esplicita, e comunque in modo mirato (singolo client) per minimizzare l'impatto. Il beacon spam invece è utile solo per dimostrazioni al cliente -- non ha valore offensivo reale ma fa capire la vulnerabilità dei management frame non protetti.

### 3.2 Evil Portal

**Cosa fa a livello tecnico**

Evil Portal trasforma l'ESP32 in un access point WiFi con captive portal integrato. Tecnicamente, l'ESP32 avvia un soft-AP (software access point) e un server DNS che risolve qualsiasi dominio verso l'IP locale dell'ESP32. Quando un dispositivo si connette all'AP e tenta di navigare, il DNS spoofing interno redirige tutte le richieste HTTP verso una pagina HTML ospitata sull'ESP32.

Questa tecnica sfrutta il meccanismo di captive portal detection presente in tutti i sistemi operativi moderni: quando un dispositivo si connette a una rete WiFi, invia una richiesta HTTP a un URL noto (es. `captive.apple.com` per iOS, `connectivitycheck.gstatic.com` per Android). Se la risposta non corrisponde a quella attesa, il sistema apre automaticamente il browser del captive portal, mostrando la pagina dell'attaccante.

La pagina può essere personalizzata per simulare qualsiasi login: portale hotel, rete aziendale, social login, aggiornamento firmware, o qualsiasi altra interfaccia che induca la vittima a inserire credenziali.

**Procedura step-by-step completa**

1. Flashare il firmware Evil Portal sull'ESP32.
2. Preparare la pagina HTML del portal:
   - Creare un file HTML con il form di login desiderato.
   - Il form deve inviare i dati via POST alla root (`/`).
   - Copiare il file HTML sulla microSD del Flipper in `SD:/apps_data/evil_portal/`.
3. Collegare l'ESP32 al Flipper via GPIO.
4. Sul Flipper: Applicazioni > GPIO > Evil Portal.
5. Configurare:
   - SSID dell'AP (es. "Hotel_WiFi_Free", "Corporate_Guest", "Starbucks_WiFi")
   - Canale WiFi (default 1, scegliere un canale libero)
   - Pagina HTML da servire
6. Avviare il portale.
7. Monitorare le connessioni e le credenziali catturate sul display del Flipper.
8. Le credenziali vengono loggate sulla microSD in formato testo.

**Struttura del file HTML di esempio:**

```html
<!DOCTYPE html>
<html>
<head>
    <title>WiFi Login</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { font-family: Arial; text-align: center; padding: 20px; }
        input { width: 80%; padding: 10px; margin: 5px; }
        button { padding: 10px 40px; background: #007bff; color: white; border: none; }
    </style>
</head>
<body>
    <h2>Free WiFi Access</h2>
    <p>Please sign in to continue</p>
    <form method="POST" action="/">
        <input type="email" name="email" placeholder="Email"><br>
        <input type="password" name="password" placeholder="Password"><br>
        <button type="submit">Connect</button>
    </form>
</body>
</html>
```

**Parametri configurabili:**
- SSID dell'access point (fino a 32 caratteri)
- Canale WiFi (1-13)
- Pagina HTML custom (dimensione limitata dalla flash dell'ESP32)
- Comportamento post-login (pagina di successo, redirect)
- Timeout sessione
- Numero massimo di client simultanei
- Nascondere SSID (hidden AP)

**Esempio di uso reale in pentest:**

Scenario: test di consapevolezza dei dipendenti in un'azienda.
1. Creare un portale che simula il login VPN aziendale o il portale WiFi guest.
2. Posizionare l'ESP32+Flipper in un'area comune (mensa, sala riunioni).
3. L'SSID deve essere credibile: "NomeAzienda-Guest" o "NomeAzienda-VPN-Login".
4. Monitorare quanti dipendenti inseriscono credenziali reali.
5. Documentare i risultati per il report -- l'obiettivo è dimostrare la necessità di formazione sulla sicurezza.

> Nota personale: Evil Portal è devastante come strumento di social engineering. La chiave del successo è la credibilità della pagina: dedica tempo a replicare fedelmente il portale reale del target, inclusi loghi, colori e font. Un portale generico "Free WiFi" funziona negli spazi pubblici, ma in ambiente aziendale devi essere specifico. Tieni presente che le credenziali catturate sono in chiaro -- se il target usa 2FA, avrai comunque la password ma non potrai accedere senza il secondo fattore. Nel report, questo dato è comunque critico.

### 3.3 Ghost ESP

**Cosa fa a livello tecnico**

Ghost ESP è un firmware per ESP32 focalizzato sulle operazioni stealth di ricognizione wireless. A differenza di Marauder che opera anche in modo attivo (injection, deauth), Ghost ESP privilegia l'approccio passivo: l'ESP32 opera esclusivamente in modalità promiscua senza trasmettere alcun frame, rendendosi invisibile ai sistemi IDS/IPS wireless (WIDS).

Tecnicamente, l'ESP32 in modalità promiscua riceve tutti i frame WiFi sul canale selezionato senza associarsi a nessuna rete. Non invia probe request, non risponde a probe response, non genera alcun traffico. L'unico segnale emesso è l'eventuale rumore RF del circuito, non distinguibile dal rumore di fondo.

Ghost ESP implementa anche la randomizzazione del MAC address: ad ogni avvio o ad intervalli configurabili, il MAC dell'interfaccia WiFi viene cambiato, impedendo il tracking del dispositivo anche in caso di rilevamento.

**Procedura step-by-step completa**

1. Flashare il firmware Ghost ESP sull'ESP32.
2. Collegare l'ESP32 al Flipper via GPIO.
3. Sul Flipper: Applicazioni > GPIO > Ghost ESP.
4. Selezionare la modalità di scansione:
   - Passive Scan: monitoraggio su canale fisso o con channel hopping
   - Signal Profiling: analisi dettagliata delle caratteristiche RF
   - Device Fingerprint: identificazione dispositivi da pattern di traffico
5. Avviare la scansione.
6. I dati vengono visualizzati in tempo reale e loggati sulla SD.

**Funzionalità dettagliate:**

`Passive WiFi Scan` - Cattura tutti i frame WiFi senza trasmettere. Identifica AP, client, traffico, canali occupati. Nessuna traccia lasciata sulla rete.

`MAC Randomization` - Cambia automaticamente il MAC dell'ESP32 ad intervalli configurabili (default: ogni 60 secondi). Impedisce il fingerprinting del dispositivo di scansione.

`Signal Profiling` - Analisi dettagliata delle caratteristiche RF di ogni sorgente: potenza media, varianza, pattern temporali. Utile per distinguere AP fissi da dispositivi mobili e per stimare la distanza.

`Client Tracking` - Monitora i probe request per tracciare i movimenti dei dispositivi nell'area. Ogni dispositivo che cerca reti WiFi rivela il proprio MAC e la lista delle reti salvate.

`Stealth Channel Hop` - Channel hopping con timing randomizzato per evitare pattern riconoscibili dai WIDS avanzati.

**Parametri configurabili:**
- Canale di ascolto (fisso o hopping)
- Intervallo di randomizzazione MAC
- Filtri per tipo di frame (management, control, data)
- Dwell time per canale (in modalità hopping)
- Formato di export dei log (CSV, JSON)
- Sensibilità minima RSSI (filtrare segnali deboli)

**Esempio di uso reale in pentest:**

Fase di ricognizione di un assessment wireless in ambiente ostile (target con WIDS attivo):
1. Attivare Ghost ESP in modalità passive scan.
2. Posizionarsi nell'area target senza destare sospetti.
3. Raccogliere per 15-30 minuti: lista completa AP, client associati, reti cercate dai dispositivi.
4. Analizzare i probe request per identificare dispositivi di interesse (es. laptop aziendali che cercano la rete corporate).
5. Esportare i dati per la fase di attacco successiva (con Marauder o Evil Portal).

> Nota personale: Ghost ESP è il tool che uso nella fase iniziale di ogni assessment wireless. Prima di fare qualsiasi cosa attiva, passo almeno 20 minuti in modalità passiva per capire l'ambiente. In ambienti con WIDS (Cisco CleanAir, Aruba RFProtect), la scansione attiva viene rilevata immediatamente -- Ghost ESP ti permette di mappare tutto senza alzare allarmi. Il trucco è combinarlo: prima Ghost per la ricognizione, poi Marauder per gli attacchi mirati.

### 3.4 Wardriver

**Cosa fa a livello tecnico**

Wardriver trasforma il Flipper Zero + ESP32 in uno strumento di wardriving classico: scansione continua delle reti WiFi con geolocalizzazione tramite modulo GPS esterno. L'ESP32 gestisce la scansione WiFi mentre un modulo GPS (collegato via UART secondario o integrato) fornisce le coordinate geografiche. I dati vengono correlati e salvati in formato compatibile con WiGLE (Wireless Geographic Logging Engine), il database mondiale delle reti WiFi.

A livello tecnico, l'ESP32 esegue un loop continuo: scan rapido su tutti i canali 2.4GHz, raccolta dei beacon frame con SSID/BSSID/canale/RSSI/crittografia, timestamp e coordinate GPS correnti, scrittura su file CSV sulla microSD.

**Procedura step-by-step completa**

1. Hardware necessario:
   - ESP32-WROOM con firmware Wardriver
   - Modulo GPS (es. NEO-6M, NEO-7M, NEO-8M) collegato all'ESP32
   - Flipper Zero
   - Powerbank per alimentazione durante il movimento
2. Collegamento GPS all'ESP32:
   - GPS TX -> ESP32 GPIO16 (RX2)
   - GPS RX -> ESP32 GPIO17 (TX2)
   - GPS VCC -> 3.3V
   - GPS GND -> GND
3. Collegare ESP32 al Flipper via GPIO standard.
4. Sul Flipper: Applicazioni > GPIO > Wardriver.
5. Attendere il fix GPS (prima acquisizione può richiedere 1-5 minuti all'aperto).
6. Iniziare a muoversi nell'area target.
7. Il display mostra: reti trovate, coordinate attuali, velocità, reti nuove/duplicate.
8. Al termine, fermare la scansione.
9. Esportare il file CSV dalla microSD.

**Formato output WiGLE CSV:**

```
MAC,SSID,AuthMode,FirstSeen,Channel,RSSI,CurrentLatitude,CurrentLongitude,AltitudeMeters,AccuracyMeters,Type
AA:BB:CC:DD:EE:FF,NomeRete,WPA2,2024-01-15 14:30:00,6,-65,45.4642,9.1900,120,5,WIFI
```

**Parametri configurabili:**
- Intervallo di scansione (default: ogni 2 secondi)
- Canali da scansionare (tutti o sottoinsieme)
- Filtro RSSI minimo (es. solo reti sopra -80 dBm)
- Formato output (WiGLE CSV, KML per Google Earth)
- Deduplicazione (filtrare reti già viste)
- Nome file output

**Esempio di uso reale in pentest:**

Assessment della superficie wireless di un campus aziendale:
1. Wardriving perimetrale in auto/a piedi attorno all'edificio.
2. Identificare tutte le reti visibili dall'esterno (potenziale rischio di signal leakage).
3. Mappare la copertura: reti aziendali non dovrebbero essere visibili a 100m dall'edificio.
4. Upload su WiGLE (opzionale) o analisi locale.
5. Includere nel report: mappa delle reti, segnale all'esterno, raccomandazioni sulla potenza TX degli AP.

### 3.5 Free Roam

**Cosa fa a livello tecnico**

Free Roam è uno strumento di esplorazione simultanea WiFi e BLE che opera in modalità continua. L'ESP32 alterna rapidamente tra la scansione WiFi (modalità promiscua) e la scansione BLE (modalità observer), fornendo una visione completa dell'ambiente radio circostante. A differenza degli scanner dedicati, Free Roam non si concentra su un protocollo specifico ma fornisce una panoramica globale.

Tecnicamente, l'ESP32 sfrutta il suo dual-core: un core gestisce la scansione WiFi mentre l'altro gestisce il BLE, permettendo una vera simultaneità senza perdita di pacchetti significativa.

**Procedura step-by-step completa**

1. Flashare il firmware appropriato sull'ESP32 (firmware con supporto Free Roam integrato).
2. Collegare l'ESP32 al Flipper via GPIO.
3. Sul Flipper: Applicazioni > GPIO > Free Roam.
4. Selezionare le modalità attive:
   - Solo WiFi
   - Solo BLE
   - WiFi + BLE simultaneo
5. Avviare il roaming.
6. Il display mostra in tempo reale:
   - Numero di AP WiFi rilevati
   - Numero di dispositivi BLE rilevati
   - Dispositivi mobili (identificati tramite probe request)
   - Grafici di densità del segnale
7. I dati vengono loggati continuamente sulla microSD.
8. Export in CSV/JSON per analisi successiva.

**Parametri configurabili:**
- Protocolli attivi (WiFi, BLE, entrambi)
- Intervallo di aggiornamento display
- Filtro RSSI minimo
- Logging continuo o a intervalli
- Formato export (CSV, JSON)
- Deduplicazione dispositivi

**Esempio di uso reale in pentest:**

Ricognizione iniziale di un ambiente sconosciuto:
1. Attivare Free Roam all'ingresso dell'area target.
2. Camminare nell'area per 10-15 minuti.
3. Ottenere una mappa completa di: reti WiFi, dispositivi BLE (smartwatch, fitness tracker, beacon, IoT), dispositivi mobili.
4. Analizzare i dati per pianificare gli attacchi successivi: quali reti attaccare, quali dispositivi BLE sono interessanti, quanti dispositivi sono presenti nell'area.

### 3.6 WiFi Mapping

**Cosa fa a livello tecnico**

WiFi Mapping crea mappe di copertura del segnale WiFi (heatmap) correlando la potenza del segnale (RSSI) alla posizione fisica. L'ESP32 esegue misurazioni continue dell'RSSI delle reti rilevate mentre l'utente si muove nell'area. I dati vengono poi aggregati per creare una rappresentazione visiva della copertura.

A differenza del Wardriver che usa il GPS per le coordinate, WiFi Mapping è progettato per ambienti interni dove il GPS non funziona: le coordinate sono basate su un sistema relativo (passi, punti di riferimento) o su input manuale dell'utente.

**Procedura step-by-step completa**

1. Collegare l'ESP32 al Flipper via GPIO.
2. Sul Flipper: Applicazioni > GPIO > WiFi Mapping.
3. Selezionare la rete target da mappare (o tutte le reti).
4. Configurare i parametri di mapping:
   - Intervallo di campionamento
   - Area da mappare (griglia virtuale)
   - Punti di riferimento
5. Iniziare il percorso nell'area:
   - Ad ogni punto significativo, confermare la posizione.
   - L'ESP32 campiona il segnale per alcuni secondi.
   - Il valore RSSI medio viene associato alla posizione.
6. Completare il percorso coprendo tutta l'area.
7. Visualizzare la heatmap generata sul display del Flipper.
8. Esportare i dati per elaborazione su PC.

**Parametri configurabili:**
- Rete target (BSSID specifico o tutte)
- Intervallo di campionamento RSSI
- Numero di campioni per punto
- Dimensione della griglia
- Soglie di colore per la heatmap (es. verde > -50dBm, giallo > -70dBm, rosso > -85dBm)
- Formato export

**Esempio di uso reale in pentest:**

Valutazione della copertura wireless in un ufficio:
1. Mappare il segnale della rete aziendale in tutto l'edificio.
2. Identificare zone morte (nessuna copertura) e zone di signal leakage (segnale forte all'esterno).
3. Verificare che le reti sensibili non siano accessibili da aree pubbliche.
4. Includere la heatmap nel report con raccomandazioni di posizionamento AP.

### 3.7 WiFi Marauder

**Cosa fa a livello tecnico**

WiFi Marauder è una versione estesa e potenziata del Marauder classico, sviluppata specificamente per l'integrazione con il Flipper Zero. Rispetto al Marauder base, offre una gestione migliorata dei pacchetti, un'interfaccia utente ottimizzata per il piccolo schermo del Flipper, e funzionalità aggiuntive di logging e automazione.

Le differenze principali rispetto al Marauder standard:
- Gestione ottimizzata della memoria: buffer circolare per i pacchetti catturati, evitando overflow su sessioni lunghe.
- Interfaccia migliorata: menu gerarchici, visualizzazione compatta delle informazioni, grafici in tempo reale.
- Logging potenziato: salvataggio automatico su SD con rotazione file, timestamp precisi, formato compatibile con tool di analisi.
- Automazione: possibilità di creare script di attacco sequenziali (es. scan -> deauth -> capture -> stop).
- Filtri avanzati: whitelist/blacklist per MAC, SSID, canale.

**Procedura step-by-step completa**

1. Flashare il firmware WiFi Marauder (diverso dal Marauder base) sull'ESP32.
2. Collegare l'ESP32 al Flipper via GPIO.
3. Sul Flipper: Applicazioni > GPIO > WiFi Marauder.
4. Menu principale:
   - Scan: scansione AP e stazioni
   - Attack: deauth, beacon spam, probe flood
   - Capture: cattura PMKID, handshake
   - Monitor: packet monitor, channel activity
   - Settings: configurazione parametri
5. Per analisi avanzata:
   - Avviare Scan -> selezionare target dalla lista.
   - Passare ad Attack -> selezionare tipo di attacco.
   - Attivare Capture per logging.
   - Monitorare in Monitor.

**Parametri configurabili aggiuntivi rispetto a Marauder base:**
- Script di automazione (sequenze di comandi)
- Rotazione automatica dei log
- Timeout automatico per attacchi
- Filtri MAC avanzati (regex-like)
- Modalità burst per deauth (intervalli configurabili)
- Formato PCAP per cattura pacchetti (compatibile Wireshark)

**Esempio di uso reale in pentest:**

Assessment wireless automatizzato:
1. Creare uno script: scan 30s -> identifica target -> deauth mirato -> cattura PMKID -> stop.
2. Eseguire lo script per ogni rete nell'ambito del test.
3. Raccogliere tutti i PMKID e handshake in file separati.
4. Analisi offline con hashcat per valutare la robustezza delle password.
5. Report dettagliato con timeline degli attacchi dal log automatico.

### 3.8 Wendigo BT+BLE+WiFi Monitor

**Cosa fa a livello tecnico**

Wendigo è un monitor tri-protocollo che scansiona simultaneamente Bluetooth Classic, Bluetooth Low Energy (BLE) e WiFi. L'ESP32, grazie al suo controller radio combinato WiFi+BT, può operare su tutti e tre i protocolli alternando rapidamente tra le modalità.

A livello tecnico:
- WiFi: scansione in modalità promiscua, cattura beacon/probe/data frame.
- BLE: scansione in modalità observer, cattura advertising packets (ADV_IND, ADV_DIRECT_IND, ADV_NONCONN_IND, ADV_SCAN_IND).
- BT Classic: inquiry scan per dispositivi discoverable, cattura del nome dispositivo e classe (CoD - Class of Device).

La peculiarità di Wendigo è la correlazione tra i protocolli: può identificare dispositivi che utilizzano contemporaneamente WiFi e BLE (es. smartphone, laptop, IoT), creando un profilo completo del dispositivo.

**Procedura step-by-step completa**

1. Flashare il firmware Wendigo sull'ESP32 (richiede ESP32-WROOM per supporto BT Classic).
2. Collegare l'ESP32 al Flipper via GPIO.
3. Sul Flipper: Applicazioni > GPIO > Wendigo.
4. Configurare i protocolli da monitorare:
   - WiFi: on/off, canali, tipo di frame
   - BLE: on/off, filtro per tipo di advertising
   - BT Classic: on/off, timeout inquiry
5. Avviare il monitoraggio.
6. Il display mostra:
   - Lista dispositivi rilevati per protocollo
   - Correlazioni tra protocolli (stesso dispositivo su WiFi+BLE)
   - RSSI per ogni dispositivo
   - Tipo di dispositivo (smartphone, laptop, IoT, wearable)
7. Filtri in tempo reale per tipo di protocollo o potenza segnale.
8. Export del log combinato.

**Parametri configurabili:**
- Protocolli attivi (qualsiasi combinazione dei tre)
- Filtro per tipo di dispositivo (CoD per BT, tipo ADV per BLE)
- Soglia RSSI minima
- Intervallo di aggiornamento
- Correlazione cross-protocol (on/off)
- Formato logging (CSV, JSON, raw)
- Durata sessione (timer automatico)

**Esempio di uso reale in pentest:**

Analisi della superficie radio di un ufficio:
1. Attivare Wendigo con tutti e tre i protocolli.
2. Monitorare per 30-60 minuti durante l'orario lavorativo.
3. Identificare: quanti dispositivi sono presenti, quali protocolli usano, dispositivi IoT non autorizzati (es. telecamere IP personali, smart speaker), dispositivi BLE con advertising esposto.
4. La correlazione cross-protocol permette di associare il MAC WiFi al MAC BLE dello stesso dispositivo -- utile per il tracking.
5. Report: inventario dispositivi radio, dispositivi non autorizzati, raccomandazioni sulla policy BYOD.

> Nota personale: Wendigo è sottovalutato. La maggior parte dei pentester si concentra solo sul WiFi, ma la superficie BLE è enorme e spesso trascurata. Ho trovato dispositivi IoT non autorizzati in uffici "sicuri" semplicemente monitorando il BLE per mezz'ora. Smart speaker, telecamere IP, fitness tracker -- tutti espongono informazioni via BLE advertising che possono essere sfruttate.

---

