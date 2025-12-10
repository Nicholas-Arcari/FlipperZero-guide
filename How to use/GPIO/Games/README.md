# GAMES

Mini-giochi che sfruttano interfacce esterne, sensori o protocolli hardware per creare esperienze interattive basate su periferiche reali.

Oltre all’aspetto ludico, questi giochi rappresentano ottimi esempi di utilizzo pratico di UART, sensori e input esterni.

### **• UART Pong**

Versione hardware di Pong controllata tramite comunicazione UART, che permette di collegare dispositivi esterni come joystick, rotary encoder, tastiere o perfino microcontrollori dedicati.

Funzionalità ampliate:

- Comunicazione seriale stabile a 9600/115200 baud (a seconda della configurazione).
- Rilevamento input real-time inviati via UART (comandi UP/DOWN).
- Possibilità di personalizzare velocità della pallina, dimensione delle paddle e difficoltà.
- Modalità “AI Mode” dove il Flipper controlla un lato e l’utente l’altro.
- Supporto per controller artigianali basati su ESP8266/Arduino.

Esempi pratici:

- Collegare un joystick analogico a un microcontrollore → inviare valori via UART al Flipper per controllare la paddle.
- Test di comunicazione seriale tra Flipper e un progetto personale.
- Creazione di un controller fisico dedicato stampato in 3D.

### **• VL6180X Pong**

Variante di Pong che utilizza il sensore di distanza VL6180X (Time-of-Flight) come input per il movimento della paddle.

Più ci si avvicina o allontana dal sensore, più la racchetta si sposta.

Funzionalità ampliate:

- Lettura distanza tramite I2C con refresh rapido.
- Mappatura dinamica dei valori misurati → posizione paddle.
- Calibrazione automatica per ambienti con luce variabile o superfici non uniformi.
- Modalità “Precision Mode” per sensori configurati a 1 mm di risoluzione.
- Adattamento della difficoltà in base alla stabilità del segnale TOF.

Esempi pratici:

- Montare il VL6180X su una piccola basetta → muovere la mano sopra il sensore per controllare il gioco.
- Utilizzare il gioco per testare il corretto funzionamento del modulo ToF.
- Dimostrazione didattica del funzionamento dei sensori di distanza.