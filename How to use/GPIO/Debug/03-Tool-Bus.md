## 4. AVR Flasher

### Programmazione ISP di microcontrollori AVR

La famiglia AVR (ATmega, ATtiny) di Microchip (ex Atmel) e ancora onnipresente in progetti Arduino, dispositivi legacy, e molti prodotti industriali. Il Flipper Zero supporta la programmazione ISP (In-System Programming), il metodo standard per flashare MCU AVR.

### Il protocollo ISP

ISP usa l'interfaccia SPI per comunicare con la MCU AVR:

```
Flipper Zero          Target AVR
-----------          ----------
Pin 2 (SCK)    -->  SCK  (Pin 19 su ATmega328P)
Pin 3 (MOSI)   -->  MOSI (Pin 17)
Pin 4 (MISO)   <--  MISO (Pin 18)
Pin 5 (CS)     -->  RESET (Pin 1)
Pin 8 (GND)    -->  GND
Pin 9 (3.3V)   -->  VCC (SOLO se target a 3.3V!)
```

> ATTENZIONE: Molti AVR operano a 5V. Il Flipper lavora a 3.3V. Programmando un ATmega328P alimentato a 5V, i livelli logici delle risposte MISO saranno a 5V e possono danneggiare il GPIO del Flipper. Soluzioni:
> - Alimenta l'AVR a 3.3V se il progetto lo permette
> - Usa un level shifter bidirezionale
> - Usa un voltage divider sulla linea MISO (resistivo, economico)

### Fuse bits -- La configurazione critica degli AVR

I fuse bits sono registri di configurazione non-volatile che controllano il comportamento fondamentale della MCU. Sono scritti una sola volta (ma riscrivibili) e un errore puo "brickare" il chip.

**ATmega328P -- Fuse bits:**

| Fuse | Bits | Funzione |
|------|------|----------|
| Low Fuse (lfuse) | 8 bit | Sorgente clock, tempo di startup, divisore clock |
| High Fuse (hfuse) | 8 bit | Bootloader, EESAVE, watchdog, SPI enable, reset |
| Extended Fuse (efuse) | 3 bit | Brown-out detection level |

**Valori comuni:**

```
Configurazione           | lfuse | hfuse | efuse
------------------------|-------|-------|------
Arduino Uno default     | 0xFF  | 0xDE  | 0xFD
Clock interno 8 MHz     | 0xE2  | 0xD9  | 0xFF
Clock esterno 16 MHz    | 0xFF  | 0xD9  | 0xFF
Clock interno no div8   | 0x62  | 0xDF  | 0xFF
```

**Bit critico -- SPIEN (hfuse bit 5):**
Se disabiliti SPIEN (SPI Enable), non potrai piu programmare il chip via ISP. Servira un programmatore High Voltage (HVPP) per recuperarlo. Il Flipper NON supporta HVPP.

**Bit critico -- RSTDISBL (hfuse bit 7):**
Disabilita il pin di reset, liberandolo come GPIO aggiuntivo. Ma senza pin di reset, ISP non funziona piu. Anche qui serve HVPP per recuperare.

### Lock bits -- Protezione del codice

I lock bits proteggono il firmware dalla lettura/scrittura non autorizzata:

| Mode | LB2 | LB1 | Descrizione |
|------|-----|-----|-------------|
| 1 | 1 | 1 | Nessuna protezione |
| 2 | 1 | 0 | Scrittura flash/EEPROM disabilitata |
| 3 | 0 | 0 | Lettura e scrittura disabilitata |

Nel pentest: se i lock bits sono in mode 3, non puoi leggere il firmware via ISP. Pero un chip erase resetta i lock bits (e cancella tutto). Se non hai bisogno del firmware originale ma vuoi riprogrammare il chip, questo e sufficiente.

> Nota personale: a differenza dei chip ARM con readout protection multilivello, gli AVR con lock bits in mode 3 sono effettivamente protetti dalla lettura ISP. Non esistono glitch attack noti per bypassarli senza erase. Se trovi un AVR con lock bits attivati e hai bisogno del firmware, le opzioni sono: analisi del bus SPI/I2C delle periferiche, intercettazione del flusso dati durante l'operazione normale, o side-channel attacks (molto avanzati).

### Procedura -- Flash ATmega328P

