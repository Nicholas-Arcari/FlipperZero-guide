# Hardware and Real-World Limitations

## The ST25R3916 Chip

The Flipper Zero uses the **ST25R3916** by STMicroelectronics:

- **Supported standards:** ISO 14443A/B, ISO 15693, FeliCa, NFC-V
- **Frequency:** 13.56 MHz
- **Field power:** adjustable, sufficient for standard tags
- **Read distance:** 2-5 cm (standard tags), up to 8-10 cm under ideal conditions
- **Data rate:** up to 6.78 Mbit/s (NFC-A/B high speed)
- **Capabilities:** reader, emulator, sniffing (limited)

---

## Real-World Limitations You Need to Know

**Read distance:** The Flipper reads tags at a maximum of 3-5 cm in practice. This is a critical limitation during pentesting - you must get very close to the target badge. The NFC coil is located on the upper part of the Flipper (above the screen).

**Imperfect emulation:** The Flipper's NFC emulation is not on par with a Proxmark3 or ChameleonMini. Some readers reject emulation due to timing differences or field level discrepancies. Certain access control systems have anti-emulation filters.

**No full EMV support:** The Flipper can read basic data from NFC payment cards (PAN, expiry) but cannot clone or emulate payment cards - EMV systems use asymmetric cryptography and challenge-response that the Flipper cannot replicate.

**MIFARE Classic only:** The crypto1 attack only works on MIFARE Classic. MIFARE Plus (SL3), DESFire, SEOS, and iClass SE tags are not vulnerable to the same attack.

**Limited sniffing:** The Flipper can perform NFC sniffing but the quality is inferior to a Proxmark3. For reliable reader-tag communication captures, the Proxmark remains the standard.

> **Personal note:** Read distance is the biggest problem in NFC pentesting. To read a badge, you need to get within 5 cm of the person carrying it - this requires social engineering techniques or situations where the badge is set down (e.g., on a desk). I've had success reading badges left on the table in the cafeteria during lunch break. Never underestimate the physical distance required.

---

## Comparison with Other Tools

| Feature | Flipper Zero | Proxmark3 RDV4 | ChameleonMini | ACR122U |
|---|---|---|---|---|
| **Portability** | Excellent | Good | Good | Desktop |
| **Read distance** | 3-5 cm | 5-8 cm | 3-5 cm | 5-8 cm |
| **Emulation** | Fair | Excellent | Excellent | No |
| **Sniffing** | Limited | Excellent | Good | No |
| **Ease of use** | High | Low | Medium | Medium |
| **Cost** | ~170 EUR | ~300 EUR | ~50 EUR | ~30 EUR |
| **Stealth** | High | Medium | High | None |

> **Personal note:** The Flipper is unbeatable for stealth - it looks like a toy and nobody suspects a thing. The Proxmark is technically superior but draws attention. For field pentesting, I use the Flipper for the collection phase and the Proxmark in the lab for in-depth analysis.
