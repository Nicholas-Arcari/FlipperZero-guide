## 8. Scenari di Pentest Reali

### 8.1 Scenario: Wardriving urbano

**Obiettivo:** Mappare la superficie wireless di un campus aziendale per valutare il signal leakage e le reti esposte.

**Kit necessario:**
- Flipper Zero con firmware custom
- ESP32-WROOM con firmware Wardriver
- Modulo GPS NEO-6M/7M
- Powerbank 10000mAh
- Antenna esterna 2.4GHz (opzionale, per maggiore sensibilità)

**Procedura operativa:**

1. **Preparazione (30 minuti)**
   - Flashare firmware Wardriver sull'ESP32.
   - Collegare GPS all'ESP32 (UART2).
   - Collegare ESP32 al Flipper via GPIO.
   - Alimentare con powerbank.
   - Verificare il fix GPS all'aperto (attendere 3-5 minuti).
   - Test rapido: verificare che le reti vengano rilevate.

2. **Wardriving perimetrale (1-2 ore)**
   - Percorrere il perimetro dell'edificio a piedi o in auto.
   - Mantenere velocità costante per copertura uniforme.
   - Coprire tutti i lati dell'edificio.
   - Annotare punti di interesse (ingressi, parcheggi, aree pubbliche).

3. **Wardriving interno (se accesso autorizzato, 1-2 ore)**
   - Percorrere tutti i piani e le aree accessibili.
   - Particolare attenzione a: sale riunioni, mense, reception, corridoi.
   - Identificare rogue AP (dispositivi personali che creano hotspot).

4. **Analisi dei dati (2-4 ore)**
   - Esportare il CSV dalla microSD.
   - Upload su WiGLE (opzionale) per cross-reference.
   - Analisi con strumenti GIS (QGIS, Google Earth):
     - Importare i dati geolocalizzati.
     - Creare mappa delle reti con copertura.
     - Identificare signal leakage: reti corporate visibili dall'esterno.
   - Categorizzare le reti trovate:
     - Corporate (con nome aziendale)
     - Guest
     - Rogue (non autorizzate)
     - Vicini (edifici adiacenti)

5. **Report**
   - Mappa delle reti con overlay sull'edificio.
   - Signal leakage: distanza massima alla quale la rete corporate è rilevabile.
   - Rogue AP identificati con posizione approssimativa.
   - Reti con crittografia debole o assente.
   - Raccomandazioni: riduzione potenza TX, disabilitazione SSID broadcast per reti sensibili, policy BYOD per rogue AP.

### 8.2 Scenario: Evil Portal credential harvesting

**Obiettivo:** Testare la consapevolezza dei dipendenti riguardo al phishing WiFi, catturando credenziali inserite in portali captive fasulli.

**Kit necessario:**
- Flipper Zero
- ESP32-WROOM o ESP32-S2 con firmware Evil Portal
- File HTML del portal preparati in anticipo
- Powerbank

**Procedura operativa:**

1. **Preparazione (1-2 ore)**
   - Raccolta informazioni sul target:
     - Nome e grafica del portale WiFi guest reale (se esiste).
     - Nome della rete corporate e guest.
     - Stile grafico aziendale (logo, colori, font).
   - Creazione della pagina HTML:
     - Replicare fedelmente il portale WiFi guest o il login VPN.
     - Includere logo aziendale, colori corporate, disclaimer legale.
     - Form con campi: email aziendale + password.
     - Pagina di successo: "Connessione in corso..." per non destare sospetti.
   - Test del portale in ambiente controllato.
   - Caricare i file HTML sulla microSD del Flipper.

2. **Deployment (15 minuti)**
   - Collegare l'ESP32 al Flipper.
   - Configurare Evil Portal:
     - SSID: nome credibile (es. "NomeAzienda-Guest", "NomeAzienda-WiFi-Upgrade").
     - Selezionare la pagina HTML preparata.
     - Avviare il portale.
   - Posizionare il dispositivo in un'area ad alto traffico:
     - Mensa, area break, sala d'attesa.
     - Nascondere in un contenitore discreto (borsa, scatola).
     - Assicurare alimentazione continua (powerbank capiente).

3. **Raccolta dati (2-8 ore)**
   - Monitorare periodicamente dal Flipper:
     - Numero di connessioni.
     - Credenziali catturate.
   - Non intervenire -- lasciare il sistema operare autonomamente.
   - Le credenziali vengono loggate sulla microSD con timestamp.

4. **Analisi e report**
   - Numero totale di connessioni al portale.
   - Numero di credenziali inserite.
   - Analisi delle credenziali (senza memorizzarle -- solo statistiche):
     - Quante sono credenziali aziendali reali.
     - Quante sono credenziali personali (email private).
     - Quante sono credenziali false/di test.
   - Tempo medio tra connessione e inserimento credenziali.
   - Raccomandazioni:
     - Formazione dipendenti sul phishing WiFi.
     - Implementazione 802.1X per la rete corporate.
     - Monitoraggio rogue AP con WIDS.
     - Policy sulla connessione a reti WiFi sconosciute.

> Nota personale: la chiave del successo con Evil Portal è l'SSID. Un SSID generico come "Free WiFi" attira pochi in ambiente aziendale. Un SSID che sembra un upgrade del WiFi aziendale ("NomeAzienda-WiFi-5G", "NomeAzienda-Guest-Fast") attira molti di piu'. Ho visto tassi di cattura del 30-40% dei dipendenti in aree comuni con SSID ben scelti. Ovviamente, tutto questo con autorizzazione scritta del management.

### 8.3 Scenario: Stealth WiFi reconnaissance

**Obiettivo:** Mappare completamente l'ambiente wireless del target senza essere rilevati da sistemi WIDS (Wireless Intrusion Detection System).