1. **Collegamento ISP** (vedi pinout sopra)
2. **Sul Flipper:** GPIO -> Debug -> AVR Flasher
3. **Rilevamento chip:**
   - Il Flipper legge la signature del chip
   - ATmega328P: signature 0x1E 0x95 0x0F
   - Se la signature e 0x00 0x00 0x00: cablaggio errato o chip non alimentato
   - Se la signature e 0xFF 0xFF 0xFF: clock non configurato o chip in stato anomalo
4. **Backup PRIMA di qualsiasi modifica:**
   - Leggi flash (32 KB per ATmega328P)
   - Leggi EEPROM (1 KB)
   - Leggi fuse bits (low, high, extended)
   - Salva tutto su SD card
5. **Programmazione:**
   - Carica il file .hex dalla SD card
   - Flash -> Verifica -> I dati scritti vengono riletti e confrontati
6. **Impostazione fuse bits:**
   - Imposta solo se sai cosa stai facendo
   - Verifica ogni bit con il datasheet aperto
   - Un fuse sbagliato puo rendere il chip irraggiungibile via ISP

### Procedura -- Flash ATtiny85

L'ATtiny85 e popolare per progetti miniaturizzati (Digispark, USB HID attack tool):

```
ATtiny85 Pinout (DIP-8):
         +---v---+
 RESET  1|       |8  VCC
 PB3    2|       |7  PB2 (SCK)
 PB4    3|       |6  PB1 (MOSI)
 GND    4|       |5  PB0 (MISO)
         +-------+
```

Collegamento al Flipper:
```
Flipper Pin 2 (SCK)   --> ATtiny85 Pin 7 (PB2/SCK)
Flipper Pin 3 (MOSI)  --> ATtiny85 Pin 6 (PB1/MOSI)
Flipper Pin 4 (MISO)  --> ATtiny85 Pin 5 (PB0/MISO)
Flipper Pin 5 (CS)    --> ATtiny85 Pin 1 (RESET)
Flipper Pin 8 (GND)   --> ATtiny85 Pin 4 (GND)
```

**Signature ATtiny85:** 0x1E 0x93 0x0B

**Fuse defaults ATtiny85:**
- lfuse: 0x62 (clock interno 8 MHz con divisore /8 = 1 MHz)
- hfuse: 0xDF
- efuse: 0xFF

Per clock a 8 MHz senza divisore: lfuse = 0xE2

**EEPROM ATtiny85:**
- 512 byte di EEPROM
- Spesso usata per memorizzare configurazioni, chiavi, parametri
- Leggere la EEPROM durante un assessment puo rivelare dati interessanti

> Nota personale: l'ATtiny85 e il chip che incontro piu spesso nei "Rubber Ducky" fai-da-te (Digispark). Molti script di attacco USB HID vengono caricati su questi chip e lasciati in giro come attacchi fisici. Poter leggere e analizzare il firmware di un ATtiny85 trovato inserito in una porta USB e una skill fondamentale per l'incident response.

### Altre MCU AVR supportate

| Chip | Flash | EEPROM | Signature | Note |
|------|-------|--------|-----------|------|
| ATmega328P | 32 KB | 1 KB | 1E 95 0F | Arduino Uno |
| ATmega328PB | 32 KB | 1 KB | 1E 95 16 | Variante migliorata |
| ATmega32U4 | 32 KB | 1 KB | 1E 95 87 | Arduino Leonardo, Pro Micro |
| ATtiny85 | 8 KB | 512 B | 1E 93 0B | Digispark |
| ATtiny84 | 8 KB | 512 B | 1E 93 0C | Progetti miniaturizzati |
| ATtiny13A | 1 KB | 64 B | 1E 90 07 | Ultra-economico |
| ATmega2560 | 256 KB | 4 KB | 1E 98 01 | Arduino Mega |

---

## 5. I2C Tools

### Il bus I2C nel contesto del pentest hardware

I2C (Inter-Integrated Circuit, pronunciato "I-squared-C") e il bus piu usato per la comunicazione tra microcontrollore e periferiche sulla stessa PCB. Quasi ogni dispositivo embedded ha almeno un bus I2C con sopra qualcosa di interessante.

### Architettura del bus

```
         VCC (3.3V o 5V)
          |        |
         [R]      [R]     R = Pull-up resistors (tipicamente 4.7K)
          |        |
SDA ------+--------+------[MCU]------[EEPROM]------[Sensore]------[RTC]
SCL ------+--------+------[MCU]------[EEPROM]------[Sensore]------[RTC]
          |
         GND
```

