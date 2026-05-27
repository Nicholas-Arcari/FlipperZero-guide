## Tool per Tool - Guida Operativa

### Infrared (Applicazione Principale)

L'applicazione Infrared integrata nel firmware è il tool principale per tutte le operazioni IR.

#### Learn New Remote

Procedura step-by-step per catturare un segnale IR:

1. Vai su **Infrared** dal menu principale
2. Seleziona **Learn New Remote**
3. Punta il telecomando sorgente verso il **ricevitore IR** del Flipper (la finestra scura nella parte superiore del dispositivo)
4. Premi il tasto che vuoi registrare sul telecomando
5. Il Flipper visualizzerà il risultato:
   - Se il protocollo è riconosciuto: mostra **nome protocollo**, **address** e **command**
   - Se il protocollo non è riconosciuto: mostra **RAW** con la durata totale
6. Premi **Save** per salvare il segnale
7. Assegna un **nome descrittivo** (es. "Power", "Vol_Up", "Temp_24")
8. Ripeti per ogni tasto che vuoi catturare

**Suggerimenti operativi:**
- Mantieni il telecomando sorgente a **5-15 cm** dal Flipper per la cattura - non troppo vicino (saturazione), non troppo lontano (errori)
- Premi il tasto **una sola volta** con decisione - non tenerlo premuto (per evitare repeat code)
- Se ottieni un risultato RAW per un protocollo che dovrebbe essere decodificato, prova ad avvicinarti e ripetere
- Per segnali AC, assicurati di catturare l'intero frame (sono lunghi - attendi che il Flipper confermi la ricezione completa)

#### Send (Universal Remote)

Il Flipper include un database di segnali IR pre-caricati per i dispositivi più comuni:

1. Vai su **Infrared** → **Universal Remotes**
2. Seleziona la categoria (TV, AC, Audio, ecc.)
3. Il Flipper invierà segnali comuni per quella categoria
4. Per le TV: invia sequenze di Power Off per le marche più diffuse

#### Saved Remotes

Gestione dei telecomandi salvati:

1. Vai su **Infrared** → **Saved Remotes**
2. Seleziona il file del telecomando
3. Scegli il comando da inviare
4. Premi **Send** - il Flipper trasmetterà il segnale

I file vengono salvati in `/ext/infrared/` sulla SD card in formato `.ir`.

### Cross Remote

Telecomando universale multi-vendor che permette di **combinare comandi da dispositivi diversi** in un unico telecomando virtuale.

**Caso d'uso tipico:** In una sala riunioni hai TV Samsung, proiettore Epson e soundbar LG. Con Cross Remote puoi creare un profilo che accende/spegne tutti e tre con un singolo telecomando.

**Procedura:**

1. Apri **Cross Remote**
2. Crea un nuovo profilo o seleziona uno esistente
3. Aggiungi comandi da telecomandi diversi (file `.ir` salvati o catturati al momento)
4. Assegna ogni comando a un tasto virtuale
5. Usa il profilo per controllare tutti i dispositivi

> **Nota personale:** Cross Remote è lo strumento operativo più pratico per il pentest fisico. Prepari in anticipo un profilo con i comandi "Power Off" per TV, proiettori e display delle marche più comuni nell'edificio target. In pochi secondi puoi spegnere tutto in una sala riunioni. È molto più veloce che cercare il file .ir giusto per ogni dispositivo.

### IR Decoder

Tool di analisi e reverse engineering per segnali IR ricevuti.

**Funzionalità:**
- Mostra il **protocollo** identificato (NEC, RC5, RC6, SIRC, Samsung, ecc.)
- Visualizza **address e command** in formato esadecimale
- Per segnali RAW: mostra la **sequenza completa** di timing
- Permette di analizzare la **struttura del frame** per protocolli sconosciuti

**Procedura:**

1. Apri **IR Decoder**
2. Seleziona **Start Decoding**
3. Punta un telecomando verso il Flipper e premi un tasto
4. Analizza i dati visualizzati
5. Ripeti per tasti diversi per mappare l'intero telecomando

**Uso nel reverse engineering:**

- Cattura lo stesso tasto più volte per verificare la consistenza
- Confronta tasti diversi per identificare la struttura (quali bit cambiano)
- Per RC5/RC6: osserva il toggle bit che cambia tra pressioni successive
- Per segnali AC: cattura piccoli cambiamenti (es. 24→25 gradi) per isolare i bit della temperatura

