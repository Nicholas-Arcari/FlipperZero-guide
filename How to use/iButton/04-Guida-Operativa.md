## Tool per Tool - Guida Operativa

### iButton - Hub Principale (Read / Emulate / Write)

L'hub iButton del Flipper Zero è il punto di partenza per tutte le operazioni sulle chiavi a contatto. Dal menu principale del Flipper:

**Navigazione:** Menu → iButton

**Opzioni disponibili:**

- **Read** - Lettura di chiavi iButton
- **Saved** - Gestione chiavi salvate
- **Add Manually** - Creazione manuale di una chiave

#### Read - Lettura Chiavi

Procedura operativa completa:

**1. Preparazione:**
- Assicurati che il pad iButton sul dorso del Flipper sia pulito
- Assicurati che la chiave da leggere sia pulita (no ossidazione, no sporcizia)
- Apri Menu → iButton → Read

**2. Posizionamento:**
- Capovolgi il Flipper (schermo verso il basso)
- Appoggia la chiave iButton centrata sul pad metallico del dorso
- Premi con decisione - serve contatto metallo-su-metallo
- Mantieni la pressione

**3. Lettura:**
- Il Flipper tenta automaticamente tutti i protocolli supportati (Dallas, Cyfral, Metakom)
- In caso di successo, lo schermo mostra:
  - Protocollo rilevato (DS1990, Cyfral, Metakom)
  - ID della chiave (in esadecimale)
  - Per Dallas: family code + serial + CRC
- Se la lettura fallisce: "Not Found" - riposiziona la chiave e riprova

**4. Salvataggio:**
- Dopo la lettura, premi il pulsante destro per salvare
- Assegna un nome descrittivo (es. "Citofono_Casa", "Ufficio_Piano2")
- Il file viene salvato in `/ext/ibutton/` con estensione `.ibtn`

**5. Formato file .ibtn:**

Il file salvato è un file di testo con questa struttura:

```
Filetype: Flipper iButton key
Version: 1
# Key type can be Dallas, Cyfral, Metakom
Protocol: Dallas
Rom Data: 01 A3 5F 2B 00 00 00 E7
```

Per Cyfral:
```
Filetype: Flipper iButton key
Version: 1
Protocol: Cyfral
Key Data: AB CD
```

Per Metakom:
```
Filetype: Flipper iButton key
Version: 1
Protocol: Metakom
Key Data: AB CD EF 01
```

> **Nota personale:** Il mio workflow standard durante un audit è leggere la chiave, salvarla con un nome che include la data e il luogo (es. "2024-03-15_Condominio_ViaRoma_12"), e poi immediatamente emulare per verificare che la lettura sia corretta. Se l'emulazione funziona sul lettore, la lettura è valida. Se non funziona, il problema è quasi sempre un contatto sporco durante la lettura - pulisci e rileggi.

#### Emulate - Emulazione Chiavi

L'emulazione trasforma il Flipper Zero in una chiave iButton virtuale - il pad sul dorso del Flipper trasmette il ROM code salvato quando viene appoggiato su un lettore.

**Procedura operativa:**

**1. Selezione chiave:**
- Menu → iButton → Saved → seleziona la chiave da emulare
- Oppure: dopo una lettura, seleziona "Emulate" direttamente

**2. Attivazione emulazione:**
- Lo schermo mostra "Emulating" con il nome della chiave e il protocollo
- Il Flipper è ora in modalità slave - attende un reset pulse dal lettore

**3. Posizionamento sul lettore:**
- Capovolgi il Flipper (schermo verso il basso)
- Appoggia il pad iButton del Flipper sulla sonda del lettore
- Premi con decisione per fare contatto
- Il lettore invia il reset pulse, il Flipper risponde con presence e ROM code
- Se il codice è nel database del lettore: azione (apertura, sblocco)

