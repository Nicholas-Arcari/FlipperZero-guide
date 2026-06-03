## Tool by Tool - Operational Guide

### Sub-GHz (Main Module)

The central hub for all RF operations.

**Main menu:**
- **Read** - Listen and automatically decode signals
- **Read RAW** - Capture the raw signal without decoding
- **Saved** - Manage saved .sub files
- **Add Manually** - Create a signal from known parameters
- **Frequency Analyzer** - Detect active frequencies
- **Test** - Hardware diagnostics

#### Read - Automatic Decoding

Complete operational procedure:

1. Open Sub-GHz -> Read
2. The Flipper listens on the configured frequency (default 433.92 MHz)
3. **To change frequency:** press <- or -> to scroll through preset frequencies, or hold <- to enter a manual frequency
4. **To change modulation:** press the config button and select AM (OOK) or FM (FSK)
5. When a remote transmits within range, the Flipper decodes the protocol and displays:
   - Protocol name (e.g., "Nice FLO")
   - Remote code/ID
   - Bit count
   - Counter (if rolling code)
   - Exact frequency
6. Press the center button to **save** the decoded signal

**Saved .sub file parameters:**
```
Filetype: Flipper SubGhz Key File
Version: 1
Frequency: 433920000
Preset: FuriHalSubGhzPresetOok650Async
Protocol: Princeton
Bit: 24
Key: 00 00 00 00 00 A4 B3 C2
```

**Available presets and when to use them:**

| Preset | Modulation | Bandwidth | Use |
|---|---|---|---|
| FuriHalSubGhzPresetOok270Async | OOK | 270 kHz | Default for most remote controls |
| FuriHalSubGhzPresetOok650Async | OOK | 650 kHz | Wideband signals, some sensors |
| FuriHalSubGhzPreset2FSKDev238Async | 2-FSK | 238 kHz dev | Standard FSK protocols |
| FuriHalSubGhzPreset2FSKDev476Async | 2-FSK | 476 kHz dev | Wide deviation FSK protocols |
| FuriHalSubGhzPresetCustom | Custom | Variable | Manual CC1101 register configuration |

> **Personal note:** The OOK270 preset is the one I use 95% of the time. I have only used OOK650 with some Oregon Scientific weather sensors that have a wider signal than normal. For the rest, if it does not decode with OOK270, I go straight to Read RAW.

#### Read RAW - Raw Capture

When the Flipper cannot decode the protocol (proprietary signal, non-standard modulation, unsupported protocol), Read RAW captures the entire signal as a sequence of pulse durations:

1. Open Sub-GHz -> Read RAW
2. Set the target frequency
3. Press the REC button (record)
4. The target remote transmits
5. The Flipper records the entire signal as raw
6. Press STOP
7. Save the file

**The RAW .sub file contains:**
```
Filetype: Flipper SubGhz RAW File
Version: 1
Frequency: 433920000
Preset: FuriHalSubGhzPresetOok650Async
Protocol: RAW
RAW_Data: 5542 -5026 501 -1020 499 -1022 499 -510 ...
```

The numbers represent durations in microseconds: positive = signal high (TX), negative = signal low (silence).

**When to use Read RAW:**
- The protocol is not recognized
- You want to capture a rolling code signal (for study, not for replay)
- The signal is very weak or noisy
- You are reverse engineering an unknown protocol
- The device uses a non-standard modulation

**Replaying a RAW file:**
1. Open Sub-GHz -> Saved -> select the RAW file
2. Press Send
3. The Flipper reproduces the exact pulse sequence

> **Personal note:** Read RAW is essential for reverse engineering. When I find an unknown device, I always capture in both OOK and FSK and then analyze the files offline. Be careful: RAW files can get very large if you record for too long. Keep the recording as short as possible - 2-3 seconds of signal is enough.

#### Saved - File Management

From here you can:
- **Send:** transmit the saved signal
- **Emulate:** for protocols that support it, emulate continuously (useful for iButton/RFID via Sub-GHz, not common)
- **Rename:** rename the file
- **Edit:** modify parameters (frequency, protocol, key)
- **Delete:** delete the file
- **Info:** show file details

