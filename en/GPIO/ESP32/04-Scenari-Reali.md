## 8. Real-World Pentest Scenarios

### 8.1 Scenario: Urban Wardriving

**Objective:** Map the wireless attack surface of a corporate campus to assess signal leakage and exposed networks.

**Required kit:**
- Flipper Zero with custom firmware
- ESP32-WROOM with Wardriver firmware
- NEO-6M/7M GPS module
- 10000mAh powerbank
- External 2.4GHz antenna (optional, for greater sensitivity)

**Operational procedure:**

1. **Preparation (30 minutes)**
   - Flash Wardriver firmware onto the ESP32.
   - Connect GPS to the ESP32 (UART2).
   - Connect ESP32 to the Flipper via GPIO.
   - Power with powerbank.
   - Verify GPS fix outdoors (wait 3-5 minutes).
   - Quick test: verify that networks are being detected.

2. **Perimeter wardriving (1-2 hours)**
   - Walk or drive around the building perimeter.
   - Maintain constant speed for uniform coverage.
   - Cover all sides of the building.
   - Note points of interest (entrances, parking lots, public areas).

3. **Internal wardriving (if authorized access, 1-2 hours)**
   - Walk through all floors and accessible areas.
   - Pay particular attention to: meeting rooms, cafeterias, reception, hallways.
   - Identify rogue APs (personal devices creating hotspots).

4. **Data analysis (2-4 hours)**
   - Export the CSV from the microSD.
   - Upload to WiGLE (optional) for cross-reference.
   - Analysis with GIS tools (QGIS, Google Earth):
     - Import geolocated data.
     - Create network map with coverage.
     - Identify signal leakage: corporate networks visible from outside.
   - Categorize found networks:
     - Corporate (with company name)
     - Guest
     - Rogue (unauthorized)
     - Neighbors (adjacent buildings)

5. **Report**
   - Network map with building overlay.
   - Signal leakage: maximum distance at which the corporate network is detectable.
   - Identified rogue APs with approximate location.
   - Networks with weak or absent encryption.
   - Recommendations: reduce TX power, disable SSID broadcast for sensitive networks, BYOD policy for rogue APs.

### 8.2 Scenario: Evil Portal Credential Harvesting

**Objective:** Test employee awareness regarding WiFi phishing by capturing credentials entered in fake captive portals.

**Required kit:**
- Flipper Zero
- ESP32-WROOM or ESP32-S2 with Evil Portal firmware
- Pre-prepared portal HTML files
- Powerbank

**Operational procedure:**

1. **Preparation (1-2 hours)**
   - Target information gathering:
     - Name and graphics of the actual guest WiFi portal (if it exists).
     - Corporate and guest network names.
     - Corporate visual style (logo, colors, fonts).
   - HTML page creation:
     - Faithfully replicate the guest WiFi portal or VPN login.
     - Include corporate logo, corporate colors, legal disclaimer.
     - Form with fields: corporate email + password.
     - Success page: "Connecting..." to avoid raising suspicion.
   - Test the portal in a controlled environment.
   - Load HTML files onto the Flipper's microSD.

2. **Deployment (15 minutes)**
   - Connect the ESP32 to the Flipper.
   - Configure Evil Portal:
     - SSID: credible name (e.g., "CompanyName-Guest", "CompanyName-WiFi-Upgrade").
     - Select the prepared HTML page.
     - Start the portal.
   - Position the device in a high-traffic area:
     - Cafeteria, break area, waiting room.
     - Conceal in a discreet container (bag, box).
     - Ensure continuous power (large powerbank).

3. **Data collection (2-8 hours)**
   - Periodically monitor from the Flipper:
     - Number of connections.
     - Captured credentials.
   - Do not intervene -- let the system operate autonomously.
   - Credentials are logged to the microSD with timestamps.

4. **Analysis and report**
   - Total number of portal connections.
   - Number of credentials entered.
   - Credential analysis (without memorizing them -- statistics only):
     - How many are real corporate credentials.
     - How many are personal credentials (private emails).
     - How many are fake/test credentials.
   - Average time between connection and credential entry.
   - Recommendations:
     - Employee training on WiFi phishing.
     - Implement 802.1X for the corporate network.
     - Rogue AP monitoring with WIDS.
     - Policy on connecting to unknown WiFi networks.

> Personal note: the key to success with Evil Portal is the SSID. A generic SSID like "Free WiFi" attracts few people in a corporate environment. An SSID that looks like a corporate WiFi upgrade ("CompanyName-WiFi-5G", "CompanyName-Guest-Fast") attracts many more. I have seen capture rates of 30-40% of employees in common areas with well-chosen SSIDs. Obviously, all of this with written management authorization.

### 8.3 Scenario: Stealth WiFi Reconnaissance

**Objective:** Completely map the target's wireless environment without being detected by WIDS (Wireless Intrusion Detection System).

