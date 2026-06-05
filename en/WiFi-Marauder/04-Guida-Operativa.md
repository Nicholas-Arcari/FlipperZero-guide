## 5. Main Features - Complete Detail

### 5.1 Scan - WiFi Discovery

Scanning is the first operation in any wireless engagement. It corresponds to
the reconnaissance phase in the PTES (Penetration Testing Execution Standard)
framework.

**Scan AP (Access Point Discovery):**

Marauder command: `scanap`

The ESP32 performs an active and passive scan on all 2.4 GHz channels (1-14,
depending on the region) and collects beacon frames from detected APs.

For each AP the following is displayed:
- **SSID**: network name (empty for hidden networks -- but the BSSID is still visible)
- **BSSID**: AP MAC address (uniquely identifies the device)
- **Channel**: operating channel (1-14)
- **RSSI**: Received Signal Strength Indicator in dBm (closer to 0 = stronger
  signal; -30 dBm = excellent, -50 dBm = good, -70 dBm = weak,
  -80 dBm = marginal, below -85 dBm = unusable)
- **Encryption**: Open, WEP, WPA, WPA2-Personal, WPA2-Enterprise, WPA3

**Scan Client (Station Discovery):**

Marauder command: `scansta`

After identifying APs, the client scan reveals devices connected to each
network.

For each client the following is displayed:
- Client MAC address
- AP it is associated with
- Client RSSI

**Tactical interpretation of results:**

As a pentester, you extract critical information from the scan:

1. **Attack surface**: how many APs, how many clients, what encryption
2. **Priority targets**: APs with weak encryption (WEP, WPA1, WPA2 without PMF)
3. **Client density**: APs with many clients = higher probability of capturing a handshake
4. **Hidden networks**: empty SSID but BSSID present -- can be discovered through
   probe response when a client connects
5. **Least congested channel**: if you need to operate a rogue AP, choose a free channel
6. **Vendor identification**: the first 3 bytes of the MAC (OUI) identify the manufacturer.
   This reveals the approximate AP model (Cisco, Ubiquiti, TP-Link, etc.)

```
Example scan output:
----------------------------------------------
#   SSID             BSSID              CH  RSSI  ENC
1   OfficeNet-5G     AA:BB:CC:DD:EE:01  6   -42   WPA2
2   Guest_WiFi       AA:BB:CC:DD:EE:02  1   -55   WPA2
3   (hidden)         AA:BB:CC:DD:EE:03  11  -68   WPA2
4   IoT_Sensors      AA:BB:CC:DD:EE:04  6   -71   Open
5   Printer_HP       AA:BB:CC:DD:EE:05  1   -75   WPA2
----------------------------------------------
```

In this example, a pentester would immediately notice:
- "IoT_Sensors" is an open network -- direct access without authentication
- The hidden network on channel 11 deserves investigation
- "OfficeNet-5G" is the primary target (strong signal, WPA2)
- "Guest_WiFi" might have client isolation disabled

> Personal note: I always perform the initial scan from the parking lot or the
> reception area of the target building. The Flipper in my pocket with the devboard
> connected is completely discreet. In 60 seconds I have the complete network map,
> without even taking out a laptop. Then I analyze the results calmly
> and plan the next steps.

### 5.2 Sniff - Packet Monitoring

WiFi sniffing with Marauder allows capturing raw frames from the radio air.
Unlike scanning (which processes data), the sniffer captures raw packets
and saves them for later analysis.

**Available sniffing types:**

**Sniff Raw:**

Command: `sniffraw`

Captures all frames on a specific channel or in channel hopping. Frames are
saved in .pcap format on the Flipper's SD card.

The .pcap file can be analyzed with:
- **Wireshark**: useful filters for WiFi analysis:
  - `wlan.fc.type == 0` -- management frames only
  - `wlan.fc.type_subtype == 0x08` -- beacons only
  - `wlan.fc.type_subtype == 0x0c` -- deauth only
  - `wlan.fc.type_subtype == 0x04` -- probe requests only
  - `eapol` -- EAPOL frames only (handshake)
  - `wlan.bssid == AA:BB:CC:DD:EE:FF` -- filter by specific AP

