# Advanced Attacks and Countermeasures - NFC

Analysis of the main NFC attack vectors and their countermeasures, with focus on MIFARE Classic and access control systems.

---

## Magic Card - Complete Guide

### Why Magic Cards Are Needed

The Flipper's NFC emulation has limitations:
- Not all readers accept an emulated Flipper
- Emulation requires the Flipper to be powered on and in the correct position
- Some readers have timing too strict for software emulation

Magic Cards solve these problems: they are **real physical tags** with the ability to be fully reprogrammed, including the UID (which is normally factory-fixed).

### Gen1 (Chinese Magic / UID Changeable)

- **Backdoor command:** WUPC (0x40, 0x43) allows writing Block 0
- **Advantages:** simple, inexpensive, well supported by the Flipper
- **Disadvantages:** detectable - a reader can send the WUPC command and if the tag responds, it knows it's a Magic

### Gen2 (CUID / Direct Write)

- **No backdoor:** Block 0 is directly writable with a standard WRITE command
- **Advantages:** not detectable with the WUPC test
- **Disadvantages:** less compatible with some readers, sometimes unstable

### Gen3 (UFUID)

- **UID writable once:** after writing, you can "lock" Block 0
- **Advantages:** once locked, it behaves like a real non-magic tag
- **Disadvantages:** you can write the UID only once (unless using a special unlock)

### Gen4 (Ultimate Magic / GDM)

- **Fully programmable:** UID, SAK, ATQA, data - everything writable unlimited times
- **Proprietary GDM command:** not detectable by standard anti-magic tests
- **1K and 4K support:** configurable
- **Advantages:** the most versatile, undetectable, unlimited
- **Disadvantages:** slightly higher cost (~2-3 euros), requires firmware with Gen4 support

### Magic Card Comparison Table

| Type | UID Rewrite | Detectable | Compatibility | Price | Recommended Use |
|------|------------|------------|---------------|-------|-----------------|
| Gen1 | Yes (backdoor) | Yes (WUPC) | Excellent | ~0.50 EUR | Lab testing |
| Gen2 | Yes (direct) | No (WUPC) | Good | ~0.80 EUR | Targets without anti-magic |
| Gen3 | Once | No (after lock) | Excellent | ~1.50 EUR | Permanent clone |
| Gen4 | Unlimited | No | Excellent | ~2-3 EUR | Professional pentesting |

> **Personal note:** For pentesting, I exclusively use Gen4 (Ultimate Magic). They are the only ones not detected by modern readers with anti-magic checks. Gen1s are blocked by about 30% of enterprise readers. Gen4s always pass. I keep about ten in my kit, pre-programmed with badge dumps used in previous engagements (obviously wiped after the report).

---

## Main Attacks

### Crypto-1 Key Recovery (MFKey32)

**Principle:** The Crypto-1 algorithm used by MIFARE Classic has known cryptographic vulnerabilities. By analyzing the nonces exchanged during authentication between reader and tag, it is possible to recover the secret keys.

**Detailed procedure:**
1. The Flipper emulates a tag with a known UID
2. It is presented to the target reader
3. The reader sends a challenge (cryptographic nonce)
4. The Flipper responds with a calculated response
5. The exchange is recorded (nonce_reader, nonce_tag, auth_response)
6. The MFKey32 attack uses the mathematical properties of Crypto-1 to derive the 48-bit key
7. A minimum of 2 captured authentications per sector is required

**Computational complexity:** a few seconds on modern hardware (the Flipper does it directly)

**Countermeasure:** migrate to DESFire EV2/EV3 with per-card diversified AES-128 keys

### Dictionary Attack

**Principle:** Many systems use known, default, or common keys. The Flipper tries thousands of known keys until it finds the correct one.

**Common keys:**
```
FFFFFFFFFFFF (factory default)
A0A1A2A3A4A5 (public transit)
D3F7D3F7D3F7 (NXP systems)
000000000000 (zero key)
B0B1B2B3B4B5 (variant)
4D3A99C351DD (payment systems)
1A982C7E459A (hotels)
```

**Countermeasure:** unique keys per installation, derived from a master secret + tag UID

### Hardcoded Key Attack

**Principle:** Many manufacturers use the same key for all badges of the same model or installation. If the key is extracted from a single badge (via hardware dump, reader firmware reverse engineering, or leak), all badges are compromised.

**Known examples:**
- Transit systems with identical keys across millions of cards
- Vending machines with a master key hardcoded in firmware
- Access control systems with a shared key per site

**Countermeasure:** diversified keys - each badge has unique keys derived from the UID using a secure derivation algorithm (e.g., AES-CMAC)

### Clone-and-Replay

**Principle:** full badge dump → write to Magic Card → access

**Procedure:**
1. Complete read of all sectors (requires all keys)
2. Write to Gen4 Magic Card (including UID, SAK, ATQA)
3. The Magic Card is indistinguishable from the original

**Countermeasure:** 
- Blacklisting duplicate UIDs (if two badges with the same UID are seen in different locations)
- Rolling data - the reader writes a timestamp/counter after each access. A clone would have stale data
- Mutual authentication - the badge verifies the reader (prevents unauthorized reading)

### UID-Only Bypass

**Principle:** Systems that verify only the UID (4 or 7 bytes) without reading sector data. Knowing the UID is enough to emulate it.

**Procedure:**
1. NFC → Read: capture only the UID (sector keys not needed)
2. NFC → Emulate with the captured UID
3. Alternatively: NFC Fuzzer to enumerate valid UIDs

**Complexity:** 4-byte UID = 4.3 billion combinations (bruteforce impractical), but UIDs are often sequential → restricted range

**Countermeasure:** ALWAYS verify data in authenticated sectors, never just the UID

### Relay Attack

**Principle:** extending reader-tag distance via real-time relay

**Architecture:**
```
[Reader] ←NFC→ [Proxy (Flipper 1)] ←network→ [Relay (Flipper 2)] ←NFC→ [Victim's badge]
```

**Critical latency:** the NFC protocol has strict timeouts (~5ms for MIFARE). The relay must add less than 1-2ms of latency to work. This limits the practical distance and requires a fast network.

**Countermeasure:**
- Distance bounding - the reader measures response time. With a relay, the time increases and the reader rejects the transaction
- Strict timeouts - reduce the authentication timeout
- Multi-factor - badge + PIN or badge + biometric

---

## Attack Matrix - Quick Reference

| Attack | Target | Complexity | Flipper Sufficient? | Impact |
|--------|--------|-----------|---------------------|--------|
| Dictionary | MIFARE Classic | Low | Yes | Full dump |
| MFKey32 | MIFARE Classic | Medium | Yes | Key recovery |
| Hardcoded Key | Various | Low (if known) | Yes | Dump + clone |
| Clone-and-Replay | MIFARE Classic | Low-Medium | Yes (+ Magic Card) | Access |
| UID-Only | Simple systems | Very Low | Yes | Access |
| Relay | Any NFC | High | Partial (needs 2) | Remote access |
| UID Fuzzing | Simple systems | Medium | Yes | Enumeration |
