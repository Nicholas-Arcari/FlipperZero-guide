# Personal Experience and Troubleshooting - NFC

Field notes, troubleshooting, and lessons learned during operational use of the NFC module.

---

## Troubleshooting

### "The Flipper won't read the badge"

| Cause | Solution |
|-------|----------|
| Wrong positioning | The NFC coil is on the upper part of the Flipper, behind the screen. Bring the badge close to that area |
| Too far away | Must be within 3-5 cm, ideally <2 cm |
| 125 kHz RFID badge | It's not NFC - try with the RFID module |
| Metal badge holder | Metal shielding blocks the signal - remove the badge from the holder |
| Low battery | NFC requires significant power for the RF field - recharge |
| Unsupported tag | Some proprietary tags (Legic, HID iClass SE) are not fully supported |

### "Dictionary attack doesn't find the keys"

| Cause | Solution |
|-------|----------|
| Keys not in dictionary | Use MFKey32 (Detect Reader) to recover keys from the reader |
| DESFire tag | DESFire doesn't use Crypto-1, not vulnerable to dictionary attack |
| iClass tag | Requires different tools (PicoPass) |
| Incomplete dictionary | Add custom keys to the dictionary from OSINT sources or previous engagements |

### "Emulation doesn't open the door"

| Cause | Solution |
|-------|----------|
| Reader verifies sectors | Full data needed, not just the UID - use complete dump |
| Anti-emulation check | The reader detects it's not a physical tag - use Gen4 Magic Card |
| Incomplete dump | Sectors with missing keys → complete with MFKey32 |
| Timing mismatch | Software emulation has different timing than a real tag - Magic Card |
| Wrong tag type | The reader expects a specific SAK - verify the SAK in the dump |

### "MFKey doesn't recover the keys"

| Cause | Solution |
|-------|----------|
| Too few captures | At least 2 authentications per sector are needed - repeat |
| Presentation too fast | Bring the Flipper close to the reader slowly, hold for 2-3 seconds |
| Non-Crypto1 reader | DESFire, iClass SE don't use Crypto-1 |
| Reader with anti-replay | Rare, but some enterprise readers detect anomalous presentations |

### "The Magic Card doesn't work"

| Cause | Solution |
|-------|----------|
| Incomplete write | Verify that all sectors were written (including Block 0) |
| Gen1 detected | The reader has anti-magic check for WUPC - use Gen4 |
| Wrong SAK/ATQA | Verify that SAK and ATQA on the Magic Card match the original |
| Wrong access keys | After writing, the access keys must match those expected by the reader |

---

## Field Experience

> **Personal note - Corporate badges in Italy:** In my experience, about 60% of Italian offices still use MIFARE Classic 1K. 25% use iClass (often Legacy, therefore vulnerable). Only 15% have migrated to DESFire or modern systems. This means that in the majority of physical pentests, badge cloning is achievable.

> **Personal note - The "cafeteria" technique:** The most effective way to read a badge during an engagement is during the lunch break. Employees leave their badge on the desk or on the cafeteria tray. 3 seconds of contact with the Flipper are enough for a full dump. No elaborate social engineering needed - just walk by.

> **Personal note - Hotel testing:** Hotels are the easiest target. The front desk gives you the card, you read it with the Flipper, clone it to a Magic Card, and test on other doors. I've found critical vulnerabilities (master card, access to all rooms) in 3 out of 4 chains. Assa Abloy Vingcard and Dormakaba systems are the most common - both have had documented vulnerabilities.

> **Personal note - Magic Cards as standard:** I never leave home without at least 10 Gen4 Magic Cards in my kit. The Flipper's emulation fails too often under real-world conditions. A Magic Card is physically a real tag - the reader cannot distinguish it from the original. It's the difference between a "partial" finding and a demo that convinces the client.

---

## Lessons Learned

### Mistakes Not to Repeat

1. **Trusting emulation alone** - it works in the lab, but in the field 40% of readers reject it. Always bring Magic Cards.

2. **Not backing up before writing** - I overwrote a Magic Card with a wrong dump and lost the previous working dump. Now I always Read → save before every Write.

3. **Ignoring the SAK** - a badge with SAK 0x08 (Classic 1K) and one with SAK 0x18 (Classic 4K) are different tags. Writing a 1K dump to a 4K Magic Card with the wrong SAK causes problems.

4. **Not documenting read sectors** - during an engagement with 15 badges, I lost track of which dump belonged to which employee. Now I always rename: `badge_[name]_[uid]_[date].nfc`

5. **Attempting MFKey32 on DESFire** - it doesn't work, DESFire uses AES. I wasted time. Always check the SAK first.

### Best Practices

- **Read → identify → strategize:** first read, then decide the approach based on SAK/ATQA
- **Carry multiple types of Magic Cards** - Gen1 for quick tests, Gen4 for real engagements
- **Custom dictionary** - after every engagement, add the recovered keys to the dictionary for future work
- **Comparator is essential** - ALWAYS use it to understand the data structure (before/after an action)
- **Reading timing** - in social engineering contexts, you have 3-5 seconds. Practice with your own badge
- **SD backup** - NFC dumps are forensic evidence. Back up before every engagement