**Sniff Beacon:**

Command: `sniffbeacon`

Specifically captures beacon frames. Useful for:
- Detailed analysis of AP configurations
- Detection of rogue APs (unauthorized APs)
- Monitoring AP stability (beacon loss)
- IE (Information Elements) analysis for AP fingerprinting

**Sniff Deauth:**

Command: `sniffdeauth`

Specifically monitors deauthentication frames. This is useful for:
- Detecting if someone is attacking the network (passive WIDS)
- Verifying if deauth attacks are ongoing in the environment
- Debugging disconnection issues

**Sniff Probe:**

Command: `sniffprobe`

Captures probe requests from nearby devices. Each probe reveals:
- Device MAC address (potentially randomized)
- Searched SSID (if directed probe)
- Device supported rates

This is an intelligence gathering operation: it reveals which networks nearby
devices have memorized. In a hotel, an airport, a conference room,
probe requests can reveal:
- Corporate network names ("CorpNet-Acme_Inc")
- Networks of visited hotels ("Hilton_WiFi_Room412")
- Home networks ("Casa_Mario_5G")

**Sniff EAPOL:**

Command: `sniffeapol`

Specifically captures EAPOL (Extensible Authentication Protocol over LAN) frames,
i.e., the WPA2 4-way handshake messages. This is the most valuable capture for
offline password cracking.

The resulting .pcap file contains the EAPOL frames that can be converted to
hashcat format with the `hcxpcapngtool` tool:

```bash
hcxpcapngtool -o hash.hc22000 capture.pcap
hashcat -m 22000 hash.hc22000 wordlist.txt
```

**Sniff PMKID:**

Command: `sniffpmkid`

Specifically captures the PMKID from the first EAPOL message. The ESP32 sends an
association request to the target AP and waits for the response containing the PMKID.

> Personal note: I use EAPOL sniffing in combination with deauth. First I start
> the EAPOL sniffer on a specific channel, then I launch a targeted deauth to force
> a client to reconnect. This way I capture the complete handshake in
> a few seconds. The key is to have the sniffer ALREADY active before the deauth,
> otherwise you miss the first message.

### 5.3 Deauth Attack

The deauthentication attack is probably the most well-known and most used
(and abused) Marauder function. It is also the most dangerous from a legal
perspective.

**How it works technically:**

The deauthentication frame is a management frame with subtype 0x0C. In original
802.11 (without 802.11w/PMF), management frames are neither authenticated nor encrypted.

This means anyone can forge a deauthentication frame with:
- Source address = AP MAC (spoofed)
- Destination address = target client MAC (or FF:FF:FF:FF:FF:FF for broadcast)
- Reason code: a numeric value indicating the reason for deauthentication

```
Deauthentication Frame:
+------------------+------------------+------------------+
|  Frame Control   |  Duration        |  DA (client MAC) |
|  Type=0, Sub=12  |                  |  or broadcast    |
+------------------+------------------+------------------+
|  SA (AP MAC)     |  BSSID (AP MAC)  |  Seq Control     |
|  (spoofed)       |                  |                  |
+------------------+------------------+------------------+
|  Reason Code (2 byte)              |  FCS             |
+------------------------------------+------------------+
```

Common reason codes:
- 1: Unspecified reason
- 2: Previous authentication no longer valid
- 3: Deauthenticated because sending station is leaving
- 4: Disassociated due to inactivity
- 6: Class 2 frame received from nonauthenticated station
- 7: Class 3 frame received from nonassociated station

The AP and the client, upon receiving the frame, believe the other party has terminated
the connection and disconnect. The client typically attempts immediate
reconnection, generating a new 4-way handshake -- which is exactly what
the pentester wants to capture.

**Targeting modes in Marauder:**

