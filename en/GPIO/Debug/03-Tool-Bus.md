## 4. AVR Flasher

### ISP programming of AVR microcontrollers

The AVR family (ATmega, ATtiny) from Microchip (formerly Atmel) is still ubiquitous in Arduino projects, legacy devices, and many industrial products. The Flipper Zero supports ISP (In-System Programming), the standard method for flashing AVR MCUs.

### The ISP protocol

ISP uses the SPI interface to communicate with the AVR MCU:

```
Flipper Zero          Target AVR
-----------          ----------
Pin 2 (SCK)    -->  SCK  (Pin 19 on ATmega328P)
Pin 3 (MOSI)   -->  MOSI (Pin 17)
Pin 4 (MISO)   <--  MISO (Pin 18)
Pin 5 (CS)     -->  RESET (Pin 1)
Pin 8 (GND)    -->  GND
Pin 9 (3.3V)   -->  VCC (ONLY if target is 3.3V!)
```

> WARNING: Many AVRs operate at 5V. The Flipper works at 3.3V. When programming an ATmega328P powered at 5V, the MISO response logic levels will be at 5V and can damage the Flipper's GPIO. Solutions:
> - Power the AVR at 3.3V if the project allows it
> - Use a bidirectional level shifter
> - Use a voltage divider on the MISO line (resistive, cheap)

### Fuse bits -- The critical AVR configuration

Fuse bits are non-volatile configuration registers that control the fundamental behavior of the MCU. They are written once (but rewritable) and an error can "brick" the chip.

**ATmega328P -- Fuse bits:**

| Fuse | Bits | Function |
|------|------|----------|
| Low Fuse (lfuse) | 8 bit | Clock source, startup time, clock divider |
| High Fuse (hfuse) | 8 bit | Bootloader, EESAVE, watchdog, SPI enable, reset |
| Extended Fuse (efuse) | 3 bit | Brown-out detection level |

**Common values:**

```
Configuration           | lfuse | hfuse | efuse
------------------------|-------|-------|------
Arduino Uno default     | 0xFF  | 0xDE  | 0xFD
Internal clock 8 MHz    | 0xE2  | 0xD9  | 0xFF
External clock 16 MHz   | 0xFF  | 0xD9  | 0xFF
Internal clock no div8  | 0x62  | 0xDF  | 0xFF
```

**Critical bit -- SPIEN (hfuse bit 5):**
If you disable SPIEN (SPI Enable), you won't be able to program the chip via ISP anymore. You'll need a High Voltage programmer (HVPP) to recover. The Flipper does NOT support HVPP.

**Critical bit -- RSTDISBL (hfuse bit 7):**
Disables the reset pin, freeing it as an additional GPIO. But without a reset pin, ISP no longer works. Here too you need HVPP to recover.

### Lock bits -- Code protection

Lock bits protect the firmware from unauthorized reading/writing:

| Mode | LB2 | LB1 | Description |
|------|-----|-----|-------------|
| 1 | 1 | 1 | No protection |
| 2 | 1 | 0 | Flash/EEPROM write disabled |
| 3 | 0 | 0 | Read and write disabled |

In pentesting: if the lock bits are in mode 3, you can't read the firmware via ISP. However, a chip erase resets the lock bits (and erases everything). If you don't need the original firmware but want to reprogram the chip, this is sufficient.

> Personal note: unlike ARM chips with multi-level readout protection, AVRs with lock bits in mode 3 are effectively protected from ISP reading. There are no known glitch attacks to bypass them without erase. If you find an AVR with activated lock bits and you need the firmware, the options are: SPI/I2C bus analysis of peripherals, data flow interception during normal operation, or side-channel attacks (very advanced).

### Procedure -- Flash ATmega328P

1. **ISP connection** (see pinout above)
2. **On the Flipper:** GPIO -> Debug -> AVR Flasher
3. **Chip detection:**
   - The Flipper reads the chip's signature
   - ATmega328P: signature 0x1E 0x95 0x0F
   - If the signature is 0x00 0x00 0x00: wrong wiring or chip not powered
   - If the signature is 0xFF 0xFF 0xFF: clock not configured or chip in abnormal state
4. **Backup BEFORE any modifications:**
   - Read flash (32 KB for ATmega328P)
   - Read EEPROM (1 KB)
   - Read fuse bits (low, high, extended)
   - Save everything to SD card
5. **Programming:**
   - Load the .hex file from the SD card
   - Flash -> Verify -> Written data is re-read and compared
6. **Setting fuse bits:**
   - Set only if you know what you're doing
   - Verify each bit with the datasheet open
   - A wrong fuse can make the chip unreachable via ISP

