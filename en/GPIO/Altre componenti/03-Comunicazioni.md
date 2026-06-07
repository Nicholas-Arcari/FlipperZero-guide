# Communications - Radio, Serial, Buses, and Protocols

This section covers GPIO tools dedicated to communications: LoRa, FM, UART, SPI, I2C, Modbus, UHF RFID, Wiegand, and other data transmission protocols. Essential for wireless network analysis, serial debugging, and integration with external devices.

---

### • E220 LoRa Configurator

Advanced tool for configuring EBYTE E220 modules (LoRa 410/433/868/915 MHz).

Extended features:

- Parameter read and write:
    - TX power
    - Data rate
    - Channel
    - Operating mode
    - Addresses and networks
- RSSI and SNR testing.
- Automated "Range Test" mode.
- Profile export/import.

Practical example

Preparing a LoRa network at 868 MHz:

- Connect M0/M1 + UART.
- Read current configuration.
- Set: 868.5 MHz, TX High Power, fixed transmission mode.
- Save profile → duplicate to secondary modules.

### • LoRa Sample

Basic communication examples using LoRa modules (433/868/915 MHz).

Extended features:

- Test packet transmission.
- Data reception and logging.
- Frequency and TX power configuration.
- Support for point-to-point and broadcast modes.
- Debug via serial monitor.

Practical example

Sending a message between two modules:

- Configure TX module → 868 MHz.
- Configure RX module → reception on same channel.
- Send packet → confirm reception on RX side.
- Record RSSI and SNR for analysis.

### • LoRa Termina

Full terminal for interfacing with advanced LoRa modules.

Extended features:

- CLI interface for sending and receiving packets.
- Advanced settings: spreading factor, bandwidth, coding rate.
- Live packet monitoring.
- Logging to CSV/HEX file.
- Compatibility with SX127x modules.

Practical example

LoRa network test:

- Connect module → open terminal.
- Send test packet "Hello LoRa".
- Check response → complete log.
- Record RSSI/SNR for link mapping.

### • Loradar

Radar via LoRa network for object detection and tracking.

Extended features:

- Periodic packet transmission with "ping" signals.
- Response time measurement for approximate distance.
- Event logging and object mapping.
- Multi-channel sweep function.
- Alert support for objects out of range.

Practical example

Object detection:

- Enable sweep on 868 MHz channel.
- Receive echo → calculate relative distance.
- Display temporal map of detected objects.

### • BunnyConnect

Interface for communicating with Bunny devices.

Extended features:

- Data transfer between Flipper and Bunny devices via GPIO/UART.
- Remote control and parameter synchronization.
- Device status and log reading.
- Multi-device support with automatic port selection.

Practical example:

- Connect Flipper to Bunny device via UART pins.
- Launch BunnyConnect → read battery status and event log.
- Send reset or firmware update command.

(Note: Compatible only with certified Bunny devices)

### • DelfiRTL

Interface/decoder for radio devices and specific modules (likely based on RTL or custom protocols).

Extended features:

- Proprietary protocol decoding.
- Raw packet monitoring.
- Event logging.
- "Protocol Trace" mode for analyzing transactions.
- Dump export capability for external analysis.

Practical example

Analysis of a custom remote control:

- Connect the radio module.
- Launch Packet Sniffer.
- Record frames during button presses.
- Export and analyze patterns in the log file.

### • Digimon F-COM

Dedicated tool for Digimon devices that use the F-COM protocol for exchanges and synchronizations.

Extended features:

- Complete F-COM handshake emulation.
- Time synchronization.
- Save backup/write.
- Status parameter reading.
- Compatibility with modern and legacy models.

Practical example

Backing up a Digimon before a reset:

- Connect F-COM line (infrared or contact).
- Perform handshake → complete dump.
- Save .fc file.
- Restore after device reset.

### • HC-11 Modem

Interface for HC-11 serial modules (433 MHz RF).

Extended features:

- AT parameter configuration.
- Dedicated serial monitor.
- Transmission power control.
- Radio range testing.
- "Transparent link" mode.

Practical example

Setting up a wireless serial link:

- Connect module.
- Set channel and baud rate.
- Send text → verify reception on remote side.

### • FM Radio

FM receiver based on dedicated modules (e.g., TEA5767, RDA5807).

Extended features:

- Automatic and manual tuning.
- RDS (if supported by the module).
- Gain and volume adjustment.
- Band scan with logging of detected channels.
- "Signal Strength" mode for basic RF measurements.

Practical example

Searching for local stations:

- Connect RDA5807 module.
- Start automatic scan.
- Save found presets.
- Manually fine-tune the best frequency.

### • FM Transmitter KT0803

FM transmitter based on KT0803 or similar, for sending audio on the low-power FM band.

Extended features:

- TX frequency setting 70-108 MHz.
- Volume and pre-emphasis control.
- Output signal level monitor.
- Support for microphone or external audio source connection.
- "Beacon" mode for brief signals.

