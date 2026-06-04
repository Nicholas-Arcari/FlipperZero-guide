# Real-World Penetration Testing Scenarios - NFC

Detailed operational scenarios for using the NFC module in physical penetration testing, red teaming, and security assessment contexts. Every scenario is based on real experiences and includes complete procedure, expected finding, and recommendations.

---

## Scenario 1 - Corporate Badge System Bypass (MIFARE Classic)

**Objective:** demonstrate that the target building's badge system is vulnerable

**Phase 1 - Reconnaissance:**
1. Identify the reader type (HID, Suprema, ZKTeco, etc.)
2. Observe employees: where do they keep their badge? Do they leave it on the desk?
3. Use NFC/RFID Detector to verify the frequency (13.56 MHz NFC vs 125 kHz RFID)

**Phase 2 - Badge Reading:**
1. Social engineering: "May I see your badge for a moment? I'm conducting an authorized security audit" (with management authorization)
2. Alternatively: wait for an employee to leave the badge on the desk → quick read (3 seconds)
3. NFC → Read → identify the type (SAK 0x08 = MIFARE Classic 1K → perfect)
4. Dictionary attack → if all keys found: full dump → immediate cloning
5. If not all keys found: continue with MFKey32

**Phase 3 - MFKey32 (if needed):**
1. Activate Detect Reader
2. Present the Flipper to the turnstile/door reader
3. Repeat 2-3 times
4. Open MFKey → recover the missing keys
5. Re-read the badge → full dump

**Phase 4 - Cloning:**
1. Write the dump to a Gen4 Magic Card
2. Test the Magic Card at the reader → the door opens
3. Document: photos, timestamp, vulnerability type

**Phase 5 - Report:**
- Finding: "The access control system uses MIFARE Classic 1K with keys recoverable via MFKey32 attack"
- Impact: "An attacker with temporary physical access to an employee's badge can clone it in less than 30 seconds and obtain permanent building access"
- CVSS: 7.2+ (High) - Physical access + Authentication Bypass
- Recommendation: "Migrate to MIFARE DESFire EV2 or iClass SE with diversified keys. Implement multi-factor authentication (badge + PIN) for sensitive areas"

---

## Scenario 2 - Hotel Card Analysis

**Objective:** evaluate the security of hotel room cards

**Procedure:**
1. Read your room card (NFC → Read)
2. Identify the type: almost always MIFARE Classic 1K or Ultralight
3. If MIFARE Classic: attempt dictionary attack + MFKey32
4. If you can read all sectors: analyze the data
5. Use NFC Comparator: compare the card before and after opening the door
6. Identify which sector contains the room number/access code
7. Modify the sector → test on a different door (only with hotel authorization)

**Typical findings:**
- Room number in plaintext in sector 1
- No integrity verification (the system accepts modified data)
- Default keys (FFFFFFFFFFFF) not changed
- Possibility of creating master cards by modifying a specific flag

> **Personal note:** I've tested hotel cards across 4 different chains. 3 out of 4 used MIFARE Classic with default keys. In one case, changing a single byte in sector 2 from "01" to "FF" made the card open ALL hotel doors, including staff areas. It was the "master flag". Critical finding that led to the replacement of the entire access system.

---

## Scenario 3 - Relay Attack on Corporate Badge

**Objective:** demonstrate that a badge can be used remotely

**Prerequisites:**
- Two Flipper Zeros (or Flipper + NFC phone with relay app)
- Network to connect the two devices

**Procedure:**
1. Attacker 1 (Proxy): positions near the building's reader
2. Attacker 2 (Relay): positions near the victim (e.g., in the cafeteria, in a meeting)
3. When the victim is nearby, Attacker 2 activates the relay → reads the badge
4. Data is forwarded in real time to Attacker 1
5. Attacker 1 emulates the badge at the reader → the door opens

**Countermeasures:**
- Distance bounding (measures response time to detect the relay)
- PIN required in addition to badge
- Anomalous access monitoring (badge used in two places simultaneously)

---

## Scenario 4 - Multi-Floor Access Control Assessment

**Objective:** evaluate access segmentation in a corporate building with multi-level NFC badges

**Context:** The building has 8 floors with areas at different security levels: reception (level 0), standard offices (levels 1-5), datacenter (level 6), executive suite (level 7). Each employee has a MIFARE Classic 4K badge with permissions for their assigned floors.

**Phase 1 - Badge profiling:**
1. Read a badge from an employee with limited access (e.g., levels 0-2) → NFC → Read
2. SAK 0x18 → MIFARE Classic 4K → dictionary attack
3. Full dump: 40 sectors x 4 blocks = 160 blocks to analyze
4. Repeat with a second badge (levels 0-3) for comparison

