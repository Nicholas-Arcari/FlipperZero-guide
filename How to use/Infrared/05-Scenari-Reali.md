## Scenari di Penetration Testing

### Scenario 1: Spegnimento TV/Display in Ambienti Target

**Contesto:** Durante un physical penetration test, hai accesso a sale riunioni, reception, lobby e aree comuni dell'edificio target. Schermi TV, monitor digital signage e proiettori mostrano informazioni o sono semplicemente accesi.

**Obiettivo:** Dimostrare il controllo non autorizzato di dispositivi elettronici nell'ambiente.

**Procedura operativa:**

1. **Ricognizione:** Identifica i dispositivi presenti e, se possibile, le marche (logo, etichetta posteriore, modello visibile)
2. **Preparazione:** Carica sul Flipper il database universale IR (pre-installato) e eventuali file .ir specifici per le marche identificate
3. **Approccio:** Avvicinati a 3-5 metri dal display target. In una sala riunioni durante una pausa, nella lobby durante orari tranquilli
4. **Esecuzione - Metodo 1 (marca nota):** Vai su Infrared → Universal Remotes → TV, seleziona la marca, invia Power Off
5. **Esecuzione - Metodo 2 (marca ignota):** Usa IR Blaster o Universal Remotes in modalità "cerca tutte le marche" - il Flipper ciclerà attraverso decine di codici Power Off
6. **Verifica:** Il display si spegne
7. **Documentazione:** Annota marca, modello, distanza di successo, orario

**Rischi operativi:**
- Lo spegnimento di un display può attirare attenzione (personale IT, security, impiegati)
- In ambienti con sorveglianza video, il gesto di puntare il Flipper potrebbe essere registrato
- Alcuni display hanno protezione "Power Lock" che impedisce lo spegnimento via IR

**Mitigazioni:**
- Esegui durante momenti di basso traffico
- Tieni il Flipper nascosto nella mano (è piccolo - non è un telecomando evidente)
- Punta verso il soffitto per usare il rimbalzo se non vuoi puntare direttamente

> **Nota personale:** Questo è l'uso IR più comune nel pentest fisico e il più spettacolare nel report. "L'operatore ha spento i display nella sala riunioni Executive del 3o piano senza alcuna autorizzazione o credenziali". I clienti capiscono immediatamente l'impatto. Ma attenzione: in molti engagement lo scope del pentest non include esplicitamente il controllo di dispositivi IR - verifica sempre con il cliente prima di procedere.

### Scenario 2: Comfort Manipulation / Social Engineering via AC

**Contesto:** In un engagement di social engineering, hai bisogno di creare una situazione che giustifichi una richiesta di accesso o crei confusione.

**Obiettivo:** Manipolare il comfort ambientale per influenzare il comportamento delle persone.

**Procedura operativa:**

1. **Ricognizione:** Identifica il tipo di climatizzatore e, se possibile, la marca
2. **Cattura:** Se hai accesso temporaneo alla stanza (es. sei un "visitatore"), cattura i segnali del telecomando originale per i comandi chiave (Power, Temp Up, Temp Down, Mode)
3. **Azione:** Abbassa la temperatura a 18 gradi o alzala a 30 gradi (in estate), poi "offri aiuto" per risolvere il problema
4. **Variante social engineering:** Imposta il climatizzatore su una modalità scomoda, poi presentati come tecnico HVAC venuto a risolvere il problema

**Esempi pratici:**
- **Stanza troppo calda:** Le persone lasciano la stanza, dandoti accesso temporaneo a documenti, schermi sbloccati, hardware
- **Stanza troppo fredda:** Le persone cercano aiuto alla reception, creando un'apertura per accedere ad aree normalmente presidiate
- **Rumore ventola al massimo:** Crea fastidio e giustifica l'intervento di un "tecnico"

**Limiti:**
- Richiede l'identificazione del protocollo AC specifico (non sempre banale)
- La portata TX limitata del Flipper richiede accesso alla stanza
- Alcuni AC aziendali sono controllati centralmente (BMS - Building Management System) e il telecomando IR è disabilitato

### Scenario 3: Reverse Engineering di Telecomando Proprietario

**Contesto:** Incontri un dispositivo con telecomando IR proprietario - sistema di allarme, controllo accessi legacy, display industriale, sistema AV di sala conferenze.

**Obiettivo:** Catturare e riprodurre i segnali per ottenere il controllo del dispositivo.

**Procedura operativa:**

1. **Cattura iniziale:** Con IR Decoder, cattura ogni tasto del telecomando originale
2. **Analisi:** Verifica se il protocollo è riconosciuto o se è RAW
3. **Mappatura:** Crea un file .ir con tutti i comandi catturati, nominandoli chiaramente
4. **Test:** Riproduci ogni segnale e verifica che il dispositivo risponda correttamente
5. **Reverse engineering avanzato (se necessario):**
   - Usa IR Scope per analizzare le waveform
   - Confronta comandi diversi per identificare la struttura (header, address, command, checksum)
   - Se il protocollo usa checksum, identificalo catturando variazioni sistematiche (es. tutti i numeri 0-9)
   - Prova a generare comandi sintetici modificando i bit del command

