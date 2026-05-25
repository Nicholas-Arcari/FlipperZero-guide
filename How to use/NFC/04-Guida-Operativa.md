# Guida Operativa - Tool per Tool

Questa sezione copre ogni singolo strumento NFC disponibile sul Flipper Zero, con procedure operative dettagliate, output attesi e note pratiche dal campo. L'ordine rispecchia un flusso di lavoro reale durante un penetration test: lettura, analisi, attacco, clonazione, verifica.

---

## NFC (Hub Principale)

**Menu principale:**
- **Read** - Leggi un tag NFC (identificazione + tentativo di lettura completa)
- **Detect Reader** - Ascolta un reader NFC (per MFKey32)
- **Saved** - Gestisci tag salvati
- **Extra Actions** - Funzionalità aggiuntive
- **Add Manually** - Crea un tag da parametri noti

---

## Read - Lettura Tag

Procedura operativa completa:

1. Apri NFC → Read
2. Avvicina il tag/badge alla bobina NFC del Flipper (parte superiore)
3. Il Flipper identifica:
   - Tipo tag (MIFARE Classic, DESFire, NTAG, ecc.)
   - UID (4/7/10 byte)
   - SAK e ATQA
4. Per MIFARE Classic: parte il dictionary attack automatico
   - Barra di progresso per ogni settore
   - Chiavi trovate: settore diventa verde
   - Chiavi non trovate: settore rimane rosso
5. Al termine, premi Save per salvare il dump

**Il file .nfc salvato contiene:**
```
Filetype: Flipper NFC device
Version: 4
Device type: Mifare Classic
UID: 04 A3 B2 C1
ATQA: 00 04
SAK: 08
Mifare Classic type: 1K
Data format version: 2
Block 0: 04 A3 B2 C1 C8 08 04 00 62 63 64 65 66 67 68 69
Block 1: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
...
Key A: FF FF FF FF FF FF
Key B: FF FF FF FF FF FF
Access bits: FF 07 80 69
```

### Interpretazione dell'Output di Lettura

| Campo | Significato | Cosa cercare |
|---|---|---|
| **UID** | Identificatore univoco del tag | Lunghezza (4/7/10 byte), pattern sequenziali tra badge |
| **SAK** | Tipo di tag | 0x08 = Classic 1K (vulnerabile), 0x20 = DESFire (resistente) |
| **ATQA** | Sotto-tipo | Conferma il tipo indicato dal SAK |
| **Key A/B** | Chiavi di settore | FF FF FF FF FF FF = chiavi di default = sistema debole |
| **Access bits** | Permessi di lettura/scrittura | FF 07 80 69 = default = permessi non customizzati |

> **Nota personale:** Quando leggo un badge per la prima volta, la prima cosa che verifico è il SAK. SAK 0x08 mi dice subito che sono di fronte a un MIFARE Classic 1K - il 90% delle volte significherà un dump completo entro 5 minuti. Se vedo SAK 0x20, so che avro' davanti ore di lavoro e probabilmente servirà il Proxmark3.

---

## Detect Reader - Per MFKey32

Procedura per cattura dati dal reader:

1. Apri NFC → Detect Reader
2. Il Flipper attende in modalità ascolto
3. Avvicina il Flipper a un lettore NFC attivo
4. Il lettore tenta di autenticarsi con il "badge" (il Flipper)
5. Il Flipper cattura: nonce del reader, risposta, dati crittografati
6. Ripeti 2-3 volte
7. I dati vengono salvati per l'analisi MFKey

### Checklist Operativa per Detect Reader

| Passo | Azione | Verifica |
|---|---|---|
| 1 | Posiziona il Flipper con la parte superiore verso il lettore | LED NFC lampeggia |
| 2 | Mantieni il contatto per almeno 2 secondi | Counter sullo schermo incrementa |
| 3 | Ripeti 2-3 volte | Almeno 2 catture per settore |
| 4 | Controlla il log | Dati di autenticazione presenti |

> **Nota personale:** Il Detect Reader è una fase critica che richiede calma e precisione. In un engagement, fingersi un dipendente che "ha problemi col badge" funziona sempre - avvicini il Flipper al lettore, aspetti 2 secondi, scuoti la testa come se non funzionasse, ripeti. Nessuno sospetta nulla.

