# Real-World Penetration Testing Scenarios - Sub-GHz

Detailed operational scenarios for using the Sub-GHz module in physical penetration testing, red teaming, and security assessment contexts. Each scenario is based on real experiences and includes the complete procedure, expected findings, and recommendations.

---

## Scenario 1 - Physical Pentest: Building Gate Bypass

**Objective:** demonstrate that the target building's RF gate is vulnerable

**Phase 1 - Reconnaissance:**
1. From the parking lot, activate the Frequency Analyzer
2. Wait for an employee to use the gate remote
3. Note the frequency (probably 433.92 or 868.35 MHz)

**Phase 2 - Capture:**
1. Position yourself within 10 meters of the gate
2. Open Sub-GHz -> Read on the identified frequency
3. Wait for an employee to press the remote
4. If it decodes (e.g., "Nice FLO 12-bit"): fixed code -> save and you are done
5. If it decodes as rolling code: note the protocol for the report
6. If it does not decode: use Read RAW for raw capture

**Phase 3 - Testing:**
1. With fixed code: Sub-GHz -> Saved -> Send -> the gate opens
2. With rolling code: document the capture and analyze with Rolling Flaws
3. In both cases: document with photos, timestamps, and frequency

**Phase 4 - Report:**
- Finding: "The gate access system uses [X] protocol with fixed/rolling code on frequency [Y] MHz"
- Impact: "An attacker with a cheap RF receiver can capture and replay the access signal"
- Recommendation: "Migrate to a rolling code system with AES encryption or use an NFC/RFID-based access system with encryption"

---

## Scenario 2 - Wireless Alarm System Analysis

**Objective:** assess the security of an alarm system that uses wireless sensors

**Procedure:**
1. Radio Scanner to identify sensor frequencies
2. Sub-GHz -> Read to decode sensor signals (door open, motion, etc.)
3. Analyze whether sensors use fixed code or rolling
4. If fixed code: replay attack to generate false alarms or, worse, send "all clear" signals to mask an intrusion
5. Spectrum Analyzer to assess the possibility of jamming on the sensor frequency

**Implications:**
- Many cheap alarms use fixed code sensors on 433 MHz
- An attacker can jam the frequency (the system does not receive alarms)
- Alternatively, they can replay the "zone OK" signal to deactivate a specific sensor
- Better systems have anti-jamming (they detect the absence of sensor heartbeat) and rolling code

---

## Scenario 3 - OSINT with TPMS and Pagers

**Objective:** gather passive intelligence on a target

**TPMS:**
1. TPMS Reader near the target parking lot
2. Collect TPMS sensor IDs for 24 hours
3. Correlate IDs with observed vehicles
4. Monitor entries/exits to build a schedule profile

**Pager:**
1. POCSAG Decoder on the local frequency
2. Monitor messages to identify patterns, names, operational information
3. This reveals the organization's internal communications transmitted in cleartext

---

## Scenario 4 - Red Team: Corporate Parking Barrier Bypass

**Objective:** gain physical access to a corporate target's underground parking lot during a red team engagement

**Context:** The target building has an automatic barrier at the parking entrance. Employees use RF remotes to access it. The objective is to enter with a vehicle without valid credentials.

**Phase 1 - Passive reconnaissance (day 1):**
1. Park in a public area with a view of the barrier
2. Open Frequency Analyzer on the Flipper
3. Observe peak hours (8:00-9:30, 17:30-19:00)
4. Note the frequency: in this case 868.35 MHz -> probably FAAC or industrial system
5. Note the timing: how long the barrier stays open after activation (~8 seconds)

**Phase 2 - Capture (day 2, early morning):**
1. Position yourself in the adjacent public parking lot, ~5 meters from the barrier
2. Sub-GHz -> Read on 868.35 MHz, FM modulation (FSK)
3. First employee arrives at 7:45: the Flipper decodes "FAAC SLH" -> rolling code
4. Second employee: same decode, counter incremented by 1
5. Conclusion: FAAC rolling code system -> direct replay not feasible

