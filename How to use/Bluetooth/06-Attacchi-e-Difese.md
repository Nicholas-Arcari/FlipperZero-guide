## Attacchi BLE Avanzati

Questa sezione descrive attacchi BLE che vanno oltre le capacità native del Flipper ma che sono rilevanti per un pentester che opera nell'ecosistema BLE.

### BLE Sniffing

Lo sniffing BLE consiste nel catturare il traffico radio tra due dispositivi BLE connessi. Il Flipper NON può fare sniffing BLE completo.

**Perchè il Flipper non può sniffare:**

1. Lo scanner del Flipper vede solo advertising packets (canali 37/38/39)
2. Una connessione BLE attiva usa i canali dati (0-36) con frequency hopping
3. Per seguire il frequency hopping, serve conoscere l'Access Address e il channel map della connessione
4. Queste informazioni sono scambiate durante la Connection Request (CONNECT_IND)
5. Il Flipper non ha la capacità di catturare CONNECT_IND e seguire il hopping pattern

**Hardware per sniffing BLE:**

| Hardware | Capacità | Prezzo |
|---|---|---|
| **Ubertooth One** | Sniffing completo BLE 4.x/5.0, follow connections | ~120-150 EUR |
| **nRF52840 Dongle** | Sniffing BLE con nRF Sniffer for Bluetooth LE | ~10-15 EUR |
| **HackRF One** | Sniffing raw 2.4 GHz (con gr-bluetooth) | ~300 EUR |
| **TI CC2540 Dongle** | Sniffing BLE 4.0 con SmartRF Sniffer | ~30-50 EUR |
| **Sniffle** (nRF52840) | Sniffer BLE 5.x open source, supporta LE Coded | ~15 EUR (solo dongle) |

**Il più raccomandato per BLE sniffing è il nRF52840 dongle con firmware Sniffle** - costa poco, è open source, supporta BLE 5.0 completo e si integra con Wireshark.

**Workflow di sniffing BLE tipico:**

1. Avviare il sniffer sul canale advertising
2. Catturare la CONNECT_IND quando il target si connette
3. Estrarre Access Address, CRC init, channel map, hop interval
4. Configurare il sniffer per seguire la connessione
5. Catturare il traffico dati (L2CAP, ATT, GATT)
6. Analizzare con Wireshark (dissector BLE integrato)

### MITM (Man-in-the-Middle) BLE

L'attacco MITM BLE consiste nel posizionarsi tra il dispositivo periferico (es. serratura smart) e il central (es. smartphone), intercettando e potenzialmente modificando la comunicazione.

**Prerequisiti:**

- Il target deve usare **Just Works** pairing o **pairing con PIN debole**
- L'attaccante deve intercettare la fase di connessione
- Serve hardware e software dedicato (GATTacker, BtleJuice, BTLE-Sniffer)

**Il Flipper NON può fare MITM BLE nativo.** Serve un setup con:

- Due radio BLE (una che finge di essere la periferica verso il central, una che finge di essere il central verso la periferica)
- Software MITM (GATTacker su Linux con due dongle BLE, o BtleJuice)
- Capacità di clonare il profilo GATT del dispositivo target

**GATTacker workflow:**

```
Smartphone <--BLE--> [Attacker Radio A] <--TCP--> [Attacker Radio B] <--BLE--> Serratura Smart
                      (finge di essere                (finge di essere
                       la serratura)                   lo smartphone)
```

1. Scansionare il GATT profile della serratura target (servizi, characteristic, descriptor)
2. Clonare il profilo sulla Radio A
3. Jammando o attendendo che lo smartphone perda la connessione originale
4. Lo smartphone si riconnette alla Radio A (che sembra la serratura)
5. La Radio B si connette alla serratura vera fingendo di essere lo smartphone
6. Tutto il traffico passa attraverso l'attaccante, che può leggere, modificare o bloccare pacchetti

### Replay Attack BLE

Il replay attack consiste nel catturare un comando BLE legittimo e ritrasmetterlo successivamente per riprodurre l'azione.

