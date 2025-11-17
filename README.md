# IoT_Lab5

## Features
- Implement a MicroPython webserver to expose DC motor control endpoints.
- Control motor direction (Forward / Backward / Stop) from a mobile app.
- Adjust motor speed (0–100% PWM) via REST `/speed?value=NN`.
- Build an MIT App Inventor app to send HTTP commands to ESP32.
- Log every command + speed change to InfluxDB.
- Visualize real-time motor activity using a Grafana dashboard.
- Wi-Fi auto-reconnect & bad request handling for reliability.

## Requirements
- ESP32 Dev Board (MicroPython firmware flashed)
- L298N motor driver
- DC motor (7–12V)
- Android phone (MIT App Inventor)
- Wi-Fi access point
- InfluxDB (local or cloud)
- Grafana dashboard
- Laptop with Thonny IDE
- Breadboard + jumper wires

## Wiring

| ESP32 Pin | L298N Pin | Function |
|----------|-----------|----------|
| GPIO25   | ENA       | PWM (speed control) |
| GPIO26   | IN1       | Direction 1 |
| GPIO27   | IN2       | Direction 2 |
| GND      | GND       | Common ground |

![Uploading image.png…]()


## Usage Instruction

### 1. Mobile App Control
- Open the MIT App Inventor app.
- Tap **Forward**, **Backward**, or **Stop** to send commands.
- Use the **speed slider** to set motor speed (0–100%).
- Status label updates show the latest action.

### 2. ESP32 Webserver Endpoints
- `/forward?speed=NN`
- `/backward?speed=NN`
- `/stop`
- `/speed?value=NN`

### 3. InfluxDB Logging
Every motor action is logged using HTTP POST in JSON format:

### 4. Grafana Dashboard

Line graph: Motor speed vs time

Stat panel: Last command

Table: Event history with timestamps

Dashboard updates live when the motor is controlled.

## Screenshots



## Short Demo Video (60–90s)


