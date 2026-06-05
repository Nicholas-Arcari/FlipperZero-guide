## 8. Troubleshooting

### 8.1 Firmware Flash Issues

**Problem: "Failed to connect to ESP32: No serial data received"**

Possible causes:
- The device is not in boot mode
- Faulty USB cable or charge-only cable (without data lines)
- USB drivers not installed
- Serial port occupied by another process

Solutions:
1. Verify the boot sequence: hold BOOT, press RESET, release BOOT
2. Try a different USB cable (preferably short, < 1m)
3. Verify drivers: `dmesg | tail -20` on Linux after connecting
4. Close programs that might be using the serial port (screen, minicom,
   Arduino IDE, another serial terminal)
5. On Linux: `fuser /dev/ttyACM0` to identify processes using the port

**Problem: Flash completed but firmware does not work**

Possible causes:
- Wrong firmware for the ESP32 model
- Incorrect flash offsets
- Flash corrupted by an interruption during writing

Solutions:
1. Verify the exact chip model: `esptool.py chip_id`
2. Completely erase the flash: `esptool.py erase_flash`
3. Reflash with the correct firmware for your model
4. Verify the offsets (different between ESP32, ESP32-S2, ESP32-S3)

**Problem: "A fatal error occurred: Chip is esp32s2 not esp32"**

Cause: specifying the wrong chip in the esptool command.

Solution: use `--chip auto` for automatic detection, or specify
the correct chip:
```bash
esptool.py --chip auto --port /dev/ttyACM0 chip_id
```

**Problem: Flash is extremely slow or freezes**

Possible causes:
- Baud rate too high for the USB connection
- USB hub degrading the signal
- EMI interference on the cable

Solutions:
1. Reduce the baud rate: use `--baud 115200` instead of 921600
2. Connect directly to the computer's USB port (no hub)
3. Use a shielded, short USB cable

### 8.2 Flipper-ESP32 Serial Communication Issues

**Problem: the WiFi Marauder app shows "Connecting..." indefinitely**

Possible causes:
- Devboard not properly connected to the GPIO pins
- Firmware not flashed on the ESP32
- Baud rate mismatch between Flipper and Marauder firmware
- UART pins not aligned

Solutions:
1. Turn off the Flipper, disconnect the devboard, reconnect firmly,
   turn it back on
2. Verify that the Marauder firmware is actually installed on the ESP32
   (connect the ESP32 to the PC and open a serial terminal at 115200 baud --
   it should show the Marauder prompt)
3. Verify that the Flipper firmware is up to date
4. Try resetting the ESP32 (RESET button on the devboard)

**Problem: illegible output or corrupted characters on the Flipper**

Cause: baud rate mismatch.

Solution: Marauder firmware uses 115200 baud by default. The app on the Flipper
must be configured to the same baud rate. If you modified the baud rate
in the Marauder firmware, adjust the app accordingly.

**Problem: commands sent from the Flipper produce no response**

Possible causes:
- Flipper TX not connected to ESP32 RX (or vice versa)
- ESP32 in an error state or crash

Solutions:
1. Verify the pin mapping (TX <-> RX must be crossed)
2. Reset the ESP32 (RESET button or power cycle)
3. If the problem persists, reflash the firmware

### 8.3 Issues During Use

**Problem: scan does not find networks known to be present**

Possible causes:
- ESP32 antenna too far from the target
- Channel not covered by the scan
- Radio interference

Solutions:
1. Move closer to the target
2. Verify that the scan covers all channels (1-13)
3. In environments with strong interference (microwaves, Bluetooth, etc.),
   move to a different location or wait

**Problem: handshake/PMKID capture is empty or incomplete**

Possible causes:
- AP does not support PMKID (for sniffpmkid)
- Client did not reconnect after the deauth
- Sniffer was not active at the time of the handshake
- Wrong channel

Solutions:
1. For PMKID: not all APs support it, switch to handshake capture
2. For handshake: verify that the sniffer was active BEFORE the deauth
3. Verify the sniffer channel matches the target AP channel
4. Retry the attempt with a different client (if available)
5. Move closer to both the AP and the client

**Problem: Evil Portal does not display the login page**

Possible causes:
- HTML template not correctly loaded on the SD card
- HTML file too large for the ESP32 memory
- The victim's device uses DNS-over-HTTPS (DoH) which bypasses DNS spoofing

Solutions:
1. Verify the HTML file path on the SD card
2. Reduce the template size (remove heavy images, minimize CSS)
3. DoH: on devices with DoH enabled (Firefox, recent Chrome) DNS spoofing does
   not work. There is no direct solution -- it is a limitation of the attack.