**Phase 3 - Alternative approach:**
1. You observe that the barrier also has an RFID badge reader on the side -> pivot to RFID analysis
2. Read RAW captures the rolling signal anyway for documentation
3. Rolling Flaws: analysis of the two captured codes -> wide resync window (>256 codes)
4. Document the resync window as a secondary finding

**Phase 4 - Assisted tailgating:**
1. During peak hours, a team member follows an authorized car
2. The barrier stays open for 8 seconds - sufficient for a second vehicle
3. Access obtained - document as a physical security finding

**Report finding:**
- **Primary:** "The barrier system uses FAAC SLH rolling code on 868.35 MHz. The rolling code implementation is correct but the resync window accepts codes with a gap >256, potentially vulnerable to resync attack"
- **Secondary:** "The barrier open time (8s) allows vehicular tailgating. Recommendation: reduce to 4-5 seconds and install anti-tailgating inductive loop sensors"
- **CVSS:** 5.3 (Physical Access, Low Complexity)

---

## Scenario 5 - IoT Assessment: Wireless Sensors in an Industrial Environment

**Objective:** assess the security of wireless sensors installed in a manufacturing plant

**Context:** A manufacturing company uses wireless sensors on 433/868 MHz to monitor temperature, humidity, and machine status. The assessment must verify whether an attacker can manipulate sensor data.

**Phase 1 - RF mapping of the plant:**
1. Radio Scanner: full scan 300-928 MHz while walking through the plant
2. Identified 23 active signals:
   - 15 on 433.92 MHz (temperature/humidity sensors)
   - 5 on 868.35 MHz (machine status sensors)
   - 3 on 315 MHz (loading dock gate remotes)
3. Spectrum Analyzer: no evidence of frequency hopping -> fixed channel

**Phase 2 - Sensor decoding:**
1. Sub-GHz -> Read on 433.92 MHz: Weather Station decoder identifies Oregon Scientific v3.0 sensors
2. Each sensor transmits every 45 seconds: ID, temperature, humidity, battery
3. No authentication: cleartext protocol, fixed code for each sensor
4. Sub-GHz -> Read on 868.35 MHz: protocol not recognized -> Read RAW

**Phase 3 - Proof of Concept:**
1. Capture a temperature sensor signal with Read
2. Modify the temperature value in the .sub file (from 22C to 85C)
3. Replay the modified signal -> the centralized system shows anomalous temperature
4. If the system has alarm thresholds: the temperature alarm triggers -> potential production line shutdown

**Phase 4 - Loading dock gate analysis:**
1. Sub-GHz -> Read on 315 MHz: "Linear 10-bit" -> fixed code
2. Bruteforcer: 1024 combinations in ~5 minutes
3. Found the valid code on attempt #387
4. Replay: the gate opens -> physical access to the loading dock area

**Report finding:**
- **Critical:** "The environmental sensors (Oregon Scientific v3.0, 433.92 MHz) transmit in cleartext without authentication. An attacker can inject false data causing false alarms or masking real dangerous conditions"
- **High:** "The loading dock gates use Linear 10-bit remotes (1024 combinations). The code can be discovered via bruteforce in less than 5 minutes"
- **Sensor recommendation:** "Migrate to sensors with an authenticated protocol (LoRaWAN with AES-128 encryption) or hardwire critical sensors"
- **Gate recommendation:** "Replace with a rolling code system or RFID access control"

---

## Scenario 6 - Residential Pentest: Complete Home Automation Analysis

**Objective:** complete security assessment of a smart home with RF automation

**Context:** The client has a home with an automatic gate, Somfy motorized roller shutters, automatic garage, wireless alarm, and weather station. They want to know how vulnerable everything is.

