# Workflow Diagrams - Operational Diagrams

Mermaid diagrams for the main workflows. GitHub renders them automatically.

---

## Physical Pentest Kill Chain

```mermaid
graph TD
    START([Engagement Start]) --> R1[Perimeter Reconnaissance]
    
    R1 --> RF[Sub-GHz Freq Analyzer]
    R1 --> WIFI[WiFi scanap/scansta]
    R1 --> BADGE[NFC/RFID Detector]
    R1 --> BLE[BLE Scanner]
    
    RF --> RF_RESULT{Signal found?}
    RF_RESULT -->|Fixed code| REPLAY[Replay Attack]
    RF_RESULT -->|Rolling code| ROLLJAM[RollJam / Rolling Flaws]
    RF_RESULT -->|Cannot decode| RAW[Read RAW]
    
    WIFI --> WIFI_RESULT{Vulnerable AP?}
    WIFI_RESULT -->|WPA2-PSK| PMKID[sniffpmkid]
    WIFI_RESULT -->|Active clients| DEAUTH[Deauth + Evil Portal]
    WIFI_RESULT -->|Open/WEP| DIRECT[Direct connection]
    
    BADGE --> BADGE_RESULT{Badge type?}
    BADGE_RESULT -->|125 kHz EM4100| CLONE_RFID[Clone to T5577]
    BADGE_RESULT -->|13.56 MHz MIFARE| DICT[Dictionary Attack]
    BADGE_RESULT -->|iButton| IBUTTON[Read + Clone RW1990]
    
    DICT --> DICT_RESULT{Keys found?}
    DICT_RESULT -->|Yes| DUMP_NFC[Full Dump]
    DICT_RESULT -->|No| MFKEY[Detect Reader + MFKey32]
    MFKEY --> DUMP_NFC
    DUMP_NFC --> CLONE_NFC[Write Magic Card Gen4]
    
    REPLAY --> ACCESS[Physical Access]
    CLONE_RFID --> ACCESS
    CLONE_NFC --> ACCESS
    IBUTTON --> ACCESS
    DEAUTH --> CREDS[WiFi Credentials]
    PMKID --> CRACK[Hashcat Crack]
    CRACK --> CREDS
    
    ACCESS --> EXPLOIT{Exploitation Vector}
    CREDS --> EXPLOIT
    
    EXPLOIT --> BADUSB[BadUSB Drop]
    EXPLOIT --> MOUSEJACK[MouseJacker]
    EXPLOIT --> IR_CTRL[IR Control Display/AC]
    EXPLOIT --> HW_HACK[SWD/I2C/SPI Dump]
    
    BADUSB --> POST[Post-Exploitation]
    MOUSEJACK --> POST
    
    POST --> PERSIST[Persistence]
    POST --> EXFIL[Exfiltration]
    POST --> PIVOT[Lateral Movement]
    
    PERSIST --> REPORT([Report])
    EXFIL --> REPORT
    PIVOT --> REPORT
    
    style START fill:#2d3436,color:#fff
    style REPORT fill:#2d3436,color:#fff
    style ACCESS fill:#e17055,color:#fff
    style POST fill:#d63031,color:#fff
```

---

## NFC Clone Pipeline

```mermaid
graph LR
    READ[NFC Read] --> ID{SAK?}
    
    ID -->|0x08| MFC1K[MIFARE Classic 1K]
    ID -->|0x18| MFC4K[MIFARE Classic 4K]
    ID -->|0x04| MFUL[MIFARE Ultralight]
    ID -->|0x44| MFULC[MIFARE UL C]
    ID -->|0x20| DESFIRE[DESFire / NTAG]
    
    MFC1K --> DICT[Dictionary Attack]
    MFC4K --> DICT
    
    DICT --> KEYS{All keys?}
    KEYS -->|Yes| FULL_DUMP[Full Dump]
    KEYS -->|No| DETECT[Detect Reader x3]
    
    DETECT --> MFKEY[MFKey32]
    MFKEY --> REREAD[Re-Read with all keys]
    REREAD --> FULL_DUMP
    
    FULL_DUMP --> WRITE[Write Magic Card Gen4]
    WRITE --> VERIFY[Verify on reader]
    
    MFUL --> DIRECT_READ[Direct Read - No crypto]
    MFULC --> PWD_ATTACK[Password Attack 3DES]
    DESFIRE --> DOCUMENT[Document as SECURE]
    
    style DESFIRE fill:#00b894,color:#fff
    style DOCUMENT fill:#00b894,color:#fff
    style FULL_DUMP fill:#e17055,color:#fff
    style WRITE fill:#d63031,color:#fff
```

---

## Sub-GHz Analysis Flow

