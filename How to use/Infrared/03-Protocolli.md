## Protocolli Dettagliati

### NEC - Il Protocollo Dominante

NEC è di gran lunga il protocollo IR più diffuso al mondo. Lo trovi in TV, soundbar, set-top box, proiettori, LED strip controller e centinaia di altri dispositivi consumer. Capire NEC nel dettaglio è fondamentale.

#### Struttura del Frame NEC Standard

Un frame NEC completo è composto da:

```
[Leader Code] [Address] [Address Inverted] [Command] [Command Inverted] [Stop Bit]
```

**1. Leader Code (AGC Burst):**
- **9000 microsecondi** di burst (portante a 38 kHz attiva)
- **4500 microsecondi** di space (silenzio)
- Totale: 13.5 ms
- Scopo: segnalare al ricevitore l'inizio di una trasmissione e permettere al circuito AGC (Automatic Gain Control) di stabilizzarsi

**2. Address (8 bit):**
- Indirizzo del dispositivo (identifica il tipo di apparecchio)
- Bit 0 trasmesso per primo (LSB first)

**3. Address Inverted (8 bit):**
- Complemento logico dell'indirizzo (ogni bit invertito)
- Serve come **verifica di integrità**: se Address XOR Address_Inverted != 0xFF, il frame è corrotto

**4. Command (8 bit):**
- Il comando effettivo (Power, Volume Up, Channel Down, ecc.)
- Bit 0 trasmesso per primo (LSB first)

**5. Command Inverted (8 bit):**
- Complemento logico del comando
- Stessa funzione di verifica dell'Address Inverted

**6. Stop Bit:**
- Un ultimo burst da 560 microsecondi per terminare il frame

#### Codifica dei Bit NEC - Pulse Distance Encoding

NEC usa la **codifica a distanza di impulso** (pulse distance encoding):

- **Bit 0:** burst 560 us + space 560 us (totale ~1.125 ms)
- **Bit 1:** burst 560 us + space 1690 us (totale ~2.25 ms)

Il burst è sempre 560 microsecondi. La differenza tra 0 e 1 sta nella durata dello **space** che segue.

```
Bit 0:  |####|    |      (560us burst + 560us space)
Bit 1:  |####|         |  (560us burst + 1690us space)
```

#### Repeat Code NEC

Se un tasto viene tenuto premuto, dopo il primo frame completo il trasmettitore invia **repeat code** ogni 108 ms:

- **9000 us** burst
- **2250 us** space (metà del leader code space)
- **560 us** burst (stop bit)

Il repeat code NON contiene dati - dice solo "ripeti l'ultimo comando". Il ricevitore continua ad eseguire l'azione precedente.

#### Variante NEC Extended (16-bit Address)

Alcuni produttori usano una variante dove i 16 bit di indirizzo non sono più complementari tra loro, ma contengono un indirizzo effettivo a 16 bit:

```
[Leader] [Address Low 8bit] [Address High 8bit] [Command] [Command Inverted] [Stop]
```

Il Flipper gestisce sia NEC standard che extended.

#### Timing Completo NEC

| Elemento | Durata |
|---|---|
| Leader burst | 9000 us |
| Leader space | 4500 us |
| Bit burst | 560 us |
| Bit 0 space | 560 us |
| Bit 1 space | 1690 us |
| Repeat burst | 9000 us |
| Repeat space | 2250 us |
| Stop bit | 560 us |
| Frame completo (32 bit) | ~67.5 ms |
| Periodo ripetizione | 108 ms |

> **Nota personale:** NEC è il protocollo che incontrerai nel 60-70% dei casi. Quando il Flipper decodifica un segnale come NEC, puoi fidarti - la struttura è robusta e il riconoscimento è affidabile. Se vedi Address e Command con i rispettivi complementi che tornano, il segnale è stato catturato correttamente.

### RC5 - Philips (Manchester Encoding)

RC5 è il protocollo sviluppato da Philips nel 1987, ancora diffusissimo nei dispositivi europei. La differenza fondamentale rispetto a NEC è l'uso della **codifica Manchester** (biphase).

#### Struttura del Frame RC5

Un frame RC5 standard è composto da **14 bit** in totale:

```
[S1] [S2] [T] [Address: 5 bit] [Command: 6 bit]
```

**S1 (Start bit 1):** sempre 1 - indica l'inizio del frame
**S2 (Start bit 2):** sempre 1 in RC5 classico (diventa il 7mo bit del comando in RC5 Extended)
**T (Toggle bit):** cambia stato (0→1 o 1→0) **ogni volta che il tasto viene premuto e rilasciato**. Se il tasto resta premuto, il toggle bit non cambia. Questo permette al ricevitore di distinguere "pressione continua" da "due pressioni rapide".
**Address (5 bit):** indirizzo del dispositivo (0-31)
**Command (6 bit):** comando (0-63), estendibile a 7 bit con S2

#### Codifica Manchester (Biphase)

Nella codifica Manchester, ogni bit occupa un periodo fisso (circa **1778 us** per RC5, corrispondente a una frequenza di bit di ~562 Hz) e contiene **sempre una transizione** al centro:

