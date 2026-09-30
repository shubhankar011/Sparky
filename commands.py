import json
import sparky_SystemPrompt as sparky
import live_snap
import serial, time
# livestr.start_vision_thread()
arduino = serial.Serial("COM3", 9600, timeout=1)
with open('commands_desc.json','r') as f:
    COMMANDS = json.load(f)
def send_command(command):
    arduino.write((command + "\n").encode())
    print("Arduino ←", command)
# print(COMMANDS)
# def execute_command(data):
    
def LIGHT_ON(location=None):
    print(f"Turning ON light: {location or 'default'}")
    send_command("LIGHT_ON")

    # ESP32 code here


def light_off(location=None):
    print(f"Turning OFF light: {location or 'default'}")
    send_command("LIGHT_OFF")

    # ESP32 code here


def fan_on(location=None):
    print(f"Turning ON fan: {location or 'default'}")
    send_command("FAN_ON")
    # ESP32 code here


def fan_off(location=None):
    print(f"Turning OFF fan: {location or 'default'}")
    send_command("FAN_OFF")
    # ESP32 code here


def detect_object(target=None):
    print(f"Detecting: {target or 'objects'}")
    # YOLO code here
    print("Detecting objects...")
    objects = live_snap.detect_objects_once()

    if target:
        message = f"Yes, I can see a {target}." if target.lower() in [o.lower() for o in objects] \
            else f"I don't see a {target} right now."
    else:
        message = "I can see " + ", ".join(objects) + "." if objects else "I don't see anything right now."

    print(message)
    sparky.speak(message)


def identify_person(target=None):
    print(f"Identifying: {target or 'person'}")
    # DeepFace code here
    people = live_snap.identify_people_once()
    known = [p for p in people if p != "Unknown"]

    if target:
        message = f"Yes, {target} is here." if target in known else f"I don't see {target} right now."
    elif known:
        message = "I can see " + ", ".join(known) + "."
    elif people:
        message = "There's someone here, but I don't recognize them."
    else:
        message = "I don't see anyone right now."

    print(message)
    sparky.speak(message)


def take_photo():
    print("Taking photo...")
    # OpenCV camera code here


def move_forward(duration=None):
    print(f"Moving forward: {duration or 'default'}")
    # Motor code here


def move_backward(duration=None):
    print(f"Moving backward: {duration or 'default'}")
    # Motor code here


def turn_left():
    print("Turning left")
    # Motor code here


def turn_right():
    print("Turning right")
    # Motor code here


def stop():
    print("Stopping")
    # Motor code here


def get_temperature():
    print("Reading temperature...")
    send_command("GET_TEMPERATURE")

    response = arduino.readline().decode().strip()
    start = time.time()
    while time.time() - start < 2:  # give it up to 2 seconds
        response = arduino.readline().decode(errors='ignore').strip()
        if not response:
            continue
        print(f"Raw response: '{response}'")
        if response.startswith("TEMP:"):
            temperature = response.split(":")[1]
            print(f"Temperature: {temperature} °C")
            sparky.speak(f"Temperature is {temperature} degree Celsius")
            return
    


def check_distance():
    print("Checking distance...")
    # HC-SR04 code here


def check_light():
    print("Checking light level...")
    # LDR code here


def SAY(text):
    print(f"Going to Sparky...")
    sparky.speak("Sparky here")


# -------------------------
# Command router
# -------------------------

COMMAND_HANDLERS = {
    "LIGHT_ON": LIGHT_ON,
    "LIGHT_OFF": light_off,

    "FAN_ON": fan_on,
    "FAN_OFF": fan_off,

    "DETECT_OBJECT": detect_object,
    "IDENTIFY_PERSON": identify_person,
    "TAKE_PHOTO": take_photo,

    "MOVE_FORWARD": move_forward,
    "MOVE_BACKWARD": move_backward,
    "TURN_LEFT": turn_left,
    "TURN_RIGHT": turn_right,
    "STOP": stop,

    "GET_TEMPERATURE": get_temperature,
    "CHECK_DISTANCE": check_distance,
    "CHECK_LIGHT": check_light,

    "SAY": SAY
}


def execute_command(data):
    command = data["command"]
    parameters = data.get("parameters", {})

    handler = COMMAND_HANDLERS.get(command)
    print("Parameters:", parameters)

    if handler is None:
        print("Unknown command:", command)
        return

    handler(**parameters)
