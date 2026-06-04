## Penetration Testing Scenarios

### Scenario 1: Cloning an Apartment Building EM4100 Badge to T5577

**Context:** An Italian apartment building with an EM4100 access control system for the main entrance, vehicle gate and bicycle storage room. The client (building administrator) wants to verify if the system is vulnerable to cloning.

**Phase 1 - Reconnaissance (Day 1)**

1. External survey: identify visible readers
   - Main entrance: wall-mounted reader, CAME or BPT type, red/green LED
   - Gate: reader recessed in the pillar
   - Bike room: touch-glass reader
2. Activate `NFC/RFID Detector` and walk near the readers
   - Result: all three emit an LF (125 kHz) field - RFID LF confirmed
3. Observe residents entering - keyfob or card badges?
   - Note: circular blue/black keyfobs (typical cheap Chinese EM4100)

**Phase 2 - Badge Acquisition (Day 1)**

1. Option A (authorized): the client provides a test badge
2. Option B (social engineering): "Excuse me, could you bring your badge closer? I need to test the system for the building administrator"
3. Reading: `RFID 125 kHz > Read` - bring the badge close
4. Result: `EM4100 - ID: 0A 00 12 34 56`
5. Save: `Save > "main_entrance"`

**Phase 3 - Cloning (Day 1)**

1. Open the saved file: `RFID 125 kHz > Saved > main_entrance`
2. Select `Write`
3. Place a blank T5577 keyfob on the Flipper
4. Wait for write confirmation (2-3 seconds)
5. Verify: `Read` the T5577 just written - it must show the same ID `0A 00 12 34 56`

**Phase 4 - Access Testing (Day 2)**

1. Bring the cloned T5577 close to the main entrance reader
2. Expected result: green LED, lock opens
3. Test all three readers - the same badge should work everywhere
4. Document with photos and video (timestamped)

**Phase 5 - Reporting**

```
FINDING: EM4100 badge cloning - Risk HIGH

Description: The apartment building's access control system
uses RFID EM4100 tags at 125 kHz without any encryption
or authentication. It was possible to read the ID of an
authorized badge and clone it to a T5577 tag in less than
10 seconds. The clone works on all three tested readers.

Impact: Any person with an RFID reading device
(cost: <20 EUR) can clone a resident's badge
by getting within 10 cm of the original badge.

Recommendation:
- Short term: raise awareness among residents about
  badge protection (do not leave it in plain sight)
- Medium term: migrate to an NFC 13.56 MHz system with
  encryption (MIFARE DESFire EV2/EV3)
- Long term: evaluate multi-factor system
  (badge + PIN or badge + biometric)
```

---

### Scenario 2: Corporate HID Prox Badge - Facility Code Analysis and Cloning

**Context:** A company with 200 employees uses HID Prox (125 kHz) badges for all access points. The CISO has commissioned a complete physical pentest.

**Phase 1 - Reconnaissance**

1. Observe employee badges:
   - ISO-format card with HID logo and company logo
   - Gray HID keyfobs for some
2. `NFC/RFID Detector` on readers:
   - Main entrance: LF
   - Stairs/elevators: LF
   - Server room: LF + HF (dual reader - possibly migrating)
3. Note: HID iCLASS R10 readers (recognizable by design)

**Phase 2 - Acquisition**

1. Social engineering: visitor badge (often has limited access but same FC)
2. Reading: `RFID 125 kHz > Read`
3. Result: `HID H10301 - FC:42 CN:8001`
4. Save and analyze:
   - Facility Code 42 - probably the same for all badges in the company
   - Card Number 8001 - visitor cards are often numbered high (>8000)

**Phase 3 - Facility Code Analysis**

If you have access to multiple badges (e.g. badge found in trash, at the photocopier, etc.):

```
Badge 1 (visitor):     FC:42 CN:8001
Badge 2 (employee):    FC:42 CN:0156
Badge 3 (found):       FC:42 CN:0312

Analysis:
- FC confirmed: 42 for the entire company
- Employee CN: low range (1-500?)
- Visitor CN: high range (8000+)
- Probably sequentially assigned CN
```

**Phase 4 - Targeted Cloning**

1. Create a badge with a low Card Number (probable employee):
   - `Add Manually > HID H10301 > FC:42 CN:1`
   - Write to T5577
2. Test on the main entrance
3. If it does not work, increment: CN:2, CN:3, ...
4. Alternative: use the `RFID Fuzzer` with FC:42 and CN:1-500

**Phase 5 - Escalation**

