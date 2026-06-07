## 8. Hardware Pentest Scenarios

### Scenario 1 -- Router firmware dump via SPI

**Objective:** Extract the complete firmware of a home router for vulnerability analysis.

**Target:** Generic TP-Link router with Winbond W25Q64 flash chip.

**Phase 1 -- Reconnaissance:**
1. Open the router case (4 screws under the rubber feet, as always)
2. Identify the main components on the PCB:
   - Main SoC (Mediatek, Qualcomm, Realtek)
   - RAM chip (DDR2/DDR3)
   - SPI flash chip (our target)
3. Photograph the PCB with good lighting -- you'll need the references
4. Identify the flash chip: SOIC-8, silkscreen "W25Q64FVSIG"
5. Verify the pinout from the Winbond datasheet

**Phase 2 -- Dump:**
1. Disconnect the router's power supply
2. Position the SOIC-8 clip on the flash chip
   - Pin 1 of the clip aligned with the dot on the chip
   - Verify with multimeter that the clip's GND is connected to the PCB's GND
3. Connect the clip to the Flipper Zero:
   - CS -> Pin 5
   - DO (MISO) -> Pin 4
   - DI (MOSI) -> Pin 3
   - CLK -> Pin 2
   - GND -> Pin 8
   - VCC -> Pin 9 (3.3V from Flipper)
4. Start SPI Mem Manager
5. The Flipper reads JEDEC ID: EF 40 17 -> Winbond W25Q64, 8 MB
6. Start full read: ~2 minutes
7. Save as `router_dump1.bin`
8. Repeat the dump: `router_dump2.bin`
9. Compare the two files: if identical, the dump is reliable

**Phase 3 -- Analysis:**
```bash
# Extract components
binwalk -e router_dump1.bin

# Typical router firmware structure:
# - Bootloader (U-Boot, ~256 KB)
# - Compressed Linux kernel (LZMA, ~1-2 MB)
# - Root filesystem (SquashFS, ~4-6 MB)
# - Configuration/ART (partition table, calibration, ~64 KB)

# Explore the extracted filesystem
ls _router_dump1.bin.extracted/squashfs-root/

# Search for credentials
grep -r "password" _router_dump1.bin.extracted/squashfs-root/etc/
cat _router_dump1.bin.extracted/squashfs-root/etc/shadow

# Search for SSH/SSL keys
find _router_dump1.bin.extracted/ -name "*.pem" -o -name "*.key"

# Search for interesting configurations
cat _router_dump1.bin.extracted/squashfs-root/etc/config/wireless
```

**What to look for:**
- Default passwords in /etc/shadow or /etc/passwd
- Hardcoded SSL/TLS keys
- Init scripts with credentials
- Backdoors or hidden services (telnetd on non-standard ports)
- Library versions with known CVEs (busybox, dnsmasq, uhttpd)

### Scenario 2 -- Root shell via UART on an IP camera

**Objective:** Obtain a root shell on an IP camera for security analysis.

**Target:** Generic IP camera based on HiSilicon/Ingenic SoC.

**Phase 1 -- Finding UART:**
1. Open the camera (careful: often delicate flat cables for the sensor)
2. Look for unpopulated 3-4 pin headers near the CPU
3. Use the multimeter:
   - One pin will be GND (continuity with ground plane)
   - One pin will be VCC (constant 3.3V)
   - One pin will be TX (voltage that varies, ~3.3V at idle)
   - One pin will be RX (constant 3.3V, pull-up)
4. Alternatively, use a logic analyzer or oscilloscope to identify TX from serial traffic during boot

**Phase 2 -- UART connection:**
1. Connect to the Flipper (or better, to a USB-UART adapter to have the console on the PC):
   - Camera TX -> Flipper/adapter RX
   - Camera RX -> Flipper/adapter TX
   - GND -> GND
2. Set the baud rate: try 115200 first (the most common)
3. If you see garbled characters, try: 9600, 19200, 38400, 57600

**Phase 3 -- Boot and interaction:**

Typical output during boot:
```
U-Boot 2016.11 (May 12 2021)
DRAM: 64 MiB
Loading kernel...
Starting kernel...
[    0.000000] Linux version 3.18.20
...
[    5.234567] Starting network...
Welcome to HiLinux
login:
```

**Possibilities:**
1. **Root shell without password:** many cheap cameras have `root:` without a password or with a known password (root, admin, xc3511, jvbzd)
2. **Interrupt U-Boot:** during boot, press a key within 1-3 seconds to enter the U-Boot console
3. **U-Boot console:** from here you can modify the kernel's boot parameters

```bash
# In the U-Boot console:
# Modify boot args to add a shell
setenv bootargs console=ttyS0,115200 init=/bin/sh
boot

# Now you have a root shell without login
# Mount the filesystem read-write
mount -o remount,rw /

# Change root password
passwd root

# Or add an SSH backdoor
```

**Phase 4 -- Post-exploitation:**
- Explore the filesystem for cloud credentials (RTSP, P2P, API)
- Search for encryption keys for the video stream
- Analyze running services (there are often manufacturer backdoors)
- Verify if the firmware is updateable and if the update is signed

### Scenario 3 -- Cryptographic key extraction via SWD on an IoT lock

**Objective:** Extract the BLE encryption keys used by a smart lock.

**Target:** Smart lock based on nRF52832 (Nordic Semiconductor).

**Phase 1 -- External analysis:**
1. The lock uses BLE to communicate with the smartphone app
2. Sniff the BLE traffic to understand the protocol (with another Flipper or Ubertooth)
3. The traffic is encrypted -- the keys are needed

