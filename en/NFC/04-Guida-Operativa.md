# Operational Guide - Tool by Tool

This section covers every single NFC tool available on the Flipper Zero, with detailed operational procedures, expected outputs, and practical field notes. The order follows a real workflow during a penetration test: reading, analysis, attack, cloning, verification.

---

## NFC (Main Hub)

**Main menu:**
- **Read** - Read an NFC tag (identification + full read attempt)
- **Detect Reader** - Listen to an NFC reader (for MFKey32)
- **Saved** - Manage saved tags
- **Extra Actions** - Additional features
- **Add Manually** - Create a tag from known parameters

---

## Read - Tag Reading

Complete operational procedure:

1. Open NFC → Read
2. Bring the tag/badge close to the Flipper's NFC coil (upper part)
3. The Flipper identifies:
   - Tag type (MIFARE Classic, DESFire, NTAG, etc.)
   - UID (4/7/10 bytes)
   - SAK and ATQA
4. For MIFARE Classic: automatic dictionary attack starts
   - Progress bar for each sector
   - Keys found: sector turns green
   - Keys not found: sector remains red
5. When finished, press Save to store the dump

**The saved .nfc file contains:**
```
Filetype: Flipper NFC device
Version: 4
Device type: Mifare Classic
UID: 04 A3 B2 C1
ATQA: 00 04
SAK: 08
Mifare Classic type: 1K
Data format version: 2
Block 0: 04 A3 B2 C1 C8 08 04 00 62 63 64 65 66 67 68 69
Block 1: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
...
Key A: FF FF FF FF FF FF
Key B: FF FF FF FF FF FF
Access bits: FF 07 80 69
```

### Interpreting the Read Output

| Field | Meaning | What to look for |
|---|---|---|
| **UID** | Unique tag identifier | Length (4/7/10 bytes), sequential patterns across badges |
| **SAK** | Tag type | 0x08 = Classic 1K (vulnerable), 0x20 = DESFire (resistant) |
| **ATQA** | Sub-type | Confirms the type indicated by SAK |
| **Key A/B** | Sector keys | FF FF FF FF FF FF = default keys = weak system |
| **Access bits** | Read/write permissions | FF 07 80 69 = default = permissions not customized |

> **Personal note:** When I read a badge for the first time, the first thing I check is the SAK. SAK 0x08 tells me immediately that I'm dealing with a MIFARE Classic 1K - 90% of the time it means a full dump within 5 minutes. If I see SAK 0x20, I know I'm looking at hours of work and will probably need the Proxmark3.

---

## Detect Reader - For MFKey32

Procedure for capturing data from the reader:

1. Open NFC → Detect Reader
2. The Flipper waits in listening mode
3. Bring the Flipper close to an active NFC reader
4. The reader attempts to authenticate with the "badge" (the Flipper)
5. The Flipper captures: reader nonce, response, encrypted data
6. Repeat 2-3 times
7. Data is saved for MFKey analysis

### Operational Checklist for Detect Reader

| Step | Action | Verification |
|---|---|---|
| 1 | Position the Flipper with the upper part facing the reader | NFC LED blinks |
| 2 | Hold contact for at least 2 seconds | Counter on screen increments |
| 3 | Repeat 2-3 times | At least 2 captures per sector |
| 4 | Check the log | Authentication data present |

> **Personal note:** Detect Reader is a critical phase that requires calm and precision. During an engagement, pretending to be an employee who "is having trouble with their badge" always works - bring the Flipper close to the reader, wait 2 seconds, shake your head as if it didn't work, repeat. Nobody suspects a thing.

---

## Emulate - Tag Emulation

After reading and saving a tag, you can emulate it:

1. Open NFC → Saved → select the file
2. Press Emulate
3. The Flipper behaves like the original tag
4. Bring the Flipper close to the reader → it should respond as if it were the original badge

**Emulation limitations:**
- Works well with readers that only check the UID
- Works with MIFARE Classic if you have the full dump (all keys)
- Does NOT work with DESFire (asymmetric cryptography)
- Some readers have anti-emulation filters based on timing or field level

### Emulation Compatibility Matrix

