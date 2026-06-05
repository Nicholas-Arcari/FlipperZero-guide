## 4. Camera Tools

### 4.1 Camera

**What it does at a technical level**

Camera is the basic tool for video streaming from the ESP32-CAM to the Flipper Zero. The ESP32-CAM captures frames from the OV2640/OV3660 camera, compresses them in JPEG format, and transmits them via UART to the Flipper, which decompresses and displays them on its 128x64 pixel monochrome display.

At a technical level, the flow is:
1. The camera sensor captures a RAW frame (YUV or RGB).
2. The ESP32's image processor compresses the frame to JPEG.
3. The JPEG is resized to the Flipper display resolution.
4. The data is transmitted via UART to the Flipper.
5. The Flipper decompresses and converts to 1-bit (black/white with dithering) for the display.

Latency depends on the resolution, JPEG quality, and UART speed. In "Low Latency" mode (reduced resolution, low JPEG quality, UART at 921600 baud) you get about 5-10 fps. In high quality mode (full resolution, high JPEG quality) the frame rate drops to 1-2 fps.

**Complete step-by-step procedure**

1. Hardware: ESP32-CAM with OV2640 or OV3660 sensor.
2. Flash the Camera firmware onto the ESP32-CAM:
   - Connect a UART-USB converter (e.g., FTDI, CP2102) to the ESP32-CAM.
   - GPIO0 to GND to enter boot mode.
   - Flash the firmware.
   - Remove the GPIO0-GND connection.
3. Connect the ESP32-CAM to the Flipper via GPIO:
   - TX/RX as standard
   - Power: preferably external (powerbank) for stability
4. On the Flipper: Applications > GPIO > Camera.
5. Streaming starts automatically.
6. Available controls:
   - Take photo (saves JPEG to Flipper SD)
   - Adjust image parameters
   - Change resolution
   - Enable/disable flash LED
   - Mirror mode

**Configurable parameters:**

Image:
- Resolution: QQVGA (160x120), QVGA (320x240), VGA (640x480), SVGA (800x600), XGA (1024x768)
- JPEG quality: 10-63 (10 = maximum quality, 63 = maximum compression)
- Brightness: -2 to +2
- Contrast: -2 to +2
- Saturation: -2 to +2
- Gain: auto or manual (0-30)
- Exposure: auto (AE) or manual
- White balance: auto (AWB) or manual
- Special effects: none, negative, grayscale, sepia

Streaming:
- Mode: continuous MJPEG or single JPEG (snapshot)
- UART baud rate: 115200, 230400, 460800, 921600
- Dithering: Floyd-Steinberg, ordered, or none

**Real-world pentest usage example:**

Physical reconnaissance during an assessment:
1. Mount the ESP32-CAM in a discreet enclosure.
2. Connect to the Flipper in your pocket.
3. Use streaming to visually verify areas without exposing yourself (e.g., check if a server room is occupied, read exposed badges, verify camera placement).
4. Take photos of racks, cabling, labels with sensitive information.

### 4.2 Camera Suite

**What it does at a technical level**

Camera Suite is an advanced application that extends the base Camera features with professional tools: time-lapse, optimized night vision, anti-noise filters, and full sensor control. Compared to the base Camera tool, it offers granular control over every OV2640/OV3660 sensor parameter.

Night vision optimization works by increasing sensor gain, extending exposure time, and activating the IR LED built into the ESP32-CAM. The anti-noise filter applies digital noise reduction algorithms (averaging between successive frames) to compensate for the high gain required in low-light conditions.

**Complete step-by-step procedure**

1. Flash the Camera Suite firmware onto the ESP32-CAM.
2. Connect to the Flipper (same wiring as the Camera tool).
3. On the Flipper: Applications > GPIO > Camera Suite.
4. Main menu:
   - Live View: real-time streaming with advanced controls
   - Time-lapse: automatic capture at intervals
   - Night Vision: mode optimized for low light
   - Photo: single high-resolution shot
   - Settings: all sensor parameters

**Time-lapse mode:**
- Set interval between shots (1 second - 24 hours)
- Set total number of shots or total duration
- Select resolution (higher = more detail but more SD space)
- Start capture
- Photos are saved to the microSD with sequential numbering
- Once complete, photos can be assembled into video on PC

**Night Vision mode:**
- Automatic IR LED activation (if present)
- Sensor gain at maximum
- Extended exposure time
- Active anti-noise filter (moving average over N frames)
- Post-processing sharpening to compensate for high-gain blur

**Configurable parameters:**
- All base Camera tool parameters
- Time-lapse interval (1s - 86400s)
- Time-lapse frame count
- IR LED intensity (0-255 PWM)
- Frame averaging (1-8 frames for noise reduction)
- Sharpening (off, low, medium, high)
- Save format (JPEG, BMP)
- File name prefix

**Real-world usage example:**

