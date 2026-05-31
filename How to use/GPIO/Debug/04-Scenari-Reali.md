## 8. Scenari di Hardware Pentest

### Scenario 1 -- Dump firmware router via SPI

**Obiettivo:** Estrarre il firmware completo di un router domestico per analisi di vulnerabilita.

**Target:** Router TP-Link generico con chip flash Winbond W25Q64.

**Fase 1 -- Ricognizione:**
1. Apri il case del router (4 viti sotto i piedini di gomma, come sempre)
2. Identifica i componenti principali sulla PCB:
   - SoC principale (Mediatek, Qualcomm, Realtek)
   - Chip RAM (DDR2/DDR3)
   - Chip flash SPI (il nostro target)
3. Fotografa la PCB con buona illuminazione -- serviranno i riferimenti
4. Identifica il chip flash: SOIC-8, serigrafia "W25Q64FVSIG"
5. Verifica il pinout dal datasheet Winbond

**Fase 2 -- Dump:**
1. Scollega l'alimentazione del router
2. Posiziona la clip SOIC-8 sul chip flash
   - Pin 1 della clip allineato con il punto sul chip
   - Verifica con multimetro che GND della clip sia connesso a GND della PCB
3. Collega la clip al Flipper Zero:
   - CS -> Pin 5
   - DO (MISO) -> Pin 4
   - DI (MOSI) -> Pin 3
   - CLK -> Pin 2
   - GND -> Pin 8
   - VCC -> Pin 9 (3.3V dal Flipper)
4. Avvia SPI Mem Manager
5. Il Flipper legge JEDEC ID: EF 40 17 -> Winbond W25Q64, 8 MB
6. Avvia lettura completa: ~2 minuti
7. Salva come `router_dump1.bin`
8. Ripeti il dump: `router_dump2.bin`
9. Confronta i due file: se identici, il dump e affidabile

**Fase 3 -- Analisi:**
```bash
# Estrai componenti
binwalk -e router_dump1.bin

# Struttura tipica firmware router:
# - Bootloader (U-Boot, ~256 KB)
# - Kernel Linux compresso (LZMA, ~1-2 MB)
# - Filesystem root (SquashFS, ~4-6 MB)
# - Configurazione/ART (partition table, calibration, ~64 KB)

# Esplora il filesystem estratto
ls _router_dump1.bin.extracted/squashfs-root/

# Cerca credenziali
grep -r "password" _router_dump1.bin.extracted/squashfs-root/etc/
cat _router_dump1.bin.extracted/squashfs-root/etc/shadow

# Cerca chiavi SSH/SSL
find _router_dump1.bin.extracted/ -name "*.pem" -o -name "*.key"

# Cerca configurazioni interessanti
cat _router_dump1.bin.extracted/squashfs-root/etc/config/wireless
```

**Cosa cercare:**
- Password di default in /etc/shadow o /etc/passwd
- Chiavi SSL/TLS hardcoded
- Script di init con credenziali
- Backdoor o servizi nascosti (telnetd su porte non standard)
- Versioni di librerie con CVE note (busybox, dnsmasq, uhttpd)

### Scenario 2 -- Shell root via UART su IP camera

**Obiettivo:** Ottenere una shell root su una telecamera IP per analisi di sicurezza.

**Target:** Telecamera IP generica basata su SoC HiSilicon/Ingenic.

**Fase 1 -- Trovare UART:**
1. Apri la telecamera (attenzione: spesso cavi flat delicati per il sensore)
2. Cerca header a 3-4 pin non popolati vicino alla CPU
3. Usa il multimetro:
   - Un pin sara GND (continuita con piano di massa)
   - Un pin sara VCC (3.3V costante)
   - Un pin sara TX (tensione che varia, ~3.3V a riposo)
   - Un pin sara RX (3.3V costante, pull-up)
4. In alternativa, usa un logic analyzer o oscilloscopio per identificare TX dal traffico seriale durante il boot

**Fase 2 -- Connessione UART:**
1. Collega al Flipper (o meglio, a un adattatore USB-UART per avere la console sul PC):
   - TX della camera -> RX del Flipper/adattatore
   - RX della camera -> TX del Flipper/adattatore
   - GND -> GND
