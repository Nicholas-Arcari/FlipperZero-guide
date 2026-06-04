## Attacks and Countermeasures

### Attack Vectors

**1. Direct Cloning**

The simplest and most common attack:

- **Requirements:** Physical access to the key for 2-3 seconds
- **Tools:** Flipper Zero, or any iButton duplicator (~20-30 euro)
- **Complexity:** None - anyone can do it
- **Success rate:** ~99% for DS1990A
- **Countermeasure:** None effective at the protocol level - DS1990A transmits in clear text by design

**Cloning scenarios:**
- Key left unattended (desk, keychain set down)
- Key briefly lent ("can I borrow it for a second to open?")
- Key stolen, cloned, and returned without the owner noticing
- Locksmith/duplicator that retains codes of all duplicated keys

**2. Replay Attack**

Technically, every iButton emulation is a replay attack:

- The Flipper reads the ROM code from the original key
- It reproduces it identically on the reader
- No challenge-response exists, so the replay always works
- There is no timestamp, nonce, or counter - the code is static and permanent

**3. Bruteforce / Fuzzing**

Attack without access to the original key:

**On Cyfral (8 bit):**
- 256 combinations
- ~2-4 minutes with automated fuzzer
- Success rate: ~100% (all combinations are tested)
- It's the equivalent of trying all combinations on a 3-digit padlock

**On Metakom (32 bit):**
- ~4.29 billion combinations
- Complete bruteforce impractical (~45 years)
- Targeted fuzzing with partial information: hours-to-days
- Success rate: depends on the quality of preliminary information

**On Dallas (48 bit effective serial):**
- ~281 trillion combinations
- Complete bruteforce absolutely impossible (~1.78 million years)
- Targeted fuzzing: only possible with very specific information (e.g., known serial range)
- Strategy: if you know one key from the building, try adjacent serials

**4. Key Database Extraction**

Attack on the reader/controller rather than the key:

- Some cheap iButton readers store the authorized code database in an unprotected EEPROM
- With physical access to the reader (by unscrewing the panel), you can read the EEPROM with a programmer
- The database contains all authorized ROM codes in clear text
- Once the database is extracted, you can create clones of all keys in the building

**Countermeasures:**
- Readers with password-protected EEPROM (rare in budget models)
- Readers with non-extractable internal memory
- Anti-tamper seals on the reader panel
- Surveillance cameras on the reader area

**5. Line Interception**

Man-in-the-middle attack on the 1-Wire bus:

- The 1-Wire bus between the reader and the iButton is physically accessible
- A tap on the wire (DQ and GND) allows sniffing all communications
- Every time a resident uses their key, the ROM code is transmitted in clear text
- With a hidden microcontroller near the reader, you can passively record all codes

**Practical implementation:**
- An Arduino/ESP32 with two wires connected to the reader's probe
- The microcontroller passively listens on the 1-Wire bus
- Records every ROM code that transits
- In a few weeks you've collected the codes of all residents

**Countermeasures:**
- Periodic inspection of the reader's wiring
- Anti-tamper seals on the probe
- Electrical signal monitoring on the line (anomalies = possible tap)

### Effective Countermeasures

**Level 1 - Mitigation (low cost):**
- Visible cameras at entrances (deterrent)
- Periodic audit of keys in circulation
- Key revocation procedure for former residents
- Adequate lighting in the reader area
- Anti-tamper seals on reader panels

**Level 2 - Improvement (medium cost):**
- Migration to NFC system with MIFARE DESFire (AES encryption)
- System with challenge-response (the key never transmits the ID in clear text)
- Access log with timestamps (who opened, when)
- Reader with rate limiting and anti-bruteforce lockout

**Level 3 - Advanced protection (high cost):**
- Multi-factor authentication (key/card + PIN)
- IP video intercom with facial recognition
- Centralized access system with remote management
- Integration with building alarm system
- Virtualized cards on smartphone (elimination of physical medium)

> **Personal note:** The reality is that most Italian apartment buildings with iButton will never adopt Level 2 or 3 countermeasures - the cost is too high and the risk perception is too low. My pragmatic approach in the report is always to suggest Level 1 countermeasures as an immediate priority (cameras, key revocation) because they are inexpensive and have a real impact on risk. I suggest the technology migration as a medium-to-long-term plan, to be implemented when the current system requires maintenance or replacement due to obsolescence.

---