| Tag Type | UID Emulation | Full Emulation | Notes |
|---|---|---|---|
| MIFARE Classic 1K | Yes | Yes (with full dump) | ~60% of readers accept it |
| MIFARE Classic 4K | Yes | Yes (with full dump) | Same limitations as 1K |
| MIFARE Ultralight | Yes | Partial | Some fields not emulable |
| NTAG 213/215/216 | Yes | Good | Works well for Amiibo and similar |
| DESFire | UID only | No | Cryptography prevents emulation |
| iClass Legacy | Yes | Partial | Depends on the reader |

> **Personal note:** MIFARE Classic emulation works on about 60% of the readers I've tested. The remaining 40% reject it for various reasons: timing too slow, field too weak, or the reader verifies specific data in sectors that I don't have in the dump. For those cases, I use a Magic Card (see [06-Attacchi-e-Difese.md](06-Attacchi-e-Difese.md)) which is an actual physical tag.

---

## MFKey

Suite for MIFARE Classic key recovery.

**Complete MFKey32 procedure:**

1. Read the target badge (NFC → Read) - obtain partial dump
2. Activate Detect Reader → present the Flipper to the reader
3. Repeat 2-3 times
4. Open MFKey from the app menu
5. The app analyzes the captured data
6. Recovered keys are added to the dictionary
7. Re-read the badge with the new keys

**MFKey32v2:** improved version that requires fewer captures and has a higher success rate.

### Complete MFKey32 Workflow

```
Read Badge (partial dump)
        |
        v
  Detect Reader (2-3 captures)
        |
        v
  MFKey → Key calculation
        |
        v
  Keys → Dictionary
        |
        v
  Re-Read Badge (full dump)
        |
        v
  Emulate / Write to Magic Card
```

> **Personal note:** MFKey32 is the attack I use most often in real engagements. It works on roughly 70-80% of the MIFARE Classic systems I've encountered. The trick is presenting the Flipper to the reader naturally - during a social engineering scenario, pretend to be an employee who "is having trouble with their badge" and bring the Flipper close to the reader. It takes 2-3 attempts, 5 seconds each.

---

## MIFARE Classic Editor

Direct editor for MIFARE Classic sectors and blocks.

**Operational procedure:**

1. Open a .nfc file of a MIFARE Classic
2. The editor shows all sectors and blocks
3. Select a block to modify
4. Edit the bytes (hex)
5. Save the changes

**Important blocks:**
- **Block 0:** UID and manufacturer data - not modifiable on normal tags
- **Sector trailer:** A/B keys and access bits - modify with caution!
- **Data blocks:** this is where useful information resides (access ID, credit, counters)

**Use in pentesting:**
- After dumping a badge, modify data to test the system
- Change the access ID to see if the system verifies integrity
- Test whether the system accepts modified data without checksum

### MIFARE Classic 1K Block Map

```
Sector 0:  Block 0 [UID + Manufacturer] | Block 1 [Data] | Block 2 [Data] | Block 3 [KeyA + ACL + KeyB]
Sector 1:  Block 4 [Data] | Block 5 [Data] | Block 6 [Data] | Block 7 [KeyA + ACL + KeyB]
...
Sector 15: Block 60 [Data] | Block 61 [Data] | Block 62 [Data] | Block 63 [KeyA + ACL + KeyB]
```

> **Personal note:** The Editor is essential for reverse engineering badge data. After dumping a badge, I compare the data with a second badge to find differences. Often the room/floor/department number is stored in plaintext in the data blocks - sometimes changing a single byte is enough to go from "floor 2 access" to "all floors access".

---

## MIFARE Fuzzer

Tool for sending non-standard or malformed commands to MIFARE tags/readers.

**Fuzzing modes:**
- **UID fuzzing:** generates random or sequential UIDs
- **Key fuzzing:** tries keys with specific patterns
- **Command fuzzing:** sends malformed ISO14443 commands
- **Data fuzzing:** writes random data to sectors

**Use:**
- Test reader robustness against anomalous input
- Discover unexpected behavior (crashes, authentication bypass)
- Identify readers that accept specific UIDs without data verification

---

## NFC APDU Runner

Manual APDU (Application Protocol Data Unit) command sending to NFC smart cards.

**Technical background:**

