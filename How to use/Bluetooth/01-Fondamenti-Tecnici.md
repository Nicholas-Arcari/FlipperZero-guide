## Fondamenti Tecnici

### Bluetooth Low Energy vs Bluetooth Classic

Prima di tutto, è fondamentale capire che il Flipper Zero utilizza **esclusivamente Bluetooth Low Energy (BLE)**, non Bluetooth Classic. Sono due stack completamente diversi, anche se condividono il nome e la banda di frequenza (2.4 GHz ISM).

**Bluetooth Classic (BR/EDR):**

- Progettato per streaming continuo di dati (audio, file transfer)
- Data rate fino a 3 Mbps (EDR)
- Consuma molta più energia
- Utilizzato per: cuffie audio, trasferimento file, tethering, tastiere legacy
- Richiede pairing formale con PIN/passkey
- Connection-oriented: deve stabilire una connessione prima di trasmettere dati

**Bluetooth Low Energy (BLE):**

- Progettato per trasmissioni brevi e intermittenti
- Data rate teorico fino a 2 Mbps (BLE 5.0), pratico 200-800 kbps
- Consumo energetico drasticamente inferiore
- Utilizzato per: IoT, beacon, tracker, sensori, wearable, serrature smart
- Supporta sia modalità connection-oriented che connectionless (advertising)
- Può trasmettere dati senza connessione formale (advertising packets)

Questa distinzione è critica: il Flipper NON può interagire con dispositivi Bluetooth Classic (cuffie audio standard, trasferimento file OBEX, tethering). Può solo operare nello spazio BLE.

### Lo Stack BLE 5.0

Il BLE è organizzato in layer ben definiti. Comprendere lo stack è essenziale per capire cosa il Flipper può e non può fare.

#### Physical Layer (PHY)

Il livello fisico opera nella banda ISM 2.4 GHz (2400-2483.5 MHz), suddivisa in 40 canali da 2 MHz:

- **Canali 37, 38, 39** - Canali di advertising (2402, 2426, 2480 MHz)
- **Canali 0-36** - Canali dati per connessioni attive

BLE 5.0 supporta tre modalità PHY:

| PHY | Data Rate | Range | Uso |
|---|---|---|---|
| **LE 1M** | 1 Mbps | Standard (~30m) | Default, compatibilità massima |
| **LE 2M** | 2 Mbps | Ridotto (~15m) | Throughput alto, minor range |
| **LE Coded** | 125/500 kbps | Esteso (~100m+) | Long range, IoT outdoor |

Il Flipper Zero usa principalmente LE 1M. Il frequency hopping avviene su tutti i 40 canali con un algoritmo pseudo-random per mitigare interferenze e migliorare la coesistenza con altri dispositivi a 2.4 GHz (WiFi, microonde, ZigBee).

#### Link Layer

Il Link Layer gestisce gli stati del dispositivo BLE:

- **Standby** - Radio spenta, nessuna attività
- **Advertising** - Trasmette advertising packets sui canali 37/38/39
- **Scanning** - Ascolta advertising packets sui canali 37/38/39
- **Initiating** - Invia connection request dopo aver ricevuto un advertising packet
- **Connected** - Connessione bidirezionale attiva su canali dati

La transizione tra stati è il cuore di come il BLE funziona:

```
Standby --> Advertising --> Connected
   |            |
   +--> Scanning --> Initiating --> Connected
```

Ogni advertising event consiste nella trasmissione dello stesso pacchetto sui tre canali advertising (37, 38, 39) in sequenza rapida. L'intervallo tra advertising event è configurabile (20ms - 10.24s). Intervalli più corti = dispositivo trovabile più rapidamente, ma maggior consumo energetico.

#### L2CAP (Logical Link Control and Adaptation Protocol)

L2CAP gestisce il multiplexing dei canali logici sulla connessione fisica:

- Frammentazione e riassemblaggio dei pacchetti
- Gestione del **MTU (Maximum Transmission Unit)** - default 23 byte, negoziabile fino a 512+ byte
- Flow control per BLE 5.0

Il MTU è un parametro importante nella pratica: un MTU di 23 byte significa che ogni pacchetto ATT trasporta al massimo 20 byte di payload (3 byte header ATT). Con MTU negoziato a 247 byte, il throughput reale aumenta significativamente.

#### ATT (Attribute Protocol)

ATT definisce il protocollo client-server per accedere ai dati:

- **Server** - Espone attributi (il dispositivo BLE periferico)
- **Client** - Legge/scrive attributi (lo smartphone, il Flipper in modalità scanner)

Ogni attributo ha:

- **Handle** - Identificatore numerico a 16 bit (0x0001 - 0xFFFF)
- **Type** - UUID che definisce il tipo di attributo
- **Value** - I dati effettivi
- **Permissions** - Read, Write, Notify, Indicate, con o senza autenticazione/encryption

Le operazioni ATT principali:

| Operazione | Direzione | Descrizione |
|---|---|---|
| Read Request | Client -> Server | Leggi il valore di un attributo |
| Write Request | Client -> Server | Scrivi un valore e attendi conferma |
| Write Command | Client -> Server | Scrivi senza conferma (fire-and-forget) |
| Notification | Server -> Client | Il server invia un aggiornamento (no conferma) |
| Indication | Server -> Client | Il server invia un aggiornamento (con conferma) |

