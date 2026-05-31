## 9. Aspetti Legali

### 9.1 Quadro normativo italiano

L'utilizzo del modulo NRF24L01+ con il Flipper Zero per attività di analisi e test rientra in un quadro normativo complesso.

**Attività consentite senza autorizzazione:**

- Studio e ricerca personale in ambiente domestico
- Test su dispositivi di propria proprietà
- Analisi spettrale passiva (solo ricezione)
- Sviluppo software e firmware

**Attività che richiedono autorizzazione:**

- Penetration test su sistemi di terzi (richiede contratto e scope of work)
- Sniffing di comunicazioni altrui (anche se in chiaro)
- Qualsiasi forma di iniezione di pacchetti su dispositivi non propri
- Test di jamming (anche in ambiente controllato, per tutela)

**Attività illegali senza eccezioni:**

- Jamming in ambiente non schermato senza autorizzazione
- Intercettazione di comunicazioni private
- Accesso non autorizzato a sistemi informatici (via MouseJacker o altro)
- Disturbo delle telecomunicazioni

### 9.2 Riferimenti normativi

- **D.Lgs. 259/2003** (Codice delle Comunicazioni Elettroniche): regola l'uso delle frequenze radio. L'uso della banda ISM 2.4 GHz è consentito per dispositivi a bassa potenza conformi alla normativa ETSI, ma il jamming intenzionale è esplicitamente vietato.
- **Art. 615-ter Codice Penale** (Accesso abusivo a sistema informatico): l'iniezione di comandi via MouseJacker su un PC senza autorizzazione configura accesso abusivo.
- **Art. 617-quater Codice Penale** (Intercettazione di comunicazioni): lo sniffing di tastiere wireless può configurare intercettazione.
- **Art. 340 Codice Penale** (Interruzione di pubblico servizio): se il jamming colpisce servizi pubblici.
- **Regolamento AGCOM**: sanzioni amministrative per uso improprio di apparecchiature radio.

### 9.3 Penetration testing autorizzato

Per operare legalmente in un pentest:

1. **Contratto firmato** con il committente che specifichi:
   - Scope delle attività (incluse esplicitamente le attività RF)
   - Elenco degli asset in scope
   - Periodo temporale autorizzato
   - Contatti di emergenza
   - Limiti e esclusioni

2. **Lettera di autorizzazione** (Get Out of Jail Free letter):
   - Firmata dal rappresentante legale dell'azienda
   - Specifica le attività autorizzate
   - Include riferimento al contratto
   - Da portare sempre durante le attività

3. **Rules of Engagement (RoE):**
   - Orari consentiti per le attività
   - Aree fisiche autorizzate
   - Tecniche autorizzate e vietate
   - Procedura di escalation in caso di incidenti
   - Gestione dei dati sensibili eventualmente catturati

4. **Per attività RF specifiche, il contratto dovrebbe menzionare:**
   - "Test di sicurezza delle periferiche wireless"
   - "Analisi dello spettro RF nell'area degli uffici"
   - "Verifica della resilienza al jamming" (se applicabile)
   - "Simulazione di attacchi MouseJacker"

### 9.4 GDPR e dati catturati

Lo sniffing di tastiere wireless può catturare dati personali (password, email, messaggi). Il trattamento di questi dati è soggetto al GDPR:

- Minimizzazione: catturare solo il necessario per la proof of concept
- Conservazione limitata: eliminare i dati raw dopo il report
- Pseudonimizzazione: nel report, non includere i dati personali catturati
- Notifica: informare il committente dei dati personali eventualmente catturati
- Sicurezza: proteggere i dati catturati con crittografia durante il trasporto e l'archiviazione

> Nota personale: la parte legale non è sexy ma è fondamentale. Ho visto colleghi finire nei guai per aver fatto sniffing RF senza autorizzazione esplicita. Il mio consiglio: fate inserire nel contratto una clausola specifica per le attività RF. I clienti spesso autorizzano il pentest "classico" (rete, web, social engineering) ma non pensano all'RF. Se il vostro scope of work dice solo "penetration test infrastrutturale", il MouseJacker potrebbe NON essere coperto. Meglio chiedere prima che spiegare dopo.

---

## 10. Strumenti Disponibili nel Flipper Zero -- Dettaglio Operativo

Riepilogo completo degli strumenti NRF24 disponibili nel Flipper Zero con firmware custom (Unleashed / RogueMaster):

### AZERTY Mouse Jacker

Versione del Mouse Jacker ottimizzata per layout AZERTY, comunemente usato in Francia, Belgio e altre regioni francofone.

Funzionalità:

