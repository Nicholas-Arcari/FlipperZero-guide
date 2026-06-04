# Legal Aspects - NFC

Italian and European regulatory framework for the use of NFC devices in security assessment contexts.

---

## Italy

### Criminal Code

- **Art. 615-ter c.p. - Unauthorized access to a computer system:** cloning an NFC badge to access a building without authorization is a criminal offense. Access control systems are considered "computer systems" under case law. Penalty: imprisonment from 1 to 5 years.

- **Art. 640-ter c.p. - Computer fraud:** modifying data on prepaid cards (e.g., cafeteria credit, transit passes) to gain an advantage constitutes computer fraud. Penalty: imprisonment from 6 months to 3 years and a fine.

- **Art. 491-bis c.p. - Forgery of electronic documents:** creating cloned badges may constitute this offense if the badge is considered an electronic document.

- **Art. 617-quater c.p. - Fraudulent interception:** capturing NFC data during reader-tag communication may fall under this provision.

### GDPR

- Data read from badges may contain personal information (UID associated with an employee, name, role, permissions)
- Unauthorized reading of badges constitutes unlawful processing of personal data
- Even during an authorized pentest, collected data must be handled according to the principle of data minimization

---

## European Union

- **RED Directive 2014/53/EU:** the Flipper Zero is compliant (NFC operates in the 13.56 MHz ISM band)
- **GDPR (Reg. 2016/679):** NFC data attributable to natural persons constitutes personal data
- **NIS2 Directive (2022/2555):** access control systems for critical infrastructure fall under security obligations

---

## Legal Best Practices for NFC Pentesting

### Before the Engagement

1. **Specific written authorization** that includes:
   - "Testing of NFC/RFID access control systems"
   - Specific list of readers/doors authorized for testing
   - Authorization for badge reading, cloning, and modification
   - Temporal and geographic scope

2. **Magic Card handling:**
   - Cloned Magic Cards are equivalent to keys/badges - secure them as credentials
   - Do not take cloned Magic Cards outside the authorized perimeter
   - Number the Magic Cards and track their use

3. **Exclusions:**
   - Clarify whether the test includes third-party cards (hotel, transit, vendors)
   - Define off-limits areas (e.g., server room, classified areas)

### During the Engagement

- Document every badge read: timestamp, UID, type, result
- Never attempt to read a badge without authorization (even informal "drive-by")
- If you find sensitive data in badges (name, national ID number, health data): note it in the report but do not retain it
- Prepaid credit modifications (cafeteria, vending machines) must be documented and immediately restored

### After the Engagement

- **Delete all dumps** from the SD card and PC
- **Format all Magic Cards** used (zero all sectors)
- **The report should describe the vulnerability** without including actual keys or full dumps
- Retain only evidence strictly necessary for a potential follow-up

---

## Gray Area - Passive Reading

NFC badge reading requires physical proximity (<5 cm) and therefore implies an intentional act. There is no equivalent of Sub-GHz "passive reception" - every NFC read is active.

**Implication:** unauthorized reading of a badge, even without writing or cloning, is potentially an unlawful act because:
- It requires a deliberate action (bringing the device close)
- It acquires data that may be personal
- The badge holder has not given consent

**Practical rule:** NEVER read a badge without authorization, not even to "see what type it is".