**Kit necessario:**
- Flipper Zero
- ESP32-WROOM con firmware Ghost ESP
- Contenitore discreto (borsa, giacca con tasca interna)

**Procedura operativa:**

1. **Pianificazione**
   - Identificare le aree da mappare.
   - Pianificare il percorso per coprire l'intera area.
   - Stimare i tempi: 30-60 minuti per un edificio medio.
   - Verificare che Ghost ESP sia configurato in modalità completamente passiva.

2. **Esecuzione**
   - Attivare Ghost ESP prima di entrare nell'area target.
   - Modalità: passive scan + MAC randomization.
   - Camminare normalmente nel percorso pianificato.
   - Non fermarsi in punti sospetti -- mantenere un comportamento naturale.
   - Il Flipper in tasca raccoglie dati senza necessità di interazione.
   - Durata: minimo 20 minuti per avere dati significativi.

3. **Analisi post-ricognizione**
   - Estrarre i log dalla microSD.
   - Analizzare:
     - Lista completa AP con canali e crittografia.
     - Client rilevati e reti che cercano (probe request).
     - Pattern di traffico per area.
     - Vendor degli AP (per identificare il produttore dell'infrastruttura).
   - Pianificare la fase successiva:
     - Target per attacchi mirati (con Marauder).
     - Vulnerabilità identificate (WEP, Open, AP isolati).
     - Dispositivi di interesse per BLE auditing.

4. **Vantaggi dell'approccio stealth**
   - Nessun frame trasmesso = nessun log sui WIDS.
   - Nessun probe request = nessun fingerprint del dispositivo.
   - MAC randomization = anche se rilevato (improbabile), non è tracciabile.
   - Il Flipper+ESP32 in tasca non attira attenzione visiva.

### 8.4 Scenario: Sorveglianza con ESP32-CAM

**Obiettivo:** Monitoraggio visivo di un'area durante un assessment di sicurezza fisica.

**Kit necessario:**
- Flipper Zero
- ESP32-CAM con LED IR (per visione notturna)
- Powerbank capiente (10000+ mAh)
- Supporto/montaggio per la camera
- MicroSD per l'ESP32-CAM (per registrazione locale)

**Procedura operativa:**

1. **Setup della camera**
   - Flashare firmware Camera Suite o Motion Detection sull'ESP32-CAM.
   - Montare l'ESP32-CAM con visuale sull'area di interesse:
     - Porta della sala server.
     - Area di passaggio.
     - Rack di rete.
   - Collegare al Flipper per configurazione iniziale.
   - Configurare:
     - Risoluzione e frame rate (bilanciare qualità vs durata batteria).
     - Modalità IR: auto per switch giorno/notte.
     - Motion detection: attivare per risparmiare spazio SD.
     - Sensibilità: media (evitare falsi positivi da cambiamenti luce).

2. **Deployment**
   - Posizionare il dispositivo in modo discreto.
   - Verificare l'inquadratura dal Flipper.
   - Assicurare alimentazione sufficiente per la durata prevista.
   - Disconnettere il Flipper se non serve monitoraggio live (l'ESP32-CAM funziona autonomamente con motion detection e registrazione su SD).

3. **Monitoraggio (opzionale)**
   - Se serve monitoraggio live: tenere il Flipper collegato.
   - Lo streaming mostra l'inquadratura in tempo reale.
   - Notifiche di movimento sul display.

4. **Raccolta risultati**
   - Recuperare la microSD dall'ESP32-CAM.
   - Analizzare le foto/registrazioni:
     - Orari di accesso alla sala server.
     - Personale che accede (autorizzato?).
     - Procedure seguite (badge, chiave, tailgating).
     - Durata degli accessi.
   - Integrare nel report di sicurezza fisica:
     - Compliance con la policy di accesso.
     - Evidenze di tailgating o accesso non autorizzato.
     - Raccomandazioni per il controllo accessi.

> Nota personale: la sorveglianza con ESP32-CAM è una delle applicazioni più potenti e sensibili dal punto di vista legale ed etico. Usa questo tool SOLO con autorizzazione scritta esplicita che menzioni la videosorveglianza. In molti paesi, la registrazione video senza consenso è illegale anche durante un pentest autorizzato se non esplicitamente prevista nel contratto. Verifica sempre con il legale prima di procedere. Dal punto di vista tecnico, l'ESP32-CAM con motion detection e LED IR funziona sorprendentemente bene come sistema di sorveglianza low-cost -- il limite principale è la risoluzione (2MP) e la qualità dell'ottica.

---

## Cross-Reference - Scenari Multi-Vettore

| Scenario | Modulo Correlato | Link | Come si collegano |
|----------|-----------------|------|-------------------|
| Evil portal + BadUSB | USB/Bad USB | [05-Scenari-Reali](../../USB/Bad%20USB/05-Scenari-Reali.md) | Credenziali WiFi via evil portal → BadUSB per accesso workstation |
| Deauth + Sub-GHz | Sub-GHz | [05-Scenari-Reali](../../Sub-GHz/05-Scenari-Reali.md) | Disruption WiFi allarme + replay RF per bypass completo |
| WiFi scan + NFC | NFC | [05-Scenari-Reali](../../NFC/05-Scenari-Reali.md) | Accesso fisico con badge NFC → ricognizione WiFi interna |
| ESP32 + NRF24 | GPIO/NRF24 | [04-Scenari-Reali](../NRF24/04-Scenari-Reali.md) | Scan WiFi + scan 2.4 GHz per mappatura wireless completa |
| ESP32 + BLE | Bluetooth | [05-Scenari-Reali](../../Bluetooth/05-Scenari-Reali.md) | WiFi + BLE scan combinati per inventario completo dispositivi IoT |

