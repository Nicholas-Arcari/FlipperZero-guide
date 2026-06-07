# IoT and Sensors - Measurements, Monitoring, and Diagnostics

This section covers GPIO tools dedicated to sensors, environmental measurements, battery monitoring, continuity testing, and physical diagnostic instruments. Ideal for IoT projects, lab work, and field testing.

---

### • GPS

External GPS module interface.

Extended features:

- NMEA data reception from GPS modules via UART.
- Parsing of latitude, longitude, altitude, and speed.
- Current position display and real-time tracking.
- GPS data logging to file for post-trip analysis.

Practical example:

- Connect GPS module to TX/RX GPIO pins.
- Launch GPS → wait for satellite fix.
- View coordinates on the Flipper → record route.

### • U-Blox GPS

U-Blox GPS module interface via GPIO/UART.

Extended features:

- NMEA/GNSS data reading.
- Position, speed, UTC time.
- GPS trace logging.
- WAAS/EGNOS support.
- Debug via serial terminal.

Practical example

Route tracking:

- Connect module → power on.
- Receive real-time position.
- Save log → map visualization.

### • CO2 Logger

Dedicated tool for measuring and recording CO2 levels from compatible sensors (MH-Z19, SCD30, CCS811, and similar).

Extended features:

- Continuous real-time readings (ppm, temperature, humidity if supported).
- Internal logging with timestamps.
- Automatic ABC or manual calibration.
- Short-term historical graph.
- Log export in CSV format.
- "Air Quality Alert" function with configurable thresholds.

Practical example

Office air quality monitoring:

- Connect TX/RX (or SDA/SCL for I2C sensors).
- Enable logging every 10 seconds.
- Set alarm at 1200 ppm.
- Analyze CSV to verify insufficient ventilation.

### • Battery Checker

Tool for measuring the battery status of the Flipper or external devices.

Extended features:

- Real-time voltage reading.
- Approximate residual capacity calculation.
- Current draw monitoring.
- Historical logging for battery degradation analysis.

Practical example:

- Connect external battery to GPIO + GND pins.
- Launch Battery Checker → read voltage → estimate remaining percentage.
- Record data across multiple sessions to verify performance.

### • Step Counter

Pedometer based on digital input or motion sensors.

Extended features:

- Step detection via accelerometer or external inputs.
- Estimated distance calculation and calorie counting.
- Real-time display on screen or via app connection.
- Support for manual or automatic daily reset.

Practical example:

- Connect accelerometer sensor to GPIO pins.
- Launch Step Counter → monitor step count on the Flipper display.
- Record activity session → export data for analysis.

### • Continuity Tester

Electrical continuity tester with visual/audible feedback and high responsiveness.

Extended features:

- Response time < 5 ms.
- Audible signal with intensity proportional to resistance.
- Resistance test (uncalibrated ohmic estimate).
- "Hands-Free" mode with latch.
- Anti-bounce logic for damaged contacts.

Practical example

Verifying traces on a damaged PCB:

- Connect probes to dedicated GPIO pins.
- Enable audible mode.
- Move probes along the trace.
- Identify the break point within seconds.

### • Flippy Temp

Temperature measurement tool via external sensors (TMP102, DS18B20, thermistors) or via ADC reading.

Extended features:

- Digital and analog sensor support.
- Automatic °C/°F conversion.
- Continuous logging with timestamps.
- Manual calibration (offset/gain).
- High/low temperature alarms.

Practical example

Monitoring water temperature in a project:

- Connect DS18B20 on a single wire.
- Set logging every 5 seconds.
- Start monitor and view graph.
- Enable alarm > 70°C.

### • INA Meter

Current, voltage, and power measurement via INA219/INA226 sensors.

Extended features:

- Precise mA/mV readings.
- Real-time power calculation.
- Consumption logging.
- Custom shunt calibration.
- "Energy Counter" mode.

Practical example

Analysis of a WiFi module:

- Connect power supply through INA.
- Connect to tool → read TX consumption peaks.
- Use log to optimize duty cycle.

### • Notel LRF Sampler

Laser Range Finder via GPIO for precise measurements.

Extended features:

- Single or continuous trigger.
- Distance measurement up to hardware limit (e.g., 40 m).
- Logging to CSV file.
- Unit conversion (m, cm, ft).
- Debug mode for trigger/echo signals.

Practical example

Room distance measurement:

- Point sensor at wall.
- Activate single trigger.
- Read distance → record in log.
- Repeat test at multiple points for mapping.

### • Wire Tester

Wiring and GPIO continuity tester.

Extended features:

- Pin-to-pin continuity verification.
- Short circuit indication.
- Single or multiple testing.
- Compatibility with 3.3V/5V digital signals.

Practical example

Flat cable verification:

- Connect wires → test continuity.
- Pass/fail indication.
- Note any shorts or breaks.

### • Fencing Test Box

Tool for diagnosing fencing equipment (foil, epee, sabre), compatible with regulatory electrical logic.

Extended features:

- Tip/weapon continuity test with adjustable thresholds.
- Referee box simulation: "valid hit / invalid hit" lights.
- Event logging for subsequent analysis.
- "Training" mode to measure reaction time.
- Support for FIE configurations (impedance, minimum times).

Practical example

Checking a foil with defective contacts:

- Connect clips to weapon terminals.
- Enable tip monitoring.
- Press and release → detect irregularities in closure time.
- Identify oxidized contact to replace.

### • Longwave Clock

Longwave (LW) clock for precise time synchronization and measurement.

Extended features:

- WWVB, DCF77, or MSF signal reception (depending on module).
- Automatic time update.
- Real-time date and time display.
- Timestamp logging to file.
- Signal debug mode for reception quality analysis.

Practical example

Automatic synchronization:

- Connect LW receiver module.
- Enable DCF77 reception.
- View current time → automatic hourly update.
- Log signal frequency for reception testing.

### • Strobometer

Strobe for rotational or frequency measurements.

Extended features:

- Adjustable flash frequency.
- Synchronization with external events.
- RPM measurement of rotating objects via LED.
- Logging to CSV file.

Practical example

Motor speed measurement:

- Aim strobe → lights flash at intervals.
- Count cycles → calculate RPM.
- Adjust frequency → verify accuracy.
