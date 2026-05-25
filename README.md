[English version](README_EN.md) | [Indice Globale](INDEX.md) | [Glossario](GLOSSARY.md)

# Flipper Zero - Guida Operativa Avanzata

Guida tecnica approfondita all'utilizzo del Flipper Zero in ambito cybersecurity, penetration testing fisico, analisi RF, reverse engineering hardware e ricerca sulla sicurezza.

Questo repository nasce dall'esperienza diretta sul campo con il dispositivo e documenta ogni modulo, protocollo e tecnica a livello operativo - non come overview superficiale, ma come riferimento pratico per chi lavora (o vuole lavorare) nella sicurezza offensiva e difensiva.

> **Nota personale:** Questo progetto raccoglie anni di sperimentazione reale con il Flipper Zero. Ogni sezione include note di esperienza personale, errori commessi, limiti reali riscontrati e workaround scoperti sul campo. Non è una wiki generica - è un quaderno operativo di un pentester.

---

## Disclaimer Etico e Legale

Tutto il contenuto di questo repository è destinato esclusivamente a:

- **Ricerca sulla sicurezza** su dispositivi e sistemi di propria proprietà
- **Penetration testing autorizzato** con contratto o autorizzazione scritta
- **Formazione e studio** in ambito cybersecurity
- **Audit di sicurezza fisica** per organizzazioni che ne fanno richiesta

L'utilizzo di queste tecniche su dispositivi, reti o sistemi altrui senza autorizzazione esplicita è **illegale** ai sensi del Codice Penale Italiano (Art. 615-ter, 617-quater, 617-quinquies) e della normativa europea.

**Il possesso del Flipper Zero è legale in Italia e nella UE.** L'uso improprio delle sue funzionalità no.

---

## Hardware Overview

### Specifiche Tecniche del Flipper Zero

| Componente | Dettaglio |
|---|---|
| **MCU** | STM32WB55RG - ARM Cortex-M4 (64 MHz) + Cortex-M0+ per BLE |
| **Sub-GHz** | CC1101 transceiver - 300-348 MHz, 387-464 MHz, 779-928 MHz |
| **NFC** | ST25R3916 - ISO 14443A/B, ISO 15693, FeliCa, NFC-V |
| **RFID 125 kHz** | Antenna LF custom + circuito analogico integrato |
| **Infrarossi** | LED TX TSAL6200 (940nm) + ricevitore TSOP75338 (38kHz) |
| **Bluetooth** | BLE 5.0 integrato nel STM32WB55 |
| **GPIO** | 18 pin - 3.3V logic, 5V tolerant su alcuni pin, UART/SPI/I2C/SWD |
| **USB** | USB-C 2.0 - CDC, HID, Mass Storage |
| **iButton** | Pad 1-Wire integrato sul dorso |
| **Storage** | microSD fino a 256 GB (FAT32/exFAT) |
| **Batteria** | LiPo 2000 mAh - ~7 giorni standby, ~2-4h uso intensivo RF |
| **Display** | LCD monocromatico 128x64 px |

### Firmware

Questa guida è basata principalmente su firmware custom **RogueMaster** e **Momentum**, che estendono significativamente le funzionalità del firmware ufficiale. Le differenze principali:

- **Firmware Ufficiale:** funzionalità base, nessuna trasmissione Sub-GHz su frequenze ristrette, set limitato di protocolli
- **RogueMaster / Momentum / Unleashed:** sblocco frequenze, protocolli aggiuntivi, app di terze parti, Sub-GHz esteso, rolling code tools

> **Nota personale:** Consiglio RogueMaster o Momentum per chi fa ricerca seria. Il firmware ufficiale è troppo limitato per attività di pentest. Il flash è reversibile e non invalida la garanzia hardware.

---

## Struttura del Repository

