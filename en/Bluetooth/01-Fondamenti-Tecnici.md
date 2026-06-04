## Technical Fundamentals

### Bluetooth Low Energy vs Bluetooth Classic

First and foremost, it's essential to understand that the Flipper Zero uses **exclusively Bluetooth Low Energy (BLE)**, not Bluetooth Classic. These are two completely different stacks, even though they share the name and frequency band (2.4 GHz ISM).

**Bluetooth Classic (BR/EDR):**

- Designed for continuous data streaming (audio, file transfer)
- Data rate up to 3 Mbps (EDR)
- Consumes significantly more power
- Used for: audio headphones, file transfer, tethering, legacy keyboards
- Requires formal pairing with PIN/passkey
- Connection-oriented: must establish a connection before transmitting data

**Bluetooth Low Energy (BLE):**

- Designed for short, intermittent transmissions
- Theoretical data rate up to 2 Mbps (BLE 5.0), practical 200-800 kbps
- Drastically lower power consumption
- Used for: IoT, beacons, trackers, sensors, wearables, smart locks
- Supports both connection-oriented and connectionless (advertising) modes
- Can transmit data without formal connection (advertising packets)

This distinction is critical: the Flipper CANNOT interact with Bluetooth Classic devices (standard audio headphones, OBEX file transfer, tethering). It can only operate in the BLE space.

### The BLE 5.0 Stack

BLE is organized into well-defined layers. Understanding the stack is essential to grasp what the Flipper can and cannot do.

#### Physical Layer (PHY)

The physical layer operates in the 2.4 GHz ISM band (2400-2483.5 MHz), divided into 40 channels of 2 MHz each:

- **Channels 37, 38, 39** - Advertising channels (2402, 2426, 2480 MHz)
- **Channels 0-36** - Data channels for active connections

BLE 5.0 supports three PHY modes:

| PHY | Data Rate | Range | Use |
|---|---|---|---|
| **LE 1M** | 1 Mbps | Standard (~30m) | Default, maximum compatibility |
| **LE 2M** | 2 Mbps | Reduced (~15m) | High throughput, lower range |
| **LE Coded** | 125/500 kbps | Extended (~100m+) | Long range, outdoor IoT |

The Flipper Zero primarily uses LE 1M. Frequency hopping occurs across all 40 channels using a pseudo-random algorithm to mitigate interference and improve coexistence with other 2.4 GHz devices (WiFi, microwaves, ZigBee).

#### Link Layer

The Link Layer manages BLE device states:

- **Standby** - Radio off, no activity
- **Advertising** - Transmits advertising packets on channels 37/38/39
- **Scanning** - Listens for advertising packets on channels 37/38/39
- **Initiating** - Sends connection request after receiving an advertising packet
- **Connected** - Active bidirectional connection on data channels

The transition between states is the core of how BLE works:

```
Standby --> Advertising --> Connected
   |            |
   +--> Scanning --> Initiating --> Connected
```

Each advertising event consists of transmitting the same packet on the three advertising channels (37, 38, 39) in rapid sequence. The interval between advertising events is configurable (20ms - 10.24s). Shorter intervals = device discoverable more quickly, but higher power consumption.

#### L2CAP (Logical Link Control and Adaptation Protocol)

L2CAP manages the multiplexing of logical channels over the physical connection:

- Packet fragmentation and reassembly
- **MTU (Maximum Transmission Unit)** management - default 23 bytes, negotiable up to 512+ bytes
- Flow control for BLE 5.0

The MTU is an important parameter in practice: an MTU of 23 bytes means each ATT packet carries at most 20 bytes of payload (3-byte ATT header). With MTU negotiated to 247 bytes, actual throughput increases significantly.

#### ATT (Attribute Protocol)

ATT defines the client-server protocol for accessing data:

- **Server** - Exposes attributes (the BLE peripheral device)
- **Client** - Reads/writes attributes (the smartphone, the Flipper in scanner mode)

Each attribute has:

- **Handle** - 16-bit numeric identifier (0x0001 - 0xFFFF)
- **Type** - UUID defining the attribute type
- **Value** - The actual data
- **Permissions** - Read, Write, Notify, Indicate, with or without authentication/encryption

Main ATT operations:

| Operation | Direction | Description |
|---|---|---|
| Read Request | Client -> Server | Read the value of an attribute |
| Write Request | Client -> Server | Write a value and wait for confirmation |
| Write Command | Client -> Server | Write without confirmation (fire-and-forget) |
| Notification | Server -> Client | Server sends an update (no confirmation) |
| Indication | Server -> Client | Server sends an update (with confirmation) |

#### GATT (Generic Attribute Profile)