- **Bit 0:** livello alto nella prima metà, transizione alto→basso al centro
- **Bit 1:** livello basso nella prima metà, transizione basso→alto al centro

```
Bit 0:  |####|____|     (alto poi basso)
Bit 1:  |____|####|     (basso poi alto)
```

La portante a 36 kHz (nota: RC5 usa 36 kHz, non 38 kHz) viene attivata durante le fasi "alto".

#### Parametri RC5

| Parametro | Valore |
|---|---|
| Frequenza portante | 36 kHz |
| Periodo di bit | 1778 us |
| Metà periodo (half-bit) | 889 us |
| Numero bit totali | 14 |
| Durata frame | ~24.9 ms |
| Indirizzi possibili | 32 (5 bit) |
| Comandi possibili | 64/128 (6/7 bit) |

#### Differenze Operative tra RC5 e NEC

- RC5 usa **36 kHz** come portante (NEC usa 38 kHz) - il ricevitore del Flipper (TSOP75338, ottimizzato per 38 kHz) riceve RC5 con sensibilità leggermente ridotta
- RC5 ha il **toggle bit** - NEC no. Questo può causare confusione: se catturi un segnale RC5 e lo ritrasmetti, il toggle bit potrebbe essere nel valore "sbagliato" e il dispositivo potrebbe interpretarlo come "tasto ancora premuto" anzichè "nuova pressione"
- RC5 ha meno combinazioni (32 indirizzi x 128 comandi) rispetto a NEC (256 indirizzi x 256 comandi, o 65536 x 256 in NEC extended)

### RC6 - Philips (Evoluzione RC5)

RC6 è l'evoluzione di RC5, sviluppata da Philips per superare i limiti del predecessore. Aggiunge complessità strutturale ma resta basata su codifica Manchester.

#### Struttura del Frame RC6

```
[Leader] [Start Bit] [Mode: 3 bit] [Trailer: 1 bit] [Control: 8 bit] [Information: 8 bit]
```

**Leader:** 2666 us burst + 889 us space (6T + 2T, dove T = 444 us)
**Start bit:** sempre 1
**Mode (3 bit):** definisce la modalità (Mode 0 è il più comune per consumer)
**Trailer (Toggle) bit:** equivalente del toggle di RC5, ma con timing **doppio** (2T per half-bit invece di T) - questo è il tratto più caratteristico di RC6
**Control (8 bit):** indirizzo del dispositivo
**Information (8 bit):** comando

#### Peculiarità del Trailer Bit

Il trailer bit (toggle) di RC6 ha un timing diverso da tutti gli altri bit:

- Bit normali: half-bit = 444 us (1T)
- Trailer bit: half-bit = 889 us (2T)

Questo rende il protocollo più complesso da decodificare e da riprodurre. Il Flipper gestisce correttamente questa peculiarità.

#### Parametri RC6

| Parametro | Valore |
|---|---|
| Frequenza portante | 36 kHz |
| Periodo base (T) | 444 us |
| Half-bit normale | 444 us (1T) |
| Half-bit trailer | 889 us (2T) |
| Leader | 2666 us burst + 889 us space |
| Indirizzi possibili | 256 (8 bit) |
| Comandi possibili | 256 (8 bit) |

### Sony SIRC - Pulse Width Encoding

Sony usa il protocollo SIRC (Sony Infrared Remote Control), con una struttura diversa da NEC e RC5.

#### Struttura del Frame SIRC

Esistono tre varianti:

- **SIRC 12 bit:** 7 bit command + 5 bit address
- **SIRC 15 bit:** 7 bit command + 8 bit address
- **SIRC 20 bit:** 7 bit command + 5 bit address + 8 bit extended

```
[Leader] [Command: 7 bit] [Address: 5/8 bit] [Extended: 8 bit opzionale]
```

**Leader:** 2400 us burst + 600 us space

#### Codifica dei Bit SIRC - Pulse Width Encoding

SIRC usa la **codifica a larghezza di impulso** (pulse width encoding), diversa dalla pulse distance di NEC:

- **Bit 0:** burst 600 us + space 600 us (totale 1.2 ms)
- **Bit 1:** burst 1200 us + space 600 us (totale 1.8 ms)

A differenza di NEC, qui è la **durata del burst** che cambia, non la durata dello space.

```
Bit 0:  |##|    |      (600us burst + 600us space)
Bit 1:  |####|    |    (1200us burst + 600us space)
```

#### Ripetizione SIRC

Sony specifica che ogni frame deve essere ripetuto **almeno 3 volte** con un intervallo di circa 45 ms tra l'inizio di ogni frame. Questo è diverso dal repeat code di NEC - in SIRC viene ripetuto l'intero frame.

#### Parametri SIRC

| Parametro | Valore |
|---|---|
| Frequenza portante | 40 kHz |
| Leader burst | 2400 us |
| Leader space | 600 us |
| Bit 0 burst | 600 us |
| Bit 1 burst | 1200 us |
| Bit space | 600 us |
| Ripetizione minima | 3 frame |
| Intervallo frame | ~45 ms |

