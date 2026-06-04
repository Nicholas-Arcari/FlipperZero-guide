## Detailed Protocols

### NEC - The Dominant Protocol

NEC is by far the most widespread IR protocol in the world. You will find it in TVs, soundbars, set-top boxes, projectors, LED strip controllers, and hundreds of other consumer devices. Understanding NEC in detail is essential.

#### NEC Standard Frame Structure

A complete NEC frame consists of:

```
[Leader Code] [Address] [Address Inverted] [Command] [Command Inverted] [Stop Bit]
```

**1. Leader Code (AGC Burst):**
- **9000 microseconds** of burst (38 kHz carrier active)
- **4500 microseconds** of space (silence)
- Total: 13.5 ms
- Purpose: signal to the receiver the start of a transmission and allow the AGC (Automatic Gain Control) circuit to stabilize

**2. Address (8 bit):**
- Device address (identifies the type of appliance)
- Bit 0 transmitted first (LSB first)

**3. Address Inverted (8 bit):**
- Logical complement of the address (every bit inverted)
- Serves as an **integrity check**: if Address XOR Address_Inverted != 0xFF, the frame is corrupted

**4. Command (8 bit):**
- The actual command (Power, Volume Up, Channel Down, etc.)
- Bit 0 transmitted first (LSB first)

**5. Command Inverted (8 bit):**
- Logical complement of the command
- Same verification function as Address Inverted

**6. Stop Bit:**
- One final 560 microsecond burst to terminate the frame

#### NEC Bit Encoding - Pulse Distance Encoding

NEC uses **pulse distance encoding**:

- **Bit 0:** burst 560 us + space 560 us (total ~1.125 ms)
- **Bit 1:** burst 560 us + space 1690 us (total ~2.25 ms)

The burst is always 560 microseconds. The difference between 0 and 1 lies in the duration of the **space** that follows.

```
Bit 0:  |####|    |      (560us burst + 560us space)
Bit 1:  |####|         |  (560us burst + 1690us space)
```

#### NEC Repeat Code

If a button is held down, after the first complete frame the transmitter sends a **repeat code** every 108 ms:

- **9000 us** burst
- **2250 us** space (half of the leader code space)
- **560 us** burst (stop bit)

The repeat code does NOT contain data - it only says "repeat the last command". The receiver continues to execute the previous action.

#### NEC Extended Variant (16-bit Address)

Some manufacturers use a variant where the 16 address bits are no longer complementary to each other, but contain an actual 16-bit address:

```
[Leader] [Address Low 8bit] [Address High 8bit] [Command] [Command Inverted] [Stop]
```

The Flipper handles both standard and extended NEC.

#### Complete NEC Timing

| Element | Duration |
|---|---|
| Leader burst | 9000 us |
| Leader space | 4500 us |
| Bit burst | 560 us |
| Bit 0 space | 560 us |
| Bit 1 space | 1690 us |
| Repeat burst | 9000 us |
| Repeat space | 2250 us |
| Stop bit | 560 us |
| Complete frame (32 bit) | ~67.5 ms |
| Repetition period | 108 ms |

> **Personal note:** NEC is the protocol you will encounter in 60-70% of cases. When the Flipper decodes a signal as NEC, you can trust it - the structure is robust and recognition is reliable. If you see Address and Command with their respective complements checking out, the signal has been captured correctly.

### RC5 - Philips (Manchester Encoding)

RC5 is the protocol developed by Philips in 1987, still extremely widespread in European devices. The fundamental difference from NEC is the use of **Manchester encoding** (biphase).

#### RC5 Frame Structure

A standard RC5 frame consists of **14 bits** in total:

```
[S1] [S2] [T] [Address: 5 bit] [Command: 6 bit]
```

**S1 (Start bit 1):** always 1 - indicates the start of the frame
**S2 (Start bit 2):** always 1 in classic RC5 (becomes the 7th command bit in RC5 Extended)
**T (Toggle bit):** changes state (0->1 or 1->0) **every time the button is pressed and released**. If the button remains held, the toggle bit does not change. This allows the receiver to distinguish "continuous press" from "two rapid presses".
**Address (5 bit):** device address (0-31)
**Command (6 bit):** command (0-63), extendable to 7 bits with S2

#### Manchester Encoding (Biphase)

In Manchester encoding, each bit occupies a fixed period (approximately **1778 us** for RC5, corresponding to a bit rate of ~562 Hz) and **always contains a transition** at the center:

- **Bit 0:** high level in the first half, high-to-low transition at center
- **Bit 1:** low level in the first half, low-to-high transition at center

```
Bit 0:  |####|____|     (high then low)
Bit 1:  |____|####|     (low then high)
```

The 36 kHz carrier (note: RC5 uses 36 kHz, not 38 kHz) is activated during the "high" phases.

#### RC5 Parameters

| Parameter | Value |
|---|---|
| Carrier frequency | 36 kHz |
| Bit period | 1778 us |
| Half period (half-bit) | 889 us |
| Total bit count | 14 |
| Frame duration | ~24.9 ms |
| Possible addresses | 32 (5 bit) |
| Possible commands | 64/128 (6/7 bit) |

#### Operational Differences Between RC5 and NEC

- RC5 uses **36 kHz** as its carrier (NEC uses 38 kHz) - the Flipper's receiver (TSOP75338, optimized for 38 kHz) receives RC5 with slightly reduced sensitivity
- RC5 has the **toggle bit** - NEC does not. This can cause confusion: if you capture an RC5 signal and retransmit it, the toggle bit might be in the "wrong" value and the device might interpret it as "button still pressed" rather than "new press"
- RC5 has fewer combinations (32 addresses x 128 commands) compared to NEC (256 addresses x 256 commands, or 65536 x 256 in NEC extended)

### RC6 - Philips (RC5 Evolution)

RC6 is the evolution of RC5, developed by Philips to overcome the predecessor's limitations. It adds structural complexity but remains based on Manchester encoding.

#### RC6 Frame Structure

```
[Leader] [Start Bit] [Mode: 3 bit] [Trailer: 1 bit] [Control: 8 bit] [Information: 8 bit]
```

**Leader:** 2666 us burst + 889 us space (6T + 2T, where T = 444 us)
**Start bit:** always 1
**Mode (3 bit):** defines the mode (Mode 0 is the most common for consumer)
**Trailer (Toggle) bit:** equivalent of the RC5 toggle, but with **double timing** (2T per half-bit instead of T) - this is the most characteristic trait of RC6
**Control (8 bit):** device address
**Information (8 bit):** command

#### Trailer Bit Peculiarity

The RC6 trailer bit (toggle) has different timing from all other bits:

- Normal bits: half-bit = 444 us (1T)
- Trailer bit: half-bit = 889 us (2T)

This makes the protocol more complex to decode and reproduce. The Flipper correctly handles this peculiarity.

#### RC6 Parameters

| Parameter | Value |
|---|---|
| Carrier frequency | 36 kHz |
| Base period (T) | 444 us |
| Normal half-bit | 444 us (1T) |
| Trailer half-bit | 889 us (2T) |
| Leader | 2666 us burst + 889 us space |
| Possible addresses | 256 (8 bit) |
| Possible commands | 256 (8 bit) |

### Sony SIRC - Pulse Width Encoding

Sony uses the SIRC protocol (Sony Infrared Remote Control), with a different structure from NEC and RC5.

#### SIRC Frame Structure

Three variants exist:

- **SIRC 12 bit:** 7 bit command + 5 bit address
- **SIRC 15 bit:** 7 bit command + 8 bit address
- **SIRC 20 bit:** 7 bit command + 5 bit address + 8 bit extended

```
[Leader] [Command: 7 bit] [Address: 5/8 bit] [Extended: 8 bit optional]
```

**Leader:** 2400 us burst + 600 us space

#### SIRC Bit Encoding - Pulse Width Encoding

SIRC uses **pulse width encoding**, different from NEC's pulse distance encoding:

- **Bit 0:** burst 600 us + space 600 us (total 1.2 ms)
- **Bit 1:** burst 1200 us + space 600 us (total 1.8 ms)

Unlike NEC, here it is the **burst duration** that changes, not the space duration.

```
Bit 0:  |##|    |      (600us burst + 600us space)
Bit 1:  |####|    |    (1200us burst + 600us space)
```

#### SIRC Repetition

Sony specifies that each frame must be repeated **at least 3 times** with an interval of approximately 45 ms between the start of each frame. This is different from the NEC repeat code - in SIRC, the entire frame is repeated.

#### SIRC Parameters

| Parameter | Value |
|---|---|
| Carrier frequency | 40 kHz |
| Leader burst | 2400 us |
| Leader space | 600 us |
| Bit 0 burst | 600 us |
| Bit 1 burst | 1200 us |
| Bit space | 600 us |
| Minimum repetition | 3 frames |
| Frame interval | ~45 ms |