```
How to use/
|-- Sub-GHz/            # RF 300-928 MHz: telecomandi, sensori, rolling code, TPMS, pager
|-- NFC/                # 13.56 MHz: MIFARE, DESFire, NTAG, iClass, badge, card trasporti
|-- RFID/               # 125 kHz: EM4100, HID Prox, T5577, badge accesso
|-- iButton/            # 1-Wire: chiavi Dallas, Cyfral, Metakom, citofoni
|-- Infrared/           # IR: telecomandi TV/AC, protocolli NEC/RC5/RC6, reverse engineering
|-- GPIO/               # Hardware esterno: ESP32, ESP8266, NRF24, sensori, debug SWD/JTAG
|   |-- ESP32/          # WiFi/BLE: Marauder, Evil Portal, camera, wardriving
|   |-- ESP8266/        # WiFi: Deauther, scanner, automazione IoT
|   |-- NRF24/          # 2.4 GHz: MouseJacker, sniffing, jamming
|   |-- Debug/          # SWD, JTAG, I2C, SPI, UART - hardware hacking
|   |-- Sensors/        # Sensori ambientali, Geiger, gas, distanza
|   |-- Malveke/        # Addon camera, printer, emulator
|   |-- Flipboard/      # Prototipazione rapida con LED e pulsanti
|   |-- Games/          # Mini-giochi hardware (UART Pong, ToF Pong)
|   |-- VGM/            # Video Game Module
|   |-- Altre componenti/ # GPS, LoRa, radio FM, automotive, sicurezza, utility
|-- USB/                # HID attacks: BadUSB, DuckyScript, exfiltration, U2F
|   |-- Bad USB/        # Payload, script, evasion, PoC
|   |-- Altre componenti/ # Mass Storage, MIDI, U2F, controller, barcode
|-- WiFi-Marauder/      # Setup e utilizzo WiFi Marauder con ESP32
|-- Bluetooth/          # BLE: spam, sniffing, pairing, tracking, sicurezza
|-- RogueMaster/        # Firmware custom: download, confronto, installazione
|
|-- examples/           # File di esempio per ogni modulo (.sub, .nfc, .rfid, .ibtn, .ir)
```

Ogni modulo principale è organizzato in sotto-file tematici:

| # | File | Contenuto |
|---|------|-----------|
| 01 | Fondamenti Tecnici | Come funziona il protocollo a basso livello |
| 02 | Hardware e Limiti | Specifiche chip, antenne, portata reale |
| 03 | Protocolli | Deep dive su ogni protocollo supportato |
| 04 | Guida Operativa | Tool-by-tool step-by-step |
| 05 | Scenari Reali | Scenari di pentest reali dal campo |
| 06 | Attacchi e Difese | Vettori di attacco + contromisure |
| 07 | Aspetti Legali | Normativa italiana e EU |
| 08 | Esperienza Personale | Note dal campo, errori, lezioni apprese |

### Risorse Aggiuntive

| File | Descrizione |
|------|-------------|
| [CHEATSHEET.md](CHEATSHEET.md) | Riferimento rapido stampabile per il campo (decision tree, frequenze, comandi) |
| [LAB-SETUP.md](LAB-SETUP.md) | Guida alla creazione di un laboratorio di test domestico |
| [REPORT-TEMPLATES.md](REPORT-TEMPLATES.md) | Template pronti per documentare finding (Sub-GHz, NFC, RFID, BadUSB, WiFi) |
| [MITRE-ATTACK.md](MITRE-ATTACK.md) | Mapping completo Flipper Zero → MITRE ATT&CK framework |
| [WORKFLOW-DIAGRAMS.md](WORKFLOW-DIAGRAMS.md) | Diagrammi Mermaid: kill chain, NFC pipeline, Sub-GHz flow, BadUSB chain |
| [GLOSSARY.md](GLOSSARY.md) | Glossario tecnico con 80+ termini (OOK, SAK, ATQA, Crypto1, etc.) |
| [INDEX.md](INDEX.md) | Indice globale navigabile di tutti i file del repository |
| [CONTRIBUTING.md](CONTRIBUTING.md) | Guida per contribuire al progetto |
| [CHANGELOG.md](CHANGELOG.md) | Storico delle modifiche al repository |
| [payloads/](payloads/README.md) | Arsenale BadUSB: 25+ payload pronti per Windows, macOS, Linux |
| [scripts/](scripts/) | Script di automazione: setup SD card, validatore file |

