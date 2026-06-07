## 9. Personal Experience

### Lessons learned in the field

> Personal note: after hundreds of hours of hardware hacking with the Flipper Zero, here are the most important lessons I've learned.

#### On the general approach

> Personal note: patience is the most important virtue in hardware hacking. Unlike software pentesting where you can iterate rapidly, with hardware every mistake can cost you a burned chip or a damaged PCB. Measure twice, connect once. Always verify voltage before connecting anything.

#### On tools

> Personal note: the Flipper Zero is not the best SWD debugger, not the best SPI programmer, not the best I2C scanner. But it's the only one that has all of them in a pocket-sized device. My field kit includes the Flipper, a set of SOIC-8 clips, jumper wires, a pocket multimeter, and a couple of pogo pins. With this kit I get into most IoT devices without problems.

#### On readout protection

> Personal note: I've lost count of how many times readout protection was disabled on "security" devices. Smart locks, alarms, cameras -- most have SWD completely open. Manufacturers don't activate protections because they complicate production and warranty debugging. This is a gift for us pentesters, but it's also a serious problem for consumer security.

#### On SPI dump

> Personal note: invest in a good SOIC-8 clip. The cheap 2 EUR clips lose contact constantly and produce corrupted dumps. The Pomona 5250 costs 15-20 EUR but makes perfect contact on the first try. In the long run, you save time and frustration. And ALWAYS do two consecutive dumps and compare them -- there is no reliable dump without verification.

#### On UART

> Personal note: UART is the first thing I look for on any PCB. It's the simplest and least invasive method for obtaining information about a device. Even when there's no interactive shell, boot logs reveal firmware versions, network addresses, active services, and sometimes credentials. I've seen WiFi passwords printed in the boot logs of IP cameras. Literally in the clear, during every reboot.

#### On AVR fuse bits

> Personal note: I bricked my first ATtiny85 within 15 minutes of starting my journey with AVRs. I had disabled RSTDISBL thinking I'd gain an extra GPIO pin, without knowing that without a reset pin you can't program via ISP anymore. Lesson learned: read the datasheet BEFORE touching fuse bits, and ALWAYS back up the current fuses before modifying them.

#### On documentation

> Personal note: document EVERYTHING. Every pin you identify, every connection you make, every dump you extract. Use photos with annotations, notes with timestamps, and a consistent file naming convention. In a complex assessment with dozens of devices, documentation is what separates a professional job from an unmanageable mess.

#### On legal compliance

> Personal note: all scenarios described in this guide are to be executed exclusively on devices you own or with explicit written authorization from the owner, in the context of security assessment, research, or learning activities. Unauthorized access to computer systems is a crime. Knowledge of hardware hacking techniques serves to defend, not to attack.

---

## Appendix A -- Quick References

### Flipper Zero Debug GPIO Pinout

```
Flipper Zero GPIO Header (top view, USB on the left):

    +--[USB-C]--+
    |           |
 1  | 3V3   GND | 18
 2  | SWC   A7  | 17
 3  | SIO   A6  | 16
 4  | MISO  A4  | 15
 5  | CS    B3  | 14
 6  | SDA   B2  | 13
 7  | SCL   C3  | 12
 8  | GND   C1  | 11
 9  | 3V3   C0  | 10
    |           |
    +-----------+

Legend:
SWC = SWCLK (Pin 2)
SIO = SWDIO (Pin 3)
```

### Quick table -- Which tool to use

| Situation | Tool | First step |
|-----------|------|------------|
| Unknown ARM MCU | SWD Probe | Read IDCODE |
| ARM firmware debug | DAP Link + OpenOCD | Connect GDB |
| AVR MCU (Arduino) | AVR Flasher | Read signature |
| EEPROM on the PCB | I2C Tools | Scan bus |
| External flash SOIC-8 | SPI Mem Manager | Read JEDEC ID |
| Suspicious Ethernet port | Ethernet Troubleshooter | Check link status |
| Serial console | UART (GPIO app) | Try 115200 baud |

### Essential post-dump commands

```bash
# Generic firmware analysis
binwalk firmware.bin
binwalk -e firmware.bin
strings -n 8 firmware.bin > strings.txt
entropy firmware.bin

# Specific to embedded Linux
unsquashfs filesystem.squashfs
cat etc/shadow
find . -name "*.conf" -exec grep -l "pass" {} \;

# AVR analysis
avr-objdump -D -m avr firmware.bin > disasm.asm

# ARM Cortex-M analysis
arm-none-eabi-objdump -D -b binary -m arm firmware.bin > disasm.asm

# Dump comparison
md5sum dump1.bin dump2.bin
diff <(xxd dump1.bin) <(xxd dump2.bin)
```

### Useful resources

- Winbond W25Qxx Datasheet: contains all SPI flash specifications
- ARM CoreSight Architecture Spec: for deep understanding of SWD/JTAG
- Nordic nRF52832 Product Spec: memory map, UICR, APPROTECT
- Atmel ATmega328P Datasheet: fuse bits, lock bits, ISP protocol
- OpenOCD User Guide: complete configuration for ARM debugging
- Ghidra: free disassembler from the NSA, supports ARM and AVR
- binwalk: embedded firmware extraction and analysis