**4. Timing:**
- L'emulazione è attiva finchè lo schermo mostra "Emulating"
- Devi mantenere il contatto per almeno 1-2 secondi
- Alcuni lettori richiedono 3-5 secondi di contatto continuo
- Se il lettore non risponde: riposiziona, pulisci le superfici, riprova

**Note sull'emulazione:**

- L'emulazione funziona per tutti e tre i protocolli (Dallas, Cyfral, Metakom)
- Il Flipper genera automaticamente il segnale corretto in base al protocollo del file
- L'emulazione è molto affidabile per Dallas - tasso di successo ~95%
- Per Cyfral e Metakom il tasso di successo è leggermente inferiore (~85-90%) perchè alcuni lettori sono sensibili a variazioni di impedenza
- L'emulazione consuma batteria - il pad iButton deve essere alimentato

> **Nota personale:** L'emulazione iButton è la più affidabile tra tutte le emulazioni del Flipper - molto più dell'emulazione NFC, che ha problemi di campo e timing. Il contatto fisico diretto elimina i problemi di distanza e accoppiamento che affliggono le emulazioni RF. Se la chiave è stata letta correttamente e il lettore funziona, l'emulazione funziona sempre. L'unico problema è il contatto fisico - devi centrare bene il pad del Flipper sulla sonda del lettore.

#### Write - Scrittura su Tag Scrivibili

La funzione Write programma tag scrivibili (RW1990) con il ROM code di una chiave salvata.

**Procedura operativa:**

**1. Prerequisiti:**
- Devi avere una chiave salvata (lettura precedente o creazione manuale)
- Devi avere un tag scrivibile:
  - **RW1990** per chiavi Dallas
  - Non esiste un equivalente scrivibile per Cyfral/Metakom - per quei protocolli, l'emulazione è l'unica opzione di "copia"

**2. Procedura:**
- Menu → iButton → Saved → seleziona la chiave → Write
- Lo schermo mostra "Writing..."
- Appoggia il tag RW1990 sul pad iButton del Flipper
- Mantieni il contatto per 3-5 secondi
- Il Flipper programma il ROM code
- Messaggio di conferma "Written!" se la scrittura ha successo

**3. Verifica:**
- Dopo la scrittura, leggi il tag programmato (Read) per verificare
- Confronta il ROM code letto con quello originale - devono essere identici
- Testa il tag sul lettore target per conferma operativa

**4. Problemi comuni nella scrittura:**
- **"Write Failed":** contatto insufficiente, tag non scrivibile (DS1990A originale), tag bloccato
- **ROM code diverso dopo scrittura:** tag difettoso o di bassa qualità
- **Il tag scritto non funziona sul lettore:** possibile errore nel CRC - riscrivere

> **Nota personale:** La scrittura su RW1990 dal Flipper è meno affidabile della lettura - circa 1 volta su 10 devo ripetere la procedura. Il trucco è mantenere il contatto molto stabile per tutta la durata della scrittura, senza muovere la chiave sul pad. Se hai tag RW1990 economici (quelli da 0.30 euro su AliExpress), aspettati un 5-10% di tag difettosi che non si programmano - buttali e usa il prossimo.

#### Add Manually - Creazione Manuale

Puoi creare una chiave iButton da zero inserendo manualmente l'ID:

**Procedura:**
- Menu → iButton → Add Manually
- Seleziona il protocollo (Dallas, Cyfral, Metakom)
- Inserisci il codice byte per byte usando l'interfaccia del Flipper
- Salva con un nome descrittivo

**Casi d'uso:**
- Hai l'ID della chiave scritto su un adesivo (alcuni installatori lo fanno)
- Hai ottenuto il codice da un database o da un dump di sistema
- Vuoi creare una chiave con un ID specifico per test
- Stai preparando un set di chiavi per il fuzzing

### iButton Converter - Conversione tra Protocolli

