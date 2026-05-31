## 4. Sniffing NRF24

### 4.1 Cattura pacchetti raw

Lo Sniffer NRF24 del Flipper Zero cattura pacchetti grezzi trasmessi dai dispositivi che usano il chip NRF24L01+ o protocolli compatibili.

Cosa cattura:

- Pacchetti Enhanced ShockBurst completi
- Indirizzo pipe (3-5 byte)
- Payload (0-32 byte per pacchetto)
- CRC (per validazione integrità)
- Informazioni di timing (timestamp)
- Canale RF di ricezione

Cosa NON cattura:

- Il preambolo (gestito internamente dal chip)
- Pacchetti su canali diversi da quello configurato (a meno di non fare scanning)
- Pacchetti con formato non-ESB (altri protocolli 2.4 GHz)

### 4.2 Modalità di funzionamento

**Sniffer generico:**

- Si configura un canale e un indirizzo pipe (o un indirizzo "promiscuo")
- Il modulo cattura tutto il traffico che corrisponde ai criteri
- I pacchetti vengono mostrati in tempo reale sul display del Flipper
- Si possono esportare per analisi successiva

**Sniffer in modalità promiscua:**

- Tecnica avanzata: si configura un indirizzo pipe molto corto (2 byte) con un pattern comune
- Si cattura un volume maggiore di traffico, inclusi pacchetti di dispositivi sconosciuti
- Utile per la fase di ricognizione quando non si conosce l'indirizzo del target
- Maggiore rumore (falsi positivi) ma copertura più ampia

**Sniffer con "Follow Target":**

- Dopo aver identificato un dispositivo, lo sniffer segue automaticamente i cambi di canale
- Basato sul pattern di frequency hopping del protocollo target
- Essenziale per Logitech Unifying che cambia canale frequentemente

### 4.3 Decodifica indirizzi pipe

Ogni dispositivo NRF24 ha un indirizzo pipe unico. Decodificare questo indirizzo è il primo passo per qualsiasi attacco mirato.

Tecniche di decodifica:

1. **Sniffing passivo**: catturare pacchetti e estrarre l'indirizzo dal campo indirizzo
2. **Brute force**: provare indirizzi comuni (molti dispositivi economici usano indirizzi di default come 0xE7E7E7E7E7)
3. **Pattern matching**: cercare sequenze note nei dati catturati
4. **Reverse engineering del firmware**: estrarre l'indirizzo dal firmware del dispositivo (se accessibile)

Indirizzi di default comuni:

```
0xE7E7E7E7E7  -- Default NRF24 (molto comune)
0xC2C2C2C2C2  -- Alternativa comune
0xA5A5A5A5A5  -- Usato da alcuni produttori cinesi
0x0102030405  -- Sequenziale (dispositivi di sviluppo)
```

> Nota personale: la quantità di dispositivi che usano indirizzi di default è sconvolgente. In un audit ho trovato 3 sensori di temperatura su 5 con indirizzo 0xE7E7E7E7E7. I produttori non cambiano nemmeno l'indirizzo di default dal reference design Nordic. È come usare admin/admin come credenziali.

### 4.4 Payload analysis

Una volta catturati i pacchetti, l'analisi del payload rivela:

**Per mouse wireless:**

- Byte di stato (pulsanti premuti)
- Delta X e Delta Y (movimento)
- Delta scroll wheel
- Byte di controllo/sequenza

Formato tipico payload mouse Logitech Unifying:

```
Byte 0: tipo dispositivo (0x00 = mouse)
Byte 1: flags (pulsanti)
Byte 2-3: delta X (little endian)
Byte 4-5: delta Y (little endian)
Byte 6: scroll wheel
Byte 7-9: riservati/padding
```

**Per tastiere wireless (non criptate):**

- Scancode del tasto premuto
- Modifier keys (Shift, Ctrl, Alt, GUI)
- Possibilità di ricostruire tutto cio' che viene digitato (keylogging via radio)

**Per sensori IoT:**

- Dati di telemetria (temperatura, umidità, pressione)
- Identificativi del sensore
- Contatori di sequenza
- Byte di stato batteria

### 4.5 Sniffer MS -- Dispositivi Microsoft

Variante dello sniffer ottimizzata per i protocolli Microsoft Wireless:

- Riconoscimento dei formati pacchetto MS proprietari
- Decodifica dei campi specifici MS (device type, battery status, extra buttons)
- Migliore aggancio sui canali usati dai dispositivi MS
- Gestione del frequency hopping pattern MS

