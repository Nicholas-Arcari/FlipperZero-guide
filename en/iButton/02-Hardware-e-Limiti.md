## Hardware and Real-World Limitations

### The Flipper Zero iButton Pad

The Flipper Zero integrates an **iButton pad** on the back (dorsal side) of the device. It consists of two concentric metal contacts:

- **Outer contact (ring):** GND
- **Inner contact (center):** Data (DQ)

This layout replicates the geometry of the standard iButton connector - a central contact (data) surrounded by a ground ring. When you place the back of the Flipper on an iButton key or on a reader, the two contacts make the bridge.

**Physical positioning:**

The pad is located on the lower part of the Flipper's back, below the belt clip. For optimal contact:

1. Flip the Flipper upside down (screen facing down)
2. The iButton pad is the metal circle visible on the back
3. To READ a key: place the iButton token centered on the pad
4. To EMULATE on a reader: place the back of the Flipper on the reader, centering the Flipper's metal pad on the reader's probe

**Physical contact is everything:**

Unlike NFC (a few centimeters), Sub-GHz (hundreds of meters), or RFID 125kHz (a few centimeters), iButton has **zero** range. It requires direct metal-to-metal physical contact. This is both a security advantage (you can't read from a distance) and the main operational limitation (you must have physical access to the key).

### Power Supply and Internal Circuitry

The Flipper generates the 1-Wire signal from its GPIO, with internal pull-up and the ability to drive the bus both as master (reading) and as slave (emulation). The firmware manages timing slots via high-priority interrupts, ensuring the microsecond precision required.

In read mode:
- The Flipper powers the iButton key via the DQ pin (parasite power)
- Sends the Read ROM command
- Receives the 64-bit ROM code
- Calculates and verifies the CRC-8

In emulation mode:
- The Flipper behaves as a 1-Wire slave
- Waits for the reset pulse from the reader
- Responds with the presence pulse
- When it receives Read ROM, it transmits the 64-bit saved ROM code
- The reader verifies the ROM code against its database

In write mode (for RW1990 tags):
- The Flipper sends specific commands to unlock writing
- Programs the new ROM code byte by byte
- Verifies the write with a confirmation Read ROM

### Range and Operational Constraints

**Read range:** 0 cm (direct contact). The iButton key must physically touch the Flipper's pad. There is no "remote" reading - even 1 mm of air gap can prevent electrical contact.

**Contact quality:** The metal surface must be clean. Oxidation, dirt, glue residue, or paint on the key or on the Flipper's pad will degrade or prevent contact. A cloth with isopropyl alcohol solves 90% of reading problems.

**Orientation:** The iButton key is symmetrical (circular), so orientation doesn't matter. But the Flipper's pad must be centered on the key - off-center contacts cause intermittent reads.

**Pressure:** Moderate and constant pressure is required. A light touch isn't enough - you must press the key onto the pad (or the Flipper onto the reader) firmly, maintaining contact for the entire duration of the operation (1-3 seconds for reading, variable for emulation).

**Multi-protocol:** The Flipper supports three protocol families on the same iButton pad:
- **Dallas (1-Wire)** - DS1990A, RW1990, TM1990
- **Cyfral** - Russian proprietary protocol
- **Metakom** - Russian proprietary protocol

The firmware automatically detects the protocol during reading - you don't need to manually select the type.

> **Personal note:** Positioning is the thing that causes the most problems for beginners. I've seen people try to read a key by placing it on the screen or the side of the Flipper. The pad is on the BACK, at the bottom. For emulation on an intercom reader, the trick is to flip the Flipper upside down and place the back directly on the reader's metal probe. If the reader has a recessed "button-style" probe, you need to press firmly to make contact. If you're having problems, clean both surfaces.

---