---

## Moduli - Panoramica Operativa

### Sub-GHz (300-928 MHz)

Il modulo più versatile per un pentester fisico. Copre telecomandi garage, cancelli, sensori wireless, pager, stazioni meteo, TPMS e qualsiasi dispositivo che comunica in banda ISM. Include analisi rolling code, replay attack, bruteforce e fuzzing RF.

**Scenari reali:** apertura cancelli durante physical pentest, analisi sicurezza domotica, intercettazione pager ospedalieri, studio TPMS veicoli, reverse engineering telecomandi proprietari.

### NFC (13.56 MHz)

Il modulo critico per il pentest di sistemi di controllo accessi. Supporta MIFARE Classic (con attacco crypto1/mfkey32), DESFire, NTAG, iClass/PicoPass e card trasporti. Permette clonazione, emulazione, relay attack e fuzzing.

**Scenari reali:** clonazione badge aziendali, bypass tornelli, analisi card hotel, test sistemi di pagamento contactless, audit access control enterprise.

### RFID 125 kHz

Il modulo per i sistemi di accesso legacy. La maggior parte degli edifici commerciali e residenziali usa ancora tag 125 kHz senza crittografia. Lettura, emulazione e clonazione sono immediate.

**Scenari reali:** clonazione badge condominio, test lettori HID Prox, audit sistemi di accesso industriali, duplicazione su T5577.

### iButton (1-Wire)

Sistemi di accesso basati su contatto fisico, molto diffusi nei citofoni dell'Europa dell'Est e in Italia. Supporta DS1990A, Cyfral e Metakom con lettura, emulazione e fuzzing.

**Scenari reali:** clonazione chiavi citofono, audit sistemi condominiali, test robustezza lettori 1-Wire.

### Infrarossi

Controllo di qualsiasi dispositivo con ricevitore IR. Utile sia per automazione che per scenari di pentest fisico dove display, TV o sistemi di digital signage devono essere controllati.

**Scenari reali:** spegnimento TV/display in ambienti target, controllo AC per social engineering, reverse engineering telecomandi proprietari, automazione fotocamere.

### GPIO - Hardware Hacking

L'interfaccia di espansione che trasforma il Flipper in una piattaforma di hardware hacking completa. Con ESP32 diventa un tool WiFi offensivo, con NRF24 attacca periferiche wireless, con SWD/JTAG estrae firmware da dispositivi embedded.

**Scenari reali:** WiFi deauth e evil portal con ESP32 Marauder, MouseJacker su tastiere/mouse wireless, dump firmware via SWD, sniffing bus I2C/SPI/UART su IoT.

### USB - HID Attacks

BadUSB trasforma il Flipper in una tastiera malevola che esegue payload automatizzati. È l'equivalente di un Rubber Ducky con il vantaggio di essere programmabile sul campo.

**Scenari reali:** drop attack durante physical pentest, exfiltration credenziali WiFi, escalation privilegi, deployment reverse shell, evasione kiosk.

### WiFi (via ESP32 Marauder)

Il Flipper Zero non ha WiFi nativo - tutto passa dall'ESP32. Con il firmware Marauder diventa uno scanner WiFi, deauther, beacon spammer e sniffer di handshake.

**Scenari reali:** ricognizione wireless durante un engagement, deauth per forzare riconnessioni, evil portal per credential harvesting, wardriving.

### Bluetooth (BLE 5.0)

Il modulo BLE integrato permette spam di pacchetti advertisement, analisi dispositivi BLE nelle vicinanze, e integrazione con app companion.

