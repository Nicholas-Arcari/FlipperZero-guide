## Tool per Tool - Guida Operativa

### Sub-GHz (Modulo Principale)

Il hub centrale per tutte le operazioni RF.

**Menu principale:**
- **Read** - Ascolta e decodifica segnali automaticamente
- **Read RAW** - Cattura il segnale grezzo senza decodifica
- **Saved** - Gestisce i file .sub salvati
- **Add Manually** - Crea un segnale da parametri noti
- **Frequency Analyzer** - Rileva frequenze attive
- **Test** - Diagnostica hardware

#### Read - Decodifica Automatica

Procedura operativa completa:

1. Apri Sub-GHz → Read
2. Il Flipper ascolta sulla frequenza impostata (default 433.92 MHz)
3. **Per cambiare frequenza:** premi ← o → per scorrere le frequenze preimpostate, oppure tieni premuto ← per inserire una frequenza manuale
4. **Per cambiare modulazione:** premi il tasto config e seleziona AM (OOK) o FM (FSK)
5. Quando un telecomando trasmette nel raggio, il Flipper decodifica il protocollo e mostra:
   - Nome del protocollo (es. "Nice FLO")
   - Codice/ID del telecomando
   - Numero di bit
   - Contatore (se rolling code)
   - Frequenza esatta
6. Premi il tasto centrale per **salvare** il segnale decodificato

**Parametri del file .sub salvato:**
```
Filetype: Flipper SubGhz Key File
Version: 1
Frequency: 433920000
Preset: FuriHalSubGhzPresetOok650Async
Protocol: Princeton
Bit: 24
Key: 00 00 00 00 00 A4 B3 C2
```

**Preset disponibili e quando usarli:**

| Preset | Modulazione | Bandwidth | Uso |
|---|---|---|---|
| FuriHalSubGhzPresetOok270Async | OOK | 270 kHz | Default per la maggior parte dei telecomandi |
| FuriHalSubGhzPresetOok650Async | OOK | 650 kHz | Segnali a banda larga, alcuni sensori |
| FuriHalSubGhzPreset2FSKDev238Async | 2-FSK | 238 kHz dev | Protocolli FSK standard |
| FuriHalSubGhzPreset2FSKDev476Async | 2-FSK | 476 kHz dev | Protocolli FSK a deviazione larga |
| FuriHalSubGhzPresetCustom | Custom | Variabile | Configurazione manuale registri CC1101 |

> **Nota personale:** Il preset OOK270 è quello che uso nel 95% dei casi. OOK650 l'ho usato solo con alcuni sensori meteo Oregon Scientific che hanno un segnale più largo del normale. Per il resto, se non decodifica con OOK270, passo direttamente a Read RAW.

#### Read RAW - Cattura Grezza

Quando il Flipper non riesce a decodificare il protocollo (segnale proprietario, modulazione non standard, protocollo non supportato), Read RAW cattura l'intero segnale come sequenza di durate di impulsi:

1. Apri Sub-GHz → Read RAW
2. Imposta la frequenza target
3. Premi il tasto REC (registra)
4. Il telecomando target trasmette
5. Il Flipper registra tutto il segnale come raw
6. Premi STOP
7. Salva il file

**Il file .sub RAW contiene:**
```
Filetype: Flipper SubGhz RAW File
Version: 1
Frequency: 433920000
Preset: FuriHalSubGhzPresetOok650Async
Protocol: RAW
RAW_Data: 5542 -5026 501 -1020 499 -1022 499 -510 ...
```

I numeri rappresentano durate in microsecondi: positivi = segnale alto (TX), negativi = segnale basso (silenzio).

**Quando usare Read RAW:**
- Il protocollo non viene riconosciuto
- Vuoi catturare un segnale rolling code (per studio, non per replay)
- Il segnale è molto debole o disturbato
- Stai facendo reverse engineering di un protocollo sconosciuto
- Il dispositivo usa una modulazione non standard

**Replay di un RAW:**
1. Apri Sub-GHz → Saved → seleziona il file RAW
2. Premi Send
3. Il Flipper riproduce la sequenza esatta di impulsi