**Caratteristiche:**
- Bus multi-master, multi-slave
- Ogni dispositivo ha un indirizzo a 7 bit (0x00-0x7F) o 10 bit
- Velocita: 100 kHz (Standard), 400 kHz (Fast), 1 MHz (Fast Mode+)
- Due fili: SDA (data), SCL (clock)
- Pull-up resistor necessari su entrambe le linee

### I2C Scan -- Trovare dispositivi sul bus

La scansione I2C e il primo passo per esplorare una PCB sconosciuta. Il Flipper invia un byte di start a ogni indirizzo possibile e verifica se qualcuno risponde con un ACK.

**Procedura:**

1. Collega SDA, SCL, GND al Flipper
2. GPIO -> Debug -> I2C Tools -> Scan
3. Il Flipper scansiona gli indirizzi da 0x01 a 0x7F
4. Gli indirizzi che rispondono vengono elencati

**Indirizzi comuni e cosa significano:**

```
Indirizzo  | Dispositivo tipico
-----------|-----------------------------------
0x20-0x27  | PCF8574 (I/O expander)
0x38-0x3F  | PCF8574A (I/O expander)
0x3C-0x3D  | SSD1306 (display OLED)
0x40       | HDC1080 (sensore umidita)
0x44       | SHT30/SHT31 (sensore temp/umidita)
0x48-0x4F  | ADS1115 (ADC), TMP102 (temp)
0x50-0x57  | AT24Cxx (EEPROM) ← MOLTO INTERESSANTE
0x68       | DS3231 (RTC), MPU6050 (IMU)
0x69       | MPU6050 (indirizzo alternativo)
0x76       | BME280/BMP280 (sensore ambientale)
0x77       | BME280 (indirizzo alternativo)
```

> CRUCIALE: l'indirizzo 0x50-0x57 e quasi sempre una EEPROM. Le EEPROM contengono configurazioni, chiavi, credenziali, certificati, parametri di calibrazione. Se trovi un dispositivo a 0x50 durante un assessment, dumpalo subito.

### Lettura e scrittura registri

Ogni dispositivo I2C ha una mappa di registri interni. Per leggere un registro:

1. Invio indirizzo dispositivo + bit W (Write)
2. Invio indirizzo del registro da leggere
3. Repeated Start
4. Invio indirizzo dispositivo + bit R (Read)
5. Lettura del byte di risposta

Il Flipper semplifica tutto questo: selezioni indirizzo, registro, e leggi/scrivi.

**Esempio -- Lettura WHO_AM_I di un BME280 (indirizzo 0x76):**

- Registro 0xD0 (Chip ID)
- Valore atteso: 0x60 (BME280) o 0x58 (BMP280)
- Se il valore non corrisponde: il chip potrebbe essere un clone o un dispositivo diverso

**Esempio -- Lettura registri di un MPU6050 (indirizzo 0x68):**

- Registro 0x75 (WHO_AM_I): valore atteso 0x68
- Registri 0x3B-0x48: dati accelerometro e giroscopio raw
- Registro 0x6B (PWR_MGMT_1): configurazione alimentazione

### Dump EEPROM I2C

Le EEPROM I2C della serie AT24Cxx sono il target piu prezioso su un bus I2C:

| Chip | Capacita | Indirizzi pagina | Indirizzo I2C base |
|------|----------|------------------|-------------------|
| AT24C01 | 128 byte | 8 bit | 0x50 |
| AT24C02 | 256 byte | 8 bit | 0x50 |
| AT24C04 | 512 byte | 8 bit | 0x50-0x51 |
| AT24C08 | 1 KB | 8 bit | 0x50-0x53 |
| AT24C16 | 2 KB | 8 bit | 0x50-0x57 |
| AT24C32 | 4 KB | 16 bit | 0x50 |
| AT24C64 | 8 KB | 16 bit | 0x50 |
| AT24C128 | 16 KB | 16 bit | 0x50 |
| AT24C256 | 32 KB | 16 bit | 0x50 |
| AT24C512 | 64 KB | 16 bit | 0x50 |

**Procedura di dump:**

1. Identifica il chip (lettura dei primi byte per capire la dimensione)
2. Leggi sequenzialmente da indirizzo 0x0000 fino alla dimensione massima
3. Salva il dump su SD card
4. Analizza con hex editor (HxD, xxd, hexdump)

