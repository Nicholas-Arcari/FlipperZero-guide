# NFC Technical Fundamentals

## What is NFC

NFC (Near Field Communication) is a short-range wireless communication technology based on electromagnetic induction at **13.56 MHz**. Unlike Sub-GHz which operates at ranges of tens of meters, NFC works at distances of **a few centimeters** (typically 1-10 cm).

NFC is based on the following standards:

- **ISO 14443 Type A** - the most widespread: MIFARE Classic, MIFARE DESFire, NTAG, MIFARE Ultralight
- **ISO 14443 Type B** - used in identity documents (passports), some payment cards
- **ISO 15693 (NFC-V)** - long-range tags (up to 1 meter), used in logistics and libraries
- **FeliCa** - Sony standard, widespread in Japan (Suica, PASMO)

---

## How NFC Communication Works

NFC communication is **master-slave** based:

1. **The reader** (e.g., turnstile) generates an electromagnetic field at 13.56 MHz
2. **The tag** (card/badge) enters the field and receives energy through induction
3. The tag "wakes up" and responds by modulating the reader's field (**load modulation**)
4. **Anti-collision** occurs if multiple tags are in the field
5. The reader selects a specific tag via its **UID** (Unique ID)
6. Communication begins: authentication, data read/write

**The tag is passive** - it has no battery. All energy comes from the reader's field. Exception: NFC-enabled phones can operate as both reader and tag.

---

## Structure of an ISO 14443A Tag

Every ISO 14443A tag has at least:

- **UID (Unique Identifier):** 4, 7, or 10 bytes - uniquely identifies the tag
  - 4-byte UID: MIFARE Classic 1K/4K (the most common)
  - 7-byte UID: MIFARE Classic EV1, NTAG, DESFire
  - 10-byte UID: rare, used in specialized applications
- **SAK (Select Acknowledge):** 1 byte - indicates the tag type
  - SAK 0x08: MIFARE Classic 1K
  - SAK 0x18: MIFARE Classic 4K
  - SAK 0x20: MIFARE DESFire / MIFARE Plus
  - SAK 0x00: MIFARE Ultralight / NTAG
  - SAK 0x04: MIFARE Mini
- **ATQA (Answer To Request A):** 2 bytes - additional identification

> **Personal note:** The SAK is the first thing I look at when reading an unknown badge. SAK 0x08 = MIFARE Classic 1K = probably vulnerable to crypto1 attack. SAK 0x20 = DESFire = significantly more work ahead. This immediate distinction tells you in 2 seconds whether the badge will be easy or difficult to clone.