2. Imposta il baud rate: prova 115200 per primo (il piu comune)
3. Se vedi caratteri corrotti, prova: 9600, 19200, 38400, 57600

**Fase 3 -- Boot e interazione:**

Output tipico durante il boot:
```
U-Boot 2016.11 (May 12 2021)
DRAM: 64 MiB
Loading kernel...
Starting kernel...
[    0.000000] Linux version 3.18.20
...
[    5.234567] Starting network...
Welcome to HiLinux
login:
```

**Possibilita:**
1. **Shell root senza password:** molte telecamere economiche hanno `root:` senza password o con password nota (root, admin, xc3511, jvbzd)
2. **Interrupt U-Boot:** durante il boot, premi un tasto entro 1-3 secondi per entrare nella console U-Boot
3. **Console U-Boot:** da qui puoi modificare i parametri di boot del kernel

```bash
# Nella console U-Boot:
# Modifica boot args per aggiungere una shell
setenv bootargs console=ttyS0,115200 init=/bin/sh
boot

# Ora hai una shell root senza login
# Monta il filesystem read-write
mount -o remount,rw /

# Cambia password root
passwd root

# Oppure aggiungi una backdoor SSH
```

**Fase 4 -- Post-exploitation:**
- Esplora il filesystem per credenziali cloud (RTSP, P2P, API)
- Cerca chiavi di crittografia per il flusso video
- Analizza i servizi in esecuzione (spesso ci sono backdoor del produttore)
- Verifica se il firmware e aggiornabile e se l'aggiornamento e firmato

### Scenario 3 -- Estrazione chiavi crittografiche via SWD su serratura IoT

**Obiettivo:** Estrarre le chiavi di crittografia BLE usate da una serratura smart.

**Target:** Serratura smart basata su nRF52832 (Nordic Semiconductor).

**Fase 1 -- Analisi esterna:**
1. La serratura usa BLE per comunicare con l'app smartphone
2. Sniffa il traffico BLE per capire il protocollo (con un altro Flipper o con Ubertooth)
3. Il traffico e crittografato -- servono le chiavi

**Fase 2 -- Accesso fisico:**
1. Smonta la serratura (solitamente 2 viti + clip a scatto)
2. Identifica il nRF52832 sulla PCB
3. Cerca i pad SWD (spesso test pad non popolati, a volte nascosti sotto adesivi)
4. Collega SWCLK, SWDIO, GND al Flipper

**Fase 3 -- SWD Probe:**
1. Avvia SWD Probe
2. Il Flipper legge IDCODE: 0x0BC11477 -> nRF52832 confermato
3. Verifica APPROTECT: se disabilitato (molto frequente sulle serrature economiche), procedi
4. Halt CPU
5. Dump completo:
   - Flash: 512 KB da 0x00000000
   - UICR: 256 byte da 0x10001000
   - RAM: 64 KB da 0x20000000 (se la serratura era accesa, la RAM contiene dati live)

**Fase 4 -- Analisi:**
```bash
# Carica il dump in Ghidra
# Target: ARM Cortex-M4 Little Endian
# Base address: 0x00000000
# Il SoftDevice Nordic occupa i primi ~148 KB

# Cerca strutture dati relative a chiavi
# Le chiavi BLE LTK (Long Term Key) sono tipicamente a 0x20000000+ in RAM
# Oppure nella flash, nella sezione di bonding data

# Cerca pattern noti
strings flash_dump.bin | grep -i "key"
strings flash_dump.bin | grep -i "pass"
strings flash_dump.bin | grep -i "pin"

# Analizza la UICR per chiavi custom
hexdump -C uicr_dump.bin
```

**Cosa cercare:**
- BLE bonding keys (LTK, IRK, CSRK)
- Chiavi AES per la crittografia del payload
- PIN/password hardcoded
- Tabelle di autorizzazione utenti
- Chiavi di firma per aggiornamenti OTA

> Nota personale: le serrature smart economiche sono tra i target piu interessanti per il pentest hardware. Il modello di business spinge a tagliare i costi sulla sicurezza: nRF52 senza APPROTECT, chiavi in chiaro nella flash, protocolli BLE custom fragili. In un assessment ho trovato le chiavi AES master hardcoded nella flash di una serratura che controllava l'accesso a un intero edificio. Con quelle chiavi, potevi aprire qualsiasi serratura dello stesso modello, non solo quella specifica unita. Il produttore usava la stessa chiave per tutti i dispositivi in produzione.