```mermaid
graph TD
    START[RF Target] --> FREQ[Frequency Analyzer]
    FREQ --> FOUND{Frequency found}
    
    FOUND --> READ[Sub-GHz Read]
    READ --> DECODE{Decoded?}
    
    DECODE -->|Yes| PROTO{Protocol}
    DECODE -->|No| RAW[Read RAW]
    
    PROTO -->|Fixed code| FIX[Princeton/CAME/etc]
    PROTO -->|Rolling code| ROLL[KeeLoq/Nice FLO]
    PROTO -->|Unknown| ANALYZE[Manual analysis]
    
    FIX --> REPLAY[Direct replay]
    REPLAY --> SUCCESS{Works?}
    SUCCESS -->|Yes| SAVE[Save + Report]
    SUCCESS -->|No| CLOSER[Get closer < 5m]
    CLOSER --> REPLAY
    
    ROLL --> ROLLING_FLAWS[Rolling Flaws Analysis]
    ROLLING_FLAWS --> VULN{Vulnerable?}
    VULN -->|Yes| EXPLOIT_ROLL[Exploit]
    VULN -->|No| DOC_SECURE[Document as secure]
    
    RAW --> RAW_REPLAY[Replay RAW]
    RAW_REPLAY --> RAW_RESULT{Works?}
    RAW_RESULT -->|Yes| SAVE
    RAW_RESULT -->|No| BRUTE{< 16 bit?}
    BRUTE -->|Yes| BRUTEFORCE[Bruteforcer]
    BRUTE -->|No| DOC_SECURE
    
    style SAVE fill:#e17055,color:#fff
    style DOC_SECURE fill:#00b894,color:#fff
```

---

## BadUSB Attack Chain

```mermaid
graph TD
    INSERT[Insert Flipper USB] --> ENUM[HID Enumeration ~1s]
    ENUM --> OS{Target OS?}
    
    OS -->|Windows| WIN_OPEN[GUI r → PowerShell]
    OS -->|macOS| MAC_OPEN[GUI SPACE → Terminal]
    OS -->|Linux| LIN_OPEN[CTRL ALT T → Terminal]
    
    WIN_OPEN --> PHASE1{Phase 1}
    MAC_OPEN --> PHASE1
    LIN_OPEN --> PHASE1
    
    PHASE1 -->|Recon| RECON[System/Network Enum]
    PHASE1 -->|Direct Shell| SHELL[Reverse Shell]
    PHASE1 -->|Evasion First| EVASION[AMSI Bypass + Defender Off]
    
    EVASION --> SHELL
    
    SHELL --> C2[C2 Connection]
    C2 --> PHASE2{Phase 2}
    
    PHASE2 --> CRED[Credential Harvest]
    PHASE2 --> PERSIST[Persistence]
    PHASE2 --> EXFIL[Exfiltration]
    PHASE2 --> PRIVESC[Privilege Escalation]
    
    CRED --> WIFI_DUMP[WiFi Passwords]
    CRED --> SAM[SAM/LSASS Dump]
    CRED --> BROWSER[Browser Creds]
    
    PERSIST --> REG[Registry Run]
    PERSIST --> SCHTASK[Scheduled Task]
    PERSIST --> WMI[WMI Subscription]
    
    EXFIL --> WEBHOOK[Webhook/Discord]
    EXFIL --> C2_EXFIL[Via C2 Channel]
    
    PRIVESC --> UAC[UAC Bypass]
    PRIVESC --> ADMIN_USER[Create Admin User]
    
    style INSERT fill:#2d3436,color:#fff
    style C2 fill:#d63031,color:#fff
    style EVASION fill:#e17055,color:#fff
```

---

## WiFi Marauder Workflow

```mermaid
graph TD
    CONNECT[ESP32 → Flipper GPIO] --> SCAN[scanap]
    SCAN --> LIST[AP List]
    LIST --> SELECT[select -a N]
    
    SELECT --> ATTACK{Attack type}
    
    ATTACK --> PMKID_PATH[sniffpmkid]
    ATTACK --> DEAUTH_PATH[deauth]
    ATTACK --> EVIL_PATH[evilportal]
    ATTACK --> BEACON_PATH[beacon spam]
    
    PMKID_PATH --> PMKID_CAP[PMKID captured]
    PMKID_CAP --> HASHCAT[hashcat -m 22000]
    HASHCAT --> PSK[WiFi Password]
    
    DEAUTH_PATH --> HANDSHAKE[sniffraw]
    HANDSHAKE --> CAP[Handshake .pcap]
    CAP --> HASHCAT
    
    EVIL_PATH --> PORTAL[Active Captive Portal]
    PORTAL --> CREDS[Credentials entered]
    
    BEACON_PATH --> FLOOD[Fake APs visible]
    FLOOD --> CONFUSION[Disruption/Confusion]
    
    PSK --> ACCESS[Network access]
    CREDS --> ACCESS
    
    ACCESS --> REPORT([Report Finding])
    
    DEAUTH_PATH -.-> STOP[stopscan]
    PMKID_PATH -.-> STOP
    
    style CONNECT fill:#2d3436,color:#fff
    style ACCESS fill:#d63031,color:#fff
    style REPORT fill:#2d3436,color:#fff
```

---

## RFID Clone Decision

```mermaid
graph LR
    READ[RFID Read] --> PROTO{Protocol}
    
    PROTO -->|EM4100| EM[64-bit, no crypto]
    PROTO -->|HID H10301| HID[26-bit FC:CN]
    PROTO -->|Indala| IND[PSK modulation]
    PROTO -->|FDX-B| FDX[Animal 134.2kHz]
    PROTO -->|Unknown| UNK[Not supported]
    
    EM --> CLONE[Write T5577]
    HID --> CLONE
    IND --> CLONE
    FDX --> DOC[Documentation only]
    UNK --> PROXMARK[Use Proxmark3]
    
    CLONE --> TEST[Test on reader]
    TEST --> OK{Works?}
    OK -->|Yes| REPORT[Report Finding]
    OK -->|No| EMUL[Try Emulation]
    EMUL --> REPORT
    
    style CLONE fill:#e17055,color:#fff
    style REPORT fill:#2d3436,color:#fff
    style PROXMARK fill:#636e72,color:#fff
```
