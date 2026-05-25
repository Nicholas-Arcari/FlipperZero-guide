## Troubleshooting e Limiti

### Problemi Comuni e Soluzioni

#### "Il Flipper non legge il tag"

**Cause possibili:**

| Causa | Diagnosi | Soluzione |
|---|---|---|
| Tag non è 125 kHz | Prova con NFC (13.56 MHz) | Usa il modulo NFC |
| Tag fuori portata | Avvicina di più | Contatto diretto con il Flipper |
| Orientamento sbagliato | Bobine non parallele | Ruota il tag di 90 gradi |
| Tag danneggiato | Prova un altro tag noto | Se anche il noto non funziona, problema del Flipper |
| Interferenza metallica | Metallo vicino all'antenna | Allontana oggetti metallici |
| Batteria scarica | Controlla livello batteria | Carica il Flipper |
| Protocollo non supportato | Il Flipper non decodifica | Usa Proxmark3 per l'analisi |
| Tag HF, non LF | Badge NFC scambiato per RFID | Controlla con il Detector |
| Cover metallica | Custodia del Flipper schermante | Rimuovi la custodia |

#### "La lettura è instabile / ID diversi ogni volta"

**Cause possibili:**
- Il tag ha un chip difettoso - prova un altro tag
- Interferenze ambientali - motori elettrici, trasformatori, neon vicini
- Il tag è multi-tecnologia (LF + HF) e il Flipper si confonde tra i due segnali
- Batteria del Flipper sotto il 20% - la potenza del campo cala

**Soluzione:** assicurati di mantenere il tag immobile durante la lettura. Se il problema persiste, usa il Proxmark3 per una lettura raw e verifica il segnale.

#### "L'emulazione non funziona sul lettore"

**Cause possibili e soluzioni:**

1. **Protocollo sbagliato:** il Flipper emula EM4100 ma il lettore aspetta HID
   - Soluzione: verifica il protocollo del lettore leggendo un badge che funziona

2. **Timing impreciso:** l'emulazione software non è identica al tag hardware
   - Soluzione: scrivi su T5577 (emulazione hardware, non software)

3. **Portata insufficiente:** il lettore richiede un segnale più forte
   - Soluzione: premi il Flipper direttamente sul lettore, prova diverse posizioni

4. **Il lettore è HF, non LF:** sembra un lettore RFID ma opera a 13.56 MHz
   - Soluzione: usa il Detector per verificare la frequenza

5. **Il lettore ha un database e l'ID non è autorizzato:**
   - Questo non è un bug - il sistema funziona correttamente
   - Soluzione: leggi un badge autorizzato e clona quello

6. **Firmware obsoleto:** il Flipper ha bug noti nell'emulazione LF
   - Soluzione: aggiorna il firmware all'ultima versione

#### "La scrittura su T5577 fallisce"

**Cause possibili e soluzioni:**

1. **Non è un T5577:** potrebbe essere un EM4100 (read-only) spacciato per T5577
   - Diagnosi: se il Flipper dice "Writing..." ma poi "Error", probabilmente non è scrivibile
   - Soluzione: prova un T5577 da un fornitore diverso

2. **T5577 protetto da password:** qualcuno ha impostato una password
   - Diagnosi: il Flipper mostra errore di scrittura anche a contatto
   - Soluzione: se conosci la password, usa il Raw Writer. Altrimenti, usa un nuovo T5577

3. **T5577 con Block 0 corrotto:** configurazione invalida scritta in precedenza
   - Diagnosi: il tag non risponde alla lettura nè alla scrittura
   - Soluzione: prova a scrivere Block 0 con valore standard (0x00148040) tramite Raw Writer. Se non funziona, il tag è irrecuperabile senza Proxmark3

4. **Posizionamento errato:** il T5577 non è abbastanza vicino
   - Soluzione: contatto diretto, immobile per 3 secondi

5. **Batteria scarica:** la scrittura richiede più potenza della lettura
   - Soluzione: carica il Flipper ad almeno il 50%

#### "Il Detector non rileva il lettore"

**Cause possibili:**

1. Il lettore è spento o in standby (alcuni si attivano solo su sensore di prossimità)
2. Il lettore opera a una frequenza non standard (es. 134.2 kHz per FDX-B)
3. Il lettore è troppo lontano - avvicinati a meno di 5 cm
4. Il lettore è schermato elettricamente (raro ma possibile)
5. Non è un lettore RFID - potrebbe essere un citofono, un sensore IR o un pulsante

