# FLIPBOARD

Addon modulare con pulsanti, LED e tracce integrate, pensato come una breadboard intelligente per prototipazione rapida.

Permette di collegare componenti elettronici al Flipper Zero in modo stabile, ordinato e immediato, fornendo sia funzioni I/O di base sia mini-app specializzate.

### **• Flipboard Blinky**

Applicazione per il controllo dei LED presenti sulla Flipboard, utile per testare alimentazione, pinout e funzioni I/O.

Funzionalità ampliate:

- Accensione, spegnimento e lampeggio dei LED integrati.
- Test rapidi dei pin GPIO associati ai LED.
- Possibilità di generare pattern di lampeggio personalizzati.
- Controllo dell’intensità (quando supportato) tramite PWM.

Esempi pratici:

- Verifica del corretto collegamento Flipper ↔ Flipboard.
- Debug rapido per capire se un pin sta funzionando.
- Creazione di indicatori visivi durante lo sviluppo di altri progetti.

### **• Flipboard Keyboard**

Trasforma Flipboard in una piccola tastiera digitale o macro-pad basato su combinazioni di pulsanti.

Funzionalità ampliate:

- Mappatura dei tasti della Flipboard in input digitali verso il Flipper.
- Possibilità di assegnare funzioni personalizzate ai pulsanti.
- Modalità "macro" per eseguire sequenze predefinite.
- Supporto per protocolli o input verso moduli esterni (I²C/SPI, quando integrato).

Esempi pratici:

- Controllo remoto di script.
- Attivazione rapida di funzioni del Flipper (es. invio di comandi UART).
- Utilizzo come controller minimale per testare UI o menu.

### **• Flipboard Signal**

Modulo dedicato al monitoraggio dei segnali elettrici sui pin della Flipboard, utile per debug o lettura rapida di stati logici.

Funzionalità ampliate:

- Lettura digitale on/off dei pin collegati.
- Analisi semplice del livello logico (HIGH/LOW).
- Visualizzazione in tempo reale tramite indicatori LED o display.
- Rilevazione di segnali in ingresso a bassa velocità.

Esempi pratici:

- Diagnostica di un sensore o pulsante esterno.
- Verifica della continuità di un circuito.
- Lettura dello stato di un relè o transistor.

### **• Flipboard Simon**

Replica del famoso gioco “Simon Says”, sfruttando LED e pulsanti della Flipboard per creare una sequenza da memorizzare.

Funzionalità ampliate:

- Sequenze di colore/luci con difficoltà crescente.
- Supporto al punteggio e alla cronologia delle partite.
- Modalità training con sequenze lente o ripetute.
- Possibilità di utilizzare suoni o vibrazioni (se presenti su moduli esterni).

Esempi pratici:

- Dimostrazione divertente delle capacità I/O della Flipboard.
- Esercitazione di reattività e memoria.
- Test funzionale completo di LED e pulsanti in un’unica app.