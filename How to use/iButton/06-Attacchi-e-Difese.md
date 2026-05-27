## Attacchi e Contromisure

### Vettori di Attacco

**1. Clonazione Diretta**

L'attacco più semplice e più comune:

- **Requisiti:** Accesso fisico alla chiave per 2-3 secondi
- **Strumenti:** Flipper Zero, o qualsiasi duplicatore iButton (~20-30 euro)
- **Complessità:** Nessuna - chiunque può farlo
- **Tasso di successo:** ~99% per DS1990A
- **Contromisura:** Nessuna efficace a livello di protocollo - il DS1990A trasmette in chiaro per design

**Scenari di clonazione:**
- Chiave lasciata incustodita (scrivania, portachiavi appoggiato)
- Chiave prestata brevemente ("me la presti un secondo per aprire?")
- Chiave rubata, clonata e restituita senza che il proprietario se ne accorga
- Ferramenta/duplicatore che conserva i codici di tutte le chiavi duplicate

**2. Replay Attack**

Tecnicamente, ogni emulazione iButton è un replay attack:

- Il Flipper legge il ROM code dalla chiave originale
- Lo riproduce identico sul lettore
- Non esiste challenge-response, quindi il replay funziona sempre
- Non c'è timestamp, nonce o contatore - il codice è statico e permanente

**3. Bruteforce / Fuzzing**

Attacco senza accesso alla chiave originale:

**Su Cyfral (8 bit):**
- 256 combinazioni
- ~2-4 minuti con fuzzer automatico
- Tasso di successo: ~100% (tutte le combinazioni vengono testate)
- È l'equivalente di provare tutte le combinazioni di un lucchetto a 3 cifre

**Su Metakom (32 bit):**
- ~4.29 miliardi di combinazioni
- Bruteforce completo impraticabile (~45 anni)
- Fuzzing mirato con informazioni parziali: ore-giorni
- Tasso di successo: dipende dalla qualità delle informazioni preliminari

**Su Dallas (48 bit serial effettivi):**
- ~281 trilioni di combinazioni
- Bruteforce completo assolutamente impossibile (~1.78 milioni di anni)
- Fuzzing mirato: possibile solo con informazioni molto specifiche (es. range di seriali noto)
- Strategia: se conosci una chiave del condominio, prova seriali adiacenti

**4. Key Database Extraction**

Attacco al lettore/centralina anzichè alla chiave:

- Alcuni lettori iButton economici memorizzano il database dei codici autorizzati in una EEPROM non protetta
- Con accesso fisico al lettore (svitando il pannello), si può leggere l'EEPROM con un programmatore
- Il database contiene tutti i ROM code autorizzati in chiaro
- Una volta estratto il database, puoi creare cloni di tutte le chiavi del condominio

**Contromisure:**
- Lettori con EEPROM protetta da password (raro nei modelli economici)
- Lettori con memoria interna non estraibile
- Sigilli anti-manomissione sul pannello del lettore
- Telecamere di sorveglianza sull'area del lettore

**5. Intercettazione sulla Linea**

Attacco man-in-the-middle sul bus 1-Wire:

- Il bus 1-Wire tra il lettore e l'iButton è accessibile fisicamente
- Un tap sul filo (DQ e GND) permette di sniffare tutte le comunicazioni
- Ogni volta che un condomino usa la chiave, il ROM code viene trasmesso in chiaro
- Con un microcontrollore nascosto vicino al lettore, puoi registrare passivamente tutti i codici

**Implementazione pratica:**
- Un Arduino/ESP32 con due fili collegati alla sonda del lettore
- Il microcontrollore ascolta passivamente il bus 1-Wire
- Registra ogni ROM code che transita
- In poche settimane hai raccolto i codici di tutti i condomini

**Contromisure:**
- Ispezione periodica dei cavi del lettore
- Sigilli anti-manomissione sulla sonda
- Monitoraggio del segnale elettrico sulla linea (anomalie = possibile tap)

### Contromisure Efficaci

**Livello 1 - Mitigazione (costo basso):**
- Telecamere visibili sugli ingressi (deterrente)
- Audit periodico delle chiavi in circolazione
- Procedura di revoca chiavi per ex-condomini
- Illuminazione adeguata nell'area del lettore
- Sigilli anti-manomissione sui pannelli dei lettori

**Livello 2 - Miglioramento (costo medio):**
- Migrazione a sistema NFC con MIFARE DESFire (crittografia AES)
- Sistema con challenge-response (la chiave non trasmette mai l'ID in chiaro)
- Access log con timestamp (chi ha aperto, quando)
- Lettore con rate limiting e lockout anti-bruteforce

**Livello 3 - Protezione avanzata (costo alto):**
- Autenticazione multi-fattore (chiave/card + PIN)
- Videocitofono IP con riconoscimento facciale
- Sistema di accesso centralizzato con gestione remota
- Integrazione con sistema di allarme condominiale
- Card virtualizzate su smartphone (eliminazione supporto fisico)

> **Nota personale:** La realtà è che la maggior parte dei condomini italiani con iButton non adotterà mai contromisure di Livello 2 o 3 - il costo è troppo alto e la percezione del rischio è troppo bassa. Il mio approccio pragmatico nel report è sempre suggerire le contromisure di Livello 1 come priorità immediata (telecamere, revoca chiavi) perchè sono economiche e hanno un impatto reale sul rischio. La migrazione tecnologica la suggerisco come piano a medio-lungo termine, da attuare quando il sistema attuale necessita di manutenzione o sostituzione per obsolescenza.

---