Time-lapse surveillance of an area:
1. Position the ESP32-CAM with a view of the area of interest.
2. Configure time-lapse: 1 shot every 30 seconds for 8 hours.
3. Power from a large powerbank (10000+ mAh).
4. Upon completion, analyze the 960 photos to reconstruct movements in the area.

### 4.3 Motion Detection

**What it does at a technical level**

Motion Detection uses the ESP32-CAM camera to detect movements in the frame through differential comparison between successive frames. The algorithm works as follows:

1. Capture reference frame (background).
2. Capture current frame.
3. Calculate pixel-by-pixel difference between the two frames (in grayscale).
4. If the difference exceeds a configurable threshold over a sufficiently large area, "motion" is declared.
5. A photo is taken and an event is generated (notification on the Flipper, log to SD).
6. The reference frame is periodically updated to adapt to gradual lighting changes.

It is not an AI-based or object recognition system -- it is purely based on inter-frame difference. This means it can generate false positives from lighting changes, shadows, animals, etc. Sensitivity must be carefully calibrated.

**Complete step-by-step procedure**

1. Flash the Motion Detection firmware onto the ESP32-CAM.
2. Connect to the Flipper.
3. On the Flipper: Applications > GPIO > Motion Detection.
4. Position the camera with a stable view (essential to reduce false positives -- even minimal vibration causes triggers).
5. Configure sensitivity:
   - Pixel difference threshold (0-255, default 30)
   - Minimum percentage of changed pixels (default 5%)
   - Region of Interest (ROI) if supported
6. Start monitoring.
7. The display shows:
   - Status: "Monitoring..." or "MOTION DETECTED"
   - Event counter
   - Last event: timestamp and photo
8. Each event is logged with timestamp and photo to the microSD.

**Configurable parameters:**
- Pixel difference threshold (0-255)
- Minimum area change percentage (1-100%)
- Background update interval (seconds)
- Cooldown between events (avoid repeated triggers for the same motion)
- Capture resolution
- Saving: log only, log + photo, log + photo + notification
- ROI (Region of Interest): limit detection to a zone within the frame

**Real-world pentest usage example:**

Physical access monitoring during an assessment:
1. Position the ESP32-CAM with a view of the server room door.
2. Medium sensitivity to avoid false positives but detect people.
3. Monitor for the entire test duration.
4. Access log: who enters, when, frequency.
5. Useful for assessing physical security and access control.

### 4.4 Nanny Cam

**What it does at a technical level**

Nanny Cam turns the ESP32-CAM into a continuous remote surveillance system, optimized for prolonged monitoring. Unlike the Camera tool which is designed for interactive use, Nanny Cam is designed to operate autonomously for extended periods with minimal interaction.

The system supports:
- Low-power continuous streaming (reduced resolution, low frame rate)
- IR LED for night vision (if the ESP32-CAM module has an IR LED)
- Optional audio (requires I2S microphone connected to the ESP32)
- Automatic recording to the ESP32-CAM's microSD
- Automatic day/night detection for IR switching

**Complete step-by-step procedure**

1. Hardware: ESP32-CAM with IR LED (AI-Thinker models with built-in IR are ideal).
2. Flash the Nanny Cam firmware.
3. Connect to the Flipper.
4. On the Flipper: Applications > GPIO > Nanny Cam.
5. Initial configuration:
   - Resolution: low for continuous streaming, high for recording
   - IR mode: auto (light sensor), manual on, manual off
   - Recording: continuous, motion-only, scheduled
   - Audio: on/off (if hardware supported)
6. Start monitoring.
7. The Flipper shows the live stream and system status.
8. Recordings are saved to the ESP32-CAM's microSD.

**Configurable parameters:**
- Streaming vs recording resolution (can be different)
- Frame rate (1-25 fps)
- IR mode: auto, on, off
- Light sensor threshold for automatic IR switch
- Recording: continuous, on motion, scheduled (times)
- Maximum recording file duration (automatic segmentation)
- JPEG compression (quality)
- Audio: on/off, microphone gain

**Real-world usage example:**

Monitoring during a physical security test:
1. Install the ESP32-CAM in a discreet position with a view of the target area.
2. Power from wall outlet (for prolonged operation).
3. Mode: motion-triggered recording + auto IR.
4. After 24-48 hours, retrieve the microSD and analyze recordings.
5. Document access patterns, schedules, personnel.

### 4.5 QR Code

**What it does at a technical level**

QR Code uses the ESP32-CAM camera to acquire images and decode QR codes and other two-dimensional codes. The ESP32 performs decoding internally using a QR recognition library (typically based on quirc or ZBar ported for ESP-IDF).

The technical process:
1. Frame capture from the camera at QVGA or VGA resolution.
2. Grayscale conversion.
3. QR finder pattern detection (the three squares in the corners).
4. Data matrix decoding.
5. Content interpretation based on type: URL, text, WiFi (SSID+password), vCard, geolocation, email.
6. Result transmission to the Flipper via UART.