1. **Deauth on specific AP**: disconnects all clients from a single AP
   - Select the AP from the scan list
   - Start the deauth

2. **Deauth on specific client**: disconnects a single client from an AP
   - Requires the pair (AP MAC, Client MAC)
   - More targeted, less noisy

3. **Broadcast deauth**: deauth frame with DA = FF:FF:FF:FF:FF:FF
   - Disconnects all clients from the target AP
   - More effective but noisier and more detectable

4. **Multi-target deauth**: simultaneous attack on multiple APs/clients
   - Useful for maximizing handshake capture probability
   - Extremely noisy -- use only in lab environments

**Countermeasures (that the pentester must be aware of):**

1. **802.11w (PMF - Protected Management Frames)**: encrypts critical
   management frames (deauth, disassoc). If active, spoofed deauth is discarded
   by the client. WPA3 mandates it.

2. **WIDS/WIPS (Wireless Intrusion Detection/Prevention System)**: systems like
   Cisco Adaptive wIPS, Aruba RFProtect, AirMagnet Enterprise detect
   deauth floods immediately. The pattern is unmistakable: a burst of
   deauth frames from the same BSSID within seconds.

3. **Client-side protection**: some modern WiFi drivers ignore broadcast deauth
   or implement a delay before disconnecting.

4. **Rate limiting**: some APs implement throttling on management frames.

**Legal risks:**

Sending deauthentication frames on networks you do not own is illegal in Italy and
throughout the EU. It constitutes unlawful interference with a computer system and
violation of communications. Penalties include up to 4 years imprisonment
(art. 617-quater c.p.). This is not a theoretical risk: there have been criminal
proceedings for deauth attacks.

> Personal note: deauth is the most used tool for forcing handshake capture,
> but it is also the noisiest. In a real engagement, if the client has a WIDS
> (and any enterprise network does), you are detected in 3 seconds.
> My approach: first attempt always with PMKID (zero noise). Only if it fails,
> a single targeted deauth (not broadcast) on a specific client, with the EAPOL
> sniffer already active. Never deauth flood. Never broadcast deauth in an enterprise environment.

### 5.4 Beacon Spam

Beacon spam generates fake beacon frames to create the illusion of tens or
hundreds of WiFi networks in the surrounding area.

**How it works:**

The ESP32 generates and transmits beacon frames with:
- Customizable SSIDs
- Randomly generated (or sequential) BSSIDs
- Realistic parameters (RSN IE, supported rates, DS parameter set)
- Standard beacon interval (100 TU)

Devices scanning for networks will see all these fake networks appear
in their WiFi list.

**Available modes:**

1. **Random SSID**: generates random network names
   - Command: `attack -t beacon -r`
   - Useful for stress testing clients

2. **Rickroll SSID List**: generates APs with names composing the lyrics of
   "Never Gonna Give You Up" by Rick Astley
   - Command: `attack -t beacon -l rickroll`
   - Classic hacking community meme

3. **Custom SSID List**: generates APs with custom names loaded from a file
   - Command: `attack -t beacon -l custom`
   - The file with SSIDs must be loaded onto the SD card
   - Useful for specific social engineering scenarios

**Use in penetration testing and social engineering:**

Beacon spam has serious applications in pentesting:

1. **User confusion**: in an office, creating dozens of networks with names similar
   to the legitimate one ("Company_WiFi", "Company-WiFi", "Company_WiFi_5G",
   "Company_WiFi_Guest") can induce users to connect to the wrong network
   (especially if combined with Evil Portal).

2. **Policy testing**: verify whether corporate devices have policies that
   prevent connection to unapproved networks. If a corporate laptop
   attempts to connect to a fake AP, the MDM policy is inadequate.

3. **Distraction**: during a red team engagement, beacon spam can saturate
   SOC consoles while you operate on another vector.

4. **WIDS testing**: verify whether the WIDS system detects and reports the sudden
   appearance of dozens of unknown APs.

**Technical aspects of beacon generation:**