**Phase 2 - Data structure analysis:**
1. NFC Comparator: compare the two dumps sector by sector
2. Typical results:
   - Sector 0: UID + manufacturing data (fixed)
   - Sectors 1-2: employee identification data (name/ID in plaintext or obfuscated)
   - Sector 3: **permissions map** - bytes differ between the two badges
   - Sector 4: last access timestamp
   - Sectors 5-39: unused or padding
3. The byte in sector 3, offset 4 contains the bitmask of authorized floors:
   - Badge 1: `0x07` = `00000111` → floors 0, 1, 2
   - Badge 2: `0x0F` = `00001111` → floors 0, 1, 2, 3

**Phase 3 - Privilege escalation:**
1. Write the dump to a Gen4 Magic Card
2. Modify the permissions byte: `0x07` → `0xFF` = `11111111` → all floors
3. Test the Magic Card at the floor 6 reader (datacenter) → access granted!
4. The controller does not verify data integrity → no MAC/checksum

**Phase 4 - Impact assessment:**
1. Test access to every floor with the modified card → document which floor opens
2. Verify whether the logging system records the original badge or the cloned one
3. Check whether an alert exists for unauthorized floor access

**Report:**
- **Critical:** "Access segmentation relies on a plaintext bitmask in sector 3 of the MIFARE Classic 4K badge. Modifying a single byte allows privilege escalation to any level, including the datacenter"
- **High:** "The system does not implement integrity checks on badge data (no MAC, CRC, or digital signature)"
- **Medium:** "Employee identification data is stored in plaintext in sectors 1-2"
- Recommendation: "Implement mutual authentication with diversified keys + MAC on critical sectors. Consider migration to DESFire EV3 with secure messaging"

---

## Scenario 5 - Cafeteria/Prepaid Credit System Audit

**Objective:** evaluate the security of the corporate cafeteriàs NFC payment system

**Context:** The cafeteria uses prepaid NFC cards - employees load credit at the register and spend it with each meal. The system uses MIFARE Classic 1K.

**Phase 1 - Card analysis:**
1. NFC → Read before the meal: full dump with dictionary attack
2. Note the current balance from the receipt: 15.50 EUR
3. Purchase a meal (3.50 EUR), new balance: 12.00 EUR
4. NFC → Read after the meal: new dump

**Phase 2 - Comparison:**
1. NFC Comparator: compare the two dumps
2. Sector 8, Block 0 - before: `0x00 0x00 0x06 0x0E` = 1550 (cents)
3. Sector 8, Block 0 - after: `0x00 0x00 0x04 0xB0` = 1200 (cents)
4. The balance is stored as a 16-bit integer in cents, without any integrity protection

**Phase 3 - Proof of Concept:**
1. Modify sector 8: write `0x00 0x00 0x27 0x10` = 10000 = 100.00 EUR
2. Verify at the register: the terminal shows 100.00 EUR of credit
3. **DO NOT make purchases** - document and restore the original value

**Report:**
- **Critical:** "The prepaid credit balance is stored in plaintext in sector 8 of the MIFARE Classic 1K card. Modification is possible with a 200 EUR device (Flipper Zero) in less than 10 seconds"
- **Financial impact:** potentially unlimited financial loss
- Recommendation: "Migrate to a server-side system where the card contains only an ID and the balance is stored in the central database. If offline operation is required, implement MIFARE DESFire with MAC-authenticated values"

---

## Scenario 6 - Public Transit NFC Assessment

**Objective:** evaluate the security of a city's public transit contactless cards

**Context:** The client (transit authority) wants a security assessment of the contactless cards used for passes and tickets. The cards are MIFARE Classic 1K.

**Phase 1 - Analysis:**
1. Purchase a regular transit card
2. NFC → Read: SAK 0x08, MIFARE Classic 1K
3. Dictionary attack: non-default keys but present in known dictionaries (sector 1 key: `A0A1A2A3A4A5`)
4. Full dump of all 16 sectors

**Phase 2 - Data structure:**
1. Sector 0: UID + manufacturing data
2. Sector 1: pass type (0x01 = single ride, 0x02 = daily, 0x03 = monthly, 0x04 = annual)
3. Sector 2: validity start date (Unix timestamp format)
4. Sector 3: validity end date
5. Sector 4: remaining ride counter (for per-ride tickets)
6. Sector 5: last validator (reader ID)