> **Nota personale:** Read RAW è fondamentale per il reverse engineering. Quando trovo un dispositivo sconosciuto, catturo sempre sia in OOK che in FSK e poi analizzo i file offline. Attenzione: i file RAW possono essere molto grandi se registri per troppo tempo. Tieni la registrazione più corta possibile - 2-3 secondi di segnale bastano.

#### Saved - Gestione File

Da qui puoi:
- **Send:** trasmetti il segnale salvato
- **Emulate:** per protocolli che lo supportano, emula continuamente (utile per iButton/RFID via Sub-GHz, non comune)
- **Rename:** rinomina il file
- **Edit:** modifica parametri (frequenza, protocollo, chiave)
- **Delete:** elimina il file
- **Info:** mostra dettagli del file

#### Add Manually - Creazione Segnali

Permette di creare un file .sub da zero specificando:
- Protocollo
- Frequenza
- Chiave/ID
- Numero bit
- Ripetizioni

Utile quando conosci il codice target (es. da un database o da analisi con SDR) e vuoi crearlo direttamente.

### Frequency Analyzer (con Antenna Esterna)

Strumento di ricognizione essenziale: rileva la frequenza su cui trasmette un dispositivo sconosciuto.

**Procedura operativa:**

1. Apri Sub-GHz → Frequency Analyzer
2. Il display mostra un grafico RSSI in tempo reale
3. Premi il pulsante del telecomando target **vicino** al Flipper (< 1 metro)
4. Un picco appare sulla frequenza del segnale
5. La frequenza dominante viene mostrata in alto
6. Annota la frequenza → usala in Read o Read RAW

**Limiti:**
- Funziona solo sulle bande supportate dal CC1101
- La risoluzione è limitata (~10-20 kHz)
- Segnali molto deboli potrebbero non essere rilevati
- Non distingue tra modulazioni (serve Read per quello)

**Con antenna esterna:** collegando un modulo CC1101 esterno via GPIO, la sensibilità aumenta notevolmente. Questo permette di rilevare segnali a distanze maggiori (10-20 metri invece di 1-2).

> **Nota personale:** Il Frequency Analyzer è il primo tool che apro quando mi trovo davanti a un dispositivo RF sconosciuto. Pero' la sua precisione è limitata - mostra la frequenza approssimativa. Per una misura precisa servono un SDR (HackRF/RTL-SDR) e software come SDR# o GQRX. In engagement reali, uso il Flipper per un'analisi rapida e poi confermo con il HackRF se necessario.

### Radio Scanner

Scansione continua dell'intero spettro Sub-GHz per identificare tutte le sorgenti RF attive in un'area.

**Procedura operativa:**

1. Apri Radio Scanner
2. Seleziona la banda da scansionare (300-928 MHz o sotto-banda)
3. Il display mostra il grafico RSSI per ogni frequenza scansionata
4. I picchi indicano dispositivi attivi
5. Puoi "zoomare" su un range specifico per maggiore dettaglio

**Uso nel pentest:**
- Mappare tutti i dispositivi RF di un edificio target
- Identificare frequenze utilizzate da sistemi di allarme
- Trovare sensori wireless nascosti
- Valutare il "rumore di fondo" RF di un'area

> **Nota personale:** Lo Scanner è lento ma utile per la fase di ricognizione. Lo uso camminando intorno all'edificio target per capire quali frequenze sono attive. Ho scoperto allarmi wireless, sensori di movimento RF e persino baby monitor in questo modo. Il trucco è farlo in orari di attività - quando le persone usano telecomandi e sensori.

### Spectrum Analyzer

Visualizzazione FFT in tempo reale dello spettro RF.

**Differenza dal Radio Scanner:** lo Spectrum Analyzer mostra lo spettro in tempo reale (come un oscilloscopio di frequenza), mentre il Radio Scanner fa una scansione sequenziale salvando i risultati.

**Procedura operativa:**

1. Apri Spectrum Analyzer
2. Imposta frequenza centrale e span
3. Il display mostra il grafico ampiezza vs frequenza
4. I segnali attivi appaiono come picchi
5. Utile per visualizzare interferenze e segnali sovrapposti

