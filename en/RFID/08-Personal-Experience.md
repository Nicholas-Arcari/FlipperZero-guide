## Troubleshooting and Limitations

### Common Problems and Solutions

#### "The Flipper does not read the tag"

**Possible causes:**

| Cause | Diagnosis | Solution |
|---|---|---|
| Tag is not 125 kHz | Try with NFC (13.56 MHz) | Use the NFC module |
| Tag out of range | Move closer | Direct contact with the Flipper |
| Wrong orientation | Coils not parallel | Rotate the tag 90 degrees |
| Damaged tag | Try another known tag | If the known one also fails, it is a Flipper issue |
| Metal interference | Metal near the antenna | Move metal objects away |
| Low battery | Check battery level | Charge the Flipper |
| Unsupported protocol | The Flipper does not decode | Use Proxmark3 for analysis |
| HF tag, not LF | NFC badge mistaken for RFID | Check with the Detector |
| Metal case | Flipper case is shielding | Remove the case |

#### "Reading is unstable / different IDs every time"

**Possible causes:**
- The tag has a defective chip - try another tag
- Environmental interference - electric motors, transformers, fluorescent lights nearby
- The tag is multi-technology (LF + HF) and the Flipper is confused between the two signals
- Flipper battery below 20% - field power drops

**Solution:** make sure to keep the tag still during reading. If the problem persists, use the Proxmark3 for a raw read and verify the signal.

#### "Emulation does not work on the reader"

**Possible causes and solutions:**

1. **Wrong protocol:** the Flipper emulates EM4100 but the reader expects HID
   - Solution: verify the reader's protocol by reading a badge that works

2. **Imprecise timing:** software emulation is not identical to a hardware tag
   - Solution: write to T5577 (hardware emulation, not software)

3. **Insufficient range:** the reader requires a stronger signal
   - Solution: press the Flipper directly against the reader, try different positions

4. **The reader is HF, not LF:** it looks like an RFID reader but operates at 13.56 MHz
   - Solution: use the Detector to verify the frequency

5. **The reader has a database and the ID is not authorized:**
   - This is not a bug - the system is working correctly
   - Solution: read an authorized badge and clone that one

6. **Outdated firmware:** the Flipper has known bugs in LF emulation
   - Solution: update the firmware to the latest version

#### "Writing to T5577 fails"

**Possible causes and solutions:**

1. **It is not a T5577:** it might be an EM4100 (read-only) sold as a T5577
   - Diagnosis: if the Flipper says "Writing..." but then "Error", it is probably not writable
   - Solution: try a T5577 from a different supplier

2. **Password-protected T5577:** someone has set a password
   - Diagnosis: the Flipper shows a write error even at contact
   - Solution: if you know the password, use the Raw Writer. Otherwise, use a new T5577

3. **T5577 with corrupted Block 0:** invalid configuration written previously
   - Diagnosis: the tag does not respond to reading or writing
   - Solution: try writing Block 0 with a standard value (0x00148040) via the Raw Writer. If it does not work, the tag is unrecoverable without a Proxmark3

4. **Incorrect positioning:** the T5577 is not close enough
   - Solution: direct contact, held still for 3 seconds

5. **Low battery:** writing requires more power than reading
   - Solution: charge the Flipper to at least 50%

#### "The Detector does not detect the reader"

**Possible causes:**

1. The reader is off or in standby (some only activate on proximity sensor)
2. The reader operates at a non-standard frequency (e.g. 134.2 kHz for FDX-B)
3. The reader is too far away - get within 5 cm
4. The reader is electrically shielded (rare but possible)
5. It is not an RFID reader - it might be an intercom, an IR sensor or a pushbutton

#### "The RFID Fuzzer does not find any valid IDs"

**Possible explanations:**

1. **The system has a restrictive database:** great for security, frustrating for the pentester
2. **You are fuzzing the wrong protocol:** verify with a valid badge
3. **The Facility Code is wrong:** for HID, you must have the correct FC
4. **Rate limiting:** the reader blocks rapid attempts - slow down the fuzzing
5. **The search space is too large:** for EM4100 at 40 bits, complete brute force is impractical
6. **The reader is not standalone:** it is connected to a central controller that manages access - local fuzzing is pointless

### Intrinsic Limitations of the Flipper Zero for RFID

1. **No raw sniffing:** you cannot intercept communication between a badge and a third-party reader (Proxmark3 needed)
2. **No password cracking:** you cannot recover the password of a protected T5577
3. **Limited protocols:** ~20 protocols vs 50+ on the Proxmark3
4. **No signal analysis:** you cannot visualize the raw waveform
5. **No EM4305 writing:** only supports T5577 as a write target
6. **Imperfect emulation:** software emulation has higher timing tolerances than a physical tag
7. **Fixed range:** you cannot connect external antennas for the LF band
8. **No support for 134.2 kHz induction tags:** FDX-B support is limited because the antenna is optimized for 125 kHz

---

## Personal Experience

### The Reality of RFID 125 kHz in Italy

> **Personal note:** After hundreds of engagements in Italy, I can say with certainty that RFID 125 kHz is the MOST vulnerable physical access technology still in use. Here is the situation:

> **Apartment buildings (90% EM4100):** the vast majority of Italian apartment buildings built or renovated between 2000 and 2020 have an access control system based on EM4100. Badges cost 2-5 EUR each, the system is cheap to install, and no one thinks about security. I have tested over 50 apartment buildings and ALL of them were vulnerable to cloning in less than 10 seconds. I have never found an Italian apartment building with encryption on the badge.

