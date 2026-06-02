# Report Templates - Template per Finding di Engagement

Template pronti per documentare i finding durante un penetration test fisico con Flipper Zero. Copia-incolla e compila.

---

## Template Generico - Finding

```markdown
## [SEVERITY] Finding Title

**ID:** FZ-[MODULE]-[NNN]
**Severity:** Critical / High / Medium / Low / Informational
**CVSS 3.1:** [score] ([vector])
**MITRE ATT&CK:** [Tactic] ([TAXXXX]) / [Technique] ([TXXXX])
**Status:** Open / Remediated / Accepted Risk

### Descrizione
[Descrizione tecnica della vulnerabilità trovata]

### Ambiente
- **Target:** [Tipo di dispositivo/sistema testato]
- **Location:** [Dove si trova fisicamente]
- **Protocollo:** [NFC/RFID/Sub-GHz/WiFi/etc.]
- **Tool:** Flipper Zero + [modulo specifico]

### Procedura di Riproduzione
1. [Step 1]
2. [Step 2]
3. [Step n]

### Evidenza
- File catturato: `[filename.ext]`
- Screenshot/foto: [riferimento]
- Hash evidenza: `sha256: [hash]`

### Impatto
[Cosa può fare un attaccante sfruttando questa vulnerabilità]

### Raccomandazione
| Priorità | Azione | Costo Stimato | Tempo |
|-----------|--------|---------------|-------|
| Immediata | [Quick fix] | Basso | 1-2 giorni |
| Breve termine | [Mitigazione] | Medio | 1-2 settimane |
| Lungo termine | [Soluzione definitiva] | Alto | 1-3 mesi |

### Riferimenti
- [CVE/Advisory se applicabile]
- [Standard di riferimento]
```

---

## Template - Sub-GHz: Replay Attack

```markdown
## [HIGH] Cancello/Barriera Vulnerabile a Replay Attack Sub-GHz

**ID:** FZ-SUBGHZ-001
**Severity:** High
**CVSS 3.1:** 7.5 (AV:P/AC:L/PR:N/UI:N/S:C/C:N/I:H/A:L)
**MITRE ATT&CK:** Initial Access (TA0001) / Hardware Additions (T1200)

### Descrizione
Il sistema di apertura [cancello/barriera/portone] utilizza un protocollo
Sub-GHz a codice fisso (protocollo: [Princeton/CAME/etc.]) sulla frequenza
[XXX.XX MHz]. Il segnale è stato catturato con il Flipper Zero e
ritrasmesso con successo, ottenendo l'apertura non autorizzata.

### Ambiente
- **Target:** [Marca/modello cancello]
- **Frequenza:** [XXX.XX MHz]
- **Protocollo:** [Nome protocollo]
- **Modulazione:** [OOK/ASK/FSK]
- **Bit:** [N bit]
- **Distanza cattura:** [X metri]
- **Distanza replay:** [X metri]

### Procedura
1. Sub-GHz → Read → frequenza [XXX.XX MHz]
2. Cattura del segnale durante apertura legittima (distanza: ~Xm)
3. Analisi: protocollo [nome], [N] bit, codice fisso [hex]
4. Sub-GHz → Saved → [file] → Send
5. Il cancello si apre

### Evidenza
- File `.sub` catturato: `gate_capture_YYYYMMDD.sub`
- Protocollo decodificato: [Nome] [N]bit Key:[HEX]
- Video apertura: [riferimento]

### Impatto
Qualsiasi persona con un dispositivo SDR o un Flipper Zero può catturare
il segnale di apertura e riprodurlo senza limiti. Non è richiesta
prossimità al telecomando originale - basta trovarsi nel raggio del
segnale durante una singola apertura legittima.

### Raccomandazione
| Priorità | Azione | Costo | Tempo |
|-----------|--------|-------|-------|
| Immediata | Limitare accesso fisico all'area del ricevitore | Basso | 1 giorno |
| Breve | Verificare se il ricevitore supporta rolling code | Basso | 1 settimana |
| Lungo | Sostituire con sistema rolling code (KeeLoq o AES) | 200-500 EUR | 2-4 settimane |
```

---

## Template - NFC: Badge Clone