> **Nota personale:** La portante SIRC a 40 kHz (non 38 kHz) può causare problemi con ricevitori fortemente filtrati su 38 kHz. Nella pratica il Flipper gestisce bene la trasmissione SIRC, ma in ricezione potrebbe perdere qualche bit a distanze maggiori. Se hai problemi con dispositivi Sony, avvicinati.

### Samsung - Variante NEC

Samsung usa un protocollo derivato da NEC con differenze nel timing del leader e nella struttura dell'indirizzo.

#### Struttura del Frame Samsung

```
[Leader] [Address: 8 bit] [Address: 8 bit ripetuto] [Command: 8 bit] [Command Inverted: 8 bit] [Stop]
```

Differenza chiave: l'indirizzo viene trasmesso **due volte identico** (non invertito), mentre il comando usa la stessa logica di inversione di NEC.

#### Timing Samsung

| Elemento | Durata |
|---|---|
| Leader burst | 4500 us |
| Leader space | 4500 us |
| Bit burst | 560 us |
| Bit 0 space | 560 us |
| Bit 1 space | 1690 us |

Il leader è **simmetrico** (4500 + 4500 us) a differenza di NEC (9000 + 4500 us). La codifica dei bit è identica a NEC.

### RAW - Cattura Universale

Quando il Flipper non riesce a decodificare un segnale in un protocollo noto, lo registra in formato RAW.

#### Formato RAW nel Flipper Zero

Un segnale RAW nel file `.ir` del Flipper è rappresentato come:

```
name: Signal_1
type: raw
frequency: 38000
duty_cycle: 0.330000
data: 9000 4500 560 560 560 1690 560 560 ...
```

I valori `data` sono durate in microsecondi, alternando burst e space:
- Valore dispari (1o, 3o, 5o...): durata del **burst** (portante attiva)
- Valore pari (2o, 4o, 6o...): durata dello **space** (silenzio)

#### Quando Serve il RAW

- **Protocolli proprietari** non riconosciuti dal Flipper
- **Telecomandi di condizionatori** con protocolli complessi (frame molto lunghi)
- **Dispositivi industriali** con codifiche non standard
- **Dispositivi vintage** con protocolli obsoleti
- **Qualsiasi segnale IR** che non viene decodificato automaticamente

#### Limiti del RAW

- **File più grandi:** un segnale RAW può occupare molte righe rispetto a un protocollo decodificato
- **Tolleranza di timing:** piccole imprecisioni nella cattura possono causare fallimenti nella riproduzione, specialmente per protocolli con timing stretto
- **Nessuna verifica:** non c'è modo automatico di sapere se la cattura è corretta - serve testare

### Protocolli AC - Il Caso Speciale dei Climatizzatori

I telecomandi dei condizionatori rappresentano il caso più complesso nella comunicazione IR. Meritano una sezione dedicata.

#### Perchè i Protocolli AC Sono Diversi

Un telecomando TV invia comandi semplici: "alza volume", "cambia canale". Il contesto (volume attuale, canale attuale) è mantenuto dalla TV stessa.

Un telecomando AC invia **lo stato completo del climatizzatore** ad ogni pressione:

- Temperatura desiderata (16-30 gradi)
- Modalità (freddo, caldo, deumidificatore, ventilazione, auto)
- Velocità ventola (bassa, media, alta, auto)
- Direzione alette (fissa, swing verticale, swing orizzontale)
- Timer on/off
- Modalità sleep/eco/turbo
- Stato on/off

Tutto questo viene codificato in un **singolo frame IR lunghissimo**, tipicamente **100-200+ bit** (contro i 32 bit di NEC). Ogni volta che premi un tasto sul telecomando, viene trasmesso l'intero stato.

#### Conseguenze Operative

- I frame AC sono spesso **troppo lunghi** per essere decodificati come protocollo standard - il Flipper li cattura in RAW
- **Un singolo bit corrotto** può rendere l'intero frame inutile - il climatizzatore non risponde
- **Ogni marca** ha il suo protocollo (Daikin, Mitsubishi, Panasonic, Toshiba, LG, Samsung, Carrier...) con strutture completamente diverse
- **Il cambio di un singolo parametro** (es. aumentare la temperatura di 1 grado) genera un frame completamente diverso
- Per controllare un AC sconosciuto, potresti dover catturare **decine di combinazioni** diverse

#### Struttura Tipica Frame AC (esempio generico)

```
[Leader] [Header: marca/modello] [Modo] [Temperatura] [Velocità ventola] [Swing] [Timer] [Checksum]
```

Il checksum varia per produttore: può essere XOR, somma modulo 256, CRC o varianti proprietarie.

> **Nota personale:** I protocolli AC sono la bestia nera dell'IR. Se ti serve controllare un climatizzatore sconosciuto durante un engagement, la strategia migliore e': (1) prova prima i profili pre-caricati del Flipper per quella marca, (2) se non funzionano, cattura il segnale originale del telecomando per ogni azione specifica che ti serve (accensione, spegnimento, cambio temperatura), (3) salva ogni segnale RAW con un nome descrittivo. Non tentare di decodificare manualmente il protocollo sul campo - non hai tempo. Fallo in lab dopo, se necessario.

---

