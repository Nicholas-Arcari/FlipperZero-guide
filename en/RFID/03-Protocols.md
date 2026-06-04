## Detailed Protocols

### EM4100 (EM-Marin)

The simplest and most widespread protocol in the world for RFID 125 kHz. Originally manufactured by EM Microelectronic (Switzerland), it has become the de facto standard for budget access control.

#### Where It Is Found

- Italian apartment buildings (the vast majority)
- Gyms and sports centers
- Barrier-controlled parking garages
- Office coffee machines
- Budget attendance tracking systems
- Temporary visitor badges
- Electronic lockers
- Pedestrian gates

#### Complete Frame Structure

An EM4100 tag continuously transmits a **64-bit** frame in a loop. The structure is:

```
[9 bit header] [D00][D01][D02][D03][P0]  <- row 0
               [D04][D05][D06][D07][P1]  <- row 1
               [D08][D09][D10][D11][P2]  <- row 2
               [D12][D13][D14][D15][P3]  <- row 3
               [D16][D17][D18][D19][P4]  <- row 4
               [D20][D21][D22][D23][P5]  <- row 5
               [D24][D25][D26][D27][P6]  <- row 6
               [D28][D29][D30][D31][P7]  <- row 7
               [D32][D33][D34][D35][P8]  <- row 8
               [D36][D37][D38][D39][P9]  <- row 9
               [PC0][PC1][PC2][PC3][S0]  <- column parity + stop bit
```

**64-bit breakdown:**

| Field | Bits | Description |
|---|---|---|
| **Header** | 9 bits | All 1s (`111111111`) - synchronization |
| **Data** | 40 bits | 10 rows x 4 bits = 40 bits of actual data |
| **Row Parity** | 10 bits | 1 even parity bit per row (P0-P9) |
| **Column Parity** | 4 bits | 1 even parity bit per column (PC0-PC3) |
| **Stop Bit** | 1 bit | Always 0 (S0) |
| **Total** | 64 bits | |

**The 40 data bits contain:**
- **8 bits** (first 2 rows): Version Number / Customer ID (typically the manufacturer or batch)
- **32 bits** (rows 2-9): Unique tag ID

**Practical example:**
```
Header:    111111111
Row 0:     0001 0    <- nibble 0x1 + parity
Row 1:     0000 0    <- nibble 0x0 + parity
Row 2:     0110 0    <- nibble 0x6 + parity
Row 3:     1010 0    <- nibble 0xA + parity
Row 4:     1111 0    <- nibble 0xF + parity
Row 5:     0011 0    <- nibble 0x3 + parity
Row 6:     1100 0    <- nibble 0xC + parity
Row 7:     0101 0    <- nibble 0x5 + parity
Row 8:     1001 0    <- nibble 0x9 + parity
Row 9:     0010 1    <- nibble 0x2 + parity
Col par:   0110 0    <- column parity + stop

Version: 0x10 = 16
ID: 0x6AFC3C592 (40 bit -> the Flipper displays 5 hex bytes)
```

#### Clock Rate

- **Carrier frequency:** 125 kHz (or 134.2 kHz in variants)
- **Clock divisor:** RF/64 (typical) = 125000/64 = 1953.125 bps
- **Also supported:** RF/32 (3906.25 bps) and RF/16 (7812.5 bps) on compatible tags
- **Full frame transmission time:** 64 bits / 1953 bps = ~32.7 ms
- **The tag repeats the frame** approximately 30 times per second

#### Security: ZERO

EM4100 has **no** form of security whatsoever:
- No encryption
- No authentication
- No challenge-response
- No anti-cloning
- The ID is transmitted in the clear, continuously, without any protection
- Anyone with a 3 EUR reader from AliExpress can read the ID
- Anyone with a 0.50 EUR T5577 can clone it

**This means that ANY access control system based solely on EM4100 should be considered INSECURE.** Cloning takes less than 5 seconds.

> **Personal note:** EM4100 is my bread and butter in physical pentests in Italy. 80% of the apartment buildings I have tested use this protocol, often with readers manufactured by companies like CAME, BPT, URMET and ELVOX. The most baffling thing is that many building administrators do not even know the badges are clonable - they think that because they are "electronic" they are secure. In reality, an EM4100 keyfob offers the same security as a key copied at the hardware store, with the difference that badge copying is instantaneous and leaves no trace.

---

### HID Prox (H10301)

HID Global is the world leader in access control systems. The "Prox" line (125 kHz) is their legacy product but still enormously widespread, especially in enterprise environments.

#### Where It Is Found

