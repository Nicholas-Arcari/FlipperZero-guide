## 5. Funzionalita Principali - Dettaglio Completo

### 5.1 Scan - WiFi Discovery

Lo scan e la prima operazione in qualsiasi engagement wireless. Corrisponde alla
fase di ricognizione nel framework PTES (Penetration Testing Execution Standard).

**Scan AP (Access Point Discovery):**

Comando Marauder: `scanap`

L'ESP32 esegue una scansione attiva e passiva su tutti i canali 2.4 GHz (1-14,
a seconda della regione) e raccoglie i beacon frame degli AP rilevati.

Per ogni AP vengono mostrati:
- **SSID**: nome della rete (vuoto per reti hidden -- ma il BSSID e comunque visibile)
- **BSSID**: indirizzo MAC dell'AP (identifica univocamente il dispositivo)
- **Canale**: canale di operazione (1-14)
- **RSSI**: Received Signal Strength Indicator in dBm (piu vicino a 0 = segnale
  piu forte; -30 dBm = eccellente, -50 dBm = buono, -70 dBm = debole,
  -80 dBm = marginale, sotto -85 dBm = inutilizzabile)
- **Cifratura**: Open, WEP, WPA, WPA2-Personal, WPA2-Enterprise, WPA3

**Scan Client (Station Discovery):**

Comando Marauder: `scansta`

Dopo aver identificato gli AP, la scansione dei client rivela i dispositivi
connessi a ciascuna rete.

Per ogni client vengono mostrati:
- MAC address del client
- AP a cui e associato
- RSSI del client

**Interpretazione tattica dei risultati:**

Come pentester, dalla scansione si estraggono informazioni critiche:

1. **Superficie di attacco**: quanti AP, quanti client, quale cifratura
2. **Target prioritari**: AP con cifratura debole (WEP, WPA1, WPA2 senza PMF)
3. **Densita di client**: AP con molti client = piu probabilita di catturare handshake
4. **Reti hidden**: SSID vuoto ma BSSID presente -- possono essere scoperte tramite
   probe response quando un client si connette
5. **Canale meno affollato**: se devi operare un rogue AP, scegli un canale libero
6. **Vendor identification**: i primi 3 byte del MAC (OUI) identificano il produttore.
   Questo rivela modello approssimativo dell'AP (Cisco, Ubiquiti, TP-Link, ecc.)

```
Esempio output scansione:
----------------------------------------------
#   SSID             BSSID              CH  RSSI  ENC
1   OfficeNet-5G     AA:BB:CC:DD:EE:01  6   -42   WPA2
2   Guest_WiFi       AA:BB:CC:DD:EE:02  1   -55   WPA2
3   (hidden)         AA:BB:CC:DD:EE:03  11  -68   WPA2
4   IoT_Sensors      AA:BB:CC:DD:EE:04  6   -71   Open
5   Printer_HP       AA:BB:CC:DD:EE:05  1   -75   WPA2
----------------------------------------------
```

In questo esempio, un pentester noterebbe immediatamente:
- "IoT_Sensors" e una rete aperta -- accesso diretto senza autenticazione
- La rete hidden sul canale 11 merita indagine
- "OfficeNet-5G" e il target principale (segnale forte, WPA2)
- "Guest_WiFi" potrebbe avere isolamento client disabilitato

> Nota personale: la scansione iniziale la faccio sempre dal parcheggio o dalla
> reception dell'edificio target. Il Flipper in tasca con il devboard collegato
> e completamente discreto. In 60 secondi ho la mappa completa delle reti,
> senza nemmeno tirare fuori un laptop. Poi analizzo i risultati con calma
> e pianifico i prossimi passi.

### 5.2 Sniff - Packet Monitoring

Lo sniffing WiFi con Marauder permette di catturare frame raw dall'etere radio.
A differenza dello scan (che elabora i dati), lo sniffer cattura i pacchetti grezzi
e li salva per analisi successiva.

**Tipi di sniffing disponibili:**

**Sniff Raw:**

Comando: `sniffraw`

