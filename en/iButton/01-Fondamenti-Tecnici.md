# Technical Fundamentals - iButton and the 1-Wire Protocol

In-depth analysis of the technical fundamentals underlying iButton technology: Dallas Semiconductor's 1-Wire protocol, bus electrical architecture, communication timing, parasite power, ROM structure, and fundamental commands. Analysis perspective oriented toward penetration testing of contact-based access control systems.

---

## What is iButton

iButton is a family of electronic devices integrated into a button-shaped metal housing (16 mm diameter), designed by **Dallas Semiconductor** (acquired by Maxim Integrated in 2001, now part of Analog Devices). The commercial name "iButton" refers to the MicroCAN contact package - a hermetically sealed F5 stainless steel enclosure, resistant to impacts, water, and corrosion.

The concept is simple: a chip with a unique identifier, accessible through direct physical contact. No antenna, no radio frequency, no internal power supply. The device communicates exclusively when physically pressed onto a reader.

In the physical security domain, iButton keys are used for:

- **Apartment building intercoms** - the most common use case in Italy and Eastern Europe
- **Contact-based access control systems**
- **Guard tour systems** for security patrols
- **Electronic locks** for industrial and residential use
- **Identification systems** in hostile environments (dust, water, vibrations)

> **Personal note:** iButton technology is a perfect case study for the pentester: a system designed in the 1990s for convenience and mechanical robustness, with zero consideration for cryptographic security. When I explain iButton to clients, I use this analogy: "it's like a license plate that anyone can read and duplicate in 3 seconds." The simplicity of the protocol is both the reason for its commercial success (it costs very little) and its fatal weakness from a security standpoint.

---

## The 1-Wire Protocol

iButton is based on the **1-Wire** bus, a serial communication protocol invented by Dallas Semiconductor. The name says it all: communication occurs over a **single wire** (plus ground), making the system as simple as possible at the hardware level.

### Electrical Architecture

The 1-Wire bus uses only two contacts:

- **Data (DQ)** - the single wire carrying data, clock, and power
- **GND (Ground)** - ground/reference

The bus is of the **open-drain with pull-up resistor** type. At idle, the data line is held at logic HIGH (typically 5V or 3.3V) by the pull-up resistor (typically 4.7 kohm). Communication occurs when the master (reader) or the slave (iButton) pulls the line to LOW.

```
          Vcc (5V / 3.3V)
           |
          [R] 4.7 kohm pull-up
           |
    DQ ----+---- iButton (slave)
           |
    Master (reader/Flipper)
           |
          GND ---- GND
```

### Bus Topology

The 1-Wire bus supports a multi-drop topology: a single master can communicate with multiple slaves on the same wire. This is relevant in more complex access systems where the reader also manages temperature sensors or EEPROM modules on the same line.

In typical iButton access systems (intercoms), the topology is almost always **point-to-point** (one reader, one key at a time), since the key is physically placed on the reader's probe.

> **Personal note:** The multi-drop topology of 1-Wire opens an interesting attack vector that few consider: if you manage to connect an additional slave device to the bus (for example, a hidden microcontroller behind the reader), you can passively sniff all communications without the reader noticing. The bus is designed to have multiple slaves, so an extra device does not generate errors.

### Bidirectional Communication on a Single Wire

The 1-Wire protocol is **half-duplex** - master and slave share the same wire and take turns communicating. The master always controls the timing:

1. **Reset Pulse:** the master pulls DQ to LOW for at least 480 microseconds
2. **Presence Pulse:** the slave detects the reset and responds by pulling DQ to LOW for 60-240 microseconds - this is the device's "I'm here" signal
3. **Time Slot (write):** the master pulls DQ to LOW for a brief period:
   - **Write 0:** holds LOW for 60-120 microseconds (the entire slot)
   - **Write 1:** pulls LOW for 1-15 microseconds then releases (the pull-up brings it back to HIGH)
