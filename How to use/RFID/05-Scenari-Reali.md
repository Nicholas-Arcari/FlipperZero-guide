## Scenari di Penetration Testing

### Scenario 1: Clonazione Badge Condominio EM4100 su T5577

**Contesto:** Un condominio italiano con sistema di accesso EM4100 per portone principale, cancello carraio e locale biciclette. Il cliente (amministratore di condominio) vuole verificare se il sistema è vulnerabile alla clonazione.

**Fase 1 - Ricognizione (Giorno 1)**

1. Sopralluogo esterno: identifica i lettori visibili
   - Portone: lettore a muro tipo CAME o BPT, LED rosso/verde
   - Cancello: lettore incassato nel pilastro
   - Locale bici: lettore a vetro touch
2. Attiva il `NFC/RFID Detector` e cammina vicino ai lettori
   - Risultato: tutti e tre emettono campo LF (125 kHz) - confermato RFID LF
3. Osserva i condomini che entrano - badge tipo keyfob o card?
   - Nota: keyfob circolari blu/neri (tipico EM4100 cinese)

**Fase 2 - Acquisizione Badge (Giorno 1)**

1. Opzione A (autorizzata): il cliente fornisce un badge di test
2. Opzione B (social engineering): "Scusi, può avvicinare il badge? Devo testare il sistema per l'amministratore"
3. Lettura: `RFID 125 kHz > Read` - avvicina il badge
4. Risultato: `EM4100 - ID: 0A 00 12 34 56`
5. Salva: `Save > "portone_principale"`

**Fase 3 - Clonazione (Giorno 1)**

1. Apri il file salvato: `RFID 125 kHz > Saved > portone_principale`
2. Seleziona `Write`
3. Posiziona un T5577 keyfob vuoto sul Flipper
4. Attendi la conferma di scrittura (2-3 secondi)
5. Verifica: `Read` il T5577 - deve mostrare lo stesso ID `0A 00 12 34 56`

**Fase 4 - Test di Accesso (Giorno 2)**

1. Avvicina il T5577 clonato al lettore del portone
2. Risultato atteso: LED verde, serratura si apre
3. Testa tutti e tre i lettori - lo stesso badge dovrebbe funzionare ovunque
4. Documenta con foto e video (timestamp)

**Fase 5 - Reporting**

```
FINDING: Clonazione badge EM4100 - Rischio ALTO

Descrizione: Il sistema di controllo accessi del condominio
utilizza tag RFID EM4100 a 125 kHz senza alcuna crittografia
o autenticazione. È stato possibile leggere l'ID di un badge
autorizzato e clonarlo su un tag T5577 in meno di 10 secondi.
Il clone funziona su tutti e tre i lettori testati.

Impatto: Qualsiasi persona con un dispositivo di lettura RFID
(costo: <20 EUR) può clonare il badge di un condomino
avvicinandosi a meno di 10 cm dal badge originale.

Raccomandazione:
- Breve termine: sensibilizzare i condomini sulla protezione
  del badge (non lasciarlo in vista)
- Medio termine: migrare a un sistema NFC 13.56 MHz con
  crittografia (MIFARE DESFire EV2/EV3)
- Lungo termine: valutare sistema multi-fattore
  (badge + PIN o badge + biometrico)
```

---

### Scenario 2: Badge HID Prox Aziendale - Analisi Facility Code e Clonazione

**Contesto:** Un'azienda con 200 dipendenti utilizza badge HID Prox (125 kHz) per tutti gli accessi. Il CISO ha commissionato un physical pentest completo.

**Fase 1 - Ricognizione**

1. Osserva i badge dei dipendenti:
   - Card formato ISO con logo HID e logo aziendale
   - Keyfob HID grigi per alcuni
2. `NFC/RFID Detector` sui lettori:
   - Ingresso principale: LF
   - Scale/ascensori: LF
   - Server room: LF + HF (dual reader - forse in migrazione)
3. Nota: lettori HID iCLASS R10 (riconoscibili dal design)

**Fase 2 - Acquisizione**

1. Social engineering: badge di un visitatore (spesso ha accesso limitato ma stesso FC)
2. Lettura: `RFID 125 kHz > Read`
3. Risultato: `HID H10301 - FC:42 CN:8001`
4. Salva e analizza:
   - Facility Code 42 - probabilmente uguale per tutti i badge dell'azienda
   - Card Number 8001 - le card per i visitatori sono spesso numerate in alto (>8000)

