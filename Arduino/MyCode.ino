#include <ESP8266WiFi.h>
#include <PubSubClient.h>

// Network credentials
const char* ssid = "?";
const char* password ="?";
const char* mqtt_username = "mqtt";
const char* mqtt_password = "mqtt";


// MQTT broker address
const char* mqtt_server = "192.168.191.3";

// Initializing the WiFi and MQTT clients
WiFiClient DiabetesPredictor20231;
PubSubClient client(DiabetesPredictor20231);

void setup() {
  // Serial communication for debugging purposes
  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, HIGH);
  Serial.begin(9600);

  // Connecting to Wi-Fi
  Serial.println();
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println(WiFi.localIP());
  Serial.println('\n');
  
  // Connecting to MQTT broker
  client.setServer(mqtt_server, 1883);
  while (!client.connected()) {
    Serial.print("Connecting to MQTT broker...");
    if (client.connect("DiabetesPredictor2023",mqtt_username, mqtt_password)) {
      Serial.println("connected");
      //client.subscribe("GetData2023", 2);
    } else {
      Serial.print("failed with state ");
      Serial.print(client.state());
      Serial.print("\n");
      delay(2000);
    }
  }
}

void loop() {
  
  // Generating a two-digit random number and convert it to a string
  int random_num = random(10, 100);
  String payload = String(random_num);

  // Publishing the payload to the MQTT topic
  client.publish("GetData2023", payload.c_str());
  
    
                         
  digitalWrite(LED_BUILTIN, LOW);
  Serial.print("Published: ");
  Serial.println(payload);
  delay(400);
  digitalWrite(LED_BUILTIN, HIGH);
    
  
  // Printing the payload and wait for 10 seconds before publishing again
  
  delay(10000);
}