**Phase 1 - RF Inventory:**
1. Radio Scanner from inside the home: complete mapping of active frequencies
2. Results:
   - 433.92 MHz: gate (Nice FLOR), alarm sensors (5 zones), weather station
   - 433.42 MHz: Somfy RTS roller shutters
   - 868.35 MHz: garage (FAAC SLH), 2 additional alarm sensors
3. Protocols Visualizer: structural analysis of captured signals

**Phase 2 - Gate test (Nice FLOR):**
1. Sub-GHz -> Read: "Nice FLOR" -> KeeLoq rolling code
2. Rolling Flaws: analysis of 3 consecutive codes -> counter with fixed increment of 1
3. Resync window: the receiver accepts codes with a gap up to ~500
4. Finding: rolling code implemented correctly, but wide resync window
5. RollJam attempt (with authorization): jammer on 433.92 + capture on adjacent frequency -> not practical with the Flipper alone (requires a dedicated jammer)

**Phase 3 - Somfy RTS roller shutter test:**
1. Sub-GHz -> Read on 433.42 MHz: "Somfy RTS" decoded
2. Somfy uses a proprietary 56-bit rolling code
3. The Somfy protocol is known to have a vulnerability: the "PROG" command allows pairing new remotes
4. Capture a normal command -> structural analysis
5. Finding: if an attacker manages to send a PROG command (capturable with Read RAW), they can pair a new remote and control all the roller shutters

**Phase 4 - Alarm test:**
1. Sub-GHz -> Read: 433 MHz sensors decoded as proprietary fixed code protocol
2. Capture the door sensor "zone OK" signal -> replay -> the control panel accepts the signal
3. Capture the "alarm" signal -> replay -> false alarm generated
4. Jamming test: Spectrum Analyzer confirms that a jammer on 433 MHz would prevent reception of sensor signals
5. The control panel does NOT detect the absence of heartbeat -> vulnerable to silent jamming

**Overall report:**
- Gate: medium risk (rolling code present but wide window)
- Roller shutters: high risk (known PROG vulnerability in Somfy RTS)
- Alarm: critical risk (fixed code, no anti-jamming, no heartbeat monitoring)
- Weather station: informational risk (cleartext data, no security impact)
- Priority recommendation: replace the alarm with a wired system or wireless with rolling code + anti-jamming + heartbeat monitoring

---

## Scenario 7 - Red Team: Multi-Tenant Building Access

**Objective:** gain physical access to an office in a building shared by multiple companies

**Context:** The building has a shared vehicle gate (all tenants use the same system), a pedestrian entrance with intercom, and each floor has its own lock. The target is on the 3rd floor.

**Phase 1 - RF Reconnaissance (days 1-2):**
1. Frequency Analyzer from the sidewalk: 433.92 MHz active frequently (every 5-10 minutes during business hours)
2. Sub-GHz -> Read: "Came 12-bit" -> fixed code!
3. Capture 3 different signals from 3 employees of different tenants -> they all have the same base code with minimal variations (the system uses 12-bit codes assigned sequentially)

**Phase 2 - Code analysis:**
1. Tenant A code: 0xA3B
2. Tenant B code: 0xA3C  
3. Tenant C code: 0xA3E
4. Obvious pattern: codes assigned sequentially -> targeted bruteforce on range 0xA30-0xA4F (32 codes) finds all valid codes in seconds

**Phase 3 - Access:**
1. Replay the captured code -> vehicle gate opens
2. Access to the lobby -> pedestrian door with electric latch (activated by the same 433 MHz signal!)
3. Elevator: free access to all floors -> reached the 3rd floor
4. The target office door has an RFID badge reader -> pivot to NFC/RFID analysis

**Key finding:**
- "The entire building perimeter access system (vehicle gate + pedestrian entrance) relies on Came 12-bit fixed code remotes. An attacker with a 10-euro RF receiver can capture and replicate any access code in less than 5 seconds"
- "Codes are assigned sequentially, allowing anyone who knows one code to enumerate the others via bruteforce"
- Impact: physical access to the entire building for any attacker with minimal RF expertise

