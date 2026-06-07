# Flipper Zero + RogueMaster

## What is RogueMaster

RogueMaster is a "custom" firmware for Flipper Zero, a fork of the official firmware (and other community-based firmware) that adds plugins, games, extra features, and customizations.

Its purpose is to offer an "all-in-one" firmware, with plugins and features from various community projects, without having to manually compile from scratch.

---

## Download Firmware

**IMPORTANT:** ALWAYS download the latest version from the official release page. Firmware included in this repository is obsolete.

| Firmware | Link | Notes |
|----------|------|-------|
| **RogueMaster** | [GitHub Releases](https://github.com/RogueMaster/flipperzero-firmware-wPlugins/releases) | Main recommended firmware |
| **Momentum** | [GitHub Releases](https://github.com/Next-Flip/Momentum-Firmware/releases) | Stable alternative |
| **Unleashed** | [GitHub Releases](https://github.com/DarkFlippers/unleashed-firmware/releases) | Popular alternative |
| **Official Firmware** | [GitHub Releases](https://github.com/flipperdevices/flipperzero-firmware/releases) | Stock, limited for pentest |

> **Note:** The `Windows/` and `Linux & MacOS/` folders in this repository contain an old firmware version (RM1112-0137-0.420.0) and can be removed to save ~1.1 GB of space. Always download the latest version from the link above.

---

## Why Use Custom Firmware

### Advantages over official firmware

- **Unlocked Sub-GHz frequencies:** transmission on bands restricted by official firmware
- **Additional protocols:** rolling code tools, extra RFID protocols, additional decoders
- **Third-party apps:** hundreds of pre-installed applications
- **Rolling Flaws:** rolling code vulnerability analysis (not present in official firmware)
- **Extended Sub-GHz:** bruteforcer, playlist, scheduler, advanced tools
- **Extra NFC/RFID:** advanced fuzzer, additional protocols, Magic Card Gen4 support
- **BLE Spam:** not available in official firmware
- **UI customization:** themes, animations, custom dolphin

### Which One to Choose

| Firmware | Pros | Cons | Recommended For |
|----------|------|------|----------------|
| **RogueMaster** | Most apps/plugins, frequent updates | Heavy, sometimes unstable | Those who want maximum features |
| **Momentum** | Stable, well-organized, modern UI | Fewer plugins than RM | Those who want stability + features |
| **Unleashed** | Lightweight, stable, active community | Fewer pre-installed apps | Those who prefer to install only what they need |
| **Official** | Most stable, Flipper support | Few features for pentest | Beginners, non-security use |

> **Personal note:** I use RogueMaster as my main firmware for work. Momentum is my second choice for when RM has bugs. The official firmware makes no sense for a pentester -- too many limitations. Flashing is reversible and does not void the hardware warranty.

---

## How to Install

### Method 1 - Web Installer (Simplest)

1. Go to the release page of the chosen firmware
2. Look for the "Web Installer" link (if available)
3. Connect the Flipper via USB
4. Follow the on-screen instructions

### Method 2 - qFlipper

1. Download and install [qFlipper](https://flipperzero.one/update) on your PC
2. Download the `.dfu` file from the release page
3. Connect the Flipper via USB
4. In qFlipper: "Install from file" → select the `.dfu`
5. Wait for the flash (~2 minutes)

### Method 3 - SD Card

1. Download the complete archive from the release page
2. Extract the contents to the `/update/` folder on the microSD
3. On the Flipper: Settings → Storage → Update
4. Select the package and confirm
5. The Flipper reboots with the new firmware

### Video Tutorial

- Flipper Zero - RogueMaster Installation Tutorial ( https://www.youtube.com/watch?v=0olHgqScuCQ )

---

## Post-Installation

### Verify Functionality

1. Check the version: Settings → About → Firmware Version
2. Verify that extra apps are present in the menu
3. Test Sub-GHz: unlocked frequencies must be available
4. Test NFC/RFID: verify that extra protocols are present
5. Insert the microSD with the necessary assets

### Recommended SD Card Structure

```
/ext/
├── subghz/assets/     ← Frequency and protocol database
├── nfc/assets/        ← MIFARE key dictionaries
├── infrared/assets/   ← Universal IR database
├── badusb/            ← DuckyScript scripts
├── apps/              ← Additional applications
└── update/            ← Firmware packages
```

---

## Legal Notes / Disclaimer

- RogueMaster is open-source / publicly available on GitHub ( https://github.com/RogueMaster )
- The original firmware and the "Flipper Zero" trademark are property of Flipper Devices Inc.
- RogueMaster is **not affiliated** with nor "official"
- Using custom firmware is at your own risk: it may void warranties, cause unexpected behavior, or lose official support
- **Owning and using the Flipper Zero with custom firmware is legal in Italy and in the EU.** Improper use of its features is not.

## License

- RogueMaster firmware: distributed under [GNU GPLv3](https://www.gnu.org/licenses/gpl-3.0.html)
- Original repository content (guides, tutorials, scripts): released under [MIT License](https://opensource.org/licenses/MIT)
