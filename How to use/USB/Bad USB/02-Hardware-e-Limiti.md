## Hardware e Limiti Reali

### Specifiche USB del Flipper

- **USB-C 2.0** con supporto HID, CDC, Mass Storage
- **VID/PID default:** personalizzabile nel firmware (utile per evasione)
- **Velocità di digitazione:** configurabile, default ~100-150 caratteri/secondo
- **Layout tastiera:** supporta US, UK, DE, FR, IT, ES e molti altri
- **Supporto mouse:** il Flipper può anche emulare un mouse USB HID

### Limiti Reali

**Layout tastiera:** il payload deve corrispondere al layout della tastiera del sistema target. Uno script scritto per layout US non funzionerà su un PC con layout IT (i caratteri speciali sono in posizioni diverse). Il Flipper supporta la selezione del layout nel menu BadUSB.

**Velocità vs affidabilità:** digitare troppo velocemente può causare caratteri persi o fuori ordine, specialmente su macchine lente o virtualizzate. Aggiungere delay tra i comandi è essenziale.

**Schermo bloccato:** su un PC con lock screen attivo, il BadUSB può digitare la password SE la conosci, ma non può bypassare l'autenticazione.

**USB lock/whitelist:** alcuni ambienti enterprise bloccano dispositivi USB sconosciuti (USB device control, endpoint protection). Il Flipper viene bloccato se il VID/PID non è nella whitelist.

**Antivirus moderni:** mentre l'input HID stesso non viene bloccato, i comandi eseguiti (es. powershell -enc ...) possono essere intercettati dall'EDR. Serve evasione specifica per ogni target.

> **Nota personale:** Il layout tastiera è il problema più comune. In Italia, il 90% dei PC ha layout italiano (IT) che ha @ su AltGr+Q, [ su AltGr+E, ecc. Se il payload è scritto per layout US, tutti i caratteri speciali saranno sbagliati. Testo SEMPRE il payload sul mio PC con lo stesso layout del target prima dell'engagement.

---

