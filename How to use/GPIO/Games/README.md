# GAMES - Mini-Giochi Hardware

Mini-giochi che sfruttano interfacce GPIO esterne, sensori e protocolli hardware per creare esperienze interattive. Oltre all'aspetto ludico, rappresentano eccellenti esempi didattici di comunicazione UART, lettura sensori e gestione input real-time.

---

## UART Pong

Versione hardware del classico Pong controllata tramite comunicazione seriale UART.

### Come Funziona

Il gioco utilizza la UART del Flipper (pin PB6 TX, PB7 RX) per ricevere input da un controller esterno. Il controller (Arduino, ESP8266, joystick seriale) invia comandi UP/DOWN via seriale, e il Flipper muove la paddle di conseguenza.

**Parametri comunicazione:**
- Baud rate: 9600 o 115200 (configurabile)
- Formato: 8N1 (8 data bit, no parity, 1 stop bit)
- Comandi: caratteri ASCII ('ù = up, 'D' = down) o valori binari

**Configurazione:**
- Velocità pallina: regolabile
- Dimensione paddle: regolabile
- Modalità AI: il Flipper controlla un lato automaticamente

### Valore Didattico

UART Pong è il modo migliore per imparare la comunicazione seriale:
- Come configurare baud rate e formato
- Come leggere dati in real-time senza blocking
- Come sincronizzare input esterno con logica di gioco
- Come gestire il timing tra frame di gioco e lettura UART

**Esempio di controller Arduino:**
```
void setup() { Serial.begin(9600); }
void loop() {
  int val = analogRead(A0); // Joystick Y
  if (val > 600) Serial.write('U');
  else if (val < 400) Serial.write('D');
  delay(50);
}
```

> **Nota personale:** Ho usato UART Pong come demo durante un workshop di hardware hacking. Collegando un joystick a un Arduino e poi al Flipper via UART, i partecipanti capivano in 5 minuti come funziona la comunicazione seriale. Molto più efficace di spiegare la teoria.

---

## VL6180X Pong

Variante di Pong controllata dal sensore di distanza VL6180X (Time-of-Flight) - più ci si avvicina o allontana dal sensore, più la paddle si sposta.

### Come Funziona

Il VL6180X è un sensore ToF che misura la distanza tramite il tempo di volo di un impulso IR. Connesso via I2C (indirizzo 0x29), fornisce misure in millimetri con refresh rate elevato.

**Mappatura:** la distanza misurata (0-100mm) viene mappata linearmente sulla posizione della paddle sullo schermo.

**Configurazione:**
- Calibrazione automatica per luce variabile
- Modalità "Precision Mode": risoluzione 1mm
- Adattamento difficoltà basato sulla stabilità del segnale

### Valore Didattico

Dimostra l'uso pratico di:
- Bus I2C con polling ad alta frequenza
- Mappatura di valori analogici su azioni discrete
- Calibrazione automatica di sensori
- Gestione del rumore nei dati del sensore
