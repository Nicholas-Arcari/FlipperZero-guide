# Scenari Reali di Penetration Testing - NFC

Scenari operativi dettagliati per l'utilizzo del modulo NFC in contesti di penetration testing fisico, red teaming e security assessment. Ogni scenario è basato su esperienze reali e include procedura completa, finding atteso e raccomandazioni.

---

## Scenario 1 - Bypass Sistema Badge Aziendale MIFARE Classic

**Obiettivo:** dimostrare che il sistema badge dell'edificio target è vulnerabile

**Fase 1 - Ricognizione:**
1. Identifica il tipo di lettore (HID, Suprema, ZKTeco, ecc.)
2. Osserva i dipendenti: dove tengono il badge? Lo lasciano sulla scrivania?
3. Usa NFC/RFID Detector per verificare la frequenza (13.56 MHz NFC vs 125 kHz RFID)

**Fase 2 - Lettura Badge:**
1. Social engineering: "Posso vedere il suo badge un momento? Sto facendo un audit di sicurezza autorizzato" (con autorizzazione del management)
2. Oppure: attendi che un dipendente lasci il badge sulla scrivania → lettura rapida (3 secondi)
3. NFC → Read → identifica il tipo (SAK 0x08 = MIFARE Classic 1K → perfetto)
4. Dictionary attack → se trova tutte le chiavi: dump completo → clonazione immediata
5. Se non trova tutte le chiavi: continua con MFKey32

**Fase 3 - MFKey32 (se necessario):**
1. Attiva Detect Reader
2. Presenta il Flipper al lettore del tornello/porta
3. Ripeti 2-3 volte
4. Apri MFKey → recupera le chiavi mancanti
5. Ri-leggi il badge → dump completo

**Fase 4 - Clonazione:**
1. Scrivi il dump su una Magic Card Gen4
2. Testa la Magic Card al lettore → la porta si apre
3. Documenta: foto, timestamp, tipo di vulnerabilità

**Fase 5 - Report:**
- Finding: "Il sistema di accesso utilizza MIFARE Classic 1K con chiavi recuperabili tramite attacco MFKey32"
- Impatto: "Un attaccante con accesso fisico temporaneo al badge di un dipendente può clonarlo in meno di 30 secondi e ottenere accesso permanente all'edificio"
- CVSS: 7.2+ (High) - Physical access + Authentication Bypass
- Raccomandazione: "Migrare a MIFARE DESFire EV2 o iClass SE con chiavi diversificate. Implementare multi-factor authentication (badge + PIN) per aree sensibili"

---

## Scenario 2 - Analisi Card Hotel

**Obiettivo:** valutare la sicurezza delle card camera di un hotel

