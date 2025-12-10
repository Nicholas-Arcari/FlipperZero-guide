# NRF24

Strumenti basati sul transceiver NRF24L01+ a 2.4 GHz, utilizzati per analisi radio, sniffing, jamming, hijacking e comunicazioni wireless low‑power.

Ideali per studiare periferiche come mouse wireless, telecomandi, sensori proprietari e protocolli RF custom.

### **• AZERTY Mouse Jacker**

Versione del Mouse Jacker ottimizzata per layout AZERTY, comunemente usato in Francia, Belgio e altre regioni.

Funzionalità ampliate:

- Hijacking di mouse wireless vulnerabili tramite spoofing del dongle USB.
- Invio comandi come movimenti, click, digitazione simulata.
- Conversione automatica layout → da QWERTY a AZERTY.
- Scan frequenze attive → aggancio automatico al target.
- Modalità “stealth delay” per simulare input umani.

Esempi pratici:

- Dimostrazione di attacchi HID su un PC aziendale.
- Test sicurezza dispositivi wireless economici.

### **• Batch**

Esecuzione automatizzata di script radio preconfigurati per flussi di lavoro ripetitivi.

Funzionalità ampliate:

- Sequenze di comandi NRF24 eseguibili in batch.
- Automazione di scan, sniff, jam in ordine definito.
- Integrazione con file script esterni.
- Logging automatico dei risultati.

Esempi pratici:

- Automatizzare un ciclo: scan → sniff → dump pacchetti.
- Script per analisi notturna di traffico RF.

### **• Channel Scan**

Effettua una scansione spettro 2.4 GHz sui canali NRF per rilevare attività.

Funzionalità ampliate:

- Analisi intensità segnale per ciascun canale.
- Identificazione rapida di canali occupati da dispositivi target.
- Visualizzazione grafica (heatmap semplificata se supportata).
- Comparazione tra scansioni successive.

Esempi pratici:

- Individuare canali usati da telecomandi wireless.
- Preparare attacchi su periferiche vulnerabili.

### **• FZ NRF24 Jammer**

Jammer RF dedicato al modulo NRF24 con ottimizzazioni specifiche per Flipper Zero.

Funzionalità ampliate:

- Inondazione canale con pacchetti fittizi.
- Modalità sequenziale: jamming multi‑canale ciclico.
- Configurazione potenza TX (se supportata).
- Log efficacia jamming in tempo reale.

Esempi pratici:

- Dimostrare vulnerabilità a jamming su sensori wireless.
- Test immunità a interferenze RF.

### **• Mouse Jacker**

Strumento dedicato all’hijacking di mouse wireless non criptati.

Funzionalità ampliate:

- Cattura del “pairing ID” della periferica.
- Spoofing dongle → Flipper si sostituisce al mouse.
- Invio sequenze HID (click, movimenti, digitazione).
- Individuazione automatica frequenza attiva.

Esempi pratici:

- Valutazione sicurezza di mouse wireless da ufficio.
- Dimostrazioni per awareness sulla sicurezza HID.

### **• Mouse Jacker MS**

Versione ottimizzata per mouse Microsoft Wireless.

Funzionalità ampliate:

- Riconoscimento protocolli MS proprietari.
- Ridotta latenza per aggancio più rapido.
- Gestione input MS come tilt‑scroll o funzioni extra.
- Migliore stabilità in ambienti RF rumorosi.

Esempi pratici:

- Attacco dimostrativo su dongle MS riducendo falsi positivi.
- Reverse engineering su protocolli MS baseband.

### **• NRF24 Jammer**

Versione generica del jammer NRF, compatibile con molte configurazioni.

Funzionalità ampliate:

- Jamming singolo o multi‑canale.
- Supporto a diverse larghezze di banda operative.
- Modalità burst o stream continuo.

Esempi pratici:

- Stress‑testing reti sensori personali.
- Analisi resilienza remote controls.

### **• NRF24Monitor**

Monitor avanzato delle attività RF su canali e pipe del modulo NRF24.

Funzionalità ampliate:

- Monitor live dei pacchetti in arrivo.
- Visualizzazione RSSI/rumore.
- Rilevamento handshake e flussi di pairing.
- Identificazione delle “pipes” attive (indirizzi logici NRF).

Esempi pratici:

- Sniffing non intrusivo per riconoscere pattern dati.
- Diagnostica problemi di trasmissione RF.

### **• Scanner**

Strumento per la ricerca di dispositivi NRF24 nell’area circostante.

Funzionalità ampliate:

- Scan indirizzi pipe e frequenze attive.
- Identificazione dispositivi sconosciuti tramite fingerprinting pacchetti.
- Stima distanza relativa attraverso forza segnale (RSSI indiretto).
- Log esportabile.

Esempi pratici:

- Localizzare un telecomando smarrito basato su NRF.
- Creare una mappa RF di dispositivi nella zona.

### **• Sniffer**

Cattura pacchetti NRF24 per analisi, reverse engineering e auditing.

Funzionalità ampliate:

- Cattura raw pacchetti con timestamp.
- Decodifica indirizzi pipe, sequence number e payload.
- Esportazione PCAP‑like.
- Modalità “Follow Target” per dispositivi in movimento.

Esempi pratici:

- Reverse engineering di un sensore proprietario da 2.4GHz.
- Cattura handshake di un mouse wireless.

### **• Sniffer MS**

Variante dello Sniffer specifica per protocolli Microsoft.

Funzionalità ampliate:

- Riconoscimento formati MS obfuscati.
- Migliore aggancio su mouse/tastiere MS 2.4 GHz.
- Decodifica preliminare pacchetti noti.

Esempi pratici:

- Analisi sicurezza dispositivi MS economici.
- Studio comunicazione MS per sviluppare script di automazione.