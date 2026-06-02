# GPIO - Guida Operativa Avanzata

Il GPIO (General Purpose Input/Output) del Flipper Zero trasforma il dispositivo in una piattaforma di hardware hacking completa. Tramite i pin GPIO, il Flipper comunica con moduli esterni (ESP32, ESP8266, NRF24), sensori, bus di debug (SWD/JTAG/UART/SPI/I2C) e periferiche custom.

Questa guida copre l'architettura hardware dei pin, i protocolli di comunicazione, le applicazioni di ogni sotto-modulo e gli scenari operativi di penetration testing hardware.

---

## Indice

1. [Architettura Hardware GPIO](#architettura-hardware-gpio)
2. [Pinout Completo](#pinout-completo)
3. [Protocolli di Comunicazione](#protocolli-di-comunicazione)
4. [Sotto-Moduli - Panoramica Operativa](#sotto-moduli--panoramica-operativa)
5. [Scenari di Hardware Hacking](#scenari-di-hardware-hacking)
6. [Sicurezza Operativa](#sicurezza-operativa)
7. [Esperienza Personale](#esperienza-personale)

---

## Architettura Hardware GPIO

### Specifiche Tecniche

Il Flipper Zero espone **18 pin GPIO** su un header a pettine sulla parte superiore del dispositivo:

- **Tensione logica:** 3.3V (LVTTL)
- **Tolleranza 5V:** alcuni pin sono 5V tolerant in input (verificare per pin specifico)
- **Corrente massima per pin:** ~20 mA (source/sink)
- **Corrente totale GPIO:** ~120 mA massimo
- **Alimentazione esterna:** pin 5V fornisce 5V direttamente dalla USB/batteria (max ~400 mA)
- **Alimentazione 3.3V:** pin 3V3 fornisce 3.3V regolati (max ~200 mA)

### Pin Disponibili

```
Pin  | Nome    | Funzione Primaria      | Funzione Alternativa
-----|---------|------------------------|---------------------
1    | 5V      | Alimentazione 5V       | Output diretto USB/batteria
2    | PA7     | GPIO / SPI MOSI        | ADC_IN7
3    | PA6     | GPIO / SPI MISO        | ADC_IN6
4    | PA4     | GPIO / SPI CS          | ADC_IN4, DAC1
5    | PB3     | GPIO / SPI SCK         |
6    | PB2     | GPIO / GDO0            |
7    | PC3     | GPIO / GDO2            | ADC_IN4
8    | GND     | Ground                 |
9    | 3V3     | Alimentazione 3.3V     | Regolatore interno
10   | PA14    | GPIO / SWCLK           | Debug SWD
11   | PA13    | GPIO / SWDIO           | Debug SWD
12   | PB6     | GPIO / UART TX1        | I2C SCL
13   | PB7     | GPIO / UART RX1        | I2C SDA
14   | PC1     | GPIO                   | ADC_IN1 / Interrupt
15   | PC0     | GPIO                   | ADC_IN0
16   | PB14    | GPIO / UART TX (iButton)| 1-Wire
17   | PB15    | GPIO / UART RX (iButton)|
18   | GND     | Ground                 |
```

**ATTENZIONE HARDWARE:** Non collegare mai tensioni superiori a 3.3V ai pin non-5V-tolerant. Non cortocircuitare 5V a GND. Non superare 20mA per pin. Danni al GPIO sono irreversibili.

> **Nota personale:** Ho bruciato un pin GPIO collegando direttamente un relè 5V senza level shifter. Il pin PA7 ha smesso di funzionare. Da allora uso SEMPRE un level shifter bidirezionale per qualsiasi interfaccia 5V e un multimetro per verificare le tensioni prima di collegare. Il costo di un level shifter è 1 euro, il costo di un Flipper nuovo è 170 euro.

---

## Protocolli di Comunicazione

### UART (Universal Asynchronous Receiver-Transmitter)

Il protocollo seriale più semplice e fondamentale per hardware hacking:

- **Pin:** PB6 (TX) + PB7 (RX) + GND
- **Baud rate supportati:** 110 - 115200+ (tipicamente 9600 o 115200)
- **Formato:** 8N1 (8 data bit, no parity, 1 stop bit) standard
- **Uso:** console di debug, comunicazione ESP32/ESP8266, shell su dispositivi embedded, bootloader access

**Perchè è critico per il pentest:** La UART è la prima porta che un hardware hacker cerca su un dispositivo target. Moltissimi router, IP camera, IoT device hanno pad UART esposti sul PCB che danno accesso diretto alla console di boot (U-Boot) o alla shell root.

### SPI (Serial Peripheral Interface)

Protocollo sincrono ad alta velocità per memorie flash e periferiche:

- **Pin:** PA7 (MOSI) + PA6 (MISO) + PB3 (SCK) + PA4 (CS) + GND
- **Clock:** fino a ~8 MHz sul Flipper
- **Uso:** lettura/scrittura memorie flash SPI (W25Qxx, AT25xxx), dump firmware, programmazione

**Perchè è critico:** Le memorie SPI contengono il firmware dei dispositivi embedded. Dump della flash = accesso al firmware = reverse engineering = ricerca vulnerabilità.

### I2C (Inter-Integrated Circuit)

Bus multi-dispositivo per sensori e periferiche lente:

- **Pin:** PB6 (SCL) + PB7 (SDA) + GND (+ pull-up resistor 4.7kOhm)
- **Clock:** 100 kHz (standard) / 400 kHz (fast mode)
- **Indirizzamento:** 7 bit (128 dispositivi possibili sul bus)
- **Uso:** sensori (temperatura, umidità, pressione, gas), EEPROM, display OLED, RTC

### SWD (Serial Wire Debug)

Interfaccia di debug ARM per microcontrollori Cortex-M:

- **Pin:** PA14 (SWCLK) + PA13 (SWDIO) + GND (+ reset opzionale)
- **Uso:** debug live, flash firmware, halt/resume CPU, lettura memoria
- **Target:** STM32, nRF52, RP2040, GD32, e qualsiasi ARM Cortex-M

**Perchè è critico:** SWD permette il dump completo della flash di un microcontrollore - firmware, chiavi crittografiche, configurazioni. È l'equivalente di avere accesso root al chip.

> **Nota personale:** SWD è il mio protocollo preferito per hardware hacking. Ho estratto firmware da IP camera, serrature smart, dispositivi IoT e persino da un sistema di allarme collegandomi ai pad SWD sul PCB. I produttori spesso lasciano i pad esposti (a volte perfino con header saldato!) e non proteggono la flash con readout protection. Un pentest hardware senza SWD probe è incompleto.

---

## Sotto-Moduli - Panoramica Operativa

### ESP32 (`GPIO/ESP32/`)

L'ESP32 trasforma il Flipper in un tool WiFi/BLE offensivo. Collegato via UART, permette:
- **WiFi Marauder:** deauth, beacon spam, sniffing, evil portal
- **Evil Portal:** captive portal con pagine custom
- **Camera (ESP32-CAM):** sorveglianza visiva remota
- **Wardriving:** mappatura reti WiFi con GPS
- **Scanner WiFi/BLE:** ricognizione wireless

[Dettagli completi → ESP32/README.md](ESP32/README.md)

### ESP8266 (`GPIO/ESP8266/`)

Modulo WiFi economico per attacchi deauthentication e automazione:
- **Deauther:** disconnessione client WiFi (attacco management frame)
- **WiFi Scanner:** ricognizione reti 2.4 GHz
- **IFTTT Button:** automazione IoT

[Dettagli completi → ESP8266/README.md](ESP8266/README.md)

### NRF24 (`GPIO/NRF24/`)

Transceiver 2.4 GHz per attacchi a periferiche wireless:
- **MouseJacker:** hijacking mouse/tastiere wireless non criptati
- **Sniffer:** cattura pacchetti 2.4 GHz
- **Jammer:** interferenza su canali specifici

[Dettagli completi → NRF24/README.md](NRF24/README.md)

### Debug (`GPIO/Debug/`)

Strumenti per hardware hacking diretto:
- **SWD Probe / DAP Link:** debug e flash microcontrollori ARM
- **AVR Flasher:** programmazione ATmega/ATtiny
- **I2C Tools:** scansione e debug bus I2C
- **SPI Mem Manager:** dump e flash memorie SPI
- **Ethernet Troubleshooter:** diagnostica rete

[Dettagli completi → Debug/README.md](Debug/README.md)

### Sensors (`GPIO/Sensors/`)

Suite di sensori ambientali per misurazioni e monitoraggio:
- Temperatura, umidità, pressione (BME280, DHT22)
- Gas e qualità aria (MQ-series, SCD30)
- Distanza (HC-SR04, VL53L0X)
- Radiazioni (Geiger counter)
- UV, luce, particolato

[Dettagli completi → Sensors/README.md](Sensors/README.md)

### Malveke (`GPIO/Malveke/`)

Addon multifunzione con camera, printer e strumenti di test.

[Dettagli completi → Malveke/README.md](Malveke/README.md)

### Flipboard (`GPIO/Flipboard/`)

Board di prototipazione con LED e pulsanti per I/O rapido.

[Dettagli completi → Flipboard/README.md](Flipboard/README.md)

### Games (`GPIO/Games/`)

Mini-giochi che dimostrano l'uso di UART e sensori (Pong via UART, Pong via ToF).

[Dettagli completi → Games/README.md](Games/README.md)

### VGM (`GPIO/VGM/`)

Video Game Module - addon per gaming con sensori di movimento.

[Dettagli completi → VGM/README.md](VGM/README.md)

### Altre Componenti (`GPIO/Altre componenti/`)

GPS, RGB LED, air mouse, analog output, Sentry Safe, ColecoVision e altri tool standalone.

[Dettagli completi → Altre componenti/README.md](Altre%20componenti/README.md)

---

## Scenari di Hardware Hacking

### Scenario 1 - Dump Firmware di un Router via SPI

**Obiettivo:** estrarre il firmware di un router per analisi di vulnerabilità

1. Apri il router e identifica la flash SPI sul PCB (chip 8-pin, tipicamente W25Qxx)
2. Identifica i pin: CS, MOSI, MISO, SCK, VCC, GND (datasheet del chip)
3. Collega il Flipper ai pin SPI della flash (con il router SPENTO)
4. Apri SPI Mem Manager → identifica il chip (JEDEC ID)
5. Dump completo della flash → file .bin
6. Analizza offline con binwalk, firmware-mod-kit, Ghidra

**Post-analisi:**
- Estrai il filesystem (squashfs, jffs2, ubifs)
- Cerca credenziali hardcoded, chiavi private, configurazioni
- Identifica servizi vulnerabili
- Cerca backdoor o funzionalità nascoste

### Scenario 2 - Debug via SWD di una Serratura Smart

**Obiettivo:** estrarre il firmware di una serratura IoT BLE

1. Apri la serratura e identifica il microcontrollore (tipicamente nRF52 o STM32)
2. Localizza i pad SWD (SWCLK, SWDIO, GND, Reset)
3. Collega il Flipper → SWD Probe
4. Identifica il target (IDCODE)
5. Verifica se la readout protection (RDP) è attiva
6. Se RDP = 0 (non protetto): dump completo della flash
7. Analizza il firmware con Ghidra: cerca chiavi BLE, algoritmo di autenticazione, vulnerabilità

### Scenario 3 - Accesso UART su IP Camera

**Obiettivo:** ottenere shell root su una IP camera

1. Apri la camera e localizza i pad UART (TX, RX, GND)
2. Identifica il baud rate (prova 115200 prima, poi 9600)
3. Collega il Flipper: TX→RX, RX→TX, GND→GND
4. Apri UART Terminal sul Flipper
5. Riavvia la camera → osserva l'output di boot (U-Boot)
6. Interrompi il boot premendo un tasto durante il countdown U-Boot
7. Da U-Boot: modifica i parametri di boot per ottenere shell root
8. Oppure: accedi direttamente alla shell Linux se non c'è password

### Scenario 4 - MouseJacker su Tastiera Wireless

**Obiettivo:** dimostrare l'hijacking di una tastiera wireless non criptata

1. Collega modulo NRF24L01+ al GPIO del Flipper
2. Apri MouseJacker → Scanner
3. Identifica il dongle USB della tastiera target (indirizzo pipe)
4. Avvia l'hijacking → il Flipper si sostituisce alla tastiera
5. Invia keystroke arbitrari al PC target
6. Demo: digita "Questa tastiera non è sicura" sul PC della vittima

---

## Sicurezza Operativa

### Protezione Hardware del Flipper

- **Non collegare mai 5V ai pin 3.3V** - brucia il GPIO
- **Usa sempre resistori di pull-up/pull-down** - segnali fluttuanti causano comportamento imprevedibile
- **Level shifter per 5V** - obbligatorio per interfacce a 5V
- **Corrente massima:** rispetta i limiti (20mA/pin, 120mA totale)
- **Alimentazione esterna:** per moduli ad alta corrente (ESP32 in TX), usa alimentazione esterna

### Precauzioni nel Pentest Hardware

- **Fotografia del PCB** prima di collegare qualsiasi cosa
- **Identifica le tensioni** con multimetro prima di collegare il Flipper
- **Non dissaldare componenti** senza autorizzazione scritta
- **Documenta ogni collegamento** fatto (foto + schema)
- **Backup prima di scrivere:** dump sempre la flash PRIMA di modificarla

---

## Esperienza Personale

> **Nota personale - Il kit GPIO completo:** Nel mio zaino da pentest hardware tengo sempre: modulo ESP32 con Marauder flashato, modulo NRF24L01+ con antenna, cavi jumper Dupont (M-M, M-F, F-F), level shifter bidirezionale, clip SOIC-8 per flash SPI, multimetro tascabile, lente d'ingrandimento. Questo kit copre il 90% degli scenari di hardware hacking sul campo.

> **Nota personale - UART ovunque:** La UART è la vulnerabilità hardware più comune che trovo. Su circa 20 dispositivi IoT testati nell'ultimo anno, 15 avevano pad UART esposti e 12 di questi davano accesso a una shell root senza password. Router, IP camera, smart speaker, NAS - quasi tutto ha una UART accessibile.

> **Nota personale - SPI dump come standard:** Il dump SPI è diventato una procedura standard nei miei hardware pentest. Con la clip SOIC-8 non serve neanche dissaldare il chip - basta agganciare la clip e dumpare. Il firmware estratto rivela quasi sempre credenziali hardcoded, chiavi private o configurazioni di debug attive.

> **Nota personale - NRF24 e MouseJacker:** L'attacco MouseJacker è il più scenografico durante le demo. Colleghi il NRF24 al Flipper, scansioni, trovi la tastiera wireless del CEO e inizi a digitare messaggi sul suo schermo. L'effetto sulla consapevolezza della sicurezza è immediato. Consiglio: usa questo attacco nelle sessioni di awareness, non solo nei report tecnici.
