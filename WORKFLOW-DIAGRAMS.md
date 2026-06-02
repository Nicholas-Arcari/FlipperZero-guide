# Workflow Diagrams - Diagrammi Operativi

Diagrammi Mermaid per i workflow principali. GitHub li renderizza automaticamente.

---

## Physical Pentest Kill Chain

```mermaid
graph TD
    START([Inizio Engagement]) --> R1[Ricognizione Perimetro]
    
    R1 --> RF[Sub-GHz Freq Analyzer]
    R1 --> WIFI[WiFi scanap/scansta]
    R1 --> BADGE[NFC/RFID Detector]
    R1 --> BLE[BLE Scanner]
    
    RF --> RF_RESULT{Segnale trovato?}
    RF_RESULT -->|Codice fisso| REPLAY[Replay Attack]
    RF_RESULT -->|Rolling code| ROLLJAM[RollJam / Rolling Flaws]
    RF_RESULT -->|Non decodifica| RAW[Read RAW]
    
    WIFI --> WIFI_RESULT{AP vulnerabile?}
    WIFI_RESULT -->|WPA2-PSK| PMKID[sniffpmkid]
    WIFI_RESULT -->|Client attivi| DEAUTH[Deauth + Evil Portal]
    WIFI_RESULT -->|Open/WEP| DIRECT[Connessione diretta]
    
    BADGE --> BADGE_RESULT{Tipo badge?}
    BADGE_RESULT -->|125 kHz EM4100| CLONE_RFID[Clone su T5577]
    BADGE_RESULT -->|13.56 MHz MIFARE| DICT[Dictionary Attack]
    BADGE_RESULT -->|iButton| IBUTTON[Read + Clone RW1990]
    
    DICT --> DICT_RESULT{Chiavi trovate?}
    DICT_RESULT -->|Si| DUMP_NFC[Dump completo]
    DICT_RESULT -->|No| MFKEY[Detect Reader + MFKey32]
    MFKEY --> DUMP_NFC
    DUMP_NFC --> CLONE_NFC[Write Magic Card Gen4]
    
    REPLAY --> ACCESS[Accesso Fisico]
    CLONE_RFID --> ACCESS
    CLONE_NFC --> ACCESS
    IBUTTON --> ACCESS
    DEAUTH --> CREDS[Credenziali WiFi]
    PMKID --> CRACK[Hashcat Crack]
    CRACK --> CREDS
    
    ACCESS --> EXPLOIT{Vettore Exploitation}
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
    
    DICT --> KEYS{Tutte le chiavi?}
    KEYS -->|Si| FULL_DUMP[Dump Completo]
    KEYS -->|No| DETECT[Detect Reader x3]
    
    DETECT --> MFKEY[MFKey32]
    MFKEY --> REREAD[Re-Read con tutte le chiavi]
    REREAD --> FULL_DUMP
    
    FULL_DUMP --> WRITE[Write Magic Card Gen4]
    WRITE --> VERIFY[Verifica su lettore]
    
    MFUL --> DIRECT_READ[Read Diretto - No crypto]
    MFULC --> PWD_ATTACK[Password Attack 3DES]
    DESFIRE --> DOCUMENT[Documenta come SICURO]
    
    style DESFIRE fill:#00b894,color:#fff
    style DOCUMENT fill:#00b894,color:#fff
    style FULL_DUMP fill:#e17055,color:#fff
    style WRITE fill:#d63031,color:#fff
```

---

## Sub-GHz Analysis Flow

