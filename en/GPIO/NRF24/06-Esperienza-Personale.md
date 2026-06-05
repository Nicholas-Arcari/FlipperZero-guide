## 11. Personal Experience -- Lessons from the Field

This section collects lessons learned during years of working with the NRF24 module on the Flipper Zero.

> Personal note: the NRF24L01+ was the first GPIO module I connected to the Flipper Zero, and it remains the one I use most often. It costs less than 2 euros in the base version, less than 5 in the PA+LNA version, and opens up a world of possibilities for wireless pentesting. It's the best cost-to-impact ratio I know of in the security field.

> Personal note: the most common mistake I see in beginners is underestimating power supply. The NRF24L01+ is extremely sensitive to power quality. Without a capacitor, the module works "almost" always -- but that "almost" will cost you hours searching for bugs in the software when the problem is hardware. Solder a capacitor on it and don't think about it again.

> Personal note: for MouseJacker, payload preparation is everything. A well-written payload works on the first try. A poorly written payload fails unpredictably. ALWAYS test your payloads on your own PC before using them during an audit. I've seen payloads that worked perfectly on Windows 10 and failed on Windows 11 due to changes in Start menu behavior. Test on the same OS version as the target.

> Personal note: range is the factor that changes everything. With the base version at 1.50 euros, you need to be in the same room as the target. With the PA+LNA at 5 euros, you can operate from the hallway, from the adjacent meeting room, or from the floor above. With a directional antenna, from the parking lot. Invest in the PA+LNA version -- it's the choice that makes the difference between "proof of concept in the lab" and "realistic attack in the field".

> Personal note: during an audit in a large open space, I used the Scanner to map all wireless devices. The result was a map with 47 mice and 12 wireless keyboards. 68% were vulnerable to MouseJacker. When I presented the data to the CISO, the response was: "we didn't even know we had that many wireless devices". The first step of remediation is always knowing what you have. The NRF24 Scanner is the perfect tool for this inventory.

> Personal note: one thing that is never said enough: MouseJacker works through walls too. 2.4 GHz waves easily penetrate office walls (drywall, glass, wood). Only thick reinforced concrete and metal block them significantly. This means an attacker in the hallway, in the adjacent office, or even on the floor above can potentially reach your wireless mouse. The "physical security" of a closed room does not protect against radio waves.

> Personal note: my favorite setup for field work is Flipper Zero + NRF24L01+ PA+LNA with a 5 dBi dipole antenna, all in a jacket pocket. It's completely invisible and the range is more than sufficient for any indoor scenario. For long-distance operations I have an 8 dBi Yagi antenna in a backpack, but I rarely use it -- the dipole is almost always sufficient.

---

## 12. Summary and Recommendations

### For the pentester:

1. Invest in the PA+LNA version with a 47 uF capacitor -- it's the minimum serious setup
2. Always have tested payloads ready for Windows, macOS, and Linux
3. Do a Channel Scan as the first step, always
4. Document every device found with address, channel, type, and vulnerability
5. Don't underestimate the legal aspects: specific written authorization for RF activities

### For the defender:

1. Inventory all wireless peripherals in the organization
2. Update Logitech Unifying dongle firmware
3. Replace non-updatable peripherals with Bluetooth or wired models
4. For critical workstations (C-suite, finance, IT admin): wired peripherals only
5. Implement corporate policies on the use of wireless peripherals
6. Include wireless peripheral testing in periodic security audits

### For the researcher:

1. The NRF24L01+ is the ideal platform for studying 2.4 GHz wireless protocols
2. The sniffer combined with payload analysis enables complete reverse engineering
3. Nordic Semiconductor documentation (datasheets, application notes) is excellent
4. The open-source community around the NRF24 is very active and collaborative
5. Every cheap wireless device is a potential research target
