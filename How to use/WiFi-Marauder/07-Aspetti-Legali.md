## 7. Aspetti Legali

### 7.1 Normativa Italiana

La legislazione italiana in materia di sicurezza informatica e intercettazione
di comunicazioni e particolarmente severa. Le norme rilevanti per l'utilizzo
di strumenti come WiFi Marauder sono:

**Art. 615-ter c.p. - Accesso abusivo ad un sistema informatico o telematico:**
- "Chiunque abusivamente si introduce in un sistema informatico o telematico
  protetto da misure di sicurezza..."
- Pena: reclusione da 1 a 5 anni
- Applicabilita: connettersi a una rete WiFi protetta senza autorizzazione
  configura accesso abusivo anche se la password e stata craccata

**Art. 617-quater c.p. - Intercettazione, impedimento o interruzione illecita
di comunicazioni informatiche o telematiche:**
- "Chiunque fraudolentemente intercetta comunicazioni relative ad un sistema
  informatico o telematico..."
- Pena: reclusione da 1 anno e 6 mesi a 5 anni
- Applicabilita: lo sniffing di traffico WiFi altrui (anche solo management
  frame) puo ricadere in questa fattispecie

**Art. 617-quinquies c.p. - Installazione di apparecchiature atte ad
intercettare comunicazioni informatiche o telematiche:**
- "Chiunque, fuori dai casi consentiti dalla legge, installa apparecchiature
  atte ad intercettare..."
- Pena: reclusione da 1 a 4 anni
- Applicabilita: posizionare un dispositivo (anche Flipper Zero) con lo scopo
  di intercettare comunicazioni wireless altrui

**Art. 640-ter c.p. - Frode informatica:**
- "Chiunque, alterando in qualsiasi modo il funzionamento di un sistema
  informatico o telematico..."
- Applicabilita: Evil Portal per credential harvesting su utenti inconsapevoli

**D.Lgs. 196/2003 e GDPR (Reg. UE 2016/679) - Protezione dati personali:**
- La cattura di MAC address, probe request con SSID, credenziali tramite
  Evil Portal costituisce trattamento di dati personali
- Senza consenso e base giuridica, e una violazione del GDPR
- Sanzioni amministrative fino al 4% del fatturato globale (per aziende)
  o fino a 20 milioni di euro

### 7.2 Normativa Europea

A livello europeo, la Direttiva 2013/40/UE (Direttiva NIS - Attacchi contro
i sistemi informativi) armonizza le normative nazionali:

- Art. 3: accesso illecito a sistemi informativi
- Art. 4: interferenza illecita nel sistema
- Art. 5: interferenza illecita nei dati
- Art. 6: intercettazione illecita
- Art. 7: strumenti utilizzati per commettere reati informatici (possesso
  di strumenti puo essere rilevante se c'e intento criminoso)

### 7.3 Condizioni per il Penetration Testing Legale

Per operare legalmente come penetration tester WiFi in Italia:

1. **Autorizzazione scritta**: contratto firmato dal proprietario della rete
   che specifica esattamente cosa e autorizzato (scope of work).

2. **Scope definito**: elenco preciso di reti target (SSID/BSSID), tecniche
   autorizzate, orari di operazione, aree fisiche.

3. **Esclusioni**: definire esplicitamente cosa NON e autorizzato (es.
   "non e autorizzato l'attacco a reti di terzi visibili dall'area").

4. **Lettera di autorizzazione (Get Out of Jail Free Letter)**: documento
   da portare sempre con se che identifica il tester, il cliente, il
   progetto e i contatti per la verifica.

5. **Assicurazione professionale**: RC professionale per pentester.

6. **Regole di ingaggio**: cosa fare se si intercettano dati sensibili di
   terzi (cancellare immediatamente, non includere nel report).

7. **Gestione dei dati**: tutti i dati catturati (handshake, credenziali,
   pcap) devono essere cancellati in modo sicuro al termine dell'engagement,
   dopo la consegna del report.

**Attenzione**: anche con autorizzazione, alcune azioni possono avere
implicazioni legali se coinvolgono reti o utenti non inclusi nello scope.
Ad esempio:
- Un deauth su un AP target puo disconnettere anche client di terzi
  che condividono lo stesso AP
- Un Evil Portal puo catturare credenziali di persone non incluse nel test
- Lo sniffing su un canale cattura frame di TUTTE le reti su quel canale

> Nota personale: porto sempre con me la lettera di autorizzazione stampata
> e una copia digitale sullo smartphone quando faccio engagement wireless.
> Una volta sono stato fermato dalla security di un edificio mentre facevo
> wardriving nel parcheggio. La lettera firmata dall'IT Director ha risolto
> la situazione in 2 minuti. Senza quella lettera, sarebbe finita con una
> chiamata alla polizia.

---

