## Tool by Tool - Operational Guide

### iButton - Main Hub (Read / Emulate / Write)

The Flipper Zero's iButton hub is the starting point for all contact key operations. From the Flipper's main menu:

**Navigation:** Menu → iButton

**Available options:**

- **Read** - Read iButton keys
- **Saved** - Manage saved keys
- **Add Manually** - Manually create a key

#### Read - Key Reading

Complete operational procedure:

**1. Preparation:**
- Make sure the iButton pad on the back of the Flipper is clean
- Make sure the key to be read is clean (no oxidation, no dirt)
- Open Menu → iButton → Read

**2. Positioning:**
- Flip the Flipper upside down (screen facing down)
- Place the iButton token centered on the metal pad on the back
- Press firmly - metal-to-metal contact is required
- Maintain pressure

**3. Reading:**
- The Flipper automatically tries all supported protocols (Dallas, Cyfral, Metakom)
- On success, the screen shows:
  - Detected protocol (DS1990, Cyfral, Metakom)
  - Key ID (in hexadecimal)
  - For Dallas: family code + serial + CRC
- If the read fails: "Not Found" - reposition the key and try again

**4. Saving:**
- After the read, press the right button to save
- Assign a descriptive name (e.g., "Home_Intercom", "Office_Floor2")
- The file is saved in `/ext/ibutton/` with the `.ibtn` extension

**5. .ibtn file format:**

The saved file is a text file with this structure:

```
Filetype: Flipper iButton key
Version: 1
# Key type can be Dallas, Cyfral, Metakom
Protocol: Dallas
Rom Data: 01 A3 5F 2B 00 00 00 E7
```

For Cyfral:
```
Filetype: Flipper iButton key
Version: 1
Protocol: Cyfral
Key Data: AB CD
```

For Metakom:
```
Filetype: Flipper iButton key
Version: 1
Protocol: Metakom
Key Data: AB CD EF 01
```

> **Personal note:** My standard workflow during an audit is to read the key, save it with a name that includes the date and location (e.g., "2024-03-15_Building_ViaRoma_12"), and then immediately emulate to verify that the read is correct. If the emulation works on the reader, the read is valid. If it doesn't work, the problem is almost always dirty contacts during the read - clean and re-read.

#### Emulate - Key Emulation

Emulation turns the Flipper Zero into a virtual iButton key - the pad on the back of the Flipper transmits the saved ROM code when placed on a reader.

**Operational procedure:**

**1. Key selection:**
- Menu → iButton → Saved → select the key to emulate
- Or: after a read, select "Emulate" directly

**2. Activating emulation:**
- The screen shows "Emulating" with the key name and protocol
- The Flipper is now in slave mode - it awaits a reset pulse from the reader

**3. Positioning on the reader:**
- Flip the Flipper upside down (screen facing down)
- Place the Flipper's iButton pad on the reader's probe
- Press firmly to make contact
- The reader sends the reset pulse, the Flipper responds with presence and ROM code
- If the code is in the reader's database: action (opening, unlock)

**4. Timing:**
- Emulation is active as long as the screen shows "Emulating"
- You must maintain contact for at least 1-2 seconds
- Some readers require 3-5 seconds of continuous contact
- If the reader doesn't respond: reposition, clean the surfaces, try again

**Notes on emulation:**

- Emulation works for all three protocols (Dallas, Cyfral, Metakom)
- The Flipper automatically generates the correct signal based on the file's protocol
- Emulation is very reliable for Dallas - success rate ~95%
- For Cyfral and Metakom the success rate is slightly lower (~85-90%) because some readers are sensitive to impedance variations
- Emulation consumes battery - the iButton pad must be powered

> **Personal note:** iButton emulation is the most reliable among all Flipper emulations - much more so than NFC emulation, which has field and timing issues. The direct physical contact eliminates the distance and coupling problems that plague RF emulations. If the key was read correctly and the reader works, emulation always works. The only issue is physical contact - you need to center the Flipper's pad well on the reader's probe.

#### Write - Writing to Writable Tags

The Write function programs writable tags (RW1990) with the ROM code of a saved key.

**Operational procedure:**

