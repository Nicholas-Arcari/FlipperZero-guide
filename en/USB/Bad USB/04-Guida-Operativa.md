## Tool by Tool - Operational Guide

### BadUSB (Main)

**Operational procedure:**

1. Prepare the script (.txt) and place it in `/ext/badusb/` on the Flipper's SD card
2. Open Apps -> USB -> Bad USB
3. Select the script
4. The Flipper shows a preview of the payload
5. Connect the Flipper to the target PC via USB-C
6. Press the center button to **start execution**
7. The Flipper types the commands in sequence
8. When finished, disconnect the Flipper

**Important settings:**
- **Keyboard Layout:** MUST match the target system's layout (IT, US, UK, DE, etc.)
- **USB VID/PID:** customizable for evasion
- **Device Name:** customizable (e.g. "Logitech Keyboard")

### Demos

Demonstration scripts for different OSes showcasing HID capabilities:
- **demo_windows** - opens PowerShell, displays system info
- **demo_macos** - opens Terminal, displays system info
- **demo_linux_gnome** - opens GNOME terminal
- **demo_android** - opens browser
- **demo_chromeos** - opens Crosh
- **demo_ios** - limited functionality

### CVE-2024-1086 Linux / wget

Educational demonstrations of the CVE-2024-1086 exploit (Linux kernel nf_tables use-after-free):

- Script that downloads and executes the PoC on vulnerable distributions
- **WARNING:** for study purposes only on your own VMs, never on production systems
- The wget version downloads the payload from a remote server

### Kiosk Evasion Bruteforce

Scripts that automatically try key combinations to escape kiosk mode:

**Tested combinations:**
```
ALT F4          - close application
CTRL W          - close tab/window
ALT TAB         - switch application
CTRL-ALT DELETE - task manager (Windows)
F11             - toggle fullscreen
CTRL ESC        - Start menu
GUI D           - show desktop
CTRL-SHIFT ESC  - direct task manager
ALT SPACE       - window menu
F5              - refresh
CTRL L          - address bar (browser kiosk)
CTRL T          - new tab (browser kiosk)
CTRL-SHIFT T    - reopen closed tab
CTRL N          - new window
```

**Use in pentesting:** test the robustness of kiosk terminals (ATMs, information totems, check-in kiosks, POS terminals).

> **Personal note:** Kiosk evasion is surprisingly effective. I've tested kiosks in airports, hotels, and shopping malls. About 40% allow escape with simple key combinations. The most vulnerable ones are those based on Chrome in kiosk mode - Ctrl+L to access the URL bar and then browse freely. The Flipper makes the test automatic and fast.

### WiFi Stealer ORG

Educational script that extracts saved WiFi passwords from the system:

**Windows:**
```
netsh wlan show profiles
netsh wlan show profile name="SSID" key=clear
```

**macOS:**
```
security find-generic-password -wa "SSID"
```

**Linux:**
```
cat /etc/NetworkManager/system-connections/*.nmconnection | grep psk=
```

The payload typically saves the output to a temporary file or sends it to a remote server.

### Mouse Test

HID scripts that test mouse emulation:
- Linear, circular, or random movements
- Left/right click
- Scroll
- Useful for verifying that HID emulation works correctly

---


---

# Scripts and Payloads - Complete Reference

For the complete guide to creating DuckyScript payloads, including templates for Windows, macOS, Linux, ChromeOS, and Android, see: [Script/README.md](Script/README.md)
