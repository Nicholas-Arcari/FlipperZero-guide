# Scenari Reali di Penetration Testing - Sub-GHz

Scenari operativi dettagliati per l'utilizzo del modulo Sub-GHz in contesti di penetration testing fisico, red teaming e security assessment. Ogni scenario è basato su esperienze reali e include procedura completa, finding atteso e raccomandazioni.

---

## Scenario 1 - Physical Pentest: Bypass Cancello Edificio

**Obiettivo:** dimostrare che il cancello RF dell'edificio target è vulnerabile

**Fase 1 - Ricognizione:**
1. Dal parcheggio, attiva il Frequency Analyzer
2. Attendi che un dipendente usi il telecomando del cancello
3. Annota la frequenza (probabilmente 433.92 o 868.35 MHz)

**Fase 2 - Cattura:**
1. Posizionati entro 10 metri dal cancello
2. Apri Sub-GHz → Read sulla frequenza identificata
3. Attendi che un dipendente prema il telecomando
4. Se decodifica (es. "Nice FLO 12-bit"): codice fisso → salva e sei a posto
5. Se decodifica come rolling code: annota il protocollo per il report
6. Se non decodifica: usa Read RAW per cattura grezza

**Fase 3 - Test:**
1. Con codice fisso: Sub-GHz → Saved → Send → il cancello si apre
2. Con rolling code: documenta la cattura e analizza con Rolling Flaws
3. In entrambi i casi: documenta con foto, timestamp e frequenza

**Fase 4 - Report:**
- Finding: "Il sistema di apertura cancello utilizza protocollo [X] a codice fisso/rolling sulla frequenza [Y] MHz"
- Impatto: "Un attaccante con un ricevitore RF economico può catturare e riprodurre il segnale di apertura"
- Raccomandazione: "Migrare a un sistema rolling code con crittografia AES o utilizzare un sistema di accesso basato su NFC/RFID con crittografia"

---

## Scenario 2 - Analisi Sistema di Allarme Wireless

**Obiettivo:** valutare la sicurezza di un sistema di allarme che usa sensori wireless

**Procedura:**
1. Radio Scanner per identificare le frequenze dei sensori
2. Sub-GHz → Read per decodificare i segnali dei sensori (apertura porta, movimento, ecc.)
3. Analizzare se i sensori usano codice fisso o rolling
4. Se codice fisso: replay attack per generare falsi allarmi o, peggio, inviare segnali "tutto OK" per mascherare un'intrusione
5. Spectrum Analyzer per valutare la possibilità di jamming sulla frequenza dei sensori