---

## Emulate - Emulazione Tag

Dopo aver letto e salvato un tag, puoi emularlo:

1. Apri NFC → Saved → seleziona il file
2. Premi Emulate
3. Il Flipper si comporta come il tag originale
4. Avvicina il Flipper al lettore → dovrebbe reagire come se fosse il badge originale

**Limiti dell'emulazione:**
- Funziona bene con lettori che controllano solo l'UID
- Funziona con MIFARE Classic se hai il dump completo (tutte le chiavi)
- NON funziona con DESFire (crittografia asimmetrica)
- Alcuni lettori hanno filtri anti-emulazione basati su timing o livello campo

### Matrice Compatibilità Emulazione

| Tipo Tag | Emulazione UID | Emulazione Completa | Note |
|---|---|---|---|
| MIFARE Classic 1K | Si | Si (con dump completo) | ~60% lettori la accettano |
| MIFARE Classic 4K | Si | Si (con dump completo) | Stesse limitazioni del 1K |
| MIFARE Ultralight | Si | Parziale | Alcuni campi non emulabili |
| NTAG 213/215/216 | Si | Buona | Funziona bene per Amiibo e simili |
| DESFire | Solo UID | No | Crittografia impedisce emulazione |
| iClass Legacy | Si | Parziale | Dipende dal lettore |

> **Nota personale:** L'emulazione MIFARE Classic funziona su circa il 60% dei lettori che ho testato. Il restante 40% rifiuta per vari motivi: timing troppo lento, campo troppo debole, o il lettore verifica dati specifici nei settori che non ho nel dump. Per questi casi, uso una Magic Card (vedi [06-Attacchi-e-Difese.md](06-Attacchi-e-Difese.md)) che è un tag fisico vero e proprio.

---

## MFKey

Suite per il recupero delle chiavi MIFARE Classic.

**Procedura completa MFKey32:**

1. Leggi il badge target (NFC → Read) - ottieni dump parziale
2. Attiva Detect Reader → presenta il Flipper al lettore
3. Ripeti 2-3 volte
4. Apri MFKey dall'app menu
5. L'app analizza i dati catturati
6. Le chiavi recuperate vengono aggiunte al dizionario
7. Ri-leggi il badge con le nuove chiavi

**MFKey32v2:** versione migliorata che richiede meno catture e ha un tasso di successo più alto.

### Workflow Completo MFKey32

```
Read Badge (dump parziale)
        |
        v
  Detect Reader (2-3 catture)
        |
        v
  MFKey → Calcolo chiavi
        |
        v
  Chiavi → Dizionario
        |
        v
  Re-Read Badge (dump completo)
        |
        v
  Emulate / Write su Magic Card
```

> **Nota personale:** Il MFKey32 è l'attacco che uso più spesso in engagement reali. Funziona su circa il 70-80% dei sistemi MIFARE Classic che ho incontrato. Il trucco è presentare il Flipper al lettore in modo naturale - durante un social engineering, fingersi un dipendente che "ha problemi col badge" e avvicinare il Flipper al lettore. Servono 2-3 tentativi, 5 secondi ciascuno.

---

## MIFARE Classic Editor

Editor diretto dei settori e blocchi di un tag MIFARE Classic.

**Procedura operativa:**

1. Apri un file .nfc di un MIFARE Classic
2. L'editor mostra tutti i settori e blocchi
3. Seleziona un blocco per modificarlo
4. Modifica i byte (hex)
5. Salva le modifiche

**Blocchi importanti:**
- **Blocco 0:** UID e manufacturer data - non modificabile su tag normali
- **Sector trailer:** chiavi A/B e access bits - modifica con cautela!
- **Blocchi dati:** qui risiede l'informazione utile (ID accesso, credito, contatori)

**Uso nel pentest:**
- Dopo aver dumpato un badge, modificare i dati per testare il sistema
- Cambiare l'ID di accesso per vedere se il sistema verifica l'integrità
- Testare se il sistema accetta dati modificati senza checksum

### Mappa dei Blocchi MIFARE Classic 1K