#### Add Manually - Signal Creation

Allows you to create a .sub file from scratch by specifying:
- Protocol
- Frequency
- Key/ID
- Bit count
- Repetitions

Useful when you know the target code (e.g., from a database or SDR analysis) and want to create it directly.

### Frequency Analyzer (with External Antenna)

Essential reconnaissance tool: detects the frequency on which an unknown device transmits.

**Operational procedure:**

1. Open Sub-GHz -> Frequency Analyzer
2. The display shows a real-time RSSI graph
3. Press the target remote's button **close** to the Flipper (< 1 meter)
4. A peak appears at the signal's frequency
5. The dominant frequency is shown at the top
6. Note the frequency -> use it in Read or Read RAW

**Limitations:**
- Only works on bands supported by the CC1101
- Resolution is limited (~10-20 kHz)
- Very weak signals may not be detected
- Does not distinguish between modulations (Read is needed for that)

**With external antenna:** connecting an external CC1101 module via GPIO significantly increases sensitivity. This allows detecting signals at greater distances (10-20 meters instead of 1-2).

> **Personal note:** The Frequency Analyzer is the first tool I open when facing an unknown RF device. However, its precision is limited - it shows the approximate frequency. For a precise measurement you need an SDR (HackRF/RTL-SDR) and software like SDR# or GQRX. In real engagements, I use the Flipper for a quick analysis and then confirm with the HackRF if needed.

### Radio Scanner

Continuous scanning of the entire Sub-GHz spectrum to identify all active RF sources in an area.

**Operational procedure:**

1. Open Radio Scanner
2. Select the band to scan (300-928 MHz or sub-band)
3. The display shows the RSSI graph for each scanned frequency
4. Peaks indicate active devices
5. You can "zoom in" on a specific range for greater detail

**Use in pentesting:**
- Map all RF devices in a target building
- Identify frequencies used by alarm systems
- Find hidden wireless sensors
- Assess the RF "background noise" of an area

> **Personal note:** The Scanner is slow but useful for the reconnaissance phase. I use it while walking around the target building to understand which frequencies are active. I have discovered wireless alarms, RF motion sensors, and even baby monitors this way. The trick is to do it during active hours - when people are using remotes and sensors.

### Spectrum Analyzer

Real-time FFT visualization of the RF spectrum.

**Difference from the Radio Scanner:** the Spectrum Analyzer shows the spectrum in real time (like a frequency oscilloscope), while the Radio Scanner performs a sequential scan saving the results.

**Operational procedure:**

1. Open Spectrum Analyzer
2. Set center frequency and span
3. The display shows the amplitude vs frequency graph
4. Active signals appear as peaks
5. Useful for visualizing interference and overlapping signals

**Preset bands:**
- 315 MHz band (US remotes)
- 433 MHz band (EU remotes)
- 868 MHz band (EU home automation)
- 915 MHz band (US ISM)

### Sub-GHz Bruteforcer

Tool for testing the robustness of fixed code systems through sequential transmission of all possible codes.

**WARNING:** Use only on systems you own or with written authorization.

**Operational procedure:**

1. Open Sub-GHz Bruteforcer
2. Select the target protocol (e.g., Nice FLO 12-bit, Came 12-bit, Linear, Chamberlain, etc.)
3. Set the frequency
4. The Flipper calculates the total number of combinations:
   - Nice FLO 12-bit: 4096 combinations
   - Came 12-bit: 4096 combinations
   - Princeton 24-bit: 16,777,216 combinations (impractical)
   - Linear 10-bit: 1024 combinations
   - Chamberlain 9-bit: 512 combinations
5. Start the bruteforce
6. The Flipper transmits all codes sequentially
7. If the receiver activates, the valid code is identified

**Estimated times (at standard speed):**
- 10 bits (1024 codes): ~5 minutes
- 12 bits (4096 codes): ~20 minutes
- 24 bits (16M codes): days -> impractical

**Optimizations:**
- Reduce the range if part of the code is known
- Increase the transmission speed (risks missing signals)
- Use an external antenna to maximize range