**Bande preimpostate:**
- 315 MHz band (US remotes)
- 433 MHz band (EU remotes)
- 868 MHz band (EU domotica)
- 915 MHz band (US ISM)

### Sub-GHz Bruteforcer

Strumento per testare la robustezza di sistemi a codice fisso tramite invio sequenziale di tutti i codici possibili.

**ATTENZIONE:** Usare solo su sistemi di propria proprietà o con autorizzazione scritta.

**Procedura operativa:**

1. Apri Sub-GHz Bruteforcer
2. Seleziona il protocollo target (es. Nice FLO 12-bit, Came 12-bit, Linear, Chamberlain, ecc.)
3. Imposta la frequenza
4. Il Flipper calcola il numero totale di combinazioni:
   - Nice FLO 12-bit: 4096 combinazioni
   - Came 12-bit: 4096 combinazioni
   - Princeton 24-bit: 16.777.216 combinazioni (impraticabile)
   - Linear 10-bit: 1024 combinazioni
   - Chamberlain 9-bit: 512 combinazioni
5. Avvia il bruteforce
6. Il Flipper trasmette tutti i codici in sequenza
7. Se il ricevitore si attiva, il codice valido viene identificato

**Tempi stimati (a velocità standard):**
- 10 bit (1024 codici): ~5 minuti
- 12 bit (4096 codici): ~20 minuti
- 24 bit (16M codici): giorni → impraticabile

**Ottimizzazioni:**
- Ridurre il range se si conosce parte del codice
- Aumentare la velocità di trasmissione (rischia di perdere segnali)
- Usare un'antenna esterna per massimizzare la portata

> **Nota personale:** Il bruteforce è praticabile solo su protocolli a basso numero di bit (10-12). Nice FLO a 12 bit è il target ideale - 4096 combinazioni in ~20 minuti è fattibile durante un engagement. Su Princeton a 24 bit non ne vale la pena: è più veloce catturare il segnale con Read. Ho usato il bruteforcer con successo su un vecchio cancello Came a 12 bit durante un physical pentest - ha trovato il codice in meno di 15 minuti.

### Sub-GHz Rolling Flaws

Analizzatore di vulnerabilità nelle implementazioni di rolling code. Questo tool è specifico per lo studio delle debolezze nei sistemi KeeLoq e simili.

**Procedura operativa:**

1. Cattura almeno 2 codici rolling consecutivi dello stesso telecomando (usando Read)
2. Apri Rolling Flaws
3. Carica i codici catturati
4. Il tool analizza:
   - **Entropia del seed:** quanto è prevedibile la sequenza
   - **Incremento contatore:** se l'incremento è fisso o variabile
   - **Debolezze crittografiche:** chiavi derivate da seriali noti
   - **Finestra di resync:** quanto è permissiva la finestra del ricevitore
5. Output: report con score di sicurezza e vulnerabilità identificate

**Vulnerabilità che può identificare:**
- Implementazioni KeeLoq con manufacturer key debole o nota
- Contatori con incremento prevedibile
- Ricevitori con finestra di resync troppo ampia
- Protocolli con seed derivato dal serial (permettendo predizione)

> **Nota personale:** Questo tool è il più interessante dal punto di vista della ricerca. L'ho usato per analizzare vecchi sistemi Nice e Came e ho trovato che alcune implementazioni hanno chiavi derivate in modo prevedibile dal numero seriale del telecomando. Non funziona su tutti i sistemi - quelli moderni (Came Atomo, FAAC SLH recenti) sono robusti.

### POCSAG Pager

Decoder per il protocollo POCSAG (Post Office Code Standardisation Advisory Group), usato dai pager (cercapersone).

**Background tecnico:**

POCSAG è un protocollo di messaggistica unidirezionale su frequenze dedicate:
- **Italia:** 466.075 MHz (banda pager)
- **UK:** 153.275 MHz
- **US:** 929-932 MHz
- **Data rate:** 512, 1200 o 2400 baud

**Struttura del messaggio POCSAG:**
```
[Preambolo: 576 bit alternati 1010...]
[Sync: 0x7CD215D8]
[Batch 1: 8 codeword da 32 bit]
[Sync]
[Batch 2: 8 codeword]
...
```

