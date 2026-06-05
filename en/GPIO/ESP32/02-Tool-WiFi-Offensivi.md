## 3. Offensive WiFi Tools

### 3.1 Marauder

**What it does at a technical level**

ESP32 Marauder is a complete WiFi 802.11 attack and analysis suite that leverages the ESP32's ability to operate in promiscuous mode and inject raw 802.11 frames. The firmware turns the ESP32 into a network analyzer and offensive tool entirely controlled from the Flipper Zero.

At the protocol level, Marauder operates by manipulating WiFi management frames which, in the 802.11 standard, are neither authenticated nor encrypted (unless 802.11w/PMF is active). This allows:

- Sending deauthentication frames (type 0xC0) spoofing the access point's BSSID, causing client disconnection.
- Generating beacon frames (type 0x80) with arbitrary SSIDs, creating phantom networks visible to nearby devices.
- Capturing probe requests (type 0x40) to identify nearby devices and the networks they are searching for.
- Monitoring all WiFi traffic in promiscuous mode for passive analysis.

**Complete step-by-step procedure**

1. Flash the Marauder firmware onto the ESP32 (see section 2).
2. Connect the ESP32 to the Flipper via GPIO (TX, RX, 3.3V, GND).
3. On the Flipper: Applications > GPIO > [ESP32] WiFi Marauder.
4. The Flipper establishes the UART connection with the ESP32.
5. The main menu opens with available options.

**Main commands and features:**

`Scan WiFi (APs)` - Starts an active scan of access points across the 14 channels of the 2.4GHz band. For each detected AP it shows: SSID, BSSID (MAC), channel, RSSI (signal strength in dBm), encryption type (Open/WEP/WPA/WPA2/WPA3), and number of associated clients. The scan cycles between channels with a configurable dwell time.

`Scan WiFi (Stations)` - Scans for client devices (stations) in the area. Captures probe requests sent by devices to reveal: client MAC address, SSIDs of networks being searched (probe requests), signal strength. Useful for device fingerprinting.

`Deauth` - Deauthentication attack. Sends spoofed deauth frames from the AP to connected clients, causing disconnection. Parameters:
- Target: single AP, all detected APs, or specific client
- Duration: continuous or limited burst
- Reason code: deauthentication code (default 7 = "Class 3 frame received from non-associated station")
- Channel: channel to operate on

`Beacon Spam` - Generates hundreds of beacon frames with random or predefined SSIDs, flooding the WiFi network list of nearby devices. Modes:
- Random: randomly generated SSIDs
- List: SSIDs from a file on the Flipper's SD
- Rickroll: classic list of SSIDs that form the lyrics to "Never Gonna Give You Up"
- Target: clones the beacons of a specific AP with variations

`Probe Flood` - Sends massive probe requests across all channels, simulating hundreds of devices searching for networks. Useful for stressing APs and IDS.

`PMKID Capture` - Attempts to capture the PMKID (Pairwise Master Key Identifier) from WPA2 APs. The PMKID is contained in the first message of the EAPOL handshake and can be cracked offline without the need to capture the full 4-way handshake. Captured PMKIDs are saved in hashcat format on the SD.

`Packet Monitor` - Displays WiFi traffic in real time on the selected channel with a packet density graph. Useful for identifying congested channels and anomalous activity.

`Channel Hop` - Continuous scanning cycling through channels with per-channel activity visualization. The dwell time (time on each channel) is configurable.

**Configurable parameters:**
- Operating channel: 1-14 (or auto-hop)
- TX power: configurable within ESP32 hardware limits
- MAC filters: whitelist/blacklist for specific targets
- Dwell time for channel hopping
- Log format: PCAP, CSV, raw
- Interface: verbose or minimalist

**Real-world pentest usage example:**

During an authorized wireless assessment, the typical procedure is:
1. Scan APs to map all networks within the test scope.
2. Scan Stations to identify connected clients.
3. Targeted deauth on a specific client to force reassociation.
4. PMKID capture during reassociation.
5. Export files to SD for offline cracking with hashcat (`hashcat -m 22000`).

> Personal note: Marauder is the tool I use the most with the ESP32, hands down. For wireless pentesting it is essential as a rapid reconnaissance tool -- the AP+Stations scan in 30 seconds gives you a complete picture of the target's wireless attack surface. I only use deauth when I have explicit written authorization, and in any case in a targeted manner (single client) to minimize impact. Beacon spam on the other hand is only useful for client demonstrations -- it has no real offensive value but it illustrates the vulnerability of unprotected management frames.

