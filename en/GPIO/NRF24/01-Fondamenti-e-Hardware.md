## 1. Technical Fundamentals of the NRF24L01+

### 1.1 Chip overview

The NRF24L01+ is a 2.4 GHz RF transceiver manufactured by Nordic Semiconductor. It is one of the most widely used radio chips in the world for short- and medium-range wireless communications, found in millions of devices: wireless mice, keyboards, remote controls, IoT sensors, toys, home automation systems, cheap drones.

Key characteristics:

- 2.4 GHz ISM band (2400-2525 MHz) -- no license required
- 126 selectable RF channels (from 2400 to 2525 MHz, with 1 MHz steps)
- Configurable data rate: 250 kbps, 1 Mbps, 2 Mbps
- Maximum TX power: +0 dBm (1 mW) on the base version
- RX sensitivity: -85 dBm at 1 Mbps, -94 dBm at 250 kbps
- Power supply: 1.9V-3.6V (typically 3.3V)
- SPI interface for communication with the host microcontroller
- Ultra-low standby consumption: 900 nA
- TX consumption at 0 dBm: 11.3 mA
- RX consumption at 1 Mbps: 12.3 mA

### 1.2 Internal architecture

The NRF24L01+ integrates:

- RF frequency synthesizer
- Power amplifier (PA)
- Low noise amplifier (LNA)
- GFSK modulator/demodulator (Gaussian Frequency Shift Keying)
- Enhanced ShockBurst engine (hardware)
- TX and RX FIFO (3 levels x 32 bytes each)
- CRC generator (1 or 2 bytes)
- Integrated voltage regulator

The architecture is designed to offload as much of the radio protocol as possible from the host MCU to the chip itself, reducing computational load and overall power consumption.

### 1.3 The 126 RF channels

The operating spectrum spans from 2400 MHz to 2525 MHz. Each channel occupies a bandwidth that depends on the selected data rate:

- At 250 kbps and 1 Mbps: channel bandwidth < 1 MHz
- At 2 Mbps: channel bandwidth < 2 MHz

To avoid overlap at 2 Mbps, channels should be spaced at least 2 MHz apart. At 1 Mbps or 250 kbps, 1 MHz separation is sufficient.

The formula for the operating frequency is:

```
F_operating = 2400 + CH [MHz]
```

Where CH is the channel number (0-125).

Example: channel 76 = 2476 MHz.

The lowest channels (0-20) and highest channels (100-125) tend to have less interference from Wi-Fi, which operates primarily on channels 1, 6, 11 (corresponding to 2412, 2437, 2462 MHz with 22 MHz bandwidth each).

### 1.4 Data Pipe -- 6 pipes per address

One of the most powerful features of the NRF24L01+ is support for 6 simultaneous data pipes in receive mode. Each pipe has a unique address (3 to 5 bytes) and can receive data independently.

- Pipe 0: fully configurable address (3-5 bytes)
- Pipe 1: fully configurable address (3-5 bytes)
- Pipe 2-5: share the upper bytes with Pipe 1, differing only in the least significant byte

This scheme allows a single receiver to communicate with up to 6 different transmitters, each identified by its own pipe address.

In the pentest context, pipes are fundamental: when sniffing, you must configure the correct pipe address to capture traffic from a specific device. MouseJacker exploits precisely the knowledge of pipe addresses to insert itself into the communication.

### 1.5 Enhanced ShockBurst (ESB)

Enhanced ShockBurst is the hardware protocol integrated into the NRF24L01+ that automatically handles:

- Packet assembly (preamble + address + payload + CRC)
- Auto-ACK: the receiver automatically sends an acknowledgment to the transmitter
- Auto-retransmit: if the ACK doesn't arrive, the transmitter repeats the transmission (configurable from 1 to 15 attempts, with delay from 250us to 4000us)
- Hardware-level TX/RX FIFO management

ESB packet format:

```
| Preamble (1 byte) | Address (3-5 bytes) | PCF (9 bit) | Payload (0-32 bytes) | CRC (1-2 bytes) |
```

