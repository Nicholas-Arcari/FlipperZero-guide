## 1. Fondamenti Tecnici del WiFi 802.11

Prima di utilizzare WiFi Marauder in modo efficace, e fondamentale comprendere come
funziona il protocollo WiFi a basso livello. Senza questa conoscenza, si usano gli
strumenti alla cieca -- e un pentester che lavora alla cieca e un rischio per se stesso
e per il cliente.

### 1.1 Architettura dei Frame 802.11

Il protocollo IEEE 802.11 definisce tre categorie fondamentali di frame che viaggiano
sull'interfaccia radio:

**Management Frames (Tipo 0)**

I frame di gestione sono il cuore delle operazioni WiFi e il bersaglio principale della
maggior parte degli attacchi wireless. Non sono cifrati (in assenza di Protected
Management Frames / 802.11w) e gestiscono tutto il ciclo di vita della connessione.

Struttura di un management frame:

```
+------------------+------------------+------------------+
|  Frame Control   |  Duration/ID     |  Address 1 (DA)  |
|  (2 byte)        |  (2 byte)        |  (6 byte)        |
+------------------+------------------+------------------+
|  Address 2 (SA)  |  Address 3       |  Sequence Ctrl   |
|  (6 byte)        |  (BSSID, 6 byte) |  (2 byte)        |
+------------------+------------------+------------------+
|  Frame Body (variabile)             |  FCS (4 byte)    |
+-------------------------------------+------------------+
```

Il campo Frame Control contiene:
- Protocol Version (2 bit): sempre 0 per 802.11 corrente
- Type (2 bit): 00 = Management, 01 = Control, 10 = Data
- Subtype (4 bit): identifica il tipo specifico di frame
- Flags: To DS, From DS, More Fragments, Retry, Power Management, More Data,
  Protected Frame, Order

I sottotipi di management frame piu rilevanti per il pentesting:

| Subtype | Nome                | Funzione                                          |
|---------|---------------------|---------------------------------------------------|
| 0000    | Association Req     | Client chiede di associarsi a un AP               |
| 0001    | Association Resp    | AP risponde alla richiesta di associazione         |
| 0010    | Reassociation Req   | Client chiede riassociazione (roaming)             |
| 0011    | Reassociation Resp  | AP risponde alla riassociazione                    |
| 0100    | Probe Request       | Client cerca reti disponibili                      |
| 0101    | Probe Response      | AP risponde con le proprie informazioni            |
| 1000    | Beacon              | AP annuncia la propria presenza periodicamente     |
| 1010    | Disassociation      | Terminazione della associazione                    |
| 1011    | Authentication      | Autenticazione Open System o Shared Key            |
| 1100    | Deauthentication    | Terminazione forzata dell'autenticazione           |
| 1101    | Action              | Frame per varie azioni (spectrum mgmt, ecc.)       |

> Nota personale: il 90% di quello che fa Marauder ruota attorno ai management frame.
> Quando ho iniziato a usare Marauder senza capire la struttura dei frame, i risultati
> erano confusi e inutili. Da quando ho studiato i frame 802.11, ogni output di scan
> e sniff ha assunto un significato preciso. Consiglio vivamente di studiare la
> specifica IEEE 802.11-2020 (almeno i capitoli su MAC frame format) prima di toccare
> qualsiasi tool wireless.

**Control Frames (Tipo 1)**

I frame di controllo gestiscono l'accesso al mezzo radio e la consegna affidabile
dei frame. Sono piu corti dei management frame e non contengono un body.

Sottotipi principali:
- **RTS (Request to Send)**: richiesta di prenotazione del canale per evitare
  collisioni in ambienti con nodi nascosti
- **CTS (Clear to Send)**: risposta a RTS, concede l'accesso al canale
- **ACK (Acknowledgment)**: conferma ricezione di un frame unicast
- **Block ACK / Block ACK Request**: conferma aggregata di piu frame
- **PS-Poll**: usato da client in power save per richiedere frame bufferizzati
- **CF-End**: segnala fine del periodo Contention-Free

