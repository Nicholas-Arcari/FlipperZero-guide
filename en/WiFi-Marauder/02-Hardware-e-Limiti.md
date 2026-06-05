## 2. Hardware - ESP32 WiFi Devboard

### 2.1 Fundamental Premise

**The Flipper Zero does NOT have built-in WiFi.**

This is the first concept that must be absolutely clear. The Flipper Zero is
a multi-tool device that includes:
- Sub-GHz transceiver (CC1101)
- NFC (ST25R3916)
- RFID 125 kHz
- Infrared
- GPIO
- Bluetooth (for communication with the mobile app)
- USB

But it does NOT include any WiFi chip. Everything related to WiFi -- scanning, sniffing,
attacks, analysis -- is performed by an external ESP32 module connected via GPIO.

The Flipper acts as a terminal / control interface, sending commands via UART
serial to the ESP32 module running the Marauder firmware.

### 2.2 ESP32-S2 WiFi Devboard (Official Flipper)

The official Flipper Devices board is based on the Espressif ESP32-S2 chip:

**ESP32-S2 technical specifications:**
- Processor: Xtensa LX7 single-core at 240 MHz
- RAM: 320 KB SRAM + 16 KB RTC SRAM
- Flash: 4 MB (depends on the module)
- WiFi: 802.11 b/g/n at 2.4 GHz
- USB interface: native USB-OTG (does not require an external UART bridge)
- GPIO: up to 43 programmable pins
- ADC: 2x SAR ADC at 13 bit

**Connection to the Flipper:**
- Connects via the GPIO connector on the top of the Flipper
- Power: 3.3V supplied by the Flipper through GPIO
- Communication: UART serial (TX/RX) through dedicated pins
- The devboard also has its own USB-C connector, used for flashing

**ESP32-S2 limitations:**
- 2.4 GHz only (does not support 5 GHz -- no analysis of 802.11a/ac/ax networks on 5 GHz)
- Single-core: limited performance in intensive operations
- Integrated antenna: limited range, typically 20-50 meters in optimal conditions
- Does not support native monitor mode like PC WiFi cards (Atheros, Ralink)
  but the Marauder firmware implements raw frame injection/capture via Espressif API

### 2.3 ESP32-S3 and Other Variants

Some alternative boards supported by the Marauder firmware:

**ESP32-S3:**
- Processor: Xtensa LX7 dual-core at 240 MHz (more powerful than the S2)
- WiFi + Bluetooth 5 (LE)
- More available RAM
- Better performance in high-speed packet capture

**ESP32-WROOM-32:**
- The classic original ESP32 (dual-core Xtensa LX6)
- Very widespread, broad community support
- Can be used with Marauder but requires manual UART pin wiring

**Note on antennas:**
To improve range, some boards have a U.FL/IPEX connector for an external
antenna. In a pentesting environment, a 5-9 dBi directional antenna can make
the difference between capturing and missing a handshake from a distant target.

> Personal note: the official Flipper devboard with ESP32-S2 works well for
> short-range work (same room / floor). For professional engagements where
> I need to operate from greater distances, I prefer using a laptop with an Alfa
> AWUS036ACH card and aircrack-ng/bettercap. The Flipper with Marauder is excellent for
> quick and discreet reconnaissance -- it fits in a pocket and is operational in 5 seconds.

### 2.4 Required Drivers

Depending on the operating system and the USB-UART chip on the board:

**Windows:**
- ESP32-S2 (official devboard): uses native USB-OTG, usually no additional
  driver is needed. If not recognized, install the ESP32-S2 driver from Espressif.