> **Personal note:** The most absurd moment of my career was when a building administrator told me: "But the badges are electronic, you can't copy them like keys!" - while I was holding a T5577 that I had just written in 5 seconds and that opened his front door. The perception of security of "electronic" is completely disconnected from reality.

### Field Operational Tips

> **Personal note: Minimum RFID kit for an engagement:**
> - 10x T5577 keyfob format (various colors to distinguish them)
> - 5x T5577 ISO card format (for readers that only accept cards)
> - 1x T5577 coin format (for special cases)
> - Colored adhesive tape for labeling clones
> - Anti-static bag for blank T5577s
> - The Flipper Zero with a full battery
> - Proxmark3 RDV4 in the backpack (for emergencies)
> - 5000 mAh power bank (continuous reading drains the battery)

> **Personal note: Mistakes I have made and you should avoid:**
>
> 1. **Not verifying the clone before use:** once I wrote a T5577 and went directly to the target reader. It did not work. The T5577 was defective and the write had not succeeded. Now I ALWAYS verify by reading the T5577 after writing.
>
> 2. **Confusing LF and HF:** modern badges are often dual-frequency (LF + HF). The badge has both an EM4100 chip and a MIFARE chip. The reader might only use the HF part. The Detector saves you from this mistake.
>
> 3. **Underestimating read range:** I thought contact was required. In reality, with good positioning I read EM4100 at 7-8 cm. This means I can read a badge in the pocket of a hanging jacket.
>
> 4. **Not protecting T5577s with a password:** if you lose a cloned T5577 during an engagement, anyone who finds it can read your client's badge ID. Always set a password on the T5577 after cloning.
>
> 5. **Operating without written authorization:** already mentioned above, but worth repeating. NEVER.

### When the Flipper Is Not Enough

> **Personal note:** There are situations where the Flipper Zero is insufficient for RFID 125 kHz work:
>
> - **Unknown protocol:** the Flipper says "Unknown" and does not decode anything. The Proxmark3 with `lf search` and `lf rawdemod` can analyze the raw signal and identify the modulation.
>
> - **Password-protected T5577:** the Flipper has no brute force function for T5577 passwords. The Proxmark3 with `lf t5 bruteforce` takes a few minutes to try common passwords.
>
> - **EM4305 tags:** an alternative to the T5577 that the Flipper does not support for writing. Proxmark3 needed.
>
> - **Real FDX-B cloning at 134.2 kHz:** the Flipper operates at 125 kHz and cannot generate a perfect signal at 134.2 kHz. For FDX-B readers that are strict about frequency, a Proxmark3 or dedicated FDX-B reader is needed.
>
> - **Analysis of custom readers:** in industrial or military environments, readers may use completely proprietary protocols. The Proxmark3 with its raw capture capability is the only adequate tool.
>
> - **Extended-range covert testing:** when ranges beyond 10 cm are needed (e.g. skimming test), the Flipper lacks the power. Custom hardware with an amplifier and external antenna is needed.

### The Future of 125 kHz

> **Personal note:** RFID 125 kHz is a dead technology that refuses to die. The reasons it is still everywhere:
>
> - **Cost:** an EM4100 system costs 1/10th of a MIFARE DESFire system
> - **Simplicity:** the installer does not have to configure cryptographic keys
> - **Compatibility:** decades of badges in circulation, impossible to replace them all
> - **Ignorance:** most installers and clients do not know it is insecure
> - **Inertia:** "it works, why change it?"
>
> The migration will happen inevitably, but slowly. In the meantime, RFID 125 kHz remains the most fertile playground for a physical pentester. A Flipper Zero and a few T5577s in your pocket - that is all you need to demonstrate that 90% of physical access control systems in Italy are nothing but a security illusion.

---

## References and Resources

### Datasheets and Specifications

- **EM4100 Datasheet** - EM Microelectronic: complete protocol structure
- **T5577 Datasheet (ATA5577)** - Microchip Technology: registers, configuration, timing
- **HID Prox Formats** - HID Global Technical Reference Guide
- **ISO 11784/11785** - International standard for animal identification (FDX-B)
- **DCF77 Protocol** - PTB (Physikalisch-Technische Bundesanstalt) specification

### Complementary Tools

- **Proxmark3** (RDV4 or Easy) - for advanced analysis and protocols not supported by the Flipper
- **RTL-SDR** - for visualizing the RF signal at 125 kHz (requires upconverter)
- **GNURadio** - for custom demodulation and signal analysis
- **RFIDler** - open source alternative to Proxmark3 for LF

### Flipper Zero Firmware

- **Official firmware** - basic RFID 125 kHz support
- **RogueMaster** - additional protocols, improved fuzzer
- **Unleashed** - additional protocols and extra features
- **Xtreme** - improved UI and additional tools

> **Personal note:** I use RogueMaster as my primary firmware for RFID work. It supports more protocols than the official firmware and the fuzzer has additional options. For a pentester, custom firmware is practically mandatory. The official firmware is perfect for learning, but in the field you need the extra features.

---

*Guide written for the FlipperZero-guide project. Content for educational and security research purposes. Improper use of the techniques described is illegal and criminally prosecutable. Always operate with written authorization.*
