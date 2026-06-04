## Tool by Tool - Operational Guide

### Infrared (Main Application)

The Infrared application built into the firmware is the primary tool for all IR operations.

#### Learn New Remote

Step-by-step procedure for capturing an IR signal:

1. Go to **Infrared** from the main menu
2. Select **Learn New Remote**
3. Point the source remote control toward the Flipper's **IR receiver** (the dark window on the top of the device)
4. Press the button you want to record on the remote
5. The Flipper will display the result:
   - If the protocol is recognized: shows **protocol name**, **address**, and **command**
   - If the protocol is not recognized: shows **RAW** with the total duration
6. Press **Save** to save the signal
7. Assign a **descriptive name** (e.g., "Power", "Vol_Up", "Temp_24")
8. Repeat for each button you want to capture

**Operational tips:**
- Keep the source remote at **5-15 cm** from the Flipper for capture - not too close (saturation), not too far (errors)
- Press the button **once** with a firm press - do not hold it down (to avoid repeat codes)
- If you get a RAW result for a protocol that should be decoded, try getting closer and repeating
- For AC signals, make sure to capture the entire frame (they are long - wait for the Flipper to confirm complete reception)

#### Send (Universal Remote)

The Flipper includes a pre-loaded database of IR signals for the most common devices:

1. Go to **Infrared** -> **Universal Remotes**
2. Select the category (TV, AC, Audio, etc.)
3. The Flipper will send common signals for that category
4. For TVs: sends Power Off sequences for the most widespread brands

#### Saved Remotes

Saved remote management:

1. Go to **Infrared** -> **Saved Remotes**
2. Select the remote file
3. Choose the command to send
4. Press **Send** - the Flipper will transmit the signal

Files are saved in `/ext/infrared/` on the SD card in `.ir` format.

### Cross Remote

Multi-vendor universal remote that allows you to **combine commands from different devices** into a single virtual remote.

**Typical use case:** In a conference room you have a Samsung TV, an Epson projector, and an LG soundbar. With Cross Remote you can create a profile that turns all three on/off with a single remote.

**Procedure:**

1. Open **Cross Remote**
2. Create a new profile or select an existing one
3. Add commands from different remotes (saved `.ir` files or captured on the spot)
4. Assign each command to a virtual button
5. Use the profile to control all devices

> **Personal note:** Cross Remote is the most practical operational tool for physical pentesting. You prepare in advance a profile with "Power Off" commands for TVs, projectors, and displays of the most common brands in the target building. In a few seconds you can turn off everything in a conference room. It is much faster than searching for the right .ir file for each device.

### IR Decoder

Analysis and reverse engineering tool for received IR signals.

**Features:**
- Shows the identified **protocol** (NEC, RC5, RC6, SIRC, Samsung, etc.)
- Displays **address and command** in hexadecimal format
- For RAW signals: shows the **complete timing sequence**
- Allows analyzing the **frame structure** for unknown protocols

**Procedure:**

1. Open **IR Decoder**
2. Select **Start Decoding**
3. Point a remote toward the Flipper and press a button
4. Analyze the displayed data
5. Repeat for different buttons to map the entire remote

**Use in reverse engineering:**

- Capture the same button multiple times to verify consistency
- Compare different buttons to identify the structure (which bits change)
- For RC5/RC6: observe the toggle bit that changes between successive presses
- For AC signals: capture small changes (e.g., 24->25 degrees) to isolate temperature bits

### IR Scope

Built-in IR oscilloscope for waveform visualization.

**Features:**
- Displays the IR signal **waveform** in real time
- Shows **burst and space timings** graphically
- Allows analyzing the **duty cycle** and **carrier frequency**
- Useful for diagnosing timing issues

**Procedure:**

1. Open **IR Scope**
2. Point a remote toward the Flipper
3. Press a button - the waveform will appear on screen
4. Analyze the waveform: bursts (high parts), spaces (low parts)
5. Measure timings to verify protocol conformance

**Practical use:**

- Verify that a captured signal has correct timing
- Diagnose why a RAW signal is not working (bursts too short, irregular spaces)
- Compare the original remote signal with the one reproduced by the Flipper
- Identify the carrier frequency by analyzing the burst structure

### IR Remote

Application for loading and using `.ir` files as virtual remotes.

**Procedure:**

1. Open **IR Remote**
2. Navigate the SD card and select an `.ir` file
3. The application presents the commands contained in the file as buttons
4. Press the desired command to transmit it

**Managing .ir files:**

Files can be:
- Created by the Flipper via Learn New Remote
- Downloaded from online repositories (Flipper-IRDB is the largest)
- Manually created with a text editor following the correct format
- Transferred from the SD card via qFlipper or mobile app

### IR Blaster

Tool for mass or burst sending of IR signals.

**Features:**
- **Repeated and rapid** sending of IR signals
- **Burst** mode to saturate receivers
- Useful for **stress testing** IR receivers
- Can cycle through different signals rapidly

**Use case in pentesting:**

