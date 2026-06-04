## Legal Aspects

### Italian Law

The use of devices such as the Flipper Zero for reading and cloning RFID badges is regulated by several laws:

**Criminal Code:**

- **Art. 615-ter** - Unauthorized access to a computer or telecommunications system: cloning a badge to access a protected location constitutes unauthorized access. Penalty: imprisonment from 1 to 5 years.

- **Art. 615-quater** - Unauthorized possession and distribution of access codes: possessing cloned badges without authorization may constitute this offense. Penalty: imprisonment up to 1 year and fine.

- **Art. 617-quater** - Unlawful interception, impediment or interruption of computer communications: unauthorized sniffing of RFID communications could fall under this provision.

- **Art. 640-ter** - Computer fraud: using cloned badges to obtain an advantage (e.g. access to services) constitutes computer fraud. Penalty: imprisonment from 6 months to 3 years and fine.

**EU Regulations:**

- **GDPR (EU Reg. 2016/679):** badge IDs are personal data if associable with natural persons. Unauthorized reading violates the GDPR.

- **NIS2 Directive (EU 2022/2555):** critical infrastructures must also protect physical access. A pentest on these systems requires formal authorization.

- **RED Regulation (EU 2014/53):** radio devices (such as the Flipper Zero) must comply with EU regulations on radio equipment. The Flipper Zero is compliant (CE certification) but improper use remains illegal.

### How to Operate Legally

1. **Written authorization ALWAYS:** before any test, obtain a signed contract specifying:
   - Scope of the test (which readers, which buildings, which badges)
   - Validity period
   - Authorized actions (reading, cloning, fuzzing, access attempts)
   - Emergency contacts
   - Indemnity clause

2. **Always carry with you:**
   - Copy of the contract
   - Photo ID
   - Phone number of the company contact person
   - "Legitimate" badge provided by the client for re-entry

3. **Boundaries to respect:**
   - Do not read badges of people not involved in the test
   - Do not access areas outside the scope
   - Do not retain data beyond the necessary period
   - Destroy cloned T5577s at the end of the engagement
   - Do not share read IDs with third parties

4. **Documentation:**
   - Detailed log of every action (time, location, ID read/used, result)
   - Timestamped photos/video
   - Final report with findings, risk and recommendations
   - Secure delivery of the report to the client

> **Personal note:** I always keep a "legal kit" in my bag, separate from the technical kit: copy of the contract, authorization letter on the client's letterhead, and my lawyer's phone number. In 8 years of physical pentesting I have never had legal issues, but once a building guard called the police when he saw me fiddling with the Flipper near the gate reader. Having the client's written authorization resolved everything in 10 minutes. Without that piece of paper, I would have been in trouble. NEVER operate without written authorization, not even on systems that "are insecure anyway."

---