4. **Time Slot (read):** the master pulls DQ to LOW for 1-15 microseconds then releases. The slave responds within 15 microseconds:
   - **Read 0:** the slave holds LOW
   - **Read 1:** the slave does nothing (the line returns HIGH via the pull-up)

### Detailed Timing Diagram

```
Reset and Presence Pulse:

     |<-------- Reset Pulse (480-960 us) -------->|<-- Recovery -->|<- Presence (60-240 us) ->|
     |                                             |   (15-60 us)   |                          |
HIGH ____                                         _________________                            ____
         |                                       |                 |                          |
LOW      |_______________________________________|                 |__________________________|


Write 0 Slot:

     |<-------------- 60-120 us ------------->|<- Recovery (1 us min) ->|
     |                                        |                        |
HIGH ____                                     __________________________
         |                                   |
LOW      |___________________________________|


Write 1 Slot:

     |<- 1-15 us ->|<--------- Pull-up restores HIGH --------->|<- Recovery ->|
     |              |                                            |              |
HIGH ____           ______________________________________________              ___
         |         |
LOW      |_________|


Read Slot:

     |<- Master 1-15 us ->|<-- Slave response window (15 us) -->|<- Recovery ->|
     |                     |                                      |              |
HIGH ____                  ________________________________________              ___  (Read 1 - slave releases)
         |                |
LOW      |________________|

         |                     |                                      |
HIGH ____                  ____                                       ___  (Read 0 - slave holds LOW)
         |                |    |                                     |
LOW      |________________|    |_____________________________________|
```

### Critical Timing Table

| Operation | Minimum Duration | Typical Duration | Maximum Duration |
|---|---|---|---|
| Reset pulse | 480 us | 480-640 us | 960 us |
| Presence pulse | 60 us | 60-120 us | 240 us |
| Write 0 slot | 60 us | 60 us | 120 us |
| Write 1 slot | 1 us | 6 us | 15 us |
| Read slot | 1 us | 1 us | 15 us |
| Recovery time | 1 us | 1 us | - |
| Total slot (min) | 61 us | 61 us | 121 us |

The timing slots are the foundation of all 1-Wire communication. Each bit requires a minimum of 60 microseconds + 1 microsecond of recovery, bringing the maximum theoretical data rate to approximately **16.3 kbit/s** in standard mode. There is also an **overdrive** mode up to ~142 kbit/s, but it is rarely used in access control systems.

> **Personal note:** The timing is relevant to the pentester in two contexts. First: when emulating from the Flipper, the firmware must respect these timings with microsecond precision - if the firmware has a timing bug, emulation fails on strict readers. Second: when analyzing an unknown protocol with an oscilloscope or logic analyzer, knowing the standard timings allows you to distinguish between 1-Wire Dallas, Cyfral, and Metakom by observing the temporal patterns. I used a Saleae Logic to analyze a reader that wasn't responding to the Flipper - the problem was a non-standard timing in the reset pulse (the reader was using 380 us instead of the 480 us minimum).

### Communication Speed

The 1-Wire protocol defines two operating speeds:

| Mode | Data Rate | Typical Use |
|---|---|---|
| **Standard** | ~16.3 kbit/s | All iButton access systems |
| **Overdrive** | ~142 kbit/s | High-speed 1-Wire devices (rare in access control) |

For reading a 64-bit ROM code in standard mode:
- Reset/presence time: ~1 ms
- Time for Read ROM command (8 bit): ~0.5 ms
- Time for 64 bits of data: ~4 ms
- **Total time for a complete read: ~5.5 ms**

This means a reader can theoretically read a key ~180 times per second. In practice, readers add processing and debouncing delays, reducing the rate to 2-10 reads per second.

---

## Parasite Power

A unique characteristic of 1-Wire is **parasite power**: the slave device draws the energy needed for operation directly from the DQ data line during HIGH periods. An internal capacitor in the chip stores enough charge to maintain operation during LOW phases.

