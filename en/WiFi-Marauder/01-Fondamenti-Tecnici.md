## 1. WiFi 802.11 Technical Fundamentals

Before using WiFi Marauder effectively, it is essential to understand how
the WiFi protocol works at a low level. Without this knowledge, you are
using tools blindly -- and a pentester who works blind is a risk to themselves
and to the client.

### 1.1 802.11 Frame Architecture

The IEEE 802.11 protocol defines three fundamental categories of frames that
travel over the radio interface:

**Management Frames (Type 0)**

Management frames are the core of WiFi operations and the primary target of
most wireless attacks. They are unencrypted (in the absence of Protected
Management Frames / 802.11w) and handle the entire connection lifecycle.

Structure of a management frame:

```
+------------------+------------------+------------------+
|  Frame Control   |  Duration/ID     |  Address 1 (DA)  |
|  (2 byte)        |  (2 byte)        |  (6 byte)        |
+------------------+------------------+------------------+
|  Address 2 (SA)  |  Address 3       |  Sequence Ctrl   |
|  (6 byte)        |  (BSSID, 6 byte) |  (2 byte)        |
+------------------+------------------+------------------+
|  Frame Body (variable)              |  FCS (4 byte)    |
+-------------------------------------+------------------+
```

The Frame Control field contains:
- Protocol Version (2 bit): always 0 for current 802.11
- Type (2 bit): 00 = Management, 01 = Control, 10 = Data
- Subtype (4 bit): identifies the specific frame type
- Flags: To DS, From DS, More Fragments, Retry, Power Management, More Data,
  Protected Frame, Order

Management frame subtypes most relevant to pentesting:

| Subtype | Name                | Function                                          |
|---------|---------------------|---------------------------------------------------|
| 0000    | Association Req     | Client requests to associate with an AP            |
| 0001    | Association Resp    | AP responds to the association request             |
| 0010    | Reassociation Req   | Client requests reassociation (roaming)            |
| 0011    | Reassociation Resp  | AP responds to the reassociation                   |
| 0100    | Probe Request       | Client searches for available networks             |
| 0101    | Probe Response      | AP responds with its own information               |
| 1000    | Beacon              | AP periodically announces its presence             |
| 1010    | Disassociation      | Termination of association                         |
| 1011    | Authentication      | Open System or Shared Key authentication           |
| 1100    | Deauthentication    | Forced termination of authentication               |
| 1101    | Action              | Frame for various actions (spectrum mgmt, etc.)    |

> Personal note: 90% of what Marauder does revolves around management frames.
> When I started using Marauder without understanding frame structure, the results
> were confusing and useless. Since I studied 802.11 frames, every scan and sniff
> output has taken on a precise meaning. I strongly recommend studying the
> IEEE 802.11-2020 specification (at least the chapters on MAC frame format) before
> touching any wireless tool.

**Control Frames (Type 1)**

Control frames manage access to the radio medium and reliable frame delivery.
They are shorter than management frames and do not contain a body.

Main subtypes:
- **RTS (Request to Send)**: channel reservation request to avoid
  collisions in environments with hidden nodes
- **CTS (Clear to Send)**: response to RTS, grants channel access
- **ACK (Acknowledgment)**: confirms reception of a unicast frame
- **Block ACK / Block ACK Request**: aggregated confirmation of multiple frames
- **PS-Poll**: used by clients in power save to request buffered frames
- **CF-End**: signals the end of the Contention-Free period

Control frames are important in the pentesting context because:
- A CTS flood attack can silence an entire channel (every device that receives
  a CTS respects the NAV -- Network Allocation Vector -- and remains silent)
- ACK frames can reveal the presence of devices even when they are not actively
  transmitting

**Data Frames (Type 2)**

Data frames carry the actual payload -- the user's application traffic.
In a WPA2 network the payload is encrypted with AES-CCMP (or TKIP in legacy systems).

Relevant subtypes:
- **Data**: standard data frame
- **QoS Data**: data frame with Quality of Service support (802.11e)
- **Null Function**: frame without payload, used to signal power management state
- **QoS Null**: same as above, with QoS header

The address structure in data frames changes based on the traffic direction:

```
To DS=0, From DS=0  ->  IBSS (ad-hoc)
    Addr1 = DA, Addr2 = SA, Addr3 = BSSID

To DS=1, From DS=0  ->  Client to AP
    Addr1 = BSSID, Addr2 = SA, Addr3 = DA

To DS=0, From DS=1  ->  AP to Client
    Addr1 = DA, Addr2 = BSSID, Addr3 = SA

To DS=1, From DS=1  ->  WDS (bridge between APs)
    Addr1 = RA, Addr2 = TA, Addr3 = DA, Addr4 = SA
```