```mermaid
graph TD
    START[Target RF] --> FREQ[Frequency Analyzer]
    FREQ --> FOUND{Frequenza trovata}
    
    FOUND --> READ[Sub-GHz Read]
    READ --> DECODE{Decodificato?}
    
    DECODE -->|Si| PROTO{Protocollo}
    DECODE -->|No| RAW[Read RAW]
    
    PROTO -->|Codice fisso| FIX[Princeton/CAME/etc]
    PROTO -->|Rolling code| ROLL[KeeLoq/Nice FLO]
    PROTO -->|Sconosciuto| ANALYZE[Analisi manuale]
    
    FIX --> REPLAY[Replay diretto]
    REPLAY --> SUCCESS{Funziona?}
    SUCCESS -->|Si| SAVE[Save + Report]
    SUCCESS -->|No| CLOSER[Avvicinati < 5m]
    CLOSER --> REPLAY
    
    ROLL --> ROLLING_FLAWS[Rolling Flaws Analysis]
    ROLLING_FLAWS --> VULN{Vulnerabile?}
    VULN -->|Si| EXPLOIT_ROLL[Exploit]
    VULN -->|No| DOC_SECURE[Documenta come sicuro]
    
    RAW --> RAW_REPLAY[Replay RAW]
    RAW_REPLAY --> RAW_RESULT{Funziona?}
    RAW_RESULT -->|Si| SAVE
    RAW_RESULT -->|No| BRUTE{< 16 bit?}
    BRUTE -->|Si| BRUTEFORCE[Bruteforcer]
    BRUTE -->|No| DOC_SECURE
    
    style SAVE fill:#e17055,color:#fff
    style DOC_SECURE fill:#00b894,color:#fff
```

---

## BadUSB Attack Chain

```mermaid
graph TD
    INSERT[Inserisci Flipper USB] --> ENUM[HID Enumeration ~1s]
    ENUM --> OS{Target OS?}
    
    OS -->|Windows| WIN_OPEN[GUI r → PowerShell]
    OS -->|macOS| MAC_OPEN[GUI SPACE → Terminal]
    OS -->|Linux| LIN_OPEN[CTRL ALT T → Terminal]
    
    WIN_OPEN --> PHASE1{Fase 1}
    MAC_OPEN --> PHASE1
    LIN_OPEN --> PHASE1
    
    PHASE1 -->|Recon| RECON[System/Network Enum]
    PHASE1 -->|Direct Shell| SHELL[Reverse Shell]
    PHASE1 -->|Evasion First| EVASION[AMSI Bypass + Defender Off]
    
    EVASION --> SHELL
    
    SHELL --> C2[Connessione C2]
    C2 --> PHASE2{Fase 2}
    
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
    SCAN --> LIST[Lista AP]
    LIST --> SELECT[select -a N]
    
    SELECT --> ATTACK{Tipo attacco}
    
    ATTACK --> PMKID_PATH[sniffpmkid]
    ATTACK --> DEAUTH_PATH[deauth]
    ATTACK --> EVIL_PATH[evilportal]
    ATTACK --> BEACON_PATH[beacon spam]
    
    PMKID_PATH --> PMKID_CAP[PMKID catturato]
    PMKID_CAP --> HASHCAT[hashcat -m 22000]
    HASHCAT --> PSK[Password WiFi]
    
    DEAUTH_PATH --> HANDSHAKE[sniffraw]
    HANDSHAKE --> CAP[Handshake .pcap]
    CAP --> HASHCAT
    
    EVIL_PATH --> PORTAL[Captive Portal attivo]
    PORTAL --> CREDS[Credenziali inserite]
    
    BEACON_PATH --> FLOOD[AP falsi visibili]
    FLOOD --> CONFUSION[Disruption/Confusion]
    
    PSK --> ACCESS[Accesso rete]
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
    READ[RFID Read] --> PROTO{Protocollo}
    
    PROTO -->|EM4100| EM[64-bit, no crypto]
    PROTO -->|HID H10301| HID[26-bit FC:CN]
    PROTO -->|Indala| IND[PSK modulation]
    PROTO -->|FDX-B| FDX[Animale 134.2kHz]
    PROTO -->|Sconosciuto| UNK[Non supportato]
    
    EM --> CLONE[Write T5577]
    HID --> CLONE
    IND --> CLONE
    FDX --> DOC[Solo documentazione]
    UNK --> PROXMARK[Usa Proxmark3]
    
    CLONE --> TEST[Test su lettore]
    TEST --> OK{Funziona?}
    OK -->|Si| REPORT[Report Finding]
    OK -->|No| EMUL[Prova Emulazione]
    EMUL --> REPORT
    
    style CLONE fill:#e17055,color:#fff
    style REPORT fill:#2d3436,color:#fff
    style PROXMARK fill:#636e72,color:#fff
```
