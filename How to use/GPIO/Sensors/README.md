# SENSORS

Suite di strumenti dedicati alla lettura, calibrazione e diagnostica di sensori esterni collegati al dispositivo tramite GPIO, I2C, UART, SPI e linee analogiche.

Il Flipper Zero, tramite il suo header GPIO a 18 pin (3.3V logic level, 5V tolerant su alcuni pin con level shifter esterno), puo interfacciarsi con una vastissima gamma di sensori. Il bus I2C utilizza i pin 15 (SCL) e 16 (SDA) con pull-up interni, la UART e disponibile sui pin 13 (TX) e 14 (RX), mentre SPI sfrutta i pin 2 (SCK), 3 (MISO), 4 (MOSI) e 5 (CS). L'ADC (pin C3) consente letture analogiche a 12 bit (0-4095 su 0-3.3V).

---

### **• Lightmeter**

Misura l'intensita luminosa ambientale in lux, utilizzando fotosensori digitali ad alta precisione collegati via I2C.

**Sensori supportati e specifiche tecniche:**

| Sensore | Protocollo | Indirizzo I2C | Range | Risoluzione | Precisione |
|---------|-----------|---------------|-------|-------------|------------|
| BH1750 | I2C | 0x23 / 0x5C | 1-65535 lux | 1 lux (high-res: 0.5 lux) | +/- 20% | 
| VEML7700 | I2C | 0x10 | 0-120000 lux | 0.0036 lux | +/- 10% tipica |
| TSL2561 | I2C | 0x29 / 0x39 / 0x49 | 0.1-40000 lux | 16 bit ADC | +/- 40% (senza calibrazione) |
| TSL2591 | I2C | 0x29 | 188 ulux - 88000 lux | 600M:1 dynamic range | molto alta con doppio fotodiodo |

**Pinout tipico:** VCC (3.3V pin 9), GND (pin 8/11/18), SDA (pin 15), SCL (pin 16). Il BH1750 ha l'ADDR pin che determina l'indirizzo: LOW = 0x23, HIGH = 0x5C.

**Firmware/librerie:** L'app utilizza il driver I2C del firmware Flipper (furi_hal_i2c). Il BH1750 richiede un comando di accensione (0x01) seguito dalla modalita di misurazione (0x10 per continuous high-res). Il VEML7700 necessita configurazione del registro ALS_CONF (0x00) per gain e integration time.

**Uso in pentest:** Un lightmeter puo sembrare banale, ma in contesti di physical security assessment e utile per valutare zone d'ombra in aree sorvegliate da telecamere (le telecamere IR hanno soglie di lux sotto le quali passano a modalita notturna, tipicamente sotto 1-10 lux). Conoscere il livello di illuminazione di un corridoio o di un parcheggio ti permette di capire se le telecamere stanno operando in condizioni ottimali o degradate.

---

### **• Dist.Sensor**

Lettura di sensori di distanza a ultrasuoni, infrarossi o Time-of-Flight collegati via GPIO digitale, analogico o I2C.

**Sensori supportati e specifiche tecniche:**

| Sensore | Protocollo | Indirizzo/Pin | Range | Precisione | Note |
|---------|-----------|--------------|-------|------------|------|
| HC-SR04 | GPIO (Trigger/Echo) | Trigger: qualsiasi GPIO out, Echo: qualsiasi GPIO in | 2 cm - 4 m | +/- 3 mm | Richiede 5V (usare level shifter o versione 3.3V HC-SR04P) |
| VL53L0X | I2C | 0x29 (default, riprogrammabile) | 30 mm - 2 m | +/- 3% | ToF laser 940nm classe 1 |
| VL6180X | I2C | 0x29 (default) | 0 - 200 mm | +/- 1 mm | ToF corto raggio + sensore ALS integrato |
| GP2Y0A21YK0F | Analogico (ADC) | Pin C3 (ADC) | 10 - 80 cm | +/- 5% a 30cm | Uscita analogica 0.4-3.1V, curva non lineare (necessita lookup table) |

**Pinout HC-SR04:** VCC (5V esterno o pin 1), Trig (es. pin 2), Echo (es. pin 3 con voltage divider 5V->3.3V), GND. Il firmware invia un impulso di 10us su Trigger e misura la durata dell'impulso Echo. Distanza = (tempo_echo * 343 m/s) / 2.

