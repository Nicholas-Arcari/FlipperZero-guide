## Hardware e Limiti Reali

### Il Chip STM32WB55

A differenza del modulo Sub-GHz (che usa un chip CC1101 separato), il BLE del Flipper Zero è integrato direttamente nel processore principale: lo **STM32WB55RGV6** di STMicroelectronics. Questo è un microcontrollore dual-core con radio BLE integrata:

**Architettura dual-core:**

- **Core applicativo (CM4)** - ARM Cortex-M4 @ 64 MHz, gestisce il firmware del Flipper, l'interfaccia utente, la logica applicativa
- **Core radio (CM0+)** - ARM Cortex-M0+ dedicato esclusivamente allo stack BLE, firmware separato e protetto

Questa architettura è importante: il core radio esegue un firmware BLE certificato da ST (il "Wireless Stack") che gestisce tutto il protocollo BLE a basso livello. Il core applicativo comunica con il core radio tramite un'interfaccia IPCC (Inter-Processor Communication Controller) e una mailbox condivisa in RAM.

**Specifiche radio BLE:**

| Parametro | Valore |
|---|---|
| Standard | Bluetooth 5.0 |
| Frequenza | 2.4 GHz ISM (2400-2483.5 MHz) |
| Canali | 40 (3 advertising + 37 dati) |
| Modulazione | GFSK |
| Potenza TX | -20 dBm a +6 dBm (configurabile) |
| Sensibilità RX | -96 dBm @ 1 Mbps |
| PHY supportati | LE 1M, LE 2M, LE Coded (S=8) |
| Throughput pratico | ~200-700 kbps |

**Potenza TX massima: +6 dBm.** Questo è il dato cruciale. +6 dBm equivale a circa 4 milliwatt. Per confronto, uno smartphone moderno trasmette BLE tipicamente a +4/+8 dBm, un beacon commerciale a +4/+8 dBm, e un dispositivo BLE long-range può arrivare a +20 dBm. Il Flipper è nella media bassa.

### Antenna PCB Integrata

Il Flipper Zero utilizza un'antenna PCB integrata stampata direttamente sulla scheda madre. Non è un'antenna esterna sostituibile come per il Sub-GHz. Caratteristiche:

- **Tipo:** Antenna a traccia PCB (Inverted-F o meander line)
- **Guadagno:** Circa 0-2 dBi (dipende dalla frequenza e dall'orientamento)
- **Pattern di radiazione:** Quasi-omnidirezionale sul piano orizzontale
- **Polarizzazione:** Lineare

L'antenna non è modificabile senza intervento hardware significativo. Questo è un limite fisso del Flipper: non puoi collegare un'antenna BLE esterna come fai con il CC1101 per il Sub-GHz.

### Portata Reale

La portata BLE del Flipper varia significativamente in base alle condizioni:

| Scenario | Portata Tipica |
|---|---|
| Linea di vista, esterno, nessuna interferenza | 20-30 metri |
| Interno, stessa stanza, pochi ostacoli | 10-20 metri |
| Interno, attraverso un muro | 5-15 metri |
| Interno, più muri, interferenze WiFi | 3-8 metri |
| Ambiente molto affollato (conferenza, ufficio) | 5-10 metri |

Fattori che degradano la portata:

- **Muri e ostacoli fisici** - Il 2.4 GHz penetra poco il cemento e il metallo
- **Interferenze WiFi** - WiFi opera sulla stessa banda e crea rumore
- **Bluetooth affollato** - In ambienti con molti dispositivi BLE, il canale si congestiona
- **Orientamento** - L'antenna PCB ha un pattern direzionale; ruotare il Flipper può fare differenza
- **Corpo umano** - Il corpo assorbe il 2.4 GHz; tenere il Flipper in tasca riduce la portata

> **Nota personale:** In ambienti reali di pentest, la portata effettiva per il BLE Spam è di circa 5-15 metri. Ho testato in uffici open space e la maggior parte dei dispositivi riceve i popup entro 10 metri. Oltre i 15 metri la percentuale di successo cala drasticamente. Per demo in meeting room, posizionare il Flipper al centro del tavolo è la strategia migliore - copertura garantita su tutto il tavolo e le sedie circostanti.

### Firmware del Core Radio

Il core CM0+ esegue il **STM32WB Wireless Stack**, un firmware binario fornito da ST:

- **stm32wb5x_BLE_Stack_full_fw.bin** - Stack BLE completo (GAP, GATT, SMP, L2CAP)
- Aggiornato tramite il firmware update del Flipper (OTA o via qFlipper)
- Non è open source - è un blob binario certificato
- Supporta fino a 8 connessioni simultanee
- Supporta advertising e scanning simultanei (se il firmware lo permette)

Il firmware custom del Flipper (RogueMaster, Unleashed, Momentum, Xtreme) non modifica lo stack wireless di ST. Modifica solo il firmware applicativo sul core CM4. Le differenze tra firmware custom per le funzionalità BLE riguardano quindi solo le applicazioni (BLE Spam, scanner, HID), non lo stack radio sottostante.

---