```
Settore 0:  Blocco 0 [UID + Manufacturer] | Blocco 1 [Dati] | Blocco 2 [Dati] | Blocco 3 [KeyA + ACL + KeyB]
Settore 1:  Blocco 4 [Dati] | Blocco 5 [Dati] | Blocco 6 [Dati] | Blocco 7 [KeyA + ACL + KeyB]
...
Settore 15: Blocco 60 [Dati] | Blocco 61 [Dati] | Blocco 62 [Dati] | Blocco 63 [KeyA + ACL + KeyB]
```

> **Nota personale:** L'Editor è fondamentale per il reverse engineering dei dati nel badge. Dopo aver dumpato un badge, confronto i dati con un secondo badge per trovare le differenze. Spesso il numero della stanza/piano/reparto è in chiaro nei blocchi dati - a volte basta cambiare un byte per passare da "accesso piano 2" a "accesso tutti i piani".

---

## MIFARE Fuzzer

Strumento per inviare comandi non standard o malformati a tag/reader MIFARE.

**Modalità di fuzzing:**
- **UID fuzzing:** genera UID casuali o sequenziali
- **Key fuzzing:** prova chiavi con pattern specifici
- **Command fuzzing:** invia comandi ISO14443 malformati
- **Data fuzzing:** scrive dati casuali nei settori

**Uso:**
- Testare la robustezza di un lettore a input anomali
- Scoprire comportamenti inattesi (crash, bypass autenticazione)
- Identificare lettori che accettano UID specifici senza verifica dati

---

## NFC APDU Runner

Invio manuale di comandi APDU (Application Protocol Data Unit) a smart card NFC.

**Background tecnico:**

APDU è il protocollo di comunicazione tra reader e smart card ISO 7816:
```
Comando APDU:
[CLA] [INS] [P1] [P2] [Lc] [Data] [Le]

Risposta:
[Data] [SW1] [SW2]

SW1 SW2 = 90 00 → successo
SW1 SW2 = 6A 82 → file non trovato
SW1 SW2 = 69 82 → sicurezza non soddisfatta
```

**Procedura operativa:**

1. Apri APDU Runner
2. Avvicina una smart card NFC
3. Inserisci il comando APDU in hex
4. Invia → visualizza la risposta

**Comandi utili:**
```
SELECT (by AID):       00 A4 04 00 [len] [AID]
READ BINARY:           00 B0 [P1] [P2] [Le]
GET DATA:              00 CA [P1] [P2] [Le]
VERIFY PIN:            00 20 00 [P2] [Lc] [PIN]
GET CHALLENGE:         00 84 00 00 [Le]
READ RECORD:           00 B2 [record] [P2] [Le]
```

### Tabella Codici di Risposta APDU

| SW1 SW2 | Significato | Azione |
|---|---|---|
| 90 00 | Successo | Comando eseguito correttamente |
| 6A 82 | File non trovato | L'AID o il file specificato non esiste |
| 69 82 | Sicurezza non soddisfatta | Autenticazione necessaria prima di questo comando |
| 6A 86 | Parametri P1/P2 errati | Controlla i parametri del comando |
| 6D 00 | Istruzione non supportata | La card non supporta questo comando |
| 6E 00 | Classe non supportata | Valore CLA errato |
| 6F 00 | Errore generico | Errore interno della card |
| 61 XX | Dati disponibili | Usa GET RESPONSE per leggere XX byte |
| 6C XX | Lunghezza errata | Ripeti con Le = XX |

> **Nota personale:** L'APDU Runner è indispensabile per l'analisi di smart card sconosciute. Lo uso per enumerare le applicazioni presenti sulla card (SELECT con AID diversi) e capire la struttura del file system. È l'equivalente NFC di una shell su un sistema sconosciuto - permette di esplorare cosa c'è dentro.

---

## NFC Comparator

Confronta due dump NFC per identificare differenze.

**Procedura operativa:**

1. Dump del badge prima dell'operazione (es. prima di passare il tornello)
2. Dump del badge dopo l'operazione (es. dopo aver passato il tornello)
3. Apri Comparator → carica i due file
4. Le differenze sono evidenziate byte per byte

**Uso nel reverse engineering:**
- Identificare quale settore/blocco viene modificato dal sistema
- Scoprire contatori (valore che incrementa ad ogni utilizzo)
- Trovare timestamp o log di accesso
- Capire come il sistema gestisce il credito (card prepagate)

