## Troubleshooting e Limiti

### Problemi Comuni e Soluzioni

#### Il segnale catturato non funziona sul dispositivo target

**Causa probabile 1 - Cattura incompleta:**
- Il segnale RAW è stato troncato (comune con protocolli AC lunghi)
- Soluzione: avvicinati al telecomando sorgente, assicurati che la cattura mostri l'intero frame

**Causa probabile 2 - Protocollo sbagliato:**
- Il Flipper ha decodificato il segnale con il protocollo errato
- Soluzione: forza la cattura RAW e prova a riprodurre quella

**Causa probabile 3 - Distanza eccessiva:**
- Stai troppo lontano dal dispositivo target
- Soluzione: avvicinati a 2-3 metri, punta direttamente al ricevitore IR

**Causa probabile 4 - Angolo sbagliato:**
- Non stai puntando verso il ricevitore IR del dispositivo
- Soluzione: identifica dove si trova il ricevitore (solitamente frontale, spesso indicato da una finestra scura) e punta direttamente li'

**Causa probabile 5 - Luce ambientale:**
- Forte luce solare o illuminazione fluorescente interferisce con il ricevitore
- Soluzione: chiudi le tende, avvicinati, prova in orari diversi

#### Il Flipper non riconosce il protocollo (tutto è RAW)

**Causa probabile 1 - Protocollo non supportato:**
- Il dispositivo usa un protocollo proprietario non nel database del Flipper
- Soluzione: usa la cattura RAW, funzionerà comunque per la riproduzione

**Causa probabile 2 - Frequenza portante non standard:**
- Il dispositivo usa 56 kHz o altra frequenza non ottimale per il TSOP75338
- Soluzione: avvicinati molto (5-10 cm) per compensare la sensibilità ridotta

**Causa probabile 3 - Segnale debole:**
- Le batterie del telecomando sorgente sono scariche
- Soluzione: sostituisci le batterie o avvicinati molto

#### Problemi specifici con climatizzatori

**Sintomo:** Il comando catturato non ha effetto sull'AC.

**Spiegazione:** I protocolli AC inviano lo stato completo. Se hai catturato "imposta 24 gradi in modalità freddo" e il climatizzatore è già a 24 gradi in freddo, potrebbe non reagire visibilmente. Oppure, il frame catturato include uno stato che non corrisponde a quello attuale del climatizzatore e viene rifiutato.

**Soluzioni:**
- Cattura il segnale di **Power On/Off** - è il comando meno dipendente dallo stato
- Cattura **ogni variazione** separatamente (ogni temperatura, ogni modalità)
- Usa i telecomandi AC dedicati del Flipper (Hitachi, Midea, Mitsubishi) che gestiscono correttamente lo stato

#### Il dispositivo risponde solo a volte

**Causa probabile 1 - Distanza al limite:**
- Sei al margine della portata TX - il segnale arriva al ricevitore con potenza borderline
- Soluzione: avvicinati di 1-2 metri

**Causa probabile 2 - Interferenza da rimbalzi:**
- In ambienti con molte superfici riflettenti, il segnale diretto e i rimbalzi possono arrivare sfasati, creando interferenza
- Soluzione: cambia posizione, prova un angolo diverso

**Causa probabile 3 - Timing RAW impreciso:**
- La cattura RAW ha piccole imprecisioni di timing che a volte causano errori di decodifica
- Soluzione: cattura il segnale più volte e usa la cattura con i timing più puliti

### Limiti Strutturali del Modulo IR

| Limite | Dettaglio | Workaround |
|---|---|---|
| **Portata TX** | 3-8 metri | Avvicinarsi al target |
| **Angolo di emissione** | ~34 gradi | Puntare direttamente |
| **Singolo LED** | Nessuna ridondanza | Nessuno (limite hardware) |
| **Frequenza portante** | Ottimizzato per 38 kHz | RAW per frequenze diverse |
| **Luce ambientale** | Riduce portata | Operare in interni/ombra |
| **Nessun LED esterno nativo** | Non espandibile via GPIO | Mod hardware non ufficiali |
| **Protocolli AC** | Cattura complessa | Telecomandi dedicati per marca |
| **Line-of-sight** | Richiede percorso ottico | Usare rimbalzi su pareti |