Cattura tutti i frame su un canale specifico o in channel hopping. I frame vengono
salvati in formato .pcap sulla SD card del Flipper.

Il file .pcap puo essere analizzato con:
- **Wireshark**: filtri utili per analisi WiFi:
  - `wlan.fc.type == 0` -- solo management frame
  - `wlan.fc.type_subtype == 0x08` -- solo beacon
  - `wlan.fc.type_subtype == 0x0c` -- solo deauth
  - `wlan.fc.type_subtype == 0x04` -- solo probe request
  - `eapol` -- solo frame EAPOL (handshake)
  - `wlan.bssid == AA:BB:CC:DD:EE:FF` -- filtra per AP specifico

**Sniff Beacon:**

Comando: `sniffbeacon`

Cattura specificamente i beacon frame. Utile per:
- Analisi dettagliata delle configurazioni degli AP
- Rilevamento di rogue AP (AP non autorizzati)
- Monitoraggio della stabilita di un AP (beacon loss)
- Analisi degli IE (Information Elements) per fingerprinting dell'AP

**Sniff Deauth:**

Comando: `sniffdeauth`

Monitora specificamente i frame di deautenticazione. Questo e utile per:
- Rilevare se qualcuno sta attaccando la rete (WIDS passivo)
- Verificare se sono in corso attacchi deauth nell'ambiente
- Debugging di problemi di disconnessione

**Sniff Probe:**

Comando: `sniffprobe`

Cattura i probe request dei dispositivi nelle vicinanze. Ogni probe rivela:
- MAC address del dispositivo (potenzialmente randomizzato)
- SSID cercato (se directed probe)
- Supported rates del dispositivo

Questo e un'operazione di intelligence gathering: rivela quali reti i dispositivi
nelle vicinanze hanno memorizzato. In un hotel, un aeroporto, una sala conferenze,
i probe request possono rivelare:
- Nomi di reti aziendali ("CorpNet-Acme_Inc")
- Reti di hotel visitati ("Hilton_WiFi_Room412")
- Reti domestiche ("Casa_Mario_5G")

**Sniff EAPOL:**

Comando: `sniffeapol`

Cattura specificamente i frame EAPOL (Extensible Authentication Protocol over LAN),
cioe i messaggi del 4-way handshake WPA2. Questa e la cattura piu preziosa per
il crack offline delle password.

Il file .pcap risultante contiene i frame EAPOL che possono essere convertiti in
formato hashcat con lo strumento `hcxpcapngtool`:

```bash
hcxpcapngtool -o hash.hc22000 capture.pcap
hashcat -m 22000 hash.hc22000 wordlist.txt
```

**Sniff PMKID:**

Comando: `sniffpmkid`

Cattura specificamente il PMKID dal primo messaggio EAPOL. L'ESP32 invia un
association request all'AP target e aspetta la risposta contenente il PMKID.

> Nota personale: uso lo sniff EAPOL in combinazione con il deauth. Prima avvio
> lo sniffer EAPOL su un canale specifico, poi lancio un deauth mirato per forzare
> la riconnessione di un client. In questo modo catturo l'handshake completo in
> pochi secondi. La chiave e avere lo sniffer GIA attivo prima del deauth,
> altrimenti si perde il primo messaggio.

### 5.3 Deauth Attack

L'attacco di deautenticazione e probabilmente la funzione piu nota e piu usata
(e abusata) di Marauder. E anche la piu pericolosa dal punto di vista legale.

**Come funziona tecnicamente:**

Il frame di deautenticazione e un management frame con subtype 0x0C. In 802.11
originale (senza 802.11w/PMF), i management frame non sono autenticati ne cifrati.

Questo significa che chiunque puo forgiare un frame di deautenticazione con:
- Source address = MAC dell'AP (spoofato)
- Destination address = MAC del client target (o FF:FF:FF:FF:FF:FF per broadcast)
- Reason code: valore numerico che indica il motivo della deautenticazione