**Esempio reale - Sistema AV sala conferenze:**

Un sistema AV Crestron in una sala conferenze usa un telecomando IR per:
- Accendere/spegnere il proiettore
- Selezionare l'input (HDMI1, HDMI2, VGA)
- Controllare il volume
- Abbassare/alzare lo schermo motorizzato

Catturando tutti i comandi del telecomando, puoi controllare l'intero sistema AV - incluso abbassare lo schermo, accendere il proiettore e selezionare l'input desiderato. In un pentest, questo dimostra il controllo dell'infrastruttura AV senza credenziali.

### Scenario 4: IR Come Covert Channel per Data Exfiltration

**Contesto:** In scenari avanzati, l'IR può essere usato come canale nascosto per l'esfiltrazione di piccole quantità di dati.

**Principio:** Se hai accesso fisico a un computer e puoi installare un programma (o sfruttare uno già presente), puoi far emettere al LED IR della webcam o a un LED IR esterno collegato via USB segnali che codificano dati. Un secondo Flipper Zero (o altro ricevitore IR) posizionato in line-of-sight cattura questi segnali.

**Caratteristiche del canale:**
- **Banda ridottissima:** pochi byte al secondo nel migliore dei casi
- **Non rilevabile da firewall o IDS:** il traffico IR non passa per la rete
- **Richiede line-of-sight:** il ricevitore deve "vedere" il trasmettitore
- **Rilevabile da ispezione visiva:** un LED IR attivo è visibile con fotocamere digitali (smartphone)

**Limiti pratici:**
- La velocità è troppo bassa per esfiltrazione di massa (niente database, niente file)
- Utile solo per dati di alto valore e piccola dimensione: chiavi crittografiche, password, hash, piccoli token
- La necessità di line-of-sight limita gli scenari possibili
- Nel mondo reale, il Bluetooth o l'emissione RF involontaria sono canali covert molto più pratici

**Questo scenario è più teorico che pratico** - lo includo perchè è discusso nella letteratura di sicurezza e dimostra un principio importante: qualsiasi canale di comunicazione, anche l'IR, può essere abusato.

### Scenario 5: Attacco a Sistemi di Digital Signage

**Contesto:** Edifici commerciali, aeroporti, stazioni, centri commerciali e reception aziendali utilizzano display di digital signage per mostrare informazioni, pubblicità, orari e mappe.

**Obiettivo:** Dimostrare che un attaccante può interferire con il sistema di digital signage.

**Procedura operativa:**

1. **Ricognizione:** Identifica i display (Samsung, LG, NEC, Sony sono i più comuni nel digital signage)
2. **Identificazione:** I display di digital signage sono spesso TV commerciali con input HDMI da un media player. Il ricevitore IR del display è quasi sempre attivo
3. **Azioni possibili:**
   - **Spegnimento:** Power Off del display
   - **Cambio input:** Passa da HDMI (contenuto digital signage) a TV tuner, USB o altro input vuoto
   - **Cambio volume:** Alza il volume al massimo o mutalo
   - **Accesso al menu OSD:** Apri il menu di servizio del display per modificare impostazioni
4. **Impatto:**
   - Display spento = informazioni non disponibili per clienti/passeggeri
   - Display su input sbagliato = schermata "No Signal" o input inatteso
   - Menu OSD visibile = evidenzia la marca e il modello del display, potenzialmente utile per ulteriori attacchi

**Contromisure che potresti incontrare:**
- Ricevitore IR coperto con nastro opaco (la più semplice ed efficace)
- Display in modalità "Hotel/Hospitality" con IR limitato
- Media player che riaccende/ripristina il display automaticamente dopo uno spegnimento
- Display montati ad altezza irraggiungibile (>5m) - fuori portata TX del Flipper

> **Nota personale:** I sistemi di digital signage sono il bersaglio IR più facile e diffuso. Nella mia esperienza, almeno il 70-80% dei display di digital signage nelle aziende italiane ha il ricevitore IR completamente accessibile e senza protezioni. Un fatto che genera sempre reazione nei report di pentest. La contromisura più efficace - un pezzo di nastro adesivo nero sul ricevitore IR - costa zero ed è efficace al 100%.

---

## Il Database IR Universale

### Cos'è il Database IR del Flipper Zero

Il Flipper Zero include un **database IR universale** pre-installato che contiene migliaia di codici per TV, proiettori, soundbar e climatizzatori di centinaia di marche diverse.

Il file principale è **`tv.ir`** (e file analoghi per AC e altri dispositivi), memorizzato nel firmware e accessibile tramite la funzione Universal Remotes.

