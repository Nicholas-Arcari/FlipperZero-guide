# Report Templates - Engagement Finding Templates

Ready-made templates for documenting findings during a physical penetration test with Flipper Zero. Copy-paste and fill in.

---

## Generic Template - Finding

```markdown
## [SEVERITY] Finding Title

**ID:** FZ-[MODULE]-[NNN]
**Severity:** Critical / High / Medium / Low / Informational
**CVSS 3.1:** [score] ([vector])
**MITRE ATT&CK:** [Tactic] ([TAXXXX]) / [Technique] ([TXXXX])
**Status:** Open / Remediated / Accepted Risk

### Description
[Technical description of the vulnerability found]

### Environment
- **Target:** [Type of device/system tested]
- **Location:** [Physical location]
- **Protocol:** [NFC/RFID/Sub-GHz/WiFi/etc.]
- **Tool:** Flipper Zero + [specific module]

### Reproduction Procedure
1. [Step 1]
2. [Step 2]
3. [Step n]

### Evidence
- Captured file: `[filename.ext]`
- Screenshot/photo: [reference]
- Evidence hash: `sha256: [hash]`

### Impact
[What an attacker can do by exploiting this vulnerability]

### Recommendation
| Priority | Action | Estimated Cost | Timeframe |
|----------|--------|----------------|-----------|
| Immediate | [Quick fix] | Low | 1-2 days |
| Short term | [Mitigation] | Medium | 1-2 weeks |
| Long term | [Definitive solution] | High | 1-3 months |

### References
- [CVE/Advisory if applicable]
- [Reference standard]
```

---

## Template - Sub-GHz: Replay Attack

```markdown
## [HIGH] Gate/Barrier Vulnerable to Sub-GHz Replay Attack

**ID:** FZ-SUBGHZ-001
**Severity:** High
**CVSS 3.1:** 7.5 (AV:P/AC:L/PR:N/UI:N/S:C/C:N/I:H/A:L)
**MITRE ATT&CK:** Initial Access (TA0001) / Hardware Additions (T1200)

### Description
The [gate/barrier/door] opening system uses a fixed-code Sub-GHz
protocol (protocol: [Princeton/CAME/etc.]) on frequency [XXX.XX MHz].
The signal was captured with the Flipper Zero and successfully
retransmitted, achieving unauthorized opening.

### Environment
- **Target:** [Gate brand/model]
- **Frequency:** [XXX.XX MHz]
- **Protocol:** [Protocol name]
- **Modulation:** [OOK/ASK/FSK]
- **Bits:** [N bits]
- **Capture distance:** [X meters]
- **Replay distance:** [X meters]

### Procedure
1. Sub-GHz → Read → frequency [XXX.XX MHz]
2. Signal capture during legitimate opening (distance: ~Xm)
3. Analysis: protocol [name], [N] bits, fixed code [hex]
4. Sub-GHz → Saved → [file] → Send
5. The gate opens

### Evidence
- Captured `.sub` file: `gate_capture_YYYYMMDD.sub`
- Decoded protocol: [Name] [N]bit Key:[HEX]
- Opening video: [reference]

### Impact
Anyone with an SDR device or a Flipper Zero can capture the opening
signal and reproduce it without limits. Proximity to the original
remote is not required - it is sufficient to be within signal range
during a single legitimate opening.

### Recommendation
| Priority | Action | Cost | Timeframe |
|----------|--------|------|-----------|
| Immediate | Restrict physical access to the receiver area | Low | 1 day |
| Short term | Verify if the receiver supports rolling code | Low | 1 week |
| Long term | Replace with rolling code system (KeeLoq or AES) | 200-500 EUR | 2-4 weeks |
```

---

## Template - NFC: Badge Clone

