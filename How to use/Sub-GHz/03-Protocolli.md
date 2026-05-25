# Sub-GHz - Modulazioni e Protocolli

## Modulazioni - Il Linguaggio Fisico del Segnale

### OOK/ASK (On-Off Keying / Amplitude Shift Keying)

La modulazione più semplice e diffusa nel mondo dei telecomandi consumer:

- **Bit 1:** il trasmettitore emette la portante RF
- **Bit 0:** il trasmettitore è silenzioso (nessuna emissione)
- **Decodifica:** il ricevitore misura la presenza/assenza del segnale

Utilizzata da: la stragrande maggioranza dei telecomandi garage (Nice, Came, FAAC, BFT, Beninca), sensori meteo, campanelli wireless, sensori allarme economici.

Varianti pratiche:
- **Manchester encoding:** ogni bit è rappresentato da una transizione (alto→basso = 1, basso→alto = 0). Usato da molti protocolli per garantire sincronizzazione.
- **PWM (Pulse Width Modulation):** la durata dell'impulso alto determina il valore del bit. Impulso lungo = 1, impulso corto = 0 (o viceversa).
- **PPM (Pulse Position Modulation):** la posizione dell'impulso nel timeslot determina il valore.

> **Nota personale:** Se stai analizzando un segnale sconosciuto, parti sempre dall'ipotesi OOK/ASK a 433.92 MHz. Copre probabilmente il 70-80% dei dispositivi consumer europei.

### 2-FSK (Frequency Shift Keying)

Modulazione a spostamento di frequenza:

- **Bit 1:** la portante si sposta su una frequenza leggermente più alta
- **Bit 0:** la portante si sposta su una frequenza leggermente più bassa
- **Deviazione tipica:** 4.8-47.6 kHz

Utilizzata da: protocolli più sofisticati come KeeLoq rolling code (alcune varianti), sistemi domotici avanzati, sensori industriali.

Vantaggi: maggiore resistenza al rumore rispetto a OOK, migliore range in ambienti rumorosi.

### GFSK (Gaussian FSK)

Variante della FSK con filtraggio gaussiano per ridurre la larghezza di banda:

- Transizioni tra frequenze più morbide
- Minore interferenza con canali adiacenti
- Usata in protocolli moderni

Utilizzata da: alcuni rolling code avanzati, protocolli proprietari.

---

## Protocolli Supportati dal Flipper Zero

Il Flipper Zero decodifica automaticamente decine di protocolli. Ecco i principali con dettagli operativi:

### Protocolli a Codice Fisso

| Protocollo | Bit | Frequenza | Modulazione | Note |
|---|---|---|---|---|
| **Princeton** | 24 | 433.92 | OOK | Generico, usato da molti cloni cinesi |
| **Nice FLO** | 12 | 433.92 | OOK | Cancelli Nice vecchia generazione |
| **Nice FLORS** | 52 | 433.92 | OOK | Nice con sync |
| **Came** | 12 | 433.92 | OOK | Came Automation codice fisso |
| **Came TWEE** | 54 | 433.92 | OOK | Came con codice esteso |
| **Linear** | 10 | 300/310 | OOK | Garage door USA |
| **Gate TX** | 24 | 433.92 | OOK | Generico gate controller |
| **Holtek HT12X** | 12 | 433.92 | OOK | Encoder/decoder economici |
| **Chamberlain** | 7/8/9 | 300/315/390 | OOK | Garage USA (alcune versioni) |
| **SMC5326** | 25 | 433.92 | OOK | Copiatrice di telecomandi |
| **PT2260/PT2262** | 24 | 433.92 | OOK | Encoder generico (alias Princeton) |
| **Honeywell** | 48 | 345 | OOK | Sensori allarme US |
| **Intertechno** | 32 | 433.92 | OOK | Domotica tedesca |

### Protocolli Rolling Code

| Protocollo | Bit | Frequenza | Sicurezza | Note |
|---|---|---|---|---|
| **KeeLoq** | 66 | 433.92/868 | Media-Alta | Il più diffuso: Nice Smilo/FLO2R, Came TOP, BFT Mitto, Beninca |
| **Nice FlorS** | 52 | 433.92 | Media | Nice con rolling code |
| **Came Atomo** | 64 | 433.92 | Alta | Came ultima generazione |
| **FAAC SLH** | 64 | 868.35 | Alta | FAAC rolling proprietario |
| **Somfy RTS** | 56 | 433.42 | Media | Tapparelle/tende Somfy |
| **Marantec** | 32 | 433.92/868 | Media | Garage door EU |
| **Secucode** | 64 | 433.92 | Alta | Implementazione sicura KeeLoq |

