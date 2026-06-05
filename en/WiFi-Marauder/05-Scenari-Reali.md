## 6. Penetration Testing Scenarios

### 6.1 Scenario 1: Wireless Reconnaissance of a Target Building

**Context**: the client has commissioned a penetration test on the security
of their wireless infrastructure. The first day is dedicated to
reconnaissance.

**Objective**: completely map the target's WiFi infrastructure without
being detected, gathering information on networks, encryption, devices,
and potential vulnerabilities.

**Phase 1 - External reconnaissance (30 min)**

Equipment: Flipper Zero + ESP32 devboard, in pocket or backpack.

1. Walk around the building perimeter
2. Start AP scan from the Flipper:
   ```
   scanap
   ```
3. Repeat from at least 4 positions (4 sides of the building) to maximize
   coverage
4. For each position, mentally note the RSSI and name of visible networks

**Phase 2 - Results analysis**

From the scan output, create a matrix:

```
+----+-------------------+--------+-----------+---------+
| #  | SSID              | Channel| Encryption| RSSI    |
+----+-------------------+--------+-----------+---------+
| 1  | Corp_WiFi         | 6      | WPA2-ENT  | -45     |
| 2  | Corp_Guest        | 1      | WPA2-PSK  | -48     |
| 3  | Corp_IoT          | 11     | WPA2-PSK  | -62     |
| 4  | (hidden)          | 6      | WPA2-PSK  | -70     |
| 5  | HP_Printer_LAN    | 1      | Open      | -72     |
| 6  | SecurityCam       | 11     | WEP       | -78     |
+----+-------------------+--------+-----------+---------+
```

**Phase 3 - Tactical analysis**

From this scan an experienced pentester identifies:

1. **Corp_WiFi (WPA2-Enterprise)**: main network, difficult to attack
   directly. Requires domain credentials or client certificate.
   Possible attack: Evil Twin with self-signed certificate to capture
   NTLM hash (MS-CHAPv2).

2. **Corp_Guest (WPA2-PSK)**: guest network with shared password. Priority
   target for PMKID/handshake. The password might be weak
   ("Guest2024", "Welcome1", etc.) and shared with visitors.

3. **Corp_IoT (WPA2-PSK)**: dedicated IoT network. If properly isolated,
   low priority. If not isolated, could provide access to the internal
   network after cracking the password.

4. **Hidden network**: deserves investigation. "Security through obscurity" suggests
   a sensitive network. By intercepting probe responses when a client
   connects, the SSID is revealed.

5. **HP_Printer_LAN (Open)**: open printer network. Direct access.
   From there, possible lateral movement if the printer has interfaces on
   the corporate network.

6. **SecurityCam (WEP)**: WEP has been broken for 20 years. Instant crack with
   aircrack-ng. Access to security cameras = critical finding.

**Phase 4 - Client scan**

```
scansta
```

Identify how many devices are connected to each network. Networks with
many clients = more visibility in the environment.

**Report output (example):**

```
FINDING: IoT network with WPA2-PSK encryption accessible from outside
  Severity: High
  Description: The Corp_IoT network is reachable from the parking lot with RSSI -62
  Risk: An attacker could attempt offline PSK cracking
  Recommendation: Reduce transmission power, implement 802.11w

FINDING: Security cameras on WEP
  Severity: Critical
  Description: The SecurityCam network uses WEP, crackable in seconds
  Risk: Unauthorized access to the camera feed
  Recommendation: Migrate immediately to WPA2/WPA3

FINDING: Open printer network
  Severity: High
  Description: The HP printer exposes an Open network without authentication
  Risk: Direct access to the printer, potential pivot to the internal network
  Recommendation: Disable WiFi Direct, connect the printer via cable
```

### 6.2 Scenario 2: WPA2 Handshake Capture for Offline Cracking

**Context**: the client has authorized testing of WiFi password strength
for the guest network "Corp_Guest" (WPA2-PSK).

**Objective**: capture the cryptographic material needed to attempt
offline password cracking.

**Phase 1 - PMKID attempt (silent)**

1. AP scan to identify the target:
   ```
   scanap
   ```
   Select "Corp_Guest"

2. PMKID capture attempt:
   ```
   sniffpmkid
   ```

3. Wait 15-30 seconds

4. If PMKID captured: success, proceed to cracking. No impact on users.

5. If PMKID not available: proceed to Phase 2.

**Phase 2 - Handshake capture via deauth (if PMKID fails)**

1. Client scan to identify devices connected to Corp_Guest:
   ```
   scansta
   ```