**Pinout VL53L0X/VL6180X:** VCC (3.3V pin 9), GND (pin 18), SDA (pin 15), SCL (pin 16), XSHUT (opzionale, per multi-sensore su stesso bus). Per usare piu VL53L0X sullo stesso bus I2C, si tiene XSHUT basso su tutti tranne uno, si riprogramma l'indirizzo, poi si abilita il successivo.

**Uso in pentest:** I sensori di distanza sono strumenti di ricognizione fisica sottovalutati. Con un VL53L0X puoi mappare rapidamente la geometria di un ambiente durante un physical penetration test: misurare la profondita di cavedi, la distanza tra sensori di allarme a infrarosso passivo (PIR) e le pareti, o verificare se un sensore volumetrico ha zone cieche. Ho usato l'HC-SR04 per stimare la distanza di sensori a tenda montati su finestre durante un assessment di un edificio: sapere che il sensore copre fino a 3 metri dalla finestra ti permette di pianificare l'approccio.

---

### **• Geiger Counter**

Interfaccia per tubi Geiger-Muller compatibili, con visualizzazione CPM (counts per minute), uSv/h (micro-Sievert/ora) e grafici temporali.

**Sensori supportati e specifiche tecniche:**

| Tubo | Tensione operativa | Sensibilita | Tipo radiazione | Dead time |
|------|-------------------|-------------|-----------------|-----------|
| SBM-20 | 400V | ~78 cps/mR/h (Co-60) | Beta, Gamma | ~190 us |
| J305B | 380-450V | ~25 cps/mR/h | Beta, Gamma | ~100 us |
| SI-3BG | 380-460V | ~21 cps/mR/h | Beta, Gamma | ~200 us |
| STS-5 | 390V | ~78 cps/mR/h | Beta, Gamma (similare SBM-20) | ~190 us |

**Collegamento:** Il modulo Geiger esterno genera impulsi TTL (3.3V o 5V) ogni volta che viene rilevata una particella ionizzante. L'uscita digitale va collegata a un pin GPIO di input del Flipper. Il firmware conta gli impulsi in una finestra temporale e calcola CPM e dose equivalente usando il fattore di conversione specifico del tubo (es. SBM-20: 1 CPM ~ 0.0057 uSv/h).

**Circuito tipico:** Il tubo GM necessita di un alimentatore ad alta tensione (350-500V DC) generato da un convertitore boost (tipicamente basato su NE555 o circuito a trasformatore). Moduli pronti all'uso come il RadiationD-v1.1 o il kit di tipo "DIY Geiger" includono tutto il necessario e forniscono un'uscita TTL pulita.

**Uso in pentest:** In scenari CBRN (Chemical, Biological, Radiological, Nuclear) assessment, un Geiger portatile e essenziale. Piu realisticamente, durante physical pentest di strutture critiche (ospedali con reparti di radioterapia, centri di ricerca nucleare, impianti industriali con sorgenti di calibrazione), avere un rilevatore di radiazioni integrato nel Flipper e utile per documentare livelli di background radiation e verificare la conformita delle zone classificate. Ho portato il Geiger durante un assessment di un ospedale: il background era ~0.12 uSv/h nei corridoi e saliva a ~0.3 uSv/h vicino al reparto di medicina nucleare, tutto nella norma ma utile da documentare.

---

### **• CO2 Sensor**

Misura la concentrazione di anidride carbonica in parti per milione (ppm) tramite sensori NDIR (Non-Dispersive Infrared).

**Sensori supportati e specifiche tecniche:**

| Sensore | Protocollo | Range | Precisione | Warm-up | Calibrazione |
|---------|-----------|-------|------------|---------|-------------|
| MH-Z19B | UART (9600 baud, 8N1) | 0-5000 ppm | +/- 50 ppm + 5% lettura | 3 min | Auto-calibrazione (ABC) ogni 24h, manuale con comando 0x87 |
| MH-Z19C | UART (9600 baud, 8N1) | 0-5000 ppm | +/- 50 ppm + 5% | 1 min | Come B, migliorata |
| SenseAir S8 | UART (9600 baud) / Modbus | 400-2000 ppm (LP) / 400-10000 (standard) | +/- 40 ppm + 3% | 2 min | ABC, calibrazione background |

