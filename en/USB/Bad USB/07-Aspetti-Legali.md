## Legal Aspects

### Italy

- **Art. 615-ter c.p. (Unauthorized access):** executing commands on someone else's PC without authorization is a criminal offense
- **Art. 615-quater c.p. (Possession of access codes):** possessing passwords stolen via exfiltration is a criminal offense
- **Art. 617-quater c.p. (Interception):** capturing other people's WiFi credentials constitutes interception
- **Art. 640-ter c.p. (Computer fraud):** altering the operation of a system for personal gain

### Pentest Best Practices

- **Written authorization** that explicitly mentions "USB HID / BadUSB attack testing"
- **Precise scope:** which PCs, which users, what timeframes, which techniques are permitted
- **Chain of custody:** document every executed payload with timestamp and target
- **Cleanup:** at the end, remove ALL artifacts (downloaded files, registry keys, created users)
- **Do not exfiltrate real data:** in a PoC, demonstrate the capability without extracting actual sensitive data

---