```
Deauthentication Frame:
+------------------+------------------+------------------+
|  Frame Control   |  Duration        |  DA (client MAC) |
|  Type=0, Sub=12  |                  |  o broadcast     |
+------------------+------------------+------------------+
|  SA (AP MAC)     |  BSSID (AP MAC)  |  Seq Control     |
|  (spoofato)      |                  |                  |
+------------------+------------------+------------------+
|  Reason Code (2 byte)              |  FCS             |
+------------------------------------+------------------+
```

Reason code comuni:
- 1: Unspecified reason
- 2: Previous authentication no longer valid
- 3: Deauthenticated because sending station is leaving
- 4: Disassociated due to inactivity
- 6: Class 2 frame received from nonauthenticated station
- 7: Class 3 frame received from nonassociated station

L'AP e il client, ricevendo il frame, credono che l'altra parte abbia terminato
la connessione e si disconnettono. Il client tipicamente tenta immediatamente
la riconnessione, generando un nuovo 4-way handshake -- che e esattamente cio
che il pentester vuole catturare.

**Modalita di targeting in Marauder:**

1. **Deauth su AP specifico**: disconnette tutti i client di un singolo AP
   - Selezionare l'AP dalla lista di scansione
   - Avviare il deauth

2. **Deauth su client specifico**: disconnette un singolo client da un AP
   - Richiede la coppia (AP MAC, Client MAC)
   - Piu mirato, meno rumoroso

3. **Deauth broadcast**: frame deauth con DA = FF:FF:FF:FF:FF:FF
   - Disconnette tutti i client dall'AP target
   - Piu efficace ma piu rumoroso e rilevabile

4. **Deauth multi-target**: attacco simultaneo su piu AP/client
   - Utile per massimizzare la probabilita di cattura handshake
   - Estremamente rumoroso -- da usare solo in lab

**Contromisure (che il pentester deve conoscere):**

1. **802.11w (PMF - Protected Management Frames)**: cifra i management frame
   critici (deauth, disassoc). Se attivo, il deauth spoofato viene scartato
   dal client. WPA3 lo richiede obbligatoriamente.

2. **WIDS/WIPS (Wireless Intrusion Detection/Prevention System)**: sistemi come
   Cisco Adaptive wIPS, Aruba RFProtect, AirMagnet Enterprise rilevano
   immediatamente i deauth flood. Il pattern e inconfondibile: raffica di
   frame deauth dallo stesso BSSID in pochi secondi.

3. **Client-side protection**: alcuni driver WiFi moderni ignorano i deauth
   broadcast o implementano un delay prima di disconnettersi.

4. **Rate limiting**: alcuni AP implementano throttling sui management frame.

**Rischi legali:**

L'invio di frame di deautenticazione su reti non proprie e illegale in Italia e
in tutta l'UE. Costituisce interferenza illecita con un sistema informatico e
violazione delle comunicazioni. Le sanzioni includono fino a 4 anni di reclusione
(art. 617-quater c.p.). Non e un rischio teorico: ci sono stati procedimenti penali
per attacchi deauth.

