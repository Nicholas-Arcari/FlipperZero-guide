## Troubleshooting and Limitations

### Common Problems and Solutions

**Problem: "The key is not being read"**

Probable causes and solutions:

1. **Insufficient contact**
   - Solution: clean the Flipper's pad and the key with isopropyl alcohol
   - Check that there are no glue, paint, or oxidation residues
   - Press harder - direct metal contact is required
   - Reposition - the pad must be centered on the key

2. **Not an iButton key**
   - Some token-shaped keys use different protocols (e.g., RFID 125 kHz in token form factor)
   - The Flipper only recognizes Dallas, Cyfral, and Metakom
   - Verify that the key is actually iButton/1-Wire

3. **Damaged key**
   - Very old keys or keys exposed to corrosion may have internal chip damage
   - Try the key on the original reader - if it doesn't work there either, it's broken
   - Severe surface oxidation: gently sand with ultra-fine sandpaper (2000 grit)

4. **Electrical interference**
   - Rare, but in industrial environments with strong EMI the 1-Wire bus can have issues
   - Move away from interference sources
   - The Flipper has good noise immunity, but it's not perfect

**Problem: "The read shows the wrong protocol"**

Probable causes:

1. **Intermittent contact**
   - An unstable contact can cause protocol decoding errors
   - Stabilize the contact and re-read
   - If the result is inconsistent (sometimes Dallas, sometimes Cyfral), the problem is the contact

2. **Multi-protocol key** (rare)
   - Some newer generation keys support multiple protocols
   - Read multiple times and compare results

**Problem: "The emulation doesn't work on the reader"**

Probable causes and solutions:

1. **Incorrect positioning**
   - The Flipper's pad must be centered on the reader's probe
   - Press firmly - the contact must be stable
   - For readers with a recessed "button-style" probe: press hard to make contact with the Flipper's pad

2. **Incompatible reader**
   - Some readers have specific impedance requirements
   - The Flipper's emulation may not meet the electrical specifications of all readers
   - Try with a physical clone (RW1990) - if the clone works but emulation doesn't, the reader is impedance-sensitive

3. **Incorrect original read**
   - If the original read was corrupted (wrong bit due to unstable contact), the emulation will have a wrong code
   - Re-read the original key and compare with the previous read

4. **Reader with anti-emulation** (rare)
   - Some modern readers verify the electrical characteristics of the device
   - They detect that the Flipper's impedance is different from a real iButton key
   - Solution: use a physical clone (RW1990) which has electrical characteristics identical to the original

**Problem: "Writing to RW1990 fails"**

Probable causes and solutions:

1. **Unstable contact during writing**
   - Writing requires stable contact for 3-5 continuous seconds
   - Any interruption corrupts the write
   - Use a flat surface, place the Flipper face down with the RW1990 underneath

2. **Defective RW1990 tag**
   - Cheap tags have a 5-10% defect rate
   - Try with another tag
   - If no tag works: it could be a Flipper issue (update firmware)

3. **Already locked tag**
   - Some RW1990s support a "lock bit" that prevents further writes
   - If the tag has been locked, it cannot be rewritten - use a new tag

4. **Family code not 0x01**
   - The standard Write function is designed for DS1990A (family code 0x01)
   - To write other family codes, you may need custom firmware

**Problem: "The fuzzer finds nothing"**

Probable causes:

1. **Keyspace too large**
   - For Dallas (48 bit): the fuzzer will find nothing in reasonable time - it is mathematically impossible
   - For Metakom (32 bit): it would take years - narrow the range if you have information
   - For Cyfral (8 bit): if it doesn't find anything in 5 minutes, the problem is elsewhere

2. **Unstable contact during fuzzing**
   - The fuzzer requires continuous and stable contact
   - If contact is interrupted, the fuzzer skips codes
   - Find a stable position and hold it

3. **Reader with rate limiting**
   - The reader imposes an increasing delay after failed attempts
   - This enormously slows down fuzzing
   - Try disconnecting and reconnecting contact every 10-20 attempts to reset the reader's timer

