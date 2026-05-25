# Tipi di Tag, Card e Protocolli

## MIFARE Classic 1K/4K

Il tag NFC più diffuso al mondo per sistemi di accesso e trasporti:

### Struttura MIFARE Classic 1K

- **16 settori** da 4 blocchi ciascuno
- **64 blocchi** totali, ognuno da 16 byte
- **1024 byte** di storage totale
- **Blocco 0:** UID (4 byte) + manufacturer data - di fabbrica, non scrivibile (su tag normali)
- **Blocco trailer (ultimo di ogni settore):** contiene Key A (6 byte) + Access Bits (4 byte) + Key B (6 byte)

### Struttura MIFARE Classic 4K

- **40 settori:** 32 da 4 blocchi + 8 da 16 blocchi
- **256 blocchi** totali
- **4096 byte** di storage
- Stessa logica di sicurezza del 1K

### Sicurezza: Crypto-1

MIFARE Classic usa l'algoritmo proprietario **Crypto-1** per l'autenticazione:
- Ogni settore è protetto da 2 chiavi: **Key A** e **Key B** (6 byte ciascuna)
- L'accesso ai dati richiede autenticazione con la chiave corretta
- **Crypto-1 è stato rotto nel 2008** - l'algoritmo ha solo 48 bit di stato interno
- Esistono attacchi pratici che recuperano le chiavi in secondi-minuti

### Chiavi di default comuni

```
FFFFFFFFFFFF - la più comune, default di fabbrica
A0A1A2A3A4A5 - MAD (MIFARE Application Directory)
D3F7D3F7D3F7 - NFC Forum
000000000000 - zero key
B0B1B2B3B4B5 - usata in alcuni sistemi trasporti
AABBCCDDEEFF - default di alcuni tool
4D3A99C351DD - usata da alcuni sistemi di accesso
1A982C7E459A - usata da alcuni distributori
```

---

## MIFARE Ultralight / NTAG

Tag semplici ed economici, tipicamente usa-e-getta:

### MIFARE Ultralight

- 64 byte di storage
- Nessuna crittografia
- Usato in biglietti monouso (metro, eventi)

### NTAG213/215/216

- 144 / 504 / 888 byte di storage
- Supporto NDEF (NFC Data Exchange Format)
- Password opzionale (4 byte - debole)
- Usato in smart poster, Amiibo (NTAG215), automazione

---

## MIFARE DESFire

Il successore sicuro di MIFARE Classic:

- **Crittografia:** DES, 3DES, AES-128
- **Autenticazione:** challenge-response con chiave simmetrica
- **File system:** struttura ad applicazioni e file (non settori)
- **Anti-clonazione:** UID random opzionale, diversified key
- **Storage:** EV1: 2K/4K/8K, EV2: fino a 4K/8K con funzionalità aggiuntive

**Implicazione per il pentest:** DESFire è significativamente più sicuro di MIFARE Classic. Non esistono attacchi pratici generici - l'attacco richiede la conoscenza delle chiavi o vulnerabilità specifiche dell'implementazione.

---

## iClass / PicoPass (HID)

Sistema proprietario HID Global, molto diffuso in contesti enterprise:

- **iClass Standard:** crittografia debole, chiavi master note → vulnerabile
- **iClass SE (Secure Identity):** crittografia forte, non vulnerabile ad attacchi generici
- **iClass SEOS:** ultima generazione, sicurezza robusta

---

## Altre Card

- **T-Union / Clipper / Navigo:** card trasporti con settori MIFARE Classic o DESFire
- **EMV (carte bancarie):** ISO 14443A/B + protocolli EMV con crittografia asimmetrica
- **Passaporti elettronici:** ISO 14443B + ICAO 9303, con BAC/PACE authentication

---

## MIFARE Classic - Deep Dive

### L'Attacco Crypto-1

L'algoritmo Crypto-1 è stato rotto nel 2007-2008 da ricercatori dell'Università di Radboud (Paesi Bassi). Le vulnerabilità principali:

1. **LFSR debole:** lo stato interno è solo 48 bit (cifrato troppo piccolo)
2. **Nonce prevedibile:** il tag genera nonce che non sono completamente random
3. **Correlazione tra bit:** relazioni tra output e stato interno permettono attacchi statistici

### MFKey32 - Come Funziona

L'attacco MFKey32 è quello usato dal Flipper per recuperare le chiavi MIFARE Classic:

**Prerequisiti:**
- Il Flipper deve emulare un tag e intercettare la comunicazione con un reader reale
- Servono almeno 2 autenticazioni catturate con lo stesso settore

**Procedura step-by-step:**

1. **Read il badge originale:** NFC → Read → avvicina il badge → salva il dump parziale
2. **Identifica le chiavi mancanti:** il dump avrà settori con "?" dove le chiavi non sono note (non erano nel dizionario)
3. **Emula il badge:** NFC → Emulate → seleziona il file → il Flipper emula il badge
4. **Presenta il Flipper al lettore reale:** avvicina il Flipper al lettore di badge dell'edificio
5. **Il lettore tenta di autenticarsi:** invia challenge al Flipper, il Flipper risponde (sbagliando, ma catturando i dati)
6. **Ripeti 2-3 volte** sullo stesso lettore
7. **Apri MFKey:** l'app analizza i dati catturati e calcola le chiavi
8. **Re-read il badge:** ora con le chiavi recuperate, fai un dump completo

> **Nota personale:** Il MFKey32 è l'attacco che uso più spesso in engagement reali. Funziona su circa il 70-80% dei sistemi MIFARE Classic che ho incontrato. Il trucco è presentare il Flipper al lettore in modo naturale - durante un social engineering, fingersi un dipendente che "ha problemi col badge" e avvicinare il Flipper al lettore. Servono 2-3 tentativi, 5 secondi ciascuno.

### Dictionary Attack

Prima di MFKey32, il Flipper tenta un **dictionary attack** - prova tutte le chiavi da un file dizionario:

**Dizionario integrato:** `/ext/nfc/assets/mf_classic_dict.nfc` (centinaia di chiavi note)
**Dizionario utente:** `/ext/nfc/assets/mf_classic_dict_user.nfc` (aggiungi le tue)

Le chiavi vengono provate in ordine. Se una chiave funziona per un settore, viene usata per leggere i dati di quel settore.

**Chiavi da aggiungere al dizionario personale:**
- Chiavi trovate online per il sistema target specifico
- Chiavi recuperate da engagement precedenti
- Chiavi estratte con Proxmark3 o ACR122U

> **Nota personale:** Mantengo un dizionario personalizzato con ~500 chiavi raccolte in anni di engagement. Include chiavi di sistemi di accesso italiani comuni (hotel, uffici, condomini). Ogni volta che recupero una chiave nuova, la aggiungo. Questo velocizza enormemente le letture future - spesso il dictionary attack trova tutto al primo tentativo su sistemi già visti.
