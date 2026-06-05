# VGM (Video Game Module) - Operational Guide

Gaming addon for the Flipper Zero that adds an accelerometer/gyroscope for control via physical movement of the device. Allows playing tilt-based games, air mouse, and gestural control.

---

## Hardware

The VGM connects to the GPIO header and integrates:
- **IMU (Inertial Measurement Unit):** 3-axis accelerometer + 3-axis gyroscope (typically MPU6050, LSM6DS3 or BMI160)
- **Communication:** I2C (typical address 0x68 or 0x6A)
- **Data rate:** up to 1 kHz for smooth readings
- **Sensitivity:** configurable (+/-2g/+/-4g/+/-8g/+/-16g for accelerometer, +/-250/+/-500/+/-1000/+/-2000 deg/s for gyroscope)

---

## Tools

### Air Arkanoid

Arkanoid version controlled by tilting the Flipper. The paddle moves left/right based on tilt on the X axis.

**Controls:** tilt the Flipper left/right to move the paddle. Sensitivity is calibrated for natural wrist movements.

### Air Labyrinth

Labyrinth controlled via tilting -- the ball moves following the gravity perceived by the accelerometer.

**Controls:** tilt the Flipper in all directions to guide the ball through the labyrinth. Requires precise and steady movements.

### VGM Air Mouse

Transforms the Flipper into an air mouse: moving the device in space moves the cursor on the PC screen connected via USB HID.

**Features:**
- 3D tracking with accelerometer + gyroscope fusion
- Automatic calibration on first use
- Adjustable sensitivity
- Click via Flipper buttons

**Practical usage:** presentation control, PC navigation from a distance, gestural control demo.

### VGM Game Remote

Gaming remote that uses the VGM as a motion controller for games or applications on PC.

### Video Game Module Tool

Utility suite for VGM module configuration, calibration, and diagnostics:
- Accelerometer test (raw values on 3 axes)
- Gyroscope test (angular velocity)
- Offset calibration
- I2C communication verification

> **Personal note:** The VGM has no direct use in pentesting, but the Air Mouse is surprisingly useful when you need to control a PC from a few meters away -- for example during a findings presentation where the PC is connected to the projector but you're on the other side of the room.