**Problem: Flipper battery drains rapidly**

Cause: the ESP32 devboard draws significant current, especially during active TX.

Solutions:
1. Use a powerbank connected to the Flipper via USB
2. Limit the active operation time
3. Turn off the devboard when not in use
4. For long operations (Evil Portal, wardriving), plan for battery life
   (the Flipper battery with an active devboard lasts approximately 2-4 hours)

**Problem: .pcap file is corrupted or cannot be opened in Wireshark**

Possible causes:
- Capture interrupted abruptly (Flipper shutdown or devboard disconnection)
- SD card full
- SD card filesystem corruption

Solutions:
1. Always stop the capture with `stopscan` before disconnecting the devboard
2. Verify free space on the SD card before starting
3. Use a good quality SD card (class 10 or higher)
4. If the file is partially corrupted, try: `pcapfix capture.pcap`

> Personal note: 50% of the issues I have had with Marauder were related
> to the USB cable during flashing. A charge-only cable without data lines appears
> to work (the LED turns on) but is not recognized by the PC. I have wasted
> hours looking for software problems when the issue was a 2-euro cable.
> I now always keep a USB cable marked "DATA" in my pentesting backpack.

---

## 9. References and Resources

### Repositories and Documentation

- **Marauder Firmware**: https://github.com/justcallmekoko/ESP32Marauder
- **Marauder Wiki**: https://github.com/justcallmekoko/ESP32Marauder/wiki
- **Windows Flasher**: https://github.com/UberGuidoZ/Flipper/tree/main/Wifi_DevBoard/FZ_Marauder_Flasher
- **Linux/macOS Flasher**: https://github.com/SkeletonMan03/FZEasyMarauderFlash
- **Flipper Zero Docs**: https://docs.flipper.net/

### Complementary Tools for Cracking

- **hashcat**: https://hashcat.net/hashcat/
- **aircrack-ng**: https://www.aircrack-ng.org/
- **hcxtools**: https://github.com/ZerBea/hcxtools
- **Wireshark**: https://www.wireshark.org/

### Wordlists and Cracking Resources

- **rockyou.txt**: included in Kali Linux, contains ~14 million passwords
- **SecLists**: https://github.com/danielmiessler/SecLists
- **CrackStation**: https://crackstation.net/crackstation-wordlist-password-cracking-dictionary.htm

### Training and Certifications

For those who want to dive deeper into wireless pentesting at a professional level:
- **OSWP** (Offensive Security Wireless Professional) -- certification
  specific to wireless pentesting
- **CEH** (Certified Ethical Hacker) -- covers wireless security among its
  various modules
- **IEEE 802.11-2020** -- the complete WiFi protocol specification
  (reference document, not a course)

### Standards and Regulations

- **IEEE 802.11-2020**: complete WiFi protocol specification
- **IEEE 802.11w-2009**: Protected Management Frames
- **IEEE 802.11i-2004**: security enhancements (WPA2)
- **WPA3 Specification**: https://www.wi-fi.org/security
- **GDPR**: EU Regulation 2016/679
- **Italian Penal Code**: artt. 615-ter, 617-quater, 617-quinquies, 640-ter

---

## Final Notes

WiFi Marauder with Flipper Zero is a powerful tool but with inherent
limitations. The ESP32 is not a replacement for a laptop with a dedicated
WiFi card (Alfa AWUS036ACH, ASUS USB-AC68, etc.) for professional
penetration testing. Its strengths are:

- **Discretion**: fits in a pocket, no one notices it
- **Speed of deployment**: operational in seconds
- **Portability**: built-in battery, no laptop needed
- **Reconnaissance**: excellent for the initial phase of an engagement

Its limitations:

- **Range**: small antenna, limited reach
- **2.4 GHz only**: cannot see 5 GHz networks
- **Computing power**: the ESP32 cannot perform cracking (that happens offline)
- **Storage**: limited SD card for long captures
- **Single-band**: cannot do fast channel hopping like multi-antenna cards

The experienced pentester uses the Flipper as a complementary tool in their
arsenal, not as their sole tool. It is the perfect tool for initial
reconnaissance, quick PMKID grabs, and social engineering scenarios with Evil Portal
where discretion is essential.

> Personal note: after 3 years of use in real engagements, my rule
> is simple: Flipper for reconnaissance and first contact, laptop for everything
> else. The Flipper tells me what is there and how it is configured. The laptop does the
> heavy lifting. Together, they are a formidable combination. Neither of them
> alone is sufficient for a serious wireless engagement.

---

*This guide is maintained for educational and professional training purposes
in the field of cybersecurity. Every technique must be applied in
compliance with the law and professional ethics.*