### Struttura del Database

Il database è organizzato per **produttore e modello** e contiene per ogni dispositivo almeno:

- **Power On/Off** (il comando più universale)
- **Volume Up/Down**
- **Mute**
- **Channel Up/Down**
- **Input Select**

Ogni voce specifica:
- **Protocollo** (NEC, RC5, RC6, SIRC, Samsung, ecc.)
- **Frequenza portante**
- **Address** del dispositivo
- **Command** per ogni funzione

### Formato dei File .ir

Un file `.ir` del Flipper ha un formato testo semplice:

```
Filetype: IR signals file
Version: 1

name: Power
type: parsed
protocol: NEC
address: 04 00 00 00
command: 08 00 00 00

name: Vol_Up
type: parsed
protocol: NEC
address: 04 00 00 00
command: 02 00 00 00

name: Custom_Signal
type: raw
frequency: 38000
duty_cycle: 0.330000
data: 9000 4500 560 560 560 1690 560 560 560 560 560 1690 560 1690 560 560 560 43000
```

**Campi per segnali decodificati (`type: parsed`):**
- `protocol`: nome del protocollo
- `address`: indirizzo del dispositivo (in formato hex, LSB first, padding a 4 byte)
- `command`: comando (stesso formato)

**Campi per segnali RAW (`type: raw`):**
- `frequency`: frequenza della portante in Hz
- `duty_cycle`: duty cycle della portante (0.0-1.0)
- `data`: sequenza di tempi in microsecondi (burst, space, burst, space...)

### Come Aggiungere Nuovi Dispositivi

**Metodo 1 - Cattura diretta:**

1. Usa Learn New Remote per catturare i comandi del telecomando originale
2. I segnali vengono salvati automaticamente nella SD card
3. Organizza i file nella cartella `/ext/infrared/` con nomi descrittivi

**Metodo 2 - Download da Flipper-IRDB:**

Il repository [Flipper-IRDB](https://github.com/Lucaslhm/Flipper-IRDB) su GitHub è la più grande collezione di file `.ir` per il Flipper Zero:

- Migliaia di dispositivi catalogati per marca e modello
- Organizzato per categoria (TV, AC, Audio, Projector, Fan, Fireplace, LED, ecc.)
- File pronti da copiare sulla SD card

**Metodo 3 - Creazione manuale:**

Puoi creare file `.ir` con un editor di testo seguendo il formato sopra. Utile quando:
- Hai i codici da un database online (es. LIRC, irdb.tk)
- Vuoi combinare segnali da fonti diverse
- Stai facendo reverse engineering e vuoi testare variazioni

### Il Database Universale Integrato

Oltre ai file `.ir` sulla SD card, il Flipper ha un database integrato nel firmware che viene usato dalla funzione **Universal Remotes**. Questo database:

- Contiene codici Power Off/On per **centinaia di marche TV**
- È organizzato per massimizzare la copertura con il minor numero di invii
- Cicla attraverso i codici più comuni prima, poi quelli meno diffusi
- Può impiegare da 2-3 secondi (marca comune) a 1-2 minuti (marca rara) per trovare il codice giusto

> **Nota personale:** Il database integrato è impressionante - nella mia esperienza copre circa l'85-90% delle TV che ho incontrato in ambienti aziendali italiani. Samsung, LG, Sony, Philips, Panasonic, Sharp, Hisense, TCL - tutti presenti. I fallimenti avvengono tipicamente con marche molto economiche o molto di nicchia, oppure con display professionali che usano protocolli RS-232 o IP invece di IR.

---

## Cross-Reference - Scenari Multi-Vettore

| Scenario | Modulo Correlato | Link | Come si collegano |
|----------|-----------------|------|-------------------|
| Hotel: IR + NFC | NFC | [05-Scenari-Reali](../NFC/05-Scenari-Reali.md) | Card hotel NFC per accesso stanza + IR per TV/AC (social engineering, disruption) |
| Conference room + WiFi | WiFi-Marauder | [05-Scenari-Reali](../WiFi-Marauder/05-Scenari-Reali.md) | IR per spegnere display/proiettore + WiFi scan della rete AV |
| Digital signage + BadUSB | USB/Bad USB | [05-Scenari-Reali](../USB/Bad%20USB/05-Scenari-Reali.md) | IR per accesso al menu del display → BadUSB sulla porta USB del media player |
| HVAC + Sub-GHz | Sub-GHz | [05-Scenari-Reali](../Sub-GHz/05-Scenari-Reali.md) | Sistemi HVAC: IR per unità locali + Sub-GHz per sensori temperatura wireless |
| IR + BLE | Bluetooth | [05-Scenari-Reali](../Bluetooth/05-Scenari-Reali.md) | Dispositivi smart: IR tradizionale + BLE per configurazione/controllo avanzato |

