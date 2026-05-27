## Funzionalità BLE del Flipper Zero

Il Flipper Zero offre quattro categorie principali di funzionalità BLE:

### 1. BLE Spam

La funzionalità BLE più nota e virale del Flipper. Invia advertisement packets crafted che triggerano popup di pairing su dispositivi Apple, Samsung, Google e Windows nelle vicinanze.

**Come funziona a livello tecnico:**

Il BLE Spam sfrutta i meccanismi di proximity pairing implementati dai vendor:

1. **Il Flipper genera advertising packets** con Manufacturer Specific Data (AD Type 0xFF) contenente il Company ID del vendor target e payload che simulano un dispositivo specifico
2. **L'advertising viene ripetuto** rapidamente (intervallo minimo ~20ms) sui tre canali advertising
3. **I dispositivi nelle vicinanze** ricevono il pacchetto e il loro OS riconosce il Company ID
4. **Il sistema operativo target** interpreta il payload come un dispositivo legittimo nelle vicinanze e mostra il popup di pairing all'utente
5. **L'utente vede** il popup "AirPods Pro Nearby" o "Galaxy Buds Found" sul proprio schermo

Il Flipper cambia continuamente il MAC address sorgente (random address) e il payload per generare popup multipli e diversi in rapida successione. In modalità "all" spamma tutti i vendor simultaneamente.

**Disponibilità:**

Il BLE Spam è disponibile nei firmware custom (Xtreme, Momentum, RogueMaster, Unleashed) come applicazione dedicata. Il firmware ufficiale Flipper NON include il BLE Spam.

**Menu tipico:**

```
BLE Spam
  |
  +-- Apple
  +-- Samsung
  +-- Google (Fast Pair)
  +-- Windows (Swift Pair)
  +-- All (tutti i vendor)
  +-- Stop
```

> **Nota personale:** Il BLE Spam è la feature che ha reso virale il Flipper su TikTok e social media. In contesti professionali, lo uso esclusivamente per demo di awareness sulla sicurezza BLE - mai in ambienti non autorizzati. L'effetto è immediato e visivamente impressionante: una stanza piena di popup è il modo più efficace per dimostrare a un board aziendale che il BLE non è "sicuro per default".

### 2. BLE App Companion

Il Flipper Zero si connette allo smartphone tramite BLE per il controllo remoto e la gestione del dispositivo. Questa è la funzionalità BLE "legittima" principale.

**Funzionamento:**

- Il Flipper agisce come **periferica BLE** (GATT server)
- Lo smartphone con l'app Flipper (iOS/Android) agisce come **central** (GATT client)
- La connessione utilizza il **Flipper RPC Protocol** su un servizio GATT custom (Nordic UART Service - NUS)
- UUID del servizio NUS: `6E400001-B5A3-F393-E0A9-E50E24DCCA9E`
- UUID TX characteristic: `6E400003-B5A3-F393-E0A9-E50E24DCCA9E`
- UUID RX characteristic: `6E400002-B5A3-F393-E0A9-E50E24DCCA9E`

**Cosa puoi fare via BLE companion:**

- Aggiornare il firmware OTA (Over The Air)
- Gestire il file system del Flipper (upload/download file)
- Eseguire comandi remoti (avviare app, controllare GPIO)
- Monitorare lo stato del dispositivo (batteria, storage)
- Inviare file .sub, .rfid, .nfc, .ir al Flipper
- Controllare Sub-GHz, IR, GPIO da smartphone

**Sicurezza della connessione companion:**

- Pairing con chiave numerica (6 cifre) mostrata sul display del Flipper
- Encryption AES-CCM dopo il pairing
- Bonding per riconnessioni automatiche
- Il Flipper mostra un popup di conferma per ogni nuova connessione

**Protocollo Flipper RPC:**

Il protocollo di comunicazione è basato su Protocol Buffers (protobuf) serializzati e trasmessi su NUS. I messaggi includono:

- `StorageReadRequest` / `StorageReadResponse` - Lettura file
- `StorageWriteRequest` - Scrittura file
- `AppStartRequest` - Avvio applicazione
- `GpioSetPinMode` / `GpioWritePin` - Controllo GPIO
- `SystemPingRequest` / `SystemPingResponse` - Keep-alive

La comunicazione è bidirezionale e asincrona. Il throughput effettivo su BLE con NUS è tipicamente 5-15 KB/s, il che spiega perchè il trasferimento di file grandi via BLE è lento (un firmware update di 1 MB richiede diversi minuti).

### 3. BLE HID (BadBT)

Il Flipper può presentarsi come un dispositivo **HID (Human Interface Device)** via BLE - in pratica, una tastiera o un mouse Bluetooth wireless. Questa funzionalità è conosciuta come **BadBT** (analogia con BadUSB, ma via Bluetooth).

**Come funziona:**

1. Il Flipper espone il servizio **HID over GATT** (UUID: 0x1812)
2. Il target device (PC, smartphone, tablet) vede il Flipper come una tastiera/mouse Bluetooth
3. L'utente target accetta il pairing (o il pairing avviene automaticamente se configurato)
4. Il Flipper invia keystroke e movimenti mouse arbitrari
5. Il target esegue i comandi ricevuti come se fossero da una tastiera fisica

**Profilo HID BLE:**

