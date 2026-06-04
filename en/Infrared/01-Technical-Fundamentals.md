# Technical Fundamentals - Infrared Communication

## What Is Infrared Communication

Infrared (IR) communication is a form of optical data transmission that uses light in the infrared spectrum, invisible to the human eye. In the context of consumer remote controls and the Flipper Zero, we operate in the **near-infrared (NIR)** region with a wavelength centered on **940 nm** (nanometers).

Unlike radio communications (Sub-GHz, NFC), IR communication is **optical and directional**: it requires a relatively clear path between transmitter and receiver (line-of-sight), although bounces off walls and ceilings provide some operational margin in indoor environments.

---

## How It Works - From LED to Bit

The IR communication process follows a precise chain:

1. **The transmitter** (remote control, Flipper Zero) activates an infrared LED at 940 nm
2. **The LED emits pulses** of IR light - not a continuous beam, but a modulated sequence
3. **Modulation occurs on a carrier** - typically at **38 kHz** (the most common), but devices exist that use 36 kHz, 40 kHz, or 56 kHz
4. **The receiver** (TV, AC, projector) contains a photodiode + filter + demodulator that extracts the useful signal from the carrier
5. **The receiver's microcontroller** decodes the bit sequence and executes the corresponding command

---

## Why a Carrier Frequency Is Used

Modulating the IR signal on a 38 kHz carrier (or similar) serves to **distinguish the useful signal from ambient light**. The sun, incandescent lamps, and fluorescent lights all emit infrared radiation, but none of them oscillate at 38 kHz. The IR receiver is designed with a bandpass filter centered exactly on that frequency, which allows it to:

- **Reject noise** from ambient light (which is "DC" or at very different frequencies)
- **Amplify only the signal** modulated at the correct frequency
- **Operate even in bright environments** (outdoors with direct sunlight, provided the distance is reduced)

The process in the receiver:

```
IR light received -> Photodiode -> 38kHz bandpass filter -> Amplifier -> Demodulator -> Digital signal
```

The demodulator produces a digital output: **LOW** when it detects the carrier (burst) and **HIGH** when it does not (space). This demodulated signal is what the microcontroller analyzes to extract the bits.

---

## Duty Cycle

The carrier's duty cycle affects signal power and energy consumption:

- **Typical duty cycle:** 25-33% (one third of the period at high level)
- **50% duty cycle:** maximum power but maximum consumption - rarely used in battery-powered remotes
- **25% duty cycle:** common compromise - sufficient to trigger the receiver with lower consumption

The Flipper Zero uses a **33%** duty cycle for transmission, which is the standard value for most consumer protocols.

---

## Modulated vs RAW Signals

There are two fundamental ways to represent an IR signal:

**Modulated signal (known protocol):**
The signal is decoded and represented as protocol + address + command. Example: `NEC, Address: 0x04, Command: 0x08`. This is compact and allows the Flipper to regenerate the perfect signal.

**RAW signal:**
The signal is recorded as a raw sequence of timings: durations of bursts (carrier active) and spaces (silence), in microseconds. Example: `9000 4500 560 560 560 1690 ...`. This method works for any IR signal, even those with unknown or proprietary protocols, but the resulting files are larger and may have minor timing inaccuracies.

> **Personal note:** In daily practice, 80% of consumer devices use known protocols (NEC above all). But when you encounter an air conditioner with a proprietary protocol or an industrial digital signage system, RAW capture becomes the only option. Always keep the difference in mind: modulated = precise and compact, RAW = universal but less reliable over long distances.

---

*Back to the [main index](README.md)*