4. **Reader with lockout**
   - The reader locks completely after N failed attempts
   - Wait for the unlock timeout (typically 30-120 seconds)
   - Resume fuzzing after unlock

5. **Empty database or powered-off system**
   - Verify that the reader is powered and functional
   - Try with a known key - if that doesn't work either, the reader is broken or off

### General Limitations of the Flipper's iButton Module

**Hardware limitations:**
- The iButton pad is small - it can be difficult to center it on probes of large or recessed readers
- Physical contact is mandatory - no wireless read/emulation
- The Flipper's battery drains during prolonged emulation

**Firmware limitations:**
- Only three protocols supported: Dallas, Cyfral, Metakom
- No support for iButton with memory (DS1991, DS1996, etc.)
- No support for iButton with sensors (DS18B20, etc.) in the standard iButton app
- The fuzzer does not support advanced patterns or scripting

**Operational limitations:**
- You must have physical access to the key OR to the reader
- Emulation requires the Flipper in hand - you cannot "launch" a remote attack
- Fuzzing is slow (2-5 attempts/second) compared to a digital attack
- Physical contact makes fuzzing very visible - it is not a discreet attack

**Comparison with alternative tools:**

| Tool | Advantages | Disadvantages |
|---|---|---|
| **Flipper Zero** | All-in-one, portable, friendly interface | Small pad, only 3 protocols, no memory iButton |
| **Generic iButton duplicator** | Cheap (~20 euro), compact, dead simple | Cloning only, no fuzzing, no analysis |
| **Arduino + 1-Wire reader** | Flexible, scriptable, inexpensive | Requires assembly, not portable |
| **Proxmark3** | Powerful, supports many protocols (with adapter) | Expensive, bulky, steep learning curve |
| **Bus Pirate** | Detailed protocol analysis, sniffing | Not designed for iButton, complex configuration |

> **Personal note:** The Flipper Zero is the best tool for a first iButton assessment - you pull it from your pocket, read the key, emulate, and demonstrate the vulnerability in 30 seconds. For more in-depth analysis (bus sniffing, non-standard protocol analysis, complex attack scripting), I switch to Arduino with the OneWire library. But for 90% of building audits, the Flipper is more than sufficient.

---

## Personal Experience

### Operational Case Studies

> **Personal note:** After years of auditing iButton systems, I've developed a workflow that works in 95% of cases:
>
> 1. Read the client's key (10 seconds)
> 2. Immediate emulation for verification (30 seconds)
> 3. Clone onto RW1990 (2 minutes)
> 4. Test the clone on all entrances (5 minutes)
> 5. If the system is Cyfral: quick fuzzing for bruteforce demonstration (3 minutes)
> 6. Photo documentation (5 minutes)
>
> Total time: 15-20 minutes for a complete iButton audit. It's the fastest Flipper module in terms of time to complete an assessment - NFC and Sub-GHz require much more time.

