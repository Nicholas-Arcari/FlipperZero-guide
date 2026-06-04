## Legal Aspects

### Italian Regulations

The use of the Flipper Zero's IR module in Italy falls within a less defined regulatory context compared to radio transmissions (Sub-GHz), but it is not without legal implications.

### What Is NOT Illegal

- **Capturing IR signals** from your own remote controls (reverse engineering of your own devices)
- **Using the Flipper as a remote** for your own devices
- **Analyzing and studying** IR protocols for educational and research purposes
- **Capturing ambient IR signals** - IR is not a "reserved" communication (there is no equivalent of intercepting radio communications)
- **Possessing** the Flipper Zero and its IR module

### What CAN Be Illegal

**Interference with other people's devices:**

Using the IR module to control or interfere with devices owned by others without authorization can constitute various offenses:

- **Art. 615-ter Italian Penal Code (Unauthorized access to a computer/telematic system):** If the device controlled via IR is connected to a computer system (e.g., digital signage display connected to a networked media player), unauthorized access via IR could be challenged as system access. The interpretation is broad and not yet consolidated in case law for IR attacks
- **Art. 635 Italian Penal Code (Damage to property):** Turning off a display or system in use can constitute damage (rendering someone else's property unusable, even temporarily)
- **Art. 340 Italian Penal Code (Interruption of public service):** If the device is part of a public service (information display at a train station, airport, hospital), interference can have serious criminal consequences
- **Art. 674 Italian Penal Code (Disturbance of occupations or rest):** A minor offense but applicable in contexts such as cinemas, waiting rooms, shared environments

### In the Penetration Testing Context

An authorized penetration test requires:

- **Written contract** that explicitly specifies the engagement scope
- **Explicit inclusion** of tests on IR/environmental control devices within the test perimeter
- **Authorization from the owner** of the building/devices (not just the client, if different)
- **Rules of engagement (ROE)** that define what is permitted
- **Get-out-of-jail letter** for protection in case of law enforcement intervention

> **Personal note:** Unlike Sub-GHz where the radio emission regulations are clear and codified, IR operates in a legal gray area. My advice: always treat IR as if it were regulated. Include IR tests explicitly in the contract, document every action, and obtain prior authorization. The absence of specific regulation is not a protection - a judge can apply general rules by analogy.

---
