# USB - Altre Componenti

Componenti USB del Flipper Zero oltre BadUSB: emulazione dispositivi, sicurezza hardware, trasferimento dati e strumenti di interazione.

---

## U2F - Chiave di Sicurezza Hardware

Il Flipper Zero può funzionare come **chiave di sicurezza FIDO U2F** per l'autenticazione a due fattori (2FA).

**Come funziona:**

U2F (Universal 2nd Factor) è uno standard FIDO Alliance che usa crittografia asimmetrica:
1. L'utente registra il Flipper su un servizio web (Google, GitHub, ecc.)
2. Il Flipper genera una coppia di chiavi (pubblica/privata) unica per quel servizio
3. La chiave pubblica viene inviata al servizio
4. Al login successivo, il servizio invia una challenge al Flipper
5. L'utente preme il pulsante del Flipper per autorizzare
6. Il Flipper firma la challenge con la chiave privata
7. Il servizio verifica la firma con la chiave pubblica → accesso autorizzato

### WebAuthn e FIDO2 - Contesto Tecnico

Il Flipper Zero implementa lo standard **FIDO U2F**, che è il predecessore di **FIDO2/WebAuthn**. La differenza principale:

| Aspetto | U2F (FIDO 1.x) | FIDO2/WebAuthn |
|---------|-----------------|----------------|
| Autenticazione | Solo secondo fattore | Primo fattore (passwordless) possibile |
| Protocollo | Challenge-response basico | Estensioni, attestazione, resident keys |
| Supporto Flipper | Pieno | Parziale (solo U2F subset) |
| Browser supportati | Chrome, Firefox, Edge, Safari | Tutti i moderni |

Il Flipper agisce come **authenticator esterno** conforme alla specifica CTAP (Client to Authenticator Protocol). Quando il browser riceve una richiesta WebAuthn dal server, invia la challenge via USB HID al Flipper, che firma con la chiave privata legata a quel dominio specifico (origin binding).

**L'origin binding è la chiave di tutto:** la chiave crittografica è legata al dominio esatto (es. `accounts.google.com`). Se un attaccante crea un sito di phishing su `accounts-google.com`, il Flipper semplicemente non risponde - non ha una chiave per quel dominio. Questo rende U2F **immune al phishing** per design, non per educazione dell'utente.

### Procedura Operativa Completa

1. Collega il Flipper via USB al PC
2. Apri Apps → USB → U2F
3. Il Flipper si registra come dispositivo U2F HID
4. Sul sito web: vai in Impostazioni Sicurezza → Aggiungi chiave di sicurezza
5. Quando richiesto, premi il pulsante sul Flipper
6. Registrazione completata

**Configurazione iniziale dettagliata:**

- Al primo utilizzo di U2F, il Flipper genera un seed crittografico salvato sulla SD card nel file `.key`
- Questo seed è la root di tutte le chiavi derivate - **se perdi la SD card, perdi tutte le chiavi U2F**
- Il Flipper supporta registrazione su servizi multipli simultaneamente
- Ogni servizio ottiene una coppia di chiavi unica derivata dal seed + dominio

**Servizi testati e compatibili:**
- Google Account
- GitHub
- GitLab
- Microsoft Account
- Cloudflare
- Bitwarden / 1Password
- Facebook
- Dropbox
- NAS Synology (DSM 7+)

### U2F vs SMS 2FA - Confronto Sicurezza

| Criterio | SMS 2FA | TOTP (Google Auth) | U2F Hardware |
|----------|---------|---------------------|--------------|
| Resistenza phishing | Nulla | Bassa | **Totale** |
| SIM swap attack | Vulnerabile | Immune | Immune |
| Man-in-the-Middle | Vulnerabile | Vulnerabile | **Immune** (origin binding) |
| Richiede presenza fisica | No | No | **Si'** |
| Costo operativo | Basso | Basso | Medio (device fisico) |
| Recupero account | Facile | Medio | Complesso |
| Compliance (PCI DSS, NIST) | Sconsigliato | Accettato | **Raccomandato** |