**Phase 3 - Manipulation testing:**
1. Single ride card with 0 rides remaining
2. Modify sector 4: counter from 0 → 10
3. Present at the turnstile → the turnstile accepts the card (rides recharged!)
4. Modify sector 1: type from 0x01 → 0x04 (single ride → annual)
5. Modify sector 3: end date from expired → +1 year
6. Present at the turnstile → access as annual pass holder

**Report:**
- **Critical:** "Transit cards use MIFARE Classic 1K with known keys. All data (pass type, validity, rides) can be modified without integrity checks"
- **Impact:** systematic fare evasion, significant estimated economic damage
- Recommendation: "Implement backend system with server-side verification. Migrate to DESFire EV2 with authenticated transactions. Implement blacklisting of anomalous UIDs"

---

## Scenario 7 - Red Team: Datacenter Access with Cloned Badge

**Objective:** gain physical access to the target datacenter during a red team engagement

**Context:** The datacenter has 3 security levels: reception with guard, corridor with NFC badge reader, server room with badge reader + PIN. Target: reach the server room.

**Phase 1 - Badge collection (days 1-3):**
1. OSINT: identify datacenter employees via LinkedIn
2. Physical recon: observe the entrance during shift change hours
3. Day 2: position yourself in the adjacent smoking area. Technicians come out with their badge around their neck
4. Flipper in pocket with NFC → Read active → "drive-by" read when a technician passes within <5cm
5. Result: SAK 0x08, MIFARE Classic 1K → dictionary attack in real-time → partial dump (only sectors with default keys)

**Phase 2 - Completing the dump:**
1. Non-default keys require MFKey32
2. Enter the lobby (accessible without a badge up to reception)
3. Detect Reader on the inner door reader (while the guard is distracted)
4. 3 presentations → nonce capture
5. MFKey32 → keys recovered
6. Return to the technician in the smoking area → second Read → full dump

**Phase 3 - Cloning and access:**
1. Gen4 Magic Card → write dump
2. Test at the corridor door → opened!
3. Second door (server room): badge + PIN → the badge works but the PIN is unknown
4. Observe a technician entering the PIN (shoulder surfing): 4 digits → noted
5. Combine cloned badge + PIN → server room access achieved

**Report:**
- **Critical:** "The datacenter access badge uses MIFARE Classic 1K vulnerable to cloning. The entire cloning process requires less than 60 seconds of physical proximity"
- **High:** "The server room access PIN is a 4-digit code shared among all technicians, not individual"
- Recommendation: "DESFire EV3 badge + individual PIN + centralized logging + camera at reader + anti-tailgating"

---

## Scenario Matrix - Quick Reference

| Scenario | Target | Technique | Complexity | Impact |
|----------|--------|-----------|------------|--------|
| Corporate badge | MIFARE Classic | Dict + MFKey32 + Clone | Medium | Critical |
| Hotel card | MIFARE Classic/UL | Dict + Data modification | Low | High |
| Relay attack | Any NFC | Real-time relay | High | Critical |
| Multi-floor | MIFARE 4K | Bitmask privilege escalation | Medium | Critical |
| Cafeteria/credit | MIFARE Classic | Value tampering | Low | High |
| Public transit | MIFARE Classic | Data manipulation | Low | High |
| Datacenter red team | MIFARE Classic | Drive-by read + MFKey32 | High | Critical |

---

## Cross-Reference - Multi-Vector Scenarios

| Scenario | Related Module | Link | How they connect |
|----------|---------------|------|------------------|
| Corporate badge + RFID | RFID | [05-Scenari-Reali](../RFID/05-Scenari-Reali.md) | Many buildings use NFC for restricted areas + 125 kHz RFID for base access. Test both. |
| Badge + BadUSB | USB/Bad USB | [05-Scenari-Reali](../USB/Bad%20USB/05-Scenari-Reali.md) | After cloning the badge and gaining physical access, drop BadUSB on workstation |
| Badge + Sub-GHz | Sub-GHz | [05-Scenari-Reali](../Sub-GHz/05-Scenari-Reali.md) | NFC access to building + Sub-GHz for garage/perimeter gate |
| Hotel card + IR | Infrared | [05-Scenari-Reali](../Infrared/05-Scenari-Reali.md) | Hotel card for room access + IR to control TV/AC (social engineering) |
| Datacenter + WiFi | WiFi-Marauder | [05-Scenari-Reali](../WiFi-Marauder/05-Scenari-Reali.md) | Physical datacenter access via badge → internal WiFi recon with ESP32 |
| Badge + BLE | Bluetooth | [05-Scenari-Reali](../Bluetooth/05-Scenari-Reali.md) | BLE analysis of NFC readers to find exposed management interfaces |
