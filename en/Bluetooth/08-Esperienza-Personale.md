## Troubleshooting and Limitations

### BLE Range Issues

**Symptom:** BLE Spam doesn't reach target devices, the scanner doesn't find devices, BadBT disconnects frequently.

**Causes and solutions:**

| Cause | Solution |
|---|---|
| Excessive distance | Move closer to < 10 meters |
| Antenna orientation | Rotate the Flipper 90 degrees |
| Physical obstacles | Remove obstacles between Flipper and target |
| WiFi interference | Move away from WiFi routers / access points |
| Human body | Don't keep the Flipper in your pocket, place it on a surface |
| Low battery | TX power decreases with low battery |
| Outdated firmware | Update firmware and wireless stack |

### 2.4 GHz Interference

The 2.4 GHz band is shared by many protocols and devices:

- **WiFi (802.11b/g/n)** - The biggest interferer, especially channels 1, 6, 11
- **Bluetooth Classic** - Uses the same band but with different hopping
- **ZigBee** - Channels 11-26 overlapping with WiFi
- **Microwaves** - Spurious emissions in the 2.4 GHz band
- **USB 3.0** - Electromagnetic emissions in the 2.4 GHz band (known issue)
- **Baby monitors** - Many operate at 2.4 GHz
- **Drones** - Remote controllers at 2.4 GHz

In environments with many WiFi networks (offices, conferences), BLE performance degrades. BLE frequency hopping partially mitigates the problem but does not eliminate it.

**Practical mitigation:**

- Test during times of lower WiFi usage
- Position the Flipper away from WiFi routers and access points
- If possible, use the WiFi channel farthest from BLE advertising channels (avoid WiFi channel 1 near BLE ch.37 and WiFi channel 11 near BLE ch.39)

### BLE Spam Compatibility by OS

Not all devices react to spam in the same way:

**Apple (iOS):**

| iOS Version | Behavior |
|---|---|
| iOS 16.x and earlier | Frequent popups, no rate limiting |
| iOS 17.0 - 17.1 | Frequent popups, minimal mitigations |
| iOS 17.2+ | Active rate limiting, less frequent popups |
| iOS 18.x | Improved mitigations, rare popups if Bluetooth properly disabled |

**Android:**

| Condition | Behavior |
|---|---|
| Android + Google Play Services | Fast Pair popups active |
| Samsung + SmartThings/Wearable | Samsung popups active |
| Android without Google Play Services | No popups (e.g., Huawei without GMS) |
| Android 14+ | Improved rate limiting on Fast Pair |

**Windows:**

| Condition | Behavior |
|---|---|
| Windows 10/11 with Swift Pair enabled | Toast notification |
| Windows 10/11 with Swift Pair disabled | No popups |
| Windows with Bluetooth disabled | No popups |

### Common BadBT Issues

| Problem | Cause | Solution |
|---|---|---|
| Target doesn't see the Flipper | Advertising not active or insufficient range | Restart BadBT, move closer |
| Pairing rejected | User cancelled or PIN doesn't match | Retry, verify PIN on Flipper display |
| Incorrect keystrokes | Wrong keyboard layout | Specify layout in script (DELAY, ALT codes) |
| Script too fast | Target doesn't process keystrokes in time | Increase DELAYs between commands |
| Frequent disconnections | Insufficient BLE range or interference | Move closer, reduce interference |
| Bonding lost | Target removed the pairing | Redo the pairing |
| Wrong special characters | IT/US/UK layout differences | Test the layout before the engagement |

### BLE Scanner Issues

| Problem | Cause | Solution |
|---|---|---|
| Few devices found | Limited range or devices not advertising | Move around the area, wait longer |
| All MAC addresses random | Modern devices with BLE privacy | Use device name for identification |
| No device name | Device doesn't include Local Name | Analyze Manufacturer Specific Data and service UUIDs |
| Unstable RSSI | Multipath, interference, movement | Average over multiple readings |

### General Flipper BLE Limitations

Summary of the main limitations:

1. **BLE only, no Bluetooth Classic** - Cannot interact with audio headphones, file transfer, BT Classic tethering
2. **No active connection sniffing** - Only sees advertising, not data traffic
3. **Non-replaceable antenna** - Fixed range, cannot be improved with an external antenna
4. **Limited TX power (+6 dBm)** - Lower range than many commercial BLE devices
5. **No native MITM** - Requires dedicated hardware and software
6. **No advanced fuzzing** - Limited capabilities for systematic GATT fuzzing
7. **No cracking** - Cannot crack pairing keys or session keys
8. **One role at a time** - Cannot be central and peripheral simultaneously for MITM
9. **No BLE direction finding** - Does not support AoA/AoD (Angle of Arrival/Departure)
10. **Limited user interface** - The small screen limits scan data visualization

---

## Personal Experience

> **Personal note:** The Flipper Zero's BLE module is probably the least technical and most "social" among all modules. BLE Spam is not a sophisticated attack - it's a visual demo that conveys a security concept in 10 seconds. BadBT is more technical but requires social engineering for the initial pairing. The scanner is useful for reconnaissance but limited compared to dedicated tools.

> **Personal note:** My setup for complete BLE assessments includes: Flipper Zero (for quick scanning and spam demos), nRF52840 dongle with Sniffle (for complete BLE sniffing), Linux laptop with Wireshark and BLEzzer (for analysis and fuzzing), and an Ubertooth as backup for Bluetooth Classic scenarios. The Flipper is the first-contact tool - quick, portable, visually effective. For in-depth analysis, dedicated tools are needed.

> **Personal note:** A common mistake I see in junior pentesters: thinking that BLE Spam is an "attack." It's not. It's interference with the user experience, not a compromise of data or systems. It has no value in a pentest report as a critical vulnerability. It has value as an awareness demo and as proof that vendor proximity pairing protocols have design flaws. The real vulnerability is that Apple, Samsung, Google, and Microsoft have implemented systems that display popups based on unauthenticated radio packets - and this is a protocol design problem, not a Flipper problem.

> **Personal note:** BLE HID (BadBT) is the BLE feature with the most real offensive potential. The ability to execute payloads from a distance, without a cable, with automatic reconnection after bonding, is an underestimated vector. In environments where BadUSB is mitigated (blocked USB ports, device control), BadBT completely bypasses those defenses because it uses a different channel. I've seen very few organizations with specific policies for Bluetooth HID devices. Most block USB but leave Bluetooth completely open.

> **Personal note:** For those who want to go deeper into BLE security testing beyond the Flipper, I recommend studying: the book "Inside Bluetooth Low Energy" by Naresh Gupta, the Sniffle project on GitHub (the best open source BLE sniffer), the GATTacker framework for MITM, and the Bluetooth SIG Core Specification (a 3000+ page document but essential for understanding every detail of the protocol). The Flipper is the entry point - the BLE rabbit hole goes much deeper.

> **Personal note:** One last practical tip: when doing BLE Spam demos, always bring a second phone as a "controlled victim." If the BLE Spam doesn't work well in the environment (interference, updated OS with mitigations), you can still show the effect on your own phone. It's frustrating to prepare a demo and discover that the latest iOS update has reduced popup frequency. The second phone with an older iOS/Android version is your safety net.

---

## Resources and References

- **Bluetooth Core Specification v5.4** - bluetooth.com/specifications/specs/core-specification-5-4/
- **Sniffle BLE Sniffer** - github.com/nccgroup/Sniffle
- **GATTacker** - github.com/securing/gattacker
- **BLE Spam Flipper App** - Available in Momentum, Xtreme, RogueMaster firmwares
- **nRF Connect** (Android/iOS) - Professional BLE analysis tool by Nordic Semiconductor
- **Wireshark BLE Dissector** - wiki.wireshark.org/Bluetooth
- **Google Fast Pair Specification** - developers.google.com/nearby/fast-pair/specifications
- **Apple Continuity Protocol RE** - github.com/furiousMAC/continuern
- **Sweyntooth BLE Vulnerabilities** - asset-group.github.io/disclosures/sweyntooth/
- **Inside Bluetooth Low Energy** (book) - Naresh Gupta, Artech House

---

*Guide written for educational and security research purposes. Every technique described must be used exclusively in authorized environments and in compliance with applicable legislation.*
