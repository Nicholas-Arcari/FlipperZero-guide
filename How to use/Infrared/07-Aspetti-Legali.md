## Aspetti Legali

### Normativa Italiana

L'uso del modulo IR del Flipper Zero in Italia ricade in un contesto normativo meno definito rispetto alle trasmissioni radio (Sub-GHz), ma non privo di implicazioni legali.

### Cosa NON È Illegale

- **Catturare segnali IR** dai propri telecomandi (reverse engineering dei propri dispositivi)
- **Utilizzare il Flipper come telecomando** per i propri dispositivi
- **Analizzare e studiare** protocolli IR a scopo educativo e di ricerca
- **Catturare segnali IR ambientali** - l'IR non è una comunicazione "riservata" (non esiste l'equivalente dell'intercettazione di comunicazioni radio)
- **Possedere** il Flipper Zero e il suo modulo IR

### Cosa Può Essere Illegale

**Interferenza con dispositivi altrui:**

L'uso del modulo IR per controllare o interferire con dispositivi di proprietà altrui senza autorizzazione può configurare diverse fattispecie:

- **Art. 615-ter Codice Penale (Accesso abusivo a sistema informatico/telematico):** Se il dispositivo controllato via IR è collegato a un sistema informatico (es. display di digital signage collegato a un media player in rete), l'accesso non autorizzato tramite IR potrebbe essere contestato come accesso al sistema. L'interpretazione è estensiva e non ancora consolidata in giurisprudenza per attacchi IR
- **Art. 635 Codice Penale (Danneggiamento):** Spegnere un display o un sistema in uso può configurare danneggiamento (rendere inservibile un bene altrui, anche temporaneamente)
- **Art. 340 Codice Penale (Interruzione di pubblico servizio):** Se il dispositivo è parte di un servizio pubblico (display informativo in stazione, aeroporto, ospedale), l'interferenza può avere conseguenze penali serie
- **Art. 674 Codice Penale (Disturbo delle occupazioni o del riposo):** Fattispecie minore ma applicabile in contesti come cinema, sale d'attesa, ambienti condivisi

### Nel Contesto del Penetration Testing

Un penetration test autorizzato richiede:

- **Contratto scritto** che specifichi esplicitamente lo scope dell'engagement
- **Inclusione esplicita** dei test su dispositivi IR/controllo ambientale nel perimetro di test
- **Autorizzazione del proprietario** dell'edificio/dispositivi (non solo del committente, se diverso)
- **Regole di ingaggio (ROE)** che definiscano cosa è permesso fare
- **Get-out-of-jail letter** per tutelarsi in caso di intervento delle forze dell'ordine

> **Nota personale:** A differenza del Sub-GHz dove la normativa sulle emissioni radio è chiara e codificata, l'IR si muove in una zona grigia legale. Il mio consiglio: tratta sempre l'IR come se fosse regolamentato. Includi i test IR esplicitamente nel contratto, documenta ogni azione e ottieni autorizzazione preventiva. L'assenza di una normativa specifica non è una protezione - un giudice può applicare norme generali per analogia.

---

