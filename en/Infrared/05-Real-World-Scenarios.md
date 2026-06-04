## Penetration Testing Scenarios

### Scenario 1: Turning Off TVs/Displays in Target Environments

**Context:** During a physical penetration test, you have access to conference rooms, reception areas, lobbies, and common areas of the target building. TV screens, digital signage monitors, and projectors are displaying information or are simply turned on.

**Objective:** Demonstrate unauthorized control of electronic devices in the environment.

**Operational procedure:**

1. **Reconnaissance:** Identify the devices present and, if possible, their brands (logo, rear label, visible model number)
2. **Preparation:** Load the universal IR database onto the Flipper (pre-installed) and any brand-specific .ir files for the identified brands
3. **Approach:** Get within 3-5 meters of the target display. In a conference room during a break, in the lobby during quiet hours
4. **Execution - Method 1 (known brand):** Go to Infrared -> Universal Remotes -> TV, select the brand, send Power Off
5. **Execution - Method 2 (unknown brand):** Use IR Blaster or Universal Remotes in "search all brands" mode - the Flipper will cycle through dozens of Power Off codes
6. **Verification:** The display turns off
7. **Documentation:** Note the brand, model, successful distance, time

**Operational risks:**
- Turning off a display can attract attention (IT staff, security, employees)
- In environments with video surveillance, the gesture of pointing the Flipper might be recorded
- Some displays have "Power Lock" protection that prevents power-off via IR

**Mitigations:**
- Execute during low-traffic moments
- Keep the Flipper hidden in your hand (it is small - it does not look like an obvious remote)
- Aim toward the ceiling to use the bounce if you do not want to point directly

> **Personal note:** This is the most common IR use in physical pentesting and the most spectacular in the report. "The operator turned off displays in the Executive conference room on the 3rd floor without any authorization or credentials." Clients immediately understand the impact. But be careful: in many engagements the pentest scope does not explicitly include control of IR devices - always verify with the client before proceeding.

### Scenario 2: Comfort Manipulation / Social Engineering via AC

**Context:** In a social engineering engagement, you need to create a situation that justifies an access request or creates confusion.

**Objective:** Manipulate environmental comfort to influence people's behavior.

**Operational procedure:**

1. **Reconnaissance:** Identify the type of air conditioner and, if possible, the brand
2. **Capture:** If you have temporary access to the room (e.g., you are a "visitor"), capture the original remote's signals for key commands (Power, Temp Up, Temp Down, Mode)
3. **Action:** Lower the temperature to 18 degrees or raise it to 30 degrees (in summer), then "offer to help" fix the problem
4. **Social engineering variant:** Set the air conditioner to an uncomfortable mode, then introduce yourself as an HVAC technician who came to fix the issue

**Practical examples:**
- **Room too hot:** People leave the room, giving you temporary access to documents, unlocked screens, hardware
- **Room too cold:** People seek help at reception, creating an opening to access normally staffed areas
- **Fan noise at maximum:** Creates annoyance and justifies the intervention of a "technician"

**Limitations:**
- Requires identification of the specific AC protocol (not always trivial)
- The Flipper's limited TX range requires access to the room
- Some corporate ACs are centrally controlled (BMS - Building Management System) and the IR remote is disabled

### Scenario 3: Reverse Engineering a Proprietary Remote

**Context:** You encounter a device with a proprietary IR remote - alarm system, legacy access control, industrial display, conference room AV system.

**Objective:** Capture and replay signals to gain control of the device.

**Operational procedure:**

1. **Initial capture:** With IR Decoder, capture every button on the original remote
2. **Analysis:** Verify whether the protocol is recognized or if it is RAW
3. **Mapping:** Create an .ir file with all captured commands, naming them clearly
4. **Testing:** Replay each signal and verify that the device responds correctly
5. **Advanced reverse engineering (if necessary):**
   - Use IR Scope to analyze the waveforms
   - Compare different commands to identify the structure (header, address, command, checksum)
   - If the protocol uses a checksum, identify it by capturing systematic variations (e.g., all numbers 0-9)
   - Try generating synthetic commands by modifying the command bits