### Procedure -- Flash ATtiny85

The ATtiny85 is popular for miniaturized projects (Digispark, USB HID attack tool):

```
ATtiny85 Pinout (DIP-8):
         +---v---+
 RESET  1|       |8  VCC
 PB3    2|       |7  PB2 (SCK)
 PB4    3|       |6  PB1 (MOSI)
 GND    4|       |5  PB0 (MISO)
         +-------+
```

Connection to the Flipper:
```
Flipper Pin 2 (SCK)   --> ATtiny85 Pin 7 (PB2/SCK)
Flipper Pin 3 (MOSI)  --> ATtiny85 Pin 6 (PB1/MOSI)
Flipper Pin 4 (MISO)  --> ATtiny85 Pin 5 (PB0/MISO)
Flipper Pin 5 (CS)    --> ATtiny85 Pin 1 (RESET)
Flipper Pin 8 (GND)   --> ATtiny85 Pin 4 (GND)
```

**ATtiny85 Signature:** 0x1E 0x93 0x0B

**ATtiny85 fuse defaults:**
- lfuse: 0x62 (internal clock 8 MHz with /8 divider = 1 MHz)
- hfuse: 0xDF
- efuse: 0xFF

For 8 MHz clock without divider: lfuse = 0xE2

**ATtiny85 EEPROM:**
- 512 bytes of EEPROM
- Often used to store configurations, keys, parameters
- Reading the EEPROM during an assessment can reveal interesting data

> Personal note: the ATtiny85 is the chip I encounter most often in DIY "Rubber Ducky" devices (Digispark). Many USB HID attack scripts are loaded onto these chips and left around as physical attacks. Being able to read and analyze the firmware of an ATtiny85 found plugged into a USB port is a fundamental skill for incident response.

### Other supported AVR MCUs

| Chip | Flash | EEPROM | Signature | Notes |
|------|-------|--------|-----------|-------|
| ATmega328P | 32 KB | 1 KB | 1E 95 0F | Arduino Uno |
| ATmega328PB | 32 KB | 1 KB | 1E 95 16 | Improved variant |
| ATmega32U4 | 32 KB | 1 KB | 1E 95 87 | Arduino Leonardo, Pro Micro |
| ATtiny85 | 8 KB | 512 B | 1E 93 0B | Digispark |
| ATtiny84 | 8 KB | 512 B | 1E 93 0C | Miniaturized projects |
| ATtiny13A | 1 KB | 64 B | 1E 90 07 | Ultra-cheap |
| ATmega2560 | 256 KB | 4 KB | 1E 98 01 | Arduino Mega |

---

## 5. I2C Tools

### The I2C bus in the hardware pentest context

I2C (Inter-Integrated Circuit, pronounced "I-squared-C") is the most widely used bus for communication between microcontroller and peripherals on the same PCB. Almost every embedded device has at least one I2C bus with something interesting on it.

### Bus architecture

```
         VCC (3.3V or 5V)
          |        |
         [R]      [R]     R = Pull-up resistors (typically 4.7K)
          |        |
SDA ------+--------+------[MCU]------[EEPROM]------[Sensor]------[RTC]
SCL ------+--------+------[MCU]------[EEPROM]------[Sensor]------[RTC]
          |
         GND
```

**Characteristics:**
- Multi-master, multi-slave bus
- Each device has a 7-bit address (0x00-0x7F) or 10-bit
- Speed: 100 kHz (Standard), 400 kHz (Fast), 1 MHz (Fast Mode+)
- Two wires: SDA (data), SCL (clock)
- Pull-up resistors required on both lines

### I2C Scan -- Finding devices on the bus

The I2C scan is the first step for exploring an unknown PCB. The Flipper sends a start byte to every possible address and checks if anyone responds with an ACK.

**Procedure:**

1. Connect SDA, SCL, GND to the Flipper
2. GPIO -> Debug -> I2C Tools -> Scan
3. The Flipper scans addresses from 0x01 to 0x7F
4. Responding addresses are listed

**Common addresses and what they mean:**

```
Address    | Typical device
-----------|-----------------------------------
0x20-0x27  | PCF8574 (I/O expander)
0x38-0x3F  | PCF8574A (I/O expander)
0x3C-0x3D  | SSD1306 (OLED display)
0x40       | HDC1080 (humidity sensor)
0x44       | SHT30/SHT31 (temp/humidity sensor)
0x48-0x4F  | ADS1115 (ADC), TMP102 (temp)
0x50-0x57  | AT24Cxx (EEPROM) <- VERY INTERESTING
0x68       | DS3231 (RTC), MPU6050 (IMU)
0x69       | MPU6050 (alternate address)
0x76       | BME280/BMP280 (environmental sensor)
0x77       | BME280 (alternate address)
```