Ogni codeword contiene:
- **Address codeword:** RIC (Radio Identity Code) del destinatario + funzione
- **Message codeword:** dati (numerico o alfanumerico)

**Procedura operativa:**

1. Apri POCSAG Pager
2. Imposta frequenza (466.075 MHz per Italia)
3. Il Flipper ascolta e decodifica i messaggi
4. Per ogni messaggio mostra: RIC, funzione, contenuto
5. I messaggi possono essere esportati in log

**Implicazioni di sicurezza:**

I pager POCSAG trasmettono in chiaro. Chiunque con un ricevitore sulla frequenza corretta può leggere tutti i messaggi. Questo è un problema serio in ambienti ospedalieri e di emergenza dove pager sono ancora utilizzati per comunicazioni sensibili.

> **Nota personale:** Ho usato il decoder POCSAG durante un engagement su un ospedale (autorizzato). I pager trasmettevano nomi di pazienti, numeri di stanza e informazioni mediche in chiaro. È stato un finding critico nel report. In Italia i pager sono ancora usati in ospedali, vigili del fuoco e alcune industrie. La frequenza 466.075 MHz è la prima da controllare.

### Weather Station

Decoder per stazioni meteo wireless che trasmettono dati su 433/868 MHz.

**Protocolli supportati:**
- Oregon Scientific v2.1/v3.0
- Acurite
- Lacrosse TX
- Ambient Weather
- Bresser
- Fine Offset / Ecowitt
- Nexus / Digoo

**Dati decodificati:**
- Temperatura
- Umidità
- Pressione barometrica
- Velocità e direzione vento
- Precipitazioni
- ID del sensore
- Batteria bassa
- Canale

**Procedura operativa:**

1. Apri Weather Station
2. Imposta 433.92 MHz (standard EU) o 868 MHz
3. I sensori nelle vicinanze vengono automaticamente decodificati
4. Ogni sensore appare con ID, temperatura, umidità e altri dati
5. I dati vengono aggiornati ad ogni trasmissione del sensore (tipicamente ogni 30-60 secondi)

**Uso nel pentest/OSINT:**
- Identificare la presenza di sistemi wireless nell'area target
- Mappare sensori meteo per capire il livello di adozione IoT
- In fase di ricognizione, la presenza di sensori indica che l'edificio ha automazione wireless potenzialmente vulnerabile

### TPMS Reader

Lettore per sensori di pressione pneumatici (Tire Pressure Monitoring System).

**Background tecnico:**

Ogni pneumatico moderno (obbligatorio in EU dal 2014) contiene un sensore che trasmette periodicamente:
- **Frequenza:** 433.92 MHz (EU) o 315 MHz (US)
- **Modulazione:** OOK o FSK
- **Dati:** ID sensore (32 bit), pressione (kPa), temperatura (C), stato batteria
- **Intervallo:** ogni 60-90 secondi o al rilevamento di variazioni

**Procedura operativa:**

1. Apri TPMS Reader
2. Imposta 433.92 MHz
3. Avvicina il Flipper a un pneumatico (< 2 metri)
4. Attendi 1-2 minuti per la trasmissione
5. Il display mostra: ID sensore, pressione, temperatura

**Implicazioni di sicurezza:**

- **Tracking veicoli:** ogni sensore TPMS ha un ID univoco. Monitorando questi ID è possibile tracciare il passaggio di veicoli specifici senza telecamere.
- **Privacy:** combinando ID TPMS con posizione, si può costruire un profilo di spostamento.
- **Falsificazione:** è teoricamente possibile inviare dati TPMS falsi per accendere la spia nel cruscotto.

> **Nota personale:** Il TPMS reader è più utile di quanto si pensi per OSINT. Durante un engagement ho usato gli ID TPMS per confermare che un veicolo specifico era nel parcheggio dell'edificio target, senza avvicinarmi fisicamente. I sensori trasmettono anche quando l'auto è ferma - serve solo pazienza.

### Restaurant Pager

Decoder per i sistemi di chiamata usati nei ristoranti e fast-food.

**Protocolli comuni:**
- **LRS (Long Range Systems):** 433.92 MHz, OOK
- **HME (HM Electronics):** frequenze variabili
- **JTECH:** 433/868 MHz

