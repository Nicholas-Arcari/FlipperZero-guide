# GAMES - Hardware Mini-Games

Mini-games that leverage external GPIO interfaces, sensors, and hardware protocols to create interactive experiences. Beyond the gaming aspect, they represent excellent educational examples of UART communication, sensor reading, and real-time input handling.

---

## UART Pong

Hardware version of the classic Pong controlled through UART serial communication.

### How It Works

The game uses the Flipper's UART (pins PB6 TX, PB7 RX) to receive input from an external controller. The controller (Arduino, ESP8266, serial joystick) sends UP/DOWN commands via serial, and the Flipper moves the paddle accordingly.

**Communication parameters:**
- Baud rate: 9600 or 115200 (configurable)
- Format: 8N1 (8 data bits, no parity, 1 stop bit)
- Commands: ASCII characters ('ù = up, 'D' = down) or binary values

**Configuration:**
- Ball speed: adjustable
- Paddle size: adjustable
- AI mode: the Flipper controls one side automatically

### Educational Value

UART Pong is the best way to learn serial communication:
- How to configure baud rate and format
- How to read data in real-time without blocking
- How to synchronize external input with game logic
- How to manage timing between game frames and UART reading

**Example Arduino controller:**
```
void setup() { Serial.begin(9600); }
void loop() {
  int val = analogRead(A0); // Joystick Y
  if (val > 600) Serial.write('U');
  else if (val < 400) Serial.write('D');
  delay(50);
}
```

> **Personal note:** I used UART Pong as a demo during a hardware hacking workshop. By connecting a joystick to an Arduino and then to the Flipper via UART, participants understood in 5 minutes how serial communication works. Much more effective than explaining the theory.

---

## VL6180X Pong

Pong variant controlled by the VL6180X distance sensor (Time-of-Flight) -- the closer or farther you get from the sensor, the more the paddle moves.

### How It Works

The VL6180X is a ToF sensor that measures distance via the time of flight of an IR pulse. Connected via I2C (address 0x29), it provides measurements in millimeters with a high refresh rate.

**Mapping:** the measured distance (0-100mm) is linearly mapped to the paddle position on the screen.

**Configuration:**
- Automatic calibration for varying light conditions
- "Precision Mode": 1mm resolution
- Difficulty adaptation based on signal stability

### Educational Value

Demonstrates practical usage of:
- I2C bus with high-frequency polling
- Mapping analog values to discrete actions
- Automatic sensor calibration
- Sensor data noise management
