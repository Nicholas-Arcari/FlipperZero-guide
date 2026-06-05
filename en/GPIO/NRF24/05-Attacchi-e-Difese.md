## 9. Legal Aspects

### 9.1 Italian regulatory framework

The use of the NRF24L01+ module with the Flipper Zero for analysis and testing activities falls within a complex regulatory framework.

**Activities permitted without authorization:**

- Personal study and research in a domestic environment
- Testing on devices you own
- Passive spectral analysis (receive only)
- Software and firmware development

**Activities requiring authorization:**

- Penetration testing on third-party systems (requires contract and scope of work)
- Sniffing of others' communications (even if in the clear)
- Any form of packet injection on devices you don't own
- Jamming tests (even in a controlled environment, for liability protection)

**Activities that are illegal without exception:**

- Jamming in an unshielded environment without authorization
- Interception of private communications
- Unauthorized access to computer systems (via MouseJacker or otherwise)
- Disruption of telecommunications

### 9.2 Regulatory references

- **D.Lgs. 259/2003** (Electronic Communications Code): regulates the use of radio frequencies. Use of the 2.4 GHz ISM band is permitted for low-power devices compliant with ETSI standards, but intentional jamming is explicitly prohibited.
- **Art. 615-ter Criminal Code** (Unauthorized access to a computer system): injecting commands via MouseJacker on a PC without authorization constitutes unauthorized access.
- **Art. 617-quater Criminal Code** (Interception of communications): sniffing wireless keyboards can constitute interception.
- **Art. 340 Criminal Code** (Disruption of public service): if jamming affects public services.
- **AGCOM Regulation**: administrative sanctions for improper use of radio equipment.

### 9.3 Authorized penetration testing

To operate legally during a pentest:

1. **Signed contract** with the client that specifies:
   - Scope of activities (explicitly including RF activities)
   - List of in-scope assets
   - Authorized time period
   - Emergency contacts
   - Limits and exclusions

2. **Authorization letter** (Get Out of Jail Free letter):
   - Signed by the company's legal representative
   - Specifies authorized activities
   - Includes reference to the contract
   - Must be carried at all times during activities

3. **Rules of Engagement (RoE):**
   - Permitted hours for activities
   - Authorized physical areas
   - Authorized and prohibited techniques
   - Escalation procedure in case of incidents
   - Handling of any sensitive data captured

4. **For specific RF activities, the contract should mention:**
   - "Wireless peripheral security testing"
   - "RF spectrum analysis within the office area"
   - "Jamming resilience verification" (if applicable)
   - "MouseJacker attack simulation"

### 9.4 GDPR and captured data

Wireless keyboard sniffing can capture personal data (passwords, emails, messages). The processing of this data is subject to GDPR:

- Minimization: capture only what is necessary for the proof of concept
- Limited retention: delete raw data after the report
- Pseudonymization: in the report, do not include captured personal data
- Notification: inform the client of any personal data captured
- Security: protect captured data with encryption during transport and storage

> Personal note: the legal part isn't sexy but it's fundamental. I've seen colleagues get into trouble for doing RF sniffing without explicit authorization. My advice: have a specific clause for RF activities inserted into the contract. Clients often authorize "classic" pentesting (network, web, social engineering) but don't think about RF. If your scope of work only says "infrastructure penetration test", MouseJacker might NOT be covered. Better to ask first than explain later.

---

## 10. Available Tools in Flipper Zero -- Operational Detail

Complete summary of NRF24 tools available in the Flipper Zero with custom firmware (Unleashed / RogueMaster):

### AZERTY Mouse Jacker

Version of the Mouse Jacker optimized for AZERTY layout, commonly used in France, Belgium, and other French-speaking regions.

Features:

