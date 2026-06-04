## Troubleshooting and Limitations

### Common Problems and Solutions

#### The captured signal does not work on the target device

**Probable cause 1 - Incomplete capture:**
- The RAW signal was truncated (common with long AC protocols)
- Solution: get closer to the source remote, make sure the capture shows the entire frame

**Probable cause 2 - Wrong protocol:**
- The Flipper decoded the signal with the wrong protocol
- Solution: force a RAW capture and try replaying that instead

**Probable cause 3 - Excessive distance:**
- You are too far from the target device
- Solution: get within 2-3 meters, aim directly at the IR receiver

**Probable cause 4 - Wrong angle:**
- You are not aiming toward the device's IR receiver
- Solution: identify where the receiver is located (usually front-facing, often indicated by a dark window) and aim directly at it

**Probable cause 5 - Ambient light:**
- Strong sunlight or fluorescent lighting is interfering with the receiver
- Solution: close the curtains, get closer, try at different times

#### The Flipper does not recognize the protocol (everything is RAW)

**Probable cause 1 - Unsupported protocol:**
- The device uses a proprietary protocol not in the Flipper's database
- Solution: use RAW capture, it will still work for playback

**Probable cause 2 - Non-standard carrier frequency:**
- The device uses 56 kHz or another frequency that is not optimal for the TSOP75338
- Solution: get very close (5-10 cm) to compensate for the reduced sensitivity

**Probable cause 3 - Weak signal:**
- The source remote's batteries are dead
- Solution: replace the batteries or get very close

#### Specific problems with air conditioners

**Symptom:** The captured command has no effect on the AC.

**Explanation:** AC protocols send the complete state. If you captured "set 24 degrees in cool mode" and the air conditioner is already at 24 degrees in cool mode, it might not react visibly. Alternatively, the captured frame includes a state that does not match the air conditioner's current state and is rejected.

**Solutions:**
- Capture the **Power On/Off** signal - it is the least state-dependent command
- Capture **each variation** separately (each temperature, each mode)
- Use the Flipper's dedicated AC remotes (Hitachi, Midea, Mitsubishi) which correctly manage state

#### The device responds only sometimes

**Probable cause 1 - At the range limit:**
- You are at the edge of the TX range - the signal reaches the receiver with borderline power
- Solution: get 1-2 meters closer

**Probable cause 2 - Bounce interference:**
- In environments with many reflective surfaces, the direct signal and bounces can arrive out of phase, creating interference
- Solution: change position, try a different angle

**Probable cause 3 - Imprecise RAW timing:**
- The RAW capture has minor timing inaccuracies that sometimes cause decoding errors
- Solution: capture the signal multiple times and use the capture with the cleanest timing

### Structural Limitations of the IR Module

| Limitation | Detail | Workaround |
|---|---|---|
| **TX range** | 3-8 meters | Get closer to the target |
| **Emission angle** | ~34 degrees | Aim directly |
| **Single LED** | No redundancy | None (hardware limitation) |
| **Carrier frequency** | Optimized for 38 kHz | RAW for different frequencies |
| **Ambient light** | Reduces range | Operate indoors/in shade |
| **No native external LED** | Not expandable via GPIO | Unofficial hardware mods |
| **AC protocols** | Complex capture | Dedicated remotes per brand |
| **Line-of-sight** | Requires optical path | Use wall bounces |

---

## Personal Experience

### The Flipper IR in Daily Life

The IR module is probably the Flipper Zero function I use **most frequently in daily life** - paradoxically more than Sub-GHz or NFC which are "more interesting" from a pentesting perspective.

Reason: the Flipper has become my universal remote. I always carry the Flipper with me, and having a remote for any TV, projector, or AC within a few meters is enormously practical.

### Field Experiences

> **Personal note:** During a physical pentest for a medium-sized company in Milan, I used the IR module to turn off 4 displays in the lobby during the internal reconnaissance phase. The incident ended up in the report as a medium-severity finding: "Corporate communication devices (information displays, digital signage) controllable by unauthorized personnel without any credentials or privileged access." The client then covered the IR receivers with opaque tape - the simplest and most effective countermeasure.

> **Personal note:** Air conditioners are the most frustrating IR devices to deal with in pentesting. Every brand has its own protocol, every model has its own variants. During an engagement, I spent 15 minutes trying to control a Daikin AC with RAW capture before discovering that the specific model used a protocol variant with a different header. Lesson learned: for air conditioners, if the built-in database does not work, capture directly from the original remote. Do not waste time guessing the protocol.

> **Personal note:** The Flipper's TX range is the number one operational constraint. In a large conference room (10+ meters), you cannot reach the display from the back of the room. You have to get closer. In environments where discretion is critical, this can be a problem. My approach: I get closer to the display with the excuse of "getting a better look at the screen" or "grabbing a coffee" from the nearby vending machine - any pretext to reduce the distance to 3-4 meters.

> **Personal note:** A trick few people know: your phone's camera can see infrared. If you want to verify that the Flipper is actually transmitting (or if you want to locate a remote's IR LED), look at it through your smartphone camera. You will see a violet flash every time the IR LED activates. Also useful for verifying that a remote's batteries are not dead before capturing signals.

> **Personal note:** IR Transfer between two Flipper devices is a trick I use in specific scenarios: when I need to transfer a captured IR signal to a colleague during an engagement and I do not want to use Bluetooth or WiFi (to avoid generating detectable wireless traffic). It is slow, but it is completely passive from an RF standpoint.

### Final Considerations

The Flipper Zero's IR module is an extraordinarily simple yet effective tool. It does not have the technical complexity of NFC or the depth of Sub-GHz, but the complete absence of encryption in IR protocols makes every IR device an easy target.

In physical pentesting, IR primarily serves as:
- **Demonstration tool** - showing the client that devices in the environment are controllable by anyone
- **Support tool** - creating distractions, manipulating the physical environment to facilitate other operations
- **Reconnaissance tool** - analyzing AV systems and environmental controls to understand the infrastructure

The main limitation remains the TX range and the line-of-sight requirement. But in indoor environments, with reflective walls and short distances, the Flipper Zero is simply the "ultimate universal remote" - and in the hands of a pentester, this is an operational weapon that is anything but negligible.
