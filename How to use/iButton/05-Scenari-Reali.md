## Scenari di Penetration Testing

### Scenario 1: Clonazione Chiave Citofono DS1990A

**Obiettivo:** Dimostrare al cliente che il sistema citofonico del suo condominio è vulnerabile alla clonazione delle chiavi.

**Contesto:** Condominio di 40 unità in una città italiana, sistema citofonico con lettore iButton installato negli anni 2000, chiavi DS1990A distribuite a tutti i condomini.

**Fasi operative:**

**Fase 1 - Ricognizione (5 minuti)**
- Identifica il tipo di lettore sul portone (marca, modello)
- Verifica che sia un sistema a contatto (sonda metallica visibile)
- Controlla se ci sono telecamere che coprono l'area del lettore
- Nota il modello di chiave usato dai condomini (forma, colore)

**Fase 2 - Acquisizione chiave (30 secondi)**
- Richiedi al cliente una delle sue chiavi personali
- Menu → iButton → Read
- Appoggia la chiave sul pad del Flipper - mantieni il contatto
- Lettura in ~1-2 secondi
- Verifica: protocollo DS1990A, family code 0x01, ROM code completo
- Salva con nome descrittivo

**Fase 3 - Verifica emulazione (1 minuto)**
- Menu → iButton → Saved → seleziona la chiave → Emulate
- Avvicinati al lettore del portone
- Appoggia il dorso del Flipper sulla sonda
- Verifica apertura - se si apre, la lettura è confermata

**Fase 4 - Creazione clone fisico (2 minuti)**
- Prendi un tag RW1990 vergine dal kit
- Menu → iButton → Saved → seleziona la chiave → Write
- Appoggia il RW1990 sul pad del Flipper
- Attendi la conferma di scrittura
- Verifica leggendo il RW1990 - ROM code identico all'originale

**Fase 5 - Verifica clone (30 secondi)**
- Appoggia il RW1990 programmato sulla sonda del lettore
- Se si apre: clone perfetto, dimostrazione completata

**Fase 6 - Documentazione**
- Fotografia del lettore (no dati personali di terzi)
- Screenshot del ROM code
- Nota: tempo totale dall'acquisizione al clone funzionante: ~5 minuti
- Raccomandazioni nel report: migrazione a sistema NFC con crittografia

**Deliverable per il cliente:**
- Dimostrazione che la chiave è clonabile in 5 minuti
- Spiegazione dell'assenza di crittografia nel protocollo
- Raccomandazione: sistema con challenge-response (MIFARE DESFire, iClass SE)
- Stima costi migrazione

> **Nota personale:** Questo è lo scenario che eseguo più frequentemente. La reazione del cliente quando vedi il portone aprirsi con il clone è sempre la stessa - sorpresa e preoccupazione. È un momento educativo potente. Nella relazione finale, sottolineo sempre che il problema non è il Flipper Zero (che è solo uno strumento), ma il protocollo DS1990A che non ha alcuna forma di autenticazione. Qualsiasi ferramenta con un duplicatore di chiavi iButton da 20 euro può fare lo stesso.

### Scenario 2: Fuzzing Lettore Citofono Cyfral/Metakom

**Obiettivo:** Determinare se un lettore Cyfral è vulnerabile al bruteforce e stimare il tempo necessario per un accesso non autorizzato.

**Contesto:** Condominio con lettore Cyfral CCD-2094, chiavi Cyfral distribuite agli inquilini, nessuna chiave disponibile per la lettura diretta.

**Fasi operative:**

**Fase 1 - Identificazione sistema (2 minuti)**
- Identifica il lettore: marca "Cyfral" o "Eltis" stampata sul pannello
- Verifica la presenza di LED di stato (rosso/verde)
- Controlla il tipo di sonda (la sonda Cyfral ha una forma caratteristica)
- Nota eventuali telecamere o sistemi di allarme

**Fase 2 - Test di reazione del lettore (2 minuti)**
- Tocca la sonda con un oggetto metallico generico (chiave di casa, moneta)
- Osserva la reazione:
  - LED rosso lampeggiante = il lettore ha ricevuto un segnale ma non valido
  - Nessuna reazione = il lettore non ha rilevato un protocollo valido
  - LED verde = improbabile, ma verificherebbe un bypass

**Fase 3 - Fuzzing Cyfral (2-5 minuti)**
- Menu → iButton Fuzzer → Cyfral
- Seleziona: modalità sequenziale (da 0x00 a 0xFF)
- Appoggia il pad del Flipper sulla sonda del lettore
- Avvia il fuzzer
- Mantieni il contatto stabile - qualsiasi oscillazione interrompe la comunicazione
- Osserva il LED del lettore ad ogni tentativo:
  - Rosso = codice rifiutato
  - Verde = codice accettato (salva immediatamente!)
- Con 256 codici a ~2 tentativi/secondo: ~128 secondi (poco più di 2 minuti)