APDU is the communication protocol between reader and ISO 7816 smart card:
```
APDU Command:
[CLA] [INS] [P1] [P2] [Lc] [Data] [Le]

Response:
[Data] [SW1] [SW2]

SW1 SW2 = 90 00 → success
SW1 SW2 = 6A 82 → file not found
SW1 SW2 = 69 82 → security not satisfied
```

**Operational procedure:**

1. Open APDU Runner
2. Bring an NFC smart card close
3. Enter the APDU command in hex
4. Send → view the response

**Useful commands:**
```
SELECT (by AID):       00 A4 04 00 [len] [AID]
READ BINARY:           00 B0 [P1] [P2] [Le]
GET DATA:              00 CA [P1] [P2] [Le]
VERIFY PIN:            00 20 00 [P2] [Lc] [PIN]
GET CHALLENGE:         00 84 00 00 [Le]
READ RECORD:           00 B2 [record] [P2] [Le]
```

### APDU Response Code Table

| SW1 SW2 | Meaning | Action |
|---|---|---|
| 90 00 | Success | Command executed successfully |
| 6A 82 | File not found | The specified AID or file does not exist |
| 69 82 | Security not satisfied | Authentication required before this command |
| 6A 86 | Incorrect P1/P2 parameters | Check the command parameters |
| 6D 00 | Instruction not supported | The card does not support this command |
| 6E 00 | Class not supported | Incorrect CLA value |
| 6F 00 | Generic error | Card internal error |
| 61 XX | Data available | Use GET RESPONSE to read XX bytes |
| 6C XX | Incorrect length | Retry with Le = XX |

> **Personal note:** The APDU Runner is indispensable for analyzing unknown smart cards. I use it to enumerate applications present on the card (SELECT with different AIDs) and understand the file system structure. It's the NFC equivalent of a shell on an unknown system - it lets you explore what's inside.

---

## NFC Comparator

Compares two NFC dumps to identify differences.

**Operational procedure:**

1. Dump the badge before the operation (e.g., before going through the turnstile)
2. Dump the badge after the operation (e.g., after going through the turnstile)
3. Open Comparator → load the two files
4. Differences are highlighted byte by byte

**Use in reverse engineering:**
- Identify which sector/block is modified by the system
- Discover counters (value that increments with each use)
- Find timestamps or access logs
- Understand how the system manages credit (prepaid cards)

### Differential Analysis Methodology

| Difference Type | Pattern | Interpretation |
|---|---|---|
| Single incremental byte | 0x0A → 0x0B | Access counter |
| 4-byte block that changes | Variable value | Timestamp or rolling code |
| Single bit flip | 0x00 → 0x01 | Status flag (in/out) |
| Entire different sector | All bytes change | Encrypted data / rolling key |

> **Personal note:** The Comparator is my favorite tool for reverse engineering transit cards. By comparing the dump before and after passing through a turnstile, I can identify exactly where the system writes the remaining credit. In an Italian metro card, the credit was in bytes 6-7 of sector 4, encoded as a 16-bit little-endian integer. Changing those 2 bytes changed the credit. Critical finding.

---

## NFC Dict Manager

MIFARE key dictionary management.

**Procedure:**
1. Open Dict Manager
2. View keys currently in the dictionary
3. Add new keys (from clipboard, from file, manually)
4. Remove obsolete keys
5. Import/export the dictionary

**Best practices:**
- Maintain a custom dictionary with keys found during engagements
- Share (securely) keys among team members
- Organize by system type (hotel, offices, transit)

---

## NFC Magic

Support for "Magic" tags - special tags with writable UID and backdoor commands.

**Magic Card types:**

| Type | Writable UID | Backdoor | Notes |
|---|---|---|---|
| **Gen1 (Chinese Magic)** | Yes, via command | WUPC (40xx) | Detectable by anti-magic readers |
| **Gen2 (CUID)** | Yes, via direct write | None | Not detectable like Gen1, but less compatible |
| **Gen3 (UFUID)** | Yes, once (lockable) | None | Behavior most similar to a real tag |
| **Gen4 (Ultimate Magic)** | Yes, unlimited | GDM (custom) | Most versatile, supports 1K/4K, SAK/ATQA changeable |

**Procedure - Cloning to Gen1 Magic Card:**

1. Read the original badge (full dump required)
2. Place a Gen1 Magic Card on the Flipper
3. NFC → Magic → Write
4. Select the dump to write
5. The Flipper writes all sectors including Block 0 (UID)
6. Verify: read the Magic Card and compare with the original

