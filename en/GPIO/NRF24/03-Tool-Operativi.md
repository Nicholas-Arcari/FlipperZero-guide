## 4. NRF24 Sniffing

### 4.1 Raw packet capture

The Flipper Zero's NRF24 Sniffer captures raw packets transmitted by devices using the NRF24L01+ chip or compatible protocols.

What it captures:

- Complete Enhanced ShockBurst packets
- Pipe address (3-5 bytes)
- Payload (0-32 bytes per packet)
- CRC (for integrity validation)
- Timing information (timestamp)
- RF channel of reception

What it does NOT capture:

- The preamble (handled internally by the chip)
- Packets on channels other than the configured one (unless scanning)
- Packets with non-ESB format (other 2.4 GHz protocols)

### 4.2 Operating modes

**Generic sniffer:**

- You configure a channel and a pipe address (or a "promiscuous" address)
- The module captures all traffic matching the criteria
- Packets are displayed in real time on the Flipper's display
- They can be exported for later analysis

**Sniffer in promiscuous mode:**

- Advanced technique: you configure a very short pipe address (2 bytes) with a common pattern
- Captures a larger volume of traffic, including packets from unknown devices
- Useful during the reconnaissance phase when the target's address is unknown
- More noise (false positives) but broader coverage

**Sniffer with "Follow Target":**

- After identifying a device, the sniffer automatically follows channel changes
- Based on the frequency hopping pattern of the target protocol
- Essential for Logitech Unifying which changes channels frequently

### 4.3 Pipe address decoding

Every NRF24 device has a unique pipe address. Decoding this address is the first step for any targeted attack.

Decoding techniques:

1. **Passive sniffing**: capture packets and extract the address from the address field
2. **Brute force**: try common addresses (many cheap devices use default addresses like 0xE7E7E7E7E7)
3. **Pattern matching**: search for known sequences in captured data
4. **Firmware reverse engineering**: extract the address from the device firmware (if accessible)

Common default addresses:

```
0xE7E7E7E7E7  -- NRF24 default (very common)
0xC2C2C2C2C2  -- Common alternative
0xA5A5A5A5A5  -- Used by some Chinese manufacturers
0x0102030405  -- Sequential (development devices)
```

> Personal note: the number of devices using default addresses is staggering. During an audit I found 3 out of 5 temperature sensors with address 0xE7E7E7E7E7. Manufacturers don't even change the default address from the Nordic reference design. It's like using admin/admin as credentials.

### 4.4 Payload analysis

Once packets are captured, payload analysis reveals:

**For wireless mice:**

- Status byte (pressed buttons)
- Delta X and Delta Y (movement)
- Scroll wheel delta
- Control/sequence byte

Typical Logitech Unifying mouse payload format:

```
Byte 0: device type (0x00 = mouse)
Byte 1: flags (buttons)
Byte 2-3: delta X (little endian)
Byte 4-5: delta Y (little endian)
Byte 6: scroll wheel
Byte 7-9: reserved/padding
```

**For wireless keyboards (unencrypted):**

- Pressed key scancode
- Modifier keys (Shift, Ctrl, Alt, GUI)
- Ability to reconstruct everything typed (keylogging via radio)

**For IoT sensors:**

- Telemetry data (temperature, humidity, pressure)
- Sensor identifiers
- Sequence counters
- Battery status byte

### 4.5 MS Sniffer -- Microsoft Devices

Sniffer variant optimized for Microsoft Wireless protocols:

- Recognition of MS proprietary packet formats
- Decoding of MS-specific fields (device type, battery status, extra buttons)
- Better lock-on to channels used by MS devices
- Handling of the MS frequency hopping pattern

Microsoft devices use a slightly different protocol from Logitech:

- Pipe addresses specific to each product family
- Different payload format for mice and keyboards
- Proprietary pairing mechanism
- Some models use a form of obfuscation (not real encryption)

### 4.6 Use for reverse engineering

The NRF24 sniffer is an excellent tool for reverse engineering proprietary protocols:

1. Capture traffic under different conditions (idle, movement, click, pairing)
2. Compare payloads to identify variable vs fixed fields
3. Correlate physical actions with payload variations
4. Reconstruct the protocol format field by field
5. Verify hypotheses by injecting modified packets

This technique has been used to reverse-engineer the protocols of:

- Wireless mice and keyboards (Logitech, Microsoft, HP, Dell)
- Wireless temperature/humidity sensors (Oregon Scientific, Acurite)
- Cheap drone remote controls
- Wireless alarm systems
- Radio-controlled toys
- Wireless doorbells
- LED light remote controls