I control frame sono importanti nel contesto del pentesting perche:
- Un attacco CTS flood puo silenziare un intero canale (ogni dispositivo che riceve
  un CTS rispetta il NAV -- Network Allocation Vector -- e rimane in silenzio)
- I frame ACK possono rivelare la presenza di dispositivi anche quando non trasmettono
  attivamente

**Data Frames (Tipo 2)**

I data frame trasportano il payload effettivo -- il traffico applicativo dell'utente.
In una rete WPA2 il payload e cifrato con AES-CCMP (o TKIP nei sistemi legacy).

Sottotipi rilevanti:
- **Data**: frame dati standard
- **QoS Data**: frame dati con supporto Quality of Service (802.11e)
- **Null Function**: frame senza payload, usato per segnalare stato power management
- **QoS Null**: come sopra, con header QoS

La struttura degli indirizzi nei data frame cambia in base alla direzione del traffico:

```
To DS=0, From DS=0  ->  IBSS (ad-hoc)
    Addr1 = DA, Addr2 = SA, Addr3 = BSSID

To DS=1, From DS=0  ->  Client verso AP
    Addr1 = BSSID, Addr2 = SA, Addr3 = DA

To DS=0, From DS=1  ->  AP verso Client
    Addr1 = DA, Addr2 = BSSID, Addr3 = SA

To DS=1, From DS=1  ->  WDS (bridge tra AP)
    Addr1 = RA, Addr2 = TA, Addr3 = DA, Addr4 = SA
```

### 1.2 Beacon Frames - Il Cuore della Discovery

I beacon frame sono trasmessi periodicamente da ogni AP (di default ogni ~102.4 ms,
cioe circa 10 volte al secondo) e contengono tutte le informazioni necessarie per
un client che cerca reti.

Struttura del body di un beacon frame:

```
+------------------+------------------+------------------+
|  Timestamp       |  Beacon Interval |  Capability Info |
|  (8 byte)        |  (2 byte)        |  (2 byte)        |
+------------------+------------------+------------------+
|  Tagged Parameters (variabili, Information Elements)   |
+--------------------------------------------------------+
```

Information Elements (IE) piu rilevanti:
- **SSID (IE 0)**: nome della rete (puo essere vuoto per reti hidden)
- **Supported Rates (IE 1)**: data rate supportati
- **DS Parameter Set (IE 3)**: canale corrente
- **TIM (IE 5)**: Traffic Indication Map, indica frame bufferizzati per client in PS
- **Country (IE 7)**: regolamentazioni del paese
- **RSN (IE 48)**: Robust Security Network, definisce la suite di cifratura
  (WPA2-Personal, WPA2-Enterprise, WPA3-SAE, cifrari supportati)
- **Vendor Specific (IE 221)**: estensioni proprietarie (WPA1, WPS, ecc.)

L'IE RSN (Robust Security Network) e particolarmente importante per il pentester:

```
RSN Information Element:
+------------------+------------------+
|  Element ID (48) |  Length           |
+------------------+------------------+
|  Version (2)     |  Group Cipher    |
|                  |  Suite (4)       |
+------------------+------------------+
|  Pairwise Count  |  Pairwise Cipher |
|  (2)             |  Suite(s) (4*n)  |
+------------------+------------------+
|  AKM Count (2)   |  AKM Suite(s)    |
|                  |  (4*n)           |
+------------------+------------------+
|  RSN Capabilities (2)              |
+------------------------------------+
```

Dall'RSN IE puoi determinare:
- Se la rete usa CCMP (AES) o TKIP (vulnerabile)
- Se supporta 802.11w (PMF - Protected Management Frames)
- Se usa PSK (Personal) o 802.1X (Enterprise)
- Se WPA3-SAE e supportato/richiesto

> Nota personale: durante un engagement, leggere i beacon frame mi ha permesso di
> identificare un vecchio AP che ancora supportava TKIP come fallback. Quello e
> diventato il mio punto di ingresso. Marauder con lo scan mostra queste informazioni
> in modo compatto, ma sapere cosa significano fa la differenza tra un pentester e
> qualcuno che preme bottoni.

