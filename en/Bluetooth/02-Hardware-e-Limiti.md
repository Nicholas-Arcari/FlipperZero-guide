## Hardware and Real-World Limitations

### The STM32WB55 Chip

Unlike the Sub-GHz module (which uses a separate CC1101 chip), the Flipper Zero's BLE is integrated directly into the main processor: the **STM32WB55RGV6** by STMicroelectronics. This is a dual-core microcontroller with an integrated BLE radio:

**Dual-core architecture:**

- **Application core (CM4)** - ARM Cortex-M4 @ 64 MHz, handles the Flipper firmware, user interface, application logic
- **Radio core (CM0+)** - ARM Cortex-M0+ dedicated exclusively to the BLE stack, separate and protected firmware

This architecture is important: the radio core runs a BLE firmware certified by ST (the "Wireless Stack") that handles all low-level BLE protocol operations. The application core communicates with the radio core through an IPCC (Inter-Processor Communication Controller) interface and a shared RAM mailbox.

**BLE radio specifications:**

| Parameter | Value |
|---|---|
| Standard | Bluetooth 5.0 |
| Frequency | 2.4 GHz ISM (2400-2483.5 MHz) |
| Channels | 40 (3 advertising + 37 data) |
| Modulation | GFSK |
| TX Power | -20 dBm to +6 dBm (configurable) |
| RX Sensitivity | -96 dBm @ 1 Mbps |
| Supported PHYs | LE 1M, LE 2M, LE Coded (S=8) |
| Practical Throughput | ~200-700 kbps |

**Maximum TX power: +6 dBm.** This is the crucial figure. +6 dBm equals approximately 4 milliwatts. For comparison, a modern smartphone typically transmits BLE at +4/+8 dBm, a commercial beacon at +4/+8 dBm, and a long-range BLE device can reach +20 dBm. The Flipper sits in the lower average.

### Integrated PCB Antenna

The Flipper Zero uses an integrated PCB antenna printed directly on the motherboard. It's not a replaceable external antenna like the Sub-GHz one. Characteristics:

- **Type:** PCB trace antenna (Inverted-F or meander line)
- **Gain:** Approximately 0-2 dBi (depends on frequency and orientation)
- **Radiation pattern:** Quasi-omnidirectional on the horizontal plane
- **Polarization:** Linear

The antenna cannot be modified without significant hardware intervention. This is a fixed limitation of the Flipper: you cannot attach an external BLE antenna like you do with the CC1101 for Sub-GHz.

### Real-World Range

The Flipper's BLE range varies significantly depending on conditions:

| Scenario | Typical Range |
|---|---|
| Line of sight, outdoor, no interference | 20-30 meters |
| Indoor, same room, few obstacles | 10-20 meters |
| Indoor, through one wall | 5-15 meters |
| Indoor, multiple walls, WiFi interference | 3-8 meters |
| Very crowded environment (conference, office) | 5-10 meters |

Factors that degrade range:

- **Walls and physical obstacles** - 2.4 GHz penetrates concrete and metal poorly
- **WiFi interference** - WiFi operates on the same band and creates noise
- **Crowded Bluetooth** - In environments with many BLE devices, the channel becomes congested
- **Orientation** - The PCB antenna has a directional pattern; rotating the Flipper can make a difference
- **Human body** - The body absorbs 2.4 GHz; keeping the Flipper in your pocket reduces range

> **Personal note:** In real-world pentest environments, the effective range for BLE Spam is approximately 5-15 meters. I've tested in open-plan offices and most devices receive the popups within 10 meters. Beyond 15 meters the success rate drops drastically. For meeting room demos, placing the Flipper in the center of the table is the best strategy - guaranteed coverage across the entire table and surrounding chairs.

### Radio Core Firmware

The CM0+ core runs the **STM32WB Wireless Stack**, a binary firmware provided by ST:

- **stm32wb5x_BLE_Stack_full_fw.bin** - Complete BLE stack (GAP, GATT, SMP, L2CAP)
- Updated through the Flipper firmware update (OTA or via qFlipper)
- Not open source - it's a certified binary blob
- Supports up to 8 simultaneous connections
- Supports simultaneous advertising and scanning (if the firmware allows it)

Custom Flipper firmware (RogueMaster, Unleashed, Momentum, Xtreme) does not modify the ST wireless stack. It only modifies the application firmware on the CM4 core. The differences between custom firmwares for BLE features therefore only concern the applications (BLE Spam, scanner, HID), not the underlying radio stack.

---
