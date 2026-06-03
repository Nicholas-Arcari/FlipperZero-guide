# Sub-GHz - Hardware and Real-World Limitations

## The CC1101 Chip

The heart of the Sub-GHz module is the **Texas Instruments CC1101**, a programmable RF transceiver:

- **Frequencies:** 300-348, 387-464, 779-928 MHz (with gaps between bands)
- **Supported modulations:** 2-FSK, 4-FSK, GFSK, MSK, OOK/ASK
- **Receive sensitivity:** -116 dBm @ 0.6 kBaud, 2-FSK
- **Maximum TX power:** +12 dBm (~16 mW) - very low by RF standards
- **Data rate:** 0.6 - 500 kBaud
- **Bandwidth:** configurable, typically 58-812 kHz

## Real-World Limitations You Need to Know

**Transmission range:** Under ideal conditions (line of sight, no interference) the Flipper reaches approximately 30-50 meters. In real environments (walls, interference, corners) the range drops to 5-15 meters. This is the most critical limitation to be aware of.

**Transmission power:** +12 dBm is very low. A typical garage remote transmits at +13/+17 dBm, and a professional transmitter reaches +27 dBm. The Flipper is significantly weaker than most devices it attempts to emulate.

**Frequency gap:** The CC1101 does NOT cover 348-387 MHz and 464-779 MHz. This excludes UHF TV frequencies, some PMR bands, and many military/government systems.

**Internal antenna:** The integrated PCB antenna is a compromise. It is optimized for 433 MHz but loses efficiency at the band edges. External antennas significantly improve performance.

**No full-duplex:** The CC1101 can only transmit OR receive, never both simultaneously.

> **Personal note:** Limited range is the number one problem in the field. During a physical pentest, you need to get very close to the target receiver - often within 10 meters indoors. I have had cases where replaying a gate signal worked perfectly at 3 meters but failed at 8. Solution: get as close as possible and, if necessary, use an external CC1101 antenna connected to the GPIO.

## Improving Performance

**External CC1101 antenna:** External CC1101 modules with a dedicated SMA antenna can be connected via GPIO. This increases the range to 100-200+ meters line of sight and improves receive sensitivity.

**External antenna connection:**
```
Flipper GPIO    CC1101 Module
GND         ->  GND
3.3V        ->  VCC
PA7 (MOSI)  ->  MOSI
PA6 (MISO)  ->  MISO
PB3 (SCK)   ->  SCK
PA4 (CS)    ->  CSN
PB2 (GDO0)  ->  GDO0
PC3 (GDO2)  ->  GDO2 (optional)
```
