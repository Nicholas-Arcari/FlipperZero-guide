# Debug - Overview

Advanced **hardware hacking** tools for the Flipper Zero: SWD/JTAG debugging, AVR programming, I2C/SPI communication, firmware dumping, and reverse engineering of embedded devices.

**Interfaces:** SWD, JTAG, I2C, SPI, UART | **Targets:** MCU (ARM, AVR), EEPROM, Flash, embedded devices

---

## Contents

| # | File | Description |
|---|------|-------------|
| 01 | [Fundamentals and Hardware](01-Fondamenti-e-Hardware.md) | SWD/JTAG protocols, debug interfaces, wiring, target identification |
| 02 | [Debug Tools](02-Tool-Debug.md) | SWD Probe (firmware extraction, register read, breakpoints), DAP Link (GDB integration), AVR Flasher (fuse, flash, EEPROM) |
| 03 | [Bus Tools](03-Tool-Bus.md) | I2C Tools (scanner, sniffer, sender), SPI Mem Manager (read/write/verify flash), Ethernet Troubleshooter |
| 04 | [Real-World Scenarios](04-Scenari-Reali.md) | Hardware hacking scenarios: IoT firmware extraction, I2C EEPROM cloning, SPI flash dump, SWD exploitation, UART console |
| 06 | [Personal Experience](06-Esperienza-Personale.md) | Field notes, hardware hacking mistakes, quick reference appendix |

---

## Quick Reference - Tools and Interfaces

| Tool | Interface | Function | Typical Target |
|------|-----------|----------|----------------|
| SWD Probe | SWD (2 pin) | Debug, firmware extraction | ARM Cortex-M |
| DAP Link | SWD/JTAG | GDB debugging | Generic ARM |
| AVR Flasher | ISP (6 pin) | Flash/fuse/EEPROM | ATmega, ATtiny |
| I2C Scanner | I2C (2 pin) | Device enumeration | Sensors, EEPROM |
| I2C Sniffer | I2C (2 pin) | Bus monitoring | Any I2C |
| SPI Mem Manager | SPI (4 pin) | Flash read/write | 25-series flash |

## Quick Reference - Debug Pinout

```
Flipper GPIO    SWD Target       I2C Target       SPI Target
PA14 (SWCLK) → SWCLK           PA7 (MOSI)     → MOSI
PA13 (SWDIO) → SWDIO           PA6 (MISO)     → MISO
GND           → GND             PB3 (SCK)      → SCK
3.3V          → VCC (opt.)     PA4 (CS)       → CS
                                PC0 (SDA)      → SDA
                                PC1 (SCL)      → SCL
```

> **Personal note:** The Flipper as a hardware hacking tool is underrated. It doesn't replace a J-Link or a Bus Pirate, but for quick field operations (I2C EEPROM dump, SPI flash read, SWD check) it's unbeatable for portability. I extracted firmware from 3 different IoT devices using only the Flipper during an engagement.
