## 1. Fondamenti -- ESP32 come coprocessore

### 1.1 Perchè un ESP32

Il Flipper Zero è un dispositivo potente per l'interazione con protocolli radio a bassa frequenza, Sub-GHz, NFC, RFID e infrarosso, ma nativamente non dispone di un modulo WiFi nè di un modulo Bluetooth classico ad alte prestazioni. L'ESP32 colma questa lacuna fungendo da coprocessore esterno collegato via UART attraverso il bus GPIO.

In pratica, il Flipper Zero diventa il "cervello" che invia comandi e visualizza risultati, mentre l'ESP32 esegue le operazioni pesanti: scansione WiFi, injection di pacchetti, creazione di access point, streaming video, comunicazione BLE e molto altro.

### 1.2 Architettura del collegamento

Il collegamento avviene via UART (Universal Asynchronous Receiver-Transmitter) attraverso i pin GPIO del Flipper Zero. La comunicazione è seriale, tipicamente a 115200 baud (alcuni firmware supportano fino a 921600 baud per operazioni di flash).

Schema di collegamento standard:

```
Flipper Zero GPIO          ESP32
─────────────────          ─────
Pin 13 (TX)       ───►     RX (GPIO3)
Pin 14 (RX)       ◄───     TX (GPIO1)
Pin 15 (3.3V)     ───►     3V3
Pin 18 (GND)      ───►     GND
```

Attenzione: i pin TX e RX vanno incrociati. Il TX del Flipper va al RX dell'ESP32 e viceversa. Questo è un errore comune che causa il mancato riconoscimento del modulo.

Per il flash del firmware, alcuni moduli richiedono anche il collegamento del pin GPIO0 (boot mode) e del pin EN (enable/reset):

```
Flipper Zero GPIO          ESP32 (solo per flash)
─────────────────          ─────
Pin 2 (A7)        ───►     GPIO0 (BOOT)
Pin 16 (C0)       ───►     EN (RESET)
```

### 1.3 Alimentazione

L'ESP32 richiede 3.3V e può assorbire fino a 500mA durante le operazioni WiFi intensive (TX a piena potenza). Il Flipper Zero fornisce 3.3V dal pin 15, ma la corrente disponibile è limitata.

Raccomandazioni:

- Per operazioni leggere (scan passivo, BLE): l'alimentazione dal Flipper è sufficiente.
- Per operazioni pesanti (deauth, beacon spam, AP mode, streaming video): utilizzare alimentazione esterna USB o batteria dedicata. L'ESP32 sotto carico può causare riavvii del Flipper o comportamento instabile.
- Per l'ESP32-CAM: alimentazione esterna quasi obbligatoria, il modulo camera + LED IR assorbono oltre 300mA.

### 1.4 Modelli ESP32 compatibili

**ESP32-WROOM-32**

Il modulo classico e più diffuso. Dual-core Xtensa LX6 a 240MHz, WiFi 802.11 b/g/n, Bluetooth 4.2 + BLE. È il modulo di riferimento per Marauder e la maggior parte dei tool WiFi offensivi. Dispone di 4MB di flash (alcuni modelli 16MB), 520KB SRAM. Supporta antenna PCB integrata o connettore U.FL per antenna esterna.

Vantaggi: massima compatibilità, ampia community, firmware testati.
Svantaggi: form factor non compattissimo, antenna PCB mediocre per wardriving a lunga distanza.

**ESP32-S2**

Single-core Xtensa LX7 a 240MHz, solo WiFi (niente Bluetooth). Ha un controller USB nativo che permette il flash diretto senza convertitore UART esterno. Supporta WiFi HT40 per throughput maggiore.

Vantaggi: USB nativo, consumo inferiore, costo ridotto.
Svantaggi: niente BLE, single-core limita il multitasking.

**ESP32-S3**

Dual-core Xtensa LX7 a 240MHz, WiFi + Bluetooth 5.0 + BLE. Rappresenta l'evoluzione del WROOM con supporto BLE 5 e prestazioni superiori. USB nativo. Supporta AI acceleration con istruzioni SIMD.

Vantaggi: BLE 5.0, prestazioni top, USB nativo.
Svantaggi: non tutti i firmware sono ancora ottimizzati per S3, costo maggiore.

**ESP32-CAM (AI-Thinker)**

Basato su ESP32-S con modulo camera OV2640 (2MP) o OV3660 (3MP). Include slot microSD, LED flash ad alta potenza e opzionale LED IR per visione notturna. È il modulo di riferimento per tutti i tool camera del Flipper.

Vantaggi: camera integrata, LED flash/IR, slot SD.
Svantaggi: niente USB nativo (serve convertitore FTDI/CP2102 per il flash), pin GPIO limitati perchè molti sono usati dalla camera, alimentazione critica.

### 1.5 Schede di sviluppo e devboard

La Flipper Zero WiFi Devboard ufficiale è basata su ESP32-S2 ed è plug-and-play: si collega direttamente al bus GPIO del Flipper senza cablaggio. È la soluzione più comoda ma non supporta BLE.

Alternative di terze parti:

- Devboard basate su ESP32-WROOM con connettore GPIO diretto
- Adattatori custom stampati in 3D con moduli ESP32 generici
- Breadboard con cavi dupont per setup sperimentali

