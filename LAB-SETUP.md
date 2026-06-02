# Lab Setup - Laboratorio di Test Domestico

Guida alla creazione di un laboratorio personale per praticare in sicurezza tutte le tecniche descritte in questo repository. Tutti i dispositivi elencati sono legali da possedere e usare su propria proprietà.

---

## Filosofia del Lab

Un laboratorio domestico permette di:
- Praticare tecniche senza rischi legali (tutto è tuo)
- Testare payload e exploit prima di un engagement reale
- Capire i limiti reali del Flipper Zero in condizioni controllate
- Sviluppare e debuggare script BadUSB
- Sperimentare con protocolli RF senza interferire con terzi

> **Nota personale:** Il mio lab domestico è stato l'investimento migliore della mia carriera di pentester. Ogni tecnica che uso in campo l'ho prima provata 10 volte a casa. Il costo totale del lab è inferiore a un singolo engagement - e si ripaga dal primo lavoro.

---

## Kit Base - Essenziali (~50-100 EUR)

### Tag e Badge di Prova

| Tipo | Quantità | Prezzo | Dove Comprare | Uso |
|------|----------|--------|---------------|-----|
| **T5577 keyfob** | 20 pezzi | ~8 EUR | AliExpress | Clonazione RFID 125 kHz |
| **T5577 card ISO** | 10 pezzi | ~6 EUR | AliExpress | Test con lettori card |
| **EM4100 keyfob** | 10 pezzi | ~3 EUR | AliExpress | Tag di riferimento read-only |
| **Magic Card Gen4 (MIFARE)** | 10 pezzi | ~20 EUR | AliExpress | Clonazione NFC |
| **MIFARE Classic 1K** | 5 pezzi | ~5 EUR | AliExpress | Tag di test NFC |
| **NTAG215** | 10 pezzi | ~5 EUR | Amazon/AliExpress | Tag NFC scrivibili |
| **iButton DS1990A** | 5 pezzi | ~5 EUR | AliExpress | Test 1-Wire |
| **iButton RW1990** | 5 pezzi | ~5 EUR | AliExpress | Clonazione iButton |

**Attenzione T5577 falsi:** molti venditori su AliExpress vendono EM4100 spacciati per T5577. Verifica: un vero T5577 è scrivibile con il Flipper, un EM4100 no. Compra da venditori con rating alto e recensioni positive.

### Lettori di Prova

| Tipo | Prezzo | Uso |
|------|--------|-----|
| **Lettore RFID 125 kHz standalone** | ~15 EUR | Target per test clonazione/fuzzing |
| **Lettore NFC ACR122U** (USB) | ~25 EUR | Lettura/scrittura NFC avanzata da PC |

### Telecomandi RF

| Tipo | Prezzo | Uso |
|------|--------|-----|
| **Telecomando 433 MHz generico** (codice fisso) | ~5 EUR | Test Sub-GHz read/replay |
| **Presa telecomandata 433 MHz** | ~10 EUR | Target per test replay |
| **Campanello wireless 433 MHz** | ~8 EUR | Target per test Sub-GHz |

---

## Kit Intermedio - Espansione (~150-300 EUR)

### Moduli GPIO

| Modulo | Prezzo | Uso |
|--------|--------|-----|
| **ESP32 WiFi Devboard** (per Flipper) | ~15 EUR | WiFi Marauder, Evil Portal |
| **ESP32 WROOM generico** | ~5 EUR | Spare/test firmware |
| **NRF24L01+ con antenna PA+LNA** | ~5 EUR | MouseJacker, sniffing 2.4 GHz |
| **CC1101 modulo esterno** | ~8 EUR | Antenna Sub-GHz esterna, portata estesa |
| **Bus Pirate v4** o clone | ~25 EUR | I2C/SPI/UART debug avanzato |

### Periferiche Wireless (Target MouseJacker)

| Tipo | Prezzo | Note |
|------|--------|------|
| **Mouse Logitech non-Unifying** (vecchio) | ~10 EUR usato | Target vulnerabile a MouseJacker |
| **Tastiera wireless 2.4 GHz economica** | ~15 EUR | Target per keystroke sniffing |
| **Mouse wireless generico (no Bluetooth)** | ~8 EUR | Test injection |

