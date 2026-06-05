## 7. Legal Aspects

### 7.1 Italian Legislation

Italian legislation on cybersecurity and interception of communications is
particularly strict. The relevant statutes for the use of tools like WiFi
Marauder are:

**Art. 615-ter c.p. - Unauthorized access to a computer or telecommunications system:**
- "Anyone who unlawfully gains access to a computer or telecommunications
  system protected by security measures..."
- Penalty: imprisonment from 1 to 5 years
- Applicability: connecting to a protected WiFi network without authorization
  constitutes unauthorized access even if the password has been cracked

**Art. 617-quater c.p. - Unlawful interception, obstruction, or interruption
of computer or telecommunications communications:**
- "Anyone who fraudulently intercepts communications relating to a computer
  or telecommunications system..."
- Penalty: imprisonment from 1 year and 6 months to 5 years
- Applicability: sniffing WiFi traffic belonging to others (even management
  frames only) can fall under this offense

**Art. 617-quinquies c.p. - Installation of equipment designed to intercept
computer or telecommunications communications:**
- "Anyone who, outside of cases permitted by law, installs equipment
  designed to intercept..."
- Penalty: imprisonment from 1 to 4 years
- Applicability: placing a device (including a Flipper Zero) with the purpose
  of intercepting others' wireless communications

**Art. 640-ter c.p. - Computer fraud:**
- "Anyone who, by altering in any way the functioning of a computer or
  telecommunications system..."
- Applicability: Evil Portal for credential harvesting on unaware users

**D.Lgs. 196/2003 and GDPR (EU Reg. 2016/679) - Personal data protection:**
- Capturing MAC addresses, probe requests with SSIDs, credentials via
  Evil Portal constitutes processing of personal data
- Without consent and a legal basis, it is a GDPR violation
- Administrative fines up to 4% of global turnover (for companies)
  or up to 20 million euros

### 7.2 European Legislation

At the European level, Directive 2013/40/EU (NIS Directive - Attacks against
information systems) harmonizes national legislation:

- Art. 3: unlawful access to information systems
- Art. 4: unlawful system interference
- Art. 5: unlawful data interference
- Art. 6: unlawful interception
- Art. 7: tools used to commit computer offenses (possession of tools
  may be relevant if there is criminal intent)

### 7.3 Requirements for Legal Penetration Testing

To operate legally as a WiFi penetration tester in Italy:

1. **Written authorization**: a contract signed by the network owner
   specifying exactly what is authorized (scope of work).

2. **Defined scope**: precise list of target networks (SSID/BSSID), authorized
   techniques, operating hours, physical areas.

3. **Exclusions**: explicitly define what is NOT authorized (e.g.,
   "attacks on third-party networks visible from the area are not authorized").

4. **Authorization letter (Get Out of Jail Free Letter)**: a document
   to carry at all times that identifies the tester, the client, the
   project, and verification contacts.

5. **Professional insurance**: professional liability insurance for pentesters.

6. **Rules of engagement**: what to do if sensitive third-party data is
   intercepted (delete immediately, do not include in the report).

7. **Data handling**: all captured data (handshakes, credentials, pcaps)
   must be securely deleted at the end of the engagement, after report
   delivery.

**Warning**: even with authorization, some actions may have legal implications
if they involve networks or users not included in the scope. For example:
- A deauth on a target AP can also disconnect third-party clients
  sharing the same AP
- An Evil Portal can capture credentials from people not included in the test
- Sniffing on a channel captures frames from ALL networks on that channel

> Personal note: I always carry the printed authorization letter and a
> digital copy on my smartphone when doing wireless engagements.
> I was once stopped by building security while wardriving in a parking lot.
> The letter signed by the IT Director resolved the situation in 2 minutes.
> Without that letter, it would have ended with a call to the police.

---