```markdown
## [CRITICAL] Badge NFC MIFARE Classic Clonabile

**ID:** FZ-NFC-001
**Severity:** Critical
**CVSS 3.1:** 8.6 (AV:P/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:N)
**MITRE ATT&CK:** Initial Access (TA0001) / Valid Accounts (T1078)

### Descrizione
Il sistema di controllo accessi [nome/marca] utilizza badge NFC MIFARE
Classic [1K/4K] con crittografia Crypto1. Le chiavi crittografiche sono
state recuperate tramite [dictionary attack / MFKey32] e il badge è stato
clonato con successo su una Magic Card Gen4.

### Ambiente
- **Lettore:** [Marca/modello]
- **Card:** MIFARE Classic [1K/4K]
- **UID:** [XX:XX:XX:XX] (anonimizzato nel report finale)
- **SAK:** [0x08/0x18]
- **Chiavi recuperate:** [N]/[TOT] settori
- **Dati sensibili:** Settore [N] contiene [tipo dato]

### Procedura
1. NFC → Read → identificato MIFARE Classic [1K/4K], SAK [0xXX]
2. NFC → Read → Dictionary Attack → [N] chiavi trovate su [N] settori
3. NFC → Detect Reader → posizionato su lettore target x3 letture
4. MFKey32 → recuperate [N] chiavi mancanti
5. NFC → Read (completo) → dump [N] settori su [N]
6. Analisi dump: settore [N] contiene [dati accesso/ID/permessi]
7. NFC → Saved → Write → Magic Card Gen4
8. Test: badge clonato apre [porta/tornello/ascensore] con successo

### Evidenza
- Dump NFC: `badge_clone_YYYYMMDD.nfc` (sha256: [hash])
- Chiavi recuperate: [lista parziale anonimizzata]
- Settori con dati: [N], [N], [N]

### Impatto
- Accesso fisico non autorizzato a [aree protette]
- Possibilità di clonare qualsiasi badge della stessa infrastruttura
- Escalation: modifica settore [N] per [cambiare piano/permessi/credito]
- Crypto1 è rotto dal 2008 - l'intera infrastruttura è compromessa

### Raccomandazione
| Priorità | Azione | Costo | Tempo |
|-----------|--------|-------|-------|
| Immediata | Audit badge in circolazione, revocare smarriti | Basso | 1-2 giorni |
| Breve | Aggiungere PIN o biometrico come secondo fattore | Medio | 2-4 settimane |
| Lungo | Migrare a DESFire EV2/EV3 con AES-128 | Alto (3-15K EUR) | 2-6 mesi |
```

---

## Template - RFID: Badge 125 kHz Clone

```markdown
## [HIGH] Badge RFID 125 kHz Clonabile Senza Crittografia

**ID:** FZ-RFID-001
**Severity:** High
**CVSS 3.1:** 7.5 (AV:P/AC:L/PR:N/UI:N/S:C/C:N/I:H/A:N)
**MITRE ATT&CK:** Initial Access (TA0001) / Valid Accounts (T1078)

### Descrizione
Il sistema di controllo accessi utilizza badge RFID 125 kHz [EM4100/HID
H10301/Indala] senza crittografia. Il badge è stato letto e clonato su
un tag T5577 in meno di 10 secondi.

### Ambiente
- **Protocollo:** [EM4100 / HID H10301 / Indala]
- **ID:** [hex] | FC:[N] CN:[N] (per HID)
- **Distanza lettura:** [X cm]
- **Tempo clone:** [X secondi]

### Raccomandazione
Migrare a NFC con crittografia (minimo MIFARE DESFire EV2, consigliato
MIFARE DESFire EV3 con AES-128). I tag 125 kHz non hanno NESSUN
meccanismo di sicurezza - non è possibile mitigarli, solo sostituirli.
```

---

## Template - BadUSB: Keystroke Injection

