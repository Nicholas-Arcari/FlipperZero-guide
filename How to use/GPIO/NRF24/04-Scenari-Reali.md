## 8. Scenari di Pentest

### 8.1 MouseJacker in ufficio

**Contesto:** audit di sicurezza di un'azienda con 50+ postazioni, la maggior parte con mouse wireless Logitech.

**Fase 1 -- Ricognizione (giorno 1):**

- Passeggiata nell'ufficio con Flipper Zero + NRF24 PA+LNA nello zaino
- Scanner in esecuzione continua
- Risultato: 34 mouse wireless identificati, 28 Logitech Unifying, 4 Microsoft, 2 sconosciuti
- 22 dei 28 Logitech risultano con firmware non aggiornato (vulnerabili)

**Fase 2 -- Proof of Concept (giorno 2):**

- Target selezionato: postazione del responsabile acquisti (mouse M185, firmware vecchio)
- Posizionamento: sala riunioni adiacente (circa 8 metri attraverso un muro)
- Payload: apertura notepad + messaggio di avviso
- Esecuzione: successo al primo tentativo, tempo totale 3 secondi
- Documentazione: screenshot, timestamp, indirizzo pipe del dispositivo

**Fase 3 -- Escalation dimostrativa (giorno 2):**

- Stesso target, payload più avanzato: PowerShell che scarica ed esegue un agente di monitoraggio
- Esecuzione: successo, agente installato in 5 secondi
- Accesso completo alla postazione via C2 server

**Fase 4 -- Report:**

- Vulnerabilità classificata come CRITICA (CVSS 9.0+)
- Remediation: aggiornamento firmware dongle + sostituzione periferiche non aggiornabili
- Raccomandazione: migrazione a periferiche Bluetooth o cablate per postazioni sensibili
- Timeline remediation raccomandata: immediata per postazioni critiche, 30 giorni per tutte

### 8.2 Sniffing sensori IoT

**Contesto:** audit di un sistema di monitoraggio ambientale basato su sensori wireless.

**Fase 1 -- Identificazione:**

- Channel Scan rivela 8 dispositivi attivi nella banda 2.4 GHz
- 5 sono sensori di temperatura/umidità (trasmissione ogni 30 secondi)
- 2 sono mouse wireless (traffico intermittente)
- 1 è un telecomando per luci LED

**Fase 2 -- Cattura e analisi:**

- Sniffer configurato sul canale dei sensori
- Cattura di 100+ pacchetti in 30 minuti
- Analisi del payload: dati in chiaro, nessuna crittografia, nessuna autenticazione
- Formato decodificato: [ID_sensore(2B)] [Temperatura(2B, BCD)] [Umidità(1B)] [Batteria(1B)] [CRC(1B)]

**Fase 3 -- Proof of Concept injection:**

- Costruzione di un pacchetto fake con temperatura alterata
- Iniezione nel sistema di monitoraggio
- Il sistema accetta il dato falso senza validazione
- Dimostrazione che un attaccante può falsificare le letture dei sensori

**Impatto:** un attaccante potrebbe alterare le letture dei sensori in un magazzino farmaceutico, simulando temperature corrette mentre la catena del freddo è interrotta.

### 8.3 Jamming -- demo controllata

**Contesto:** test di resilienza di un sistema di allarme wireless in ambiente controllato.

**Setup:**

- Sistema di allarme con sensori wireless a 2.4 GHz
- Test in laboratorio schermato (gabbia di Faraday)
- Autorizzazione scritta dal cliente

**Test 1 -- Jamming singolo canale:**

- Identificazione del canale usato dai sensori: canale 52
- Attivazione del jammer su canale 52
- Risultato: i sensori non riescono più a comunicare con la centralina
- La centralina NON rileva il jamming (nessun allarme di tamper)
- Il sensore continua a tentare la trasmissione ma i pacchetti vengono persi
- Tempo per perdita comunicazione: 3 secondi

**Test 2 -- Recovery dopo jamming:**

- Disattivazione del jammer
- I sensori riprendono la comunicazione in 2-5 secondi
- La centralina non ha registrato l'interruzione

**Conclusione:** il sistema di allarme è vulnerabile a jamming RF senza alcuna detection. Raccomandazione: implementare rilevamento anti-jamming (monitoraggio della mancanza di heartbeat dai sensori).

### 8.4 Audit periferiche wireless -- checklist

Checklist completa per audit delle periferiche wireless in un'organizzazione:

**Inventario:**

- [ ] Censimento di tutte le periferiche wireless (mouse, tastiere, presentatori)
- [ ] Identificazione marca, modello e firmware di ogni dispositivo
- [ ] Mappatura dei dongle USB associati
- [ ] Identificazione delle postazioni con dati sensibili

**Test tecnici:**

- [ ] Channel Scan dell'intero ambiente
- [ ] Identificazione di tutti i dispositivi NRF24-compatibili
- [ ] Verifica crittografia per ogni dispositivo identificato
- [ ] Test MouseJacker su campione rappresentativo
- [ ] Test di sniffing passivo (verifica dati in chiaro)
- [ ] Test di injection su dispositivi vulnerabili

**Valutazione rischio:**

- [ ] Classificazione dei dispositivi per livello di vulnerabilità
- [ ] Correlazione con il valore degli asset sulla postazione
- [ ] Stima dell'impatto di un attacco riuscito
- [ ] Identificazione delle postazioni a maggior rischio

**Remediation:**

- [ ] Aggiornamento firmware dove possibile
- [ ] Sostituzione dispositivi non aggiornabili
- [ ] Migrazione a Bluetooth per postazioni critiche
- [ ] Policy aziendale sull'uso di periferiche wireless
- [ ] Formazione utenti sui rischi delle periferiche wireless

> Nota personale: la checklist qui sopra è quella che uso realmente nei miei audit. L'ho raffinata nel corso di una dozzina di assessment. Il punto che le aziende sottovalutano sempre è l'inventario: nessuno sa quanti mouse wireless ci sono in ufficio. La risposta è sempre "molti più di quelli che pensavamo". In un'azienda da 200 dipendenti ho trovato 47 mouse wireless non inventariati, di cui 31 vulnerabili a MouseJacker. Il responsabile IT era convinto che fossero "al massimo una decina".

---

## Cross-Reference - Scenari Multi-Vettore

| Scenario | Modulo Correlato | Link | Come si collegano |
|----------|-----------------|------|-------------------|
| MouseJacker vs BadUSB | USB/Bad USB | [05-Scenari-Reali](../../USB/Bad%20USB/05-Scenari-Reali.md) | MouseJacker è l'alternativa wireless al BadUSB cablato - stesso payload, diverso delivery |
| NRF24 + WiFi | GPIO/ESP32 | [04-Scenari-Reali](../ESP32/04-Scenari-Reali.md) | Scan 2.4 GHz per periferiche + scan WiFi per rete: mappatura wireless completa |
| Periferiche + RFID | RFID | [05-Scenari-Reali](../../RFID/05-Scenari-Reali.md) | Accesso fisico via badge RFID → MouseJacker su workstation interne |
| NRF24 + BLE | Bluetooth | [05-Scenari-Reali](../../Bluetooth/05-Scenari-Reali.md) | Entrambi su 2.4 GHz: NRF24 per periferiche, BLE per IoT/wearable |
| NRF24 + Sub-GHz | Sub-GHz | [05-Scenari-Reali](../../Sub-GHz/05-Scenari-Reali.md) | Assessment RF completo: Sub-GHz (sensori, cancelli) + 2.4 GHz (periferiche) |