- Corporate offices
- Banks and insurance companies
- Hospitals
- Universities
- Data centers (often in combination with other factors)
- Government buildings (especially USA)
- Airports (non-critical zones)

#### 26-bit Format (H10301) - The Most Common

The HID 26-bit format is the industry standard. Structure:

```
[Leading 0] [Parity Even] [Facility Code 8-bit] [Card Number 16-bit] [Parity Odd]
```

**Breakdown:**

| Field | Bits | Range | Description |
|---|---|---|---|
| **Even Parity** | 1 bit (bit 0) | - | Even parity over bits 1-12 |
| **Facility Code** | 8 bits (bits 1-8) | 0-255 | Identifies the building/organization |
| **Card Number** | 16 bits (bits 9-24) | 0-65535 | Identifies the specific card |
| **Odd Parity** | 1 bit (bit 25) | - | Odd parity over bits 13-24 |

**Practical example:**
```
Raw bits:    1 01100100 0000001010110011 0
             P FFFFFFFF CCCCCCCCCCCCCCCC P

Even Parity: 1 (even parity of first 12 data bits)
Facility:    01100100 = 100
Card Number: 0000001010110011 = 691
Odd Parity:  0 (odd parity of last 12 data bits)

On the Flipper you see: HID H10301 FC:100 CN:691
```

#### Modulation and Transmission

- **Modulation:** FSK2 (2-level Frequency Shift Keying)
- **Frequencies:** ~12.5 kHz (RF/10) for 0 and ~15.625 kHz (RF/8) for 1
- **Carrier:** 125 kHz
- **Encoding:** Biphase / Differential Manchester
- **Data rate:** RF/50 = 2.5 kbps

The complete HID frame transmitted over the air is longer than the 26 format bits - it includes a preamble, proprietary HID header and CRC. The Flipper decodes everything automatically and shows only FC and CN.

#### Alternative HID Formats

Beyond the 26-bit H10301, HID supports many other formats:

- **34-bit:** Extended Facility Code
- **35-bit Corporate 1000:** used in large corporations
- **37-bit H10302/H10304:** larger card number
- **48-bit:** OSDP format
- **Custom:** many companies define proprietary formats

The Flipper Zero natively supports the 26-bit H10301 and recognizes most other formats, but may show only raw data for custom formats.

#### Security: VIRTUALLY ZERO

Like EM4100, HID Prox **has no encryption**:
- The ID is transmitted in the clear
- No challenge-response
- No mutual authentication
- Cloning is trivial (identical to EM4100)
- The only "protection" is the Facility Code (easily discoverable)
- HID themselves recommend migrating to iCLASS SE or SEOS (NFC 13.56 MHz)

The only advantage over EM4100 is that the proprietary HID format makes reverse engineering slightly more complex for those without the right tools. But with a Flipper Zero or a Proxmark3, reading is instantaneous.

> **Personal note:** The Facility Code is a goldmine in a pentest. If you read a single HID badge and discover the FC is 42, you can reasonably assume that ALL badges in that building have FC:42. At that point the Flipper's fuzzer can try all 65536 possible Card Numbers. In one engagement I discovered that a hospital was using HID 26-bit with FC:10 and sequential Card Numbers starting from 1. Simply writing FC:10 CN:1 to a T5577 was enough to gain access to the first door. It is impressive how widespread this vulnerability is.

---

### Indala

Indala (now part of HID Global after the acquisition) is a proprietary 125 kHz RFID system that differs significantly from HID Prox.

#### Where It Is Found

- Government and military buildings (especially USA)
- Legacy installations that never migrated to HID Prox
- Some universities and hospitals
- Systems installed before 2005 (when Indala was independent)

#### Technical Characteristics

- **Modulation:** PSK (Phase Shift Keying) - different from HID's FSK
- **Data encoding:** proprietary, not publicly documented
- **Formats:** 26-bit (similar to H10301) and 29-bit (Motorola format)
- **Carrier frequency:** 125 kHz
- **Data rate:** variable, typically RF/32 or RF/64

#### Differences from HID Prox

| Feature | HID Prox | Indala |
|---|---|---|
| **Modulation** | FSK2 | PSK1 |
| **Standard format** | 26-bit H10301 | 26-bit / 29-bit |
| **Encoding** | Biphase | Proprietary |
| **Documentation** | Semi-public | Closed |
| **Prevalence** | Global | Primarily USA |
| **Badge cost** | Medium | High (single vendor) |

#### 26-bit Indala Format

Similar to HID 26-bit but with different encoding and modulation:

```
[Preamble PSK] [Facility Code 8-bit] [Card Number 16-bit] [Checksum]
```

