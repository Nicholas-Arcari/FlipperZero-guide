# Attacchi Avanzati e Contromisure - NFC

Analisi dei principali vettori di attacco NFC e relative contromisure, con focus su MIFARE Classic e sistemi di controllo accessi.

---

## Magic Card - Guida Completa

### Perchè Servono le Magic Card

L'emulazione NFC del Flipper ha limiti:
- Non tutti i lettori accettano un Flipper emulato
- L'emulazione richiede che il Flipper sia acceso e nella posizione corretta
- Alcuni lettori hanno timing troppo stretti per l'emulazione software

Le Magic Card risolvono questi problemi: sono **tag fisici reali** con la capacità di essere completamente riprogrammati, incluso l'UID (che normalmente è fisso di fabbrica).

### Gen1 (Chinese Magic / UID Changeable)

- **Comando backdoor:** WUPC (0x40, 0x43) permette di scrivere il Blocco 0
- **Vantaggi:** semplice, economica, ben supportata dal Flipper
- **Svantaggi:** rilevabile - un lettore può inviare il comando WUPC e se il tag risponde, sa che è una Magic

### Gen2 (CUID / Direct Write)

- **Nessun backdoor:** il Blocco 0 è scrivibile direttamente con un comando WRITE standard
- **Vantaggi:** non rilevabile con il test WUPC
- **Svantaggi:** meno compatibile con alcuni lettori, a volte instabile

### Gen3 (UFUID)

- **UID scrivibile una volta:** dopo la scrittura, puoi "bloccare" il Blocco 0
- **Vantaggi:** una volta bloccata, si comporta come un tag reale non-magic
- **Svantaggi:** puoi scrivere l'UID solo una volta (a meno di non usare un unlock speciale)

### Gen4 (Ultimate Magic / GDM)

- **Completamente programmabile:** UID, SAK, ATQA, dati, tutto scrivibile illimitatamente
- **Comando proprietario GDM:** non rilevabile dai test anti-magic standard
- **Supporto 1K e 4K:** configurabile
- **Vantaggi:** la più versatile, non rilevabile, illimitata
- **Svantaggi:** costo leggermente superiore (~2-3 euro), richiede firmware con supporto Gen4

### Tabella Comparativa Magic Card

| Tipo | UID Rewrite | Rilevabile | Compatibilità | Prezzo | Uso Consigliato |
|------|------------|------------|----------------|--------|-----------------|
| Gen1 | Si' (backdoor) | Si' (WUPC) | Ottima | ~0.50 EUR | Test in lab |
| Gen2 | Si' (direct) | No (WUPC) | Buona | ~0.80 EUR | Target senza anti-magic |
| Gen3 | Una volta | No (dopo lock) | Ottima | ~1.50 EUR | Clone permanente |
| Gen4 | Illimitato | No | Ottima | ~2-3 EUR | Pentest professionale |

> **Nota personale:** Per il pentest, uso esclusivamente Gen4 (Ultimate Magic). Sono le uniche che non vengono rilevate da lettori moderni con anti-magic check. Le Gen1 vengono bloccate da circa il 30% dei lettori enterprise. Le Gen4 passano sempre. Ne tengo una decina nel kit, pre-programmate con dump di badge usati in engagement precedenti (ovviamente cancellate dopo il report).

---

## Attacchi Principali

### Crypto-1 Key Recovery (MFKey32)

**Principio:** L'algoritmo Crypto-1 usato da MIFARE Classic ha vulnerabilità crittografiche note. Analizzando le nonce scambiate durante l'autenticazione tra lettore e tag, è possibile recuperare le chiavi segrete.

**Procedura dettagliata:**
1. Il Flipper emula un tag con UID noto
2. Viene presentato al lettore target
3. Il lettore invia un challenge (nonce crittografico)
4. Il Flipper risponde con una risposta calcolata
5. Lo scambio viene registrato (nonce_reader, nonce_tag, auth_response)
6. L'attacco MFKey32 usa le proprietà matematiche di Crypto-1 per derivare la chiave a 48 bit
7. Servono minimo 2 autenticazioni catturate per settore

**Complessità computazionale:** pochi secondi su hardware moderno (il Flipper lo fa direttamente)

**Contromisura:** migrare a DESFire EV2/EV3 con chiavi AES-128 diversificate per-card

