# Hardware e Limiti Reali - Modulo IR Flipper Zero

## LED Trasmettitore - TSAL6200

Il Flipper Zero monta un LED IR **Vishay TSAL6200** come trasmettitore:

| Parametro | Valore |
|---|---|
| **Lunghezza d'onda di picco** | 940 nm |
| **Angolo di emissione (half-angle)** | +-17 gradi (totale ~34 gradi) |
| **Corrente forward tipica** | 100 mA |
| **Corrente forward di picco** | 200 mA (impulsi) |
| **Potenza radiante** | ~35 mW/sr @ 100mA |
| **Tempo di salita/discesa** | ~800 ns |

Il TSAL6200 è un LED ad alta potenza per la sua categoria, ma resta un singolo LED. I telecomandi commerciali spesso montano 2-3 LED in parallelo per aumentare la potenza e l'angolo di copertura. Il Flipper, avendo un solo LED, ha una portata TX inferiore a molti telecomandi dedicati.

---

## Ricevitore - TSOP75338

Il Flipper Zero usa un ricevitore IR **Vishay TSOP75338** (o equivalente nella stessa famiglia):

| Parametro | Valore |
|---|---|
| **Frequenza portante ottimale** | 38 kHz |
| **Range frequenze accettate** | ~33-41 kHz (con sensibilità ridotta ai bordi) |
| **Sensibilità** | molto alta - rileva segnali deboli |
| **Distanza di ricezione** | fino a 15-20 metri (da telecomandi potenti) |
| **Filtro luce ambientale** | integrato |
| **Uscita** | attiva bassa (LOW = burst rilevato) |
| **Alimentazione** | 2.5-5.5V |

Il TSOP75338 è ottimizzato per 38 kHz. Segnali a 36 kHz o 40 kHz vengono comunque ricevuti, ma con sensibilità ridotta (circa -3 dB per ogni 2 kHz di scostamento). Segnali a 56 kHz (usati da alcuni sistemi Bang & Olufsen) vengono ricevuti con difficoltà o non ricevuti affatto.

---

## Portata Reale - TX vs RX

Questa è la distinzione più importante da capire:

**Portata in trasmissione (TX):**
- **Condizioni ideali** (stanza buia, line-of-sight diretto, ricevitore sensibile): **5-8 metri**
- **Condizioni reali** (luce ambientale, angolo non perfetto): **3-5 metri**
- **Condizioni pessime** (luce solare diretta, angolo ampio, ricevitore poco sensibile): **1-2 metri**

**Portata in ricezione (RX):**
- **Da telecomando potente** (multi-LED): **15-20 metri**
- **Da singolo LED telecomando** standard: **8-12 metri**
- **Da altro Flipper Zero:** **3-6 metri**

L'asimmetria è enorme: il Flipper riceve molto meglio di quanto trasmetta. Questo è un dato operativo critico.

---

## Angolo di Emissione e Posizionamento

L'angolo di emissione del TSAL6200 è stretto: circa **+-17 gradi** dal centro (half-angle al 50% della potenza). Nella pratica questo significa:

- Devi **puntare ragionevolmente** il Flipper verso il ricevitore target
- Non è necessaria una precisione millimetrica - i rimbalzi su pareti bianche e soffitti aiutano
- In una stanza normale, puoi spesso controllare un dispositivo anche puntando verso il soffitto (rimbalzo)
- All'aperto o in grandi ambienti, devi puntare direttamente al ricevitore

---

## Limiti Reali che Devi Conoscere

**Singolo LED:** Un solo LED trasmettitore limita sia la portata che l'angolo rispetto ai telecomandi commerciali. Non c'è modo hardware di migliorare questo aspetto senza modifiche.

**Nessun LED esterno nativo:** A differenza del modulo Sub-GHz (che supporta moduli CC1101 esterni via GPIO), il modulo IR non ha un supporto nativo per LED esterni. Esistono mod hardware, ma non sono ufficiali.

**Frequenza portante fissa per protocolli noti:** Quando il Flipper trasmette un protocollo decodificato (NEC, RC5, ecc.), usa la frequenza portante standard del protocollo. Non c'è modo di forzare una frequenza diversa senza usare il modo RAW.

**Luce ambientale - il nemico principale:** La luce solare contiene una forte componente IR a 940 nm. In condizioni di luce solare diretta, la portata TX del Flipper può scendere a meno di 1 metro. Operare in ambienti interni o di sera aumenta drasticamente l'affidabilità.

**Line-of-sight obbligatorio:** L'IR non attraversa muri, porte, mobili opachi. Richiede sempre un percorso ottico, anche se indiretto (rimbalzo). Questo è un vincolo operativo fondamentale nel pentest.

---

## Tabella Riepilogativa Limiti Strutturali

| Limite | Dettaglio | Workaround |
|---|---|---|
| **Portata TX** | 3-8 metri | Avvicinarsi al target |
| **Angolo di emissione** | ~34 gradi | Puntare direttamente |
| **Singolo LED** | Nessuna ridondanza | Nessuno (limite hardware) |
| **Frequenza portante** | Ottimizzato per 38 kHz | RAW per frequenze diverse |
| **Luce ambientale** | Riduce portata | Operare in interni/ombra |
| **Nessun LED esterno nativo** | Non espandibile via GPIO | Mod hardware non ufficiali |
| **Protocolli AC** | Cattura complessa | Telecomandi dedicati per marca |
| **Line-of-sight** | Richiede percorso ottico | Usare rimbalzi su pareti |

> **Nota personale:** La portata limitata in TX è il fattore che condiziona tutto il lavoro operativo IR. In un engagement, se devi spegnere un display in una sala riunioni, devi entrare nella stanza e avvicinarti a 3-5 metri dal display. Non puoi farlo dal corridoio attraverso una porta chiusa. Pianifica sempre l'accesso fisico prima dell'azione IR. Detto questo, i rimbalzi in stanze con pareti chiare sono sorprendentemente efficaci - ho spento TV da angolazioni che non avrei ritenuto possibili, puntando verso il soffitto.

---

*Torna all'[indice principale](README.md)*