---

## Scenario 8 - Incident Response: Suspected Remote Cloning

**Objective:** investigate suspected unauthorized access via cloned remote

**Context:** A company reports that the parking gate opens at night without any employee present. Security cameras show an unidentified vehicle entering. The company suspects remote cloning.

**Phase 1 - System analysis:**
1. Identification: Nice FLO 12-bit system on 433.92 MHz -> fixed code
2. Confirmation: the system is vulnerable to replay attack
3. Sub-GHz -> Read: capture the company remote's signal -> immediate decode

**Phase 2 - Attack simulation:**
1. From 10 meters away, Read captures the code in 1 press
2. Replay: the gate opens
3. Conclusion: an attacker could have captured the code at any time

**Phase 3 - Incident response recommendations:**
1. Immediately replace all remotes with a rolling code system (Nice FLOR/Smilo)
2. Reprogram the gate receiver
3. Invalidate all old codes
4. Install an additional camera with license plate reading
5. Consider an additional physical barrier (bollards)
6. Access logging: if the system supports it, enable logging of every opening with timestamp

**IR Report:**
- "The unauthorized access was made possible by the use of a fixed code system (Nice FLO 12-bit) that allows instant remote cloning via passive RF capture"
- "The attacker likely captured the signal from an employee during business hours and replayed it at night"
- Estimated attack timeline and mitigation recommendations

---

## Scenario Matrix - Quick Reference

| Scenario | Target | Primary Technique | Complexity | Impact |
|----------|--------|-------------------|------------|--------|
| Gate bypass | RF gate | Fixed code replay | Low | High |
| Wireless alarm | Alarm system | Replay + Jamming | Medium | Critical |
| OSINT TPMS/Pager | Vehicles/Communications | Passive reception | Low | Medium |
| Corporate barrier | Corporate parking | Rolling code analysis | Medium-High | High |
| Industrial IoT | Sensors + gates | Replay + Bruteforce | Medium | Critical |
| Residential home automation | Smart home | Multi-protocol | High | High |
| Multi-tenant | Shared building | Replay + Enumeration | Low | Critical |
| Incident Response | Post-incident | RF forensic analysis | Medium | N/A |

---

## Cross-Reference - Multi-Vector Scenarios

Many real engagements combine multiple modules. Here are links to related scenarios in other modules:

| Scenario | Related Module | Link | How They Connect |
|----------|---------------|------|------------------|
| Gate bypass + building access | RFID | [05-Scenari-Reali](../RFID/05-Scenari-Reali.md) | After opening the gate via Sub-GHz, use RFID to clone a badge and enter the building |
| Wireless alarm + WiFi | WiFi-Marauder | [05-Scenari-Reali](../WiFi-Marauder/05-Scenari-Reali.md) | While jamming the RF alarm, use ESP32 to also disable any WiFi notifications |
| Industrial IoT + Debug | GPIO/Debug | [04-Scenari-Reali](../GPIO/Debug/04-Scenari-Reali.md) | After capturing RF signals from the IoT system, extract firmware via SWD for offline analysis |
| Home automation + IR | Infrared | [05-Scenari-Reali](../Infrared/05-Scenari-Reali.md) | Home automation systems often combine RF (shutters, sensors) + IR (TV, AC, lights) |
| Multi-tenant + NFC | NFC | [05-Scenari-Reali](../NFC/05-Scenari-Reali.md) | Multi-tenant buildings often use Sub-GHz for the garage + NFC for floor access |
| Barrier + BadUSB | USB/Bad USB | [05-Scenari-Reali](../USB/Bad%20USB/05-Scenari-Reali.md) | Physical access via Sub-GHz -> drop BadUSB on a workstation in the parking lot |