**Fase 3 - Analisi del Facility Code**

Se hai accesso a più badge (es. badge trovato nel cestino, nella fotocopiatrice, ecc.):

```
Badge 1 (visitatore):    FC:42 CN:8001
Badge 2 (dipendente):    FC:42 CN:0156
Badge 3 (trovato):       FC:42 CN:0312

Analisi:
- FC confermato: 42 per tutta l'azienda
- CN dipendenti: range basso (1-500?)
- CN visitatori: range alto (8000+)
- Probabilmente CN assegnati sequenzialmente
```

**Fase 4 - Clonazione Mirata**

1. Crea un badge con Card Number basso (probabile dipendente):
   - `Add Manually > HID H10301 > FC:42 CN:1`
   - Scrivi su T5577
2. Testa sull'ingresso principale
3. Se non funziona, incrementa: CN:2, CN:3, ...
4. Alternativa: usa il `RFID Fuzzer` con FC:42 e CN:1-500

**Fase 5 - Escalation**

1. Una volta dentro, mappa gli accessi interni
2. La server room ha un lettore dual (LF+HF):
   - Il badge HID Prox 125 kHz potrebbe funzionare sul lato LF
   - Se non funziona, il lato HF richiede un badge NFC - diverso engagement
3. Documenta ogni porta accessibile con il badge clonato

> **Nota personale:** Il Facility Code è la chiave di volta in un pentest HID. Una volta che lo conosci, hai metà del lavoro fatto. In un engagement per una multinazionale ho scoperto che usavano FC diversi per edifici diversi (FC:10 per la sede, FC:20 per il magazzino, FC:30 per il laboratorio). Questo è un buon segno - significa che almeno c'è una segmentazione. Ma all'interno di ogni edificio, tutti i badge avevano lo stesso FC e Card Number sequenziali partendo da 1. Il primo badge del CEO era probabilmente CN:1. In assenza di crittografia, il Facility Code è l'unica forma di "sicurezza" - ed è facilmente scopribile.

---

### Scenario 3: Fuzzing di un Lettore RFID per Scoprire Vulnerabilità

**Contesto:** Test di sicurezza di un lettore RFID standalone (non collegato a un controller centrale) installato su una porta interna.

**Obiettivo:** Determinare se il lettore ha vulnerabilità di implementazione.

**Fase 1 - Identificazione**

1. `NFC/RFID Detector`: campo LF attivo - confermato 125 kHz
2. Lettura di un badge autorizzato: `EM4100 - ID: 05 00 AA BB CC`
3. Nota il Version Number: `05` - potrebbe essere significativo

**Fase 2 - Test di Base**

1. Badge clonato: funziona - il sistema accetta l'ID originale
2. Badge con ID casuale: non funziona - il sistema ha un database
3. Fin qui tutto nella norma

**Fase 3 - Fuzzing Intelligente**

Test 1: **Manipolazione del Version Number**
```
ID originale:     05:00:AA:BB:CC -> APRE
ID modificato:    05:00:AA:BB:CD -> NON APRE
ID modificato:    05:00:AA:BB:CB -> NON APRE
ID modificato:    05:01:AA:BB:CC -> APRE (!!!)
```

**Scoperta:** il lettore ignora il secondo byte! Controlla solo il Version Number (byte 0) e gli ultimi 3 byte.

Test 2: **Brute force sugli ultimi 3 byte con Version Number fisso**
- Con `RFID Fuzzer`: protocollo EM4100, byte fissi 05:00, fuzzing sui restanti 3 byte
- 2^24 = ~16 milioni di combinazioni - troppo per brute force completo
- Ma: fuzzing di 5 minuti scopre 3 ID validi oltre all'originale

Test 3: **Behavior anomalo**
```
Invio rapido di 100 ID diversi in 30 secondi:
- Il lettore smette di rispondere per 10 secondi (blocco temporaneo)
- Dopo il blocco, riprende normalmente
- Nessun allarme generato
- Nessun log (il lettore è standalone)
```

**Fase 4 - Reporting**

