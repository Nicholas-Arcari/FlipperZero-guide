# FLIPBOARD - Guida Operativa

Addon modulare con pulsanti fisici, LED RGB e tracce integrate, progettato come breadboard intelligente per prototipazione rapida e interazione I/O con il Flipper Zero.

---

## Hardware

La Flipboard si collega all'header GPIO del Flipper e fornisce:
- **4 pulsanti fisici** mappati su pin GPIO
- **4 LED RGB** controllabili via PWM
- **Tracce di collegamento** per componenti esterni
- **Area di prototipazione** per saldature rapide

---

## Tool

### Flipboard Blinky

Controllo diretto dei LED integrati.

**Funzionalità:**
- Accensione/spegnimento individuale dei 4 LED
- Pattern di lampeggio personalizzabili (frequenza, duty cycle)
- Controllo colore RGB tramite PWM sui tre canali
- Test rapido del pinout GPIO → LED

**Uso pratico:**
- Verifica del collegamento Flipper ↔ Flipboard
- Debug visivo: assegna un LED a un evento (es. LED rosso = errore, verde = successo)
- Indicatore di stato durante script GPIO automatizzati

### Flipboard Keyboard

Trasforma i pulsanti della Flipboard in un macro-pad programmabile.

**Funzionalità:**
- Mappatura di ogni pulsante su un'azione (invio UART, comando GPIO, toggle LED)
- Modalità "macro": sequenze predefinite per ogni tasto
- Supporto a combinazioni e sequenze multi-step

**Uso nel pentest:**
- Macro-pad per azioni frequenti durante un engagement
- Tasto 1: avvia scan WiFi, Tasto 2: cattura Sub-GHz, Tasto 3: toggle LED stato, Tasto 4: salva log
- Automazione rapida senza navigare i menu

### Flipboard Signal

Monitoraggio segnali elettrici sui pin della Flipboard.

**Funzionalità:**
- Lettura digitale HIGH/LOW in tempo reale
- Analisi livello logico con visualizzazione su display
- Rilevazione segnali in ingresso a bassa velocità
- Indicazione tramite LED del livello logico

**Uso:** diagnostica di sensori, pulsanti esterni, rele', transistor. Utile per verificare che un circuito funzioni prima di collegarlo al Flipper.

### Flipboard Simon

Gioco "Simon Says" con LED e pulsanti - sequenze di colori da memorizzare.

**Valore didattico:** dimostra l'uso completo di I/O GPIO (input da pulsanti + output su LED + logica di gioco). Ottimo esempio per capire come funzionano interrupt, debounce e timing su GPIO.

> **Nota personale:** La Flipboard è più un tool da maker che da pentester, ma l'ho usata come macro-pad durante engagement lunghi. Avere 4 pulsanti fisici mappati su azioni frequenti velocizza il lavoro quando passi ore a catturare segnali RF o testare badge NFC.
