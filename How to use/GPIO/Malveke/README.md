# MALVEKE - Guida Operativa

Il modulo Malveke è un addon multi-funzione che estende il Flipper Zero con fotocamera, storage aggiuntivo, stampante termica, gestione pin avanzata e capacità di test/debug. Progettato per maker, analisti hardware e pentester che necessitano di documentazione visiva e strumenti di prototipazione sul campo.

---

## Hardware

Il Malveke si collega al Flipper tramite l'header GPIO e aggiunge:
- **Modulo fotocamera** (OV2640 o compatibile) per foto e streaming video
- **Slot microSD aggiuntivo** per storage esteso
- **Interfaccia stampante termica** ESC/POS per stampa sul campo
- **Pin test integrati** per diagnostica GPIO

---

## Tool per Tool

### Cartridge

Sistema di gestione firmware modulari per il Malveke.

**Funzionalità:**
- Caricamento e gestione di "cartucce" software (funzioni aggiuntive, firmware specializzati)
- Backup e ripristino del contenuto delle cartucce
- Verifica integrità con firma digitale
- Compatibilità con estensioni della community

**Procedura:**
1. Scarica la cartuccia desiderata (file .bin dalla community)
2. Copia sulla SD card del Flipper in `/ext/apps_data/malveke/`
3. Apri Cartridge → seleziona la cartuccia
4. Installa e verifica integrità

### Emulator

Modulo di emulazione per firmware e funzionalità hardware.

**Funzionalità:**
- Emulazione di moduli hardware esterni (sensori I2C, GPIO)
- Modalità sandbox per test sicuri senza hardware fisico
- Debug tramite log di stato interno
- Simulazione segnali digitali/analogici

**Uso nel pentest:** testare script e automazioni prima di eseguirle su hardware reale. Permette di validare che il firmware interagirà correttamente con il target.

### Link-Camera / Live Camera

Streaming video dal modulo fotocamera del Malveke.

**Link-Camera:**
- Streaming MJPEG continuo
- Regolazione risoluzione (QVGA, VGA, SVGA)
- Controllo esposizione, bilanciamento bianco, luminosità
- Modalità "Low Latency" per uso real-time

**Live Camera:**
- Anteprima live senza buffer per risposta immediata
- Modalità macro per ispezioni ravvicinate
- Cattura rapida fotogrammi su SD

**Uso nel pentest/hardware hacking:**
- Documentazione visiva durante analisi PCB
- Ispezione saldature e componenti miniaturizzati
- Mini-endoscopio digitale per ispezionare slot, connettori
- Registrazione video delle procedure per il report

> **Nota personale:** La camera del Malveke è utilissima durante l'analisi hardware. Quando devo documentare i pad UART/SWD su un PCB per il report, scatto foto direttamente dal Flipper senza dover tirare fuori il telefono. Più discreto e con le foto già sulla SD card del Flipper.

### Photo

Fotografia statica con il modulo camera.

**Funzionalità:**
- Scatti JPEG compressi
- Regolazione ISO, esposizione, focus
- Gestione album con preview
- Esportazione via USB/UART/SD

### Pin Test

Strumento di diagnostica per i pin GPIO del Malveke e accessori collegati.

**Funzionalità:**
- Scanner pin digitali e analogici
- Rilevazione tensioni e stati logici (HIGH/LOW)
- Test continuity tra pin
- Script di test automatici per verifica cablaggi

**Uso:** debug rapido prima di collegare moduli esterni. Verifica che tutti i pin funzionino correttamente dopo un assemblaggio.

### Printer

Interfaccia per stampanti termiche ESC/POS.

**Funzionalità:**
- Stampa testo con font variabili
- QR code, barcode, immagini monocromatiche
- Configurazione densità e velocità
- Stampa log diagnostici da altri moduli

**Uso nel pentest:**
- Stampa rapida di note durante un engagement (senza usare il telefono)
- Etichette per componenti durante analisi hardware
- Stampa QR code per condividere URL/dati rapidamente
- Log cartaceo delle operazioni per documentazione

> **Nota personale:** La stampante termica collegata al Flipper è un gadget ma ha uso pratico: durante un hardware pentest su un impianto industriale, ho stampato le etichette con gli indirizzi I2C di ogni dispositivo trovato sul bus. Le ho attaccate direttamente sulle schede per tenere traccia. Più veloce che prendere appunti.