**Fase 4 - Analisi risultati**
- Se trovato: salva il codice, verifica con emulazione manuale
- Se non trovato: il lettore potrebbe usare una variante Cyfral con keyspace esteso
- Nota il comportamento del lettore durante il fuzzing:
  - Ha imposto rate limiting? Dopo quanti tentativi?
  - Ha generato allarmi?
  - Si è bloccato temporaneamente?

**Fase 5 - Documentazione**
- Tempo effettivo per trovare un codice valido
- Comportamento del lettore sotto fuzzing (rate limiting, lockout, allarmi)
- Raccomandazioni: sostituzione sistema Cyfral con Dallas o NFC crittografato

> **Nota personale:** Il fuzzing Cyfral è il mio "party trick" durante le demo ai clienti. 256 combinazioni in 2 minuti - il cliente resta sempre colpito. Ma è importante spiegare che questo funziona perchè il protocollo Cyfral ha un keyspace minuscolo. Non tutti i sistemi Cyfral sono cosi' deboli - alcune installazioni usano varianti con codici più lunghi. E in ogni caso, la raccomandazione è sempre la stessa: migrare a un sistema con crittografia.

### Scenario 3: Conversione Chiave per Sistema Misto

**Obiettivo:** Testare un sistema che accetta sia chiavi Dallas che Cyfral, verificando la corretta segregazione dei protocolli.

**Contesto:** Condominio con lettore multi-protocollo (accetta Dallas e Cyfral), alcune unità hanno chiavi Dallas, altre Cyfral. L'amministratore vuole verificare che non ci siano falle nella configurazione.

**Fasi operative:**

**Fase 1 - Acquisizione campioni (5 minuti)**
- Ottieni una chiave Dallas dal cliente (condomino con Dallas)
- Ottieni una chiave Cyfral dal cliente (condomino con Cyfral)
- Leggi entrambe le chiavi e salva i file

**Fase 2 - Test di base (2 minuti)**
- Emula la chiave Dallas sul lettore - verifica apertura
- Emula la chiave Cyfral sul lettore - verifica apertura
- Entrambe dovrebbero funzionare su un lettore multi-protocollo

**Fase 3 - Test di conversione (5 minuti)**
- Apri iButton Converter
- Converti la chiave Dallas in formato Cyfral
- Converti la chiave Cyfral in formato Dallas
- Testa le chiavi convertite sul lettore:
  - La Dallas-convertita-in-Cyfral funziona? Se si': il lettore non verifica il protocollo, solo l'ID
  - La Cyfral-convertita-in-Dallas funziona? Stessa analisi

**Fase 4 - Analisi delle implicazioni**
- Se le chiavi convertite funzionano: il lettore usa un database unico senza segregazione per protocollo - vulnerabilità
- Se non funzionano: il lettore mantiene database separati per protocollo - corretto
- Verifica se un codice Dallas valido per un condomino apre anche con protocollo Cyfral - cross-protocol weakness

**Fase 5 - Fuzzing cross-protocol**
- Usa il fuzzer Cyfral sul lettore per cercare codici validi
- Se trovi un codice Cyfral che apre: verifica se corrisponde a un Dallas nel database
- Documenta tutte le correlazioni trovate

**Fase 6 - Documentazione**
- Matrice di compatibilità protocolli/codici
- Vulnerabilità cross-protocol identificate
- Raccomandazioni: segregazione database o migrazione a protocollo unico crittografato

> **Nota personale:** Questo scenario è raro ma illuminante quando si presenta. Ho trovato un condominio a Torino dove il lettore multi-protocollo aveva un bug nel firmware: accettava qualsiasi codice Cyfral se era stato appena usato un codice Dallas valido. Il lettore non resettava lo stato di autenticazione tra una lettura e l'altra. Questo tipo di bug è il motivo per cui i test cross-protocol sono importanti - i lettori economici multi-protocollo hanno spesso firmware scritto male.

### Scenario 4: Audit Sicurezza Sistema Condominiale

**Obiettivo:** Audit completo della sicurezza del sistema di accesso iButton di un intero condominio, con report finale e raccomandazioni.

**Contesto:** L'amministratore condominiale commissiona un audit dopo una serie di intrusioni. Il condominio ha 60 unità, sistema citofonico con iButton installato nel 2005, lettore sul portone principale e su due ingressi secondari.

**Fasi operative:**

**Fase 1 - Ricognizione fisica (30 minuti)**
- Mappa tutti gli ingressi: portone principale, ingressi secondari, garage, aree comuni
- Per ogni ingresso:
  - Tipo di lettore (marca, modello, anno stimato)
  - Protocollo usato (Dallas, Cyfral, Metakom)
  - Condizione fisica del lettore (ossidazione, danni, manomissioni)
  - Presenza di telecamere, allarmi, illuminazione
  - Visibilità della sonda (esposta, incassata, protetta)
