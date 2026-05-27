## Attacchi e Contromisure

### La Realtà Fondamentale: IR Non Ha Crittografia

Questo è il punto critico che distingue l'IR da quasi tutte le altre tecnologie wireless:

**I segnali IR sono completamente privi di crittografia, autenticazione, rolling code o qualsiasi forma di protezione.**

Ogni segnale catturato può essere riprodotto infinite volte con successo al 100%. Non esiste l'equivalente dei rolling code del Sub-GHz, della crittografia Crypto-1 di MIFARE, o dei challenge-response di DESFire.

Perche'? Perchè l'IR è stato progettato negli anni '70-'80 per telecomandi consumer, dove:
- La portata limitata (line-of-sight, pochi metri) era considerata una protezione sufficiente
- Il costo di aggiungere crittografia a telecomandi economici non era giustificabile
- La minaccia di "replay IR" non era considerata un rischio reale

Risultato: nel 2025, miliardi di dispositivi sono controllabili da chiunque abbia un trasmettitore IR e i codici giusti (pubblicamente disponibili).

### Replay Attack - Banale e Inarrestabile

L'attacco più semplice è il replay:

1. **Cattura** il segnale IR con il Flipper (o qualsiasi ricevitore IR)
2. **Riproduci** il segnale identico
3. **Il dispositivo esegue il comando** - non ha modo di distinguere il segnale originale da una copia

Non servono competenze speciali. Non ci sono contromisure a livello di protocollo. L'unica difesa è impedire fisicamente al segnale IR di raggiungere il ricevitore.

### Il Flipper Zero come "TV-B-Gone Definitivo"

Il "TV-B-Gone" è un dispositivo creato nel 2004 da Mitch Altman: un piccolo circuito che cicla attraverso centinaia di codici Power Off per marche TV diverse, spegnendo praticamente qualsiasi televisore nel raggio d'azione.

Il Flipper Zero è un TV-B-Gone enormemente potenziato:

- **Database più grande:** migliaia di codici vs centinaia del TV-B-Gone originale
- **Aggiornabile:** il database può essere espanso caricando nuovi file .ir
- **Bidirezionale:** può anche catturare e analizzare segnali, non solo trasmetterli
- **Multi-dispositivo:** non solo TV - anche AC, proiettori, soundbar, display
- **Programmabile:** puoi creare script personalizzati con sequenze specifiche
- **Discreto:** il Flipper sembra un gadget generico, non un dispositivo di attacco

### Automazione TV-B-Gone con il Flipper

Per massimizzare l'efficacia, puoi preparare sequenze ottimizzate:

1. Crea un file `.ir` con tutti i codici Power Off delle marche più comuni
2. Ordina per diffusione (Samsung e LG prima, marche rare dopo)
3. Usa Universal Remotes per una scansione automatica
4. In alternativa, usa IR Blaster per invio burst rapido

In una scansione aggressiva, il Flipper può provare tutti i codici più comuni in circa **30-60 secondi**.

### Jamming IR

Il jamming IR è l'equivalente ottico del jamming radio:

**Principio:** Un LED IR potente che emette continuamente alla frequenza portante (38 kHz) satura il ricevitore IR del target, impedendogli di ricevere qualsiasi segnale utile.

**Il Flipper può fare jamming?** In teoria si' - trasmettendo una portante continua a 38 kHz. In pratica, il singolo LED e la potenza limitata rendono il jamming efficace solo a distanze molto ravvicinate (1-2 metri).

**Contromisure al jamming:**
- Filtri IR direzionali sul ricevitore
- Ricevitori con AGC avanzato che si adatta alla saturazione
- Utilizzo di protocolli con frequenze portanti diverse (36, 40, 56 kHz)
- Ridondanza: ricevitori IR multipli posizionati in punti diversi

### Contromisure Generali Contro Attacchi IR

Per i difensori (e per il report di pentest):

**Contromisure fisiche (le più efficaci):**
- **Copertura del ricevitore IR:** nastro opaco agli infrarossi sul ricevitore. Costa zero, efficace al 100%. Nota: il nastro deve bloccare i 940 nm - alcuni nastri che sembrano opachi alla luce visibile sono trasparenti all'IR
- **Posizionamento protetto:** ricevitore IR rivolto verso il muro o verso l'alto, non verso il pubblico
- **Involucro:** coperchio fisico con fessura direzionale che limita l'angolo di ricezione

**Contromisure di configurazione:**
- **Hotel/Hospitality mode:** molte TV commerciali hanno una modalità che disabilita o limita i comandi IR (es. blocca Power Off, limita il volume massimo)
- **Disabilitazione IR:** alcuni display professionali permettono di disabilitare completamente il ricevitore IR, gestendo il controllo via RS-232 o rete
- **Power Lock:** funzione che impedisce lo spegnimento via telecomando - richiede lo spegnimento dal pannello fisico o dal software di gestione

**Contromisure di sistema:**
- **Watchdog software:** il media player rileva lo spegnimento del display e lo riaccende automaticamente (comune nei sistemi di digital signage)
- **Controllo centralizzato:** gestione via rete (IP, RS-232) che bypassa completamente l'IR
- **Monitoraggio:** telecamere nelle aree con display critici

---