```markdown
## [CRITICAL] Clonable NFC MIFARE Classic Badge

**ID:** FZ-NFC-001
**Severity:** Critical
**CVSS 3.1:** 8.6 (AV:P/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:N)
**MITRE ATT&CK:** Initial Access (TA0001) / Valid Accounts (T1078)

### Description
The [name/brand] access control system uses NFC MIFARE Classic [1K/4K]
badges with Crypto1 encryption. The cryptographic keys were recovered
via [dictionary attack / MFKey32] and the badge was successfully cloned
onto a Magic Card Gen4.

### Environment
- **Reader:** [Brand/model]
- **Card:** MIFARE Classic [1K/4K]
- **UID:** [XX:XX:XX:XX] (anonymized in the final report)
- **SAK:** [0x08/0x18]
- **Keys recovered:** [N]/[TOT] sectors
- **Sensitive data:** Sector [N] contains [data type]

### Procedure
1. NFC → Read → identified MIFARE Classic [1K/4K], SAK [0xXX]
2. NFC → Read → Dictionary Attack → [N] keys found on [N] sectors
3. NFC → Detect Reader → positioned on target reader x3 reads
4. MFKey32 → recovered [N] missing keys
5. NFC → Read (complete) → dump [N] sectors out of [N]
6. Dump analysis: sector [N] contains [access data/ID/permissions]
7. NFC → Saved → Write → Magic Card Gen4
8. Test: cloned badge opens [door/turnstile/elevator] successfully

### Evidence
- NFC dump: `badge_clone_YYYYMMDD.nfc` (sha256: [hash])
- Recovered keys: [partially anonymized list]
- Sectors with data: [N], [N], [N]

### Impact
- Unauthorized physical access to [protected areas]
- Ability to clone any badge from the same infrastructure
- Escalation: modify sector [N] to [change floor/permissions/credit]
- Crypto1 has been broken since 2008 - the entire infrastructure is compromised

### Recommendation
| Priority | Action | Cost | Timeframe |
|----------|--------|------|-----------|
| Immediate | Audit badges in circulation, revoke lost ones | Low | 1-2 days |
| Short term | Add PIN or biometric as a second factor | Medium | 2-4 weeks |
| Long term | Migrate to DESFire EV2/EV3 with AES-128 | High (3-15K EUR) | 2-6 months |
```

---

## Template - RFID: 125 kHz Badge Clone

```markdown
## [HIGH] Clonable 125 kHz RFID Badge Without Encryption

**ID:** FZ-RFID-001
**Severity:** High
**CVSS 3.1:** 7.5 (AV:P/AC:L/PR:N/UI:N/S:C/C:N/I:H/A:N)
**MITRE ATT&CK:** Initial Access (TA0001) / Valid Accounts (T1078)

### Description
The access control system uses 125 kHz RFID badges [EM4100/HID
H10301/Indala] without encryption. The badge was read and cloned onto
a T5577 tag in under 10 seconds.

### Environment
- **Protocol:** [EM4100 / HID H10301 / Indala]
- **ID:** [hex] | FC:[N] CN:[N] (for HID)
- **Read distance:** [X cm]
- **Clone time:** [X seconds]

### Recommendation
Migrate to NFC with encryption (minimum MIFARE DESFire EV2, recommended
MIFARE DESFire EV3 with AES-128). 125 kHz tags have NO security
mechanism - they cannot be mitigated, only replaced.
```

---

## Template - BadUSB: Keystroke Injection

