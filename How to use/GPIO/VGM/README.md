# VGM (Video Game Module) - Guida Operativa

Addon gaming per il Flipper Zero che aggiunge un accelerometro/giroscopio per il controllo tramite movimento fisico del dispositivo. Permette di giocare a giochi basati su tilt, air mouse e controllo gestuale.

---

## Hardware

Il VGM si collega all'header GPIO e integra:
- **IMU (Inertial Measurement Unit):** accelerometro 3 assi + giroscopio 3 assi (tipicamente MPU6050, LSM6DS3 o BMI160)
- **Comunicazione:** I2C (indirizzo tipico 0x68 o 0x6A)
- **Data rate:** fino a 1 kHz per letture fluide
- **Sensibilità:** configurabile (±2g/±4g/±8g/±16g per accelerometro, ±250/±500/±1000/±2000°/s per giroscopio)

---

## Tool

### Air Arkanoid

Versione di Arkanoid controllata inclinando il Flipper. Il paddle si muove a destra/sinistra in base al tilt sull'asse X.

**Controlli:** inclina il Flipper a sinistra/destra per muovere il paddle. La sensibilità è calibrata per movimenti naturali del polso.

### Air Labyrinth

Labirinto controllato tramite inclinazione - la pallina si muove seguendo la gravità percepita dall'accelerometro.

**Controlli:** inclina il Flipper in tutte le direzioni per guidare la pallina attraverso il labirinto. Richiede movimenti precisi e stabili.

### VGM Air Mouse

Trasforma il Flipper in un mouse aereo: muovendo il dispositivo nello spazio, il cursore si sposta sullo schermo del PC collegato via USB HID.

**Funzionalità:**
- Tracking 3D con fusione accelerometro + giroscopio
- Calibrazione automatica al primo utilizzo
- Sensibilità regolabile
- Click tramite pulsanti del Flipper

**Uso pratico:** controllo presentazioni, navigazione PC da distanza, demo di controllo gestuale.

### VGM Game Remote

Telecomando gaming che usa il VGM come controller di movimento per giochi o applicazioni su PC.

### Video Game Module Tool

Suite di utility per configurazione, calibrazione e diagnostica del modulo VGM:
- Test accelerometro (valori raw su 3 assi)
- Test giroscopio (velocità angolare)
- Calibrazione offset
- Verifica comunicazione I2C

> **Nota personale:** Il VGM non ha uso diretto nel pentest, ma l'Air Mouse è sorprendentemente utile quando devi controllare un PC da qualche metro di distanza - ad esempio durante una presentazione di findings dove il PC è collegato al proiettore ma tu sei dall'altra parte della stanza.