```markdown
## [CRITICAL] Workstation Vulnerabile a Keystroke Injection USB

**ID:** FZ-USB-001
**Severity:** Critical
**CVSS 3.1:** 8.4 (AV:P/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H)
**MITRE ATT&CK:** Initial Access (TA0001) / Hardware Additions (T1200)

### Descrizione
La workstation [identificativo] accetta dispositivi USB HID senza
restrizioni. Un Flipper Zero configurato come BadUSB ha eseguito un
payload DuckyScript che ha [aperto una reverse shell / estratto credenziali
WiFi / creato un utente admin / disabilitato le difese].

### Ambiente
- **Target OS:** [Windows 10/11 / macOS / Linux]
- **EDR/AV:** [Nome e versione, o "Nessuno"]
- **USB Policy:** [Nessuna restrizione / GPO parziale]
- **Tempo di esecuzione:** [X secondi]
- **Rilevato:** [Si/No]

### Procedura
1. Inserito Flipper Zero nella porta USB [frontale/posteriore]
2. Payload: [nome_payload.txt]
3. Tempo totale: [X secondi]
4. Risultato: [shell ottenuta / credenziali estratte / etc.]

### Raccomandazione
| Priorità | Azione | Costo | Tempo |
|-----------|--------|-------|-------|
| Immediata | Disabilitare porte USB non necessarie (BIOS + GPO) | Basso | 1 giorno |
| Breve | Implementare USB device whitelisting | Medio | 1-2 settimane |
| Breve | Bloccare nuovi HID device tramite GPO | Basso | 1 giorno |
| Lungo | Deploy soluzione DLP con controllo USB | Alto | 1-3 mesi |
```

---

## Template - WiFi: Evil Portal

```markdown
## [HIGH] Rete WiFi Vulnerabile a Evil Portal / Credential Harvest

**ID:** FZ-WIFI-001
**Severity:** High
**CVSS 3.1:** 7.1 (AV:A/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:N)
**MITRE ATT&CK:** Initial Access (TA0001) / Phishing (T1566)

### Descrizione
Tramite ESP32 Marauder connesso al Flipper Zero, è stato possibile:
1. Deautenticare client dalla rete target [SSID]
2. Creare un Evil Portal con SSID identico
3. Raccogliere [N] set di credenziali da utenti che si sono riconnessi

### Ambiente
- **SSID target:** [nome]
- **Sicurezza:** WPA2-PSK / WPA2-Enterprise
- **Client deautenticati:** [N]
- **Credenziali raccolte:** [N] in [X minuti]
- **Distanza:** [X metri]

### Raccomandazione
| Priorità | Azione | Costo | Tempo |
|-----------|--------|-------|-------|
| Immediata | Implementare 802.11w (Protected Management Frames) | Basso | 1 giorno |
| Breve | Migrare a WPA2/WPA3-Enterprise con 802.1X | Medio | 2-4 settimane |
| Breve | Deploy WIDS per rilevare rogue AP | Medio | 1-2 settimane |
| Lungo | Formazione utenti su riconoscimento captive portal malevoli | Basso | Continuo |
```

---

## Template - Infrared: Device Control

```markdown
## [MEDIUM] Dispositivi IR Controllabili Senza Autenticazione

**ID:** FZ-IR-001
**Severity:** Medium
**CVSS 3.1:** 5.3 (AV:P/AC:L/PR:N/UI:N/S:U/C:N/I:L/A:H)
**MITRE ATT&CK:** Impact (TA0040) / Service Stop (T1489)

### Descrizione
I seguenti dispositivi nell'area [location] sono controllabili via
infrarosso senza autenticazione: [lista dispositivi]. È stato possibile
[spegnerli/modificare impostazioni/cambiare input] utilizzando il database
IR universale del Flipper Zero.

### Raccomandazione
- Posizionare dispositivi critici in armadi chiusi con finestra IR schermata
- Utilizzare sistemi di controllo via rete (IP/RS-232) con autenticazione
- Per display informativi: disabilitare ricevitore IR se non necessario
```

---

## Template Riassuntivo - Executive Summary

```markdown
# Executive Summary - Physical Penetration Test

**Cliente:** [Nome azienda]
**Data:** [GG/MM/AAAA]
**Scope:** Physical security assessment degli edifici [indirizzi]
**Tester:** [Nome]
**Autorizzazione:** [Riferimento contratto/lettera]

## Risultati

| Severity | Count | Esempi |
|----------|-------|--------|
| Critical | [N] | [Badge NFC clonabili, workstation aperte a BadUSB] |
| High | [N] | [Cancelli replay, WiFi evil portal] |
| Medium | [N] | [IR device control, BLE spam] |
| Low | [N] | [Informational findings] |

## Finding Principali

1. **[CRITICAL]** [Titolo] - [una riga di impatto]
2. **[HIGH]** [Titolo] - [una riga di impatto]
3. ...

## Raccomandazioni Prioritarie

1. [Azione più urgente]
2. [Seconda priorità]
3. [Terza priorità]

## Prossimi Passi
- [ ] Presentazione risultati al management ([data])
- [ ] Remediation plan entro [data]
- [ ] Re-test pianificato per [data]
```
