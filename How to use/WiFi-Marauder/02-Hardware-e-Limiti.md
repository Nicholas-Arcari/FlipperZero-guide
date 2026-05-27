## 2. Hardware - ESP32 WiFi Devboard

### 2.1 Premessa Fondamentale

**Il Flipper Zero NON ha WiFi integrato.**

Questo e il primo concetto che deve essere assolutamente chiaro. Il Flipper Zero e
un dispositivo multi-tool che include:
- Sub-GHz transceiver (CC1101)
- NFC (ST25R3916)
- RFID 125 kHz
- Infrarosso
- GPIO
- Bluetooth (per comunicazione con app mobile)
- USB

Ma NON include alcun chip WiFi. Tutto cio che riguarda WiFi -- scansione, sniffing,
attacchi, analisi -- viene eseguito da un modulo esterno ESP32 collegato via GPIO.

Il Flipper funge da terminale / interfaccia di controllo, inviando comandi via UART
seriale al modulo ESP32 che esegue il firmware Marauder.

### 2.2 ESP32-S2 WiFi Devboard (Ufficiale Flipper)

La scheda ufficiale di Flipper Devices e basata sul chip ESP32-S2 di Espressif:

**Specifiche tecniche ESP32-S2:**
- Processore: Xtensa LX7 single-core a 240 MHz
- RAM: 320 KB SRAM + 16 KB RTC SRAM
- Flash: 4 MB (dipende dal modulo)
- WiFi: 802.11 b/g/n a 2.4 GHz
- Interfaccia USB: USB-OTG nativo (non richiede bridge UART esterno)
- GPIO: fino a 43 pin programmabili
- ADC: 2x SAR ADC a 13 bit

**Connessione al Flipper:**
- Si collega tramite il connettore GPIO sulla parte superiore del Flipper
- Alimentazione: 3.3V forniti dal Flipper tramite GPIO
- Comunicazione: UART seriale (TX/RX) tramite pin dedicati
- Il devboard ha anche un connettore USB-C proprio, usato per il flashing

**Limitazioni dell'ESP32-S2:**
- Solo 2.4 GHz (non supporta 5 GHz -- nessuna analisi di reti 802.11a/ac/ax su 5 GHz)
- Single-core: prestazioni limitate in operazioni intensive
- Antenna integrata: raggio limitato, tipicamente 20-50 metri in condizioni ottimali
- Non supporta monitor mode nativo come le schede WiFi per PC (Atheros, Ralink)
  ma il firmware Marauder implementa il raw frame injection/capture via API Espressif

### 2.3 ESP32-S3 e Altre Varianti

Alcune board alternative supportate dal firmware Marauder:

**ESP32-S3:**
- Processore: Xtensa LX7 dual-core a 240 MHz (piu potente dell'S2)
- WiFi + Bluetooth 5 (LE)
- Piu RAM disponibile
- Migliori prestazioni nella cattura di pacchetti ad alta velocita

**ESP32-WROOM-32:**
- Il classico ESP32 originale (dual-core Xtensa LX6)
- Molto diffuso, ampio supporto community
- Puo essere usato con Marauder ma richiede collegamento manuale dei pin UART

**Nota sulle antenne:**
Per migliorare il raggio, alcune board hanno un connettore U.FL/IPEX per antenna
esterna. In ambiente di pentesting, un'antenna direzionale da 5-9 dBi puo fare
la differenza tra catturare e perdere un handshake da un target distante.

> Nota personale: la devboard ufficiale Flipper con ESP32-S2 funziona bene per
> lavori a corto raggio (stessa stanza / piano). Per engagement professionali dove
> devo operare da distanze maggiori, preferisco usare un laptop con scheda Alfa
> AWUS036ACH e aircrack-ng/bettercap. Il Flipper con Marauder e eccellente per
> ricognizione rapida e discreta -- entra in tasca ed e operativo in 5 secondi.

### 2.4 Driver Necessari

A seconda del sistema operativo e del chip USB-UART sulla board:

**Windows:**
- ESP32-S2 (devboard ufficiale): usa USB-OTG nativo, di solito non serve driver
  aggiuntivo. Se non riconosciuto, installare il driver ESP32-S2 da Espressif.
- ESP32 con chip CP2102/CP2104: scaricare il driver Silicon Labs CP210x
  (https://www.silabs.com/developers/usb-to-uart-bridge-vcp-drivers)
- ESP32 con chip CH340/CH341: scaricare il driver WCH CH340
  (http://www.wch.cn/download/CH341SER_EXE.html)

**Linux:**
- Kernel 5.x+: driver cp210x e ch341 gia inclusi nel kernel
- Verifica con: `dmesg | grep -i ttyUSB` o `dmesg | grep -i ttyACM`
- Potrebbe servire aggiungere l'utente al gruppo dialout:
  `sudo usermod -aG dialout $USER` (logout/login per applicare)

**macOS:**
- CP2102/CP2104: installare il driver Silicon Labs
- CH340: installare il driver CH340, disponibile su brew:
  `brew install --cask wch-ch34x-usb-serial-driver`
- Nota: su macOS Ventura+ potrebbero servire permessi aggiuntivi in
  System Preferences > Privacy & Security

---

## 3. Flash del Firmware Marauder

### 3.1 Prerequisiti

Prima di flashare:
1. Identificare ESATTAMENTE il modello del proprio ESP32 (S2, S3, WROOM-32, ecc.)
2. Scaricare il firmware corretto per quel modello -- firmware sbagliato = brick
   (recuperabile, ma fastidioso)
3. Avere un cavo USB-C funzionante (non solo di ricarica -- deve supportare dati)

Repository di riferimento:
- Firmware Marauder: https://github.com/justcallmekoko/ESP32Marauder
- Flasher per Windows: https://github.com/UberGuidoZ/Flipper/tree/main/Wifi_DevBoard/FZ_Marauder_Flasher
- Flasher per Linux/macOS: https://github.com/SkeletonMan03/FZEasyMarauderFlash

### 3.2 Metodo 1: Flash via Web Browser (Raccomandato per principianti)

Questo e il metodo piu semplice e utilizza l'ESP Web Flasher direttamente dal browser.
Richiede un browser basato su Chromium (Chrome, Edge, Brave) per il supporto Web Serial API.

**Procedura dettagliata:**

1. Scollegare il devboard dal Flipper (flashare sempre con il devboard disconnesso
   dal Flipper)

2. Collegare il devboard al PC via USB-C

3. Mettere il chip in modalita boot:
   - ESP32-S2 devboard ufficiale: tenere premuto il pulsante BOOT, premere e
     rilasciare RESET, poi rilasciare BOOT
   - Se non ci sono pulsanti fisici: collegare GPIO0 a GND durante il power-on

4. Verificare che il dispositivo sia riconosciuto:
   - Windows: Device Manager -> Porte COM (dovrebbe apparire una nuova porta)
   - Linux: `ls /dev/ttyACM*` o `ls /dev/ttyUSB*`
   - macOS: `ls /dev/cu.usbmodem*`

5. Aprire il FZEE Flasher o lo strumento web equivalente nel browser

6. Selezionare la board corretta (es. "ESP32-S2" per la devboard ufficiale)

7. Selezionare la versione del firmware Marauder (usare l'ultima stabile)

8. Cliccare "Connect" -> selezionare la porta seriale del dispositivo

9. Cliccare "Program" e attendere il completamento

10. Al termine: premere RESET sul devboard (o scollegare/ricollegare USB)

11. Ricollegare il devboard al Flipper e verificare il funzionamento

**Vantaggi:**
- Non richiede installazione di software
- Interfaccia grafica intuitiva
- Seleziona automaticamente gli offset di flash corretti

**Svantaggi:**
- Richiede browser Chromium (Firefox non supporta Web Serial)
- Dipende dal servizio web esterno
- Meno controllo sui parametri di flash

### 3.3 Metodo 2: Flash via ESP Web Flasher Manuale

Questo metodo offre piu controllo e richiede il download dei file binari individuali.

**Procedura:**

1. Scaricare i file binari dalla release page di Marauder su GitHub:
   - `bootloader.bin` -- bootloader di secondo stadio
   - `partitions.bin` -- tabella delle partizioni
   - `boot_app0.bin` -- OTA boot selector
   - `esp32marauder_vX.X.X_BOARD.bin` -- firmware principale (BOARD = il tuo modello)

2. Aprire https://espressif.github.io/esptool-js/ nel browser

3. Configurare gli offset di flash:

   Per ESP32-S2:
   ```
   0x1000   -> bootloader.bin
   0x8000   -> partitions.bin
   0xe000   -> boot_app0.bin
   0x10000  -> esp32marauder_vX.X.X_flipper.bin
   ```

   Per ESP32 (WROOM-32):
   ```
   0x1000   -> bootloader.bin
   0x8000   -> partitions.bin
   0xe000   -> boot_app0.bin
   0x10000  -> esp32marauder_vX.X.X_esp32.bin
   ```

4. Baud rate consigliato: 921600 (piu veloce) o 115200 (piu affidabile)

5. Flash mode: DIO (per la maggior parte delle board)

6. Cliccare "Program" per ogni slot nell'ordine indicato, oppure "Program All"

7. Reset del dispositivo al termine

> Nota personale: questo metodo mi ha salvato piu volte quando il flasher automatico
> dava errori inspiegabili. Avere il controllo diretto sugli offset e i file binari
> permette di diagnosticare problemi come partizioni corrotte o bootloader incompatibili.
> Lo consiglio a chi vuole capire davvero cosa succede durante il flash.

### 3.4 Metodo 3: Flash via esptool.py (Metodo avanzato / riga di comando)

Per chi preferisce il terminale e il controllo totale. Questo e il metodo che uso
regolarmente.

**Installazione di esptool:**

```bash
pip install esptool
```

Oppure su sistemi con Python 3:

```bash
pip3 install esptool
```

**Identificazione della porta seriale:**

```bash
# Linux
ls -la /dev/ttyACM* /dev/ttyUSB*

# macOS
ls /dev/cu.usbmodem* /dev/cu.SLAB*

# Windows (PowerShell)
Get-WMIObject Win32_SerialPort | Select-Object DeviceID, Description
```

**Cancellazione della flash (consigliata prima del primo flash):**

```bash
esptool.py --chip esp32s2 --port /dev/ttyACM0 erase_flash
```

**Flash completo (ESP32-S2):**

```bash
esptool.py --chip esp32s2 \
    --port /dev/ttyACM0 \
    --baud 921600 \
    --before default_reset \
    --after hard_reset \
    write_flash \
    -z \
    --flash_mode dio \
    --flash_freq 80m \
    --flash_size 4MB \
    0x1000 bootloader.bin \
    0x8000 partitions.bin \
    0xe000 boot_app0.bin \
    0x10000 esp32marauder_vX.X.X_flipper.bin
```

**Flash completo (ESP32 WROOM-32):**

```bash
esptool.py --chip esp32 \
    --port /dev/ttyUSB0 \
    --baud 921600 \
    write_flash \
    -z \
    --flash_mode dio \
    --flash_freq 40m \
    --flash_size 4MB \
    0x1000 bootloader.bin \
    0x8000 partitions.bin \
    0xe000 boot_app0.bin \
    0x10000 esp32marauder_vX.X.X_esp32.bin
```

**Verifica del flash:**

```bash
esptool.py --chip esp32s2 --port /dev/ttyACM0 verify_flash \
    0x10000 esp32marauder_vX.X.X_flipper.bin
```

**Lettura delle informazioni del chip:**

```bash
esptool.py --chip esp32s2 --port /dev/ttyACM0 chip_id
esptool.py --chip esp32s2 --port /dev/ttyACM0 flash_id
```

**Problemi comuni con esptool:**

| Problema | Soluzione |
|----------|-----------|
| "Failed to connect" | Mettere in boot mode (BOOT + RESET), verificare cavo USB |
| "Invalid head of packet" | Ridurre baud rate a 115200 |
| "Permission denied" su Linux | `sudo chmod 666 /dev/ttyACM0` o aggiungere utente a dialout |
| "A fatal error occurred" | Verificare chip corretto (esp32 vs esp32s2 vs esp32s3) |
| Flash completa ma non funziona | Verificare offset corretti per il proprio chip |
| Timeout durante write | Cavo USB difettoso o troppo lungo, provare un altro cavo |

> Nota personale: uso sempre esptool da terminale. E il metodo piu affidabile e
> ripetibile. Ho uno script bash che automatizza l'intero processo: scarica l'ultimo
> firmware da GitHub, cancella la flash, e programma tutto con un singolo comando.
> In ambiente di pentesting, dove potresti dover riflashare rapidamente sul campo,
> avere lo script pronto e fondamentale.

---

## 4. Configurazione del Flipper Zero

### 4.1 Collegamento del Devboard

1. **Spegnere il Flipper Zero** prima di collegare il devboard (buona pratica per
   evitare danni ai pin GPIO)

2. Allineare i pin del devboard con il connettore GPIO sulla parte superiore del
   Flipper. Il devboard ufficiale ha un connettore che si inserisce in modo univoco.

3. Premere con fermezza ma senza forzare. Il devboard deve essere ben saldo.

4. Accendere il Flipper Zero.

5. Verificare che il devboard sia alimentato (LED di stato, se presente).

### 4.2 Accesso all'App WiFi Marauder

Il percorso varia in base al firmware installato sul Flipper:

**Firmware ufficiale con app pack:**
```
Apps -> GPIO -> [ESP32] WiFi Marauder
```

**Firmware Momentum (ex Xtreme):**
```
Apps -> GPIO -> [ESP32] WiFi Marauder
```

**Firmware Unleashed:**
```
Apps -> GPIO -> [ESP32] WiFi Marauder
```

La maggior parte dei firmware custom includono gia l'app Marauder preinstallata.
Se non presente, puo essere installata come app .fap dalla SD card.

### 4.3 Comunicazione Flipper-ESP32

Il Flipper comunica con l'ESP32 tramite UART seriale:
- Baud rate: 115200 (default di Marauder)
- Pin TX del Flipper -> Pin RX dell'ESP32
- Pin RX del Flipper -> Pin TX dell'ESP32
- GND condiviso
- 3.3V fornito dal Flipper

L'app sul Flipper e essenzialmente un terminale seriale che:
1. Invia comandi testuali al firmware Marauder
2. Riceve e formatta l'output
3. Fornisce un menu grafico per i comandi piu comuni
4. Salva i risultati sulla SD card del Flipper

I comandi Marauder sono stringhe di testo inviate via seriale. Ad esempio:
- `scanap` -- avvia scansione degli AP
- `scansta` -- avvia scansione delle stazioni (client)
- `sniffpmkid` -- avvia cattura PMKID
- `attack -t deauth` -- avvia attacco deauth
- `stopscan` -- ferma qualsiasi operazione in corso

### 4.4 Salvataggio dei Risultati

I dati catturati vengono salvati sulla SD card del Flipper in formati diversi:
- Scansioni: file di testo con lista AP/client
- Catture pacchetti: file .pcap (leggibili con Wireshark)
- PMKID: formato compatibile con hashcat
- Handshake: file .pcap contenente i frame EAPOL
- Wardriving: formato CSV compatibile con WiGLE

Il percorso tipico sulla SD e:
```
/ext/apps_data/marauder/
```

---