> CRUCIAL: address 0x50-0x57 is almost always an EEPROM. EEPROMs contain configurations, keys, credentials, certificates, calibration parameters. If you find a device at 0x50 during an assessment, dump it immediately.

### Register reading and writing

Every I2C device has an internal register map. To read a register:

1. Send device address + W (Write) bit
2. Send the register address to read
3. Repeated Start
4. Send device address + R (Read) bit
5. Read the response byte

The Flipper simplifies all of this: you select address, register, and read/write.

**Example -- Reading WHO_AM_I of a BME280 (address 0x76):**

- Register 0xD0 (Chip ID)
- Expected value: 0x60 (BME280) or 0x58 (BMP280)
- If the value doesn't match: the chip might be a clone or a different device

**Example -- Reading registers of an MPU6050 (address 0x68):**

- Register 0x75 (WHO_AM_I): expected value 0x68
- Registers 0x3B-0x48: raw accelerometer and gyroscope data
- Register 0x6B (PWR_MGMT_1): power configuration

### I2C EEPROM dump

AT24Cxx series I2C EEPROMs are the most valuable target on an I2C bus:

| Chip | Capacity | Page addresses | Base I2C address |
|------|----------|----------------|------------------|
| AT24C01 | 128 bytes | 8 bit | 0x50 |
| AT24C02 | 256 bytes | 8 bit | 0x50 |
| AT24C04 | 512 bytes | 8 bit | 0x50-0x51 |
| AT24C08 | 1 KB | 8 bit | 0x50-0x53 |
| AT24C16 | 2 KB | 8 bit | 0x50-0x57 |
| AT24C32 | 4 KB | 16 bit | 0x50 |
| AT24C64 | 8 KB | 16 bit | 0x50 |
| AT24C128 | 16 KB | 16 bit | 0x50 |
| AT24C256 | 32 KB | 16 bit | 0x50 |
| AT24C512 | 64 KB | 16 bit | 0x50 |

**Dump procedure:**

1. Identify the chip (read the first bytes to determine the size)
2. Read sequentially from address 0x0000 to the maximum size
3. Save the dump to the SD card
4. Analyze with a hex editor (HxD, xxd, hexdump)

**What to look for in an EEPROM dump:**
- Readable ASCII strings (credentials, URLs, names)
- MAC addresses
- AES/DES keys (high-entropy byte sequences, length 16/24/32 bytes)
- X.509 certificates (start with 0x30 0x82)
- Configuration structures (often in the first bytes)
- Serial numbers, firmware versions, calibration parameters

### I2C sensor debugging

When an I2C sensor isn't working correctly, the Flipper can help diagnose:

**Common problems:**

| Symptom | Probable cause | Verification |
|---------|---------------|--------------|
| No ACK | Wrong address, wiring, dead chip | Scan, check pull-ups |
| Read always 0x00 | Sensor in sleep/reset | Write wakeup register |
| Read always 0xFF | Floating bus, missing pull-ups | Check pull-up resistors |
| Unstable data | Interference, cables too long, clock too high | Reduce speed, shorten cables |
| ACK but wrong data | Wrong register configuration | Compare with datasheet |

**Diagnostic procedure:**

1. I2C Scan -- verify the device responds
2. Read ID/WHO_AM_I register -- confirm the chip type
3. Read status registers -- check if the sensor is in an error state
4. Read configuration registers -- compare with expected values
5. Write correct configuration -- modify registers if necessary
6. Read data registers -- verify values are plausible

> Personal note: the I2C scan is the first thing I do when opening an unknown device. It's fast (a few seconds), non-invasive, and immediately gives you a picture of what's on the PCB. I once found an undocumented EEPROM on a home automation controller that contained WiFi passwords in the clear. The manufacturer had forgotten to remove the configuration EEPROM from the production version.

---

## 6. SPI Mem Manager

### SPI dump -- The most widely used technique for extracting firmware

The majority of embedded devices with more powerful processors (routers, IP cameras, NAS, smart TVs) use external SPI flash memories to store firmware. These memories are chips separate from the CPU, connected via SPI bus, and almost always directly readable with an SOIC-8 clip without needing to interface with the CPU.

This is why SPI dump is the most widely used and most reliable technique for extracting firmware.

### The SPI bus