- ESP32 with CP2102/CP2104 chip: download the Silicon Labs CP210x driver
  (https://www.silabs.com/developers/usb-to-uart-bridge-vcp-drivers)
- ESP32 with CH340/CH341 chip: download the WCH CH340 driver
  (http://www.wch.cn/download/CH341SER_EXE.html)

**Linux:**
- Kernel 5.x+: cp210x and ch341 drivers already included in the kernel
- Verify with: `dmesg | grep -i ttyUSB` or `dmesg | grep -i ttyACM`
- You may need to add the user to the dialout group:
  `sudo usermod -aG dialout $USER` (logout/login to apply)

**macOS:**
- CP2102/CP2104: install the Silicon Labs driver
- CH340: install the CH340 driver, available via brew:
  `brew install --cask wch-ch34x-usb-serial-driver`
- Note: on macOS Ventura+ additional permissions may be required in
  System Preferences > Privacy & Security

---

## 3. Flashing the Marauder Firmware

### 3.1 Prerequisites

Before flashing:
1. Identify EXACTLY the model of your ESP32 (S2, S3, WROOM-32, etc.)
2. Download the correct firmware for that model -- wrong firmware = brick
   (recoverable, but annoying)
3. Have a working USB-C cable (not charge-only -- it must support data)

Reference repositories:
- Marauder firmware: https://github.com/justcallmekoko/ESP32Marauder
- Windows flasher: https://github.com/UberGuidoZ/Flipper/tree/main/Wifi_DevBoard/FZ_Marauder_Flasher
- Linux/macOS flasher: https://github.com/SkeletonMan03/FZEasyMarauderFlash

### 3.2 Method 1: Flash via Web Browser (Recommended for beginners)

This is the simplest method and uses the ESP Web Flasher directly from the browser.
It requires a Chromium-based browser (Chrome, Edge, Brave) for Web Serial API support.

**Detailed procedure:**

1. Disconnect the devboard from the Flipper (always flash with the devboard disconnected
   from the Flipper)

2. Connect the devboard to the PC via USB-C

3. Put the chip in boot mode:
   - ESP32-S2 official devboard: hold the BOOT button, press and
     release RESET, then release BOOT
   - If there are no physical buttons: connect GPIO0 to GND during power-on

4. Verify the device is recognized:
   - Windows: Device Manager -> COM Ports (a new port should appear)
   - Linux: `ls /dev/ttyACM*` or `ls /dev/ttyUSB*`
   - macOS: `ls /dev/cu.usbmodem*`

5. Open the FZEE Flasher or equivalent web tool in the browser

6. Select the correct board (e.g., "ESP32-S2" for the official devboard)

7. Select the Marauder firmware version (use the latest stable)

8. Click "Connect" -> select the device's serial port

9. Click "Program" and wait for completion

10. When finished: press RESET on the devboard (or unplug/replug USB)

11. Reconnect the devboard to the Flipper and verify functionality

**Advantages:**
- No software installation required
- Intuitive graphical interface
- Automatically selects the correct flash offsets

**Disadvantages:**
- Requires a Chromium browser (Firefox does not support Web Serial)
- Depends on an external web service
- Less control over flash parameters

### 3.3 Method 2: Manual ESP Web Flasher

This method offers more control and requires downloading the individual binary files.

**Procedure:**

1. Download the binary files from the Marauder release page on GitHub:
   - `bootloader.bin` -- second-stage bootloader
   - `partitions.bin` -- partition table
   - `boot_app0.bin` -- OTA boot selector
   - `esp32marauder_vX.X.X_BOARD.bin` -- main firmware (BOARD = your model)

2. Open https://espressif.github.io/esptool-js/ in the browser

3. Configure the flash offsets:

   For ESP32-S2:
   ```
   0x1000   -> bootloader.bin
   0x8000   -> partitions.bin
   0xe000   -> boot_app0.bin
   0x10000  -> esp32marauder_vX.X.X_flipper.bin
   ```

   For ESP32 (WROOM-32):
   ```
   0x1000   -> bootloader.bin
   0x8000   -> partitions.bin
   0xe000   -> boot_app0.bin
   0x10000  -> esp32marauder_vX.X.X_esp32.bin
   ```

4. Recommended baud rate: 921600 (faster) or 115200 (more reliable)

5. Flash mode: DIO (for most boards)

6. Click "Program" for each slot in the indicated order, or "Program All"

7. Reset the device when finished

> Personal note: this method has saved me multiple times when the automatic flasher
> gave unexplainable errors. Having direct control over the offsets and binary files
> allows you to diagnose problems like corrupted partitions or incompatible bootloaders.
> I recommend it to anyone who wants to truly understand what happens during the flash.

### 3.4 Method 3: Flash via esptool.py (Advanced / command line method)

For those who prefer the terminal and full control. This is the method I use
regularly.

**Installing esptool:**

```bash
pip install esptool
```

Or on systems with Python 3:

```bash
pip3 install esptool
```

**Identifying the serial port:**

```bash
# Linux
ls -la /dev/ttyACM* /dev/ttyUSB*

# macOS
ls /dev/cu.usbmodem* /dev/cu.SLAB*

# Windows (PowerShell)
Get-WMIObject Win32_SerialPort | Select-Object DeviceID, Description
```

**Erasing the flash (recommended before the first flash):**

```bash
esptool.py --chip esp32s2 --port /dev/ttyACM0 erase_flash
```

**Full flash (ESP32-S2):**

```bash
esptool.py --chip esp32s2 \
    --port /dev/ttyACM0 \
    --baud 921600 \
    --before default_reset \
    --after hard_reset \
    write_flash \
    -z \
    --flash_mode dio \
    --flash_freq 80m \
    --flash_size 4MB \
    0x1000 bootloader.bin \
    0x8000 partitions.bin \
    0xe000 boot_app0.bin \
    0x10000 esp32marauder_vX.X.X_flipper.bin
```

**Full flash (ESP32 WROOM-32):**

```bash
esptool.py --chip esp32 \
    --port /dev/ttyUSB0 \
    --baud 921600 \
    write_flash \
    -z \
    --flash_mode dio \
    --flash_freq 40m \
    --flash_size 4MB \
    0x1000 bootloader.bin \
    0x8000 partitions.bin \
    0xe000 boot_app0.bin \
    0x10000 esp32marauder_vX.X.X_esp32.bin
```

**Flash verification:**

```bash
esptool.py --chip esp32s2 --port /dev/ttyACM0 verify_flash \
    0x10000 esp32marauder_vX.X.X_flipper.bin
```

**Reading chip information:**

```bash
esptool.py --chip esp32s2 --port /dev/ttyACM0 chip_id
esptool.py --chip esp32s2 --port /dev/ttyACM0 flash_id
```

**Common issues with esptool:**

| Problem | Solution |
|----------|-----------|
| "Failed to connect" | Enter boot mode (BOOT + RESET), verify USB cable |
| "Invalid head of packet" | Reduce baud rate to 115200 |
| "Permission denied" on Linux | `sudo chmod 666 /dev/ttyACM0` or add user to dialout |
| "A fatal error occurred" | Verify correct chip (esp32 vs esp32s2 vs esp32s3) |
| Flash completes but does not work | Verify correct offsets for your chip |
| Timeout during write | Faulty or too-long USB cable, try a different cable |

> Personal note: I always use esptool from the terminal. It is the most reliable and
> repeatable method. I have a bash script that automates the entire process: downloads the
> latest firmware from GitHub, erases the flash, and programs everything with a single command.
> In a pentesting environment, where you might need to quickly reflash in the field,
> having the script ready is essential.

---

## 4. Flipper Zero Configuration

### 4.1 Connecting the Devboard

1. **Turn off the Flipper Zero** before connecting the devboard (good practice to
   avoid damage to the GPIO pins)

2. Align the devboard pins with the GPIO connector on the top of the
   Flipper. The official devboard has a connector that inserts in a single orientation.

3. Press firmly but without forcing. The devboard must be securely seated.

4. Turn on the Flipper Zero.

5. Verify that the devboard is powered (status LED, if present).

### 4.2 Accessing the WiFi Marauder App

The path varies depending on the firmware installed on the Flipper:

**Official firmware with app pack:**
```
Apps -> GPIO -> [ESP32] WiFi Marauder
```

**Momentum firmware (formerly Xtreme):**
```
Apps -> GPIO -> [ESP32] WiFi Marauder
```

**Unleashed firmware:**
```
Apps -> GPIO -> [ESP32] WiFi Marauder
```

Most custom firmwares already include the Marauder app preinstalled.
If not present, it can be installed as a .fap app from the SD card.

### 4.3 Flipper-ESP32 Communication

The Flipper communicates with the ESP32 via UART serial:
- Baud rate: 115200 (Marauder default)
- Flipper TX pin -> ESP32 RX pin
- Flipper RX pin -> ESP32 TX pin
- Shared GND
- 3.3V supplied by the Flipper

The app on the Flipper is essentially a serial terminal that:
1. Sends text commands to the Marauder firmware
2. Receives and formats the output
3. Provides a graphical menu for the most common commands
4. Saves results to the Flipper's SD card

Marauder commands are text strings sent via serial. For example:
- `scanap` -- starts AP scanning
- `scansta` -- starts station (client) scanning
- `sniffpmkid` -- starts PMKID capture
- `attack -t deauth` -- starts deauth attack
- `stopscan` -- stops any operation in progress

### 4.4 Saving Results

Captured data is saved on the Flipper's SD card in various formats:
- Scans: text files with AP/client list
- Packet captures: .pcap files (readable with Wireshark)
- PMKID: hashcat-compatible format
- Handshake: .pcap file containing EAPOL frames
- Wardriving: CSV format compatible with WiGLE

The typical path on the SD is:
```
/ext/apps_data/marauder/
```

---
