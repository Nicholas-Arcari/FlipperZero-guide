## 2. SWD Probe

### Cos'e SWD e perche e il protocollo piu importante

SWD (Serial Wire Debug) e il protocollo di debug standard per tutti i microcontrollori ARM Cortex-M. Usa solo 2 fili piu la massa:

- **SWCLK** (Serial Wire Clock) -- Clock generato dal debugger
- **SWDIO** (Serial Wire Data I/O) -- Linea dati bidirezionale

Rispetto a JTAG (che richiede 4-5 fili), SWD e piu semplice, occupa meno pin, e offre le stesse funzionalita per i Cortex-M. Per questo motivo, la stragrande maggioranza dei dispositivi IoT con MCU ARM ha header SWD esposti sulla PCB.

### Architettura del protocollo SWD

Il protocollo SWD si basa su un modello a pacchetti:

```
Host (Flipper) --> Target (MCU)
   |                    |
   |--- SWCLK (clock) -->|
   |<-- SWDIO (data) --->|
   |                    |
   [Debug Port (DP)]
        |
   [Access Port (AP)]
        |
   [Memory Bus / Core Registers]
```

**Debug Port (DP)**
- Primo livello di accesso
- Contiene registri IDCODE, CTRL/STAT, SELECT, RDBUFF
- L'IDCODE identifica il chip (fondamentale per sapere cosa stai debuggando)

**Access Port (AP)**
- Secondo livello, selezionato tramite il registro SELECT del DP
- MEM-AP: accesso al bus AHB della MCU (memoria, periferiche, flash)
- JTAG-AP: per catene JTAG downstream (raro)

**Operazioni fondamentali via SWD:**

| Operazione | Descrizione | Uso nel pentest |
|---|---|---|
| Read IDCODE | Identifica il chip target | Prima cosa da fare per sapere cosa hai davanti |
| Halt CPU | Ferma l'esecuzione | Necessario per leggere flash senza interferenze |
| Resume CPU | Riprende l'esecuzione | Dopo aver finito di ispezionare |
| Read Memory | Legge indirizzi di memoria | Dump flash, RAM, registri periferiche |
| Write Memory | Scrive in memoria | Patch firmware, modifica configurazioni |
| Set Breakpoint | Punto di interruzione | Debug live del firmware |
| Flash Program | Programma la flash interna | Upload firmware modificato |

### Procedura operativa con il Flipper Zero

**Collegamento fisico:**

```
Flipper Zero          Target MCU
-----------          ----------
Pin 2 (SWCLK)  -->  SWCLK
Pin 3 (SWDIO)  -->  SWDIO
Pin 8 (GND)    -->  GND
```

> IMPORTANTE: Il target deve essere alimentato dalla propria sorgente. Il Flipper puo fornire 3.3V dal pin 9, ma solo per target a basso consumo (< 100mA). Per MCU con periferiche esterne, usa l'alimentazione originale del dispositivo.

**Passo 1 -- Connessione e identificazione:**

1. Sul Flipper: GPIO -> Debug -> SWD Probe
2. Il Flipper tenta la connessione SWD
3. Se il target risponde, legge l'IDCODE
4. L'IDCODE identifica il produttore e il modello del chip

Tabella IDCODE comuni:

```
IDCODE          | Chip
----------------|---------------------------
0x1BA01477      | STM32F1xx (Cortex-M3)
0x2BA01477      | STM32F4xx (Cortex-M4)
0x6BA02477      | STM32H7xx (Cortex-M7)
0x0BC11477      | nRF52832 (Nordic)
0x0BC12477      | nRF52840 (Nordic)
0x01002927      | RP2040 (Raspberry Pi)
```

**Passo 2 -- Halt e ispezione:**

