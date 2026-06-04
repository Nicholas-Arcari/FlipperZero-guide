## Legal Considerations

### Applicable Italian Regulations

The use of tools like the Flipper Zero for reading, cloning, and fuzzing iButton keys is regulated by several Italian laws:

**Criminal Code:**

- **Art. 615 ter c.p. - Unauthorized access to a computer or telecommunications system:** "Anyone who unlawfully gains access to a computer or telecommunications system protected by security measures, or remains in it against the express or implied will of whoever has the right to exclude them, is punished with imprisonment from one to five years."
  - An iButton access system is considered a system protected by security measures, even if weak
  - Cloning someone else's key and using it to access a building can constitute this offense
  - The penalty is increased if the act is committed by a public official or by someone practicing as a private investigator

- **Art. 615 quater c.p. - Unlawful possession and distribution of access codes to computer or telecommunications systems:** "Anyone who, with the purpose of procuring a profit for themselves or others, or of causing damage to others, unlawfully obtains, reproduces, distributes, communicates, or delivers codes, passwords, or other means suitable for accessing a computer or telecommunications system protected by security measures, or in any case provides information or instructions suitable for the aforementioned purpose, is punished with imprisonment up to one year and a fine up to 5,164 euros."
  - The ROM code of an iButton key is an "access code"
  - Reproduction (cloning) without authorization constitutes the offense
  - Even mere possession of the cloned code can be problematic

- **Art. 624 c.p. - Theft:** If the key is taken (even temporarily) for cloning purposes, it may constitute theft of use.

- **Art. 640 ter c.p. - Computer fraud:** If cloning and use of the clone produce an unjust financial advantage.

**Privacy Code (D.Lgs. 196/2003 and GDPR):**

- iButton access logs contain personal data (who accesses, when)
- The collection of this data must comply with the GDPR
- Intercepting access codes of third parties violates privacy

**D.Lgs. 231/2001 - Administrative liability of entities:**

- A company commissioning security tests must have formal authorization
- The pentester must operate within the scope of a contract that defines scope and limits

### What You Can Legally Do

**Always legal:**
- Reading and cloning YOUR OWN personal keys
- Testing iButton systems that are YOUR OWN property (e.g., your home automation system)
- Studying the 1-Wire protocol for educational/research purposes
- Possessing a Flipper Zero (it is not illegal to own the tool)
- Making backups of your own keys

**Legal with written authorization:**
- Penetration testing on third-party systems (pentest contract)
- Building security audit (residents' assembly resolution + contract)
- Resilience testing on clients' readers (consulting contract)

**Always illegal:**
- Cloning others' keys without consent
- Using clones to access buildings that are not yours
- Fuzzing readers without authorization from the owner
- Intercepting iButton codes of third parties
- Selling or distributing cloned codes

### Recommendations for the Pentester

1. **Written contract ALWAYS** - before touching any system, have a signed contract that specifies:
   - Assessment scope (which readers, which keys)
   - Authorized time period
   - Operational limits (e.g., "no fuzzing after 10:00 PM")
   - Liability in case of damages
   - Confidentiality clause

2. **Specific authorization for fuzzing** - fuzzing is more aggressive than simple reading/emulation. Explicit authorization in the contract is required.

3. **Document everything** - record every action with timestamps, screenshots, photos. In case of dispute, documentation is your defense.

4. **Do not retain third-party codes** - after the audit, delete all `.ibtn` files containing client codes. Keep only hashes or redacted screenshots for the report.

5. **Anonymized report** - in the report, do not include complete ROM codes of the keys. Use redacted versions (e.g., `01:XX:XX:XX:XX:XX:XX:E7`).

> **Personal note:** I always have a signed contract before starting any activity on third-party systems - no exceptions. For building audits, I require a copy of the residents' assembly resolution authorizing the assessment, in addition to the contract with the building manager. For fuzzing, I always include a specific clause in the contract that explicitly mentions it. The bureaucracy is tedious but it saves your life - a frightened resident who sees you tinkering with the intercom and calls the police is not a situation you want to be in without documentation.

---
