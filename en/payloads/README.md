# BadUSB Arsenal - Ready-to-Use Payloads for Flipper Zero

Collection of tested DuckyScript payloads ready for use in authorized penetration testing. Each script is commented, categorized, and includes indications on target OS, required privileges, and EDR detection.

> **DISCLAIMER:** These payloads are intended EXCLUSIVELY for authorized penetration testing. Unauthorized use is a criminal offense (Art. 615-ter, 615-quater Italian Penal Code). ALWAYS test in a VM before using in the field.

---

## Structure

```
payloads/
├── windows/
│   ├── recon/                 # System and network information gathering
│   ├── reverse-shell/         # PowerShell, netcat, meterpreter remote shells
│   ├── credential-harvest/    # WiFi, browser, SAM password extraction
│   ├── persistence/           # Scheduled task, registry, startup
│   ├── exfiltration/          # Data exfiltration to remote server
│   ├── evasion/               # AMSI bypass, Defender disable, EDR evasion
│   └── privilege-escalation/  # UAC bypass, admin shell
├── macos/                     # macOS payloads
├── linux/                     # Linux payloads
└── multi-os/                  # Cross-platform payloads
```

## How to Use

1. Copy the `.txt` file to the `/ext/badusb/` folder on the Flipper's SD card
2. On the Flipper: Bad USB → select the file → Run
3. **IMPORTANT:** Modify placeholders before use:
   - `ATTACKER_IP` → your C2 IP/domain
   - `ATTACKER_PORT` → your listener port
   - `WEBHOOK_URL` → your webhook (Discord, Slack, custom)
   - `EXFIL_URL` → your data collection server

## Payload Matrix

| Payload | OS | Privileges | EDR Evasion | Time | Detection Risk |
|---------|-----|----------|-------------|------|----------------|
| **RECON** | | | | | |
| System Recon | Win | User | No | 8s | Low |
| Network Enum | Win | User | No | 10s | Low |
| WiFi Passwords | Win | Admin | No | 6s | Medium |
| AD Recon | Win | User | No | 12s | Medium |
| **REVERSE SHELL** | | | | | |
| PS Reverse Shell | Win | User | Yes | 5s | High |
| PS Encrypted Shell | Win | User | Yes | 6s | Medium |
| Netcat Shell | Win | User | No | 8s | High |
| LOLBin Shell | Win | User | Yes | 7s | Low |
| **CREDENTIAL HARVEST** | | | | | |
| WiFi Cred Dump | Win | Admin | No | 6s | Medium |
| Browser Creds | Win | User | No | 8s | High |
| SAM Dump | Win | Admin | No | 10s | High |
| Mimikatz Loader | Win | Admin | Yes | 8s | Critical |
| **PERSISTENCE** | | | | | |
| Registry Run | Win | User | No | 5s | Medium |
| Scheduled Task | Win | Admin | No | 6s | Medium |
| WMI Persistence | Win | Admin | Yes | 8s | Low |
| Startup Folder | Win | User | No | 5s | High |
| **EVASION** | | | | | |
| Defender Disable | Win | Admin | Yes | 5s | High |
| AMSI Bypass | Win | User | Yes | 4s | Medium |
| ETW Blind | Win | Admin | Yes | 5s | Low |
| **EXFILTRATION** | | | | | |
| File Exfil | Win | User | No | 10s | Medium |
| Clipboard Steal | Win | User | No | 6s | Low |
| **macOS** | | | | | |
| macOS Reverse Shell | Mac | User | No | 8s | Medium |
| macOS Recon | Mac | User | No | 10s | Low |
| **Linux** | | | | | |
| Linux Reverse Shell | Linux | User | No | 6s | Medium |
| SSH Key Exfil | Linux | User | No | 8s | Low |

## External Resources

| Repository | Content |
|------------|---------|
| [I-Am-Jakoby/Flipper-Zero-BadUSB](https://github.com/I-Am-Jakoby/Flipper-Zero-BadUSB) | Advanced payloads with GUI, exfiltration, evasion |
| [UberGuidoZ/Flipper/BadUSB](https://github.com/UberGuidoZ/Flipper/tree/main/BadUSB) | Community collection of tested payloads |
| [FalsePhilosopher/badusb](https://github.com/FalsePhilosopher/badusb) | Payloads organized by OS and objective |
| [hak5/usbrubberducky-payloads](https://github.com/hak5/usbrubberducky-payloads) | Official Hak5 Rubber Ducky repository |
| [aleff-github/my-flipper-shits](https://github.com/aleff-github/my-flipper-shits) | Flipper payloads for Windows/macOS/Linux |