**1. Prerequisites:**
- You must have a saved key (previous read or manual creation)
- You must have a writable tag:
  - **RW1990** for Dallas keys
  - There is no writable equivalent for Cyfral/Metakom - for those protocols, emulation is the only "copy" option

**2. Procedure:**
- Menu → iButton → Saved → select the key → Write
- The screen shows "Writing..."
- Place the RW1990 tag on the Flipper's iButton pad
- Maintain contact for 3-5 seconds
- The Flipper programs the ROM code
- Confirmation message "Written!" if the write succeeds

**3. Verification:**
- After writing, read the programmed tag (Read) to verify
- Compare the read ROM code with the original - they must be identical
- Test the tag on the target reader for operational confirmation

**4. Common writing problems:**
- **"Write Failed":** insufficient contact, non-writable tag (original DS1990A), locked tag
- **Different ROM code after write:** defective or low-quality tag
- **Written tag doesn't work on the reader:** possible CRC error - rewrite

> **Personal note:** Writing to RW1990 from the Flipper is less reliable than reading - about 1 out of 10 times I need to repeat the procedure. The trick is to maintain very stable contact throughout the entire write duration, without moving the key on the pad. If you have cheap RW1990 tags (the 0.30 euro ones from AliExpress), expect a 5-10% defective rate of tags that won't program - throw them away and use the next one.

#### Add Manually - Manual Creation

You can create an iButton key from scratch by manually entering the ID:

**Procedure:**
- Menu → iButton → Add Manually
- Select the protocol (Dallas, Cyfral, Metakom)
- Enter the code byte by byte using the Flipper's interface
- Save with a descriptive name

**Use cases:**
- You have the key ID written on a sticker (some installers do this)
- You obtained the code from a database or system dump
- You want to create a key with a specific ID for testing
- You're preparing a set of keys for fuzzing

### iButton Converter - Cross-Protocol Conversion

The iButton Converter is a tool for converting keys between different formats. It is useful when a system accepts a specific protocol but you have the key in another format.

**Available conversions:**

- **Cyfral → Dallas:** converts a Cyfral code to an emulable DS1990A format
- **Dallas → Cyfral:** converts a Dallas code to Cyfral format
- **Metakom → Dallas:** converts a Metakom code to Dallas format
- **Dallas → Metakom:** converts a Dallas code to Metakom format
- **Cyfral <-> Metakom:** cross-conversions

**How conversion works:**

The conversion is not a direct 1:1 translation - the protocols have different formats and code lengths. The converter:

1. Takes the source code
2. Maps it into the destination protocol format
3. Calculates any necessary checksums/CRC
4. Generates a valid `.ibtn` file for the destination protocol

**When conversion is needed:**

- An intercom has a Dallas reader but the distributed keys are Cyfral (this happens with installations done by mixed companies)
- You're testing a reader's compatibility with different protocols
- You want to verify if a multi-protocol reader responds to all advertised formats

**Operational procedure:**

1. Read the source key (or select a saved file)
2. Open iButton Converter
3. Select the desired conversion (e.g., "Cyfral → Dallas")
4. The converter generates the converted code
5. Save as a new key
6. Test the emulation of the converted key on the target reader

**Conversion limitations:**

- Conversion does not guarantee that the reader will accept the converted code - it depends on the reader's firmware
- Readers that verify only the ID (without checking the protocol) are more permissive
- Readers that also verify the communication protocol will reject converted codes
- The different keyspace between protocols means that not all conversions are reversible

> **Personal note:** The iButton Converter is a niche tool - I use it rarely, perhaps 1 out of 20 iButton operations. The real use case is when an apartment building has a "mixed" system (e.g., multi-protocol reader with both Dallas and Cyfral keys) and you need to understand how the reader handles different formats. It's more of an analysis tool than an attack tool.

### iButton Fuzzer (DS1990 / Metakom / Cyfral)

The iButton Fuzzer is the most aggressive tool in the iButton module - it generates and transmits iButton codes in sequence to test the security of a reader. It is the equivalent of a bruteforce attack on physical access.

**Operating principle:**