The ESP32 can generate approximately 50-100 different beacons credibly, limited by:
- Transmission speed (each beacon requires airtime)
- Available memory for beacon structures
- The need to maintain a realistic beacon interval (if too slow, clients
  do not list the network; if too fast, it is obviously artificial)

> Personal note: I used beacon spam in an engagement to test whether the
> client's IT team monitored the wireless environment. I generated 50 APs with names
> similar to the corporate network. Result: no alarm for 48 hours. That ended up
> in the report as a critical finding -- absence of wireless monitoring.

### 5.5 Probe Flood

Probe flood generates a massive number of probe requests to saturate APs
in the area.

**How it works:**

The ESP32 transmits probe requests with:
- Randomized source MAC addresses (simulates hundreds of clients)
- Variable or broadcast SSIDs
- Maximum transmission rate

**Effects:**

1. **AP saturation**: APs must process every probe request and respond
   with a probe response. A probe flood can:
   - Increase the AP's CPU load
   - Reduce performance for legitimate clients
   - In extreme cases, cause cheap APs to reboot

2. **Log pollution**: AP logs fill up with probes from fictitious MACs,
   making forensic analysis difficult

3. **Stress test**: verify the resilience of the wireless infrastructure under
   anomalous load

**Detectability:**

Probe flood is easily detectable by any WIDS because:
- Anomalous volume of probe requests
- Source MAC addresses without valid OUI (or with OUIs from nonexistent chips)
- Unnatural temporal pattern (probes every few milliseconds)

### 5.6 Evil Portal

Evil Portal is the most powerful social engineering tool via WiFi
in Marauder. It combines a rogue AP with a captive portal to intercept
credentials.

**How it works - Complete architecture:**

```
[Victim]                         [ESP32 Marauder]              [Internet]
    |                              |                            |
    |  1. Connects to fake AP      |                            |
    |----------------------------->|                            |
    |                              |                            |
    |  2. Any DNS request          |                            |
    |----------------------------->|                            |
    |                              |                            |
    |  3. DNS Spoofing: responds   |                            |
    |     with ESP32 IP            |                            |
    |<-----------------------------|                            |
    |                              |                            |
    |  4. HTTP Request to portal   |                            |
    |----------------------------->|                            |
    |                              |                            |
    |  5. Fake login page          |                            |
    |<-----------------------------|                            |
    |                              |                            |
    |  6. Victim enters creds      |                            |
    |----------------------------->|                            |
    |                              |                            |
    |  7. Credentials saved        |                            |
    |  on SD card                  |                            |
    |                              |                            |
```

**Step 1 - Rogue AP:**

The ESP32 creates an AP with an SSID chosen by the attacker. In a pentesting
context, you choose a name the victim expects to find:
- "Hotel_WiFi_Free" in a hotel
- "Airport_Free_WiFi" in an airport
- "CompanyName_Guest" in an office
- The EXACT name of the legitimate network (Evil Twin)

The AP is created without encryption (Open) to allow connection without
a password.

**Step 2/3 - DNS Spoofing:**

The ESP32 runs a DNS server that responds to ANY DNS query with its own
IP address. When the victim's device attempts to resolve any domain
(google.com, facebook.com, etc.), it receives the ESP32's IP.

This mechanism is the same one used by legitimate captive portals (hotels, airports):
the device detects that it has no real Internet connectivity and automatically
opens the captive portal browser.

On iOS and Android, captive portal detection occurs through:
- **iOS**: HTTP request to `captive.apple.com/hotspot-detect.html`
- **Android**: HTTP request to `connectivitycheck.gstatic.com/generate_204`
  or `clients3.google.com/generate_204`
- **Windows**: HTTP request to `www.msftconnecttest.com/connecttest.txt`

If the response does not match the expected one, the operating system
automatically displays the captive portal browser with the attacker's page.

**Step 4/5 - Phishing Page:**

The ESP32 serves an HTML/CSS web page that simulates a login page. Pages
can be customized and loaded onto the SD card.

