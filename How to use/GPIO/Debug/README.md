# DEBUG

Strumenti avanzati di diagnostica, test e programmazione.

### **• AVR Flasher**

Tool per la programmazione di microcontrollori AVR (Atmel/Microchip) tramite interfacce compatibili con il pinout GPIO del dispositivo.

Funzionalità ampliate:

- Supporto ai protocolli più comuni (ISP, HVPP se abilitato da adattatori esterni).
- Lettura/Scrittura della Flash.
- Manipolazione dei fuse bits e lock bits.
- Backup completo del microcontrollore prima della riprogrammazione.
- Verifica integrità post-flash.
- Compatibilità con MCU popolari come ATmega328P, ATtiny85, ATmega32U4 e molte altre.

Esempio pratico

Programmazione di un ATtiny85 per un progetto LED PWM:

- Collegare i pin GPIO → ISP (MOSI/MISO/SCK/RESET).
- Caricare il file firmware.hex.
- Impostare fuse bits per usare il clock interno a 8 MHz.
- Flash → Verifica → Test del LED pilotato.

(Note: Alcuni chip AVR richiedono alimentazione 5 V)

### **• DAP Link**

Interfaccia multiprotocollo SWD/JTAG per debugger ARM. Ideale per lavorare con microcontrollori Cortex-M.

Funzionalità ampliate:

- Supporto alle estensioni CMSIS-DAP.
- Debug live: breakpoints, step-through, memory watch.
- Flashing firmware diretto via SWD/JTAG.
- Monitoraggio registri core ARM.
- Compatibilità con IDE e toolchain note:
    - Keil
    - PlatformIO
    - OpenOCD
    - pyOCD

Esempio pratico

Debug di un firmware STM32 che gestisce un sensore I2C:

- Connettere SWDIO, SWCLK, GND.
- Avviare debug → eseguire step-through del codice.
- Monitorare i registri I2C nel debugger.
- Risolvere un problema di ACK mancante sul sensore.

(Note: Assicurarsi che il target sia alimentato dalla propria sorgente)

### **• Ethernet Troubleshooter**

Strumento per diagnosticare problemi di rete tramite adattatori Ethernet supportati.

Funzionalità ampliate:

- Rilevamento link (10/100/1000 Mbps).
- Analisi dei pacchetti ARP, DHCP, ICMP (in base a supporto hardware).
- Verifica connettività LAN e gateway.
- Test velocità negoziata e duplex.
- Lettura parametri PHY: link state, errori, collisioni.
- Modalità “Quick Ping” per test rapidi di raggiungibilità.

Esempio pratico

Verifica del cablaggio di una rete domestica:

- Connettere adattatore USB-Ethernet.
- Controllare stato link → verifica negoziazione 1000 Mbps.
- Effettuare Ping verso router.
- Confermare cablaggio corretto e assenza di disconnessioni.

### **• I2C Tools**

Suite completa per l'analisi del bus I2C, pensata per debugging rapido di sensori e moduli.

Funzionalità ampliate:

- Scansione indirizzi I2C e rilevamento dispositivi attivi.
- Lettura e scrittura registri a 8 o 16 bit.
- Dump completo di memoria su dispositivi che lo supportano (EEPROM, sensori).
- Modalità “Continuous Polling” per visualizzare variazioni di stato in real-time.
- Supporto a clock standard: 100 kHz, 400 kHz, eventuale Fast Mode+ se hardware compatibile.

Esempio pratico

Debug di un sensore BME280 che risponde con valori errati:

- Avviare I2C scan → verificare indirizzo 0x76.
- Leggere registri interni → confrontare con datasheet.
- Trovata configurazione errata del bit di oversampling.
- Correggere il registro e verificare i valori corretti.

### **• SPI Mem Manager**

Gestione avanzata di memorie SPI NOR/NAND, EEPROM SPI e flash esterne.

Funzionalità ampliate:

- Lettura completa della memoria (dump su file).
- Scrittura settoriale o completa.
- Cancellazione pagine, settori, o chip erase totale.
- Identificazione automatica tramite JEDEC ID.
- Supporto a memorie tipiche: W25Qxx, AT25xxx, MXIC, GD25Qxx...
- Verifica CRC e confronto binari dopo la scrittura.

Esempio pratico

Backup e modifica firmware di una memoria W25Q16:

- Collegare CS/MOSI/MISO/SCK.
- Estrarre il dump → salvare backup.
- Modificare alcune stringhe del firmware.
- Flashare nuovo contenuto → verifica CRC.

### **• SWD Probe**

Sonda ARM SWD leggera per debug e flash di microcontrollori Cortex-M.

Funzionalità ampliate:

- Programmazione firmware tramite SWD.
- Halt/Resume, breakpoints, accesso ai registri core.
- Lettura/scrittura memoria interna (flash e RAM).
- Supporto a dispositivi STM32, nRF52, GD32, RP2040 e altri ARM Cortex-M.
- Funzione “Auto-Detect Target” con riconoscimento IDCODE.

Esempio pratico

- Flash di un firmware su RP2040 (Raspberry Pi Pico):
- Collegare SWCLK/SWDIO.
- Caricare firmware.uf2 o binario.
- Programmare → riavviare → testare.
- Verificare IDCODE per confermare target corretto.