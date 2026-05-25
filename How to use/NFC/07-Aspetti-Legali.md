# Aspetti Legali - NFC

Quadro normativo italiano ed europeo per l'uso di dispositivi NFC in contesti di security assessment.

---

## Italia

### Codice Penale

- **Art. 615-ter c.p. - Accesso abusivo a sistema informatico:** la clonazione di un badge NFC per accedere a un edificio senza autorizzazione è reato. I sistemi di controllo accessi sono considerati "sistemi informatici" dalla giurisprudenza. Pena: reclusione da 1 a 5 anni.

- **Art. 640-ter c.p. - Frode informatica:** la modifica di dati su card prepagate (es. credito mensa, abbonamenti trasporto) per ottenere un vantaggio è frode informatica. Pena: reclusione da 6 mesi a 3 anni e multa.

- **Art. 491-bis c.p. - Falsità in documento informatico:** la creazione di badge clonati può configurare questo reato se il badge è considerato documento informatico.

- **Art. 617-quater c.p. - Intercettazione fraudolenta:** la cattura di dati NFC durante la comunicazione reader-tag può rientrare in questa fattispecie.

### GDPR

- I dati letti dai badge possono contenere informazioni personali (UID associato a un dipendente, nome, ruolo, permessi)
- La lettura non autorizzata di badge è trattamento illecito di dati personali
- Anche durante un pentest autorizzato, i dati raccolti vanno trattati secondo il principio di minimizzazione

---

## Unione Europea

- **Direttiva RED 2014/53/EU:** il Flipper Zero è conforme (NFC opera nella banda ISM 13.56 MHz)
- **GDPR (Reg. 2016/679):** i dati NFC associabili a persone fisiche sono dati personali
- **Direttiva NIS2 (2022/2555):** i sistemi di controllo accessi di infrastrutture critiche rientrano negli obblighi di sicurezza

---

## Best Practice Legali per il Pentest NFC

### Prima dell'Engagement

1. **Autorizzazione scritta specifica** che includa:
   - "Test dei sistemi NFC/RFID di controllo accessi"
   - Elenco specifico di lettori/porte autorizzati per il test
   - Autorizzazione alla lettura, clonazione e modifica di badge
   - Scope temporale e geografico

2. **Gestione Magic Card:**
   - Le Magic Card clonate sono equivalenti a chiavi/badge - custodirle come credenziali
   - Non portare Magic Card clonate fuori dal perimetro autorizzato
   - Numerare le Magic Card e tracciarne l'uso

3. **Esclusioni:**
   - Chiarire se il test include card di terze parti (hotel, trasporti, fornitori)
   - Definire le aree off-limits (es. sala server, aree classificate)

### Durante l'Engagement

- Documentare ogni lettura di badge: timestamp, UID, tipo, risultato
- Non tentare mai la lettura di badge senza autorizzazione (anche "drive-by" informale)
- Se trovi dati sensibili nei badge (nome, CF, dati sanitari): annotare nel report ma non conservare
- La modifica di credito prepagato (mensa, distributori) va documentata e immediatamente ripristinata

### Dopo l'Engagement

- **Cancellare tutti i dump** dalla SD card e dal PC
- **Formattare tutte le Magic Card** utilizzate (azzerare tutti i settori)
- **Il report deve descrivere la vulnerabilità** senza includere chiavi effettive o dump completi
- Conservare solo le evidenze strettamente necessarie per un eventuale follow-up

---

## Zona Grigia - Lettura Passiva

La lettura NFC di un badge richiede prossimità fisica (<5 cm) e quindi implica un atto intenzionale. Non esiste l'equivalente della "ricezione passiva" del Sub-GHz - ogni lettura NFC è attiva.

**Implicazione:** la lettura non autorizzata di un badge, anche senza scrivere o clonare, è potenzialmente un atto illecito perche':
- Richiede un'azione volontaria (avvicinare il dispositivo)
- Acquisisce dati che possono essere personali
- Il titolare del badge non ha prestato consenso

**Regola pratica:** non leggere MAI un badge senza autorizzazione, nemmeno per "vedere che tipo e'".
