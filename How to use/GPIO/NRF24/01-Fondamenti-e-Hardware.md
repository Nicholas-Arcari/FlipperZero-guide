## 1. Fondamenti Tecnici del NRF24L01+

### 1.1 Panoramica del chip

Il NRF24L01+ è un transceiver RF a 2.4 GHz prodotto da Nordic Semiconductor. È uno dei chip radio più diffusi al mondo per comunicazioni wireless a corto e medio raggio, usato in milioni di dispositivi: mouse wireless, tastiere, telecomandi, sensori IoT, giocattoli, sistemi domotici, droni economici.

Caratteristiche principali:

- Banda ISM 2.4 GHz (2400-2525 MHz) -- non richiede licenza
- 126 canali RF selezionabili (da 2400 a 2525 MHz, con step di 1 MHz)
- Data rate configurabile: 250 kbps, 1 Mbps, 2 Mbps
- Potenza di trasmissione massima: +0 dBm (1 mW) sulla versione base
- Sensibilità RX: -85 dBm a 1 Mbps, -94 dBm a 250 kbps
- Alimentazione: 1.9V-3.6V (tipicamente 3.3V)
- Interfaccia SPI per la comunicazione con il microcontroller host
- Consumo ultra-basso in standby: 900 nA
- Consumo in TX a 0 dBm: 11.3 mA
- Consumo in RX a 1 Mbps: 12.3 mA

### 1.2 Architettura interna

Il NRF24L01+ integra:

- Sintetizzatore di frequenza RF
- Amplificatore di potenza (PA)
- Amplificatore a basso rumore (LNA)
- Modulatore/demodulatore GFSK (Gaussian Frequency Shift Keying)
- Enhanced ShockBurst engine (hardware)
- FIFO TX e RX (3 livelli x 32 byte ciascuno)
- Generatore CRC (1 o 2 byte)
- Regolatore di tensione integrato

L'architettura è progettata per scaricare il più possibile del protocollo radio dall'MCU host al chip stesso, riducendo il carico computazionale e il consumo energetico complessivo.

### 1.3 I 126 canali RF

Lo spettro operativo va da 2400 MHz a 2525 MHz. Ogni canale occupa una larghezza di banda che dipende dal data rate selezionato:

- A 250 kbps e 1 Mbps: larghezza di banda del canale < 1 MHz
- A 2 Mbps: larghezza di banda del canale < 2 MHz

Per evitare sovrapposizioni a 2 Mbps, i canali dovrebbero essere distanziati di almeno 2 MHz. A 1 Mbps o 250 kbps, 1 MHz di separazione è sufficiente.

La formula per la frequenza operativa e':

```
F_operativa = 2400 + CH [MHz]
```

Dove CH è il numero del canale (0-125).

Esempio: canale 76 = 2476 MHz.

I canali più bassi (0-20) e più alti (100-125) tendono ad avere meno interferenze dal Wi-Fi, che opera principalmente sui canali 1, 6, 11 (corrispondenti a 2412, 2437, 2462 MHz con larghezza di 22 MHz ciascuno).

### 1.4 Data Pipe -- 6 pipe per indirizzo

Una delle caratteristiche più potenti del NRF24L01+ è il supporto per 6 data pipe simultanee in ricezione. Ogni pipe ha un indirizzo unico (da 3 a 5 byte) e può ricevere dati indipendentemente.

- Pipe 0: indirizzo completo configurabile (3-5 byte)
- Pipe 1: indirizzo completo configurabile (3-5 byte)
- Pipe 2-5: condividono i byte alti con Pipe 1, differiscono solo per il byte meno significativo

Questo schema permette a un singolo ricevitore di comunicare con fino a 6 trasmettitori diversi, ciascuno identificato dal proprio indirizzo pipe.

Nel contesto del pentest, le pipe sono fondamentali: quando si fa sniffing, si deve configurare l'indirizzo pipe corretto per catturare il traffico di un dispositivo specifico. Il MouseJacker sfrutta proprio la conoscenza degli indirizzi pipe per inserirsi nella comunicazione.

### 1.5 Enhanced ShockBurst (ESB)

L'Enhanced ShockBurst è il protocollo hardware integrato nel NRF24L01+ che gestisce automaticamente:

- Assemblaggio pacchetto (preambolo + indirizzo + payload + CRC)
- Auto-ACK: il ricevitore invia automaticamente un acknowledgement al trasmettitore
- Auto-retransmit: se l'ACK non arriva, il trasmettitore ripete la trasmissione (configurabile da 1 a 15 tentativi, con delay da 250us a 4000us)
- Gestione FIFO TX/RX a livello hardware

Formato del pacchetto ESB:

```
| Preambolo (1 byte) | Indirizzo (3-5 byte) | PCF (9 bit) | Payload (0-32 byte) | CRC (1-2 byte) |
```

