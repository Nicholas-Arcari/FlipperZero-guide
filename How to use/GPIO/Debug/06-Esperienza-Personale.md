## 9. Esperienza Personale

### Lezioni apprese sul campo

> Nota personale: dopo centinaia di ore di hardware hacking con il Flipper Zero, ecco le lezioni piu importanti che ho imparato.

#### Sull'approccio generale

> Nota personale: la pazienza e la virtu piu importante nell'hardware hacking. A differenza del software pentest dove puoi iterare rapidamente, con l'hardware ogni errore puo costare un chip bruciato o una PCB danneggiata. Misura due volte, collega una volta. Verifica sempre la tensione prima di collegare qualsiasi cosa.

#### Sugli strumenti

> Nota personale: il Flipper Zero non e il miglior debugger SWD, non e il miglior programmatore SPI, non e il miglior scanner I2C. Ma e l'unico che li ha tutti in un device tascabile. Il mio kit da campo include il Flipper, un set di clip SOIC-8, cavetti jumper, un multimetro tascabile, e un paio di pogopins. Con questo kit entro nella maggior parte dei dispositivi IoT senza problemi.

#### Sulla readout protection

> Nota personale: ho perso il conto di quante volte la readout protection era disabilitata su dispositivi "di sicurezza". Serrature smart, allarmi, telecamere -- la maggior parte ha SWD completamente aperto. I produttori non attivano le protezioni perche complicano la produzione e il debug in garanzia. Questo e un regalo per noi pentester, ma e anche un problema serio per la sicurezza dei consumatori.

#### Sul dump SPI

> Nota personale: investi in una buona clip SOIC-8. Le clip economiche da 2 EUR perdono contatto continuamente e producono dump corrotti. La Pomona 5250 costa 15-20 EUR ma fa contatto perfetto al primo colpo. Nel lungo periodo, risparmi tempo e frustrazione. E fai SEMPRE due dump consecutivi e confrontali -- non esiste dump affidabile senza verifica.

#### Sull'UART

> Nota personale: la UART e la prima cosa che cerco su qualsiasi PCB. E il metodo piu semplice e meno invasivo per ottenere informazioni su un dispositivo. Anche quando non c'e una shell interattiva, i log di boot rivelano versioni firmware, indirizzi di rete, servizi attivi, e a volte credenziali. Ho visto password WiFi stampate nei log di boot di telecamere IP. Letteralmente in chiaro, durante ogni riavvio.

#### Sui fuse bit AVR

> Nota personale: ho brickato il mio primo ATtiny85 a 15 minuti dall'inizio del mio percorso con gli AVR. Avevo disabilitato RSTDISBL pensando di guadagnare un pin GPIO extra, senza sapere che senza pin di reset non puoi piu programmare via ISP. Lezione imparata: leggi il datasheet PRIMA di toccare i fuse bits, e fai SEMPRE un backup dei fuse correnti prima di modificarli.

#### Sulla documentazione

> Nota personale: documenta TUTTO. Ogni pin che identifichi, ogni connessione che fai, ogni dump che estrai. Usa foto con annotazioni, appunti con timestamp, e una naming convention coerente per i file. In un assessment complesso con decine di dispositivi, la documentazione e quello che separa un lavoro professionale da un casino ingestibile.

#### Sul rispetto della legalita

> Nota personale: tutti gli scenari descritti in questa guida sono da eseguire esclusivamente su dispositivi di tua proprieta o con esplicita autorizzazione scritta del proprietario, nell'ambito di attivita di security assessment, ricerca, o apprendimento. L'accesso non autorizzato a sistemi informatici e un reato. La conoscenza delle tecniche di hardware hacking serve per difendere, non per attaccare.

---

## Appendice A -- Riferimenti rapidi

### Pinout GPIO Debug del Flipper Zero

```
Flipper Zero GPIO Header (vista dall'alto, USB a sinistra):

    +--[USB-C]--+
    |           |
 1  | 3V3   GND | 18
 2  | SWC   A7  | 17
 3  | SIO   A6  | 16
 4  | MISO  A4  | 15
 5  | CS    B3  | 14
 6  | SDA   B2  | 13
 7  | SCL   C3  | 12
 8  | GND   C1  | 11
 9  | 3V3   C0  | 10
    |           |
    +-----------+

Legenda:
SWC = SWCLK (Pin 2)
SIO = SWDIO (Pin 3)
```

### Tabella veloce -- Quale tool usare

| Situazione | Tool | Primo passo |
|-----------|------|-------------|
| MCU ARM sconosciuta | SWD Probe | Leggi IDCODE |
| Debug firmware ARM | DAP Link + OpenOCD | Connetti GDB |
| MCU AVR (Arduino) | AVR Flasher | Leggi signature |
| EEPROM sulla PCB | I2C Tools | Scan bus |
| Flash esterna SOIC-8 | SPI Mem Manager | Leggi JEDEC ID |
| Porta Ethernet sospetta | Ethernet Troubleshooter | Check link status |
| Console seriale | UART (GPIO app) | Prova 115200 baud |

### Comandi post-dump essenziali

```bash
# Analisi firmware generico
binwalk firmware.bin
binwalk -e firmware.bin
strings -n 8 firmware.bin > strings.txt
entropy firmware.bin

# Analisi specifiche per Linux embedded
unsquashfs filesystem.squashfs
cat etc/shadow
find . -name "*.conf" -exec grep -l "pass" {} \;

# Analisi AVR
avr-objdump -D -m avr firmware.bin > disasm.asm

# Analisi ARM Cortex-M
arm-none-eabi-objdump -D -b binary -m arm firmware.bin > disasm.asm

# Confronto dump
md5sum dump1.bin dump2.bin
diff <(xxd dump1.bin) <(xxd dump2.bin)
```

### Risorse utili

- Datasheet Winbond W25Qxx: contiene tutte le specifiche SPI flash
- ARM CoreSight Architecture Spec: per capire SWD/JTAG a fondo
- Nordic nRF52832 Product Spec: mappa memoria, UICR, APPROTECT
- Atmel ATmega328P Datasheet: fuse bits, lock bits, ISP protocol
- OpenOCD User Guide: configurazione completa per debug ARM
- Ghidra: disassemblatore gratuito della NSA, supporta ARM e AVR
- binwalk: estrazione e analisi firmware embedded
