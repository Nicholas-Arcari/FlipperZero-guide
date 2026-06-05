# SENSORS

Suite of tools dedicated to reading, calibration, and diagnostics of external sensors connected to the device via GPIO, I2C, UART, SPI, and analog lines.

The Flipper Zero, through its 18-pin GPIO header (3.3V logic level, 5V tolerant on some pins with external level shifter), can interface with a vast range of sensors. The I2C bus uses pins 15 (SCL) and 16 (SDA) with internal pull-ups, UART is available on pins 13 (TX) and 14 (RX), while SPI uses pins 2 (SCK), 3 (MISO), 4 (MOSI), and 5 (CS). The ADC (pin C3) allows 12-bit analog readings (0-4095 over 0-3.3V).

---

### **Lightmeter**

Measures ambient light intensity in lux, using high-precision digital photosensors connected via I2C.

**Supported sensors and technical specifications:**

| Sensor | Protocol | I2C Address | Range | Resolution | Accuracy |
|--------|----------|-------------|-------|------------|----------|
| BH1750 | I2C | 0x23 / 0x5C | 1-65535 lux | 1 lux (high-res: 0.5 lux) | +/- 20% |
| VEML7700 | I2C | 0x10 | 0-120000 lux | 0.0036 lux | +/- 10% typical |
| TSL2561 | I2C | 0x29 / 0x39 / 0x49 | 0.1-40000 lux | 16 bit ADC | +/- 40% (without calibration) |
| TSL2591 | I2C | 0x29 | 188 ulux - 88000 lux | 600M:1 dynamic range | Very high with dual photodiode |

**Typical pinout:** VCC (3.3V pin 9), GND (pin 8/11/18), SDA (pin 15), SCL (pin 16). The BH1750 has an ADDR pin that determines the address: LOW = 0x23, HIGH = 0x5C.

**Firmware/libraries:** The app uses the Flipper firmware I2C driver (furi_hal_i2c). The BH1750 requires a power-on command (0x01) followed by the measurement mode (0x10 for continuous high-res). The VEML7700 needs configuration of the ALS_CONF register (0x00) for gain and integration time.

**Use in pentesting:** A lightmeter might seem trivial, but in physical security assessment contexts it's useful for evaluating shadow zones in areas monitored by cameras (IR cameras have lux thresholds below which they switch to night mode, typically under 1-10 lux). Knowing the illumination level of a corridor or parking lot lets you understand whether the cameras are operating under optimal or degraded conditions.

---

### **Dist.Sensor**

Reading of ultrasonic, infrared, or Time-of-Flight distance sensors connected via digital GPIO, analog, or I2C.

**Supported sensors and technical specifications:**

| Sensor | Protocol | Address/Pin | Range | Accuracy | Notes |
|--------|----------|-------------|-------|----------|-------|
| HC-SR04 | GPIO (Trigger/Echo) | Trigger: any GPIO out, Echo: any GPIO in | 2 cm - 4 m | +/- 3 mm | Requires 5V (use level shifter or 3.3V version HC-SR04P) |
| VL53L0X | I2C | 0x29 (default, reprogrammable) | 30 mm - 2 m | +/- 3% | ToF 940nm class 1 laser |
| VL6180X | I2C | 0x29 (default) | 0 - 200 mm | +/- 1 mm | Short-range ToF + integrated ALS sensor |
| GP2Y0A21YK0F | Analog (ADC) | Pin C3 (ADC) | 10 - 80 cm | +/- 5% at 30cm | Analog output 0.4-3.1V, non-linear curve (requires lookup table) |

**HC-SR04 pinout:** VCC (5V external or pin 1), Trig (e.g., pin 2), Echo (e.g., pin 3 with 5V->3.3V voltage divider), GND. The firmware sends a 10us pulse on Trigger and measures the Echo pulse duration. Distance = (echo_time * 343 m/s) / 2.

