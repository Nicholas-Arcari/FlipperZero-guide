# Automotive - CAN Bus and Vehicle Diagnostics

This section covers GPIO tools dedicated to the automotive world: standard CAN Bus and CAN-FD interfaces, diagnostic tools, packet injection, and command terminals for ECUs and vehicle networks.

---

### • CAN Transceiver

Standard CAN (Controller Area Network) bus interface.

Extended features:

- CAN packet read and write.
- Real-time traffic monitoring.
- Communication error analysis (CRC, ACK).
- Support for standard speeds: 125k, 250k, 500k, 1Mbps.

Practical example:

- Connect CAN_H and CAN_L to the dedicated GPIO pins.
- Launch CAN Transceiver → monitor messages from automotive ECUs.
- Send test packets to simulate sensors.

(Note: Use proper termination resistors to avoid bus errors)

### • CANBus

Advanced read and write on CAN networks.

Extended features:

- CAN packet recording and analysis.
- Multi-ID and filter support.
- Compatible with standard and extended CAN.

Practical example:

- Connect CANBus to GPIO pins.
- Start reading → save message dump to file.
- Analyze traffic for ECU or industrial device diagnostics.

### • CANBus Attack

Diagnostic and attack tools for the CAN bus.

Extended features:

- CAN packet injection for security testing.
- Replay attack on stored messages.
- CAN network vulnerability analysis.

Practical example:

- Connect Flipper to the test vehicle's CAN bus.
- Start packet replay → observe ECU or gateway reactions.
- Assess security or fail-safe behavior.

### • CANCommander

Terminal for manual or scripted CAN command transmission.

Extended features:

- Text interface for sending and receiving messages.
- Support for automated test scripts.
- Live display of errors and bus status.

Practical example:

- Launch CANCommander → type CAN messages.
- Send command to test ECU → monitor response.
- Script for cyclic message testing across various IDs.

(Note: Useful for debugging and developing automotive tools)

### • Serma CAN-FD-HS

High-speed CAN-FD bus interface via GPIO.

Extended features:

- CAN and CAN-FD packet read and write.
- Bus analysis with timestamps.
- Message ID filtering.
- Support for automotive and industrial buses.
- Advanced logging and debugging.

Practical example

Vehicle ECU monitoring:

- Connect CAN_H / CAN_L.
- Start packet logging.
- Analyze signals for ECU diagnostics.
- Send test messages to verify controls.
