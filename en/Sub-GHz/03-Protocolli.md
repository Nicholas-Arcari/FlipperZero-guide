# Sub-GHz - Modulations and Protocols

## Modulations - The Physical Language of the Signal

### OOK/ASK (On-Off Keying / Amplitude Shift Keying)

The simplest and most widespread modulation in the consumer remote control world:

- **Bit 1:** the transmitter emits the RF carrier
- **Bit 0:** the transmitter is silent (no emission)
- **Decoding:** the receiver measures the presence/absence of the signal

Used by: the vast majority of garage remote controls (Nice, Came, FAAC, BFT, Beninca), weather sensors, wireless doorbells, cheap alarm sensors.

Practical variants:
- **Manchester encoding:** each bit is represented by a transition (high->low = 1, low->high = 0). Used by many protocols to ensure synchronization.
- **PWM (Pulse Width Modulation):** the duration of the high pulse determines the bit value. Long pulse = 1, short pulse = 0 (or vice versa).
- **PPM (Pulse Position Modulation):** the position of the pulse within the timeslot determines the value.

> **Personal note:** If you are analyzing an unknown signal, always start with the OOK/ASK hypothesis at 433.92 MHz. It probably covers 70-80% of European consumer devices.

### 2-FSK (Frequency Shift Keying)

Frequency shift modulation:

- **Bit 1:** the carrier shifts to a slightly higher frequency
- **Bit 0:** the carrier shifts to a slightly lower frequency
- **Typical deviation:** 4.8-47.6 kHz

Used by: more sophisticated protocols like KeeLoq rolling code (some variants), advanced home automation systems, industrial sensors.

Advantages: greater noise resistance compared to OOK, better range in noisy environments.

### GFSK (Gaussian FSK)

Variant of FSK with Gaussian filtering to reduce bandwidth:

- Smoother transitions between frequencies
- Less interference with adjacent channels
- Used in modern protocols

Used by: some advanced rolling codes, proprietary protocols.

---

## Protocols Supported by the Flipper Zero

The Flipper Zero automatically decodes dozens of protocols. Here are the main ones with operational details:

### Fixed Code Protocols

| Protocol | Bits | Frequency | Modulation | Notes |
|---|---|---|---|---|
| **Princeton** | 24 | 433.92 | OOK | Generic, used by many Chinese clones |
| **Nice FLO** | 12 | 433.92 | OOK | Old generation Nice gates |
| **Nice FLORS** | 52 | 433.92 | OOK | Nice with sync |
| **Came** | 12 | 433.92 | OOK | Came Automation fixed code |
| **Came TWEE** | 54 | 433.92 | OOK | Came with extended code |
| **Linear** | 10 | 300/310 | OOK | Garage door USA |
| **Gate TX** | 24 | 433.92 | OOK | Generic gate controller |
| **Holtek HT12X** | 12 | 433.92 | OOK | Cheap encoder/decoder |
| **Chamberlain** | 7/8/9 | 300/315/390 | OOK | US garage (some versions) |
| **SMC5326** | 25 | 433.92 | OOK | Remote control copier |
| **PT2260/PT2262** | 24 | 433.92 | OOK | Generic encoder (alias Princeton) |
| **Honeywell** | 48 | 345 | OOK | US alarm sensors |
| **Intertechno** | 32 | 433.92 | OOK | German home automation |

### Rolling Code Protocols

| Protocol | Bits | Frequency | Security | Notes |
|---|---|---|---|---|
| **KeeLoq** | 66 | 433.92/868 | Medium-High | The most widespread: Nice Smilo/FLO2R, Came TOP, BFT Mitto, Beninca |
| **Nice FlorS** | 52 | 433.92 | Medium | Nice with rolling code |
| **Came Atomo** | 64 | 433.92 | High | Latest generation Came |
| **FAAC SLH** | 64 | 868.35 | High | FAAC proprietary rolling |
| **Somfy RTS** | 56 | 433.42 | Medium | Somfy roller shutters/awnings |
| **Marantec** | 32 | 433.92/868 | Medium | Garage door EU |
| **Secucode** | 64 | 433.92 | High | Secure KeeLoq implementation |

> **Personal note:** In practice, the majority of Italian residential gates use Nice or Came. The older Nice models (Nice FLO at 12 bits) are fixed code and can be cloned in 5 seconds. The newer Nice models (FLOR, Smilo) use KeeLoq rolling code - significantly harder. FAAC is almost always on 868 MHz with strong rolling code.

---

## Fixed Codes vs Rolling Code

### Fixed Code - How It Works

A fixed code remote control transmits **always the same message** when you press the button:

```
Every press: [SYNC] [ID: 0xA4B3C2] [BUTTON: 01] [STOP]
Every press: [SYNC] [ID: 0xA4B3C2] [BUTTON: 01] [STOP]
Every press: [SYNC] [ID: 0xA4B3C2] [BUTTON: 01] [STOP]
```

**Vulnerability:** anyone who captures the signal can replay it indefinitely. The replay attack is trivial.

**How to attack (on your own / authorized systems):**
1. Sub-GHz -> Read -> press the remote -> save the .sub file
2. Sub-GHz -> Saved -> select the file -> Send
3. The receiver cannot distinguish the original signal from the copy

**Vulnerable protocols:** Princeton, Nice FLO, Came 12-bit, Linear, Gate TX, Holtek, PT2262

### Rolling Code - How It Works

A rolling code remote control generates a **different code with every press** thanks to a cryptographic algorithm shared with the receiver:

```
Press 1: [SYNC] [SERIAL] [ENCRYPTED_COUNTER: 0x1A3F] [BUTTON]
Press 2: [SYNC] [SERIAL] [ENCRYPTED_COUNTER: 0x7B82] [BUTTON]
Press 3: [SYNC] [SERIAL] [ENCRYPTED_COUNTER: 0xC4D1] [BUTTON]
```

The receiver maintains an **acceptance window** (typically 256 future codes). If the received code falls within the window, it accepts it and advances the counter.

### KeeLoq - The Most Widespread Rolling Code

KeeLoq is a proprietary block cipher by Microchip Technology, used by Nice, Came, BFT, Beninca, Chamberlain, and many others:

- **Key:** 64 bits (cryptographic key shared between TX and RX)
- **Counter:** 16 bits (65536 values before rollover)
- **Serial:** 28 bits (identifies the transmitter)
- **Algorithm:** non-linear block cipher with 528 rounds
- **Key derivation:** the individual remote's key is derived from the manufacturer key + serial number

**Known KeeLoq vulnerabilities:**

1. **Manufacturer key brute force:** if the manufacturer's key is compromised (and many have been), all remotes from that manufacturer become vulnerable. Researchers have extracted the keys from Nice, Came, and others through side-channel attacks on the chips.

2. **RollJam Attack:** the attacker uses a jammer to block the legitimate remote's signal while capturing the valid rolling code. The user presses again, the attacker captures the second code too and releases the first one. Now they hold a valid rolling code that has not been used yet.

3. **RollBack Attack:** exploits weaknesses in the counter implementation to force the receiver into accepting previous codes.

4. **Resync window:** many receivers have a resynchronization mode that can be exploited by sending specific sequences of codes.

> **Personal note:** RollJam is the most practical attack against rolling code, but it requires additional hardware (jammer + simultaneous receiver). The Flipper Zero alone CANNOT perform a classic RollJam because it cannot jam and receive simultaneously. However, the "Rolling Flaws" tool analyzes specific weaknesses in various manufacturers' implementations. In real engagements, I have found that many "rolling code" systems are actually misconfigured or running old firmware with known vulnerabilities.
