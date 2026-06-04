# Hardware and Real-World Limitations - RFID 125 kHz

## The Flipper Zero LF Antenna

The Flipper Zero integrates a dedicated antenna for the LF 125 kHz band, separate from the NFC antenna (13.56 MHz):

- **Type:** copper trace coil printed on PCB
- **Position:** lower part of the device, below the screen
- **Resonant frequency:** tuned to 125 kHz (with matching network)
- **Dual function:** both reader (generates field) and emulator (modulates load)
- **Controller:** dedicated chip for LF protocol management

The LF antenna is physically larger than the NFC one, which gives it a slight advantage in terms of range compared to HF.

---

## Real-World Range

The declared range and the actual range diverge significantly:

**In read mode (Flipper as reader):**
- **EM4100:** 3-8 cm (depends on tag size)
- **HID Prox (ISO card format):** 3-6 cm
- **HID Prox (keyfob):** 2-4 cm (smaller antenna)
- **FDX-B (animal implant):** 1-3 cm (microscopic antenna)
- **T5577 (coin/card):** 3-7 cm

**In emulation mode (Flipper as tag):**
- **On standard wall-mounted reader:** 2-5 cm
- **On long-range reader:** 3-8 cm
- **On portable reader:** 1-3 cm

**Factors affecting range:**

| Factor | Effect |
|---|---|
| Tag antenna size | Larger = more range |
| Reader power | Industrial readers > consumer readers |
| Metal interference | Nearby metal drastically reduces range |
| Orientation | Parallel coils = maximum range |
| Flipper battery | Below 20% TX power drops |
| Cases/covers | Metal cases eliminate reading entirely |
| Temperature | Extreme temperatures reduce efficiency |

> **Personal note:** The Flipper's LF range is noticeably better than its NFC range. On average I get 5-8 cm on EM4100 card-format tags, versus the typical 2-4 cm for NFC MIFARE reads. This makes a huge difference in pentesting: with LF you can read a badge in someone's back pocket by passing relatively close. With NFC you practically have to touch the badge. I have verified this across dozens of engagements.

---

## Power Limitations

The Flipper Zero, being battery-powered and with a small antenna, has intrinsic limitations:

- **Generated field power:** sufficient for standard tags but insufficient for very small or shielded tags
- **No external amplification:** it is not possible to connect external LF antennas (unlike Sub-GHz with SMA)
- **Continuous read power consumption:** approximately 50-80 mA (drains the battery in 3-4 hours)
- **Continuous emulation:** similar to reading, approximately 60 mA

---

## Comparison with Proxmark3

The Proxmark3 (especially the RDV4 version) is the gold standard for RFID/NFC in pentesting. Here is an honest comparison:

| Feature | Flipper Zero | Proxmark3 RDV4 |
|---|---|---|
| **LF read range** | 3-8 cm | 5-15 cm |
| **LF emulation range** | 2-5 cm | 3-10 cm |
| **Supported LF protocols** | ~10 | 50+ |
| **Raw sniffing** | No | Yes (essential) |
| **ID brute force** | Yes (RFID Fuzzer) | Yes (faster and more configurable) |
| **Custom demodulation** | No | Yes (any modulation) |
| **T5577 writing** | Yes | Yes (with more options) |
| **EM4305 writing** | No | Yes |
| **Raw signal analysis** | No | Yes (built-in oscilloscope) |
| **Form factor** | Pocket-sized, discreet | Bulky, requires laptop |
| **Battery life** | 4-6 hours | USB-powered |
| **Price** | ~170 EUR | ~300-400 EUR (RDV4) |
| **Learning curve** | Low | High (CLI-based) |
| **Discretion** | Excellent (looks like a toy) | Poor (looks like a hacking device) |

**When to use the Flipper:**
- Quick read/clone of EM4100, HID, Indala badges
- On-the-fly emulation during an engagement
- Initial reconnaissance (what type of tag is this?)
- Situations where discretion is critical
- Standard badges without special protections

**When you need the Proxmark3:**
- Raw signal analysis (unknown demodulation)
- Exotic protocols not supported by the Flipper
- Massive ID brute force
- Writing to tags other than T5577 (EM4305, Q5, etc.)
- Sniffing reader-tag communication
- Research and reverse engineering of proprietary protocols

> **Personal note:** In 90% of physical pentesting engagements in Italy, the Flipper Zero is sufficient. Apartment buildings use EM4100, small and medium businesses use HID Prox without encryption. I only need the Proxmark3 for special cases: unknown tags, proprietary industrial systems or when I need to do passive sniffing of the communication. I always carry both, but the Flipper comes out of my pocket 10 times more often than the Proxmark.