- Hijacking di mouse wireless vulnerabili tramite spoofing del dongle USB
- Invio comandi come movimenti, click, digitazione simulata
- Conversione automatica layout da QWERTY a AZERTY
- Scan frequenze attive con aggancio automatico al target
- Modalità "stealth delay" per simulare input umani e ridurre il sospetto
- Supporto per caratteri accentati francesi (e', e`, a`, u`, c cediglia)

Quando usarlo:

- Target con layout tastiera francese/belga
- Penetration test in aziende francofone
- Quando il layout QWERTY produce caratteri errati sul target

### Batch

Esecuzione automatizzata di script radio preconfigurati per flussi di lavoro ripetitivi.

Funzionalità:

- Sequenze di comandi NRF24 eseguibili in batch da file script
- Automazione di scan, sniff, jam in ordine definito dall'utente
- Integrazione con file script esterni dalla SD card
- Logging automatico dei risultati con timestamp
- Possibilità di concatenare più operazioni senza intervento manuale

Quando usarlo:

- Ricognizione automatizzata all'inizio di un audit
- Monitoraggio continuo in background
- Esecuzione di test ripetitivi su più target
- Generazione automatica di log per il report

### Channel Scan

Scansione spettro 2.4 GHz sui canali NRF per rilevare attività.

Funzionalità:

- Analisi intensità segnale per ciascun canale (0-125)
- Identificazione rapida di canali occupati da dispositivi target
- Visualizzazione grafica semplificata della distribuzione del segnale
- Comparazione tra scansioni successive per rilevare cambiamenti
- Identificazione interferenze Wi-Fi nella stessa banda

Quando usarlo:

- Come primo passo in qualsiasi operazione NRF24
- Per identificare il canale di un dispositivo target
- Per scegliere un canale pulito per le proprie trasmissioni
- Per mappare l'ambiente RF dell'area di interesse

### FZ NRF24 Jammer

Jammer RF dedicato con ottimizzazioni specifiche per il Flipper Zero.

Funzionalità:

- Inondazione canale con pacchetti fittizi ad alta velocità
- Modalità sequenziale: jamming multi-canale ciclico
- Configurazione potenza TX
- Log efficacia jamming in tempo reale
- Interfaccia ottimizzata per il display del Flipper

Quando usarlo:

- Test di resilienza di sistemi wireless in laboratorio schermato
- Verifica delle contromisure anti-jamming di un sistema
- Solo con autorizzazione esplicita e in ambiente controllato

### Mouse Jacker

Strumento principale per l'hijacking di mouse wireless non criptati.

Funzionalità:

- Scansione automatica dei canali alla ricerca di periferiche wireless
- Cattura del pairing ID della periferica target
- Spoofing dongle: il Flipper si sostituisce al mouse legittimo
- Invio sequenze HID (click, movimenti, digitazione via DuckyScript)
- Individuazione automatica della frequenza attiva
- Supporto per payload personalizzati dalla SD card

Quando usarlo:

- Proof of concept per audit di sicurezza periferiche wireless
- Demo di awareness per il management
- Test di lateral movement in penetration test
- Verifica dell'efficacia di aggiornamenti firmware

### Mouse Jacker MS

Versione ottimizzata per mouse e periferiche Microsoft Wireless.

Funzionalità:

- Riconoscimento protocolli MS proprietari
- Ridotta latenza per aggancio più rapido sui dispositivi MS
- Gestione input MS specifici come tilt-scroll e funzioni extra
- Migliore stabilità in ambienti RF rumorosi
- Compatibilità con le varie generazioni di dongle MS

Quando usarlo:

- Target specificamente Microsoft Wireless
- Quando il Mouse Jacker generico non aggancia il dispositivo MS
- Per reverse engineering dei protocolli MS proprietari

### NRF24 Jammer

Versione generica del jammer, compatibile con configurazioni diverse.

Funzionalità:

- Jamming singolo canale o multi-canale
- Supporto a diverse larghezze di banda operative
- Modalità burst (impulsi) o stream continuo
- Configurazione del pattern di sweep per multi-canale

Quando usarlo:

- Alternativa all'FZ NRF24 Jammer per configurazioni non standard
- Test su bande di canali specifiche
- Stress testing di dispositivi con frequency hopping

### NRF24Monitor

Monitor avanzato delle attività RF su canali e pipe del modulo NRF24.

Funzionalità:

- Monitor live dei pacchetti in arrivo con contatore
- Visualizzazione RSSI/rumore stimato
- Rilevamento handshake e flussi di pairing
- Identificazione delle pipe attive (indirizzi logici NRF)
- Alert su nuovi dispositivi rilevati
- Log continuo esportabile

Quando usarlo:

- Osservazione passiva dell'ambiente RF
- Rilevamento di nuovi dispositivi nell'area
- Studio del comportamento di un dispositivo target nel tempo
- Diagnostica problemi di trasmissione RF

### Scanner

Strumento per la ricerca attiva di dispositivi NRF24 nell'area circostante.

Funzionalità:

- Scan indirizzi pipe e frequenze attive su tutti i 126 canali
- Identificazione dispositivi sconosciuti tramite fingerprinting pacchetti
- Classificazione tipo dispositivo (mouse, tastiera, sensore, altro)
- Stima distanza relativa attraverso forza segnale (RPD)
- Log esportabile con tutti i dettagli dei dispositivi trovati

Quando usarlo:

- Mappatura completa dei dispositivi NRF24 in un'area
- Inventario delle periferiche wireless in un ufficio
- Localizzazione fisica di un dispositivo specifico
- Preparazione dell'attacco (identificazione target e parametri)

### Sniffer

Cattura pacchetti NRF24 per analisi, reverse engineering e auditing.

Funzionalità:

- Cattura raw pacchetti con timestamp preciso
- Decodifica indirizzi pipe, sequence number e payload
- Esportazione in formato analizzabile esternamente
- Modalità "Follow Target" per dispositivi che cambiano canale
- Filtro per indirizzo pipe per isolare un dispositivo specifico
- Cattura continua con buffer circolare

Quando usarlo:

- Reverse engineering di protocolli proprietari
- Cattura di credenziali da tastiere non criptate
- Analisi del traffico di sensori IoT
- Studio del protocollo di pairing di dispositivi nuovi
- Raccolta prove per il report di audit

### Sniffer MS

Variante dello Sniffer specifica per protocolli Microsoft.

Funzionalità:

- Riconoscimento formati MS con decodifica automatica
- Migliore aggancio su mouse/tastiere MS a 2.4 GHz
- Decodifica preliminare dei campi noti del protocollo MS
- Tracking del frequency hopping pattern MS

Quando usarlo:

- Analisi specifica di dispositivi Microsoft Wireless
- Quando lo Sniffer generico non cattura correttamente i pacchetti MS
- Reverse engineering approfondito del protocollo MS
- Audit di sicurezza di ambienti con periferiche Microsoft

---

