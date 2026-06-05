## Technical Fundamentals

### What is BadUSB

BadUSB exploits the fact that computers blindly trust USB devices that identify themselves as keyboards. When you connect the Flipper Zero via USB and activate BadUSB, the computer sees it as a **USB HID keyboard** and accepts all "keystrokes" as legitimate user input.

The Flipper executes pre-programmed scripts that type commands at superhuman speed - typically hundreds of characters per second. In less than 3 seconds it can:
- Open a terminal/PowerShell
- Type and execute arbitrary commands
- Download and execute malware
- Exfiltrate data
- Modify system configurations

### How It Works at the USB Level

1. The Flipper presents itself to the PC as a **USB HID Keyboard** device (class 0x03, subclass 0x01, protocol 0x01)
2. The operating system's generic HID driver recognizes it automatically - no additional drivers needed
3. The USB stack negotiates: VID/PID, endpoint, descriptor
4. The Flipper sends **HID reports** containing keycodes (e.g. 0x04 = 'à, 0x28 = ENTER)
5. The operating system processes the keycodes as if a physical user were pressing the keys
6. No antivirus or EDR intercepts input from a USB keyboard - it is a trusted channel

### Why It Is So Effective

- **Implicit trust:** operating systems trust USB keyboards - there is no native way to distinguish a real keyboard from a Flipper
- **Speed:** the Flipper types faster than any human - the user has no time to react
- **Universality:** works on Windows, macOS, Linux, ChromeOS, Android (OTG), and partially on iOS
- **No files on disk:** commands are typed, not downloaded as files - difficult for traditional AV to detect
- **Pre-lock screen:** some payloads work even on the lock screen (e.g. USB HID at login)

> **Personal note:** BadUSB is the Flipper's most powerful physical pentest tool. In a typical engagement, if I manage to get 5 seconds of physical access to an unlocked PC, I can install a persistent reverse shell. The key is payload preparation - it must be perfect on the first attempt because you won't get a second chance.

---
