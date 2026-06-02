# ESP8266 - Guida Operativa Avanzata

Moduli WiFi compatti ed economici per attacchi wireless, automazione IoT e sperimentazione. L'ESP8266 è l'alternativa più economica all'ESP32 per operazioni WiFi specifiche, in particolare gli attacchi di deauthentication.

---

## Fondamenti Tecnici

L'ESP8266 è un SoC WiFi 2.4 GHz single-band con processore Tensilica L106 a 80/160 MHz. A differenza dell'ESP32, ha un solo core, nessun supporto BLE e una potenza TX leggermente inferiore. Tuttavia, per attacchi deauth e scansioni WiFi, le prestazioni sono equivalenti a costo molto inferiore (~2 euro vs ~8 euro).

**Collegamento al Flipper Zero:**
```
Flipper GPIO    ESP8266
3V3          -> VCC (ATTENZIONE: 3.3V, MAI 5V!)
GND          -> GND
PB7 (RX)     -> TX
PB6 (TX)     -> RX
```

> **Nota personale:** L'ESP8266 è il primo modulo che ho comprato per il Flipper. Costa nulla, si salda in 5 minuti e ti da immediatamente capacità WiFi offensive. Per chi inizia con il pentest wireless, è il punto di partenza ideale prima di investire in un ESP32 completo.

---

## Deauther

### Come Funziona l'Attacco Deauthentication

L'attacco deauth sfrutta una debolezza fondamentale del protocollo 802.11: i **management frame** (in particolare i frame di deauthentication e disassociation) non sono autenticati in WPA2 standard. Questo significa che chiunque può inviare un frame di deauthentication con l'indirizzo MAC sorgente spoofato dell'AP, e il client si disconnetterà.

**Struttura del frame deauth:**
```
[Frame Control: 0x00C0] [Duration] [DA: client MAC] [SA: AP MAC] [BSSID: AP MAC] [Seq] [Reason Code: 0x0007]
```

**Reason codes comuni:**
- 0x01: Unspecified reason
- 0x04: Disassociated due to inactivity
- 0x05: Disassociated because AP is unable to handle all currently associated STAs
- 0x07: Class 3 frame received from nonassociated STA (il più usato)

**Procedura operativa:**

1. Flash il firmware Deauther sull'ESP8266 (via web flasher o esptool)
2. Collega al Flipper via UART
3. Apri l'app Deauther sul Flipper
4. **Scan:** l'ESP scansiona tutte le reti 2.4 GHz circostanti
5. Identifica l'AP target e i client connessi
6. **Select target:** seleziona AP e/o client specifici
7. **Start Deauth:** l'ESP invia frame di deauthentication continui
8. I client target vengono disconnessi ripetutamente

**Configurazione avanzata:**
- **Channel:** blocca su un canale specifico o scansiona tutti
- **Target:** singolo AP, singolo client, o broadcast
- **Packet rate:** numero di frame deauth al secondo (default ~10-50)
- **Reason code:** selezionabile per test di compatibilità

### Deauther V2

Evoluzione con interfaccia web migliorata:
- Dashboard HTML accessibile collegandosi al WiFi dell'ESP
- Lista live di AP e client con RSSI
- Multi-target simultaneo
- Logging dettagliato
- Profili salvabili

**Uso nel pentest:**
- Forzare la riconnessione di un client per catturare l'handshake WPA2 (con ESP32 Marauder o airodump-ng)
- Test di resilienza della rete: i client gestiscono correttamente la riconnessione?
- Demo per awareness: mostrare quanto è facile disconnettere dispositivi WiFi
- Stress test dispositivi IoT: come reagiscono a disconnessioni ripetute?

> **Nota personale:** Il deauth è l'attacco WiFi più semplice e più d'impatto durante le demo. Disconnettere tutti i dispositivi di una sala riunioni in 3 secondi fa molta impressione. Ma ATTENZIONE: il deauth su reti altrui senza autorizzazione è illegale. Inoltre, 802.11w (Management Frame Protection) blocca il deauth su reti che lo supportano - i router WiFi 6 moderni spesso lo hanno attivo.

---

## WiFi Scanner

Scanner passivo per reti WiFi 2.4 GHz.

**Dati raccolti per ogni AP:**
- **SSID:** nome della rete (o "Hidden" se nascosto)
- **BSSID:** MAC address dell'AP
- **Channel:** canale WiFi (1-13 in EU)
- **RSSI:** potenza del segnale (dBm) - più vicino a 0 = più forte
- **Encryption:** Open, WEP, WPA, WPA2, WPA3
- **Client count:** numero stimato di client connessi

**Procedura operativa:**

1. Avvia WiFi Scanner
2. L'ESP scansiona tutti i canali
3. Lista delle reti ordinata per RSSI
4. Seleziona un AP per vedere i dettagli e i client

**Uso nel pentest:**
- Fase di ricognizione: mappare tutte le reti dell'edificio target
- Identificare reti con sicurezza debole (WEP, Open)
- Trovare reti nascoste (hidden SSID - rilevabili dai probe response)
- Stimare il numero di dispositivi connessi
- Identificare canali congestionati per wardriving

> **Nota personale:** Il WiFi Scanner dell'ESP8266 è limitato al 2.4 GHz. Per una ricognizione completa serve anche il 5 GHz (che richiede un ESP32 o un adattatore WiFi con supporto 5GHz e monitor mode). In engagement reali, uso l'ESP8266 per il quick scan iniziale e poi completo con airodump-ng su un laptop per il quadro completo.

---

## IFTTT Button

Trasforma il Flipper + ESP8266 in un trigger IoT via IFTTT Webhooks.

**Come funziona:**
1. L'ESP si connette a una rete WiFi nota
2. Al trigger (pressione pulsante sul Flipper), invia una richiesta HTTP GET/POST a IFTTT Webhooks
3. IFTTT esegue l'automazione configurata

**Configurazione:**
- SSID e password della rete WiFi
- IFTTT Webhook key (dalla dashboard IFTTT)
- Nome evento (es. "flipper_trigger")
- Dati opzionali (value1, value2, value3)

**Uso creativo nel pentest:**
- Trigger automatico di notifiche quando un evento si verifica
- Attivazione di script remoti dalla posizione target
- Integrazione con sistemi di C2 leggeri
- Log di attività in tempo reale su Google Sheets

---

## Aspetti Legali

- Il deauthentication su reti WiFi non autorizzate è illegale in Italia (D.Lgs. 259/2003, interferenza con comunicazioni)
- La scansione passiva (WiFi Scanner) è generalmente legale - non trasmetti nulla, ascolti solo
- L'uso di IFTTT/automazione su reti proprie è legale

---

## Esperienza Personale

> **Nota personale - ESP8266 vs ESP32:** Per chi ha budget limitato, l'ESP8266 con firmware Deauther è il miglior investimento. Costa 2 euro, si collega in 2 minuti e ti da il deauth - l'attacco WiFi più usato nel pentest. L'ESP32 con Marauder è superiore in tutto ma costa 4x tanto. Il mio consiglio: inizia con ESP8266 per capire le basi, poi migra a ESP32 per funzionalità complete.

> **Nota personale - 802.11w:** Sempre più reti supportano Management Frame Protection (802.11w/PMF). Su queste reti, il deauth non funziona perchè i management frame sono autenticati. WiFi 6 (802.11ax) lo include di default. Questo significa che l'attacco deauth sta diventando meno efficace su hardware moderno - ma la maggior parte delle reti aziendali usa ancora hardware senza PMF.