The Flipper Zero reads Indala tags and displays them as "Indala" with raw data. Interpreting the Facility Code and Card Number may require manual analysis for non-standard formats.

#### Security

Identical to HID Prox and EM4100: **no encryption**. The proprietary protocol offers only "security through obscurity", which is not real security. Cloning to T5577 is possible with the Flipper Zero.

> **Personal note:** Indala tags are fairly rare in Italy. I have encountered them in only two engagements: a NATO base and an American company with an Italian branch that had imported the system from headquarters. The Flipper reads them without issues, but emulation can be less reliable compared to EM4100/HID because PSK modulation is more sensitive to timing. When possible, I prefer cloning to T5577 rather than using software emulation for Indala.

---

### FDX-B (ISO 11784/11785)

FDX-B (Full Duplex Type B) is the international standard for electronic animal identification. It is regulated by ISO 11784 (code structure) and ISO 11785 (technical characteristics).

#### Where It Is Found

- Subcutaneous microchips for dogs, cats, horses and other domestic animals
- Livestock identification (mandatory in the EU)
- Wildlife tracking
- Aquariology (identification of valuable fish)
- Mandatory in Italy for all dogs since 2005 (canine registry)

#### Technical Characteristics

- **Frequency:** 134.2 kHz (NOT 125 kHz - important!)
- **Modulation:** ASK / HDX or FDX-B
- **Data rate:** RF/32 = 4193.75 bps
- **Encoding:** NRZ with bit stuffing
- **Type:** passive, read-only (the microchip cannot be rewritten)

#### Frame Structure (128 bits)

The FDX-B frame consists of 128 bits with this structure:

```
[11 bit header] [10 bit data] [1 control] [10 bit data] [1 control] ...
```

**Decoded data structure:**

| Field | Bits | Description |
|---|---|---|
| **Header** | 11 bits | Synchronization pattern `00000000001` |
| **Animal ID** | 38 bits | Unique animal identification number (0 - 274,877,906,943) |
| **Country Code** | 10 bits | ISO 3166 country code (380 = Italy) |
| **Data Flag** | 1 bit | 1 if the tag contains additional data |
| **Animal Flag** | 1 bit | 1 if it is an animal (vs object) |
| **Extra Data** | 24 bits | Supplementary data (breed, vaccinations, etc.) |
| **CRC** | 16 bits | CRC-CCITT for integrity verification |

**Practical example of an Italian microchip:**
```
Animal ID:    123456789012345
Country Code: 380 (Italy)
Animal Flag:  1 (it is an animal)
Data Flag:    0 (no extra data)

Complete code: 380 123456789012345
(15 total visible digits, the first 3 being the country)
```

#### How the Flipper Reads FDX-B

The Flipper Zero can read FDX-B microchips but with significant limitations:

- **The frequency is 134.2 kHz, not 125 kHz** - the Flipper adapts but sensitivity is reduced
- **Very limited range:** 1-2 cm for subcutaneous implants (microscopic chip antenna)
- **To read an animal:** you must position the Flipper exactly on the implant site (typically between the shoulder blades for dogs and cats)
- **The Flipper shows:** Country Code + Animal ID
- **It CANNOT write** real FDX-B microchips (they are OTP - One Time Programmable)

#### Security

FDX-B microchips are read-only (once programmed at the factory they cannot be modified), but:
- The ID is transmitted in the clear without encryption
- It is possible to **emulate** an FDX-B microchip with the Flipper
- It is possible to **write** an FDX-B ID to a T5577 (which operates at 125 kHz though, not 134.2 kHz - it may not work with all readers)
- It is possible to **create** fake FDX-B IDs with the FDX-B Maker

> **Personal note:** Reading animal microchips with the Flipper is possible but frustrating. The range is so limited that you literally have to press the Flipper against the animal's skin at the exact point of the microchip. With a cooperative dog it is doable, with a nervous cat it is practically impossible. For real veterinary use, a dedicated FDX-B reader (like those 30 EUR ones on Amazon) is infinitely more practical. The usefulness of FDX-B support in the Flipper is more for research and study than for practical use.

---

### T5577 - The Universal Tag

The T5577 (manufactured by Atmel, now Microchip Technology) is the most versatile and important 125 kHz RFID tag for any pentester. It is a **programmable and rewritable** tag that can emulate virtually any LF protocol.

#### Why It Is Essential