> **Personal note:** Bruteforce is only practical on protocols with a low bit count (10-12). Nice FLO at 12 bits is the ideal target - 4096 combinations in ~20 minutes is feasible during an engagement. On Princeton at 24 bits it is not worth it: it is faster to capture the signal with Read. I have successfully used the bruteforcer on an old 12-bit Came gate during a physical pentest - it found the code in less than 15 minutes.

### Sub-GHz Rolling Flaws

Vulnerability analyzer for rolling code implementations. This tool is specifically designed for studying weaknesses in KeeLoq and similar systems.

**Operational procedure:**

1. Capture at least 2 consecutive rolling codes from the same remote (using Read)
2. Open Rolling Flaws
3. Load the captured codes
4. The tool analyzes:
   - **Seed entropy:** how predictable the sequence is
   - **Counter increment:** whether the increment is fixed or variable
   - **Cryptographic weaknesses:** keys derived from known serials
   - **Resync window:** how permissive the receiver's window is
5. Output: report with security score and identified vulnerabilities

**Vulnerabilities it can identify:**
- KeeLoq implementations with weak or known manufacturer key
- Counters with predictable increment
- Receivers with overly wide resync window
- Protocols with seed derived from serial (allowing prediction)

> **Personal note:** This tool is the most interesting from a research perspective. I have used it to analyze old Nice and Came systems and found that some implementations have keys derived predictably from the remote's serial number. It does not work on all systems - modern ones (Came Atomo, recent FAAC SLH) are robust.

### POCSAG Pager

Decoder for the POCSAG (Post Office Code Standardisation Advisory Group) protocol, used by pagers.

**Technical background:**

POCSAG is a unidirectional messaging protocol on dedicated frequencies:
- **Italy:** 466.075 MHz (pager band)
- **UK:** 153.275 MHz
- **US:** 929-932 MHz
- **Data rate:** 512, 1200 or 2400 baud

**POCSAG message structure:**
```
[Preamble: 576 alternating bits 1010...]
[Sync: 0x7CD215D8]
[Batch 1: 8 codewords of 32 bits]
[Sync]
[Batch 2: 8 codewords]
...
```

Each codeword contains:
- **Address codeword:** RIC (Radio Identity Code) of the recipient + function
- **Message codeword:** data (numeric or alphanumeric)

**Operational procedure:**

1. Open POCSAG Pager
2. Set frequency (466.075 MHz for Italy)
3. The Flipper listens and decodes messages
4. For each message it shows: RIC, function, content
5. Messages can be exported to a log

**Security implications:**

POCSAG pagers transmit in cleartext. Anyone with a receiver on the correct frequency can read all messages. This is a serious problem in hospital and emergency environments where pagers are still used for sensitive communications.

> **Personal note:** I used the POCSAG decoder during an engagement at a hospital (authorized). The pagers were transmitting patient names, room numbers, and medical information in cleartext. It was a critical finding in the report. In Italy, pagers are still used in hospitals, fire departments, and some industries. The 466.075 MHz frequency is the first one to check.

### Weather Station

Decoder for wireless weather stations that transmit data on 433/868 MHz.

**Supported protocols:**
- Oregon Scientific v2.1/v3.0
- Acurite
- Lacrosse TX
- Ambient Weather
- Bresser
- Fine Offset / Ecowitt
- Nexus / Digoo

**Decoded data:**
- Temperature
- Humidity
- Barometric pressure
- Wind speed and direction
- Precipitation
- Sensor ID
- Low battery
- Channel

**Operational procedure:**

1. Open Weather Station
2. Set to 433.92 MHz (EU standard) or 868 MHz
3. Nearby sensors are automatically decoded
4. Each sensor appears with ID, temperature, humidity, and other data
5. Data is updated with each sensor transmission (typically every 30-60 seconds)

**Use in pentesting/OSINT:**
- Identify the presence of wireless systems in the target area
- Map weather sensors to understand the level of IoT adoption
- During reconnaissance, the presence of sensors indicates that the building has potentially vulnerable wireless automation