### 3.2 Evil Portal

**What it does at a technical level**

Evil Portal turns the ESP32 into a WiFi access point with an integrated captive portal. Technically, the ESP32 starts a soft-AP (software access point) and a DNS server that resolves any domain to the ESP32's local IP. When a device connects to the AP and attempts to browse, the internal DNS spoofing redirects all HTTP requests to an HTML page hosted on the ESP32.

This technique exploits the captive portal detection mechanism present in all modern operating systems: when a device connects to a WiFi network, it sends an HTTP request to a known URL (e.g., `captive.apple.com` for iOS, `connectivitycheck.gstatic.com` for Android). If the response does not match the expected one, the system automatically opens the captive portal browser, displaying the attacker's page.

The page can be customized to simulate any login: hotel portal, corporate network, social login, firmware update, or any other interface that induces the victim to enter credentials.

**Complete step-by-step procedure**

1. Flash the Evil Portal firmware onto the ESP32.
2. Prepare the portal HTML page:
   - Create an HTML file with the desired login form.
   - The form must submit data via POST to the root (`/`).
   - Copy the HTML file to the Flipper's microSD at `SD:/apps_data/evil_portal/`.
3. Connect the ESP32 to the Flipper via GPIO.
4. On the Flipper: Applications > GPIO > Evil Portal.
5. Configure:
   - AP SSID (e.g., "Hotel_WiFi_Free", "Corporate_Guest", "Starbucks_WiFi")
   - WiFi channel (default 1, choose a free channel)
   - HTML page to serve
6. Start the portal.
7. Monitor connections and captured credentials on the Flipper display.
8. Credentials are logged to the microSD in text format.

**Example HTML file structure:**

```html
<!DOCTYPE html>
<html>
<head>
    <title>WiFi Login</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { font-family: Arial; text-align: center; padding: 20px; }
        input { width: 80%; padding: 10px; margin: 5px; }
        button { padding: 10px 40px; background: #007bff; color: white; border: none; }
    </style>
</head>
<body>
    <h2>Free WiFi Access</h2>
    <p>Please sign in to continue</p>
    <form method="POST" action="/">
        <input type="email" name="email" placeholder="Email"><br>
        <input type="password" name="password" placeholder="Password"><br>
        <button type="submit">Connect</button>
    </form>
</body>
</html>
```

**Configurable parameters:**
- Access point SSID (up to 32 characters)
- WiFi channel (1-13)
- Custom HTML page (size limited by ESP32 flash)
- Post-login behavior (success page, redirect)
- Session timeout
- Maximum simultaneous clients
- Hidden SSID (hidden AP)

**Real-world pentest usage example:**

Scenario: employee awareness testing in a company.
1. Create a portal that simulates the corporate VPN login or WiFi guest portal.
2. Position the ESP32+Flipper in a common area (cafeteria, meeting room).
3. The SSID must be credible: "CompanyName-Guest" or "CompanyName-VPN-Login".
4. Monitor how many employees enter real credentials.
5. Document the results for the report -- the goal is to demonstrate the need for security training.

> Personal note: Evil Portal is devastating as a social engineering tool. The key to success is page credibility: spend time faithfully replicating the target's real portal, including logos, colors, and fonts. A generic "Free WiFi" portal works in public spaces, but in a corporate environment you need to be specific. Keep in mind that captured credentials are in cleartext -- if the target uses 2FA, you will still have the password but you won't be able to access without the second factor. In the report, this data point is still critical.

### 3.3 Ghost ESP

**What it does at a technical level**

Ghost ESP is an ESP32 firmware focused on stealth wireless reconnaissance operations. Unlike Marauder which also operates actively (injection, deauth), Ghost ESP favors the passive approach: the ESP32 operates exclusively in promiscuous mode without transmitting any frame, making itself invisible to wireless IDS/IPS systems (WIDS).

Technically, the ESP32 in promiscuous mode receives all WiFi frames on the selected channel without associating with any network. It does not send probe requests, does not respond to probe responses, and generates no traffic. The only emitted signal is the possible RF noise from the circuit, indistinguishable from background noise.

Ghost ESP also implements MAC address randomization: at each startup or at configurable intervals, the WiFi interface MAC is changed, preventing device tracking even in the event of detection.

**Complete step-by-step procedure**

