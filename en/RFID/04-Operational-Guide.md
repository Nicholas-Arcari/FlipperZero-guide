## Tool by Tool - Operational Guide

### RFID 125 kHz - Main Module

The main module for managing 125 kHz tags. Accessible from: `Main Menu > RFID 125 kHz`.

#### Read

**Step-by-step procedure:**

1. Turn on the Flipper and navigate to `RFID 125 kHz`
2. Select `Read`
3. The screen shows "Reading..." with an animation
4. Bring the tag close to the lower part of the Flipper (below the screen)
5. Hold the tag at 0-5 cm, parallel to the Flipper
6. When the tag is read, the Flipper vibrates and displays:
   - Protocol type (EM4100, HID, Indala, etc.)
   - Tag ID in hexadecimal format
   - For HID: decoded Facility Code and Card Number
   - For FDX-B: Country Code and Animal ID
7. Post-read options:
   - `Save` - save to SD card in `/lfrfid/`
   - `Emulate` - start emulating the tag immediately
   - `Write` - write to a T5577

**Automatically recognized protocols:**
- EM4100
- HID H10301 (26-bit)
- HID H10302 (37-bit)
- HID H10304 (37-bit)
- Indala (26-bit)
- Indala (raw)
- FDX-B (ISO 11784/11785)
- FDX-A
- EM4305
- Viking
- Jablotron
- Paradox
- PAC/Stanley
- Keri
- Gallagher
- AWID
- Pyramid
- GProxII
- IoProx
- Nexwatch

**Saved file format (.rfid):**
```
Filetype: Flipper RFID key
Version: 1
Key type: EM4100
Data: 01 02 03 04 05
```

**Reading tips:**
- If the tag is not read, try rotating it 90 degrees
- Remove metal covers from the Flipper
- Try both the top and bottom of the Flipper (the antenna is underneath)
- Approach gradually - do not slam the tag against the Flipper
- If it reads the wrong protocol (e.g. EM4100 instead of HID), the tag might be multi-protocol or the Flipper confused - try again

#### Emulate (Emulation)

**Step-by-step procedure:**

1. Open a saved .rfid file or read a tag and choose `Emulate`
2. The screen shows "Emulating..." with the ID displayed
3. Bring the Flipper close to the badge reader/door
4. The Flipper modulates its field to simulate the tag
5. If the reader accepts the ID, the door opens / the system responds
6. Press `Back` to stop emulation

**Emulation limitations:**
- Works only if the reader is within the Flipper's range (2-5 cm)
- Emulation timing must be precise - it may not work on the first attempt
- Some readers have minimum power thresholds the Flipper cannot reach
- HID/Indala emulation is less reliable than EM4100
- FDX-B emulation at 134.2 kHz may not work (the Flipper operates at 125 kHz)

> **Personal note:** Emulation is convenient but not always reliable. In pentesting I ALWAYS prefer writing to a T5577 rather than using emulation. Reasons: the T5577 is a real physical tag, it generates a signal identical to the original, it does not depend on the Flipper's battery, and it works with any reader. I only use emulation for quick lab tests or when I do not have a T5577 available.

#### Write

**Step-by-step procedure:**

1. Read a tag or open a saved .rfid file
2. Select `Write`
3. The Flipper asks you to bring a T5577 close
4. Place the T5577 on the lower part of the Flipper
5. Hold still - the process takes 2-3 seconds
6. If the write succeeds, the Flipper vibrates and confirms
7. Verify: go to `Read` and read the T5577 you just wrote
8. The read ID must match the original one

**What happens during writing:**
1. The Flipper calculates the appropriate Block 0 configuration for the protocol
2. Writes Block 0 (configuration)
3. Writes Blocks 1-N (ID data)
4. The T5577 reconfigures itself and begins transmitting as the original tag

**Common writing issues:**
- T5577 not recognized: it may be password-protected or not a real T5577
- Write failed: hold the T5577 more firmly and closer
- Verification failed: rewrite - sometimes the first attempt corrupts a block
- "Bricked" T5577: if Block 0 was written with incorrect values, the tag may stop responding. In this case a Proxmark3 is needed for recovery

#### Add Manually

**Step-by-step procedure:**

1. Go to `RFID 125 kHz > Add Manually`
2. Select the protocol:
   - EM4100
   - HID H10301
   - Indala
   - (others depending on firmware)
3. Enter the data:
   - EM4100: 5 hexadecimal bytes (10 hex digits)
   - HID: Facility Code (0-255) and Card Number (0-65535)
   - Indala: raw data
4. Save the file
5. You can then emulate or write to T5577

