## Penetration Testing Scenarios

### Scenario 1: DS1990A Intercom Key Cloning

**Objective:** Demonstrate to the client that their apartment building's intercom system is vulnerable to key cloning.

**Context:** 40-unit apartment building in an Italian city, intercom system with iButton reader installed in the 2000s, DS1990A keys distributed to all residents.

**Operational phases:**

**Phase 1 - Reconnaissance (5 minutes)**
- Identify the type of reader on the main entrance (brand, model)
- Verify it is a contact-based system (visible metal probe)
- Check if there are cameras covering the reader area
- Note the key model used by residents (shape, color)

**Phase 2 - Key acquisition (30 seconds)**
- Request one of the client's personal keys
- Menu → iButton → Read
- Place the key on the Flipper's pad - maintain contact
- Read in ~1-2 seconds
- Verify: DS1990A protocol, family code 0x01, complete ROM code
- Save with descriptive name

**Phase 3 - Emulation verification (1 minute)**
- Menu → iButton → Saved → select the key → Emulate
- Approach the entrance reader
- Place the back of the Flipper on the probe
- Verify opening - if it opens, the read is confirmed

**Phase 4 - Physical clone creation (2 minutes)**
- Take a blank RW1990 tag from the kit
- Menu → iButton → Saved → select the key → Write
- Place the RW1990 on the Flipper's pad
- Wait for write confirmation
- Verify by reading the RW1990 - ROM code identical to the original

**Phase 5 - Clone verification (30 seconds)**
- Place the programmed RW1990 on the reader's probe
- If it opens: perfect clone, demonstration completed

**Phase 6 - Documentation**
- Photograph of the reader (no third-party personal data)
- Screenshot of the ROM code
- Note: total time from acquisition to working clone: ~5 minutes
- Recommendations in the report: migration to NFC system with encryption

**Deliverables for the client:**
- Demonstration that the key is clonable in 5 minutes
- Explanation of the absence of encryption in the protocol
- Recommendation: system with challenge-response (MIFARE DESFire, iClass SE)
- Migration cost estimate

> **Personal note:** This is the scenario I execute most frequently. The client's reaction when they see the entrance open with the clone is always the same - surprise and concern. It's a powerful educational moment. In the final report, I always emphasize that the problem is not the Flipper Zero (which is just a tool), but the DS1990A protocol that has no form of authentication whatsoever. Any hardware store with a 20-euro iButton duplicator can do the same thing.

### Scenario 2: Cyfral/Metakom Intercom Reader Fuzzing

**Objective:** Determine if a Cyfral reader is vulnerable to bruteforce and estimate the time required for unauthorized access.

**Context:** Apartment building with Cyfral CCD-2094 reader, Cyfral keys distributed to tenants, no key available for direct reading.

**Operational phases:**

**Phase 1 - System identification (2 minutes)**
- Identify the reader: "Cyfral" or "Eltis" brand printed on the panel
- Check for status LEDs (red/green)
- Check the probe type (the Cyfral probe has a characteristic shape)
- Note any cameras or alarm systems

**Phase 2 - Reader reaction test (2 minutes)**
- Touch the probe with a generic metal object (house key, coin)
- Observe the reaction:
  - Flashing red LED = the reader received a signal but it was invalid
  - No reaction = the reader did not detect a valid protocol
  - Green LED = unlikely, but would verify a bypass

**Phase 3 - Cyfral Fuzzing (2-5 minutes)**
- Menu → iButton Fuzzer → Cyfral
- Select: sequential mode (from 0x00 to 0xFF)
- Place the Flipper's pad on the reader's probe
- Start the fuzzer
- Maintain stable contact - any wobble interrupts communication
- Watch the reader's LED on each attempt:
  - Red = code rejected
  - Green = code accepted (save immediately!)
- With 256 codes at ~2 attempts/second: ~128 seconds (just over 2 minutes)