1. Flash the Ghost ESP firmware onto the ESP32.
2. Connect the ESP32 to the Flipper via GPIO.
3. On the Flipper: Applications > GPIO > Ghost ESP.
4. Select the scanning mode:
   - Passive Scan: monitoring on fixed channel or with channel hopping
   - Signal Profiling: detailed RF characteristic analysis
   - Device Fingerprint: device identification from traffic patterns
5. Start the scan.
6. Data is displayed in real time and logged to the SD.

**Detailed features:**

`Passive WiFi Scan` - Captures all WiFi frames without transmitting. Identifies APs, clients, traffic, occupied channels. No trace left on the network.

`MAC Randomization` - Automatically changes the ESP32 MAC at configurable intervals (default: every 60 seconds). Prevents fingerprinting of the scanning device.

`Signal Profiling` - Detailed analysis of the RF characteristics of each source: average power, variance, temporal patterns. Useful for distinguishing fixed APs from mobile devices and for estimating distance.

`Client Tracking` - Monitors probe requests to track device movements in the area. Any device searching for WiFi networks reveals its own MAC and the list of saved networks.

`Stealth Channel Hop` - Channel hopping with randomized timing to avoid recognizable patterns by advanced WIDS.

**Configurable parameters:**
- Listening channel (fixed or hopping)
- MAC randomization interval
- Filters by frame type (management, control, data)
- Per-channel dwell time (in hopping mode)
- Export format for logs (CSV, JSON)
- Minimum RSSI sensitivity (filter weak signals)

**Real-world pentest usage example:**

Reconnaissance phase of a wireless assessment in a hostile environment (target with active WIDS):
1. Activate Ghost ESP in passive scan mode.
2. Position yourself in the target area without raising suspicion.
3. Collect for 15-30 minutes: complete AP list, associated clients, networks searched by devices.
4. Analyze probe requests to identify devices of interest (e.g., corporate laptops searching for the corporate network).
5. Export data for the subsequent attack phase (with Marauder or Evil Portal).

> Personal note: Ghost ESP is the tool I use in the initial phase of every wireless assessment. Before doing anything active, I spend at least 20 minutes in passive mode to understand the environment. In environments with WIDS (Cisco CleanAir, Aruba RFProtect), active scanning is detected immediately -- Ghost ESP lets you map everything without raising alarms. The trick is to combine them: Ghost first for reconnaissance, then Marauder for targeted attacks.

### 3.4 Wardriver

**What it does at a technical level**

Wardriver turns the Flipper Zero + ESP32 into a classic wardriving tool: continuous WiFi network scanning with geolocation via an external GPS module. The ESP32 handles the WiFi scanning while a GPS module (connected via secondary UART or integrated) provides geographic coordinates. The data is correlated and saved in a format compatible with WiGLE (Wireless Geographic Logging Engine), the worldwide WiFi network database.

At a technical level, the ESP32 runs a continuous loop: rapid scan across all 2.4GHz channels, collection of beacon frames with SSID/BSSID/channel/RSSI/encryption, timestamp and current GPS coordinates, writing to CSV file on the microSD.

**Complete step-by-step procedure**

1. Required hardware:
   - ESP32-WROOM with Wardriver firmware
   - GPS module (e.g., NEO-6M, NEO-7M, NEO-8M) connected to the ESP32
   - Flipper Zero
   - Powerbank for power during movement
2. GPS connection to ESP32:
   - GPS TX -> ESP32 GPIO16 (RX2)
   - GPS RX -> ESP32 GPIO17 (TX2)
   - GPS VCC -> 3.3V
   - GPS GND -> GND
3. Connect ESP32 to Flipper via standard GPIO.
4. On the Flipper: Applications > GPIO > Wardriver.
5. Wait for GPS fix (first acquisition may take 1-5 minutes outdoors).
6. Start moving through the target area.
7. The display shows: networks found, current coordinates, speed, new/duplicate networks.
8. When finished, stop the scan.
9. Export the CSV file from the microSD.

**WiGLE CSV output format:**

```
MAC,SSID,AuthMode,FirstSeen,Channel,RSSI,CurrentLatitude,CurrentLongitude,AltitudeMeters,AccuracyMeters,Type
AA:BB:CC:DD:EE:FF,NetworkName,WPA2,2024-01-15 14:30:00,6,-65,45.4642,9.1900,120,5,WIFI
```

**Configurable parameters:**
- Scan interval (default: every 2 seconds)
- Channels to scan (all or subset)
- Minimum RSSI filter (e.g., only networks above -80 dBm)
- Output format (WiGLE CSV, KML for Google Earth)
- Deduplication (filter already seen networks)
- Output file name

