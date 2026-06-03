# Arsenale BadUSB - Payload Pronti per Flipper Zero

Raccolta di payload DuckyScript testati e pronti all'uso per penetration testing autorizzato. Ogni script è commentato, categorizzato e include indicazioni su target OS, privilegi richiesti e rilevamento EDR.

> **DISCLAIMER:** Questi payload sono destinati ESCLUSIVAMENTE a penetration testing autorizzato. L'uso senza autorizzazione scritta è reato (Art. 615-ter, 615-quater C.P.). Testa SEMPRE in VM prima di usarli in campo.

---

## Struttura

```
payloads/
├── windows/
│   ├── recon/                 # Raccolta informazioni sistema e rete
│   ├── reverse-shell/         # Shell remote PowerShell, netcat, meterpreter
│   ├── credential-harvest/    # Estrazione password WiFi, browser, SAM
│   ├── persistence/           # Scheduled task, registry, startup
│   ├── exfiltration/          # Invio dati a server remoto
│   ├── evasion/               # AMSI bypass, Defender disable, EDR evasion
│   └── privilege-escalation/  # UAC bypass, admin shell
├── macos/                     # Payload per macOS
├── linux/                     # Payload per Linux
└── multi-os/                  # Payload cross-platform
```

## Come Usare

1. Copia il file `.txt` nella cartella `/ext/badusb/` della SD del Flipper
2. Sul Flipper: Bad USB → seleziona il file → Run
3. **IMPORTANTE:** Modifica i placeholder prima dell'uso:
   - `ATTACKER_IP` → il tuo IP/dominio C2
   - `ATTACKER_PORT` → la porta del tuo listener
   - `WEBHOOK_URL` → il tuo webhook (Discord, Slack, custom)
   - `EXFIL_URL` → il tuo server di raccolta dati

## Matrice Payload

| Payload | OS | Privilegi | EDR Evasion | Tempo | Rischio Detect |
|---------|-----|----------|-------------|-------|----------------|
| **RECON** | | | | | |
| System Recon | Win | User | No | 8s | Basso |
| Network Enum | Win | User | No | 10s | Basso |
| WiFi Passwords | Win | Admin | No | 6s | Medio |
| AD Recon | Win | User | No | 12s | Medio |
| **REVERSE SHELL** | | | | | |
| PS Reverse Shell | Win | User | Si | 5s | Alto |
| PS Encrypted Shell | Win | User | Si | 6s | Medio |
| Netcat Shell | Win | User | No | 8s | Alto |
| LOLBin Shell | Win | User | Si | 7s | Basso |
| **CREDENTIAL HARVEST** | | | | | |
| WiFi Cred Dump | Win | Admin | No | 6s | Medio |
| Browser Creds | Win | User | No | 8s | Alto |
| SAM Dump | Win | Admin | No | 10s | Alto |
| Mimikatz Loader | Win | Admin | Si | 8s | Critico |
| **PERSISTENCE** | | | | | |
| Registry Run | Win | User | No | 5s | Medio |
| Scheduled Task | Win | Admin | No | 6s | Medio |
| WMI Persistence | Win | Admin | Si | 8s | Basso |
| Startup Folder | Win | User | No | 5s | Alto |
| **EVASION** | | | | | |
| Defender Disable | Win | Admin | Si | 5s | Alto |
| AMSI Bypass | Win | User | Si | 4s | Medio |
| ETW Blind | Win | Admin | Si | 5s | Basso |
| **EXFILTRATION** | | | | | |
| File Exfil | Win | User | No | 10s | Medio |
| Clipboard Steal | Win | User | No | 6s | Basso |
| **macOS** | | | | | |
| macOS Reverse Shell | Mac | User | No | 8s | Medio |
| macOS Recon | Mac | User | No | 10s | Basso |
| **Linux** | | | | | |
| Linux Reverse Shell | Linux | User | No | 6s | Medio |
| SSH Key Exfil | Linux | User | No | 8s | Basso |

## Risorse Esterne

| Repository | Contenuto |
|------------|-----------|
| [I-Am-Jakoby/Flipper-Zero-BadUSB](https://github.com/I-Am-Jakoby/Flipper-Zero-BadUSB) | Payload avanzati con GUI, exfiltration, evasion |
| [UberGuidoZ/Flipper/BadUSB](https://github.com/UberGuidoZ/Flipper/tree/main/BadUSB) | Raccolta community di payload testati |
| [FalsePhilosopher/badusb](https://github.com/FalsePhilosopher/badusb) | Payload organizzati per OS e obiettivo |
| [hak5/usbrubberducky-payloads](https://github.com/hak5/usbrubberducky-payloads) | Repository ufficiale Hak5 Rubber Ducky |
| [aleff-github/my-flipper-shits](https://github.com/aleff-github/my-flipper-shits) | Payload Flipper per Windows/macOS/Linux |
