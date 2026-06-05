# ESP8266 - Advanced Operational Guide

Compact and affordable WiFi modules for wireless attacks, IoT automation, and experimentation. The ESP8266 is the most economical alternative to the ESP32 for specific WiFi operations, particularly deauthentication attacks.

---

## Technical Fundamentals

The ESP8266 is a 2.4 GHz single-band WiFi SoC with a Tensilica L106 processor at 80/160 MHz. Unlike the ESP32, it has a single core, no BLE support, and slightly lower TX power. However, for deauth attacks and WiFi scanning, performance is equivalent at a much lower cost (~2 euros vs ~8 euros).

**Connection to the Flipper Zero:**
```
Flipper GPIO    ESP8266
3V3          -> VCC (WARNING: 3.3V, NEVER 5V!)
GND          -> GND
PB7 (RX)     -> TX
PB6 (TX)     -> RX
```

> **Personal note:** The ESP8266 was the first module I bought for the Flipper. It costs next to nothing, solders in 5 minutes, and immediately gives you offensive WiFi capabilities. For those starting with wireless pentesting, it's the ideal starting point before investing in a full ESP32.

---

## Deauther

### How the Deauthentication Attack Works

The deauth attack exploits a fundamental weakness in the 802.11 protocol: **management frames** (specifically deauthentication and disassociation frames) are not authenticated in standard WPA2. This means anyone can send a deauthentication frame with the AP's spoofed source MAC address, and the client will disconnect.

**Deauth frame structure:**
```
[Frame Control: 0x00C0] [Duration] [DA: client MAC] [SA: AP MAC] [BSSID: AP MAC] [Seq] [Reason Code: 0x0007]
```

**Common reason codes:**
- 0x01: Unspecified reason
- 0x04: Disassociated due to inactivity
- 0x05: Disassociated because AP is unable to handle all currently associated STAs
- 0x07: Class 3 frame received from nonassociated STA (the most commonly used)

**Operational procedure:**

1. Flash the Deauther firmware onto the ESP8266 (via web flasher or esptool)
2. Connect to the Flipper via UART
3. Open the Deauther app on the Flipper
4. **Scan:** the ESP scans all surrounding 2.4 GHz networks
5. Identify the target AP and connected clients
6. **Select target:** select specific AP and/or clients
7. **Start Deauth:** the ESP sends continuous deauthentication frames
8. Target clients are disconnected repeatedly

**Advanced configuration:**
- **Channel:** lock to a specific channel or scan all
- **Target:** single AP, single client, or broadcast
- **Packet rate:** number of deauth frames per second (default ~10-50)
- **Reason code:** selectable for compatibility testing

### Deauther V2

Evolution with improved web interface:
- HTML dashboard accessible by connecting to the ESP's WiFi
- Live list of APs and clients with RSSI
- Simultaneous multi-target
- Detailed logging
- Saveable profiles

**Usage in pentesting:**
- Force client reconnection to capture the WPA2 handshake (with ESP32 Marauder or airodump-ng)
- Network resilience testing: do clients handle reconnection correctly?
- Awareness demos: show how easy it is to disconnect WiFi devices
- IoT device stress testing: how do they react to repeated disconnections?

> **Personal note:** Deauth is the simplest and highest-impact WiFi attack during demos. Disconnecting all devices in a meeting room in 3 seconds makes a big impression. But WARNING: deauth on unauthorized networks is illegal. Additionally, 802.11w (Management Frame Protection) blocks deauth on networks that support it -- modern WiFi 6 routers often have it enabled.

---

## WiFi Scanner

Passive scanner for 2.4 GHz WiFi networks.

**Data collected for each AP:**
- **SSID:** network name (or "Hidden" if hidden)
- **BSSID:** AP MAC address
- **Channel:** WiFi channel (1-13 in EU)
- **RSSI:** signal strength (dBm) -- closer to 0 = stronger
- **Encryption:** Open, WEP, WPA, WPA2, WPA3
- **Client count:** estimated number of connected clients

**Operational procedure:**

1. Launch WiFi Scanner
2. The ESP scans all channels
3. Network list sorted by RSSI
4. Select an AP to see details and clients

**Usage in pentesting:**
- Reconnaissance phase: map all networks in the target building
- Identify networks with weak security (WEP, Open)
- Find hidden networks (hidden SSID -- detectable from probe responses)
- Estimate the number of connected devices
- Identify congested channels for wardriving

> **Personal note:** The ESP8266 WiFi Scanner is limited to 2.4 GHz. For complete reconnaissance you also need 5 GHz (which requires an ESP32 or a WiFi adapter with 5GHz and monitor mode support). In real engagements, I use the ESP8266 for the initial quick scan and then complete with airodump-ng on a laptop for the full picture.

---

## IFTTT Button

Transforms the Flipper + ESP8266 into an IoT trigger via IFTTT Webhooks.

**How it works:**
1. The ESP connects to a known WiFi network
2. On trigger (button press on the Flipper), it sends an HTTP GET/POST request to IFTTT Webhooks
3. IFTTT executes the configured automation

**Configuration:**
- WiFi network SSID and password
- IFTTT Webhook key (from the IFTTT dashboard)
- Event name (e.g., "flipper_trigger")
- Optional data (value1, value2, value3)

**Creative usage in pentesting:**
- Automatic trigger of notifications when an event occurs
- Activation of remote scripts from the target location
- Integration with lightweight C2 systems
- Real-time activity logging to Google Sheets

---

## Legal Aspects

- Deauthentication on unauthorized WiFi networks is illegal in Italy (D.Lgs. 259/2003, interference with communications)
- Passive scanning (WiFi Scanner) is generally legal -- you don't transmit anything, you only listen
- Use of IFTTT/automation on your own networks is legal

---

## Personal Experience

> **Personal note -- ESP8266 vs ESP32:** For those on a limited budget, the ESP8266 with Deauther firmware is the best investment. It costs 2 euros, connects in 2 minutes, and gives you deauth -- the most used WiFi attack in pentesting. The ESP32 with Marauder is superior in every way but costs 4x as much. My advice: start with the ESP8266 to learn the basics, then migrate to ESP32 for full functionality.

> **Personal note -- 802.11w:** More and more networks support Management Frame Protection (802.11w/PMF). On these networks, deauth doesn't work because management frames are authenticated. WiFi 6 (802.11ax) includes it by default. This means the deauth attack is becoming less effective on modern hardware -- but the majority of enterprise networks still use hardware without PMF.
