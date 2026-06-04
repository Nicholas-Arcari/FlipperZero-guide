## Flipper Zero BLE Features

The Flipper Zero offers four main categories of BLE features:

### 1. BLE Spam

The most well-known and viral BLE feature of the Flipper. It sends crafted advertisement packets that trigger pairing popups on nearby Apple, Samsung, Google, and Windows devices.

**How it works at a technical level:**

BLE Spam exploits the proximity pairing mechanisms implemented by vendors:

1. **The Flipper generates advertising packets** with Manufacturer Specific Data (AD Type 0xFF) containing the target vendor's Company ID and payloads that simulate a specific device
2. **The advertising is repeated** rapidly (minimum interval ~20ms) on the three advertising channels
3. **Nearby devices** receive the packet and their OS recognizes the Company ID
4. **The target operating system** interprets the payload as a legitimate device nearby and displays the pairing popup to the user
5. **The user sees** the "AirPods Pro Nearby" or "Galaxy Buds Found" popup on their screen

The Flipper continuously changes the source MAC address (random address) and the payload to generate multiple different popups in rapid succession. In "all" mode it spams all vendors simultaneously.

**Availability:**

BLE Spam is available in custom firmwares (Xtreme, Momentum, RogueMaster, Unleashed) as a dedicated application. The official Flipper firmware does NOT include BLE Spam.

**Typical menu:**

```
BLE Spam
  |
  +-- Apple
  +-- Samsung
  +-- Google (Fast Pair)
  +-- Windows (Swift Pair)
  +-- All (all vendors)
  +-- Stop
```

> **Personal note:** BLE Spam is the feature that made the Flipper go viral on TikTok and social media. In professional contexts, I use it exclusively for BLE security awareness demos - never in unauthorized environments. The effect is immediate and visually impressive: a room full of popups is the most effective way to demonstrate to a corporate board that BLE is not "secure by default."

### 2. BLE Companion App

The Flipper Zero connects to the smartphone via BLE for remote control and device management. This is the main "legitimate" BLE feature.

**How it works:**

- The Flipper acts as a **BLE peripheral** (GATT server)
- The smartphone with the Flipper app (iOS/Android) acts as a **central** (GATT client)
- The connection uses the **Flipper RPC Protocol** over a custom GATT service (Nordic UART Service - NUS)
- NUS service UUID: `6E400001-B5A3-F393-E0A9-E50E24DCCA9E`
- TX characteristic UUID: `6E400003-B5A3-F393-E0A9-E50E24DCCA9E`
- RX characteristic UUID: `6E400002-B5A3-F393-E0A9-E50E24DCCA9E`

**What you can do via BLE companion:**

- Update firmware OTA (Over The Air)
- Manage the Flipper file system (upload/download files)
- Execute remote commands (launch apps, control GPIO)
- Monitor device status (battery, storage)
- Send .sub, .rfid, .nfc, .ir files to the Flipper
- Control Sub-GHz, IR, GPIO from smartphone

**Companion connection security:**

- Pairing with numeric key (6 digits) displayed on the Flipper screen
- AES-CCM encryption after pairing
- Bonding for automatic reconnections
- The Flipper shows a confirmation popup for each new connection

**Flipper RPC Protocol:**

The communication protocol is based on Protocol Buffers (protobuf) serialized and transmitted over NUS. Messages include:

- `StorageReadRequest` / `StorageReadResponse` - File reading
- `StorageWriteRequest` - File writing
- `AppStartRequest` - Application launch
- `GpioSetPinMode` / `GpioWritePin` - GPIO control
- `SystemPingRequest` / `SystemPingResponse` - Keep-alive

The communication is bidirectional and asynchronous. Effective throughput over BLE with NUS is typically 5-15 KB/s, which explains why transferring large files via BLE is slow (a 1 MB firmware update takes several minutes).

### 3. BLE HID (BadBT)

The Flipper can present itself as an **HID (Human Interface Device)** over BLE - essentially, a wireless Bluetooth keyboard or mouse. This feature is known as **BadBT** (analogous to BadUSB, but via Bluetooth).

**How it works:**

1. The Flipper exposes the **HID over GATT** service (UUID: 0x1812)
2. The target device (PC, smartphone, tablet) sees the Flipper as a Bluetooth keyboard/mouse
3. The target user accepts the pairing (or pairing occurs automatically if configured)
4. The Flipper sends arbitrary keystrokes and mouse movements
5. The target executes the received commands as if they came from a physical keyboard