**Required kit:**
- Flipper Zero
- ESP32-WROOM with Ghost ESP firmware
- Discreet container (bag, jacket with inside pocket)

**Operational procedure:**

1. **Planning**
   - Identify areas to map.
   - Plan the route to cover the entire area.
   - Estimate timing: 30-60 minutes for a medium building.
   - Verify that Ghost ESP is configured in fully passive mode.

2. **Execution**
   - Activate Ghost ESP before entering the target area.
   - Mode: passive scan + MAC randomization.
   - Walk normally along the planned route.
   - Do not stop at suspicious points -- maintain natural behavior.
   - The Flipper in your pocket collects data without requiring interaction.
   - Duration: minimum 20 minutes for meaningful data.

3. **Post-reconnaissance analysis**
   - Extract logs from the microSD.
   - Analyze:
     - Complete AP list with channels and encryption.
     - Detected clients and networks they are searching for (probe requests).
     - Traffic patterns by area.
     - AP vendors (to identify the infrastructure manufacturer).
   - Plan the next phase:
     - Targets for directed attacks (with Marauder).
     - Identified vulnerabilities (WEP, Open, isolated APs).
     - Devices of interest for BLE auditing.

4. **Advantages of the stealth approach**
   - No frames transmitted = no WIDS logs.
   - No probe requests = no device fingerprint.
   - MAC randomization = even if detected (unlikely), it is not traceable.
   - The Flipper+ESP32 in your pocket does not attract visual attention.

### 8.4 Scenario: Surveillance with ESP32-CAM

**Objective:** Visual monitoring of an area during a physical security assessment.

**Required kit:**
- Flipper Zero
- ESP32-CAM with IR LED (for night vision)
- Large powerbank (10000+ mAh)
- Camera support/mount
- MicroSD for the ESP32-CAM (for local recording)

**Operational procedure:**

1. **Camera setup**
   - Flash Camera Suite or Motion Detection firmware onto the ESP32-CAM.
   - Mount the ESP32-CAM with a view of the area of interest:
     - Server room door.
     - Passageway area.
     - Network rack.
   - Connect to the Flipper for initial configuration.
   - Configure:
     - Resolution and frame rate (balance quality vs battery life).
     - IR mode: auto for day/night switching.
     - Motion detection: enable to save SD space.
     - Sensitivity: medium (avoid false positives from lighting changes).

2. **Deployment**
   - Position the device discreetly.
   - Verify the framing from the Flipper.
   - Ensure sufficient power for the planned duration.
   - Disconnect the Flipper if live monitoring is not needed (the ESP32-CAM operates autonomously with motion detection and SD recording).

3. **Monitoring (optional)**
   - If live monitoring is needed: keep the Flipper connected.
   - The stream shows the framing in real time.
   - Motion notifications on the display.

4. **Results collection**
   - Retrieve the microSD from the ESP32-CAM.
   - Analyze photos/recordings:
     - Server room access times.
     - Personnel who accessed (authorized?).
     - Procedures followed (badge, key, tailgating).
     - Access duration.
   - Integrate into the physical security report:
     - Compliance with access policy.
     - Evidence of tailgating or unauthorized access.
     - Access control recommendations.

> Personal note: surveillance with the ESP32-CAM is one of the most powerful and sensitive applications from a legal and ethical standpoint. Use this tool ONLY with explicit written authorization that mentions video surveillance. In many countries, video recording without consent is illegal even during an authorized pentest if not explicitly provided for in the contract. Always verify with legal counsel before proceeding. From a technical standpoint, the ESP32-CAM with motion detection and IR LED works surprisingly well as a low-cost surveillance system -- the main limitation is the resolution (2MP) and optics quality.

---

## Cross-Reference - Multi-Vector Scenarios

| Scenario | Related Module | Link | How They Connect |
|----------|---------------|------|------------------|
| Evil portal + BadUSB | USB/Bad USB | [05-Scenari-Reali](../../USB/Bad%20USB/05-Scenari-Reali.md) | WiFi credentials via evil portal → BadUSB for workstation access |
| Deauth + Sub-GHz | Sub-GHz | [05-Scenari-Reali](../../Sub-GHz/05-Scenari-Reali.md) | WiFi alarm disruption + RF replay for complete bypass |
| WiFi scan + NFC | NFC | [05-Scenari-Reali](../../NFC/05-Scenari-Reali.md) | Physical access with NFC badge → internal WiFi reconnaissance |
| ESP32 + NRF24 | GPIO/NRF24 | [04-Scenari-Reali](../NRF24/04-Scenari-Reali.md) | WiFi scan + 2.4 GHz scan for complete wireless mapping |
| ESP32 + BLE | Bluetooth | [05-Scenari-Reali](../../Bluetooth/05-Scenari-Reali.md) | WiFi + BLE combined scans for complete IoT device inventory |