- Can emulate EM4100, HID Prox, Indala, FDX-B, AWID, Pyramid, Viking, Jablotron and many others
- Rewritable an unlimited number of times (unlike OTP tags)
- Costs 0.30-1 EUR in card, keyfob or coin form
- It is the "blank CD" of the RFID 125 kHz world
- The Flipper Zero uses it as the primary write target

#### Memory Structure

The T5577 has EEPROM memory organized in **2 pages** of **8 blocks** each (7+1 per page):

```
Page 0 (user data):
  Block 0: Configuration Word (32 bit) <-- CRITICAL
  Block 1: Data Word 1 (32 bit)
  Block 2: Data Word 2 (32 bit)
  Block 3: Data Word 3 (32 bit)
  Block 4: Data Word 4 (32 bit)
  Block 5: Data Word 5 (32 bit)
  Block 6: Data Word 6 (32 bit)
  Block 7: Password (32 bit) <-- optional protection

Page 1 (tracing data):
  Block 1: Tracing Data 1
  Block 2: Tracing Data 2
  Block 3: Tracing Data 3
  Block 4: Tracing Data 4
  (Block 0 of Page 1: config mirror)
```

#### Block 0 - Configuration Word (Crucial)

Block 0 of Page 0 is the heart of the T5577. It determines HOW the tag behaves - which protocol it emulates, which modulation it uses, at what data rate it transmits:

```
32-bit Configuration Word bits:

[Bit 0]      Master Key flag
[Bit 1-3]    Reserved
[Bit 4]      POR Delay (Power-On Reset delay)
[Bit 5-9]    Data Bit Rate (divisor: RF/8, RF/16, RF/32, RF/40, RF/50, RF/64, RF/100, RF/128)
[Bit 10-12]  Modulation scheme
               000 = Direct
               001 = PSK1
               010 = PSK2
               011 = PSK3
               100 = FSK1 (RF/8 + RF/5)
               101 = FSK2 (RF/8 + RF/10)
               110 = FSK1a (RF/5 + RF/8)
               111 = FSK2a (RF/10 + RF/8)
[Bit 13]     PSK Clock Frequency
[Bit 14]     Inverse Data
[Bit 15-16]  Modulation (extended)
               00 = ASK/Manchester
               01 = ASK/Biphase
               10 = ASK/Reserved
               11 = NRZ/Direct (no encoding)
[Bit 17]     ST sequence terminator
[Bit 18-20]  Max Block (how many blocks to transmit: 0-7)
[Bit 21]     Password Write (1 = password required for writing)
[Bit 22]     Reserved
[Bit 23]     AOR (Answer On Request - single shot vs continuous)
[Bit 24-27]  Reserved
[Bit 28]     Init Delay
[Bit 29]     PWD (1 = password enabled)
[Bit 30-31]  Reserved
```

#### Common Configurations for Emulation

Here are the Block 0 configuration values to emulate the most common protocols:

**EM4100:**
```
Config: 0x00148040
- Modulation: ASK/Manchester
- Data rate: RF/64
- Max blocks: 2 (Block 1 + Block 2 = 64 bit)
- No password
```

**HID Prox 26-bit (H10301):**
```
Config: 0x00107060
- Modulation: FSK2 (RF/8 + RF/10)
- Data rate: RF/50
- Max blocks: 3
- Encoding: Biphase
```

**Indala 26-bit:**
```
Config: 0x00081040
- Modulation: PSK1
- Data rate: RF/32
- Max blocks: 2
- Encoding: direct
```

**FDX-B:**
```
Config: 0x603E1040
- Modulation: ASK
- Data rate: RF/32
- Max blocks: 4
- Note: some FDX-B readers operate at 134.2 kHz
  and may not read a T5577 at 125 kHz
```

#### Password Protection

The T5577 supports a 32-bit password to protect writing:

- Without password: anyone can overwrite the content
- With password: the password is required to write new data
- The password is stored in Block 7 of Page 0
- **The password does NOT protect reading** - the ID is still transmitted in the clear
- The password only protects against overwriting
- Factory default: 0x00000000 (no password)
- If you forget the password, the tag is unusable (there is no reset)

> **Personal note:** The T5577 is the most powerful tool in a pentester's LF toolkit. I always carry 10-15 T5577s in keyfob and card format in my kit. They cost next to nothing and allow me to clone any 125 kHz badge in seconds. A tip: buy T5577s in bulk from AliExpress (50 pieces for about 15 EUR). Verify they are real T5577s and not EM4100s sold as T5577s - it happens frequently. To verify: a real T5577 is writable, an EM4100 is not. Another tip: after cloning a badge during a pentest, protect the T5577 with a random password. If you lose it, no one will be able to read it and trace it back to the engagement.

---