### IR Scope

Oscilloscopio IR integrato per la visualizzazione delle forme d'onda.

**Funzionalità:**
- Visualizza la **waveform** del segnale IR in tempo reale
- Mostra i **tempi dei burst e space** graficamente
- Permette di analizzare il **duty cycle** e la **frequenza portante**
- Utile per diagnosticare problemi di timing

**Procedura:**

1. Apri **IR Scope**
2. Punta un telecomando verso il Flipper
3. Premi un tasto - la waveform apparirà sullo schermo
4. Analizza la forma d'onda: burst (parti alte), space (parti basse)
5. Misura i tempi per verificare la conformità al protocollo

**Uso pratico:**

- Verificare se un segnale catturato ha timing corretti
- Diagnosticare perchè un segnale RAW non funziona (burst troppo corti, space irregolari)
- Confrontare il segnale originale del telecomando con quello riprodotto dal Flipper
- Identificare la frequenza portante analizzando la struttura dei burst

### IR Remote

Applicazione per caricare e utilizzare file `.ir` come telecomandi virtuali.

**Procedura:**

1. Apri **IR Remote**
2. Naviga nella SD card e seleziona un file `.ir`
3. L'applicazione presenta i comandi contenuti nel file come pulsanti
4. Premi il comando desiderato per trasmetterlo

**Gestione file .ir:**

I file possono essere:
- Creati dal Flipper tramite Learn New Remote
- Scaricati da repository online (Flipper-IRDB è il più grande)
- Creati manualmente con un editor di testo seguendo il formato corretto
- Trasferiti dalla SD card via qFlipper o app mobile

### IR Blaster

Tool per l'invio massivo o burst di segnali IR.

**Funzionalità:**
- Invio **ripetuto e rapido** di segnali IR
- Modalità **burst** per saturare ricevitori
- Utile per test di **stress** su ricevitori IR
- Può ciclare tra diversi segnali rapidamente

**Caso d'uso nel pentest:**

IR Blaster è lo strumento per l'approccio "TV-B-Gone": ciclare rapidamente attraverso centinaia di comandi Power Off per marche diverse. In modalità burst, il Flipper può inviare un comando dopo l'altro senza pausa, massimizzando la probabilità di spegnere un dispositivo sconosciuto.

**Procedura:**

1. Apri **IR Blaster**
2. Seleziona il set di segnali da trasmettere (o usa il database universale)
3. Seleziona la modalità (singolo, burst, ciclico)
4. Punta verso il dispositivo target
5. Avvia la trasmissione

### IR Intervalometer

Controllo remoto per scatto automatico di fotocamere DSLR e mirrorless compatibili con trigger IR.

**Fotocamere compatibili:**
- Nikon (serie D3000, D5000, D7000, Z5, Z6, Z7, ecc.)
- Canon (selezionate - molte Canon usano telecomandi radio, non IR)
- Sony (serie Alpha con ricevitore IR)
- Pentax, Olympus/OM System (modelli con ricevitore IR)
- Fujifilm (modelli selezionati)

**Funzionalità:**
- Scatto singolo a distanza
- Scatto intervallato (time-lapse) con intervallo configurabile
- Ritardo iniziale configurabile

**Procedura:**

1. Apri **IR Intervalometer**
2. Seleziona il produttore della fotocamera
3. Imposta l'intervallo tra gli scatti (es. 5 secondi)
4. Imposta il numero di scatti o lascia in continuo
5. Posiziona il Flipper di fronte al ricevitore IR della fotocamera (di solito frontale)
6. Avvia

> **Nota personale:** L'Intervalometer è un tool di nicchia, ma sorprendentemente utile. L'ho usato per time-lapse durante sorveglianza fisica in engagement - il Flipper controlla una DSLR su treppiede che documenta accessi a un edificio. Non è il suo uso principale, ma funziona.

### IR Transfer

Sistema per il trasferimento di file tra due Flipper Zero utilizzando la comunicazione IR.

**Funzionalità:**
- Invio di piccoli file da un Flipper all'altro via IR
- Nessuna connessione wireless necessaria (no BT, no WiFi)
- Utile in ambienti dove le trasmissioni radio sono monitorate o vietate