**VL53L0X/VL6180X pinout:** VCC (3.3V pin 9), GND (pin 18), SDA (pin 15), SCL (pin 16), XSHUT (optional, for multi-sensor on same bus). To use multiple VL53L0X on the same I2C bus, hold XSHUT low on all except one, reprogram the address, then enable the next.

**Use in pentesting:** Distance sensors are underrated physical reconnaissance tools. With a VL53L0X you can quickly map the geometry of an environment during a physical penetration test: measure the depth of cable trays, the distance between passive infrared (PIR) alarm sensors and walls, or verify if a volumetric sensor has blind spots. I used the HC-SR04 to estimate the distance of curtain sensors mounted on windows during a building assessment: knowing that the sensor covers up to 3 meters from the window lets you plan your approach.

---

### **Geiger Counter**

Interface for compatible Geiger-Muller tubes, with CPM (counts per minute), uSv/h (micro-Sievert/hour) display and time-series graphs.

**Supported sensors and technical specifications:**

| Tube | Operating Voltage | Sensitivity | Radiation Type | Dead Time |
|------|-------------------|-------------|----------------|-----------|
| SBM-20 | 400V | ~78 cps/mR/h (Co-60) | Beta, Gamma | ~190 us |
| J305B | 380-450V | ~25 cps/mR/h | Beta, Gamma | ~100 us |
| SI-3BG | 380-460V | ~21 cps/mR/h | Beta, Gamma | ~200 us |
| STS-5 | 390V | ~78 cps/mR/h | Beta, Gamma (similar to SBM-20) | ~190 us |

**Connection:** The external Geiger module generates TTL (3.3V or 5V) pulses each time an ionizing particle is detected. The digital output goes to a Flipper GPIO input pin. The firmware counts pulses within a time window and calculates CPM and equivalent dose using the tube-specific conversion factor (e.g., SBM-20: 1 CPM ~ 0.0057 uSv/h).

**Typical circuit:** The GM tube requires a high-voltage power supply (350-500V DC) generated by a boost converter (typically based on NE555 or transformer circuit). Ready-to-use modules like the RadiationD-v1.1 or "DIY Geiger" kits include everything needed and provide a clean TTL output.

**Use in pentesting:** In CBRN (Chemical, Biological, Radiological, Nuclear) assessment scenarios, a portable Geiger counter is essential. More realistically, during physical pentests of critical facilities (hospitals with radiotherapy departments, nuclear research centers, industrial plants with calibration sources), having a radiation detector integrated into the Flipper is useful for documenting background radiation levels and verifying compliance of classified zones. I brought the Geiger during a hospital assessment: background was ~0.12 uSv/h in the corridors and rose to ~0.3 uSv/h near the nuclear medicine department, all within normal range but useful to document.

---

### **CO2 Sensor**

Measures carbon dioxide concentration in parts per million (ppm) via NDIR (Non-Dispersive Infrared) sensors.

**Supported sensors and technical specifications:**

| Sensor | Protocol | Range | Accuracy | Warm-up | Calibration |
|--------|----------|-------|----------|---------|-------------|
| MH-Z19B | UART (9600 baud, 8N1) | 0-5000 ppm | +/- 50 ppm + 5% reading | 3 min | Auto-calibration (ABC) every 24h, manual with command 0x87 |
| MH-Z19C | UART (9600 baud, 8N1) | 0-5000 ppm | +/- 50 ppm + 5% | 1 min | Same as B, improved |
| SenseAir S8 | UART (9600 baud) / Modbus | 400-2000 ppm (LP) / 400-10000 (standard) | +/- 40 ppm + 3% | 2 min | ABC, background calibration |