### 1.3 Probe Request e Probe Response

Il meccanismo di probe e il modo attivo con cui i client cercano reti WiFi.

**Probe Request**: un client trasmette un probe request in broadcast (o diretto a un
SSID specifico) per scoprire quali AP sono raggiungibili.

Ci sono due tipi:
1. **Directed Probe**: contiene un SSID specifico -- il client cerca una rete nota.
   Questo rivela le reti a cui il dispositivo si e connesso in passato (privacy leak).
2. **Broadcast Probe (Wildcard)**: SSID vuoto -- il client chiede a tutti gli AP di
   rispondere.

**Probe Response**: l'AP risponde con le stesse informazioni di un beacon frame,
ma in unicast verso il client richiedente.

Implicazioni per il pentesting:
- I probe request directed rivelano la "storia WiFi" di un dispositivo. Se un telefono
  trasmette probe per "Hotel_Roma_WiFi", sai dove e stato il proprietario.
- Questa informazione puo essere usata per creare un Evil Twin mirato: basta creare
  un AP con l'SSID cercato dal client, e il dispositivo potrebbe connettersi
  automaticamente.
- I sistemi operativi moderni (iOS 14+, Android 10+, Windows 10 recente) randomizzano
  il MAC address nei probe per mitigare il tracking, ma non tutti i dispositivi lo
  fanno correttamente.

### 1.4 Autenticazione e Associazione

Il processo di connessione WiFi segue una sequenza precisa:

```
Client                                    AP
  |                                        |
  |  1. Probe Request (opzionale)          |
  |--------------------------------------->|
  |  2. Probe Response (opzionale)         |
  |<---------------------------------------|
  |                                        |
  |  3. Authentication Request             |
  |--------------------------------------->|
  |  4. Authentication Response            |
  |<---------------------------------------|
  |                                        |
  |  5. Association Request                |
  |--------------------------------------->|
  |  6. Association Response               |
  |<---------------------------------------|
  |                                        |
  |  --- 4-Way Handshake (WPA2) ---        |
  |                                        |
  |  7. EAPOL Message 1 (ANonce)           |
  |<---------------------------------------|
  |  8. EAPOL Message 2 (SNonce + MIC)     |
  |--------------------------------------->|
  |  9. EAPOL Message 3 (GTK + MIC)        |
  |<---------------------------------------|
  | 10. EAPOL Message 4 (ACK)              |
  |--------------------------------------->|
  |                                        |
  | === Traffico cifrato ===               |
```

In WPA2-Personal (PSK), l'autenticazione al passo 3-4 e di tipo "Open System"
(cioe non verifica davvero nulla -- la vera autenticazione avviene nel 4-way handshake).

### 1.5 Il 4-Way Handshake WPA2

Il 4-way handshake e il processo critico che stabilisce le chiavi di sessione per
la cifratura del traffico. E anche l'obiettivo principale per il crack offline delle
password WiFi.

**Derivazione delle chiavi:**

```
PSK = PBKDF2-SHA1(Passphrase, SSID, 4096 iterazioni, 256 bit)
     |
     v
PMK (Pairwise Master Key) = PSK  (in WPA2-Personal, PMK == PSK)
     |
     v
PTK = PRF-X(PMK, "Pairwise key expansion",
            Min(AA,SA) || Max(AA,SA) || Min(ANonce,SNonce) || Max(ANonce,SNonce))
     |
     +-> KCK (Key Confirmation Key, 128 bit) -- usata per calcolare il MIC
     +-> KEK (Key Encryption Key, 128 bit) -- usata per cifrare il GTK
     +-> TK  (Temporal Key, 128 bit) -- usata per cifrare il traffico dati
```

