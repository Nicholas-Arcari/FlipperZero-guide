# Tag Types, Cards, and Protocols

## MIFARE Classic 1K/4K

The most widespread NFC tag in the world for access control and transportation systems:

### MIFARE Classic 1K Structure

- **16 sectors** of 4 blocks each
- **64 blocks** total, each 16 bytes
- **1024 bytes** of total storage
- **Block 0:** UID (4 bytes) + manufacturer data - factory set, not writable (on normal tags)
- **Trailer block (last of each sector):** contains Key A (6 bytes) + Access Bits (4 bytes) + Key B (6 bytes)

### MIFARE Classic 4K Structure

- **40 sectors:** 32 with 4 blocks + 8 with 16 blocks
- **256 blocks** total
- **4096 bytes** of storage
- Same security logic as the 1K

### Security: Crypto-1

MIFARE Classic uses the proprietary **Crypto-1** algorithm for authentication:
- Each sector is protected by 2 keys: **Key A** and **Key B** (6 bytes each)
- Data access requires authentication with the correct key
- **Crypto-1 was broken in 2008** - the algorithm has only 48 bits of internal state
- Practical attacks exist that recover keys in seconds to minutes

### Common Default Keys

```
FFFFFFFFFFFF - the most common, factory default
A0A1A2A3A4A5 - MAD (MIFARE Application Directory)
D3F7D3F7D3F7 - NFC Forum
000000000000 - zero key
B0B1B2B3B4B5 - used in some transportation systems
AABBCCDDEEFF - default in some tools
4D3A99C351DD - used by some access control systems
1A982C7E459A - used by some vending machines
```

---

## MIFARE Ultralight / NTAG

Simple and inexpensive tags, typically disposable:

### MIFARE Ultralight

- 64 bytes of storage
- No encryption
- Used in single-use tickets (metro, events)

### NTAG213/215/216

- 144 / 504 / 888 bytes of storage
- NDEF support (NFC Data Exchange Format)
- Optional password (4 bytes - weak)
- Used in smart posters, Amiibo (NTAG215), automation

---

## MIFARE DESFire

The secure successor to MIFARE Classic:

- **Encryption:** DES, 3DES, AES-128
- **Authentication:** challenge-response with symmetric key
- **File system:** application and file structure (not sectors)
- **Anti-cloning:** optional random UID, diversified key
- **Storage:** EV1: 2K/4K/8K, EV2: up to 4K/8K with additional features

**Pentesting implication:** DESFire is significantly more secure than MIFARE Classic. No practical generic attacks exist - attacking it requires knowledge of the keys or implementation-specific vulnerabilities.

---

## iClass / PicoPass (HID)

Proprietary HID Global system, very common in enterprise environments:

- **iClass Standard:** weak encryption, known master keys → vulnerable
- **iClass SE (Secure Identity):** strong encryption, not vulnerable to generic attacks
- **iClass SEOS:** latest generation, robust security

---

## Other Cards

- **T-Union / Clipper / Navigo:** transit cards with MIFARE Classic or DESFire sectors
- **EMV (payment cards):** ISO 14443A/B + EMV protocols with asymmetric cryptography
- **Electronic passports:** ISO 14443B + ICAO 9303, with BAC/PACE authentication

---

## MIFARE Classic - Deep Dive

### The Crypto-1 Attack

The Crypto-1 algorithm was broken in 2007-2008 by researchers at Radboud University (Netherlands). The main vulnerabilities:

1. **Weak LFSR:** the internal state is only 48 bits (cipher too small)
2. **Predictable nonce:** the tag generates nonces that are not fully random
3. **Bit correlation:** relationships between output and internal state enable statistical attacks

### MFKey32 - How It Works

The MFKey32 attack is what the Flipper uses to recover MIFARE Classic keys:

**Prerequisites:**
- The Flipper must emulate a tag and intercept communication with a real reader
- At least 2 captured authentications with the same sector are required

**Step-by-step procedure:**

1. **Read the original badge:** NFC → Read → bring the badge close → save the partial dump
2. **Identify missing keys:** the dump will have sectors marked with "?" where keys are unknown (not found in the dictionary)
3. **Emulate the badge:** NFC → Emulate → select the file → the Flipper emulates the badge
4. **Present the Flipper to the real reader:** bring the Flipper close to the building's badge reader
5. **The reader attempts to authenticate:** sends a challenge to the Flipper, the Flipper responds (incorrectly, but capturing the data)
6. **Repeat 2-3 times** on the same reader
7. **Open MFKey:** the app analyzes the captured data and calculates the keys
8. **Re-read the badge:** now with the recovered keys, perform a full dump

> **Personal note:** MFKey32 is the attack I use most often in real engagements. It works on roughly 70-80% of the MIFARE Classic systems I've encountered. The trick is presenting the Flipper to the reader naturally - during a social engineering scenario, pretend to be an employee who "is having trouble with their badge" and bring the Flipper close to the reader. It takes 2-3 attempts, 5 seconds each.

### Dictionary Attack

Before MFKey32, the Flipper attempts a **dictionary attack** - it tries all keys from a dictionary file:

**Built-in dictionary:** `/ext/nfc/assets/mf_classic_dict.nfc` (hundreds of known keys)
**User dictionary:** `/ext/nfc/assets/mf_classic_dict_user.nfc` (add your own)

Keys are tried in order. If a key works for a sector, it is used to read that sector's data.

**Keys to add to your personal dictionary:**
- Keys found online for the specific target system
- Keys recovered from previous engagements
- Keys extracted with Proxmark3 or ACR122U

> **Personal note:** I maintain a custom dictionary with ~500 keys collected over years of engagements. It includes keys from common Italian access control systems (hotels, offices, apartment buildings). Every time I recover a new key, I add it. This dramatically speeds up future reads - often the dictionary attack finds everything on the first try for systems I've seen before.