### 1.2 Beacon Frames - The Heart of Discovery

Beacon frames are transmitted periodically by every AP (by default every ~102.4 ms,
i.e., approximately 10 times per second) and contain all the information necessary for
a client searching for networks.

Structure of a beacon frame body:

```
+------------------+------------------+------------------+
|  Timestamp       |  Beacon Interval |  Capability Info |
|  (8 byte)        |  (2 byte)        |  (2 byte)        |
+------------------+------------------+------------------+
|  Tagged Parameters (variable, Information Elements)    |
+--------------------------------------------------------+
```

Most relevant Information Elements (IE):
- **SSID (IE 0)**: network name (can be empty for hidden networks)
- **Supported Rates (IE 1)**: supported data rates
- **DS Parameter Set (IE 3)**: current channel
- **TIM (IE 5)**: Traffic Indication Map, indicates buffered frames for clients in PS
- **Country (IE 7)**: country regulations
- **RSN (IE 48)**: Robust Security Network, defines the cipher suite
  (WPA2-Personal, WPA2-Enterprise, WPA3-SAE, supported ciphers)
- **Vendor Specific (IE 221)**: proprietary extensions (WPA1, WPS, etc.)

The RSN IE (Robust Security Network) is particularly important for the pentester:

```
RSN Information Element:
+------------------+------------------+
|  Element ID (48) |  Length           |
+------------------+------------------+
|  Version (2)     |  Group Cipher    |
|                  |  Suite (4)       |
+------------------+------------------+
|  Pairwise Count  |  Pairwise Cipher |
|  (2)             |  Suite(s) (4*n)  |
+------------------+------------------+
|  AKM Count (2)   |  AKM Suite(s)    |
|                  |  (4*n)           |
+------------------+------------------+
|  RSN Capabilities (2)              |
+------------------------------------+
```

From the RSN IE you can determine:
- Whether the network uses CCMP (AES) or TKIP (vulnerable)
- Whether it supports 802.11w (PMF - Protected Management Frames)
- Whether it uses PSK (Personal) or 802.1X (Enterprise)
- Whether WPA3-SAE is supported/required

> Personal note: during an engagement, reading beacon frames allowed me to
> identify an old AP that still supported TKIP as a fallback. That became
> my entry point. Marauder's scan shows this information in a compact format,
> but knowing what it means makes the difference between a pentester and
> someone who just presses buttons.

### 1.3 Probe Request and Probe Response

The probe mechanism is the active way clients search for WiFi networks.

**Probe Request**: a client transmits a probe request in broadcast (or directed at a
specific SSID) to discover which APs are reachable.

There are two types:
1. **Directed Probe**: contains a specific SSID -- the client is looking for a known network.
   This reveals the networks the device has connected to in the past (privacy leak).
2. **Broadcast Probe (Wildcard)**: empty SSID -- the client asks all APs to
   respond.

**Probe Response**: the AP responds with the same information as a beacon frame,
but in unicast to the requesting client.

Implications for pentesting:
- Directed probe requests reveal the "WiFi history" of a device. If a phone
  transmits probes for "Hotel_Roma_WiFi", you know where the owner has been.
- This information can be used to create a targeted Evil Twin: simply create
  an AP with the SSID the client is looking for, and the device may connect
  automatically.
- Modern operating systems (iOS 14+, Android 10+, recent Windows 10) randomize
  the MAC address in probes to mitigate tracking, but not all devices do it
  correctly.

### 1.4 Authentication and Association

The WiFi connection process follows a precise sequence:

```
Client                                    AP
  |                                        |
  |  1. Probe Request (optional)           |
  |--------------------------------------->|
  |  2. Probe Response (optional)          |
  |<---------------------------------------|
  |                                        |
  |  3. Authentication Request             |
  |--------------------------------------->|
  |  4. Authentication Response            |
  |<---------------------------------------|
  |                                        |
  |  5. Association Request                |
  |--------------------------------------->|
  |  6. Association Response               |
  |<---------------------------------------|
  |                                        |
  |  --- 4-Way Handshake (WPA2) ---        |
  |                                        |
  |  7. EAPOL Message 1 (ANonce)           |
  |<---------------------------------------|
  |  8. EAPOL Message 2 (SNonce + MIC)     |
  |--------------------------------------->|
  |  9. EAPOL Message 3 (GTK + MIC)        |
  |<---------------------------------------|
  | 10. EAPOL Message 4 (ACK)              |
  |--------------------------------------->|
  |                                        |
  | === Encrypted traffic ===              |
```

