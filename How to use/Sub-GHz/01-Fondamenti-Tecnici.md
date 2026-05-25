# Sub-GHz - Fondamenti Tecnici

## Che cos'è il Sub-GHz

Il termine "Sub-GHz" indica qualsiasi comunicazione radio a frequenza inferiore a 1 GHz. Nel contesto del Flipper Zero, copre le bande ISM (Industrial, Scientific, Medical) utilizzate globalmente per:

- **Telecomandi** per cancelli, garage, barriere, tapparelle
- **Sensori wireless** per allarmi, stazioni meteo, rilevatori fumo
- **Sistemi domotici** (Somfy, Nice, FAAC, Came, Beninca, ecc.)
- **Pager** (POCSAG su 466 MHz in Italia)
- **TPMS** (sensori pressione pneumatici, 433.92 MHz)
- **Chiavi auto** (315/433 MHz - solo analisi, non apertura)
- **Dispositivi industriali** (telemetria, SCADA wireless legacy)
- **Walkie-talkie analogici** (PMR446, FRS)
- **Telecomandi per droni** (protocolli FrSky, ELRS su 868/915 MHz)

## Come Funziona la Comunicazione RF

Un segnale Sub-GHz è un'onda elettromagnetica modulata che trasporta informazione digitale. Il processo base:

1. **Il trasmettitore** (telecomando) codifica un messaggio binario
2. **La modulazione** converte i bit in variazioni del segnale radio (ampiezza, frequenza o fase)
3. **Il segnale viaggia** nell'aria alla velocità della luce
4. **Il ricevitore** (centralina cancello) demodula il segnale e verifica il codice
5. **Se il codice è valido**, il ricevitore esegue l'azione (apre il cancello)

## Le Bande di Frequenza

Il Flipper Zero copre queste bande tramite il chip CC1101:

| Banda | Range | Uso Tipico | Regione |
|---|---|---|---|
| **300-348 MHz** | 300.00 - 348.00 MHz | Telecomandi legacy, sensori industriali | Globale |
| **387-464 MHz** | 387.00 - 464.00 MHz | Telecomandi garage (433.92), pager, TPMS, meteo | EU/Asia |
| **779-928 MHz** | 779.00 - 928.00 MHz | Telecomandi US (315), LoRa (868/915), sensori | US/EU |

Le frequenze più utilizzate nella pratica quotidiana:

- **315.00 MHz** - Telecomandi USA, chiavi auto mercato americano
- **433.92 MHz** - La più comune in Europa: cancelli, sensori, meteo, TPMS
- **434.42 MHz** - Variante usata da alcuni produttori EU
- **868.35 MHz** - Domotica EU (Somfy, EnOcean), allarmi
- **915.00 MHz** - ISM band americana, LoRa US

> **Nota personale:** Il 90% del lavoro sul campo in Italia si concentra su 433.92 MHz e 868.35 MHz. Ho raramente avuto bisogno di altre frequenze in engagement europei. I 315 MHz servono solo se si lavora con hardware importato dagli USA.