### Dictionary Attack

**Principio:** Molti sistemi usano chiavi note, di default, o comuni. Il Flipper prova migliaia di chiavi conosciute fino a trovare quella corretta.

**Chiavi comuni:**
```
FFFFFFFFFFFF (default di fabbrica)
A0A1A2A3A4A5 (trasporti pubblici)
D3F7D3F7D3F7 (sistemi NXP)
000000000000 (zero key)
B0B1B2B3B4B5 (variante)
4D3A99C351DD (sistemi di pagamento)
1A982C7E459A (hotel)
```

**Contromisura:** chiavi uniche per installazione, derivate da un master secret + UID del tag

### Hardcoded Key Attack

**Principio:** Molti produttori usano la stessa chiave per tutti i badge dello stesso modello o installazione. Se la chiave viene estratta da un singolo badge (tramite dump hardware, reverse engineering del firmware del lettore, o leak), tutti i badge sono compromessi.

**Esempi noti:**
- Sistemi di trasporto con chiavi identiche su milioni di card
- Distributori automatici con chiave master hardcoded nel firmware
- Sistemi di accesso con chiave comune per sito

**Contromisura:** chiavi diversificate - ogni badge ha chiavi uniche derivate dall'UID con un algoritmo di derivazione sicuro (es. AES-CMAC)

### Clone-and-Replay

**Principio:** dump completo del badge → scrittura su Magic Card → accesso

**Procedura:**
1. Lettura completa di tutti i settori (richiede tutte le chiavi)
2. Scrittura su Magic Card Gen4 (incluso UID, SAK, ATQA)
3. La Magic Card è indistinguibile dall'originale

**Contromisura:** 
- Blacklisting di UID duplicati (se due badge con lo stesso UID vengono visti in posti diversi)
- Rolling data - il lettore scrive un timestamp/contatore dopo ogni accesso. Un clone avrebbe dati stale
- Mutual authentication - il badge verifica il lettore (impedisce la lettura non autorizzata)

### UID-Only Bypass

**Principio:** Sistemi che verificano solo l'UID (4 o 7 byte) senza leggere i dati nei settori. Basta conoscere l'UID per emularlo.

**Procedura:**
1. NFC → Read: cattura solo l'UID (non servono le chiavi dei settori)
2. NFC → Emulate con l'UID catturato
3. Oppure: NFC Fuzzer per enumerare UID validi

**Complessità:** UID a 4 byte = 4.3 miliardi di combinazioni (bruteforce impraticabile), ma spesso gli UID sono sequenziali → range ristretto

**Contromisura:** verificare SEMPRE i dati nei settori autenticati, mai solo l'UID

### Relay Attack

**Principio:** estensione della distanza reader-tag tramite relay in tempo reale

**Architettura:**
```
[Lettore] ←NFC→ [Proxy (Flipper 1)] ←rete→ [Relay (Flipper 2)] ←NFC→ [Badge vittima]
```

**Latenza critica:** il protocollo NFC ha timeout stretti (~5ms per MIFARE). Il relay deve aggiungere meno di 1-2ms di latenza per funzionare. Questo limita la distanza pratica e richiede una rete veloce.

**Contromisura:**
- Distance bounding - il lettore misura il tempo di risposta. Con un relay, il tempo aumenta e il lettore rifiuta la transazione
- Timeout stretti - ridurre il timeout di autenticazione
- Multi-factor - badge + PIN o badge + biometrico

---

## Matrice Attacchi - Quick Reference

| Attacco | Target | Complessità | Flipper Sufficiente? | Impatto |
|---------|--------|-------------|---------------------|---------|
| Dictionary | MIFARE Classic | Bassa | Si' | Dump completo |
| MFKey32 | MIFARE Classic | Media | Si' | Key recovery |
| Hardcoded Key | Vari | Bassa (se nota) | Si' | Dump + clone |
| Clone-and-Replay | MIFARE Classic | Bassa-Media | Si' (+ Magic Card) | Accesso |
| UID-Only | Sistemi semplici | Molto Bassa | Si' | Accesso |
| Relay | Qualsiasi NFC | Alta | Parziale (serve 2) | Accesso remoto |
| Fuzzing UID | Sistemi semplici | Media | Si' | Enumerazione |