**When to use it:**
- When you know the ID from a different source (system logs, photos, social engineering)
- When you want to generate specific IDs for testing
- When you want to create incremental IDs for manual fuzzing
- When you have data from a Proxmark3 and want to use it on the Flipper

---

### EM4100 Key Generator

Application for quickly generating valid EM4100 IDs.

#### How It Works

1. Open `EM4100 Key Generator` from the applications menu
2. The app generates a random valid EM4100 ID
3. Options:
   - `Generate` - generate a new random ID
   - `Save` - save the ID as a .rfid file
   - `Emulate` - emulate immediately
   - `Write T5577` - write directly to a tag

#### When to Use It

- **Manual fuzzing:** generate different IDs and test them one by one on a reader
- **System testing:** verify that a reader rejects unauthorized IDs
- **Creating test badges:** for lab work or demonstrations
- **Database population:** generate many IDs for load testing an access control system

> **Personal note:** The EM4100 Key Generator is useful but limited. For serious fuzzing I use the RFID Fuzzer which is automated. I use the EM4100 Key Generator to quickly create test badges when I need to demonstrate to a client that their system accepts any ID (no authorization database - the reader opens for anyone). This happens more often than you would think, especially with standalone systems not connected to a controller.

---

### FDX-B Maker

Application for creating FDX-B (ISO 11784/11785) tags with custom data.

#### How It Works

1. Open `FDX-B Maker`
2. Enter the fields:
   - **Country Code:** numeric ISO 3166 country code (e.g. 380 for Italy)
   - **National ID:** identification number (up to 38 bits, max ~274 billion)
   - **Animal Flag:** 1 = animal, 0 = object
   - **Data Flag:** 1 = supplementary data present
3. The app calculates the complete FDX-B frame with CRC
4. Options: save, emulate or write to T5577

#### When to Use It

- **Protocol study:** understanding how an FDX-B ID is structured
- **Veterinary reader testing:** verifying that a reader decodes correctly
- **Research:** studying the format and national variants
- **Demonstration:** showing the possibility of creating fake animal IDs

**Common country codes:**

| Code | Country |
|---|---|
| 380 | Italy |
| 276 | Germany |
| 250 | France |
| 724 | Spain |
| 826 | United Kingdom |
| 840 | United States |
| 036 | Australia |

> **Personal note:** The FDX-B Maker is a niche tool. I have used it exactly twice: once to verify the operation of a veterinary reader in a lab, once to demonstrate in a presentation that animal microchips have no cryptographic protection. In theory one could create a fake microchip for a stolen animal, but in practice the chip must be physically implanted by a veterinarian and registered in the registry - the problem is bureaucratic, not technical. There are almost never real pentesting implications.

---

### RFID Fuzzer

The most powerful tool for active testing of RFID 125 kHz systems. It generates and transmits IDs in sequence to discover vulnerabilities.

#### Fuzzing Modes

**1. Sequential:**
- Increments the ID by 1 at each iteration
- Starts from a base value (default: 00:00:00:00:00) or from a read ID
- Useful for discovering valid IDs when you know the range
- Speed: approximately 3-5 IDs per second

**2. Random:**
- Generates random IDs
- Useful for reader robustness testing
- Less efficient than sequential for finding valid IDs
- Useful for stress-testing

**3. BF (Brute Force) on specific byte:**
- Allows you to fix the known bytes and fuzz only the unknown ones
- Example: you know the first 3 bytes (version + part of ID) and fuzz the last 2
- Much faster than complete brute force
- Ideal when you have partial information

#### Protocols Supported by the Fuzzer

- EM4100
- HID H10301 (fuzzing on FC, CN or both)
- Indala (26-bit)
- PAC/Stanley
- Viking
- Jablotron
- Pyramid

#### Operational Procedure for Pentesting

1. **Reconnaissance phase:**
   - Read at least one valid badge (social engineering, dumpster diving)
   - Identify the protocol and ID
   - For HID: note the Facility Code
   
2. **Fuzzer configuration:**
   - Select the correct protocol
   - Set the base ID (the badge you read)
   - Choose the mode (sequential starting from the known ID is the most effective)
   
3. **Execution:**
   - Position the Flipper on the target reader
   - Start fuzzing
   - Observe the reader's behavior (LEDs, sounds, door opening)
   - The Flipper shows the current ID on screen
   
4. **Results analysis:**
   - If the reader opens: you found a valid ID - save it
   - If the reader locks up/errors: you found a bug - document it
   - If the reader never reacts: the system may have a restrictive database (good sign for security)

#### Fuzzing Limitations

- **Speed:** 3-5 IDs/second means a complete brute force on EM4100 (2^40 possibilities) would take thousands of years
- **Detection:** a monitored system could generate alerts after many failed attempts
- **Range:** you must keep the Flipper on the reader for the entire duration - not very discreet
- **Reader lockout:** some readers lock up after N rapid failed attempts (rate limiting)

