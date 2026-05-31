# BadUSB - Overview

Modulo di emulazione **USB HID** (Human Interface Device) per attacchi di keystroke injection. Il Flipper Zero si presenta come una tastiera USB e digita comandi automaticamente. Supporta DuckyScript per lo sviluppo di payload cross-platform.

**Emulazione:** USB HID (tastiera) | **Linguaggio:** DuckyScript | **VID/PID:** configurabile | **Target OS:** Windows, macOS, Linux, ChromeOS, Android

---

## Contenuti

| # | File | Descrizione |
|---|------|-------------|
| 01 | [Fondamenti Tecnici](01-Fondamenti-Tecnici.md) | USB HID protocol, descriptors, keystroke injection, USB enumeration |
| 02 | [Hardware e Limiti](02-Hardware-e-Limiti.md) | Flipper come USB HID, VID/PID spoofing, typing speed, limiti reali |
| 03 | [DuckyScript e Payload](03-Protocolli.md) | DuckyScript syntax, comandi, ALT codes, ALTSTRING, payload per Windows/macOS/Linux |
| 04 | [Guida Operativa](04-Guida-Operativa.md) | Step-by-step BadUSB, esecuzione payload, configurazione + [Script e Payload](Script/README.md) |
| 05 | [Scenari Reali](05-Scenari-Reali.md) | Scenari pentest: corporate laptop compromise, kiosk exploitation, EDR bypass, physical+BadUSB combo |
| 06 | [Attacchi e Difese](06-Attacchi-e-Difese.md) | Tecniche di evasione (LOLBins, AMSI bypass, VID/PID spoofing) + contromisure (USB policies, MDM) |
| 07 | [Aspetti Legali](07-Aspetti-Legali.md) | Normativa italiana/EU per USB HID testing |
| 08 | [Esperienza Personale](08-Esperienza-Personale.md) | Troubleshooting, note dal campo, errori da evitare |

---

## Quick Reference - DuckyScript Comandi Base

| Comando | Funzione | Esempio |
|---------|----------|---------|
| `DELAY` | Pausa (ms) | `DELAY 1000` |
| `STRING` | Digita testo | `STRING cmd.exe` |
| `ENTER` | Premi Invio | `ENTER` |
| `GUI` | Tasto Windows/Cmd | `GUI r` (Esegui) |
| `ALT` | Tasto Alt | `ALT F4` |
| `CTRL` | Tasto Ctrl | `CTRL c` |
| `TAB` | Tasto Tab | `TAB` |
| `ALTSTRING` | Digita via ALT codes | `ALTSTRING ciao` |

## Quick Reference - Payload Principali

| Payload | OS | Scopo | Tempo |
|---------|-----|-------|-------|
| Reverse shell PS | Windows | Shell remota | ~5s |
| WiFi password exfil | Windows | Esfiltrazione credenziali WiFi | ~8s |
| Disable Defender | Windows | Disattivazione AV | ~3s |
| Hidden admin user | Windows | Persistenza | ~4s |
| Certutil download | Windows | Download file | ~5s |
| Terminal + curl | macOS/Linux | Reverse shell/download | ~4s |

> **Nota personale:** Il BadUSB è lo strumento più impattante in un physical pentest. 5 secondi di accesso fisico a un laptop non presidiato = shell remota. La chiave è la preparazione: payload testato, timing calibrato, pretesto credibile. L'errore più comune è non considerare il layout tastiera del target.