GATT is the framework built on top of ATT that organizes data in a hierarchical structure:

```
GATT Server
  |
  +-- Service (UUID: 0x180F - Battery Service)
  |     |
  |     +-- Characteristic (UUID: 0x2A19 - Battery Level)
  |           |
  |           +-- Value: 85 (percentage)
  |           +-- Descriptor (CCCD: 0x2902 - Client Config)
  |
  +-- Service (UUID: 0x1812 - HID Service)
        |
        +-- Characteristic (Report Map)
        +-- Characteristic (Report)
        +-- Characteristic (Protocol Mode)
```

**Services** group logical functionalities. Standard services have 16-bit UUIDs assigned by the Bluetooth SIG:

| UUID | Service | Description |
|---|---|---|
| 0x1800 | Generic Access | Device name, appearance |
| 0x1801 | Generic Attribute | Service Changed |
| 0x180A | Device Information | Manufacturer, model, firmware |
| 0x180F | Battery Service | Battery level |
| 0x1812 | Human Interface Device | HID (keyboard, mouse) |
| 0xFE2C | Google Fast Pair | Google quick pairing |

Custom services use 128-bit UUIDs (e.g.: `6E400001-B5A3-F393-E0A9-E50E24DCCA9E` for the Nordic UART Service used by the Flipper).

**Characteristics** contain the actual values and their properties. **Descriptors** provide additional metadata about the characteristic (the most important being the CCCD - Client Characteristic Configuration Descriptor, used to enable notification/indication).

#### GAP (Generic Access Profile)

GAP defines the roles and procedures for discovery and connection:

**GAP Roles:**

- **Broadcaster** - Transmits advertisements, does not accept connections
- **Observer** - Receives advertisements, does not connect
- **Peripheral** - Advertises and accepts connections (the Flipper in HID mode)
- **Central** - Scans and initiates connections (the Flipper in scanner mode, the smartphone)

**GAP Procedures:**

- **Discovery** - Finding nearby devices through scanning
- **Connection Establishment** - Creating a BLE connection
- **Bonding** - Saving security keys for future reconnections
- **Name Discovery** - Reading the remote device name

### Advertising Packets - The Heart of BLE

Advertising packets are the fundamental mechanism of BLE and underpin everything the Flipper does with Bluetooth. Each advertising PDU (Protocol Data Unit) has this structure:

```
+----------+----------+------------------+
| Preamble | Access   | PDU              |
| (1 byte) | Address  | (2-39 bytes)     |
|          | (4 bytes)|                  |
+----------+----------+------------------+

PDU:
+--------+--------+----------------------------+
| Header | Length | Payload                    |
| (2 B)  | (1 B)  | (0-31 bytes data + addr)  |
+--------+--------+----------------------------+
```

**Advertising PDU types:**

| Type | Name | Description |
|---|---|---|
| 0x00 | ADV_IND | Connectable, undirected - the most common |
| 0x01 | ADV_DIRECT_IND | Connectable, directed - for a specific target |
| 0x02 | ADV_NONCONN_IND | Non-connectable, undirected - broadcast only |
| 0x03 | SCAN_REQ | Scan response request |
| 0x04 | SCAN_RSP | Scan request response - additional data |
| 0x06 | ADV_SCAN_IND | Scannable, non-connectable |

The advertising payload contains **AD Structures** (Advertising Data Structures), each with the format:

```
+--------+--------+-------------------+
| Length | Type   | Data              |
| (1 B)  | (1 B)  | (Length-1 bytes) |
+--------+--------+-------------------+
```

Common AD types:

| Type | Name | Use |
|---|---|---|
| 0x01 | Flags | LE General Discoverable, BR/EDR Not Supported |
| 0x02 | 16-bit UUID List (incomplete) | Offered services |
| 0x06 | 128-bit UUID List (incomplete) | Custom services |
| 0x08 | Shortened Local Name | Device name |
| 0x09 | Complete Local Name | Complete device name |
| 0x0A | TX Power Level | Transmission power |
| 0xFF | Manufacturer Specific Data | Vendor proprietary data |

The **0xFF (Manufacturer Specific Data)** type is the most relevant for BLE Spam: it contains a 16-bit Company ID (assigned by the Bluetooth SIG) followed by proprietary data. Apple (0x004C), Samsung (0x0075), Google (0x00E0), Microsoft (0x0006) use this field to implement their proximity pairing systems.

> **Personal note:** Understanding the structure of advertising packets is the key to understanding all BLE hacking with the Flipper. 90% of what the Flipper does in the Bluetooth domain boils down to crafting and transmitting advertising packets with specific payloads. If you understand this mechanism, you understand BLE Spam, Fast Pair, Swift Pair, and everything else.

---
