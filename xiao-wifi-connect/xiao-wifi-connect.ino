#include <WiFi.h>
// #include "CircularBuffer.hpp"

const char* ssid     = "BigLukeNetwork";
const char* password = "lukethedog";

const int array_length = 1000;
const float a0_middle = 1062;
const float int2mV = 0.805664;
const float middlemV = 3.3/2.0;

float Analog0 = 0;
float Analog1 = 0;
float Analog2 = 0;
float Analog3 = 0;

// CircularBuffer<uint8_t, fast_buf_length> fast_buffer;
// CircularBuffer<double, 1000> A0_buffer;

void setup()
{
    Serial.begin(115200);
    delay(10);

    // We start by connecting to a WiFi network

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
    Serial.println("IP address: ");
    Serial.println(WiFi.localIP());

    pinMode(A0, INPUT); //ADC
    pinMode(A1, INPUT);
    pinMode(A2, INPUT);
    pinMode(A3, INPUT);
    pinMode(D7, OUTPUT);
}  


double readAnalog(){
  float a1_array[array_length];

  digitalWrite(D7, HIGH);
  for(int k=0; k<array_length; k++){
    a1_array[k] = analogReadMilliVolts(A1)/1000.0;
  }
  digitalWrite(D7, LOW);

  //now for the RMS part
  double a0_rms = 0;
  double a1_rms = 0;
  double a2_rms = 0;
  double a3_rms = 0;
  for(int k=0; k<array_length; k++){
    a1_rms = a1_rms + pow(a1_array[k]-middlemV, 2);
  }
  a1_rms = a1_rms/array_length;

  a1_rms = sqrt(a1_rms);

  return a1_rms;
}



void loop()
{
  digitalWrite(D7, HIGH);
  Analog0 = analogRead(A0);
  Analog1 = readAnalog();
  Analog2 = analogRead(A2);
  Analog3 = analogRead(A3);



  // Serial.println(Analog0);
  Serial.println(Analog1);
  // Serial.println(Analog2);
  // Serial.println(Analog3);


  delay(10);
  digitalWrite(D7, LOW);
  delay(10);
}