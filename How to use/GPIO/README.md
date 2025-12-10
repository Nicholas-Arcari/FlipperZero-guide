# FlipperZero Guide – GPIO Module

La cartella GPIO raccoglie tutte le applicazioni, estensioni e strumenti che utilizzano i pin GPIO del Flipper Zero per interfacciarsi con hardware esterno, moduli aggiuntivi e sensori.

Questo README fornisce una panoramica completa su:

* Che cos'è il GPIO del Flipper Zero
* Struttura delle cartelle
* Funzione generale di ogni categoria
* Spiegazione specifica di ogni singolo componente

---

## Cos’è il GPIO del Flipper Zero?

I GPIO (General Purpose Input/Output) del Flipper Zero sono pin multifunzione che permettono al dispositivo di comunicare con componenti elettronici esterni, sensori, attuatori, moduli radio e microcontrollori. 

Grazie al GPIO, il Flipper può:

* Leggere segnali digitali e analogici
* Controllare periferiche esterne
* Comunicare via UART, I2C, SPI, SWD
* Programmare microcontrollori
* Usare moduli WiFi/BLE come esp32/esp8266

Il GPIO offre quindi la massima espandibilità al dispositivo.