# Glossario Tecnico

Definizioni dei termini tecnici, acronimi e concetti usati in questo repository. Ordinato alfabeticamente.

---

## A

| Termine | Definizione |
|---------|------------|
| **ACL** | Access Control List - lista di permessi che definisce chi può accedere a una risorsa |
| **AES** | Advanced Encryption Standard - cifrario a blocchi (128/192/256 bit), usato in DESFire, WiFi WPA2 |
| **AMSI** | Antimalware Scan Interface - API Windows che permette agli AV di ispezionare script prima dell'esecuzione |
| **AP** | Access Point - punto di accesso WiFi |
| **ASK** | Amplitude Shift Keying - modulazione che codifica i dati variando l'ampiezza del segnale RF |
| **ATQA** | Answer To Request type A - risposta di 2 byte di un tag NFC ISO 14443A, identifica il tipo |

## B

| Termine | Definizione |
|---------|------------|
| **BadUSB** | Attacco che sfrutta un dispositivo USB che si presenta come tastiera HID per iniettare comandi |
| **BLE** | Bluetooth Low Energy - versione a basso consumo del Bluetooth (4.0+), usata in IoT |
| **Bruteforce** | Attacco che prova tutte le combinazioni possibili fino a trovare quella corretta |

## C

| Termine | Definizione |
|---------|------------|
| **C2** | Command & Control - server che controlla un implant/agente su un sistema compromesso |
| **CC1101** | Chip transceiver Sub-GHz di Texas Instruments, usato nel Flipper Zero (300-928 MHz) |
| **CN** | Card Number - numero identificativo della card in un sistema HID Prox |
| **Crypto1** | Algoritmo crittografico proprietario di NXP usato in MIFARE Classic, rotto nel 2008 |
| **CVSS** | Common Vulnerability Scoring System - sistema standardizzato di valutazione gravità vulnerabilità |

## D

| Termine | Definizione |
|---------|------------|
| **DAP** | Debug Access Port - interfaccia ARM per debugging via SWD/JTAG |
| **DESFire** | Famiglia di smart card NXP con crittografia AES/3DES, molto più sicura di MIFARE Classic |
| **DFU** | Device Firmware Update - formato file per aggiornamento firmware via USB |
| **DuckyScript** | Linguaggio di scripting per keystroke injection, creato da Hak5 per USB Rubber Ducky |

## E

| Termine | Definizione |
|---------|------------|
| **EDR** | Endpoint Detection and Response - software di sicurezza che monitora comportamenti sospetti |
| **EM4100** | Chip RFID 125 kHz read-only, il più comune in badge economici, ZERO sicurezza |
| **Emulazione** | Il Flipper si comporta come il dispositivo originale (tag, telecomando, tastiera) |
| **Evil Portal** | Captive portal malevolo che imita pagine di login per raccogliere credenziali |

## F

| Termine | Definizione |
|---------|------------|
| **FC** | Facility Code - codice che identifica la struttura/edificio in un sistema HID Prox |
| **FDX-B** | Full Duplex B - standard ISO 11784/11785 per microchip animali (134.2 kHz) |
| **FSK** | Frequency Shift Keying - modulazione che codifica dati variando la frequenza |
| **Fuzzing** | Tecnica di test che invia input casuali o semi-casuali per trovare vulnerabilità |

## G

| Termine | Definizione |
|---------|------------|
| **GATT** | Generic Attribute Profile - protocollo BLE per lo scambio dati tra dispositivi |
| **Gen4** | Generazione 4 di Magic Card NFC - card MIFARE programmabile con UID scrivibile e Block 0 modificabile |
| **GPIO** | General Purpose Input/Output - pin del Flipper per connettere hardware esterno |

## H

| Termine | Definizione |
|---------|------------|
| **HID** | Human Interface Device - classe USB per tastiere, mouse, gamepad. Anche: HID Global (produttore badge) |
| **HID Prox** | Sistema di badge 125 kHz di HID Global, molto diffuso in ambito corporate |
| **H10301** | Formato HID a 26 bit: 1 parity + 8 FC + 16 CN + 1 parity |

## I

| Termine | Definizione |
|---------|------------|
| **I2C** | Inter-Integrated Circuit - bus seriale a 2 fili (SDA, SCL) per comunicazione tra chip |
| **ISM** | Industrial, Scientific, Medical - bande di frequenza libere (433 MHz, 868 MHz, 2.4 GHz) |
| **ISO 14443** | Standard per smart card contactless (NFC), Type A (MIFARE) e Type B |

## J-K

| Termine | Definizione |
|---------|------------|
| **JTAG** | Joint Test Action Group - interfaccia di debug hardware (4-5 pin), più complessa di SWD |
| **KeeLoq** | Algoritmo rolling code di Microchip, usato in telecomandi garage (Nice, Came, BFT) |
| **Keystroke Injection** | Iniezione di battute di tastiera - il principio alla base di BadUSB e MouseJacker |

## L

