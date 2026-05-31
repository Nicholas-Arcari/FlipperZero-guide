## 11. Esperienza Personale -- Lezioni dal Campo

Questa sezione raccoglie le lezioni apprese durante anni di attività con il modulo NRF24 sul Flipper Zero.

> Nota personale: il NRF24L01+ è stato il primo modulo GPIO che ho collegato al Flipper Zero, e rimane quello che uso più spesso. Costa meno di 2 euro nella versione base, meno di 5 nella versione PA+LNA, e apre un mondo di possibilità per il pentest wireless. È il miglior rapporto costo/impatto che conosca nel campo della sicurezza.

> Nota personale: l'errore più comune che vedo nei principianti è sottovalutare l'alimentazione. Il NRF24L01+ è sensibilissimo alla qualità dell'alimentazione. Senza condensatore, il modulo funziona "quasi" sempre -- ma quel "quasi" vi farà perdere ore a cercare bug nel software quando il problema è hardware. Saldateci un condensatore e non pensateci piu'.

> Nota personale: per il MouseJacker, la preparazione dei payload è tutto. Un payload ben scritto funziona al primo colpo. Un payload mal scritto fallisce in modo imprevedibile. Testate SEMPRE i vostri payload su un vostro PC prima di usarli durante un audit. Ho visto payload che funzionavano perfettamente su Windows 10 e fallivano su Windows 11 a causa di cambiamenti nel comportamento del menu Start. Testate sulla stessa versione del SO del target.

> Nota personale: la portata è il fattore che cambia tutto. Con la versione base da 1.50 euro, dovete essere nella stessa stanza del target. Con la PA+LNA da 5 euro, potete operare dal corridoio, dalla sala riunioni adiacente, o dal piano di sopra. Con un'antenna direzionale, dal parcheggio. Investite nella versione PA+LNA -- è la scelta che fa la differenza tra "proof of concept in laboratorio" e "attacco realistico in campo".

> Nota personale: durante un audit in un grande open space, ho usato lo Scanner per mappare tutti i dispositivi wireless. Il risultato era una mappa con 47 mouse e 12 tastiere wireless. Il 68% era vulnerabile a MouseJacker. Quando ho presentato il dato al CISO, la risposta è stata: "non sapevamo nemmeno di avere cosi' tanti dispositivi wireless". Il primo passo della remediation è sempre sapere cosa si ha. Il NRF24 Scanner è lo strumento perfetto per questo inventario.

> Nota personale: una cosa che non viene mai detta abbastanza: il MouseJacker funziona anche attraverso i muri. Le onde a 2.4 GHz penetrano facilmente le pareti degli uffici (cartongesso, vetro, legno). Solo il cemento armato spesso e il metallo le bloccano significativamente. Questo significa che un attaccante nel corridoio, nell'ufficio accanto, o persino al piano di sopra può potenzialmente raggiungere il vostro mouse wireless. La "sicurezza fisica" di una stanza chiusa non protegge dalle onde radio.

> Nota personale: il mio setup preferito per il field work è Flipper Zero + NRF24L01+ PA+LNA con antenna dipolo 5 dBi, tutto in una tasca della giacca. È completamente invisibile e la portata è più che sufficiente per qualsiasi scenario indoor. Per operazioni a lunga distanza ho un'antenna Yagi da 8 dBi in uno zaino, ma la uso raramente -- la dipolo è quasi sempre sufficiente.

---

## 12. Riepilogo e Raccomandazioni

### Per il pentester:

1. Investire nella versione PA+LNA con condensatore da 47 uF -- è il setup minimo serio
2. Avere sempre payload testati e pronti per Windows, macOS e Linux
3. Fare Channel Scan come primo passo, sempre
4. Documentare ogni dispositivo trovato con indirizzo, canale, tipo e vulnerabilità
5. Non sottovalutare gli aspetti legali: autorizzazione scritta specifica per attività RF

### Per il difensore:

1. Inventariare tutte le periferiche wireless nell'organizzazione
2. Aggiornare i firmware dei dongle Logitech Unifying
3. Sostituire le periferiche non aggiornabili con modelli Bluetooth o cablati
4. Per postazioni critiche (C-suite, finance, IT admin): solo periferiche cablate
5. Implementare policy aziendali sull'uso di periferiche wireless
6. Includere il test delle periferiche wireless negli audit di sicurezza periodici

### Per il ricercatore:

1. Il NRF24L01+ è la piattaforma ideale per studiare i protocolli wireless a 2.4 GHz
2. Lo sniffer combinato con l'analisi dei payload permette reverse engineering completo
3. La documentazione Nordic Semiconductor (datasheet, application notes) è eccellente
4. La comunità open source attorno al NRF24 è molto attiva e collaborativa
5. Ogni dispositivo wireless economico è un potenziale target di ricerca