### TPMS Reader

Reader for tire pressure monitoring sensors (Tire Pressure Monitoring System).

**Technical background:**

Every modern tire (mandatory in the EU since 2014) contains a sensor that periodically transmits:
- **Frequency:** 433.92 MHz (EU) or 315 MHz (US)
- **Modulation:** OOK or FSK
- **Data:** sensor ID (32 bits), pressure (kPa), temperature (C), battery status
- **Interval:** every 60-90 seconds or upon detecting changes

**Operational procedure:**

1. Open TPMS Reader
2. Set to 433.92 MHz
3. Bring the Flipper close to a tire (< 2 meters)
4. Wait 1-2 minutes for the transmission
5. The display shows: sensor ID, pressure, temperature

**Security implications:**

- **Vehicle tracking:** each TPMS sensor has a unique ID. By monitoring these IDs it is possible to track the passage of specific vehicles without cameras.
- **Privacy:** combining TPMS IDs with location, a movement profile can be built.
- **Spoofing:** it is theoretically possible to send fake TPMS data to trigger the warning light on the dashboard.

> **Personal note:** The TPMS reader is more useful than you would think for OSINT. During an engagement I used TPMS IDs to confirm that a specific vehicle was in the target building's parking lot, without physically approaching it. The sensors transmit even when the car is parked - you just need patience.

### Restaurant Pager

Decoder for call systems used in restaurants and fast-food chains.

**Common protocols:**
- **LRS (Long Range Systems):** 433.92 MHz, OOK
- **HME (HM Electronics):** variable frequencies
- **JTECH:** 433/868 MHz

**Decoded data:**
- Pager ID
- Command (vibrate, LED, beep)
- Group

**Use in security research:**
- Demonstrate that these systems transmit in cleartext
- Test the possibility of activating pagers you do not own (only in a controlled environment)
- Analyze protocol robustness

### Enhanced Sub-GHz Chat

Bidirectional communication system between Flipper Zero devices via RF.

**Operational procedure:**

1. On both Flippers: open Enhanced Sub-GHz Chat
2. Set the same frequency (e.g., 433.92 MHz)
3. Type a message -> Send
4. The other Flipper receives and displays the message
5. Alternating communication (half-duplex)

**Configurable parameters:**
- Frequency
- TX power
- Data rate

**Practical use:**
- Communication between team members during a physical pentest when you do not want to use phones
- Antenna range testing
- Verification that the RF module is working correctly

> **Personal note:** I have used this as backup communication during a physical pentest in a building with thick walls where cell service was poor. It works surprisingly well at 433 MHz through 2-3 concrete walls at distances of 15-20 meters. It is not encrypted, so do not use it for sensitive communications.

### Chief Cooker

Custom RF signal generator from raw parameters.

**Operational procedure:**

1. Open Chief Cooker
2. Select parameters:
   - Frequency (e.g., 433.92 MHz)
   - Modulation (OOK/FSK)
   - Data rate
   - Bit sequence to transmit
3. Generate the signal
4. Test the transmission

**Advanced use:**
- Create signals for protocols not natively supported
- Test receivers with custom patterns
- Reverse engineering: send variations of a captured signal to understand which bits control which function
- Generate test sequences for calibration

### Genie Door Recorder

Specialized recorder and replayer for Genie garage remotes (a very popular American brand).

**Technical background:**

Genie systems use a variant of the Intellicode protocol with rolling code. Some older models use fixed code DIP switches.

**Operational procedure for fixed code:**
1. Open Genie Door Recorder
2. Press the Genie remote button near the Flipper
3. The signal is captured and decoded
4. Save -> you can replay it

**For rolling code (Intellicode):**
- Capture works but replay is limited (the code has already been "consumed")
- Useful for protocol analysis, not for direct cloning

### Protocols Visualizer

Analysis tool that graphically displays the structure of decoded RF signals.

**Operational procedure:**

1. Capture a signal with Read or Read RAW
2. Open the file in the Protocols Visualizer
3. The display shows:
   - Signal waveform (high/low pulses)
   - Segmentation into: preamble, sync word, header, payload, checksum
   - Decoded bits with annotations
   - Comparison between multiple presses of the same remote
