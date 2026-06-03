# Advanced Attacks and Countermeasures - Sub-GHz

Analysis of the main Sub-GHz RF attack vectors and their countermeasures. For each attack: operating principle, prerequisites, real-world limitations, and effective defenses.

---

## Replay Attack (Fixed Code)

### Principle
The attacker captures the RF signal transmitted by a legitimate remote and replays it identically. Since the code is static, the receiver cannot distinguish the original from the copy.

### Prerequisites
- The target system uses fixed code (no rolling code)
- The attacker is within the transmitter's reception range (~10-50m)
- Knowledge of the frequency (obtainable with Frequency Analyzer)

### Procedure with Flipper Zero
1. Sub-GHz -> Read on the target frequency
2. Wait for a legitimate transmission
3. The Flipper decodes and saves the signal
4. Sub-GHz -> Saved -> Send to replay

### Real-World Limitations
- Flipper transmission range is limited (~5-15m indoor)
- Some receivers have tight timing filters that reject signals with jitter
- The signal must be captured under low RF noise conditions

### Countermeasures
- **Migrate to rolling code** (KeeLoq, AES rolling) - completely eliminates replay
- **Challenge-response systems** - the receiver sends a challenge, the transmitter responds with the code + challenge. Impossible to replicate
- **Aggressive timeout** - the code is only valid for N seconds after transmission
- **Anomaly detection** - logging and alerting on openings at unusual times

---

## RollJam Attack

### Principle
The most sophisticated attack against rolling code systems. The attacker simultaneously uses:
1. A **jammer** that prevents the receiver from receiving the legitimate code
2. A **receiver** (on a slightly different frequency or with a directional antenna) that captures the code

The user presses the remote, the code is captured but not received (jammed). The user presses again - the second code is captured, and the first one is released (replayed). The attacker now possesses a valid rolling code (the second one) that has not yet been consumed.

### Prerequisites
- Dedicated RF jammer (the Flipper alone is not enough - it cannot jam and receive simultaneously)
- Two receiving devices, or a device with full-duplex capability
- Proximity to the target (the jammer must overpower the remote's signal)
- Precise timing

### Why the Flipper Zero Alone Is Not Enough
The Flipper's CC1101 is half-duplex: it can only transmit OR receive, never both. For a RollJam you need a minimum of two radios: one to jam, one to receive. Possible with Flipper + external CC1101 module via GPIO, but requires custom firmware.

### Countermeasures
- **Aggressive rolling code timeout** - the code expires after 30-60 seconds
- **Anti-jamming** - the receiver detects jamming (anomalous RF energy without valid decode) and triggers an alarm
- **Double verification** - the system requires two presses with specific timing
- **802.11w-style protection** - authenticated management frames (applied to Sub-GHz)
- **Counter gap detection** - if the receiver notices the counter has jumped by >1 without intermediate openings, it locks the system

---

## Bruteforce

### Principle
Sequential transmission of all possible codes until the valid one is found. Only feasible on systems with a reduced code space.

### Realistic Timeframes

| Bits | Combinations | Time (~10 codes/sec) | Feasibility |
|-----|-------------|----------------------|-------------|
| 8 | 256 | ~26 seconds | Trivial |
| 10 | 1,024 | ~2 minutes | Easy |
| 12 | 4,096 | ~7 minutes | Feasible |
| 16 | 65,536 | ~2 hours | Possible |
| 20 | 1,048,576 | ~29 hours | Difficult |
| 24 | 16,777,216 | ~19 days | Impractical |
| 32 | 4,294,967,296 | ~13 years | Impossible |

### Procedure with Flipper Zero
1. Sub-GHz Bruteforcer -> select protocol and bit-length
2. Set the target frequency
3. Start -> the Flipper transmits sequentially
4. Observe the receiver to detect activation

### Real-World Limitations
- Speed limited by the duration of each transmission (~100ms per code)
- Some receivers have lockout after N rapid attempts
- The Flipper's range limits effectiveness (you need to be close)
- Battery: bruteforce consumes a lot of TX energy

### Countermeasures
- **Sufficient code length** (minimum 20 bits, ideally 32+)
- **Temporal lockout** after N invalid attempts
- **Rate limiting** on the receiver (ignores transmissions that are too close together)
- **Rolling code** - renders bruteforce useless (the effective space is 2^64+)
- **Alert on multiple attempts** - the system flags anomalous activity

---

## Jamming (RF Interference)

### Principle
Saturation of the target frequency with RF noise to prevent communication between transmitter and receiver. Does not require knowledge of the protocol - simply transmitting energy on the same frequency is enough.

### Types
- **Barrage jamming:** continuous noise across the entire band - easy to detect
- **Spot jamming:** targeted noise on the exact frequency - more effective, less detectable
- **Deceptive jamming:** transmission of false signals that confuse the receiver
- **Reactive jamming:** the jammer activates only when it detects a legitimate transmission - the hardest to counter

### The Flipper as a Jammer
The Flipper can transmit a continuous signal on a specific frequency (via Read RAW with a noise file), but the power (+12 dBm) is very limited. Effective only at short range (<5m) and easily overpowered by more powerful transmitters.

### Countermeasures
- **Anti-jamming with heartbeat monitoring** - the receiver expects a periodic signal from the sensor. If the signal disappears (because it is jammed), the alarm triggers
- **Frequency hopping** - the system changes frequency according to a pseudorandom pattern
- **Spread spectrum** - the signal is distributed across a wide band, difficult to jam
- **Dual-band** - sensors that transmit on both 433 AND 868 MHz. Jamming both requires twice the equipment
- **Anomalous energy detection** - the receiver measures the noise level and generates an alarm if it is abnormally high

---

## Side-Channel on the Manufacturer Key (KeeLoq)

### Principle
KeeLoq implementations use a "manufacturer key" shared among all devices from the same manufacturer. If this key is extracted (via DPA/SPA analysis on a single remote), all devices from that manufacturer are compromised.

### DPA Attack (Differential Power Analysis)
1. Purchase a remote from the same manufacturer as the target
2. Connect a high-speed oscilloscope to the chip
3. Measure the power consumption variations during encryption
4. Statistical analysis of the power traces to extract the key

### Prerequisites
- Laboratory equipment (1+ GHz oscilloscope, differential probes)
- Advanced skills in side-channel cryptanalysis
- Physical access to a remote from the same manufacturer
- Time: hours/days for the analysis

### Relevance for the Flipper
The Flipper Zero does not directly perform side-channel attacks, but if the manufacturer key is known (published in academic papers or leaks), the Rolling Flaws tool can use it to predict future codes.

### Countermeasures
- **Per-device keys** - each remote has a unique key derived from the serial + master secret
- **Side-channel protection on the chip** - temporal randomization, power consumption masking
- **AES instead of KeeLoq** - modern algorithms with better side-channel resistance
- **Secure element** - dedicated cryptographic chip with hardware protections

---

## Attack Matrix - Quick Reference

| Attack | Target | Complexity | Flipper Sufficient? | Impact |
|--------|--------|-----------|---------------------|--------|
| Replay | Fixed code | Low | Yes | Immediate opening |
| RollJam | Rolling code | High | No (requires jammer) | Single opening |
| Bruteforce | Fixed code <16 bits | Low-Medium | Yes | Opening after time |
| Jamming | Any | Low | Partial (low power) | Temporary DoS |
| Side-Channel | KeeLoq | Very High | No (requires lab) | Total compromise |