#### "Il RFID Fuzzer non trova nessun ID valido"

**Possibili spiegazioni:**

1. **Il sistema ha un database restrittivo:** ottimo per la sicurezza, frustrante per il pentester
2. **Stai fuzzando il protocollo sbagliato:** verifica con un badge valido
3. **Il Facility Code è sbagliato:** per HID, devi avere il FC corretto
4. **Rate limiting:** il lettore blocca i tentativi rapidi - rallenta il fuzzing
5. **Lo spazio di ricerca è troppo grande:** per EM4100 a 40 bit, il brute force completo è impraticabile
6. **Il lettore non è standalone:** è collegato a un controller centrale che gestisce gli accessi - il fuzzing locale è inutile

### Limiti Intrinseci del Flipper Zero per RFID

1. **Nessun sniffing raw:** non puoi intercettare la comunicazione tra un badge e un lettore di terze parti (serve Proxmark3)
2. **Nessun password cracking:** non puoi recuperare la password di un T5577 protetto
3. **Protocolli limitati:** ~20 protocolli vs 50+ del Proxmark3
4. **Nessuna analisi del segnale:** non puoi visualizzare la forma d'onda raw
5. **Nessuna scrittura su EM4305:** supporta solo T5577 come target di scrittura
6. **Emulazione imperfetta:** l'emulazione software ha tolleranze di timing superiori a un tag fisico
7. **Portata fissa:** non puoi collegare antenne esterne per la banda LF
8. **Nessun supporto per tag a induzione a 134.2 kHz:** il supporto FDX-B è limitato perchè l'antenna è ottimizzata per 125 kHz

---

## Esperienza Personale

### La Realtà del RFID 125 kHz in Italia

> **Nota personale:** Dopo centinaia di engagement in Italia, posso dire con certezza che l'RFID 125 kHz è la tecnologia di accesso fisico PIù vulnerabile ancora in uso. La situazione è questa:

> **Condomini (90% EM4100):** la stragrande maggioranza dei condomini italiani costruiti o ristrutturati tra il 2000 e il 2020 ha un sistema di accesso basato su EM4100. I badge costano 2-5 EUR ciascuno, il sistema è economico da installare, e nessuno pensa alla sicurezza. Ho testato oltre 50 condomini e TUTTI erano vulnerabili alla clonazione in meno di 10 secondi. Non ho mai trovato un condominio italiano con crittografia sul badge.

> **Nota personale:** Il momento più assurdo della mia carriera è stato quando un amministratore di condominio mi ha detto: "Ma i badge sono elettronici, non si possono copiare come le chiavi!" - mentre io tenevo in mano un T5577 che avevo appena scritto in 5 secondi e che apriva il suo portone. La percezione di sicurezza dell'"elettronico" è completamente scollegata dalla realtà.

### Consigli Operativi da Campo

> **Nota personale: Kit RFID minimo per un engagement:**
> - 10x T5577 formato keyfob (vari colori per distinguerli)
> - 5x T5577 formato card ISO (per lettori che accettano solo card)
> - 1x T5577 formato coin (per casi particolari)
> - Nastro adesivo colorato per etichettare i cloni
> - Sacchetto antistatico per i T5577 vergini
> - Il Flipper Zero con batteria piena
> - Proxmark3 RDV4 nel backpack (per emergenze)
> - Powerbank da 5000 mAh (la lettura continua drena la batteria)

> **Nota personale: Errori che ho fatto e che dovresti evitare:**
>
> 1. **Non verificare il clone prima dell'uso:** una volta ho scritto un T5577 e sono andato direttamente al lettore target. Non funzionava. Il T5577 era difettoso e la scrittura non era andata a buon fine. Ora verifico SEMPRE leggendo il T5577 dopo la scrittura.
>
> 2. **Confondere LF e HF:** i badge moderni sono spesso dual-frequency (LF + HF). Il badge ha sia un chip EM4100 che un MIFARE. Il lettore potrebbe usare solo la parte HF. Il Detector ti salva da questo errore.
>
> 3. **Sottovalutare la portata di lettura:** pensavo servisse il contatto. In realtà con un buon posizionamento leggo EM4100 a 7-8 cm. Questo significa che posso leggere un badge nella tasca di una giacca appesa.
>
> 4. **Non proteggere i T5577 con password:** se perdi un T5577 clonato durante un engagement, chiunque lo trovi può leggere l'ID del badge del tuo cliente. Imposta sempre una password sul T5577 dopo la clonazione.
>
> 5. **Operare senza autorizzazione scritta:** già detto sopra, ma vale la pena ripeterlo. MAI.