Il PCF (Packet Control Field) contiene:

- Payload length (6 bit)
- PID -- Packet ID (2 bit) per rilevare pacchetti duplicati
- NO_ACK flag (1 bit) per disabilitare l'ACK per singolo pacchetto

L'ESB è un'arma a doppio taglio per la sicurezza:

- Pro (per il difensore): il meccanismo di ACK fornisce affidabilità
- Contro (per il difensore): il protocollo è completamente in chiaro, senza crittografia nè autenticazione. Chiunque conosca l'indirizzo pipe può iniettare pacchetti

> Nota personale: l'Enhanced ShockBurst è il cuore di tutto cio' che facciamo con il NRF24 sul Flipper. Capire come funziona a livello di pacchetto è essenziale. Ho passato settimane a studiare i datasheet Nordic prima di sentirmi davvero a mio agio con lo sniffing avanzato. Il consiglio è di leggere almeno il capitolo 7 del datasheet originale del NRF24L01+ -- è sorprendentemente ben scritto.

### 1.6 Potenza TX e sensibilità RX

La potenza di trasmissione è configurabile su 4 livelli:

| Livello | Potenza TX | Consumo corrente |
|---------|-----------|-----------------|
| 0       | -18 dBm   | 7.0 mA          |
| 1       | -12 dBm   | 7.5 mA          |
| 2       | -6 dBm    | 9.0 mA          |
| 3       | 0 dBm     | 11.3 mA         |

La sensibilità del ricevitore varia con il data rate:

| Data Rate | Sensibilità RX |
|-----------|----------------|
| 250 kbps  | -94 dBm        |
| 1 Mbps    | -85 dBm        |
| 2 Mbps    | -82 dBm        |

A 250 kbps si ha la massima sensibilità (-94 dBm) e quindi la massima portata, a scapito della velocità. È il data rate consigliato per lo sniffing a lunga distanza.

### 1.7 Data rate: 250 kbps vs 1 Mbps vs 2 Mbps

La scelta del data rate influenza direttamente:

- Portata: 250 kbps raggiunge le distanze maggiori
- Larghezza di banda del canale: 2 Mbps richiede canali più larghi
- Throughput: 2 Mbps per trasferimenti veloci, 250 kbps per sensori low-power
- Compatibilità: molti dispositivi economici usano 1 Mbps o 2 Mbps

Per il pentest con Flipper Zero:

- Sniffing generico: 1 Mbps (il default della maggior parte dei dispositivi)
- Sniffing a lunga distanza: 250 kbps
- MouseJacker: il data rate deve corrispondere a quello della periferica target (tipicamente 2 Mbps per Logitech Unifying)

---

## 2. Hardware

### 2.1 Versioni del modulo NRF24L01+

Esistono due versioni principali del modulo comunemente disponibili:

**Versione base (antenna PCB integrata):**

- Antenna stampata direttamente sul PCB
- Potenza TX: 0 dBm (1 mW)
- Portata reale in interno: 10-30 metri (con ostacoli)
- Portata reale in esterno (line of sight): 50-80 metri
- Costo: 1-2 euro
- Dimensioni: circa 15mm x 29mm
- Header a 8 pin (2x4)

**Versione PA+LNA (antenna SMA esterna):**

- Power Amplifier esterno + Low Noise Amplifier
- Potenza TX: fino a +20 dBm (100 mW) con il modulo RFX2401C
- Portata reale in interno: 50-100 metri
- Portata reale in esterno (line of sight): 200-1000 metri (con antenna direzionale)
- Costo: 3-5 euro
- Dimensioni: circa 40mm x 17mm
- Connettore SMA per antenna esterna
- Header a 8 pin (2x4)

Per il pentest, la versione PA+LNA è fortemente consigliata:

- La portata extra permette operazioni da distanze sicure
- L'antenna esterna è sostituibile (si può usare una direzionale Yagi)
- La sensibilità RX migliorata dal LNA cattura pacchetti che la versione base perderebbe

> Nota personale: ho iniziato con la versione base da 1.50 euro su AliExpress e funzionava, ma la portata era frustrante. Con la PA+LNA il salto di qualità è enorme. Per meno di 5 euro si ha un trasmettitore che raggiunge facilmente un ufficio intero dal corridoio. Se montate un'antenna Yagi da 8 dBi, la portata in line-of-sight supera i 300 metri -- testato personalmente in un parcheggio vuoto.

### 2.2 Pinout e collegamento GPIO al Flipper Zero

Il modulo NRF24L01+ comunica via SPI. Il collegamento al Flipper Zero avviene tramite il connettore GPIO superiore.