---

## Esperienza Personale

### Il Flipper IR nel Quotidiano

Il modulo IR è probabilmente la funzione del Flipper Zero che uso **più frequentemente nella vita quotidiana** - paradossalmente più del Sub-GHz o dell'NFC che sono "più interessanti" dal punto di vista del pentest.

Motivo: il Flipper è diventato il mio telecomando universale. Porto sempre il Flipper con me, e avere un telecomando per qualsiasi TV, proiettore o AC nel raggio di pochi metri è enormemente pratico.

### Esperienze sul Campo

> **Nota personale:** In un physical pentest per un'azienda di medie dimensioni a Milano, ho usato il modulo IR per spegnere 4 display nella lobby durante la fase di ricognizione interna. Il fatto è finito nel report come finding di severità media: "Dispositivi di comunicazione aziendale (display informativi, digital signage) controllabili da personale non autorizzato senza alcuna credenziale o accesso privilegiato". Il cliente ha poi coperto i ricevitori IR con nastro opaco - la contromisura più semplice e più efficace.

> **Nota personale:** I condizionatori sono i dispositivi IR più frustranti da gestire nel pentest. Ogni marca ha il suo protocollo, ogni modello ha le sue varianti. In un engagement, ho passato 15 minuti a cercare di controllare un AC Daikin con cattura RAW prima di scoprire che il modello specifico usava una variante del protocollo con header diverso. Lezione appresa: per i climatizzatori, se il database integrato non funziona, cattura direttamente dal telecomando originale. Non perdere tempo a indovinare il protocollo.

> **Nota personale:** La portata TX del Flipper è il vincolo operativo numero uno. In una sala riunioni di grandi dimensioni (10+ metri), non riesci a raggiungere il display dal fondo della stanza. Devi avvicinarti. In ambienti dove la discrezione è critica, questo può essere un problema. Il mio approccio: mi avvicino al display con la scusa di "guardare meglio lo schermo" o "prendere un caffe'" dal distributore vicino - qualsiasi pretesto per ridurre la distanza a 3-4 metri.

> **Nota personale:** Un trucco che pochi conoscono: la fotocamera del telefono vede l'infrarosso. Se vuoi verificare che il Flipper stia effettivamente trasmettendo (o se vuoi localizzare il LED IR di un telecomando), guardalo attraverso la fotocamera dello smartphone. Vedrai un flash violetto ogni volta che il LED IR si attiva. Utile anche per verificare che le batterie di un telecomando non siano scariche prima di catturare i segnali.

> **Nota personale:** IR Transfer tra due Flipper è un trick che uso in scenari specifici: quando devo trasferire un segnale IR catturato a un collega durante un engagement e non voglio usare Bluetooth o WiFi (per non generare traffico wireless rilevabile). È lento, ma è completamente passivo dal punto di vista RF.

### Considerazioni Finali

Il modulo IR del Flipper Zero è uno strumento straordinariamente semplice ma efficace. Non ha la complessità tecnica dell'NFC o la profondità del Sub-GHz, ma la completa assenza di crittografia nei protocolli IR rende ogni dispositivo IR un bersaglio facile.

Nel pentest fisico, l'IR serve principalmente come:
- **Tool di dimostrazione** - mostrare al cliente che i dispositivi nell'ambiente sono controllabili da chiunque
- **Tool di supporto** - creare distrazioni, manipolare l'ambiente fisico per facilitare altre operazioni
- **Tool di ricognizione** - analizzare i sistemi AV e di controllo ambientale per capire l'infrastruttura

La limitazione principale resta la portata TX e il requisito di line-of-sight. Ma in ambienti interni, con pareti riflettenti e distanze ridotte, il Flipper Zero è semplicemente il "telecomando universale definitivo" - e nelle mani di un pentester, questo è un'arma operativa tutt'altro che trascurabile.
