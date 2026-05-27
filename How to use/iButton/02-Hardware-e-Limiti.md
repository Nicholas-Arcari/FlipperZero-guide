## Hardware e Limiti Reali

### Il Pad iButton del Flipper Zero

Il Flipper Zero integra un **pad iButton** nella parte posteriore (dorso) del dispositivo. Si tratta di due contatti metallici concentrici:

- **Contatto esterno (anello):** GND
- **Contatto interno (centro):** Data (DQ)

Questa disposizione replica la geometria del connettore standard iButton - un contatto centrale (data) circondato da un anello di massa. Quando appoggi il dorso del Flipper su una chiave iButton o su un lettore, i due contatti fanno ponte.

**Posizionamento fisico:**

Il pad si trova nella parte bassa del dorso del Flipper, sotto la clip per aggancio a cintura. Per un contatto ottimale:

1. Capovolgi il Flipper (schermo verso il basso)
2. Il pad iButton è il cerchio metallico visibile sul retro
3. Per LEGGERE una chiave: appoggia la pastiglia iButton centrata sul pad
4. Per EMULARE su un lettore: appoggia il dorso del Flipper sul lettore, centrando il pad metallico del Flipper sulla sonda del lettore

**Il contatto fisico è tutto:**

A differenza di NFC (qualche centimetro), Sub-GHz (centinaia di metri) o RFID 125kHz (qualche centimetro), iButton ha portata **zero**. Serve contatto fisico diretto metallo-su-metallo. Questo è sia un vantaggio di sicurezza (non puoi leggere da lontano) sia il limite operativo principale (devi avere accesso fisico alla chiave).

### Alimentazione e Circuito Interno

Il Flipper genera il segnale 1-Wire dal suo GPIO, con pull-up interno e capacità di pilotare il bus sia come master (lettura) che come slave (emulazione). Il firmware gestisce i timing slot via interrupt ad alta priorità, garantendo la precisione dei microsecondi necessaria.

In modalità lettura:
- Il Flipper alimenta la chiave iButton tramite il pin DQ (alimentazione parassita)
- Invia il comando Read ROM
- Riceve i 64 bit del ROM code
- Calcola e verifica il CRC-8

In modalità emulazione:
- Il Flipper si comporta come uno slave 1-Wire
- Attende il reset pulse dal lettore
- Risponde con il presence pulse
- Quando riceve Read ROM, trasmette i 64 bit del ROM code salvato
- Il lettore verifica il ROM code nel suo database

In modalità scrittura (per tag RW1990):
- Il Flipper invia comandi specifici per sbloccare la scrittura
- Programma il nuovo ROM code byte per byte
- Verifica la scrittura con un Read ROM di conferma

### Portata e Vincoli Operativi

**Portata di lettura:** 0 cm (contatto diretto). La chiave iButton deve toccare fisicamente il pad del Flipper. Non esiste lettura "a distanza" - anche 1 mm di aria può impedire il contatto elettrico.

**Qualità del contatto:** La superficie metallica deve essere pulita. Ossidazione, sporcizia, residui di colla o vernice sulla chiave o sul pad del Flipper degradano o impediscono il contatto. Un panno con alcool isopropilico risolve il 90% dei problemi di lettura.

**Orientamento:** La chiave iButton è simmetrica (circolare), quindi l'orientamento non conta. Ma il pad del Flipper deve essere centrato sulla chiave - contatti decentrati causano letture intermittenti.

**Pressione:** Serve una pressione moderata e costante. Non basta sfiorare - devi premere la chiave sul pad (o il Flipper sul lettore) con decisione, mantenendo il contatto per tutta la durata dell'operazione (1-3 secondi per la lettura, variabile per l'emulazione).

**Multi-protocollo:** Il Flipper supporta tre famiglie di protocollo sullo stesso pad iButton:
- **Dallas (1-Wire)** - DS1990A, RW1990, TM1990
- **Cyfral** - protocollo proprietario russo
- **Metakom** - protocollo proprietario russo

Il firmware rileva automaticamente il protocollo durante la lettura - non devi selezionare manualmente il tipo.

> **Nota personale:** Il posizionamento è la cosa che crea più problemi ai principianti. Ho visto persone tentare di leggere una chiave appoggiandola sullo schermo o sul lato del Flipper. Il pad è sul DORSO, in basso. Per l'emulazione su un lettore da citofono, il trucco è capovolgere il Flipper e appoggiare il dorso direttamente sulla sonda metallica del lettore. Se il lettore ha una sonda a "pulsante" rientrata, devi premere con decisione per fare contatto. Se hai problemi, pulisci entrambe le superfici.

---

