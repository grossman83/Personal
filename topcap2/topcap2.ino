#include "HX711.h"

// HX711 circuit wiring
const int LOADCELL1_DOUT_PIN = 22;
const int LOADCELL1_SCK_PIN = 23;

const int LOADCELL2_DOUT_PIN = 2;
const int LOADCELL2_SCK_PIN = 3;

HX711 scale1;
HX711 scale2;

void setup() {
  Serial.begin(115200);
  scale1.begin(LOADCELL1_DOUT_PIN, LOADCELL1_SCK_PIN, 32);
  scale2.begin(LOADCELL2_DOUT_PIN, LOADCELL2_SCK_PIN, 32);
  
}

void loop() {

  float mV1 = 0;
  float N1 = 0;
  float mV2 = 0;
  float N2 = 0;
  
  if (scale1.is_ready()) {
    long reading1 = scale1.read();
    mV1 = reading1 / 2040;
    N1 = mV1/7.402/32.0;
  }

  if (scale2.is_ready()) {
    long reading2 = scale2.read();
    mV2 = reading2 / 2040;
    N2 = mV2/7.402/32.0;
  }

  if(N1 != 0 && N2 !=0){
    Serial.print(N1);
    Serial.print(", ");
    Serial.println(N2);
  }

  delay(20);

  //8,388,607
}
