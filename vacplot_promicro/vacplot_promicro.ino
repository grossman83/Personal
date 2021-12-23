void setup() {
  // start serial port at 115200 bps and wait for port to open:
  Serial.begin(115200);
  while (!Serial) {
    ; // wait for serial port to connect. Needed for native USB port only
  }
}


float count2kpa(int adc_count){
  return (0.92 - adc_count/1023.0) / 0.007652;
}

unsigned int adc0 = 0;
unsigned long int ts = 0;

void loop() {
  // put your main code here, to run repeatedly:
  adc0 = analogRead(A0); //yields 10 bits of useful information
  ts = micros();

//  while (adc0 > 920){
//    Serial.print(ts);
//    Serial.print(", ");
//    Serial.print(0);
//    Serial.print('\n');
//    delay(2);
//    adc0 = analogRead(A0);
//  }
//  
  Serial.print(ts);
  Serial.print(", ");
  Serial.print(count2kpa(adc0));
  Serial.print('\n');
  delay(2);
}