> **Personal note:** RFID fuzzing is useful but must be used strategically, not blindly. If you read an HID badge with FC:42 CN:500, do not brute force the entire space - try CN:1-1000 (low numbers, often assigned first). In one engagement I found that a corporate parking garage accepted any EM4100 with the correct first 2 bytes (the "version number" of the badge batch). All you had to do was read a badge, keep the first 2 bytes and change the last 3 - any combination opened it. The fuzzer found this in less than 5 minutes.

---

### T5577 MultiWriter

Tool for rapid automatic tag cloning to T5577.

#### How It Works

1. Open `T5577 MultiWriter`
2. Select the source:
   - .rfid file saved on SD card
   - Last tag read in memory
3. Place a blank T5577 on the Flipper
4. The app automatically writes:
   - Block 0 (protocol configuration)
   - Blocks 1-N (ID data)
5. Confirmation via vibration
6. You can immediately place another T5577 for a new copy

#### Differences from Standard Write

| Feature | Write (RFID module) | T5577 MultiWriter |
|---|---|---|
| **Data source** | Only freshly read tag | Saved file or read tag |
| **Workflow** | Read > Write (2 steps) | Select file > Write (1 step) |
| **Multiple copies** | Requires re-reading | Place and write in a loop |
| **Verification** | Manual | Automatic (reads after writing) |

#### When to Use It

- You need to create multiple copies of the same badge (e.g. for a pentest team)
- You need to prepare badges before the engagement (offline cloning from file)
- Rapid duplication for a client who wants backup badges
- Lab testing with many tags

> **Personal note:** The MultiWriter is my favorite tool for preparing an engagement. The evening before, I take all the .rfid files collected during reconnaissance and write them to T5577s - one for each badge I need to clone. I label them with adhesive tape (e.g. "Main door EM4100", "Parking HID FC:42 CN:500"). On engagement day I have everything ready in my pocket.

---

### T5577 Raw Writer

Advanced tool for direct writing to T5577 registers, bypassing protocol decoding.

#### How It Works

1. Open `T5577 Raw Writer`
2. Select the block to write (0-7, Page 0 or Page 1)
3. Enter the 32-bit value in hexadecimal
4. Place the T5577 on the Flipper
5. The app writes the specified block

#### Advanced Usage

**Writing Block 0 (configuration):**
- Allows manual configuration of modulation, data rate, number of blocks
- Useful for protocols not natively supported by the Flipper
- **WARNING:** an incorrect Block 0 can render the T5577 unreadable

**Writing data blocks:**
- Enter raw data directly without going through a .rfid file
- Useful for replicating data obtained from a Proxmark3 or external analyzer

**Setting a password:**
- Write Block 7 with the desired password
- Then write Block 0 with the PWD bit (bit 29) set to 1
- From now on every write will require the password

**Recovering a T5577:**
- If a T5577 has a corrupted Block 0 and does not respond normally
- Try writing Block 0 with a known-good configuration (e.g. 0x00148040 for EM4100)
- If protected by an unknown password: a Proxmark3 is needed for brute force (the Flipper does not support T5577 password cracking)

#### Practical Example: Configuring a T5577 as EM4100 from Scratch

```
1. Write Block 0: 0x00148040
   (ASK/Manchester, RF/64, 2 blocks, no password)

2. Write Block 1: 0xFF01020304
   (first 32 bits of the EM4100 frame: 9x1 header + first nibbles)

3. Write Block 2: 0x0506070800
   (last nibbles + column parity + stop bit)

Result: the T5577 behaves as an EM4100 with ID 01:02:03:04:05
```

> **Personal note:** The Raw Writer is the tool I use when the standard method does not work. Once I had a tag from an industrial access control system that the Flipper read as "Unknown protocol". With the Proxmark3 I decoded the raw data and the configuration. Then with the Raw Writer I wrote exactly those values to a T5577 - and it worked. It is the tool for when you need to go low-level and cannot rely on automation.

---

### DCF77 Clock Sync

Receiver and decoder for the DCF77 time signal.

#### What Is DCF77

DCF77 is a radio signal transmitted at 77.5 kHz from the Mainflingen station (Germany). It carries date and time information with atomic precision and is used by millions of radio-controlled clocks in Europe.

#### Technical Characteristics

- **Frequency:** 77.5 kHz (not exactly 125 kHz but within the LF range)
- **Modulation:** ASK with 25% amplitude reduction
- **Frame:** 1 minute = 59 bits (1 bit per second)
- **Range:** ~2000 km from Germany
- **Precision:** microsecond (derived from cesium atomic clock)