**Procedura:**
1. Leggi la card della tua camera (NFC → Read)
2. Identifica il tipo: quasi sempre MIFARE Classic 1K o Ultralight
3. Se MIFARE Classic: tenta dictionary attack + MFKey32
4. Se riesci a leggere tutti i settori: analizza i dati
5. Usa NFC Comparator: confronta la card prima e dopo aver aperto la porta
6. Identifica quale settore contiene il numero di camera/codice accesso
7. Modifica il settore → testa su una porta diversa (solo con autorizzazione dell'hotel)

**Finding tipici:**
- Numero camera in chiaro nel settore 1
- Nessuna verifica di integrità (il sistema accetta dati modificati)
- Chiavi di default (FFFFFFFFFFFF) non cambiate
- Possibilità di creare card master modificando un flag specifico

> **Nota personale:** Ho testato card hotel in 4 catene diverse. 3 su 4 usavano MIFARE Classic con chiavi di default. In un caso, cambiando un singolo byte nel settore 2 da "01" a "FF", la card apriva TUTTE le porte dell'hotel, incluse le aree staff. Era il "master flag". Finding critico che ha portato alla sostituzione dell'intero sistema di accesso.

---

## Scenario 3 - Relay Attack su Badge Aziendale

**Obiettivo:** dimostrare che un badge può essere usato a distanza

**Prerequisiti:**
- Due Flipper Zero (o Flipper + telefono NFC con app relay)
- Rete per collegare i due dispositivi

**Procedura:**
1. Attaccante 1 (Proxy): si posiziona vicino al lettore dell'edificio
2. Attaccante 2 (Relay): si posiziona vicino alla vittima (es. in mensa, in riunione)
3. Quando la vittima è vicina, Attaccante 2 attiva il relay → legge il badge
4. I dati vengono inoltrati in tempo reale ad Attaccante 1
5. Attaccante 1 emula il badge al lettore → la porta si apre

**Contromisure:**
- Distance bounding (misura il tempo di risposta per rilevare il relay)
- PIN richiesto in aggiunta al badge
- Monitoraggio accessi anomali (badge usato in due posti contemporaneamente)

---

## Scenario 4 - Assessment Controllo Accessi Multi-Piano

**Obiettivo:** valutare la segmentazione degli accessi in un edificio corporate con badge NFC su più livelli

**Contesto:** L'edificio ha 8 piani con aree a diversi livelli di sicurezza: reception (livello 0), uffici standard (livelli 1-5), datacenter (livello 6), sala dirigenza (livello 7). Ogni dipendente ha un badge MIFARE Classic 4K con permessi per i propri piani.

**Fase 1 - Profiling dei badge:**
1. Leggi il badge di un dipendente con accesso limitato (es. livelli 0-2) → NFC → Read
2. SAK 0x18 → MIFARE Classic 4K → dictionary attack
3. Dump completo: 40 settori × 4 blocchi = 160 blocchi da analizzare
4. Ripeti con un secondo badge (livelli 0-3) per comparazione

**Fase 2 - Analisi della struttura dati:**
1. NFC Comparator: confronta i due dump settore per settore
2. Risultati tipici:
   - Settore 0: UID + dati manifatturiero (fissi)
   - Settore 1-2: dati identificativi dipendente (nome/ID in chiaro o offuscato)
   - Settore 3: **mappa permessi** - byte diversi tra i due badge
   - Settore 4: timestamp ultimo accesso
   - Settori 5-39: non utilizzati o padding
3. Il byte nel settore 3, offset 4 contiene la bitmask dei piani autorizzati:
   - Badge 1: `0x07` = `00000111` → piani 0, 1, 2
   - Badge 2: `0x0F` = `00001111` → piani 0, 1, 2, 3

**Fase 3 - Escalation dei privilegi:**
1. Scrivi il dump su Magic Card Gen4
2. Modifica il byte permessi: `0x07` → `0xFF` = `11111111` → tutti i piani
3. Testa la Magic Card al lettore del piano 6 (datacenter) → accesso consentito!
4. La centralina non verifica l'integrità dei dati del settore → nessun MAC/checksum

**Fase 4 - Valutazione impatto:**
1. Testa accesso a ogni piano con la card modificata → documenta quale piano si apre
2. Verifica se il sistema di logging registra il badge originale o quello clonato
3. Controlla se esiste un alert per accessi a piani non autorizzati

**Report:**
- **Critico:** "La segmentazione degli accessi si basa su una bitmask in chiaro nel settore 3 del badge MIFARE Classic 4K. La modifica di un singolo byte permette privilege escalation a qualsiasi livello, incluso il datacenter"
- **Alto:** "Il sistema non implementa verifiche di integrità sui dati del badge (nessun MAC, CRC o firma digitale)"
- **Medio:** "I dati identificativi del dipendente sono memorizzati in chiaro nei settori 1-2"
- Raccomandazione: "Implementare mutual authentication con chiavi diversificate + MAC su settori critici. Considerare migrazione a DESFire EV3 con secure messaging"

---

## Scenario 5 - Audit Sistema Mensa/Credito Prepagato

**Obiettivo:** valutare la sicurezza del sistema di pagamento NFC della mensa aziendale

**Contesto:** La mensa usa card NFC prepagate - i dipendenti caricano credito alla cassa e lo scalano ad ogni pasto. Il sistema usa MIFARE Classic 1K.

**Fase 1 - Analisi della card:**
1. NFC → Read prima del pasto: dump completo con dictionary attack
2. Annota il saldo corrente dalla ricevuta: 15.50 EUR
3. Acquista un pasto (3.50 EUR), nuovo saldo: 12.00 EUR
4. NFC → Read dopo il pasto: nuovo dump

**Fase 2 - Comparazione:**
1. NFC Comparator: confronta i due dump
2. Settore 8, Blocco 0 - prima: `0x00 0x00 0x06 0x0E` = 1550 (centesimi)
3. Settore 8, Blocco 0 - dopo: `0x00 0x00 0x04 0xB0` = 1200 (centesimi)
4. Il saldo è memorizzato come integer a 16 bit in centesimi, senza alcuna protezione di integrità

**Fase 3 - Proof of Concept:**
1. Modifica il settore 8: scrivi `0x00 0x00 0x27 0x10` = 10000 = 100.00 EUR
2. Verifica alla cassa: il terminale mostra 100.00 EUR di credito
3. **NON effettuare acquisti** - documenta e ripristina il valore originale

**Report:**
- **Critico:** "Il saldo del credito prepagato è memorizzato in chiaro nel settore 8 della card MIFARE Classic 1K. La modifica è possibile con un dispositivo da 200 EUR (Flipper Zero) in meno di 10 secondi"
- **Impatto economico:** potenziale perdita finanziaria illimitata
- Raccomandazione: "Migrare a sistema server-side dove la card contiene solo un ID e il saldo è memorizzato nel database centrale. Se necessario offline, implementare MIFARE DESFire con valore autenticato tramite MAC"

---

## Scenario 6 - Assessment Trasporto Pubblico NFC

**Obiettivo:** valutare la sicurezza delle card di trasporto pubblico di una città italiana

**Contesto:** Il cliente (azienda di trasporto) vuole un assessment della sicurezza delle card contactless utilizzate per abbonamenti e biglietti. Le card sono MIFARE Classic 1K.

**Fase 1 - Analisi:**
1. Acquista una card di trasporto regolare
2. NFC → Read: SAK 0x08, MIFARE Classic 1K
3. Dictionary attack: chiavi non di default ma presenti in dizionari noti (chiave settore 1: `A0A1A2A3A4A5`)
4. Dump completo di tutti i 16 settori

**Fase 2 - Struttura dati:**
1. Settore 0: UID + dati fabbricazione
2. Settore 1: tipo abbonamento (0x01 = singolo, 0x02 = giornaliero, 0x03 = mensile, 0x04 = annuale)
3. Settore 2: data inizio validità (formato timestamp Unix)
4. Settore 3: data fine validità
5. Settore 4: contatore corse rimanenti (per biglietti a corsa)
6. Settore 5: ultimo obliteratore (ID del lettore)

**Fase 3 - Test di manipolazione:**
1. Card singola corsa con 0 corse rimanenti
2. Modifica settore 4: contatore da 0 → 10
3. Presenta al tornello → il tornello accetta la card (corse ricaricate!)
4. Modifica settore 1: tipo da 0x01 → 0x04 (singolo → annuale)
5. Modifica settore 3: data fine da passata → +1 anno
6. Presenta al tornello → accesso come abbonato annuale

**Report:**
- **Critico:** "Le card di trasporto utilizzano MIFARE Classic 1K con chiavi note. Tutti i dati (tipo abbonamento, validità, corse) sono modificabili senza controllo di integrità"
- **Impatto:** evasione tariffaria sistematica, danno economico stimato significativo
- Raccomandazione: "Implementare sistema backend con verifica server-side. Migrare a DESFire EV2 con transazioni autenticate. Implementare blacklist di UID anomali"

---

## Scenario 7 - Red Team: Accesso Datacenter con Badge Clonato

**Obiettivo:** ottenere accesso fisico al datacenter target durante un red team engagement

**Contesto:** Il datacenter ha 3 livelli di sicurezza: reception con guardia, corridoio con lettore badge NFC, sala server con lettore badge + PIN. Target: raggiungere la sala server.

**Fase 1 - Raccolta badge (giorni 1-3):**
1. OSINT: identifica dipendenti del datacenter via LinkedIn
2. Physical recon: osserva l'ingresso durante gli orari di cambio turno
3. Day 2: posizionati nell'area fumatori adiacente. I tecnici escono con il badge al collo
4. Flipper in tasca con NFC → Read attivo → lettura "drive-by" quando un tecnico passa a <5cm
5. Risultato: SAK 0x08, MIFARE Classic 1K → dictionary attack in real-time → dump parziale (solo settori con chiavi di default)

**Fase 2 - Completamento dump:**
1. Le chiavi non-default richiedono MFKey32
2. Entra nell'atrio (accessibile senza badge fino alla reception)
3. Detect Reader sul lettore della porta interna (mentre il guardiano è distratto)
4. 3 presentazioni → cattura nonce
5. MFKey32 → chiavi recuperate
6. Ritorna al tecnico nell'area fumatori → secondo Read → dump completo

**Fase 3 - Clonazione e accesso:**
1. Magic Card Gen4 → scrivi dump
2. Testa alla porta del corridoio → aperta!
3. Seconda porta (sala server): badge + PIN → il badge funziona ma il PIN è sconosciuto
4. Osserva un tecnico che digita il PIN (shoulder surfing): 4 cifre → annotato
5. Combina badge clonato + PIN → accesso alla sala server ottenuto

**Report:**
- **Critico:** "Il badge di accesso al datacenter utilizza MIFARE Classic 1K vulnerabile a clonazione. L'intero processo di clonazione richiede meno di 60 secondi di prossimità fisica"
- **Alto:** "Il PIN di accesso alla sala server è un codice a 4 cifre condiviso tra tutti i tecnici, non individuale"
- Raccomandazione: "Badge DESFire EV3 + PIN individuale + logging centralizzato + telecamera al lettore + anti-tailgating"

---

## Matrice Scenari - Quick Reference

| Scenario | Target | Tecnica | Complessità | Impatto |
|----------|--------|---------|-------------|---------|
| Badge aziendale | MIFARE Classic | Dict + MFKey32 + Clone | Media | Critico |
| Card hotel | MIFARE Classic/UL | Dict + Data modification | Bassa | Alto |
| Relay attack | Qualsiasi NFC | Relay real-time | Alta | Critico |
| Multi-piano | MIFARE 4K | Bitmask privilege escalation | Media | Critico |
| Mensa/credito | MIFARE Classic | Value tampering | Bassa | Alto |
| Trasporto pubblico | MIFARE Classic | Data manipulation | Bassa | Alto |
| Datacenter red team | MIFARE Classic | Drive-by read + MFKey32 | Alta | Critico |

---

## Cross-Reference - Scenari Multi-Vettore

| Scenario | Modulo Correlato | Link | Come si collegano |
|----------|-----------------|------|-------------------|
| Badge aziendale + RFID | RFID | [05-Scenari-Reali](../RFID/05-Scenari-Reali.md) | Molti edifici usano NFC per aree riservate + RFID 125kHz per accesso base. Testa entrambi. |
| Badge + BadUSB | USB/Bad USB | [05-Scenari-Reali](../USB/Bad%20USB/05-Scenari-Reali.md) | Dopo aver clonato il badge e ottenuto accesso fisico, drop BadUSB su workstation |
| Badge + Sub-GHz | Sub-GHz | [05-Scenari-Reali](../Sub-GHz/05-Scenari-Reali.md) | Accesso NFC all'edificio + Sub-GHz per garage/cancello perimetrale |
| Card hotel + IR | Infrared | [05-Scenari-Reali](../Infrared/05-Scenari-Reali.md) | Card hotel per accesso stanza + IR per controllare TV/AC (social engineering) |
| Datacenter + WiFi | WiFi-Marauder | [05-Scenari-Reali](../WiFi-Marauder/05-Scenari-Reali.md) | Accesso fisico al datacenter via badge → ricognizione WiFi interna con ESP32 |
| Badge + BLE | Bluetooth | [05-Scenari-Reali](../Bluetooth/05-Scenari-Reali.md) | Analisi BLE dei lettori NFC per trovare interfacce di management esposte |
