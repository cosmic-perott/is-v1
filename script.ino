#include <WiFi.h>

const char* ssid = "";
const char* password = "";

WiFiServer server(8888); // Set up a server on port 8888

void setup() {
  Serial.begin(115200);
  
  pinMode(LEDR, OUTPUT);
  pinMode(LEDG, OUTPUT);
  pinMode(LEDB, OUTPUT);
  
  digitalWrite(LEDR, HIGH);
  digitalWrite(LEDG, HIGH);
  digitalWrite(LEDB, HIGH);

  // Connect to your Wi-Fi router
  WiFi.begin(ssid, password);
  Serial.print("Connecting to WiFi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  
  Serial.println("\nWiFi connected!");
  Serial.print("ESP32 IP Address: ");
  Serial.println(WiFi.localIP()); // Look for this IP in the Serial Monitor!

  server.begin();
}

void loop() {
  WiFiClient client = server.available(); // Listen for your Mac
  if (client) {
    while (client.connected()) {
      if (client.available()) {
        String line = client.readStringUntil('\n');
        line.trim();
        Serial.println("Received wirelessly: [" + line + "]");

        // Change LED color based on letter
        if (line == "A") {
          setColor(LOW, HIGH, HIGH); // Red
        } else if (line == "B") {
          setColor(HIGH, HIGH, LOW); // Blue
        } else if (line == "C") {
          setColor(HIGH, LOW, HIGH); // Green
        } else if (line == "D") {
          setColor(LOW, LOW, HIGH);  // Yellow
        }
      }
    }
    client.stop();
  }
}

void setColor(bool r, bool g, bool b) {
  digitalWrite(LEDR, r);
  digitalWrite(LEDG, g);
  digitalWrite(LEDB, b);
}
