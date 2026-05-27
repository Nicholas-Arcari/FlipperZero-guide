# Fondamenti Tecnici - iButton e Protocollo 1-Wire

Analisi approfondita dei fondamenti tecnici alla base della tecnologia iButton: protocollo 1-Wire di Dallas Semiconductor, architettura elettrica del bus, timing di comunicazione, alimentazione parassita, struttura ROM e comandi fondamentali. Prospettiva di analisi orientata al penetration testing di sistemi di controllo accessi a contatto.

---

## Che cos'è iButton

iButton è una famiglia di dispositivi elettronici integrati in un contenitore a forma di pastiglia metallica (16 mm di diametro), progettati da **Dallas Semiconductor** (acquisita da Maxim Integrated nel 2001, oggi parte di Analog Devices). Il nome commerciale "iButton" si riferisce al package a contatto MicroCAN - un involucro in acciaio inossidabile F5 ermetico, resistente a urti, acqua e corrosione.

Il concetto è semplice: un chip con un identificativo unico, accessibile tramite contatto fisico diretto. Nessuna antenna, nessuna frequenza radio, nessuna alimentazione interna. Il dispositivo comunica esclusivamente quando viene premuto fisicamente su un lettore.

In ambito sicurezza fisica, le chiavi iButton vengono usate per:

- **Citofoni condominiali** - il caso d'uso più diffuso in Italia e nell'est Europa
- **Sistemi di controllo accessi** a contatto
- **Registratori di ronda** per guardie di sicurezza (guard tour systems)
- **Serrature elettroniche** industriali e residenziali
- **Sistemi di identificazione** in ambienti ostili (polvere, acqua, vibrazioni)

> **Nota personale:** La tecnologia iButton è un caso di studio perfetto per il pentester: un sistema progettato negli anni '90 per comodità e robustezza meccanica, senza alcuna considerazione per la sicurezza crittografica. Quando spiego ai clienti cos'è iButton, uso questa analogia: "è come una targa automobilistica che chiunque può leggere e duplicare in 3 secondi." La semplicità del protocollo è sia il motivo del suo successo commerciale (costa pochissimo) sia la sua debolezza fatale dal punto di vista della sicurezza.

---

## Il Protocollo 1-Wire

iButton si basa sul bus **1-Wire**, un protocollo di comunicazione seriale inventato da Dallas Semiconductor. Il nome dice tutto: la comunicazione avviene su un **singolo filo** (più la massa), rendendo il sistema il più semplice possibile a livello hardware.

### Architettura Elettrica

Il bus 1-Wire utilizza solo due contatti:

- **Data (DQ)** - il filo singolo su cui viaggiano dati, clock e alimentazione
- **GND (Ground)** - massa/riferimento

Il bus è di tipo **open-drain con resistore di pull-up**. In condizioni di riposo, la linea dati è mantenuta a livello logico HIGH (tipicamente 5V o 3.3V) dal resistore di pull-up (tipicamente 4.7 kohm). La comunicazione avviene quando il master (lettore) o lo slave (iButton) tirano la linea a LOW.

```
          Vcc (5V / 3.3V)
           |
          [R] 4.7 kohm pull-up
           |
    DQ ----+---- iButton (slave)
           |
    Master (lettore/Flipper)
           |
          GND ---- GND
```

### Topologia del Bus

Il bus 1-Wire supporta una topologia multi-drop: un singolo master può comunicare con più slave sullo stesso filo. Questo è rilevante nei sistemi di accesso più complessi dove il lettore gestisce anche sensori di temperatura o moduli EEPROM sulla stessa linea.

Nei sistemi di accesso iButton tipici (citofoni), la topologia è quasi sempre **punto-punto** (un lettore, una chiave alla volta), dato che la chiave viene appoggiata fisicamente sulla sonda del lettore.

> **Nota personale:** La topologia multi-drop del 1-Wire apre un vettore di attacco interessante che pochi considerano: se riesci a collegare un dispositivo slave aggiuntivo al bus (ad esempio un microcontrollore nascosto dietro al lettore), puoi sniffare passivamente tutte le comunicazioni senza che il lettore se ne accorga. Il bus è progettato per avere più slave, quindi un dispositivo in più non genera errori.

### Comunicazione Bidirezionale su Singolo Filo

Il protocollo 1-Wire è **half-duplex** - master e slave condividono lo stesso filo e parlano a turno. Il master controlla sempre il timing:

