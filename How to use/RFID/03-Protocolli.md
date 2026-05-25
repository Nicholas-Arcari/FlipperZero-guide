## Protocolli Dettagliati

### EM4100 (EM-Marin)

Il protocollo più semplice e diffuso al mondo per RFID 125 kHz. Prodotto originariamente da EM Microelectronic (Svizzera), è diventato lo standard de facto per il controllo accessi economico.

#### Dove si Trova

- Condomini italiani (la stragrande maggioranza)
- Palestre e centri sportivi
- Parcheggi a sbarra
- Macchinette del caffè aziendali
- Sistemi di controllo presenze economici
- Badge visitatori temporanei
- Armadietti elettronici
- Cancelli pedonali

#### Struttura Completa del Frame

Un tag EM4100 trasmette continuamente un frame di **64 bit** in loop. La struttura e':

```
[9 bit header] [D00][D01][D02][D03][P0]  <- riga 0
               [D04][D05][D06][D07][P1]  <- riga 1
               [D08][D09][D10][D11][P2]  <- riga 2
               [D12][D13][D14][D15][P3]  <- riga 3
               [D16][D17][D18][D19][P4]  <- riga 4
               [D20][D21][D22][D23][P5]  <- riga 5
               [D24][D25][D26][D27][P6]  <- riga 6
               [D28][D29][D30][D31][P7]  <- riga 7
               [D32][D33][D34][D35][P8]  <- riga 8
               [D36][D37][D38][D39][P9]  <- riga 9
               [PC0][PC1][PC2][PC3][S0]  <- colonne parità + stop bit
```

**Dettaglio dei 64 bit:**

| Campo | Bit | Descrizione |
|---|---|---|
| **Header** | 9 bit | Tutti 1 (`111111111`) - sincronizzazione |
| **Data** | 40 bit | 10 righe x 4 bit = 40 bit di dati effettivi |
| **Row Parity** | 10 bit | 1 bit di parità pari per ogni riga (P0-P9) |
| **Column Parity** | 4 bit | 1 bit di parità pari per ogni colonna (PC0-PC3) |
| **Stop Bit** | 1 bit | Sempre 0 (S0) |
| **Totale** | 64 bit | |

**I 40 bit di dati contengono:**
- **8 bit** (prime 2 righe): Version Number / Customer ID (tipicamente il produttore o il lotto)
- **32 bit** (righe 2-9): Unique ID del tag

**Esempio pratico:**
```
Header:    111111111
Riga 0:    0001 0    <- nibble 0x1 + parità
Riga 1:    0000 0    <- nibble 0x0 + parità
Riga 2:    0110 0    <- nibble 0x6 + parità
Riga 3:    1010 0    <- nibble 0xA + parità
Riga 4:    1111 0    <- nibble 0xF + parità
Riga 5:    0011 0    <- nibble 0x3 + parità
Riga 6:    1100 0    <- nibble 0xC + parità
Riga 7:    0101 0    <- nibble 0x5 + parità
Riga 8:    1001 0    <- nibble 0x9 + parità
Riga 9:    0010 1    <- nibble 0x2 + parità
Col par:   0110 0    <- parità colonne + stop

Version: 0x10 = 16
ID: 0x6AFC3C592 (40 bit -> il Flipper mostra 5 byte hex)
```

#### Clock Rate

- **Frequenza portante:** 125 kHz (o 134.2 kHz in varianti)
- **Clock divisor:** RF/64 (tipico) = 125000/64 = 1953.125 bps
- **Anche supportati:** RF/32 (3906.25 bps) e RF/16 (7812.5 bps) su tag compatibili
- **Tempo trasmissione frame completo:** 64 bit / 1953 bps = ~32.7 ms
- **Il tag ripete il frame** circa 30 volte al secondo

#### Sicurezza: ZERO

EM4100 non ha **nessuna** forma di sicurezza:
- Nessuna crittografia
- Nessuna autenticazione
- Nessun challenge-response
- Nessun anti-cloning
- L'ID è trasmesso in chiaro, continuamente, senza alcuna protezione
- Chiunque con un lettore a 3 EUR da AliExpress può leggere l'ID
- Chiunque con un T5577 da 0.50 EUR può clonarlo