Template examples:
- Google/Microsoft login (email credential harvesting)
- Hotel WiFi access page (personal data collection)
- Corporate portal login page
- Firmware update page (social engineering to install malware)

**Creating a custom template:**

The template is a standard HTML file. The ESP32 has limited resources, so:
- Keep the HTML/CSS simple (no heavy frameworks)
- Include CSS inline (do not load external stylesheets)
- Images must be base64-encoded inline or very small
- The form must POST to the ESP32's address

Basic template structure:

```html
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>WiFi Login</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: #f5f5f5;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            margin: 0;
        }
        .login-box {
            background: white;
            padding: 40px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            max-width: 400px;
            width: 90%;
        }
        input {
            width: 100%;
            padding: 12px;
            margin: 8px 0;
            border: 1px solid #ddd;
            border-radius: 4px;
            box-sizing: border-box;
        }
        button {
            width: 100%;
            padding: 12px;
            background: #4285f4;
            color: white;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 16px;
        }
    </style>
</head>
<body>
    <div class="login-box">
        <h2>WiFi Access</h2>
        <p>Enter your credentials to access the Internet</p>
        <form method="POST" action="/login">
            <input type="email" name="email" placeholder="Email" required>
            <input type="password" name="password" placeholder="Password" required>
            <button type="submit">Connect</button>
        </form>
    </div>
</body>
</html>
```

**Step 6/7 - Credential Harvesting:**

When the victim fills out the form and presses "Connect", the credentials are:
1. Received by the ESP32 via HTTP POST
2. Saved to a file on the Flipper's SD card
3. Optionally displayed on the Flipper's screen

The captured credentials file is typically at:
```
/ext/apps_data/marauder/portal_creds.txt
```

**Advanced Evil Portal considerations:**

1. **HTTPS**: the ESP32 cannot serve HTTPS with valid certificates. Modern
   browsers display security warnings. However, for captive portals,
   most users do not notice (or ignore) the absence of HTTPS
   because it is normal for WiFi login pages.

2. **HSTS**: if the victim has visited a site with HSTS (HTTP Strict Transport
   Security), the browser will refuse the HTTP connection. This limits
   effectiveness against users who frequently visit sites with HSTS.

3. **Duration**: the Evil Portal must remain active for the necessary time.
   The Flipper battery with the devboard connected lasts approximately 2-4 hours
   (depending on the load).

4. **Realism**: the template quality determines success. A template
   that faithfully replicates the WiFi portal of the location where you are operating
   (hotel, conference, office) has a much higher success rate.

> Personal note: Evil Portal is the tool that has produced the most
> impressive results in my engagements. In a test for a hotel, I created
> a portal that exactly replicated the hotel's WiFi login page
> (same colors, logo, font). In 4 hours I captured 23 sets of valid
> email credentials. The report highlighted how the absence of WPA2-Enterprise
> and the lack of guest education created a concrete risk.
> The hotel subsequently implemented WPA2-Enterprise with authentication
> via room number + surname.

### 5.7 PMKID Attack

As described in the theory section, the PMKID attack is the preferred method
for obtaining offline WPA2 cracking material without disturbing clients.

**Operational procedure with Marauder:**

1. Perform an AP scan: `scanap`
2. Identify the target (must be WPA2-Personal)
3. Select the target
4. Start PMKID capture: `sniffpmkid`
5. The ESP32 sends an association request to the AP
6. If the AP supports PMK caching, it responds with the PMKID in message 1
7. The PMKID is captured and saved to the SD card
8. Stop the capture: `stopscan`

**Result analysis:**

The captured PMKID is saved in a hashcat-compatible format.
The PMKID structure is:

```
PMKID*MAC_AP*MAC_CLIENT*SSID_HEX
```

Example:
```
2582a8281bf9d4308d6f5731d0e61c61*aabbccddeeff*112233445566*4f66666963654e6574
```

**Cracking with hashcat:**