> Personal note: reverse engineering with the NRF24 sniffer is one of the most educational activities you can do with the Flipper. I spent an entire weekend decoding the protocol of an Oregon Scientific temperature sensor. By the end I had documented every single byte of the payload: sensor ID, channel, temperature (BCD encoded with sign), humidity, battery status, checksum. The satisfaction of seeing correctly decoded data is priceless. This is how you truly learn how RF communications work.

---

## 5. 2.4 GHz Jamming

### 5.1 How it works

Jamming consists of flooding one or more RF channels with interfering signal, preventing legitimate devices from communicating.

The NRF24L01+ can be used as a jammer in two ways:

**Continuous carrier jamming:**

- The module transmits a continuous signal on a specific channel
- Any device on that channel cannot communicate
- Simple but effective

**Packet jamming:**

- The module transmits fictitious packets at high speed
- Fills the channel with junk traffic
- Legitimate devices cannot get a word in
- More effective than continuous carrier for some protocols

### 5.2 Targeted jamming by channel

By selecting a specific channel, you can disrupt only the devices operating on that channel:

- Identify the target's channel with Channel Scan or Sniffer
- Configure the jammer on that specific channel
- Activate continuous transmission

Advantages:

- Disrupts only the target, not all devices in the area
- Less conspicuous and more surgical
- Useful for targeted tests on specific devices

### 5.3 Multi-channel jamming

Mode that cyclically scans multiple channels, transmitting briefly on each:

- Covers a broader spectrum
- Disrupts devices with frequency hopping
- Less effective on each individual channel (reduced dwell time)
- Useful against protocols that change channels when they detect interference

The Flipper Zero with NRF24 offers two implementations:

**FZ NRF24 Jammer:**

- Optimized for the Flipper Zero
- Simplified configuration via menu
- Single channel and sweep modes
- Real-time effectiveness logging

**NRF24 Jammer (generic):**

- Standard version
- Cyclic multi-channel support
- Burst and stream modes
- Operational bandwidth configuration

### 5.4 Effectiveness and limitations

Jamming with the NRF24L01+ has inherent limitations:

- Maximum power 0 dBm (base version) or +20 dBm (PA+LNA)
- A single module can only transmit on one channel at a time
- Cyclic multi-channel leaves temporal "gaps"
- Devices with aggressive frequency hopping can resist
- Wi-Fi (which operates in the same band) can be disrupted but has much higher power

For effective jamming:

- Use the PA+LNA version for maximum power
- Position yourself as close to the target as possible
- Identify the target's exact channels before jamming
- Consider that Bluetooth frequency hopping is highly resistant to NRF24 jamming

### 5.5 Legal implications of jamming

RF jamming is ILLEGAL in virtually all jurisdictions, including Italy.

Italian regulatory references:

- Electronic Communications Code (D.Lgs. 259/2003)
- Art. 340 Criminal Code (disruption of public service, if jamming affects public services)
- Art. 617-quater Criminal Code (interception of computer or telecommunications)
- AGCOM sanctions for improper use of radio equipment

Jamming is permitted ONLY:

- In fully shielded environments (Faraday cage)
- With explicit written authorization from the client
- In military/government contexts with specific authorization
- For laboratory testing with contained emissions

> Personal note: NEVER use the jammer in uncontrolled environments. During a pentest at a company, a colleague accidentally turned on the NRF24 jammer at full power. It disrupted the wireless mice of three offices and a Wi-Fi access point on the same band. The IT team showed up in 5 minutes. We had to explain the situation to the manager. Since that day, the jammer is used ONLY in a shielded test room or with specific written authorization that explicitly mentions RF jamming. The golden rule: if your scope of work doesn't explicitly say "jamming authorized", don't do it.

---

## 6. Channel Scan

### 6.1 2.4 GHz spectrum scanning

The Channel Scan performs a systematic scan of the 126 available channels to identify RF activity.

How it works:

1. The NRF24 module tunes to each channel in sequence
2. For each channel, it measures the received signal level
3. It detects whether there are valid packets (with correct CRC)
4. It presents the results as a spectral map

### 6.2 Active channel identification

Active channels are identified based on:

- Signal level above a configurable threshold
- Presence of packets with valid CRC
- Activity pattern (constant vs intermittent)
- Signal type (Enhanced ShockBurst vs noise)

Interpreting results:

- **Narrow peaks on specific channels**: NRF24 devices (mice, sensors, remotes)
- **Wide bands of activity**: Wi-Fi interference
- **Intermittent activity**: devices that transmit only on events (mouse in motion, periodic sensors)
- **Constantly occupied channels**: devices in continuous streaming or beaconing

### 6.3 RSSI and distance estimation

