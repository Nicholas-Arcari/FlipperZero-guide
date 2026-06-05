# NRF24L01+ - Overview

**NRF24L01+** 2.4 GHz transceiver module connected via GPIO for sniffing, jamming, and hijacking wireless peripherals (mice, keyboards, presenters). Includes the famous **MouseJacker** attack.

**Chip:** NRF24L01+ | **Frequency:** 2.4 GHz ISM | **Channels:** 126 (2400-2525 MHz) | **Protocol:** Enhanced ShockBurst | **Interface:** SPI via GPIO

---

## Contents

| # | File | Description |
|---|------|-------------|
| 01 | [Fundamentals and Hardware](01-Fondamenti-e-Hardware.md) | NRF24L01+ specs, Enhanced ShockBurst, 2.4 GHz ISM, wiring GPIO, antenna |
| 02 | [MouseJacker Deep Dive](02-MouseJacker-Deep-Dive.md) | MouseJacker attack: vulnerable devices, Logitech Unifying, keystroke injection via wireless mouse |
| 03 | [Operational Tools](03-Tool-Operativi.md) | NRF24 sniffing, 2.4 GHz jamming, Channel Scan, NRF24Monitor, Scanner, Batch operations |
| 04 | [Real-World Scenarios](04-Scenari-Reali.md) | Pentest scenarios: wireless keyboard exploitation, meeting room attack, device enumeration |
| 05 | [Attacks and Defenses](05-Attacchi-e-Difese.md) | Legal aspects + NRF24 attacks + countermeasures + detailed Flipper tool operations |
| 06 | [Personal Experience](06-Esperienza-Personale.md) | Field notes, summary, recommendations |

---

## Quick Reference - NRF24 Attacks

| Attack | Target | Complexity | Impact |
|--------|--------|------------|--------|
| MouseJacker | Unencrypted wireless mice/keyboards | Low | Keystroke injection |
| Sniffing | NRF24 communications | Medium | Data interception |
| 2.4 GHz Jamming | Any 2.4 GHz device | Low | DoS |
| Channel Scan | NRF24 devices | Low | Reconnaissance |

> **Personal note:** MouseJacker is devastating in office environments where cheap wireless mice and keyboards are everywhere. During an engagement I injected commands into a non-Unifying Logitech mouse from the adjacent meeting room - keystroke injection through the wall. The owner had no idea what was happening.