**Questo significa che QUALSIASI sistema di controllo accessi basato esclusivamente su EM4100 è da considerarsi NON sicuro.** La clonazione richiede meno di 5 secondi.

> **Nota personale:** L'EM4100 è il mio pane quotidiano nei pentest fisici in Italia. L'80% dei condomini che ho testato usa questo protocollo, spesso con lettori prodotti da aziende come CAME, BPT, URMET e ELVOX. La cosa più sconcertante è che molti amministratori di condominio non sanno nemmeno che i badge sono clonabili - pensano che siccome sono "elettronici" siano sicuri. In realtà un portachiavi EM4100 offre la stessa sicurezza di una chiave copiata dal ferramenta, con la differenza che la copia del badge è istantanea e non lascia traccia.

---

### HID Prox (H10301)

HID Global è il leader mondiale nei sistemi di controllo accessi. La linea "Prox" (125 kHz) è il loro prodotto legacy ma ancora enormemente diffuso, specialmente in ambienti enterprise.

#### Dove si Trova

- Uffici aziendali
- Banche e assicurazioni
- Ospedali
- Università
- Data center (spesso in combinazione con altri fattori)
- Edifici governativi (specialmente USA)
- Aeroporti (zone non critiche)

#### Formato 26-bit (H10301) - Il Più Comune

Il formato HID 26-bit è lo standard industriale. Struttura:

```
[Leading 0] [Parity Even] [Facility Code 8-bit] [Card Number 16-bit] [Parity Odd]
```

**Dettaglio:**

| Campo | Bit | Range | Descrizione |
|---|---|---|---|
| **Even Parity** | 1 bit (bit 0) | - | Parità pari sui bit 1-12 |
| **Facility Code** | 8 bit (bit 1-8) | 0-255 | Identifica l'edificio/azienda |
| **Card Number** | 16 bit (bit 9-24) | 0-65535 | Identifica la carta specifica |
| **Odd Parity** | 1 bit (bit 25) | - | Parità dispari sui bit 13-24 |

**Esempio pratico:**
```
Bit raw:     1 01100100 0000001010110011 0
             P FFFFFFFF CCCCCCCCCCCCCCCC P

Even Parity: 1 (parità pari dei primi 12 bit dati)
Facility:    01100100 = 100
Card Number: 0000001010110011 = 691
Odd Parity:  0 (parità dispari degli ultimi 12 bit dati)

Sul Flipper vedi: HID H10301 FC:100 CN:691
```

#### Modulazione e Trasmissione

- **Modulazione:** FSK2 (Frequency Shift Keying a 2 livelli)
- **Frequenze:** ~12.5 kHz (RF/10) per lo 0 e ~15.625 kHz (RF/8) per l'1
- **Portante:** 125 kHz
- **Codifica:** Biphase / Manchester differenziale
- **Data rate:** RF/50 = 2.5 kbps

Il frame completo HID trasmesso via aria è più lungo dei 26 bit del formato - include preamble, header HID proprietario e CRC. Il Flipper decodifica tutto automaticamente e mostra solo FC e CN.

#### Formati HID Alternativi

Oltre al 26-bit H10301, HID supporta molti altri formati:

- **34-bit:** Facility Code esteso
- **35-bit Corporate 1000:** usato in grandi corporation
- **37-bit H10302/H10304:** card number più grande
- **48-bit:** formato OSDP
- **Custom:** molte aziende definiscono formati proprietari

Il Flipper Zero supporta nativamente il 26-bit H10301 e riconosce la maggior parte degli altri formati, ma potrebbe mostrare solo i dati raw per formati custom.

#### Sicurezza: QUASI ZERO

Come EM4100, HID Prox **non ha crittografia**:
- L'ID è trasmesso in chiaro
- Nessun challenge-response
- Nessuna mutua autenticazione
- La clonazione è banale (identica a EM4100)
- L'unica "protezione" è il Facility Code (facilmente scopribile)
- HID stessa consiglia la migrazione a iCLASS SE o SEOS (NFC 13.56 MHz)

L'unico vantaggio rispetto a EM4100 è che il formato proprietario HID rende leggermente più complesso il reverse engineering per chi non ha gli strumenti giusti. Ma con un Flipper Zero o un Proxmark3, la lettura è immediata.

