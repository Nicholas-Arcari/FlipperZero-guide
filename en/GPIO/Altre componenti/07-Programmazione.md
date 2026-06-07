# Programming - EEPROM, Flashing, and Memory

This section covers GPIO tools dedicated to chip programming, EEPROM read/write, and firmware flashing on compatible microcontrollers.

---

### • Coffee EEPROM

Tool for accessing EEPROMs found in coffee machines (DeLonghi, Nespresso, etc.) used to store counters, configurations, and calibration parameters.

Extended features:

- Automatic chip identification (24Cxx, 93Cxx, etc.).
- Complete memory read.
- Binary backup.
- Safe editing of known areas (volumes, descaling cycles).
- "Safe Zone" protection to avoid firmware corruption.

Practical example

Descaling counter reset:

- Connect SDA/SCL.
- Perform complete dump → save backup.
- Modify the byte related to the counter.
- Write only the modified sector.
- Restart the machine and verify the reset.

### • WHC SWIO Flasher

SWIO module flasher via GPIO.

Extended features:

- SWIO firmware read and write.
- Complete module backup.
- Post-flash checksum verification.
- Compatible with various SWIO-compatible microcontrollers.

Practical example

Firmware update:

- Connect SWIO → power the target.
- Load firmware → flash.
- Verify checksum → test functionality.
