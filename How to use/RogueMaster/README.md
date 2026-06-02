# Flipper Zero + RogueMaster

## Cos'è RogueMaster

RogueMaster è un firmware "custom" per Flipper Zero, un fork del firmware ufficiale (e di altri firmware community-based) che aggiunge plugin, giochi, funzionalità extra e personalizzazioni.

Lo scopo è offrire un firmware "all-in-one", con plugin e feature derivanti da vari progetti della comunità, senza dover compilare manualmente da zero.

---

## Download Firmware

**IMPORTANTE:** Scarica SEMPRE l'ultima versione dalla release page ufficiale. I firmware inclusi in questo repository sono obsoleti.

| Firmware | Link | Note |
|----------|------|------|
| **RogueMaster** | [GitHub Releases](https://github.com/RogueMaster/flipperzero-firmware-wPlugins/releases) | Firmware principale raccomandato |
| **Momentum** | [GitHub Releases](https://github.com/Next-Flip/Momentum-Firmware/releases) | Alternativa stabile |
| **Unleashed** | [GitHub Releases](https://github.com/DarkFlippers/unleashed-firmware/releases) | Alternativa popolare |
| **Firmware Ufficiale** | [GitHub Releases](https://github.com/flipperdevices/flipperzero-firmware/releases) | Stock, limitato per pentest |

> **Nota:** Le cartelle `Windows/` e `Linux & MacOS/` in questo repository contengono una vecchia versione del firmware (RM1112-0137-0.420.0) e possono essere eliminate per risparmiare ~1.1 GB di spazio. Scarica sempre la versione più recente dal link sopra.

---

## Perchè Usare un Firmware Custom

### Vantaggi rispetto al firmware ufficiale

- **Frequenze Sub-GHz sbloccate:** trasmissione su bande ristrette dal firmware ufficiale
- **Protocolli aggiuntivi:** rolling code tools, protocolli RFID extra, decoder aggiuntivi
- **App di terze parti:** centinaia di applicazioni pre-installate
- **Rolling Flaws:** analisi vulnerabilità rolling code (non presente nel firmware ufficiale)
- **Sub-GHz esteso:** bruteforcer, playlist, scheduler, tools avanzati
- **NFC/RFID extra:** fuzzer avanzato, protocolli aggiuntivi, Magic Card Gen4 support
- **BLE Spam:** non disponibile nel firmware ufficiale
- **Personalizzazione UI:** temi, animazioni, dolphin personalizzato

### Quale Scegliere

| Firmware | Pro | Contro | Consigliato Per |
|----------|-----|--------|----------------|
| **RogueMaster** | Più app/plugin, aggiornamenti frequenti | Pesante, a volte instabile | Chi vuole il massimo delle features |
| **Momentum** | Stabile, ben organizzato, UI moderna | Meno plugin di RM | Chi vuole stabilità + features |
| **Unleashed** | Leggero, stabile, community attiva | Meno app pre-installate | Chi preferisce installare solo quello che serve |
| **Ufficiale** | Più stabile, supporto Flipper | Poche features per pentest | Principianti, uso non-security |

> **Nota personale:** Uso RogueMaster come firmware principale per il lavoro. Momentum è la mia seconda scelta per quando RM ha bug. Il firmware ufficiale non ha senso per un pentester - troppe limitazioni. Il flash è reversibile e non invalida la garanzia hardware.

---

## Come Installare

### Metodo 1 - Web Installer (Più Semplice)

1. Vai sulla release page del firmware scelto
2. Cerca il link "Web Installer" (se disponibile)
3. Collega il Flipper via USB
4. Segui le istruzioni a schermo

### Metodo 2 - qFlipper

1. Scarica e installa [qFlipper](https://flipperzero.one/update) sul PC
2. Scarica il file `.dfu` dalla release page
3. Collega il Flipper via USB
4. In qFlipper: "Install from file" → seleziona il `.dfu`
5. Attendi il flash (~2 minuti)

### Metodo 3 - SD Card

1. Scarica l'archivio completo dalla release page
2. Decomprimi il contenuto nella cartella `/update/` della microSD
3. Sul Flipper: Settings → Storage → Update
4. Seleziona il pacchetto e conferma
5. Il Flipper si riavvia con il nuovo firmware

### Video Tutorial

- Flipper Zero - Tutorial Installazione RogueMaster ( https://www.youtube.com/watch?v=0olHgqScuCQ )

---

## Post-Installazione

### Verifica Funzionamento

1. Controlla la versione: Settings → About → Firmware Version
2. Verifica che le app extra siano presenti nel menu
3. Testa Sub-GHz: le frequenze sbloccate devono essere disponibili
4. Testa NFC/RFID: verifica che i protocolli extra siano presenti
5. Inserisci la microSD con gli asset necessari

### Struttura SD Card Consigliata

```
/ext/
├── subghz/assets/     ← Database frequenze e protocolli
├── nfc/assets/        ← Dizionari chiavi MIFARE
├── infrared/assets/   ← Database IR universale
├── badusb/            ← Script DuckyScript
├── apps/              ← Applicazioni aggiuntive
└── update/            ← Pacchetti firmware
```

---

## Note Legali / Disclaimer

- RogueMaster è open-source / pubblico su GitHub ( https://github.com/RogueMaster )
- Il firmware originale e il marchio "Flipper Zero" sono proprietà di Flipper Devices Inc.
- RogueMaster **non è affiliato** nè "ufficiale"
- Usare firmware custom è a proprio rischio: può invalidare garanzie, causare comportamenti non previsti, o perdere supporto ufficiale
- **Il possesso e l'uso del Flipper Zero con firmware custom è legale in Italia e nella UE.** L'uso improprio delle sue funzionalità no.

## Licenza

- Firmware RogueMaster: distribuito sotto [GNU GPLv3](https://www.gnu.org/licenses/gpl-3.0.html)
- Contenuti originali della repo (guide, tutorial, script): rilasciati sotto [MIT License](https://opensource.org/licenses/MIT)