**Real-world pentest usage example:**

Wireless attack surface assessment of a corporate campus:
1. Perimeter wardriving by car/on foot around the building.
2. Identify all networks visible from outside (potential signal leakage risk).
3. Map the coverage: corporate networks should not be visible 100m from the building.
4. Upload to WiGLE (optional) or local analysis.
5. Include in the report: network map, external signal, AP TX power recommendations.

### 3.5 Free Roam

**What it does at a technical level**

Free Roam is a simultaneous WiFi and BLE exploration tool that operates in continuous mode. The ESP32 rapidly alternates between WiFi scanning (promiscuous mode) and BLE scanning (observer mode), providing a complete view of the surrounding radio environment. Unlike dedicated scanners, Free Roam does not focus on a specific protocol but provides a global overview.

Technically, the ESP32 leverages its dual-core: one core handles WiFi scanning while the other handles BLE, enabling true simultaneity without significant packet loss.

**Complete step-by-step procedure**

1. Flash the appropriate firmware onto the ESP32 (firmware with integrated Free Roam support).
2. Connect the ESP32 to the Flipper via GPIO.
3. On the Flipper: Applications > GPIO > Free Roam.
4. Select active modes:
   - WiFi only
   - BLE only
   - WiFi + BLE simultaneous
5. Start roaming.
6. The display shows in real time:
   - Number of detected WiFi APs
   - Number of detected BLE devices
   - Mobile devices (identified via probe requests)
   - Signal density graphs
7. Data is continuously logged to the microSD.
8. Export in CSV/JSON for subsequent analysis.

**Configurable parameters:**
- Active protocols (WiFi, BLE, both)
- Display update interval
- Minimum RSSI filter
- Continuous or interval-based logging
- Export format (CSV, JSON)
- Device deduplication

**Real-world pentest usage example:**

Initial reconnaissance of an unknown environment:
1. Activate Free Roam at the entrance of the target area.
2. Walk through the area for 10-15 minutes.
3. Obtain a complete map of: WiFi networks, BLE devices (smartwatches, fitness trackers, beacons, IoT), mobile devices.
4. Analyze the data to plan subsequent attacks: which networks to attack, which BLE devices are interesting, how many devices are present in the area.

### 3.6 WiFi Mapping

**What it does at a technical level**

WiFi Mapping creates WiFi signal coverage maps (heatmaps) by correlating signal strength (RSSI) to physical position. The ESP32 performs continuous RSSI measurements of detected networks while the user moves through the area. The data is then aggregated to create a visual representation of coverage.

Unlike Wardriver which uses GPS for coordinates, WiFi Mapping is designed for indoor environments where GPS does not work: coordinates are based on a relative system (steps, reference points) or manual user input.

**Complete step-by-step procedure**

1. Connect the ESP32 to the Flipper via GPIO.
2. On the Flipper: Applications > GPIO > WiFi Mapping.
3. Select the target network to map (or all networks).
4. Configure mapping parameters:
   - Sampling interval
   - Area to map (virtual grid)
   - Reference points
5. Start the path through the area:
   - At each significant point, confirm the position.
   - The ESP32 samples the signal for a few seconds.
   - The average RSSI value is associated with the position.
6. Complete the path covering the entire area.
7. View the generated heatmap on the Flipper display.
8. Export data for PC processing.

**Configurable parameters:**
- Target network (specific BSSID or all)
- RSSI sampling interval
- Number of samples per point
- Grid size
- Color thresholds for the heatmap (e.g., green > -50dBm, yellow > -70dBm, red > -85dBm)
- Export format

**Real-world pentest usage example:**

Office wireless coverage assessment:
1. Map the corporate network signal throughout the building.
2. Identify dead zones (no coverage) and signal leakage zones (strong signal outside).
3. Verify that sensitive networks are not accessible from public areas.
4. Include the heatmap in the report with AP placement recommendations.

### 3.7 WiFi Marauder

**What it does at a technical level**

WiFi Marauder is an extended and enhanced version of the classic Marauder, developed specifically for Flipper Zero integration. Compared to the base Marauder, it offers improved packet management, a user interface optimized for the Flipper's small screen, and additional logging and automation features.