> Nota personale: per il pentest serio uso la devboard ufficiale ESP32-S2 per WiFi puro (Marauder, Evil Portal) e un ESP32-WROOM separato su breadboard per quando serve il BLE. L'ESP32-CAM la tengo per ricognizione visiva e la alimento sempre con un powerbank dedicato -- non fidarti mai dell'alimentazione dal Flipper per la camera, si riavvia nel momento peggiore.

---

## 2. Setup e Flash del Firmware

### 2.1 Preparazione dell'ambiente

Prima di utilizzare qualsiasi tool ESP32 sul Flipper, il modulo deve essere flashato con il firmware corretto. Ogni tool richiede un firmware specifico sull'ESP32 -- non esiste un firmware universale che abilita tutti i tool contemporaneamente.

Firmware principali:

| Firmware | Tool supportati | Modulo target |
|----------|----------------|---------------|
| Marauder | Marauder, WiFi Marauder | ESP32-WROOM, ESP32-S2 |
| Evil Portal | Evil Portal | ESP32-WROOM, ESP32-S2 |
| Ghost ESP | Ghost ESP | ESP32-WROOM |
| Camera firmware | Camera, Camera Suite, Motion Detection, Nanny Cam, QR Code | ESP32-CAM |
| BlackMagic | Debugger UART | ESP32-S2 |
| Wardriver | Wardriver | ESP32-WROOM + GPS |

### 2.2 Flash tramite Web Flasher (metodo consigliato)

Il metodo più semplice è il web flasher, che funziona direttamente dal browser (Chrome/Edge con supporto Web Serial API).

Procedura step-by-step:

1. Collegare l'ESP32 al PC via USB (o via convertitore UART-USB se il modulo non ha USB nativo).
2. Aprire il web flasher appropriato:
   - Marauder: `https://flasher.marauder.dev`
   - Evil Portal: `https://flasher.evilportal.dev`
   - Camera firmware: dipende dalla versione, consultare il repository GitHub del tool
3. Selezionare il modulo ESP32 corretto dal menu a tendina.
4. Cliccare "Connect" e selezionare la porta seriale del modulo.
5. Selezionare il firmware desiderato.
6. Cliccare "Flash" e attendere il completamento.
7. Al termine, il modulo si riavvia automaticamente con il nuovo firmware.

Nota: se il modulo non entra in boot mode automaticamente, tenere premuto il pulsante BOOT (GPIO0 a GND) durante il collegamento o prima di cliccare Flash.

### 2.3 Flash tramite esptool (metodo avanzato)

Per chi preferisce la riga di comando o deve flashare firmware custom:

```bash
# Installare esptool
pip install esptool

# Identificare il chip
esptool.py --port /dev/ttyUSB0 chip_id

# Cancellare la flash (consigliato prima del primo flash)
esptool.py --port /dev/ttyUSB0 erase_flash

# Flash del firmware (esempio Marauder)
esptool.py --port /dev/ttyUSB0 \
  --baud 921600 \
  --before default_reset \
  --after hard_reset \
  write_flash -z \
  --flash_mode dio \
  --flash_freq 80m \
  --flash_size 4MB \
  0x1000 bootloader.bin \
  0x8000 partitions.bin \
  0x10000 marauder.bin
```

Gli offset (0x1000, 0x8000, 0x10000) variano in base al firmware. Consultare sempre la documentazione specifica.

Per ESP32-S2 e S3, gli offset cambiano:

```bash
esptool.py --port /dev/ttyUSB0 \
  --chip esp32s2 \
  --baud 921600 \
  write_flash -z \
  0x1000 bootloader.bin \
  0x8000 partitions.bin \
  0x10000 firmware.bin
```

### 2.4 Flash tramite ESP Flasher del Flipper

Il Flipper stesso può flashare l'ESP32 collegato via GPIO, usando il tool ESP Flasher (descritto nella sezione Tool Vari). Questo metodo è comodo ma più lento e richiede che i file .bin siano già sulla microSD del Flipper.

### 2.5 Troubleshooting del flash

**Il modulo non viene riconosciuto**
- Verificare driver USB: CP2102, CH340 o FTDI a seconda del convertitore.
- Su Linux: `ls /dev/ttyUSB*` o `ls /dev/ttyACM*` per verificare la porta.
- Su Windows: verificare in Gestione Dispositivi sotto "Porte COM".
- Provare un cavo USB diverso (molti cavi economici sono solo di ricarica, senza dati).

**Errore "Failed to connect to ESP32"**
- Il modulo non è in boot mode: tenere premuto BOOT, premere e rilasciare EN/RESET, poi rilasciare BOOT.
- Per ESP32-CAM senza pulsante BOOT: collegare GPIO0 a GND prima di alimentare.
- Provare baud rate inferiore (115200 invece di 921600).

**Flash completato ma il modulo non risponde**
- Verificare il collegamento TX/RX (ricordare: vanno incrociati).
- Verificare che il firmware sia compatibile con il modulo specifico.
- Provare un erase_flash completo prima di ri-flashare.

**Il Flipper non riconosce l'ESP32 dopo il flash**
- Riavviare sia il Flipper che l'ESP32.
- Verificare che il firmware dell'ESP32 sia compatibile con la versione del firmware Flipper.
- Controllare i pin di collegamento GPIO.

> Nota personale: il problema più frequente in assoluto è il cavo USB. Ho perso ore a debuggare problemi che si risolvevano semplicemente cambiando cavo. Tieni sempre un cavo USB dati di qualità nel kit. Secondo problema più comune: offset sbagliati nel flash manuale -- controlla sempre la documentazione del firmware specifico.

---