I dispositivi Microsoft usano un protocollo leggermente diverso da Logitech:

- Indirizzi pipe specifici per ogni famiglia di prodotti
- Formato payload diverso per mouse e tastiere
- Meccanismo di pairing proprietario
- Alcuni modelli usano una forma di offuscamento (non crittografia vera)

### 4.6 Uso per reverse engineering

Lo sniffer NRF24 è uno strumento eccellente per il reverse engineering di protocolli proprietari:

1. Catturare traffico in diverse condizioni (riposo, movimento, click, pairing)
2. Confrontare i payload per identificare campi variabili vs fissi
3. Correlare azioni fisiche con variazioni nel payload
4. Ricostruire il formato del protocollo campo per campo
5. Verificare le ipotesi iniettando pacchetti modificati

Questa tecnica è stata usata per reverse-engineerare i protocolli di:

- Mouse e tastiere wireless (Logitech, Microsoft, HP, Dell)
- Sensori di temperatura/umidità wireless (Oregon Scientific, Acurite)
- Telecomandi per droni economici
- Sistemi di allarme wireless
- Giocattoli radiocontrollati
- Campanelli wireless
- Telecomandi per luci LED

> Nota personale: il reverse engineering con lo sniffer NRF24 è una delle attività più educative che si possano fare con il Flipper. Ho passato un weekend intero a decodificare il protocollo di un sensore di temperatura Oregon Scientific. Alla fine avevo documentato ogni singolo byte del payload: ID sensore, canale, temperatura (BCD encoded con segno), umidità, stato batteria, checksum. La soddisfazione di vedere i dati decodificati correttamente è impagabile. È cosi' che si impara davvero come funzionano le comunicazioni RF.

---

## 5. Jamming 2.4 GHz

### 5.1 Come funziona

Il jamming consiste nell'inondare uno o più canali RF con segnale interferente, impedendo ai dispositivi legittimi di comunicare.

Il NRF24L01+ può essere usato come jammer in due modi:

**Jamming a portante continua:**

- Il modulo trasmette un segnale continuo su un canale specifico
- Qualsiasi dispositivo su quel canale non riesce a comunicare
- Semplice ma efficace

**Jamming a pacchetti:**

- Il modulo trasmette pacchetti fittizi ad alta velocità
- Riempie il canale con traffico spazzatura
- I dispositivi legittimi non riescono a inserirsi nella conversazione
- Più efficace della portante continua per alcuni protocolli

### 5.2 Jamming mirato per canale

Selezionando un canale specifico, si può disturbare solo i dispositivi che operano su quel canale:

- Identificare il canale del target con Channel Scan o Sniffer
- Configurare il jammer su quel canale specifico
- Attivare la trasmissione continua

Vantaggi:

- Disturba solo il target, non tutti i dispositivi nella zona
- Meno evidente e più chirurgico
- Utile per test mirati su dispositivi specifici

### 5.3 Jamming multi-canale

Modalità che scansiona ciclicamente più canali, trasmettendo brevemente su ciascuno:

- Copre uno spettro più ampio
- Disturba dispositivi con frequency hopping
- Meno efficace su ciascun singolo canale (tempo di dwell ridotto)
- Utile contro protocolli che cambiano canale quando rilevano interferenze

Il Flipper Zero con NRF24 offre due implementazioni:

**FZ NRF24 Jammer:**

- Ottimizzato per il Flipper Zero
- Configurazione semplificata via menu
- Modalità singolo canale e sweep
- Log efficacia in tempo reale

**NRF24 Jammer (generico):**

- Versione standard
- Supporto multi-canale ciclico
- Modalità burst e stream
- Configurazione larghezza di banda operativa

### 5.4 Efficacia e limiti

Il jamming con NRF24L01+ ha limiti intrinseci:

- Potenza massima 0 dBm (versione base) o +20 dBm (PA+LNA)
- Un singolo modulo può trasmettere su un solo canale alla volta
- Il multi-canale ciclico lascia "buchi" temporali
- Dispositivi con frequency hopping aggressivo possono resistere
- Il Wi-Fi (che opera nella stessa banda) può essere disturbato ma ha potenza molto superiore

Per un jamming efficace:

- Usare la versione PA+LNA per massima potenza
- Posizionarsi il più vicino possibile al target
- Identificare i canali esatti del target prima di jammmare
- Considerare che il frequency hopping Bluetooth è molto resistente al jamming NRF24