```bash
# Conversion (if necessary)
hcxpcapngtool -o hash.hc22000 capture.pcap

# Dictionary crack
hashcat -m 22000 hash.hc22000 /usr/share/wordlists/rockyou.txt

# Crack with rules
hashcat -m 22000 hash.hc22000 wordlist.txt -r rules/best64.rule

# Crack with mask (brute force pattern)
hashcat -m 22000 hash.hc22000 -a 3 ?d?d?d?d?d?d?d?d  # 8 digits

# Crack status
hashcat -m 22000 hash.hc22000 --show
```

**Cracking performance (approximate estimates):**

| Hardware | Approximate Speed |
|----------|-------------------------|
| CPU (recent i7) | ~20,000 PMK/s |
| GPU NVIDIA RTX 3080 | ~800,000 PMK/s |
| GPU NVIDIA RTX 4090 | ~1,500,000 PMK/s |
| 4x RTX 4090 (rig) | ~6,000,000 PMK/s |

With these speeds:
- 8-digit password (10^8 = 100M combinations): ~67 seconds with RTX 4090
- 8-character lowercase password (26^8 = 208B): ~38 hours with RTX 4090
- 8-character mixed password (62^8 = 218T): ~4.5 years with RTX 4090
- 12-character mixed password: computationally impossible with current technology

**When PMKID does not work:**

- The AP does not support PMK caching (no PMKID in message 1)
- The AP uses WPA3-SAE (immune to the attack)
- The AP has PMF (802.11w) enabled with MFPR (Management Frame Protection Required)
- The AP rejects the association request (rate limiting or MAC filtering)

In these cases, move on to traditional handshake capture (section 5.8).

> Personal note: in my experience, approximately 60-70% of WPA2-Personal APs
> respond with the PMKID. The remaining 30-40% require the traditional method
> with deauth. I always start with PMKID because it is silent and fast. If after
> 30 seconds I get no result, I switch to plan B.

### 5.8 Handshake Capture (4-Way Handshake WPA2)

Traditional 4-way handshake capture is the classic method for obtaining
the material needed for offline WPA2 password cracking.

**Operational procedure with Marauder:**

The procedure requires combining two functions: EAPOL sniff + deauth.

1. Perform AP and client scan:
   ```
   scanap
   scansta
   ```

2. Identify the target:
   - AP with WPA2-Personal
   - At least one connected client (necessary -- without a client, no handshake)
   - Decent signal (RSSI > -75 dBm for both the AP and the client)

3. Note the target AP's channel and ensure the sniffer operates on the
   same channel

4. Start EAPOL sniffing:
   ```
   sniffeapol
   ```

5. Start the targeted deauth on the target AP (or better, on the specific client):
   ```
   attack -t deauth
   ```
   Select the AP or client from the list.

6. The deauth forces the client disconnection. The client reconnects
   automatically, generating a new 4-way handshake.

7. The EAPOL sniffer captures the 4 messages and saves them to the .pcap file.

8. Stop everything:
   ```
   stopscan
   ```

9. Extract the .pcap file from the Flipper's SD card.

**Capture verification:**

Not all captured handshakes are usable. To be valid, the .pcap must
contain at least messages 1 and 2 (ideally all 4):

```bash
# Verify with aircrack-ng
aircrack-ng capture.pcap
# Should show "1 handshake" for the target network

# Verify with Wireshark
# Filter: eapol
# 4 EAPOL frames should appear for the AP-Client pair

# Conversion for hashcat
hcxpcapngtool -o hash.hc22000 capture.pcap
# Should report "EAPOL pairs written"
```

**Common capture problems:**

| Problem | Cause | Solution |
|----------|-------|-----------|
| No handshake captured | Sniffer on wrong channel | Verify the AP channel and lock the sniffer to the same one |
| Incomplete handshake (only msg 1-2) | Client too far away | Move closer to the client, not the AP |
| Handshake not crackable | MIC corrupted by interference | Repeat the capture with better signal |
| Client does not reconnect | PMF enabled, deauth ignored | Try with a different client or wait for natural reconnection |
| Too many frames, confusion | Congested channel | Filter by specific BSSID in the analysis |