**Cosa cercare in un dump EEPROM:**
- Stringhe ASCII leggibili (credenziali, URL, nomi)
- Indirizzi MAC
- Chiavi AES/DES (sequenze di byte ad alta entropia, lunghezza 16/24/32 byte)
- Certificati X.509 (iniziano con 0x30 0x82)
- Strutture di configurazione (spesso nei primi byte)
- Numeri di serie, versioni firmware, parametri di calibrazione

### Debug di sensori I2C

Quando un sensore I2C non funziona correttamente, il Flipper puo aiutare a diagnosticare:

**Problemi comuni:**

| Sintomo | Causa probabile | Verifica |
|---------|----------------|----------|
| Nessun ACK | Indirizzo sbagliato, cablaggio, chip morto | Scan, controlla pull-up |
| Lettura sempre 0x00 | Sensore in sleep/reset | Scrivi registro di wakeup |
| Lettura sempre 0xFF | Bus flottante, pull-up mancanti | Controlla resistori pull-up |
| Dati instabili | Interferenze, cavi troppo lunghi, clock troppo alto | Riduci velocita, accorcia cavi |
| ACK ma dati errati | Configurazione registri sbagliata | Confronta con datasheet |

**Procedura diagnostica:**

1. I2C Scan -- verifica che il dispositivo risponda
2. Leggi registro ID/WHO_AM_I -- conferma il tipo di chip
3. Leggi registri di stato -- verifica se il sensore e in stato di errore
4. Leggi registri di configurazione -- confronta con valori attesi
5. Scrivi configurazione corretta -- modifica registri se necessario
6. Leggi registri dati -- verifica che i valori siano plausibili

> Nota personale: l'I2C scan e la prima cosa che faccio quando apro un dispositivo sconosciuto. E veloce (pochi secondi), non invasiva, e ti da immediatamente un quadro di cosa c'e sulla PCB. Una volta ho trovato una EEPROM non documentata su una centralina domotica che conteneva le password WiFi in chiaro. Il produttore aveva dimenticato di rimuovere la EEPROM di configurazione dalla versione di produzione.

---

## 6. SPI Mem Manager

### Il dump SPI -- La tecnica piu usata per estrarre firmware

La maggior parte dei dispositivi embedded con processori piu potenti (router, telecamere IP, NAS, smart TV) usa memorie flash SPI esterne per memorizzare il firmware. Queste memorie sono chip separati dalla CPU, collegati via bus SPI, e quasi sempre leggibili direttamente con un clip SOIC-8 senza bisogno di interfacciarsi con la CPU.

Questo e il motivo per cui il dump SPI e la tecnica piu usata e piu affidabile per estrarre firmware.

### Il bus SPI

```
Flipper Zero          Flash SPI
-----------          ---------
Pin 2 (SCK)    -->  CLK    (Pin 6)
Pin 3 (MOSI)   -->  DI     (Pin 5)
Pin 4 (MISO)   <--  DO     (Pin 2)
Pin 5 (CS)     -->  CS#    (Pin 1)
Pin 8 (GND)    -->  GND    (Pin 4)
Pin 9 (3.3V)   -->  VCC    (Pin 8)
```

**Pinout chip SPI SOIC-8 (standard):**

```
        +---v---+
 CS#   1|       |8  VCC
 DO    2|       |7  HOLD#
 WP#   3|       |6  CLK
 GND   4|       |5  DI
        +-------+
```

### La clip SOIC-8 -- Evitare di dissaldare

La clip SOIC-8 (Pomona 5250 o equivalenti economiche) e lo strumento che fa la differenza tra un'operazione pulita e un casino. Si aggancia direttamente al chip sulla PCB senza doverlo dissaldare.

**Procedura con clip SOIC-8:**

1. **Identifica il chip flash sulla PCB**
   - Cerca chip SOIC-8 vicino alla CPU principale
   - Serigrafia tipica: W25Q32, W25Q64, MX25L128, AT25SF041
   - Se non c'e serigrafia, cerca il package SOIC-8 e verifica con multimetro