### Metodologia di Analisi Differenziale

| Tipo di Differenza | Pattern | Interpretazione |
|---|---|---|
| Singolo byte incrementale | 0x0A → 0x0B | Contatore accessi |
| Blocco di 4 byte che cambia | Valore variabile | Timestamp o rolling code |
| Singolo bit flip | 0x00 → 0x01 | Flag stato (dentro/fuori) |
| Intero settore diverso | Tutti i byte cambiano | Dati crittografati / rolling key |

> **Nota personale:** Il Comparator è il mio strumento preferito per il reverse engineering di card trasporti. Confrontando il dump prima e dopo un passaggio al tornello, riesco a identificare esattamente dove il sistema scrive il credito residuo. In una card metro italiana, il credito era nei byte 6-7 del settore 4, codificato come intero a 16 bit little-endian. Cambiando quei 2 byte, il credito cambiava. Finding critico.

---

## NFC Dict Manager

Gestione del dizionario chiavi MIFARE.

**Procedura:**
1. Apri Dict Manager
2. Visualizza le chiavi attualmente nel dizionario
3. Aggiungi nuove chiavi (dalla clipboard, da file, manualmente)
4. Rimuovi chiavi obsolete
5. Importa/esporta il dizionario

**Best practice:**
- Mantieni un dizionario personalizzato con chiavi trovate in engagement
- Condividi (in modo sicuro) chiavi tra membri del team
- Organizza per tipo di sistema (hotel, uffici, trasporti)

---

## NFC Magic

Supporto per tag "Magic" - tag speciali con UID scrivibile e comandi backdoor.

**Tipi di Magic Card:**

| Tipo | UID Scrivibile | Backdoor | Note |
|---|---|---|---|
| **Gen1 (Chinese Magic)** | Si, via comando | WUPC (40xx) | Rilevabile da lettori anti-magic |
| **Gen2 (CUID)** | Si, via write diretto | Nessuna | Non rilevabile come Gen1, ma meno compatibile |
| **Gen3 (UFUID)** | Si, una volta (lockabile) | Nessuna | Comportamento più simile a tag reale |
| **Gen4 (Ultimate Magic)** | Si, illimitato | GDM (custom) | Il più versatile, supporta 1K/4K, cambio SAK/ATQA |

**Procedura - Clonazione su Magic Card Gen1:**

1. Leggi il badge originale (dump completo necessario)
2. Inserisci una Magic Card Gen1 sul Flipper
3. NFC → Magic → Write
4. Seleziona il dump da scrivere
5. Il Flipper scrive tutti i settori incluso il Blocco 0 (UID)
6. Verifica: leggi la Magic Card e confronta con l'originale

> **Nota personale:** Le Magic Card Gen1 sono le più facili da usare ma vengono rilevate da lettori moderni (il lettore invia il comando WUPC e se il tag risponde, sa che è una Magic). Le Gen4 (Ultimate Magic) sono le migliori per il pentest - non rilevabili e completamente programmabili. Costano circa 2-3 euro l'una su AliExpress. Tengo sempre 10-15 Magic Card Gen4 nel kit da pentest.

---

## NFC Sniffer

Intercetta la comunicazione tra un lettore NFC e un tag.

**Procedura operativa:**

1. Posiziona il Flipper tra il lettore e il tag (fisicamente difficile - lo spazio è di pochi cm)
2. Attiva NFC Sniffer
3. Presenta il tag al lettore con il Flipper nel mezzo
4. Il Flipper cattura i dati scambiati
5. Salva il log per analisi

**Limiti:**
- Posizionamento fisico molto critico
- Non cattura tutto il traffico (perdita di pacchetti)
- Per sniffing professionale, usa Proxmark3 o HydraNFC

---

## NFC Relay

Relay attack NFC - estende la distanza tra reader e tag.

**Come funziona:**
- Due Flipper (o Flipper + telefono NFC)
- Flipper 1 (Proxy): vicino al lettore, emula il tag
- Flipper 2 (Relay): vicino al badge reale, legge il tag
- I comandi del reader vengono inoltrati dal Proxy al Relay e viceversa
- Il reader "pensa" di comunicare direttamente con il badge

