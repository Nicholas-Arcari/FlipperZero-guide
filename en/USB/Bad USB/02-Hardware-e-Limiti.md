## Hardware and Real-World Limitations

### Flipper USB Specifications

- **USB-C 2.0** with HID, CDC, Mass Storage support
- **Default VID/PID:** customizable in the firmware (useful for evasion)
- **Typing speed:** configurable, default ~100-150 characters/second
- **Keyboard layout:** supports US, UK, DE, FR, IT, ES and many others
- **Mouse support:** the Flipper can also emulate a USB HID mouse

### Real-World Limitations

**Keyboard layout:** the payload must match the keyboard layout of the target system. A script written for US layout will not work on a PC with IT layout (special characters are in different positions). The Flipper supports layout selection in the BadUSB menu.

**Speed vs reliability:** typing too fast can cause missed or out-of-order characters, especially on slow or virtualized machines. Adding delays between commands is essential.

**Lock screen:** on a PC with an active lock screen, BadUSB can type the password IF you know it, but it cannot bypass authentication.

**USB lock/whitelist:** some enterprise environments block unknown USB devices (USB device control, endpoint protection). The Flipper gets blocked if the VID/PID is not on the whitelist.

**Modern antivirus:** while HID input itself is not blocked, the executed commands (e.g. powershell -enc ...) can be intercepted by the EDR. Target-specific evasion is required.

> **Personal note:** Keyboard layout is the most common problem. In Italy, 90% of PCs have an Italian (IT) layout which has @ on AltGr+Q, [ on AltGr+E, etc. If the payload is written for US layout, all special characters will be wrong. I ALWAYS test the payload on my PC with the same layout as the target before the engagement.

---