Dove:
- AA = Authenticator Address (MAC dell'AP)
- SA = Supplicant Address (MAC del client)
- ANonce = numero random generato dall'AP
- SNonce = numero random generato dal client

**I quattro messaggi EAPOL:**

1. **Messaggio 1 (AP -> Client)**: l'AP invia l'ANonce in chiaro. A questo punto
   il client ha tutto il necessario per calcolare la PTK (conosce gia il PMK
   derivato dalla password, il proprio SNonce che genera localmente, e i MAC address
   di entrambi). Il client calcola la PTK.

2. **Messaggio 2 (Client -> AP)**: il client invia il proprio SNonce e un MIC
   (Message Integrity Code) calcolato con la KCK derivata dalla PTK. L'AP ora ha
   tutto per calcolare la PTK a sua volta e verifica il MIC: se e corretto, il client
   conosce la password corretta.

3. **Messaggio 3 (AP -> Client)**: l'AP invia il GTK (Group Temporal Key, per il
   traffico multicast/broadcast) cifrato con la KEK, piu un MIC. L'AP installa
   la PTK.

4. **Messaggio 4 (Client -> AP)**: il client conferma la ricezione. Il client
   installa la PTK e il GTK. La connessione cifrata e attiva.

**Cosa serve per il crack offline:**

Per tentare un attacco brute force / dizionario offline servono:
- ANonce (dal messaggio 1)
- SNonce (dal messaggio 2)
- MAC dell'AP (AA)
- MAC del client (SA)
- MIC dal messaggio 2 (o 3)

Con questi dati si puo derivare la PTK per ogni password candidata e verificare
se il MIC calcolato corrisponde a quello catturato. Se corrisponde, la password
e stata trovata.

> Nota personale: molti pensano che catturando l'handshake si "cracka" la rete
> in tempo reale. Non e cosi. La cattura e solo il primo passo -- il crack avviene
> offline, sul proprio hardware, e puo richiedere da secondi (password deboli +
> dizionario) a mesi/anni (password complesse + brute force). Con una GPU moderna
> e hashcat si testano circa 500.000+ PMK/s per WPA2, ma una password di 12+
> caratteri casuali resta praticamente inviolabile.

### 1.6 PMKID - L'Attacco Superiore

Scoperto da Jens "atom" Steube (creatore di hashcat) nel 2018, l'attacco PMKID
rappresenta un'evoluzione significativa rispetto alla cattura tradizionale del
4-way handshake.

**Come funziona:**

Nell'RSN IE dei beacon frame, alcuni AP supportano il PMK caching (802.11r/PMK-ID).
Quando un client si associa, l'AP puo includere un PMKID nel primo messaggio EAPOL:

```
PMKID = HMAC-SHA1-128(PMK, "PMK Name" || MAC_AP || MAC_Client)
```

Il PMKID e un hash derivato direttamente dal PMK (che in WPA2-Personal e il PSK,
che a sua volta e derivato dalla password).

**Perche e superiore alla cattura dell'handshake:**

1. **Non richiede un client connesso**: basta che l'AP supporti il PMK caching.
   Si invia un association request e si aspetta il messaggio 1 con il PMKID.
2. **Non richiede deauthentication**: nessun client viene disconnesso, l'attacco
   e completamente passivo dal punto di vista degli utenti della rete.
3. **Piu veloce**: si ottiene il PMKID in pochi secondi, senza dover aspettare
   che un client si riconnetta.
4. **Meno rilevabile**: nessun frame di deauth, nessuna anomalia evidente nel
   traffico.

**Limitazioni:**
- Non tutti gli AP includono il PMKID nel messaggio 1
- Alcuni AP moderni disabilitano il PMK caching di default
- WPA3-SAE non e vulnerabile a questo attacco (usa SAE, che non espone il PMKID)

**Formato per hashcat:**

```
hashcat -m 22000 hash.hc22000 wordlist.txt
```

Il formato .hc22000 e il formato unificato di hashcat 6.0+ che supporta sia
handshake che PMKID nella stessa struttura.

> Nota personale: il PMKID e il primo attacco che provo sempre su una rete WPA2
> target. Se l'AP lo supporta, ho il materiale per il crack in 10 secondi senza
> disturbare nessuno. Solo se PMKID fallisce passo alla cattura dell'handshake
> con deauth. E una questione di OPSEC: meno rumore fai, meglio e.

---

