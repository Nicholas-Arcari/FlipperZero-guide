## BLE Spam - Deep Dive

BLE Spam is the most well-known BLE feature of the Flipper and deserves an in-depth analysis of the internal workings for each vendor.

### Apple BLE Spam

Apple uses a proprietary protocol based on Manufacturer Specific Data (Company ID: 0x004C) for proximity notifications. This system is used for:

- AirPods/AirPods Pro/AirPods Max (popup "Not Your AirPods")
- Apple TV setup
- AirTag detection
- Handoff/Continuity
- HomeKit
- "Hey Siri" routing

**Apple proximity packet structure:**

```
Advertising Data:
  AD Structure 1: Flags (0x01)
    Length: 0x02
    Type:   0x01
    Flags:  0x06 (LE General Discoverable + BR/EDR Not Supported)

  AD Structure 2: Manufacturer Specific Data (0xFF)
    Length: variable (typically 0x17 = 23 bytes)
    Type:   0xFF
    Company ID: 0x004C (Apple, Inc.)
    Proximity Type: 0x0715
    Payload: [device-specific data]
```

**Simulatable Apple device types:**

| Device | Popup Displayed | Effectiveness |
|---|---|---|
| AirPods Pro | "Not Your AirPods Pro" with image | High - very visible popup |
| AirPods 3rd Gen | "Not Your AirPods" with image | High |
| AirPods Max | "Not Your AirPods Max" with image | High - large image |
| Beats Fit Pro | "Not Your Beats Fit Pro" | Medium |
| Apple TV Setup | Setup assistant popup | Medium |
| AppleTV Keyboard | Keyboard request | Medium |
| AppleTV New User | New user setup | Medium |
| Beats Solo 3 | "Not Your Beats Solo 3" | Medium |
| PowerBeats Pro | "Not Your Powerbeats Pro" | Medium |

**How Apple handles proximity detection:**

1. The iOS device receives the advertising packet with Company ID 0x004C
2. The system verifies the message type (proximity pairing = 0x07)
3. The subtype identifies the specific device (0x15 for one type, 0x01 for another)
4. iOS displays the corresponding popup with the device image
5. The popup remains visible for a few seconds, then disappears

**Apple countermeasures:**

Starting with iOS 17.2, Apple introduced partial mitigations:

- Rate limiting on proximity popups (no more popups in rapid succession)
- Option to disable proximity notifications in Settings > Bluetooth
- Detection of anomalous patterns (too many different devices from the same MAC in a short time)

However, these mitigations do not completely eliminate the problem. With MAC address rotation and appropriate timing, BLE Spam continues to be effective even on recent iOS versions, albeit with reduced popup frequency.

**Disabling Apple popups:**

```
Settings > Bluetooth > Turn off Bluetooth
or
Settings > Notifications > Siri Suggestions > Turn off
```

Note: disabling Bluetooth from the Control Center does NOT fully disable BLE scanning. Apple keeps BLE active for Find My, Handoff, and AirDrop. Only disabling it completely from Settings stops reception.

### Samsung BLE Spam

Samsung uses the **Nearby Device** protocol with Company ID 0x0075 for rapid pairing of its accessories:

**Simulatable Samsung devices:**

| Device | Popup |
|---|---|
| Galaxy Buds Pro | "Galaxy Buds Pro found nearby" |
| Galaxy Buds Live | "Galaxy Buds Live found" |
| Galaxy Buds 2 | "Galaxy Buds2 found" |
| Galaxy Buds 2 Pro | "Galaxy Buds2 Pro found" |
| Galaxy Buds FE | "Galaxy Buds FE found" |
| Galaxy SmartTag | SmartTag popup |
| Galaxy Fit | Galaxy Fit popup |
| Galaxy Watch | Galaxy Watch popup |
| Galaxy Ring | Galaxy Ring popup |

**Samsung packet structure:**

```
Advertising Data:
  AD Structure 1: Flags
    0x02 0x01 0x06

  AD Structure 2: Manufacturer Specific Data
    Length: variable
    Type: 0xFF
    Company ID: 0x0075 (Samsung Electronics)
    Nearby Device Protocol: [device type byte] [model ID] [payload]
```

The Samsung Nearby protocol is less publicly documented compared to Apple, but the community's reverse engineering efforts have identified the key bytes for each device type.

**Effectiveness on Samsung devices:**

Samsung popups are very effective on Galaxy phones running Android with the Samsung SmartThings or Samsung Wearable app installed. The notification appears as a full-screen popup with the device image, very similar to the Apple experience.