**Cracking the handshake:**

Identical to PMKID cracking (same hashcat mode -m 22000), since the
.hc22000 format is unified.

With aircrack-ng (alternative without GPU):

```bash
# Dictionary crack
aircrack-ng -w /usr/share/wordlists/rockyou.txt capture.pcap

# Crack with custom dictionary
aircrack-ng -w custom_wordlist.txt -b AA:BB:CC:DD:EE:FF capture.pcap
```

hashcat is superior to aircrack-ng for cracking because it supports GPU acceleration,
mutation rules, combination attacks, and masks.

> Personal note: handshake capture is an art that requires practice. The
> first few times it took me dozens of attempts to get a clean handshake.
> The critical factors: physical position (you must be within range of both the AP and the
> client), timing (the sniffer must be active BEFORE the deauth), and channel
> (must be correct). A common mistake is launching the deauth before the
> sniffer: handshake messages 1-2 occur within milliseconds after
> reconnection, and if the sniffer is not already listening you miss them.

### 5.9 Wardriving

Wardriving is the practice of physically moving through an area to map
the WiFi networks present. With the Flipper and Marauder it is possible to do
basic wardriving.

**How it works with Marauder:**

1. Connect a GPS module to the Flipper (if available) or use the smartphone's
   GPS via BLE
2. Start continuous scanning
3. Move through the target area (on foot, by car, by bicycle)
4. Results are saved with GPS coordinates

**Output format - WiGLE CSV:**

Data is saved in CSV format compatible with WiGLE (Wireless Geographic
Logging Engine), the worldwide WiFi network database:

```csv
MAC,SSID,AuthMode,FirstSeen,Channel,RSSI,CurrentLatitude,CurrentLongitude,AltitudeMeters,AccuracyMeters,Type
AA:BB:CC:DD:EE:FF,OfficeNet,WPA2,2024-01-15 10:30:22,6,-42,41.9028,12.4964,50,10,WIFI
```

Fields:
- MAC: AP BSSID
- SSID: network name
- AuthMode: encryption type
- FirstSeen: timestamp of first detection
- Channel: channel
- RSSI: signal strength
- CurrentLatitude/Longitude: GPS coordinates
- Type: WIFI (for WiFi networks)

**Upload to WiGLE:**

CSV files can be uploaded to https://wigle.net to contribute to the
global database or for map analysis.

**Applications in penetration testing:**

1. **Perimeter reconnaissance**: map all WiFi networks of a corporate campus,
   identifying:
   - Corporate networks
   - Guest networks
   - IoT networks
   - Rogue networks (unauthorized APs installed by employees)
   - Perimeter weak points (networks with signal that "leaks" outside the building)

2. **Coverage analysis**: determine from where it is possible to reach
   the target networks. If the corporate network signal is strong in the
   external parking lot, an attacker can comfortably operate from their car.

3. **Historical comparison**: repeat wardriving over time to identify
   changes in the wireless infrastructure.

**Wardriving limitations with the Flipper:**

- No built-in GPS (requires external module)
- Limited ESP32 antenna (misses networks with weak signal that a laptop
  with an external antenna would detect)
- Small screen, difficult to review results in the field
- Limited autonomy from battery

For professional wardriving, tools like Kismet on a laptop with USB GPS
and an external antenna remain superior. The Flipper is useful for quick
and discreet reconnaissance.

> Personal note: I use wardriving with the Flipper only for the initial
> "walk-by" reconnaissance of a target building. I walk around the perimeter
> with the Flipper in my pocket and in 15 minutes I have the map of networks visible
> from outside. For serious wardriving (entire city, industrial area),
> I use a Raspberry Pi 4 with Kismet, USB GPS, and a 9 dBi Alfa antenna mounted
> in the car. The Flipper cannot compete in that context.

---