1. Once inside, map the internal access points
2. The server room has a dual reader (LF+HF):
   - The HID Prox 125 kHz badge might work on the LF side
   - If it does not work, the HF side requires an NFC badge - different engagement
3. Document every door accessible with the cloned badge

> **Personal note:** The Facility Code is the keystone in an HID pentest. Once you know it, you have half the work done. In an engagement for a multinational I discovered they used different FCs for different buildings (FC:10 for headquarters, FC:20 for the warehouse, FC:30 for the lab). This is a good sign - it means there is at least some segmentation. But within each building, all badges had the same FC and sequential Card Numbers starting from 1. The CEO's first badge was probably CN:1. In the absence of encryption, the Facility Code is the only form of "security" - and it is easily discoverable.

---

### Scenario 3: Fuzzing an RFID Reader to Discover Vulnerabilities

**Context:** Security testing of a standalone RFID reader (not connected to a central controller) installed on an internal door.

**Objective:** Determine if the reader has implementation vulnerabilities.

**Phase 1 - Identification**

1. `NFC/RFID Detector`: active LF field - confirmed 125 kHz
2. Reading an authorized badge: `EM4100 - ID: 05 00 AA BB CC`
3. Note the Version Number: `05` - it might be significant

**Phase 2 - Baseline Testing**

1. Cloned badge: works - the system accepts the original ID
2. Badge with random ID: does not work - the system has a database
3. So far everything is normal

**Phase 3 - Intelligent Fuzzing**

Test 1: **Version Number Manipulation**
```
Original ID:    05:00:AA:BB:CC -> OPENS
Modified ID:    05:00:AA:BB:CD -> DOES NOT OPEN
Modified ID:    05:00:AA:BB:CB -> DOES NOT OPEN
Modified ID:    05:01:AA:BB:CC -> OPENS (!!!)
```

**Discovery:** the reader ignores the second byte! It only checks the Version Number (byte 0) and the last 3 bytes.

Test 2: **Brute force on the last 3 bytes with fixed Version Number**
- With `RFID Fuzzer`: protocol EM4100, fixed bytes 05:00, fuzzing on the remaining 3 bytes
- 2^24 = ~16 million combinations - too many for complete brute force
- But: 5 minutes of fuzzing discovers 3 valid IDs beyond the original

Test 3: **Anomalous behavior**
```
Rapid sending of 100 different IDs in 30 seconds:
- The reader stops responding for 10 seconds (temporary lockout)
- After lockout, it resumes normally
- No alarm generated
- No logging (the reader is standalone)
```

**Phase 4 - Reporting**

```
FINDING 1: Partial ID validation - Risk HIGH
The reader ignores the second byte of the EM4100 ID, reducing
the search space from 2^40 to 2^32.

FINDING 2: No effective rate limiting - Risk MEDIUM
The reader locks out briefly but resumes without
permanent countermeasures. Brute force is feasible.

FINDING 3: No logging - Risk HIGH
The standalone reader generates no logs. Unauthorized
access attempts are not recorded.

FINDING 4: No alarm - Risk MEDIUM
No notification after multiple failed attempts.
An attacker can operate without being detected.
```

---

### Scenario 4: Detecting Hidden Readers with the Detector

**Context:** Physical security audit of an office floor. The client wants a complete map of all electronic access points.

**Procedure**

1. Prepare a floor plan (A3 format, printed)
2. Activate `NFC/RFID Detector`
3. Walk systematically along every corridor, wall, door
4. At each detection, mark on the floor plan:
   - Reader position
   - Field type (LF / HF / dual)
   - Intensity (low/medium/high)
   - Visible or hidden

**Typical results:**

```
Floor 3 - RFID Reader Mapping

Door     | Type  | Field | Visible | Notes
---------|-------|-------|---------|-----
P01      | Entr. | LF    | Yes     | HID iCLASS R10
P02      | Off.  | LF    | Yes     | CAME
P03      | DC    | LF+HF | Yes    | HID multiCLASS
P04      | Arch. | LF    | No      | Under plaster!
P05      | WC    | -     | -       | No reader
P06      | Strs  | LF    | Yes     | BPT
P07      | Elev. | HF    | Yes     | NFC only
P08      | Stor. | LF    | No      | Behind panel
```

**Critical discoveries:**
- P04 (Archive): reader hidden under plaster - no one knew about it. Probably a previous installation never removed but still functional. The power cable was still active. This is a potential bypass: if the old reader is connected to the lock, an EM4100 badge from the previous system could still open it.
- P08 (Storage): reader hidden behind a decorative panel - possible discreet installation attempt, but also a potential unmonitored vulnerability point.