On non-Samsung Android phones, the Samsung popup does not appear (since the Samsung Nearby protocol is handled by Samsung's proprietary framework, not stock Android).

### Google Fast Pair

Google Fast Pair is Google's proximity pairing protocol, supported by all Android devices with Google Play Services 11.7+. It uses Google's Company ID (0x00E0) with a standardized protocol:

**How Google Fast Pair works:**

1. The BLE device transmits an advertisement with the service UUID **0xFE2C** (Google Fast Pair Service)
2. The payload contains a 24-bit **Model ID** that identifies the device
3. Google Play Services on the Android phone receives the advertisement
4. The service queries a cloud database of registered Model IDs
5. If the Model ID matches a known device, it displays the popup with name and image

**Fast Pair packet structure:**

```
Advertising Data:
  AD Structure 1: Flags
    0x02 0x01 0x06

  AD Structure 2: Service Data (0x16)
    Length: 0x06
    Type: 0x16
    Service UUID: 0xFE2C (Google Fast Pair)
    Model ID: [3 bytes - device identifier]

  AD Structure 3 (optional): TX Power Level
    0x02 0x0A 0xF4
```

**Notable Model IDs:**

Model IDs are registered in the Google database. Some examples used by BLE Spam:

- Google Pixel Buds
- Google Pixel Buds Pro
- JBL various devices
- Sony WH-1000XM (various generations)
- Bose QuietComfort
- And many other Fast Pair certified devices

**Effectiveness:**

Fast Pair is the most universal among the spammable protocols because it works on ANY Android device with Google Play Services (not just Samsung or Pixel). The popup is a half-sheet notification displaying the device name and a "Connect" button.

**Google countermeasures:**

- Android 14+ introduced rate limiting on Fast Pair notifications
- Fast Pair can be disabled: Settings > Google > Devices & sharing > Devices > Turn off "Show notifications"
- Alternatively: completely disable Bluetooth

### Windows Swift Pair

Microsoft Swift Pair is the proximity pairing protocol for Windows 10/11, introduced with the Windows 10 April 2018 Update. It uses a different mechanism from the other vendors.

**How Swift Pair works:**

1. The BLE device transmits an advertisement with **Manufacturer Specific Data** and Microsoft Company ID (0x0006)
2. The payload contains a specific Swift Pair marker
3. The Windows BLE scanner detects the packet and recognizes the marker
4. The system displays a toast notification "New Bluetooth device found nearby"
5. The user can click to initiate pairing

**Swift Pair packet structure:**

```
Advertising Data:
  AD Structure 1: Flags
    0x02 0x01 0x06

  AD Structure 2: Manufacturer Specific Data
    Length: variable
    Type: 0xFF
    Company ID: 0x0006 (Microsoft)
    Beacon Type: 0x03 (Swift Pair scenario)
    Payload: [device info, RSSI threshold, display name]

  AD Structure 3: Complete Local Name
    Length: variable
    Type: 0x09
    Name: "Device Name"
```

**Effectiveness on Windows:**

Swift Pair popups appear as toast notifications in the bottom-right corner of Windows. They are less invasive than Apple popups (which take up half the screen) but still annoying in quantity.

Swift Pair is enabled by default on Windows 10/11 but can be disabled:

```
Settings > Bluetooth & devices > Devices
> Show notifications to connect using Swift Pair: OFF
```

Or via Group Policy:

```
Computer Configuration > Administrative Templates > 
Windows Components > Bluetooth > 
Allow Swift Pair Notifications: Disabled
```

### Packet Crafting - Technical Analysis

The Flipper's BLE Spam builds advertisement packets by directly manipulating the BLE APIs of the STM32WB stack:

**Execution flow:**

1. **Initialization** - The app configures the BLE stack through ST HAL APIs
2. **MAC generation** - Generates a random BLE address (type 0x01 = Random) for each burst
3. **Payload construction** - Assembles the advertising data with the appropriate AD Structures for the target vendor
4. **Advertising configuration** - Sets advertising parameters (interval, type, channel map)
5. **Transmission** - Starts advertising
6. **Rotation** - After a brief interval, stops advertising, changes MAC and payload, and restarts

**Typical BLE Spam advertising parameters:**

| Parameter | Value | Rationale |
|---|---|---|
| Adv Interval Min | 20 ms | Maximum transmission frequency |
| Adv Interval Max | 40 ms | Tight range for high frequency |
| Adv Type | ADV_NONCONN_IND (0x02) | Does not accept connections, broadcast only |
| Channel Map | 0x07 (all 3) | Transmits on channels 37, 38, 39 |
| Own Address Type | Random | Randomized MAC for each burst |

MAC address rotation is critical: without rotation, the target device would receive advertising from the same MAC and display only one popup. With rotation, each new MAC appears as a new device, generating multiple popups.

> **Personal note:** I analyzed the BLE Spam behavior with an nRF52840 dongle and Wireshark. The Flipper generates approximately 10-20 advertising packets per second per vendor, with MAC rotation every 2-3 seconds. In "All" mode (all vendors), it alternates between Apple, Samsung, Google, and Windows every few seconds, creating a continuous stream of popups on all devices in the room. It's chaotic but effective as a demo. In an environment of 20 people, at least 70% will receive at least one popup within the first 30 seconds.

---