IR Blaster is the tool for the "TV-B-Gone" approach: rapidly cycling through hundreds of Power Off commands for different brands. In burst mode, the Flipper can send one command after another without pause, maximizing the probability of turning off an unknown device.

**Procedure:**

1. Open **IR Blaster**
2. Select the set of signals to transmit (or use the universal database)
3. Select the mode (single, burst, cyclic)
4. Aim toward the target device
5. Start transmission

### IR Intervalometer

Remote control for automatic triggering of DSLR and mirrorless cameras compatible with IR triggers.

**Compatible cameras:**
- Nikon (D3000, D5000, D7000 series, Z5, Z6, Z7, etc.)
- Canon (select models - many Canon cameras use radio remotes, not IR)
- Sony (Alpha series with IR receiver)
- Pentax, Olympus/OM System (models with IR receiver)
- Fujifilm (select models)

**Features:**
- Remote single shot
- Interval shooting (time-lapse) with configurable interval
- Configurable initial delay

**Procedure:**

1. Open **IR Intervalometer**
2. Select the camera manufacturer
3. Set the interval between shots (e.g., 5 seconds)
4. Set the number of shots or leave in continuous mode
5. Position the Flipper in front of the cameràs IR receiver (usually front-facing)
6. Start

> **Personal note:** The Intervalometer is a niche tool, but surprisingly useful. I have used it for time-lapse during physical surveillance in engagements - the Flipper controls a DSLR on a tripod documenting access to a building. It is not its primary use, but it works.

### IR Transfer

System for file transfer between two Flipper Zero devices using IR communication.

**Features:**
- Sending small files from one Flipper to another via IR
- No wireless connection needed (no BT, no WiFi)
- Useful in environments where radio transmissions are monitored or prohibited

**Limitations:**
- Speed is very low (IR is not designed for mass data transfer)
- Requires line-of-sight and close distance (1-3 meters)
- Suitable only for small files (IR signals, small configurations)

**Procedure:**

1. Open **IR Transfer** on both Flipper devices
2. On the sending Flipper: select **Send File** and choose the file
3. On the receiving Flipper: select **Receive**
4. Position the two Flipper devices facing each other at 50 cm - 1 meter
5. Start the transfer

### Flame RNG

Random number generator based on IR signals and stress test tool for receivers.

**Features:**
- Generates and transmits random IR signals
- Used to test the robustness of IR receivers
- Can cause unexpected behavior in devices that do not properly handle invalid signals

**Use in pentesting:**

Flame RNG can reveal vulnerabilities in IR receivers that:
- Do not properly filter malformed signals
- Crash or freeze when receiving unexpected data
- Execute unintended actions with random address/command combinations

### Specific Remotes

#### Hitachi AC Remote

Dedicated remote for Hitachi air conditioners. Implements the proprietary Hitachi protocol with long frames (typically 104 bits for the most common models).

**Features:**
- Temperature control (16-32 degrees)
- Mode (Cool, Heat, Dry, Fan, Auto)
- Fan speed
- Vane swing
- Power On/Off

#### Midea AC Remote

Remote for Midea air conditioners. The Midea protocol is relatively simple compared to other AC manufacturers (approximately 48 bits per frame), which makes it more reliable in capture and playback.

#### Mitsubishi AC Remote

Remote for Mitsubishi Electric air conditioners. 144-bit frames (18 bytes) with proprietary checksum. One of the most complex AC protocols.

#### Xbox Control

IR control for Xbox consoles (Xbox One and Xbox Series X/S). Xbox consoles have a front-facing IR receiver for media remotes.

**Available commands:**
- Power On/Off
- Guide button
- Menu navigation
- Media controls (Play, Pause, Stop, Skip)

#### Netflix TV Remote

Remote optimized for Netflix navigation on compatible smart TVs. Some TVs have a dedicated IR receiver with specific commands for streaming apps.

#### R.O.B. Control

IR control for the **Robotic Operating Buddy** (R.O.B.) for the Nintendo NES, released in 1985. The R.O.B. receives commands via IR flash from the TV screen. This tool emulates those signals.

Commands: Open Arms, Close Arms, Raise, Lower, Spin CW, Spin CCW, Test.

A niche but fascinating tool for retrogaming hardware collectors.

#### XRemote

Advanced universal remote with configurable interface. Allows you to:
- Define custom button layouts
- Combine commands from different brands
- Create macros (command sequences)
- Import/export configurations

XRemote is the most flexible tool for daily use of the Flipper as a universal remote.

### LIDAR Emulator

Emulator of IR signals similar to those emitted by proximity sensors and low-cost LIDAR.

**Context:** Many robots, robotic vacuums, parking systems, and barriers use IR sensors to detect obstacles. These sensors emit IR pulses and measure the reflection to calculate distance.

**Features:**
- Emits IR patterns that simulate the presence of an obstacle at configurable distances
- Can fool simple IR proximity sensors
- Useful for testing security systems based on IR sensors

**Limitations:**
- Only works with simple IR sensors (not with real time-of-flight LIDAR)
- The Flipper's LED power limits the operational distance
- More sophisticated sensors (e.g., ToF LIDAR) cannot be fooled with this method

---
