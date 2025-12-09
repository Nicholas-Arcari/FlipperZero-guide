# Flipper Zero + RogueMaster

## Cos’è RogueMaster

RogueMaster è un firmware “custom” per Flipper Zero, un fork del firmware ufficiale (e di altri firmware community‑based) che aggiunge plugin, giochi, funzionalità extra e personalizzazioni.

Lo scopo è offrire un firmware “all‑in‑one”, con plugin e feature derivanti da vari progetti della comunità, senza dover compilare manualmente da zero.

---

## Perché usare RogueMaster - pro & benefici

- Plugin, applicazioni e giochi integrati “out of the box”: non serve compilare nulla
- Funzionalità estese rispetto al firmware stock: più compatibilità, più strumenti disponibili, extra come NFC, Sub‑GHz, IR, utilities aggiuntive
- Comunità e aggiornamenti relativamente attivi: il progetto viene mantenuto con nuove release periodiche
- Facilità d’installazione: per molti utenti non serve compilare: basta scaricare un .zip / .tgz e installare (via SD, qFlipper o “web installer”)

---

## Contro / Limitazioni / Cosa sapere

- Alcune build “ricche” con molti plugin/giochi/animazioni possono essere molto pesanti e rallentare il device
- Non è il firmware “ufficiale”: modifiche non ufficiali possono implicare rischi (compatibilità, stabilità, supporto, garanzia)
- Alcune funzionalità extra potrebbero richiedere una scheda microSD e la struttura giusta delle cartelle (es. per assets Sub‑GHz, NFC, giochi)
- Se si volesse massima flessibilità (plugin, compilazioni custom, fine controllo) potreste dover ricorrere a compilazioni manuali (o usare un firmware diverso), alcuni utenti segnalano che la natura “pre‑pacchettizzata” limita la personalizzazione totale

---

## Come installare RogueMaster - passaggi (con qFlipper / SD / Web)

Puoi seguire questi passaggi generali:

1. Assicurati che il tuo Flipper Zero abbia un firmware ufficiale aggiornato. 
2. Installa qFlipper sul tuo PC.
3. Visita la pagina delle release di RogueMaster su GitHub e scarica l’ultima versione disponibile ( https://github.com/RogueMaster/flipperzero-firmware-wPlugins/releases ).  
4. A seconda del metodo scelto:  
   - Metodo “Web Installer / SD card”: decomprimi l’archivio scaricato e copia i contenuti nella cartella `/update` della microSD del Flipper. Inserisci SD, riconnetti e lancia l’aggiornamento
   - Metodo qFlipper: collega il Flipper via USB, avvia qFlipper e carica il file firmware `.dfu` presente nel pacchetto RogueMaster
   - (In passato era possibile anche flash direttamente da device, ma questo metodo è meno consigliato/meno supportato dagli sviluppatori RogueMaster)
5. Dopo il flash, inserisci microSD (se richiesta), riavvia e verifica che tutto funzioni: plugin, giochi, IR / NFC / Sub‑GHz, ecc...  

Per chi preferisce seguire un tutorial video: ci sono guide step‑by‑step su YouTube che mostrano l’intero processo ( https://www.youtube.com/watch?v=0olHgqScuCQ )

---

## Note legali / disclaimer

RogueMaster è open‑source / pubblico su GitHub come fork del firmware ufficiale + contributi comunitari ( https://github.com/RogueMaster )

Il firmware originale del device (stock firmware) e il marchio “Flipper Zero” sono proprietà di Flipper Devices Inc. - RogueMaster *non è affiliato* né “ufficiale”

(Usare RogueMaster è a tuo rischio e pericolo: con firmware custom potresti invalidare garanzie, incorrere in comportamenti non previsti, o perdere supporto ufficiale)

---

## Licenza

- Firmware RogueMaster: distribuito sotto [GNU GPLv3](https://www.gnu.org/licenses/gpl-3.0.html). Qualsiasi modifica o redistribuzione del firmware deve rispettare questa licenza e rendere disponibile il codice sorgente.  

- Contenuti originali della repo (guide, tutorial, script): rilasciati sotto [MIT License](https://opensource.org/licenses/MIT). Puoi usarli liberamente, anche in progetti commerciali, mantenendo l’attribuzione.  

> Flipper Zero e i suoi marchi sono di proprietà di Flipper Devices Inc. RogueMaster non è affiliato né ufficialmente supportato da Flipper Devices.