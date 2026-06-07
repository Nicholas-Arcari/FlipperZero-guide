# Security - Exploitation, Forensics, and Offensive Tools

This section covers GPIO tools oriented toward security: magnetic card emulation, safe control, exploitation modules, forensic suites, and optical surveillance tools. Usable in penetration testing and vulnerability research contexts.

---

### • Sentry Safe

Interface with Sentry safes via control protocols.

Extended features:

- Digital open and close via GPIO sequences.
- Support for models with analog/digital input.
- Ability to record combinations for testing or automation.
- Lock status monitoring and internal LED feedback.

Practical example:

- Connect GPIO pins to the safe's control board.
- Activate opening sequence → verify status LED.
- Test multiple combinations for correctness verification.

### • Evil BW16 Controller

Advanced control tool for BW16 / Ameba RTL modules used in automation and exploitation.

Extended features:

- UART/SPI/I2C communication with BW16.
- Firmware programming.
- Debug log reading.
- Direct interaction with the module's GPIO.
- Customizable scripts for rapid automation.
- Serial monitor with automatic parsing.

Practical example

Real-time flash and monitoring:

- Connect UART and hold the module's BOOT button.
- Load firmware binary → write it.
- Open serial monitor → verify boot sequence.
- Use script commands to drive GPIO.

### • MagSpoof

Magnetic stripe emulation for card and POS system testing.

Extended features:

- ISO 7811 stripe emulation.
- Magnetic track recording and replay.
- Reading system security testing.
- Support for multiple card types (credit, hotel, access).
- Raw data visualization.

Practical example

Badge reader test:

- Connect MagSpoof → select track.
- Execute swipe → verify reader response.
- Analyze raw data for debugging.

### • Flipper BlackHat

Set of experimental and undocumented tools, oriented toward deep-level testing, research, and development.

Extended features:

- Direct access to internal registers.
- Advanced diagnostic functions.
- Possible exploit/experimentation tools (varies by release).
- Low-level raw logging.
- Optional "unsafe" mode.

Practical example

Low-level debug:

- Enable advanced mode.
- Monitor GPIO registers in real time.
- Identify anomalous pin behavior.

### • LAB401 DigiLab

Digital forensics/hardware test suite (depends on supported modules).

Extended features:

- Digital signal visualization.
- Rapid capture tools.
- Input replay functions.
- Protocol pattern analysis.
- Raw data export.

Practical example

Custom protocol verification:

- Connect data lines.
- Record repetitive pattern.
- Compare with internal documentation.

### • LAB401 Light Messenger

Optical communication system via LED and photodiode.

Extended features:

- Optical text/bit transmission.
- Beacon mode.
- Modulation speed adjustment.
- Input light level detection.
- Automatic encoding/decoding.

Practical example

Sending a message via light beam:

- Align LED and photodiode.
- Write message.
- Automatic decoding on the receiving end.

### • Lasercat

Laser control + beam motion detection.

Extended features:

- Controlled laser activation.
- Beam interruption detection.
- "Cat laser chase" game mode.
- Optical alarms.
- Event logging.

Practical example

Laser barrier:

- Activate laser + sensor.
- Object passes → interruption → event trigger.
