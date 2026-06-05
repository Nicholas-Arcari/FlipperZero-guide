# MALVEKE - Operational Guide

The Malveke module is a multi-function addon that extends the Flipper Zero with a camera, additional storage, thermal printer, advanced pin management, and test/debug capabilities. Designed for makers, hardware analysts, and pentesters who need visual documentation and prototyping tools in the field.

---

## Hardware

The Malveke connects to the Flipper via the GPIO header and adds:
- **Camera module** (OV2640 or compatible) for photos and video streaming
- **Additional microSD slot** for extended storage
- **Thermal printer interface** ESC/POS for field printing
- **Integrated test pins** for GPIO diagnostics

---

## Tool by Tool

### Cartridge

Modular firmware management system for the Malveke.

**Features:**
- Loading and management of software "cartridges" (additional functions, specialized firmware)
- Backup and restore of cartridge contents
- Integrity verification with digital signature
- Compatibility with community extensions

**Procedure:**
1. Download the desired cartridge (.bin file from the community)
2. Copy to the Flipper's SD card at `/ext/apps_data/malveke/`
3. Open Cartridge -> select the cartridge
4. Install and verify integrity

### Emulator

Emulation module for hardware firmware and functionality.

**Features:**
- Emulation of external hardware modules (I2C sensors, GPIO)
- Sandbox mode for safe testing without physical hardware
- Debug via internal status log
- Digital/analog signal simulation

**Usage in pentesting:** test scripts and automations before running them on real hardware. Allows validating that the firmware will interact correctly with the target.

### Link-Camera / Live Camera

Video streaming from the Malveke camera module.

**Link-Camera:**
- Continuous MJPEG streaming
- Resolution adjustment (QVGA, VGA, SVGA)
- Exposure control, white balance, brightness
- "Low Latency" mode for real-time usage

**Live Camera:**
- Live preview without buffering for immediate response
- Macro mode for close-up inspections
- Quick frame capture to SD

**Usage in pentesting/hardware hacking:**
- Visual documentation during PCB analysis
- Inspection of miniaturized solder joints and components
- Mini digital endoscope for inspecting slots, connectors
- Video recording of procedures for the report

> **Personal note:** The Malveke camera is extremely useful during hardware analysis. When I need to document UART/SWD pads on a PCB for the report, I take photos directly from the Flipper without having to pull out my phone. More discreet and with photos already on the Flipper's SD card.

### Photo

Static photography with the camera module.

**Features:**
- Compressed JPEG shots
- ISO, exposure, focus adjustment
- Album management with preview
- Export via USB/UART/SD

### Pin Test

Diagnostic tool for the Malveke GPIO pins and connected accessories.

**Features:**
- Digital and analog pin scanner
- Voltage and logic state detection (HIGH/LOW)
- Pin-to-pin continuity testing
- Automated test scripts for wiring verification

**Usage:** quick debug before connecting external modules. Verifies that all pins work correctly after assembly.

### Printer

Interface for ESC/POS thermal printers.

**Features:**
- Text printing with variable fonts
- QR codes, barcodes, monochromatic images
- Density and speed configuration
- Diagnostic log printing from other modules

**Usage in pentesting:**
- Quick note printing during an engagement (without using the phone)
- Labels for components during hardware analysis
- QR code printing to quickly share URLs/data
- Paper log of operations for documentation

> **Personal note:** The thermal printer connected to the Flipper is a gadget but has practical use: during a hardware pentest on an industrial facility, I printed labels with the I2C addresses of every device found on the bus. I attached them directly to the boards to keep track. Faster than taking notes.
