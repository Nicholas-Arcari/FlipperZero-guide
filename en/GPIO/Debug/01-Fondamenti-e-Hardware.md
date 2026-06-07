## 1. Fundamentals -- The Flipper Zero as a Hardware Hacking Tool

### Why hardware debugging is fundamental

Every embedded device -- routers, IP cameras, smart locks, automotive ECUs, industrial PLCs -- at the end of the day is a microcontroller with firmware running on top. That firmware contains the business logic, cryptographic keys, hardcoded credentials, and vulnerabilities. To access it, you need physical interfaces.

The Flipper Zero, thanks to its GPIO pins and open-source firmware, becomes a Swiss army knife for hardware debugging. It doesn't replace a J-Link or a bench-mounted Saleae Logic, but it's something you carry in your pocket, that runs on battery, and that makes a real difference during a field assessment.

### The entry points of hardware reverse engineering

Every PCB you analyze during a hardware pentest potentially has these exposed interfaces:

**SWD (Serial Wire Debug)**
- ARM 2-wire protocol (SWCLK + SWDIO)
- Direct CPU access: halt, resume, memory read/write, flash
- THE most important protocol for pentesting ARM Cortex-M devices
- Present on virtually every ARM MCU in production
- Often left exposed even on final products

**JTAG (Joint Test Action Group)**
- IEEE 1149.1 standard protocol
- 4-5 wires: TCK, TMS, TDI, TDO (+ optional TRST)
- More complex than SWD but more versatile
- Used on more powerful processors (Cortex-A, MIPS, RISC-V)
- Allows boundary scan to test every pin on the chip

**UART (Universal Asynchronous Receiver/Transmitter)**
- 2-wire asynchronous serial (TX + RX)
- The FIRST thing to look for on any PCB
- Often connected to the boot console (U-Boot, Linux shell)
- Common baud rates: 9600, 19200, 38400, 57600, 115200
- If you find a root shell on UART, game over

**SPI (Serial Peripheral Interface)**
- Synchronous bus: MOSI, MISO, SCK, CS
- Used for external flash memories (firmware storage)
- The most widely used technique for extracting firmware from devices
- SOIC-8 clip for reading without desoldering

**I2C (Inter-Integrated Circuit)**
- 2-wire bus: SDA + SCL
- Connection between MCU and peripherals (sensors, EEPROM, RTC, display)
- Bus scan to find "hidden" devices
- Access to EEPROMs with configurations and sensitive data

### Why the Flipper Zero is different from other tools

| Feature | Flipper Zero | J-Link EDU | Bus Pirate | Multimeter |
|---|---|---|---|---|
| Portable (battery) | Yes | No | No | Yes |
| SWD Probe | Yes | Yes | No | No |
| SPI Flash Reader | Yes | No | Yes | No |
| I2C Scanner | Yes | No | Yes | No |
| Integrated display | Yes | No | No | Yes |
| Cost | ~170 EUR | ~60 EUR | ~35 EUR | Variable |
| Open Source FW | Yes | No | Yes | No |

The point is not that the Flipper is the absolute best at every single function. The point is that it has ALL of them in a pocket-sized device, with battery, display, and firmware you can modify.

### Basic hardware setup

Flipper Zero GPIO pins used for debugging:

```
Pin  | Function        | Suggested color
-----|-----------------|------------------
 2   | SWCLK / SCK     | Yellow
 3   | SWDIO / MOSI    | Green
 4   | MISO            | Blue
 5   | CS (Chip Select)| White
 6   | SDA (I2C)       | Green
 7   | SCL (I2C)       | Yellow
 8   | GND             | Black
 9   | 3.3V Out        | Red
 11  | TX (UART)       | Orange
 13  | RX (UART)       | Brown
```

> Personal note: before connecting anything, ALWAYS verify the target's operating voltage. The Flipper works at 3.3V. If the target is at 5V, you risk burning the GPIO port. A level shifter costing a few euros can save your device. I once burned a pin on a Flipper by connecting it to a 5V AVR without thinking -- a beginner mistake I won't repeat.

### Operational philosophy

When you're facing a device to analyze, always follow this order:

1. **Visual inspection** -- Look for unpopulated headers, test pads, silkscreen with labels like "UART", "DBG", "JTAG", "SWD", "J1"
2. **UART scan** -- Search for TX with an oscilloscope or logic analyzer (or even just a multimeter in AC mode)
3. **I2C scan** -- Connect SDA/SCL and scan the bus to find devices
4. **SWD/JTAG probe** -- Try to connect to the main MCU
5. **SPI dump** -- If there's an external flash, dump the firmware
6. **Firmware analysis** -- binwalk, Ghidra, strings, entropy analysis

---