**Real example - Conference room AV system:**

A Crestron AV system in a conference room uses an IR remote to:
- Turn the projector on/off
- Select the input (HDMI1, HDMI2, VGA)
- Control the volume
- Lower/raise the motorized screen

By capturing all remote commands, you can control the entire AV system - including lowering the screen, turning on the projector, and selecting the desired input. In a pentest, this demonstrates control of AV infrastructure without credentials.

### Scenario 4: IR as a Covert Channel for Data Exfiltration

**Context:** In advanced scenarios, IR can be used as a covert channel for exfiltrating small amounts of data.

**Principle:** If you have physical access to a computer and can install a program (or exploit one already present), you can make the webcam's IR LED or an external IR LED connected via USB emit signals that encode data. A second Flipper Zero (or other IR receiver) positioned in line-of-sight captures these signals.

**Channel characteristics:**
- **Very low bandwidth:** a few bytes per second at best
- **Undetectable by firewalls or IDS:** IR traffic does not pass through the network
- **Requires line-of-sight:** the receiver must "see" the transmitter
- **Detectable by visual inspection:** an active IR LED is visible with digital cameras (smartphones)

**Practical limitations:**
- Speed is too low for mass exfiltration (no databases, no files)
- Useful only for high-value, small-size data: cryptographic keys, passwords, hashes, small tokens
- The line-of-sight requirement limits possible scenarios
- In the real world, Bluetooth or unintentional RF emissions are much more practical covert channels

**This scenario is more theoretical than practical** - I include it because it is discussed in the security literature and demonstrates an important principle: any communication channel, even IR, can be abused.

### Scenario 5: Attack on Digital Signage Systems

**Context:** Commercial buildings, airports, train stations, shopping centers, and corporate reception areas use digital signage displays to show information, advertising, schedules, and maps.

**Objective:** Demonstrate that an attacker can interfere with the digital signage system.

**Operational procedure:**

1. **Reconnaissance:** Identify the displays (Samsung, LG, NEC, Sony are the most common in digital signage)
2. **Identification:** Digital signage displays are often commercial TVs with HDMI input from a media player. The display's IR receiver is almost always active
3. **Possible actions:**
   - **Power off:** Power Off the display
   - **Input change:** Switch from HDMI (digital signage content) to TV tuner, USB, or another empty input
   - **Volume change:** Raise the volume to maximum or mute it
   - **OSD menu access:** Open the display's service menu to modify settings
4. **Impact:**
   - Display off = information unavailable for customers/passengers
   - Display on wrong input = "No Signal" screen or unexpected input
   - OSD menu visible = reveals the display's brand and model, potentially useful for further attacks

**Countermeasures you might encounter:**
- IR receiver covered with opaque tape (the simplest and most effective)
- Display in "Hotel/Hospitality" mode with limited IR
- Media player that automatically turns on/restores the display after a power-off
- Displays mounted at unreachable height (>5m) - outside the Flipper's TX range

> **Personal note:** Digital signage systems are the easiest and most widespread IR target. In my experience, at least 70-80% of digital signage displays in Italian companies have the IR receiver fully accessible and without any protection. A fact that always generates a reaction in pentest reports. The most effective countermeasure - a piece of black adhesive tape over the IR receiver - costs nothing and is 100% effective.

---

## The Universal IR Database

### What Is the Flipper Zero's IR Database

The Flipper Zero includes a **universal IR database** pre-installed that contains thousands of codes for TVs, projectors, soundbars, and air conditioners from hundreds of different brands.

The main file is **`tv.ir`** (and analogous files for ACs and other devices), stored in the firmware and accessible through the Universal Remotes function.

### Database Structure

The database is organized by **manufacturer and model** and contains for each device at least:

- **Power On/Off** (the most universal command)
- **Volume Up/Down**
- **Mute**
- **Channel Up/Down**
- **Input Select**