**Limiti:**
- La velocità è molto bassa (IR non è progettato per trasferimento dati massivo)
- Richiede line-of-sight e distanza ravvicinata (1-3 metri)
- Adatto solo per file piccoli (segnali IR, piccole configurazioni)

**Procedura:**

1. Apri **IR Transfer** su entrambi i Flipper
2. Sul Flipper mittente: seleziona **Send File** e scegli il file
3. Sul Flipper ricevente: seleziona **Receive**
4. Posiziona i due Flipper uno di fronte all'altro a 50 cm - 1 metro
5. Avvia il trasferimento

### Flame RNG

Generatore di numeri casuali basato su segnali IR e tool di stress test per ricevitori.

**Funzionalità:**
- Genera e trasmette segnali IR casuali
- Usato per testare la robustezza dei ricevitori IR
- Può causare comportamenti inaspettati in dispositivi che non gestiscono correttamente segnali non validi

**Uso nel pentest:**

Flame RNG può rivelare vulnerabilità in ricevitori IR che:
- Non filtrano correttamente segnali malformati
- Crashano o si bloccano ricevendo dati imprevisti
- Eseguono azioni non volute con combinazioni casuali di address/command

### Telecomandi Specifici

#### Hitachi AC Remote

Telecomando dedicato per climatizzatori Hitachi. Implementa il protocollo proprietario Hitachi con frame lunghi (tipicamente 104 bit per i modelli più comuni).

**Funzionalità:**
- Controllo temperatura (16-32 gradi)
- Modalità (Cool, Heat, Dry, Fan, Auto)
- Velocità ventola
- Swing alette
- Power On/Off

#### Midea AC Remote

Telecomando per climatizzatori Midea. Il protocollo Midea è relativamente semplice rispetto ad altri produttori AC (circa 48 bit per frame), il che lo rende più affidabile nella cattura e riproduzione.

#### Mitsubishi AC Remote

Telecomando per climatizzatori Mitsubishi Electric. Frame da 144 bit (18 byte) con checksum proprietario. Uno dei protocolli AC più complessi.

#### Xbox Control

Controllo IR per console Xbox (Xbox One e Xbox Series X/S). Le console Xbox hanno un ricevitore IR frontale per i telecomandi multimediali.

**Comandi disponibili:**
- Power On/Off
- Guide button
- Navigazione menu
- Controlli media (Play, Pause, Stop, Skip)

#### Netflix TV Remote

Telecomando ottimizzato per la navigazione Netflix su smart TV compatibili. Alcuni TV hanno un ricevitore IR dedicato con comandi specifici per app streaming.

#### R.O.B. Control

Controllo IR per il **Robotic Operating Buddy** (R.O.B.) del Nintendo NES, rilasciato nel 1985. Il R.O.B. riceve comandi tramite flash IR dallo schermo della TV. Questo tool emula quei segnali.

Comandi: Open Arms, Close Arms, Raise, Lower, Spin CW, Spin CCW, Test.

Un tool di nicchia ma affascinante per chi colleziona hardware retrogaming.

#### XRemote

Telecomando universale avanzato con interfaccia configurabile. Permette di:
- Definire layout personalizzati dei pulsanti
- Combinare comandi da marche diverse
- Creare macro (sequenze di comandi)
- Importare/esportare configurazioni

XRemote è il tool più flessibile per l'uso quotidiano del Flipper come telecomando universale.

### LIDAR Emulator

Emulatore di segnali IR simili a quelli emessi da sensori di prossimità e LIDAR a basso costo.

**Contesto:** Molti robot, aspirapolvere automatici, sistemi di parcheggio e barriere usano sensori IR per rilevare ostacoli. Questi sensori emettono impulsi IR e misurano il riflesso per calcolare la distanza.

**Funzionalità:**
- Emette pattern IR che simulano la presenza di un ostacolo a distanze configurabili
- Può ingannare sensori di prossimità IR semplici
- Utile per testare sistemi di sicurezza basati su sensori IR

**Limiti:**
- Funziona solo con sensori IR semplici (non con LIDAR a tempo di volo reali)
- La potenza del LED del Flipper limita la distanza operativa
- Sensori più sofisticati (es. LIDAR ToF) non sono ingannabili con questo metodo

---