**Scenari reali:** BLE spam per disruption, tracciamento dispositivi, analisi sicurezza wearable, fuzzing servizi BLE.

---

## Metodologia di Utilizzo in un Engagement

In un penetration test fisico, il Flipper Zero si inserisce in diverse fasi:

### 1. Ricognizione (Reconnaissance)

- **Sub-GHz Frequency Analyzer** per identificare dispositivi RF nell'area target
- **Radio Scanner** per mappare le frequenze attive di un edificio
- **WiFi Scanner** (ESP32) per enumerare reti e client
- **NFC/RFID Detector** per localizzare lettori di badge nascosti
- **BLE Scanner** per identificare dispositivi IoT e wearable

### 2. Analisi (Analysis)

- **Sub-GHz Read** per catturare e decodificare segnali di telecomandi e sensori
- **NFC Read** per identificare tipo e sicurezza dei badge
- **RFID Read** per classificare tag 125 kHz
- **IR Decoder** per reverse engineering di telecomandi
- **Spectrum Analyzer** per studiare lo spettro RF dell'ambiente

### 3. Exploitation

- **Sub-GHz Replay/Bruteforce** per testare sistemi di apertura
- **NFC Emulate/Magic Write** per clonare badge
- **RFID Emulate** per accedere con badge clonati
- **BadUSB** per eseguire payload su workstation
- **Evil Portal** (ESP32) per credential harvesting WiFi
- **MouseJacker** (NRF24) per hijacking periferiche wireless

### 4. Post-Exploitation

- **BadUSB** per exfiltration dati
- **Sub-GHz Scheduler** per persistenza su sistemi RF
- **NFC Relay** per mantenere accesso a sistemi badge

### 5. Reporting

- Log di tutte le frequenze rilevate
- Dump dei badge clonati (con hash, non dati in chiaro)
- Screenshot delle vulnerabilità trovate
- Raccomandazioni di mitigazione per ogni finding

---

## Quick Reference - Comandi e Percorsi Utili

### Percorsi SD Card

```
/ext/subghz/         - File .sub registrati
/ext/nfc/            - Dump .nfc salvati
/ext/lfrfid/         - File RFID 125 kHz
/ext/ibutton/        - File .ibtn
/ext/infrared/       - File .ir e database universali
/ext/badusb/         - Script DuckyScript / BadUSB
/ext/apps/           - Applicazioni installate
/ext/apps_data/      - Dati delle applicazioni
/ext/subghz/assets/  - Database frequenze e protocolli
/ext/nfc/assets/     - Dizionari chiavi MIFARE
```

### File di Configurazione Importanti

```
/ext/subghz/assets/setting_user    - Frequenze custom Sub-GHz
/ext/nfc/assets/mf_classic_dict_user.nfc - Chiavi MIFARE custom
/ext/infrared/assets/tv.ir         - Database IR universale
```

---

## Risorse Esterne Utili

- **Firmware RogueMaster:** repository GitHub principale per il firmware custom utilizzato in questa guida
- **Flipper Zero Docs:** documentazione ufficiale per reference API e hardware
- **MIFARE Classic Tool (Android):** app complementare per analisi NFC sul campo
- **Proxmark3:** reference per confronto con tool NFC/RFID professionale
- **HackRF / RTL-SDR:** per analisi RF avanzata che va oltre le capacità del CC1101
- **Wireshark:** per analisi dei dump di pacchetti catturati

---

## Note sull'Autore

Questa guida è il risultato di esperienza pratica quotidiana con il Flipper Zero in contesti di:

- Penetration testing fisico su edifici commerciali e industriali
- Audit di sistemi di controllo accessi (NFC, RFID, iButton)
- Ricerca sulla sicurezza di protocolli RF consumer e industriali
- Hardware hacking e reverse engineering di dispositivi IoT
- Formazione e awareness sulla sicurezza fisica

Ogni sezione contiene blocchi `> Nota personale:` che documentano esperienze reali, successi, fallimenti e lezioni apprese sul campo.