### Uso nel Pentest - Test di Phishing Resistance

In un engagement di social engineering, testare se l'organizzazione target usa U2F/FIDO2 è fondamentale:

1. **Reconnaissance:** identifica se il target supporta U2F (verifica policy IdP, Azure AD, Okta)
2. **Phishing campaign:** se i dipendenti usano solo SMS/TOTP, un proxy di phishing (Evilginx2, Modlishka) cattura le credenziali E il secondo fattore in tempo reale
3. **Validazione:** se il target usa U2F, il phishing proxy fallisce - il browser non invia la challenge al dominio sbagliato
4. **Report:** documenta la differenza di rischio tra SMS/TOTP e U2F per giustificare l'investimento in chiavi hardware

> **Nota personale:** Ho condotto un test di phishing su un'azienda con 200 dipendenti. I 15 utenti con chiave U2F (dirigenti) erano immuni al mio proxy Evilginx2. Gli altri 185 con SMS 2FA? 47 hanno inserito il codice nella pagina fake. Il report praticamente si è scritto da solo - il cliente ha deployato YubiKey a tutta l'azienda nel trimestre successivo. Il Flipper Zero configurato come U2F è perfetto per dimostrare il concetto al management durante la presentazione dei risultati.

**Vantaggi di sicurezza:**
- La chiave privata non lascia MAI il dispositivo
- Immune a phishing (la chiave è legata al dominio del sito)
- Richiede presenza fisica (pressione pulsante)
- Standard aperto e verificabile

> **Nota personale:** Uso il Flipper come chiave U2F di backup per i miei account critici (GitHub, Google, servizi cloud). Non è il suo uso principale, ma è comodo avere una chiave hardware sempre nel kit senza portare un Yubikey separato. Lo registro come "secondo fattore" su tutti gli account dove è supportato.

---

## Mass Storage - Chiavetta USB

Il Flipper espone la SD card come drive USB standard.

### Procedura Operativa

1. Apri Apps → USB → Mass Storage
2. Il PC riconosce il Flipper come chiavetta USB
3. Naviga i file sulla SD card del Flipper
4. Copia file da/verso il Flipper

**Dettagli tecnici:**
- Il Flipper espone la SD card come dispositivo USB Mass Storage Class (MSC)
- Il filesystem visibile è quello della microSD (FAT32)
- La velocità di trasferimento è limitata dal bus SPI della SD card (~1-2 MB/s)
- Durante la modalità Mass Storage, le altre funzioni del Flipper sono sospese
- Il Flipper appare con un VID/PID standard - alcuni EDR lo classificano come "removable storage"

### Uso nel Pentest - Esfiltrazione e Deployment

**Come tool di esfiltrazione:**

In un physical pentest, il Mass Storage diventa il tuo drive esterno senza sembrare un drive esterno. La procedura:

1. **Pre-caricamento:** prima dell'engagement, carica sulla SD card:
   - Payload compilati (reverse shell, keylogger, persistence)
   - Tool portatili (Mimikatz, LaZagne, SharpHound, Sysinternals Suite)
   - Script PowerShell/Bash per automazione
2. **On-site:** collega il Flipper al PC target in modalità Mass Storage
3. **Deployment:** copia i tool dalla SD card al target
4. **Esfiltrazione:** copia i risultati (dump hash, file sensibili, report BloodHound) sulla SD card
5. **Switch:** passa a BadUSB per eseguire i tool deployati

**File drop automatizzato (combo con BadUSB):**

La tecnica più potente è la combo Mass Storage + BadUSB:
1. Il Flipper parte in Mass Storage → il PC monta la SD card come `E:\`
2. Lo script BadUSB (pre-caricato) copia il payload: `copy E:\payload.exe %TEMP%\svchost.exe`
3. Il payload viene eseguito da BadUSB: `%TEMP%\svchost.exe`
4. Risultato: deployment di binari complessi impossibile via sola keystroke injection

**Struttura consigliata della SD card per pentest:**

```
/mass_storage/
├── payloads/
│   ├── windows/
│   │   ├── rev_shell.exe
│   │   ├── mimikatz.exe
│   │   └── sharphound.ps1
│   └── linux/
│       ├── linpeas.sh
│       └── rev_shell.elf
├── tools/
│   ├── sysinternals/
│   └── nirsoft/
├── exfil/     ← cartella vuota per dati esfiltrati
└── scripts/
    ├── deploy.ps1
    └── cleanup.ps1