> Nota personale: il deauth e lo strumento piu usato per forzare la cattura di
> un handshake, ma e anche il piu rumoroso. In un engagement reale, se il cliente
> ha un WIDS (e qualsiasi rete enterprise ce l'ha), vieni rilevato in 3 secondi.
> Il mio approccio: primo tentativo sempre con PMKID (zero rumore). Solo se fallisce,
> un singolo deauth mirato (non broadcast) su un client specifico, con lo sniffer
> EAPOL gia attivo. Mai deauth flood. Mai deauth broadcast in ambiente enterprise.

### 5.4 Beacon Spam

Il beacon spam genera beacon frame fasulli per creare l'illusione di decine o
centinaia di reti WiFi nell'area circostante.

**Come funziona:**

L'ESP32 genera e trasmette beacon frame con:
- SSID personalizzabili
- BSSID generati casualmente (o sequenziali)
- Parametri realistici (RSN IE, supported rates, DS parameter set)
- Beacon interval standard (100 TU)

I dispositivi che scansionano le reti vedranno apparire tutte queste reti fake
nella loro lista WiFi.

**Modalita disponibili:**

1. **Random SSID**: genera nomi casuali di reti
   - Comando: `attack -t beacon -r`
   - Utile per test di stress su client

2. **Rickroll SSID List**: genera AP con nomi che compongono il testo di
   "Never Gonna Give You Up" di Rick Astley
   - Comando: `attack -t beacon -l rickroll`
   - Classico meme della community hacking

3. **Custom SSID List**: genera AP con nomi personalizzati caricati da file
   - Comando: `attack -t beacon -l custom`
   - Il file con gli SSID va caricato sulla SD card
   - Utile per scenari specifici di social engineering

**Uso nel penetration testing e social engineering:**

Il beacon spam ha applicazioni serie nel pentesting:

1. **Confusione dell'utente**: in un ufficio, creare decine di reti con nomi simili
   a quella legittima ("Company_WiFi", "Company-WiFi", "Company_WiFi_5G",
   "Company_WiFi_Guest") puo indurre gli utenti a connettersi alla rete sbagliata
   (specialmente se combinato con Evil Portal).

2. **Test di policy**: verificare se i dispositivi aziendali hanno policy che
   impediscono la connessione a reti non approvate. Se un laptop aziendale
   tenta di connettersi a un fake AP, la policy MDM e inadeguata.

3. **Distrazione**: durante un red team engagement, il beacon spam puo saturare
   le console del SOC mentre si opera su un altro vettore.

4. **Test WIDS**: verificare se il sistema WIDS rileva e segnala la comparsa
   improvvisa di decine di AP sconosciuti.

**Aspetti tecnici del beacon generation:**

L'ESP32 puo generare circa 50-100 beacon diversi in modo credibile, limitato dalla:
- Velocita di trasmissione (ogni beacon richiede tempo di airtime)
- Memoria disponibile per le strutture beacon
- Necessita di mantenere il beacon interval realistico (se troppo lento, i client
  non elencano la rete; se troppo veloce, e ovviamente artificiale)

> Nota personale: ho usato il beacon spam in un engagement per testare se il team
> IT del cliente monitorava l'ambiente wireless. Ho generato 50 AP con nomi
> simili alla rete corporate. Risultato: nessun allarme per 48 ore. Quello e
> finito nel report come finding critico -- assenza di monitoraggio wireless.

### 5.5 Probe Flood

Il probe flood genera un numero massiccio di probe request per saturare gli AP
nella zona.

**Come funziona:**

L'ESP32 trasmette probe request con:
- MAC address source randomizzati (simula centinaia di client)
- SSID variabili o broadcast
- Rate massimo di trasmissione

**Effetti:**

1. **Saturazione AP**: gli AP devono processare ogni probe request e rispondere
   con un probe response. Un flood di probe puo:
   - Aumentare il carico CPU dell'AP
   - Ridurre le performance per i client legittimi
   - In casi estremi, causare il riavvio di AP economici

2. **Inquinamento log**: i log dell'AP si riempiono di probe da MAC fittizi,
   rendendo difficile l'analisi forense

3. **Stress test**: verificare la resilienza dell'infrastruttura wireless sotto
   carico anomalo

**Rilevabilita:**

Il probe flood e facilmente rilevabile da qualsiasi WIDS perche:
- Volume anomalo di probe request
- MAC address source senza OUI valido (o con OUI di chip inesistenti)
- Pattern temporale innaturale (probe ogni pochi millisecondi)

### 5.6 Evil Portal

L'Evil Portal e lo strumento piu potente per il social engineering via WiFi
in Marauder. Combina un rogue AP con un captive portal per intercettare
credenziali.

**Come funziona - Architettura completa:**

```
[Vittima]                    [ESP32 Marauder]              [Internet]
    |                              |                            |
    |  1. Si connette al fake AP   |                            |
    |----------------------------->|                            |
    |                              |                            |
    |  2. Richiesta DNS qualsiasi  |                            |
    |----------------------------->|                            |
    |                              |                            |
    |  3. DNS Spoofing: risponde   |                            |
    |     con IP dell'ESP32        |                            |
    |<-----------------------------|                            |
    |                              |                            |
    |  4. HTTP Request al portale  |                            |
    |----------------------------->|                            |
    |                              |                            |
    |  5. Pagina di login fake     |                            |
    |<-----------------------------|                            |
    |                              |                            |
    |  6. Vittima inserisce cred.  |                            |
    |----------------------------->|                            |
    |                              |                            |
    |  7. Credenziali salvate      |                            |
    |  su SD card                  |                            |
    |                              |                            |
```

**Step 1 - Rogue AP:**

L'ESP32 crea un AP con un SSID scelto dall'attaccante. In un contesto di
pentesting, si sceglie un nome che la vittima si aspetta di trovare:
- "Hotel_WiFi_Free" in un hotel
- "Airport_Free_WiFi" in un aeroporto
- "CompanyName_Guest" in un ufficio
- Il nome ESATTO della rete legittima (Evil Twin)

L'AP viene creato senza cifratura (Open) per permettere la connessione senza
password.

**Step 2/3 - DNS Spoofing:**

L'ESP32 esegue un DNS server che risponde a QUALSIASI query DNS con il proprio
indirizzo IP. Quando il dispositivo della vittima tenta di risolvere qualsiasi
dominio (google.com, facebook.com, ecc.), riceve l'IP dell'ESP32.

Questo meccanismo e lo stesso usato dai captive portal legittimi (hotel, aeroporti):
il dispositivo rileva che non ha connettivita Internet reale e apre
automaticamente il browser del captive portal.

Su iOS e Android, la rilevazione del captive portal avviene tramite:
- **iOS**: richiesta HTTP a `captive.apple.com/hotspot-detect.html`
- **Android**: richiesta HTTP a `connectivitycheck.gstatic.com/generate_204`
  o `clients3.google.com/generate_204`
- **Windows**: richiesta HTTP a `www.msftconnecttest.com/connecttest.txt`

Se la risposta non corrisponde a quella attesa, il sistema operativo mostra
automaticamente il browser del captive portal con la pagina dell'attaccante.

**Step 4/5 - Pagina di Phishing:**

L'ESP32 serve una pagina web HTML/CSS che simula una pagina di login. Le pagine
possono essere personalizzate e caricate sulla SD card.

Esempi di template:
- Login Google/Microsoft (raccolta credenziali email)
- Pagina di accesso WiFi dell'hotel (raccolta dati personali)
- Pagina di login del portale aziendale
- Pagina di aggiornamento firmware (ingegneria sociale per installare malware)

**Creazione di un template custom:**

Il template e un file HTML standard. L'ESP32 ha risorse limitate, quindi:
- Mantenere l'HTML/CSS semplice (no framework pesanti)
- Includere il CSS inline (non caricare fogli di stile esterni)
- Le immagini devono essere base64-encoded inline o molto piccole
- Il form deve fare POST all'indirizzo dell'ESP32

Struttura base di un template:

```html
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>WiFi Login</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: #f5f5f5;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            margin: 0;
        }
        .login-box {
            background: white;
            padding: 40px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            max-width: 400px;
            width: 90%;
        }
        input {
            width: 100%;
            padding: 12px;
            margin: 8px 0;
            border: 1px solid #ddd;
            border-radius: 4px;
            box-sizing: border-box;
        }
        button {
            width: 100%;
            padding: 12px;
            background: #4285f4;
            color: white;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 16px;
        }
    </style>
</head>
<body>
    <div class="login-box">
        <h2>WiFi Access</h2>
        <p>Inserisci le tue credenziali per accedere a Internet</p>
        <form method="POST" action="/login">
            <input type="email" name="email" placeholder="Email" required>
            <input type="password" name="password" placeholder="Password" required>
            <button type="submit">Accedi</button>
        </form>
    </div>
</body>
</html>
```

**Step 6/7 - Credential Harvesting:**

Quando la vittima compila il form e preme "Accedi", le credenziali vengono:
1. Ricevute dall'ESP32 via HTTP POST
2. Salvate in un file sulla SD card del Flipper
3. Visualizzate (opzionalmente) sullo schermo del Flipper

Il file delle credenziali catturate e tipicamente in:
```
/ext/apps_data/marauder/portal_creds.txt
```

**Considerazioni avanzate sull'Evil Portal:**

1. **HTTPS**: l'ESP32 non puo servire HTTPS con certificati validi. I browser
   moderni mostrano avvisi di sicurezza. Tuttavia, per i captive portal,
   la maggior parte degli utenti non nota (o ignora) l'assenza di HTTPS
   perche e normale per le pagine di login WiFi.

2. **HSTS**: se la vittima ha visitato un sito con HSTS (HTTP Strict Transport
   Security), il browser rifiutera la connessione HTTP. Questo limita
   l'efficacia contro utenti che visitano frequentemente siti con HSTS.

3. **Durata**: l'Evil Portal deve restare attivo per il tempo necessario.
   La batteria del Flipper con il devboard collegato dura circa 2-4 ore
   (dipende dal carico).

4. **Realismo**: la qualita del template determina il successo. Un template
   che replica fedelmente il portale WiFi del luogo in cui si opera
   (hotel, conferenza, ufficio) ha un tasso di successo molto superiore.

> Nota personale: l'Evil Portal e lo strumento che ha prodotto i risultati
> piu impressionanti nei miei engagement. In un test per un hotel, ho creato
> un portale che replicava esattamente la pagina di login WiFi dell'hotel
> (stessi colori, logo, font). In 4 ore ho catturato 23 set di credenziali
> email valide. Il report ha evidenziato come l'assenza di WPA2-Enterprise
> e la mancanza di educazione degli ospiti creassero un rischio concreto.
> L'hotel ha successivamente implementato WPA2-Enterprise con autenticazione
> via room number + cognome.

### 5.7 PMKID Attack

Come descritto nella sezione teorica, l'attacco PMKID e il metodo preferito
per ottenere materiale per il crack offline di WPA2 senza disturbare i client.

**Procedura operativa con Marauder:**

1. Eseguire una scansione AP: `scanap`
2. Identificare il target (deve essere WPA2-Personal)
3. Selezionare il target
4. Avviare la cattura PMKID: `sniffpmkid`
5. L'ESP32 invia un association request all'AP
6. Se l'AP supporta PMK caching, risponde con il PMKID nel messaggio 1
7. Il PMKID viene catturato e salvato sulla SD card
8. Interrompere la cattura: `stopscan`

**Analisi del risultato:**

Il PMKID catturato viene salvato in un formato compatibile con hashcat.
La struttura del PMKID e:

```
PMKID*MAC_AP*MAC_CLIENT*SSID_HEX
```

Esempio:
```
2582a8281bf9d4308d6f5731d0e61c61*aabbccddeeff*112233445566*4f66666963654e6574
```

**Crack con hashcat:**

```bash
# Conversione (se necessario)
hcxpcapngtool -o hash.hc22000 capture.pcap

# Crack con dizionario
hashcat -m 22000 hash.hc22000 /usr/share/wordlists/rockyou.txt

# Crack con regole
hashcat -m 22000 hash.hc22000 wordlist.txt -r rules/best64.rule

# Crack con maschera (brute force pattern)
hashcat -m 22000 hash.hc22000 -a 3 ?d?d?d?d?d?d?d?d  # 8 cifre

# Stato del crack
hashcat -m 22000 hash.hc22000 --show
```

**Performance di crack (stime indicative):**

| Hardware | Velocita approssimativa |
|----------|-------------------------|
| CPU (i7 recente) | ~20.000 PMK/s |
| GPU NVIDIA RTX 3080 | ~800.000 PMK/s |
| GPU NVIDIA RTX 4090 | ~1.500.000 PMK/s |
| 4x RTX 4090 (rig) | ~6.000.000 PMK/s |

Con queste velocita:
- Password di 8 cifre (10^8 = 100M combinazioni): ~67 secondi con RTX 4090
- Password di 8 caratteri lowercase (26^8 = 208B): ~38 ore con RTX 4090
- Password di 8 caratteri misti (62^8 = 218T): ~4.5 anni con RTX 4090
- Password di 12 caratteri misti: computazionalmente impossibile con tecnologia attuale

**Quando PMKID non funziona:**

- L'AP non supporta PMK caching (nessun PMKID nel messaggio 1)
- L'AP usa WPA3-SAE (immune all'attacco)
- L'AP ha PMF (802.11w) abilitato con MFPR (Management Frame Protection Required)
- L'AP rifiuta l'association request (rate limiting o MAC filtering)

