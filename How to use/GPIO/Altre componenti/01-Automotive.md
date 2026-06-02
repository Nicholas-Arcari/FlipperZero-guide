# Automotive - CAN Bus e Diagnostica Veicolare

Questa sezione raccoglie gli strumenti GPIO dedicati al mondo automotive: interfacce CAN Bus standard e CAN-FD, tool di diagnostica, iniezione pacchetti e terminali di comando per ECU e reti veicolari.

---

### • CAN Transceiver

Interfaccia al bus CAN standard (Controller Area Network).

Funzionalità ampliate:

- Lettura e scrittura pacchetti CAN.
- Monitoraggio traffico in tempo reale.
- Analisi errori di comunicazione (CRC, ACK).
- Supporto a velocità standard: 125k, 250k, 500k, 1Mbps.

Esempio pratico:

- Collegare CAN_H e CAN_L ai pin GPIO dedicati.
- Avviare CAN Transceiver → monitorare messaggi da ECU automotive.
- Inviare pacchetti test per simulare sensori.

(Note: Usare resistenze di terminazione corrette per evitare errori sul bus)

### • CANBus

Lettura e scrittura avanzata su reti CAN.

Funzionalità ampliate:

- Registrazione e analisi pacchetti CAN.
- Supporto multi-ID e filtri.
- Compatibile con CAN standard e extended.

Esempio pratico:

- Collegare CANBus ai pin GPIO.
- Avviare lettura → salvare dump dei messaggi su file.
- Analizzare traffico per diagnostica ECU o dispositivi industriali.

### • CANBus Attack

Strumenti diagnostici e di attacco sul bus CAN.

Funzionalità ampliate:

- Iniezione pacchetti CAN per test di sicurezza.
- Replay attack su messaggi memorizzati.
- Analisi vulnerabilità del network CAN.

Esempio pratico:

- Collegare Flipper al bus CAN dell'auto in test.
- Avviare replay pacchetti → osservare reazioni ECU o gateway.
- Valutare sicurezza o comportamento di fail-safe.

### • CANCommander

Terminale per invio comandi CAN manuale o scriptato.

Funzionalità ampliate:

- Interfaccia testo per invio e ricezione messaggi.
- Supporto script di test automatizzati.
- Visualizzazione live di errori e stato del bus.

Esempio pratico:

- Avviare CANCommander → digitare messaggi CAN.
- Inviare comando a ECU di test → monitorare risposta.
- Script per test ciclici di messaggi su vari ID.

(Note: Utile per debugging e sviluppo di tool automotive)

### • Serma CAN-FD-HS

Interfaccia bus CAN-FD ad alta velocità tramite GPIO.

Funzionalità ampliate:

- Lettura e scrittura pacchetti CAN e CAN-FD.
- Analisi bus con timestamp.
- Filtraggio ID messaggi.
- Supporto a bus automotive e industriali.
- Logging e debug avanzato.

Esempio pratico

Monitoraggio ECU auto:

- Collegare CAN_H / CAN_L.
- Avviare logging pacchetti.
- Analizzare segnali per diagnostica ECU.
- Inviare messaggi test per verifica controlli.
