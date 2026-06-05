## 8. Pentest Scenarios

### 8.1 MouseJacker in the office

**Context:** security audit of a company with 50+ workstations, most with Logitech wireless mice.

**Phase 1 -- Reconnaissance (day 1):**

- Walk through the office with Flipper Zero + NRF24 PA+LNA in the backpack
- Scanner running continuously
- Result: 34 wireless mice identified, 28 Logitech Unifying, 4 Microsoft, 2 unknown
- 22 of the 28 Logitech units found to have non-updated firmware (vulnerable)

**Phase 2 -- Proof of Concept (day 2):**

- Selected target: purchasing manager's workstation (M185 mouse, old firmware)
- Positioning: adjacent meeting room (approximately 8 meters through a wall)
- Payload: open notepad + warning message
- Execution: successful on the first attempt, total time 3 seconds
- Documentation: screenshot, timestamp, device pipe address

**Phase 3 -- Demonstrative escalation (day 2):**

- Same target, more advanced payload: PowerShell that downloads and executes a monitoring agent
- Execution: successful, agent installed in 5 seconds
- Full access to the workstation via C2 server

**Phase 4 -- Report:**

- Vulnerability classified as CRITICAL (CVSS 9.0+)
- Remediation: update dongle firmware + replace non-updatable peripherals
- Recommendation: migrate to Bluetooth or wired peripherals for sensitive workstations
- Recommended remediation timeline: immediate for critical workstations, 30 days for all

### 8.2 IoT sensor sniffing

**Context:** audit of an environmental monitoring system based on wireless sensors.

**Phase 1 -- Identification:**

- Channel Scan reveals 8 active devices in the 2.4 GHz band
- 5 are temperature/humidity sensors (transmitting every 30 seconds)
- 2 are wireless mice (intermittent traffic)
- 1 is an LED light remote control

**Phase 2 -- Capture and analysis:**

- Sniffer configured on the sensors' channel
- Capture of 100+ packets in 30 minutes
- Payload analysis: data in the clear, no encryption, no authentication
- Decoded format: [Sensor_ID(2B)] [Temperature(2B, BCD)] [Humidity(1B)] [Battery(1B)] [CRC(1B)]

**Phase 3 -- Proof of Concept injection:**

- Construction of a fake packet with altered temperature
- Injection into the monitoring system
- The system accepts the fake data without validation
- Demonstration that an attacker can falsify sensor readings

**Impact:** an attacker could alter sensor readings in a pharmaceutical warehouse, simulating correct temperatures while the cold chain is broken.

### 8.3 Jamming -- controlled demo

**Context:** resilience testing of a wireless alarm system in a controlled environment.

**Setup:**

- Alarm system with wireless sensors at 2.4 GHz
- Test in a shielded laboratory (Faraday cage)
- Written authorization from the client

**Test 1 -- Single channel jamming:**

- Identification of the channel used by sensors: channel 52
- Activation of the jammer on channel 52
- Result: sensors can no longer communicate with the control unit
- The control unit does NOT detect the jamming (no tamper alarm)
- The sensor continues to attempt transmission but packets are lost
- Time to communication loss: 3 seconds

**Test 2 -- Recovery after jamming:**

- Deactivation of the jammer
- Sensors resume communication in 2-5 seconds
- The control unit did not log the interruption

**Conclusion:** the alarm system is vulnerable to RF jamming without any detection. Recommendation: implement anti-jamming detection (monitoring for missing heartbeats from sensors).

### 8.4 Wireless peripheral audit -- checklist

Complete checklist for auditing wireless peripherals in an organization:

**Inventory:**

- [ ] Census of all wireless peripherals (mice, keyboards, presenters)
- [ ] Identification of make, model, and firmware of each device
- [ ] Mapping of associated USB dongles
- [ ] Identification of workstations with sensitive data

**Technical tests:**

- [ ] Channel Scan of the entire environment
- [ ] Identification of all NRF24-compatible devices
- [ ] Encryption verification for each identified device
- [ ] MouseJacker test on a representative sample
- [ ] Passive sniffing test (verify data in the clear)
- [ ] Injection test on vulnerable devices

**Risk assessment:**

- [ ] Classification of devices by vulnerability level
- [ ] Correlation with the value of assets on the workstation
- [ ] Estimation of the impact of a successful attack
- [ ] Identification of the highest-risk workstations

**Remediation:**

- [ ] Firmware update where possible
- [ ] Replacement of non-updatable devices
- [ ] Migration to Bluetooth for critical workstations
- [ ] Corporate policy on the use of wireless peripherals
- [ ] User training on the risks of wireless peripherals

> Personal note: the checklist above is the one I actually use in my audits. I've refined it over the course of a dozen assessments. The point that companies always underestimate is the inventory: nobody knows how many wireless mice are in the office. The answer is always "many more than we thought". At a 200-employee company I found 47 non-inventoried wireless mice, 31 of which were vulnerable to MouseJacker. The IT manager was convinced there were "ten at most".

---

## Cross-Reference - Multi-Vector Scenarios

| Scenario | Related Module | Link | How they connect |
|----------|---------------|------|------------------|
| MouseJacker vs BadUSB | USB/Bad USB | [05-Scenari-Reali](../../USB/Bad%20USB/05-Scenari-Reali.md) | MouseJacker is the wireless alternative to wired BadUSB -- same payload, different delivery |
| NRF24 + WiFi | GPIO/ESP32 | [04-Scenari-Reali](../ESP32/04-Scenari-Reali.md) | 2.4 GHz scan for peripherals + WiFi scan for network: complete wireless mapping |
| Peripherals + RFID | RFID | [05-Scenari-Reali](../../RFID/05-Scenari-Reali.md) | Physical access via RFID badge -> MouseJacker on internal workstations |
| NRF24 + BLE | Bluetooth | [05-Scenari-Reali](../../Bluetooth/05-Scenari-Reali.md) | Both on 2.4 GHz: NRF24 for peripherals, BLE for IoT/wearables |
| NRF24 + Sub-GHz | Sub-GHz | [05-Scenari-Reali](../../Sub-GHz/05-Scenari-Reali.md) | Complete RF assessment: Sub-GHz (sensors, gates) + 2.4 GHz (peripherals) |