Autofocus is digital (software-based) since the OV2640 has a fixed-focus lens: the algorithm varies exposure and contrast parameters to optimize QR readability.

**Complete step-by-step procedure**

1. Connect ESP32-CAM to the Flipper.
2. On the Flipper: Applications > GPIO > QR Code.
3. Point the camera at the QR code.
4. Hold the QR in the frame at about 10-20cm distance.
5. Decoding happens automatically when the QR is recognized.
6. The Flipper shows the decoded content:
   - URL: shows the URL with open option (via Postman/Web Crawler)
   - WiFi: shows SSID, password, and authentication type
   - Text: shows the full text
   - vCard: shows the contact
7. Option to save content to the microSD.

**Configurable parameters:**
- Capture resolution (higher = smaller QRs readable)
- Autofocus mode: continuous or single
- Flash LED: auto (in low-light conditions), on, off
- Result save format
- Automatic post-decode action (e.g., open URL, connect WiFi)

**Real-world pentest usage example:**

Analyzing exposed QR codes in a target environment:
1. QR codes are everywhere: badges, posters, stickers, screens.
2. Scan all visible QR codes in the target area.
3. Verify where they point: they often contain internal URLs, WiFi credentials, links to internal systems.
4. Document: "QR code in the main hall contains guest WiFi credentials in cleartext".
5. Recommendation: do not expose credentials via QR codes in publicly accessible areas.

> Personal note: QR codes are an underestimated goldmine in physical pentesting. I have found QR codes in meeting rooms containing corporate (not guest) WiFi credentials, links to internal portals with pre-authenticated sessions, and even building automation system credentials. Always scan all visible QR codes during a physical assessment.

---

## 5. Network Tools

### 5.1 FlipWiFi

**What it does at a technical level**

FlipWiFi is a complete WiFi manager that allows the Flipper Zero to connect to WiFi networks through the ESP32 and perform network operations. The ESP32 acts as a WiFi modem, establishing the connection and providing the Flipper with network access through UART communication.

Implemented network features:
- Detailed AP scan with all parameters (SSID, BSSID, channel, RSSI, encryption, vendor from MAC OUI)
- Connection to open, WPA2-PSK, WPA3-SAE networks (if firmware supports)
- Saved WiFi profile management (SSID + password)
- Connectivity tests: ICMP ping, traceroute, DNS resolution
- Connection information: local IP, gateway, DNS, subnet mask
- Connection speed and signal quality in real time

**Complete step-by-step procedure**

1. Connect ESP32 to the Flipper via GPIO.
2. On the Flipper: Applications > GPIO > FlipWiFi.
3. Main menu:
   - Scan Networks: available network scan
   - Saved Networks: quick connection to saved networks
   - Connect: manual connection (SSID + password)
   - Tools: ping, traceroute, DNS lookup
   - Status: current connection information
4. To connect:
   - Scan -> select network -> enter password -> Connect.
   - Or: Saved Networks -> select profile -> Connect.
5. Once connected, other network tools (Postman, Web Crawler, FlipDownloader) can operate.

**Configurable parameters:**
- Connection timeout
- Custom DNS (default: 8.8.8.8)
- Static IP vs DHCP
- Saved WiFi profiles (max depends on memory)
- Ping interval for connectivity tests
- Maximum hop count for traceroute

**Real-world pentest usage example:**

Network segmentation verification:
1. Connect to the guest network with FlipWiFi.
2. Execute ping toward hosts on the corporate network.
3. If reachable -> insufficient network segmentation.
4. Traceroute to identify the path and intermediate network devices.
5. DNS lookup to resolve internal names from the guest network.

### 5.2 FlipMap

**What it does at a technical level**

FlipMap is a WiFi network mapping tool that focuses on detailed cataloging of detected access points with complete technical information. Unlike WiFi Mapping (which creates coverage heatmaps), FlipMap creates a structured network catalog with advanced metadata.

The ESP32 scans networks and for each AP detects:
- SSID and BSSID (MAC address)
- Channel and bandwidth
- RSSI (signal strength)
- Encryption type and details (WPA2-PSK, WPA2-Enterprise, WPA3, etc.)
- AP vendor (from MAC OUI prefix)
- Beacon interval
- 802.11 feature support (WMM, HT, VHT)
- Number of associated clients (if detectable)

**Complete step-by-step procedure**

1. Connect ESP32 to the Flipper.
2. On the Flipper: Applications > GPIO > FlipMap.
3. Start the scan.
4. Results are shown in a sortable list by:
   - RSSI (strongest signal first)
   - Channel
   - Encryption
   - Vendor
5. For each AP, select to see full details.
6. Export the network map in CSV/JSON format.

**Configurable parameters:**
- Scan duration per cycle
- Channels to scan
- Result sorting
- Filters (by RSSI, encryption, vendor)
- Export format
- Continuous update or single snapshot