**Implicazioni di sicurezza:**
- Permette di "estendere" un badge a distanza illimitata (con rete)
- Un attaccante potrebbe aprire una porta usando il badge di un dipendente che si trova in un'altra stanza/edificio
- Difesa: relay protection (timeout stretti, distance bounding)

---

## MFDesfire Auth

Tester di autenticazione per MIFARE DESFire.

**Procedura:**
1. Avvicina una card DESFire
2. Seleziona il tipo di autenticazione (DES, 3DES, AES)
3. Inserisci la chiave
4. Avvia il test → successo/fallimento

**Uso:**
- Verificare se una card DESFire usa chiavi di default
- Testare chiavi recuperate da altre fonti
- Enumerare le applicazioni e i file accessibili con una chiave

### Chiavi di Default DESFire da Testare

```
00 00 00 00 00 00 00 00                - DES default key
00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  - 3DES default key
00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  - AES-128 default key
```

> **Nota personale:** Sono rimasto sorpreso da quante card DESFire in produzione usino ancora la chiave di default (tutti zeri). Il sistema è sicuro, ma se chi lo configura lascia la chiave di default, tutta la sicurezza crittografica crolla. Sempre testare le chiavi di default prima di tutto.

---

## Passport Reader

Lettore NFC per documenti di viaggio elettronici (eMRTD).

**Background tecnico:**

I passaporti elettronici contengono un chip NFC con:
- **DG1:** MRZ data (nome, cognome, data nascita, numero documento)
- **DG2:** foto del titolare (JPEG2000)
- **DG3:** impronte digitali (accesso ristretto)
- **DG14/15:** chiavi per autenticazione

**Procedura operativa:**

1. Apri Passport Reader
2. Inserisci i dati MRZ (la stringa in fondo alla pagina dati del passaporto)
3. La MRZ genera la chiave BAC (Basic Access Control)
4. Avvicina il passaporto al Flipper
5. Il Flipper autentica con BAC e legge i dati base

**Sicurezza:**
- BAC è necessario → senza i dati MRZ non puoi leggere nulla
- PACE (Password Authenticated Connection Establishment) è più sicuro ed è usato nei documenti recenti
- I dati sono firmati digitalmente dal Paese emittente

### Struttura MRZ e Derivazione Chiave BAC

```
MRZ Linea 1: P<ITAROSSI<<MARIO<<<<<<<<<<<<<<<<<<<<<<<<
MRZ Linea 2: YA12345678ITA8001015M3012315<<<<<<<<<<<04

Chiave BAC derivata da:
- Numero documento: YA1234567
- Data di nascita: 800101
- Data di scadenza: 301231
```

> **Nota personale:** Il Passport Reader è utile per verificare che i documenti di identità dei dipendenti siano autentici durante un audit di sicurezza fisica. La verifica della firma digitale conferma che il documento non è stato alterato. Non usare mai questo strumento senza autorizzazione esplicita - leggere il passaporto di qualcuno senza consenso è un reato.

---

## PicoPass / iClass

Gestione tag iClass/PicoPass di HID Global.

**Background:**

iClass è il sistema di accesso più diffuso in ambienti enterprise/governativi:
- **iClass Legacy:** chiave master nota → vulnerabile, leggibile dal Flipper
- **iClass SE:** chiave diversificata → non vulnerabile ad attacchi generici
- **iClass SEOS:** ultima generazione, sicurezza robusta

**Procedura per iClass Legacy:**

1. NFC → Read → avvicina il badge iClass
2. Il Flipper identifica come PicoPass
3. Con la chiave master nota, legge i dati
4. Salva il dump
5. Emula o scrivi su una card compatibile

> **Nota personale:** I badge iClass Legacy sono sorprendentemente comuni anche in edifici "sicuri". Ho trovato iClass Legacy in banche, uffici governativi e sedi aziendali che spendono migliaia di euro in sicurezza IT ma non hanno mai aggiornato il sistema di badge. Il Flipper li legge e clona in 10 secondi. È un finding ricorrente nei miei report.

---

## SEADER

Analizzatore di protocolli Secure Element per card con SE integrato.

**Uso:** invio di comandi APDU specializzati per esplorare il Secure Element di card bancarie, SIM, o smart card governative. Richiede conoscenza specifica dei protocolli del SE target.

---