L'iButton Converter è uno strumento per la conversione di chiavi tra formati diversi. È utile quando un sistema accetta un protocollo specifico ma hai la chiave in un altro formato.

**Conversioni disponibili:**

- **Cyfral → Dallas:** converte un codice Cyfral in un formato DS1990A emulabile
- **Dallas → Cyfral:** converte un codice Dallas in formato Cyfral
- **Metakom → Dallas:** converte un codice Metakom in formato Dallas
- **Dallas → Metakom:** converte un codice Dallas in formato Metakom
- **Cyfral ↔ Metakom:** conversioni incrociate

**Come funziona la conversione:**

La conversione non è una traduzione diretta 1:1 - i protocolli hanno formati e lunghezze di codice diversi. Il converter:

1. Prende il codice sorgente
2. Lo mappa nel formato del protocollo di destinazione
3. Calcola eventuali checksum/CRC necessari
4. Genera un file `.ibtn` valido per il protocollo di destinazione

**Quando serve la conversione:**

- Un citofono ha un lettore Dallas ma le chiavi distribuite sono Cyfral (succede con installazioni fatte da aziende miste)
- Stai testando la compatibilità di un lettore con protocolli diversi
- Vuoi verificare se un lettore multi-protocollo risponde a tutti i formati pubblicizzati

**Procedura operativa:**

1. Leggi la chiave sorgente (o seleziona un file salvato)
2. Apri iButton Converter
3. Seleziona la conversione desiderata (es. "Cyfral → Dallas")
4. Il converter genera il codice convertito
5. Salva come nuova chiave
6. Testa l'emulazione della chiave convertita sul lettore target

**Limiti della conversione:**

- La conversione non garantisce che il lettore accetterà il codice convertito - dipende dal firmware del lettore
- Lettori che verificano solo l'ID (senza controllare il protocollo) sono più permissivi
- Lettori che verificano anche il protocollo di comunicazione rifiuteranno codici convertiti
- Il keyspace diverso tra protocolli significa che non tutte le conversioni sono reversibili

> **Nota personale:** L'iButton Converter è uno strumento di nicchia - lo uso raramente, forse 1 volta su 20 operazioni iButton. Il caso d'uso reale è quando un condominio ha un sistema "misto" (es. lettore multi-protocollo con chiavi sia Dallas che Cyfral) e devi capire come il lettore gestisce i diversi formati. È più uno strumento di analisi che di attacco.

### iButton Fuzzer (DS1990 / Metakom / Cyfral)

L'iButton Fuzzer è lo strumento più aggressivo del modulo iButton - genera e trasmette codici iButton in sequenza per testare la sicurezza di un lettore. È l'equivalente di un bruteforce sull'accesso fisico.

**Principio di funzionamento:**

Il fuzzer genera codici iButton (ROM code per Dallas, codici per Cyfral/Metakom) e li emula in rapida successione sul lettore target, tentando di trovare un codice valido nel database del lettore.

**Modalità disponibili:**

**1. Random (Casuale):**
- Genera codici casuali ad ogni tentativo
- Utile per test statistici e per verificare la reazione del lettore a codici non validi
- Non garantisce di trovare un codice valido - la probabilità è funzione del keyspace e del numero di codici nel database del lettore

**2. Sequenziale:**
- Incrementa il codice di 1 ad ogni tentativo (o secondo un pattern definito)
- Percorre lo spazio dei codici in ordine
- Più sistematico del random ma più prevedibile

**3. Custom:**
- L'utente definisce un range o un set di codici da provare
- Utile quando hai informazioni parziali sul target (es. conosci il family code, o sai che i seriali del condominio iniziano con un prefix specifico)

**Timing tra tentativi:**

Il tempo tra un tentativo e l'altro dipende da:
- **Tempo di reset/presence/read:** ~1-2 ms per ciclo 1-Wire completo
- **Tempo di risposta del lettore:** variabile, tipicamente 100-500 ms
- **Tempo di recovery del lettore:** alcuni lettori impongono un delay anti-bruteforce