```
Flipper Zero          Flash SPI
-----------          ---------
Pin 2 (SCK)    -->  CLK    (Pin 6)
Pin 3 (MOSI)   -->  DI     (Pin 5)
Pin 4 (MISO)   <--  DO     (Pin 2)
Pin 5 (CS)     -->  CS#    (Pin 1)
Pin 8 (GND)    -->  GND    (Pin 4)
Pin 9 (3.3V)   -->  VCC    (Pin 8)
```

**SPI SOIC-8 chip pinout (standard):**

```
        +---v---+
 CS#   1|       |8  VCC
 DO    2|       |7  HOLD#
 WP#   3|       |6  CLK
 GND   4|       |5  DI
        +-------+
```

### The SOIC-8 clip -- Avoiding desoldering

The SOIC-8 clip (Pomona 5250 or cheap equivalents) is the tool that makes the difference between a clean operation and a mess. It clamps directly onto the chip on the PCB without having to desolder it.

**Procedure with SOIC-8 clip:**

1. **Identify the flash chip on the PCB**
   - Look for SOIC-8 chips near the main CPU
   - Typical silkscreen: W25Q32, W25Q64, MX25L128, AT25SF041
   - If there's no silkscreen, look for the SOIC-8 package and verify with a multimeter

2. **Connect the clip**
   - Align pin 1 of the clip with pin 1 of the chip (dot/notch on the corner)
   - Press firmly -- the contact must be solid
   - The clip must be perfectly aligned, even half a millimeter offset causes erroneous reads

3. **Power management**
   - IMPORTANT: if the PCB is powered, the CPU might contend for the SPI bus
   - Option A: PCB off, power from Flipper (3.3V pin 9) -- preferred
   - Option B: PCB on, hold the CPU in reset to avoid bus contention
   - Option C: PCB on, hope the CPU doesn't interfere -- not recommended

> WARNING: Flipper's pin 9 provides 3.3V but with limited current. For flash chips that require more current during write operations, you might need external power. For reading only, the Flipper is generally sufficient.

### JEDEC ID -- Automatic chip identification

Every SPI flash memory has a unique JEDEC ID that identifies manufacturer, type, and capacity:

```bash
# The Flipper automatically reads the JEDEC ID
# Format: Manufacturer ID + Memory Type + Capacity

Manufacturer ID  | Manufacturer
-----------------|------------
0xEF             | Winbond
0xC2             | Macronix (MXIC)
0xC8             | GigaDevice
0x1F             | Adesto (ex Atmel)
0x20             | Micron/Numonyx
0x01             | Spansion/Cypress
0xBF             | SST/Microchip
```

**Common SPI flash chips in the IoT world:**

| Chip | JEDEC ID | Capacity | Sector | Page | Typical use |
|------|----------|----------|--------|------|-------------|
| W25Q16 | EF 40 15 | 2 MB | 4 KB | 256 B | Cheap IoT |
| W25Q32 | EF 40 16 | 4 MB | 4 KB | 256 B | Low-end routers |
| W25Q64 | EF 40 17 | 8 MB | 4 KB | 256 B | Routers, cameras |
| W25Q128 | EF 40 18 | 16 MB | 4 KB | 256 B | Advanced routers |
| W25Q256 | EF 40 19 | 32 MB | 4 KB | 256 B | NAS, smart TVs |
| MX25L6406E | C2 20 17 | 8 MB | 4 KB | 256 B | Macronix devices |
| MX25L12835F | C2 20 18 | 16 MB | 4 KB | 256 B | TP-Link routers |
| GD25Q64 | C8 40 17 | 8 MB | 4 KB | 256 B | Winbond clone |
| AT25SF041 | 1F 84 01 | 512 KB | 4 KB | 256 B | Ultra-cheap IoT |

### Complete dump procedure

**Step 1 -- Connection and identification:**

1. On the Flipper: GPIO -> Debug -> SPI Mem Manager
2. The Flipper reads the JEDEC ID
3. If the chip is in the database, it shows name and capacity
4. If not recognized, it shows the raw JEDEC ID -- look it up manually in the datasheet

**Step 2 -- Full read (dump):**

1. Select "Read"
2. The Flipper reads the entire chip sequentially
3. Estimated time:
   - 2 MB (W25Q16): ~30 seconds
   - 8 MB (W25Q64): ~2 minutes
   - 16 MB (W25Q128): ~4 minutes
   - 32 MB (W25Q256): ~8 minutes
4. The dump is saved to the SD card as a .bin file

**Step 3 -- Integrity verification:**

1. Select "Verify" or do a second dump
2. Compare the two dumps (CRC or byte-by-byte)
3. If they differ: unstable clip contact, interference, or bus contention
4. Repeat until you have two identical dumps

**Step 4 -- Dump analysis:**

