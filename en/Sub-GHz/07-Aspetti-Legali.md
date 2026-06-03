# Legal Aspects - Sub-GHz

Italian and European regulatory framework concerning the use of RF devices for security analysis, penetration testing, and research.

---

## Italy

### Criminal Code

- **Art. 617-quater c.p. - Fraudulent interception of communications:** capturing RF signals may fall under this offense if done without authorization. Penalty: imprisonment from 6 months to 4 years. Passive capture (reception only) is a gray area - case law is not uniform.

- **Art. 615-ter c.p. - Unauthorized access to a computer or telecommunications system:** opening a gate, door, or barrier via replay attack or bruteforce without authorization is a criminal offense. Penalty: imprisonment from 1 to 5 years. The gate automation system is considered a "computer system" under recent case law.

- **Art. 617-quinquies c.p. - Installation of equipment designed to intercept communications:** possession and use of devices for intercepting RF communications may constitute this offense if the intent is fraudulent.

### Electronic Communications Code (D.Lgs. 259/2003)

- Use of the ISM bands (433 MHz, 868 MHz) is free within the established power limits (25 mW ERP for 433 MHz, 25 mW for 868 MHz)
- **Intentional interference** (jamming) is always prohibited, regardless of frequency
- Transmission on non-ISM frequencies requires a license
- The Flipper Zero complies with ISM power limits (+12 dBm = ~16 mW < 25 mW)

### National Frequency Allocation Plan (PNRF)

- Frequencies 433.05-434.79 MHz are assigned as ISM in Italy
- Frequencies 863-870 MHz are Short Range Devices (SRD) with limited duty cycle
- Usage must comply with duty cycle limits (typically 1% or 10% depending on the sub-band)

---

## European Union

### Directive RED 2014/53/EU (Radio Equipment Directive)

- Regulates the placing on the market of radio equipment
- The Flipper Zero is compliant (CE marking)
- Does not regulate specific use, but the product must comply with harmonized standards

### ETSI EN 300 220 (Short Range Devices)

- Technical standard for short-range devices in the 25-1000 MHz bands
- Defines power limits, duty cycle, bandwidth
- The Flipper Zero operates within these limits

### GDPR (Regulation 2016/679)

- Collection of RF data that can be associated with natural persons (e.g., TPMS IDs, unique remote control codes, POCSAG messages with personal data) is subject to GDPR
- Interception of POCSAG messages containing health data constitutes processing of sensitive data (art. 9)
- Even during an authorized pentest, collected data must be handled according to the principle of data minimization

---

## Operational Rules for the Pentester

### Before the Engagement

1. **Written authorization:** always obtain explicit authorization specifying:
   - Frequencies authorized for capture
   - Target devices authorized for replay
   - Geographic scope (the authorization covers only the specified area)
   - Temporal duration of the authorization
   
2. **Specific RF scope:** the authorization must explicitly cover RF operations. A generic "authorized pentest" may not cover interception of third-party radio signals.

3. **Exclusions:** clarify that passive capture may intercept signals from non-target devices (neighbors, passersby). The authorization should anticipate this eventuality.

### During the Engagement

- **Passive reception only** without specific authorization for transmission
- **Transmission (replay/bruteforce)** only with explicit authorization for the target device
- **Never jam** without specific written authorization - jamming can impact third-party devices
- **Document everything:** frequencies used, timestamp of every capture/transmission, results
- **Data minimization:** delete captured signals not pertinent to the report

### After the Engagement

- Delete all RF captures from the SD card after completing the report
- Do not retain valid access codes - they represent credentials
- The report should describe the vulnerability without including the actual codes

---

## Gray Area - Passive Reception

Passive reception of RF signals (without transmission) is a legal gray area:

- **Argument in favor of legality:** radio signals traverse public space, reception does not require access to protected systems
- **Counterargument:** targeted interception of specific communications (e.g., a hospital's POCSAG) may constitute a criminal offense even without transmission
- **Precedents:** Italian case law is sparse on this specific topic for ISM bands

**Practical rule:** treat passive reception as "probably legal but potentially contestable" and always obtain prior authorization in professional contexts.
