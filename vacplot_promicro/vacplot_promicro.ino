//#include <RingBuf.h>


void setup() {
  // start serial port at 115200 bps and wait for port to open:
  Serial.begin(115200);
  while (!Serial) {
    ; // wait for serial port to connect. Needed for native USB port only
  }
}

unsigned int p = 0;
unsigned long int ts = 0;

void loop() {
  // put your main code here, to run repeatedly:
  p = analogRead(A0); //yields 10 bits of useful information
  while (p > 920) {
    delay(1);
    p = analogRead(A0);
  }
  ts = micros();
  Serial.print(p);
  Serial.print(", ");
  Serial.print(ts);
  Serial.print('\n');
  delay(2);

}