4. 

**Use in reverse engineering:**
- Identify the structure of unknown protocols
- Find the bits that change between successive presses (rolling code counter)
- Identify checksums and CRCs
- Understand timeslot lengths

> **Personal note:** The Visualizer is irreplaceable when you are trying to understand a proprietary protocol. I used it to reverse-engineer a wireless alarm system that used an undocumented protocol. By recording 10-15 different transmissions and comparing them in the Visualizer, I managed to identify the fields: sensor ID, event type (open/close/tamper), counter, and checksum.

### Sub-GHz Playlist / Playlist Creator

Management and creation of RF signal sequences for ordered playback.

**Operational procedure - Playlist Creator:**

1. Open Playlist Creator
2. Add .sub files from the saved library
3. Set the playback order
4. Configure the delay between signals (ms)
5. Save the playlist

**Operational procedure - Playlist Player:**

1. Open Sub-GHz Playlist
2. Select the saved playlist
3. Press Play
4. Signals are transmitted in sequence

**Operational use:**
- Test multiple devices in sequence (e.g., test 5 different gates)
- Routine automation (open gate + garage + light)
- Demos during security presentations
- Stress testing: replay the same signal N times to test the receiver's robustness

### Sub-GHz Remote

Remote control interface with configurable buttons.

**Operational procedure:**

1. Open Sub-GHz Remote
2. Assign a .sub file to each on-screen button
3. Use the buttons to transmit the corresponding signals
4. Supports up to 4-8 buttons (depends on firmware)

**Practical use:**
- Create a "universal remote" for your RF devices
- Have quick access to the most-used signals
- During a pentest: immediate access to test signals

### Sub-GHz Scheduler

Time-based automation of RF transmissions.

**Operational procedure:**

1. Open Scheduler
2. Select the .sub file to transmit
3. Configure:
   - Interval (e.g., every 10 minutes)
   - Number of repetitions (or infinite)
   - Initial delay
4. Start the scheduler
5. The Flipper transmits automatically according to the schedule

**Operational use:**
- Persistence testing: verify whether a receiver desynchronizes after repeated transmissions
- Home automation: send commands at regular intervals
- RF traffic simulation for environmental testing

### Sub-GHz Test

Diagnostic suite for verifying RF hardware functionality.

**Available tests:**
- **TX Test:** transmits a test signal and verifies power
- **RX Test:** listens and measures the RSSI of the received signal
- **Antenna Test:** verifies antenna response across different frequencies
- **Crystal Test:** verifies oscillator stability

**When to use it:**
- After dropping the device
- If you suspect hardware issues
- To compare performance before/after a hardware modification
- To verify that an external antenna is working correctly

### Shapshup

Creative tool for modifying recorded RF signals.

**Available operations:**
- **Stretch:** extend pulse durations (e.g., +5%, +10%)
- **Compress:** shorten pulse durations
- **Invert:** invert highs and lows
- **Slice:** cut a portion of the signal
- **Repeat:** repeat a pattern N times

**Use in reverse engineering:**
- Test a receiver's tolerance to signal variations
- Understand the timing margin of the protocol
- Create signal variants for fuzzing tests

### Marmalade / Music to Sub-GHz Radio

Creative tools for converting audio/music into RF signals.

**Limited practical use** - mostly demonstrative. Converts audio patterns into OOK sequences that can be "listened to" by an RF receiver tuned to the same frequency (like a DIY AM radio).

### FRSSCAN

Scanner for FrSky protocols (drone/RC model radio controllers).

**Supported protocols:** FrSky D8, D16, ACCESS

**Use:** analysis of RC model radio controllers. Useful for:
- Understanding which frequencies a drone uses
- Analyzing the binding between transmitter and receiver
- Studying telemetry protocols

### SubGHz Toolkit

Collection of quick utilities in a single interface:
- Quick frequency scan
- Quick recording with automatic save
- Protocol format conversion
- Quick visualization of saved .sub files

---