**MH-Z19B/C pinout:** VIN (5V), GND, TX (-> Flipper RX pin 14), RX (<- Flipper TX pin 13). The protocol is a 9-byte frame: 0xFF (start), 0x01 (sensor #), command, data (5 bytes), checksum. To read the concentration, send command 0x86 and receive the value in bytes 2-3 of the response (high byte * 256 + low byte = ppm).

**Use in pentesting:** CO2 level is an indirect indicator of room occupancy. In an empty office CO2 is ~400-500 ppm (outdoor level). With people present it rises rapidly: 800-1000 ppm with 3-5 people in an average room. During reconnaissance activities, measuring CO2 outside a closed door can give indications of how many people are inside without having to open it or use invasive methods. It's a little-known but effective method of physical OSINT.

---

### **Accelerometer**

Detects linear acceleration, vibrations, tilt, and orientation via 3-axis MEMS sensors connected via I2C or SPI.

**Supported sensors and technical specifications:**

| Sensor | Protocol | I2C Address | Range | Resolution | Max ODR | Extra |
|--------|----------|-------------|-------|------------|---------|-------|
| ADXL345 | I2C / SPI | 0x53 (SDO LOW) / 0x1D (SDO HIGH) | +/- 2/4/8/16 g | 13 bit (up to 4 mg/LSB at +/-2g) | 3200 Hz | Tap detection, free-fall, activity/inactivity |
| MMA8452Q | I2C | 0x1C (SA0 LOW) / 0x1D (SA0 HIGH) | +/- 2/4/8 g | 12 bit | 800 Hz | Landscape/portrait detection |
| MPU6050 | I2C | 0x68 (AD0 LOW) / 0x69 (AD0 HIGH) | +/- 2/4/8/16 g (acc), +/- 250/500/1000/2000 dps (gyro) | 16 bit | 1 kHz (acc), 8 kHz (gyro) | Accelerometer + gyroscope 6-DOF, integrated DMP |

**Pinout:** VCC (3.3V pin 9), GND (pin 18), SDA (pin 15), SCL (pin 16), INT1/INT2 (optional, any GPIO for interrupts). The MPU6050 also has XDA/XCL pins for connecting an external magnetometer (e.g., HMC5883L) as an I2C slave.

**Key ADXL345 registers:** POWER_CTL (0x2D) to exit standby (bit 3 = 1), DATA_FORMAT (0x31) for range and resolution, DATAX0-DATAZ1 (0x32-0x37) for the 6 bytes of XYZ data.

**Use in pentesting:** An accelerometer connected to the Flipper can function as a tamper detector. Placed on a door, a drawer, or a container, it records any opening or movement. During a physical pentest I used the ADXL345 as a "digital tripwire": left on a server room rack cabinet, it recorded timestamps of every significant vibration (threshold set at 0.5g), allowing me to know if someone had opened the rack during the night. The MPU6050, with its integrated gyroscope, is even more precise for detecting rotations (like a door opening).

---

### **Monitor Sensor**

Universal dashboard for real-time visualization of data from multiple sensors connected simultaneously to the I2C bus or GPIO/analog pins.

**Supported sensors and technical specifications:**

| Sensor | Protocol | I2C Address | Measurements | Accuracy |
|--------|----------|-------------|--------------|----------|
| BME280 | I2C / SPI | 0x76 (SDO LOW) / 0x77 (SDO HIGH) | Temperature (-40/+85C), Humidity (0-100% RH), Pressure (300-1100 hPa) | T: +/-1C, H: +/-3%, P: +/-1 hPa |
| DHT22 / AM2302 | Proprietary 1-Wire | N/A (digital pin) | Temperature (-40/+80C), Humidity (0-100% RH) | T: +/-0.5C, H: +/-2% |
| MQ-135 | Analog | N/A (ADC pin) | NH3, NOx, Alcohol, Benzene, Smoke, CO2 | Qualitative (requires calibration) |
| BH1750 | I2C | 0x23 / 0x5C | Illuminance (1-65535 lux) | +/-20% |

**Notes on BME280:** It is the most versatile environmental sensor for the Flipper. It uses configurable oversampling (x1, x2, x4, x8, x16) to balance precision and consumption. In "weather monitoring" mode (1 sample/min, x1 oversampling) it consumes only 0.16 uA. Data registers are 0xF7-0xFE (8 bytes: 20-bit pressure, 20-bit temperature, 16-bit humidity) with compensation via calibration coefficients in ROM.

**Notes on DHT22:** Uses a proprietary 1-Wire protocol (not compatible with Dallas/Maxim 1-Wire). The Flipper sends a 1-10ms pull-down as a start signal, then the sensor responds with 40 bits (16 humidity + 16 temperature + 8 checksum). Timing is critical: each bit is encoded by the HIGH signal duration (26-28us = 0, 70us = 1).

**Use in pentesting:** An environmental dashboard is useful during extended site surveys. Monitoring temperature and humidity of a server room during an assessment can reveal infrastructure problems (malfunctioning HVAC, zones with abnormal temperatures indicating heat concentration from equipment). The MQ-135 connected to the ADC can detect the presence of smoke, useful as an improvised alarm if you're working in a technical area.

---

### **Read Scan**

I2C bus scanner that automatically detects all connected devices, listing addresses that respond with ACK.

**Technical details:** The app sends a start condition byte + address (7 bit) + R/W bit across all 128 possible I2C address combinations (0x00-0x7F, excluding reserved addresses 0x00-0x07 and 0x78-0x7F). If a device responds with ACK, its address is shown on screen.

This is the equivalent of a "port scan" for the I2C bus: it immediately tells you which sensors are present and operational without having to know their address in advance. Extremely useful for debugging: if you've connected a BME280 and it doesn't respond, a Read Scan immediately tells you if the problem is in the wiring (no addresses found), the wrong address (responds on 0x77 instead of 0x76), or a conflict (two devices on the same address).

**Use in pentesting:** If during a hardware pentest you find a device with an exposed I2C connector (debug header, maintenance port), a Read Scan is the first step to understand what's connected to the bus. It's the equivalent of nmap for hardware: you discover the active "services". From there you can attempt to read specific registers to identify the chip (many have a WHO_AM_I register with a unique ID).

---

### **Sleep Counter**

Monitoring of sleep and movement data via MEMS and environmental sensors, with logging to SD card.

**Sensors used:**
- **ADXL345** (movement): configured in low-power mode with low activity threshold (~62.5 mg), detects micro-movements during sleep. The THRESH_ACT register (0x24) sets the threshold, ACT_INACT_CTL (0x27) enables detection on specific axes.
- **BME280** (environment): records temperature and humidity during the night to correlate sleep quality with environmental conditions.

**Operation:** The app samples the accelerometer at low frequency (e.g., 12.5 Hz in low-power mode, consumption ~23 uA) and counts "activity" events (threshold exceedance) in 5-10 minute intervals. More events = restless sleep. Environmental data is sampled every minute. Everything is logged to the SD card in CSV format for later analysis.

**Use in pentesting:** Marginal, but the activity detection concept is transferable: the same setup can be used as an ultra-low-power passive surveillance system to monitor access to an area during an overnight assessment.

---

### **Atomic Dice Roller**

Random number generator based on physical sensor noise, providing real hardware entropy (not pseudo-random).

**Entropy sources:**
- **LDR photoresistor (GL5528):** connected to the ADC pin (C3) with a pull-down resistor (10k). Ambient light fluctuations generate analog noise. Resistance varies from ~1k ohm (bright light) to ~1M ohm (dark). The 12-bit ADC LSB noise (~1-2 LSB) combined with light micro-fluctuations provides entropy.
- **ADXL345 accelerometer:** the MEMS sensor's thermal noise (~1.1 LSB RMS at 100 Hz, +/-2g range) across 3 axes provides additional entropy. Even with the sensor stationary, the least significant bits vary randomly.

**Algorithm:** The app repeatedly samples the sources, takes the LSB bits (1-2 bits per sample), accumulates them in a buffer, and applies a hash (or simple XOR mixing) to generate a value in the selected die range (D4, D6, D8, D10, D12, D20). Entropy quality is sufficient for games but not for cryptographic applications without further conditioning (e.g., Von Neumann debiasing).

---

### **Gas Sensor**

Interface for MQ-series gas sensors, which use a tin oxide (SnO2) heating element whose resistance varies in the presence of specific gases.

**Supported sensors and technical specifications:**

| Sensor | Primary Target Gas | Detection Range | Heater Voltage | Preheat Time |
|--------|-------------------|-----------------|----------------|--------------|
| MQ-2 | LPG, Propane, Methane, Smoke | 300-10000 ppm | 5V (draws ~150mA!) | >24h for stable calibration |
| MQ-4 | Methane, Natural Gas | 300-10000 ppm | 5V | >24h |
| MQ-7 | Carbon Monoxide (CO) | 20-2000 ppm | 5V (1.4V/5V cycle) | >48h |
| MQ-9 | CO + Combustible Gases | CO: 10-1000 ppm, Gas: 100-10000 ppm | 5V (cycle) | >24h |
| MQ-135 | NH3, NOx, Alcohol, Benzene, Smoke | 10-1000 ppm (varies by gas) | 5V | >24h |

**Connection:** MQ sensors have 4 pins (VCC, GND, DOUT digital with comparator, AOUT analog). For quantitative readings, AOUT is connected to the Flipper's ADC pin (C3) with a voltage divider if needed (output can reach 5V). WARNING: MQ sensors draw considerable current (150-180mA) for the heater, so they require external power (not from the Flipper's 3.3V).