```markdown
## [CRITICAL] Workstation Vulnerable to USB Keystroke Injection

**ID:** FZ-USB-001
**Severity:** Critical
**CVSS 3.1:** 8.4 (AV:P/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H)
**MITRE ATT&CK:** Initial Access (TA0001) / Hardware Additions (T1200)

### Description
Workstation [identifier] accepts USB HID devices without restrictions.
A Flipper Zero configured as BadUSB executed a DuckyScript payload
that [opened a reverse shell / extracted WiFi credentials / created
an admin user / disabled defenses].

### Environment
- **Target OS:** [Windows 10/11 / macOS / Linux]
- **EDR/AV:** [Name and version, or "None"]
- **USB Policy:** [No restrictions / Partial GPO]
- **Execution time:** [X seconds]
- **Detected:** [Yes/No]

### Procedure
1. Inserted Flipper Zero into USB port [front/rear]
2. Payload: [payload_name.txt]
3. Total time: [X seconds]
4. Result: [shell obtained / credentials extracted / etc.]

### Recommendation
| Priority | Action | Cost | Timeframe |
|----------|--------|------|-----------|
| Immediate | Disable unnecessary USB ports (BIOS + GPO) | Low | 1 day |
| Short term | Implement USB device whitelisting | Medium | 1-2 weeks |
| Short term | Block new HID devices via GPO | Low | 1 day |
| Long term | Deploy DLP solution with USB control | High | 1-3 months |
```

---

## Template - WiFi: Evil Portal

```markdown
## [HIGH] WiFi Network Vulnerable to Evil Portal / Credential Harvest

**ID:** FZ-WIFI-001
**Severity:** High
**CVSS 3.1:** 7.1 (AV:A/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:N)
**MITRE ATT&CK:** Initial Access (TA0001) / Phishing (T1566)

### Description
Using ESP32 Marauder connected to the Flipper Zero, it was possible to:
1. Deauthenticate clients from the target network [SSID]
2. Create an Evil Portal with an identical SSID
3. Collect [N] sets of credentials from users who reconnected

### Environment
- **Target SSID:** [name]
- **Security:** WPA2-PSK / WPA2-Enterprise
- **Deauthenticated clients:** [N]
- **Credentials collected:** [N] in [X minutes]
- **Distance:** [X meters]

### Recommendation
| Priority | Action | Cost | Timeframe |
|----------|--------|------|-----------|
| Immediate | Implement 802.11w (Protected Management Frames) | Low | 1 day |
| Short term | Migrate to WPA2/WPA3-Enterprise with 802.1X | Medium | 2-4 weeks |
| Short term | Deploy WIDS to detect rogue APs | Medium | 1-2 weeks |
| Long term | User training on malicious captive portal recognition | Low | Ongoing |
```

---

## Template - Infrared: Device Control

```markdown
## [MEDIUM] IR Devices Controllable Without Authentication

**ID:** FZ-IR-001
**Severity:** Medium
**CVSS 3.1:** 5.3 (AV:P/AC:L/PR:N/UI:N/S:U/C:N/I:L/A:H)
**MITRE ATT&CK:** Impact (TA0040) / Service Stop (T1489)

### Description
The following devices in the [location] area are controllable via
infrared without authentication: [device list]. It was possible to
[power them off/modify settings/change input] using the Flipper Zero's
universal IR database.

### Recommendation
- Place critical devices in locked cabinets with shielded IR window
- Use network-based control systems (IP/RS-232) with authentication
- For informational displays: disable IR receiver if not needed
```

---

## Summary Template - Executive Summary

```markdown
# Executive Summary - Physical Penetration Test

**Client:** [Company name]
**Date:** [DD/MM/YYYY]
**Scope:** Physical security assessment of buildings [addresses]
**Tester:** [Name]
**Authorization:** [Contract/letter reference]

## Results

| Severity | Count | Examples |
|----------|-------|---------|
| Critical | [N] | [Clonable NFC badges, workstations open to BadUSB] |
| High | [N] | [Gate replay, WiFi evil portal] |
| Medium | [N] | [IR device control, BLE spam] |
| Low | [N] | [Informational findings] |

## Key Findings

1. **[CRITICAL]** [Title] - [one line of impact]
2. **[HIGH]** [Title] - [one line of impact]
3. ...

## Priority Recommendations

1. [Most urgent action]
2. [Second priority]
3. [Third priority]

## Next Steps
- [ ] Present results to management ([date])
- [ ] Remediation plan by [date]
- [ ] Re-test planned for [date]
```
