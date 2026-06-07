# Lab Setup - Home Testing Laboratory

Guide to creating a personal laboratory to safely practice all the techniques described in this repository. All listed devices are legal to own and use on your own property.

---

## Lab Philosophy

A home laboratory allows you to:
- Practice techniques without legal risks (everything is yours)
- Test payloads and exploits before a real engagement
- Understand the real limits of the Flipper Zero under controlled conditions
- Develop and debug BadUSB scripts
- Experiment with RF protocols without interfering with third parties

> **Personal note:** My home lab was the best investment of my pentesting career. Every technique I use in the field, I first practiced 10 times at home. The total lab cost is less than a single engagement -- and it pays for itself from the first job.

---

## Basic Kit - Essentials (~50-100 EUR)

### Test Tags and Badges

| Type | Quantity | Price | Where to Buy | Use |
|------|----------|-------|---------------|-----|
| **T5577 keyfob** | 20 pieces | ~8 EUR | AliExpress | RFID 125 kHz cloning |
| **T5577 ISO card** | 10 pieces | ~6 EUR | AliExpress | Card reader testing |
| **EM4100 keyfob** | 10 pieces | ~3 EUR | AliExpress | Read-only reference tags |
| **Magic Card Gen4 (MIFARE)** | 10 pieces | ~20 EUR | AliExpress | NFC cloning |
| **MIFARE Classic 1K** | 5 pieces | ~5 EUR | AliExpress | NFC test tags |
| **NTAG215** | 10 pieces | ~5 EUR | Amazon/AliExpress | Writable NFC tags |
| **iButton DS1990A** | 5 pieces | ~5 EUR | AliExpress | 1-Wire testing |
| **iButton RW1990** | 5 pieces | ~5 EUR | AliExpress | iButton cloning |

**Beware of fake T5577s:** many sellers on AliExpress sell EM4100 tags disguised as T5577. Verify: a real T5577 is writable with the Flipper, an EM4100 is not. Buy from high-rated sellers with positive reviews.

### Test Readers

| Type | Price | Use |
|------|-------|-----|
| **RFID 125 kHz standalone reader** | ~15 EUR | Target for cloning/fuzzing tests |
| **NFC ACR122U reader** (USB) | ~25 EUR | Advanced NFC read/write from PC |

### RF Remote Controls

| Type | Price | Use |
|------|-------|-----|
| **Generic 433 MHz remote** (fixed code) | ~5 EUR | Sub-GHz read/replay testing |
| **433 MHz remote-controlled outlet** | ~10 EUR | Target for replay testing |
| **433 MHz wireless doorbell** | ~8 EUR | Target for Sub-GHz testing |

---

## Intermediate Kit - Expansion (~150-300 EUR)

### GPIO Modules

| Module | Price | Use |
|--------|-------|-----|
| **ESP32 WiFi Devboard** (for Flipper) | ~15 EUR | WiFi Marauder, Evil Portal |
| **Generic ESP32 WROOM** | ~5 EUR | Spare/firmware testing |
| **NRF24L01+ with PA+LNA antenna** | ~5 EUR | MouseJacker, 2.4 GHz sniffing |
| **CC1101 external module** | ~8 EUR | External Sub-GHz antenna, extended range |
| **Bus Pirate v4** or clone | ~25 EUR | Advanced I2C/SPI/UART debugging |

### Wireless Peripherals (MouseJacker Targets)

| Type | Price | Notes |
|------|-------|-------|
| **Non-Unifying Logitech mouse** (old) | ~10 EUR used | Target vulnerable to MouseJacker |
| **Cheap 2.4 GHz wireless keyboard** | ~15 EUR | Target for keystroke sniffing |
| **Generic wireless mouse (no Bluetooth)** | ~8 EUR | Injection testing |

### WiFi Test Equipment

| Type | Price | Use |
|------|-------|-----|
| **Old WiFi router** (WPA2-PSK) | ~10 EUR used | Target for handshake/PMKID |
| **Raspberry Pi 3/4** with hostapd | ~35-50 EUR | Configurable test AP |

### IR Test Equipment

| Type | Price | Use |
|------|-------|-----|
| **Cheap TV with IR remote** | ~30 EUR used | Target for IR testing |
| **Portable air conditioner** | already have one? | Target for AC IR testing |
| **IR LED receiver module** | ~2 EUR | IR signal verification |

---

## Advanced Kit - Professional (~500-1000 EUR)

### Complementary Hardware

| Tool | Price | Why You Need It |
|------|-------|----------------|
| **Proxmark3 RDV4** | ~300 EUR | Advanced RFID/NFC: reader-tag sniffing, T5577 password cracking, protocols not supported by the Flipper |
| **HackRF One** | ~200 EUR | Full-duplex SDR: professional RF analysis, capture/replay on any frequency |
| **RTL-SDR v3** | ~25 EUR | Budget SDR for reception: spectrum analyzer, signal analysis, POCSAG |
| **Log-periodic antenna** | ~50 EUR | Directional wideband reception |
| **WiFi adapter (monitor mode)** | ~20 EUR | Alfa AWUS036ACH for WiFi auditing from laptop |

### Recommended Software

| Software | Platform | Use |
|----------|----------|-----|
| **SDR#** / **GQRX** | Win / Linux | RF spectrum analysis with RTL-SDR/HackRF |
| **GNURadio** | Linux | Custom demodulation, RF flowgraph creation |
| **Wireshark** | Cross-platform | Packet analysis (WiFi, BLE) |
| **hashcat** | Cross-platform | WPA2 handshake/PMKID cracking |
| **aircrack-ng** | Linux | Complete WiFi auditing suite |
| **Proxmark3 client** | Cross-platform | Proxmark3 interface |
| **MIFARE Classic Tool** | Android | NFC analysis from smartphone |
| **NFC TagInfo** | Android/iOS | Quick NFC tag identification |

