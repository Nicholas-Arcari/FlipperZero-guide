# Hardware e Limiti Reali - RFID 125 kHz

## L'Antenna LF del Flipper Zero

Il Flipper Zero integra un'antenna dedicata per la banda LF 125 kHz, separata dall'antenna NFC (13.56 MHz):

- **Tipo:** bobina stampata su PCB (copper trace coil)
- **Posizione:** parte inferiore del dispositivo, sotto lo schermo
- **Frequenza di risonanza:** sintonizzata su 125 kHz (con matching network)
- **Funzione duale:** sia lettore (genera campo) che emulatore (modula il carico)
- **Controller:** chip dedicato per la gestione del protocollo LF

L'antenna LF è fisicamente più grande di quella NFC, il che le conferisce un leggero vantaggio in termini di portata rispetto all'HF.

---

## Portata Reale

La portata dichiarata e quella reale divergono significativamente:

**In lettura (Flipper come lettore):**
- **EM4100:** 3-8 cm (dipende dalla dimensione del tag)
- **HID Prox (card formato ISO):** 3-6 cm
- **HID Prox (keyfob):** 2-4 cm (antenna più piccola)
- **FDX-B (impianto animale):** 1-3 cm (antenna microscopica)
- **T5577 (coin/card):** 3-7 cm

**In emulazione (Flipper come tag):**
- **Su lettore standard da muro:** 2-5 cm
- **Su lettore long-range:** 3-8 cm
- **Su lettore portatile:** 1-3 cm

**Fattori che influenzano la portata:**

| Fattore | Effetto |
|---|---|
| Dimensione antenna del tag | Più grande = più portata |
| Potenza del lettore | Lettori industriali > lettori consumer |
| Interferenze metalliche | Metallo vicino riduce drasticamente la portata |
| Orientamento | Bobine parallele = massima portata |
| Batteria del Flipper | Sotto il 20% la potenza TX cala |
| Cover/custodie | Custodie metalliche eliminano la lettura |
| Temperatura | Estremi termici riducono l'efficienza |

> **Nota personale:** La portata LF del Flipper è sensibilmente migliore di quella NFC. In media ottengo 5-8 cm su tag EM4100 formato card, contro i 2-4 cm tipici della lettura NFC MIFARE. Questo fa una differenza enorme nel pentesting: con LF puoi leggere un badge nella tasca posteriore di qualcuno passandogli relativamente vicino. Con NFC devi praticamente toccare il badge. Ho verificato questo in decine di engagement.

---

## Limiti di Potenza

Il Flipper Zero, essendo alimentato a batteria e con antenna piccola, ha limiti intrinseci:

- **Potenza del campo generato:** sufficiente per tag standard ma insufficiente per tag molto piccoli o schermati
- **Nessuna amplificazione esterna:** non è possibile collegare antenne LF esterne (a differenza del Sub-GHz con SMA)
- **Consumo in lettura continua:** circa 50-80 mA (drena la batteria in 3-4 ore)
- **Emulazione continua:** simile alla lettura, circa 60 mA

---

## Confronto con Proxmark3

Il Proxmark3 (specialmente la versione RDV4) è il gold standard per RFID/NFC nel pentesting. Ecco un confronto onesto:

| Caratteristica | Flipper Zero | Proxmark3 RDV4 |
|---|---|---|
| **Portata LF lettura** | 3-8 cm | 5-15 cm |
| **Portata LF emulazione** | 2-5 cm | 3-10 cm |
| **Protocolli LF supportati** | ~10 | 50+ |
| **Sniffing raw** | No | Si (fondamentale) |
| **Brute force ID** | Si (RFID Fuzzer) | Si (più veloce e configurabile) |
| **Demodulazione custom** | No | Si (qualsiasi modulazione) |
| **Scrittura T5577** | Si | Si (con più opzioni) |
| **Scrittura EM4305** | No | Si |
| **Analisi segnale raw** | No | Si (oscilloscopio integrato) |
| **Formato** | Tascabile, discreto | Ingombrante, richiede laptop |
| **Autonomia** | 4-6 ore | Alimentato via USB |
| **Prezzo** | ~170 EUR | ~300-400 EUR (RDV4) |
| **Curva di apprendimento** | Bassa | Alta (CLI-based) |
| **Discrezione** | Eccellente (sembra un giocattolo) | Pessima (sembra un dispositivo hacker) |

**Quando usare il Flipper:**
- Lettura/clonazione rapida di badge EM4100, HID, Indala
- Emulazione on-the-fly durante un engagement
- Ricognizione iniziale (che tipo di tag e'?)
- Situazioni dove la discrezione è fondamentale
- Badge standard senza protezioni particolari

**Quando serve il Proxmark3:**
- Analisi raw del segnale (demodulazione sconosciuta)
- Protocolli esotici non supportati dal Flipper
- Brute force massivo di ID
- Scrittura su tag diversi dal T5577 (EM4305, Q5, ecc.)
- Sniffing della comunicazione lettore-tag
- Ricerca e reverse engineering di protocolli proprietari

> **Nota personale:** Nel 90% degli engagement di physical pentesting in Italia, il Flipper Zero è sufficiente. I condomini usano EM4100, le aziende medio-piccole usano HID Prox senza crittografia. Il Proxmark3 mi serve solo per casi particolari: tag sconosciuti, sistemi industriali proprietari o quando devo fare sniffing passivo della comunicazione. Porto sempre entrambi, ma il Flipper esce dalla tasca 10 volte più spesso del Proxmark.
