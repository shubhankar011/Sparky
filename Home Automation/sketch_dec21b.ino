#include <DHT.h>
#include <SoftwareSerial.h>

// HC-05 TX ->  D2, HC-05 RX ->  D3
#define BT_RX 2
#define BT_TX 3
SoftwareSerial myBT(BT_RX, BT_TX);

const int relayPin = 13;
const int relayPin2 = 12  ;
const int pirPIN = 10;
const int DHT_PIN = 11;
// static int
// Define the sensor type as DHT11
#define DHTTYPE DHT11
DHT dht(DHT_PIN, DHTTYPE);

unsigned long previousMillis = 0;
const long interval = 2000;
// char command = 0;
String command = "";
float temperature;
void setup()
{
  Serial.begin(9600);

  pinMode(pirPIN, INPUT);
  dht.begin();
  Serial.println("System starting up... Calibrating PIR.");
  delay(2000); // Standard PIR warmup delay

  pinMode(relayPin, OUTPUT);
  digitalWrite(relayPin, LOW);
  pinMode(relayPin2, OUTPUT);
  digitalWrite(relayPin2, LOW);
  myBT.begin(9600);
  myBT.println("System Ready. Connect via App and send '1' for ON.");
  Serial.println("System Ready. Connect via App and send '1' for ON.");
}

void loop()
{
  // 1. CONSTANTLY CHECK PIR FOR MOTION

  int motionState = digitalRead(pirPIN);

  if (motionState == HIGH)
  {
    Serial.println("[ALERT] Motion Detected!");
    myBT.println("[ALERT] Motion Detected!");
    delay(200);
  }
  unsigned long currentMillis = millis();
  if (currentMillis - previousMillis >= interval)
  {
    previousMillis = currentMillis;
    // Read humidity and temperature values
    float humidity = dht.readHumidity();
    temperature = dht.readTemperature();
    // Temperature in Celsius
    // Check if the readings failed
    if (isnan(humidity) || isnan(temperature))
    {
      Serial.println("[ERROR] Failed to read from DHT11 sensor!");
      myBT.println("[ERROR] Failed to read from DHT11 sensor!");
    }
    else
    {
      // Stream data cleanly to the Serial Monitor
      Serial.print("Environment -> Temp: ");
      Serial.print(temperature);
      Serial.print(" °C | Humidity: ");
      Serial.print(humidity);
      Serial.println(" %");
      // Stream data cleanly to the Bluetooth App
      myBT.print("Env -> Temp: ");
      myBT.print(temperature);
      myBT.print(" C | Hum: ");
      myBT.print(humidity);
      myBT.println(" %");
    }
  }
  // 2. CHECK BLUETOOTH COMMANDS
  if (myBT.available())
  {
    command = myBT.readStringUntil('\n');
    command.trim();

    Serial.print("Received: ");
    Serial.println(command);

    if (command == "LIGHT_ON")
    {
      digitalWrite(relayPin, HIGH);
      myBT.println("LIGHT_ON_OK");
      Serial.println("Light ON");
    }

    else if (command == "LIGHT_OFF")
    {
      digitalWrite(relayPin, LOW);
      myBT.println("LIGHT_OFF_OK");
      Serial.println("Light OFF");
    }

    else if (command == "FAN_ON")
    {
      digitalWrite(relayPin2, HIGH);
      myBT.println("FAN_ON_OK");
      Serial.println("Fan ON");
    }

    else if (command == "FAN_OFF")
    {
      digitalWrite(relayPin2, LOW);
      myBT.println("FAN_OFF_OK");
      Serial.println("Fan OFF");
    }
    else if (command == "GET_TEMPERATURE")
    {
      if (isnan(temperature))
      {
        Serial.println("TEMP_ERROR");
      }
      else
      {
        Serial.print("TEMP:");
        Serial.println(temperature);
      }
    }
    else
    {
      myBT.println("UNKNOWN_COMMAND");
      Serial.print("Unknown command: ");
      Serial.println(command);
    }
  }
  if (Serial.available())
  {
    command = Serial.readStringUntil('\n');
    command.trim();

    Serial.print("Received: ");
    Serial.println(command);

    if (command == "LIGHT_ON")
    {
      digitalWrite(relayPin, HIGH);
      myBT.println("LIGHT_ON_OK");
      Serial.println("Light ON");
    }

    else if (command == "LIGHT_OFF")
    {
      digitalWrite(relayPin, LOW);
      myBT.println("LIGHT_OFF_OK");
      Serial.println("Light OFF");
    }

    else if (command == "FAN_ON")
    {
      digitalWrite(relayPin2, HIGH);
      myBT.println("FAN_ON_OK");
      Serial.println("Fan ON");
    }

    else if (command == "FAN_OFF")
    {
      digitalWrite(relayPin2, LOW);
      myBT.println("FAN_OFF_OK");
      Serial.println("Fan OFF");
    }
    else if (command == "GET_TEMPERATURE")
    {
      if (isnan(temperature))
      {
        Serial.println("TEMP_ERROR");
      }
      else
      {
        Serial.print("TEMP:");
        Serial.println(temperature);
      }
    }
    else
    {
      myBT.println("UNKNOWN_COMMAND");
      Serial.print("Unknown command: ");
      Serial.println(command);
    }
  }
}

// const int pirPIN = 13;

// void setup() {
//   Serial.begin(9600);
//   pinMode(pirPIN, INPUT);
//   delay(20000);
// }

// void loop() {
//   Serial.println(digitalRead(pirPIN));
//   delay(200);
// }
// void setup() {
//   pinMode(13, OUTPUT);
//   pinMode(10, OUTPUT);

//   digitalWrite(13, LOW);
//   digitalWrite(10, LOW);
// }

// void loop() {
//   digitalWrite(13, HIGH);
//   digitalWrite(10, LOW);
//   delay(2000);

//   digitalWrite(13, LOW);
//   digitalWrite(10, HIGH);
//   delay(2000);
// }