```
FINDING 1: Validazione parziale dell'ID - Rischio ALTO
Il lettore ignora il secondo byte dell'ID EM4100, riducendo
lo spazio di ricerca da 2^40 a 2^32.

FINDING 2: Nessun rate limiting efficace - Rischio MEDIO
Il lettore si blocca brevemente ma riprende senza
contromisure permanenti. Il brute force è fattibile.

FINDING 3: Nessun logging - Rischio ALTO
Il lettore standalone non genera log. Tentativi di
accesso non autorizzato non vengono registrati.

FINDING 4: Nessun allarme - Rischio MEDIO
Nessuna notifica dopo multipli tentativi falliti.
Un attaccante può operare senza essere rilevato.
```

---

### Scenario 4: Rilevamento Lettori Nascosti con Detector

**Contesto:** Audit di sicurezza fisica di un piano uffici. Il cliente vuole una mappa completa di tutti i punti di accesso elettronico.

**Procedura**

1. Prepara una planimetria del piano (formato A3, stampata)
2. Attiva `NFC/RFID Detector`
3. Cammina sistematicamente lungo ogni corridoio, parete, porta
4. Ad ogni rilevamento, segna sulla planimetria:
   - Posizione del lettore
   - Tipo di campo (LF / HF / dual)
   - Intensità (bassa/media/alta)
   - Visibile o nascosto

**Risultati tipici:**

```
Piano 3 - Mappatura lettori RFID

Porta    | Tipo  | Campo | Visibile | Note
---------|-------|-------|----------|-----
P01      | Ing.  | LF    | Si       | HID iCLASS R10
P02      | Uff.  | LF    | Si       | CAME
P03      | CED   | LF+HF | Si      | HID multiCLASS
P04      | Arch. | LF    | No       | Sotto intonaco! 
P05      | WC    | -     | -        | Nessun lettore
P06      | Scale | LF    | Si       | BPT
P07      | Asc.  | HF    | Si       | Solo NFC
P08      | Mag.  | LF    | No       | Dietro pannello
```

**Scoperte critiche:**
- P04 (Archivio): lettore nascosto sotto intonaco - nessuno lo sapeva. Probabilmente un'installazione precedente mai rimossa ma ancora funzionante. Il cavo di alimentazione era ancora attivo. Questo è un bypass potenziale: se il vecchio lettore è collegato alla serratura, un badge EM4100 dell'impianto precedente potrebbe ancora aprire.
- P08 (Magazzino): lettore nascosto dietro un pannello decorativo - possibile tentativo di installazione discreta, ma anche possibile punto di vulnerabilità non monitorato.

> **Nota personale:** La mappatura con il Detector è una fase che molti pentester saltano, e secondo me è un errore grave. In un caso ho trovato un lettore RFID attivo collegato alla porta della sala server che era stato "dismesso" dal responsabile IT - ma in realtà era ancora alimentato e la serratura elettrica rispondeva ancora ai vecchi badge EM4100. L'IT manager era convinto che il nuovo sistema NFC fosse l'unico attivo. Quel lettore fantasma era la vulnerabilità più grave dell'intera infrastruttura.

---


---

### Scenario 5: Assessment Parcheggio Aziendale Multipiano

**Contesto:** Un parcheggio aziendale sotterraneo con barriera automatica e lettore RFID 125 kHz. Il sistema utilizza badge EM4100 per tutti i dipendenti e badge visitatori temporanei. Il CISO vuole verificare la robustezza del sistema.

**Fase 1 - Ricognizione**

1. Detector sul lettore della barriera: campo LF confermato
2. Osserva i dipendenti: keyfob attaccati al portachiavi dell'auto
3. Nota: il lettore è un modello generico cinese senza brand visibile

**Fase 2 - Acquisizione badge visitatore**

