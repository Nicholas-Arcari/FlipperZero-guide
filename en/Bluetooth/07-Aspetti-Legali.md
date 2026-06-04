## Legal Aspects

The use of the Flipper Zero's BLE features in unauthorized contexts has significant legal implications.

### BLE Spam

BLE Spam constitutes **interference with other people's wireless communications**. In Italy and the EU:

- **Directive 2014/53/EU (RED)** - Regulates the use of radio equipment. Sending radio signals that interfere with other people's devices is prohibited
- **Art. 617-bis c.p. (Italy)** - Installation of equipment designed to intercept or prevent communications
- **Art. 617-quater c.p.** - Unlawful interception, prevention, or interruption of computer or telematic communications
- **Electronic Communications Code (D.Lgs. 259/2003)** - Regulates the use of the radio spectrum in Italy

In practice, BLE Spam in a public place without authorization can be prosecuted as disturbance of communications, interference with other people's wireless devices, or in extreme cases as computer sabotage if it causes measurable damage.

### BLE HID (BadBT)

The use of BadBT on other people's devices without authorization constitutes **unauthorized access to a computer system** (Art. 615-ter c.p. in Italy), aggravated by the fact that it occurs without physical contact.

### BLE Scanning

Passive scanning of nearby BLE devices is generally legal (devices voluntarily transmit on public bands). However:

- Systematic tracking of individual BLE devices may violate GDPR (the BLE MAC address is personal data if associable with an individual)
- The use of collected data for profiling or surveillance is subject to privacy regulations
- In corporate contexts, internal policy may prohibit wireless scanning

### Recommendations

- **Always obtain written authorization** before any BLE testing in environments you don't own
- **Define the scope** - Specify which BLE features will be used and on which targets
- **Document everything** - Timestamps, screenshots, logs of every activity
- **Do not use BLE Spam in public places** - Hospitals, airports, public transportation are sensitive environments
- **Beware of medical devices** - Pacemakers, insulin pumps, and other BLE medical devices must NEVER be targets of unauthorized testing
- **Educational context** - In educational settings, use controlled environments (isolated lab, Faraday cage)

> **Personal note:** In every engagement that includes BLE testing, I include a specific clause in the contract listing the authorized BLE techniques (scanning, spam demo, HID testing) and the specific targets. I never use BLE Spam in shared public areas or in areas with medical devices. For awareness demos, I limit the range of action to the designated meeting room and notify participants before starting. Transparency is fundamental - BLE Spam is a demo, not an attack.

---