### Scenario 4 -- Riprogrammazione microcontrollore per bypass sicurezza

**Obiettivo:** Bypassare il sistema di autenticazione di un dispositivo modificando il firmware.

**Target:** Sistema di accesso basato su ATmega328P con lettore RFID.

**Fase 1 -- Analisi:**
1. Il dispositivo legge badge RFID e li confronta con una whitelist in EEPROM
2. Se il badge e nella lista, attiva un rele che apre la porta
3. Ipotesi: modificando la EEPROM o il firmware, possiamo bypassare il controllo

**Fase 2 -- Accesso ISP:**
1. Identifica l'ATmega328P sulla PCB del lettore
2. Cerca l'header ISP (6 pin standard: MOSI, MISO, SCK, RESET, VCC, GND)
3. Collega il Flipper in modalita AVR Flasher

**Fase 3 -- Dump e analisi:**
1. Leggi la signature: 0x1E 0x95 0x0F -> ATmega328P confermato
2. Verifica lock bits: se mode 1 (nessuna protezione), procedi
3. Dump flash (32 KB)
4. Dump EEPROM (1 KB)
5. Leggi fuse bits (backup)

**Fase 4 -- Analisi firmware:**
```bash
# Disassembla con avr-objdump
avr-objdump -D -m avr firmware.bin > firmware.asm

# Oppure carica in Ghidra con il processore AVR8
# Cerca le routine di confronto RFID
# Tipicamente: lettura tag -> confronto con tabella in EEPROM -> decisione

# Analizza EEPROM
hexdump -C eeprom.bin
# Cerca pattern di UID RFID (4 o 7 byte, solitamente in sequenza)
```

**Fase 5 -- Modifica:**

Opzione A -- Aggiungi il tuo badge alla whitelist:
- Modifica la EEPROM aggiungendo l'UID del tuo badge nella tabella
- Flashare solo la EEPROM modificata (non tocca il firmware)
- Il dispositivo funziona normalmente ma accetta anche il tuo badge

Opzione B -- Patch del firmware:
- Trova la routine di confronto nel disassemblato
- Modifica il branch condizionale che decide "accesso concesso/negato"
- Tipicamente: cambia un `BRNE` (Branch if Not Equal) in `NOP` o `BREQ`
- Flashare il firmware patchato
- Ora qualsiasi badge viene accettato

Opzione C -- Sostituisci il firmware:
- Scrivi un firmware custom che attiva sempre il rele
- Piu invasivo ma piu semplice da implementare

> Nota personale: lo scenario della EEPROM e il piu elegante e il meno rilevabile. Il firmware originale resta intatto, il dispositivo funziona normalmente per tutti gli utenti legittimi, e il tuo badge viene semplicemente aggiunto alla lista. In un red team exercise, questo approccio e passato inosservato per settimane perche il sistema continuava a funzionare perfettamente -- i log mostravano solo accessi autorizzati.

---

## Cross-Reference - Scenari Multi-Vettore

| Scenario | Modulo Correlato | Link | Come si collegano |
|----------|-----------------|------|-------------------|
| Firmware dump + NFC | NFC | [05-Scenari-Reali](../../NFC/05-Scenari-Reali.md) | Dump firmware lettore NFC via SWD per estrarre chiavi MIFARE hardcoded |
| EEPROM + RFID | RFID | [05-Scenari-Reali](../../RFID/05-Scenari-Reali.md) | Dump EEPROM lettore RFID per estrarre lista badge autorizzati |
| UART console + WiFi | WiFi-Marauder | [05-Scenari-Reali](../../WiFi-Marauder/05-Scenari-Reali.md) | Console UART su router/AP → credenziali WiFi → ESP32 per pivot |
| SPI flash + Sub-GHz | Sub-GHz | [05-Scenari-Reali](../../Sub-GHz/05-Scenari-Reali.md) | Dump SPI flash di ricevitore RF per analisi rolling code keys |
| Debug + BadUSB | USB/Bad USB | [05-Scenari-Reali](../../USB/Bad%20USB/05-Scenari-Reali.md) | Estrai firmware via debug → analizza offline → crea payload BadUSB mirato |

