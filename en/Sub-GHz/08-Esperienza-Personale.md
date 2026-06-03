# Personal Experience and Troubleshooting - Sub-GHz

Field notes, mistakes made, lessons learned, and solutions to the most common problems during operational use of the Sub-GHz module.

---

## Troubleshooting

### "Read does not decode anything"

| Cause | Solution |
|-------|----------|
| Wrong frequency | Use the Frequency Analyzer before Read |
| Wrong modulation | Try AM <-> FM in the config menu |
| Too far from the transmitter | Move closer to <5 meters |
| Unsupported protocol | Switch to Read RAW for raw capture |
| Damaged antenna | Run Sub-GHz Test for diagnostics |
| Environmental interference | Move the Flipper away from RF sources (routers, phones) |
| Outdated firmware | Some protocols were added in recent updates |

### "Replay does not work"

| Cause | Solution |
|-------|----------|
| Rolling code | The captured code has already been "consumed" - not reusable |
| Insufficient range | Move closer to the receiver (<3-5 meters for indoor environments) |
| Slightly different frequency | Verify the receiver's exact frequency with the Frequency Analyzer |
| Tight receiver timing | The Flipper may not reproduce the exact timing - try repeating |
| Receiver in pairing mode | Some receivers ignore normal signals during pairing |
| Low battery | TX power drops with low battery - recharge and retry |

### "Range too short"

| Cause | Solution |
|-------|----------|
| Limited internal antenna | Use an external CC1101 antenna via GPIO |
| Walls/obstacles | Position yourself in line of sight with the receiver |
| Wrong orientation | The PCB antenna is horizontal - orient the Flipper accordingly |
| Low battery | TX power drops - recharge |
| Receiver with low sensitivity | Not the Flipper's fault - the receiver has a high threshold |

### ".sub file too large"

- RAW recordings can be very large if you record for too long
- Solution: record only 2-3 seconds of signal
- Manually trim the file by removing leading/trailing silence
- Use Shapshup to extract only the useful portion of the signal

### "Frequency Analyzer shows nothing"

- The transmitter is out of range (<1 meter for the Analyzer)
- The frequency might be in the CC1101's gap (348-387 MHz or 464-779 MHz)
- The signal might be too weak or narrowband
- Try with an external antenna for greater sensitivity

---

## Field Experience

> **Personal note - Italian residential gates:** The majority of residential gates I have tested in Italy use Nice or Came systems. Those installed before 2010 are almost always fixed code (Nice FLO 12-bit, Came 12-bit) and are trivial to clone. Those after 2012-2015 use rolling code (Nice FLOR/Smilo, Came TOP). FAAC has always been ahead with security - they use 868 MHz with robust rolling code. BFT and Beninca are mixed.

> **Personal note - Wireless alarms:** I have tested several consumer alarm systems (the ones sold at big-box stores). The majority use 433 MHz sensors with fixed code - 30 seconds of capture with Read is enough to replicate the "zone OK" signal and mask an intrusion. Professional systems (Tecnoalarm, Bentel, DSC) use proprietary protocols with rolling code and anti-jamming. I ALWAYS recommend wired systems for critical zones.

> **Personal note - Real-world Flipper limitations:** The Flipper Zero is fantastic for reconnaissance and quick attacks on fixed codes, but it is not a substitute for a professional SDR setup. For serious analysis I use HackRF + GNURadio to capture and analyze signals, and the Flipper for replay. The combination of the two is extremely powerful: HackRF to understand, Flipper to act.

> **Personal note - TPMS in OSINT:** During an OSINT engagement I used the TPMS reader for 3 days in a target building's parking lot. I built a complete map of employee arrival/departure times based on TPMS sensor IDs. This without cameras, without physical contact, without being detectable. It was one of the most impressive findings for the client.

> **Personal note - Hospital pagers:** Intercepting POCSAG at a hospital (authorized) was one of the most educational experiences. The messages contained patient names, medications, room numbers, emergency codes. All in cleartext. The report led to the replacement of the pager system with an encrypted app. This is the type of finding that justifies the entire engagement.

---

## Lessons Learned

### Mistakes Not to Repeat

1. **Recording RAW for too long** - the files become huge and unusable. 3-5 seconds of recording maximum.

2. **Not verifying the frequency before Read** - I wasted 20 minutes trying to decode a signal on the wrong frequency. ALWAYS use the Frequency Analyzer first.

3. **Attempting replay from too far away** - my first attempts were from 15-20 meters. Total failure. Under 5 meters in indoor environments is much more reliable.

4. **Not documenting captured signals** - I lost important captures because I had not renamed them. Now I always rename with: `[target]_[freq]_[date]_[protocol].sub`

5. **Ignoring protocol timing** - some receivers are timing-sensitive. If the replay does not work, it is not necessarily rolling code - it could be a timing issue.

### Operational Best Practices

- **Frequency Analyzer always first** - before any operation
- **Multiple captures** - record at least 3 different presses of the same remote to confirm consistency
- **Naming convention** - `gate_433_92_nice_flo_12bit.sub`
- **SD backup** - back up the SD card before an engagement - captures are evidence
- **Contextual notes** - save a text file alongside the .sub files with notes about where, when, how
- **External antenna** - for serious engagements, always bring an external CC1101 module
- **Battery** - full charge before the engagement. Sub-GHz consumes more than the other modules
