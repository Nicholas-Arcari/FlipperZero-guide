## Detailed Protocols

### DS1990A (Dallas) - The Standard Protocol

The **DS1990A** is the most widely deployed iButton device in the world for contact-based identification systems. It is a minimal chip that contains exclusively a 64-bit ROM code - no writable memory, no encryption, no application logic.

**Technical specifications:**

| Parameter | Value |
|---|---|
| ROM Code | 64 bit (8 byte) |
| Family Code | 0x01 |
| Serial Number | 48 bit (globally unique) |
| CRC | 8 bit (DOW CRC) |
| Operating voltage | 2.8V - 6.0V |
| Current draw | < 5 mA |
| Operating temperature | -40C to +85C |
| 1-Wire speed | Standard (16.3 kbit/s) and Overdrive (142 kbit/s) |
| Package | MicroCAN (16 mm stainless steel) |

**DS1990A ROM Code Structure:**

```
Byte 0:    0x01              (Family Code - identifies DS1990A)
Byte 1-6:  XX:XX:XX:XX:XX:XX (48-bit Serial Number)
Byte 7:    YY                (CRC-8)

Example: 01:A3:5F:2B:00:00:00:E7
              |  |              |  |
              |  +-- Serial ----+  |
              |                    |
              Family Code       CRC-8
```

**How reading works:**

1. You touch the DS1990A key to the reader
2. The reader sends a Reset Pulse (480+ us LOW)
3. The key responds with a Presence Pulse (60-240 us LOW)
4. The reader sends the Read ROM command (0x33)
5. The key transmits the 64-bit ROM code, LSB first
6. The reader calculates the CRC-8 on the first 56 bits and compares it with byte 7
7. If the CRC is valid, the reader looks up the ROM code in the internal database
8. If found: action (opens door, activates intercom, logs presence)

All "security" is based on this: **a number transmitted in clear text, without any challenge-response authentication**. Anyone who reads the key once has all the information needed to clone it.

**Prevalence in Italy:**

The DS1990A is enormously widespread in Italian apartment building intercoms, in particular:

- Installations from 2000-2010 (the golden age of iButton keys in Italy)
- Common brands: Urmet, Comelit, Terraneo, Elvox, BPT
- Typically used in apartment buildings with 10-100 units
- The extremely low system cost (key ~1-2 euro, reader ~20-50 euro) drove massive adoption

> **Personal note:** In my experience, approximately 60-70% of key-based intercoms I find in Italy use DS1990A. That's an enormous percentage. In a building audit I conducted in Milan, out of 5 buildings examined, 4 had DS1990A systems with no additional protection. The fifth had Cyfral. None had systems with encryption or challenge-response. Cloning is trivial - literally 3 seconds of contact with the original key.

### Cyfral - Russian Proprietary Protocol

**Cyfral** is a proprietary protocol developed by the Russian company Cyfral for intercom systems. It is the most widespread contact-based access protocol in the former Soviet Union and is commonly found in Italy as well, especially in areas with Eastern European communities or in installations done by companies that import Russian components.

**How it works:**

Unlike Dallas 1-Wire which uses digital timing slots, Cyfral uses **analog pulse communication** based on resistance ratios:

- The Cyfral reader provides continuous power on the probe
- The Cyfral key modifies the current draw in specific patterns
- The reader interprets current variations as data bits

**Cyfral signal structure:**

The Cyfral protocol transmits an **8-bit** code (some variants up to 36 bits) through a sequence of pulses:

1. **Start condition:** the key begins drawing current in a specific pattern
2. **Bit encoding:** each bit is encoded as a ratio between HIGH duration and LOW duration of a pulse
   - **Bit 0:** low ratio (short pulse relative to the pause)
   - **Bit 1:** high ratio (long pulse relative to the pause)
3. **Repetition:** the code is transmitted repeatedly as long as the key remains in contact

**Key differences from Dallas:**

| Characteristic | Dallas (1-Wire) | Cyfral |
|---|---|---|
| Standard | Open (Dallas/Maxim) | Proprietary |
| Code bits | 64 bit (48 significant) | 8-36 bit |
| Communication | Digital timing slots | Analog pulses (resistive ratio) |
| CRC | Yes (8-bit DOW CRC) | No (in the base version) |
| Power | Parasite from DQ | Supplied by reader |
| Encryption | No | No |
| Keyspace complexity | 2^48 (~281 trillion) | 2^8-2^36 (256 - 68 billion) |
| Prevalence in Italy | High (modern intercoms) | Medium (budget intercoms, Eastern Europe) |

**Common Cyfral readers:**

- **CCD-2094** - the most widespread Cyfral intercom reader
- **CCD-2094.1/M** - variant with memory for more codes
- **Eltis** - associated brand that uses the Cyfral protocol

> **Personal note:** I've encountered Cyfral readers mostly in two contexts in Italy: buildings with Eastern European tenants where the installer used imported components, and old installations on the outskirts where cost was the decisive factor. The protocol is weaker than Dallas from a keyspace perspective - 8 bits means only 256 possible codes in the base version. Some Cyfral systems can be literally brute-forced by hand by trying all combinations in a few minutes. This makes fuzzing extremely effective.