**Real-world pentest usage example:**

Organization wireless inventory:
1. Complete scan with FlipMap from multiple positions in the building.
2. Identify all APs: corporate, guest, rogue (unauthorized).
3. Verify encryption: APs with WEP or Open are critical.
4. Identify APs from vendors different from the corporate one (potential rogue APs).
5. Report: complete inventory with recommendations for each anomaly found.

### 5.3 FlipRPI

**What it does at a technical level**

FlipRPI enables remote control of a Raspberry Pi through the ESP32's WiFi connection. The ESP32 connects to the local network, establishes a connection with the Raspberry Pi (typically via HTTP API or tunneled SSH commands) and transmits commands from the Flipper.

The architecture is:
- Flipper Zero -> UART -> ESP32 -> WiFi -> Local network -> Raspberry Pi
- Commands are sent as HTTP requests to an API server running on the Pi
- Responses are transmitted back to the Flipper for display

Main features:
- Sending preconfigured commands (reboot, shutdown, update)
- Resource monitoring: CPU, RAM, temperature, disk space
- Custom script execution
- Reading files from predefined directories
- Service management (start/stop)

**Complete step-by-step procedure**

1. On the Raspberry Pi:
   - Install the companion API server (Python/Node script)
   - Configure authentication (API token)
   - Start the service
2. On the ESP32:
   - Flash firmware with FlipRPI support
   - Configure WiFi network (SSID + password)
   - Configure the Raspberry Pi IP and API token
3. On the Flipper: Applications > GPIO > FlipRPI.
4. Main menu:
   - Status: shows Pi CPU/RAM/temp
   - Commands: preconfigured command list
   - Custom: custom command input
   - Files: known directory browser
   - Services: service management

**Configurable parameters:**
- Raspberry Pi IP/hostname
- API server port
- Authentication token
- Preconfigured command list
- Accessible directories for the file browser
- Status polling interval
- Connection timeout

**Real-world pentest usage example:**

Drop box management:
1. The Raspberry Pi is configured as a drop box (hidden device in the target network).
2. FlipRPI allows controlling it from the Flipper without a laptop.
3. Typical commands: start nmap scan, check results, download files, restart services.
4. Useful when physical access is limited and you need to quickly control the drop box.

### 5.4 Postman

**What it does at a technical level**

Postman is an integrated HTTP/HTTPS client that allows sending API requests directly from the Flipper through the ESP32. The ESP32 handles the WiFi connection, the TCP/IP stack, the TLS handshake (for HTTPS), and the sending/receiving of HTTP requests. Results are transmitted to the Flipper via UART.

Supported HTTP methods:
- GET: resource request
- POST: data submission (JSON body, form-encoded)
- PUT: resource update
- DELETE: resource deletion

The main limitation is ESP32 memory: very large responses (> 50-100KB) can cause issues. Responses are truncated if they exceed capacity.

**Complete step-by-step procedure**

