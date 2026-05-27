## BLE Spam - Deep Dive

Il BLE Spam è la funzionalità BLE più nota del Flipper e merita un'analisi approfondita del funzionamento interno per ogni vendor.

### Apple BLE Spam

Apple utilizza un protocollo proprietario basato su Manufacturer Specific Data (Company ID: 0x004C) per le notifiche di prossimità. Questo sistema è usato per:

- AirPods/AirPods Pro/AirPods Max (popup "Not Your AirPods")
- Apple TV setup
- AirTag detection
- Handoff/Continuity
- HomeKit
- "Hey Siri" routing

**Struttura del pacchetto Apple proximity:**

```
Advertising Data:
  AD Structure 1: Flags (0x01)
    Length: 0x02
    Type:   0x01
    Flags:  0x06 (LE General Discoverable + BR/EDR Not Supported)

  AD Structure 2: Manufacturer Specific Data (0xFF)
    Length: variabile (tipicamente 0x17 = 23 bytes)
    Type:   0xFF
    Company ID: 0x004C (Apple, Inc.)
    Proximity Type: 0x0715
    Payload: [device-specific data]
```

**Tipi di device Apple simulabili:**

| Device | Popup Mostrato | Efficacia |
|---|---|---|
| AirPods Pro | "Not Your AirPods Pro" con immagine | Alta - popup molto visibile |
| AirPods 3rd Gen | "Not Your AirPods" con immagine | Alta |
| AirPods Max | "Not Your AirPods Max" con immagine | Alta - immagine grande |
| Beats Fit Pro | "Not Your Beats Fit Pro" | Media |
| Apple TV Setup | Setup assistant popup | Media |
| AppleTV Keyboard | Richiesta tastiera | Media |
| AppleTV New User | Setup nuovo utente | Media |
| Beats Solo 3 | "Not Your Beats Solo 3" | Media |
| PowerBeats Pro | "Not Your Powerbeats Pro" | Media |

**Come Apple gestisce la proximity detection:**

1. Il dispositivo iOS riceve l'advertising packet con Company ID 0x004C
2. Il sistema verifica il tipo di messaggio (proximity pairing = 0x07)
3. Il sottotipo identifica il dispositivo specifico (0x15 per un tipo, 0x01 per un altro)
4. iOS mostra il popup corrispondente con l'immagine del dispositivo
5. Il popup rimane visibile per alcuni secondi, poi scompare

**Contromisure Apple:**

A partire da iOS 17.2, Apple ha introdotto mitigazioni parziali:

- Rate limiting sui popup di proximity (non più popup in rapida successione)
- Opzione per disabilitare le notifiche di proximity in Impostazioni > Bluetooth
- Detection di pattern anomali (troppi dispositivi diversi dallo stesso MAC in poco tempo)

Tuttavia, queste mitigazioni non eliminano completamente il problema. Con MAC address rotation e timing appropriato, il BLE Spam continua a essere efficace anche su iOS recenti, seppur con frequenza ridotta dei popup.

**Disabilitare i popup Apple:**

```
Impostazioni > Bluetooth > Disattivare Bluetooth
oppure
Impostazioni > Notifiche > Suggerimenti di Siri > Disattivare
```

Nota: disabilitare il Bluetooth dal Control Center NON disabilita completamente il BLE scanning. Apple mantiene il BLE attivo per Find My, Handoff e AirDrop. Solo disabilitando completamente dalle Impostazioni si ferma la ricezione.

### Samsung BLE Spam

Samsung utilizza il protocollo **Nearby Device** con Company ID 0x0075 per il pairing rapido dei suoi accessori:

**Dispositivi Samsung simulabili:**

| Device | Popup |
|---|---|
| Galaxy Buds Pro | "Galaxy Buds Pro trovati nelle vicinanze" |
| Galaxy Buds Live | "Galaxy Buds Live trovati" |
| Galaxy Buds 2 | "Galaxy Buds2 trovati" |
| Galaxy Buds 2 Pro | "Galaxy Buds2 Pro trovati" |
| Galaxy Buds FE | "Galaxy Buds FE trovati" |
| Galaxy SmartTag | Popup SmartTag |
| Galaxy Fit | Popup Galaxy Fit |
| Galaxy Watch | Popup Galaxy Watch |
| Galaxy Ring | Popup Galaxy Ring |

**Struttura del pacchetto Samsung:**

```
Advertising Data:
  AD Structure 1: Flags
    0x02 0x01 0x06

  AD Structure 2: Manufacturer Specific Data
    Length: variabile
    Type: 0xFF
    Company ID: 0x0075 (Samsung Electronics)
    Nearby Device Protocol: [device type byte] [model ID] [payload]
```

Il protocollo Samsung Nearby è meno documentato pubblicamente rispetto ad Apple, ma il reverse engineering della community ha identificato i byte chiave per ogni tipo di dispositivo.

**Efficacia su dispositivi Samsung:**

I popup Samsung sono molto efficaci sui telefoni Galaxy con Android e l'app Samsung SmartThings o Samsung Wearable installata. La notifica appare come un popup a schermo intero con l'immagine del dispositivo, molto simile all'esperienza Apple.

Su telefoni Android non-Samsung, il popup Samsung non appare (poichè il protocollo Nearby Samsung è gestito dal framework Samsung proprietario, non da Android stock).

### Google Fast Pair

Google Fast Pair è il protocollo di proximity pairing di Google, supportato da tutti i dispositivi Android con Google Play Services 11.7+. Usa Company ID Google (0x00E0) con un protocollo standardizzato:

**Come funziona Google Fast Pair:**

