# Technical Glossary

Definitions of technical terms, acronyms, and concepts used in this repository. Sorted alphabetically.

---

## A

| Term | Definition |
|------|-----------|
| **ACL** | Access Control List -- a list of permissions defining who can access a resource |
| **AES** | Advanced Encryption Standard -- block cipher (128/192/256 bit), used in DESFire, WiFi WPA2 |
| **AMSI** | Antimalware Scan Interface -- Windows API that allows AVs to inspect scripts before execution |
| **AP** | Access Point -- WiFi access point |
| **ASK** | Amplitude Shift Keying -- modulation that encodes data by varying the amplitude of the RF signal |
| **ATQA** | Answer To Request type A -- 2-byte response from an NFC ISO 14443A tag, identifies the type |

## B

| Term | Definition |
|------|-----------|
| **BadUSB** | Attack that exploits a USB device presenting itself as an HID keyboard to inject commands |
| **BLE** | Bluetooth Low Energy -- low-power version of Bluetooth (4.0+), used in IoT |
| **Bruteforce** | Attack that tries all possible combinations until finding the correct one |

## C

| Term | Definition |
|------|-----------|
| **C2** | Command & Control -- server that controls an implant/agent on a compromised system |
| **CC1101** | Sub-GHz transceiver chip by Texas Instruments, used in Flipper Zero (300-928 MHz) |
| **CN** | Card Number -- card identification number in an HID Prox system |
| **Crypto1** | Proprietary cryptographic algorithm by NXP used in MIFARE Classic, broken in 2008 |
| **CVSS** | Common Vulnerability Scoring System -- standardized system for rating vulnerability severity |

## D

| Term | Definition |
|------|-----------|
| **DAP** | Debug Access Port -- ARM interface for debugging via SWD/JTAG |
| **DESFire** | NXP smart card family with AES/3DES encryption, much more secure than MIFARE Classic |
| **DFU** | Device Firmware Update -- file format for firmware updates via USB |
| **DuckyScript** | Scripting language for keystroke injection, created by Hak5 for USB Rubber Ducky |

## E

| Term | Definition |
|------|-----------|
| **EDR** | Endpoint Detection and Response -- security software that monitors suspicious behaviors |
| **EM4100** | 125 kHz read-only RFID chip, the most common in cheap badges, ZERO security |
| **Emulation** | The Flipper behaves like the original device (tag, remote, keyboard) |
| **Evil Portal** | Malicious captive portal that mimics login pages to harvest credentials |

## F

| Term | Definition |
|------|-----------|
| **FC** | Facility Code -- code that identifies the facility/building in an HID Prox system |
| **FDX-B** | Full Duplex B -- ISO 11784/11785 standard for animal microchips (134.2 kHz) |
| **FSK** | Frequency Shift Keying -- modulation that encodes data by varying the frequency |
| **Fuzzing** | Testing technique that sends random or semi-random inputs to find vulnerabilities |

## G

| Term | Definition |
|------|-----------|
| **GATT** | Generic Attribute Profile -- BLE protocol for data exchange between devices |
| **Gen4** | Generation 4 NFC Magic Card -- programmable MIFARE card with writable UID and modifiable Block 0 |
| **GPIO** | General Purpose Input/Output -- Flipper pins for connecting external hardware |

## H

| Term | Definition |
|------|-----------|
| **HID** | Human Interface Device -- USB class for keyboards, mice, gamepads. Also: HID Global (badge manufacturer) |
| **HID Prox** | 125 kHz badge system by HID Global, widely deployed in corporate environments |
| **H10301** | HID 26-bit format: 1 parity + 8 FC + 16 CN + 1 parity |

## I

| Term | Definition |
|------|-----------|
| **I2C** | Inter-Integrated Circuit -- 2-wire serial bus (SDA, SCL) for inter-chip communication |
| **ISM** | Industrial, Scientific, Medical -- license-free frequency bands (433 MHz, 868 MHz, 2.4 GHz) |
| **ISO 14443** | Standard for contactless smart cards (NFC), Type A (MIFARE) and Type B |

## J-K

| Term | Definition |
|------|-----------|
| **JTAG** | Joint Test Action Group -- hardware debug interface (4-5 pins), more complex than SWD |
| **KeeLoq** | Rolling code algorithm by Microchip, used in garage door remotes (Nice, Came, BFT) |
| **Keystroke Injection** | Injection of keystrokes -- the principle behind BadUSB and MouseJacker |

## L