Una volta connesso, puoi:
- Halt della CPU (ferma l'esecuzione)
- Leggere i registri core (R0-R15, PSR, MSP, PSP)
- Ispezionare la memoria a qualsiasi indirizzo

**Passo 3 -- Dump del firmware:**

Il dump della flash interna e l'operazione piu importante. Ogni MCU ha la flash mappata a indirizzi specifici:

```
Chip          | Flash Start  | Dimensione tipica
--------------|-------------|-------------------
STM32F103     | 0x08000000  | 64-128 KB
STM32F411     | 0x08000000  | 512 KB
nRF52832      | 0x00000000  | 512 KB
nRF52840      | 0x00000000  | 1 MB
RP2040        | 0x10000000  | 2-16 MB (flash esterna)
```

Dal Flipper, puoi leggere l'intero range di flash e salvarlo su SD card come file binario. Questo file puo poi essere analizzato con:
- `binwalk` per estrarre filesystem e componenti
- `strings` per cercare credenziali e URL
- `Ghidra` per disassemblaggio completo
- `radare2` per analisi rapida

### Readout Protection (RDP) -- Il nemico del pentester

La Readout Protection e il meccanismo che impedisce la lettura della flash via debug. Ogni produttore la implementa diversamente:

**STM32 -- RDP (Read-out Protection)**

| Livello | Descrizione | Aggirabile? |
|---------|-------------|-------------|
| RDP 0 | Nessuna protezione | Si -- lettura libera |
| RDP 1 | Flash protetta da lettura esterna, debug possibile | Parzialmente -- esistono glitch attack |
| RDP 2 | Debug completamente disabilitato, irreversibile | No -- il chip e "murato" per il debug |

La realta del campo: la maggior parte dei dispositivi IoT consumer ha RDP 0 (nessuna protezione). I produttori non attivano la readout protection per semplificare la produzione e gli aggiornamenti firmware. Questo significa che nella maggioranza dei casi, il dump via SWD funziona al primo tentativo.

> Nota personale: su circa 40 dispositivi IoT che ho analizzato in assessment reali, solo 3 avevano RDP attivata a livello 1 e nessuno a livello 2. E di quei 3 con RDP 1, due avevano comunque la flash esterna SPI leggibile senza protezione. Il take-away e chiaro: provare sempre SWD per primo, perche le probabilita sono a tuo favore.

**Nordic nRF52 -- APPROTECT**

| Stato | Descrizione |
|-------|-------------|
| Disabilitato | Accesso libero via SWD |
| Abilitato | Blocca l'accesso alla flash e RAM via debug |

APPROTECT e abilitato scrivendo un valore specifico nel registro UICR (User Information Configuration Register). Per disabilitarlo serve un full chip erase, che cancella tutto il firmware. Utile solo se vuoi riprogrammare il chip, non per estrarre il firmware originale.

Nota: sulle versioni piu vecchie del nRF52 (pre-2020), esisteva una vulnerabilita nel meccanismo APPROTECT che permetteva di bypassarlo tramite un glitch sul pin di reset durante il boot. Questa vulnerabilita e stata corretta nelle revisioni successive del silicio.

**RP2040 -- Secure Boot**

L'RP2040 di per se non ha readout protection nativa sulla flash esterna. La flash e una SPI esterna e puo essere letta direttamente. Nelle revisioni RP2350 e stata introdotta la Secure Boot con OTP (One-Time Programmable) fuses.

### Dump firmware -- Procedura dettagliata per STM32

Questa e la procedura passo-passo per dumpare il firmware di un STM32F103 (uno dei chip piu comuni nei dispositivi IoT economici):

1. **Identifica i pad SWD sulla PCB**
   - Cerca header a 4 pin etichettati SWD, DBG, J-Link
   - In assenza di etichette, cerca pad da 1.27mm in gruppi di 4
   - Usa il multimetro per identificare GND (continuita con piano di massa)
   - SWCLK e SWDIO sono tipicamente pull-up a 3.3V (resistenza verso VCC)

2. **Collegamento**
   - Salda fili temporanei o usa pogopins / test clip
   - Collega SWCLK, SWDIO, GND al Flipper
   - Alimenta il target dalla sua sorgente originale

3. **Connessione SWD**
   - Avvia SWD Probe sul Flipper
   - Verifica che l'IDCODE venga letto correttamente
   - Se non risponde: controlla cablaggio, verifica che il target sia alimentato

4. **Lettura flash**
   - Seleziona lettura memoria
   - Indirizzo start: 0x08000000
   - Dimensione: dipende dal chip (controlla il datasheet)
   - Il Flipper salva il dump su SD card

5. **Verifica del dump**
   - Il file deve iniziare con il vettore di reset (primi 4 byte = indirizzo dello stack pointer iniziale)
   - Un dump valido di STM32 ha i primi 4 byte che puntano alla fine della RAM (es. 0x20005000)
   - I secondi 4 byte puntano al reset handler nella flash (es. 0x080001xx)
   - Se il dump e tutto 0x00 o tutto 0xFF, qualcosa e andato storto

### Dump firmware -- Procedura per nRF52

I chip Nordic nRF52 sono onnipresenti nei dispositivi BLE: fitness tracker, sensori, beacon, serrature smart.

1. **Pinout SWD nRF52**
   - SWDIO e SWCLK sono sempre disponibili
   - Pin di reset opzionale (utile se il chip e in sleep profondo)

2. **Mappa memoria nRF52832:**
   ```
   0x00000000 - 0x0007FFFF  Flash (512 KB)
   0x10001000 - 0x100010FF  UICR (configurazione)
   0x20000000 - 0x2000FFFF  RAM (64 KB)
   ```

3. **Dump completo:**
   - Flash: 512 KB da 0x00000000
   - UICR: 256 byte da 0x10001000 (contiene configurazione BLE, chiavi, parametri)

4. **Struttura tipica della flash nRF52:**
   ```
   0x00000000 - 0x00000FFF  MBR (Master Boot Record)
   0x00001000 - 0x00025FFF  SoftDevice (stack BLE Nordic)
   0x00026000 - 0x0007BFFF  Application firmware
   0x0007C000 - 0x0007FFFF  Bootloader
   ```

5. **Analisi post-dump:**
   - Il SoftDevice e firmware Nordic proprietario (non molto interessante)
   - L'application firmware contiene la logica del dispositivo
   - Il bootloader puo contenere chiavi DFU (Device Firmware Update)
   - Cerca nell'UICR le chiavi BLE e i parametri di configurazione

> Nota personale: i dispositivi BLE basati su nRF52 sono i piu divertenti da analizzare. Il firmware applicativo e spesso piccolo (50-100 KB), il che rende il reverse engineering con Ghidra molto piu gestibile rispetto a firmware Linux da 16 MB. In piu, i Nordic SDK lasciano molti simboli di debug nel firmware, il che facilita enormemente la comprensione del codice.

---

## 3. DAP Link

### CMSIS-DAP -- Lo standard industriale per il debug ARM

DAP Link (Debug Access Port Link) implementa lo standard CMSIS-DAP (Cortex Microcontroller Software Interface Standard - Debug Access Port). E un protocollo standardizzato da ARM che definisce come un debugger hardware comunica con il software di debug sul PC.

Il Flipper Zero, quando opera in modalita DAP Link, si presenta al PC come un dispositivo USB CMSIS-DAP compatibile. Questo significa che puoi usarlo con qualsiasi tool che supporti questo standard:

- **OpenOCD** (Open On-Chip Debugger)
- **pyOCD** (Python On-Chip Debugger)
- **Keil uVision**
- **PlatformIO / VSCode**
- **IAR Embedded Workbench**

### Differenza tra SWD Probe e DAP Link

| Aspetto | SWD Probe | DAP Link |
|---------|-----------|----------|
| Interfaccia | Standalone (display Flipper) | USB verso PC |
| Controllo | Dal Flipper direttamente | Da software sul PC |
| Funzionalita | Dump, flash base | Debug completo, step-through |
| Breakpoint | Limitati | Completi (hardware + software) |
| Memory watch | Lettura manuale | Real-time continuo |
| Adatto per | Field assessment | Analisi approfondita in lab |

In pratica: la SWD Probe e per il lavoro rapido sul campo. DAP Link e per quando torni in laboratorio e vuoi fare debug serio con tutti gli strumenti.

### Setup con OpenOCD

OpenOCD e il tool open source piu usato per il debug embedded. Configurazione per usare il Flipper come probe:

**Installazione:**
```bash
# Debian/Ubuntu/Kali
sudo apt install openocd

# macOS
brew install openocd

# Arch Linux
sudo pacman -S openocd
```

**File di configurazione per Flipper Zero DAP Link:**

Crea un file `flipper-dap.cfg`:
```
# Interfaccia CMSIS-DAP (Flipper Zero)
adapter driver cmsis-dap

# Velocita SWD (in kHz) -- inizia basso, aumenta se stabile
adapter speed 4000

# Trasporto SWD
transport select swd
```

**Connessione a un target STM32F103:**
```bash
openocd -f flipper-dap.cfg -f target/stm32f1x.cfg
```

Output atteso:
```
Open On-Chip Debugger 0.12.0
Info : CMSIS-DAP: SWD supported
Info : CMSIS-DAP: FW Version = Flipper Zero DAP v1
Info : SWCLK/TCK = 1 SWDIO/TMS = 1
Info : cmsis-dap: SWD IDCODE = 0x1ba01477
Info : stm32f1x.cpu: Cortex-M3 r1p1 processor detected
Info : stm32f1x.cpu: target has 6 breakpoints, 4 watchpoints
```

**Comandi OpenOCD essenziali per il pentest:**

```bash
# Connessione telnet a OpenOCD (porta 4444 di default)
telnet localhost 4444

# Halt della CPU
> halt

# Dump flash su file
> flash read_image firmware.bin 0x08000000 0x20000

# Dump RAM
> dump_image ram.bin 0x20000000 0x5000

# Lettura singolo registro
> reg r0
> reg pc
> reg sp

# Lettura memoria (32 bit)
> mdw 0x08000000 16

# Scrittura memoria
> mww 0x20000000 0xDEADBEEF

# Lettura readout protection
> stm32f1x options_read 0

# Reset del target
> reset halt
> reset run

# Flash di nuovo firmware
> program nuovo_firmware.bin 0x08000000 verify reset
```

### Setup con pyOCD

pyOCD e un'alternativa Python-native a OpenOCD, piu semplice da usare per operazioni rapide:

```bash
# Installazione
pip install pyocd

# Lista probe connesse
pyocd list

# Connessione e shell interattiva
pyocd commander --target stm32f103rc --probe cmsis-dap

# Comandi nella shell pyOCD
>>> halt
>>> read32 0x08000000
>>> read8 0x08000000 256
>>> savefile firmware.bin 0x08000000 0x20000
>>> reg
>>> resume
```

### Debug live -- Step-through con GDB

Il debug step-by-step e fondamentale quando vuoi capire il comportamento del firmware in tempo reale:

**Avvio GDB server via OpenOCD:**
```bash
# OpenOCD espone un GDB server sulla porta 3333
openocd -f flipper-dap.cfg -f target/stm32f1x.cfg
```

**Connessione con GDB:**
```bash
# Usa arm-none-eabi-gdb o gdb-multiarch
arm-none-eabi-gdb firmware.elf

# Dentro GDB
(gdb) target remote localhost:3333
(gdb) monitor reset halt
(gdb) break main
(gdb) continue
(gdb) step
(gdb) next
(gdb) info registers
(gdb) x/16xw 0x08000000
(gdb) print variable_name
```

Se non hai il file ELF con i simboli (caso tipico nel pentest -- stai analizzando firmware estratto), puoi comunque usare GDB per il debug a livello assembly:

```bash
gdb-multiarch

(gdb) target remote localhost:3333
(gdb) set architecture arm
(gdb) monitor reset halt
(gdb) x/20i $pc          # Disassembla da program counter
(gdb) si                  # Step instruction (singola istruzione)
(gdb) ni                  # Next instruction (salta chiamate)
(gdb) break *0x08001234   # Breakpoint su indirizzo specifico
(gdb) watch *0x20000100   # Watchpoint su indirizzo in RAM
```

### Integrazione con PlatformIO / VSCode

Per chi preferisce un IDE grafico:

1. Installa PlatformIO in VSCode
2. Nel file `platformio.ini`:
   ```ini
   [env:debug]
   platform = ststm32
   board = genericSTM32F103RC
   debug_tool = cmsis-dap
   upload_protocol = cmsis-dap
   debug_speed = 4000
   ```
3. Collega il Flipper in modalita DAP Link
4. F5 per avviare il debug con breakpoint grafici, memory view, register view

> Nota personale: la combo Flipper Zero DAP Link + VSCode + PlatformIO e il setup che uso piu spesso in lab. E veloce da configurare, il debug grafico rende molto piu facile seguire il flusso del firmware, e il memory view in tempo reale e impagabile per capire cosa fa il codice. Per il campo, uso la SWD Probe standalone. Per l'analisi seria, DAP Link sempre.

---