In WPA2-Personal (PSK), the authentication at steps 3-4 is of the "Open System" type
(meaning it does not actually verify anything -- the real authentication occurs in the 4-way handshake).

### 1.5 The WPA2 4-Way Handshake

The 4-way handshake is the critical process that establishes session keys for
traffic encryption. It is also the primary target for offline WiFi password
cracking.

**Key derivation:**

```
PSK = PBKDF2-SHA1(Passphrase, SSID, 4096 iterations, 256 bit)
     |
     v
PMK (Pairwise Master Key) = PSK  (in WPA2-Personal, PMK == PSK)
     |
     v
PTK = PRF-X(PMK, "Pairwise key expansion",
            Min(AA,SA) || Max(AA,SA) || Min(ANonce,SNonce) || Max(ANonce,SNonce))
     |
     +-> KCK (Key Confirmation Key, 128 bit) -- used to compute the MIC
     +-> KEK (Key Encryption Key, 128 bit) -- used to encrypt the GTK
     +-> TK  (Temporal Key, 128 bit) -- used to encrypt data traffic
```

Where:
- AA = Authenticator Address (AP MAC)
- SA = Supplicant Address (client MAC)
- ANonce = random number generated by the AP
- SNonce = random number generated by the client

**The four EAPOL messages:**

1. **Message 1 (AP -> Client)**: the AP sends the ANonce in cleartext. At this point
   the client has everything needed to compute the PTK (it already knows the PMK
   derived from the password, its own SNonce which it generates locally, and both
   MAC addresses). The client computes the PTK.

2. **Message 2 (Client -> AP)**: the client sends its SNonce and a MIC
   (Message Integrity Code) computed with the KCK derived from the PTK. The AP now has
   everything to compute the PTK on its end and verifies the MIC: if it is correct, the client
   knows the correct password.

3. **Message 3 (AP -> Client)**: the AP sends the GTK (Group Temporal Key, for
   multicast/broadcast traffic) encrypted with the KEK, plus a MIC. The AP installs
   the PTK.

4. **Message 4 (Client -> AP)**: the client confirms reception. The client
   installs the PTK and the GTK. The encrypted connection is active.

**What is needed for offline cracking:**

To attempt an offline brute force / dictionary attack you need:
- ANonce (from message 1)
- SNonce (from message 2)
- AP MAC (AA)
- Client MAC (SA)
- MIC from message 2 (or 3)

With this data you can derive the PTK for each candidate password and verify
whether the computed MIC matches the captured one. If it matches, the password
has been found.

> Personal note: many people think that capturing the handshake "cracks" the network
> in real time. That is not the case. The capture is only the first step -- the crack happens
> offline, on your own hardware, and can take anywhere from seconds (weak passwords +
> dictionary) to months/years (complex passwords + brute force). With a modern GPU
> and hashcat you can test approximately 500,000+ PMK/s for WPA2, but a password of 12+
> random characters remains practically unbreakable.

### 1.6 PMKID - The Superior Attack

Discovered by Jens "atom" Steube (creator of hashcat) in 2018, the PMKID attack
represents a significant evolution over the traditional 4-way handshake capture.

**How it works:**

In the RSN IE of beacon frames, some APs support PMK caching (802.11r/PMK-ID).
When a client associates, the AP can include a PMKID in the first EAPOL message:

```
PMKID = HMAC-SHA1-128(PMK, "PMK Name" || MAC_AP || MAC_Client)
```

The PMKID is a hash derived directly from the PMK (which in WPA2-Personal is the PSK,
which in turn is derived from the password).

**Why it is superior to handshake capture:**

1. **Does not require a connected client**: it is sufficient that the AP supports PMK caching.
   You send an association request and wait for message 1 with the PMKID.
2. **Does not require deauthentication**: no client is disconnected, the attack
   is completely passive from the perspective of network users.
3. **Faster**: you obtain the PMKID in a few seconds, without having to wait
   for a client to reconnect.
4. **Less detectable**: no deauth frames, no obvious anomalies in the
   traffic.

**Limitations:**
- Not all APs include the PMKID in message 1
- Some modern APs disable PMK caching by default
- WPA3-SAE is not vulnerable to this attack (it uses SAE, which does not expose the PMKID)

**Format for hashcat:**

```
hashcat -m 22000 hash.hc22000 wordlist.txt
```

The .hc22000 format is the unified format of hashcat 6.0+ that supports both
handshake and PMKID in the same structure.

> Personal note: PMKID is the first attack I always try on a target WPA2 network.
> If the AP supports it, I have the material for cracking in 10 seconds without
> disturbing anyone. Only if PMKID fails do I move on to handshake capture
> with deauth. It is a matter of OPSEC: the less noise you make, the better.

---
