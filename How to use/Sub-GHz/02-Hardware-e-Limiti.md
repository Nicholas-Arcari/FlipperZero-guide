# Sub-GHz - Hardware e Limiti Reali

## Il Chip CC1101

Il cuore del modulo Sub-GHz è il **Texas Instruments CC1101**, un transceiver RF programmabile:

- **Frequenze:** 300-348, 387-464, 779-928 MHz (con gap tra le bande)
- **Modulazioni supportate:** 2-FSK, 4-FSK, GFSK, MSK, OOK/ASK
- **Sensibilità in ricezione:** -116 dBm @ 0.6 kBaud, 2-FSK
- **Potenza TX massima:** +12 dBm (~16 mW) - molto bassa per standard RF
- **Data rate:** 0.6 - 500 kBaud
- **Larghezza di banda:** configurabile, tipicamente 58-812 kHz

## Limiti Reali che Devi Conoscere

**Portata di trasmissione:** In condizioni ideali (linea di vista, nessuna interferenza) il Flipper raggiunge circa 30-50 metri. In ambienti reali (muri, interferenze, angoli) la portata scende a 5-15 metri. Questo è il limite più critico da conoscere.

**Potenza di trasmissione:** +12 dBm è molto poco. Un telecomando garage tipico trasmette a +13/+17 dBm, e un trasmettitore professionale arriva a +27 dBm. Il Flipper è significativamente più debole della maggior parte dei dispositivi che cerca di emulare.

**Gap di frequenza:** Il CC1101 NON copre 348-387 MHz e 464-779 MHz. Questo esclude le frequenze UHF TV, alcune bande PMR e molti sistemi militari/governativi.

**Antenna interna:** L'antenna PCB integrata è un compromesso. È ottimizzata per 433 MHz ma perde efficienza alle estremità delle bande. Antenne esterne migliorano significativamente le prestazioni.

**Nessun full-duplex:** Il CC1101 può solo trasmettere O ricevere, mai entrambi contemporaneamente.

> **Nota personale:** La portata limitata è il problema numero uno sul campo. Durante un physical pentest, devi avvicinarti molto al ricevitore target - spesso a meno di 10 metri in ambienti interni. Ho avuto casi dove il replay di un segnale di cancello funzionava perfettamente a 3 metri ma falliva a 8. Soluzione: avvicinarsi il più possibile e, se necessario, usare un'antenna esterna CC1101 collegata al GPIO.

## Migliorare le Prestazioni

**Antenna esterna CC1101:** Moduli CC1101 esterni con antenna SMA dedicata possono essere collegati via GPIO. Questo aumenta la portata a 100-200+ metri in linea di vista e migliora la sensibilità in ricezione.

**Collegamento antenna esterna:**
```
Flipper GPIO    CC1101 Module
GND         ->  GND
3.3V        ->  VCC
PA7 (MOSI)  ->  MOSI
PA6 (MISO)  ->  MISO
PB3 (SCK)   ->  SCK
PA4 (CS)    ->  CSN
PB2 (GDO0)  ->  GDO0
PC3 (GDO2)  ->  GDO2 (opzionale)
```
