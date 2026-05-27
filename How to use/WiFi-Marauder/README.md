# WiFi Marauder - Overview

Modulo WiFi basato su **ESP32** con firmware **Marauder** per penetration testing wireless 802.11. Permette scansione reti, deauthentication, evil portal, cattura PMKID/handshake, beacon spam, probe flood e wardriving.

**Hardware:** ESP32 WiFi Devboard | **Frequenza:** 2.4 GHz | **Standard:** 802.11 b/g/n | **Firmware:** ESP32 Marauder

---

## Video di Riferimento

Flipper Zero - Tutorial Italiano - 15 - WIFI MARAUDER ( https://www.youtube.com/watch?v=z3ft9ND-3iA )

Flipper Zero - Tutorial Italiano - 17 - WIFI MARAUDER ( https://www.youtube.com/watch?v=CP0cmj3byJE )

---

## Contenuti

| # | File | Descrizione |
|---|------|-------------|
| 01 | [Fondamenti Tecnici](01-Fondamenti-Tecnici.md) | 802.11 frame architecture, Beacon, Probe, Authentication, Association, 4-Way Handshake WPA2, PMKID |
| 02 | [Hardware e Flash](02-Hardware-e-Limiti.md) | ESP32 devboard specs, procedura flash Marauder (Web/CLI/manuale), configurazione Flipper |
| 03 | [Protocolli 802.11](03-Protocolli.md) | Deep dive architettura frame, management/control/data, WPA2 key derivation, PMKID math |
| 04 | [Guida Operativa](04-Guida-Operativa.md) | Tool-by-tool: Scan, Sniff (PMKID/Handshake/Raw), Deauth, Beacon Spam, Probe Flood, Evil Portal, Wardriving |
| 05 | [Scenari Reali](05-Scenari-Reali.md) | Scenari pentest: corporate WiFi assessment, evil twin, WPA2 handshake capture, guest network, rogue AP detection |
| 06 | [Attacchi e Difese](06-Attacchi-e-Difese.md) | Deauth, Evil Portal, PMKID, Handshake, Beacon Spam, Wardriving - attacchi e contromisure (802.11w, WPA3, WIDS) |
| 07 | [Aspetti Legali](07-Aspetti-Legali.md) | Normativa italiana/EU per WiFi testing, Art. 617-quater, regole operative |
| 08 | [Esperienza Personale](08-Esperienza-Personale.md) | Troubleshooting flash/connessione, note dal campo, errori da evitare, risorse |

---

## Quick Reference - Comandi Principali Marauder

| Comando | Funzione | Uso Pentest |
|---------|----------|-------------|
| `scanap` | Scansione Access Point | Reconnaissance |
| `scansta` | Scansione stazioni (client) | Client enumeration |
| `sniffpmkid` | Cattura PMKID | WPA2 password recovery |
| `sniffraw` | Cattura handshake 4-way | WPA2 password recovery |
| `deauth` | Deauthentication frame | DoS / forza riconnessione |
| `evilportal` | Captive portal falso | Credential harvesting |
| `beaconspam` | SSID falsi massivi | Confusione / copertura |
| `probeflood` | Probe Request flood | DoS su AP |
| `wardrive` | Scansione + GPS | Mappatura WiFi |

> **Nota personale:** Il WiFi Marauder trasforma il Flipper in un tool di WiFi pentest portatile. Non sostituisce un laptop con aircrack-ng, ma per ricognizione rapida, deauth testing e evil portal è eccellente. La cattura PMKID funziona sorprendentemente bene - in un engagement ho recuperato 3 PMKID in meno di 5 minuti e crackato la password WPA2 con hashcat in 2 ore.