### 5.5 Implicazioni legali del jamming

Il jamming RF è ILLEGALE in praticamente tutte le giurisdizioni, inclusa l'Italia.

Riferimenti normativi italiani:

- Codice delle Comunicazioni Elettroniche (D.Lgs. 259/2003)
- Art. 340 Codice Penale (interruzione di pubblico servizio, se il jamming colpisce servizi pubblici)
- Art. 617-quater Codice Penale (intercettazione di comunicazioni informatiche o telematiche)
- Sanzioni AGCOM per uso improprio di apparecchiature radio

Il jamming è consentito SOLO:

- In ambienti completamente schermati (gabbia di Faraday)
- Con autorizzazione scritta esplicita del committente
- In ambito militare/governativo con autorizzazione specifica
- Per test in laboratorio con emissioni contenute

> Nota personale: non usate MAI il jammer in ambienti non controllati. Durante un pentest in un'azienda, un collega ha acceso per errore il jammer NRF24 a massima potenza. Ha disturbato i mouse wireless di tre uffici e un access point Wi-Fi nella stessa banda. Il team IT si è presentato in 5 minuti. Abbiamo dovuto spiegare la situazione al responsabile. Da quel giorno, il jammer si usa SOLO in sala test schermata o con autorizzazione scritta specifica che menziona esplicitamente il jamming RF. La regola d'oro: se il vostro scope of work non dice esplicitamente "jamming autorizzato", non fatelo.

---

## 6. Channel Scan

### 6.1 Scansione spettro 2.4 GHz

Il Channel Scan effettua una scansione sistematica dei 126 canali disponibili per identificare attività RF.

Funzionamento:

1. Il modulo NRF24 si sintonizza su ciascun canale in sequenza
2. Per ogni canale, misura il livello di segnale ricevuto
3. Rileva se ci sono pacchetti validi (con CRC corretto)
4. Presenta i risultati sotto forma di mappa spettrale

### 6.2 Identificazione canali attivi

I canali attivi vengono identificati in base a:

- Livello di segnale sopra una soglia configurabile
- Presenza di pacchetti con CRC valido
- Pattern di attività (costante vs intermittente)
- Tipo di segnale (Enhanced ShockBurst vs rumore)

Interpretazione dei risultati:

- **Picchi stretti su canali specifici**: dispositivi NRF24 (mouse, sensori, telecomandi)
- **Bande larghe di attività**: interferenza Wi-Fi
- **Attività intermittente**: dispositivi che trasmettono solo su evento (mouse in movimento, sensori periodici)
- **Canali costantemente occupati**: dispositivi in streaming continuo o beacon

### 6.3 RSSI e stima della distanza

Il NRF24L01+ non fornisce un valore RSSI diretto come altri transceiver. Tuttavia, è possibile stimare indirettamente la forza del segnale:

- RPD (Received Power Detector): flag binario che indica se il segnale supera -64 dBm
- Tasso di pacchetti persi: più alto = segnale debole / distanza maggiore
- CRC errors: aumentano con il degrado del segnale

Per una stima più precisa della distanza:

1. Eseguire una scansione di riferimento a distanza nota
2. Muoversi e ripetere la scansione
3. Confrontare il tasso di ricezione pacchetti
4. Triangolare con più misurazioni da posizioni diverse

### 6.4 Uso pratico nel pentest

Il Channel Scan è il primo passo in qualsiasi operazione con NRF24:

1. **Ricognizione**: scansionare per identificare tutti i dispositivi wireless attivi
2. **Pianificazione**: scegliere il canale meno congestionato per operazioni proprie
3. **Targeting**: identificare il canale del dispositivo target
4. **Validazione**: verificare dopo un attacco che il target abbia cambiato canale o sia offline

Workflow tipico:

```
Channel Scan → Identificare target → Sniffer (cattura indirizzo) → MouseJacker/Analisi
```

> Nota personale: faccio sempre almeno due scansioni complete prima di iniziare qualsiasi operazione. La prima per avere un baseline dell'ambiente RF, la seconda dopo 5-10 minuti per confermare quali dispositivi sono permanenti e quali transitori. In un ufficio tipico trovo tra 5 e 15 dispositivi NRF24-compatibili. I mouse wireless sono i più comuni, seguiti da tastiere e poi da sensori IoT vari.