### Quando il Flipper Non Basta

> **Nota personale:** Ci sono situazioni in cui il Flipper Zero non è sufficiente per il lavoro RFID 125 kHz:
>
> - **Protocollo sconosciuto:** il Flipper dice "Unknown" e non decodifica nulla. Il Proxmark3 con `lf search` e `lf rawdemod` può analizzare il segnale grezzo e identificare la modulazione.
>
> - **T5577 protetto da password:** il Flipper non ha una funzione di brute force per la password T5577. Il Proxmark3 con `lf t5 bruteforce` ci mette qualche minuto a provare le password comuni.
>
> - **Tag EM4305:** un'alternativa al T5577 che il Flipper non supporta per la scrittura. Serve il Proxmark3.
>
> - **Clonazione di FDX-B reale a 134.2 kHz:** il Flipper opera a 125 kHz e non può generare un segnale perfetto a 134.2 kHz. Per lettori FDX-B stretti sulla frequenza, serve un Proxmark3 o un lettore FDX-B dedicato.
>
> - **Analisi di lettori custom:** in ambienti industriali o militari, i lettori possono usare protocolli completamente proprietari. Il Proxmark3 con la sua capacità di cattura raw è l'unico strumento adeguato.
>
> - **Testing sotto copertura con portata estesa:** quando servono portate superiori a 10 cm (es. skimming test), il Flipper non ha la potenza. Serve hardware custom con amplificatore e antenna esterna.

### Il Futuro del 125 kHz

> **Nota personale:** L'RFID 125 kHz è una tecnologia morta che si rifiuta di morire. Le ragioni per cui è ancora ovunque:
>
> - **Costo:** un sistema EM4100 costa 1/10 di un sistema MIFARE DESFire
> - **Semplicità:** l'installatore non deve configurare chiavi crittografiche
> - **Compatibilità:** decenni di badge in circolazione, impossibile sostituirli tutti
> - **Ignoranza:** la maggior parte degli installatori e dei clienti non sa che è insicuro
> - **Inerzia:** "funziona, perchè cambiarlo?"
>
> La migrazione avverrà inevitabilmente, ma lentamente. Nel frattempo, l'RFID 125 kHz rimane il terreno di gioco più fertile per un pentester fisico. Un Flipper Zero e qualche T5577 in tasca - è tutto cio' che serve per dimostrare che il 90% dei sistemi di accesso fisico in Italia è un'illusione di sicurezza.

---

## Riferimenti e Risorse

### Datasheet e Specifiche

- **EM4100 Datasheet** - EM Microelectronic: struttura completa del protocollo
- **T5577 Datasheet (ATA5577)** - Microchip Technology: registri, configurazione, timing
- **HID Prox Formats** - HID Global Technical Reference Guide
- **ISO 11784/11785** - Standard internazionale per identificazione animale (FDX-B)
- **DCF77 Protocol** - PTB (Physikalisch-Technische Bundesanstalt) specification

### Strumenti Complementari

- **Proxmark3** (RDV4 o Easy) - per analisi avanzata e protocolli non supportati dal Flipper
- **RTL-SDR** - per visualizzare il segnale RF a 125 kHz (richiede upconverter)
- **GNURadio** - per demodulazione custom e analisi del segnale
- **RFIDler** - alternativa open source al Proxmark3 per LF

### Firmware Flipper Zero

- **Firmware ufficiale** - supporto base RFID 125 kHz
- **RogueMaster** - protocolli aggiuntivi, fuzzer migliorato
- **Unleashed** - protocolli aggiuntivi e features extra
- **Xtreme** - UI migliorata e tool aggiuntivi

> **Nota personale:** Uso RogueMaster come firmware principale per il lavoro RFID. Supporta più protocolli del firmware ufficiale e il fuzzer ha opzioni aggiuntive. Per un pentester, il firmware custom è praticamente obbligatorio. Il firmware ufficiale è perfetto per imparare, ma in campo servono le features extra.

---

*Guida scritta per il progetto FlipperZero-guide. Contenuto a scopo educativo e di ricerca sulla sicurezza. L'uso improprio delle tecniche descritte è illegale e perseguibile penalmente. Operare sempre con autorizzazione scritta.*