1. Richiedi un badge visitatore alla reception (scenario legittimo per l'engagement)
2. Lettura: `EM4100 - ID: 0A 00 FF 01 00`
3. Il Version Number `0A` potrebbe essere il "lotto visitatori"

**Fase 3 - Analisi del sistema**

1. Badge visitatore → barriera: si apre (accesso consentito ai visitatori)
2. Leggi un badge dipendente (con autorizzazione): `EM4100 - ID: 05 00 12 34 56`
3. Version Number diverso: `05` per dipendenti, `0A` per visitatori
4. Il sistema probabilmente usa il Version Number per distinguere i livelli di accesso

**Fase 4 - Test privilege escalation**

1. Crea un badge: Version `05` + ID casuale → `Add Manually > EM4100 > 05:00:00:00:01`
2. Scrivi su T5577
3. Testa alla barriera: NON si apre → il sistema ha un database
4. Fuzzing mirato: `05:00:12:34:55`, `05:00:12:34:57` (vicini all'ID dipendente noto)
5. `05:00:12:34:57` → SI APRE! Card Number sequenziali confermati

**Fase 5 - Accesso ai piani**

1. Dopo la barriera, ogni piano ha un lettore separato per la porta di ingresso
2. Il badge clonato apre anche la porta del piano del dipendente → nessuna segmentazione
3. Badge visitatore (`0A:...`) non apre i piani → almeno questa separazione funziona

**Report:**
```
FINDING 1: Card Number sequenziali - Rischio ALTO
I badge dipendenti usano ID EM4100 con numerazione sequenziale.
Conoscendo un singolo ID, è possibile enumerare gli altri con
il RFID Fuzzer. Tempo stimato: <5 minuti per +-100 ID.

FINDING 2: Nessuna segmentazione per piano - Rischio MEDIO
Un badge dipendente apre tutti i piani, indipendentemente
dall'assegnazione. Non c'è least-privilege.

FINDING 3: EM4100 clonabile - Rischio ALTO
Tutti i badge sono EM4100 senza crittografia.
La clonazione richiede <10 secondi.
```

---

### Scenario 6: Palestra/Centro Sportivo - Bypass Tornello

**Contesto:** Una palestra con tornello d'ingresso controllato da badge RFID 125 kHz. L'abbonamento è associato al badge. Il titolare vuole verificare se è possibile usare badge duplicati per accessi non autorizzati.

**Fase 1 - Analisi sistema**

1. Detector sul tornello: campo LF
2. Lettura badge cliente: `EM4100 - ID: 01 00 AB CD EF`
3. Il sistema è un controller standalone con display LCD

**Fase 2 - Test clonazione**

1. Clona su T5577 → testa al tornello → si apre
2. L'LCD mostra il nome del titolare dell'abbonamento → il sistema associa l'ID al database
3. Due persone con lo stesso badge: entrambe possono entrare → nessun controllo anti-passback

**Fase 3 - Test anti-passback**

1. Entrata con badge originale → OK
2. Entrata immediata con badge clonato → OK (nessun anti-passback!)
3. Il sistema permette accessi multipli con lo stesso ID senza cooldown

**Fase 4 - Impatto economico**

1. Un cliente può clonare il suo badge e darlo a un amico
2. Entrambi possono usare la palestra con un solo abbonamento
3. Su 500 abbonati, anche il 5% di abuso = 25 abbonamenti persi

**Report:**
```
FINDING: Sistema di accesso senza anti-passback e con badge
clonabili (EM4100). Un cliente può duplicare il badge
e condividerlo. Perdita economica potenziale stimata: 5-10%
del fatturato abbonamenti.

Raccomandazione: Implementare anti-passback temporale
(minimo 30 minuti tra ingressi successivi con lo stesso ID)
e migrare a badge con crittografia.
```

> **Nota personale:** Ho fatto questo test per 3 palestre diverse. Tutte e tre usavano EM4100 senza anti-passback. In una, il titolare non aveva idea che i badge fossero clonabili. In un'altra, il problema era noto ma non l'avevano risolto perchè "costa troppo cambiare sistema". La terza ha deciso di migrare a NFC dopo il mio report. Il ROI del pentest si ripaga da solo in abbonamenti non condivisi.

---

### Scenario 7: Red Team - Building Entry tramite Badge Clonato e Tailgating

**Contesto:** Red team engagement su un edificio uffici con 4 aziende inquiline. Sistema di accesso HID Prox 125 kHz per il portone principale. Target: raggiungere l'ufficio dell'azienda X al 2° piano.

**Fase 1 - Reconnaissance esterna (giorno 1-2)**

1. Osservazione dell'ingresso: dipendenti usano badge HID (card con logo aziendale + HID)
2. Orari di punta: 8:30-9:30 ingresso, 12:30-13:30 pausa pranzo, 17:30-18:30 uscita
3. Nota: la porta ha un chiudiporta lento (~5 secondi per chiudersi)

**Fase 2 - Acquisizione (giorno 3)**

1. Area fumatori: un dipendente ha il badge al collo con laccetto
2. Avvicinamento con pretesto: "Scusi, sa dove si trova la sala riunioni dell'azienda Y?"
3. Durante la conversazione, Flipper in tasca → `RFID Read` → nessun segnale a quella distanza
4. Piano B: attendo la pausa pranzo, un dipendente lascia la giacca sulla sedia del bar
5. Il badge è nella tasca della giacca → Flipper a contatto con la tasca → `HID H10301 FC:23 CN:445`
6. Tempo totale di contatto: 2 secondi

**Fase 3 - Clonazione e accesso (giorno 3, pomeriggio)**

1. `Add Manually > HID H10301 > FC:23 CN:445` → scrivi su T5577 card
2. Test al portone principale → LED verde → accesso consentito!
3. Salgo al 2° piano → porta dell'azienda X → il badge funziona anche qui
4. All'interno: nessun controllo ulteriore fino alla sala server (badge + PIN)

**Fase 4 - Enumerazione (giorno 4)**

1. Con FC:23 confermato, provo badge con CN diversi per verificare la segmentazione
2. CN:1 → accesso consentito (probabilmente admin/reception)
3. CN:100 → accesso consentito (dipendente)
4. CN:500 → accesso consentito (range visitatori?)
5. Tutte le 4 aziende dell'edificio condividono lo STESSO Facility Code → nessuna segmentazione tra tenant!

**Report:**
```
FINDING CRITICO: Tutti gli inquilini dell'edificio condividono
lo stesso Facility Code HID (FC:23). Un dipendente di qualsiasi
azienda può accedere agli uffici di tutte le altre.

FINDING ALTO: Badge HID Prox clonabile in <10 secondi.
L'accesso fisico all'edificio richiede solo la prossimità
temporanea a un badge valido.

FINDING MEDIO: Il chiudiporta lento (5s) permette tailgating
facile durante gli orari di punta.
```

---

## Matrice Scenari - Quick Reference

| Scenario | Target | Protocollo | Tecnica | Complessità | Impatto |
|----------|--------|-----------|---------|-------------|---------|
| Condominio | EM4100 | 125 kHz LF | Clone diretto | Bassa | Alto |
| HID aziendale | HID H10301 | 125 kHz LF | FC analysis + clone | Media | Critico |
| Fuzzing lettore | EM4100/HID | 125 kHz LF | Fuzzer + comportamento | Media | Alto |
| Lettori nascosti | Vari | LF/HF | Detector mapping | Bassa | Variabile |
| Parcheggio | EM4100 | 125 kHz LF | Enumerazione sequenziale | Media | Alto |
| Palestra | EM4100 | 125 kHz LF | Clone + anti-passback test | Bassa | Medio |
| Red team building | HID H10301 | 125 kHz LF | Social eng + clone | Alta | Critico |

---

## Cross-Reference - Scenari Multi-Vettore

| Scenario | Modulo Correlato | Link | Come si collegano |
|----------|-----------------|------|-------------------|
| Badge RFID + NFC | NFC | [05-Scenari-Reali](../NFC/05-Scenari-Reali.md) | Edifici dual-tech: RFID per ingresso base, NFC per aree riservate |
| Badge + Sub-GHz | Sub-GHz | [05-Scenari-Reali](../Sub-GHz/05-Scenari-Reali.md) | Clone badge RFID per edificio + replay Sub-GHz per cancello perimetrale |
| Badge + iButton | iButton | [05-Scenari-Reali](../iButton/05-Scenari-Reali.md) | Condomini: RFID per portone + iButton per citofono/ascensore |
| Red team + BadUSB | USB/Bad USB | [05-Scenari-Reali](../USB/Bad%20USB/05-Scenari-Reali.md) | Dopo accesso fisico con badge clonato → deploy payload BadUSB |
| Red team + WiFi | WiFi-Marauder | [05-Scenari-Reali](../WiFi-Marauder/05-Scenari-Reali.md) | Accesso fisico → evil portal WiFi per credential harvest interno |
| Parcheggio + Debug | GPIO/Debug | [04-Scenari-Reali](../GPIO/Debug/04-Scenari-Reali.md) | Dopo aver clonato badge parcheggio, estrai firmware dal lettore per analisi |
