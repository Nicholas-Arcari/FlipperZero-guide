# Attacchi Avanzati e Contromisure - Sub-GHz

Analisi dei principali vettori di attacco RF Sub-GHz e relative contromisure. Per ogni attacco: principio di funzionamento, prerequisiti, limitazioni reali e difese efficaci.

---

## Replay Attack (Codice Fisso)

### Principio
L'attaccante cattura il segnale RF trasmesso da un telecomando legittimo e lo riproduce identico. Poichè il codice è statico, il ricevitore non distingue tra l'originale e la copia.

### Prerequisiti
- Il sistema target usa codice fisso (nessun rolling code)
- L'attaccante si trova nel raggio di ricezione del trasmettitore (~10-50m)
- Conoscenza della frequenza (ottenibile con Frequency Analyzer)

### Procedura con Flipper Zero
1. Sub-GHz → Read sulla frequenza target
2. Attendi una trasmissione legittima
3. Il Flipper decodifica e salva il segnale
4. Sub-GHz → Saved → Send per riprodurre

### Limitazioni Reali
- Portata di trasmissione del Flipper limitata (~5-15m indoor)
- Alcuni ricevitori hanno filtri di timing stretti che rifiutano segnali con jitter
- Il segnale deve essere catturato in condizioni di basso rumore RF

### Contromisure
- **Migrare a rolling code** (KeeLoq, AES rolling) - elimina completamente il replay
- **Sistemi challenge-response** - il ricevitore invia una challenge, il trasmettitore risponde con il codice + challenge. Impossibile da replicare
- **Timeout aggressivo** - il codice è valido solo per N secondi dopo la trasmissione
- **Rilevamento anomalie** - log e alert su aperture in orari insoliti

---

## RollJam Attack

### Principio
L'attacco più sofisticato contro sistemi rolling code. L'attaccante usa simultaneamente:
1. Un **jammer** che impedisce al ricevitore di ricevere il codice legittimo
2. Un **ricevitore** (su frequenza leggermente diversa o con antenna direzionale) che cattura il codice

L'utente preme il telecomando, il codice viene catturato ma non ricevuto (jammato). L'utente preme di nuovo - il secondo codice viene catturato, e il primo viene rilasciato (replay). L'attaccante ora possiede un codice rolling valido (il secondo) non ancora consumato.

### Prerequisiti
- Jammer RF dedicato (il Flipper da solo non basta - non può jammmare e ricevere contemporaneamente)
- Due dispositivi di ricezione, o un dispositivo con capacità full-duplex
- Prossimità al target (il jammer deve sovrastare il segnale del telecomando)
- Timing preciso

### Perchè il Flipper Zero da Solo Non Basta
Il CC1101 del Flipper è half-duplex: può solo trasmettere O ricevere, mai entrambi. Per un RollJam servono minimo due radio: una per jammmare, una per ricevere. Possibile con Flipper + modulo CC1101 esterno via GPIO, ma richiede firmware custom.

### Contromisure
- **Timeout aggressivo sul rolling code** - il codice scade dopo 30-60 secondi
- **Anti-jamming** - il ricevitore rileva il jamming (energia RF anomala senza decodifica valida) e attiva un allarme
- **Doppia verifica** - il sistema richiede due pressioni con timing specifico
- **802.11w-style protection** - management frame autenticati (applicato al Sub-GHz)
- **Rilevamento gap nel contatore** - se il ricevitore nota che il contatore è saltato di >1 senza aperture intermedie, blocca il sistema

---

## Bruteforce

### Principio
Invio sequenziale di tutti i codici possibili fino a trovare quello valido. Fattibile solo su sistemi con spazio di codici ridotto.

### Tempi Realistici

| Bit | Combinazioni | Tempo (~10 codici/sec) | Praticabilità |
|-----|-------------|----------------------|----------------|
| 8 | 256 | ~26 secondi | Triviale |
| 10 | 1.024 | ~2 minuti | Facile |
| 12 | 4.096 | ~7 minuti | Fattibile |
| 16 | 65.536 | ~2 ore | Possibile |
| 20 | 1.048.576 | ~29 ore | Difficile |
| 24 | 16.777.216 | ~19 giorni | Impraticabile |
| 32 | 4.294.967.296 | ~13 anni | Impossibile |

### Procedura con Flipper Zero
1. Sub-GHz Bruteforcer → seleziona protocollo e bit-length
2. Imposta frequenza target
3. Avvia → il Flipper trasmette in sequenza
4. Osserva il ricevitore per rilevare l'apertura

