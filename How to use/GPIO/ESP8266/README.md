# ESP8266

Moduli WiFi compatti ed economici, ideali per attacchi wireless, automazione e sperimentazione rapida tramite GPIO.

Questi strumenti sfruttano la flessibilità dell’ESP8266 per eseguire funzioni di rete avanzate, generare pacchetti, leggere segnali o integrare servizi web.

### **• Deauther**

Modulo specializzato negli attacchi WiFi deauthentication, sfruttando vulnerabilità del protocollo 802.11.

Permette di disconnettere client da reti wireless non protette da gestione robusta dei pacchetti di management.

Funzionalità ampliate:

- Invia pacchetti di deauth/disassoc verso client o access point specifici.
- Analisi in tempo reale dei dispositivi connessi all’AP.
- Attacco di probe request flooding e beacon spamming.
- Controllo manuale dei canali e potenza di trasmissione (quando supportato dall’hardware).

Esempi pratici:

- Test di sicurezza di reti aziendali.
- Dimostrazione educativa di vulnerabilità WiFi.
- Stress test su dispositivi IoT mal configurati.

### **• Deauther V2**

Evoluzione avanzata del Deauther classico, con maggiore stabilità, UI migliorata e strumenti aggiuntivi.

Funzionalità ampliate:

- Interfaccia web più completa con lista reti, client, e log live.
- Aggiunta di attacchi mirati e di modalità multi-target.
- Supporto migliorato a più board ESP8266 e a configurazioni custom.
- Possibilità di salvare profili e impostazioni.

Esempi pratici:

- Analisi approfondita del traffico management frame.
- Stress test più prolungati su infrastrutture WiFi.
- Utilizzo come strumento didattico con UI intuitiva.

### **• IFTTT Button**

Trasforma il Flipper + ESP8266 in un pulsante smart capace di attivare automazioni online tramite IFTTT Webhooks.

Funzionalità ampliate:

- Esecuzione di script cloud tramite semplici richieste HTTP.
- Supporto GET/POST verso servizi IFTTT o endpoint personalizzati.
- Configurazione facile tramite SSID, chiave webhook e evento.
- Possibilità di integrare sensori o trigger personalizzati.

Esempi pratici:

- Accendere una luce smart.
- Inviare un messaggio Telegram con un clic.
- Registrare eventi su Google Sheet.
- Attivare automazioni domestiche o notifiche push.

### **• WiFi Scanner**

Scanner WiFi avanzato per la rilevazione di reti e parametri tecnici circostanti.

Funzionalità ampliate:

- Scansione continua dei canali 2.4 GHz.
- Identificazione SSID, BSSID, RSSI, tipo di cifratura.
- Raccolta dati per wardriving leggero o mappatura ambientale.
- Modalità di monitoraggio passivo quando supportata.

Esempi pratici:

- Analisi del segnale in ambienti complessi.
- Individuazione di reti non autorizzate.
- Supporto preliminare per attività Red Team/Blue Team.
- Diagnostica per migliorare la copertura WiFi domestica.