> **Nota personale:** Nella pratica, la maggior parte dei cancelli residenziali italiani usa Nice o Came. I Nice più vecchi (Nice FLO a 12 bit) sono codice fisso e si clonano in 5 secondi. I Nice più nuovi (FLOR, Smilo) usano KeeLoq rolling code - significativamente più difficili. FAAC è quasi sempre su 868 MHz con rolling code forte.

---

## Codici Fissi vs Rolling Code

### Codice Fisso - Come Funziona

Un telecomando a codice fisso trasmette **sempre lo stesso messaggio** quando premi il pulsante:

```
Ogni pressione: [SYNC] [ID: 0xA4B3C2] [BUTTON: 01] [STOP]
Ogni pressione: [SYNC] [ID: 0xA4B3C2] [BUTTON: 01] [STOP]
Ogni pressione: [SYNC] [ID: 0xA4B3C2] [BUTTON: 01] [STOP]
```

**Vulnerabilità:** chiunque catturi il segnale può riprodurlo illimitatamente. Il replay attack è banale.

**Come attaccare (su sistemi propri / autorizzati):**
1. Sub-GHz → Read → premi il telecomando → salva il file .sub
2. Sub-GHz → Saved → seleziona il file → Send
3. Il ricevitore non distingue il segnale originale dalla copia

**Protocolli vulnerabili:** Princeton, Nice FLO, Came 12-bit, Linear, Gate TX, Holtek, PT2262

### Rolling Code - Come Funziona

Un telecomando a rolling code genera un **codice diverso ad ogni pressione** grazie a un algoritmo crittografico condiviso con il ricevitore:

```
Pressione 1: [SYNC] [SERIAL] [ENCRYPTED_COUNTER: 0x1A3F] [BUTTON]
Pressione 2: [SYNC] [SERIAL] [ENCRYPTED_COUNTER: 0x7B82] [BUTTON]
Pressione 3: [SYNC] [SERIAL] [ENCRYPTED_COUNTER: 0xC4D1] [BUTTON]
```

Il ricevitore mantiene una **finestra di accettazione** (tipicamente 256 codici futuri). Se il codice ricevuto è all'interno della finestra, lo accetta e avanza il contatore.

### KeeLoq - Il Rolling Code più Diffuso

KeeLoq è un cifrario a blocchi proprietario di Microchip Technology, usato da Nice, Came, BFT, Beninca, Chamberlain e molti altri:

- **Chiave:** 64 bit (chiave crittografica condivisa tra TX e RX)
- **Contatore:** 16 bit (65536 valori prima del rollover)
- **Seriale:** 28 bit (identifica il trasmettitore)
- **Algoritmo:** cifrario a blocchi non-lineare con 528 round
- **Derivazione chiave:** la chiave del singolo telecomando è derivata dalla manufacturer key + serial number

**Vulnerabilità note di KeeLoq:**

1. **Brute force della manufacturer key:** se la chiave del produttore viene compromessa (e molte lo sono state), tutti i telecomandi di quel produttore diventano vulnerabili. Ricercatori hanno estratto le chiavi di Nice, Came e altri tramite side-channel attack sui chip.

2. **RollJam Attack:** l'attaccante usa un jammer per bloccare il segnale del telecomando legittimo mentre cattura il codice rolling valido. L'utente preme di nuovo, l'attaccante cattura anche il secondo codice e rilascia il primo. Ora ha un codice rolling valido non ancora usato.

3. **RollBack Attack:** sfrutta debolezze nell'implementazione del contatore per forzare il ricevitore ad accettare codici precedenti.

4. **Finestra di resync:** molti ricevitori hanno una modalità di risincronizzazione che può essere sfruttata inviando sequenze specifiche di codici.

> **Nota personale:** Il RollJam è l'attacco più pratico contro rolling code, ma richiede hardware aggiuntivo (jammer + ricevitore simultaneo). Il Flipper Zero da solo NON può fare un RollJam classico perchè non può jammare e ricevere contemporaneamente. Tuttavia, il tool "Rolling Flaws" analizza debolezze specifiche nelle implementazioni di vari produttori. In engagement reali, ho trovato che molti sistemi "rolling code" sono in realtà mal configurati o usano firmware vecchio con vulnerabilità note.