The fuzzer generates iButton codes (ROM code for Dallas, codes for Cyfral/Metakom) and emulates them in rapid succession on the target reader, attempting to find a valid code in the reader's database.

**Available modes:**

**1. Random:**
- Generates random codes on each attempt
- Useful for statistical testing and for verifying the reader's reaction to invalid codes
- No guarantee of finding a valid code - probability is a function of keyspace and number of codes in the reader's database

**2. Sequential:**
- Increments the code by 1 on each attempt (or according to a defined pattern)
- Traverses the code space in order
- More systematic than random but more predictable

**3. Custom:**
- The user defines a range or set of codes to try
- Useful when you have partial information about the target (e.g., you know the family code, or you know the building's serials start with a specific prefix)

**Timing between attempts:**

The time between one attempt and the next depends on:
- **Reset/presence/read time:** ~1-2 ms for a complete 1-Wire cycle
- **Reader response time:** variable, typically 100-500 ms
- **Reader recovery time:** some readers impose an anti-bruteforce delay

In practice, the maximum rate is approximately **2-5 attempts per second** for Dallas, limited by the reader's response time and the need to maintain stable physical contact.

**Keyspace analysis:**

**DS1990A (Dallas):**
- Total keyspace: 2^64 = ~1.8 x 10^19
- Effective keyspace (serial only): 2^48 = ~2.8 x 10^14
- At 5 attempts/second: ~1.78 x 10^6 years to exhaust the keyspace
- **Conclusion:** pure bruteforce is impractical on Dallas

**Cyfral:**
- Base keyspace: 2^8 = 256
- At 2 attempts/second: ~128 seconds to exhaust the keyspace
- **Conclusion:** bruteforce is absolutely practical - approximately 2 minutes

**Metakom:**
- Keyspace: 2^32 = ~4.29 x 10^9
- At 3 attempts/second: ~45 years to exhaust the keyspace
- **Conclusion:** pure bruteforce is impractical, but reduced ranges are feasible

**Operational procedure - DS1990 Fuzzing:**

1. Menu → iButton Fuzzer → DS1990
2. Select the mode:
   - Random: generates random IDs with family code 0x01 and valid CRC
   - Sequential: starts from a base ID and increments
   - Custom: enter a prefix or a range
3. Flip the Flipper upside down and place the pad on the target reader
4. Start fuzzing - maintain stable physical contact
5. The screen shows the current code and the attempt counter
6. If the reader responds positively (opens the door), the code is saved automatically

**Operational procedure - Cyfral Fuzzing:**

1. Menu → iButton Fuzzer → Cyfral
2. Select the mode (for Cyfral, sequential is the most effective given the reduced keyspace)
3. Place the pad on the Cyfral reader
4. Start - the fuzzer traverses all 256 possible codes
5. Estimated time: 2-4 minutes to exhaust the entire keyspace
6. If it finds a valid code, it saves automatically

**Operational procedure - Metakom Fuzzing:**

1. Menu → iButton Fuzzer → Metakom
2. Select the mode (custom with a reduced range is the best choice)
3. If you have information about the target, narrow the range
4. Place the pad on the Metakom reader
5. Start - for a range of 1000 codes, approximately 5-8 minutes
6. For the complete keyspace: impractical, use information to narrow down

**Anti-fuzzing reader countermeasures:**

Some modern readers implement protections:
- **Rate limiting:** increasing delay after N failed attempts
- **Lockout:** temporary block after N failed attempts (typically 10-30 seconds)
- **Alarm:** audible/visual alert after repeated attempts
- **Logging:** recording of failed attempts (rare in budget intercoms)

> **Personal note:** iButton fuzzing is extraordinarily effective on Cyfral - 256 combinations are nothing. I've opened Cyfral intercoms in under 3 minutes during authorized audits. For Dallas, pure fuzzing is useless - you'll never exhaust 2^48 combinations. However, there's a trick: many installers use keys with sequential serials (purchased in batch from the same production run). If you recover one key, try adjacent serials - I've found apartment buildings where all keys had serials in the range XX:XX:XX:00:00:01 - XX:XX:XX:00:00:60 (96 units). In that case, range-based fuzzing is devastating.

---
