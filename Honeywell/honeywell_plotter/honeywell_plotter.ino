//#include <Serial.h>

int analogPin = 18;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(19200);

}

void loop() {
  // put your main code here, to run repeatedly:
  int adcval = 0;
  while(1){
    adcval = analogRead(analogPin);
    Serial.println(adcval);
    delay(10);
  }

}