1. **Reset Pulse:** il master tira DQ a LOW per almeno 480 microsecondi
2. **Presence Pulse:** lo slave rileva il reset e risponde tirando DQ a LOW per 60-240 microsecondi - questo è il "sono qui" del dispositivo
3. **Time Slot (scrittura):** il master tira DQ a LOW per un breve periodo:
   - **Write 0:** mantiene LOW per 60-120 microsecondi (l'intero slot)
   - **Write 1:** tira LOW per 1-15 microsecondi poi rilascia (il pull-up riporta a HIGH)
4. **Time Slot (lettura):** il master tira DQ a LOW per 1-15 microsecondi poi rilascia. Lo slave risponde entro 15 microsecondi:
   - **Legge 0:** lo slave mantiene LOW
   - **Legge 1:** lo slave non fa nulla (la linea torna HIGH per il pull-up)

### Diagramma Temporale Dettagliato

```
Reset e Presence Pulse:

     |<-------- Reset Pulse (480-960 us) -------->|<-- Recovery -->|<- Presence (60-240 us) ->|
     |                                             |   (15-60 us)   |                          |
HIGH ____                                         _________________                            ____
         |                                       |                 |                          |
LOW      |_______________________________________|                 |__________________________|


Write 0 Slot:

     |<-------------- 60-120 us ------------->|<- Recovery (1 us min) ->|
     |                                        |                        |
HIGH ____                                     __________________________
         |                                   |
LOW      |___________________________________|


Write 1 Slot:

     |<- 1-15 us ->|<--------- Pull-up restores HIGH --------->|<- Recovery ->|
     |              |                                            |              |
HIGH ____           ______________________________________________              ___
         |         |
LOW      |_________|


Read Slot:

     |<- Master 1-15 us ->|<-- Slave response window (15 us) -->|<- Recovery ->|
     |                     |                                      |              |
HIGH ____                  ________________________________________              ___  (Read 1 - slave rilascia)
         |                |
LOW      |________________|

         |                     |                                      |
HIGH ____                  ____                                       ___  (Read 0 - slave mantiene LOW)
         |                |    |                                     |
LOW      |________________|    |_____________________________________|
```

### Tabella Timing Critico

| Operazione | Durata Minima | Durata Tipica | Durata Massima |
|---|---|---|---|
| Reset pulse | 480 us | 480-640 us | 960 us |
| Presence pulse | 60 us | 60-120 us | 240 us |
| Write 0 slot | 60 us | 60 us | 120 us |
| Write 1 slot | 1 us | 6 us | 15 us |
| Read slot | 1 us | 1 us | 15 us |
| Recovery time | 1 us | 1 us | - |
| Slot totale (min) | 61 us | 61 us | 121 us |

I timing slot sono la base di tutta la comunicazione 1-Wire. Ogni bit richiede un minimo di 60 microsecondi + 1 microsecondo di recovery, portando il data rate massimo teorico a circa **16.3 kbit/s** in modalità standard. Esiste anche una modalità **overdrive** fino a ~142 kbit/s, ma raramente usata nei sistemi di accesso.

> **Nota personale:** I timing sono rilevanti per il pentester in due contesti. Primo: quando fai emulazione dal Flipper, il firmware deve rispettare questi timing con precisione di microsecondi - se il firmware ha un bug nei timing, l'emulazione fallisce su lettori strict. Secondo: quando analizzi un protocollo sconosciuto con un oscilloscopio o un logic analyzer, conoscere i timing standard ti permette di distinguere tra 1-Wire Dallas, Cyfral e Metakom osservando i pattern temporali. Ho usato un Saleae Logic per analizzare un lettore che non rispondeva al Flipper - il problema era un timing non-standard nel reset pulse (il lettore usava 380 us invece dei 480 us minimi).

### Velocità di Comunicazione

Il protocollo 1-Wire definisce due velocità operative:

| Modalità | Data Rate | Uso Tipico |
|---|---|---|
| **Standard** | ~16.3 kbit/s | Tutti i sistemi di accesso iButton |
| **Overdrive** | ~142 kbit/s | Dispositivi 1-Wire ad alta velocità (raro in accesso) |

Per la lettura di un ROM code a 64 bit in modalità standard:
- Tempo di reset/presence: ~1 ms
- Tempo per Read ROM command (8 bit): ~0.5 ms
- Tempo per 64 bit di dati: ~4 ms
- **Tempo totale per una lettura completa: ~5.5 ms**

Questo significa che un lettore può teoricamente leggere una chiave ~180 volte al secondo. In pratica, i lettori aggiungono delay di processing e debouncing, riducendo il rate a 2-10 letture al secondo.

---

## Alimentazione Parassita (Parasite Power)

Una caratteristica unica del 1-Wire è l'**alimentazione parassita**: il dispositivo slave estrae l'energia necessaria al funzionamento direttamente dalla linea dati DQ durante i periodi HIGH. Un condensatore interno al chip immagazzina la carica sufficiente per mantenere il funzionamento durante le fasi LOW.

```
Circuito equivalente alimentazione parassita:

    DQ ────┬───── [Chip Logic]
           |
          [C] Condensatore interno (~800 pF tipico)
           |
    GND ───┘

    Durante HIGH: DQ carica il condensatore attraverso diodo interno
    Durante LOW:  il condensatore alimenta la logica del chip
```

Questo significa che l'iButton non ha batteria - riceve alimentazione dal contatto fisico col lettore. Quando tocchi la chiave sul lettore, il chip si accende, comunica il suo ID e poi si spegne appena rimuovi la chiave.

Alcuni dispositivi 1-Wire più complessi (sensori di temperatura, EEPROM) possono richiedere alimentazione esterna dedicata (Vcc separato) per operazioni che consumano più corrente, come la scrittura in EEPROM o la conversione di temperatura. Ma per le chiavi iButton usate nei sistemi di accesso, l'alimentazione parassita è sufficiente.

> **Nota personale:** L'alimentazione parassita ha un'implicazione importante per la scrittura su RW1990: durante la programmazione, il chip richiede più corrente del normale. Se il contatto elettrico non è perfetto, la tensione sul condensatore interno scende sotto la soglia minima e la scrittura si corrompe. Questo è il motivo per cui la scrittura è meno affidabile della lettura - la lettura richiede pochissima corrente, la scrittura ne richiede di piu'. Un contatto pulito e stabile è ancora più critico per la scrittura che per la lettura.

---

## Family Code e Struttura ROM

Ogni dispositivo 1-Wire ha un **ROM code** univoco di 64 bit (8 byte). Questa è la struttura:

```
| Family Code | Serial Number           | CRC-8  |
| 8 bit       | 48 bit                  | 8 bit  |
| Byte 0      | Byte 1 | ... | Byte 6   | Byte 7 |
```

### Family Code (8 bit)

Il family code identifica il tipo di dispositivo:

| Family Code | Dispositivo | Descrizione |
|---|---|---|
| `0x01` | DS1990A / DS1990R / DS2401 | Chiave identificazione solo lettura |
| `0x02` | DS1991 | Chiave con memoria protetta |
| `0x04` | DS1994 | Timer + memoria |
| `0x06` | DS1993 | 4 Kbit memoria |
| `0x08` | DS1992 | 1 Kbit memoria |
| `0x0A` | DS1995 | 16 Kbit memoria |
| `0x0C` | DS1996 | 64 Kbit memoria |
| `0x10` | DS18S20 | Sensore temperatura |
| `0x14` | DS1971/DS2430A | 256-bit EEPROM |
| `0x23` | DS2433 | 4 Kbit EEPROM |
| `0x28` | DS18B20 | Sensore temperatura digitale |
| `0x81` | DS1420 | Serial ID + contatore |

### Serial Number (48 bit)

Il numero di serie univoco assegnato in fabbrica. Questo è lo spazio dell'indirizzo effettivo - 2^48 = **281.474.976.710.656** combinazioni possibili. Ogni chip Dallas esce dalla fabbrica con un seriale unico, mai ripetuto. Maxim/Analog Devices garantisce l'unicità globale.

### CRC-8 (8 bit)

Checksum calcolato con il polinomio DOW-CRC (x^8 + x^5 + x^4 + 1, polinomio 0x31). Il CRC viene calcolato sui primi 7 byte (family code + serial number) e consente al lettore di verificare l'integrità della comunicazione.

**Calcolo del CRC-8 DOW (Dallas One-Wire):**

```
Polinomio: x^8 + x^5 + x^4 + 1  (0x31, o 0x8C riflesso)
Valore iniziale: 0x00
Input: byte 0 a byte 6 (family code + serial number)
Il CRC valido produce 0x00 quando calcolato su tutti gli 8 byte
```

**Algoritmo CRC-8 DOW (pseudocodice):**

```
function dow_crc8(data[], length):
    crc = 0x00
    for i = 0 to length-1:
        byte = data[i]
        for bit = 0 to 7:
            mix = (crc ^ byte) & 0x01
            crc = crc >> 1
            if mix:
                crc = crc ^ 0x8C
            byte = byte >> 1
    return crc
```

**Esempio pratico - una chiave DS1990A con ROM code `01:A2:B3:C4:D5:E6:F7:XX`:**

- Family code: `0x01` (DS1990A)
- Serial: `A2:B3:C4:D5:E6:F7`
- CRC-8: calcolato automaticamente sui primi 7 byte

> **Nota personale:** Il CRC-8 è importante nel pentesting iButton per due motivi. Primo: se generi ID a mano per il fuzzing, devi calcolare il CRC corretto altrimenti il lettore scarterà l'ID prima ancora di verificarlo nel database. Secondo: alcuni lettori economici (soprattutto quelli Cyfral/Metakom) non verificano il CRC - questo li rende vulnerabili a ID malformati. Ho trovato citofoni che accettano qualsiasi cosa con family code 0x01, ignorando completamente il CRC.

> **Nota personale:** Per il pentester che vuole generare ID validi programmaticamente (ad esempio per fuzzing personalizzato via script), implementare il CRC-8 DOW è essenziale. Ho uno script Python che genera batch di ID validi con CRC corretto - lo uso per preparare dizionari di fuzzing mirati quando conosco il prefix dei seriali di un condominio. Senza CRC valido, il lettore scarta l'ID al primo controllo e il fuzzing diventa inutile.

---

## Comandi ROM 1-Wire

Dopo il reset/presence, il master deve inviare un comando ROM per selezionare il dispositivo:

| Comando | Codice | Descrizione |
|---|---|---|
| **Read ROM** | `0x33` | Legge i 64 bit del ROM code. Funziona solo se c'è un unico slave sul bus |
| **Match ROM** | `0x55` | Seleziona uno slave specifico inviando i suoi 64 bit - usato con più slave sul bus |
| **Skip ROM** | `0xCC` | Salta la selezione - comunica col dispositivo presente (solo se uno) |
| **Search ROM** | `0xF0` | Algoritmo di ricerca per enumerare tutti i dispositivi sul bus |
| **Alarm Search** | `0xEC` | Come Search ROM ma cerca solo dispositivi in stato di allarme |

Per le chiavi di accesso (DS1990A), l'unico comando rilevante è **Read ROM** - il lettore fa reset, legge i 64 bit del ROM code e li confronta con il database interno.

### Sequenza Completa di Lettura

```
Master                              Slave (iButton)
  |                                      |
  |--- Reset Pulse (480+ us LOW) ------->|
  |                                      |
  |<--- Presence Pulse (60-240 us LOW) --|
  |                                      |
  |--- Read ROM (0x33, 8 bit) --------->|
  |                                      |
  |<--- ROM Code (64 bit, LSB first) ---|
  |                                      |
  [Calcola CRC-8 sui primi 56 bit]      |
  [Confronta con byte 7]                |
  [Se valido: cerca nel database]        |
  [Se trovato: azione]                   |
```

> **Nota personale:** La bellezza (e la debolezza) del sistema è proprio questa: tutta la "sicurezza" si basa sulla segretezza di un numero a 64 bit trasmesso in chiaro, senza alcuna crittografia, su un bus fisico. Chiunque possa toccare la chiave per un secondo può leggere quel numero e replicarlo. Questo è il motivo per cui iButton è considerato estremamente insicuro dagli standard moderni - ma è ancora installato in milioni di citofoni.

> **Nota personale:** L'algoritmo Search ROM (0xF0) ha un'applicazione interessante nel pentesting: se riesci a collegare un dispositivo al bus interno di un lettore multi-drop (ad esempio un sistema di guard tour con più lettori in cascata), puoi enumerare tutti i dispositivi 1-Wire sulla rete usando Search ROM. Questo ti dà una mappa di tutti i sensori, EEPROM e moduli collegati - informazioni utili per capire l'architettura del sistema target.

---

## Implicazioni per la Sicurezza

### Assenza di Crittografia

Il protocollo 1-Wire è stato progettato per semplicità e affidabilità, non per sicurezza. Le implicazioni per i sistemi di accesso sono:

| Aspetto | Implicazione di Sicurezza |
|---|---|
| ID trasmesso in chiaro | Chiunque può leggere l'ID con un lettore 1-Wire da 2 euro |
| Nessun challenge-response | Non esiste autenticazione reciproca |
| Nessun nonce/timestamp | Il replay attack funziona sempre, senza scadenza |
| ID statico e permanente | Una volta letto, l'ID è valido per sempre |
| Nessuna revoca a livello di protocollo | La revoca avviene solo sul database del lettore |

### Il Paradosso della Sicurezza iButton

Il contatto fisico obbligatorio è spesso citato come "misura di sicurezza" di iButton - "non si può leggere da lontano." Questo è vero ma fuorviante:

1. Il contatto fisico protegge dalla lettura a distanza (a differenza di RFID/NFC)
2. Ma non protegge dalla clonazione - basta toccare la chiave per 2 secondi
3. E non protegge dal fuzzing - basta toccare il lettore con un dispositivo attaccante

La sicurezza di iButton si basa interamente sulla sicurezza fisica della chiave e sulla gestione del database del lettore, non sul protocollo.

> **Nota personale:** Spiego sempre ai clienti che iButton è come una chiave meccanica tradizionale: se qualcuno la prende in mano per 3 secondi, può farsi una copia. La differenza è che con iButton la "copia" costa 50 centesimi e richiede zero competenze, mentre duplicare una chiave meccanica di alta sicurezza (tipo Evva MCS o Mul-T-Lock) è significativamente più difficile e costoso. Paradossalmente, la chiave meccanica che protegge la porta dell'appartamento è spesso più sicura della chiave iButton che protegge il portone del palazzo.
