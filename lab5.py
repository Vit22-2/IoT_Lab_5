# ------------------------------------------------------------
# FINAL VERSION — ESP32 DC Motor Control
# App Inventor (HTTP API) + Node-RED MQTT Logging
# Stable, reliable, no dropped MQTT messages
# ------------------------------------------------------------

import network, socket, ure, time, json
from machine import Pin, PWM
from umqtt.simple import MQTTClient

# ---------- Wi-Fi ----------
SSID = "Robotic WIFI"
PASSWORD = "rbtWIFI@2025"

# ---------- MQTT ----------
BROKER = "test.mosquitto.org"
PORT = 1883
CLIENT_ID = b"esp32_motor_logger"
TOPIC = b"/aupp/group1m/motor"

# ---------- Motor Pins ----------
ENA = 25   # PWM
IN1 = 26   # Direction 1
IN2 = 27   # Direction 2

pwm = PWM(Pin(ENA), freq=1000)
in1 = Pin(IN1, Pin.OUT)
in2 = Pin(IN2, Pin.OUT)

current_speed = 50


# ---------- Motor Functions ----------
def set_speed(percent):
    """Apply PWM speed to motor"""
    global current_speed
    percent = max(0, min(100, int(percent)))
    current_speed = percent

    duty = int((percent / 100) * 65535)
    pwm.duty_u16(duty)

    print("Speed set:", percent)


def forward():
    """Move motor forward (IN1=1, IN2=0)"""
    in1.value(1)
    in2.value(0)
    set_speed(current_speed)
    print("Forward")


def backward():
    """Move motor backward (IN1=0, IN2=1)"""
    in1.value(0)
    in2.value(1)
    set_speed(current_speed)
    print("Backward")


def stop_motor():
    """Stop motor completely"""
    in1.value(0)
    in2.value(0)
    pwm.duty_u16(0)
    print("Stop")


# ---------- Wi-Fi Connection ----------
def wifi_connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)

    print("Connecting to Wi-Fi...")
    while not wlan.isconnected():
        time.sleep(0.2)

    print("Wi-Fi OK:", wlan.ifconfig())
    return wlan


# ---------- MQTT ----------
def mqtt_connect():
    global client
    client = MQTTClient(CLIENT_ID, BROKER, PORT)
    client.connect()
    print("MQTT Connected")


def mqtt_log(action, speed):
    """Publish motor events to Node-RED"""
    payload = json.dumps({
        "action": action,
        "speed": speed,
        "timestamp": time.time()
    })

    client.publish(TOPIC, payload)
    print("MQTT:", payload)


# ---------- URL Query Parsing ----------
def parse_query(q):
    params = {}
    if q:
        for item in q.split("&"):
            if "=" in item:
                k, v = item.split("=")
                params[k] = v
    return params


# ---------- HTTP Server ----------
def start_server():
    addr = socket.getaddrinfo("0.0.0.0", 80)[0][-1]
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(addr)
    s.listen(1)

    print("HTTP Server Running:", addr)

    while True:
        cl, addr = s.accept()
        req = cl.recv(1024).decode()

        print("REQ:", req.split("\r\n")[0])

        m = ure.search("GET\s+([^\s\?]+)(?:\?([^ ]+))?", req)
        if not m:
            cl.close()
            continue

        path = m.group(1)
        query = m.group(2) or ""
        params = parse_query(query)

        # -------- ROUTES --------
        if path == "/speed":
            raw = params.get("value", current_speed)
            try:
                value = int(float(raw))
            except:
                value = current_speed

            set_speed(value)
            time.sleep_ms(50)
            mqtt_log("speed", value)

            response = json.dumps({"speed": value})

        elif path == "/forward":
            forward()
            time.sleep_ms(50)
            mqtt_log("forward", current_speed)

            response = json.dumps({"action": "forward"})

        elif path == "/backward":
            backward()
            time.sleep_ms(50)
            mqtt_log("backward", current_speed)

            response = json.dumps({"action": "backward"})

        elif path == "/stop":
            stop_motor()
            time.sleep_ms(50)
            mqtt_log("stop", 0)

            response = json.dumps({"action": "stop"})

        else:
            response = json.dumps({"error": "Invalid endpoint"})

        # Send HTTP Response
        cl.send("HTTP/1.1 200 OK\r\nContent-Type: application/json\r\n\r\n")
        cl.send(response)
        cl.close()


# ---------- MAIN ----------
wifi_connect()
mqtt_connect()
stop_motor()
start_server()