- Hijacking of vulnerable wireless mice via USB dongle spoofing
- Sending commands as movements, clicks, simulated typing
- Automatic layout conversion from QWERTY to AZERTY
- Active frequency scanning with automatic target lock-on
- "Stealth delay" mode to simulate human input and reduce suspicion
- Support for French accented characters (e', e`, a`, u`, c cedilla)

When to use it:

- Targets with French/Belgian keyboard layout
- Penetration testing at French-speaking companies
- When the QWERTY layout produces incorrect characters on the target

### Batch

Automated execution of preconfigured radio scripts for repetitive workflows.

Features:

- Sequences of NRF24 commands executable in batch from script files
- Automation of scan, sniff, jam in user-defined order
- Integration with external script files from the SD card
- Automatic result logging with timestamps
- Ability to chain multiple operations without manual intervention

When to use it:

- Automated reconnaissance at the start of an audit
- Continuous background monitoring
- Execution of repetitive tests on multiple targets
- Automatic log generation for reporting

### Channel Scan

2.4 GHz spectrum scanning on NRF channels to detect activity.

Features:

- Signal intensity analysis for each channel (0-125)
- Rapid identification of channels occupied by target devices
- Simplified graphical display of signal distribution
- Comparison between successive scans to detect changes
- Identification of Wi-Fi interference in the same band

When to use it:

- As the first step in any NRF24 operation
- To identify a target device's channel
- To choose a clean channel for your own transmissions
- To map the RF environment of the area of interest

### FZ NRF24 Jammer

Dedicated RF jammer with optimizations specific to the Flipper Zero.

Features:

- Channel flooding with fictitious packets at high speed
- Sequential mode: cyclic multi-channel jamming
- TX power configuration
- Real-time jamming effectiveness logging
- Interface optimized for the Flipper display

When to use it:

- Resilience testing of wireless systems in a shielded laboratory
- Verification of a system's anti-jamming countermeasures
- Only with explicit authorization and in a controlled environment

### Mouse Jacker

Main tool for hijacking unencrypted wireless mice.

Features:

- Automatic channel scanning to search for wireless peripherals
- Capture of the target peripheral's pairing ID
- Dongle spoofing: the Flipper replaces the legitimate mouse
- Sending HID sequences (clicks, movements, typing via DuckyScript)
- Automatic active frequency detection
- Support for custom payloads from the SD card

When to use it:

- Proof of concept for wireless peripheral security audits
- Awareness demos for management
- Lateral movement testing in penetration tests
- Verification of firmware update effectiveness

### Mouse Jacker MS

Version optimized for Microsoft Wireless mice and peripherals.

Features:

- Recognition of MS proprietary protocols
- Reduced latency for faster lock-on to MS devices
- Handling of MS-specific inputs like tilt-scroll and extra functions
- Better stability in noisy RF environments
- Compatibility with various generations of MS dongles

When to use it:

- Specifically Microsoft Wireless targets
- When the generic Mouse Jacker doesn't lock onto the MS device
- For reverse engineering of MS proprietary protocols

### NRF24 Jammer

Generic version of the jammer, compatible with different configurations.

Features:

- Single channel or multi-channel jamming
- Support for different operational bandwidths
- Burst (pulse) or continuous stream mode
- Sweep pattern configuration for multi-channel

When to use it:

- Alternative to the FZ NRF24 Jammer for non-standard configurations
- Testing on specific channel bands
- Stress testing of devices with frequency hopping

### NRF24Monitor

Advanced RF activity monitor on NRF24 module channels and pipes.

Features:

- Live packet monitoring with counter
- Estimated RSSI/noise display
- Handshake and pairing flow detection
- Active pipe identification (NRF logical addresses)
- Alerts on newly detected devices
- Exportable continuous log

When to use it:

- Passive observation of the RF environment
- Detection of new devices in the area
- Study of a target device's behavior over time
- RF transmission problem diagnostics

### Scanner

Tool for actively searching for NRF24 devices in the surrounding area.

Features:

- Pipe address and active frequency scanning on all 126 channels
- Unknown device identification through packet fingerprinting
- Device type classification (mouse, keyboard, sensor, other)
- Relative distance estimation through signal strength (RPD)
- Exportable log with all details of found devices

When to use it:

- Complete mapping of NRF24 devices in an area
- Wireless peripheral inventory in an office
- Physical location of a specific device
- Attack preparation (target identification and parameters)

### Sniffer

NRF24 packet capture for analysis, reverse engineering, and auditing.

Features:

- Raw packet capture with precise timestamps
- Pipe address, sequence number, and payload decoding
- Export in externally analyzable format
- "Follow Target" mode for devices that change channels
- Pipe address filter to isolate a specific device
- Continuous capture with circular buffer

When to use it:

- Reverse engineering of proprietary protocols
- Credential capture from unencrypted keyboards
- IoT sensor traffic analysis
- Study of the pairing protocol of new devices
- Evidence collection for the audit report

### Sniffer MS

Sniffer variant specific to Microsoft protocols.

Features:

- MS format recognition with automatic decoding
- Better lock-on to MS mice/keyboards at 2.4 GHz
- Preliminary decoding of known MS protocol fields
- Tracking of the MS frequency hopping pattern

When to use it:

- Specific analysis of Microsoft Wireless devices
- When the generic Sniffer doesn't correctly capture MS packets
- In-depth reverse engineering of the MS protocol
- Security audit of environments with Microsoft peripherals

---
