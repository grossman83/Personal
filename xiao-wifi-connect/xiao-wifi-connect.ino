#include <WiFi.h>
#include <ArduinoIoTCloud.h>
#include <Arduino_ConnectionHandler.h>

const char ssid[] = "BigLukeNetwork";           // Your WiFi SSID
const char pass[] = "lukethedog";       // Your WiFi password

void setup() {
  Serial.begin(115200);
  // Attempt to connect to WiFi network:
  while (WiFi.status() != WL_CONNECTED) {
    Serial.print("Attempting to connect to WPA SSID: ");
    Serial.println(ssid);
    // Connect to WPA/WPA2 network:
    WiFi.begin(ssid, pass);
    // Wait 10 seconds for connection:
    delay(10000);
  }

  // Print WiFi status:
  Serial.println("You're connected to the network");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}

void loop() {
  // Add your repeated code here
}
