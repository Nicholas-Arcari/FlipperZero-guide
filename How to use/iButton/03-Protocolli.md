## Protocolli Dettagliati

### DS1990A (Dallas) - Il Protocollo Standard

Il **DS1990A** è il dispositivo iButton più diffuso al mondo per sistemi di identificazione a contatto. È un chip minimo che contiene esclusivamente un ROM code di 64 bit - niente memoria scrivibile, niente crittografia, niente logica applicativa.

**Specifiche tecniche:**

| Parametro | Valore |
|---|---|
| ROM Code | 64 bit (8 byte) |
| Family Code | 0x01 |
| Serial Number | 48 bit (univoco globale) |
| CRC | 8 bit (DOW CRC) |
| Tensione operativa | 2.8V - 6.0V |
| Corrente assorbita | < 5 mA |
| Temperatura operativa | -40C a +85C |
| Velocità 1-Wire | Standard (16.3 kbit/s) e Overdrive (142 kbit/s) |
| Package | MicroCAN (16 mm acciaio inox) |

**Struttura del ROM Code DS1990A:**

```
Byte 0:    0x01              (Family Code - identifica DS1990A)
Byte 1-6:  XX:XX:XX:XX:XX:XX (48-bit Serial Number)
Byte 7:    YY                (CRC-8)

Esempio reale: 01:A3:5F:2B:00:00:00:E7
              |  |              |  |
              |  +-- Serial ----+  |
              |                    |
              Family Code       CRC-8
```

**Come funziona la lettura:**

1. Tocchi la chiave DS1990A sul lettore
2. Il lettore invia un Reset Pulse (480+ us LOW)
3. La chiave risponde con Presence Pulse (60-240 us LOW)
4. Il lettore invia il comando Read ROM (0x33)
5. La chiave trasmette i 64 bit del ROM code, LSB first
6. Il lettore calcola il CRC-8 sui primi 56 bit e lo confronta col byte 7
7. Se il CRC è valido, il lettore cerca il ROM code nel database interno
8. Se trovato: azione (apre porta, attiva citofono, registra presenza)

Tutta la "sicurezza" si basa su questo: **un numero trasmesso in chiaro, senza alcuna autenticazione challenge-response**. Chiunque legga la chiave una volta ha tutte le informazioni necessarie per clonarla.

**Diffusione in Italia:**

Il DS1990A è enormemente diffuso nei citofoni condominiali italiani, in particolare:

- Installazioni anni 2000-2010 (il periodo d'oro delle chiavi iButton in Italia)
- Marchi comuni: Urmet, Comelit, Terraneo, Elvox, BPT
- Tipicamente usato in condomini da 10-100 unità
- Il costo bassissimo del sistema (chiave ~1-2 euro, lettore ~20-50 euro) ne ha favorito l'adozione massiva

> **Nota personale:** Nella mia esperienza, circa il 60-70% dei citofoni a chiave che trovo in Italia usa DS1990A. È una percentuale enorme. In un audit condominiale che ho fatto a Milano, su 5 palazzi esaminati, 4 avevano sistemi DS1990A senza alcuna protezione aggiuntiva. Il quinto aveva Cyfral. Nessuno aveva sistemi con crittografia o challenge-response. La clonazione è banale - letteralmente 3 secondi di contatto con la chiave originale.

### Cyfral - Protocollo Proprietario Russo

**Cyfral** è un protocollo proprietario sviluppato dalla società russa Cyfral per sistemi citofonici. È il protocollo di accesso a contatto più diffuso nell'ex-Unione Sovietica e si trova comunemente anche in Italia, specialmente in zone con comunità dell'est Europa o in installazioni fatte da aziende che importano componentistica russa.

**Come funziona:**

A differenza del 1-Wire Dallas che usa timing slot digitali, Cyfral utilizza una **comunicazione a impulsi analogica** basata su rapporti di resistenza:

- Il lettore Cyfral fornisce alimentazione continua sulla sonda
- La chiave Cyfral modifica la corrente assorbita in pattern specifici
- Il lettore interpreta le variazioni di corrente come bit di dati

**Struttura del segnale Cyfral:**

Il protocollo Cyfral trasmette un codice di **8 bit** (alcune varianti fino a 36 bit) tramite una sequenza di impulsi:

1. **Start condition:** la chiave inizia assorbendo corrente in un pattern specifico
2. **Bit encoding:** ogni bit è codificato come rapporto tra durata HIGH e durata LOW di un impulso
   - **Bit 0:** rapporto basso (impulso corto rispetto alla pausa)
   - **Bit 1:** rapporto alto (impulso lungo rispetto alla pausa)
3. **Ripetizione:** il codice viene trasmesso ripetutamente finchè la chiave resta a contatto

**Differenze chiave da Dallas:**

| Caratteristica | Dallas (1-Wire) | Cyfral |
|---|---|---|
| Standard | Aperto (Dallas/Maxim) | Proprietario |
| Bit del codice | 64 bit (48 significativi) | 8-36 bit |
| Comunicazione | Timing slot digitali | Impulsi analogici (rapporto resistivo) |
| CRC | Si (8-bit DOW CRC) | No (nella versione base) |
| Alimentazione | Parassita da DQ | Fornita dal lettore |
| Crittografia | No | No |
| Complessità keyspace | 2^48 (~281 trilioni) | 2^8-2^36 (256 - 68 miliardi) |
| Diffusione in Italia | Alta (citofoni moderni) | Media (citofoni economici, est Europa) |

**Lettori Cyfral comuni:**

- **CCD-2094** - il lettore citofonico Cyfral più diffuso
- **CCD-2094.1/M** - variante con memoria per più codici
- **Eltis** - marca associata che usa protocollo Cyfral

> **Nota personale:** Ho incontrato lettori Cyfral soprattutto in due contesti in Italia: palazzi con inquilini dell'est Europa dove l'installatore ha usato componentistica di importazione, e vecchie installazioni in periferia dove il costo era il fattore decisivo. Il protocollo è più debole del Dallas dal punto di vista del keyspace - 8 bit significano solo 256 possibili codici nella versione base. Alcuni sistemi Cyfral possono essere letteralmente forzati a mano provando tutte le combinazioni in pochi minuti. Questo rende il fuzzing estremamente efficace.

### Metakom - Altro Protocollo Proprietario Russo

**Metakom** (nome completo: Metakom, dal russo "Metal Communication") è il terzo protocollo supportato dal Flipper Zero per iButton. È un protocollo proprietario russo usato nei citofoni Metakom, diffuso nell'ex-URSS e in alcune installazioni in Italia e nel sud-est Europa.

**Come funziona:**

Metakom usa un approccio simile a Cyfral ma con un protocollo di segnalazione diverso:

- Comunicazione basata su **impulsi a durata variabile**
- La chiave codifica il proprio ID variando la durata degli impulsi trasmessi
- Il lettore misura le durate e decodifica il codice

**Struttura del segnale Metakom:**

1. **Sincronizzazione:** impulso iniziale di sincronizzazione
2. **Data bits:** sequenza di impulsi dove la durata codifica 0 o 1
   - **Bit 0:** impulso breve seguito da pausa lunga
   - **Bit 1:** impulso lungo seguito da pausa breve
3. **Codice completo:** tipicamente 32 bit di dato utile
4. **Ripetizione continua** durante il contatto

**Differenze da Cyfral:**

| Caratteristica | Cyfral | Metakom |
|---|---|---|
| Encoding | Rapporto resistivo | Durata impulsi |
| Lunghezza codice | 8-36 bit | 32 bit tipici |
| Keyspace | Piccolo (256 - 68 mld) | Medio (~4.29 miliardi con 32 bit) |
| Sync | Pattern di corrente | Impulso di sincronizzazione |
| Diffusione Italia | Media | Bassa-media |
| Marca principale | Cyfral/Eltis | Metakom |

**Diffusione:**

- Russia e Ucraina: molto comune nei palazzi residenziali
- Italia: raro, presente in alcune installazioni in grandi città con comunità dell'est
- Est Europa (Bulgaria, Romania, Moldova): moderatamente diffuso

> **Nota personale:** Metakom è il protocollo che incontro meno in Italia, ma quando lo trovo è quasi sempre in contesti dove l'intero sistema citofonico è stato importato dall'est. Il keyspace di 32 bit lo rende più resistente al fuzzing rispetto a Cyfral, ma 4.29 miliardi di combinazioni sono comunque un numero che, con il giusto rate di tentativi e un po' di pazienza, non è irraggiungibile. In pratica pero', il fuzzing su Metakom richiede ore-giorni, non minuti come con Cyfral.

### RW1990 - La Versione Scrivibile

Il **RW1990** è un chip iButton compatibile DS1990A ma con una differenza fondamentale: il ROM code è **riscrivibile**. Se il DS1990A è programmato in fabbrica con un seriale permanente, il RW1990 permette di scrivere qualsiasi ROM code di 64 bit - è l'equivalente iButton del **T5577** nel mondo RFID 125 kHz.

**Specifiche tecniche RW1990:**

| Parametro | Valore |
|---|---|
| Compatibilità | Emula DS1990A (family code 0x01) |
| ROM Code | 64 bit, scrivibile |
| Numero scritture | Tipicamente ~100.000 cicli |
| Alimentazione | Parassita da DQ |
| Velocità | Standard 1-Wire |
| Costo | ~0.50-2 euro (acquistabile online) |

**Come funziona la programmazione:**

La scrittura del RW1990 richiede una procedura specifica:

1. **Invio comando di sblocco scrittura:** una sequenza proprietaria che mette il chip in modalità programmazione
2. **Scrittura byte per byte:** i 64 bit del nuovo ROM code vengono scritti un byte alla volta
3. **Verifica:** lettura del ROM code scritto per confermare la programmazione
4. **Blocco (opzionale):** alcuni RW1990 supportano un "lock" che impedisce ulteriori scritture

**Processo sul Flipper Zero:**

1. Leggi la chiave originale DS1990A - salva il file `.ibtn`
2. Inserisci un RW1990 vergine o da sovrascrivere
3. Vai su iButton → Write → seleziona il file salvato
4. Appoggia il RW1990 sul pad iButton del Flipper
5. Il Flipper programma il RW1990 con il ROM code della chiave originale
6. Verifica automatica - il Flipper legge il RW1990 per confermare

**Il risultato è un clone fisico perfetto** - il RW1990 programmato è elettricamente indistinguibile dall'originale DS1990A per qualsiasi lettore. Non c'è modo per un lettore standard di distinguere un originale da un clone.

**Dove acquistare RW1990:**

- AliExpress: ~0.30-0.50 euro a pezzo (in lotti da 10+)
- Amazon: ~1-2 euro a pezzo
- Shop specializzati in sicurezza fisica e fabbri

> **Nota personale:** Il RW1990 è lo strumento di clonazione iButton per eccellenza. Ne tengo sempre una decina nel kit - costano pochissimo e sono fondamentali per dimostrare a un cliente la vulnerabilità del suo sistema di accesso. "Guarda, ho clonato la chiave del tuo citofono in 5 secondi, ecco il clone fisico che funziona identicamente" è una dimostrazione che ha un impatto molto maggiore rispetto a un emulazione da Flipper. Il clone fisico funziona anche senza il Flipper - è una chiave permanente.

### TM1990 - Variante Compatibile

Il **TM1990** (dove TM sta per Touch Memory, il nome generico russo per i dispositivi a contatto) è una variante del DS1990A prodotta da vari costruttori, inclusi produttori cinesi e russi. È elettricamente compatibile con il DS1990A:

- Stesso protocollo 1-Wire
- Stesso family code 0x01
- Stesso formato ROM code a 64 bit
- Stessa interfaccia fisica MicroCAN

Le differenze sono principalmente di marca e produzione - non ci sono differenze funzionali rilevanti per il pentesting. Il Flipper li legge e li emula esattamente come i DS1990A.

Alcune varianti TM1990 note:

- **TM1990A** - clone diretto del DS1990A
- **TM1990A-F5** - versione in package F5 (il più comune)
- **TM2004** - variante con memoria aggiuntiva (rara nei sistemi di accesso)

In contesto operativo, trattare TM1990 e DS1990A come identici è sempre corretto.

---

