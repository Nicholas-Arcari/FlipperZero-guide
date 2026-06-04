## Attacks and Countermeasures

### The Fundamental Reality: IR Has No Encryption

This is the critical point that distinguishes IR from almost all other wireless technologies:

**IR signals are completely devoid of encryption, authentication, rolling codes, or any form of protection.**

Every captured signal can be replayed an infinite number of times with 100% success. There is no equivalent of Sub-GHz rolling codes, MIFARE Crypto-1 encryption, or DESFire challenge-response.

Why? Because IR was designed in the 1970s-80s for consumer remote controls, where:
- The limited range (line-of-sight, a few meters) was considered sufficient protection
- The cost of adding encryption to cheap remotes was not justifiable
- The threat of "IR replay" was not considered a real risk

Result: in 2025, billions of devices are controllable by anyone with an IR transmitter and the right codes (publicly available).

### Replay Attack - Trivial and Unstoppable

The simplest attack is replay:

1. **Capture** the IR signal with the Flipper (or any IR receiver)
2. **Replay** the identical signal
3. **The device executes the command** - it has no way to distinguish the original signal from a copy

No special skills are required. There are no protocol-level countermeasures. The only defense is to physically prevent the IR signal from reaching the receiver.

### The Flipper Zero as the "Ultimate TV-B-Gone"

The "TV-B-Gone" is a device created in 2004 by Mitch Altman: a small circuit that cycles through hundreds of Power Off codes for different TV brands, turning off virtually any television within range.

The Flipper Zero is an enormously enhanced TV-B-Gone:

- **Larger database:** thousands of codes vs hundreds in the original TV-B-Gone
- **Updatable:** the database can be expanded by loading new .ir files
- **Bidirectional:** can also capture and analyze signals, not just transmit them
- **Multi-device:** not just TVs - also ACs, projectors, soundbars, displays
- **Programmable:** you can create custom scripts with specific sequences
- **Discreet:** the Flipper looks like a generic gadget, not an attack device

### TV-B-Gone Automation with the Flipper

To maximize effectiveness, you can prepare optimized sequences:

1. Create an `.ir` file with all Power Off codes for the most common brands
2. Sort by prevalence (Samsung and LG first, rare brands last)
3. Use Universal Remotes for an automatic scan
4. Alternatively, use IR Blaster for rapid burst sending

In an aggressive scan, the Flipper can try all the most common codes in approximately **30-60 seconds**.

### IR Jamming

IR jamming is the optical equivalent of radio jamming:

**Principle:** A powerful IR LED continuously emitting at the carrier frequency (38 kHz) saturates the target's IR receiver, preventing it from receiving any useful signal.

**Can the Flipper do jamming?** In theory yes - by transmitting a continuous 38 kHz carrier. In practice, the single LED and limited power make jamming effective only at very close distances (1-2 meters).

**Counter-countermeasures to jamming:**
- Directional IR filters on the receiver
- Receivers with advanced AGC that adapts to saturation
- Use of protocols with different carrier frequencies (36, 40, 56 kHz)
- Redundancy: multiple IR receivers positioned at different locations

### General Countermeasures Against IR Attacks

For defenders (and for the pentest report):

**Physical countermeasures (the most effective):**
- **IR receiver coverage:** infrared-opaque tape over the receiver. Zero cost, 100% effective. Note: the tape must block 940 nm - some tapes that appear opaque to visible light are transparent to IR
- **Protected positioning:** IR receiver facing the wall or upward, not toward the public
- **Enclosure:** physical cover with a directional slot that limits the reception angle

**Configuration countermeasures:**
- **Hotel/Hospitality mode:** many commercial TVs have a mode that disables or limits IR commands (e.g., blocks Power Off, limits maximum volume)
- **IR disable:** some professional displays allow completely disabling the IR receiver, managing control via RS-232 or network
- **Power Lock:** function that prevents power-off via remote - requires power-off from the physical panel or management software

**System countermeasures:**
- **Software watchdog:** the media player detects display power-off and automatically turns it back on (common in digital signage systems)
- **Centralized control:** management via network (IP, RS-232) that completely bypasses IR
- **Monitoring:** cameras in areas with critical displays

---