> **Nota personale:** Il Facility Code è una miniera d'oro in un pentest. Se leggi un singolo badge HID e scopri che il FC è 42, puoi ragionevolmente assumere che TUTTI i badge di quell'edificio hanno FC:42. A quel punto il fuzzer del Flipper può provare tutti i 65536 Card Number possibili. In un engagement ho scoperto che un ospedale usava HID 26-bit con FC:10 e Card Number sequenziali partendo da 1. Bastava scrivere FC:10 CN:1 su un T5577 per avere accesso alla prima porta. Impressionante quanto sia diffusa questa vulnerabilità.

---

### Indala

Indala (ora parte di HID Global dopo l'acquisizione) è un sistema RFID 125 kHz proprietario che si differenzia significativamente da HID Prox.

#### Dove si Trova

- Edifici governativi e militari (specialmente USA)
- Strutture legacy che non hanno mai migrato ad HID Prox
- Alcune università e ospedali
- Sistemi installati prima del 2005 (quando Indala era indipendente)

#### Caratteristiche Tecniche

- **Modulazione:** PSK (Phase Shift Keying) - diversa dalla FSK di HID
- **Codifica dati:** proprietaria, non documentata pubblicamente
- **Formati:** 26-bit (simile a H10301) e 29-bit (formato Motorola)
- **Frequenza portante:** 125 kHz
- **Data rate:** variabile, tipicamente RF/32 o RF/64

#### Differenze da HID Prox

| Caratteristica | HID Prox | Indala |
|---|---|---|
| **Modulazione** | FSK2 | PSK1 |
| **Formato standard** | 26-bit H10301 | 26-bit / 29-bit |
| **Codifica** | Biphase | Proprietaria |
| **Documentazione** | Semi-pubblica | Chiusa |
| **Diffusione** | Globale | Principalmente USA |
| **Costo badge** | Medio | Alto (fornitore unico) |

#### Formato 26-bit Indala

Simile all'HID 26-bit ma con codifica e modulazione diverse:

```
[Preamble PSK] [Facility Code 8-bit] [Card Number 16-bit] [Checksum]
```

Il Flipper Zero legge i tag Indala e li mostra come "Indala" con i dati grezzi. L'interpretazione del Facility Code e Card Number può richiedere analisi manuale per formati non standard.

#### Sicurezza

Identica a HID Prox e EM4100: **nessuna crittografia**. Il protocollo proprietario offre solo "security through obscurity", che non è sicurezza reale. La clonazione su T5577 è possibile con il Flipper Zero.

> **Nota personale:** I tag Indala sono abbastanza rari in Italia. Li ho incontrati solo in due engagement: una base NATO e un'azienda americana con sede in Italia che aveva importato il sistema dalla casa madre. Il Flipper li legge senza problemi, ma l'emulazione può essere meno affidabile rispetto a EM4100/HID perchè la modulazione PSK è più sensibile al timing. Se possibile, preferisco clonare su T5577 piuttosto che usare l'emulazione software per Indala.

---

### FDX-B (ISO 11784/11785)

FDX-B (Full Duplex Type B) è lo standard internazionale per l'identificazione elettronica degli animali. È regolato dalle norme ISO 11784 (struttura del codice) e ISO 11785 (caratteristiche tecniche).

#### Dove si Trova

- Microchip sottocutanei per cani, gatti, cavalli e altri animali domestici
- Identificazione del bestiame (obbligatoria in EU)
- Tracciamento fauna selvatica
- Acquariologia (identificazione pesci pregiati)
- Obbligatorio in Italia per tutti i cani dal 2005 (anagrafe canina)

#### Caratteristiche Tecniche

- **Frequenza:** 134.2 kHz (NON 125 kHz - attenzione!)
- **Modulazione:** ASK / HDX o FDX-B
- **Data rate:** RF/32 = 4193.75 bps
- **Codifica:** NRZ con bit stuffing
- **Tipo:** passivo, read-only (il microchip non può essere riscritto)

#### Struttura del Frame (128 bit)

Il frame FDX-B è composto da 128 bit con questa struttura:

```
[11 bit header] [10 bit dati] [1 control] [10 bit dati] [1 control] ...
```

**Struttura dei dati decodificati:**

| Campo | Bit | Descrizione |
|---|---|---|
| **Header** | 11 bit | Pattern di sincronizzazione `00000000001` |
| **Animal ID** | 38 bit | Numero identificativo unico dell'animale (0 - 274.877.906.943) |
| **Country Code** | 10 bit | Codice paese ISO 3166 (380 = Italia) |
| **Data Flag** | 1 bit | 1 se il tag contiene dati aggiuntivi |
| **Animal Flag** | 1 bit | 1 se è un animale (vs oggetto) |
| **Extra Data** | 24 bit | Dati supplementari (razza, vaccinazioni, ecc.) |
| **CRC** | 16 bit | CRC-CCITT per la verifica integrità |

**Esempio pratico di un microchip italiano:**
```
Animal ID:    123456789012345
Country Code: 380 (Italia)
Animal Flag:  1 (è un animale)
Data Flag:    0 (nessun dato extra)

Codice completo: 380 123456789012345
(15 cifre totali visibili, di cui le prime 3 sono il paese)
```

#### Come il Flipper Legge FDX-B

Il Flipper Zero può leggere i microchip FDX-B ma con importanti limitazioni:

- **La frequenza è 134.2 kHz, non 125 kHz** - il Flipper si adatta ma la sensibilità è ridotta
- **Portata molto limitata:** 1-2 cm per impianti sottocutanei (antenna del chip microscopica)
- **Per leggere un animale:** devi posizionare il Flipper esattamente sul punto di impianto (tipicamente tra le scapole per cani e gatti)
- **Il Flipper mostra:** Country Code + Animal ID
- **NON può scrivere** microchip FDX-B reali (sono OTP - One Time Programmable)

#### Sicurezza

I microchip FDX-B sono read-only (una volta programmati in fabbrica non possono essere modificati), ma:
- L'ID è trasmesso in chiaro senza crittografia
- È possibile **emulare** un microchip FDX-B con il Flipper
- È possibile **scrivere** un ID FDX-B su un T5577 (che opera pero' a 125 kHz, non 134.2 kHz - potrebbe non funzionare con tutti i lettori)
- È possibile **creare** ID FDX-B falsi con il FDX-B Maker

> **Nota personale:** La lettura di microchip animali con il Flipper è possibile ma frustrante. La portata è cosi' ridotta che devi letteralmente premere il Flipper sulla pelle dell'animale nel punto esatto del microchip. Con un cane collaborativo è fattibile, con un gatto nervoso è praticamente impossibile. Per uso veterinario reale, un lettore FDX-B dedicato (come quelli da 30 EUR di Amazon) è infinitamente più pratico. L'utilità del supporto FDX-B nel Flipper è più per ricerca e studio che per uso pratico.

---

### T5577 - Il Tag Universale

Il T5577 (prodotto da Atmel, ora Microchip Technology) è il tag RFID 125 kHz più versatile e importante per qualsiasi pentester. È un tag **programmabile e riscrivibile** che può emulare praticamente qualsiasi protocollo LF.

#### Perchè è Fondamentale

- Può emulare EM4100, HID Prox, Indala, FDX-B, AWID, Pyramid, Viking, Jablotron e molti altri
- È riscrivibile illimitatamente (a differenza dei tag OTP)
- Costa 0.30-1 EUR in forma di card, keyfob o coin
- È il "blank CD" del mondo RFID 125 kHz
- Il Flipper Zero lo usa come target principale per la scrittura

#### Struttura della Memoria

Il T5577 ha una memoria EEPROM organizzata in **2 pagine** da **8 blocchi** ciascuna (7+1 per page):

```
Page 0 (user data):
  Block 0: Configuration Word (32 bit) <-- FONDAMENTALE
  Block 1: Data Word 1 (32 bit)
  Block 2: Data Word 2 (32 bit)
  Block 3: Data Word 3 (32 bit)
  Block 4: Data Word 4 (32 bit)
  Block 5: Data Word 5 (32 bit)
  Block 6: Data Word 6 (32 bit)
  Block 7: Password (32 bit) <-- protezione opzionale

Page 1 (tracing data):
  Block 1: Tracing Data 1
  Block 2: Tracing Data 2
  Block 3: Tracing Data 3
  Block 4: Tracing Data 4
  (Block 0 di Page 1: config mirror)
```

#### Block 0 - Configuration Word (Cruciale)

Il Block 0 di Page 0 è il cuore del T5577. Determina COME il tag si comporta - quale protocollo emula, quale modulazione usa, a quale data rate trasmette:

```
Bit 32-bit Configuration Word:

[Bit 0]      Master Key flag
[Bit 1-3]    Reserved
[Bit 4]      POR Delay (Power-On Reset delay)
[Bit 5-9]    Data Bit Rate (divisor: RF/8, RF/16, RF/32, RF/40, RF/50, RF/64, RF/100, RF/128)
[Bit 10-12]  Modulation scheme
               000 = Direct
               001 = PSK1
               010 = PSK2
               011 = PSK3
               100 = FSK1 (RF/8 + RF/5)
               101 = FSK2 (RF/8 + RF/10)
               110 = FSK1a (RF/5 + RF/8)
               111 = FSK2a (RF/10 + RF/8)
[Bit 13]     PSK Clock Frequency
[Bit 14]     Inverse Data
[Bit 15-16]  Modulation (extended)
               00 = ASK/Manchester
               01 = ASK/Biphase
               10 = ASK/Reserved
               11 = NRZ/Direct (no encoding)
[Bit 17]     ST sequence terminator
[Bit 18-20]  Max Block (quanti blocchi trasmettere: 0-7)
[Bit 21]     Password Write (1 = password richiesta per scrittura)
[Bit 22]     Reserved
[Bit 23]     AOR (Answer On Request - single shot vs continuous)
[Bit 24-27]  Reserved
[Bit 28]     Init Delay
[Bit 29]     PWD (1 = password abilitata)
[Bit 30-31]  Reserved
```

#### Configurazioni Comuni per Emulazione

Ecco i valori di configurazione del Block 0 per emulare i protocolli più comuni:

**EM4100:**
```
Config: 0x00148040
- Modulazione: ASK/Manchester
- Data rate: RF/64
- Max blocks: 2 (Block 1 + Block 2 = 64 bit)
- Nessuna password
```

**HID Prox 26-bit (H10301):**
```
Config: 0x00107060
- Modulazione: FSK2 (RF/8 + RF/10)
- Data rate: RF/50
- Max blocks: 3
- Codifica: Biphase
```

**Indala 26-bit:**
```
Config: 0x00081040
- Modulazione: PSK1
- Data rate: RF/32
- Max blocks: 2
- Codifica: diretta
```

**FDX-B:**
```
Config: 0x603E1040
- Modulazione: ASK
- Data rate: RF/32
- Max blocks: 4
- Note: alcuni lettori FDX-B operano a 134.2 kHz
  e potrebbero non leggere un T5577 a 125 kHz
```

#### Protezione con Password

Il T5577 supporta una password a 32 bit per proteggere la scrittura:

- Senza password: chiunque può sovrascrivere il contenuto
- Con password: serve la password per scrivere nuovi dati
- La password è memorizzata nel Block 7 di Page 0
- **La password NON protegge la lettura** - l'ID viene comunque trasmesso in chiaro
- La password protegge solo dalla sovrascrittura
- Default di fabbrica: 0x00000000 (nessuna password)
- Se dimentichi la password, il tag è inutilizzabile (non c'è reset)

> **Nota personale:** Il T5577 è lo strumento più potente nel toolkit LF di un pentester. Porto sempre 10-15 T5577 in formato keyfob e card nel mio kit. Costano niente e mi permettono di clonare qualsiasi badge 125 kHz in secondi. Un consiglio: compra T5577 in bulk da AliExpress (50 pezzi per circa 15 EUR). Verifica che siano veri T5577 e non EM4100 spacciati per T5577 - succede spesso. Per verificare: un vero T5577 è scrivibile, un EM4100 no. Un altro consiglio: dopo aver clonato un badge durante un pentest, proteggi il T5577 con una password casuale. Se lo perdi, nessuno potrà leggerlo e risalire all'engagement.

---

