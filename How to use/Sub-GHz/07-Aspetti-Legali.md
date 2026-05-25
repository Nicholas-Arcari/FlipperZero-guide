# Aspetti Legali - Sub-GHz

Quadro normativo italiano ed europeo relativo all'uso di dispositivi RF per analisi di sicurezza, penetration testing e ricerca.

---

## Italia

### Codice Penale

- **Art. 617-quater c.p. - Intercettazione fraudolenta di comunicazioni:** la cattura di segnali RF può rientrare in questa fattispecie se fatta senza autorizzazione. Pena: reclusione da 6 mesi a 4 anni. La cattura passiva (solo ricezione) è una zona grigia - la giurisprudenza non è uniforme.

- **Art. 615-ter c.p. - Accesso abusivo a sistema informatico o telematico:** l'apertura di un cancello, porta o barriera tramite replay attack o bruteforce senza autorizzazione è un reato. Pena: reclusione da 1 a 5 anni. Il sistema di automazione del cancello è considerato "sistema informatico" dalla giurisprudenza recente.

- **Art. 617-quinquies c.p. - Installazione di apparecchiature atte ad intercettare comunicazioni:** il possesso e l'uso di dispositivi per intercettare comunicazioni RF può configurare questo reato se l'intento è fraudolento.

### Codice delle Comunicazioni Elettroniche (D.Lgs. 259/2003)

- L'uso delle bande ISM (433 MHz, 868 MHz) è libero entro i limiti di potenza stabiliti (25 mW ERP per 433 MHz, 25 mW per 868 MHz)
- L'**interferenza intenzionale** (jamming) è sempre vietata, indipendentemente dalla frequenza
- La trasmissione su frequenze non ISM richiede licenza
- Il Flipper Zero è conforme ai limiti di potenza ISM (+12 dBm = ~16 mW < 25 mW)

### Piano Nazionale di Ripartizione delle Frequenze (PNRF)

- Le frequenze 433.05-434.79 MHz sono assegnate come ISM in Italia
- Le frequenze 863-870 MHz sono Short Range Devices (SRD) con duty cycle limitato
- L'uso deve rispettare i limiti di duty cycle (tipicamente 1% o 10% a seconda della sotto-banda)

---

## Unione Europea

### Direttiva RED 2014/53/EU (Radio Equipment Directive)

- Regola l'immissione sul mercato di apparecchiature radio
- Il Flipper Zero è conforme (marcatura CE)
- Non regola l'uso specifico, ma il prodotto deve rispettare gli standard armonizzati

### ETSI EN 300 220 (Short Range Devices)

- Standard tecnico per dispositivi a corto raggio nelle bande 25-1000 MHz
- Definisce limiti di potenza, duty cycle, larghezza di banda
- Il Flipper Zero opera entro questi limiti

### GDPR (Regolamento 2016/679)

- La raccolta di dati RF che possono essere associati a persone fisiche (es. ID TPMS, codici telecomando univoci, messaggi POCSAG con dati personali) è soggetta al GDPR
- L'intercettazione di messaggi POCSAG contenenti dati sanitari è trattamento di dati sensibili (art. 9)
- Anche durante un pentest autorizzato, i dati raccolti devono essere trattati secondo il principio di minimizzazione

---

## Regole Operative per il Pentester

### Prima dell'Engagement

1. **Autorizzazione scritta:** ottenere sempre un'autorizzazione esplicita che specifichi:
   - Frequenze autorizzate per la cattura
   - Dispositivi target autorizzati per il replay
   - Scope geografico (l'autorizzazione copre solo l'area specificata)
   - Durata temporale dell'autorizzazione
   
2. **Scope RF specifico:** l'autorizzazione deve coprire esplicitamente le operazioni RF. Un generico "pentest autorizzato" potrebbe non coprire l'intercettazione di segnali radio di terze parti.

3. **Esclusioni:** chiarire che la cattura passiva potrebbe intercettare segnali di dispositivi non-target (vicini, passanti). L'autorizzazione dovrebbe prevedere questa eventualità.

### Durante l'Engagement

- **Solo ricezione passiva** senza autorizzazione specifica per la trasmissione
- **Trasmissione (replay/bruteforce)** solo con autorizzazione esplicita per il dispositivo target
- **Mai jamming** senza autorizzazione scritta specifica - il jamming può impattare dispositivi di terze parti
- **Documentare tutto:** frequenze usate, timestamp di ogni cattura/trasmissione, risultati
- **Minimizzazione dati:** cancellare i segnali catturati non pertinenti al report

### Dopo l'Engagement

- Cancellare tutte le catture RF dalla SD card dopo aver completato il report
- Non conservare codici validi di accesso - rappresentano credenziali
- Il report deve descrivere la vulnerabilità senza includere i codici effettivi

---

## Zona Grigia - Ricezione Passiva

La ricezione passiva di segnali RF (senza trasmissione) è una zona grigia legale:

- **Argomento a favore della legalità:** i segnali radio attraversano lo spazio pubblico, la ricezione non richiede accesso a sistemi protetti
- **Argomento contrario:** l'intercettazione mirata di comunicazioni specifiche (es. POCSAG di un ospedale) può configurare reato anche senza trasmissione
- **Precedenti:** la giurisprudenza italiana è scarsa su questo tema specifico per le bande ISM

**Regola pratica:** tratta la ricezione passiva come "probabilmente legale ma potenzialmente contestabile" e ottieni sempre autorizzazione preventiva in contesti professionali.