#### GATT (Generic Attribute Profile)

GATT è il framework costruito sopra ATT che organizza i dati in una struttura gerarchica:

```
GATT Server
  |
  +-- Service (UUID: 0x180F - Battery Service)
  |     |
  |     +-- Characteristic (UUID: 0x2A19 - Battery Level)
  |           |
  |           +-- Value: 85 (percentuale)
  |           +-- Descriptor (CCCD: 0x2902 - Client Config)
  |
  +-- Service (UUID: 0x1812 - HID Service)
        |
        +-- Characteristic (Report Map)
        +-- Characteristic (Report)
        +-- Characteristic (Protocol Mode)
```

I **Service** raggruppano funzionalità logiche. I servizi standard hanno UUID a 16 bit assegnati dal Bluetooth SIG:

| UUID | Servizio | Descrizione |
|---|---|---|
| 0x1800 | Generic Access | Nome dispositivo, aspetto |
| 0x1801 | Generic Attribute | Service Changed |
| 0x180A | Device Information | Manufacturer, model, firmware |
| 0x180F | Battery Service | Livello batteria |
| 0x1812 | Human Interface Device | HID (tastiera, mouse) |
| 0xFE2C | Google Fast Pair | Pairing veloce Google |

I servizi custom usano UUID a 128 bit (es: `6E400001-B5A3-F393-E0A9-E50E24DCCA9E` per il Nordic UART Service usato dal Flipper).

Le **Characteristic** contengono i valori effettivi e le loro proprietà. I **Descriptor** forniscono metadati aggiuntivi sulla characteristic (il più importante è il CCCD - Client Characteristic Configuration Descriptor, usato per abilitare notification/indication).

#### GAP (Generic Access Profile)

GAP definisce i ruoli e le procedure per discovery e connessione:

**Ruoli GAP:**

- **Broadcaster** - Trasmette advertisement, non accetta connessioni
- **Observer** - Riceve advertisement, non si connette
- **Peripheral** - Advertise e accetta connessioni (il Flipper in modalità HID)
- **Central** - Scansiona e inizia connessioni (il Flipper in modalità scanner, lo smartphone)

**Procedure GAP:**

- **Discovery** - Trovare dispositivi nelle vicinanze tramite scanning
- **Connection Establishment** - Creare una connessione BLE
- **Bonding** - Salvare le chiavi di sicurezza per riconnessioni future
- **Name Discovery** - Leggere il nome del dispositivo remoto

### Advertising Packets - Il Cuore del BLE

Gli advertising packets sono il meccanismo fondamentale del BLE e sono alla base di tutto cio' che il Flipper fa con il Bluetooth. Ogni advertising PDU (Protocol Data Unit) ha questa struttura:

```
+----------+----------+------------------+
| Preamble | Access   | PDU              |
| (1 byte) | Address  | (2-39 bytes)     |
|          | (4 bytes)|                  |
+----------+----------+------------------+

PDU:
+--------+--------+----------------------------+
| Header | Length | Payload                    |
| (2 B)  | (1 B)  | (0-31 bytes data + addr)  |
+--------+--------+----------------------------+
```

**Tipi di advertising PDU:**

| Tipo | Nome | Descrizione |
|---|---|---|
| 0x00 | ADV_IND | Connectable, undirected - il più comune |
| 0x01 | ADV_DIRECT_IND | Connectable, directed - per un target specifico |
| 0x02 | ADV_NONCONN_IND | Non-connectable, undirected - solo broadcast |
| 0x03 | SCAN_REQ | Richiesta di scan response |
| 0x04 | SCAN_RSP | Risposta a scan request - dati aggiuntivi |
| 0x06 | ADV_SCAN_IND | Scannable, non-connectable |

Il payload dell'advertising contiene **AD Structures** (Advertising Data Structures), ognuna con formato:

```
+--------+--------+-------------------+
| Length | Type   | Data              |
| (1 B)  | (1 B)  | (Length-1 bytes) |
+--------+--------+-------------------+
```

Tipi AD comuni:

| Type | Nome | Uso |
|---|---|---|
| 0x01 | Flags | LE General Discoverable, BR/EDR Not Supported |
| 0x02 | 16-bit UUID List (incomplete) | Servizi offerti |
| 0x06 | 128-bit UUID List (incomplete) | Servizi custom |
| 0x08 | Shortened Local Name | Nome dispositivo |
| 0x09 | Complete Local Name | Nome dispositivo completo |
| 0x0A | TX Power Level | Potenza di trasmissione |
| 0xFF | Manufacturer Specific Data | Dati proprietari del vendor |

Il tipo **0xFF (Manufacturer Specific Data)** è il più rilevante per il BLE Spam: contiene un Company ID a 16 bit (assegnato dal Bluetooth SIG) seguito da dati proprietari. Apple (0x004C), Samsung (0x0075), Google (0x00E0), Microsoft (0x0006) usano questo campo per implementare i loro sistemi di proximity pairing.

> **Nota personale:** Capire la struttura degli advertising packets è la chiave per comprendere tutto il BLE hacking con il Flipper. Il 90% di cio' che il Flipper fa in ambito Bluetooth si riduce a crafting e trasmissione di advertising packets con payload specifici. Se capisci questo meccanismo, capisci il BLE Spam, il Fast Pair, il Swift Pair e tutto il resto.

---