**Conversion formula:** The sensor resistance Rs is calculated as: Rs = ((Vcc * RL) / Vout) - RL, where RL is the load resistor (typically 10-47k ohm). The Rs/R0 ratio (R0 = resistance in clean air after calibration) is used with the datasheet characteristic curves to obtain the concentration in ppm.

**Use in pentesting:** In physical security assessment scenarios at industrial or chemical facilities, having a portable gas detector is a personal safety measure. Before entering a cable tray, an attic, or a mechanical room, a quick reading with an MQ-2 (combustible gases) or MQ-7 (CO) can save your life. It's not paranoid: I've worked in facilities where mechanical rooms had known and "tolerated" gas leaks. An MQ-2 connected to the Flipper gave me a warning at ~800 ppm methane in a boiler room (the LEL threshold for methane is ~50000 ppm, so there was no immediate danger, but the leak was there).

---

### **MAX31855**

Reading of type K thermocouples via the MAX31855 digital converter, which provides temperature with 0.25C resolution over an extended range.

**Technical specifications:**
- **Protocol:** SPI (read-only, no MOSI needed)
- **Pinout:** VCC (3.3V pin 9), GND (pin 18), SCK (pin 2), CS (pin 5), DO/MISO (pin 3)
- **Range:** -200C to +1350C (type K thermocouple), with internal cold junction compensation (-40C to +125C)
- **Resolution:** 0.25C (thermocouple), 0.0625C (cold junction)
- **Accuracy:** +/-2C (0-1000C range), +/-4C at limits
- **Data format:** 32-bit SPI frame: D[31:18] = 14-bit thermocouple temperature (signed), D[17] = reserved, D[16] = fault bit, D[15:4] = 12-bit internal temperature, D[3] = reserved, D[2] = SCV (short to VCC), D[1] = SCG (short to GND), D[0] = OC (open circuit)

