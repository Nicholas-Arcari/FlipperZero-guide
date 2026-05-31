# Debug - Overview

Strumenti avanzati di **hardware hacking** del Flipper Zero: debug SWD/JTAG, programmazione AVR, comunicazione I2C/SPI, dump firmware e reverse engineering di dispositivi embedded.

**Interfacce:** SWD, JTAG, I2C, SPI, UART | **Target:** MCU (ARM, AVR), EEPROM, Flash, dispositivi embedded

---

## Contenuti

| # | File | Descrizione |
|---|------|-------------|
| 01 | [Fondamenti e Hardware](01-Fondamenti-e-Hardware.md) | SWD/JTAG protocols, debug interfaces, wiring, target identification |
| 02 | [Tool Debug](02-Tool-Debug.md) | SWD Probe (firmware extraction, register read, breakpoints), DAP Link (GDB integration), AVR Flasher (fuse, flash, EEPROM) |
| 03 | [Tool Bus](03-Tool-Bus.md) | I2C Tools (scanner, sniffer, sender), SPI Mem Manager (read/write/verify flash), Ethernet Troubleshooter |
| 04 | [Scenari Reali](04-Scenari-Reali.md) | Scenari hardware hacking: firmware extraction IoT, I2C EEPROM cloning, SPI flash dump, SWD exploitation, UART console |
| 06 | [Esperienza Personale](06-Esperienza-Personale.md) | Note dal campo, errori hardware hacking, appendice riferimenti rapidi |

---

## Quick Reference - Tool e Interfacce

| Tool | Interfaccia | Funzione | Target Tipico |
|------|------------|----------|---------------|
| SWD Probe | SWD (2 pin) | Debug, firmware extraction | ARM Cortex-M |
| DAP Link | SWD/JTAG | GDB debugging | ARM generico |
| AVR Flasher | ISP (6 pin) | Flash/fuse/EEPROM | ATmega, ATtiny |
| I2C Scanner | I2C (2 pin) | Device enumeration | Sensori, EEPROM |
| I2C Sniffer | I2C (2 pin) | Bus monitoring | Qualsiasi I2C |
| SPI Mem Manager | SPI (4 pin) | Flash read/write | 25-series flash |

## Quick Reference - Pinout Debug

```
Flipper GPIO    SWD Target       I2C Target       SPI Target
PA14 (SWCLK) → SWCLK           PA7 (MOSI)     → MOSI
PA13 (SWDIO) → SWDIO           PA6 (MISO)     → MISO
GND           → GND             PB3 (SCK)      → SCK
3.3V          → VCC (opz.)     PA4 (CS)       → CS
                                PC0 (SDA)      → SDA
                                PC1 (SCL)      → SCL
```

> **Nota personale:** Il Flipper come tool di hardware hacking è sottovalutato. Non sostituisce un J-Link o un Bus Pirate, ma per operazioni rapide sul campo (dump EEPROM I2C, read SPI flash, check SWD) è imbattibile per portabilità. Ho estratto firmware da 3 IoT device diversi usando solo il Flipper durante un engagement.