### WiFi di Test

| Tipo | Prezzo | Uso |
|------|--------|-----|
| **Router WiFi vecchio** (WPA2-PSK) | ~10 EUR usato | Target per handshake/PMKID |
| **Raspberry Pi 3/4** con hostapd | ~35-50 EUR | AP di test configurabile |

### IR di Test

| Tipo | Prezzo | Uso |
|------|--------|-----|
| **TV economica con telecomando IR** | ~30 EUR usata | Target per IR testing |
| **Condizionatore portatile** | già presente? | Target per test AC IR |
| **LED IR receiver module** | ~2 EUR | Verifica segnali IR |

---

## Kit Avanzato - Professionale (~500-1000 EUR)

### Hardware Complementare

| Strumento | Prezzo | Perchè Serve |
|-----------|--------|--------------|
| **Proxmark3 RDV4** | ~300 EUR | RFID/NFC avanzato: sniffing reader-tag, password cracking T5577, protocolli non supportati dal Flipper |
| **HackRF One** | ~200 EUR | SDR full-duplex: analisi RF professionale, cattura/replay su qualsiasi frequenza |
| **RTL-SDR v3** | ~25 EUR | SDR economico per ricezione: spectrum analyzer, analisi segnali, POCSAG |
| **Antenna log-periodica** | ~50 EUR | Ricezione direzionale wideband |
| **WiFi adapter (monitor mode)** | ~20 EUR | Alfa AWUS036ACH per WiFi auditing da laptop |

### Software Consigliato

| Software | Piattaforma | Uso |
|----------|------------|-----|
| **SDR#** / **GQRX** | Win / Linux | Analisi spettro RF con RTL-SDR/HackRF |
| **GNURadio** | Linux | Demodulazione custom, creazione flowgraph RF |
| **Wireshark** | Cross-platform | Analisi pacchetti (WiFi, BLE) |
| **hashcat** | Cross-platform | Cracking WPA2 handshake/PMKID |
| **aircrack-ng** | Linux | Suite completa WiFi auditing |
| **Proxmark3 client** | Cross-platform | Interfaccia Proxmark3 |
| **MIFARE Classic Tool** | Android | Analisi NFC da smartphone |
| **NFC TagInfo** | Android/iOS | Identificazione rapida tag NFC |

---

## Setup del Laboratorio

### Postazione RF

```
[PC/Laptop con SDR#/GNURadio]
    |
    |-- [RTL-SDR] ←antenna→ ricezione segnali Sub-GHz
    |-- [HackRF]  ←antenna→ TX/RX full-duplex
    |
[Flipper Zero] ←GPIO→ [CC1101 esterno] ←antenna SMA→
    |
[Target RF:]
    |-- Telecomando 433 MHz + presa telecomandata
    |-- Campanello wireless
    |-- Sensore meteo wireless (opzionale)
```

### Postazione NFC/RFID

```
[PC con Proxmark3 client]
    |-- [Proxmark3 RDV4] ←antenna→
    |
[Flipper Zero]
    |
[Target:]
    |-- Lettore RFID 125 kHz standalone
    |-- Tag EM4100 / HID Prox / T5577
    |-- MIFARE Classic 1K / Gen4 Magic Card
    |-- iButton DS1990A / RW1990
```

### Postazione WiFi

```
[PC con aircrack-ng / hashcat]
    |-- [Alfa WiFi adapter] (monitor mode)
    |
[Flipper Zero] ←GPIO→ [ESP32 Marauder]
    |
[Target:]
    |-- Router WiFi WPA2 (password nota per test)
    |-- Raspberry Pi come rogue AP
```

### Postazione BadUSB

```
[PC target (vecchio laptop / VM)]
    |
    |-- USB →← [Flipper Zero BadUSB]
    |
[Ambiente di test:]
    |-- Windows 10/11 VM (senza AV per test base)
    |-- Windows 10/11 VM (con Defender per test evasione)
    |-- macOS VM o fisico
    |-- Linux VM
```

---

## Regole del Laboratorio

### Sicurezza RF

