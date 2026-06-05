## Troubleshooting and Limitations

### "The payload doesn't type anything"

- Verify that the Flipper is recognized as a USB keyboard (keyboard icon on the PC)
- Check the USB-C cable (not all cables support data)
- Verify that the layout is correct in the BadUSB menu

### "Special characters are wrong"

- The Flipper's layout does not match the target PC's layout
- Solution 1: change the layout in the BadUSB menu
- Solution 2: use ALTCHAR/ALTSTRING to input characters via Alt code (layout independent)
- Solution 3: use Base64 encoding to avoid special characters

### "The payload is too slow / too fast"

- Adjust DEFAULT_DELAY
- Use specific DELAY before critical commands (window opening, UAC, etc.)
- On slow machines, use 1000-2000ms delays after GUI r

### "PowerShell gets blocked"

- The EDR detected the command -> use evasion techniques
- Try cmd.exe instead of PowerShell
- Use LOLBins (mshta, certutil, bitsadmin)
- Encode the payload in Base64

### "The PC has USB disabled"

- Check if it's a hardware (BIOS) or software (GPO) block
- If software: it might be bypassable (but outside BadUSB scope)
- If hardware: BadUSB won't work - a different approach is needed

---

## Personal Experience

> **Personal note - The Italian layout:** The most recurring problem in Italy is the keyboard layout. I've lost entire engagements because the payload had @ in the wrong position. Now I ALWAYS test on a VM with IT layout before every engagement. The AltGr+at-sign combination on IT layout is different from Shift+2 on US layout. A single wrong character and the payload fails completely.

> **Personal note - Delay timing:** The delay after GUI r (Win+R) is the most critical. On a new PC with SSD, 300ms is enough. On an old corporate PC with a mechanical drive and heavy antivirus, you may need up to 2000ms. I use 500ms as default and adjust based on the target. Better to wait an extra half second than lose the entire payload.

> **Personal note - Effective drop attack:** The most effective technique I've used is the "coffee break attack": I identify an employee who goes to the bar/coffee machine leaving their PC unlocked, I approach the desk, connect the Flipper, execute the payload (8 seconds), disconnect and walk away. Total exposure time: less than 15 seconds. It works surprisingly often because people don't lock their PCs.

> **Personal note - Kiosk escape on totems:** I've tested kiosks in 6 different contexts (airport, hotel, hospital, shopping mall, bank, restaurant). 4 out of 6 were vulnerable to simple key combinations (Ctrl+L on the browser, Alt+F4, F11). The Flipper with the bruteforce script finds the escape in less than 30 seconds. Always an appreciated finding in reports because kiosks often have access to the internal network.

> **Personal note - EDR evasion:** CrowdStrike and SentinelOne block most direct PowerShell payloads. The technique that works best for me is using certutil to download a legitimate (signed) executable that in turn loads the payload via DLL sideloading. The initial BadUSB command appears innocuous and the EDR doesn't block it. Requires more preparation but has a much higher success rate.