**Phase 2 -- Physical access:**
1. Disassemble the lock (usually 2 screws + snap clips)
2. Identify the nRF52832 on the PCB
3. Look for SWD pads (often unpopulated test pads, sometimes hidden under stickers)
4. Connect SWCLK, SWDIO, GND to the Flipper

**Phase 3 -- SWD Probe:**
1. Start SWD Probe
2. The Flipper reads IDCODE: 0x0BC11477 -> nRF52832 confirmed
3. Check APPROTECT: if disabled (very common on cheap locks), proceed
4. Halt CPU
5. Complete dump:
   - Flash: 512 KB from 0x00000000
   - UICR: 256 bytes from 0x10001000
   - RAM: 64 KB from 0x20000000 (if the lock was powered on, RAM contains live data)

**Phase 4 -- Analysis:**
```bash
# Load the dump in Ghidra
# Target: ARM Cortex-M4 Little Endian
# Base address: 0x00000000
# The Nordic SoftDevice occupies the first ~148 KB

# Search for data structures related to keys
# BLE LTK (Long Term Key) keys are typically at 0x20000000+ in RAM
# Or in flash, in the bonding data section

# Search for known patterns
strings flash_dump.bin | grep -i "key"
strings flash_dump.bin | grep -i "pass"
strings flash_dump.bin | grep -i "pin"

# Analyze UICR for custom keys
hexdump -C uicr_dump.bin
```

**What to look for:**
- BLE bonding keys (LTK, IRK, CSRK)
- AES keys for payload encryption
- Hardcoded PIN/password
- User authorization tables
- Signing keys for OTA updates

> Personal note: cheap smart locks are among the most interesting targets for hardware pentesting. The business model pushes to cut costs on security: nRF52 without APPROTECT, keys in the clear in flash, fragile custom BLE protocols. During an assessment I found the hardcoded AES master keys in the flash of a lock that controlled access to an entire building. With those keys, you could open any lock of the same model, not just that specific unit. The manufacturer was using the same key for all devices in production.

### Scenario 4 -- Microcontroller reprogramming for security bypass

**Objective:** Bypass the authentication system of a device by modifying the firmware.

**Target:** Access system based on ATmega328P with RFID reader.

**Phase 1 -- Analysis:**
1. The device reads RFID badges and compares them against a whitelist in EEPROM
2. If the badge is on the list, it activates a relay that opens the door
3. Hypothesis: by modifying the EEPROM or firmware, we can bypass the check

**Phase 2 -- ISP access:**
1. Identify the ATmega328P on the reader's PCB
2. Look for the ISP header (6-pin standard: MOSI, MISO, SCK, RESET, VCC, GND)
3. Connect the Flipper in AVR Flasher mode

**Phase 3 -- Dump and analysis:**
1. Read the signature: 0x1E 0x95 0x0F -> ATmega328P confirmed
2. Check lock bits: if mode 1 (no protection), proceed
3. Dump flash (32 KB)
4. Dump EEPROM (1 KB)
5. Read fuse bits (backup)

**Phase 4 -- Firmware analysis:**
```bash
# Disassemble with avr-objdump
avr-objdump -D -m avr firmware.bin > firmware.asm

# Or load in Ghidra with the AVR8 processor
# Search for RFID comparison routines
# Typically: tag read -> compare with table in EEPROM -> decision

# Analyze EEPROM
hexdump -C eeprom.bin
# Search for RFID UID patterns (4 or 7 bytes, usually sequential)
```

**Phase 5 -- Modification:**

Option A -- Add your badge to the whitelist:
- Modify the EEPROM by adding your badge's UID to the table
- Flash only the modified EEPROM (doesn't touch the firmware)
- The device works normally but also accepts your badge

Option B -- Firmware patching:
- Find the comparison routine in the disassembly
- Modify the conditional branch that decides "access granted/denied"
- Typically: change a `BRNE` (Branch if Not Equal) to `NOP` or `BREQ`
- Flash the patched firmware
- Now any badge is accepted

Option C -- Replace the firmware:
- Write a custom firmware that always activates the relay
- More invasive but simpler to implement

> Personal note: the EEPROM scenario is the most elegant and the least detectable. The original firmware remains intact, the device works normally for all legitimate users, and your badge is simply added to the list. In a red team exercise, this approach went undetected for weeks because the system continued to function perfectly -- logs showed only authorized accesses.

---

## Cross-Reference - Multi-Vector Scenarios

| Scenario | Related Module | Link | How they connect |
|----------|---------------|------|------------------|
| Firmware dump + NFC | NFC | [05-Scenari-Reali](../../NFC/05-Scenari-Reali.md) | Dump NFC reader firmware via SWD to extract hardcoded MIFARE keys |
| EEPROM + RFID | RFID | [05-Scenari-Reali](../../RFID/05-Scenari-Reali.md) | Dump RFID reader EEPROM to extract authorized badge list |
| UART console + WiFi | WiFi-Marauder | [05-Scenari-Reali](../../WiFi-Marauder/05-Scenari-Reali.md) | UART console on router/AP -> WiFi credentials -> ESP32 for pivot |
| SPI flash + Sub-GHz | Sub-GHz | [05-Scenari-Reali](../../Sub-GHz/05-Scenari-Reali.md) | Dump SPI flash of RF receiver for rolling code key analysis |
| Debug + BadUSB | USB/Bad USB | [05-Scenari-Reali](../../USB/Bad%20USB/05-Scenari-Reali.md) | Extract firmware via debug -> analyze offline -> create targeted BadUSB payload |