In pratica, il rate massimo è di circa **2-5 tentativi al secondo** per Dallas, limitato dal tempo di risposta del lettore e dalla necessità di mantenere il contatto fisico stabile.

**Analisi del keyspace:**

**DS1990A (Dallas):**
- Keyspace totale: 2^64 = ~1.8 x 10^19
- Keyspace effettivo (solo serial): 2^48 = ~2.8 x 10^14
- Al ritmo di 5 tentativi/secondo: ~1.78 x 10^6 anni per esaurire il keyspace
- **Conclusione:** il bruteforce puro è impraticabile su Dallas

**Cyfral:**
- Keyspace base: 2^8 = 256
- Al ritmo di 2 tentativi/secondo: ~128 secondi per esaurire il keyspace
- **Conclusione:** il bruteforce è assolutamente praticabile - 2 minuti circa

**Metakom:**
- Keyspace: 2^32 = ~4.29 x 10^9
- Al ritmo di 3 tentativi/secondo: ~45 anni per esaurire il keyspace
- **Conclusione:** il bruteforce puro è impraticabile, ma range ridotti sono fattibili

**Procedura operativa - Fuzzing DS1990:**

1. Menu → iButton Fuzzer → DS1990
2. Seleziona la modalità:
   - Random: genera ID casuali con family code 0x01 e CRC valido
   - Sequenziale: parte da un ID base e incrementa
   - Custom: inserisci un prefix o un range
3. Capovolgi il Flipper e appoggia il pad sul lettore target
4. Avvia il fuzzing - mantieni il contatto fisico stabile
5. Lo schermo mostra il codice corrente e il contatore di tentativi
6. Se il lettore risponde positivamente (apre la porta), il codice viene salvato automaticamente

**Procedura operativa - Fuzzing Cyfral:**

1. Menu → iButton Fuzzer → Cyfral
2. Seleziona la modalità (per Cyfral, la sequenziale è la più efficace dato il keyspace ridotto)
3. Appoggia il pad sul lettore Cyfral
4. Avvia - il fuzzer percorre i 256 codici possibili
5. Tempo stimato: 2-4 minuti per esaurire tutto il keyspace
6. Se trova un codice valido, lo salva automaticamente

**Procedura operativa - Fuzzing Metakom:**

1. Menu → iButton Fuzzer → Metakom
2. Seleziona la modalità (custom con range ridotto è la scelta migliore)
3. Se hai informazioni sul target, restringi il range
4. Appoggia il pad sul lettore Metakom
5. Avvia - per un range di 1000 codici, circa 5-8 minuti
6. Per il keyspace completo: impraticabile, usa informazioni per restringere

**Contromisure dei lettori anti-fuzzing:**

Alcuni lettori moderni implementano protezioni:
- **Rate limiting:** delay crescente dopo N tentativi falliti
- **Lockout:** blocco temporaneo dopo N tentativi falliti (tipicamente 10-30 secondi)
- **Alarm:** segnalazione acustica/visiva dopo tentativi ripetuti
- **Logging:** registrazione dei tentativi falliti (raro nei citofoni economici)

> **Nota personale:** Il fuzzing iButton è straordinariamente efficace su Cyfral - 256 combinazioni sono niente. Ho aperto citofoni Cyfral in meno di 3 minuti durante audit autorizzati. Per Dallas, il fuzzing puro è inutile - 2^48 combinazioni non le esaurisci mai. Pero' c'è un trucco: molti installatori usano chiavi con seriali sequenziali (comprate in lotto dalla stessa produzione). Se recuperi una chiave, prova i seriali adiacenti - ho trovato condomini dove tutte le chiavi avevano seriali nel range XX:XX:XX:00:00:01 - XX:XX:XX:00:00:60 (96 unità). In quel caso il fuzzing con range è devastante.

---

