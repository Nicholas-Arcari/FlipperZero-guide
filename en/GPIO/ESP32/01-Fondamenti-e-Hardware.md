## 1. Fundamentals -- ESP32 as Coprocessor

### 1.1 Why an ESP32

The Flipper Zero is a powerful device for interacting with low-frequency radio protocols, Sub-GHz, NFC, RFID, and infrared, but it natively lacks a WiFi module or a high-performance classic Bluetooth module. The ESP32 fills this gap by acting as an external coprocessor connected via UART through the GPIO bus.

In practice, the Flipper Zero becomes the "brain" that sends commands and displays results, while the ESP32 performs the heavy operations: WiFi scanning, packet injection, access point creation, video streaming, BLE communication, and much more.

### 1.2 Connection Architecture

The connection is made via UART (Universal Asynchronous Receiver-Transmitter) through the Flipper Zero GPIO pins. Communication is serial, typically at 115200 baud (some firmware supports up to 921600 baud for flash operations).

Standard connection schematic:

```
Flipper Zero GPIO          ESP32
-----------------          -----
Pin 13 (TX)       --->     RX (GPIO3)
Pin 14 (RX)       <---     TX (GPIO1)
Pin 15 (3.3V)     --->     3V3
Pin 18 (GND)      --->     GND
```

Note: TX and RX pins must be crossed. The Flipper's TX goes to the ESP32's RX and vice versa. This is a common error that causes the module to not be recognized.

For firmware flashing, some modules also require connecting the GPIO0 (boot mode) and EN (enable/reset) pins:

```
Flipper Zero GPIO          ESP32 (flash only)
-----------------          -----
Pin 2 (A7)        --->     GPIO0 (BOOT)
Pin 16 (C0)       --->     EN (RESET)
```

### 1.3 Power Supply

The ESP32 requires 3.3V and can draw up to 500mA during intensive WiFi operations (TX at full power). The Flipper Zero provides 3.3V from pin 15, but the available current is limited.

Recommendations:

- For light operations (passive scan, BLE): power from the Flipper is sufficient.
- For heavy operations (deauth, beacon spam, AP mode, video streaming): use external USB power or a dedicated battery. The ESP32 under load can cause Flipper reboots or unstable behavior.
- For the ESP32-CAM: external power is almost mandatory, the camera module + IR LED draw over 300mA.

### 1.4 Compatible ESP32 Models

**ESP32-WROOM-32**

The classic and most widespread module. Dual-core Xtensa LX6 at 240MHz, WiFi 802.11 b/g/n, Bluetooth 4.2 + BLE. It's the reference module for Marauder and most offensive WiFi tools. Comes with 4MB flash (some models 16MB), 520KB SRAM. Supports integrated PCB antenna or U.FL connector for external antenna.

Advantages: maximum compatibility, large community, tested firmware.
Disadvantages: not the most compact form factor, mediocre PCB antenna for long-range wardriving.

**ESP32-S2**

Single-core Xtensa LX7 at 240MHz, WiFi only (no Bluetooth). Has a native USB controller that allows direct flashing without an external UART converter. Supports WiFi HT40 for higher throughput.

Advantages: native USB, lower power consumption, reduced cost.
Disadvantages: no BLE, single-core limits multitasking.

**ESP32-S3**

Dual-core Xtensa LX7 at 240MHz, WiFi + Bluetooth 5.0 + BLE. Represents the evolution of the WROOM with BLE 5 support and superior performance. Native USB. Supports AI acceleration with SIMD instructions.

Advantages: BLE 5.0, top performance, native USB.
Disadvantages: not all firmware is optimized for S3 yet, higher cost.

**ESP32-CAM (AI-Thinker)**

Based on ESP32-S with OV2640 (2MP) or OV3660 (3MP) camera module. Includes microSD slot, high-power flash LED, and optional IR LED for night vision. It's the reference module for all Flipper camera tools.

Advantages: integrated camera, flash/IR LED, SD slot.
Disadvantages: no native USB (requires FTDI/CP2102 converter for flashing), limited GPIO pins because many are used by the camera, critical power requirements.

### 1.5 Development Boards and Devboards

The official Flipper Zero WiFi Devboard is based on ESP32-S2 and is plug-and-play: it connects directly to the Flipper GPIO bus without wiring. It's the most convenient solution but doesn't support BLE.

Third-party alternatives:

- Devboards based on ESP32-WROOM with direct GPIO connector
- Custom 3D-printed adapters with generic ESP32 modules
- Breadboard with dupont wires for experimental setups