2. **Collega la clip**
   - Allinea il pin 1 della clip con il pin 1 del chip (punto/tacca sull'angolo)
   - Premi con decisione -- il contatto deve essere saldo
   - La clip deve essere perfettamente allineata, anche mezzo millimetro di offset causa letture errate

3. **Gestione dell'alimentazione**
   - IMPORTANTE: se la PCB e alimentata, la CPU potrebbe contendere il bus SPI
   - Opzione A: PCB spenta, alimentazione dal Flipper (3.3V pin 9) -- preferibile
   - Opzione B: PCB accesa, tieni la CPU in reset per evitare contesa bus
   - Opzione C: PCB accesa, prega che la CPU non interferisca -- sconsigliato

> ATTENZIONE: il pin 9 del Flipper fornisce 3.3V ma con corrente limitata. Per chip flash che richiedono piu corrente durante le operazioni di scrittura, potresti aver bisogno di alimentazione esterna. Per la sola lettura, il Flipper e generalmente sufficiente.

### JEDEC ID -- Identificazione automatica del chip

Ogni memoria flash SPI ha un JEDEC ID unico che identifica produttore, tipo e capacita:

```bash
# Il Flipper legge automaticamente il JEDEC ID
# Formato: Manufacturer ID + Memory Type + Capacity

Manufacturer ID  | Produttore
-----------------|------------
0xEF             | Winbond
0xC2             | Macronix (MXIC)
0xC8             | GigaDevice
0x1F             | Adesto (ex Atmel)
0x20             | Micron/Numonyx
0x01             | Spansion/Cypress
0xBF             | SST/Microchip
```

**Chip flash SPI comuni nel mondo IoT:**

| Chip | JEDEC ID | Capacita | Settore | Pagina | Uso tipico |
|------|----------|----------|---------|--------|------------|
| W25Q16 | EF 40 15 | 2 MB | 4 KB | 256 B | IoT economici |
| W25Q32 | EF 40 16 | 4 MB | 4 KB | 256 B | Router low-end |
| W25Q64 | EF 40 17 | 8 MB | 4 KB | 256 B | Router, telecamere |
| W25Q128 | EF 40 18 | 16 MB | 4 KB | 256 B | Router avanzati |
| W25Q256 | EF 40 19 | 32 MB | 4 KB | 256 B | NAS, smart TV |
| MX25L6406E | C2 20 17 | 8 MB | 4 KB | 256 B | Dispositivi Macronix |
| MX25L12835F | C2 20 18 | 16 MB | 4 KB | 256 B | Router TP-Link |
| GD25Q64 | C8 40 17 | 8 MB | 4 KB | 256 B | Clone Winbond |
| AT25SF041 | 1F 84 01 | 512 KB | 4 KB | 256 B | IoT ultra-economici |

### Procedura di dump completa

**Passo 1 -- Connessione e identificazione:**

1. Sul Flipper: GPIO -> Debug -> SPI Mem Manager
2. Il Flipper legge il JEDEC ID
3. Se il chip e nel database, mostra nome e capacita
4. Se non riconosciuto, mostra il JEDEC ID raw -- cercalo manualmente nel datasheet

**Passo 2 -- Lettura completa (dump):**

1. Seleziona "Read"
2. Il Flipper legge l'intero chip sequenzialmente
3. Tempo stimato:
   - 2 MB (W25Q16): ~30 secondi
   - 8 MB (W25Q64): ~2 minuti
   - 16 MB (W25Q128): ~4 minuti
   - 32 MB (W25Q256): ~8 minuti
4. Il dump viene salvato su SD card come file .bin

**Passo 3 -- Verifica integrita:**

1. Seleziona "Verify" o fai un secondo dump
2. Confronta i due dump (CRC o byte-by-byte)
3. Se differiscono: contatto clip instabile, interferenze, o contesa bus
4. Ripeti finche non hai due dump identici

**Passo 4 -- Analisi del dump:**

```bash
# Informazioni base
file firmware.bin
hexdump -C firmware.bin | head -50

# Ricerca filesystem e componenti
binwalk firmware.bin

# Output tipico di un router:
# DECIMAL       HEXADECIMAL     DESCRIPTION
# 0             0x0             uImage header, header size: 64 bytes
# 64            0x40            LZMA compressed data
# 1048576       0x100000        Squashfs filesystem, little endian

# Estrazione
binwalk -e firmware.bin

# Ricerca stringhe
strings -n 8 firmware.bin | grep -i password
strings -n 8 firmware.bin | grep -i admin
strings -n 8 firmware.bin | grep -i key
strings -n 8 firmware.bin | grep -i secret

# Analisi entropia (per trovare sezioni crittografate/compresse)
binwalk -E firmware.bin
```

### Operazioni di scrittura

Oltre al dump (lettura), il SPI Mem Manager supporta:

**Scrittura completa:**
- Carica un file .bin dalla SD card
- Il Flipper scrive pagina per pagina (256 byte alla volta)
- Verifica automatica dopo la scrittura

**Cancellazione:**
- Sector Erase: cancella un settore da 4 KB
- Block Erase (32 KB o 64 KB): cancella un blocco
- Chip Erase: cancella l'intero chip (necessario prima di riscrivere)

**Flusso tipico per modificare firmware:**

1. Dump originale (salvare come backup!)
2. Analisi e modifica del dump sul PC
3. Chip Erase sul target
4. Scrittura del firmware modificato
5. Verifica CRC
6. Test funzionale del dispositivo

> Nota personale: il dump SPI e la tecnica che uso nel 70% dei miei assessment hardware. E affidabile, non richiede interazione con la CPU del target, e funziona anche quando SWD/JTAG sono protetti. Il consiglio piu importante: fai SEMPRE un secondo dump e confrontalo con il primo. Una clip SOIC-8 che fa contatto imperfetto produce dump corrotti ma plausibili -- potresti non accorgerti dell'errore finche non tenti di analizzare il firmware e trovi dati senza senso. Due dump identici = dump affidabile.

### Problemi comuni e soluzioni

| Problema | Causa | Soluzione |
|----------|-------|-----------|
| JEDEC ID = 0x000000 | Nessun contatto | Verifica clip, cablaggio |
| JEDEC ID = 0xFFFFFF | Bus flottante, CS non attivo | Controlla CS, verifica pull-up |
| Dump tutto 0xFF | Chip vuoto o lettura fallita | Verifica alimentazione, rifai dump |
| Dump diversi ogni volta | Contatto instabile | Pulisci pad, riallinea clip |
| Lettura lenta/timeout | Clock troppo alto | Riduci velocita SPI |
| Chip non riconosciuto | JEDEC ID non nel DB | Aggiungi manualmente con datasheet |
| Contesa bus con CPU | CPU attiva sul bus SPI | Tieni CPU in reset o scollega |

---

## 7. Ethernet Troubleshooter

### Diagnostica di rete via adattatore USB-Ethernet

L'Ethernet Troubleshooter e uno strumento complementare che usa un adattatore USB-Ethernet collegato alla porta USB-C del Flipper Zero per diagnosticare problemi di rete a livello fisico e di link.

### Funzionalita

**Rilevamento link:**
- Stato del link (up/down)
- Velocita negoziata (10/100/1000 Mbps)
- Modalita duplex (half/full)
- Auto-negotiation status

**Diagnostica cablaggio:**
- Verifica continuita delle coppie
- Rilevamento cross-over
- Identificazione coppie interrotte o in corto
- Stima lunghezza cavo (TDR - Time Domain Reflectometry, se supportato dall'adattatore)

**Test di connettivita:**
- Ping (ICMP echo)
- Verifica DHCP (richiesta indirizzo IP)
- Rilevamento gateway
- Test raggiungibilita server DNS

**Analisi PHY:**
- Lettura registri PHY
- Statistiche errori (CRC errors, frame errors, collisions)
- Stato auto-negotiation
- Capacita del link partner

### Quando usarlo nel pentest

L'Ethernet Troubleshooter e utile in scenari specifici:

1. **Verifica di porte di rete sospette**
   - Trovi una porta Ethernet su un dispositivo (es. pannello di controllo industriale)
   - Vuoi verificare se e attiva e a quale rete e connessa
   - Il Flipper puo verificare link, ottenere DHCP, e fare ping

2. **Diagnostica rapida in ambienti ICS/SCADA**
   - Verifica connettivita tra PLC e HMI
   - Test di cavi in ambienti industriali
   - Controllo parametri fisici del link

3. **Verifica segmentazione di rete**
   - Collegati a una porta e verifica quale VLAN/subnet viene assegnata
   - Testa se la segmentazione e effettivamente implementata

**Adattatori USB-Ethernet supportati:**
- Chip ASIX AX88179 (USB 3.0, Gigabit)
- Chip Realtek RTL8152B (USB 2.0, 100 Mbps)
- Verifica compatibilita con il firmware in uso

> Nota personale: l'Ethernet Troubleshooter non e lo strumento piu usato del toolkit Debug, ma ha salvato qualche situazione. In un assessment di una rete industriale, ho usato il Flipper per verificare rapidamente quali porte di un armadio rack erano attive e in quale VLAN, senza dover portare un laptop completo. Non sostituisce uno strumento di rete professionale, ma per un check rapido in campo e perfetto.

---