```
Parasite power equivalent circuit:

    DQ ────┬───── [Chip Logic]
           |
          [C] Internal capacitor (~800 pF typical)
           |
    GND ───┘

    During HIGH: DQ charges the capacitor through an internal diode
    During LOW:  the capacitor powers the chip logic
```

This means the iButton has no battery - it receives power from physical contact with the reader. When you touch the key to the reader, the chip powers on, communicates its ID, and then powers off as soon as you remove the key.

Some more complex 1-Wire devices (temperature sensors, EEPROM) may require dedicated external power (separate Vcc) for operations that consume more current, such as EEPROM writes or temperature conversion. But for iButton keys used in access control systems, parasite power is sufficient.

> **Personal note:** Parasite power has an important implication for writing to RW1990: during programming, the chip requires more current than normal. If the electrical contact is not perfect, the voltage on the internal capacitor drops below the minimum threshold and the write gets corrupted. This is why writing is less reliable than reading - reading requires very little current, writing requires more. A clean and stable contact is even more critical for writing than for reading.

---

## Family Code and ROM Structure

Every 1-Wire device has a unique 64-bit (8 byte) **ROM code**. This is the structure:

```
| Family Code | Serial Number           | CRC-8  |
| 8 bit       | 48 bit                  | 8 bit  |
| Byte 0      | Byte 1 | ... | Byte 6   | Byte 7 |
```

### Family Code (8 bit)

The family code identifies the device type:

| Family Code | Device | Description |
|---|---|---|
| `0x01` | DS1990A / DS1990R / DS2401 | Read-only identification key |
| `0x02` | DS1991 | Key with protected memory |
| `0x04` | DS1994 | Timer + memory |
| `0x06` | DS1993 | 4 Kbit memory |
| `0x08` | DS1992 | 1 Kbit memory |
| `0x0A` | DS1995 | 16 Kbit memory |
| `0x0C` | DS1996 | 64 Kbit memory |
| `0x10` | DS18S20 | Temperature sensor |
| `0x14` | DS1971/DS2430A | 256-bit EEPROM |
| `0x23` | DS2433 | 4 Kbit EEPROM |
| `0x28` | DS18B20 | Digital temperature sensor |
| `0x81` | DS1420 | Serial ID + counter |

### Serial Number (48 bit)

The unique serial number assigned at the factory. This is the effective address space - 2^48 = **281,474,976,710,656** possible combinations. Every Dallas chip leaves the factory with a unique serial number, never repeated. Maxim/Analog Devices guarantees global uniqueness.

### CRC-8 (8 bit)

Checksum calculated with the DOW-CRC polynomial (x^8 + x^5 + x^4 + 1, polynomial 0x31). The CRC is calculated on the first 7 bytes (family code + serial number) and allows the reader to verify communication integrity.

**CRC-8 DOW (Dallas One-Wire) Calculation:**

```
Polynomial: x^8 + x^5 + x^4 + 1  (0x31, or 0x8C reflected)
Initial value: 0x00
Input: byte 0 through byte 6 (family code + serial number)
A valid CRC produces 0x00 when calculated over all 8 bytes
```

**CRC-8 DOW Algorithm (pseudocode):**

```
function dow_crc8(data[], length):
    crc = 0x00
    for i = 0 to length-1:
        byte = data[i]
        for bit = 0 to 7:
            mix = (crc ^ byte) & 0x01
            crc = crc >> 1
            if mix:
                crc = crc ^ 0x8C
            byte = byte >> 1
    return crc
```

**Practical example - a DS1990A key with ROM code `01:A2:B3:C4:D5:E6:F7:XX`:**

- Family code: `0x01` (DS1990A)
- Serial: `A2:B3:C4:D5:E6:F7`
- CRC-8: automatically calculated on the first 7 bytes

> **Personal note:** The CRC-8 is important in iButton pentesting for two reasons. First: if you generate IDs manually for fuzzing, you must calculate the correct CRC otherwise the reader will discard the ID before even checking it against the database. Second: some cheap readers (especially Cyfral/Metakom ones) do not verify the CRC - this makes them vulnerable to malformed IDs. I've found intercoms that accept anything with family code 0x01, completely ignoring the CRC.

