# WiFi Attacks and Countermeasures - WiFi Marauder

Overview of WiFi attack vectors executable with ESP32 Marauder via Flipper Zero, along with their respective countermeasures.

---

## Deauthentication Attack

### Principle
Transmission of spoofed 802.11 deauthentication frames to disconnect clients from an AP. Exploits the fact that 802.11 management frames are not authenticated in the original protocol.

### Impact
- DoS: disconnection of all clients from the target AP
- Enabler for other attacks: forces the client to reconnect → handshake capture
- Disruption: renders a WiFi network unusable

### Countermeasures
- **802.11w (PMF - Protected Management Frames):** authenticates management frames with MIC. Prevents spoofing. Mandatory in WPA3, optional in WPA2
- **Client isolation:** limits the damage of a deauth on individual clients
- **WIDS (Wireless Intrusion Detection System):** detects massive deauth and generates alerts
- **WPA3:** includes mandatory PMF → deauth does not work

---

## Evil Portal

### Principle
Creation of a fake captive portal (evil twin + phishing) to capture credentials. The ESP32 creates an AP with an SSID identical to the target, the client connects and is redirected to a fake login page.

### Impact
- Credential harvesting: WiFi username/password, corporate credentials
- Session hijacking: interception of post-login traffic
- Malware delivery: page serving a payload

### Countermeasures
- **HSTS (HTTP Strict Transport Security):** prevents downgrade to HTTP
- **Certificate pinning:** the browser rejects invalid certificates
- **Mandatory VPN:** traffic is encrypted end-to-end
- **User awareness:** do not enter credentials in suspicious captive portals
- **802.1X/EAP-TLS:** certificate-based authentication, not password-based

---

## PMKID Capture

### Principle
Capture of the PMKID from the first part of the 4-Way Handshake (EAPOL M1). Does not require a connected client - a single frame from the AP is sufficient. The PMKID is derived from the PMK and can be attacked offline with hashcat.

### Impact
- Recovery of the WPA2 password if weak (offline brute force)
- Does not require active clients - works on APs without clients
- More efficient than traditional handshake capture

### Countermeasures
- **Strong WPA2 password** (>12 characters, mixed, not from a dictionary)
- **WPA3-SAE:** uses Dragonfly key exchange, resistant to offline brute force
- **Password rotation:** change the password periodically
- **Disable PMKID caching** on the AP (vendor-specific option)

---

## Handshake Capture (4-Way WPA2)

### Principle
Capture of the 4 EAPOL frames exchanged during WPA2 authentication. Requires a client to connect (or be forced to via deauth). The captured handshake is cracked offline.

### Impact
- Identical to PMKID: offline WPA2 password recovery
- Requires an active client or deauth to force reconnection

### Countermeasures
- Same as PMKID + **deauth monitoring** (WIDS)

---

## Beacon Spam / Probe Flood

### Principle
- **Beacon Spam:** generation of hundreds of fake SSIDs that flood the WiFi list on client devices
- **Probe Flood:** massive transmission of Probe Requests to overload APs

### Impact
- Confusion: the user cannot find the real network among hundreds of fake SSIDs
- DoS: slowdown of APs that must process the requests
- Distraction: used as cover for other attacks

### Countermeasures
- **WIDS:** detects anomalous beacons and probe flood
- **Client configuration:** automatic connection only to known networks
- **Ignore unknown SSIDs:** corporate policy

---

## Wardriving

### Principle
Systematic scanning of WiFi networks in a geographical area, collecting SSID, BSSID, security type, signal strength, and GPS coordinates.

### Impact
- Complete mapping of a target's WiFi infrastructure
- Identification of networks with weak security (WEP, WPA-TKIP, open)
- Input for targeted attacks

### Countermeasures
- **Hiding SSID:** ineffective (the SSID is still present in Probe Responses)
- **WPA2/WPA3:** strong security makes wardriving purely reconnaissance
- **Segmentation:** guest networks separated from corporate networks
- **Perimeter WIDS:** detection of external scanning

---

## Attack Matrix - Quick Reference

| Attack | Complexity | Marauder Tool | Impact | Key Countermeasure |
|---------|-------------|---------------|---------|-------------------|
| Deauth | Low | deauth | DoS + enabler | 802.11w/PMF |
| Evil Portal | Medium | evilportal | Credential theft | HSTS + awareness |
| PMKID | Low | sniffpmkid | Password recovery | WPA3/strong password |
| Handshake | Medium | sniffraw | Password recovery | WPA3/strong password |
| Beacon Spam | Low | beaconspam | Confusion | WIDS |
| Probe Flood | Low | probeflood | AP DoS | WIDS |
| Wardriving | Low | wardrive | Reconnaissance | Strong WPA2/WPA3 |