> **Personal note:** Mapping with the Detector is a phase that many pentesters skip, and in my opinion it is a serious mistake. In one case I found an active RFID reader connected to the server room door that had been "decommissioned" by the IT manager - but in reality it was still powered and the electric lock still responded to the old EM4100 badges. The IT manager was convinced that the new NFC system was the only active one. That ghost reader was the most severe vulnerability in the entire infrastructure.

---


---

### Scenario 5: Corporate Multi-Level Parking Garage Assessment

**Context:** An underground corporate parking garage with an automatic barrier and RFID 125 kHz reader. The system uses EM4100 badges for all employees and temporary visitor badges. The CISO wants to verify the system's robustness.

**Phase 1 - Reconnaissance**

1. Detector on the barrier reader: LF field confirmed
2. Observe employees: keyfobs attached to car keychains
3. Note: the reader is a generic brandless Chinese model

**Phase 2 - Visitor Badge Acquisition**

1. Request a visitor badge at reception (legitimate scenario for the engagement)
2. Reading: `EM4100 - ID: 0A 00 FF 01 00`
3. The Version Number `0A` might be the "visitor batch"

**Phase 3 - System Analysis**

1. Visitor badge at barrier: opens (visitor access granted)
2. Read an employee badge (with authorization): `EM4100 - ID: 05 00 12 34 56`
3. Different Version Number: `05` for employees, `0A` for visitors
4. The system probably uses the Version Number to distinguish access levels

**Phase 4 - Privilege Escalation Testing**

1. Create a badge: Version `05` + random ID: `Add Manually > EM4100 > 05:00:00:00:01`
2. Write to T5577
3. Test at the barrier: DOES NOT open -> the system has a database
4. Targeted fuzzing: `05:00:12:34:55`, `05:00:12:34:57` (close to the known employee ID)
5. `05:00:12:34:57` -> OPENS! Sequential Card Numbers confirmed

**Phase 5 - Floor Access**

1. After the barrier, each floor has a separate reader for the entry door
2. The cloned badge also opens the employee's floor door -> no segmentation
3. Visitor badge (`0A:...`) does not open the floors -> at least this separation works

**Report:**
```
FINDING 1: Sequential Card Numbers - Risk HIGH
Employee badges use EM4100 IDs with sequential numbering.
Knowing a single ID, it is possible to enumerate the others
with the RFID Fuzzer. Estimated time: <5 minutes for +-100 IDs.

FINDING 2: No per-floor segmentation - Risk MEDIUM
An employee badge opens all floors, regardless of
assignment. There is no least-privilege enforcement.

FINDING 3: Clonable EM4100 - Risk HIGH
All badges are EM4100 without encryption.
Cloning takes <10 seconds.
```

---

### Scenario 6: Gym/Sports Center - Turnstile Bypass

**Context:** A gym with an entry turnstile controlled by RFID 125 kHz badges. The membership is associated with the badge. The owner wants to verify if duplicate badges can be used for unauthorized access.

**Phase 1 - System Analysis**

1. Detector on the turnstile: LF field
2. Reading a member badge: `EM4100 - ID: 01 00 AB CD EF`
3. The system is a standalone controller with LCD display

**Phase 2 - Cloning Test**

1. Clone to T5577 -> test at turnstile -> opens
2. The LCD shows the membership holder's name -> the system associates the ID with the database
3. Two people with the same badge: both can enter -> no anti-passback control

**Phase 3 - Anti-passback Test**

1. Entry with original badge -> OK
2. Immediate entry with cloned badge -> OK (no anti-passback!)
3. The system allows multiple entries with the same ID without cooldown

**Phase 4 - Economic Impact**

1. A member can clone their badge and give it to a friend
2. Both can use the gym with a single membership
3. Out of 500 members, even 5% abuse = 25 lost memberships

**Report:**
```
FINDING: Access system without anti-passback and with
clonable badges (EM4100). A member can duplicate the badge
and share it. Estimated potential revenue loss: 5-10%
of membership income.

Recommendation: Implement temporal anti-passback
(minimum 30 minutes between successive entries with
the same ID) and migrate to badges with encryption.
```

> **Personal note:** I have done this test for 3 different gyms. All three used EM4100 without anti-passback. In one, the owner had no idea the badges were clonable. In another, the problem was known but they had not fixed it because "it costs too much to change the system." The third decided to migrate to NFC after my report. The pentest ROI pays for itself in non-shared memberships.