**Dati decodificati:**
- ID del pager
- Comando (vibra, LED, beep)
- Gruppo

**Uso nella ricerca di sicurezza:**
- Dimostrare che questi sistemi trasmettono in chiaro
- Testare la possibilità di attivare pager non propri (solo in ambiente controllato)
- Analizzare la robustezza del protocollo

### Enhanced Sub-GHz Chat

Sistema di comunicazione bidirezionale tra Flipper Zero via RF.

**Procedura operativa:**

1. Su entrambi i Flipper: apri Enhanced Sub-GHz Chat
2. Imposta la stessa frequenza (es. 433.92 MHz)
3. Digita un messaggio → Send
4. L'altro Flipper riceve e mostra il messaggio
5. Comunicazione alternata (half-duplex)

**Parametri configurabili:**
- Frequenza
- Potenza TX
- Data rate

**Uso pratico:**
- Comunicazione tra membri del team durante un physical pentest quando non si vogliono usare telefoni
- Test di portata dell'antenna
- Verifica che il modulo RF funzioni correttamente

> **Nota personale:** L'ho usato come comunicazione di backup durante un physical pentest in un edificio con muri spessi dove il cellulare non prendeva. Funziona sorprendentemente bene a 433 MHz attraverso 2-3 muri di calcestruzzo a distanze di 15-20 metri. Non è criptato, quindi non usarlo per comunicazioni sensibili.

### Chief Cooker

Generatore di segnali RF personalizzati da parametri grezzi.

**Procedura operativa:**

1. Apri Chief Cooker
2. Seleziona i parametri:
   - Frequenza (es. 433.92 MHz)
   - Modulazione (OOK/FSK)
   - Data rate
   - Sequenza di bit da trasmettere
3. Genera il segnale
4. Testa la trasmissione

**Uso avanzato:**
- Creare segnali per protocolli non supportati nativamente
- Testare ricevitori con pattern personalizzati
- Reverse engineering: inviare variazioni di un segnale catturato per capire quali bit controllano quale funzione
- Generare sequenze di test per calibrazione

### Genie Door Recorder

Registratore e riproduttore specializzato per telecomandi garage Genie (brand americano molto diffuso).

**Background tecnico:**

I sistemi Genie usano una variante del protocollo Intellicode con rolling code. Alcuni modelli più vecchi usano codice fisso DIP switch.

**Procedura operativa per codice fisso:**
1. Apri Genie Door Recorder
2. Premi il pulsante del telecomando Genie vicino al Flipper
3. Il segnale viene catturato e decodificato
4. Salva → puoi riprodurlo

**Per rolling code (Intellicode):**
- La cattura funziona ma il replay è limitato (il codice è già stato "consumato")
- Utile per analisi del protocollo, non per clonazione diretta

### Protocols Visualizer

Strumento di analisi che mostra graficamente la struttura dei segnali RF decodificati.

**Procedura operativa:**

1. Cattura un segnale con Read o Read RAW
2. Apri il file nel Protocols Visualizer
3. Il display mostra:
   - Waveform del segnale (impulsi alti/bassi)
   - Segmentazione in: preambolo, sync word, header, payload, checksum
   - Bit decodificati con annotazioni
   - Confronto tra pressioni multiple dello stesso telecomando

**Uso nel reverse engineering:**
- Identificare la struttura di protocolli sconosciuti
- Trovare i bit che cambiano tra pressioni successive (contatore rolling code)
- Identificare checksum e CRC
- Capire la lunghezza dei timeslot

> **Nota personale:** Il Visualizer è insostituibile quando stai cercando di capire un protocollo proprietario. L'ho usato per reverse-engineerare un sistema di allarme wireless che usava un protocollo non documentato. Registrando 10-15 trasmissioni diverse e confrontandole nel Visualizer, sono riuscito a identificare i campi: ID sensore, tipo evento (apertura/chiusura/tamper), contatore e checksum.

### Sub-GHz Playlist / Playlist Creator

Gestione e creazione di sequenze di segnali RF da riprodurre in ordine.

**Procedura operativa - Playlist Creator:**