> **Personal note:** Gen1 Magic Cards are the easiest to use but are detected by modern readers (the reader sends the WUPC command and if the tag responds, it knows it's a Magic). Gen4 (Ultimate Magic) are the best for pentesting - undetectable and fully programmable. They cost about 2-3 euros each on AliExpress. I always keep 10-15 Gen4 Magic Cards in my pentest kit.

---

## NFC Sniffer

Intercepts communication between an NFC reader and a tag.

**Operational procedure:**

1. Position the Flipper between the reader and tag (physically difficult - the gap is only a few cm)
2. Activate NFC Sniffer
3. Present the tag to the reader with the Flipper in between
4. The Flipper captures the exchanged data
5. Save the log for analysis

**Limitations:**
- Physical positioning is very critical
- Does not capture all traffic (packet loss)
- For professional sniffing, use Proxmark3 or HydraNFC

---

## NFC Relay

NFC relay attack - extends the distance between reader and tag.

**How it works:**
- Two Flippers (or Flipper + NFC phone)
- Flipper 1 (Proxy): near the reader, emulates the tag
- Flipper 2 (Relay): near the real badge, reads the tag
- Commands from the reader are forwarded from Proxy to Relay and vice versa
- The reader "thinks" it is communicating directly with the badge

**Security implications:**
- Allows "extending" a badge over unlimited distance (with network)
- An attacker could open a door using the badge of an employee who is in a different room/building
- Defense: relay protection (strict timeouts, distance bounding)

---

## MFDesfire Auth

Authentication tester for MIFARE DESFire.

**Procedure:**
1. Bring a DESFire card close
2. Select the authentication type (DES, 3DES, AES)
3. Enter the key
4. Start the test → success/failure

**Use:**
- Verify whether a DESFire card uses default keys
- Test keys recovered from other sources
- Enumerate applications and files accessible with a key

### Default DESFire Keys to Test

```
00 00 00 00 00 00 00 00                - DES default key
00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  - 3DES default key
00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  - AES-128 default key
```

> **Personal note:** I've been surprised by how many DESFire cards in production still use the default key (all zeros). The system itself is secure, but if whoever configured it leaves the default key, all cryptographic security collapses. Always test default keys first.

---

## Passport Reader

NFC reader for electronic travel documents (eMRTD).

**Technical background:**

Electronic passports contain an NFC chip with:
- **DG1:** MRZ data (first name, last name, date of birth, document number)
- **DG2:** holder's photo (JPEG2000)
- **DG3:** fingerprints (restricted access)
- **DG14/15:** keys for authentication

**Operational procedure:**

1. Open Passport Reader
2. Enter the MRZ data (the string at the bottom of the passport's data page)
3. The MRZ generates the BAC key (Basic Access Control)
4. Bring the passport close to the Flipper
5. The Flipper authenticates via BAC and reads the basic data

**Security:**
- BAC is required → without the MRZ data you cannot read anything
- PACE (Password Authenticated Connection Establishment) is more secure and is used in recent documents
- Data is digitally signed by the issuing country

### MRZ Structure and BAC Key Derivation

```
MRZ Line 1: P<ITAROSSI<<MARIO<<<<<<<<<<<<<<<<<<<<<<<<
MRZ Line 2: YA12345678ITA8001015M3012315<<<<<<<<<<<04

BAC key derived from:
- Document number: YA1234567
- Date of birth: 800101
- Expiry date: 301231
```

> **Personal note:** The Passport Reader is useful for verifying that employee identity documents are authentic during a physical security audit. Digital signature verification confirms the document has not been tampered with. Never use this tool without explicit authorization - reading someone's passport without consent is a criminal offense.

---

## PicoPass / iClass

HID Global iClass/PicoPass tag management.

**Background:**

iClass is the most widespread access control system in enterprise/government environments:
- **iClass Legacy:** known master key → vulnerable, readable by the Flipper
- **iClass SE:** diversified key → not vulnerable to generic attacks
- **iClass SEOS:** latest generation, robust security

**Procedure for iClass Legacy:**

1. NFC → Read → bring the iClass badge close
2. The Flipper identifies it as PicoPass
3. With the known master key, it reads the data
4. Save the dump
5. Emulate or write to a compatible card

> **Personal note:** iClass Legacy badges are surprisingly common even in "secure" buildings. I've found iClass Legacy in banks, government offices, and corporate headquarters that spend thousands of euros on IT security but have never upgraded their badge system. The Flipper reads and clones them in 10 seconds. It's a recurring finding in my reports.

---

## SEADER

Secure Element protocol analyzer for cards with integrated SE.

**Use:** sending specialized APDU commands to explore the Secure Element of payment cards, SIMs, or government smart cards. Requires specific knowledge of the target SE protocols.

---

## UID Brute Smarter

Optimized NFC UID bruteforce.

**How it works:**
- Generates UIDs in sequence or with specific patterns
- Emulates each UID and presents it to the reader
- If the reader accepts (opens the door), the valid UID is found

**When to use it:**
- Systems that verify ONLY the UID without reading tag data
- Systems with predictable UIDs (e.g., sequential badges)
- As a last resort when you cannot obtain the dump

> **Personal note:** Few modern systems verify only the UID, but they exist. I found an access control system in a luxury apartment building that accepted any tag with a UID starting with "04 A3" - it was enough to enumerate the last 2 bytes (65,536 combinations). UID Brute found a valid access in less than an hour.

---

## Cyborg Detector

Subcutaneous NFC implant detector (biohacking).

**Procedure:**
1. Activate the Detector
2. Scan the hand/forearm area (typically between thumb and index finger)
3. If it detects an NFC field, it signals the presence of an implant
4. It can attempt to read the type of implanted tag

---

## NFC Maker / NFC URL

Tools for creating NFC tags with NDEF content.

**NDEF record types:**
- **URL:** opens a link in the browser
- **Text:** displays text
- **WiFi:** automatically configures a WiFi network
- **vCard:** adds a contact
- **Bluetooth pairing:** initiates BT pairing
- **App launch:** opens a specific app

**Use in pentesting:**
- Create malicious NFC tags that redirect to phishing pages
- Tags that configure an evil twin WiFi network
- Tags that launch specific apps for social engineering

---

## NFC E-Ink Tags

Management of NFC tags with integrated e-ink display (e.g., Waveshare, Good Display).

**Procedure:**
1. Bring the e-ink tag close to the Flipper
2. Write the desired content (text, monochrome image)
3. The tag updates the display

---

## NFC Keyboard

Transforms the Flipper into a keyboard emulator via NFC.

**How it works:**
- Program a key sequence
- When the Flipper touches an HID-type NFC reader, it sends the sequence
- Similar to BadUSB but via NFC

**Use:** automatic password or command entry on terminals with an NFC reader.

---

## Other NFC Apps

- **Amusement IC:** reading arcade and amusement park cards
- **MetroFlip:** metropolitan transit card analysis
- **Mi Band NFC:** reading Xiaomi NFC wristband data
- **MiZip Balance Editor:** reading MiZip cards
- **NFC Playlist:** creating multimedia playlists on tags
- **Open Print Tag:** printer tag analysis
- **SLI Writer:** SLI tag writing
- **T-Union Master:** Chinese transit cards
- **TuLlave:** South American transit cards
- **UdECard:** UdE card support
- **VB Migration Assistant:** legacy format migration
- **Weebo:** advanced NFC tools

---

## Operational Workflow Summary

```
1. IDENTIFICATION     →  NFC Read → SAK/ATQA → Tag type
2. READING            →  Dictionary Attack → Partial/full dump
3. KEY RECOVERY       →  MFKey32 (if keys missing) → Detect Reader → Calculation
4. FULL DUMP          →  Re-Read with new keys → Save
5. ANALYSIS           →  Editor + Comparator → Data reverse engineering
6. CLONING            →  Emulate (software) or Magic Card Write (hardware)
7. VERIFICATION       →  Test at target reader → Finding documentation
```

> **Personal note:** This workflow is my standard for every NFC engagement. The most critical phase is 2-3: the dictionary attack + MFKey32. If you can get a full dump, the rest is mechanical. If you can't, you need to switch to the Proxmark3 for more sophisticated attacks. The Flipper covers 80% of real-world scenarios - for the remaining 20%, dedicated equipment is required.