> **Personal note:** For the pentester who wants to generate valid IDs programmatically (for example, for custom fuzzing via script), implementing the CRC-8 DOW is essential. I have a Python script that generates batches of valid IDs with correct CRC - I use it to prepare targeted fuzzing dictionaries when I know the serial prefix of an apartment building. Without a valid CRC, the reader discards the ID at the first check and fuzzing becomes useless.

---

## 1-Wire ROM Commands

After the reset/presence, the master must send a ROM command to select the device:

| Command | Code | Description |
|---|---|---|
| **Read ROM** | `0x33` | Reads the 64-bit ROM code. Only works if there is a single slave on the bus |
| **Match ROM** | `0x55` | Selects a specific slave by sending its 64 bits - used with multiple slaves on the bus |
| **Skip ROM** | `0xCC` | Skips selection - communicates with the device present (only if there is one) |
| **Search ROM** | `0xF0` | Search algorithm to enumerate all devices on the bus |
| **Alarm Search** | `0xEC` | Like Search ROM but only searches for devices in alarm state |

For access keys (DS1990A), the only relevant command is **Read ROM** - the reader performs a reset, reads the 64-bit ROM code, and compares it against the internal database.

### Complete Read Sequence

```
Master                              Slave (iButton)
  |                                      |
  |--- Reset Pulse (480+ us LOW) ------->|
  |                                      |
  |<--- Presence Pulse (60-240 us LOW) --|
  |                                      |
  |--- Read ROM (0x33, 8 bit) --------->|
  |                                      |
  |<--- ROM Code (64 bit, LSB first) ---|
  |                                      |
  [Calculate CRC-8 on first 56 bits]     |
  [Compare with byte 7]                 |
  [If valid: search in database]         |
  [If found: action]                     |
```

> **Personal note:** The beauty (and weakness) of the system is precisely this: all "security" relies on the secrecy of a 64-bit number transmitted in clear text, without any encryption, over a physical bus. Anyone who can touch the key for one second can read that number and replicate it. This is why iButton is considered extremely insecure by modern standards - but it is still installed in millions of intercoms.

> **Personal note:** The Search ROM algorithm (0xF0) has an interesting application in pentesting: if you manage to connect a device to the internal bus of a multi-drop reader (for example, a guard tour system with multiple readers in cascade), you can enumerate all 1-Wire devices on the network using Search ROM. This gives you a map of all sensors, EEPROMs, and modules connected - useful information for understanding the target system's architecture.

---

## Security Implications

### Absence of Encryption

The 1-Wire protocol was designed for simplicity and reliability, not security. The implications for access control systems are:

| Aspect | Security Implication |
|---|---|
| ID transmitted in clear text | Anyone can read the ID with a 2-euro 1-Wire reader |
| No challenge-response | No mutual authentication exists |
| No nonce/timestamp | Replay attacks always work, with no expiration |
| Static and permanent ID | Once read, the ID is valid forever |
| No revocation at protocol level | Revocation only happens on the reader's database |

### The iButton Security Paradox

The mandatory physical contact is often cited as iButton's "security measure" - "you can't read it from a distance." This is true but misleading:

1. Physical contact protects against remote reading (unlike RFID/NFC)
2. But it does not protect against cloning - you just need to touch the key for 2 seconds
3. And it does not protect against fuzzing - you just need to touch the reader with an attacking device

iButton security relies entirely on the physical security of the key and the management of the reader's database, not on the protocol.

> **Personal note:** I always explain to clients that iButton is like a traditional mechanical key: if someone holds it for 3 seconds, they can make a copy. The difference is that with iButton the "copy" costs 50 cents and requires zero skill, while duplicating a high-security mechanical key (like an Evva MCS or Mul-T-Lock) is significantly more difficult and expensive. Paradoxically, the mechanical key protecting the apartment door is often more secure than the iButton key protecting the building's main entrance.