### Metakom - Another Russian Proprietary Protocol

**Metakom** (full name: Metakom, from the Russian for "Metal Communication") is the third protocol supported by the Flipper Zero for iButton. It is a Russian proprietary protocol used in Metakom intercoms, widespread in the former USSR and in some installations in Italy and Southeast Europe.

**How it works:**

Metakom uses an approach similar to Cyfral but with a different signaling protocol:

- Communication based on **variable-duration pulses**
- The key encodes its ID by varying the duration of transmitted pulses
- The reader measures the durations and decodes the code

**Metakom signal structure:**

1. **Synchronization:** initial synchronization pulse
2. **Data bits:** sequence of pulses where the duration encodes 0 or 1
   - **Bit 0:** short pulse followed by long pause
   - **Bit 1:** long pulse followed by short pause
3. **Complete code:** typically 32 bits of useful data
4. **Continuous repetition** during contact

**Differences from Cyfral:**

| Characteristic | Cyfral | Metakom |
|---|---|---|
| Encoding | Resistive ratio | Pulse duration |
| Code length | 8-36 bit | 32 bit typical |
| Keyspace | Small (256 - 68 billion) | Medium (~4.29 billion with 32 bit) |
| Sync | Current pattern | Synchronization pulse |
| Prevalence in Italy | Medium | Low-medium |
| Main brand | Cyfral/Eltis | Metakom |

**Prevalence:**

- Russia and Ukraine: very common in residential buildings
- Italy: rare, present in some installations in large cities with Eastern European communities
- Eastern Europe (Bulgaria, Romania, Moldova): moderately widespread

> **Personal note:** Metakom is the protocol I encounter least in Italy, but when I find it, it's almost always in contexts where the entire intercom system was imported from the East. The 32-bit keyspace makes it more resistant to fuzzing than Cyfral, but 4.29 billion combinations is still a number that, with the right attempt rate and some patience, is not unreachable. In practice though, fuzzing on Metakom takes hours-to-days, not minutes like with Cyfral.

### RW1990 - The Writable Version

The **RW1990** is an iButton chip compatible with DS1990A but with one fundamental difference: the ROM code is **rewritable**. While the DS1990A is factory-programmed with a permanent serial number, the RW1990 allows writing any 64-bit ROM code - it is the iButton equivalent of the **T5577** in the RFID 125 kHz world.

**RW1990 technical specifications:**

| Parameter | Value |
|---|---|
| Compatibility | Emulates DS1990A (family code 0x01) |
| ROM Code | 64 bit, writable |
| Write cycles | Typically ~100,000 cycles |
| Power | Parasite from DQ |
| Speed | Standard 1-Wire |
| Cost | ~0.50-2 euro (purchasable online) |

**How programming works:**

Writing to the RW1990 requires a specific procedure:

1. **Send write unlock command:** a proprietary sequence that puts the chip in programming mode
2. **Write byte by byte:** the 64 bits of the new ROM code are written one byte at a time
3. **Verification:** reading the written ROM code to confirm programming
4. **Lock (optional):** some RW1990s support a "lock" that prevents further writes

**Process on the Flipper Zero:**

1. Read the original DS1990A key - save the `.ibtn` file
2. Insert a blank or overwritable RW1990
3. Go to iButton → Write → select the saved file
4. Place the RW1990 on the Flipper's iButton pad
5. The Flipper programs the RW1990 with the original key's ROM code
6. Automatic verification - the Flipper reads the RW1990 to confirm

**The result is a perfect physical clone** - the programmed RW1990 is electrically indistinguishable from the original DS1990A to any reader. There is no way for a standard reader to distinguish an original from a clone.

**Where to buy RW1990:**

- AliExpress: ~0.30-0.50 euro per piece (in lots of 10+)
- Amazon: ~1-2 euro per piece
- Specialty shops for physical security and locksmiths

> **Personal note:** The RW1990 is the quintessential iButton cloning tool. I always keep about ten in my kit - they cost very little and are essential for demonstrating to a client the vulnerability of their access system. "Look, I cloned your intercom key in 5 seconds, here's the physical clone that works identically" is a demonstration that has much greater impact than a Flipper emulation. The physical clone works even without the Flipper - it's a permanent key.

### TM1990 - Compatible Variant

The **TM1990** (where TM stands for Touch Memory, the generic Russian name for contact devices) is a variant of the DS1990A manufactured by various producers, including Chinese and Russian manufacturers. It is electrically compatible with the DS1990A:

- Same 1-Wire protocol
- Same family code 0x01
- Same 64-bit ROM code format
- Same MicroCAN physical interface

The differences are mainly in branding and manufacturing - there are no functional differences relevant to pentesting. The Flipper reads and emulates them exactly like DS1990As.

Some notable TM1990 variants:

- **TM1990A** - direct clone of the DS1990A
- **TM1990A-F5** - F5 package version (the most common)
- **TM2004** - variant with additional memory (rare in access control systems)

In an operational context, treating TM1990 and DS1990A as identical is always correct.

---
