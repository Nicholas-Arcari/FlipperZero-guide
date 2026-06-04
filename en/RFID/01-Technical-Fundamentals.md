# Technical Fundamentals - RFID 125 kHz

## What is RFID 125 kHz

RFID (Radio-Frequency Identification) at 125 kHz is a radio-frequency identification technology that operates in the LF (Low Frequency) band. It is the oldest and simplest form of RFID still in massive use, born in the 1980s and extremely widespread in:

- **Access control** - apartment building badges, offices, parking garages, gyms
- **Animal identification** - subcutaneous microchips (ISO 11784/11785)
- **Attendance tracking** - employee time clocks
- **Industrial systems** - asset identification, legacy logistics
- **Automation** - coffee machines, vending machines, lockers
- **Hotels and hospitality** - room keys (often migrated to NFC by now)

The 125 kHz frequency (and its 134.2 kHz variant used in FDX-B) falls in the LF band, well below NFC frequencies (13.56 MHz) and Sub-GHz (300-900 MHz). This has precise physical implications.

---

## How It Works at the Physical Level

The operating principle is **near-field inductive coupling**. Here is what happens when you bring a badge close to a reader:

1. **The reader generates an oscillating magnetic field at 125 kHz** through its antenna (a coil). This field carries energy, not data.

2. **The tag's antenna (a coil printed on the badge circuit)** is immersed in the magnetic field. According to Faraday's law, a change in magnetic flux through a coil induces an electromotive force (voltage).

3. **The induced voltage powers the tag's chip**. This is why passive tags have no battery: they receive all their energy from the reader's field. An internal capacitor accumulates the charge.

4. **Once powered, the chip begins transmitting its ID** by modulating the load on the antenna (load modulation). In practice, the chip connects and disconnects a resistive load in parallel with its coil, varying the impedance seen by the reader.

5. **The reader detects these impedance variations** as small fluctuations in the amplitude or frequency of the field it is generating. It demodulates these variations and reconstructs the bit sequence of the ID.

6. **The reader compares the received ID** against its database and decides whether to grant access or not.

This process occurs in a few milliseconds and repeats continuously as long as the tag is within the field.

> **Personal note:** The key concept to understand is that the tag does NOT transmit anything in the strict sense. It merely modifies the load seen by the reader's antenna. It is like someone pressing and releasing the brake on a wheel you are spinning - you would feel the change in resistance. This is the "transmission" of a passive RFID tag.

---

## Passive Tags vs Active Tags

**Passive Tags (the vast majority at 125 kHz):**
- No internal battery
- Powered exclusively by the reader's field
- Typical range: 2-15 cm (depends on the reader's antenna)
- Unlimited lifespan (as long as the chip is not physically damaged)
- Cost: 0.05-0.50 EUR per tag
- Size: can be extremely small (2mm for animal implants)
- All apartment building badges, access cards and animal microchips are passive

**Active Tags:**
- Internal battery (lithium, 3-10 year lifespan)
- Range: up to 100 meters
- Cost: 5-50 EUR per tag
- Used in industrial logistics, vehicle tracking, electronic toll collection
- Do NOT operate at 125 kHz (they use UHF 860-960 MHz or 2.4 GHz)
- The Flipper Zero does NOT handle active tags

For 99.9% of work with the Flipper Zero on RFID 125 kHz, we are talking exclusively about passive tags.

---

## Signal Modulation

RFID 125 kHz tags use different modulation techniques to encode bits. Understanding modulation is fundamental for debugging and understanding why certain tags are not read.

**ASK (Amplitude Shift Keying):**
- The most common technique at 125 kHz
- The tag varies the amplitude of the reflected signal
- Bit 1 = high amplitude, Bit 0 = low amplitude (or vice versa)
- Used by: EM4100, HID Prox, most budget tags
- Simple to demodulate but sensitive to ambient noise
- OOK variant (On-Off Keying): special case of ASK where bit 0 = no signal

**FSK (Frequency Shift Keying):**
- The tag varies the subcarrier frequency
- Two distinct frequencies represent 0 and 1
- Used by: HID Prox (FSK2 at 50 kHz / 40 kHz), Indala
- More robust against noise compared to ASK
- FSK1: frequencies RF/8 and RF/5 (15.625 kHz and 25 kHz)
- FSK2: frequencies RF/8 and RF/10 (15.625 kHz and 12.5 kHz)

**PSK (Phase Shift Keying):**
- The tag varies the phase of the signal
- Bit 1 = phase inversion, Bit 0 = no inversion (or vice versa)
- Used by: some industrial tags, AWID, Pyramid
- The most robust against noise but the most complex to demodulate
- PSK1: phase change on 0->1 transition
- PSK2: phase change on every bit 1
- PSK3: bidirectional variant

---

## Data Encoding (Line Coding)

Beyond RF modulation, data is encoded with specific schemes to ensure clock synchronization between reader and tag:

**Manchester Encoding:**
- The most widespread standard (used by EM4100)
- Each bit is represented by a transition at mid-period
- Bit 1 = low->high transition
- Bit 0 = high->low transition
- Advantage: the clock is embedded in the signal, self-synchronizing
- Disadvantage: requires double the bandwidth (each bit occupies two clock periods)

**Biphase (FM0/FM1):**
- Used by HID, FDX-B
- Transition at the beginning of every bit period
- Bit 0 or 1 = additional transition at mid-period (depends on variant)

**NRZ (Non-Return-to-Zero):**
- The simplest: high level = 1, low level = 0
- No guaranteed transition - synchronization issues on long sequences of 0s or 1s
- Rarely used alone, often combined with scrambling

**Differential Manchester:**
- Variant of Manchester where encoding depends on the transition relative to the previous bit
- More robust against inverted polarity

---

## Data Rate

The transmission speed of 125 kHz tags is extremely low:

- **EM4100:** RF/64 = ~1.95 kbps (125000 / 64)
- **HID Prox:** RF/50 = 2.5 kbps
- **FDX-B:** RF/32 = ~3.9 kbps
- **T5577:** configurable, typically RF/32 or RF/64

For comparison, NFC operates at 106-848 kbps and Wi-Fi at hundreds of Mbps. The low speed is not an issue because an ID is only a few bytes long - the complete transmission takes just a few milliseconds.

> **Personal note:** The low data rate has a practical advantage: 125 kHz tags are extremely tolerant of misalignment and distance. You can read an EM4100 even with the Flipper not perfectly centered on the tag's antenna, something much more difficult with NFC at 13.56 MHz. This makes "on-the-fly" cloning (social engineering, quick pass) considerably more feasible.
