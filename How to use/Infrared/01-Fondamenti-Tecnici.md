# Fondamenti Tecnici - Comunicazione Infrarossi

## Che cos'è la Comunicazione Infrarossi

La comunicazione infrarossi (IR) è una forma di trasmissione dati ottica che utilizza luce nello spettro infrarosso, invisibile all'occhio umano. Nel contesto dei telecomandi consumer e del Flipper Zero, si opera nella regione del **vicino infrarosso (NIR)** con lunghezza d'onda centrata su **940 nm** (nanometri).

A differenza delle comunicazioni radio (Sub-GHz, NFC), la comunicazione IR è **ottica e direzionale**: richiede un percorso relativamente libero tra trasmettitore e ricevitore (line-of-sight), anche se i rimbalzi su pareti e soffitti consentono un certo margine operativo in ambienti chiusi.

---

## Come Funziona - Dal LED al Bit

Il processo di comunicazione IR segue una catena precisa:

1. **Il trasmettitore** (telecomando, Flipper Zero) attiva un LED infrarosso a 940 nm
2. **Il LED emette impulsi** di luce IR - non un fascio continuo, ma una sequenza modulata
3. **La modulazione avviene su una portante** - tipicamente a **38 kHz** (la più comune), ma esistono dispositivi che usano 36 kHz, 40 kHz o 56 kHz
4. **Il ricevitore** (TV, AC, proiettore) contiene un fotodiodo + filtro + demodulatore che estrae il segnale utile dalla portante
5. **Il microcontrollore** del ricevitore decodifica la sequenza di bit e esegue il comando corrispondente

---

## Perchè Si Usa una Portante (Carrier Frequency)

Modulare il segnale IR su una portante a 38 kHz (o simile) serve a **distinguere il segnale utile dalla luce ambientale**. Il sole, le lampade a incandescenza e i neon emettono tutti radiazione infrarossa, ma nessuno di questi oscilla a 38 kHz. Il ricevitore IR è progettato con un filtro passa-banda centrato esattamente su quella frequenza, il che gli permette di:

- **Rigettare il rumore** della luce ambientale (che è "DC" o a frequenze molto diverse)
- **Amplificare solo il segnale** modulato alla frequenza corretta
- **Operare anche in ambienti luminosi** (outdoor con luce solare diretta, a patto che la distanza sia ridotta)

Il processo nel ricevitore:

```
Luce IR ricevuta → Fotodiodo → Filtro passa-banda 38kHz → Amplificatore → Demodulatore → Segnale digitale
```

Il demodulatore produce un'uscita digitale: **LOW** quando rileva la portante (burst) e **HIGH** quando non la rileva (space). Questo segnale demodulato è quello che il microcontrollore analizza per estrarre i bit.

---

## Duty Cycle

Il duty cycle della portante influenza la potenza del segnale e il consumo energetico:

- **Duty cycle tipico:** 25-33% (un terzo del periodo a livello alto)
- **Duty cycle 50%:** massima potenza ma massimo consumo - usato raramente nei telecomandi a batteria
- **Duty cycle 25%:** compromesso comune - sufficiente per attivare il ricevitore con minore consumo

Il Flipper Zero usa un duty cycle del **33%** per la trasmissione, che è il valore standard per la maggior parte dei protocolli consumer.

---

## Segnali Modulati vs RAW

Esistono due modi fondamentali di rappresentare un segnale IR:

**Segnale modulato (protocollo noto):**
Il segnale viene decodificato e rappresentato come protocollo + indirizzo + comando. Esempio: `NEC, Address: 0x04, Command: 0x08`. Questo è compatto e permette al Flipper di rigenerare il segnale perfetto.

**Segnale RAW:**
Il segnale viene registrato come sequenza grezza di tempi: durate dei burst (portante attiva) e degli space (silenzio), in microsecondi. Esempio: `9000 4500 560 560 560 1690 ...`. Questo metodo funziona per qualsiasi segnale IR, anche quelli con protocolli sconosciuti o proprietari, ma i file risultanti sono più grandi e possono avere piccole imprecisioni di timing.

> **Nota personale:** Nella pratica quotidiana, l'80% dei dispositivi consumer usa protocolli noti (NEC su tutti). Ma quando incontri un condizionatore con protocollo proprietario o un sistema di digital signage industriale, la cattura RAW diventa l'unica opzione. Tieni sempre presente la differenza: modulato = preciso e compatto, RAW = universale ma meno affidabile sulle lunghe distanze.

---

*Torna all'[indice principale](README.md)*
