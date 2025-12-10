# SENSORS

Suite di strumenti dedicati alla lettura, calibrazione e diagnostica di sensori esterni collegati al dispositivo (GPIO, I²C, UART, SPI).

### **• Lightmeter**

Misura l’intensità luminosa ambientale.

Esempio d’uso: valutare condizioni di illuminazione per fotografia o domotica.

Nome sensori: BH1750, VEML7700, TSL2561, TSL2591

### **• Dist.Sensor**

Lettura di sensori di distanza a ultrasuoni o infrarossi (HC‑SR04, VL53L0X ecc.).

Esempio d’uso: testare moduli per robotica o misurazioni rapide.

Nome sensori:
- HC‑SR04 (ultrasuoni)
- VL53L0X, VL6180X (ToF)
- GP2Y0A21YK0F (IR analogico)

### **• Geiger Counter**

Interfaccia per tubi Geiger-Müller compatibili.

Esempio d’uso: monitorare la presenza di radiazioni con grafici e soglie di allarme.

Nome sensori: Tubo SBM‑20, J305B, SI-3BG, STS‑5

### **• CO2 Sensor**

Misura la concentrazione di anidride carbonica.

Esempio d’uso: verifica qualità dell’aria in ambienti chiusi.

Nome sensori:
- MH‑Z19B / MH‑Z19C
- SenseAir S8

### **• Accelerometer**

Rileva accelerazione, vibrazioni e orientamento.

Esempio d’uso: analisi movimento, allarmi anti‑urto o registrazione cadute.

Nome sensori: ADXL345, MMA8452Q, MPU6050 (acc+gyro)

### **• Monitor Sensor**

Dashboard universale per visualizzare più sensori in tempo reale.

Esempio d’uso: controllare simultaneamente temperatura, gas, PM e luminosità.

Nome sensori:
- BME280 (temp/umidità/pressione)
- DHT22 / AM2302
- MQ‑135 (gas)
- BH1750 (luce)

### **• Read Scan**

Letture rapide da sensori multipli.

Esempio d’uso: test immediato per verificare che tutti i moduli rispondano correttamente.

(Note: non è un sensore specifico → scanner I2C (tecnicamente usa un I2C bus scan))
### **• Sleep Counter**

Monitoraggio dei dati legati al sonno tramite sensori di movimento o ambientali.

Esempio d’uso: registrare brevi cicli di riposo durante attività outdoor.

Nome sensore:
- ADXL345 (movimento)
- BME280 (ambiente)

### **• Atomic Dice Roller**

Generatore casuale basato su rumore di sensori.

Esempio d’uso: dadi elettronici affidabili per giochi o test di randomizzazione.

Nome sensori:
- LDR fotoresistenza (es. GL5528)
- accelerometro (ADXL345)

### **• Gas Sensor**

Interfaccia per sensori di gas (MQ‑series, ecc.).

Esempio d’uso: rilevare metano, GPL, fumo o VOC.

Nome sensori: Famiglia MQ‑series: MQ‑2, MQ‑4, MQ‑7, MQ‑9, MQ‑135

### **• MAX31855**

Lettura termocoppie tipo K tramite convertitore digitale.

Esempio d’uso: misurazioni ad alte temperature in ambito tecnico o hobbistico.

### **• MH-Z19 UART**

Supporto per sensori CO₂ MH‑Z19 via UART.

Esempio d’uso: misure affidabili con calibrazione integrata.

Nome sensore: MH‑Z19B / C

### **• Plantower PMSx003**

Lettura sensori di particolato PM1.0/2.5/10.

Esempio d’uso: monitoraggio qualità dell’aria esterna o interna.

Nome sensori: PMS3003, PMS5003, PMS7003

### **• Radiation Sensor**

Supporto a moduli di rilevamento radiazioni alternativi.

Esempio d’uso: comparazione con contatori Geiger o test ambientali.

Nome sensori:
- Geiger digitali TTL
- LND 712 (con elettronica)

### **• Temp Sensor Reader**

Compatibilità con termometri digitali multipli (DS18B20, DHTxx ecc.).

Esempio d’uso: misurazioni di temperatura/umidità in tempo reale.

Nome sensore:
- DS18B20 (1‑Wire)
- TMP117, LM75, TMP102 (I²C)
- NTC 10k (analogici)

### **• UV Meter**

Misurazione dell’indice UV.

Esempio d’uso: valutare esposizione solare per sicurezza o progetti scientifici.

Nome sensori: VEML6075, ML8511

### **• VEML7700 Lux Meter**

Misurazione precisa dei lux tramite sensore VEML7700.

Esempio d’uso: calibrazione di luci LED o test fotografici.

Nome sensore: VEML7700

### **• VL6180X Distance Sensor**

Sensore di distanza e prossimità basato su Time‑of‑Flight.

Esempio d’uso: misurazioni a corto raggio molto precise.

Nome sensore: VL6180X (ToF a corto raggio)

### **• Water Sensor Reader**

Lettura di sensori di umidità del suolo o rilevatori d'acqua.

Esempio d’uso: irrigazione intelligente o rilevamento perdite.

Nome sensori:
- Capacitive Soil Moisture v1.2
- YL‑69 / YL‑38 (analogici)
- Leak Sensor a contatto semplice