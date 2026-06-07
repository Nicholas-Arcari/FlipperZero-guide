# Creative and Utility - GPIO Tools, Signal Analysis, and Automation

This section covers general-purpose GPIO tools: LED control, analog outputs, pin reading, encoders, oscilloscopes, logic analyzers, signal generators, servo testers, and other daily utility tools for makers, testers, and hardware developers.

---

### • Air Mouse

Tool for controlling the device or PC cursor via Flipper Zero movements.

Extended features:

- 3-axis motion detection via internal accelerometer.
- Support for HID mouse protocols via GPIO or Bluetooth.
- Adjustable sensitivity and automatic calibration.
- Selectable relative and absolute movement.

Practical example:

- Connect the Flipper via USB HID.
- Enable "Mouse" mode.
- Move the device → the cursor on the PC moves.
- Test click with GPIO button configured as left click.

(Note: Some PCs require updated HID drivers)

### • 7-Segment Output

Drives 7-segment displays via GPIO.

Extended features:

- Individual segment control at digital level or via external driver.
- Multiplexing support for multiple displays.
- Ability to display numbers, limited letters, and custom symbols.

Practical example:

- Connect common cathode → GPIO configured as outputs.
- Set number sequence (0-9) for testing.
- Enable number or symbol "scrolling".

(Note: Watch the maximum LED current: use appropriate resistors)

### • Input Reader 2

Simultaneous reading of multiple digital inputs.

Extended features:

- Support for multiple GPIO channels.
- HIGH/LOW level detection and software debounce.
- Rising/falling edge trigger.
- Polling and interrupt modes (if hardware compatible).

Practical example:

- Connect 4 buttons to 4 GPIO pins.
- Start multi-read.
- Press buttons → Flipper console shows which one was pressed.

(Note: Avoid cables that are too long without pull-up/pull-down resistors)

### • Intervalometer

Timer for cameras, automation, or sequential triggers.

Extended features:

- Configurable for intervals in seconds, minutes, or hours.
- Trigger via GPIO or relay for external actuators.
- Single shot, continuous interval, or count-based modes.

Practical example:

- Connect relay module to camera.
- Set interval to 10 sec.
- Start → the Flipper activates the relay every 10 seconds.

(Note: Some camera modules require triggers with specific polarity)

### • Canon Intervalometer

Dedicated timer for Canon cameras.

Extended features:

- Programmed and interval-based shots.
- Timelapse mode with frequency setting.
- Remote control via GPIO.
- Compatible with many Canon DSLRs via remote connector.

Practical example:

- Connect Flipper to Canon remote connector.
- Set interval to 5s → start automatic shots.
- Save images → analyze timelapse.

(Note: Not all Canon models are supported; verify compatibility)

### • Pins Reader

Quick GPIO pin state reading.

Extended features:

- Multiple digital level monitoring.
- Real-time reading with frequent updates.
- Support for internal or external pull-up/pull-down.
- Programmable triggers on rising/falling edge.

Practical example:

- Connect 6 pins to digital sensors.
- Launch Pins Reader → read HIGH/LOW values on all pins simultaneously.
- Configure alert on pins that change state.

(Note: Useful for hardware debugging or custom board testing)

### • RGB LED

RGB LED control via PWM.

Extended features:

- Color management via PWM on three channels (R/G/B).
- Support for fade, blink, and custom patterns.
- Brightness and combination preset saving.

Practical example:

- Connect common anode/cathode RGB LED to GPIO pins.
- Set PWM → display color combinations.
- Use cyclic patterns for visual status signaling.

(Note: Check maximum LED current, use appropriate resistors)

### • Analog Output

Simulated analog output via Flipper Zero PWM or DAC.

Extended features:

- Variable analog signal generation.
- Voltage/average control on GPIO pin.
- Support for PWM modulation, variable frequency, and programmable duty cycle.
- Compatible with small test circuits or analog actuators.

Practical example:

- Connect LED or motor to analog pin.
- Set duty cycle to 50% → LED at half brightness.
- Modify duty cycle for gradual variations.

(Note: Not suitable for high-current loads without external driver)

### • Encoder Reader

Tool for reading rotary (incremental) encoders with high precision.

Extended features:

- A/B quadrature recognition.
- Step counting with anti-bounce filtering.
- Speed mode (steps/sec).
- Reset, zero offset, inverted direction.
- Real-time motion graph.

Practical example

Testing a 600 PPR industrial encoder:

- Connect A/B channels to GPIO.
- Start live monitoring.
- Rotate the shaft and verify direction and steps.
- Use graph to check stability and jitter.

### • Flashlight

Turns the device into a high-brightness flashlight using the built-in LED or an external LED.

Extended features:

- Variable brightness mode.
- Strobe with adjustable frequency.
- SOS function in Morse code.
- High-efficiency PWM to reduce power consumption.
- Ability to drive a powerful external LED.

Practical example

Use in dark environment for PCB diagnostics:

- Connect small LED to GPIO.
- Set intensity to maximum.
- Aim at PCB to check for microfractures.

### • GPIO