1. Connect the ESP32 to a WiFi network (via FlipWiFi or firmware configuration).
2. On the Flipper: Applications > GPIO > Postman.
3. Configure the request:
   - Method: GET, POST, PUT, DELETE
   - URL: complete endpoint (http:// or https://)
   - Headers: key-value (e.g., Authorization: Bearer token)
   - Body: JSON text or form-encoded (for POST/PUT)
4. Send the request.
5. View the response:
   - Status code (200, 404, 500, etc.)
   - Response headers
   - Body (parsed JSON or raw text)
6. Save the request for future use.
7. Save the response to the microSD.

**Configurable parameters:**
- HTTP method
- URL
- Headers (multiple)
- Body (JSON, form-encoded, raw text)
- Request timeout (seconds)
- Follow redirect (on/off)
- SSL certificate verification (on/off -- disable for self-signed)
- Saved requests (library)

**Real-world pentest usage example:**

Testing exposed APIs:
1. During an assessment, an exposed API endpoint is discovered.
2. With Postman, quickly test the endpoint without a laptop.
3. GET /api/users -> verify if it returns data without authentication.
4. POST /api/login with test credentials.
5. PUT /api/users/1 -> unauthorized data modification attempt.
6. Document responses for the report.

> Personal note: Postman on the Flipper is limited but surprisingly useful for quick tests. I use it when I can't pull out the laptop -- for example during physical walkthroughs when I find a web admin panel and want to do a quick test. The main limitation is input: typing URLs and JSON on the Flipper's virtual keyboard is tedious. Prepare requests as saved templates before the assessment.

### 5.5 Web Crawler

**What it does at a technical level**

Web Crawler is a mini web spider that downloads HTML pages and extracts information. The ESP32 makes HTTP/HTTPS requests, downloads the HTML content, performs basic parsing to extract links, text, metadata, and optionally follows found links up to a configurable depth.

The technical process:
1. HTTP GET request to the initial URL.
2. HTML content download (truncated if it exceeds the memory limit).
3. HTML parsing: extraction of `<a href>`, `<meta>`, `<title>`, `<img>` tags, visible text.
4. If configured for link following: addition of found URLs to the queue.
5. Process repetition for each URL in the queue (up to the depth limit).
6. Result collection: URL list, extracted text, metadata.
7. Result transmission to the Flipper and/or saving to microSD.

Limitations are significant: no JavaScript support (so no SPAs), limited memory (large pages are truncated), no cookie/advanced session support, speed limited by the UART connection.

**Complete step-by-step procedure**

1. Connect the ESP32 to a WiFi network.
2. On the Flipper: Applications > GPIO > Web Crawler.
3. Enter the starting URL.
4. Configure:
   - Crawling depth (0 = page only, 1 = page + direct links, etc.)
   - Page download limit
   - URL filter (stay on same domain, or follow external links)
   - Content to extract (text, links, meta, all)
5. Start crawling.
6. The display shows progress: pages downloaded, links found, errors.
7. Upon completion, view results or export to SD.

**Configurable parameters:**
- Starting URL
- Crawling depth (0-5, beyond becomes too slow/heavy)
- Maximum number of pages
- Domain filter (same-domain, any)
- Content type to extract
- Per-page timeout
- Custom User-Agent
- Follow redirect

**Real-world pentest usage example:**

Internal web application reconnaissance:
1. Connect the ESP32 to the target network.
2. Crawl the corporate intranet site.
3. Extract: page structure, links to internal systems, metadata (software versions, HTML comments).
4. Identify login pages, admin panels, exposed files.
5. Results feed into the more detailed enumeration phase.

### 5.6 FlipDownloader

**What it does at a technical level**

FlipDownloader is a download manager that uses the ESP32 to download files from the Internet and save them to the Flipper's microSD. The ESP32 handles the HTTP/HTTPS connection, the file download, and transmission to the Flipper via UART for SD storage.

Technical features:
- HTTP and HTTPS download
- Redirect support (follow 301/302)
- Interrupted download resume (if the server supports Range header)
- Downloaded file hash verification (MD5, SHA256)
- Progress bar with speed and estimated time
- Remote file browser (HTTP directory listing)

Maximum download speed is limited by UART (at 921600 baud, about 90KB/s theoretical) and ESP32 memory (limited download buffer).

**Complete step-by-step procedure**

1. Connect the ESP32 to a WiFi network.
2. On the Flipper: Applications > GPIO > FlipDownloader.
3. Options:
   - Download URL: enter direct file URL
   - Browse: navigate HTTP directory listing (if available)
   - Resume: continue interrupted download
4. For download:
   - Enter the file URL.
   - Select the destination folder on the microSD.
   - Optional: enter expected hash for verification.
   - Start download.
5. Progress bar shows: percentage, speed, remaining time.
6. Upon completion, hash verification (if configured) and notification.

**Configurable parameters:**
- Download URL
- SD destination folder
- Expected hash (MD5/SHA256) for integrity verification
- Connection timeout
- Number of retry attempts on error
- SSL certificate verification

**Real-world pentest usage example:**

Field tool update:
1. During a prolonged assessment, an updated ESP32 firmware or new Evil Portal file is needed.
2. Connect the ESP32 to an available network (phone hotspot).
3. Download the file directly to the Flipper's SD.
4. Flash the new firmware or load the new file without returning to the PC.

---

## 6. BLE Tools

### 6.1 BLE Killer

**What it does at a technical level**

BLE Killer is a Bluetooth Low Energy auditing suite. The ESP32 operates as a BLE scanner and protocol analyzer, allowing discovery of devices, enumeration of services and characteristics, and testing the security of BLE connections in the area.

At a technical level, BLE operates on three layers:
- GAP (Generic Access Profile): manages discovery and connection. BLE Killer scans advertising packets to detect devices.
- GATT (Generic Attribute Profile): defines the structure of exposed services. BLE Killer enumerates services, characteristics, and descriptors.
- L2CAP (Logical Link Control and Adaptation Protocol): handles data transport. BLE Killer can test L2CAP layer robustness.

BLE advertising packets contain valuable information:
- Device MAC address (often randomized but not always)
- Device name (if broadcast)
- UUID of exposed services
- Manufacturer-specific data (often contains sensitive information)
- TX power level (for distance estimation)
- Connectability flags

**Complete step-by-step procedure**

1. Flash firmware with BLE Killer support onto the ESP32-WROOM (requires a module with Bluetooth, does not work on ESP32-S2).
2. Connect the ESP32 to the Flipper via GPIO.
3. On the Flipper: Applications > GPIO > BLE Killer.
4. Main menu:
   - Scan: BLE device scan
   - Inspect: selected device details
   - Services: GATT service enumeration
   - Monitor: continuous advertising monitoring
   - Attack: BLE security tests

**Scan mode:**
- Passive scan: advertising listening only (no transmission)
- Active scan: sending scan requests to obtain scan responses with additional data
- For each device:
  - MAC address (public or random)
  - Name (if available)
  - RSSI (signal strength)
  - Advertising type (connectable, non-connectable, scannable)
  - Manufacturer data

**Inspect mode (post-connection):**
- Connection to the selected device
- Enumeration of all GATT services:
  - Service UUID (standard or custom)
  - Characteristics: UUID, properties (read, write, notify, indicate), value
  - Descriptors: UUID, value
- Reading values of readable characteristics
- Identification of known services: Battery Service, Device Information, Heart Rate, etc.

**Monitor mode:**
- Continuous advertising packet monitoring
- Device tracking: appearance, disappearance, RSSI variation
- Useful for counting people/devices in an area over time

**Attack mode (security testing):**
- MAC spoofing: attempt to clone a BLE device's MAC address
- Advertising flood: massive advertising packet transmission to saturate scanners
- Advertising packet monitoring for exposed data analysis

**Configurable parameters:**
- Scan type (passive/active)
- Scan duration
- Minimum RSSI filter
- Device name filter (regex)
- Service UUID filter
- Connection timeout
- Result export format

**Real-world pentest usage example:**

BLE IoT device auditing:
1. BLE scan in the target area: identify all devices.
2. Filter for connectable devices.
3. For each device of interest, perform Inspect:
   - Verify if services expose sensitive data without authentication.
   - Verify if writable characteristics allow unauthorized modifications.
   - Verify the presence of undocumented custom services.
4. Commonly found: smart locks with readable PIN, medical sensors with exposed patient data, beacons with modifiable configuration.
5. Document each vulnerability in the report with the service UUID and exposed value.

> Personal note: BLE is the most neglected protocol in IoT security. Most consumer BLE devices implement no authentication at the GATT level -- anyone can connect and read/write. I have found smart locks configurable via BLE without a PIN, thermostats with modifiable scheduling, and fitness trackers exposing biometric data. BLE Killer is essential for IoT pentesting.

---

## 7. Miscellaneous Tools

### 7.1 ESP Flasher

**What it does at a technical level**

ESP Flasher allows flashing firmware onto connected ESP32s directly from the Flipper Zero, without the need for a PC. The Flipper communicates with the ESP32 bootloader via UART, sending firmware data previously copied to the microSD.

The technical process is identical to esptool but implemented in the Flipper firmware:
1. ESP32 reset into boot mode (GPIO0 low during reset).
2. Synchronization with the ESP32 bootloader via UART.
3. Chip identification (ESP32, ESP32-S2, ESP32-S3).
4. Optional: flash erase.
5. Firmware writing at specified offsets.
6. Checksum verification.
7. ESP32 reset for normal boot.

**Complete step-by-step procedure**

1. Copy firmware files (.bin) to the Flipper's microSD:
   - `SD:/apps_data/esp_flasher/` or dedicated directory
   - Typically needed: bootloader.bin, partitions.bin, firmware.bin
2. Connect the ESP32 to the Flipper with flash pins:
   - TX, RX, GND, 3.3V (standard)
   - GPIO0 for boot mode
   - EN for reset
3. On the Flipper: Applications > GPIO > ESP Flasher.
4. Configure:
   - Chip type: ESP32, ESP32-S2, ESP32-S3
   - Baud rate: 115200, 230400, 460800, 921600
   - Firmware file and offset
5. Put the ESP32 in boot mode (if not automatic).
6. Start flashing.
7. Wait for completion (progress bar).
8. Automatic checksum verification.
9. Automatic ESP32 reset.

**Configurable parameters:**
- Target chip type
- Flash baud rate
- Firmware files (multiple with offsets)
- Erase flash before flashing (yes/no)
- Flash mode: DIO, QIO, DOUT, QOUT
- Flash frequency: 40MHz, 80MHz
- Flash size: 2MB, 4MB, 8MB, 16MB
- Post-flash verification (yes/no)

**Real-world usage example:**

Quick firmware change in the field:
1. During an assessment, you need to switch from Marauder to Evil Portal on the ESP32.
2. The firmware files are already on the microSD.
3. With ESP Flasher, flash the new firmware in 2-3 minutes without a PC.
4. Reconnect the ESP32 and launch the desired tool.

> Personal note: ESP Flasher is slow compared to PC flashing (the Flipper's UART is not the fastest) but it is a lifesaver when you are in the field without a laptop. Always keep the main firmware files on the SD (Marauder, Evil Portal, Camera) ready for flashing. A full flash takes about 3-5 minutes at 115200 baud, 1-2 minutes at 921600 if the connection is stable.

### 7.2 FlipLibrary

**What it does at a technical level**

FlipLibrary is a client for remote repositories of resources, scripts, and modules for the Flipper Zero. Through the ESP32 connected to the Internet, it allows browsing an online catalog, downloading new tools, firmware updates, and resources directly to the Flipper.

The system works like a simplified package manager:
1. The ESP32 connects to the repository server via HTTPS.
2. Downloads the index of available resources (JSON with metadata).
3. The user browses the catalog on the Flipper display.
4. Selects the resource to download.
5. The ESP32 downloads the file and transmits it to the Flipper for SD storage.

**Complete step-by-step procedure**

1. Connect the ESP32 to a WiFi network.
2. On the Flipper: Applications > GPIO > FlipLibrary.
3. The catalog is downloaded automatically.
4. Browse by categories:
   - ESP32 Firmware
   - Scripts
   - Resources (HTML pages for Evil Portal, wordlists, etc.)
   - Additional tools
5. Select the desired resource.
6. View description, size, version.
7. Download -> the file is saved to the microSD in the appropriate directory.
8. Automatic installation if supported.

**Configurable parameters:**
- Repository URL (default or custom)
- Download directory
- Automatic catalog update (yes/no)
- Filters by category, tag, date

### 7.3 FlipSocial

**What it does at a technical level**

FlipSocial is a social network interface that uses the ESP32 to communicate with social platform APIs through an intermediary proxy/server. The Flipper does not communicate directly with platform APIs (which would require complex OAuth) but with a bridge server that handles authentication.

The architecture:
- Flipper -> UART -> ESP32 -> WiFi -> Proxy server -> Social platform API
- The proxy server manages OAuth tokens and sessions
- The Flipper only sends/receives simplified messages

**Complete step-by-step procedure**

1. Configure the proxy server (if self-hosted) or register with the service.
2. Obtain the API token.
3. Configure the ESP32 with WiFi SSID and API token.
4. On the Flipper: Applications > GPIO > FlipSocial.
5. Features:
   - View notifications/feed
   - Send short messages
   - Read received messages
6. Interaction is limited by the Flipper's display and input.

**Configurable parameters:**
- API token
- Target social platform
- Feed update frequency
- Number of messages to display
- Maximum message length

### 7.4 FlipTrader

**What it does at a technical level**

FlipTrader accesses crypto and financial market data through public APIs. The ESP32 makes periodic HTTP requests to APIs (e.g., CoinGecko, CoinMarketCap, Yahoo Finance) and transmits the data to the Flipper for display.

**Complete step-by-step procedure**

1. Connect the ESP32 to a WiFi network.
2. On the Flipper: Applications > GPIO > FlipTrader.
3. Configure:
   - Tickers to monitor (e.g., BTC, ETH, SOL)
   - Reference currency (USD, EUR)
   - Update interval
   - Price alerts (high/low targets)
4. The display shows:
   - Current price
   - 24h change (percentage)
   - Volume
   - Simplified chart (sparkline)
5. Sound/vibration alert upon reaching target price.

**Configurable parameters:**
- Monitored ticker list
- Reference currency
- Update interval (seconds)
- High and low target price for alerts
- API key (if required by data source)
- Data source (CoinGecko, CMC, custom)

### 7.5 FlipWeather

**What it does at a technical level**

FlipWeather retrieves weather data from online APIs (typically OpenWeatherMap) and displays them on the Flipper. The ESP32 makes HTTP requests to the weather API, parses the JSON response, and transmits formatted data to the Flipper.

**Complete step-by-step procedure**

1. Obtain a free API key from OpenWeatherMap (or similar service).
2. Configure the ESP32 with WiFi SSID and API key.
3. On the Flipper: Applications > GPIO > FlipWeather.
4. Configure the city (name or GPS coordinates).
5. The display shows:
   - Current temperature
   - Conditions (clear, cloudy, rain, etc.)
   - Humidity
   - Wind speed and direction
   - Atmospheric pressure
   - 1-3 day forecast
6. Alerts for critical conditions (storms, extreme temperatures).

**Configurable parameters:**
- API key
- City or coordinates
- Units of measure (Celsius/Fahrenheit, km/h or mph)
- Update interval
- Description language
- Critical condition alerts

### 7.6 FlipWorld

**What it does at a technical level**

FlipWorld provides global and geolocated information through various APIs. The ESP32 queries online services to obtain data on countries, currencies, time zones, and IP geolocation.

**Complete step-by-step procedure**

1. Connect the ESP32 to a WiFi network.
2. On the Flipper: Applications > GPIO > FlipWorld.
3. Features:
   - Country Info: enter country name -> complete data (capital, population, language, currency, time zone, phone code)
   - IP Geolocation: resolve IP -> geographic position, ISP, ASN
   - Currency Converter: real-time currency conversion
   - Timezone: current time zone for any city
4. Results are shown on the display and can be saved to SD.

**Configurable parameters:**
- Information language
- Date/time format
- Base currency for conversions
- IP geolocation data source

**Real-world pentest usage example:**

IP geolocation during reconnaissance:
1. Obtain a list of target IPs (from DNS, scans, etc.).
2. With FlipWorld, geolocate IPs to identify: datacenters, CDNs, office locations.
3. Useful for understanding the target's geographic infrastructure without a laptop.

### 7.7 Gemini AI

**What it does at a technical level**

Gemini AI is an interface to the Google Gemini artificial intelligence model through the ESP32. The ESP32 sends HTTP requests to the Google Gemini API with the user's prompt and receives the text response, which is transmitted to the Flipper for display.

The technical flow:
1. The user writes a prompt on the Flipper (virtual keyboard).
2. The prompt is transmitted via UART to the ESP32.
3. The ESP32 builds the HTTP POST request to the Gemini API with the prompt and API token.
4. The API responds with generated text (JSON).
5. The ESP32 parses the response and transmits it to the Flipper.
6. The Flipper displays the response (scrollable if long).

**Complete step-by-step procedure**

1. Obtain an API key for Google Gemini.
2. Configure the ESP32 with WiFi SSID and Gemini API key.
3. On the Flipper: Applications > GPIO > Gemini AI.
4. Write the prompt.
5. Send -> wait for the response (a few seconds).
6. Read the response on the display.
7. Option to continue the conversation (history is maintained).

**Configurable parameters:**
- Google Gemini API key
- Model (gemini-pro, gemini-pro-vision if supported)
- Temperature (0-1, controls response creativity)
- Max response tokens
- Conversation mode (single question or chat)
- Custom system prompt

**Real-world pentest usage example:**

Quick assistant during an assessment:
1. Quick questions: "What is the default port for service X?"
2. Payload generation: "Generate an XSS payload for an input field"
3. Quick analysis: "Explain what this Base64 script does: [paste]"
4. Limitation: the Flipper keyboard makes input slow, only useful for short questions.

### 7.8 Gravity

**What it does at a technical level**

Gravity is a tool for reading and visualizing data from physical sensors connected to the ESP32 via I2C or SPI. It supports accelerometers, gyroscopes, magnetometers, temperature/humidity/pressure sensors, and other compatible sensors.

The ESP32 reads data from sensors connected to I2C pins (SDA/SCL) or SPI, processes them, and transmits them to the Flipper for visualization as real-time graphs and numerical values.

Typical supported sensors:
- IMU (Inertial Measurement Unit): MPU6050, MPU9250, LSM6DS3
- Barometer: BMP280, BME280
- Magnetometer: HMC5883L, QMC5883L
- Temperature/Humidity: DHT22, SHT31, BME280

**Complete step-by-step procedure**

1. Connect the sensor to the ESP32:
   - I2C: SDA -> GPIO21, SCL -> GPIO22 (ESP32 default)
   - Power: 3.3V, GND
2. Flash the Gravity firmware onto the ESP32.
3. Connect the ESP32 to the Flipper via GPIO.
4. On the Flipper: Applications > GPIO > Gravity.
5. The tool automatically detects connected sensors.
6. Select the sensor to visualize.
7. The display shows:
   - Real-time numerical values
   - Time graph (X axis = time, Y axis = value)
   - Appropriate units of measure
8. Logging to SD for subsequent analysis.

**Configurable parameters:**
- Active sensor
- Sampling frequency (Hz)
- Graph axis scale (auto or manual)
- Graph window duration
- Logging format
- Units of measure
- Sensor calibration

### 7.9 Morse Flash

**What it does at a technical level**

Morse Flash uses the ESP32-CAM's high-power LED as an optical Morse code transmitter. The Flipper converts text to Morse code (dots and dashes) and controls the ESP32-CAM LED to transmit it visually.

The encoding follows the international standard:
- Dot (dit): LED on for 1 time unit
- Dash (dah): LED on for 3 time units
- Pause between elements of the same character: 1 unit
- Pause between characters: 3 units
- Pause between words: 7 units

The time unit duration depends on the speed in WPM (Words Per Minute). The reference word is "PARIS" (50 units): at 20 WPM, one unit lasts 60ms.

**Complete step-by-step procedure**

1. Connect ESP32-CAM to the Flipper.
2. On the Flipper: Applications > GPIO > Morse Flash.
3. Enter the text to transmit.
4. Configure:
   - Speed (WPM)
   - Mode: single or loop
   - LED brightness
5. Start transmission.
6. The ESP32-CAM LED transmits the message in Morse.
7. In loop mode, the message repeats indefinitely.

**Configurable parameters:**
- Speed (WPM: 5-40, default 20)
- Mode: single send, continuous loop, burst (N repetitions)
- LED brightness (0-255 PWM)
- Saved predefined messages
- Encoding: international, extensions for special characters

**Real-world usage example:**

Long-distance optical communication:
1. The ESP32-CAM flash LED is very powerful (typically 600-700mA).
2. In dark conditions, the Morse signal is visible at hundreds of meters.
3. Useful for simple communication when radio and cellular are not options.
4. Application in CTFs or exercises: flag/code transmission via Morse.

---