#### DCF77 Frame Structure (59 bits)

| Second | Field | Description |
|---|---|---|
| 0 | Start | Minute start (no reduction) |
| 1-14 | Weather | Encrypted weather data |
| 15 | Antenna | Backup antenna active |
| 16 | CEST/CET | Daylight saving time change imminent |
| 17-18 | Timezone | 01=CET, 10=CEST |
| 19 | Leap | Leap second imminent |
| 20 | Start time | Always 1 (time block start) |
| 21-27 | Minutes | BCD (0-59) + parity |
| 28 | P1 | Minutes parity |
| 29-34 | Hours | BCD (0-23) + parity |
| 35 | P2 | Hours parity |
| 36-41 | Day | BCD (1-31) |
| 42-44 | Day of week | 1=Mon ... 7=Sun |
| 45-49 | Month | BCD (1-12) |
| 50-57 | Year | BCD (00-99) |
| 58 | P3 | Date parity |

#### Usage on the Flipper

1. Open `DCF77 Clock Sync`
2. The Flipper uses the LF antenna as a passive receiver
3. It decodes bits one at a time (requires ~1 minute for a complete frame)
4. Displays the decoded date and time
5. In Italy the signal is receivable but with variable quality (distance from Germany)

#### Practical Use

- Studying the DCF77 protocol
- Verifying reception in your area
- Debugging radio-controlled clocks
- Understanding BCD encoding and time signals

---

### DCF77 Transmitter

Artificial DCF77 signal generator.

#### How It Works

1. Open `DCF77 Transmitter`
2. Set the desired date and time (or use the Flipper's current time)
3. Start transmission
4. The Flipper generates a DCF77 signal at 77.5 kHz via the LF antenna
5. Radio-controlled clocks within a few centimeters will synchronize

#### Practical Use

- **Testing radio-controlled clocks:** force synchronization with a specific time
- **Debugging:** verify that a clock correctly decodes DCF77
- **Demonstration:** show how a time signal can be spoofed
- **Time setting:** set the correct time on clocks that cannot receive DCF77 in their area

#### Range and Limitations

- The Flipper's range as a DCF77 transmitter is a few centimeters (1-5 cm)
- The real DCF77 signal has a power of 50 kW - the Flipper generates milliwatts
- Works only with clocks placed very close to the Flipper
- Does not interfere with the real DCF77 signal (too weak)

> **Personal note:** The DCF77 Transmitter is fun but of almost zero utility in pentesting. I used it exactly once to synchronize an old desk clock that could not pick up the signal. As a proof-of-concept for time signal spoofing it is interesting, but in practice there are no real attack scenarios with the Flipper's range.

---

### NFC/RFID Detector

Passive detector for NFC (13.56 MHz) and RFID (125 kHz) fields.

#### How It Works

1. Open `NFC/RFID Detector`
2. The Flipper activates the antennas in passive receive mode (does not generate a field)
3. The screen shows two indicators:
   - **LF (125 kHz):** field intensity bar for detected LF field
   - **HF (13.56 MHz):** field intensity bar for detected HF field
4. Bring the Flipper close to potential readers
5. If a field is detected, the corresponding indicator lights up

#### Interpreting Results

| Detected field | Meaning |
|---|---|
| LF only | RFID 125 kHz reader (traditional badge) |
| HF only | NFC 13.56 MHz reader (MIFARE, iCLASS, etc.) |
| LF + HF | Dual-frequency reader (supports both) |
| None | No active reader nearby / reader powered off |

#### Use in Pentesting

**Access point mapping:**
1. Walk through the target building's corridors with the Detector active
2. Note every point where you detect a field (door, turnstile, elevator)
3. Classify readers by type (LF/HF/dual)
4. This map is essential for planning the engagement

**Identifying hidden readers:**
- Readers behind plaster or panels
- Readers recessed in door frames
- Disguised readers (looking like light switches, cover plates)
- Readers in unexpected locations (drawers, lockers)

**Technology assessment:**
- Pure LF = legacy system, probably clonable
- Pure HF = more modern system, may have encryption
- Dual = system undergoing migration or high security

> **Personal note:** The Detector is the FIRST tool I use in a physical pentest engagement. Before any read or emulation attempt, I map the entire building. In 5 minutes of walking I know exactly how many readers there are, where they are, and what type they are. In a bank engagement, I discovered an LF reader hidden behind a decorative panel next to the vault entrance - the Detector picked it up at 10 cm even through the panel. It was a legacy EM4100 system that no one had ever upgraded, despite the rest of the bank using HID iCLASS SE. That forgotten reader was the most critical vulnerability in the entire system.

---