2. Select a client with good signal

3. Start EAPOL sniffer:
   ```
   sniffeapol
   ```
   Verify the channel is correct.

4. Wait 2-3 seconds for the sniffer to become operational

5. Send a single deauth frame to the selected client (not broadcast):
   ```
   attack -t deauth
   ```

6. The client disconnects and reconnects automatically in 1-5 seconds

7. The sniffer captures the handshake (4 EAPOL messages)

8. Stop everything:
   ```
   stopscan
   ```

9. Verify the capture: extract the .pcap from the SD card

**Phase 3 - Offline cracking**

On your own hardware (not on the Flipper):

```bash
# Format conversion
hcxpcapngtool -o corp_guest.hc22000 capture.pcap

# Verification
hashcat -m 22000 corp_guest.hc22000 --show

# Attempt 1: standard dictionary
hashcat -m 22000 corp_guest.hc22000 /usr/share/wordlists/rockyou.txt

# Attempt 2: dictionary with rules
hashcat -m 22000 corp_guest.hc22000 wordlist.txt -r /usr/share/hashcat/rules/best64.rule

# Attempt 3: custom dictionary (company name + variants)
# Create a file with variants: CorpName2024, CorpName2024!, corp_name_guest, etc.
hashcat -m 22000 corp_guest.hc22000 custom_corp.txt -r rules/best64.rule

# Attempt 4: numeric brute force (many guest networks use numbers)
hashcat -m 22000 corp_guest.hc22000 -a 3 ?d?d?d?d?d?d?d?d

# Attempt 5: common pattern (word + numbers)
hashcat -m 22000 corp_guest.hc22000 -a 6 wordlist.txt ?d?d?d?d
```

**Report output (example):**

```
FINDING: Weak guest WiFi password
  Severity: Medium
  Description: The Corp_Guest network password ("Welcome2024!") was
  cracked in 4 minutes using a custom dictionary with mutation rules.
  The password follows a common pattern (word + year + symbol) that is
  easily predictable.
  Risk: Unauthorized access to the guest network. If the network is not
  properly isolated, possible pivot to the corporate network.
  Recommendation: Implement complex passwords (16+ random characters),
  rotate them monthly, or migrate to WPA2-Enterprise with individual
  authentication for the guest network.
```

### 6.3 Scenario 3: Evil Portal for Credential Harvesting in a Hotel

**Context**: the client is a hotel chain that wants to test the
awareness of their guests regarding WiFi phishing. Test authorized
by hotel management.

**Objective**: create a captive portal that simulates the hotel's WiFi
login page to measure how many guests enter their credentials.

**Phase 1 - Reconnaissance**

1. Connect to the hotel's legitimate WiFi network as a normal guest
2. Document the legitimate captive portal login page:
   - Screenshot of the page
   - Colors, font, logo, layout
   - Required fields (first name, last name, room number, email, etc.)
   - Terms and conditions text

3. Environment scan with Marauder:
   ```
   scanap
   ```
   Identify SSID, channel, and parameters of the legitimate network.

**Phase 2 - Template preparation**

Create an HTML template that replicates the hotel's login page.
Load the file onto the Flipper's SD card.

Critical points for realism:
- Hotel logo (converted to base64)
- Same form fields as the original
- Same color scheme
- Similar legal disclaimer
- Identical "Accept & Connect" button

**Phase 3 - Evil Portal deployment**

1. Position the Flipper in a common area of the hotel (lobby, breakfast
   room, pool area) where the legitimate network signal is weak.

2. Configure the Evil Portal:
   - SSID identical to the hotel's network (Evil Twin)
   - Or similar SSID: "Hotel_Roma_WiFi_Free" if the legitimate network is
     "Hotel_Roma_WiFi"
   - Template: the custom page created

3. Start the Evil Portal

4. The Flipper creates the AP and serves the captive portal

5. Guests looking for WiFi see the fake network (often with stronger
   signal because the Flipper is in the same room)

6. They connect, the captive portal appears automatically

7. They enter the requested credentials

8. Credentials are saved to the SD card

**Phase 4 - Collection and analysis**

After the agreed test period (e.g., 24 hours), collect the data:

```
Credentials captured: 31 complete sets
Data collected: first name, last name, email, room number
Operating time: 22 hours (with external powerbank)
Success rate: ~40% of devices that saw the network
```

**Phase 5 - Report**