In questi casi, si passa alla cattura dell'handshake tradizionale (sezione 5.8).

> Nota personale: nella mia esperienza, circa il 60-70% degli AP WPA2-Personal
> risponde con il PMKID. Il restante 30-40% richiede il metodo tradizionale
> con deauth. Inizio sempre con PMKID perche e silenzioso e veloce. Se dopo
> 30 secondi non ottengo risultato, passo al piano B.

### 5.8 Handshake Capture (4-Way Handshake WPA2)

La cattura tradizionale del 4-way handshake e il metodo classico per ottenere
il materiale necessario al crack offline di password WPA2.

**Procedura operativa con Marauder:**

La procedura richiede la combinazione di due funzioni: sniff EAPOL + deauth.

1. Eseguire scansione AP e client:
   ```
   scanap
   scansta
   ```

2. Identificare il target:
   - AP con WPA2-Personal
   - Almeno un client connesso (necessario -- senza client, niente handshake)
   - Segnale decente (RSSI > -75 dBm sia per l'AP che per il client)

3. Annotare il canale dell'AP target e assicurarsi che lo sniffer operi sullo
   stesso canale

4. Avviare lo sniff EAPOL:
   ```
   sniffeapol
   ```

5. Avviare il deauth mirato sull'AP target (o meglio, sul client specifico):
   ```
   attack -t deauth
   ```
   Selezionare l'AP o il client dalla lista.

6. Il deauth forza la disconnessione del client. Il client si riconnette
   automaticamente, generando un nuovo 4-way handshake.

7. Lo sniffer EAPOL cattura i 4 messaggi e li salva nel file .pcap.

8. Fermare tutto:
   ```
   stopscan
   ```

9. Estrarre il file .pcap dalla SD card del Flipper.

**Verifica della cattura:**

Non tutti gli handshake catturati sono utilizzabili. Per essere valido, il .pcap deve
contenere almeno i messaggi 1 e 2 (meglio tutti e 4):

```bash
# Verifica con aircrack-ng
aircrack-ng capture.pcap
# Dovrebbe mostrare "1 handshake" per la rete target

# Verifica con Wireshark
# Filtro: eapol
# Dovrebbero apparire 4 frame EAPOL per la coppia AP-Client

# Conversione per hashcat
hcxpcapngtool -o hash.hc22000 capture.pcap
# Dovrebbe riportare "EAPOL pairs written"
```

**Problemi comuni nella cattura:**

| Problema | Causa | Soluzione |
|----------|-------|-----------|
| Nessun handshake catturato | Sniffer su canale sbagliato | Verificare canale AP e fissare lo sniffer sullo stesso |
| Handshake incompleto (solo msg 1-2) | Client troppo lontano | Avvicinarsi al client, non all'AP |
| Handshake non crackabile | MIC corrotto da interferenze | Ripetere la cattura con segnale migliore |
| Client non si riconnette | PMF abilitato, deauth ignorato | Provare con client diverso o attendere riconnessione naturale |
| Troppi frame, confusione | Canale affollato | Filtrare per BSSID specifico nell'analisi |

**Crack dell'handshake:**

Identico al crack del PMKID (stessa modalita hashcat -m 22000), dato che il
formato .hc22000 e unificato.

Con aircrack-ng (alternativa senza GPU):

```bash
# Crack con dizionario
aircrack-ng -w /usr/share/wordlists/rockyou.txt capture.pcap

# Crack con dizionario personalizzato
aircrack-ng -w custom_wordlist.txt -b AA:BB:CC:DD:EE:FF capture.pcap
```

Hashcat e superiore ad aircrack-ng per il crack perche supporta GPU acceleration,
regole di mutazione, attacchi combinati e maschere.

> Nota personale: la cattura dell'handshake e un'arte che richiede pratica. Le
> prime volte ci ho messo decine di tentativi per ottenere un handshake pulito.
> I fattori critici: posizione fisica (devi essere a portata sia dell'AP che del
> client), timing (lo sniffer deve essere attivo PRIMA del deauth), e canale
> (deve essere corretto). Un errore comune e lanciare il deauth prima dello
> sniffer: i messaggi 1-2 dell'handshake avvengono in millisecondi dopo la
> riconnessione, e se lo sniffer non e gia in ascolto li perdi.

### 5.9 Wardriving

Il wardriving e la pratica di spostarsi fisicamente in un'area per mappare
le reti WiFi presenti. Con il Flipper e Marauder e possibile fare wardriving
basilare.

**Come funziona con Marauder:**

1. Collegare un modulo GPS al Flipper (se disponibile) o usare il GPS dello
   smartphone via BLE
2. Avviare la scansione continua
3. Spostarsi nell'area target (a piedi, in auto, in bicicletta)
4. I risultati vengono salvati con coordinate GPS

**Formato di output - WiGLE CSV:**

I dati vengono salvati in formato CSV compatibile con WiGLE (Wireless Geographic
Logging Engine), il database mondiale di reti WiFi:

```csv
MAC,SSID,AuthMode,FirstSeen,Channel,RSSI,CurrentLatitude,CurrentLongitude,AltitudeMeters,AccuracyMeters,Type
AA:BB:CC:DD:EE:FF,OfficeNet,WPA2,2024-01-15 10:30:22,6,-42,41.9028,12.4964,50,10,WIFI
```

Campi:
- MAC: BSSID dell'AP
- SSID: nome della rete
- AuthMode: tipo di cifratura
- FirstSeen: timestamp della prima rilevazione
- Channel: canale
- RSSI: potenza del segnale
- CurrentLatitude/Longitude: coordinate GPS
- Type: WIFI (per reti WiFi)

**Upload su WiGLE:**

I file CSV possono essere caricati su https://wigle.net per contribuire al
database globale o per analisi sulla mappa.

**Applicazioni nel penetration testing:**

1. **Ricognizione perimetrale**: mappare tutte le reti WiFi di un campus
   aziendale, identificando:
   - Reti corporate
   - Reti guest
   - Reti IoT
   - Reti rogue (AP non autorizzati installati da dipendenti)
   - Punti deboli nel perimetro (reti con segnale che "esce" dall'edificio)

2. **Coverage analysis**: determinare da dove e possibile raggiungere
   le reti target. Se il segnale della rete corporate e forte nel parcheggio
   esterno, un attaccante puo operare comodamente dalla propria auto.

3. **Storico**: ripetere il wardriving a distanza di tempo per identificare
   cambiamenti nell'infrastruttura wireless.

**Limitazioni del wardriving con Flipper:**

- GPS non integrato (richiede modulo esterno)
- Antenna ESP32 limitata (perde reti con segnale debole che un laptop
  con antenna esterna rileverebbe)
- Schermo piccolo, difficile consultare i risultati sul campo
- Autonomia limitata dalla batteria

Per wardriving professionale, strumenti come Kismet su laptop con GPS USB
e antenna esterna rimangono superiori. Il Flipper e utile per ricognizione
rapida e discreta.

> Nota personale: uso il wardriving con Flipper solo per la ricognizione
> iniziale "walk-by" di un edificio target. Passeggio attorno al perimetro
> con il Flipper in tasca e in 15 minuti ho la mappa delle reti visibili
> dall'esterno. Per il wardriving serio (citta intera, area industriale),
> uso un Raspberry Pi 4 con Kismet, GPS USB e antenna Alfa da 9 dBi montata
> in auto. Il Flipper non puo competere in quel contesto.

---

