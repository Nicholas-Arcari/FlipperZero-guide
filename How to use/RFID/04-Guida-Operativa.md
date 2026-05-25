## Tool per Tool - Guida Operativa

### RFID 125 kHz - Modulo Principale

Il modulo principale per la gestione dei tag 125 kHz. Accessibile da: `Menu Principale > RFID 125 kHz`.

#### Read (Lettura)

**Procedura step-by-step:**

1. Accendi il Flipper e vai su `RFID 125 kHz`
2. Seleziona `Read`
3. Lo schermo mostra "Reading..." con un'animazione
4. Avvicina il tag alla parte inferiore del Flipper (sotto lo schermo)
5. Mantieni il tag a 0-5 cm, parallelo al Flipper
6. Quando il tag viene letto, il Flipper vibra e mostra:
   - Tipo di protocollo (EM4100, HID, Indala, ecc.)
   - ID del tag in formato esadecimale
   - Per HID: Facility Code e Card Number decodificati
   - Per FDX-B: Country Code e Animal ID
7. Opzioni post-lettura:
   - `Save` - salva su SD card in `/lfrfid/`
   - `Emulate` - inizia a emulare il tag immediatamente
   - `Write` - scrivi su un T5577

**Protocolli riconosciuti automaticamente:**
- EM4100
- HID H10301 (26-bit)
- HID H10302 (37-bit)
- HID H10304 (37-bit)
- Indala (26-bit)
- Indala (raw)
- FDX-B (ISO 11784/11785)
- FDX-A
- EM4305
- Viking
- Jablotron
- Paradox
- PAC/Stanley
- Keri
- Gallagher
- AWID
- Pyramid
- GProxII
- IoProx
- Nexwatch

**Formato file salvato (.rfid):**
```
Filetype: Flipper RFID key
Version: 1
Key type: EM4100
Data: 01 02 03 04 05
```