**Vulnerabilità al replay:**

I dispositivi BLE sono vulnerabili al replay se:

- Non usano nonce/counter nei comandi
- Non usano challenge-response
- Non verificano la freshness dei messaggi
- Usano comandi statici per operazioni critiche (apertura serratura, sblocco)

**Il Flipper può fare replay BLE limitato:**

- Può catturare advertising packets e ritrasmetterli (utile per beacon spoofing)
- NON può catturare e ritrasmettere traffico su connessioni attive (serve sniffer)
- Per replay su connessioni, serve prima sniffare il traffico con hardware dedicato, poi usare uno strumento per ritrasmetterlo

**Esempio pratico - serratura smart vulnerabile:**

Alcune serrature smart economiche usano comandi BLE GATT statici per l'apertura:

```
Write Request to Handle 0x0015: Value 0x55AA01 (Unlock)
Write Request to Handle 0x0015: Value 0x55AA02 (Lock)
```

Se catturi questo comando con uno sniffer, puoi ritrasmetterlo con qualsiasi dispositivo BLE (incluso il Flipper, se riesci a connetterti alla serratura). Questo tipo di vulnerabilità è comune nelle serrature economiche cinesi ma raro nei prodotti di brand affermati (August, Yale, Nuki) che usano challenge-response con nonce.

### Fuzzing GATT

Il GATT fuzzing consiste nell'inviare dati malformati o inattesi alle characteristic GATT di un dispositivo per trovare crash, vulnerabilità o comportamenti anomali.

**Tecniche di fuzzing GATT:**

- **Value fuzzing** - Inviare valori fuori range, troppo lunghi, troppo corti, NULL
- **Handle fuzzing** - Tentare read/write su handle inesistenti o protetti
- **Type fuzzing** - Inviare operazioni non supportate (write a read-only, etc.)
- **Sequence fuzzing** - Inviare operazioni in ordine inatteso
- **MTU fuzzing** - Negoziare MTU anomali

**Tool dedicati:**

- **BLEzzer** - Framework di fuzzing BLE open source
- **Sweyntooth** - Suite di exploit per vulnerabilità BLE stack
- **InternalBlue** - Framework per analisi Bluetooth a livello firmware
- **BTLE-Sniffer** - Tool per analisi e manipolazione BLE

Il Flipper può essere usato per fuzzing molto basilare (tentare connessioni, leggere servizi, scrivere valori), ma per fuzzing sistematico serve un setup Linux con dongle BLE e framework dedicati.

### BLE Denial of Service

L'invio massivo di advertising packets (BLE Spam) è di fatto una forma di Denial of Service soft sul canale BLE:

- **Saturazione canali advertising** - Con alta frequenza di advertising, i canali 37/38/39 si congestionano, rendendo difficile per dispositivi legittimi completare la discovery
- **Popup flooding** - Su dispositivi target, i popup continui rendono difficile l'uso normale del telefono
- **Battery drain** - Il processing continuo di advertising packets aumenta il consumo batteria dei dispositivi nelle vicinanze (effetto minimo ma misurabile)
- **Connection interference** - In rari casi, l'advertising aggressivo può interferire con connessioni BLE esistenti se il dispositivo target perde un connection event per processare l'advertising

Tuttavia, il BLE è resiliente al DoS grazie al frequency hopping e alla coesistenza con altri protocolli 2.4 GHz. Un singolo Flipper non può bloccare completamente il BLE in un'area.

> **Nota personale:** Ho testato l'impatto del BLE Spam sulla connettività BLE esistente. Con il Flipper che spamma a piena potenza, le connessioni BLE esistenti (cuffie, wearable) NON si disconnettono. L'impatto è limitato ai popup e a un leggero aumento della latenza nella discovery di nuovi dispositivi. Non è un DoS efficace contro connessioni attive - solo un'interferenza sull'esperienza utente. Per un vero DoS BLE servirebbero più trasmettitori o un jammer a 2.4 GHz (che è illegale).

---