Generic tool for manipulating digital pins as input/output.

Extended features:

- Quick pin configuration as INPUT/OUTPUT/PU/PD.
- Automatic pulsing (toggling) at defined frequency.
- Monitor mode for tracking state changes.
- Digital pattern injection.
- Output consumption profiling.

Practical example

Testing a relay:

- Set pin as OUTPUT.
- Enable slow toggling (1 Hz).
- Listen for relay click → verify operability.

### • GPIO Badge

Electronic badge with programmable GPIO interfaces.

Extended features:

- Built-in LED control.
- Basic button and sensor reading.
- "Badge Animation" mode for lighting effects.
- API compatible with other GPIO extensions.
- Rapid scripting capability.

Practical example

Logo animation:

- Load script with flashing patterns.
- Start LED sequence.
- Set continuous loop.

### • GPIO Controller

Suite for advanced digital and analog pin management.

Extended features:

Complete dashboard of all pins.

- ADC/DAC adjustments (if available).
- Conditional triggers: notifications and automations.
- Integration with external SPI/I2C modules.
- Support for macros and custom sequences.

Practical example

Simple automation:

- Configure input on magnetic sensor.
- When triggered → activate LED output for 5s.
- Save and test macro.

### • GPIO Explorer

Dedicated tool for electrical activity analysis on pins.

Extended features:

- Multi-pin real-time monitoring.
- Signal timeline with high-precision timestamps.
- Pulse width measurement.
- Frequency and duty cycle detection.
- Log export.

Practical example

Anti-bounce button signal analysis:

- Connect button.
- Press → observe real bouncing.
- Optimize debounce circuit or software.

### • Logic Analyzer

Multi-channel digital logic analyzer via GPIO.

Extended features:

- Sampling up to available hardware limits.
- Rising/falling edge trigger.
- Basic protocol decoding (UART, I2C, SPI).
- VCD/CSV export.
- Real-time waveform visualization.

Practical example

UART traffic analysis:

- Connect RX to signal.
- Set trigger on START bit.
- Record frame → decode text.

### • Oscilloscope

Digital oscilloscope via GPIO.

Extended features:

- Analog waveform visualization.
- Multi-channel up to hardware limits.
- Rising/falling trigger.
- Frequency, duty cycle, amplitude measurement.
- Data export in CSV or VCD.

Practical example

PWM signal analysis:

- Connect pin → oscilloscope input.
- Visualize waveform → measure duty cycle.
- Export data for report.

### • Signal Generator

Signal generator via GPIO.

Extended features:

- Waveform creation: sine, square, triangle.
- Adjustable frequency.
- Adjustable amplitude according to hardware capability.
- Sweep and burst modes.
- Electronic circuit testing and calibration.

Practical example

Analog input test:

- Connect generator pin → ADC input.
- Set 1 kHz square wave.
- Measure circuit response → verify linearity.

### • Servo Tester 2

Advanced tester for analog and digital servos.

Extended features:

- Angle control 0-180 degrees (or more for continuous models).
- PWM adjustable in frequency and duty cycle.
- Support for digital servos with PPM signal.
- Continuous sweep mode for calibration.
- Value display on built-in screen (if present).

Practical example

Servo motor test:

- Connect servo to GPIO pin + power supply.
- Set sweep from 0 to 180 degrees.
- Observe movement → verify responsiveness.
- Optional PWM frequency adjustment.

### • ServoTester

Basic tester for analog servos.

Extended features:

- Manual servo angle control.
- Servo motor power via external GPIO.
- Quick functional test before project integration.

Practical example

Servo verification:

- Connect servo.
- Manually rotate angle slider.
- Check response and range of motion.

### • Spotify Remote

Spotify remote control via GPIO + ESP/Internet.

Extended features:

- Play/Pause, next/previous track.
- Volume control.
- Playlist management via GPIO + network interface.
- LED feedback on playback status.

Practical example

Music playback:

- Connect buttons → Play/Pause.
- Connect LED → status indication.
- Test controls → correct playback on remote device.

### • WAV Recorder

Digital audio recorder in WAV format.

Extended features:

- 8/16/24-bit sampling.
- Frequency 8-48 kHz (hardware dependent).
- Save to SD or internal memory.
- Recording trigger via GPIO or timer.

Practical example

Ambient recording:

- Activate trigger → begin recording.
- Save file to SD.
- Play WAV to verify audio quality.

### • WA2812B LED Tester

Addressable LED tester for WS2812/APA102 via GPIO.

Extended features:

- Color and brightness control.
- Animated sequence testing.
- Data line and power debugging.
- Single or multiple strip support.

Practical example

LED strip test:

- Connect strip → start color sequence.
- Check for defective LEDs → fix connections.

### • Yuricable Pro Max

Advanced multi-purpose diagnostic tool.

Extended features:

- Multi-protocol cable and connection testing.
- Voltage, continuity, and digital signal measurements.
- Test logging for documentation.
- External module support and optional power supply.

Practical example

Sensor network diagnostics:

- Connect cables → run continuity and voltage test.
- Identify malfunctioning lines.
- Record log for maintenance.