**Phase 4 - Results analysis**
- If found: save the code, verify with manual emulation
- If not found: the reader might use a Cyfral variant with extended keyspace
- Note the reader's behavior during fuzzing:
  - Did it impose rate limiting? After how many attempts?
  - Did it generate alarms?
  - Did it temporarily lock out?

**Phase 5 - Documentation**
- Actual time to find a valid code
- Reader behavior under fuzzing (rate limiting, lockout, alarms)
- Recommendations: replace Cyfral system with Dallas or encrypted NFC

> **Personal note:** Cyfral fuzzing is my "party trick" during client demos. 256 combinations in 2 minutes - the client is always impressed. But it's important to explain that this works because the Cyfral protocol has a tiny keyspace. Not all Cyfral systems are this weak - some installations use variants with longer codes. And in any case, the recommendation is always the same: migrate to an encrypted system.

### Scenario 3: Key Conversion for Mixed Systems

**Objective:** Test a system that accepts both Dallas and Cyfral keys, verifying proper protocol segregation.

**Context:** Apartment building with multi-protocol reader (accepts Dallas and Cyfral), some units have Dallas keys, others have Cyfral. The building manager wants to verify there are no configuration flaws.

**Operational phases:**

**Phase 1 - Sample acquisition (5 minutes)**
- Obtain a Dallas key from the client (resident with Dallas)
- Obtain a Cyfral key from the client (resident with Cyfral)
- Read both keys and save the files

**Phase 2 - Baseline test (2 minutes)**
- Emulate the Dallas key on the reader - verify opening
- Emulate the Cyfral key on the reader - verify opening
- Both should work on a multi-protocol reader

**Phase 3 - Conversion test (5 minutes)**
- Open iButton Converter
- Convert the Dallas key to Cyfral format
- Convert the Cyfral key to Dallas format
- Test the converted keys on the reader:
  - Does the Dallas-converted-to-Cyfral work? If yes: the reader doesn't verify the protocol, only the ID
  - Does the Cyfral-converted-to-Dallas work? Same analysis

**Phase 4 - Implications analysis**
- If converted keys work: the reader uses a single database without protocol segregation - vulnerability
- If they don't work: the reader maintains separate databases per protocol - correct behavior
- Check if a valid Dallas code for one resident also opens with the Cyfral protocol - cross-protocol weakness

**Phase 5 - Cross-protocol fuzzing**
- Use the Cyfral fuzzer on the reader to search for valid codes
- If you find a Cyfral code that opens: verify if it corresponds to a Dallas entry in the database
- Document all correlations found

**Phase 6 - Documentation**
- Protocol/code compatibility matrix
- Cross-protocol vulnerabilities identified
- Recommendations: database segregation or migration to a single encrypted protocol

> **Personal note:** This scenario is rare but illuminating when it comes up. I found an apartment building in Turin where the multi-protocol reader had a firmware bug: it accepted any Cyfral code if a valid Dallas code had just been used. The reader wasn't resetting the authentication state between reads. This kind of bug is why cross-protocol tests are important - cheap multi-protocol readers often have poorly written firmware.

### Scenario 4: Building Access System Security Audit

**Objective:** Complete security audit of the iButton access system of an entire apartment building, with final report and recommendations.

**Context:** The building manager commissions an audit after a series of intrusions. The building has 60 units, intercom system with iButton installed in 2005, reader on the main entrance and two secondary entrances.

**Operational phases:**

**Phase 1 - Physical reconnaissance (30 minutes)**
- Map all entrances: main entrance, secondary entrances, garage, common areas
- For each entrance:
  - Reader type (brand, model, estimated year)
  - Protocol used (Dallas, Cyfral, Metakom)
  - Physical condition of the reader (oxidation, damage, tampering)
  - Presence of cameras, alarms, lighting
  - Probe visibility (exposed, recessed, protected)
- Count the number of keys in circulation (ask the building manager)
- Check if master keys or administrator codes exist

**Phase 2 - Protocol analysis (15 minutes)**
- Read the client's key on each reader - verify the protocol
- Check if all readers use the same protocol
- Check if all readers share the same database (does the key work on all of them?)
- Identify the exact model of keys in use