Practical example

Local audio transmission:

- Connect audio source (jack or microphone).
- Set frequency, e.g., 100.1 MHz.
- Transmit → verify reception at a few meters.
- Adjust pre-emphasis for voice clarity.

### • SI4713 Tuner

FM tuner based on SI4713 chip.

Extended features:

- FM frequency tuning (87-108 MHz).
- RSSI signal reading and quality.
- Frequency and RDS station name display (if available).
- Favorite station preset saving.

Practical example

FM station listening:

- Connect antenna → power SI4713.
- Tune to 101.1 MHz → display station name.
- Save preset → automatic playback.

### • UART Echo

UART serial echo for communication testing.

Extended features:

- UART data reception and immediate retransmission.
- TX/RX line testing.
- Baud rate and parity monitoring.

Practical example

Serial wiring verification:

- Connect TX/RX → send test character.
- Check echo → confirm working line.

### • UART Terminal

Full terminal for UART communications.

Extended features:

- ASCII/HEX data send/receive.
- File logging.
- Baud rate, parity, stop bit configuration.
- Serial flow monitoring.

Practical example

UART sensor debug:

- Connect sensor → open terminal.
- Receive data output.
- Analyze values and log to file.

### • Modbus

Modbus RTU/ASCII bus interface via GPIO.

Extended features:

- Register read and write.
- Slave device polling.
- CRC checksum support.
- Transaction logging.
- Compatible with PLCs and industrial instruments.

Practical example

Reading an industrial sensor register:

- Connect GPIO → RS485/TTL converter.
- Send Modbus command → read holding register.
- Verify current value → log to CSV.

### • Wiegand Reader

Standard Wiegand badge reader.

Extended features:

- 26/34 bit badge code reading.
- Event logging.
- Integration with access control systems.
- D0/D1 line debug via GPIO.

Practical example

Badge access:

- Connect reader → GPIO.
- Swipe badge → read code.
- Confirm event log to file.

### • Simultaneous UHF RFID

Simultaneous UHF RFID tag reading.

Extended features:

- Multiple tag detection in range.
- EPC, TID, and other data reading.
- File logging for analysis.
- EPC Gen2 protocol support.

Practical example

RFID inventory:

- Activate reader → scan area.
- Detect multiple tags → save EPC.
- Analyze list for object presence confirmation.

### • UHF RFID

UHF RFID tag read/write interface.

Extended features:

- EPC Gen2 support.
- Single or multiple tag read/find.
- Data logging.
- New EPC writing.

Practical example

Warehouse management:

- Scan tags → read EPC.
- Save data → update inventory.
- Write updated EPCs if needed.

### • SPI Terminal

Advanced terminal for SPI devices.

Extended features:

- Byte/word read and write.
- External SPI memory dump.
- CS/MISO/MOSI/SCK line debug.
- Packet and timing logging.

Practical example

SPI memory test:

- Connect external flash.
- Execute dump → analyze content.
- Write test bytes → confirm correct write.

### • I2C Explorer

Advanced I2C bus inspection tool.

Extended features:

- Deep scan (0x03-0x77).
- Live register reading.
- Memory dump of compatible sensors.
- Digital scope for SDA/SCL.
- Auto-identification of common devices.

Practical example

Diagnosing an unresponsive sensor:

- Launch scan → no device found.
- Enable SDA/SCL visualization.
- Notice SCL stuck LOW → short on line.

### • GPIO with I2C

Combined interface allowing the use of GPIO pins alongside I2C bus.

Extended features:

- I2C device scanning.
- Register read/write.
- Mixed mode: simultaneous GPIO + I2C.
- Support for multiple I2C sensors in parallel.
- Clock adjustment 100/400 kHz.

Practical example

Dual sensor management:

- Connect two modules (e.g., MPU6050 and BH1750).
- Scan → detected 0x68 and 0x23.
- Read data from both in streaming.

### • SD SPI

SD card management via SPI interface.

Extended features:

- FAT16/FAT32 file system read and write.
- File creation, deletion, and modification.
- Complete card dump.
- Compatibility with standard SD, SDHC, and microSD via adapter.
- SPI line debug for signal analysis.

Practical example

Sensor data storage:

- Connect SD card to SPI pins (MOSI/MISO/SCK/CS).
- Create file "log.csv".
- Write values read from sensor.
- Read file → confirm data integrity.

### • GS1 Parser

GS1 code reader and decoder (EAN, UPC, DataMatrix GS1).

Extended features:

- Automatic Application Identifier (AI) parsing.
- Identification of dates, batches, product numbers.
- Support for linear and 2D formats.
- Scan logging with timestamps.
- CSV export.

Practical example

Decoding a food product:

- Scan GS1 code.
- Display AI: expiration, batch, manufacturer.
- Save data for inventory.