**Practical use:** Essential for measurements in contexts where standard digital sensors can't reach: verifying processor temperature under load during hardware reverse engineering, measuring the temperature of a motor or power component, or monitoring soldering processes.

---

### **MH-Z19 UART**

Dedicated support for MH-Z19B and MH-Z19C CO2 sensors with UART communication and advanced calibration features.

**Detailed UART protocol:**
- Baud rate: 9600, 8 bit, no parity, 1 stop bit (8N1)
- Command frame (9 bytes): `[0xFF] [0x01] [CMD] [0x00] [0x00] [0x00] [0x00] [0x00] [CHECKSUM]`
- Checksum: negation of the sum of bytes 1-7 + 1 (two's complement)
- CO2 read command: CMD = 0x86
- Response (9 bytes): `[0xFF] [0x86] [CO2_HIGH] [CO2_LOW] [TEMP] [STATUS] [0x00] [0x00] [CHECKSUM]`
- CO2 ppm = CO2_HIGH * 256 + CO2_LOW
- Temperature = TEMP - 40 (degrees Celsius, approximate)

**Useful commands:**
| Command | CMD Byte | Description |
|---------|----------|-------------|
| Read CO2 | 0x86 | Reads CO2 concentration |
| Calibrate Zero | 0x87 | Zero point calibration (400 ppm in open air) |
| Calibrate Span | 0x88 | Span point calibration (with reference gas) |
| ABC On/Off | 0x79 | Enable/disable auto-calibration (byte 3: 0xA0=on, 0x00=off) |
| Set Range | 0x99 | Set range (bytes 3-4 for value: 0x13 0x88 = 5000 ppm) |

**Note on ABC calibration:** The Automatic Baseline Correction assumes that the lowest CO2 level measured in the last 24 hours is ~400 ppm (atmospheric level). In always-occupied environments this can cause drift. In these cases, disable ABC and calibrate manually by bringing the sensor outdoors.

---

### **Plantower PMSx003**

Reading of Plantower particulate matter sensors, which use laser diffusion to count and size particles suspended in the air.

**Supported sensors:**

| Sensor | Dimensions | PM Range | Data Output | Baud Rate |
|--------|-----------|----------|-------------|-----------|
| PMS3003 | 65x42x23 mm | PM1.0, PM2.5, PM10 | 24-byte frame | 9600 |
| PMS5003 | 50x38x21 mm | PM1.0, PM2.5, PM10 + particle count | 32-byte frame | 9600 |
| PMS7003 | 48x37x12 mm | Same as PMS5003, more compact | 32-byte frame | 9600 |

**UART protocol (PMS5003/7003):**
- 32-byte frame: `[0x42] [0x4D] [Frame Length High] [Frame Length Low] [Data 1-13] [Checksum High] [Checksum Low]`
- Data 1-2: PM1.0 standard (ug/m3)
- Data 3-4: PM2.5 standard (ug/m3)
- Data 5-6: PM10 standard (ug/m3)
- Data 7-8: PM1.0 atmospheric (ug/m3)
- Data 9-10: PM2.5 atmospheric (ug/m3)
- Data 11-12: PM10 atmospheric (ug/m3)
- Data 13-18: Particle count >0.3um, >0.5um, >1.0um, >2.5um, >5.0um, >10um (per 0.1L of air)

**Pinout:** VCC (5V), GND, TX (-> Flipper RX pin 14), RX (<- Flipper TX pin 13), SET (optional, digital pin for sleep mode), RESET (optional).

**Use in pentesting:** PM2.5 is an air quality indicator that can reveal the presence of hidden industrial activity, malfunctioning HVAC systems, or areas with excessive dust (relevant for equipment safety in data centers, where ASHRAE standards recommend PM10 < 15 ug/m3).

---

### **Radiation Sensor**

Support for alternative radiation detection modules beyond classic Geiger tubes, including solid-state detectors and digital modules with TTL output.

**Supported sensors:**

| Sensor | Type | Output | Sensitivity | Notes |
|--------|------|--------|-------------|-------|
| Digital Geiger TTL | GM tube with integrated electronics | TTL pulses (3.3/5V) | Depends on tube | Ready-to-use modules (RadSens, RadiationD) |
| LND 712 | Halogen-quenched GM tube | Pulses (requires electronics) | ~18 cps/mR/h (Cs-137) | Sensitive to Beta, Gamma, X-ray |

**Differences from Geiger Counter:** This app is designed for modules with more advanced communication protocols compared to simple pulse counting. Some modules (e.g., RadSens based on CTC-5/SBM-20 with microcontroller) communicate via I2C and directly provide processed values (uSv/h, CPM, statistical data). The RadSens default I2C address is 0x66.

---

### **Temp Sensor Reader**

Compatibility with a wide range of digital thermometers using different protocols: 1-Wire, I2C, and analog.

**Supported sensors and technical specifications:**

| Sensor | Protocol | Address/Pin | Range | Resolution | Accuracy |
|--------|----------|-------------|-------|------------|----------|
| DS18B20 | 1-Wire (Dallas) | Any GPIO + 4.7k pull-up | -55C to +125C | 9-12 bit configurable (0.5C - 0.0625C) | +/-0.5C (range -10/+85C) |
| TMP117 | I2C | 0x48/0x49/0x4A/0x4B | -55C to +150C | 0.0078C (16 bit) | +/-0.1C (range -20/+50C) |
| LM75 | I2C | 0x48-0x4F (3 configurable bits) | -55C to +125C | 0.5C (9 bit) | +/-2C |
| TMP102 | I2C | 0x48/0x49/0x4A/0x4B | -40C to +125C | 0.0625C (12 bit) | +/-0.5C (range -25/+85C) |
| NTC 10k | Analog (ADC) | Pin C3 + voltage divider | -40C to +125C (depends on table) | Depends on ADC (12 bit) | +/-1-2C with calibration |

**1-Wire protocol (DS18B20):** The master (Flipper) sends a reset pulse (480us pull-down), the DS18B20 responds with a presence pulse. Communication follows with ROM commands (0x33 Read ROM, 0xCC Skip ROM, 0x55 Match ROM) and function commands (0x44 Convert T, 0xBE Read Scratchpad). 12-bit conversion takes ~750ms.

**NTC 10k with Steinhart-Hart equation:** To convert the ADC reading to temperature: R_NTC = R_fixed * (ADC_max / ADC_value - 1), then 1/T = A + B*ln(R) + C*(ln(R))^3, with typical coefficients A=1.009249522e-3, B=2.378405444e-4, C=2.019202697e-7 for a standard 10k NTC.

---

### **UV Meter**

Measurement of UV index and ultraviolet radiation power via dedicated sensors.

**Supported sensors:**

| Sensor | Protocol | I2C Address | Range | Bands | Notes |
|--------|----------|-------------|-------|-------|-------|
| VEML6075 | I2C | 0x10 | UV Index 0-15+ | UVA (365nm) + UVB (330nm) | Integrated IR and visible light compensation |
| ML8511 | Analog | N/A (ADC pin) | 0-15 mW/cm2 | UV (280-390nm) | Linear output ~0.99V (no UV) to ~2.8V (15 mW/cm2) |

**UV Index calculation (VEML6075):** UVA_calc = UVA_raw - a*UVcomp1 - b*UVcomp2, UVB_calc = UVB_raw - c*UVcomp1 - d*UVcomp2, where UVcomp1 and UVcomp2 are compensation channels for visible light and IR. The UV Index is calculated as (UVA_calc * UVA_resp + UVB_calc * UVB_resp) / 2, with response factors from the datasheet.

---

### **VEML7700 Lux Meter**

Precision illuminance measurement in lux via the VEML7700 sensor with extremely wide dynamic range.

**Detailed technical specifications:**
- **Protocol:** I2C, fixed address 0x10
- **Range:** 0 - 120000 lux
- **Minimum resolution:** 0.0036 lux (gain x2, integration 800ms)
- **Main registers:** ALS_CONF (0x00) for gain/integration time configuration, ALS (0x04) for the raw value, WHITE (0x05) for the white channel, ALS_INT (0x06) for interrupt thresholds
- **Configurable gain:** x1, x2, x1/8, x1/4
- **Integration time:** 25ms, 50ms, 100ms, 200ms, 400ms, 800ms
- **Lux = raw_ALS * resolution_factor** (depends on gain and integration time, see table in datasheet)

**Comparison with BH1750:** The VEML7700 has a much wider dynamic range (120k lux vs 65k) and finer resolution, but is more complex to configure. For quick measurements the BH1750 is more straightforward.

---

### **VL6180X Distance Sensor**

Short-range distance and proximity sensor based on Time-of-Flight, with integrated ALS (Ambient Light Sensor).

**Detailed technical specifications:**
- **Protocol:** I2C, default address 0x29 (reprogrammable via register 0x0212)
- **Distance range:** 0 - 200 mm
- **Resolution:** ~1 mm
- **Source:** VCSEL laser 850nm (class 1, eye-safe)
- **ToF principle:** The sensor emits a laser pulse, measures the reflected photon's time of flight with a SPAD (Single Photon Avalanche Diode). Distance = (c * t) / 2, but the sensor handles everything internally and directly returns the value in mm.
- **Key registers:** RESULT_RANGE_VAL (0x0062) for distance value, RESULT_ALS_VAL (0x0050) for lux, RESULT_RANGE_STATUS (0x004D) for measurement validity
- **Cross-talk compensation:** Essential when using with a cover glass. Calibrate cross-talk by placing a target at a known distance and saving the compensation value in register 0x001E.

---

### **Water Sensor Reader**

Reading of soil moisture sensors and water detectors via analog or digital input.

**Supported sensors:**

| Sensor | Type | Output | Operating Principle |
|--------|------|--------|---------------------|
| Capacitive Soil Moisture v1.2 | Analog | 0-3V (inversely proportional to moisture) | Measures the dielectric constant of soil via capacitance (does not corrode) |
| YL-69 / YL-38 | Analog + Digital | AOUT: 0-5V, DOUT: HIGH/LOW | Measures resistance between two electrodes (corrodes over time) |
| Leak Sensor (contact type) | Digital | HIGH/LOW | Two conductive traces: water closes the circuit |

**Capacitive Soil Moisture connection:** VCC (3.3V or 5V), GND, AOUT -> ADC pin (C3). Typical value is ~520 in air (dry), ~260 in water (saturated). This sensor is superior to resistive types (YL-69) because it has no exposed electrodes that corrode from electrolysis.

**Practical and pentest use:** Beyond the obvious use in smart agriculture, a leak sensor can be deployed during a physical assessment to monitor water infiltration in server rooms or archives. Water is hardware's number one enemy, and early warning can prevent damage to critical equipment during an extended assessment.

---

## General Notes on Sensor Use in Pentesting

The Flipper Zero's GPIO sensor suite transforms the device from a simple wireless hacking tool into a complete environmental reconnaissance platform. During a physical penetration test or red team engagement, environmental data provides valuable intelligence:

- **Temperature/humidity** (BME280): server room conditions, ASHRAE compliance
- **CO2** (MH-Z19): room occupancy
- **Distance** (VL53L0X): space mapping, sensor blind spots
- **Gas** (MQ-series): personal safety in technical rooms
- **Radiation** (Geiger): documentation in facilities with radioactive sources
- **Light** (BH1750): evaluation of CCTV camera operating conditions
- **Particulate** (PMS5003): data center air quality

From my experience, the most useful sensors to always carry in the backpack during an engagement are the BME280 (compact, multi-function, ultra-low consumption), the VL53L0X (quick and precise measurements), and an MQ-7 for CO if working in industrial environments. The Flipper Zero as a central hub for all these sensors eliminates the need to carry separate dedicated instruments.