1. Apri Playlist Creator
2. Aggiungi file .sub dalla libreria salvata
3. Imposta l'ordine di riproduzione
4. Configura il delay tra un segnale e l'altro (ms)
5. Salva la playlist

**Procedura operativa - Playlist Player:**

1. Apri Sub-GHz Playlist
2. Seleziona la playlist salvata
3. Premi Play
4. I segnali vengono trasmessi in sequenza

**Uso operativo:**
- Test multipli dispositivi in sequenza (es. testare 5 cancelli diversi)
- Automazione di routine (apertura cancello + garage + luce)
- Demo durante presentazioni di sicurezza
- Stress test: riprodurre lo stesso segnale N volte per testare la robustezza del ricevitore

### Sub-GHz Remote

Interfaccia telecomando con pulsanti configurabili.

**Procedura operativa:**

1. Apri Sub-GHz Remote
2. Assegna un file .sub a ogni pulsante dello schermo
3. Usa i pulsanti per trasmettere i segnali corrispondenti
4. Supporta fino a 4-8 pulsanti (dipende dal firmware)

**Uso pratico:**
- Creare un "telecomando universale" per i tuoi dispositivi RF
- Avere accesso rapido ai segnali più usati
- Durante un pentest: accesso immediato a segnali di test

### Sub-GHz Scheduler

Automazione temporizzata di trasmissioni RF.

**Procedura operativa:**

1. Apri Scheduler
2. Seleziona il file .sub da trasmettere
3. Imposta:
   - Intervallo (es. ogni 10 minuti)
   - Numero di ripetizioni (o infinito)
   - Delay iniziale
4. Avvia lo scheduler
5. Il Flipper trasmette automaticamente secondo il programma

**Uso operativo:**
- Test di persistenza: verificare se un ricevitore si desincronizza dopo ripetute trasmissioni
- Automazione domotica: inviare comandi a intervalli regolari
- Simulazione traffico RF per test ambientali

### Sub-GHz Test

Suite diagnostica per verificare il funzionamento dell'hardware RF.

**Test disponibili:**
- **TX Test:** trasmette un segnale di test e verifica la potenza
- **RX Test:** ascolta e misura il RSSI del segnale ricevuto
- **Antenna Test:** verifica la risposta dell'antenna su diverse frequenze
- **Crystal Test:** verifica la stabilità dell'oscillatore

**Quando usarlo:**
- Dopo una caduta del dispositivo
- Se sospetti problemi hardware
- Per confrontare le prestazioni prima/dopo una modifica hardware
- Per verificare che un'antenna esterna funzioni correttamente

### Shapshup

Strumento creativo per modificare segnali RF registrati.

**Operazioni disponibili:**
- **Stretch:** allunga la durata degli impulsi (es. +5%, +10%)
- **Compress:** accorcia la durata degli impulsi
- **Invert:** inverte alti e bassi
- **Slice:** taglia una porzione del segnale
- **Repeat:** ripete un pattern N volte

**Uso nel reverse engineering:**
- Testare la tolleranza di un ricevitore a variazioni del segnale
- Capire quanto margine ha il timing del protocollo
- Creare varianti di un segnale per test di fuzzing

### Marmalade / Music to Sub-GHz Radio

Tool creativi per convertire audio/musica in segnali RF.

**Uso pratico limitato** - più che altro dimostrativo. Converte pattern audio in sequenze OOK che possono essere "ascoltate" da un ricevitore RF sintonizzato sulla stessa frequenza (come una radio AM artigianale).

### FRSSCAN

Scanner per protocolli FrSky (radiocomandi per droni/aeromodelli).

**Protocolli supportati:** FrSky D8, D16, ACCESS

**Uso:** analisi dei radiocomandi per modellismo RC. Utile per:
- Capire quali frequenze usa un drone
- Analizzare il binding tra trasmettitore e ricevitore
- Studio dei protocolli di telemetria

### SubGHz Toolkit

Raccolta di utility rapide in un'unica interfaccia:
- Quick scan frequenze
- Registrazione rapida con salvataggio automatico
- Conversione tra formati di protocollo
- Visualizzazione rapida dei file .sub salvati

---