**Pinout del modulo NRF24L01+ (visto dall'alto, header in basso):**

```
         +-----+-----+
         | GND | VCC |
         +-----+-----+
         | CE  | CSN |
         +-----+-----+
         | SCK | MOSI|
         +-----+-----+
         | MISO| IRQ |
         +-----+-----+
```

**Collegamento al Flipper Zero GPIO:**

| NRF24 Pin | Funzione      | Flipper Zero Pin |
|-----------|---------------|------------------|
| VCC       | Alimentazione | 3.3V (pin 9)    |
| GND       | Massa         | GND (pin 8)      |
| CE        | Chip Enable   | GPIO C0 (pin 15) |
| CSN       | Chip Select   | GPIO A4 (pin 2)  |
| SCK       | SPI Clock     | GPIO B3 (pin 4)  |
| MOSI      | SPI Data In   | GPIO A7 (pin 6)  |
| MISO      | SPI Data Out  | GPIO A6 (pin 5)  |
| IRQ       | Interrupt     | Non collegato    |

Il pin IRQ non è utilizzato dalla maggior parte delle applicazioni Flipper Zero per NRF24. Può essere lasciato non collegato senza problemi.

### 2.3 Alimentazione -- attenzione ai 3.3V

Questo è un punto critico. Il NRF24L01+ funziona a 3.3V e NON tollera 5V sui pin di I/O nè sull'alimentazione. Collegare 5V distrugge il chip istantaneamente.

Il Flipper Zero fornisce 3.3V dal suo regolatore interno, perfettamente compatibile.

Problemi comuni di alimentazione:

- **Corrente insufficiente**: il NRF24L01+ può assorbire picchi di 115 mA in trasmissione (versione PA+LNA). Se il regolatore del Flipper non riesce a fornire abbastanza corrente, si verificano reset del modulo, comunicazioni fallite, comportamento erratico.
- **Soluzione**: aggiungere un condensatore elettrolitico da 10-47 uF tra VCC e GND del modulo, il più vicino possibile ai pin. Questo stabilizza l'alimentazione durante i picchi di corrente.
- **Filtro aggiuntivo**: un condensatore ceramico da 100 nF in parallelo al condensatore elettrolitico filtra il rumore ad alta frequenza.

Per la versione PA+LNA:

- Il consumo in TX a massima potenza (+20 dBm) raggiunge 115 mA
- Il regolatore del Flipper può andare in sofferenza
- Considerare un'alimentazione esterna da 3.3V se si notano problemi
- Il condensatore da 47 uF è quasi obbligatorio

> Nota personale: il condensatore è la differenza tra un modulo che funziona al 50% e uno che funziona al 100%. Ho perso due giorni a debuggare problemi di comunicazione SPI prima di scoprire che era semplicemente un problema di alimentazione. Da quando saldo un condensatore da 47uF tra VCC e GND di ogni modulo NRF24, zero problemi. È un consiglio che do a chiunque.

### 2.4 Portata reale -- aspettative vs realtà

La portata dipende da molti fattori:

- Versione del modulo (base vs PA+LNA)
- Tipo di antenna (PCB, dipolo, Yagi)
- Data rate selezionato
- Potenza TX configurata
- Ambiente (indoor/outdoor, muri, interferenze Wi-Fi)
- Orientamento dell'antenna
- Frequenza del canale utilizzato

Tabella portata reale misurata (approssimativa):

| Configurazione                     | Indoor | Outdoor LOS |
|------------------------------------|--------|-------------|
| Base, antenna PCB, 1 Mbps          | 15m    | 50m         |
| Base, antenna PCB, 250 kbps        | 25m    | 80m         |
| PA+LNA, dipolo 2 dBi, 1 Mbps      | 50m    | 200m        |
| PA+LNA, dipolo 2 dBi, 250 kbps    | 80m    | 400m        |
| PA+LNA, Yagi 8 dBi, 250 kbps      | N/A    | 800m+       |

Per il MouseJacker, la portata operativa è tipicamente 10-50 metri in un ambiente d'ufficio con la versione PA+LNA. Sufficiente per operare dalla sala riunioni accanto o dal corridoio.

### 2.5 Assemblaggio pratico

Il modo più pulito per collegare il modulo NRF24L01+ al Flipper Zero è tramite una scheda adattatrice dedicata o un cablaggio con cavetti Dupont femmina-femmina.

Procedura consigliata:

1. Usare cavetti Dupont femmina-femmina da 10-15 cm
2. Collegare ogni pin secondo la tabella sopra
3. Saldare il condensatore da 47 uF direttamente sui pin VCC/GND del modulo
4. Fissare i cavetti con nastro Kapton per evitare disconnessioni
5. Verificare i collegamenti con un multimetro prima di accendere
6. Verificare che VCC sia su 3.3V e NON su 5V

Se si usa una proto board o un PCB adattatore personalizzato:

- Mantenere le piste SPI il più corte possibile
- Aggiungere un piano di massa sotto le piste SPI
- Posizionare i condensatori di bypass il più vicino possibile al modulo

---