The NRF24L01+ does not provide a direct RSSI value like other transceivers. However, signal strength can be estimated indirectly:

- RPD (Received Power Detector): binary flag indicating whether the signal exceeds -64 dBm
- Packet loss rate: higher = weak signal / greater distance
- CRC errors: increase with signal degradation

For a more precise distance estimate:

1. Perform a reference scan at a known distance
2. Move and repeat the scan
3. Compare the packet reception rate
4. Triangulate with multiple measurements from different positions

### 6.4 Practical use in pentesting

Channel Scan is the first step in any NRF24 operation:

1. **Reconnaissance**: scan to identify all active wireless devices
2. **Planning**: choose the least congested channel for your own operations
3. **Targeting**: identify the target device's channel
4. **Validation**: verify after an attack that the target has changed channels or is offline

Typical workflow:

```
Channel Scan -> Identify target -> Sniffer (capture address) -> MouseJacker/Analysis
```

> Personal note: I always do at least two complete scans before starting any operation. The first to get a baseline of the RF environment, the second after 5-10 minutes to confirm which devices are permanent and which are transient. In a typical office I find between 5 and 15 NRF24-compatible devices. Wireless mice are the most common, followed by keyboards and then various IoT sensors.

---

## 7. NRF24Monitor / Scanner / Batch

### 7.1 NRF24Monitor

The monitor is the tool for continuous observation of RF activity.

Features:

- Live monitoring of incoming packets on a selected channel
- Display of packet count per pipe address
- Detection of new devices appearing in the area
- Activity tracking over time (burst vs constant vs periodic)
- Identification of handshakes and pairing sequences
- Detection of active pipes (NRF logical addresses)

Operating modes:

**Single channel monitor:**

- You fix a channel and observe all traffic
- Ideal after identifying the target's channel with Channel Scan
- Maximum sensitivity (no time wasted switching channels)

**Multi-channel monitor:**

- Rapid cyclic scanning of multiple channels
- Broader coverage but possibility of missing packets
- Useful during the initial reconnaissance phase

**RSSI/noise display:**

- Shows signal level for each received packet
- Useful for estimating the relative distance of devices
- Allows physically locating a device by moving and observing the level

### 7.2 Scanner

The Scanner is dedicated to actively searching for NRF24 devices in the area.

Differences from the Monitor:

- The Scanner actively searches for devices, rather than just passively observing
- It scans all channels in sequence
- It identifies devices through packet fingerprinting
- It estimates relative distance through signal strength

Features:

- Pipe address scanning on all channels
- Fingerprinting: identifies device type from packet format
- Classification: mouse, keyboard, sensor, unknown
- Relative distance estimation (near/medium/far based on RPD and packet loss)
- Exportable log with timestamp, address, channel, type, signal strength

Typical use:

1. Start the Scanner at the entrance of a target area
2. Walk slowly through the area
3. The Scanner identifies and catalogs every NRF24 device
4. Export the log for later planning
5. Select targets for in-depth analysis

### 7.3 Batch

Batch execution allows automating sequences of NRF24 operations.

Features:

- Execution of preconfigured scripts
- Command sequences: scan, sniff, jam in a defined order
- Integration with external script files from the SD card
- Automatic result logging
- Scheduled (timed) execution

Batch script examples:

**Automatic reconnaissance script:**

```
# Full scan + address capture
CHANNEL_SCAN ALL
WAIT 30
SNIFFER PROMISCUOUS CH:0-125
WAIT 60
LOG EXPORT /ext/nrf24/recon_log.txt
```

**Overnight monitoring script:**

```
# Continuous monitoring for 8 hours
MONITOR MULTI_CH
DURATION 28800
LOG CONTINUOUS /ext/nrf24/night_monitor.txt
ALERT ON_NEW_DEVICE
```

**Peripheral audit script:**

```
# Scan and test each found device
SCANNER FULL
FOR EACH DEVICE
  IDENTIFY TYPE
  IF TYPE == MOUSE
    LOG "Wireless mouse found" + ADDRESS
    TEST MOUSEJACKER DRY_RUN
  ENDIF
NEXT
LOG EXPORT /ext/nrf24/audit_report.txt
```

Batch automation is particularly useful for:

- Recurring audits (running the same scan weekly)
- Continuous background monitoring
- Regression testing after remediation
- Automatic documentation for reports

> Personal note: batch is underrated. I use it to automate the reconnaissance phase during pentests: I arrive, attach the Flipper with NRF24, launch the reconnaissance script and in the meantime I take care of other things. After 10 minutes I have a complete map of all NRF24 devices in the area with addresses, channels, and types. It saves me at least half an hour of manual work every time.

---