> **Personal note:** The kit I bring for iButton audits is minimal:
>
> - Flipper Zero (obviously)
> - 10x blank RW1990 tags (in an anti-static bag)
> - Cloth with isopropyl alcohol to clean contacts
> - Tweezers for handling small tags
> - Power bank (the Flipper runs out of battery)
> - Pre-printed authorization forms (in case the building manager hasn't already signed)
>
> Everything fits in a pocket. It's the thing I love about iButton - zero extra equipment.

> **Personal note:** The most common mistake I see in junior pentesters with iButton is not cleaning the contacts. The Flipper's pad gets dirty with use - fingerprints, dust, residue. After 10-20 reads, the metal surface has an invisible film that degrades electrical contact. A quick wipe with isopropyl alcohol before every work session eliminates 80% of reading problems.

> **Personal note:** A story I always tell clients: during an audit in Rome, I found an 80-unit apartment building where the iButton system had been installed since 2003. The building manager had NEVER revoked a key - there were 120 active keys in the database for 80 apartments. 40 extra keys belonged to former residents who had sold their apartments and left, taking their key (or clone) with them. When I presented this finding, the assembly voted unanimously to replace the system. I didn't even need to demonstrate cloning - the management issue was already sufficient.

> **Personal note:** On Cyfral fuzzing - my personal record is 47 seconds to find a valid code on a CCD-2094 reader during an authorized audit in Bologna. The code was 0x1A, meaning the 26th out of 256 - pure luck. But even in the worst case (code 0xFF, last in the sequence), it would have been less than 3 minutes. When I present these numbers to clients, the effect is immediate: "our security system can be breached in 3 minutes by anyone with a 200-euro device." That's a message that comes through loud and clear.

> **Personal note:** An aspect that doesn't get enough consideration: locksmiths and key duplication centers. Many shops in Italy offer iButton duplication service for 5-10 euro. The process is identical to what I do with the Flipper - they read the key, copy it onto an RW1990. The point is that they don't verify the identity of whoever brings the key. Anyone can walk in with a neighbor's key and get a copy made. This is a real-world attack vector that requires zero technical skill - just temporary access to the key and 5 euro.

> **Personal note:** Comparison with NFC and RFID for access system pentesting:
>
> - **iButton:** the easiest to clone (no encryption, physical contact = reliable read), but requires physical access to the key. Assessment in 15 minutes.
> - **RFID 125 kHz (EM4100):** equally easy (no encryption), read from a few centimeters without contact. Assessment in 15 minutes.
> - **NFC (MIFARE Classic):** moderately difficult (crypto-1 broken but requires dictionary attack or MFKey32). Assessment in 30-60 minutes.
> - **NFC (MIFARE DESFire):** difficult (AES encryption, challenge-response). Assessment may not produce results.
>
> In terms of client impact, the iButton demonstration is the most convincing because the physical clone (RW1990) is tangible - the client holds the "fake key" that opens their entrance in their hand. With NFC and RFID, emulation is less tangible and harder to explain to a non-technical person.

> **Personal note:** Final practical tip - if you have an apartment building with an iButton system and want to improve security without replacing the entire installation, the most economical solution is to add a **second factor**. Some installers propose pairing the iButton reader with a 4-digit PIN keypad. The resident must touch the key AND enter the PIN. This doesn't solve the cloning problem (the PIN can be observed), but it significantly raises the barrier - an attacker needs both the key clone and the PIN. Cost: 50-100 euro per reader. It's not perfect, but it's much better than iButton alone.

---

## Technical References

### Official Documentation

- **Dallas Semiconductor / Maxim Integrated:** Application Note AN937 - "Book of iButton Standards"
- **Maxim Integrated:** DS1990A Datasheet - "Serial Number iButton"
- **Dallas Semiconductor:** Application Note AN126 - "1-Wire Communication Through Software"
- **Dallas Semiconductor:** Application Note AN187 - "1-Wire Search Algorithm"
- **Maxim Integrated:** Application Note AN27 - "Understanding and Using Cyclic Redundancy Checks with Maxim iButton Products"

### Standards and Protocols

- **1-Wire Protocol:** Dallas Semiconductor proprietary protocol (now public), specifications in the "Book of iButton Standards"
- **DOW CRC-8:** Polynomial x^8 + x^5 + x^4 + 1 (0x31), documented in AN27
- **MicroCAN Package:** F5 mechanical standard for iButton (16 mm diameter, 3.3 mm height)

### Tools and Resources

- **Flipper Zero Firmware:** https://github.com/flipperdevices/flipperzero-firmware - iButton module source code
- **OneWire Library (Arduino):** https://github.com/PaulStoffregen/OneWire - 1-Wire library for Arduino/ESP
- **iButton Programmer (DIY):** Arduino Nano + 1-Wire reader for programming RW1990 without Flipper
- **Flipper Zero Documentation:** https://docs.flipper.net/ - official documentation
