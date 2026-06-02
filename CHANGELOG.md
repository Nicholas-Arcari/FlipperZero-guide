# Changelog

Storico delle modifiche principali al repository.

---

## v4.0 - 2026-04-07 - Arsenale, automazione e professionalizzazione

### Aggiunte
- `INDEX.md` - indice globale navigabile di tutti i file, organizzato per modulo e per tipo
- `GLOSSARY.md` - glossario tecnico con 80+ termini (OOK, SAK, Crypto1, AMSI, LOLBin, etc.)
- `CONTRIBUTING.md` - guida per contribuire al progetto
- `MITRE-ATTACK.md` - mapping completo tecniche Flipper → MITRE ATT&CK framework con kill chain
- `REPORT-TEMPLATES.md` - template report per 6 tipi di finding (Sub-GHz, NFC, RFID, BadUSB, WiFi, IR)
- `WORKFLOW-DIAGRAMS.md` - 6 diagrammi Mermaid (kill chain, NFC pipeline, Sub-GHz flow, BadUSB chain, WiFi Marauder, RFID decision)
- `README_EN.md` - traduzione inglese del README principale
- `scripts/setup-sd.sh` - script bash per setup SD card (struttura + download database IR/NFC)
- `scripts/validate-files.py` - validatore sintassi file .sub/.nfc/.rfid/.ibtn/.ir + link check
- `.github/workflows/validate.yml` - GitHub Actions CI per validazione struttura e file
- `payloads/` - arsenale BadUSB con 25+ payload organizzati per OS e categoria:
  - Windows: recon (system, network, AD, security enum), reverse shell (PS, encrypted, LOLBin mshta/certutil), credential harvest (WiFi, browser, SAM, mimikatz), persistence (registry, schtask, WMI), evasion (Defender, AMSI, ETW), privilege escalation (UAC fodhelper, admin user), exfiltration (webhook, clipboard)
  - macOS: reverse shell, recon, persistence LaunchAgent
  - Linux: reverse shell, SSH key exfil, persistence cron/bashrc
  - Multi-OS: demo awareness (rickroll, wallpaper)

### Modifiche
- Root `README.md` aggiornato con link a tutte le nuove risorse
- Eliminati binari firmware RogueMaster obsoleti (~1.1 GB)

---

## v3.0 - 2026-04-07 - Miglioramenti strutturali

### Aggiunte
- `CHEATSHEET.md` - riferimento rapido stampabile per il campo
- `LAB-SETUP.md` - guida alla creazione di un laboratorio di test domestico
- `CHANGELOG.md` - questo file
- Cartelle `examples/` con file di esempio per ogni modulo
- Cross-reference tra moduli negli scenari multi-vettore
- Esempi file `.ir` e link al database IR ufficiale
- GPIO/Altre componenti splittato in 7 sotto-file per categoria

### Modifiche
- Root `README.md` aggiornato per riflettere la nuova struttura split
- `USB/Altre componenti/README.md` espanso con scenari di sicurezza
- `RogueMaster/` - binari firmware sostituiti con link alle release ufficiali

---

## v2.0 - 2026-04-05 - Ingegnerizzazione in sotto-file

### Modifiche strutturali
Ogni modulo principale è stato splittato in sotto-file tematici:

```
Modulo/
├── README.md                    ← Indice con link
├── 01-Fondamenti-Tecnici.md     ← Basi tecniche
├── 02-Hardware-e-Limiti.md      ← Specifiche e limiti reali
├── 03-Protocolli.md             ← Deep dive protocolli
├── 04-Guida-Operativa.md        ← Tool-by-tool step-by-step
├── 05-Scenari-Reali.md          ← Scenari di pentest (ESPANSI)
├── 06-Attacchi-e-Difese.md      ← Vettori di attacco + contromisure
├── 07-Aspetti-Legali.md         ← Normativa italiana/EU
└── 08-Esperienza-Personale.md   ← Note dal campo + troubleshooting
```

### Moduli splittati (8 file ciascuno)
- Sub-GHz, NFC, RFID, iButton, Infrared, Bluetooth, WiFi-Marauder, USB/BadUSB

### Moduli splittati (6 file ciascuno)
- GPIO/ESP32, GPIO/NRF24, GPIO/Debug

### Scenari reali espansi
- Sub-GHz: da 3 a 8 scenari
- NFC: da 3 a 7 scenari
- RFID: da 4 a 7 scenari

---

## v1.0 - 2026-04-04 - Espansione contenuti a basso livello

### Modifiche
- Tutti i README.md riscritti da overview ad alto livello a guide operative a basso livello
- Contenuto totale: da ~3,000 righe a ~17,000+ righe
- Prospettiva: senior cybersecurity analyst + senior penetration tester
- Aggiunta analisi a livello di bit per ogni protocollo
- Aggiunta procedure step-by-step per ogni tool
- Aggiunta scenari di penetration testing reali per ogni modulo
- Aggiunta sezioni aspetti legali (Italia/EU) per ogni modulo
- Aggiunta troubleshooting dettagliato per ogni modulo
- Preservate tutte le note di esperienza personale

### Nuovi moduli
- `Bluetooth/` - sezione BLE creata da zero (1247 righe)
- `WiFi-Marauder/` - rinominato da `Wifi-Maruder/`, riscritto (2300 righe)
- `GPIO/ESP32/` - rinominato da `GPIO/EPS32/`, riscritto (1854 righe)
- `GPIO/NRF24/` - riscritto (1397 righe)
- `GPIO/Debug/` - riscritto (1410 righe)

### Fix strutturali
- Corretto typo: `EPS32` → `ESP32`
- Corretto typo: `Wifi-Maruder` → `WiFi-Marauder`
- Root `README.md` riscritto come guida completa (236 righe)

---

## v0.1 - Pre-refactoring

Versione originale con overview ad alto livello (5-15 righe per tool), link a video YouTube, file binari firmware nella repo.