```
FINDING: Guests vulnerable to WiFi phishing
  Severity: High
  Description: Out of 78 devices that connected to the rogue AP, 31 guests
  (40%) entered real personal data on the phishing page. Of these, 12
  entered their personal email password (password reuse between the hotel
  WiFi and personal email).
  Risk: A real attacker could use the email credentials for access to
  personal/corporate services of the victims.
  Recommendations:
  - Implement WPA2-Enterprise with individual per-room credentials
  - Eliminate the captive portal based on email/password
  - Communicate the EXACT WiFi network name to guests at check-in
  - Implement WIDS to detect rogue APs with identical SSID
  - Train IT staff on Evil Twin detection
```

> Personal note: the 40% rate is realistic -- I have seen it in multiple engagements.
> People do not verify which network they connect to, especially in environments
> where they expect free WiFi. The most effective advice I give clients is
> always the same: eliminate captive portals based on credentials and switch to
> WPA2-Enterprise. The captive portal is a vulnerability by design.

### 6.4 Scenario 4: Wardriving for Area Network Mapping

**Context**: the client is a company with offices in a business park. They want
to know how many wireless networks are reachable from the surrounding area and whether
their own networks are visible from outside the perimeter.

**Objective**: map all WiFi networks within a 500m radius of the target
building.

**Phase 1 - Preparation**

1. Load updated Marauder on the ESP32
2. Verify GPS functionality (if external module available)
3. Prepare the route: circular walk around the business park,
   covering all corners and entrances

**Phase 2 - Wardriving**

1. Start continuous scanning with GPS logging
2. Walk along the planned route at a normal pace (constant speed
   for uniform sample distribution)
3. The Flipper continuously records: SSID, BSSID, channel, RSSI,
   encryption, GPS coordinates
4. Typical duration: 30-60 minutes for a 500m perimeter

**Phase 3 - Analysis**

1. Extract the CSV file from the SD card
2. Import into analysis tools:
   - Upload to WiGLE (map visualization)
   - Import into Google Earth / QGIS for custom mapping
   - Analysis with Python/pandas scripts for statistics

3. Create a WiFi coverage heatmap for the target

**Phase 4 - Typical results**

```
Total networks detected: 147
Client networks: 12
Client networks visible from outside: 8 out of 12 (67%)

Encryption detected:
  WPA3:           4 (3%)
  WPA2-Enterprise: 18 (12%)
  WPA2-Personal:  89 (61%)
  WPA:            11 (7%)
  WEP:            3 (2%)
  Open:           22 (15%)

Most used channels:
  Channel 1:  31 networks
  Channel 6:  42 networks
  Channel 11: 38 networks
  Others:     36 networks
```

**Phase 5 - Report**

```
FINDING: Corporate WiFi coverage beyond the physical perimeter
  Severity: Medium
  Description: 8 of the 12 corporate WiFi networks are detectable with
  usable signal (RSSI > -75 dBm) from the external parking lot and sidewalk.
  The industrial IoT network "Corp_IoT_Prod" is detectable at 200m from the building.
  Risk: An attacker could comfortably operate from outside without
  entering the building, attempting offline cracking or Evil Twin.
  Recommendations:
  - Reduce TX power on perimeter APs
  - Implement directional antennas pointed inward
  - Evaluate RF shielding for server rooms
  - Segment IoT networks on dedicated VLANs with firewalls
```

---

## Cross-Reference - Multi-Vector Scenarios

| Scenario | Related Module | Link | How they connect |
|----------|-----------------|------|-------------------|
| Evil portal + BadUSB | USB/Bad USB | [05-Scenari-Reali](../USB/Bad%20USB/05-Scenari-Reali.md) | Evil portal collects WiFi credentials → BadUSB for workstation pivot |
| Deauth + Sub-GHz | Sub-GHz | [05-Scenari-Reali](../Sub-GHz/05-Scenari-Reali.md) | WiFi alarm jamming + Sub-GHz sensor replay for complete bypass |
| WiFi reconnaissance + NFC | NFC | [05-Scenari-Reali](../NFC/05-Scenari-Reali.md) | NFC badge for physical access → internal WiFi scan for network mapping |
| WiFi + NRF24 | GPIO/NRF24 | [04-Scenari-Reali](../GPIO/NRF24/04-Scenari-Reali.md) | WiFi scan to find targets → MouseJacker on wireless peripherals |
| WiFi + BLE | Bluetooth | [05-Scenari-Reali](../Bluetooth/05-Scenari-Reali.md) | WiFi scan + BLE scan for complete wireless environment mapping |
| Wardriving + RFID | RFID | [05-Scenari-Reali](../RFID/05-Scenari-Reali.md) | Perimeter wardriving + parking badge testing in the same session |