The PCF (Packet Control Field) contains:

- Payload length (6 bit)
- PID -- Packet ID (2 bit) for detecting duplicate packets
- NO_ACK flag (1 bit) to disable ACK for a single packet

ESB is a double-edged sword for security:

- Pro (for the defender): the ACK mechanism provides reliability
- Con (for the defender): the protocol is completely in the clear, with no encryption or authentication. Anyone who knows the pipe address can inject packets

> Personal note: Enhanced ShockBurst is the heart of everything we do with the NRF24 on the Flipper. Understanding how it works at the packet level is essential. I spent weeks studying the Nordic datasheets before truly feeling comfortable with advanced sniffing. My advice is to read at least chapter 7 of the original NRF24L01+ datasheet -- it's surprisingly well written.

### 1.6 TX power and RX sensitivity

TX power is configurable across 4 levels:

| Level | TX Power | Current Consumption |
|-------|----------|---------------------|
| 0     | -18 dBm  | 7.0 mA              |
| 1     | -12 dBm  | 7.5 mA              |
| 2     | -6 dBm   | 9.0 mA              |
| 3     | 0 dBm    | 11.3 mA             |

Receiver sensitivity varies with data rate:

| Data Rate | RX Sensitivity |
|-----------|----------------|
| 250 kbps  | -94 dBm        |
| 1 Mbps    | -85 dBm        |
| 2 Mbps    | -82 dBm        |

At 250 kbps you get the highest sensitivity (-94 dBm) and therefore the maximum range, at the expense of speed. It's the recommended data rate for long-distance sniffing.

### 1.7 Data rate: 250 kbps vs 1 Mbps vs 2 Mbps

The choice of data rate directly affects:

- Range: 250 kbps achieves the greatest distances
- Channel bandwidth: 2 Mbps requires wider channels
- Throughput: 2 Mbps for fast transfers, 250 kbps for low-power sensors
- Compatibility: many cheap devices use 1 Mbps or 2 Mbps

For pentesting with Flipper Zero:

- Generic sniffing: 1 Mbps (the default for most devices)
- Long-distance sniffing: 250 kbps
- MouseJacker: the data rate must match that of the target peripheral (typically 2 Mbps for Logitech Unifying)

---

## 2. Hardware

### 2.1 NRF24L01+ module versions

There are two main versions of the module commonly available:

**Base version (integrated PCB antenna):**

- Antenna printed directly on the PCB
- TX power: 0 dBm (1 mW)
- Real indoor range: 10-30 meters (with obstacles)
- Real outdoor range (line of sight): 50-80 meters
- Cost: 1-2 euros
- Dimensions: approximately 15mm x 29mm
- 8-pin header (2x4)

**PA+LNA version (external SMA antenna):**

- External Power Amplifier + Low Noise Amplifier
- TX power: up to +20 dBm (100 mW) with the RFX2401C module
- Real indoor range: 50-100 meters
- Real outdoor range (line of sight): 200-1000 meters (with directional antenna)
- Cost: 3-5 euros
- Dimensions: approximately 40mm x 17mm
- SMA connector for external antenna
- 8-pin header (2x4)

For pentesting, the PA+LNA version is strongly recommended:

- The extra range allows operations from safe distances
- The external antenna is replaceable (you can use a directional Yagi)
- The improved RX sensitivity from the LNA captures packets that the base version would miss

> Personal note: I started with the base version at 1.50 euros on AliExpress and it worked, but the range was frustrating. With the PA+LNA the quality leap is enormous. For less than 5 euros you have a transmitter that easily reaches an entire office from the hallway. If you mount an 8 dBi Yagi antenna, the line-of-sight range exceeds 300 meters -- personally tested in an empty parking lot.

### 2.2 Pinout and GPIO connection to the Flipper Zero

The NRF24L01+ module communicates via SPI. The connection to the Flipper Zero is made through the top GPIO connector.

**NRF24L01+ module pinout (viewed from above, header at the bottom):**

