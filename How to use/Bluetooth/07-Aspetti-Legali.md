## Aspetti Legali

L'utilizzo delle funzionalità BLE del Flipper Zero in contesti non autorizzati ha implicazioni legali significative.

### BLE Spam

Il BLE Spam si configura come **interferenza con comunicazioni wireless altrui**. In Italia e nella UE:

- **Direttiva 2014/53/EU (RED)** - Regola l'uso di apparecchiature radio. L'invio di segnali radio che interferiscono con dispositivi altrui è vietato
- **Art. 617-bis c.p. (Italia)** - Installazione di apparecchiature atte ad intercettare o impedire comunicazioni
- **Art. 617-quater c.p.** - Intercettazione, impedimento o interruzione illecita di comunicazioni informatiche o telematiche
- **Codice delle Comunicazioni Elettroniche (D.Lgs. 259/2003)** - Regola l'uso dello spettro radio in Italia

In pratica, il BLE Spam in un luogo pubblico senza autorizzazione può essere perseguito come disturbo alle comunicazioni, interferenza con dispositivi wireless altrui, o in casi estremi come sabotaggio informatico se causa danni misurabili.

### BLE HID (BadBT)

L'uso di BadBT su dispositivi altrui senza autorizzazione è **accesso abusivo a sistema informatico** (Art. 615-ter c.p. in Italia), aggravato dal fatto che avviene senza contatto fisico.

### BLE Scanning

La scansione passiva di dispositivi BLE nelle vicinanze è generalmente legale (i dispositivi trasmettono volontariamente su bande pubbliche). Tuttavia:

- Il tracciamento sistematico di dispositivi BLE individuali può violare il GDPR (il MAC address BLE è dato personale se associabile a un individuo)
- L'uso dei dati raccolti per profilazione o sorveglianza è soggetto alla normativa privacy
- In contesti aziendali, la policy interna potrebbe vietare la scansione wireless

### Raccomandazioni

- **Ottenere sempre autorizzazione scritta** prima di qualsiasi test BLE in ambienti non propri
- **Definire il perimetro** - Specificare quali funzionalità BLE saranno usate e su quali target
- **Documentare tutto** - Timestamp, screenshot, log di ogni attività
- **Non usare BLE Spam in luoghi pubblici** - Ospedali, aeroporti, trasporti pubblici sono ambienti sensibili
- **Attenzione ai dispositivi medici** - Pacemaker, pompe insulina e altri dispositivi medici BLE NON devono MAI essere target di test non autorizzati
- **Contesto educational** - In contesti didattici, usare ambienti controllati (lab isolato, gabbia di Faraday)

> **Nota personale:** In ogni engagement che include test BLE, inserisco una clausola specifica nel contratto che elenca le tecniche BLE autorizzate (scanning, spam demo, HID test) e i target specifici. Non uso mai il BLE Spam in aree pubbliche condivise o in aree con dispositivi medici. Per le demo di awareness, limito il raggio d'azione alla meeting room designata e avviso i partecipanti prima di iniziare. La trasparenza è fondamentale - il BLE Spam è una demo, non un attacco.

---

