# Bluetooth Low Energy (BLE) - Overview

Modulo BLE 5.0 integrato nel MCU **STM32WB55RG** del Flipper Zero. Utilizzato per BLE Spam (advertising PDU spoofing), BLE HID (BadBT keyboard/mouse), scanner dispositivi, app companion e comunicazione seriale.

**Chip:** STM32WB55 (BLE 5.0) | **Portata:** 10-30m | **Bande:** 2.4 GHz ISM | **Canali ADV:** 37, 38, 39

---

## Contenuti

| # | File | Descrizione |
|---|------|-------------|
| 01 | [Fondamenti Tecnici](01-Fondamenti-Tecnici.md) | Stack BLE 5.0, advertising PDU, connection architecture, GATT, GAP, pairing |
| 02 | [Hardware e Limiti](02-Hardware-e-Limiti.md) | STM32WB55 BLE capabilities, potenza TX, portata reale, limiti del Flipper |
| 03 | [Protocolli e Funzionalità](03-Protocolli.md) | BLE HID, Serial CLI, App Companion, Remote Control, BLE Scanner |
| 04 | [Guida Operativa - BLE Spam](04-Guida-Operativa.md) | BLE Spam deep dive: Apple (AirPods, AirTag, Handoff), Samsung (Galaxy, SmartTag), Google Fast Pair, Windows Swift Pair, crafting PDU |
| 05 | [Scenari Reali](05-Scenari-Reali.md) | Scenari pentest: BLE spam in ambiente corporate, device enumeration, BLE HID injection, disruption assessment |
| 06 | [Attacchi e Difese](06-Attacchi-e-Difese.md) | BLE spam, MITM, eavesdropping, replay, downgrade - attacchi e contromisure |
| 07 | [Aspetti Legali](07-Aspetti-Legali.md) | Normativa italiana/EU per BLE testing |
| 08 | [Esperienza Personale](08-Esperienza-Personale.md) | Troubleshooting, note dal campo, limiti, risorse |

---

## Quick Reference - Funzionalità BLE

| Funzione | Descrizione | Uso Pentest |
|----------|-------------|-------------|
| BLE Spam | Advertising PDU spoofing (Apple/Samsung/Google/Windows) | Disruption, awareness testing |
| BLE HID (BadBT) | Tastiera/mouse Bluetooth wireless | Keystroke injection wireless |
| BLE Scanner | Scansione dispositivi BLE nelle vicinanze | Reconnaissance, device enumeration |
| App Companion | Controllo remoto del Flipper via smartphone | Gestione remota |
| Serial CLI | Console seriale via BLE | Debug, scripting |

> **Nota personale:** Il BLE Spam è lo strumento più visivamente impressionante del Flipper - genera notifiche su tutti gli iPhone/Samsung/Android nella stanza. In un pentest è utile per dimostrare quanto facilmente si possano generare notifiche false. BLE HID (BadBT) è più utile operativamente - è un BadUSB wireless che funziona fino a 10-15 metri.