---

### Scenario 7: Red Team - Building Entry via Cloned Badge and Tailgating

**Context:** Red team engagement on an office building with 4 tenant companies. HID Prox 125 kHz access control system for the main entrance. Target: reach Company X's office on the 2nd floor.

**Phase 1 - External Reconnaissance (Day 1-2)**

1. Entrance observation: employees use HID badges (cards with company logo + HID)
2. Peak hours: 8:30-9:30 entry, 12:30-13:30 lunch break, 17:30-18:30 exit
3. Note: the door has a slow door closer (~5 seconds to close)

**Phase 2 - Acquisition (Day 3)**

1. Smoking area: an employee has their badge around their neck on a lanyard
2. Approach with pretext: "Excuse me, do you know where Company Y's meeting room is?"
3. During the conversation, Flipper in pocket -> `RFID Read` -> no signal at that distance
4. Plan B: wait for lunch break, an employee leaves their jacket on the chair at the bar
5. The badge is in the jacket pocket -> Flipper in contact with the pocket -> `HID H10301 FC:23 CN:445`
6. Total contact time: 2 seconds

**Phase 3 - Cloning and Access (Day 3, afternoon)**

1. `Add Manually > HID H10301 > FC:23 CN:445` -> write to T5577 card
2. Test at the main entrance -> green LED -> access granted!
3. Go up to the 2nd floor -> Company X's door -> the badge works here too
4. Inside: no further controls until the server room (badge + PIN)

**Phase 4 - Enumeration (Day 4)**

1. With FC:23 confirmed, try badges with different CNs to verify segmentation
2. CN:1 -> access granted (probably admin/reception)
3. CN:100 -> access granted (employee)
4. CN:500 -> access granted (visitor range?)
5. All 4 tenant companies in the building share the SAME Facility Code -> no tenant segmentation!

**Report:**
```
FINDING CRITICAL: All building tenants share the same
HID Facility Code (FC:23). An employee of any company
can access the offices of all others.

FINDING HIGH: HID Prox badge clonable in <10 seconds.
Physical access to the building requires only temporary
proximity to a valid badge.

FINDING MEDIUM: The slow door closer (5s) allows easy
tailgating during peak hours.
```

---

## Scenario Matrix - Quick Reference

| Scenario | Target | Protocol | Technique | Complexity | Impact |
|----------|--------|-----------|---------|-------------|---------|
| Apartment building | EM4100 | 125 kHz LF | Direct clone | Low | High |
| Corporate HID | HID H10301 | 125 kHz LF | FC analysis + clone | Medium | Critical |
| Reader fuzzing | EM4100/HID | 125 kHz LF | Fuzzer + behavior | Medium | High |
| Hidden readers | Various | LF/HF | Detector mapping | Low | Variable |
| Parking garage | EM4100 | 125 kHz LF | Sequential enumeration | Medium | High |
| Gym | EM4100 | 125 kHz LF | Clone + anti-passback test | Low | Medium |
| Red team building | HID H10301 | 125 kHz LF | Social eng + clone | High | Critical |

---

## Cross-Reference - Multi-Vector Scenarios

| Scenario | Related Module | Link | How They Connect |
|----------|-----------------|------|-------------------|
| RFID + NFC badge | NFC | [05-Real-World-Scenarios](../NFC/05-Real-World-Scenarios.md) | Dual-tech buildings: RFID for basic entry, NFC for restricted areas |
| Badge + Sub-GHz | Sub-GHz | [05-Real-World-Scenarios](../Sub-GHz/05-Real-World-Scenarios.md) | Clone RFID badge for building + Sub-GHz replay for perimeter gate |
| Badge + iButton | iButton | [05-Real-World-Scenarios](../iButton/05-Real-World-Scenarios.md) | Apartment buildings: RFID for entrance + iButton for intercom/elevator |
| Red team + BadUSB | USB/Bad USB | [05-Real-World-Scenarios](../USB/Bad%20USB/05-Real-World-Scenarios.md) | After physical access with cloned badge -> deploy BadUSB payload |
| Red team + WiFi | WiFi-Marauder | [05-Real-World-Scenarios](../WiFi-Marauder/05-Real-World-Scenarios.md) | Physical access -> evil portal WiFi for internal credential harvest |
| Parking + Debug | GPIO/Debug | [04-Real-World-Scenarios](../GPIO/Debug/04-Real-World-Scenarios.md) | After cloning parking badge, extract firmware from reader for analysis |