---

## 7. NRF24Monitor / Scanner / Batch

### 7.1 NRF24Monitor

Il monitor è lo strumento di osservazione continua dell'attività RF.

Funzionalità:

- Monitoraggio live dei pacchetti in arrivo su un canale selezionato
- Visualizzazione del conteggio pacchetti per indirizzo pipe
- Rilevamento di nuovi dispositivi che appaiono nell'area
- Tracking dell'attività nel tempo (burst vs costante vs periodica)
- Identificazione di handshake e sequenze di pairing
- Rilevamento delle pipe attive (indirizzi logici NRF)

Modalità operative:

**Monitor singolo canale:**

- Si fissa un canale e si osserva tutto il traffico
- Ideale dopo aver identificato il canale del target con Channel Scan
- Massima sensibilità (nessun tempo perso a cambiare canale)

**Monitor multi-canale:**

- Scansione ciclica di più canali in rapida successione
- Copertura più ampia ma possibilità di perdere pacchetti
- Utile in fase di ricognizione iniziale

**Visualizzazione RSSI/rumore:**

- Mostra il livello di segnale per ogni pacchetto ricevuto
- Utile per stimare la distanza relativa dei dispositivi
- Permette di localizzare fisicamente un dispositivo muovendosi e osservando il livello

### 7.2 Scanner

Lo Scanner è dedicato alla ricerca attiva di dispositivi NRF24 nell'area.

Differenze dal Monitor:

- Lo Scanner cerca attivamente dispositivi, non si limita a osservare passivamente
- Scansiona tutti i canali in sequenza
- Identifica dispositivi tramite fingerprinting dei pacchetti
- Stima la distanza relativa tramite forza del segnale

Funzionalità:

- Scan indirizzi pipe su tutti i canali
- Fingerprinting: identifica il tipo di dispositivo dal formato dei pacchetti
- Classificazione: mouse, tastiera, sensore, sconosciuto
- Stima distanza relativa (vicino/medio/lontano basato su RPD e perdita pacchetti)
- Log esportabile con timestamp, indirizzo, canale, tipo, forza segnale

Uso tipico:

1. Avviare lo Scanner all'ingresso di un'area target
2. Camminare lentamente attraverso l'area
3. Lo Scanner identifica e cataloga ogni dispositivo NRF24
4. Esportare il log per pianificazione successiva
5. Selezionare i target per analisi approfondita

### 7.3 Batch

L'esecuzione batch permette di automatizzare sequenze di operazioni NRF24.

Funzionalità:

- Esecuzione di script preconfigurati
- Sequenze di comandi: scan, sniff, jam in ordine definito
- Integrazione con file script esterni dalla SD card
- Logging automatico dei risultati
- Esecuzione programmata (temporizzata)

Esempi di script batch:

**Script di ricognizione automatica:**

```
# Scansione completa + cattura indirizzi
CHANNEL_SCAN ALL
WAIT 30
SNIFFER PROMISCUOUS CH:0-125
WAIT 60
LOG EXPORT /ext/nrf24/recon_log.txt
```

**Script di monitoraggio notturno:**

```
# Monitoraggio continuo per 8 ore
MONITOR MULTI_CH
DURATION 28800
LOG CONTINUOUS /ext/nrf24/night_monitor.txt
ALERT ON_NEW_DEVICE
```

**Script di audit periferiche:**

```
# Scansiona e testa ogni dispositivo trovato
SCANNER FULL
FOR EACH DEVICE
  IDENTIFY TYPE
  IF TYPE == MOUSE
    LOG "Mouse wireless trovato" + ADDRESS
    TEST MOUSEJACKER DRY_RUN
  ENDIF
NEXT
LOG EXPORT /ext/nrf24/audit_report.txt
```

L'automazione batch è particolarmente utile per:

- Audit ricorrenti (eseguire la stessa scansione settimanalmente)
- Monitoraggio continuo in background
- Test di regressione dopo remediation
- Documentazione automatica per report

> Nota personale: il batch è sottovalutato. Lo uso per automatizzare la fase di ricognizione nei pentest: arrivo, attacco il Flipper con NRF24, lancio lo script di ricognizione e nel frattempo mi occupo di altre cose. Dopo 10 minuti ho una mappa completa di tutti i dispositivi NRF24 nell'area con indirizzi, canali e tipi. Risparmio almeno mezz'ora di lavoro manuale ogni volta.

---

