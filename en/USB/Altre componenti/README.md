# USB - Other Components

Flipper Zero USB components beyond BadUSB: device emulation, hardware security, data transfer, and interaction tools.

---

## U2F - Hardware Security Key

The Flipper Zero can function as a **FIDO U2F hardware security key** for two-factor authentication (2FA).

**How it works:**

U2F (Universal 2nd Factor) is a FIDO Alliance standard that uses asymmetric cryptography:
1. The user registers the Flipper on a web service (Google, GitHub, etc.)
2. The Flipper generates a unique key pair (public/private) for that service
3. The public key is sent to the service
4. On the next login, the service sends a challenge to the Flipper
5. The user presses the Flipper's button to authorize
6. The Flipper signs the challenge with the private key
7. The service verifies the signature with the public key -> access authorized

### WebAuthn and FIDO2 - Technical Context

The Flipper Zero implements the **FIDO U2F** standard, which is the predecessor to **FIDO2/WebAuthn**. The main difference:

| Aspect | U2F (FIDO 1.x) | FIDO2/WebAuthn |
|--------|-----------------|----------------|
| Authentication | Second factor only | First factor (passwordless) possible |
| Protocol | Basic challenge-response | Extensions, attestation, resident keys |
| Flipper Support | Full | Partial (U2F subset only) |
| Supported browsers | Chrome, Firefox, Edge, Safari | All modern browsers |

The Flipper acts as an **external authenticator** compliant with the CTAP (Client to Authenticator Protocol) specification. When the browser receives a WebAuthn request from the server, it sends the challenge via USB HID to the Flipper, which signs it with the private key bound to that specific domain (origin binding).

**Origin binding is the key to everything:** the cryptographic key is bound to the exact domain (e.g. `accounts.google.com`). If an attacker creates a phishing site on `accounts-google.com`, the Flipper simply doesn't respond - it has no key for that domain. This makes U2F **immune to phishing** by design, not by user education.

### Complete Operational Procedure

1. Connect the Flipper via USB to the PC
2. Open Apps -> USB -> U2F
3. The Flipper registers as a U2F HID device
4. On the website: go to Security Settings -> Add security key
5. When prompted, press the button on the Flipper
6. Registration complete

**Detailed initial setup:**

- On first U2F use, the Flipper generates a cryptographic seed saved on the SD card in the `.key` file
- This seed is the root of all derived keys - **if you lose the SD card, you lose all U2F keys**
- The Flipper supports registration on multiple services simultaneously
- Each service gets a unique key pair derived from the seed + domain

**Tested and compatible services:**
- Google Account
- GitHub
- GitLab
- Microsoft Account
- Cloudflare
- Bitwarden / 1Password
- Facebook
- Dropbox
- NAS Synology (DSM 7+)

### U2F vs SMS 2FA - Security Comparison

| Criterion | SMS 2FA | TOTP (Google Auth) | U2F Hardware |
|-----------|---------|---------------------|--------------|
| Phishing resistance | None | Low | **Total** |
| SIM swap attack | Vulnerable | Immune | Immune |
| Man-in-the-Middle | Vulnerable | Vulnerable | **Immune** (origin binding) |
| Requires physical presence | No | No | **Yes** |
| Operational cost | Low | Low | Medium (physical device) |
| Account recovery | Easy | Medium | Complex |
| Compliance (PCI DSS, NIST) | Discouraged | Accepted | **Recommended** |

### Use in Pentesting - Phishing Resistance Testing

In a social engineering engagement, testing whether the target organization uses U2F/FIDO2 is fundamental:

1. **Reconnaissance:** identify whether the target supports U2F (check IdP policy, Azure AD, Okta)
2. **Phishing campaign:** if employees only use SMS/TOTP, a phishing proxy (Evilginx2, Modlishka) captures credentials AND the second factor in real time
3. **Validation:** if the target uses U2F, the phishing proxy fails - the browser doesn't send the challenge to the wrong domain
4. **Report:** document the risk difference between SMS/TOTP and U2F to justify the investment in hardware keys

> **Personal note:** I conducted a phishing test on a company with 200 employees. The 15 users with U2F keys (executives) were immune to my Evilginx2 proxy. The other 185 with SMS 2FA? 47 entered the code on the fake page. The report practically wrote itself - the client deployed YubiKeys to the entire company the following quarter. The Flipper Zero configured as U2F is perfect for demonstrating the concept to management during the results presentation.