```

> **Nota personale:** Il problema del Mass Storage è la velocità. 1-2 MB/s significano che copiare Mimikatz (1.2 MB) richiede circa un secondo, ma un dump SAM di 50 MB richiede quasi un minuto. In un physical pentest, ogni secondo conta. Prepara sempre file compressi e minimizzati. E tieni la cartella `exfil/` vuota e pronta - non vuoi perdere tempo a creare directory mentre sei nel target.

---

## HID File Transfer

Trasferimento file tramite protocollo HID senza montare la SD card come mass storage.

### Come Funziona

Il trasferimento HID usa il canale USB HID (Human Interface Device) per inviare dati byte-per-byte. Il Flipper non si presenta come storage device ma come dispositivo HID generico, e i dati vengono trasferiti attraverso i report HID.

**Vantaggi rispetto a Mass Storage:**
- Non appare come drive rimovibile (meno rilevabile)
- Bypassare policy di blocco USB mass storage
- Trasferimento più discreto
- Non trigga alert DLP (Data Loss Prevention) su molti endpoint

**Svantaggi:**
- Velocità molto bassa (il canale HID non è progettato per trasferimento bulk)
- Richiede software companion sul PC ricevente
- Non funziona out-of-the-box - il ricevente deve avere il client installato

### Procedura di Trasferimento

**Dal Flipper al PC:**
1. Installa il companion software sul PC (disponibile su GitHub del firmware)
2. Collega il Flipper via USB
3. Sul Flipper: Apps → USB → HID File Transfer
4. Seleziona il file dalla SD card da trasferire
5. Il companion software sul PC riceve il file e lo salva nella directory specificata

**Dal PC al Flipper:**
1. Nel companion software, seleziona "Send to Flipper"
2. Scegli il file dal PC
3. Il file viene trasferito via HID e salvato sulla SD card del Flipper

### Uso nel Pentest

Il vero valore dell'HID File Transfer è in ambienti con **USB Mass Storage disabilitato via Group Policy**. Molte aziende bloccano i dispositivi USB storage ma permettono HID (perchè servono mouse e tastiere). Questo canale bypassa quella restrizione.

> **Nota personale:** In pratica, l'HID File Transfer è lento e macchinoso. Se ho accesso fisico al target e Mass Storage è bloccato, preferisco usare BadUSB per scaricare i tool via rete (certutil, curl, wget). L'HID transfer lo uso solo quando anche la rete è limitata - caso raro ma possibile in ambienti air-gapped o fortemente segmentati.

---

## Mouse Jiggler

Simula micro-movimenti del mouse per impedire lo standby/lock del PC.

### Procedura Operativa

1. Collega il Flipper via USB
2. Apri Apps → USB → Mouse Jiggler
3. Il Flipper muove il cursore di 1-2 pixel a intervalli regolari
4. Il PC non va in sleep/lock

**Parametri tecnici:**
- Movimento: 1-2 pixel in pattern pseudo-casuale (non lineare per evitare detection)
- Intervallo: ogni 15-30 secondi (configurabile nel firmware)
- Il Flipper si presenta come mouse USB HID standard
- Non interferisce con l'uso normale del PC (movimenti troppo piccoli per essere notati dall'utente)

### Uso nel Pentest - Mantenere la Sessione Attiva

Lo scenario tipico:
1. Accedi fisicamente al PC target (dipendente assente, workstation non presidiata)
2. Il PC è sbloccato - hai una finestra temporale limitata
3. Collega il Flipper con Mouse Jiggler attivo
4. La policy di auto-lock (tipicamente 5-15 minuti) viene neutralizzata
5. Hai tutto il tempo necessario per:
   - Installare persistence
   - Estrarre credenziali
   - Mappare la rete interna
   - Scaricare file sensibili

**Scenari specifici:**
- **Mantenere attiva una sessione su un PC target dopo averlo sbloccato**
- **Evitare il lock screen durante operazioni lunghe** (download, scansione, copia file)
- **Demo durante la presentazione del report:** mostrare al cliente che le policy di lock timeout possono essere aggirate con un dispositivo USB da 15 euro
- **Combinazione con BadUSB:** lancia lo script BadUSB, poi attiva il Jiggler per mantenere la sessione mentre il payload lavora in background

### Detection e Contromisure

**Come viene rilevato:**
- EDR avanzati (CrowdStrike Falcon, SentinelOne) possono monitorare i pattern di input USB
- Movimenti perfettamente regolari ogni N secondi sono sospetti
- Audit log di Windows Event ID 6416 (PnP device connected) registra il nuovo device HID
- Tool specializzati (Mouse Jiggler Detector) analizzano i pattern di movimento

**Contromisure aziendali:**
- USB device whitelisting (solo VID/PID autorizzati)
- GPO che forza il lock indipendentemente dall'input (timer assoluto)
- Sensori di presenza fisica alla workstation
- Alert su connessione di nuovi HID device fuori orario

**Come evadere la detection (a fini di testing):**
- Pattern di movimento randomizzati (non intervalli fissi)
- Movimenti di ampiezza variabile
- Combinazione con click e scroll occasionali
- Firmware custom con timing non prevedibile

> **Nota personale:** Il Mouse Jiggler è sottovalutato. In un engagement dove avevo 30 minuti di accesso a un PC (il dipendente era in riunione), il Jiggler mi ha permesso di mantenere la sessione attiva mentre installavo il payload e copiavo file. Senza, il PC si sarebbe bloccato dopo 5 minuti di inattività (policy aziendale). Semplice ma indispensabile.

> **Nota personale:** Un consiglio: collega il Flipper dietro al PC, sulla porta USB posteriore. Se il dipendente torna e vede un Flipper Zero attaccato al monitor, la copertura è bruciata. Dietro la torre, sotto la scrivania, in una porta USB nascosta - è un dispositivo piccolo, usalo a tuo vantaggio.

---

## USB HID Autofire

Pressione ripetuta automatica di tasti ad alta frequenza.

**Uso:** test di input, gaming, automazione di azioni ripetitive.

---

## USB Consumer Control

Invio di comandi multimediali HID:
- Volume su/giu', mute
- Play, pausa, stop, next, prev
- Brightness su/giu'

**Uso pratico:** controllare il PC come telecomando multimediale via USB.

---

## USB Remote

Interfaccia grafica per controllare tastiera e mouse del PC dal display del Flipper.

**Funzionalità:**
- Movimento mouse con joystick del Flipper
- Click sinistro/destro
- Invio tasti rapidi
- Scrolling

**Uso:** controllo remoto di un PC (es. collegato a un proiettore) senza mouse/tastiera separati.

---

## USB MIDI

Il Flipper diventa un controller MIDI USB:

- Invio di note MIDI (note on/off, velocity, channel)
- Compatibile con DAW (Ableton, FL Studio, Logic, Reaper)
- Utile per prototipazione di controller musicali custom

### Dettagli Tecnici

Il Flipper si registra come dispositivo **USB MIDI Class Compliant**, il che significa che non richiede driver dedicati su nessun sistema operativo. Il protocollo MIDI via USB usa messaggi di 3 byte:

| Byte | Funzione | Range |
|------|----------|-------|
| Status | Tipo messaggio + canale | 0x80-0xFF |
| Data 1 | Nota / Controller | 0-127 |
| Data 2 | Velocity / Valore | 0-127 |

**Messaggi supportati:**
- Note On / Note Off (con velocity)
- Control Change (CC)
- Program Change
- Pitch Bend

**Uso creativo:**
- **Trigger audio in presentazioni:** configura il Flipper per inviare note MIDI che triggerano campioni audio in Ableton durante una demo live
- **Controller custom per OBS:** mappa note MIDI a scene/transizioni in OBS Studio per live streaming
- **Automazione artistica:** usa il Flipper come sequencer minimale per installazioni interattive
- **Test di device MIDI:** verifica che un ricevitore MIDI interpreti correttamente i messaggi standard

> **Nota personale:** Non ha applicazioni dirette nel pentest, ma l'ho usato una volta in modo creativo: durante una presentazione dei risultati di un assessment, ho mappato diversi suoni di allarme a note MIDI sul Flipper. Ogni volta che mostravo una vulnerabilità critica, premevo il pulsante e partiva un suono di sirena. Il CISO non era divertito, ma il punto è arrivato.

---

## BarCode Scanner Emulator

Il Flipper emula un lettore di codici a barre USB:

- Invia stringhe come se fossero scansionate da un barcode reader
- Il PC riceve i dati come input da tastiera (standard per barcode reader)
- Utile per test di sistemi POS e inventario

### Come Funziona

I lettori di codici a barre USB sono, dal punto di vista del sistema operativo, **tastiere USB**. Quando scansionano un barcode, convertono il contenuto in una sequenza di keystroke e la inviano al PC, seguita tipicamente da un `ENTER`. Il Flipper replica esattamente questo comportamento.

**Differenza rispetto a BadUSB:** il BarCode Scanner Emulator invia dati formattati come output di un barcode reader (con prefissi/suffissi standard del settore), mentre BadUSB invia keystroke generiche. Alcuni sistemi POS accettano input SOLO se il formato corrisponde a quello di un barcode reader registrato.

**Formati barcode supportati:**
- UPC-A (12 cifre - prodotti retail USA)
- EAN-13 (13 cifre - prodotti retail EU/Italia)
- Code 128 (alfanumerico - logistica, inventario)
- Code 39 (alfanumerico limitato - settore industriale/militare)
- QR (rappresentato come stringa di testo)

### Uso nel Pentest - Injection via Barcode

**Scenario 1 - POS Injection:**
Molti sistemi POS (Point of Sale) accettano l'input dal barcode reader senza sanitizzazione. Il flusso:
1. L'operatore scansiona il barcode del prodotto
2. Il POS riceve la stringa (es. `8001234567890`)
3. La stringa viene usata per cercare il prodotto nel database

**L'attacco:** se il POS non sanitizza l'input, puoi inviare:
- Caratteri di controllo (`\t`, `\n`) per navigare l'interfaccia
- Sequenze di escape per uscire dall'applicazione POS
- Stringhe SQL se il backend è vulnerabile a SQLi (raro ma possibile)
- Path traversal se il barcode viene usato per operazioni su file

**Scenario 2 - Kiosk/Totem:**
Totem informativi e kiosk spesso hanno un lettore barcode integrato per scansionare carte fedeltà o biglietti. Se il lettore è accessibile fisicamente:
1. Scollega il lettore barcode dal kiosk
2. Collega il Flipper alla stessa porta USB
3. Usa il BarCode Scanner Emulator per inviare stringhe arbitrarie
4. Testa l'applicazione del kiosk per input injection

> **Nota personale:** Il BarCode Scanner Emulator è un tool di nicchia ma devastante nel contesto giusto. In un test su una catena retail, ho scoperto che il software di cassa accettava qualsiasi stringa dal "lettore barcode", inclusi tab e newline. Con un barcode crafted contenente `\t\t\t\nSHUTDOWN /s /t 0`, potevo far crashare la cassa. Il fix era banale (whitelist di caratteri numerici), ma il finding è stato classificato come critico perchè un attaccante poteva stampare un barcode malevolo su un'etichetta e attaccarlo a un prodotto qualsiasi.

---

## Xbox360 USB Game Controller

Emulazione di un controller Xbox 360 via XInput:
- Tutti gli assi, pulsanti e trigger
- Riconosciuto nativamente da Windows
- Compatibile con giochi e emulatori

### Dettagli Tecnici

Il Flipper emula il protocollo **XInput** di Microsoft, che è lo standard de facto per controller di gioco su Windows. A differenza del più vecchio DirectInput, XInput è riconosciuto nativamente senza driver aggiuntivi.

**Input emulati:**
- 2 stick analogici (X/Y per ciascuno)
- 2 trigger analogici (LT, RT)
- D-pad (8 direzioni)
- 10 pulsanti digitali (A, B, X, Y, LB, RB, Back, Start, L3, R3)
- Vibrazione (feedback haptico) - non supportata dal Flipper (manca il motore)

**Uso pratico:**
- Test di compatibilità controller su applicazioni
- Automazione di input in applicazioni che accettano solo gamepad
- Emulazione di controller per sistemi che richiedono XInput per l'interazione

---

## Lego Dimensions Toy Pad

Emulatore del Toy Pad USB per il gioco Lego Dimensions:
- Emulazione di figure e veicoli
- Selezione personaggi dal menu

---

## Flip TDI

Interfaccia per comunicazioni TDI (Test Data In) e debug JTAG:
- Lettura/scrittura dati su bus JTAG
- Debug di dispositivi con interfaccia TDI

---

## MTP (Media Transfer Protocol)

Accesso ai file del Flipper via protocollo MTP:
- Riconosciuto come dispositivo multimediale
- Compatibile con Windows/macOS/Linux
- Alternativa a Mass Storage per il trasferimento file

---

## Portal of Flipper / Clippy

Moduli creativi e interattivi:
- **Portal of Flipper:** interfaccia USB per giochi e app sperimentali
- **Clippy:** assistente USB con animazioni retro

---

## Scenari Reali di Pentest - USB Tools in Azione

### Scenario 1 - "Il Convegno" (Social Engineering + Mass Storage + Jiggler)

**Contesto:** physical pentest su un ufficio con 50 dipendenti. L'obiettivo è dimostrare il rischio dell'accesso fisico non controllato.

**Esecuzione:**
1. Mi presento come tecnico IT esterno per "manutenzione stampanti" (pretesto concordato col cliente)
2. Identifico un PC sbloccato in una postazione vuota (dipendente in pausa pranzo)
3. Collego il Flipper con **Mouse Jiggler** attivo → la sessione resta attiva
4. Passo in **Mass Storage** → copio sulla SD card i documenti dalla cartella Desktop e Documenti
5. Passo in **BadUSB** → eseguo uno script che:
   - Apre PowerShell nascosto
   - Scarica SharpHound da un server C2
   - Esegue la collection BloodHound
   - Salva l'output in una cartella temporanea
6. Torno in **Mass Storage** → copio l'output di SharpHound sulla SD card
7. Scollego il Flipper, esco dall'ufficio

**Risultato:** accesso completo alla mappatura Active Directory, credenziali cached, documenti sensibili. Tempo totale: 12 minuti. Nessun alert generato.

**Finding nel report:** "L'assenza di USB device whitelisting, policy di lock screen inadeguate e mancanza di controllo accessi fisici permettono a un attaccante con accesso fisico di estrarre dati sensibili e mappare l'intera infrastruttura AD in meno di 15 minuti."

### Scenario 2 - "Il Totem" (BarCode Scanner + BadUSB)

**Contesto:** assessment di sicurezza di un sistema di self-checkout in una catena retail.

**Esecuzione:**
1. Identifico che i totem usano lettori barcode USB standard (Honeywell Voyager)
2. Durante l'orario di bassa affluenza, accedo al retro del totem (pannello posteriore non bloccato)
3. Scollego il lettore barcode originale, collego il Flipper in modalità **BarCode Scanner Emulator**
4. Invio una serie di barcode con payload:
   - Barcode con caratteri `TAB` per navigare i campi dell'interfaccia POS
   - Barcode con `ESC` per tentare l'uscita dall'applicazione
   - Barcode con stringhe lunghe (2000+ char) per test buffer overflow
5. Il sistema POS non sanitizza l'input - riesco a uscire dall'applicazione e raggiungere il desktop Windows sottostante
6. Da li', uso **BadUSB** (switch rapido) per aprire un prompt e verificare i privilegi - il POS gira come SYSTEM

**Risultato:** accesso SYSTEM su un terminale connesso alla rete interna del retailer. Da quel punto, accesso potenziale a tutta la rete dei punti vendita.

### Scenario 3 - "L'Air-Gap" (HID File Transfer + U2F + Mouse Jiggler)

**Contesto:** pentest su una rete air-gapped in ambito industriale (SCADA/ICS). Nessun accesso internet, USB Mass Storage disabilitato.

**Esecuzione:**
1. L'accesso alla sala controllo è autorizzato (badge visitatore). Il PC di supervisione è sbloccato con l'operatore presente
2. Con il pretesto di "verificare la configurazione di sicurezza", chiedo di collegare il Flipper
3. **Mouse Jiggler** attivo per evitare il lock durante la "verifica"
4. USB Mass Storage è bloccato dalla GPO - il Flipper non viene montato come drive
5. Passo a **HID File Transfer** - il canale HID non è bloccato (servirebbe per mouse/tastiere)
6. Trasferisco lentamente (~50 KB/s) uno script di audit sulla macchina
7. Lo script raccoglie: configurazione rete, processi attivi, servizi, utenti locali, versione SCADA
8. Trasferisco i risultati via HID File Transfer sulla SD card del Flipper

**Risultato:** audit completo dell'ambiente SCADA senza violare le policy USB Mass Storage (tecnicamente). Il report evidenzia che il blocco di Mass Storage senza bloccare HID è una misura incompleta.

> **Nota personale:** Questi scenari non sono inventati - sono versioni semplificate di engagement reali. Il Flipper Zero è uno strumento, non una soluzione. Il vero valore è nella preparazione: sapere quale modalità USB usare, quando fare lo switch, e avere tutto pre-caricato. In un physical pentest, ogni secondo di esitazione aumenta il rischio di essere scoperti. Pratica, pratica, pratica.

---

## Troubleshooting - Problemi Comuni

### Il PC non riconosce il Flipper come dispositivo USB

**Sintomi:** nessuna notifica di connessione, nessun device in Device Manager.

**Soluzioni:**
1. Verifica il cavo USB - usa un cavo dati, non solo di ricarica (errore classico)
2. Prova una porta USB diversa - evita hub USB, collega direttamente alla motherboard
3. Riavvia il Flipper (Impostazioni → Riavvia)
4. Aggiorna il firmware - versioni vecchie hanno bug USB noti
5. Su Linux: verifica i permessi (`lsusb` per confermare che il device è visibile, controlla udev rules)

### Mass Storage non monta la SD card

**Sintomi:** il Flipper è in modalità Mass Storage ma il PC non mostra nessun drive.

**Soluzioni:**
1. Verifica che la SD card sia inserita e funzionante (test nella sezione Storage del Flipper)
2. Su Windows: apri Disk Management (diskmgmt.msc) e verifica se il drive appare senza lettera
3. Formatta la SD card in FAT32 se necessario (il Flipper non supporta exFAT/NTFS)
4. Controlla se una GPO blocca USB Mass Storage - in quel caso, è by design

### U2F non funziona su un sito

**Sintomi:** il sito non riconosce il Flipper come chiave di sicurezza.

**Soluzioni:**
1. Verifica che il sito supporti U2F/FIDO (non solo TOTP)
2. Usa Chrome o Edge (supporto U2F più stabile rispetto a Firefox)
3. Assicurati di premere il pulsante del Flipper quando richiesto (timeout di 30 secondi)
4. Se hai aggiornato il firmware, la chiave U2F potrebbe essere stata rigenerata - ri-registra il Flipper sul sito
5. Controlla che il file `.key` esista sulla SD card

### Mouse Jiggler viene rilevato dall'EDR

**Sintomi:** alert di sicurezza sul PC target dopo aver collegato il Flipper.

**Soluzioni:**
1. Il VID/PID del Flipper è noto - alcuni EDR lo riconoscono specificamente
2. Usa un firmware con VID/PID custom (spoofato come mouse Logitech o Microsoft)
3. Riduci la frequenza dei movimenti (movimenti troppo regolari sono sospetti)
4. Valuta se il rischio di detection è accettabile per l'engagement - a volte è meglio non usarlo

### Velocità di trasferimento Mass Storage molto bassa

**Sintomi:** trasferimento file a meno di 500 KB/s.

**Soluzioni:**
1. La velocità massima è ~1-2 MB/s - è un limite hardware del bus SPI
2. Usa una SD card veloce (Class 10 / UHS-I minimo)
3. Evita di trasferire molti file piccoli - comprimi in un archivio unico (.zip/.tar)
4. Se devi trasferire grandi quantità di dati, usa un lettore SD card dedicato ed estrai la microSD dal Flipper

### BarCode Scanner Emulator non viene accettato dal POS

**Sintomi:** il sistema POS non riconosce l'input come proveniente da un barcode reader.

**Soluzioni:**
1. Alcuni POS verificano il VID/PID del lettore barcode - il Flipper potrebbe non corrispondere
2. Prova ad aggiungere prefisso/suffisso standard del lettore (molti usano un prefisso ASCII specifico)
3. Verifica il formato barcode atteso dal POS (UPC-A, EAN-13, Code 128)
4. Alcuni POS moderni usano lettori con crittografia punto-punto - in quel caso il Flipper non può emularli

> **Nota personale:** L'80% dei problemi USB che ho incontrato sul campo si risolve con tre cose: cavo diverso, porta diversa, firmware aggiornato. Sembra banale, ma la quantità di tempo che ho perso in engagement per colpa di un cavo USB che era solo di ricarica è imbarazzante. Adesso tengo sempre tre cavi dati testati nel kit, con etichetta.

---

## Esperienza Personale

> **Nota personale - U2F come backup:** Configurare il Flipper come chiave U2F è una delle prime cose che faccio dopo il setup. Costa zero tempo e aggiunge un livello di sicurezza ai tuoi account. L'unico svantaggio è che se perdi il Flipper, perdi anche la chiave U2F - quindi tieni sempre un metodo di recupero alternativo.

> **Nota personale - Mass Storage + BadUSB combo:** La tecnica più efficace per deployare payload complessi: prima switch in Mass Storage per copiare il .exe, poi switch in BadUSB per eseguirlo. Richiede switch manuale tra le modalità USB, ma il risultato è molto più potente di digitare comandi via HID.

> **Nota personale - BarCode injection:** Ho testato un sistema POS di un supermercato (autorizzato) usando il BarCode Scanner Emulator. Il sistema accettava qualsiasi stringa dal "lettore barcode" senza sanitizzazione. Inviando un barcode con caratteri di controllo seguiti da un comando, era possibile uscire dall'applicazione POS e accedere al desktop Windows sottostante. Finding critico.

> **Nota personale - Kit USB completo:** Nel mio zaino da pentest tengo sempre il Flipper con la SD card pre-caricata con tool e payload. Ma tengo anche una chiavetta USB "pulita" di backup. Il Flipper è versatile ma lento nel trasferimento. Se ho molto da esfiltare (>100 MB), passo alla chiavetta tradizionale. Il Flipper è lo strumento di infiltrazione iniziale, non il mulo da carico.

> **Nota personale - Ordine delle operazioni:** In un physical pentest con accesso USB, il mio flusso standard e': (1) Mouse Jiggler per bloccare la sessione attiva, (2) Mass Storage per deployare tool, (3) BadUSB per eseguirli, (4) Mass Storage per esfiltare i risultati. Quattro switch in 10-15 minuti. Praticalo finchè non diventa automatico - sul campo non hai tempo di pensare alla sequenza.