Key differences from the standard Marauder:
- Optimized memory management: circular buffer for captured packets, avoiding overflow on long sessions.
- Improved interface: hierarchical menus, compact information display, real-time graphs.
- Enhanced logging: automatic SD saving with file rotation, precise timestamps, format compatible with analysis tools.
- Automation: ability to create sequential attack scripts (e.g., scan -> deauth -> capture -> stop).
- Advanced filters: MAC, SSID, channel whitelist/blacklist.

**Complete step-by-step procedure**

1. Flash the WiFi Marauder firmware (different from the base Marauder) onto the ESP32.
2. Connect the ESP32 to the Flipper via GPIO.
3. On the Flipper: Applications > GPIO > WiFi Marauder.
4. Main menu:
   - Scan: AP and station scanning
   - Attack: deauth, beacon spam, probe flood
   - Capture: PMKID capture, handshake
   - Monitor: packet monitor, channel activity
   - Settings: parameter configuration
5. For advanced analysis:
   - Launch Scan -> select target from the list.
   - Switch to Attack -> select attack type.
   - Enable Capture for logging.
   - Monitor in Monitor.

**Additional configurable parameters compared to base Marauder:**
- Automation scripts (command sequences)
- Automatic log rotation
- Automatic timeout for attacks
- Advanced MAC filters (regex-like)
- Burst mode for deauth (configurable intervals)
- PCAP format for packet capture (Wireshark compatible)

**Real-world pentest usage example:**

Automated wireless assessment:
1. Create a script: scan 30s -> identify target -> targeted deauth -> PMKID capture -> stop.
2. Execute the script for each network within the test scope.
3. Collect all PMKIDs and handshakes in separate files.
4. Offline analysis with hashcat to assess password strength.
5. Detailed report with attack timeline from the automatic log.

### 3.8 Wendigo BT+BLE+WiFi Monitor

**What it does at a technical level**

Wendigo is a tri-protocol monitor that simultaneously scans Bluetooth Classic, Bluetooth Low Energy (BLE), and WiFi. The ESP32, thanks to its combined WiFi+BT radio controller, can operate on all three protocols by rapidly alternating between modes.

At a technical level:
- WiFi: scanning in promiscuous mode, capturing beacon/probe/data frames.
- BLE: scanning in observer mode, capturing advertising packets (ADV_IND, ADV_DIRECT_IND, ADV_NONCONN_IND, ADV_SCAN_IND).
- BT Classic: inquiry scan for discoverable devices, capturing device name and class (CoD - Class of Device).

Wendigo's distinguishing feature is cross-protocol correlation: it can identify devices that simultaneously use WiFi and BLE (e.g., smartphones, laptops, IoT), creating a complete device profile.

**Complete step-by-step procedure**

1. Flash the Wendigo firmware onto the ESP32 (requires ESP32-WROOM for BT Classic support).
2. Connect the ESP32 to the Flipper via GPIO.
3. On the Flipper: Applications > GPIO > Wendigo.
4. Configure protocols to monitor:
   - WiFi: on/off, channels, frame type
   - BLE: on/off, advertising type filter
   - BT Classic: on/off, inquiry timeout
5. Start monitoring.
6. The display shows:
   - List of detected devices per protocol
   - Cross-protocol correlations (same device on WiFi+BLE)
   - RSSI per device
   - Device type (smartphone, laptop, IoT, wearable)
7. Real-time filters by protocol type or signal strength.
8. Combined log export.

**Configurable parameters:**
- Active protocols (any combination of the three)
- Filter by device type (CoD for BT, ADV type for BLE)
- Minimum RSSI threshold
- Update interval
- Cross-protocol correlation (on/off)
- Logging format (CSV, JSON, raw)
- Session duration (automatic timer)

**Real-world pentest usage example:**

Radio surface analysis of an office:
1. Activate Wendigo with all three protocols.
2. Monitor for 30-60 minutes during business hours.
3. Identify: how many devices are present, which protocols they use, unauthorized IoT devices (e.g., personal IP cameras, smart speakers), BLE devices with exposed advertising.
4. Cross-protocol correlation allows associating a device's WiFi MAC with its BLE MAC -- useful for tracking.
5. Report: radio device inventory, unauthorized devices, BYOD policy recommendations.

> Personal note: Wendigo is underrated. Most pentesters focus only on WiFi, but the BLE attack surface is enormous and often neglected. I have found unauthorized IoT devices in "secure" offices simply by monitoring BLE for half an hour. Smart speakers, IP cameras, fitness trackers -- they all expose information via BLE advertising that can be exploited.

---