## UID Brute Smarter

Bruteforce ottimizzato di UID NFC.

**Come funziona:**
- Genera UID in sequenza o con pattern specifici
- Emula ogni UID e lo presenta al lettore
- Se il lettore accetta (apre la porta), l'UID valido è trovato

**Quando usarlo:**
- Sistemi che verificano SOLO l'UID senza leggere i dati del tag
- Sistemi con UID prevedibili (es. badge sequenziali)
- Come ultimo resort quando non si riesce a ottenere il dump

> **Nota personale:** Pochi sistemi moderni verificano solo l'UID, ma esistono. Ho trovato un sistema di accesso in un condominio di lusso che accettava qualsiasi tag con un UID che iniziava per "04 A3" - bastava enumerare gli ultimi 2 byte (65536 combinazioni). Il UID Brute ha trovato un accesso valido in meno di un'ora.

---

## Cyborg Detector

Rilevatore di impianti NFC sottocutanei (biohacking).

**Procedura:**
1. Attiva il Detector
2. Scansiona la zona della mano/avambraccio (tipicamente tra pollice e indice)
3. Se rileva un campo NFC, segnala la presenza dell'impianto
4. Può tentare di leggere il tipo di tag impiantato

---

## NFC Maker / NFC URL

Strumenti per creare tag NFC con contenuto NDEF.

**Tipi di record NDEF:**
- **URL:** apre un link nel browser
- **Testo:** mostra un testo
- **WiFi:** configura automaticamente una rete WiFi
- **vCard:** aggiunge un contatto
- **Bluetooth pairing:** avvia il pairing BT
- **App launch:** apre un'app specifica

**Uso nel pentest:**
- Creare tag NFC malevoli che redirigono a pagine di phishing
- Tag che configurano una rete WiFi evil twin
- Tag che avviano app specifiche per social engineering

---

## NFC E-Ink Tags

Gestione di tag NFC con display e-ink integrato (es. Waveshare, Good Display).

**Procedura:**
1. Avvicina il tag e-ink al Flipper
2. Scrivi il contenuto desiderato (testo, immagine monocromatica)
3. Il tag aggiorna il display

---

## NFC Keyboard

Trasforma il Flipper in un emulatore di tastiera via NFC.

**Come funziona:**
- Programma una sequenza di tasti
- Quando il Flipper tocca un lettore NFC di tipo HID, invia la sequenza
- Simile a BadUSB ma via NFC

**Uso:** inserimento automatico di password o comandi su terminali con lettore NFC.

---

## Altre App NFC

- **Amusement IC:** lettura card per sale giochi e parchi
- **MetroFlip:** analisi card trasporti metropolitani
- **Mi Band NFC:** lettura dati NFC braccialetti Xiaomi
- **MiZip Balance Editor:** lettura card MiZip
- **NFC Playlist:** creazione playlist multimediali su tag
- **Open Print Tag:** analisi tag stampanti
- **SLI Writer:** scrittura tag SLI
- **T-Union Master:** card trasporti cinesi
- **TuLlave:** card trasporti sudamericani
- **UdECard:** supporto carte UdE
- **VB Migration Assistant:** migrazione formati legacy
- **Weebo:** tool NFC avanzati

---

## Riepilogo Workflow Operativo

```
1. IDENTIFICAZIONE     →  NFC Read → SAK/ATQA → Tipo tag
2. LETTURA             →  Dictionary Attack → Dump parziale/completo
3. KEY RECOVERY        →  MFKey32 (se chiavi mancanti) → Detect Reader → Calcolo
4. DUMP COMPLETO       →  Re-Read con nuove chiavi → Salvataggio
5. ANALISI             →  Editor + Comparator → Reverse engineering dati
6. CLONAZIONE          →  Emulate (software) o Magic Card Write (hardware)
7. VERIFICA            →  Test al lettore target → Documentazione finding
```

> **Nota personale:** Questo workflow è il mio standard per ogni engagement NFC. La fase più critica è la 2-3: il dictionary attack + MFKey32. Se riesci a ottenere un dump completo, il resto è meccanico. Se non riesci, devi passare al Proxmark3 per attacchi più sofisticati. Il Flipper copre l'80% degli scenari reali - per il restante 20%, serve attrezzatura dedicata.