```
         +-----+-----+
         | GND | VCC |
         +-----+-----+
         | CE  | CSN |
         +-----+-----+
         | SCK | MOSI|
         +-----+-----+
         | MISO| IRQ |
         +-----+-----+
```

**Connection to Flipper Zero GPIO:**

| NRF24 Pin | Function      | Flipper Zero Pin |
|-----------|---------------|------------------|
| VCC       | Power         | 3.3V (pin 9)     |
| GND       | Ground        | GND (pin 8)      |
| CE        | Chip Enable   | GPIO C0 (pin 15) |
| CSN       | Chip Select   | GPIO A4 (pin 2)  |
| SCK       | SPI Clock     | GPIO B3 (pin 4)  |
| MOSI      | SPI Data In   | GPIO A7 (pin 6)  |
| MISO      | SPI Data Out  | GPIO A6 (pin 5)  |
| IRQ       | Interrupt     | Not connected    |

The IRQ pin is not used by most Flipper Zero NRF24 applications. It can be left unconnected without issues.

### 2.3 Power supply -- watch out for 3.3V

This is a critical point. The NRF24L01+ runs on 3.3V and does NOT tolerate 5V on the I/O pins or on the power supply. Connecting 5V destroys the chip instantly.

The Flipper Zero provides 3.3V from its internal regulator, perfectly compatible.

Common power issues:

- **Insufficient current**: the NRF24L01+ can draw peaks of 115 mA during transmission (PA+LNA version). If the Flipper's regulator cannot provide enough current, you get module resets, failed communications, erratic behavior.
- **Solution**: add a 10-47 uF electrolytic capacitor between VCC and GND of the module, as close to the pins as possible. This stabilizes the power supply during current peaks.
- **Additional filter**: a 100 nF ceramic capacitor in parallel with the electrolytic capacitor filters high-frequency noise.

For the PA+LNA version:

- Consumption in TX at maximum power (+20 dBm) reaches 115 mA
- The Flipper's regulator may struggle
- Consider an external 3.3V power supply if you notice problems
- The 47 uF capacitor is almost mandatory

> Personal note: the capacitor is the difference between a module that works 50% of the time and one that works 100%. I lost two days debugging SPI communication issues before discovering it was simply a power supply problem. Since I started soldering a 47uF capacitor between VCC and GND on every NRF24 module, zero problems. It's advice I give to everyone.

### 2.4 Real-world range -- expectations vs reality

Range depends on many factors:

- Module version (base vs PA+LNA)
- Antenna type (PCB, dipole, Yagi)
- Selected data rate
- Configured TX power
- Environment (indoor/outdoor, walls, Wi-Fi interference)
- Antenna orientation
- Channel frequency in use

Measured real-world range table (approximate):

| Configuration                      | Indoor | Outdoor LOS |
|------------------------------------|--------|-------------|
| Base, PCB antenna, 1 Mbps          | 15m    | 50m         |
| Base, PCB antenna, 250 kbps        | 25m    | 80m         |
| PA+LNA, 2 dBi dipole, 1 Mbps      | 50m    | 200m        |
| PA+LNA, 2 dBi dipole, 250 kbps    | 80m    | 400m        |
| PA+LNA, 8 dBi Yagi, 250 kbps      | N/A    | 800m+       |

For MouseJacker, the operational range is typically 10-50 meters in an office environment with the PA+LNA version. Sufficient to operate from the adjacent meeting room or the hallway.

### 2.5 Practical assembly

The cleanest way to connect the NRF24L01+ module to the Flipper Zero is via a dedicated adapter board or wiring with female-to-female Dupont cables.

Recommended procedure:

1. Use 10-15 cm female-to-female Dupont cables
2. Connect each pin according to the table above
3. Solder the 47 uF capacitor directly onto the module's VCC/GND pins
4. Secure the cables with Kapton tape to prevent disconnections
5. Verify connections with a multimeter before powering on
6. Verify that VCC is on 3.3V and NOT on 5V

If using a proto board or custom PCB adapter:

- Keep SPI traces as short as possible
- Add a ground plane under the SPI traces
- Position bypass capacitors as close to the module as possible

---