---

## Laboratory Setup

### RF Workstation

```
[PC/Laptop with SDR#/GNURadio]
    |
    |-- [RTL-SDR] ←antenna→ Sub-GHz signal reception
    |-- [HackRF]  ←antenna→ full-duplex TX/RX
    |
[Flipper Zero] ←GPIO→ [external CC1101] ←SMA antenna→
    |
[RF Targets:]
    |-- 433 MHz remote + remote-controlled outlet
    |-- Wireless doorbell
    |-- Wireless weather sensor (optional)
```

### NFC/RFID Workstation

```
[PC with Proxmark3 client]
    |-- [Proxmark3 RDV4] ←antenna→
    |
[Flipper Zero]
    |
[Targets:]
    |-- RFID 125 kHz standalone reader
    |-- EM4100 / HID Prox / T5577 tags
    |-- MIFARE Classic 1K / Gen4 Magic Card
    |-- iButton DS1990A / RW1990
```

### WiFi Workstation

```
[PC with aircrack-ng / hashcat]
    |-- [Alfa WiFi adapter] (monitor mode)
    |
[Flipper Zero] ←GPIO→ [ESP32 Marauder]
    |
[Targets:]
    |-- WPA2 WiFi router (known password for testing)
    |-- Raspberry Pi as rogue AP
```

### BadUSB Workstation

```
[Target PC (old laptop / VM)]
    |
    |-- USB →← [Flipper Zero BadUSB]
    |
[Test environment:]
    |-- Windows 10/11 VM (no AV for basic testing)
    |-- Windows 10/11 VM (with Defender for evasion testing)
    |-- macOS VM or physical
    |-- Linux VM
```

---

## Laboratory Rules

### RF Safety

- **Do not transmit on frequencies you don't own** -- even at home, RF transmissions propagate
- **Use minimum power** -- the Flipper at +12 dBm is already low, but avoid prolonged transmissions
- **Sub-GHz:** use ISM frequencies (433.92 MHz, 868 MHz) which are license-free for low-power transmissions
- **WiFi:** use YOUR router on a channel that doesn't interfere with neighbors
- **If possible:** use a Faraday cage (even improvised with aluminum foil) for RF testing

### Network Safety

- **Isolate the test network** -- use a dedicated router not connected to the Internet
- **Do not use your main WiFi** for deauth/evil portal testing
- **VM for BadUSB** -- do not test payloads on machines with real data

### Legal Safety

- Everything in the lab is on devices YOU own -- you are in compliance
- Do not extend tests to neighbors' devices (WiFi, RF)
- If you live in an apartment building: be careful with Sub-GHz signals that can reach other units
- Keep a lab notebook with dates and activities performed (good professional practice)

---

## Recommended First Exercises

### Exercise 1 - Sub-GHz: Capture and Replay
1. Take the 433 MHz remote for the remote-controlled outlet
2. Sub-GHz → Read → capture the signal
3. Analyze: protocol, bits, modulation
4. Sub-GHz → Saved → Send → the outlet turns on/off
5. Try Read RAW for raw capture
6. Compare the two .sub files

### Exercise 2 - RFID: Clone to T5577
1. Read an EM4100 tag with RFID → Read
2. Save the file
3. Write to a T5577 with Write
4. Verify by reading the T5577
5. Test both on the standalone reader

### Exercise 3 - NFC: Dictionary Attack
1. Read a MIFARE Classic 1K with NFC → Read
2. Launch the Dictionary Attack
3. If keys are found: full dump
4. Write the dump to a Magic Card Gen4
5. Use the Comparator to compare original and clone

### Exercise 4 - BadUSB: Hello World
1. Create a script: `STRING Hello from Flipper!` + `ENTER`
2. Upload to SD card in `/ext/badusb/`
3. Execute on a Windows VM
4. Progress: open notepad, type text, save file

### Exercise 5 - WiFi: Scan with Marauder
1. Flash Marauder onto the ESP32
2. Connect to the Flipper via GPIO
3. `scanap` → list all nearby APs
4. `scansta` → list all clients
5. `sniffpmkid` → capture PMKID from YOUR router

### Exercise 6 - IR: Capture and Replay
1. Point the TV remote at the Flipper
2. IR → Learn New Remote → capture each button
3. Save as custom remote
4. Use the Flipper as a remote control

### Exercise 7 - NRF24: Channel Scan
1. Connect the NRF24L01+ to GPIO
2. Launch Channel Scan
3. Observe active channels at 2.4 GHz
4. Identify your wireless mouse/keyboard

> **Personal note:** I started with these exercises even before my first professional engagement. Lab practice gave me the confidence to operate in the field without hesitation. Every pentester should have a lab -- it's like a musician rehearsing before a concert.

---

## Budget Summary

| Level | Budget | What It Covers |
|-------|--------|---------------|
| **Basic** | 50-100 EUR | Test tags/badges, RF remote, remote-controlled outlet |
| **Intermediate** | 150-300 EUR | Basic + ESP32, NRF24, CC1101, test router, wireless peripherals |
| **Advanced** | 500-1000 EUR | Intermediate + Proxmark3, HackRF, RTL-SDR, WiFi adapter |
| **Professional** | 1000+ EUR | Advanced + directional antenna, oscilloscope, logic analyzer |

> **Personal note:** Start with the Basic Kit -- it costs less than a dinner out and lets you practice 80% of the techniques. Add the Proxmark3 when you feel the Flipper isn't enough (it happens quickly with NFC/RFID). The HackRF is a luxury that becomes a necessity when you start doing serious RF analysis.