```bash
# Basic information
file firmware.bin
hexdump -C firmware.bin | head -50

# Search for filesystems and components
binwalk firmware.bin

# Typical router firmware output:
# DECIMAL       HEXADECIMAL     DESCRIPTION
# 0             0x0             uImage header, header size: 64 bytes
# 64            0x40            LZMA compressed data
# 1048576       0x100000        Squashfs filesystem, little endian

# Extraction
binwalk -e firmware.bin

# Search for strings
strings -n 8 firmware.bin | grep -i password
strings -n 8 firmware.bin | grep -i admin
strings -n 8 firmware.bin | grep -i key
strings -n 8 firmware.bin | grep -i secret

# Entropy analysis (to find encrypted/compressed sections)
binwalk -E firmware.bin
```

### Write operations

In addition to dumping (reading), SPI Mem Manager supports:

**Full write:**
- Load a .bin file from the SD card
- The Flipper writes page by page (256 bytes at a time)
- Automatic verification after writing

**Erase:**
- Sector Erase: erases a 4 KB sector
- Block Erase (32 KB or 64 KB): erases a block
- Chip Erase: erases the entire chip (required before rewriting)

**Typical workflow for modifying firmware:**

1. Original dump (save as backup!)
2. Analysis and modification of the dump on the PC
3. Chip Erase on the target
4. Write the modified firmware
5. CRC verification
6. Functional test of the device

> Personal note: the SPI dump is the technique I use in 70% of my hardware assessments. It's reliable, doesn't require interaction with the target's CPU, and works even when SWD/JTAG are protected. The most important advice: ALWAYS do a second dump and compare it with the first. An SOIC-8 clip with imperfect contact produces corrupted but plausible dumps -- you might not notice the error until you try to analyze the firmware and find nonsensical data. Two identical dumps = reliable dump.

### Common problems and solutions

| Problem | Cause | Solution |
|---------|-------|----------|
| JEDEC ID = 0x000000 | No contact | Verify clip, wiring |
| JEDEC ID = 0xFFFFFF | Floating bus, CS not active | Check CS, verify pull-ups |
| Dump all 0xFF | Empty chip or failed read | Verify power, redo dump |
| Different dumps each time | Unstable contact | Clean pads, realign clip |
| Slow read/timeout | Clock too high | Reduce SPI speed |
| Chip not recognized | JEDEC ID not in DB | Add manually with datasheet |
| Bus contention with CPU | CPU active on SPI bus | Hold CPU in reset or disconnect |

---

## 7. Ethernet Troubleshooter

### Network diagnostics via USB-Ethernet adapter

The Ethernet Troubleshooter is a complementary tool that uses a USB-Ethernet adapter connected to the Flipper Zero's USB-C port for diagnosing network problems at the physical and link level.

### Features

**Link detection:**
- Link status (up/down)
- Negotiated speed (10/100/1000 Mbps)
- Duplex mode (half/full)
- Auto-negotiation status

**Cable diagnostics:**
- Pair continuity verification
- Cross-over detection
- Identification of broken or shorted pairs
- Cable length estimation (TDR - Time Domain Reflectometry, if supported by the adapter)

**Connectivity tests:**
- Ping (ICMP echo)
- DHCP verification (IP address request)
- Gateway detection
- DNS server reachability test

**PHY analysis:**
- PHY register reading
- Error statistics (CRC errors, frame errors, collisions)
- Auto-negotiation status
- Link partner capabilities

### When to use it in pentesting

The Ethernet Troubleshooter is useful in specific scenarios:

1. **Verification of suspicious network ports**
   - You find an Ethernet port on a device (e.g., industrial control panel)
   - You want to verify if it's active and which network it's connected to
   - The Flipper can verify link, obtain DHCP, and ping

2. **Quick diagnostics in ICS/SCADA environments**
   - Verify connectivity between PLC and HMI
   - Cable testing in industrial environments
   - Physical link parameter checking

3. **Network segmentation verification**
   - Connect to a port and verify which VLAN/subnet is assigned
   - Test whether segmentation is actually implemented

**Supported USB-Ethernet adapters:**
- ASIX AX88179 chip (USB 3.0, Gigabit)
- Realtek RTL8152B chip (USB 2.0, 100 Mbps)
- Verify compatibility with the firmware in use

> Personal note: the Ethernet Troubleshooter isn't the most used tool in the Debug toolkit, but it's saved a few situations. During an assessment of an industrial network, I used the Flipper to quickly verify which ports of a rack cabinet were active and in which VLAN, without having to bring a full laptop. It doesn't replace a professional network tool, but for a quick field check it's perfect.

---