### Limitazioni Reali
- Velocità limitata dalla durata di ogni trasmissione (~100ms per codice)
- Alcuni ricevitori hanno lockout dopo N tentativi rapidi
- La portata del Flipper limita l'efficacia (devi stare vicino)
- Batteria: il bruteforce consuma molta energia TX

### Contromisure
- **Lunghezza codice sufficiente** (minimo 20 bit, ideale 32+)
- **Lockout temporale** dopo N tentativi non validi
- **Rate limiting** sul ricevitore (ignora trasmissioni troppo ravvicinate)
- **Rolling code** - rende il bruteforce inutile (lo spazio effettivo è 2^64+)
- **Alert su tentativi multipli** - il sistema segnala attività anomala

---

## Jamming (Interferenza RF)

### Principio
Saturazione della frequenza target con rumore RF per impedire la comunicazione tra trasmettitore e ricevitore. Non richiede conoscenza del protocollo - basta trasmettere energia sulla stessa frequenza.

### Tipologie
- **Barrage jamming:** rumore continuo su tutta la banda - facile da rilevare
- **Spot jamming:** rumore mirato sulla frequenza esatta - più efficace, meno rilevabile
- **Deceptive jamming:** trasmissione di segnali falsi che confondono il ricevitore
- **Reactive jamming:** il jammer si attiva solo quando rileva una trasmissione legittima - il più difficile da contrastare

### Il Flipper Come Jammer
Il Flipper può trasmettere un segnale continuo su una frequenza specifica (via Read RAW con file di rumore), ma la potenza (+12 dBm) è molto limitata. Efficace solo a breve distanza (<5m) e facilmente sopraffatto da trasmettitori più potenti.

### Contromisure
- **Anti-jamming con heartbeat monitoring** - il ricevitore si aspetta un segnale periodico dal sensore. Se il segnale scompare (perchè jammato), scatta l'allarme
- **Frequency hopping** - il sistema cambia frequenza secondo un pattern pseudocasuale
- **Spread spectrum** - il segnale è distribuito su una banda larga, difficile da jammmare
- **Dual-band** - sensori che trasmettono su 433 E 868 MHz. Per jammmarli entrambi serve il doppio dell'equipaggiamento
- **Rilevamento energia anomala** - il ricevitore misura il livello di rumore e genera allarme se anomalmente alto

---

## Side-Channel sulla Manufacturer Key (KeeLoq)

### Principio
Le implementazioni KeeLoq usano una "manufacturer key" condivisa tra tutti i dispositivi dello stesso produttore. Se questa chiave viene estratta (tramite analisi DPA/SPA su un singolo telecomando), tutti i dispositivi del produttore sono compromessi.

### Attacco DPA (Differential Power Analysis)
1. Si acquista un telecomando dello stesso produttore del target
2. Si collega un oscilloscopio ad alta velocità al chip
3. Si misurano le variazioni di consumo elettrico durante la cifratura
4. Analisi statistica delle tracce di potenza per estrarre la chiave

### Prerequisiti
- Equipaggiamento da laboratorio (oscilloscopio 1+ GHz, sonde differenziali)
- Competenze avanzate in crittanalisi side-channel
- Accesso fisico a un telecomando dello stesso produttore
- Tempo: ore/giorni per l'analisi

### Rilevanza per il Flipper
Il Flipper Zero non esegue direttamente attacchi side-channel, ma se la manufacturer key è nota (pubblicata in paper accademici o leak), il tool Rolling Flaws può usarla per predire codici futuri.

### Contromisure
- **Chiavi per-device** - ogni telecomando ha una chiave unica derivata dal seriale + master secret
- **Protezione side-channel sul chip** - randomizzazione temporale, mascheramento del consumo
- **AES invece di KeeLoq** - algoritmi moderni con migliore resistenza side-channel
- **Secure element** - chip dedicato alla crittografia con protezioni hardware

---

## Matrice Attacchi - Quick Reference

| Attacco | Target | Complessità | Flipper Sufficiente? | Impatto |
|---------|--------|-------------|---------------------|---------|
| Replay | Codice fisso | Bassa | Si' | Apertura immediata |
| RollJam | Rolling code | Alta | No (serve jammer) | Apertura singola |
| Bruteforce | Codice fisso <16 bit | Bassa-Media | Si' | Apertura dopo tempo |
| Jamming | Qualsiasi | Bassa | Parziale (bassa potenza) | DoS temporaneo |
| Side-Channel | KeeLoq | Molto Alta | No (serve lab) | Compromissione totale |