Each entry specifies:
- **Protocol** (NEC, RC5, RC6, SIRC, Samsung, etc.)
- **Carrier frequency**
- **Address** of the device
- **Command** for each function

### .ir File Format

A Flipper `.ir` file has a simple text format:

```
Filetype: IR signals file
Version: 1

name: Power
type: parsed
protocol: NEC
address: 04 00 00 00
command: 08 00 00 00

name: Vol_Up
type: parsed
protocol: NEC
address: 04 00 00 00
command: 02 00 00 00

name: Custom_Signal
type: raw
frequency: 38000
duty_cycle: 0.330000
data: 9000 4500 560 560 560 1690 560 560 560 560 560 1690 560 1690 560 560 560 43000
```

**Fields for decoded signals (`type: parsed`):**
- `protocol`: protocol name
- `address`: device address (in hex format, LSB first, padded to 4 bytes)
- `command`: command (same format)

**Fields for RAW signals (`type: raw`):**
- `frequency`: carrier frequency in Hz
- `duty_cycle`: carrier duty cycle (0.0-1.0)
- `data`: sequence of timings in microseconds (burst, space, burst, space...)

### How to Add New Devices

**Method 1 - Direct capture:**

1. Use Learn New Remote to capture the original remote's commands
2. Signals are automatically saved to the SD card
3. Organize files in the `/ext/infrared/` folder with descriptive names

**Method 2 - Download from Flipper-IRDB:**

The [Flipper-IRDB](https://github.com/Lucaslhm/Flipper-IRDB) repository on GitHub is the largest collection of `.ir` files for the Flipper Zero:

- Thousands of devices cataloged by brand and model
- Organized by category (TV, AC, Audio, Projector, Fan, Fireplace, LED, etc.)
- Files ready to copy to the SD card

**Method 3 - Manual creation:**

You can create `.ir` files with a text editor following the format above. Useful when:
- You have codes from an online database (e.g., LIRC, irdb.tk)
- You want to combine signals from different sources
- You are doing reverse engineering and want to test variations

### The Built-in Universal Database

In addition to `.ir` files on the SD card, the Flipper has a firmware-integrated database used by the **Universal Remotes** function. This database:

- Contains Power Off/On codes for **hundreds of TV brands**
- Is organized to maximize coverage with the fewest number of transmissions
- Cycles through the most common codes first, then less widespread ones
- Can take from 2-3 seconds (common brand) to 1-2 minutes (rare brand) to find the right code

> **Personal note:** The built-in database is impressive - in my experience it covers approximately 85-90% of TVs I have encountered in Italian corporate environments. Samsung, LG, Sony, Philips, Panasonic, Sharp, Hisense, TCL - all present. Failures typically occur with very cheap or very niche brands, or with professional displays that use RS-232 or IP protocols instead of IR.

---

## Cross-Reference - Multi-Vector Scenarios

| Scenario | Related Module | Link | How They Connect |
|----------|---------------|------|------------------|
| Hotel: IR + NFC | NFC | [05-Real-World-Scenarios](../NFC/05-Real-World-Scenarios.md) | Hotel NFC card for room access + IR for TV/AC (social engineering, disruption) |
| Conference room + WiFi | WiFi-Marauder | [05-Real-World-Scenarios](../WiFi-Marauder/05-Real-World-Scenarios.md) | IR to turn off display/projector + WiFi scan of the AV network |
| Digital signage + BadUSB | USB/Bad USB | [05-Real-World-Scenarios](../USB/Bad%20USB/05-Real-World-Scenarios.md) | IR for display menu access -> BadUSB on the media player's USB port |
| HVAC + Sub-GHz | Sub-GHz | [05-Real-World-Scenarios](../Sub-GHz/05-Real-World-Scenarios.md) | HVAC systems: IR for local units + Sub-GHz for wireless temperature sensors |
| IR + BLE | Bluetooth | [05-Real-World-Scenarios](../Bluetooth/05-Real-World-Scenarios.md) | Smart devices: traditional IR + BLE for advanced configuration/control |