**Pinout MH-Z19B/C:** VIN (5V), GND, TX (-> Flipper RX pin 14), RX (<- Flipper TX pin 13). Il protocollo e un frame di 9 byte: 0xFF (start), 0x01 (sensor #), comando, dati (5 byte), checksum. Per leggere la concentrazione si invia il comando 0x86 e si riceve il valore nei byte 2-3 della risposta (high byte * 256 + low byte = ppm).

**Uso in pentest:** Il livello di CO2 e un indicatore indiretto dell'occupazione di un ambiente. In un ufficio vuoto il CO2 e ~400-500 ppm (livello esterno). Con persone presenti sale rapidamente: 800-1000 ppm con 3-5 persone in una stanza media. Durante attivita di ricognizione, misurare il CO2 fuori da una porta chiusa puo dare indicazioni su quante persone si trovano all'interno senza dover aprire o utilizzare metodi invasivi. E un metodo di OSINT fisico poco noto ma efficace.

---

### **• Accelerometer**

Rileva accelerazione lineare, vibrazioni, inclinazione e orientamento tramite sensori MEMS a 3 assi collegati via I2C o SPI.

**Sensori supportati e specifiche tecniche:**

| Sensore | Protocollo | Indirizzo I2C | Range | Risoluzione | ODR max | Extra |
|---------|-----------|---------------|-------|-------------|---------|-------|
| ADXL345 | I2C / SPI | 0x53 (SDO LOW) / 0x1D (SDO HIGH) | +/- 2/4/8/16 g | 13 bit (fino a 4 mg/LSB a +/-2g) | 3200 Hz | Tap detection, free-fall, activity/inactivity |
| MMA8452Q | I2C | 0x1C (SA0 LOW) / 0x1D (SA0 HIGH) | +/- 2/4/8 g | 12 bit | 800 Hz | Landscape/portrait detection |
| MPU6050 | I2C | 0x68 (AD0 LOW) / 0x69 (AD0 HIGH) | +/- 2/4/8/16 g (acc), +/- 250/500/1000/2000 dps (gyro) | 16 bit | 1 kHz (acc), 8 kHz (gyro) | Accelerometro + giroscopio 6-DOF, DMP integrato |

**Pinout:** VCC (3.3V pin 9), GND (pin 18), SDA (pin 15), SCL (pin 16), INT1/INT2 (opzionale, qualsiasi GPIO per interrupt). L'MPU6050 ha anche un pin XDA/XCL per collegare un magnetometro esterno (es. HMC5883L) come slave I2C.

**Registri chiave ADXL345:** POWER_CTL (0x2D) per uscire dallo standby (bit 3 = 1), DATA_FORMAT (0x31) per range e risoluzione, DATAX0-DATAZ1 (0x32-0x37) per i 6 byte dei dati XYZ.

**Uso in pentest:** Un accelerometro collegato al Flipper puo funzionare come rilevatore di manomissione. Posizionato su una porta, un cassetto o un contenitore, registra qualsiasi apertura o movimento. Durante un physical pentest ho usato l'ADXL345 come "tripwire digitale": lasciato su un armadio rack del server room, registrava i timestamp di ogni vibrazione significativa (soglia impostata a 0.5g), permettendomi di sapere se qualcuno aveva aperto il rack durante la notte. L'MPU6050, con il giroscopio integrato, e ancora piu preciso per rilevare rotazioni (come l'apertura di una porta).

---

### **• Monitor Sensor**

Dashboard universale per visualizzare in tempo reale i dati di piu sensori collegati simultaneamente al bus I2C o a pin GPIO/analogici.

**Sensori supportati e specifiche tecniche:**

| Sensore | Protocollo | Indirizzo I2C | Misure | Precisione |
|---------|-----------|---------------|--------|------------|
| BME280 | I2C / SPI | 0x76 (SDO LOW) / 0x77 (SDO HIGH) | Temperatura (-40/+85C), Umidita (0-100% RH), Pressione (300-1100 hPa) | T: +/-1C, H: +/-3%, P: +/-1 hPa |
| DHT22 / AM2302 | 1-Wire proprietario | N/A (pin digitale) | Temperatura (-40/+80C), Umidita (0-100% RH) | T: +/-0.5C, H: +/-2% |
| MQ-135 | Analogico | N/A (pin ADC) | NH3, NOx, Alcol, Benzene, Fumo, CO2 | Qualitativa (necessita calibrazione) |
| BH1750 | I2C | 0x23 / 0x5C | Illuminamento (1-65535 lux) | +/-20% |

**Note sul BME280:** E il sensore ambientale piu versatile per il Flipper. Utilizza oversampling configurabile (x1, x2, x4, x8, x16) per bilanciare precisione e consumo. In modalita "weather monitoring" (1 sample/min, oversampling x1) consuma solo 0.16 uA. I registri dati sono 0xF7-0xFE (8 byte: pressione 20bit, temperatura 20bit, umidita 16bit) con compensazione tramite coefficienti di calibrazione in ROM.

**Note sul DHT22:** Usa un protocollo 1-Wire proprietario (non compatibile con il 1-Wire di Dallas/Maxim). Il Flipper invia un pull-down di 1-10ms come start signal, poi il sensore risponde con 40 bit (16 umidita + 16 temperatura + 8 checksum). Il timing e critico: ogni bit e codificato dalla durata del segnale HIGH (26-28us = 0, 70us = 1).

**Uso in pentest:** Una dashboard ambientale e utile durante site survey prolungati. Monitorare temperatura e umidita di una server room durante un assessment puo rivelare problemi infrastrutturali (HVAC malfunzionante, zone con temperature anomale che indicano concentrazione di calore da apparati). L'MQ-135 collegato all'ADC puo rilevare la presenza di fumo, utile come allarme improvvisato se stai lavorando in un'area tecnica.

---

### **• Read Scan**

Scanner del bus I2C che rileva automaticamente tutti i dispositivi collegati, elencando gli indirizzi che rispondono con ACK.

**Dettagli tecnici:** L'app invia un byte di start condition + indirizzo (7 bit) + bit R/W su tutte le 128 possibili combinazioni di indirizzi I2C (0x00-0x7F, escludendo gli indirizzi riservati 0x00-0x07 e 0x78-0x7F). Se un dispositivo risponde con ACK, il suo indirizzo viene mostrato a schermo.

Questo e l'equivalente di un "port scan" per il bus I2C: ti dice immediatamente quali sensori sono presenti e funzionanti senza dover conoscere a priori il loro indirizzo. Utilissimo per il debug: se hai collegato un BME280 e non risponde, un Read Scan ti dice subito se il problema e nel cablaggio (nessun indirizzo trovato), nell'indirizzo sbagliato (risponde su 0x77 invece di 0x76) o in un conflitto (due dispositivi sullo stesso indirizzo).

**Uso in pentest:** Se durante un hardware pentest trovi un dispositivo con un connettore I2C esposto (header di debug, porta di manutenzione), un Read Scan e il primo passo per capire cosa c'e collegato al bus. E l'equivalente di un nmap per hardware: scopri i "servizi" attivi. Da li puoi tentare di leggere registri specifici per identificare il chip (molti hanno un registro WHO_AM_I con un ID univoco).

---

### **• Sleep Counter**

Monitoraggio dei dati legati al sonno e al movimento tramite sensori MEMS e ambientali, con logging su SD card.

**Sensori utilizzati:**
- **ADXL345** (movimento): configurato in modalita low-power con soglia di attivita bassa (~62.5 mg), rileva micro-movimenti durante il sonno. Il registro THRESH_ACT (0x24) imposta la soglia, ACT_INACT_CTL (0x27) abilita il rilevamento su assi specifici.
- **BME280** (ambiente): registra temperatura e umidita durante la notte per correlare la qualita del sonno con le condizioni ambientali.

**Funzionamento:** L'app campiona l'accelerometro a bassa frequenza (es. 12.5 Hz in low-power mode, consumo ~23 uA) e conta gli eventi di "attivita" (superamento soglia) in intervalli di 5-10 minuti. Piu eventi = sonno agitato. I dati ambientali vengono campionati ogni minuto. Tutto viene loggato su SD card in formato CSV per analisi successiva.

**Uso in pentest:** Marginale, ma il concetto di activity detection e trasferibile: lo stesso setup puo essere usato come sistema di sorveglianza passiva a bassissimo consumo per monitorare l'accesso a un'area durante un assessment notturno.

---

### **• Atomic Dice Roller**

Generatore di numeri casuali basato su rumore fisico dei sensori, che fornisce entropia hardware reale (non pseudo-random).

**Sorgenti di entropia:**
- **Fotoresistenza LDR (GL5528):** collegata al pin ADC (C3) con un resistore pull-down (10k). Le fluttuazioni di luce ambientale generano rumore analogico. La resistenza varia da ~1k ohm (luce forte) a ~1M ohm (buio). Il rumore LSB dell'ADC a 12 bit (~1-2 LSB) combinato con le microfluttuazioni luminose fornisce entropia.
- **Accelerometro ADXL345:** il rumore termico del sensore MEMS (~1.1 LSB RMS a 100 Hz, +/-2g range) sui 3 assi fornisce ulteriore entropia. Anche con il sensore fermo, i bit meno significativi variano casualmente.

**Algoritmo:** L'app campiona ripetutamente le sorgenti, prende i bit LSB (1-2 bit per campione), li accumula in un buffer e applica un hash (o semplice XOR mixing) per generare un valore nel range del dado selezionato (D4, D6, D8, D10, D12, D20). La qualita dell'entropia e sufficiente per giochi ma non per applicazioni crittografiche senza ulteriore conditioning (es. Von Neumann debiasing).

---

### **• Gas Sensor**

Interfaccia per sensori di gas della famiglia MQ-series, che utilizzano un elemento riscaldante a ossido di stagno (SnO2) la cui resistenza varia in presenza di gas specifici.

**Sensori supportati e specifiche tecniche:**

| Sensore | Gas target primario | Range rilevamento | Tensione riscaldatore | Tempo preriscaldamento |
|---------|-------------------|-------------------|----------------------|----------------------|
| MQ-2 | GPL, Propano, Metano, Fumo | 300-10000 ppm | 5V (consuma ~150mA!) | >24h per calibrazione stabile |
| MQ-4 | Metano, Gas naturale | 300-10000 ppm | 5V | >24h |
| MQ-7 | Monossido di carbonio (CO) | 20-2000 ppm | 5V (ciclo 1.4V/5V) | >48h |
| MQ-9 | CO + Gas combustibili | CO: 10-1000 ppm, Gas: 100-10000 ppm | 5V (ciclo) | >24h |
| MQ-135 | NH3, NOx, Alcol, Benzene, Fumo | 10-1000 ppm (varia per gas) | 5V | >24h |

**Collegamento:** I sensori MQ hanno 4 pin (VCC, GND, DOUT digitale con comparatore, AOUT analogico). Per letture quantitative si usa AOUT collegato al pin ADC del Flipper (C3) con un voltage divider se necessario (l'uscita puo arrivare a 5V). ATTENZIONE: i sensori MQ consumano parecchia corrente (150-180mA) per il riscaldatore, quindi necessitano alimentazione esterna (non dal 3.3V del Flipper).

**Formula di conversione:** La resistenza del sensore Rs si calcola come: Rs = ((Vcc * RL) / Vout) - RL, dove RL e il resistore di carico (tipicamente 10-47k ohm). Il rapporto Rs/R0 (R0 = resistenza in aria pulita dopo calibrazione) viene usato con le curve caratteristiche del datasheet per ottenere la concentrazione in ppm.

**Uso in pentest:** In scenari di physical security assessment di strutture industriali o chimiche, avere un rilevatore di gas portatile e una misura di sicurezza personale. Prima di entrare in un cavedio, un sottotetto o un locale tecnico, una lettura rapida con MQ-2 (gas combustibili) o MQ-7 (CO) puo salvare la vita. Non e paranoico: ho lavorato in strutture dove i locali tecnici avevano perdite di gas note e "tollerate". Un MQ-2 collegato al Flipper mi ha dato un warning a ~800 ppm di metano in un locale caldaia (la soglia LEL per il metano e ~50000 ppm, quindi non c'era pericolo immediato, ma la perdita c'era).

---

### **• MAX31855**

Lettura di termocoppie tipo K tramite il convertitore digitale MAX31855, che fornisce temperatura con risoluzione di 0.25C su un range esteso.

**Specifiche tecniche:**
- **Protocollo:** SPI (read-only, nessun MOSI necessario)
- **Pinout:** VCC (3.3V pin 9), GND (pin 18), SCK (pin 2), CS (pin 5), DO/MISO (pin 3)
- **Range:** -200C a +1350C (termocoppia tipo K), con cold junction compensation interna (-40C a +125C)
- **Risoluzione:** 0.25C (termocoppia), 0.0625C (cold junction)
- **Precisione:** +/-2C (range 0-1000C), +/-4C ai limiti
- **Data format:** 32 bit SPI frame: D[31:18] = 14 bit temperatura termocoppia (signed), D[17] = riservato, D[16] = fault bit, D[15:4] = 12 bit temperatura interna, D[3] = riservato, D[2] = SCV (short to VCC), D[1] = SCG (short to GND), D[0] = OC (open circuit)

**Uso pratico:** Essenziale per misurazioni in contesti dove i sensori digitali standard non arrivano: verificare la temperatura di un processore sotto carico durante hardware reverse engineering, misurare la temperatura di un motore o di un componente di potenza, o monitorare processi di saldatura.

---

### **• MH-Z19 UART**

Supporto dedicato per i sensori CO2 MH-Z19B e MH-Z19C con comunicazione UART e funzionalita avanzate di calibrazione.

**Protocollo UART dettagliato:**
- Baud rate: 9600, 8 bit, no parity, 1 stop bit (8N1)
- Frame di comando (9 byte): `[0xFF] [0x01] [CMD] [0x00] [0x00] [0x00] [0x00] [0x00] [CHECKSUM]`
- Checksum: negazione della somma dei byte 1-7 + 1 (complemento a 2)
- Comando lettura CO2: CMD = 0x86
- Risposta (9 byte): `[0xFF] [0x86] [CO2_HIGH] [CO2_LOW] [TEMP] [STATUS] [0x00] [0x00] [CHECKSUM]`
- CO2 ppm = CO2_HIGH * 256 + CO2_LOW
- Temperatura = TEMP - 40 (gradi Celsius, approssimativa)

**Comandi utili:**
| Comando | Byte CMD | Descrizione |
|---------|---------|-------------|
| Read CO2 | 0x86 | Legge concentrazione CO2 |
| Calibrate Zero | 0x87 | Calibrazione zero point (400 ppm in aria aperta) |
| Calibrate Span | 0x88 | Calibrazione span point (con gas di riferimento) |
| ABC On/Off | 0x79 | Abilita/disabilita auto-calibrazione (byte 3: 0xA0=on, 0x00=off) |
| Set Range | 0x99 | Imposta range (byte 3-4 per valore: 0x13 0x88 = 5000 ppm) |

**Nota sulla calibrazione ABC:** L'Automatic Baseline Correction assume che il livello piu basso di CO2 misurato nelle ultime 24h sia ~400 ppm (livello atmosferico). In ambienti sempre occupati questo puo causare drift. In questi casi, disabilitare ABC e calibrare manualmente portando il sensore all'esterno.

---

### **• Plantower PMSx003**

Lettura di sensori di particolato fine della serie Plantower, che utilizzano diffusione laser per contare e dimensionare le particelle sospese nell'aria.

**Sensori supportati:**

| Sensore | Dimensioni | Range PM | Dati output | Baud rate |
|---------|-----------|---------|------------|-----------|
| PMS3003 | 65x42x23 mm | PM1.0, PM2.5, PM10 | 24 byte frame | 9600 |
| PMS5003 | 50x38x21 mm | PM1.0, PM2.5, PM10 + conteggio particelle | 32 byte frame | 9600 |
| PMS7003 | 48x37x12 mm | Come PMS5003, piu compatto | 32 byte frame | 9600 |

**Protocollo UART (PMS5003/7003):**
- Frame 32 byte: `[0x42] [0x4D] [Frame Length High] [Frame Length Low] [Data 1-13] [Checksum High] [Checksum Low]`
- Data 1-2: PM1.0 standard (ug/m3)
- Data 3-4: PM2.5 standard (ug/m3)
- Data 5-6: PM10 standard (ug/m3)
- Data 7-8: PM1.0 ambientale (ug/m3)
- Data 9-10: PM2.5 ambientale (ug/m3)
- Data 11-12: PM10 ambientale (ug/m3)
- Data 13-18: Conteggio particelle >0.3um, >0.5um, >1.0um, >2.5um, >5.0um, >10um (per 0.1L di aria)

**Pinout:** VCC (5V), GND, TX (-> Flipper RX pin 14), RX (<- Flipper TX pin 13), SET (opzionale, pin digitale per sleep mode), RESET (opzionale).

**Uso in pentest:** Il PM2.5 e un indicatore della qualita dell'aria che puo rivelare la presenza di attivita industriali nascoste, sistemi HVAC malfunzionanti, o aree con polvere eccessiva (rilevante per la sicurezza delle apparecchiature in data center, dove le norme ASHRAE raccomandano PM10 < 15 ug/m3).

---

### **• Radiation Sensor**

Supporto per moduli di rilevamento radiazioni alternativi ai tubi Geiger classici, inclusi rilevatori a stato solido e moduli digitali con output TTL.

**Sensori supportati:**

| Sensore | Tipo | Output | Sensibilita | Note |
|---------|------|--------|-------------|------|
| Geiger digitali TTL | Tubo GM con elettronica integrata | Impulsi TTL (3.3/5V) | Dipende dal tubo | Moduli pronti all'uso (RadSens, RadiationD) |
| LND 712 | Tubo GM halogen-quenched | Impulsi (necessita elettronica) | ~18 cps/mR/h (Cs-137) | Sensibile a Beta, Gamma, X-ray |

**Differenze con Geiger Counter:** Questa app e progettata per moduli con protocolli di comunicazione piu avanzati rispetto al semplice conteggio impulsi. Alcuni moduli (es. RadSens basato su CTC-5/SBM-20 con microcontrollore) comunicano via I2C e forniscono direttamente valori elaborati (uSv/h, CPM, dati statistici). L'indirizzo I2C del RadSens e 0x66 di default.

---

### **• Temp Sensor Reader**

Compatibilita con una vasta gamma di termometri digitali che utilizzano protocolli diversi: 1-Wire, I2C e analogico.

**Sensori supportati e specifiche tecniche:**

| Sensore | Protocollo | Indirizzo/Pin | Range | Risoluzione | Precisione |
|---------|-----------|--------------|-------|-------------|------------|
| DS18B20 | 1-Wire (Dallas) | Qualsiasi GPIO + pull-up 4.7k | -55C a +125C | 9-12 bit configurabile (0.5C - 0.0625C) | +/-0.5C (range -10/+85C) |
| TMP117 | I2C | 0x48/0x49/0x4A/0x4B | -55C a +150C | 0.0078C (16 bit) | +/-0.1C (range -20/+50C) |
| LM75 | I2C | 0x48-0x4F (3 bit configurabili) | -55C a +125C | 0.5C (9 bit) | +/-2C |
| TMP102 | I2C | 0x48/0x49/0x4A/0x4B | -40C a +125C | 0.0625C (12 bit) | +/-0.5C (range -25/+85C) |
| NTC 10k | Analogico (ADC) | Pin C3 + voltage divider | -40C a +125C (dipende dalla tabella) | Dipende da ADC (12 bit) | +/-1-2C con calibrazione |

**Protocollo 1-Wire (DS18B20):** Il master (Flipper) invia un reset pulse (pull-down 480us), il DS18B20 risponde con un presence pulse. Segue la comunicazione con comandi ROM (0x33 Read ROM, 0xCC Skip ROM, 0x55 Match ROM) e comandi funzione (0x44 Convert T, 0xBE Read Scratchpad). La conversione a 12 bit richiede ~750ms.

**NTC 10k con equazione di Steinhart-Hart:** Per convertire la lettura ADC in temperatura: R_NTC = R_fixed * (ADC_max / ADC_value - 1), poi 1/T = A + B*ln(R) + C*(ln(R))^3, con coefficienti tipici A=1.009249522e-3, B=2.378405444e-4, C=2.019202697e-7 per un NTC 10k standard.

---

### **• UV Meter**

Misurazione dell'indice UV e della potenza della radiazione ultravioletta tramite sensori dedicati.

**Sensori supportati:**

| Sensore | Protocollo | Indirizzo I2C | Range | Bande | Note |
|---------|-----------|---------------|-------|-------|------|
| VEML6075 | I2C | 0x10 | UV Index 0-15+ | UVA (365nm) + UVB (330nm) | Compensazione IR e luce visibile integrata |
| ML8511 | Analogico | N/A (pin ADC) | 0-15 mW/cm2 | UV (280-390nm) | Output lineare ~0.99V (no UV) a ~2.8V (15 mW/cm2) |

**Calcolo UV Index (VEML6075):** UVA_calc = UVA_raw - a*UVcomp1 - b*UVcomp2, UVB_calc = UVB_raw - c*UVcomp1 - d*UVcomp2, dove UVcomp1 e UVcomp2 sono i canali di compensazione per luce visibile e IR. L'UV Index si calcola come (UVA_calc * UVA_resp + UVB_calc * UVB_resp) / 2, con response factors dal datasheet.

---

### **• VEML7700 Lux Meter**

Misurazione di precisione dell'illuminamento in lux tramite il sensore VEML7700 con amplissimo range dinamico.

**Specifiche tecniche dettagliate:**
- **Protocollo:** I2C, indirizzo fisso 0x10
- **Range:** 0 - 120000 lux
- **Risoluzione minima:** 0.0036 lux (gain x2, integration 800ms)
- **Registri principali:** ALS_CONF (0x00) per configurazione gain/integration time, ALS (0x04) per il valore raw, WHITE (0x05) per il canale bianco, ALS_INT (0x06) per soglie interrupt
- **Gain configurabile:** x1, x2, x1/8, x1/4
- **Integration time:** 25ms, 50ms, 100ms, 200ms, 400ms, 800ms
- **Lux = raw_ALS * resolution_factor** (dipende da gain e integration time, vedi tabella nel datasheet)

**Confronto con BH1750:** Il VEML7700 ha un range dinamico molto superiore (120k lux vs 65k) e risoluzione piu fine, ma e piu complesso da configurare. Per misurazioni rapide il BH1750 e piu immediato.

---

### **• VL6180X Distance Sensor**

Sensore di distanza e prossimita a corto raggio basato su Time-of-Flight, con sensore ALS (Ambient Light Sensor) integrato.

**Specifiche tecniche dettagliate:**
- **Protocollo:** I2C, indirizzo default 0x29 (riprogrammabile via registro 0x0212)
- **Range distanza:** 0 - 200 mm
- **Risoluzione:** ~1 mm
- **Sorgente:** VCSEL laser 850nm (classe 1, eye-safe)
- **Principio ToF:** Il sensore emette un impulso laser, misura il tempo di volo del fotone riflesso con un SPAD (Single Photon Avalanche Diode). Distanza = (c * t) / 2, ma il sensore gestisce tutto internamente e restituisce direttamente il valore in mm.
- **Registri chiave:** RESULT_RANGE_VAL (0x0062) per il valore distanza, RESULT_ALS_VAL (0x0050) per il lux, RESULT_RANGE_STATUS (0x004D) per la validita della misura
- **Cross-talk compensation:** Fondamentale quando si usa con un vetro di copertura. Si calibra il cross-talk posizionando un target a distanza nota e salvando il valore di compensazione nel registro 0x001E.

---

### **• Water Sensor Reader**

Lettura di sensori di umidita del suolo e rilevatori d'acqua tramite input analogico o digitale.

**Sensori supportati:**

| Sensore | Tipo | Output | Principio di funzionamento |
|---------|------|--------|--------------------------|
| Capacitive Soil Moisture v1.2 | Analogico | 0-3V (inversamente proporzionale all'umidita) | Misura la costante dielettrica del suolo tramite capacita (non corrode) |
| YL-69 / YL-38 | Analogico + Digitale | AOUT: 0-5V, DOUT: HIGH/LOW | Misura la resistenza tra due elettrodi (corrode nel tempo) |
| Leak Sensor a contatto | Digitale | HIGH/LOW | Due piste conduttive: l'acqua chiude il circuito |

**Collegamento Capacitive Soil Moisture:** VCC (3.3V o 5V), GND, AOUT -> pin ADC (C3). Il valore tipico e ~520 in aria (asciutto), ~260 in acqua (saturo). Questo sensore e superiore ai resistivi (YL-69) perche non ha elettrodi esposti che si corrodono con l'elettrolisi.

**Uso pratico e in pentest:** Oltre all'ovvio uso in agricoltura smart, un leak sensor puo essere deployato durante un physical assessment per monitorare infiltrazioni d'acqua in sale server o archivi. L'acqua e il nemico numero uno dell'hardware, e un allarme precoce puo prevenire danni a apparecchiature critiche durante un assessment prolungato.

---

## Note generali sull'uso dei sensori in ambito pentest

La sensoristica GPIO del Flipper Zero trasforma il dispositivo da semplice tool di hacking wireless a piattaforma di ricognizione ambientale completa. Durante un physical penetration test o un red team engagement, i dati ambientali forniscono intelligence preziosa:

- **Temperatura/umidita** (BME280): condizioni della server room, conformita ASHRAE
- **CO2** (MH-Z19): occupazione degli ambienti
- **Distanza** (VL53L0X): mappatura spazi, zone cieche dei sensori
- **Gas** (MQ-series): sicurezza personale in locali tecnici
- **Radiazioni** (Geiger): documentazione in strutture con sorgenti radioattive
- **Luce** (BH1750): valutazione condizioni operative delle telecamere CCTV
- **Particolato** (PMS5003): qualita dell'aria in data center

Dalla mia esperienza, i sensori piu utili da portare sempre nello zaino durante un engagement sono il BME280 (compatto, multi-funzione, bassissimo consumo), il VL53L0X (misurazioni rapide e precise) e un MQ-7 per il CO se si lavora in ambienti industriali. Il Flipper Zero come hub centrale per tutti questi sensori elimina la necessita di portare strumenti dedicati separati.
