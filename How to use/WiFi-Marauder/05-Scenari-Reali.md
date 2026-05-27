## 6. Scenari di Penetration Testing

### 6.1 Scenario 1: Ricognizione Wireless di un Edificio Target

**Contesto**: il cliente ha commissionato un penetration test sulla sicurezza
della propria infrastruttura wireless. Il primo giorno e dedicato alla
ricognizione.

**Obiettivo**: mappare completamente l'infrastruttura WiFi del target senza
essere rilevati, raccogliendo informazioni su reti, cifrature, dispositivi
e potenziali vulnerabilita.

**Fase 1 - Ricognizione esterna (30 min)**

Equipaggiamento: Flipper Zero + devboard ESP32, in tasca o zaino.

1. Passeggiata attorno al perimetro dell'edificio
2. Avvio scansione AP dal Flipper:
   ```
   scanap
   ```
3. Ripetere da almeno 4 posizioni (4 lati dell'edificio) per massimizzare
   la copertura
4. Per ogni posizione, annotare mentalmente RSSI e nome delle reti visibili

**Fase 2 - Analisi dei risultati**

Dall'output della scansione, creare una matrice:

```
+----+-------------------+--------+-----------+---------+
| #  | SSID              | Canale | Cifratura | RSSI    |
+----+-------------------+--------+-----------+---------+
| 1  | Corp_WiFi         | 6      | WPA2-ENT  | -45     |
| 2  | Corp_Guest        | 1      | WPA2-PSK  | -48     |
| 3  | Corp_IoT          | 11     | WPA2-PSK  | -62     |
| 4  | (hidden)          | 6      | WPA2-PSK  | -70     |
| 5  | HP_Printer_LAN    | 1      | Open      | -72     |
| 6  | SecurityCam       | 11     | WEP       | -78     |
+----+-------------------+--------+-----------+---------+
```

**Fase 3 - Analisi tattica**

Da questa scansione un pentester esperto identifica:

1. **Corp_WiFi (WPA2-Enterprise)**: rete principale, difficile da attaccare
   direttamente. Richiede credenziali di dominio o certificato client.
   Possibile attacco: Evil Twin con certificato self-signed per catturare
   hash NTLM (MS-CHAPv2).

2. **Corp_Guest (WPA2-PSK)**: rete guest con password condivisa. Target
   prioritario per PMKID/handshake. La password potrebbe essere debole
   ("Guest2024", "Welcome1", ecc.) ed essere condivisa con visitatori.

3. **Corp_IoT (WPA2-PSK)**: rete dedicata IoT. Se isolata correttamente,
   bassa priorita. Se non isolata, potrebbe fornire accesso alla rete
   interna dopo il crack della password.

4. **Rete hidden**: merita indagine. "Security through obscurity" suggerisce
   una rete sensibile. Intercettando i probe response quando un client
   si connette, l'SSID viene rivelato.

5. **HP_Printer_LAN (Open)**: rete aperta della stampante. Accesso diretto.
   Da li, possibile lateral movement se la stampante ha interfacce sulla
   rete corporate.

6. **SecurityCam (WEP)**: WEP e rotto da 20 anni. Crack istantaneo con
   aircrack-ng. Accesso alle telecamere di sicurezza = finding critico.

**Fase 4 - Scansione client**

```
scansta
```

Identificare quanti dispositivi sono connessi a ciascuna rete. Reti con
molti client = piu visibilita nell'ambiente.

**Output del report (esempio):**

```
FINDING: Rete IoT con cifratura WPA2-PSK accessibile dall'esterno
  Severita: Alta
  Descrizione: La rete Corp_IoT e raggiungibile dal parcheggio con RSSI -62
  Rischio: Un attaccante potrebbe tentare il crack offline della PSK
  Raccomandazione: Ridurre la potenza di trasmissione, implementare 802.11w

FINDING: Telecamere di sicurezza su WEP
  Severita: Critica
  Descrizione: La rete SecurityCam utilizza WEP, crackabile in secondi
  Rischio: Accesso non autorizzato al feed delle telecamere
  Raccomandazione: Migrare immediatamente a WPA2/WPA3

FINDING: Rete aperta della stampante
  Severita: Alta
  Descrizione: La stampante HP espone una rete Open senza autenticazione
  Rischio: Accesso diretto alla stampante, potenziale pivot sulla rete interna
  Raccomandazione: Disabilitare WiFi Direct, connettere la stampante via cavo
```

### 6.2 Scenario 2: Cattura Handshake WPA2 per Crack Offline

**Contesto**: il cliente ha autorizzato il test della robustezza delle password
WiFi della rete guest "Corp_Guest" (WPA2-PSK).

**Obiettivo**: catturare il materiale crittografico necessario per tentare
il crack offline della password.

**Fase 1 - Tentativo PMKID (silenzioso)**

1. Scansione AP per identificare il target:
   ```
   scanap
   ```
   Selezionare "Corp_Guest"

2. Tentativo cattura PMKID:
   ```
   sniffpmkid
   ```

3. Attendere 15-30 secondi

4. Se PMKID catturato: successo, procedere al crack. Nessun impatto sugli utenti.

5. Se PMKID non disponibile: procedere alla Fase 2.

**Fase 2 - Cattura handshake via deauth (se PMKID fallisce)**

1. Scansione client per identificare dispositivi connessi a Corp_Guest:
   ```
   scansta
   ```

2. Selezionare un client con buon segnale

3. Avviare sniffer EAPOL:
   ```
   sniffeapol
   ```
   Verificare che il canale sia corretto.

4. Attendere 2-3 secondi che lo sniffer sia operativo

5. Inviare un singolo frame deauth al client selezionato (non broadcast):
   ```
   attack -t deauth
   ```

6. Il client si disconnette e si riconnette automaticamente in 1-5 secondi

7. Lo sniffer cattura l'handshake (4 messaggi EAPOL)

8. Fermare tutto:
   ```
   stopscan
   ```

9. Verificare la cattura: estrarre il .pcap dalla SD card

**Fase 3 - Crack offline**

Sul proprio hardware (non sul Flipper):

```bash
# Conversione formato
hcxpcapngtool -o corp_guest.hc22000 capture.pcap

# Verifica
hashcat -m 22000 corp_guest.hc22000 --show

# Tentativo 1: dizionario standard
hashcat -m 22000 corp_guest.hc22000 /usr/share/wordlists/rockyou.txt

# Tentativo 2: dizionario con regole
hashcat -m 22000 corp_guest.hc22000 wordlist.txt -r /usr/share/hashcat/rules/best64.rule

# Tentativo 3: dizionario personalizzato (nome azienda + varianti)
# Creare un file con varianti: CorpName2024, CorpName2024!, corp_name_guest, ecc.
hashcat -m 22000 corp_guest.hc22000 custom_corp.txt -r rules/best64.rule

# Tentativo 4: brute force numerico (molte reti guest usano numeri)
hashcat -m 22000 corp_guest.hc22000 -a 3 ?d?d?d?d?d?d?d?d

# Tentativo 5: pattern comune (parola + numeri)
hashcat -m 22000 corp_guest.hc22000 -a 6 wordlist.txt ?d?d?d?d
```

**Output del report (esempio):**

```
FINDING: Password WiFi guest debole
  Severita: Media
  Descrizione: La password della rete Corp_Guest ("Welcome2024!") e stata
  crackata in 4 minuti usando un dizionario personalizzato con regole di
  mutazione. La password segue un pattern comune (parola + anno + simbolo)
  facilmente predicibile.
  Rischio: Accesso non autorizzato alla rete guest. Se la rete non e
  adeguatamente isolata, possibile pivot sulla rete corporate.
  Raccomandazione: Implementare password complesse (16+ caratteri casuali),
  ruotarle mensilmente, oppure migrare a WPA2-Enterprise con autenticazione
  individuale per la rete guest.
```

### 6.3 Scenario 3: Evil Portal per Credential Harvesting in un Hotel

**Contesto**: il cliente e una catena alberghiera che vuole testare la
consapevolezza dei propri ospiti riguardo al phishing WiFi. Test autorizzato
con il management dell'hotel.

**Obiettivo**: creare un captive portal che simuli la pagina di login WiFi
dell'hotel per misurare quanti ospiti inseriscono le proprie credenziali.

**Fase 1 - Ricognizione**

1. Connettersi alla rete WiFi legittima dell'hotel come ospite normale
2. Documentare la pagina di login del captive portal legittimo:
   - Screenshot della pagina
   - Colori, font, logo, layout
   - Campi richiesti (nome, cognome, numero stanza, email, ecc.)
   - Testo dei termini e condizioni

3. Scansione dell'ambiente con Marauder:
   ```
   scanap
   ```
   Identificare SSID, canale e parametri della rete legittima.

**Fase 2 - Preparazione del template**

Creare un template HTML che replichi la pagina di login dell'hotel.
Caricare il file sulla SD card del Flipper.

Punti critici per il realismo:
- Logo dell'hotel (convertito in base64)
- Stessi campi del form originale
- Stesso schema di colori
- Disclaimer legale simile
- Pulsante "Accept & Connect" identico

**Fase 3 - Deploy dell'Evil Portal**

1. Posizionare il Flipper in un'area comune dell'hotel (lobby, sala
   colazione, area piscina) dove il segnale della rete legittima e debole.

2. Configurare l'Evil Portal:
   - SSID identico alla rete dell'hotel (Evil Twin)
   - Oppure SSID simile: "Hotel_Roma_WiFi_Free" se la rete legittima e
     "Hotel_Roma_WiFi"
   - Template: la pagina custom creata

3. Avviare l'Evil Portal

4. Il Flipper crea l'AP e serve il captive portal

5. Gli ospiti che cercano WiFi vedono la rete fake (spesso con segnale
   piu forte perche il Flipper e nella stessa stanza)

6. Si connettono, il captive portal appare automaticamente

7. Inseriscono le credenziali richieste

8. Le credenziali vengono salvate sulla SD card

**Fase 4 - Raccolta e analisi**

Dopo il periodo di test concordato (es. 24 ore), raccogliere i dati:

```
Credenziali catturate: 31 set completi
Dati raccolti: nome, cognome, email, numero stanza
Tempo operativo: 22 ore (con powerbank esterno)
Tasso di successo: ~40% dei dispositivi che hanno visto la rete
```

**Fase 5 - Report**

```
FINDING: Ospiti vulnerabili al WiFi phishing
  Severita: Alta
  Descrizione: Su 78 dispositivi che si sono connessi al rogue AP, 31 ospiti
  (40%) hanno inserito dati personali reali nella pagina di phishing. Di
  questi, 12 hanno inserito la propria password email personale (riutilizzo
  password fra WiFi dell'hotel e email personale).
  Rischio: Un attaccante reale potrebbe usare le credenziali email per
  accesso a servizi personali/aziendali delle vittime.
  Raccomandazioni:
  - Implementare WPA2-Enterprise con credenziali individuali per stanza
  - Eliminare il captive portal basato su email/password
  - Comunicare agli ospiti il nome ESATTO della rete WiFi al check-in
  - Implementare WIDS per rilevare rogue AP con SSID uguale
  - Formazione del personale IT sulla rilevazione di Evil Twin
```

> Nota personale: il tasso del 40% e realistico -- l'ho visto in piu engagement.
> Le persone non verificano a quale rete si connettono, specialmente in ambienti
> dove si aspettano WiFi gratuito. Il consiglio piu efficace che do ai clienti e
> sempre lo stesso: eliminare i captive portal basati su credenziali e passare a
> WPA2-Enterprise. Il captive portal e una vulnerabilita by design.

### 6.4 Scenario 4: Wardriving per Mappatura Reti di un'Area

**Contesto**: il cliente e un'azienda con uffici in un business park. Vuole
sapere quante reti wireless sono raggiungibili dall'area circostante e se
le proprie reti sono visibili dall'esterno del perimetro.

**Obiettivo**: mappare tutte le reti WiFi nel raggio di 500m dall'edificio
target.

**Fase 1 - Preparazione**

1. Caricare Marauder aggiornato sull'ESP32
2. Verificare funzionamento GPS (se modulo esterno disponibile)
3. Preparare percorso: camminata circolare attorno al business park,
   coprendo tutti gli angoli e gli ingressi

**Fase 2 - Wardriving**

1. Avviare la scansione continua con GPS logging
2. Camminare lungo il percorso pianificato a passo normale (velocita
   costante per distribuzione uniforme dei campioni)
3. Il Flipper registra continuamente: SSID, BSSID, canale, RSSI,
   cifratura, coordinate GPS
4. Durata tipica: 30-60 minuti per un perimetro di 500m

**Fase 3 - Analisi**

1. Estrarre il file CSV dalla SD card
2. Importare in tool di analisi:
   - Upload su WiGLE (visualizzazione su mappa)
   - Import in Google Earth / QGIS per mapping personalizzato
   - Analisi con script Python/pandas per statistiche

3. Creare mappa di calore (heatmap) della copertura WiFi del target

**Fase 4 - Risultati tipici**

```
Reti totali rilevate: 147
Reti del cliente: 12
Reti del cliente visibili dall'esterno: 8 su 12 (67%)

Cifrature rilevate:
  WPA3:           4 (3%)
  WPA2-Enterprise: 18 (12%)
  WPA2-Personal:  89 (61%)
  WPA:            11 (7%)
  WEP:            3 (2%)
  Open:           22 (15%)

Canali piu usati:
  Canale 1:  31 reti
  Canale 6:  42 reti
  Canale 11: 38 reti
  Altri:     36 reti
```

**Fase 5 - Report**

```
FINDING: Copertura WiFi corporate oltre il perimetro fisico
  Severita: Media
  Descrizione: 8 delle 12 reti WiFi aziendali sono rilevabili con segnale
  utilizzabile (RSSI > -75 dBm) dal parcheggio esterno e dal marciapiede.
  La rete IoT industriale "Corp_IoT_Prod" e rilevabile a 200m dall'edificio.
  Rischio: Un attaccante potrebbe operare comodamente dall'esterno senza
  entrare nell'edificio, tentando crack offline o Evil Twin.
  Raccomandazioni:
  - Ridurre potenza TX degli AP perimetrali
  - Implementare antenne direzionali verso l'interno
  - Valutare schermatura RF delle sale server
  - Segmentare reti IoT su VLAN dedicate con firewall
```

---

## Cross-Reference - Scenari Multi-Vettore

| Scenario | Modulo Correlato | Link | Come si collegano |
|----------|-----------------|------|-------------------|
| Evil portal + BadUSB | USB/Bad USB | [05-Scenari-Reali](../USB/Bad%20USB/05-Scenari-Reali.md) | Evil portal raccoglie credenziali WiFi → BadUSB per pivot su workstation |
| Deauth + Sub-GHz | Sub-GHz | [05-Scenari-Reali](../Sub-GHz/05-Scenari-Reali.md) | Jamming WiFi allarme + replay Sub-GHz sensori per bypass completo |
| Ricognizione WiFi + NFC | NFC | [05-Scenari-Reali](../NFC/05-Scenari-Reali.md) | Badge NFC per accesso fisico → scan WiFi interna per mapping rete |
| WiFi + NRF24 | GPIO/NRF24 | [04-Scenari-Reali](../GPIO/NRF24/04-Scenari-Reali.md) | Scan WiFi per trovare target → MouseJacker su periferiche wireless |
| WiFi + BLE | Bluetooth | [05-Scenari-Reali](../Bluetooth/05-Scenari-Reali.md) | Scan WiFi + BLE scan per mappatura completa wireless dell'ambiente |
| Wardriving + RFID | RFID | [05-Scenari-Reali](../RFID/05-Scenari-Reali.md) | Wardriving perimetrale + test badge parcheggio nella stessa sessione |