**Consigli per la lettura:**
- Se il tag non viene letto, prova a ruotarlo di 90 gradi
- Rimuovi cover metalliche dal Flipper
- Prova sia la parte superiore che inferiore del Flipper (l'antenna è sotto)
- Avvicina gradualmente - non sbattere il tag sul Flipper
- Se legge un protocollo sbagliato (es. EM4100 invece di HID), il tag potrebbe essere multi-protocollo o il Flipper confuso - riprova

#### Emulate (Emulazione)

**Procedura step-by-step:**

1. Apri un file .rfid salvato o leggi un tag e scegli `Emulate`
2. Lo schermo mostra "Emulating..." con l'ID visualizzato
3. Avvicina il Flipper al lettore di badge/porta
4. Il Flipper modula il suo campo per simulare il tag
5. Se il lettore accetta l'ID, la porta si apre / il sistema risponde
6. Premi `Back` per interrompere l'emulazione

**Limitazioni dell'emulazione:**
- Funziona solo se il lettore è nella portata del Flipper (2-5 cm)
- Il timing dell'emulazione deve essere preciso - potrebbe non funzionare al primo tentativo
- Alcuni lettori hanno soglie di potenza minima che il Flipper non raggiunge
- L'emulazione HID/Indala è meno affidabile di EM4100
- L'emulazione FDX-B a 134.2 kHz potrebbe non funzionare (il Flipper opera a 125 kHz)

> **Nota personale:** L'emulazione è comoda ma non sempre affidabile. Nel pentest preferisco SEMPRE scrivere su un T5577 piuttosto che usare l'emulazione. Motivi: il T5577 è un tag fisico reale, genera un segnale identico all'originale, non dipende dalla batteria del Flipper, e funziona con qualsiasi lettore. L'emulazione la uso solo per test rapidi in laboratorio o quando non ho un T5577 disponibile.

#### Write (Scrittura)

**Procedura step-by-step:**

1. Leggi un tag o apri un file .rfid salvato
2. Seleziona `Write`
3. Il Flipper chiede di avvicinare un T5577
4. Posiziona il T5577 sulla parte inferiore del Flipper
5. Mantieni fermo - il processo dura 2-3 secondi
6. Se la scrittura va a buon fine, il Flipper vibra e conferma
7. Verifica: vai su `Read` e leggi il T5577 appena scritto
8. L'ID letto deve corrispondere a quello originale

**Cosa succede durante la scrittura:**
1. Il Flipper calcola la configurazione del Block 0 appropriata per il protocollo
2. Scrive il Block 0 (configurazione)
3. Scrive i Block 1-N (dati dell'ID)
4. Il T5577 si riconfigura e inizia a trasmettere come il tag originale

**Problemi comuni nella scrittura:**
- T5577 non riconosciuto: potrebbe essere protetto da password o non essere un vero T5577
- Scrittura fallita: mantieni il T5577 più fermo e vicino
- Verifica fallita: riscrivi - a volte il primo tentativo corrompe un blocco
- T5577 "brickato": se il Block 0 è stato scritto con valori errati, il tag potrebbe non rispondere piu'. In questo caso serve un Proxmark3 per il recovery

#### Add Manually (Aggiunta Manuale)

**Procedura step-by-step:**

1. Vai su `RFID 125 kHz > Add Manually`
2. Seleziona il protocollo:
   - EM4100
   - HID H10301
   - Indala
   - (altri a seconda del firmware)
3. Inserisci i dati:
   - EM4100: 5 byte esadecimali (10 cifre hex)
   - HID: Facility Code (0-255) e Card Number (0-65535)
   - Indala: raw data
4. Salva il file
5. Puoi poi emulare o scrivere su T5577

**Quando usarlo:**
- Quando conosci l'ID da una fonte diversa (log del sistema, foto, social engineering)
- Quando vuoi generare ID specifici per test
- Quando vuoi creare ID incrementali per il fuzzing manuale
- Quando hai dati da un Proxmark3 e vuoi usarli sul Flipper

---

### EM4100 Key Generator

Applicazione per generare ID EM4100 validi in modo rapido.

#### Funzionamento

1. Apri `EM4100 Key Generator` dal menu applicazioni
2. L'app genera un ID EM4100 casuale valido
3. Opzioni:
   - `Generate` - genera un nuovo ID casuale
   - `Save` - salva l'ID come file .rfid
   - `Emulate` - emula immediatamente
   - `Write T5577` - scrivi direttamente su tag

#### Quando Usarlo

- **Fuzzing manuale:** genera ID diversi e testali uno alla volta su un lettore
- **Test di sistema:** verifica che un lettore rifiuti ID non autorizzati
- **Creazione badge di test:** per laboratorio o dimostrazioni
- **Popolamento database:** genera molti ID per test di carico su sistema di accesso

> **Nota personale:** L'EM4100 Key Generator è utile ma limitato. Per il fuzzing serio uso il RFID Fuzzer che è automatizzato. L'EM4100 Key Generator lo uso per creare rapidamente badge di test quando devo dimostrare a un cliente che il suo sistema accetta qualsiasi ID (nessun database di autorizzazione - il lettore apre per chiunque). Succede più spesso di quanto si pensi, specialmente con sistemi standalone non connessi a un controller.

---

### FDX-B Maker

Applicazione per creare tag FDX-B (ISO 11784/11785) con dati personalizzati.

#### Funzionamento

1. Apri `FDX-B Maker`
2. Inserisci i campi:
   - **Country Code:** codice paese ISO 3166 numerico (es. 380 per Italia)
   - **National ID:** numero identificativo (fino a 38 bit, max ~274 miliardi)
   - **Animal Flag:** 1 = animale, 0 = oggetto
   - **Data Flag:** 1 = dati supplementari presenti
3. L'app calcola il frame FDX-B completo con CRC
4. Opzioni: salva, emula o scrivi su T5577

#### Quando Usarlo

- **Studio del protocollo:** capire come è strutturato un ID FDX-B
- **Test lettori veterinari:** verificare che un lettore decodifichi correttamente
- **Ricerca:** studiare il formato e le varianti nazionali
- **Dimostrazione:** mostrare la possibilità di creare ID animali falsi

**Codici paese comuni:**

| Codice | Paese |
|---|---|
| 380 | Italia |
| 276 | Germania |
| 250 | Francia |
| 724 | Spagna |
| 826 | Regno Unito |
| 840 | Stati Uniti |
| 036 | Australia |

> **Nota personale:** Il FDX-B Maker è uno strumento di nicchia. L'ho usato esattamente due volte: una per verificare il funzionamento di un lettore veterinario in un laboratorio, una per dimostrare in una presentazione che i microchip animali non hanno alcuna protezione crittografica. In teoria si potrebbe creare un microchip falso per un animale rubato, ma nella pratica il chip deve essere fisicamente impiantato da un veterinario e registrato nell'anagrafe - il problema non è tecnico ma burocratico. Non ci sono quasi mai implicazioni di pentesting reale.

---

### RFID Fuzzer

Lo strumento più potente per il testing attivo dei sistemi RFID 125 kHz. Genera e trasmette ID in sequenza per scoprire vulnerabilità.

#### Modalità di Fuzzing

**1. Sequential (Sequenziale):**
- Incrementa l'ID di 1 ad ogni iterazione
- Parte da un valore base (default: 00:00:00:00:00) o da un ID letto
- Utile per scoprire ID validi quando conosci il range
- Velocità: circa 3-5 ID al secondo

**2. Random:**
- Genera ID casuali
- Utile per test di robustezza del lettore
- Meno efficiente del sequenziale per trovare ID validi
- Utile per stress-testing

**3. BF (Brute Force) su byte specifico:**
- Permette di fissare i byte noti e fuzzare solo quelli sconosciuti
- Esempio: conosci i primi 3 byte (version + parte dell'ID) e fuzzi gli ultimi 2
- Molto più veloce del brute force completo
- Ideale quando hai informazioni parziali

#### Protocolli Supportati dal Fuzzer

- EM4100
- HID H10301 (fuzzing su FC, CN o entrambi)
- Indala (26-bit)
- PAC/Stanley
- Viking
- Jablotron
- Pyramid

#### Procedura Operativa per Pentest

1. **Fase di ricognizione:**
   - Leggi almeno un badge valido (social engineering, dumpster diving)
   - Identifica il protocollo e l'ID
   - Per HID: annota il Facility Code
   
2. **Configurazione del Fuzzer:**
   - Seleziona il protocollo corretto
   - Imposta l'ID base (il badge che hai letto)
   - Scegli la modalità (sequential partendo dall'ID noto è la più efficace)
   
3. **Esecuzione:**
   - Posiziona il Flipper sul lettore target
   - Avvia il fuzzing
   - Osserva il comportamento del lettore (LED, suoni, apertura)
   - Il Flipper mostra l'ID corrente sullo schermo
   
4. **Analisi risultati:**
   - Se il lettore apre: hai trovato un ID valido - salvalo
   - Se il lettore va in blocco/errore: hai trovato un bug - documenta
   - Se il lettore non reagisce mai: il sistema potrebbe avere un database restrittivo (buon segno per la sicurezza)

#### Limiti del Fuzzing

- **Velocità:** 3-5 ID/secondo significa che un brute force completo su EM4100 (2^40 possibilità) richiederebbe migliaia di anni
- **Rilevamento:** un sistema monitorato potrebbe generare allarmi dopo molti tentativi falliti
- **Portata:** devi mantenere il Flipper sul lettore per tutta la durata - poco discreto
- **Blocco lettore:** alcuni lettori si bloccano dopo N tentativi falliti rapidi (rate limiting)

> **Nota personale:** Il fuzzing RFID è utile ma va usato strategicamente, non alla cieca. Se hai letto un badge HID con FC:42 CN:500, non fare brute force su tutto lo spazio - prova CN:1-1000 (numeri bassi, spesso assegnati per primi). In un engagement ho trovato che un parcheggio aziendale accettava qualsiasi EM4100 con i primi 2 byte corretti (il "version number" del lotto di badge). Bastava leggere un badge, mantenere i primi 2 byte e cambiare gli ultimi 3 - qualsiasi combinazione apriva. Il fuzzer ha trovato questo in meno di 5 minuti.

---

### T5577 MultiWriter

Strumento per la clonazione automatica rapida di tag su T5577.

#### Funzionamento

1. Apri `T5577 MultiWriter`
2. Seleziona la sorgente:
   - File .rfid salvato su SD card
   - Ultimo tag letto in memoria
3. Posiziona un T5577 vuoto sul Flipper
4. L'app scrive automaticamente:
   - Block 0 (configurazione del protocollo)
   - Block 1-N (dati dell'ID)
5. Conferma con vibrazione
6. Puoi immediatamente posizionare un altro T5577 per una nuova copia

#### Differenze dal Write Standard

| Caratteristica | Write (modulo RFID) | T5577 MultiWriter |
|---|---|---|
| **Fonte dati** | Solo tag appena letto | File salvato o tag letto |
| **Flusso** | Read > Write (2 passaggi) | Select file > Write (1 passaggio) |
| **Copie multiple** | Richiede ri-lettura | Posiziona e scrivi in loop |
| **Verifica** | Manuale | Automatica (legge dopo scrittura) |

#### Quando Usarlo

- Devi creare più copie dello stesso badge (es. per un team di pentest)
- Devi preparare badge prima dell'engagement (clonazione offline da file)
- Duplicazione rapida per il cliente che vuole badge di backup
- Test in laboratorio con molti tag

> **Nota personale:** Il MultiWriter è il mio tool preferito per preparare un engagement. La sera prima, prendo tutti i file .rfid raccolti durante la ricognizione e li scrivo su T5577 - uno per ogni badge che devo clonare. Li etichetto con nastro adesivo (es. "Porta principale EM4100", "Parcheggio HID FC:42 CN:500"). Il giorno dell'engagement ho tutto pronto in tasca.

---

### T5577 Raw Writer

Strumento avanzato per la scrittura diretta dei registri del T5577, senza passare per la decodifica del protocollo.

#### Funzionamento

1. Apri `T5577 Raw Writer`
2. Seleziona il blocco da scrivere (0-7, Page 0 o Page 1)
3. Inserisci il valore a 32 bit in esadecimale
4. Posiziona il T5577 sul Flipper
5. L'app scrive il blocco specificato

#### Uso Avanzato

**Scrittura del Block 0 (configurazione):**
- Permette di configurare manualmente la modulazione, il data rate, il numero di blocchi
- Utile per protocolli non supportati nativamente dal Flipper
- **ATTENZIONE:** un Block 0 errato può rendere il T5577 illeggibile

**Scrittura dei blocchi dati:**
- Inserisci direttamente i dati raw senza dover passare per un file .rfid
- Utile per replicare dati ottenuti da un Proxmark3 o da un analizzatore esterno

**Impostazione password:**
- Scrivi il Block 7 con la password desiderata
- Poi scrivi il Block 0 con il bit PWD (bit 29) settato a 1
- D'ora in poi ogni scrittura richiederà la password

**Recovery di un T5577:**
- Se un T5577 ha il Block 0 corrotto e non risponde normalmente
- Prova a scrivere il Block 0 con una configurazione nota buona (es. 0x00148040 per EM4100)
- Se protetto da password sconosciuta: serve un Proxmark3 per il brute force (il Flipper non supporta il password cracking del T5577)

#### Esempio Pratico: Configurare un T5577 come EM4100 da Zero

```
1. Scrivi Block 0: 0x00148040
   (ASK/Manchester, RF/64, 2 blocchi, nessuna password)

2. Scrivi Block 1: 0xFF01020304
   (primi 32 bit del frame EM4100: header 9x1 + primi nibble)

3. Scrivi Block 2: 0x0506070800
   (ultimi nibble + parità colonne + stop bit)

Risultato: il T5577 si comporta come un EM4100 con ID 01:02:03:04:05
```

> **Nota personale:** Il Raw Writer è lo strumento che uso quando il metodo standard non funziona. Una volta ho avuto un tag da un sistema di accesso industriale che il Flipper leggeva come "Unknown protocol". Con il Proxmark3 ho decodificato i raw data e la configurazione. Poi con il Raw Writer ho scritto esattamente quei valori su un T5577 - e ha funzionato. È lo strumento per quando devi andare a basso livello e non puoi affidarti all'automazione.

---

### DCF77 Clock Sync

Ricevitore e decodificatore del segnale orario DCF77.

#### Che cos'è DCF77

DCF77 è un segnale radio trasmesso a 77.5 kHz dalla stazione di Mainflingen (Germania). Trasporta informazioni di data e ora con precisione atomica ed è usato da milioni di orologi radiocontrollati in Europa.

#### Caratteristiche Tecniche

- **Frequenza:** 77.5 kHz (non esattamente 125 kHz ma nella gamma LF)
- **Modulazione:** ASK con riduzione di ampiezza al 25%
- **Frame:** 1 minuto = 59 bit (1 bit al secondo)
- **Portata:** ~2000 km dalla Germania
- **Precisione:** microsecondo (derivata da orologio atomico al cesio)

#### Struttura del Frame DCF77 (59 bit)

| Secondo | Campo | Descrizione |
|---|---|---|
| 0 | Start | Inizio minuto (nessuna riduzione) |
| 1-14 | Meteo | Dati meteorologici criptati |
| 15 | Antenna | Antenna di riserva attiva |
| 16 | CEST/CET | Cambio ora legale imminente |
| 17-18 | Fuso | 01=CET, 10=CEST |
| 19 | Leap | Secondo intercalare imminente |
| 20 | Start time | Sempre 1 (inizio blocco tempo) |
| 21-27 | Minuti | BCD (0-59) + parità |
| 28 | P1 | Parità minuti |
| 29-34 | Ore | BCD (0-23) + parità |
| 35 | P2 | Parità ore |
| 36-41 | Giorno | BCD (1-31) |
| 42-44 | Giorno sett. | 1=Lun ... 7=Dom |
| 45-49 | Mese | BCD (1-12) |
| 50-57 | Anno | BCD (00-99) |
| 58 | P3 | Parità data |

#### Uso nel Flipper

1. Apri `DCF77 Clock Sync`
2. Il Flipper usa l'antenna LF come ricevitore
3. Decodifica i bit uno alla volta (richiede ~1 minuto per un frame completo)
4. Mostra data e ora decodificate
5. In Italia il segnale è ricevibile ma con qualità variabile (distanza dalla Germania)

#### Uso Pratico

- Studio del protocollo DCF77
- Verifica della ricezione nella propria zona
- Debug di orologi radiocontrollati
- Comprensione della codifica BCD e dei segnali orari

---

### DCF77 Transmitter

Generatore di segnale DCF77 artificiale.

#### Funzionamento

1. Apri `DCF77 Transmitter`
2. Imposta data e ora desiderate (o usa l'ora corrente del Flipper)
3. Avvia la trasmissione
4. Il Flipper genera un segnale DCF77 a 77.5 kHz tramite l'antenna LF
5. Gli orologi radiocontrollati nel raggio di pochi centimetri si sincronizzano

#### Uso Pratico

- **Test orologi radiocontrollati:** forza la sincronizzazione con un'ora specifica
- **Debug:** verifica se un orologio decodifica correttamente DCF77
- **Dimostrazione:** mostra come un segnale orario possa essere spoofato
- **Impostazione ora:** imposta l'ora corretta su orologi che non ricevono DCF77 nella propria zona

#### Portata e Limiti

- La portata del Flipper come trasmettitore DCF77 è di pochi centimetri (1-5 cm)
- Il segnale reale DCF77 ha una potenza di 50 kW - il Flipper genera milliwatt
- Funziona solo con orologi posti molto vicino al Flipper
- Non interferisce con il segnale DCF77 reale (troppo debole)

> **Nota personale:** Il DCF77 Transmitter è divertente ma di utilità quasi nulla nel pentesting. L'ho usato una sola volta per sincronizzare un vecchio orologio da scrivania che non prendeva il segnale. Come proof-of-concept dello spoofing dei segnali orari è interessante, ma nella pratica non ci sono scenari di attacco reali con la portata del Flipper.

---

### NFC/RFID Detector

Rilevatore passivo di campi NFC (13.56 MHz) e RFID (125 kHz).

#### Funzionamento

1. Apri `NFC/RFID Detector`
2. Il Flipper attiva le antenne in modalità ricezione passiva (non genera campo)
3. Lo schermo mostra due indicatori:
   - **LF (125 kHz):** barra di intensità del campo LF rilevato
   - **HF (13.56 MHz):** barra di intensità del campo HF rilevato
4. Avvicina il Flipper a potenziali lettori
5. Se rileva un campo, l'indicatore corrispondente si illumina

#### Interpretazione dei Risultati

| Campo rilevato | Significato |
|---|---|
| Solo LF | Lettore RFID 125 kHz (badge tradizionale) |
| Solo HF | Lettore NFC 13.56 MHz (MIFARE, iCLASS, ecc.) |
| LF + HF | Lettore dual-frequency (supporta entrambi) |
| Nessuno | Nessun lettore attivo nelle vicinanze / lettore spento |

#### Uso nel Pentesting

**Mappatura degli accessi:**
1. Cammina lungo i corridoi dell'edificio target con il Detector attivo
2. Annota ogni punto dove rilevi un campo (porta, tornello, ascensore)
3. Classifica i lettori per tipo (LF/HF/dual)
4. Questa mappa è fondamentale per pianificare l'engagement

**Identificazione lettori nascosti:**
- Lettori sotto intonaco o dietro pannelli
- Lettori incassati nel telaio della porta
- Lettori camuffati (sembrare interruttori, placchette)
- Lettori in punti inaspettati (cassetti, armadietti)

**Valutazione della tecnologia:**
- LF puro = sistema legacy, probabilmente clonabile
- HF puro = sistema più moderno, potrebbe avere crittografia
- Dual = sistema con migrazione in corso o alta sicurezza

> **Nota personale:** Il Detector è il PRIMO tool che uso in un engagement di physical pentest. Prima di qualsiasi tentativo di lettura o emulazione, mappo l'intero edificio. In 5 minuti di camminata so esattamente quanti lettori ci sono, dove sono e di che tipo sono. In un engagement per una banca, ho scoperto un lettore LF nascosto dietro un pannello decorativo accanto all'ingresso del caveau - il Detector lo ha rilevato a 10 cm anche attraverso il pannello. Era un sistema legacy EM4100 che nessuno aveva mai aggiornato, nonostante il resto della banca usasse HID iCLASS SE. Quel lettore dimenticato era la vulnerabilità più critica dell'intero sistema.

---