Il servizio HID su GATT espone queste characteristic:

| Characteristic | UUID | Funzione |
|---|---|---|
| HID Information | 0x2A4A | Versione HID, country code |
| Report Map | 0x2A4B | Descriptor che descrive i report (layout tastiera/mouse) |
| Report | 0x2A4D | I report effettivi (keystroke, mouse movement) |
| Protocol Mode | 0x2A4E | Boot Protocol o Report Protocol |
| Boot Keyboard Input Report | 0x2A22 | Report tastiera in boot mode |
| Boot Keyboard Output Report | 0x2A32 | LED status (Caps Lock, etc.) |

**Differenze chiave BadBT vs BadUSB:**

| Aspetto | BadUSB (USB) | BadBT (Bluetooth) |
|---|---|---|
| Connessione | Fisica (cavo USB) | Wireless (BLE, fino a 10-15m) |
| Richiede accesso fisico | Si, al momento dell'inserimento | No, dopo il pairing iniziale |
| Pairing richiesto | No (plug-and-play) | Si (richiede accettazione utente) |
| Velocità keystroke | Molto alta (~100+ char/sec) | Più lenta (~30-50 char/sec) |
| Visibilità | Cavo USB visibile | Nessun cavo visibile |
| Persistenza | Solo quando inserito | Può riconnettersi dopo bonding |
| Detection | Device Manager mostra HID | Bluetooth settings mostra dispositivo |
| Portata | 0m (contatto fisico) | 5-15m tipico |

**Script BadBT:**

Il Flipper usa lo stesso formato di script DuckyScript usato per BadUSB, con estensioni per il BLE:

```
REM BadBT Example - Open terminal on macOS
DELAY 2000
GUI SPACE
DELAY 500
STRING Terminal
DELAY 500
ENTER
DELAY 1000
STRING echo "BadBT payload executed"
ENTER
```

**Processo di attacco BadBT:**

1. Caricare lo script DuckyScript sul Flipper (SD card, cartella `/badbt/`)
2. Avviare l'app BadBT sul Flipper
3. Il Flipper inizia l'advertising come tastiera BLE
4. Il target deve accettare il pairing
5. Una volta connesso, il Flipper esegue lo script

Il punto critico è il **pairing**: a differenza del BadUSB (che è plug-and-play), il BadBT richiede che l'utente target accetti la connessione Bluetooth. Questo limita significativamente gli scenari di attacco rispetto al BadUSB.

Tuttavia, in scenari dove il target ha già accettato il pairing (social engineering, accesso pregresso, dispositivo non presidiato con auto-accept), il BadBT è potente perchè può operare a distanza e senza contatto fisico.

> **Nota personale:** Il BadBT ha un vantaggio tattico sottovalutato: la riconnessione dopo bonding. Se riesci a fare il pairing iniziale (magari durante una demo "innocua"), puoi riconnetterti in un secondo momento senza che il target debba accettare di nuovo. In un physical pentest, ho usato questa tecnica: pairing durante una presentazione "di test", poi esecuzione del payload il giorno dopo dalla stanza accanto. L'utente non ha visto nulla. Ovviamente, tutto autorizzato e nel perimetro dell'engagement.

### 4. BLE Scanner

Il Flipper può scansionare l'ambiente per dispositivi BLE nelle vicinanze, mostrando informazioni dettagliate su ogni dispositivo trovato.

**Cosa rileva lo scanner:**

- **MAC Address** - Indirizzo del dispositivo (spesso randomizzato)
- **RSSI** - Received Signal Strength Indicator (potenza del segnale, in dBm)
- **Nome dispositivo** - Se presente nell'advertising (Local Name)
- **Servizi esposti** - UUID dei servizi GATT advertised
- **Manufacturer Specific Data** - Dati proprietari del vendor
- **TX Power Level** - Potenza dichiarata dal dispositivo
- **Advertising Type** - Connectable, scannable, non-connectable
- **Flags** - LE General Discoverable, BR/EDR Not Supported, etc.

**Interpretazione RSSI:**

| RSSI (dBm) | Distanza Approssimativa | Qualità |
|---|---|---|
| -30 a -50 | < 1 metro | Eccellente, dispositivo vicinissimo |
| -50 a -65 | 1-3 metri | Buona, stessa stanza |
| -65 a -75 | 3-10 metri | Discreta, potrebbe essere in stanza adiacente |
| -75 a -85 | 10-20 metri | Debole, al limite della portata |
| -85 a -100 | 20+ metri | Molto debole, connessione instabile |

L'RSSI è utile per stimare la prossimità ma NON è un indicatore preciso di distanza. Muri, orientamento dell'antenna, interferenze e riflessioni rendono la stima molto approssimativa.

**Limiti dello scanner Flipper:**

Lo scanner del Flipper è un **passive/active scanner** che opera sui tre canali advertising. NON è uno sniffer completo:

- Vede solo advertising packets, non il traffico dati su connessioni attive
- Non può decodificare connessioni crittografate
- Non può intercettare il pairing di altri dispositivi
- Non può fare MITM su connessioni esistenti
- Vede solo i canali advertising (37, 38, 39), non i 37 canali dati

Per sniffing BLE completo serve hardware dedicato (Ubertooth, nRF52840 dongle, HackRF con gr-bluetooth).

---