| Term | Definition |
|------|-----------|
| **LF** | Low Frequency -- 125 kHz, used for legacy RFID (EM4100, HID Prox) |
| **LOLBins** | Living Off the Land Binaries -- legitimate Windows executables used for malicious purposes |
| **LoRa** | Long Range -- low-power radio technology for IoT (433/868/915 MHz) |

## M

| Term | Definition |
|------|-----------|
| **Magic Card** | MIFARE-compatible NFC card with writable UID and sectors, used for cloning |
| **Manchester** | Line encoding that represents bits through transitions (used in RC5, RFID) |
| **MFKey32** | Attack that recovers MIFARE Classic keys by observing authentication with a real reader |
| **MIFARE Classic** | NXP smart card with Crypto1 encryption (broken), the most widely deployed for access control |
| **MITM** | Man In The Middle -- attack that intercepts and manipulates communications between two parties |
| **MouseJacker** | Vulnerability in non-Bluetooth 2.4 GHz wireless mice/keyboards (Bastille Research, 2016) |

## N

| Term | Definition |
|------|-----------|
| **NEC** | Most common IR protocol, 9ms+4.5ms header, 8-bit address + 8-bit command + inversion |
| **NFC** | Near Field Communication -- contactless communication at 13.56 MHz, range 1-10 cm |
| **NRF24L01+** | 2.4 GHz radio chip by Nordic Semiconductor, used for MouseJacker and sniffing |
| **NTAG** | NXP NFC tag family (NTAG213/215/216), used for URLs, automations, amiibo |

## O

| Term | Definition |
|------|-----------|
| **OOK** | On-Off Keying -- simplest form of ASK, signal is present (1) or absent (0) |
| **OSINT** | Open Source Intelligence -- information gathering from public sources |

## P

| Term | Definition |
|------|-----------|
| **PMKID** | Pairwise Master Key Identifier -- hash capturable without a connected client for offline WPA2 cracking |
| **POCSAG** | Post Office Code Standardization Advisory Group -- protocol for pagers, unencrypted |
| **PSK** | Phase Shift Keying -- modulation that encodes data by varying the phase. Also: Pre-Shared Key (WiFi) |

## R

| Term | Definition |
|------|-----------|
| **RC5/RC6** | Philips IR protocols with Manchester encoding, used in European TVs |
| **Relay Attack** | Attack that extends the distance between NFC tag and reader via two bridge devices |
| **Replay Attack** | Retransmission of a captured signal to reproduce an action (open gate, etc.) |
| **Rolling Code** | Code that changes with each transmission (KeeLoq, AUT64), resists simple replay |
| **RollJam** | Attack against rolling code: jamming + capture of 2 consecutive codes |
| **RW1990** | Writable iButton, compatible with DS1990A, used for cloning |

## S

| Term | Definition |
|------|-----------|
| **SAK** | Select Acknowledge -- NFC response byte that identifies the card type (0x08=Classic 1K, 0x20=DESFire) |
| **SDA/SCL** | Data and clock lines of the I2C bus |
| **SIRC** | Sony Infrared Remote Control -- Sony IR protocol (12/15/20 bit) |
| **SPI** | Serial Peripheral Interface -- 4-wire serial bus (MOSI, MISO, SCK, CS) |
| **ST25R3916** | Flipper Zero's NFC chip, supports ISO 14443A/B, ISO 15693, FeliCa |
| **SWD** | Serial Wire Debug -- 2-wire ARM debug interface (SWCLK, SWDIO), lightweight alternative to JTAG |

## T

| Term | Definition |
|------|-----------|
| **T5577** | Programmable 125 kHz RFID chip, can emulate EM4100, HID Prox, Indala and others |
| **TPMS** | Tire Pressure Monitoring System -- tire pressure sensors, transmit at 433 MHz |
| **TSAL6200** | Flipper Zero's infrared LED, 940nm, 100mW power |

## U-V

| Term | Definition |
|------|-----------|
| **U2F** | Universal 2nd Factor -- FIDO standard for two-factor authentication via USB/NFC |
| **UAC** | User Account Control -- Windows mechanism that requires confirmation for admin actions |
| **UART** | Universal Asynchronous Receiver/Transmitter -- serial interface (TX, RX), used for debug consoles |
| **UID** | Unique Identifier -- unique identifier of an NFC/RFID tag |

## W-Z

| Term | Definition |
|------|-----------|
| **Wiegand** | Communication protocol used between badge readers and access control panels |
| **WPA2** | WiFi Protected Access 2 -- WiFi security standard based on AES-CCMP |
| **XInput** | Microsoft API for Xbox gamepads, used by the Flipper for controller emulation |