1. Il dispositivo BLE trasmette un advertising con il servizio UUID **0xFE2C** (Google Fast Pair Service)
2. Il payload contiene un **Model ID** a 24 bit che identifica il dispositivo
3. Google Play Services sul telefono Android riceve l'advertising
4. Il servizio consulta un database cloud di Model ID registrati
5. Se il Model ID corrisponde a un dispositivo noto, mostra il popup con nome e immagine

**Struttura del pacchetto Fast Pair:**

```
Advertising Data:
  AD Structure 1: Flags
    0x02 0x01 0x06

  AD Structure 2: Service Data (0x16)
    Length: 0x06
    Type: 0x16
    Service UUID: 0xFE2C (Google Fast Pair)
    Model ID: [3 bytes - identificativo del dispositivo]

  AD Structure 3 (opzionale): TX Power Level
    0x02 0x0A 0xF4
```

**Model ID notevoli:**

I Model ID sono registrati nel database Google. Alcuni esempi usati dal BLE Spam:

- Google Pixel Buds
- Google Pixel Buds Pro
- JBL dispositivi vari
- Sony WH-1000XM (varie generazioni)
- Bose QuietComfort
- E molti altri dispositivi certificati Fast Pair

**Efficacia:**

Fast Pair è il più universale tra i protocolli spammabili perchè funziona su QUALSIASI dispositivo Android con Google Play Services (non solo Samsung o Pixel). Il popup è una notifica half-sheet che mostra il nome del dispositivo e un pulsante "Connetti".

**Contromisure Google:**

- Android 14+ ha introdotto rate limiting sulle notifiche Fast Pair
- È possibile disabilitare Fast Pair: Impostazioni > Google > Dispositivi e condivisione > Dispositivi > Disattiva "Mostra notifiche"
- In alternativa: disabilitare completamente il Bluetooth

### Windows Swift Pair

Microsoft Swift Pair è il protocollo di proximity pairing per Windows 10/11, introdotto con Windows 10 April 2018 Update. Usa un meccanismo diverso dagli altri vendor.

**Come funziona Swift Pair:**

1. Il dispositivo BLE trasmette advertising con **Manufacturer Specific Data** e Company ID Microsoft (0x0006)
2. Il payload contiene un marcatore Swift Pair specifico
3. Windows BLE scanner rileva il pacchetto e riconosce il marcatore
4. Il sistema mostra un toast notification "Nuovo dispositivo Bluetooth trovato nelle vicinanze"
5. L'utente può cliccare per avviare il pairing

**Struttura del pacchetto Swift Pair:**

```
Advertising Data:
  AD Structure 1: Flags
    0x02 0x01 0x06

  AD Structure 2: Manufacturer Specific Data
    Length: variabile
    Type: 0xFF
    Company ID: 0x0006 (Microsoft)
    Beacon Type: 0x03 (Swift Pair scenario)
    Payload: [device info, RSSI threshold, display name]

  AD Structure 3: Complete Local Name
    Length: variabile
    Type: 0x09
    Name: "Device Name"
```

**Efficacia su Windows:**

I popup Swift Pair appaiono come toast notification nell'angolo in basso a destra di Windows. Sono meno invasivi dei popup Apple (che occupano metà schermo) ma comunque fastidiosi in quantità.

Swift Pair è abilitato di default su Windows 10/11 ma può essere disabilitato:

```
Impostazioni > Bluetooth e dispositivi > Dispositivi
> Mostra notifiche per la connessione tramite Swift Pair: OFF
```

Oppure via Group Policy:

```
Computer Configuration > Administrative Templates > 
Windows Components > Bluetooth > 
Allow Swift Pair Notifications: Disabled
```

### Crafting dei Pacchetti - Analisi Tecnica

Il BLE Spam del Flipper costruisce i pacchetti advertisement manipolando direttamente le API BLE dello stack STM32WB:

**Flusso di esecuzione:**

1. **Inizializzazione** - L'app configura lo stack BLE tramite le HAL API di ST
2. **Generazione MAC** - Genera un random BLE address (tipo 0x01 = Random) per ogni burst
3. **Costruzione payload** - Assembla l'advertising data con gli AD Structures appropriati per il vendor target
4. **Configurazione advertising** - Imposta advertising parameters (interval, type, channel map)
5. **Trasmissione** - Avvia l'advertising
6. **Rotazione** - Dopo un breve intervallo, ferma l'advertising, cambia MAC e payload, e riparte

**Parametri advertising tipici del BLE Spam:**

| Parametro | Valore | Motivazione |
|---|---|---|
| Adv Interval Min | 20 ms | Massima frequenza di trasmissione |
| Adv Interval Max | 40 ms | Range stretto per alta frequenza |
| Adv Type | ADV_NONCONN_IND (0x02) | Non accetta connessioni, solo broadcast |
| Channel Map | 0x07 (tutti e 3) | Trasmette su canali 37, 38, 39 |
| Own Address Type | Random | MAC randomizzato per ogni burst |

La rotazione del MAC address è critica: senza rotazione, il dispositivo target riceverebbe advertising dallo stesso MAC e mostrerebbe un solo popup. Con rotazione, ogni nuovo MAC appare come un nuovo dispositivo, generando popup multipli.

> **Nota personale:** Ho analizzato il comportamento del BLE Spam con un nRF52840 dongle e Wireshark. Il Flipper genera circa 10-20 advertising packets al secondo per vendor, con MAC rotation ogni 2-3 secondi. In modalità "All" (tutti i vendor), alterna tra Apple, Samsung, Google e Windows ogni pochi secondi, creando un flusso continuo di popup su tutti i dispositivi nella stanza. È caotico ma efficace come demo. In un ambiente di 20 persone, almeno il 70% riceverà almeno un popup nei primi 30 secondi.

---