- **Non trasmettere su frequenze che non ti appartengono** - anche in casa, le trasmissioni RF si propagano
- **Usa la potenza minima** - il Flipper a +12 dBm è già basso, ma evita trasmissioni prolungate
- **Sub-GHz:** usa frequenze ISM (433.92 MHz, 868 MHz) che sono libere per trasmissioni a bassa potenza
- **WiFi:** usa il TUO router su un canale che non interferisce con i vicini
- **Se possibile:** usa una gabbia di Faraday (anche improvvisata con foglio di alluminio) per i test RF

### Sicurezza Rete

- **Isola la rete di test** - usa un router dedicato non connesso a Internet
- **Non usare il tuo WiFi principale** per test di deauth/evil portal
- **VM per BadUSB** - non testare payload su macchine con dati reali

### Sicurezza Legale

- Tutto il lab è su dispositivi di TUA proprietà - sei in regola
- Non estendere i test ai dispositivi dei vicini (WiFi, RF)
- Se vivi in condominio: attenzione ai segnali Sub-GHz che possono raggiungere altri appartamenti
- Tieni un quaderno di lab con le date e le attività svolte (buona pratica professionale)

---

## Primi Esercizi Consigliati

### Esercizio 1 - Sub-GHz: Cattura e Replay
1. Prendi il telecomando 433 MHz della presa telecomandata
2. Sub-GHz → Read → cattura il segnale
3. Analizza: protocollo, bit, modulazione
4. Sub-GHz → Saved → Send → la presa si accende/spegne
5. Prova Read RAW per la cattura grezza
6. Confronta i due file .sub

### Esercizio 2 - RFID: Clone su T5577
1. Leggi un tag EM4100 con RFID → Read
2. Salva il file
3. Scrivi su un T5577 con Write
4. Verifica leggendo il T5577
5. Testa entrambi sul lettore standalone

### Esercizio 3 - NFC: Dictionary Attack
1. Leggi una MIFARE Classic 1K con NFC → Read
2. Avvia il Dictionary Attack
3. Se trova le chiavi: dump completo
4. Scrivi il dump su una Magic Card Gen4
5. Usa il Comparator per confrontare originale e clone

### Esercizio 4 - BadUSB: Hello World
1. Crea uno script: `STRING Hello from Flipper!` + `ENTER`
2. Carica su SD card in `/ext/badusb/`
3. Esegui su una VM Windows
4. Progredisci: apri notepad, digita testo, salva file

### Esercizio 5 - WiFi: Scan con Marauder
1. Flash Marauder sull'ESP32
2. Connetti al Flipper via GPIO
3. `scanap` → lista tutti gli AP nelle vicinanze
4. `scansta` → lista tutti i client
5. `sniffpmkid` → cattura PMKID dal TUO router

### Esercizio 6 - IR: Cattura e Replay
1. Punta il telecomando della TV verso il Flipper
2. IR → Learn New Remote → cattura ogni pulsante
3. Salva come remote custom
4. Usa il Flipper come telecomando

### Esercizio 7 - NRF24: Channel Scan
1. Collega il NRF24L01+ al GPIO
2. Avvia il Channel Scan
3. Osserva i canali attivi a 2.4 GHz
4. Identifica il tuo mouse/tastiera wireless

> **Nota personale:** Ho iniziato con questi esercizi prima ancora del mio primo engagement professionale. La pratica in lab mi ha dato la confidenza per operare in campo senza esitazioni. Ogni pentester dovrebbe avere un lab - è come un musicista che prova prima del concerto.

---

## Budget Riassuntivo

| Livello | Budget | Cosa Copre |
|---------|--------|-----------|
| **Base** | 50-100 EUR | Tag/badge di prova, telecomando RF, presa telecomandata |
| **Intermedio** | 150-300 EUR | Base + ESP32, NRF24, CC1101, router test, periferiche wireless |
| **Avanzato** | 500-1000 EUR | Intermedio + Proxmark3, HackRF, RTL-SDR, WiFi adapter |
| **Professionale** | 1000+ EUR | Avanzato + antenna direzionale, oscilloscopio, logic analyzer |

> **Nota personale:** Parti dal Kit Base - costa meno di una cena fuori e ti permette di praticare l'80% delle tecniche. Aggiungi il Proxmark3 quando senti che il Flipper non basta (succede velocemente con NFC/RFID). L'HackRF è un lusso che diventa necessità quando inizi a fare analisi RF seria.
