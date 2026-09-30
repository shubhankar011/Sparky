# Sparky

### AI-Assisted Smart Robotic System

**Sparky** is an AI-powered robotic assistant designed to combine **artificial intelligence, computer vision, sensor data, home automation, and physical robotics** into a single modular system.

The goal is simple:

> **See → Sense → Understand → Decide → Act**

Sparky uses a computer as its intelligence layer while communicating with external microcontrollers, sensors, cameras, and actuators. This architecture allows the intelligence and hardware layers to evolve independently.

---

## Features

### AI Assistant

* Natural-language interaction
* LLM-powered responses using **Qwen via Groq**
* Concise and context-aware personality
* Text-to-speech using `pyttsx3`
* Speech recognition support
* Modular system prompt

### Computer Vision

Sparky's vision system combines multiple computer-vision components:

* Real-time camera input
* **OpenCV** image processing
* **YOLO** object detection
* Face detection
* Face recognition using **DeepFace**
* Basic person profiling
* Persistent face tracking between frames
* Web-based live camera streaming

### Command Intelligence

Instead of relying entirely on large `if/else` chains, Sparky uses a structured command architecture.

Commands are defined in:

```text
commands_desc.json
```

The system can classify natural-language requests into structured commands such as:

```text
LIGHT_ON
LIGHT_OFF
FAN_ON
FAN_OFF

MOVE_FORWARD
MOVE_BACKWARD
TURN_LEFT
TURN_RIGHT
STOP

DETECT_OBJECT
IDENTIFY_PERSON
TAKE_PHOTO

GET_TEMPERATURE
CHECK_DISTANCE
CHECK_LIGHT

SAY
```

This makes it easier to add new capabilities without redesigning the entire command system.

---

## Architecture

```text
                    ┌─────────────────────┐
                    │      USER INPUT     │
                    │ Voice / Text / Web  │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │    AI / LLM Layer   │
                    │   Qwen + Groq API   │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Command Classifier  │
                    │                     │
                    │ Natural Language →  │
                    │ Structured Command  │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Command Registry    │
                    │ commands_desc.json  │
                    └──────────┬──────────┘
                               │
                               ▼
             ┌─────────────────┴─────────────────┐
             │                                   │
             ▼                                   ▼
    ┌──────────────────┐               ┌──────────────────┐
    │ Computer Vision  │               │ Hardware Control │
    │                  │               │                  │
    │ OpenCV           │               │ Arduino / ESP    │
    │ YOLO             │               │ Sensors          │
    │ DeepFace         │               │ Motors           │
    │ Camera           │               │ Relays           │
    └──────────────────┘               └──────────────────┘
```

The system is intentionally modular. Vision, intelligence, command processing, web streaming, and hardware control can be developed independently.

---

## Project Structure

```text
Sparky/
│
├── classifier.py
│   └── Command classification and execution pipeline
│
├── commands.py
│   └── Hardware/action command handlers
│
├── commands_desc.json
│   └── Structured command definitions and examples
│
├── sparky_SystemPrompt.py
│   └── AI assistant, speech recognition and text-to-speech
│
├── registering.py
│   └── Face registration utilities
│
├── livestreaming.py
│   └── Camera, object detection and face-recognition pipeline
│
├── live_snap.py
│   └── Camera snapshot functionality
│
├── webServer.py
│   └── Flask server for browser-based camera streaming
│
├── templates/
│   └── Web interface templates
│
├── static/
│   └── Static web assets
│
├── gen.py
│   └── Competition presentation generator
│
└── .gitignore
```

---

# Technology Stack

| Component               | Technology                      |
| ----------------------- | ------------------------------- |
| Programming             | Python                          |
| AI / LLM                | Qwen via Groq                   |
| Computer Vision         | OpenCV                          |
| Object Detection        | YOLO                            |
| Face Recognition        | DeepFace                        |
| Web Server              | Flask                           |
| Text-to-Speech          | pyttsx3                         |
| Speech Recognition      | SpeechRecognition               |
| Hardware                | Arduino / ESP-based controllers |
| Command Definition      | JSON                            |
| Presentation Generation | python-pptx                     |

---

## Vision System

Sparky's vision pipeline processes camera frames and combines object detection with face recognition.

### Object Detection

YOLO is used to identify objects in the camera feed.

Conceptually:

```text
Camera
   │
   ▼
OpenCV Frame
   │
   ▼
YOLO
   │
   ▼
Detected Objects
```

### Face Recognition

The face pipeline tracks detected faces and assigns temporary IDs so that expensive recognition operations don't have to be performed on every frame.

```text
Camera Frame
     │
     ▼
Face Detection
     │
     ▼
Face Tracking
     │
     ▼
Face ID
     │
     ▼
DeepFace
     │
     ▼
Known Person / Unknown
```

Recognition work is performed asynchronously to keep the camera pipeline responsive.

---

# AI Command System

Sparky separates **understanding what the user wants** from **executing the action**.

For example:

```text
User:
"Turn on the lights"

        ↓

AI / Classifier

        ↓

{
    "command": "LIGHT_ON",
    "parameters": {}
}

        ↓

Command Handler

        ↓

Hardware
```

The command definitions are stored in `commands_desc.json`.