**Implicazioni:**
- Molti allarmi economici usano sensori a codice fisso su 433 MHz
- Un attaccante può jammer la frequenza (il sistema non riceve allarmi)
- Oppure può replay il segnale "zona OK" per disattivare un sensore specifico
- Sistemi migliori hanno anti-jamming (rilevano l'assenza di heartbeat dal sensore) e rolling code

---

## Scenario 3 - OSINT con TPMS e Pager

**Obiettivo:** raccogliere intelligence passiva su un target

**TPMS:**
1. TPMS Reader in prossimità del parcheggio target
2. Raccogli ID dei sensori TPMS per 24 ore
3. Correla gli ID con i veicoli osservati
4. Monitora entrate/uscite per costruire un profilo di orari

**Pager:**
1. POCSAG Decoder sulla frequenza locale
2. Monitora i messaggi per identificare pattern, nomi, informazioni operative
3. Questo rivela comunicazioni interne dell'organizzazione trasmesse in chiaro

---

## Scenario 4 - Red Team: Bypass Barriera Parcheggio Aziendale

**Obiettivo:** ottenere accesso fisico al parcheggio sotterraneo di un target corporate durante un red team engagement

**Contesto:** L'edificio target ha una barriera automatica all'ingresso del parcheggio. I dipendenti usano telecomandi RF per accedere. L'obiettivo è entrare con un veicolo senza credenziali valide.

**Fase 1 - Ricognizione passiva (giorno 1):**
1. Parcheggia in zona pubblica con visuale sulla barriera
2. Apri Frequency Analyzer sul Flipper
3. Osserva gli orari di punta (8:00-9:30, 17:30-19:00)
4. Annota la frequenza: in questo caso 868.35 MHz → probabilmente FAAC o sistema industriale
5. Annota il timing: quanto tempo resta aperta la barriera dopo l'attivazione (~8 secondi)

**Fase 2 - Cattura (giorno 2, mattina presto):**
1. Posizionati nel parcheggio pubblico adiacente, a ~5 metri dalla barriera
2. Sub-GHz → Read su 868.35 MHz, modulazione FM (FSK)
3. Primo dipendente arriva alle 7:45: il Flipper decodifica "FAAC SLH" → rolling code
4. Secondo dipendente: stessa decodifica, contatore incrementato di 1
5. Conclusione: sistema rolling code FAAC → replay diretto non fattibile

**Fase 3 - Approccio alternativo:**
1. Osservi che la barriera ha anche un lettore badge RFID sul lato → pivot su analisi RFID
2. Read RAW cattura comunque il segnale rolling per documentazione
3. Rolling Flaws: analisi dei due codici catturati → finestra di resync ampia (>256 codici)
4. Documenta la finestra di resync come finding secondario

**Fase 4 - Tailgating assistito:**
1. All'orario di punta, un membro del team segue un'auto autorizzata
2. La barriera resta aperta 8 secondi - sufficiente per un secondo veicolo
3. Accesso ottenuto - documenta come finding di sicurezza fisica

**Report finding:**
- **Primario:** "Il sistema di barriera utilizza FAAC SLH rolling code su 868.35 MHz. L'implementazione rolling code è corretta ma la finestra di resync accetta codici con gap >256, potenzialmente vulnerabile a resync attack"
- **Secondario:** "Il tempo di apertura della barriera (8s) permette il tailgating veicolare. Raccomandazione: ridurre a 4-5 secondi e installare sensori anti-tailgating a loop induttivo"
- **CVSS:** 5.3 (Physical Access, Low Complexity)

---

## Scenario 5 - Assessment IoT: Sensori Wireless in Ambiente Industriale

**Obiettivo:** valutare la sicurezza dei sensori wireless installati in un impianto di produzione

**Contesto:** Un'azienda manifatturiera usa sensori wireless su 433/868 MHz per monitorare temperatura, umidità e stato delle macchine. L'assessment deve verificare se un attaccante può manipolare i dati dei sensori.

**Fase 1 - Mappatura RF dell'impianto:**
1. Radio Scanner: scansione completa 300-928 MHz camminando nell'impianto
2. Identificati 23 segnali attivi:
   - 15 su 433.92 MHz (sensori temperatura/umidità)
   - 5 su 868.35 MHz (sensori stato macchine)
   - 3 su 315 MHz (telecomandi portoni carico/scarico)
3. Spectrum Analyzer: nessuna evidenza di frequency hopping → canale fisso

**Fase 2 - Decodifica sensori:**
1. Sub-GHz → Read su 433.92 MHz: Weather Station decoder identifica sensori Oregon Scientific v3.0
2. Ogni sensore trasmette ogni 45 secondi: ID, temperatura, umidità, batteria
3. Nessuna autenticazione: protocollo in chiaro, codice fisso per ogni sensore
4. Sub-GHz → Read su 868.35 MHz: protocollo non riconosciuto → Read RAW

**Fase 3 - Proof of Concept:**
1. Cattura il segnale di un sensore temperatura con Read
2. Modifica il valore temperatura nel file .sub (da 22°C a 85°C)
3. Replay del segnale modificato → il sistema centralizzato mostra temperatura anomala
4. Se il sistema ha soglie di allarme: si attiva l'allarme temperatura → potenziale arresto della linea produttiva

**Fase 4 - Analisi portoni carico/scarico:**
1. Sub-GHz → Read su 315 MHz: "Linear 10-bit" → codice fisso
2. Bruteforcer: 1024 combinazioni in ~5 minuti
3. Trovato il codice valido al tentativo #387
4. Replay: il portone si apre → accesso fisico all'area carico/scarico

**Report finding:**
- **Critico:** "I sensori ambientali (Oregon Scientific v3.0, 433.92 MHz) trasmettono in chiaro senza autenticazione. Un attaccante può iniettare dati falsi causando falsi allarmi o mascherando condizioni pericolose reali"
- **Alto:** "I portoni carico/scarico usano telecomandi Linear a 10 bit (1024 combinazioni). Il codice può essere scoperto via bruteforce in meno di 5 minuti"
- **Raccomandazione sensori:** "Migrare a sensori con protocollo autenticato (LoRaWAN con encryption AES-128) o cablare i sensori critici"
- **Raccomandazione portoni:** "Sostituire con sistema rolling code o controllo accessi RFID"

---

## Scenario 6 - Pentest Residenziale: Analisi Completa Domotica

**Obiettivo:** security assessment completo di un'abitazione smart con automazione RF

**Contesto:** Il cliente ha un'abitazione con cancello automatico, tapparelle motorizzate Somfy, garage automatico, allarme wireless e stazione meteo. Vuole sapere quanto è vulnerabile il tutto.

**Fase 1 - Inventory RF:**
1. Radio Scanner dall'interno dell'abitazione: mappatura completa delle frequenze attive
2. Risultati:
   - 433.92 MHz: cancello (Nice FLOR), sensori allarme (5 zone), stazione meteo
   - 433.42 MHz: tapparelle Somfy RTS
   - 868.35 MHz: garage (FAAC SLH), 2 sensori allarme addizionali
3. Protocols Visualizer: analisi struttura segnali catturati

**Fase 2 - Test cancello (Nice FLOR):**
1. Sub-GHz → Read: "Nice FLOR" → rolling code KeeLoq
2. Rolling Flaws: analisi di 3 codici consecutivi → contatore con incremento fisso di 1
3. Finestra di resync: il ricevitore accetta codici con gap fino a ~500
4. Finding: rolling code implementato correttamente, ma finestra di resync ampia
5. Tentativo RollJam (con autorizzazione): jammer su 433.92 + cattura su frequenza adiacente → non praticabile con solo Flipper (serve jammer dedicato)

**Fase 3 - Test tapparelle Somfy RTS:**
1. Sub-GHz → Read su 433.42 MHz: "Somfy RTS" decodificato
2. Somfy usa un rolling code proprietario a 56 bit
3. Il protocollo Somfy è noto per avere una vulnerabilità: il comando "PROG" permette di accoppiare nuovi telecomandi
4. Cattura un comando normale → analisi della struttura
5. Finding: se un attaccante riesce a inviare un comando PROG (catturabile con Read RAW), può accoppiare un nuovo telecomando e controllare tutte le tapparelle

**Fase 4 - Test allarme:**
1. Sub-GHz → Read: sensori 433 MHz decodificati come protocollo proprietario a codice fisso
2. Cattura segnale "zona OK" del sensore porta → replay → la centralina accetta il segnale
3. Cattura segnale "allarme" → replay → falso allarme generato
4. Test jamming: Spectrum Analyzer conferma che un jammer su 433 MHz impedirebbe la ricezione dei segnali dei sensori
5. La centralina NON rileva l'assenza di heartbeat → vulnerabile a jamming silenzioso

**Report complessivo:**
- Cancello: rischio medio (rolling code presente ma finestra ampia)
- Tapparelle: rischio alto (vulnerabilità PROG nota in Somfy RTS)
- Allarme: rischio critico (codice fisso, nessun anti-jamming, nessun heartbeat monitoring)
- Stazione meteo: rischio informativo (dati in chiaro, nessun impatto sulla sicurezza)
- Raccomandazione prioritaria: sostituire l'allarme con sistema cablato o wireless con rolling code + anti-jamming + heartbeat monitoring

---

## Scenario 7 - Red Team: Accesso Edificio Multi-Tenant

**Obiettivo:** ottenere accesso fisico a un ufficio in un edificio condiviso da più aziende

**Contesto:** L'edificio ha un cancello carrabile condiviso (tutti i tenant usano lo stesso sistema), portone pedonale con citofono, e ogni piano ha la propria serratura. Il target è al 3° piano.

**Fase 1 - Ricognizione RF (giorno 1-2):**
1. Frequency Analyzer dal marciapiede: 433.92 MHz attivo frequentemente (ogni 5-10 minuti durante orario lavorativo)
2. Sub-GHz → Read: "Came 12-bit" → codice fisso!
3. Cattura 3 segnali diversi da 3 dipendenti di tenant diversi → tutti hanno lo stesso codice base con varianti minime (il sistema usa codici a 12 bit assegnati sequenzialmente)

**Fase 2 - Analisi codici:**
1. Codice tenant A: 0xA3B
2. Codice tenant B: 0xA3C  
3. Codice tenant C: 0xA3E
4. Pattern evidente: codici assegnati in sequenza → bruteforce mirato su range 0xA30-0xA4F (32 codici) trova tutti i codici validi in secondi

**Fase 3 - Accesso:**
1. Replay del codice catturato → cancello carrabile si apre
2. Accesso all'atrio → portone pedonale con chiudiporta elettrico (attivato dallo stesso segnale 433 MHz!)
3. Ascensore: libero accesso a tutti i piani → raggiunto il 3° piano
4. La porta dell'ufficio target ha un lettore badge RFID → pivot su analisi NFC/RFID

**Finding chiave:**
- "L'intero sistema di accesso perimetrale dell'edificio (cancello carrabile + portone pedonale) si basa su telecomandi Came a 12 bit con codice fisso. Un attaccante con un ricevitore RF da 10 euro può catturare e replicare qualsiasi codice di accesso in meno di 5 secondi"
- "I codici sono assegnati sequenzialmente, permettendo a chiunque conosca un codice di enumerare gli altri per bruteforce"
- Impatto: accesso fisico all'intero edificio per qualsiasi attaccante con minima competenza RF

---

## Scenario 8 - Incident Response: Sospetto Clonazione Telecomando

**Obiettivo:** indagare su un sospetto accesso non autorizzato tramite telecomando clonato

**Contesto:** Un'azienda segnala che il cancello del parcheggio si apre in orari notturni senza che nessun dipendente sia presente. La security camera mostra un veicolo non identificato che entra. L'azienda sospetta clonazione del telecomando.

**Fase 1 - Analisi del sistema:**
1. Identificazione: sistema Nice FLO a 12 bit su 433.92 MHz → codice fisso
2. Conferma: il sistema è vulnerabile a replay attack
3. Sub-GHz → Read: cattura segnale del telecomando aziendale → decodifica immediata

**Fase 2 - Simulazione attacco:**
1. Da 10 metri di distanza, Read cattura il codice in 1 pressione
2. Replay: il cancello si apre
3. Conclusione: un attaccante avrebbe potuto catturare il codice in qualsiasi momento

**Fase 3 - Raccomandazioni per incident response:**
1. Sostituire immediatamente tutti i telecomandi con sistema rolling code (Nice FLOR/Smilo)
2. Riprogrammare il ricevitore cancello
3. Invalidare tutti i vecchi codici
4. Installare telecamera aggiuntiva con lettura targa
5. Considerare barriera fisica aggiuntiva (pilomat)
6. Log di accesso: se il sistema lo supporta, abilitare il logging di ogni apertura con timestamp

**Report IR:**
- "L'accesso non autorizzato è stato possibile grazie all'utilizzo di un sistema a codice fisso (Nice FLO 12-bit) che permette la clonazione istantanea del telecomando tramite cattura RF passiva"
- "L'attaccante ha probabilmente catturato il segnale da un dipendente durante le ore lavorative e lo ha riprodotto in orario notturno"
- Timeline stimata dell'attacco e raccomandazioni di mitigazione

---

## Matrice Scenari - Quick Reference

| Scenario | Target | Tecnica Principale | Complessità | Impatto |
|----------|--------|-------------------|-------------|---------|
| Bypass cancello | Cancello RF | Replay codice fisso | Bassa | Alto |
| Allarme wireless | Sistema allarme | Replay + Jamming | Media | Critico |
| OSINT TPMS/Pager | Veicoli/Comunicazioni | Ricezione passiva | Bassa | Medio |
| Barriera aziendale | Parcheggio corporate | Rolling code analysis | Media-Alta | Alto |
| IoT industriale | Sensori + portoni | Replay + Bruteforce | Media | Critico |
| Domotica residenziale | Casa smart | Multi-protocollo | Alta | Alto |
| Multi-tenant | Edificio condiviso | Replay + Enumerazione | Bassa | Critico |
| Incident Response | Post-incidente | Analisi forense RF | Media | N/A |

---

## Cross-Reference - Scenari Multi-Vettore

Molti engagement reali combinano più moduli. Ecco i link agli scenari correlati in altri moduli:

| Scenario | Modulo Correlato | Link | Come si collegano |
|----------|-----------------|------|-------------------|
| Bypass cancello + accesso edificio | RFID | [05-Scenari-Reali](../RFID/05-Scenari-Reali.md) | Dopo aver aperto il cancello via Sub-GHz, usa RFID per clonare badge e entrare nell'edificio |
| Allarme wireless + WiFi | WiFi-Marauder | [05-Scenari-Reali](../WiFi-Marauder/05-Scenari-Reali.md) | Jammando l'allarme RF, usa ESP32 per disabilitare anche eventuali notifiche WiFi |
| IoT industriale + Debug | GPIO/Debug | [04-Scenari-Reali](../GPIO/Debug/04-Scenari-Reali.md) | Dopo aver catturato segnali RF del sistema IoT, estrai firmware via SWD per analisi offline |
| Domotica + IR | Infrared | [05-Scenari-Reali](../Infrared/05-Scenari-Reali.md) | Sistemi domotici spesso combinano RF (tapparelle, sensori) + IR (TV, AC, luci) |
| Multi-tenant + NFC | NFC | [05-Scenari-Reali](../NFC/05-Scenari-Reali.md) | Edifici multi-tenant usano spesso Sub-GHz per garage + NFC per accesso ai piani |
| Barriera + BadUSB | USB/Bad USB | [05-Scenari-Reali](../USB/Bad%20USB/05-Scenari-Reali.md) | Accesso fisico via Sub-GHz → drop BadUSB su workstation nel parcheggio |
