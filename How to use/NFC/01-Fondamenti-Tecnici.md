# Fondamenti Tecnici NFC

## Che cos'è NFC

NFC (Near Field Communication) è una tecnologia di comunicazione wireless a corto raggio basata su induzione elettromagnetica a **13.56 MHz**. A differenza del Sub-GHz che lavora a decine di metri, NFC opera a distanze di **pochi centimetri** (1-10 cm tipicamente).

NFC si basa sugli standard:

- **ISO 14443 Type A** - il più diffuso: MIFARE Classic, MIFARE DESFire, NTAG, MIFARE Ultralight
- **ISO 14443 Type B** - usato in documenti di identità (passaporti), alcune card bancarie
- **ISO 15693 (NFC-V)** - tag a lungo raggio (fino a 1 metro), usato in logistica e librerie
- **FeliCa** - standard Sony, diffuso in Giappone (Suica, PASMO)

---

## Come Funziona la Comunicazione NFC

La comunicazione NFC è di tipo **master-slave**:

1. **Il reader** (lettore, es. tornello) genera un campo elettromagnetico a 13.56 MHz
2. **Il tag** (card/badge) entra nel campo e riceve energia per induzione
3. Il tag si "sveglia" e risponde modulando il campo del reader (**load modulation**)
4. Avviene un **anti-collision** se ci sono più tag nel campo
5. Il reader seleziona un tag specifico tramite il suo **UID** (Unique ID)
6. Inizia la comunicazione: autenticazione, lettura/scrittura dati

**Il tag è passivo** - non ha batteria. Tutta l'energia viene dal campo del reader. Eccezione: i telefoni NFC possono funzionare sia come reader che come tag.

---

## Struttura di un Tag ISO 14443A

Ogni tag ISO 14443A ha almeno:

- **UID (Unique Identifier):** 4, 7 o 10 byte - identifica univocamente il tag
  - UID 4 byte: MIFARE Classic 1K/4K (il più comune)
  - UID 7 byte: MIFARE Classic EV1, NTAG, DESFire
  - UID 10 byte: raro, usato in applicazioni speciali
- **SAK (Select Acknowledge):** 1 byte - indica il tipo di tag
  - SAK 0x08: MIFARE Classic 1K
  - SAK 0x18: MIFARE Classic 4K
  - SAK 0x20: MIFARE DESFire / MIFARE Plus
  - SAK 0x00: MIFARE Ultralight / NTAG
  - SAK 0x04: MIFARE Mini
- **ATQA (Answer To Request A):** 2 byte - ulteriore identificazione

> **Nota personale:** Il SAK è la prima cosa che guardo quando leggo un badge sconosciuto. SAK 0x08 = MIFARE Classic 1K = probabilmente vulnerabile a crypto1 attack. SAK 0x20 = DESFire = servirà molto più lavoro. Questa distinzione immediata ti dice in 2 secondi se il badge sarà facile o difficile da clonare.