This approach makes the system easier to extend.

Adding a new capability can involve:

1. Defining the command.
2. Adding example phrases.
3. Implementing its handler.
4. Connecting the handler to the appropriate hardware or software module.

---

# Camera Web Streaming

Sparky includes a Flask-based camera server.

Run:

```bash
python webServer.py
```

The server provides:

```text
http://127.0.0.1:5000
```

and can also be accessed from another device on the same network using the computer's local IP address:

```text
http://<YOUR-LAPTOP-IP>:5000
```

The web server streams the processed camera feed rather than simply serving a static image.

---

# Installation

Clone the repository:

```bash
git clone https://github.com/shubhankar011/Sparky.git
cd Sparky
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows:

```bash
.venv\Scripts\activate
```

Install the required Python packages according to the modules you intend to use.

Typical dependencies include:

```bash
pip install opencv-python
pip install flask
pip install ultralytics
pip install deepface
pip install groq
pip install python-dotenv
pip install pyttsx3
pip install SpeechRecognition
pip install python-pptx
```

Some features may require additional system-level dependencies.

---

# Environment Variables

Sparky uses environment variables for API credentials.

Create a `.env` file:

```env
GROQ_API_KEY=your_api_key_here
```

**Do not commit your `.env` file or API keys to GitHub.**

---

# Running Sparky

## AI Assistant

Run:

```bash
python sparky_SystemPrompt.py
```

The current implementation accepts text input for debugging while retaining the speech-recognition and speech-output components.

---

## Vision System

Run:

```bash
python livestreaming.py
```

The vision pipeline can process the camera feed using OpenCV, YOLO and face recognition.

---

## Web Vision Interface

Run:

```bash
python webServer.py
```

Then open:

```text
http://127.0.0.1:5000
```

---

# Hardware Integration

Sparky is designed to communicate with external microcontrollers for physical actions.

Potential hardware modules include:

* Arduino
* ESP8266 / ESP32
* DC motors
* Motor drivers
* Servo motors
* Ultrasonic distance sensors
* PIR sensors
* DHT11 temperature/humidity sensors
* LDR/light sensors
* Relays
* Displays
* Cameras

A typical hardware loop is:

```text
AI Command
     │
     ▼
Command Classifier
     │
     ▼
Command Handler
     │
     ▼
Microcontroller
     │
     ├── Sensors
     ├── Motors
     ├── Relays
     └── Other Actuators
```

Hardware integration is being developed independently from the PC-side intelligence layer.

---

# Design Philosophy

Sparky is built around a few principles.

### Modular

Each major capability should be replaceable without rewriting the entire project.

### Structured

AI-generated decisions should be converted into predictable commands before reaching hardware.

### Extensible

New commands, sensors and hardware should be addable without creating a huge collection of hard-coded conditions.

### Computer + Hardware

The computer handles computationally expensive tasks such as:

* AI reasoning
* Computer vision
* Face recognition
* Command interpretation

Microcontrollers handle:

* Sensor reading
* Motor control
* Relays
* Real-time hardware operations

---

# Current Development Status

Sparky is an active prototype.

### Working / Developed

* [x] AI assistant integration
* [x] Groq/Qwen integration
* [x] Structured command definitions
* [x] Command classification architecture
* [x] OpenCV camera processing
* [x] YOLO object detection integration
* [x] Face detection
* [x] Face recognition pipeline
* [x] Face tracking
* [x] Flask camera streaming
* [x] Camera web interface
* [x] Arduino-based home-automation experiments
* [x] Sensor experiments

### In Development

* [ ] Complete robot chassis
* [ ] Motor-control integration
* [ ] Full sensor integration
* [ ] Closed-loop AI → hardware control
* [ ] Improved safety layer
* [ ] Unified Sparky application
* [ ] More robust voice interaction
* [ ] Expanded computer-vision capabilities

---

# Future Roadmap

```text
Phase 1
AI + Computer Vision
        ↓
Phase 2
Command Classification
        ↓
Phase 3
Sensor Integration
        ↓
Phase 4
Motor & Actuator Control
        ↓
Phase 5
Closed-Loop Autonomous Robot
        ↓
Phase 6
Smarter Perception + Decision Making
```

Future versions of Sparky are intended to support more advanced perception, autonomous navigation, home automation, and context-aware robotic behavior.

---

# Project Goals

The long-term goal is to create a robot that can:

1. **See** its environment.
2. **Sense** physical conditions.
3. **Understand** natural-language instructions.
4. **Reason** about what needs to happen.
5. **Decide** which structured action to perform.
6. **Act** through physical hardware.
7. **Observe the result** and respond accordingly.

In other words:

> **Sparky isn't just meant to execute commands. It's being built as a complete perception → intelligence → action system.**

---

## Team

**Sparky** is being developed by:

**Shubhankar and team**

Built as a student robotics and AI project combining:

* Artificial Intelligence
* Generative AI
* Computer Vision
* IoT
* Robotics
* Home Automation

---

## Repository

**GitHub:**
https://github.com/shubhankar011/Sparky

---

## License

This project currently does not specify a license.

If you intend to allow others to freely use, modify, and distribute Sparky, consider adding an open-source license such as MIT in a future revision.
