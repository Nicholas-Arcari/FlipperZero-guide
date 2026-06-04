## Advanced BLE Attacks

This section describes BLE attacks that go beyond the Flipper's native capabilities but are relevant for a pentester operating in the BLE ecosystem.

### BLE Sniffing

BLE sniffing consists of capturing radio traffic between two connected BLE devices. The Flipper CANNOT perform complete BLE sniffing.

**Why the Flipper cannot sniff:**

1. The Flipper's scanner only sees advertising packets (channels 37/38/39)
2. An active BLE connection uses data channels (0-36) with frequency hopping
3. To follow the frequency hopping, you need to know the Access Address and channel map of the connection
4. This information is exchanged during the Connection Request (CONNECT_IND)
5. The Flipper does not have the capability to capture CONNECT_IND and follow the hopping pattern

**Hardware for BLE sniffing:**

| Hardware | Capability | Price |
|---|---|---|
| **Ubertooth One** | Complete BLE 4.x/5.0 sniffing, follow connections | ~120-150 EUR |
| **nRF52840 Dongle** | BLE sniffing with nRF Sniffer for Bluetooth LE | ~10-15 EUR |
| **HackRF One** | Raw 2.4 GHz sniffing (with gr-bluetooth) | ~300 EUR |
| **TI CC2540 Dongle** | BLE 4.0 sniffing with SmartRF Sniffer | ~30-50 EUR |
| **Sniffle** (nRF52840) | Open source BLE 5.x sniffer, supports LE Coded | ~15 EUR (dongle only) |

**The most recommended for BLE sniffing is the nRF52840 dongle with Sniffle firmware** - it's inexpensive, open source, supports full BLE 5.0, and integrates with Wireshark.

**Typical BLE sniffing workflow:**

1. Start the sniffer on the advertising channel
2. Capture the CONNECT_IND when the target connects
3. Extract Access Address, CRC init, channel map, hop interval
4. Configure the sniffer to follow the connection
5. Capture data traffic (L2CAP, ATT, GATT)
6. Analyze with Wireshark (built-in BLE dissector)

### BLE MITM (Man-in-the-Middle)

The BLE MITM attack consists of positioning yourself between the peripheral device (e.g., smart lock) and the central (e.g., smartphone), intercepting and potentially modifying the communication.

**Prerequisites:**

- The target must use **Just Works** pairing or **pairing with a weak PIN**
- The attacker must intercept the connection phase
- Dedicated hardware and software are required (GATTacker, BtleJuice, BTLE-Sniffer)

**The Flipper CANNOT perform native BLE MITM.** A setup is needed with:

- Two BLE radios (one pretending to be the peripheral to the central, one pretending to be the central to the peripheral)
- MITM software (GATTacker on Linux with two BLE dongles, or BtleJuice)
- Ability to clone the GATT profile of the target device

**GATTacker workflow:**

```
Smartphone <--BLE--> [Attacker Radio A] <--TCP--> [Attacker Radio B] <--BLE--> Smart Lock
                      (pretends to be                (pretends to be
                       the lock)                      the smartphone)
```

1. Scan the GATT profile of the target lock (services, characteristics, descriptors)
2. Clone the profile on Radio A
3. Jam or wait for the smartphone to lose the original connection
4. The smartphone reconnects to Radio A (which looks like the lock)
5. Radio B connects to the real lock pretending to be the smartphone
6. All traffic passes through the attacker, who can read, modify, or block packets

### BLE Replay Attack

A replay attack consists of capturing a legitimate BLE command and retransmitting it later to reproduce the action.

**Replay vulnerability:**

BLE devices are vulnerable to replay if:

- They don't use nonce/counter in commands
- They don't use challenge-response
- They don't verify message freshness
- They use static commands for critical operations (lock opening, unlock)

**The Flipper can perform limited BLE replay:**

- It can capture advertising packets and retransmit them (useful for beacon spoofing)
- It CANNOT capture and retransmit traffic on active connections (requires a sniffer)
- For replay on connections, you first need to sniff the traffic with dedicated hardware, then use a tool to retransmit it

**Practical example - vulnerable smart lock:**

Some cheap smart locks use static BLE GATT commands for opening:

```
Write Request to Handle 0x0015: Value 0x55AA01 (Unlock)
Write Request to Handle 0x0015: Value 0x55AA02 (Lock)
```

If you capture this command with a sniffer, you can retransmit it with any BLE device (including the Flipper, if you manage to connect to the lock). This type of vulnerability is common in cheap Chinese locks but rare in established brand products (August, Yale, Nuki) that use challenge-response with nonce.

### GATT Fuzzing

GATT fuzzing consists of sending malformed or unexpected data to a device's GATT characteristics to find crashes, vulnerabilities, or anomalous behavior.

**GATT fuzzing techniques:**

- **Value fuzzing** - Send out-of-range values, too long, too short, NULL
- **Handle fuzzing** - Attempt read/write on non-existent or protected handles
- **Type fuzzing** - Send unsupported operations (write to read-only, etc.)
- **Sequence fuzzing** - Send operations in unexpected order
- **MTU fuzzing** - Negotiate anomalous MTUs

**Dedicated tools:**

- **BLEzzer** - Open source BLE fuzzing framework
- **Sweyntooth** - Exploit suite for BLE stack vulnerabilities
- **InternalBlue** - Framework for firmware-level Bluetooth analysis
- **BTLE-Sniffer** - Tool for BLE analysis and manipulation

The Flipper can be used for very basic fuzzing (attempting connections, reading services, writing values), but for systematic fuzzing a Linux setup with BLE dongles and dedicated frameworks is required.

### BLE Denial of Service

The massive sending of advertising packets (BLE Spam) is effectively a form of soft Denial of Service on the BLE channel:

- **Advertising channel saturation** - With high advertising frequency, channels 37/38/39 become congested, making it difficult for legitimate devices to complete discovery
- **Popup flooding** - On target devices, continuous popups make normal phone usage difficult
- **Battery drain** - Continuous processing of advertising packets increases battery consumption of nearby devices (minimal but measurable effect)
- **Connection interference** - In rare cases, aggressive advertising can interfere with existing BLE connections if the target device misses a connection event to process the advertising

However, BLE is resilient to DoS thanks to frequency hopping and coexistence with other 2.4 GHz protocols. A single Flipper cannot completely block BLE in an area.

> **Personal note:** I tested the impact of BLE Spam on existing BLE connectivity. With the Flipper spamming at full power, existing BLE connections (headphones, wearables) do NOT disconnect. The impact is limited to the popups and a slight increase in latency for new device discovery. It's not an effective DoS against active connections - just interference with the user experience. For a real BLE DoS you would need multiple transmitters or a 2.4 GHz jammer (which is illegal).

---
