# Hardware and Real-World Limitations - Flipper Zero IR Module

## Transmitter LED - TSAL6200

The Flipper Zero is equipped with a **Vishay TSAL6200** IR LED as its transmitter:

| Parameter | Value |
|---|---|
| **Peak wavelength** | 940 nm |
| **Emission angle (half-angle)** | +-17 degrees (total ~34 degrees) |
| **Typical forward current** | 100 mA |
| **Peak forward current** | 200 mA (pulsed) |
| **Radiant power** | ~35 mW/sr @ 100mA |
| **Rise/fall time** | ~800 ns |

The TSAL6200 is a high-power LED for its category, but it remains a single LED. Commercial remote controls often mount 2-3 LEDs in parallel to increase power and coverage angle. The Flipper, having only one LED, has a lower TX range than many dedicated remotes.

---

## Receiver - TSOP75338

The Flipper Zero uses a **Vishay TSOP75338** IR receiver (or equivalent from the same family):

| Parameter | Value |
|---|---|
| **Optimal carrier frequency** | 38 kHz |
| **Accepted frequency range** | ~33-41 kHz (with reduced sensitivity at the edges) |
| **Sensitivity** | very high - detects weak signals |
| **Reception distance** | up to 15-20 meters (from powerful remotes) |
| **Ambient light filter** | integrated |
| **Output** | active low (LOW = burst detected) |
| **Power supply** | 2.5-5.5V |

The TSOP75338 is optimized for 38 kHz. Signals at 36 kHz or 40 kHz are still received, but with reduced sensitivity (approximately -3 dB for every 2 kHz offset). Signals at 56 kHz (used by some Bang & Olufsen systems) are received with difficulty or not received at all.

---

## Real-World Range - TX vs RX

This is the most important distinction to understand:

**Transmission range (TX):**
- **Ideal conditions** (dark room, direct line-of-sight, sensitive receiver): **5-8 meters**
- **Real-world conditions** (ambient light, imperfect angle): **3-5 meters**
- **Worst-case conditions** (direct sunlight, wide angle, low-sensitivity receiver): **1-2 meters**

**Reception range (RX):**
- **From a powerful remote** (multi-LED): **15-20 meters**
- **From a standard single-LED remote**: **8-12 meters**
- **From another Flipper Zero:** **3-6 meters**

The asymmetry is enormous: the Flipper receives much better than it transmits. This is a critical operational data point.

---

## Emission Angle and Positioning

The TSAL6200's emission angle is narrow: approximately **+-17 degrees** from center (half-angle at 50% power). In practice, this means:

- You need to **reasonably aim** the Flipper toward the target receiver
- Millimeter precision is not necessary - bounces off white walls and ceilings help
- In a normal room, you can often control a device even by pointing toward the ceiling (bounce)
- Outdoors or in large environments, you must aim directly at the receiver

---

## Real-World Limitations You Need to Know

**Single LED:** A single transmitter LED limits both range and angle compared to commercial remotes. There is no hardware way to improve this without modifications.

**No native external LED:** Unlike the Sub-GHz module (which supports external CC1101 modules via GPIO), the IR module has no native support for external LEDs. Hardware mods exist, but they are unofficial.

**Fixed carrier frequency for known protocols:** When the Flipper transmits a decoded protocol (NEC, RC5, etc.), it uses the protocol's standard carrier frequency. There is no way to force a different frequency without using RAW mode.

**Ambient light - the main enemy:** Sunlight contains a strong IR component at 940 nm. Under direct sunlight conditions, the Flipper's TX range can drop to less than 1 meter. Operating indoors or in the evening dramatically increases reliability.

**Line-of-sight required:** IR does not pass through walls, doors, or opaque furniture. It always requires an optical path, even if indirect (bounce). This is a fundamental operational constraint in pentesting.

---

## Structural Limitations Summary Table

| Limitation | Detail | Workaround |
|---|---|---|
| **TX range** | 3-8 meters | Get closer to the target |
| **Emission angle** | ~34 degrees | Aim directly |
| **Single LED** | No redundancy | None (hardware limitation) |
| **Carrier frequency** | Optimized for 38 kHz | RAW for different frequencies |
| **Ambient light** | Reduces range | Operate indoors/in shade |
| **No native external LED** | Not expandable via GPIO | Unofficial hardware mods |
| **AC protocols** | Complex capture | Dedicated remotes per brand |
| **Line-of-sight** | Requires optical path | Use wall bounces |

> **Personal note:** The limited TX range is the factor that conditions all operational IR work. During an engagement, if you need to turn off a display in a conference room, you must enter the room and get within 3-5 meters of the display. You cannot do it from the hallway through a closed door. Always plan physical access before the IR action. That said, bounces in rooms with light-colored walls are surprisingly effective - I have turned off TVs from angles I would not have thought possible, aiming toward the ceiling.

---

*Back to the [main index](README.md)*
