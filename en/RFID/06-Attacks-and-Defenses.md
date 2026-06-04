## Attacks and Countermeasures

### Replay / Cloning

**The attack:**
1. The attacker reads the victim's badge (3-8 cm distance, less than 1 second)
2. Clones the ID to a T5577 (5 seconds)
3. Uses the clone to gain access

**Feasibility:** Trivial. No technical skill required. The Flipper Zero makes the process accessible to anyone.

**Acquisition scenarios:**
- In line at the coffee machine (the badge is hanging around the neck)
- At a restaurant (the badge is in the bag/jacket on the adjacent chair)
- In an elevator (confined spaces, forced proximity)
- Badge left on the desk
- Badge in the back pocket of trousers (easy to approach)

**Countermeasures:**
- **Migration to NFC with encryption** (MIFARE DESFire EV2/EV3, HID SEOS)
- **Multi-factor:** badge + PIN, badge + biometric
- **Shielding sleeves** (Faraday sleeve) - limited effectiveness, inconvenient
- **Policy:** badge always concealed, never left unattended
- **Monitoring:** access logs with alerts on anomalies (same badge in two different locations)

### Brute Force

**The attack:**
1. The attacker knows the badge type (e.g. HID 26-bit) and the Facility Code
2. Uses the RFID Fuzzer to try sequential Card Numbers
3. With 65536 possibilities at 3-5 IDs/second: ~4-6 hours for the complete space
4. In practice much less, because CNs are often in limited ranges

**Feasibility:** Medium. Requires hours of physical access to the reader (not discreet) but technically simple.

**Countermeasures:**
- **Rate limiting:** the reader locks out after N failed attempts within T seconds
- **Alarm:** notification to the security center after anomalous attempts
- **Logging:** recording every attempt (including failed ones) with timestamps
- **Anti-tamper:** detection of physical reader tampering
- **Non-sequential Card Numbers:** using random numbers makes brute force less efficient

### Jamming

**The attack:**
1. The attacker generates a strong 125 kHz signal that "drowns out" the legitimate badge signal
2. The reader cannot read any badge
3. Used as a DoS (Denial of Service) or to force manual door opening

**Feasibility:** The Flipper Zero is NOT an effective jammer (power too low). Dedicated hardware is needed. But the concept is important to understand.

**Countermeasures:**
- **RF detection:** sensors that detect anomalous fields at 125 kHz
- **Failsafe policy:** if the reader is not working, the door stays closed (fail-closed) - NEVER fail-open
- **Backup:** secondary access system (PIN pad, mechanical key)
- **Monitoring:** alert when a reader fails to read badges for an anomalous period

### Long-Range Skimming

**The attack:**
1. The attacker builds an RFID reader with an amplified antenna
2. Hides it at a point where badges pass nearby (under a doormat, inside a small table)
3. The reader captures badge IDs without the owners noticing
4. The IDs are saved and cloned later

**Feasibility:** Medium-high for a motivated attacker. Requires custom hardware but components are inexpensive and guides are available online. With a well-designed antenna, the read distance can reach 30-50 cm (much more than the Flipper).

**Countermeasures:**
- **Shielding sleeves** for badges
- **Encryption** (makes the captured ID useless without the key)
- **Regular physical inspection** of sensitive areas
- **Policy:** badge in shielding sleeve when not in use

### Database Manipulation

**The attack:**
1. The attacker compromises the access management system (often a Windows PC with proprietary software)
2. Adds their own ID to the authorized database
3. Or disables the control and puts the system in "pass-through" mode

**Feasibility:** Requires network access or access to the controller PC. This is a cyber attack, not a physical one, but often more devastating than cloning.

**Countermeasures:**
- **Network segregation** of the access control system (dedicated VLAN)
- **Hardening** of the controller server/PC
- **Audit logs** with protected integrity
- **Monitoring** of database modifications

---
