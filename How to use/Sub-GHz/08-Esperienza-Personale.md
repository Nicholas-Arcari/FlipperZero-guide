# Esperienza Personale e Troubleshooting - Sub-GHz

Note dal campo, errori commessi, lezioni apprese e soluzioni ai problemi più comuni durante l'uso operativo del modulo Sub-GHz.

---

## Troubleshooting

### "Read non decodifica niente"

| Causa | Soluzione |
|-------|----------|
| Frequenza sbagliata | Usa il Frequency Analyzer prima di Read |
| Modulazione sbagliata | Prova AM ↔ FM nel menu config |
| Troppo lontano dal trasmettitore | Avvicinati a <5 metri |
| Protocollo non supportato | Passa a Read RAW per cattura grezza |
| Antenna danneggiata | Esegui Sub-GHz Test per diagnostica |
| Interferenza ambientale | Sposta il Flipper lontano da fonti RF (router, telefoni) |
| Firmware non aggiornato | Alcuni protocolli sono stati aggiunti in aggiornamenti recenti |

### "Il replay non funziona"

| Causa | Soluzione |
|-------|----------|
| Rolling code | Il codice catturato è già stato "consumato" - non riutilizzabile |
| Portata insufficiente | Avvicinati al ricevitore (<3-5 metri per ambienti indoor) |
| Frequenza leggermente diversa | Verifica con Frequency Analyzer la frequenza esatta del ricevitore |
| Timing stretto del ricevitore | Il Flipper potrebbe non riprodurre il timing esatto - prova a ripetere |
| Ricevitore in modalità pairing | Alcuni ricevitori ignorano i segnali normali durante il pairing |
| Batteria scarica | La potenza TX cala con batteria bassa - ricarica e riprova |

### "Portata troppo corta"

| Causa | Soluzione |
|-------|----------|
| Antenna interna limitata | Usa antenna esterna CC1101 via GPIO |
| Muri/ostacoli | Posizionati in linea di vista con il ricevitore |
| Orientamento sbagliato | L'antenna PCB è orizzontale - orienta il Flipper di conseguenza |
| Batteria scarica | La potenza TX cala - ricarica |
| Ricevitore con bassa sensibilità | Non è colpa del Flipper - il ricevitore ha soglia alta |

### "File .sub troppo grande"

- Le registrazioni RAW possono pesare molto se registri a lungo
- Soluzione: registra solo 2-3 secondi di segnale
- Taglia il file manualmente rimuovendo il silenzio iniziale/finale
- Usa Shapshup per estrarre solo la porzione utile del segnale

### "Il Frequency Analyzer non mostra niente"

- Il trasmettitore è fuori range (<1 metro per l'Analyzer)
- La frequenza potrebbe essere nel gap del CC1101 (348-387 MHz o 464-779 MHz)
- Il segnale potrebbe essere troppo debole o a banda stretta
- Prova con antenna esterna per maggiore sensibilità

---

## Esperienza sul Campo

> **Nota personale - Cancelli residenziali italiani:** La maggior parte dei cancelli residenziali che ho testato in Italia usa sistemi Nice o Came. Quelli installati prima del 2010 sono quasi sempre a codice fisso (Nice FLO 12-bit, Came 12-bit) e sono triviali da clonare. Quelli dopo il 2012-2015 usano rolling code (Nice FLOR/Smilo, Came TOP). FAAC è sempre stato più avanti con la sicurezza - usa 868 MHz con rolling code robusto. BFT e Beninca sono misti.

> **Nota personale - Allarmi wireless:** Ho testato diversi sistemi di allarme consumer (quelli venduti nei centri commerciali). La maggior parte usa sensori a 433 MHz con codice fisso - bastano 30 secondi di cattura con Read per replicare il segnale "zona OK" e mascherare un'intrusione. I sistemi professionali (Tecnoalarm, Bentel, DSC) usano protocolli proprietari con rolling code e anti-jamming. Raccomando SEMPRE sistemi cablati per zone critiche.

> **Nota personale - Limiti reali del Flipper:** Il Flipper Zero è fantastico per la ricognizione e per attacchi rapidi su codici fissi, ma non è un sostituto per un setup SDR professionale. Per analisi seria uso HackRF + GNURadio per catturare e analizzare i segnali, e il Flipper per il replay. La combinazione dei due è potentissima: HackRF per capire, Flipper per agire.

> **Nota personale - TPMS in OSINT:** Durante un engagement OSINT ho usato il TPMS reader per 3 giorni nel parcheggio di un edificio target. Ho costruito una mappa completa degli orari di arrivo/partenza dei dipendenti basandomi sugli ID dei sensori TPMS. Questo senza telecamere, senza contatto fisico, senza essere rilevabile. È stato uno dei finding più impressionanti per il cliente.

> **Nota personale - Pager ospedalieri:** L'intercettazione POCSAG in un ospedale (autorizzata) è stata una delle esperienze più educative. I messaggi contenevano nomi pazienti, farmaci, numeri di stanza, codici di emergenza. Tutto in chiaro. Il report ha portato alla sostituzione del sistema pager con un'app criptata. Questo è il tipo di finding che giustifica l'intero engagement.

---

## Lezioni Apprese

### Errori da Non Ripetere

1. **Registrare RAW troppo a lungo** - i file diventano enormi e inutilizzabili. Massimo 3-5 secondi di registrazione.

2. **Non verificare la frequenza prima del Read** - ho perso 20 minuti a cercare di decodificare un segnale sulla frequenza sbagliata. Usa SEMPRE il Frequency Analyzer prima.

3. **Tentare il replay da troppo lontano** - i primi tentativi li facevo da 15-20 metri. Fallimento totale. Sotto i 5 metri in ambienti indoor è molto più affidabile.

4. **Non documentare i segnali catturati** - ho perso catture importanti perchè non le avevo rinominate. Adesso rinomino sempre con: `[target]_[freq]_[data]_[protocollo].sub`

5. **Ignorare il timing del protocollo** - alcuni ricevitori sono sensibili al timing. Se il replay non funziona, non è necessariamente rolling code - potrebbe essere un problema di timing.

### Best Practice Operative

- **Frequency Analyzer sempre per primo** - prima di qualsiasi operazione
- **Cattura multipla** - registra almeno 3 pressioni diverse dello stesso telecomando per confermare la coerenza
- **Naming convention** - `cancello_433_92_nice_flo_12bit.sub`
- **Backup SD** - fai backup della SD card prima di un engagement - le catture sono evidenza
- **Note contestuali** - salva un file di testo accanto ai .sub con note su dove, quando, come
- **Antenna esterna** - per engagement seri, porta sempre un modulo CC1101 esterno
- **Batteria** - carica completa prima dell'engagement. Il Sub-GHz consuma più degli altri moduli
