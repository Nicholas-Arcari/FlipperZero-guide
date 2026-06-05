# GPIO - Advanced Operational Guide

The GPIO (General Purpose Input/Output) of the Flipper Zero transforms the device into a complete hardware hacking platform. Through the GPIO pins, the Flipper communicates with external modules (ESP32, ESP8266, NRF24), sensors, debug buses (SWD/JTAG/UART/SPI/I2C), and custom peripherals.

This guide covers the hardware pin architecture, communication protocols, applications of each sub-module, and operational hardware penetration testing scenarios.

---

## Table of Contents

1. [GPIO Hardware Architecture](#gpio-hardware-architecture)
2. [Full Pinout](#full-pinout)
3. [Communication Protocols](#communication-protocols)
4. [Sub-Modules - Operational Overview](#sub-modules--operational-overview)
5. [Hardware Hacking Scenarios](#hardware-hacking-scenarios)
6. [Operational Security](#operational-security)
7. [Personal Experience](#personal-experience)

---

## GPIO Hardware Architecture

### Technical Specifications

The Flipper Zero exposes **18 GPIO pins** on a header on the top of the device:

- **Logic voltage:** 3.3V (LVTTL)
- **5V tolerance:** some pins are 5V tolerant on input (verify for specific pin)
- **Maximum current per pin:** ~20 mA (source/sink)
- **Total GPIO current:** ~120 mA maximum
- **External power:** the 5V pin provides 5V directly from USB/battery (max ~400 mA)
- **3.3V power:** the 3V3 pin provides regulated 3.3V (max ~200 mA)

### Available Pins

```
Pin  | Name    | Primary Function       | Alternate Function
-----|---------|------------------------|---------------------
1    | 5V      | 5V Power               | Direct USB/battery output
2    | PA7     | GPIO / SPI MOSI        | ADC_IN7
3    | PA6     | GPIO / SPI MISO        | ADC_IN6
4    | PA4     | GPIO / SPI CS          | ADC_IN4, DAC1
5    | PB3     | GPIO / SPI SCK         |
6    | PB2     | GPIO / GDO0            |
7    | PC3     | GPIO / GDO2            | ADC_IN4
8    | GND     | Ground                 |
9    | 3V3     | 3.3V Power             | Internal regulator
10   | PA14    | GPIO / SWCLK           | SWD Debug
11   | PA13    | GPIO / SWDIO           | SWD Debug
12   | PB6     | GPIO / UART TX1        | I2C SCL
13   | PB7     | GPIO / UART RX1        | I2C SDA
14   | PC1     | GPIO                   | ADC_IN1 / Interrupt
15   | PC0     | GPIO                   | ADC_IN0
16   | PB14    | GPIO / UART TX (iButton)| 1-Wire
17   | PB15    | GPIO / UART RX (iButton)|
18   | GND     | Ground                 |
```

**HARDWARE WARNING:** Never connect voltages higher than 3.3V to non-5V-tolerant pins. Never short 5V to GND. Never exceed 20mA per pin. GPIO damage is irreversible.

> **Personal note:** I burned a GPIO pin by directly connecting a 5V relay without a level shifter. Pin PA7 stopped working. Since then I ALWAYS use a bidirectional level shifter for any 5V interface and a multimeter to verify voltages before connecting. The cost of a level shifter is 1 euro, the cost of a new Flipper is 170 euros.

---

## Communication Protocols

### UART (Universal Asynchronous Receiver-Transmitter)

The simplest and most fundamental serial protocol for hardware hacking:

- **Pins:** PB6 (TX) + PB7 (RX) + GND
- **Supported baud rates:** 110 - 115200+ (typically 9600 or 115200)
- **Format:** 8N1 (8 data bits, no parity, 1 stop bit) standard
- **Usage:** debug console, ESP32/ESP8266 communication, shell on embedded devices, bootloader access

**Why it's critical for pentesting:** UART is the first port a hardware hacker looks for on a target device. Many routers, IP cameras, and IoT devices have exposed UART pads on the PCB that give direct access to the boot console (U-Boot) or root shell.

### SPI (Serial Peripheral Interface)

High-speed synchronous protocol for flash memory and peripherals:

- **Pins:** PA7 (MOSI) + PA6 (MISO) + PB3 (SCK) + PA4 (CS) + GND
- **Clock:** up to ~8 MHz on the Flipper
- **Usage:** reading/writing SPI flash memory (W25Qxx, AT25xxx), firmware dump, programming

**Why it's critical:** SPI memories contain the firmware of embedded devices. Flash dump = firmware access = reverse engineering = vulnerability research.

### I2C (Inter-Integrated Circuit)

Multi-device bus for sensors and slow peripherals:

- **Pins:** PB6 (SCL) + PB7 (SDA) + GND (+ 4.7kOhm pull-up resistor)
- **Clock:** 100 kHz (standard) / 400 kHz (fast mode)
- **Addressing:** 7-bit (128 possible devices on the bus)
- **Usage:** sensors (temperature, humidity, pressure, gas), EEPROM, OLED display, RTC

### SWD (Serial Wire Debug)

ARM debug interface for Cortex-M microcontrollers:

- **Pins:** PA14 (SWCLK) + PA13 (SWDIO) + GND (+ optional reset)
- **Usage:** live debugging, firmware flash, CPU halt/resume, memory reading
- **Targets:** STM32, nRF52, RP2040, GD32, and any ARM Cortex-M

**Why it's critical:** SWD allows complete flash dump of a microcontroller -- firmware, cryptographic keys, configurations. It's the equivalent of having root access to the chip.

> **Personal note:** SWD is my favorite protocol for hardware hacking. I've extracted firmware from IP cameras, smart locks, IoT devices, and even from an alarm system by connecting to the SWD pads on the PCB. Manufacturers often leave the pads exposed (sometimes even with a soldered header!) and don't protect the flash with readout protection. A hardware pentest without an SWD probe is incomplete.

---

## Sub-Modules - Operational Overview

### ESP32 (`GPIO/ESP32/`)

The ESP32 transforms the Flipper into an offensive WiFi/BLE tool. Connected via UART, it enables:
- **WiFi Marauder:** deauth, beacon spam, sniffing, evil portal
- **Evil Portal:** captive portal with custom pages
- **Camera (ESP32-CAM):** remote visual surveillance
- **Wardriving:** WiFi network mapping with GPS
- **WiFi/BLE Scanner:** wireless reconnaissance

[Full details -> ESP32/README.md](ESP32/README.md)

### ESP8266 (`GPIO/ESP8266/`)

Budget WiFi module for deauthentication attacks and automation:
- **Deauther:** WiFi client disconnection (management frame attack)
- **WiFi Scanner:** 2.4 GHz network reconnaissance
- **IFTTT Button:** IoT automation

[Full details -> ESP8266/README.md](ESP8266/README.md)

### NRF24 (`GPIO/NRF24/`)

2.4 GHz transceiver for wireless peripheral attacks:
- **MouseJacker:** hijacking unencrypted wireless mice/keyboards
- **Sniffer:** 2.4 GHz packet capture
- **Jammer:** interference on specific channels

[Full details -> NRF24/README.md](NRF24/README.md)

### Debug (`GPIO/Debug/`)

Tools for direct hardware hacking:
- **SWD Probe / DAP Link:** ARM microcontroller debugging and flashing
- **AVR Flasher:** ATmega/ATtiny programming
- **I2C Tools:** I2C bus scanning and debugging
- **SPI Mem Manager:** SPI memory dump and flash
- **Ethernet Troubleshooter:** network diagnostics

[Full details -> Debug/README.md](Debug/README.md)

### Sensors (`GPIO/Sensors/`)

Environmental sensor suite for measurements and monitoring:
- Temperature, humidity, pressure (BME280, DHT22)
- Gas and air quality (MQ-series, SCD30)
- Distance (HC-SR04, VL53L0X)
- Radiation (Geiger counter)
- UV, light, particulate matter

[Full details -> Sensors/README.md](Sensors/README.md)

### Malveke (`GPIO/Malveke/`)

Multifunction addon with camera, printer, and testing tools.

[Full details -> Malveke/README.md](Malveke/README.md)

### Flipboard (`GPIO/Flipboard/`)

Prototyping board with LEDs and buttons for rapid I/O.

[Full details -> Flipboard/README.md](Flipboard/README.md)

### Games (`GPIO/Games/`)

Mini-games demonstrating UART and sensor usage (Pong via UART, Pong via ToF).

[Full details -> Games/README.md](Games/README.md)

### VGM (`GPIO/VGM/`)

Video Game Module -- gaming addon with motion sensors.

[Full details -> VGM/README.md](VGM/README.md)

### Other Components (`GPIO/Altre componenti/`)

GPS, RGB LED, air mouse, analog output, Sentry Safe, ColecoVision, and other standalone tools.

[Full details -> Altre componenti/README.md](Altre%20componenti/README.md)

---

## Hardware Hacking Scenarios

### Scenario 1 - Router Firmware Dump via SPI

**Objective:** extract router firmware for vulnerability analysis

1. Open the router and identify the SPI flash on the PCB (8-pin chip, typically W25Qxx)
2. Identify the pins: CS, MOSI, MISO, SCK, VCC, GND (from the chip datasheet)
3. Connect the Flipper to the SPI flash pins (with the router POWERED OFF)
4. Open SPI Mem Manager -> identify the chip (JEDEC ID)
5. Full flash dump -> .bin file
6. Analyze offline with binwalk, firmware-mod-kit, Ghidra

**Post-analysis:**
- Extract the filesystem (squashfs, jffs2, ubifs)
- Search for hardcoded credentials, private keys, configurations
- Identify vulnerable services
- Search for backdoors or hidden functionality

### Scenario 2 - SWD Debug of a Smart Lock

**Objective:** extract firmware from a BLE IoT lock

1. Open the lock and identify the microcontroller (typically nRF52 or STM32)
2. Locate the SWD pads (SWCLK, SWDIO, GND, Reset)
3. Connect the Flipper -> SWD Probe
4. Identify the target (IDCODE)
5. Check if readout protection (RDP) is active
6. If RDP = 0 (unprotected): full flash dump
7. Analyze the firmware with Ghidra: search for BLE keys, authentication algorithm, vulnerabilities

### Scenario 3 - UART Access on IP Camera

**Objective:** obtain root shell on an IP camera

1. Open the camera and locate the UART pads (TX, RX, GND)
2. Identify the baud rate (try 115200 first, then 9600)
3. Connect the Flipper: TX->RX, RX->TX, GND->GND
4. Open UART Terminal on the Flipper
5. Reboot the camera -> observe the boot output (U-Boot)
6. Interrupt the boot by pressing a key during the U-Boot countdown
7. From U-Boot: modify boot parameters to obtain root shell
8. Or: directly access the Linux shell if there's no password

### Scenario 4 - MouseJacker on Wireless Keyboard

**Objective:** demonstrate hijacking of an unencrypted wireless keyboard

1. Connect the NRF24L01+ module to the Flipper GPIO
2. Open MouseJacker -> Scanner
3. Identify the target keyboard's USB dongle (pipe address)
4. Start hijacking -> the Flipper impersonates the keyboard
5. Send arbitrary keystrokes to the target PC
6. Demo: type "This keyboard is not secure" on the victim's PC

---

## Operational Security

### Flipper Hardware Protection

- **Never connect 5V to 3.3V pins** -- burns the GPIO
- **Always use pull-up/pull-down resistors** -- floating signals cause unpredictable behavior
- **Level shifter for 5V** -- mandatory for 5V interfaces
- **Maximum current:** respect the limits (20mA/pin, 120mA total)
- **External power:** for high-current modules (ESP32 in TX), use external power

### Precautions in Hardware Pentesting

- **Photograph the PCB** before connecting anything
- **Identify voltages** with a multimeter before connecting the Flipper
- **Don't desolder components** without written authorization
- **Document every connection** made (photos + schematic)
- **Backup before writing:** always dump the flash BEFORE modifying it

---

## Personal Experience

> **Personal note -- The complete GPIO kit:** In my hardware pentest backpack I always keep: ESP32 module flashed with Marauder, NRF24L01+ module with antenna, Dupont jumper wires (M-M, M-F, F-F), bidirectional level shifter, SOIC-8 clip for SPI flash, pocket multimeter, magnifying glass. This kit covers 90% of hardware hacking scenarios in the field.

> **Personal note -- UART everywhere:** UART is the most common hardware vulnerability I find. Out of about 20 IoT devices tested in the past year, 15 had exposed UART pads and 12 of those gave access to a root shell without a password. Routers, IP cameras, smart speakers, NAS -- almost everything has an accessible UART.

> **Personal note -- SPI dump as standard:** SPI dumping has become a standard procedure in my hardware pentests. With the SOIC-8 clip you don't even need to desolder the chip -- just clip on and dump. The extracted firmware almost always reveals hardcoded credentials, private keys, or active debug configurations.

> **Personal note -- NRF24 and MouseJacker:** The MouseJacker attack is the most dramatic during demos. You connect the NRF24 to the Flipper, scan, find the CEO's wireless keyboard, and start typing messages on their screen. The impact on security awareness is immediate. Tip: use this attack in awareness sessions, not just in technical reports.