**BLE HID Profile:**

The HID service over GATT exposes these characteristics:

| Characteristic | UUID | Function |
|---|---|---|
| HID Information | 0x2A4A | HID version, country code |
| Report Map | 0x2A4B | Descriptor describing the reports (keyboard/mouse layout) |
| Report | 0x2A4D | The actual reports (keystroke, mouse movement) |
| Protocol Mode | 0x2A4E | Boot Protocol or Report Protocol |
| Boot Keyboard Input Report | 0x2A22 | Keyboard report in boot mode |
| Boot Keyboard Output Report | 0x2A32 | LED status (Caps Lock, etc.) |

**Key differences BadBT vs BadUSB:**

| Aspect | BadUSB (USB) | BadBT (Bluetooth) |
|---|---|---|
| Connection | Physical (USB cable) | Wireless (BLE, up to 10-15m) |
| Requires physical access | Yes, at the moment of insertion | No, after initial pairing |
| Pairing required | No (plug-and-play) | Yes (requires user acceptance) |
| Keystroke speed | Very high (~100+ char/sec) | Slower (~30-50 char/sec) |
| Visibility | USB cable visible | No cable visible |
| Persistence | Only when inserted | Can reconnect after bonding |
| Detection | Device Manager shows HID | Bluetooth settings shows device |
| Range | 0m (physical contact) | 5-15m typical |

**BadBT Scripts:**

The Flipper uses the same DuckyScript script format used for BadUSB, with extensions for BLE:

```
REM BadBT Example - Open terminal on macOS
DELAY 2000
GUI SPACE
DELAY 500
STRING Terminal
DELAY 500
ENTER
DELAY 1000
STRING echo "BadBT payload executed"
ENTER
```

**BadBT attack process:**

1. Load the DuckyScript script onto the Flipper (SD card, folder `/badbt/`)
2. Launch the BadBT app on the Flipper
3. The Flipper starts advertising as a BLE keyboard
4. The target must accept the pairing
5. Once connected, the Flipper executes the script

The critical point is **pairing**: unlike BadUSB (which is plug-and-play), BadBT requires the target user to accept the Bluetooth connection. This significantly limits attack scenarios compared to BadUSB.

However, in scenarios where the target has already accepted pairing (social engineering, prior access, unattended device with auto-accept), BadBT is powerful because it can operate at a distance without physical contact.

> **Personal note:** BadBT has an underestimated tactical advantage: reconnection after bonding. If you manage to complete the initial pairing (perhaps during an "innocent" demo), you can reconnect at a later time without the target having to accept again. In a physical pentest, I used this technique: pairing during a "test" presentation, then payload execution the next day from the adjacent room. The user saw nothing. Obviously, everything was authorized and within the engagement scope.

### 4. BLE Scanner

The Flipper can scan the environment for nearby BLE devices, displaying detailed information about each device found.

**What the scanner detects:**

- **MAC Address** - Device address (often randomized)
- **RSSI** - Received Signal Strength Indicator (signal power, in dBm)
- **Device name** - If present in the advertising (Local Name)
- **Exposed services** - UUIDs of advertised GATT services
- **Manufacturer Specific Data** - Vendor proprietary data
- **TX Power Level** - Power declared by the device
- **Advertising Type** - Connectable, scannable, non-connectable
- **Flags** - LE General Discoverable, BR/EDR Not Supported, etc.

**RSSI interpretation:**

| RSSI (dBm) | Approximate Distance | Quality |
|---|---|---|
| -30 to -50 | < 1 meter | Excellent, device very close |
| -50 to -65 | 1-3 meters | Good, same room |
| -65 to -75 | 3-10 meters | Fair, could be in adjacent room |
| -75 to -85 | 10-20 meters | Weak, at the edge of range |
| -85 to -100 | 20+ meters | Very weak, unstable connection |

RSSI is useful for estimating proximity but is NOT a precise distance indicator. Walls, antenna orientation, interference, and reflections make the estimate very approximate.

**Flipper scanner limitations:**

The Flipper's scanner is a **passive/active scanner** that operates on the three advertising channels. It is NOT a complete sniffer:

- It only sees advertising packets, not data traffic on active connections
- It cannot decode encrypted connections
- It cannot intercept the pairing of other devices
- It cannot perform MITM on existing connections
- It only sees advertising channels (37, 38, 39), not the 37 data channels

For complete BLE sniffing, dedicated hardware is needed (Ubertooth, nRF52840 dongle, HackRF with gr-bluetooth).

---