**Security advantages:**
- The private key NEVER leaves the device
- Immune to phishing (the key is bound to the site's domain)
- Requires physical presence (button press)
- Open and auditable standard

> **Personal note:** I use the Flipper as a backup U2F key for my critical accounts (GitHub, Google, cloud services). It's not its primary use, but it's convenient to have a hardware key always in the kit without carrying a separate YubiKey. I register it as a "second factor" on all accounts where it's supported.

---

## Mass Storage - USB Drive

The Flipper exposes the SD card as a standard USB drive.

### Operational Procedure

1. Open Apps -> USB -> Mass Storage
2. The PC recognizes the Flipper as a USB drive
3. Browse files on the Flipper's SD card
4. Copy files to/from the Flipper

**Technical details:**
- The Flipper exposes the SD card as a USB Mass Storage Class (MSC) device
- The visible filesystem is the microSD's (FAT32)
- Transfer speed is limited by the SD card's SPI bus (~1-2 MB/s)
- During Mass Storage mode, the Flipper's other functions are suspended
- The Flipper appears with a standard VID/PID - some EDR solutions classify it as "removable storage"

### Use in Pentesting - Exfiltration and Deployment

**As an exfiltration tool:**

In a physical pentest, Mass Storage becomes your external drive without looking like an external drive. The procedure:

1. **Pre-loading:** before the engagement, load onto the SD card:
   - Compiled payloads (reverse shell, keylogger, persistence)
   - Portable tools (Mimikatz, LaZagne, SharpHound, Sysinternals Suite)
   - PowerShell/Bash automation scripts
2. **On-site:** connect the Flipper to the target PC in Mass Storage mode
3. **Deployment:** copy tools from the SD card to the target
4. **Exfiltration:** copy results (hash dumps, sensitive files, BloodHound reports) to the SD card
5. **Switch:** switch to BadUSB to execute the deployed tools

**Automated file drop (combo with BadUSB):**

The most powerful technique is the Mass Storage + BadUSB combo:
1. The Flipper starts in Mass Storage -> the PC mounts the SD card as `E:\`
2. The BadUSB script (pre-loaded) copies the payload: `copy E:\payload.exe %TEMP%\svchost.exe`
3. The payload is executed by BadUSB: `%TEMP%\svchost.exe`
4. Result: deployment of complex binaries impossible via keystroke injection alone

**Recommended SD card structure for pentesting:**

```
/mass_storage/
├── payloads/
│   ├── windows/
│   │   ├── rev_shell.exe
│   │   ├── mimikatz.exe
│   │   └── sharphound.ps1
│   └── linux/
│       ├── linpeas.sh
│       └── rev_shell.elf
├── tools/
│   ├── sysinternals/
│   └── nirsoft/
├── exfil/     ← empty folder for exfiltrated data
└── scripts/
    ├── deploy.ps1
    └── cleanup.ps1
```

> **Personal note:** The problem with Mass Storage is speed. 1-2 MB/s means copying Mimikatz (1.2 MB) takes about a second, but a 50 MB SAM dump takes almost a minute. In a physical pentest, every second counts. Always prepare compressed and minimized files. And keep the `exfil/` folder empty and ready - you don't want to waste time creating directories while you're in the target.

---

## HID File Transfer

File transfer via HID protocol without mounting the SD card as mass storage.

### How It Works

HID transfer uses the USB HID (Human Interface Device) channel to send data byte-by-byte. The Flipper doesn't present itself as a storage device but as a generic HID device, and data is transferred through HID reports.

**Advantages over Mass Storage:**
- Does not appear as a removable drive (less detectable)
- Bypasses USB mass storage blocking policies
- More discreet transfer
- Does not trigger DLP (Data Loss Prevention) alerts on many endpoints

**Disadvantages:**
- Very low speed (the HID channel is not designed for bulk transfer)
- Requires companion software on the receiving PC
- Does not work out-of-the-box - the receiver must have the client installed

### Transfer Procedure

**From Flipper to PC:**
1. Install the companion software on the PC (available on the firmware's GitHub)
2. Connect the Flipper via USB
3. On the Flipper: Apps -> USB -> HID File Transfer
4. Select the file from the SD card to transfer
5. The companion software on the PC receives the file and saves it to the specified directory

**From PC to Flipper:**
1. In the companion software, select "Send to Flipper"
2. Choose the file from the PC
3. The file is transferred via HID and saved on the Flipper's SD card

### Use in Pentesting

The real value of HID File Transfer is in environments with **USB Mass Storage disabled via Group Policy**. Many companies block USB storage devices but allow HID (because they need mice and keyboards). This channel bypasses that restriction.

> **Personal note:** In practice, HID File Transfer is slow and cumbersome. If I have physical access to the target and Mass Storage is blocked, I prefer using BadUSB to download tools via the network (certutil, curl, wget). I only use HID transfer when the network is also restricted - a rare but possible case in air-gapped or heavily segmented environments.

---

## Mouse Jiggler

Simulates micro mouse movements to prevent PC standby/lock.

### Operational Procedure

1. Connect the Flipper via USB
2. Open Apps -> USB -> Mouse Jiggler
3. The Flipper moves the cursor by 1-2 pixels at regular intervals
4. The PC does not go to sleep/lock

**Technical parameters:**
- Movement: 1-2 pixels in a pseudo-random pattern (not linear to avoid detection)
- Interval: every 15-30 seconds (configurable in firmware)
- The Flipper presents itself as a standard USB HID mouse
- Does not interfere with normal PC use (movements too small to be noticed by the user)

### Use in Pentesting - Keeping the Session Active

The typical scenario:
1. Physically access the target PC (absent employee, unattended workstation)
2. The PC is unlocked - you have a limited time window
3. Connect the Flipper with Mouse Jiggler active
4. The auto-lock policy (typically 5-15 minutes) is neutralized
5. You have all the time needed to:
   - Install persistence
   - Extract credentials
   - Map the internal network
   - Download sensitive files

**Specific scenarios:**
- **Keeping a session active on a target PC after unlocking it**
- **Preventing the lock screen during long operations** (download, scanning, file copying)
- **Demo during the report presentation:** show the client that lock timeout policies can be circumvented with a 15-euro USB device
- **Combination with BadUSB:** launch the BadUSB script, then activate the Jiggler to keep the session while the payload works in the background

### Detection and Countermeasures

**How it gets detected:**
- Advanced EDR solutions (CrowdStrike Falcon, SentinelOne) can monitor USB input patterns
- Perfectly regular movements every N seconds are suspicious
- Windows Event ID 6416 audit log (PnP device connected) records the new HID device
- Specialized tools (Mouse Jiggler Detector) analyze movement patterns

**Corporate countermeasures:**
- USB device whitelisting (only authorized VID/PIDs)
- GPO that forces lock regardless of input (absolute timer)
- Physical presence sensors at the workstation
- Alerts on new HID device connections outside business hours

**How to evade detection (for testing purposes):**
- Randomized movement patterns (not fixed intervals)
- Variable movement amplitude
- Combination with occasional clicks and scrolling
- Custom firmware with unpredictable timing

> **Personal note:** The Mouse Jiggler is underrated. In an engagement where I had 30 minutes of access to a PC (the employee was in a meeting), the Jiggler allowed me to keep the session active while I installed the payload and copied files. Without it, the PC would have locked after 5 minutes of inactivity (corporate policy). Simple but indispensable.

> **Personal note:** A tip: connect the Flipper behind the PC, on the rear USB port. If the employee comes back and sees a Flipper Zero attached to the monitor, your cover is blown. Behind the tower, under the desk, in a hidden USB port - it's a small device, use it to your advantage.

---

## USB HID Autofire

Automatic repeated key pressing at high frequency.

**Use:** input testing, gaming, automation of repetitive actions.

---

## USB Consumer Control

Sending HID multimedia commands:
- Volume up/down, mute
- Play, pause, stop, next, prev
- Brightness up/down

**Practical use:** control the PC as a multimedia remote via USB.

---

## USB Remote

Graphical interface to control the PC's keyboard and mouse from the Flipper's display.

**Features:**
- Mouse movement with the Flipper's joystick
- Left/right click
- Quick key sending
- Scrolling

**Use:** remote control of a PC (e.g. connected to a projector) without a separate mouse/keyboard.

---

## USB MIDI

The Flipper becomes a USB MIDI controller:

- Sending MIDI notes (note on/off, velocity, channel)
- Compatible with DAWs (Ableton, FL Studio, Logic, Reaper)
- Useful for prototyping custom music controllers

### Technical Details

The Flipper registers as a **USB MIDI Class Compliant** device, which means it requires no dedicated drivers on any operating system. The MIDI-over-USB protocol uses 3-byte messages:

| Byte | Function | Range |
|------|----------|-------|
| Status | Message type + channel | 0x80-0xFF |
| Data 1 | Note / Controller | 0-127 |
| Data 2 | Velocity / Value | 0-127 |

**Supported messages:**
- Note On / Note Off (with velocity)
- Control Change (CC)
- Program Change
- Pitch Bend

**Creative uses:**
- **Audio triggers in presentations:** configure the Flipper to send MIDI notes that trigger audio samples in Ableton during a live demo
- **Custom OBS controller:** map MIDI notes to scenes/transitions in OBS Studio for live streaming
- **Artistic automation:** use the Flipper as a minimal sequencer for interactive installations
- **MIDI device testing:** verify that a MIDI receiver correctly interprets standard messages

> **Personal note:** It has no direct applications in pentesting, but I used it once creatively: during a results presentation for an assessment, I mapped different alarm sounds to MIDI notes on the Flipper. Every time I showed a critical vulnerability, I pressed the button and a siren sound played. The CISO was not amused, but the point got across.

---

## BarCode Scanner Emulator

The Flipper emulates a USB barcode reader:

- Sends strings as if they were scanned by a barcode reader
- The PC receives the data as keyboard input (standard for barcode readers)
- Useful for testing POS and inventory systems

### How It Works

USB barcode readers are, from the operating system's perspective, **USB keyboards**. When they scan a barcode, they convert the content into a keystroke sequence and send it to the PC, typically followed by an `ENTER`. The Flipper replicates this behavior exactly.

**Difference from BadUSB:** the BarCode Scanner Emulator sends data formatted as barcode reader output (with industry-standard prefixes/suffixes), while BadUSB sends generic keystrokes. Some POS systems accept input ONLY if the format matches that of a registered barcode reader.

**Supported barcode formats:**
- UPC-A (12 digits - US retail products)
- EAN-13 (13 digits - EU/Italian retail products)
- Code 128 (alphanumeric - logistics, inventory)
- Code 39 (limited alphanumeric - industrial/military sector)
- QR (represented as text string)

### Use in Pentesting - Injection via Barcode

**Scenario 1 - POS Injection:**
Many POS (Point of Sale) systems accept barcode reader input without sanitization. The flow:
1. The operator scans the product barcode
2. The POS receives the string (e.g. `8001234567890`)
3. The string is used to look up the product in the database

**The attack:** if the POS doesn't sanitize input, you can send:
- Control characters (`\t`, `\n`) to navigate the interface
- Escape sequences to exit the POS application
- SQL strings if the backend is vulnerable to SQLi (rare but possible)
- Path traversal if the barcode is used for file operations

**Scenario 2 - Kiosk/Totem:**
Information totems and kiosks often have an integrated barcode reader for scanning loyalty cards or tickets. If the reader is physically accessible:
1. Disconnect the original barcode reader from the kiosk
2. Connect the Flipper to the same USB port
3. Use the BarCode Scanner Emulator to send arbitrary strings
4. Test the kiosk application for input injection

> **Personal note:** The BarCode Scanner Emulator is a niche tool but devastating in the right context. In a test on a retail chain, I discovered that the checkout software accepted any string from the "barcode reader," including tab and newline. With a crafted barcode containing `\t\t\t\nSHUTDOWN /s /t 0`, I could crash the register. The fix was trivial (whitelist of numeric characters), but the finding was classified as critical because an attacker could print a malicious barcode on a label and stick it on any product.

---

## Xbox360 USB Game Controller

Xbox 360 controller emulation via XInput:
- All axes, buttons, and triggers
- Natively recognized by Windows
- Compatible with games and emulators

### Technical Details

The Flipper emulates Microsoft's **XInput** protocol, which is the de facto standard for game controllers on Windows. Unlike the older DirectInput, XInput is natively recognized without additional drivers.

**Emulated inputs:**
- 2 analog sticks (X/Y for each)
- 2 analog triggers (LT, RT)
- D-pad (8 directions)
- 10 digital buttons (A, B, X, Y, LB, RB, Back, Start, L3, R3)
- Vibration (haptic feedback) - not supported by the Flipper (lacks the motor)

**Practical use:**
- Controller compatibility testing on applications
- Input automation in applications that only accept gamepad
- Controller emulation for systems that require XInput for interaction

---

## Lego Dimensions Toy Pad

USB Toy Pad emulator for the Lego Dimensions game:
- Figure and vehicle emulation
- Character selection from the menu

---

## Flip TDI

Interface for TDI (Test Data In) communications and JTAG debugging:
- Read/write data on the JTAG bus
- Debugging of devices with TDI interface

---

## MTP (Media Transfer Protocol)

Access to Flipper files via MTP protocol:
- Recognized as a multimedia device
- Compatible with Windows/macOS/Linux
- Alternative to Mass Storage for file transfer

---

## Portal of Flipper / Clippy

Creative and interactive modules:
- **Portal of Flipper:** USB interface for games and experimental apps
- **Clippy:** USB assistant with retro animations

---

## Real-World Pentest Scenarios - USB Tools in Action

### Scenario 1 - "The Conference" (Social Engineering + Mass Storage + Jiggler)

**Context:** physical pentest on an office with 50 employees. The objective is to demonstrate the risk of uncontrolled physical access.

**Execution:**
1. I present myself as an external IT technician for "printer maintenance" (pretext agreed with the client)
2. I identify an unlocked PC at an empty workstation (employee on lunch break)
3. I connect the Flipper with **Mouse Jiggler** active -> the session stays active
4. I switch to **Mass Storage** -> I copy documents from the Desktop and Documents folders to the SD card
5. I switch to **BadUSB** -> I execute a script that:
   - Opens hidden PowerShell
   - Downloads SharpHound from a C2 server
   - Runs the BloodHound collection
   - Saves the output to a temporary folder
6. I switch back to **Mass Storage** -> I copy the SharpHound output to the SD card
7. I disconnect the Flipper, leave the office

**Result:** complete access to Active Directory mapping, cached credentials, sensitive documents. Total time: 12 minutes. No alerts generated.

**Report finding:** "The absence of USB device whitelisting, inadequate lock screen policies, and lack of physical access controls allow an attacker with physical access to extract sensitive data and map the entire AD infrastructure in less than 15 minutes."

### Scenario 2 - "The Totem" (BarCode Scanner + BadUSB)

**Context:** security assessment of a self-checkout system in a retail chain.

**Execution:**
1. I identify that the totems use standard USB barcode readers (Honeywell Voyager)
2. During low-traffic hours, I access the back of the totem (rear panel not locked)
3. I disconnect the original barcode reader, connect the Flipper in **BarCode Scanner Emulator** mode
4. I send a series of barcodes with payloads:
   - Barcodes with `TAB` characters to navigate the POS interface fields
   - Barcodes with `ESC` to attempt application escape
   - Barcodes with long strings (2000+ chars) for buffer overflow testing
5. The POS system doesn't sanitize input - I manage to escape the application and reach the underlying Windows desktop
6. From there, I use **BadUSB** (quick switch) to open a prompt and check privileges - the POS runs as SYSTEM

**Result:** SYSTEM access on a terminal connected to the retailer's internal network. From that point, potential access to the entire point-of-sale network.

### Scenario 3 - "The Air-Gap" (HID File Transfer + U2F + Mouse Jiggler)

**Context:** pentest on an air-gapped network in an industrial environment (SCADA/ICS). No internet access, USB Mass Storage disabled.

**Execution:**
1. Access to the control room is authorized (visitor badge). The supervisory PC is unlocked with the operator present
2. Under the pretext of "verifying the security configuration," I ask to connect the Flipper
3. **Mouse Jiggler** active to prevent lock during the "verification"
4. USB Mass Storage is blocked by GPO - the Flipper is not mounted as a drive
5. I switch to **HID File Transfer** - the HID channel is not blocked (needed for mice/keyboards)
6. I slowly transfer (~50 KB/s) an audit script to the machine
7. The script collects: network configuration, active processes, services, local users, SCADA version
8. I transfer the results via HID File Transfer to the Flipper's SD card

**Result:** complete audit of the SCADA environment without violating USB Mass Storage policies (technically). The report highlights that blocking Mass Storage without blocking HID is an incomplete measure.

> **Personal note:** These scenarios are not made up - they are simplified versions of real engagements. The Flipper Zero is a tool, not a solution. The real value is in preparation: knowing which USB mode to use, when to switch, and having everything pre-loaded. In a physical pentest, every second of hesitation increases the risk of being discovered. Practice, practice, practice.

---

## Troubleshooting - Common Problems

### The PC does not recognize the Flipper as a USB device

**Symptoms:** no connection notification, no device in Device Manager.

**Solutions:**
1. Check the USB cable - use a data cable, not a charge-only cable (classic mistake)
2. Try a different USB port - avoid USB hubs, connect directly to the motherboard
3. Restart the Flipper (Settings -> Restart)
4. Update the firmware - old versions have known USB bugs
5. On Linux: check permissions (`lsusb` to confirm the device is visible, check udev rules)

### Mass Storage does not mount the SD card

**Symptoms:** the Flipper is in Mass Storage mode but the PC shows no drive.

**Solutions:**
1. Verify that the SD card is inserted and working (test in the Flipper's Storage section)
2. On Windows: open Disk Management (diskmgmt.msc) and check if the drive appears without a letter
3. Format the SD card in FAT32 if needed (the Flipper does not support exFAT/NTFS)
4. Check if a GPO blocks USB Mass Storage - in that case, it's by design

### U2F does not work on a site

**Symptoms:** the site does not recognize the Flipper as a security key.

**Solutions:**
1. Verify that the site supports U2F/FIDO (not just TOTP)
2. Use Chrome or Edge (more stable U2F support compared to Firefox)
3. Make sure to press the Flipper button when prompted (30-second timeout)
4. If you updated the firmware, the U2F key may have been regenerated - re-register the Flipper on the site
5. Check that the `.key` file exists on the SD card

### Mouse Jiggler is detected by EDR

**Symptoms:** security alert on the target PC after connecting the Flipper.

**Solutions:**
1. The Flipper's VID/PID is well-known - some EDR solutions recognize it specifically
2. Use firmware with custom VID/PID (spoofed as Logitech or Microsoft mouse)
3. Reduce the frequency of movements (overly regular movements are suspicious)
4. Evaluate whether the detection risk is acceptable for the engagement - sometimes it's better not to use it

### Very low Mass Storage transfer speed

**Symptoms:** file transfer at less than 500 KB/s.

**Solutions:**
1. Maximum speed is ~1-2 MB/s - it's a hardware limitation of the SPI bus
2. Use a fast SD card (Class 10 / UHS-I minimum)
3. Avoid transferring many small files - compress into a single archive (.zip/.tar)
4. If you need to transfer large amounts of data, use a dedicated SD card reader and extract the microSD from the Flipper

### BarCode Scanner Emulator is not accepted by the POS

**Symptoms:** the POS system does not recognize the input as coming from a barcode reader.

**Solutions:**
1. Some POS systems verify the barcode reader's VID/PID - the Flipper may not match
2. Try adding standard reader prefix/suffix (many use a specific ASCII prefix)
3. Verify the barcode format expected by the POS (UPC-A, EAN-13, Code 128)
4. Some modern POS systems use readers with point-to-point encryption - in that case the Flipper cannot emulate them

> **Personal note:** 80% of USB problems I've encountered in the field are solved with three things: different cable, different port, updated firmware. It sounds trivial, but the amount of time I've wasted in engagements because of a USB cable that was charge-only is embarrassing. Now I always keep three tested data cables in my kit, with labels.

---

## Personal Experience

> **Personal note - U2F as backup:** Configuring the Flipper as a U2F key is one of the first things I do after setup. It costs zero time and adds a layer of security to your accounts. The only downside is that if you lose the Flipper, you also lose the U2F key - so always keep an alternative recovery method.

> **Personal note - Mass Storage + BadUSB combo:** The most effective technique for deploying complex payloads: first switch to Mass Storage to copy the .exe, then switch to BadUSB to execute it. Requires manual switching between USB modes, but the result is much more powerful than typing commands via HID.

> **Personal note - BarCode injection:** I tested a supermarket POS system (authorized) using the BarCode Scanner Emulator. The system accepted any string from the "barcode reader" without sanitization. By sending a barcode with control characters followed by a command, it was possible to exit the POS application and access the underlying Windows desktop. Critical finding.

> **Personal note - Complete USB kit:** In my pentest backpack I always carry the Flipper with the SD card pre-loaded with tools and payloads. But I also carry a "clean" backup USB drive. The Flipper is versatile but slow in transfer. If I have a lot to exfiltrate (>100 MB), I switch to a traditional drive. The Flipper is the initial infiltration tool, not the pack mule.

> **Personal note - Order of operations:** In a physical pentest with USB access, my standard flow is: (1) Mouse Jiggler to hold the active session, (2) Mass Storage to deploy tools, (3) BadUSB to execute them, (4) Mass Storage to exfiltrate results. Four switches in 10-15 minutes. Practice it until it becomes automatic - in the field you don't have time to think about the sequence.