> **Personal note:** The SIRC carrier at 40 kHz (not 38 kHz) can cause issues with receivers tightly filtered at 38 kHz. In practice, the Flipper handles SIRC transmission well, but in reception it might lose some bits at greater distances. If you have problems with Sony devices, get closer.

### Samsung - NEC Variant

Samsung uses a protocol derived from NEC with differences in leader timing and address structure.

#### Samsung Frame Structure

```
[Leader] [Address: 8 bit] [Address: 8 bit repeated] [Command: 8 bit] [Command Inverted: 8 bit] [Stop]
```

Key difference: the address is transmitted **twice identically** (not inverted), while the command uses the same inversion logic as NEC.

#### Samsung Timing

| Element | Duration |
|---|---|
| Leader burst | 4500 us |
| Leader space | 4500 us |
| Bit burst | 560 us |
| Bit 0 space | 560 us |
| Bit 1 space | 1690 us |

The leader is **symmetrical** (4500 + 4500 us) unlike NEC (9000 + 4500 us). The bit encoding is identical to NEC.

### RAW - Universal Capture

When the Flipper cannot decode a signal into a known protocol, it records it in RAW format.

#### RAW Format in the Flipper Zero

A RAW signal in the Flipper's `.ir` file is represented as:

```
name: Signal_1
type: raw
frequency: 38000
duty_cycle: 0.330000
data: 9000 4500 560 560 560 1690 560 560 ...
```

The `data` values are durations in microseconds, alternating burst and space:
- Odd-position values (1st, 3rd, 5th...): duration of the **burst** (carrier active)
- Even-position values (2nd, 4th, 6th...): duration of the **space** (silence)

#### When RAW Is Needed

- **Proprietary protocols** not recognized by the Flipper
- **Air conditioner remotes** with complex protocols (very long frames)
- **Industrial devices** with non-standard encodings
- **Vintage devices** with obsolete protocols
- **Any IR signal** that is not automatically decoded

#### RAW Limitations

- **Larger files:** a RAW signal can take up many lines compared to a decoded protocol
- **Timing tolerance:** minor inaccuracies in capture can cause playback failures, especially for protocols with tight timing
- **No verification:** there is no automatic way to know if the capture is correct - testing is required

### AC Protocols - The Special Case of Air Conditioners

Air conditioner remote controls represent the most complex case in IR communication. They deserve a dedicated section.

#### Why AC Protocols Are Different

A TV remote sends simple commands: "raise volume", "change channel". The context (current volume, current channel) is maintained by the TV itself.

An AC remote sends **the complete state of the air conditioner** with every button press:

- Desired temperature (16-30 degrees)
- Mode (cool, heat, dehumidifier, fan, auto)
- Fan speed (low, medium, high, auto)
- Vane direction (fixed, vertical swing, horizontal swing)
- Timer on/off
- Sleep/eco/turbo mode
- On/off state

All of this is encoded in a **single very long IR frame**, typically **100-200+ bits** (compared to NEC's 32 bits). Every time you press a button on the remote, the entire state is transmitted.

#### Operational Consequences

- AC frames are often **too long** to be decoded as a standard protocol - the Flipper captures them in RAW
- **A single corrupted bit** can render the entire frame useless - the air conditioner will not respond
- **Every brand** has its own protocol (Daikin, Mitsubishi, Panasonic, Toshiba, LG, Samsung, Carrier...) with completely different structures
- **Changing a single parameter** (e.g., increasing temperature by 1 degree) generates a completely different frame
- To control an unknown AC, you might need to capture **dozens of different combinations**

#### Typical AC Frame Structure (generic example)

```
[Leader] [Header: brand/model] [Mode] [Temperature] [Fan speed] [Swing] [Timer] [Checksum]
```

The checksum varies by manufacturer: it can be XOR, modulo 256 sum, CRC, or proprietary variants.

> **Personal note:** AC protocols are the bane of IR. If you need to control an unknown air conditioner during an engagement, the best strategy is: (1) first try the Flipper's pre-loaded profiles for that brand, (2) if they do not work, capture the original remote's signal for each specific action you need (power on, power off, temperature change), (3) save each RAW signal with a descriptive name. Do not attempt to manually decode the protocol in the field - you do not have time. Do it in the lab afterwards, if necessary.

---