| Termine | Definizione |
|---------|------------|
| **LF** | Low Frequency - 125 kHz, usata per RFID legacy (EM4100, HID Prox) |
| **LOLBins** | Living Off the Land Binaries - eseguibili legittimi di Windows usati per scopi malevoli |
| **LoRa** | Long Range - tecnologia radio a basso consumo per IoT (433/868/915 MHz) |

## M

| Termine | Definizione |
|---------|------------|
| **Magic Card** | Card NFC compatibile MIFARE con UID e settori scrivibili, usata per clonazione |
| **Manchester** | Codifica di linea che rappresenta i bit tramite transizioni (usata in RC5, RFID) |
| **MFKey32** | Attacco che recupera chiavi MIFARE Classic osservando l'autenticazione con un lettore reale |
| **MIFARE Classic** | Smart card NXP con crittografia Crypto1 (rotta), la più diffusa per controllo accessi |
| **MITM** | Man In The Middle - attacco che intercetta e manipola comunicazioni tra due parti |
| **MouseJacker** | Vulnerabilità nei mouse/tastiere wireless 2.4 GHz non Bluetooth (Bastille Research, 2016) |

## N

| Termine | Definizione |
|---------|------------|
| **NEC** | Protocollo IR più comune, header 9ms+4.5ms, address 8bit + command 8bit + inversione |
| **NFC** | Near Field Communication - comunicazione contactless a 13.56 MHz, range 1-10 cm |
| **NRF24L01+** | Chip radio 2.4 GHz di Nordic Semiconductor, usato per MouseJacker e sniffing |
| **NTAG** | Famiglia di tag NFC di NXP (NTAG213/215/216), usati per URL, automazioni, amiibo |

## O

| Termine | Definizione |
|---------|------------|
| **OOK** | On-Off Keying - forma più semplice di ASK, il segnale è presente (1) o assente (0) |
| **OSINT** | Open Source Intelligence - raccolta informazioni da fonti pubbliche |

## P

| Termine | Definizione |
|---------|------------|
| **PMKID** | Pairwise Master Key Identifier - hash catturabile senza client connesso per cracking WPA2 offline |
| **POCSAG** | Post Office Code Standardization Advisory Group - protocollo per pager, non cifrato |
| **PSK** | Phase Shift Keying - modulazione che codifica dati variando la fase. Anche: Pre-Shared Key (WiFi) |

## R

| Termine | Definizione |
|---------|------------|
| **RC5/RC6** | Protocolli IR Philips con codifica Manchester, usati in TV europee |
| **Relay Attack** | Attacco che estende la distanza tra tag e lettore NFC tramite due dispositivi ponte |
| **Replay Attack** | Ritrasmissione di un segnale catturato per riprodurre un'azione (aprire cancello, ecc.) |
| **Rolling Code** | Codice che cambia ad ogni trasmissione (KeeLoq, AUT64), resiste al replay semplice |
| **RollJam** | Attacco contro rolling code: jamming + cattura di 2 codici consecutivi |
| **RW1990** | iButton scrivibile, compatibile con DS1990A, usato per clonazione |

## S

| Termine | Definizione |
|---------|------------|
| **SAK** | Select Acknowledge - byte di risposta NFC che identifica il tipo di card (0x08=Classic 1K, 0x20=DESFire) |
| **SDA/SCL** | Linee dati e clock del bus I2C |
| **SIRC** | Sony Infrared Remote Control - protocollo IR Sony (12/15/20 bit) |
| **SPI** | Serial Peripheral Interface - bus seriale a 4 fili (MOSI, MISO, SCK, CS) |
| **ST25R3916** | Chip NFC del Flipper Zero, supporta ISO 14443A/B, ISO 15693, FeliCa |
| **SWD** | Serial Wire Debug - interfaccia debug ARM a 2 fili (SWCLK, SWDIO), alternativa leggera a JTAG |

## T

| Termine | Definizione |
|---------|------------|
| **T5577** | Chip RFID 125 kHz programmabile, può emulare EM4100, HID Prox, Indala e altri |
| **TPMS** | Tire Pressure Monitoring System - sensori pressione pneumatici, trasmettono a 433 MHz |
| **TSAL6200** | LED infrarosso del Flipper Zero, 940nm, potenza 100mW |

## U-V

| Termine | Definizione |
|---------|------------|
| **U2F** | Universal 2nd Factor - standard FIDO per autenticazione a due fattori via USB/NFC |
| **UAC** | User Account Control - meccanismo Windows che richiede conferma per azioni admin |
| **UART** | Universal Asynchronous Receiver/Transmitter - interfaccia seriale (TX, RX), usata per console debug |
| **UID** | Unique Identifier - identificativo univoco di un tag NFC/RFID |

## W-Z

| Termine | Definizione |
|---------|------------|
| **Wiegand** | Protocollo di comunicazione usato tra lettori badge e centraline di controllo accessi |
| **WPA2** | WiFi Protected Access 2 - standard di sicurezza WiFi basato su AES-CCMP |
| **XInput** | API Microsoft per gamepad Xbox, usata dal Flipper per emulazione controller |