> Personal note: for serious pentesting I use the official ESP32-S2 devboard for pure WiFi (Marauder, Evil Portal) and a separate ESP32-WROOM on a breadboard for when BLE is needed. The ESP32-CAM I keep for visual reconnaissance and always power it with a dedicated power bank -- never trust the Flipper's power for the camera, it reboots at the worst moment.

---

## 2. Setup and Firmware Flashing

### 2.1 Environment Preparation

Before using any ESP32 tool on the Flipper, the module must be flashed with the correct firmware. Each tool requires a specific firmware on the ESP32 -- there is no universal firmware that enables all tools simultaneously.

Main firmware:

| Firmware | Supported Tools | Target Module |
|----------|----------------|---------------|
| Marauder | Marauder, WiFi Marauder | ESP32-WROOM, ESP32-S2 |
| Evil Portal | Evil Portal | ESP32-WROOM, ESP32-S2 |
| Ghost ESP | Ghost ESP | ESP32-WROOM |
| Camera firmware | Camera, Camera Suite, Motion Detection, Nanny Cam, QR Code | ESP32-CAM |
| BlackMagic | UART Debugger | ESP32-S2 |
| Wardriver | Wardriver | ESP32-WROOM + GPS |

### 2.2 Flash via Web Flasher (Recommended Method)

The simplest method is the web flasher, which works directly from the browser (Chrome/Edge with Web Serial API support).

Step-by-step procedure:

1. Connect the ESP32 to the PC via USB (or via UART-USB converter if the module doesn't have native USB).
2. Open the appropriate web flasher:
   - Marauder: `https://flasher.marauder.dev`
   - Evil Portal: `https://flasher.evilportal.dev`
   - Camera firmware: depends on version, consult the tool's GitHub repository
3. Select the correct ESP32 module from the dropdown menu.
4. Click "Connect" and select the module's serial port.
5. Select the desired firmware.
6. Click "Flash" and wait for completion.
7. Upon completion, the module automatically reboots with the new firmware.

Note: if the module doesn't enter boot mode automatically, hold the BOOT button (GPIO0 to GND) during connection or before clicking Flash.

### 2.3 Flash via esptool (Advanced Method)

For those who prefer the command line or need to flash custom firmware:

```bash
# Install esptool
pip install esptool

# Identify the chip
esptool.py --port /dev/ttyUSB0 chip_id

# Erase the flash (recommended before first flash)
esptool.py --port /dev/ttyUSB0 erase_flash

# Flash the firmware (Marauder example)
esptool.py --port /dev/ttyUSB0 \
  --baud 921600 \
  --before default_reset \
  --after hard_reset \
  write_flash -z \
  --flash_mode dio \
  --flash_freq 80m \
  --flash_size 4MB \
  0x1000 bootloader.bin \
  0x8000 partitions.bin \
  0x10000 marauder.bin
```

The offsets (0x1000, 0x8000, 0x10000) vary depending on the firmware. Always consult the specific documentation.

For ESP32-S2 and S3, offsets change:

```bash
esptool.py --port /dev/ttyUSB0 \
  --chip esp32s2 \
  --baud 921600 \
  write_flash -z \
  0x1000 bootloader.bin \
  0x8000 partitions.bin \
  0x10000 firmware.bin
```

### 2.4 Flash via Flipper ESP Flasher

The Flipper itself can flash the ESP32 connected via GPIO, using the ESP Flasher tool (described in the Various Tools section). This method is convenient but slower and requires the .bin files to already be on the Flipper's microSD.

### 2.5 Flash Troubleshooting

**Module not recognized**
- Check USB drivers: CP2102, CH340, or FTDI depending on the converter.
- On Linux: `ls /dev/ttyUSB*` or `ls /dev/ttyACM*` to verify the port.
- On Windows: check in Device Manager under "COM Ports".
- Try a different USB cable (many cheap cables are charge-only, without data).

**"Failed to connect to ESP32" error**
- The module is not in boot mode: hold BOOT, press and release EN/RESET, then release BOOT.
- For ESP32-CAM without BOOT button: connect GPIO0 to GND before powering on.
- Try a lower baud rate (115200 instead of 921600).

**Flash completed but module doesn't respond**
- Check TX/RX connection (remember: they must be crossed).
- Verify that the firmware is compatible with the specific module.
- Try a full erase_flash before re-flashing.

**Flipper doesn't recognize the ESP32 after flash**
- Restart both the Flipper and the ESP32.
- Verify that the ESP32 firmware is compatible with the Flipper firmware version.
- Check the GPIO connection pins.

> Personal note: the most frequent problem by far is the USB cable. I've lost hours debugging issues that were solved simply by changing the cable. Always keep a quality data USB cable in your kit. Second most common problem: wrong offsets in manual flashing -- always check the specific firmware documentation.

---