- Conta il numero di chiavi in circolazione (chiedi all'amministratore)
- Verifica se esistono chiavi "master" o codici amministratore

**Fase 2 - Analisi protocollo (15 minuti)**
- Leggi la chiave del committente su ogni lettore - verifica il protocollo
- Verifica se tutti i lettori usano lo stesso protocollo
- Verifica se tutti i lettori condividono lo stesso database (la chiave funziona su tutti?)
- Identifica il modello esatto delle chiavi in uso

**Fase 3 - Test di clonazione (10 minuti)**
- Clona la chiave del committente su un RW1990
- Testa il clone su tutti i lettori - deve funzionare su tutti quelli dove funziona l'originale
- Documenta il tempo di clonazione (dalla lettura al clone funzionante)
- Stima il costo di un attaccante (Flipper + RW1990 = ~200 euro, o duplicatore iButton generico = ~30 euro)

**Fase 4 - Test di resilienza (20 minuti)**
- Fuzzing leggero su un lettore (con autorizzazione scritta dell'amministratore)
- Verifica:
  - Il lettore ha rate limiting? Dopo quanti tentativi?
  - Il lettore registra tentativi falliti?
  - Il lettore genera allarmi?
  - Il lettore si blocca dopo N tentativi?
- Test di codici non validi: reazione del lettore a ID malformati, CRC errati, family code non standard
- Test di contatto prolungato: il lettore gestisce correttamente timeout e reset?

**Fase 5 - Analisi del database (se accessibile)**
- Richiedi accesso al sistema di gestione chiavi (se esiste)
- Verifica:
  - Numero di chiavi registrate vs chiavi in circolazione (chiavi "fantasma"?)
  - Presenza di chiavi master
  - Data dell'ultimo aggiornamento del database
  - Procedura di revoca chiavi (es. condomino che vende e se ne va)

**Fase 6 - Report finale**

Struttura del report:

```
1. Executive Summary
   - Livello di rischio: CRITICO / ALTO / MEDIO / BASSO
   - Vulnerabilità principali identificate
   - Raccomandazioni prioritarie

2. Metodologia
   - Strumenti utilizzati
   - Test eseguiti
   - Durata dell'assessment

3. Findings
   3.1 Assenza di crittografia nel protocollo
       - Severità: CRITICA
       - Impatto: clonazione chiave in <5 minuti
       - Evidenza: clone funzionante dimostrato
   3.2 Assenza di rate limiting
       - Severità: ALTA
       - Impatto: fuzzing non ostacolato
       - Evidenza: N tentativi senza lockout
   3.3 Chiavi non revocate
       - Severità: MEDIA
       - Impatto: ex-condomini con accesso attivo
       - Evidenza: N chiavi nel database, M condomini attuali
   3.4 [Ulteriori finding specifici]

4. Raccomandazioni
   4.1 Breve termine (0-3 mesi):
       - Audit delle chiavi in circolazione
       - Revoca chiavi di ex-condomini
       - Installazione telecamere sugli ingressi
   4.2 Medio termine (3-12 mesi):
       - Migrazione a sistema NFC con crittografia (MIFARE DESFire)
       - Implementazione access log
       - Procedura formale di gestione chiavi
   4.3 Lungo termine (1-3 anni):
       - Sistema di accesso integrato con videocitofono IP
       - Autenticazione multi-fattore (chiave + PIN)
       - Integrazione con sistema domotico condominiale

5. Appendici
   - Dettagli tecnici dei test
   - Timeline dell'assessment
   - Costo stimato delle mitigazioni
```

> **Nota personale:** Questo tipo di audit è il servizio più richiesto per iButton. L'amministratore condominiale tipicamente non sa nemmeno che tecnologia usa il suo citofono - "sono quelle chiavette rotonde" è il massimo della consapevolezza. Quando presenti il report con la dimostrazione di clonazione in 5 minuti, l'assemblea condominiale prende la cosa molto seriamente. Il costo di migrazione a un sistema NFC è tipicamente 3000-8000 euro per un condominio medio - una spesa significativa ma giustificabile dopo aver dimostrato la vulnerabilità. Il mio consiglio è sempre di partire dalle raccomandazioni a breve termine (revoca chiavi, telecamere) perchè sono a costo zero o molto basso, e poi pianificare la migrazione tecnologica.

---

## Cross-Reference - Scenari Multi-Vettore

| Scenario | Modulo Correlato | Link | Come si collegano |
|----------|-----------------|------|-------------------|
| Citofono + RFID | RFID | [05-Scenari-Reali](../RFID/05-Scenari-Reali.md) | Condomini: iButton per citofono + badge RFID per portone/garage |
| Citofono + Sub-GHz | Sub-GHz | [05-Scenari-Reali](../Sub-GHz/05-Scenari-Reali.md) | iButton per accesso scale + telecomando Sub-GHz per cancello carraio |
| Accesso fisico + BadUSB | USB/Bad USB | [05-Scenari-Reali](../USB/Bad%20USB/05-Scenari-Reali.md) | Dopo accesso via iButton clonato → deploy BadUSB su PC reception |
| iButton + Debug | GPIO/Debug | [04-Scenari-Reali](../GPIO/Debug/04-Scenari-Reali.md) | Dump firmware del lettore iButton per analisi codici memorizzati |

