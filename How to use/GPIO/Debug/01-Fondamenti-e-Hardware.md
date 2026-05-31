## 1. Fondamenti -- Il Flipper Zero come tool di Hardware Hacking

### Perche il debug hardware e fondamentale

Ogni dispositivo embedded -- router, telecamere IP, serrature smart, centraline automotive, PLC industriali -- alla fine dei conti e un microcontrollore con del firmware che gira sopra. Quel firmware contiene la logica di business, le chiavi crittografiche, le credenziali hardcoded, le vulnerabilita. Per accedervi, servono interfacce fisiche.

Il Flipper Zero, grazie ai suoi pin GPIO e al firmware open source, diventa un coltellino svizzero per il debug hardware. Non sostituisce un J-Link o un Saleae Logic da banco, ma e qualcosa che porti in tasca, che funziona a batteria, e che in un assessment sul campo fa la differenza.

### Le porte d'ingresso del reverse engineering hardware

Ogni PCB che analizzi durante un pentest hardware ha potenzialmente queste interfacce esposte:

**SWD (Serial Wire Debug)**
- Protocollo ARM a 2 fili (SWCLK + SWDIO)
- Accesso diretto alla CPU: halt, resume, lettura/scrittura memoria, flash
- IL protocollo piu importante per il pentest di dispositivi ARM Cortex-M
- Presente su praticamente ogni MCU ARM in produzione
- Spesso lasciato esposto anche su prodotti finali

**JTAG (Joint Test Action Group)**
- Protocollo standard IEEE 1149.1
- 4-5 fili: TCK, TMS, TDI, TDO (+ opzionale TRST)
- Piu complesso di SWD ma piu versatile
- Usato su processori piu potenti (Cortex-A, MIPS, RISC-V)
- Permette boundary scan per testare ogni pin del chip

**UART (Universal Asynchronous Receiver/Transmitter)**
- Seriale asincrona a 2 fili (TX + RX)
- La PRIMA cosa da cercare su qualsiasi PCB
- Spesso collegata alla console di boot (U-Boot, Linux shell)
- Baud rate comuni: 9600, 19200, 38400, 57600, 115200
- Se trovi una shell root su UART, il gioco e fatto

**SPI (Serial Peripheral Interface)**
- Bus sincrono: MOSI, MISO, SCK, CS
- Usato per memorie flash esterne (firmware storage)
- La tecnica piu usata per estrarre firmware da dispositivi
- Clip SOIC-8 per leggere senza dissaldare

**I2C (Inter-Integrated Circuit)**
- Bus a 2 fili: SDA + SCL
- Collegamento tra MCU e periferiche (sensori, EEPROM, RTC, display)
- Scan del bus per trovare dispositivi "nascosti"
- Accesso a EEPROM con configurazioni e dati sensibili

### Perche il Flipper Zero e diverso da altri tool

| Caratteristica | Flipper Zero | J-Link EDU | Bus Pirate | Multimetro |
|---|---|---|---|---|
| Portatile (a batteria) | Si | No | No | Si |
| SWD Probe | Si | Si | No | No |
| SPI Flash Reader | Si | No | Si | No |
| I2C Scanner | Si | No | Si | No |
| Display integrato | Si | No | No | Si |
| Costo | ~170 EUR | ~60 EUR | ~35 EUR | Variabile |
| Open Source FW | Si | No | Si | No |

Il punto non e che il Flipper sia il migliore in assoluto su ogni singola funzione. Il punto e che li ha TUTTI in un device tascabile, con batteria, display, e un firmware che puoi modificare.

### Setup hardware di base

Pin GPIO del Flipper Zero usati per il debug:

```
Pin  | Funzione        | Colore suggerito
-----|-----------------|------------------
 2   | SWCLK / SCK     | Giallo
 3   | SWDIO / MOSI    | Verde
 4   | MISO            | Blu
 5   | CS (Chip Select)| Bianco
 6   | SDA (I2C)       | Verde
 7   | SCL (I2C)       | Giallo
 8   | GND             | Nero
 9   | 3.3V Out        | Rosso
 11  | TX (UART)       | Arancione
 13  | RX (UART)       | Marrone
```

> Nota personale: prima di collegare qualsiasi cosa, verifica SEMPRE la tensione di lavoro del target. Il Flipper lavora a 3.3V. Se il target e a 5V, rischi di bruciare la porta GPIO. Un level shifter da pochi euro puo salvarti il dispositivo. Mi e capitato di bruciare un pin su un Flipper collegandolo a un AVR a 5V senza pensarci -- errore da principiante che non ripetero.

### Filosofia operativa

Quando ti trovi davanti a un dispositivo da analizzare, segui sempre questo ordine:

1. **Ispezione visiva** -- Cerca header non popolati, test pad, serigrafia con label come "UART", "DBG", "JTAG", "SWD", "J1"
2. **UART scan** -- Cerca TX con oscilloscopio o logic analyzer (o anche solo un multimetro in AC)
3. **I2C scan** -- Collega SDA/SCL e scansiona il bus per trovare dispositivi
4. **SWD/JTAG probe** -- Prova a connetterti alla MCU principale
5. **SPI dump** -- Se c'e una flash esterna, dumpa il firmware
6. **Analisi firmware** -- binwalk, Ghidra, strings, entropy analysis

---

