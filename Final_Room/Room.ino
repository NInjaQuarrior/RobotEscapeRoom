/*
 *  File Created By:  Grace O'Reilly
 *  This sketch demonstrates how to scan WiFi networks.
 *  The API is almost the same as with the WiFi Shield library,
 *  the most obvious difference being the different file you need to include:
 */

#include "WiFi.h"
#include <PubSubClient.h>
// #include "analogWrite.h"

const int yellowLED = 14;
const int redLED = 27;
const int blueLED = 22;
int brightnessY; // The value read by the photoresistor
int brightnessR;
int brightnessB;
bool redOn;
bool blueOn;
bool yellowOn;

int count;

const int AIN1 = 36;
const int AIN2 = 37;
const int PWMA = 26;

// --- MQTT Setup ---
const int httpPort = 80;
const char *ssid = "WPI-Open";
const char *password = NULL;
const char *ID = "room_mqtt";
const char *mqtt_server = "mqtt.eclipseprojects.io";

WiFiClient wclient;
PubSubClient client(wclient);

void wifi_setup()
{
  Serial.print("Connecting to ");
  Serial.println(ssid);

  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED)
  {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());

  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);
  sub("website/status");
}
// --- MQTT Setup Ends ---

void setup()
{
  Serial.begin(115200);

  // pinMode(LED_BUILTIN, OUTPUT);
  pinMode(yellowLED, OUTPUT);
  pinMode(redLED, OUTPUT);
  pinMode(blueLED, OUTPUT);

  pinMode(AIN1, OUTPUT);
  pinMode(AIN2, OUTPUT);
  pinMode(PWMA, OUTPUT);

  redOn = false;
  blueOn = false;
  yellowOn = false;
  count = 0;

  wifi_setup();
  check_connection();
  pub("room/puzzle", "1");

  // Serial.println("Setup done");
}

bool simonRed()
{
  brightnessR = analogRead(33);   // Read the brightness
  brightnessR = brightnessR / 16; // Adjust the brightness value
  Serial.print("Red");
  Serial.println(brightnessR);
  if (brightnessR < 200 && redOn == false)
  {
    // Serial.println("Flashing RED");
    digitalWrite(redLED, LOW); // turn off light
    delay(500);
    digitalWrite(redLED, HIGH); // turn on the LED
    delay(500);                 // wait for half a second or 500 milliseconds
    digitalWrite(redLED, LOW);  // turn off the LED
    delay(500);                 // wait for half a second or 500 milliseconds
  }
  else
  {
    digitalWrite(redLED, HIGH); // turn on light
    delay(10);                  // Wait 10 ms//digitalWrite (ledPin2, HIGH);
    // Serial.println("RED FOUND");
    redOn = true;
    return true;
  }
  return false;
}

bool simonBlue()
{
  if (redOn == true && blueOn == false)
  {
    brightnessB = analogRead(34);
    brightnessB = brightnessB / 16;
    Serial.println("Brightness B: " + brightnessB);
    if (brightnessB < 200)
    {
      // Serial.println("Flash BLUE");
      digitalWrite(blueLED, LOW); // turn off light
      delay(500);
      digitalWrite(blueLED, HIGH); // turn on the LED
      delay(500);                  // wait for half a second or 500milliseconds
      digitalWrite(blueLED, LOW);  // turn off the LED
      delay(500);                  // wait for half a second or 500milliseconds
    }
    else
    {
      digitalWrite(blueLED, HIGH);
      delay(10);
      // Serial.println("BLUE FOUND");
      blueOn = true;
      return true;
    }
  }
  return false;
}

bool simonYellow()
{
  if (blueOn == true && yellowOn == false)
  {
    brightnessY = analogRead(35);
    brightnessY = brightnessY / 16;
    Serial.print("Brightness Y: ");
    // Serial.println(brightnessY);
    if (brightnessY < 200)
    {
      // Serial.println("YELLOW FLASH");
      digitalWrite(yellowLED, LOW); // turn off light
      delay(500);
      digitalWrite(yellowLED, HIGH); // turn on the LED
      delay(500);                    // wait for half a second or 500 milliseconds
      digitalWrite(yellowLED, LOW);  // turn off the LED
      delay(500);                    // wait for half a second or 500 milliseconds
    }
    else
    {
      // Serial.println("FOUND YELLOW");
      digitalWrite(yellowLED, HIGH);
      delay(10);
      yellowOn = true;
      return true;
    }
  }
  return false;
}

bool simon()
{
  // Serial.println("START RED");
  if (redOn == false)
  {
    simonRed();
  }
  // Serial.println("END RED");
  // Serial.println("START BLUE");
  if (blueOn == false)
  {
    simonBlue();
  }
  // Serial.println("END BLUE");
  // Serial.println("START YELLOW");
  if (yellowOn == false)
  {
    simonYellow();
  }
  else
  {
    pub("room/puzzle", "2");
    delay(10000);
    // sleep for 10 seconds (place holder)
  }
  // Serial.println("END YELLOW");
  // door();

  return true;
}

void loop()
{
  // Serial.println("HIHI");
  check_connection();
  simon();
  delay(100);
  // door();

  // analogWrite (yellowLED, brightness); // Put the value read for the LED
}

/************************ MQTT Methods ************************/
void pub(const char *topic, char *msg)
{
  client.publish(topic, msg);
}
void sub(const char *topic)
{
  client.subscribe(topic);
}

void reconnect()
{
  char *recn = "connecting...";
  while (!client.connected())
  {
    Serial.print("Attempting MQTT connection...");
    // Attempt to connect
    if (client.connect(ID))
    {
      // Write ALL Subscribers
      sub("website/status");
      pub("room/puzzle", "1");
    }
    else
    {
      WiFi.disconnect();
      WiFi.reconnect();
      Serial.println(" try again in 5 seconds");
      // Wait 5 seconds before retrying
      delay(5000);
    }
  }
}

void check_connection()
{
  if (!client.connected())
  {
    reconnect();
  }
  client.loop();
}

/* Handles ALL Subscribers */
void callback(char *topic, byte *message, unsigned int length)
{
  String messageTemp;

  for (int i = 0; i < length; i++)
  {
    messageTemp += (char)message[i];
  }

  Serial.println(messageTemp);

  if (messageTemp == "rotate puzzle completed.")
  {
    Serial.println("we want to open the door!");
  }
}
/*************************************************************/