**Phase 3 - Cloning test (10 minutes)**
- Clone the client's key onto an RW1990
- Test the clone on all readers - it should work on all readers where the original works
- Document the cloning time (from read to working clone)
- Estimate the attacker's cost (Flipper + RW1990 = ~200 euro, or generic iButton duplicator = ~30 euro)

**Phase 4 - Resilience testing (20 minutes)**
- Light fuzzing on one reader (with written authorization from the building manager)
- Verify:
  - Does the reader have rate limiting? After how many attempts?
  - Does the reader log failed attempts?
  - Does the reader generate alarms?
  - Does the reader lock out after N attempts?
- Invalid code testing: reader reaction to malformed IDs, incorrect CRCs, non-standard family codes
- Extended contact test: does the reader correctly handle timeout and reset?

**Phase 5 - Database analysis (if accessible)**
- Request access to the key management system (if one exists)
- Verify:
  - Number of registered keys vs keys in circulation (phantom keys?)
  - Presence of master keys
  - Date of last database update
  - Key revocation procedure (e.g., resident who sells and moves out)

**Phase 6 - Final report**

Report structure:

```
1. Executive Summary
   - Risk level: CRITICAL / HIGH / MEDIUM / LOW
   - Main vulnerabilities identified
   - Priority recommendations

2. Methodology
   - Tools used
   - Tests performed
   - Assessment duration

3. Findings
   3.1 Absence of encryption in the protocol
       - Severity: CRITICAL
       - Impact: key cloning in <5 minutes
       - Evidence: working clone demonstrated
   3.2 Absence of rate limiting
       - Severity: HIGH
       - Impact: unhindered fuzzing
       - Evidence: N attempts without lockout
   3.3 Non-revoked keys
       - Severity: MEDIUM
       - Impact: former residents with active access
       - Evidence: N keys in database, M current residents
   3.4 [Additional specific findings]

4. Recommendations
   4.1 Short term (0-3 months):
       - Audit of keys in circulation
       - Revocation of former residents' keys
       - Camera installation at entrances
   4.2 Medium term (3-12 months):
       - Migration to NFC system with encryption (MIFARE DESFire)
       - Access log implementation
       - Formal key management procedure
   4.3 Long term (1-3 years):
       - Integrated access system with IP video intercom
       - Multi-factor authentication (key + PIN)
       - Integration with building automation system

5. Appendices
   - Technical details of the tests
   - Assessment timeline
   - Estimated cost of mitigations
```

> **Personal note:** This type of audit is the most requested service for iButton. The typical building manager doesn't even know what technology their intercom uses - "they're those round key fobs" is the extent of their awareness. When you present the report with a cloning demonstration in 5 minutes, the residents' assembly takes the matter very seriously. The cost of migrating to an NFC system is typically 3,000-8,000 euro for an average apartment building - a significant expense but justifiable after demonstrating the vulnerability. My advice is always to start with the short-term recommendations (key revocation, cameras) because they are free or very low cost, and then plan the technology migration.

---

## Cross-Reference - Multi-Vector Scenarios

| Scenario | Related Module | Link | How they connect |
|----------|-----------------|------|-------------------|
| Intercom + RFID | RFID | [05-Scenari-Reali](../RFID/05-Scenari-Reali.md) | Apartment buildings: iButton for intercom + RFID badge for entrance/garage |
| Intercom + Sub-GHz | Sub-GHz | [05-Scenari-Reali](../Sub-GHz/05-Scenari-Reali.md) | iButton for stairway access + Sub-GHz remote for vehicle gate |
| Physical access + BadUSB | USB/Bad USB | [05-Scenari-Reali](../USB/Bad%20USB/05-Scenari-Reali.md) | After access via cloned iButton → deploy BadUSB on reception PC |
| iButton + Debug | GPIO/Debug | [04-Scenari-Reali](../GPIO/Debug/04-Scenari-Reali.md) | Firmware dump of iButton reader for stored code analysis |
