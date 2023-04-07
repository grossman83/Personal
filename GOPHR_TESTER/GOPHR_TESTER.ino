#include <Arduino.h>

int red = 23;
int green = 22;

float m_24V = A0; // pin to measure 24V
float m_5V = A1; // pin to measure 5V
float m_4V5 = A2; // measure 4.5V
float V24 = 0;
float V5 = 0;
float V4v5 = 0;

float touchsens = A3;
float m_touch = 0;
float o_touch = 0;

int var = 1;
int i = 0;

int ledctl0 = 5;
int ledctl1 = 4;
int ledctl2 = 7;
int ledctl3 = 6;

int v_ctl1 = 9;
int v_ctl2 = 8;
int v_ctl3 = 11;
int v_ctl4 = 10;
int v_ctl5 = 13;
int v_ctl6 = 12;

int ctl1 = 14;
int ctl2 = 15;
int ctl3 = 16;
int ctl4 = 17;
int ctl5 = 18;
int ctl6 = 19;

float m_fingerprint = A4;
int fingerprint = 3;
float Fingprint = 0;

float m_VACsens = A5;
int VACsens = 2;
float vacs = 0;

int portHIGH = 0;
int portLOW = 0;
int tap_old = 0;
int tap_ok = 0;

void setup() {
  pinMode(red, OUTPUT);
  pinMode(green, OUTPUT);
  pinMode(m_24V, INPUT);
  pinMode(m_5V, INPUT);
  pinMode(m_4V5, INPUT);

  pinMode(m_fingerprint, INPUT);
  //pinMode(fingerprint, INPUT);
  pinMode(fingerprint, OUTPUT);

  pinMode(m_VACsens, INPUT);
  //pinMode(VACsens, INPUT);
  pinMode(VACsens, OUTPUT);

  pinMode(ledctl0, OUTPUT);
  pinMode(ledctl1, OUTPUT);
  pinMode(ledctl2, OUTPUT);
  pinMode(ledctl3, OUTPUT);

  pinMode(v_ctl1, OUTPUT);
  pinMode(v_ctl2, OUTPUT);
  pinMode(v_ctl3, OUTPUT);
  pinMode(v_ctl4, OUTPUT);
  pinMode(v_ctl5, OUTPUT);
  pinMode(v_ctl6, OUTPUT);

  pinMode(ctl1, INPUT);
  pinMode(ctl2, INPUT);
  pinMode(ctl3, INPUT);
  pinMode(ctl4, INPUT);
  pinMode(ctl5, INPUT);
  pinMode(ctl6, INPUT);

  pinMode(touchsens, INPUT);

  Serial.begin(9600);
}

void redled(){
  digitalWrite(green, LOW);
  digitalWrite(red, HIGH);
  }

  void greenled(){
  digitalWrite(green, HIGH);
  digitalWrite(red, LOW);
  }

void sw_case(){
  switch (var) {
    case 1:
      Serial.println("");
      Serial.println("You can start the test, please write *start* word");
      var = 0;
      break;

    case 2:
      Serial.println("Test results:");
      Serial.println("24V\t5V\t4.5V\tULN1\tULN2\tULN3\tULN4\tULN5\tULN6\tINA\tFP\tVAC\tCAN\t");
      delay(1000);
      V24 = analogRead(m_24V);
      V24 = (((V24*3.3)/1024)*11.00244498);
      //Serial.print("24V =");
      Serial.print(V24);
      Serial.print("\t");
      
      
      V5 = analogRead(m_5V);
      V5 = (((V5 * 3.3)/1024)*11.00244498);
      //Serial.print("5V =");
      Serial.print(V5);
      Serial.print("\t");
    
    
      V4v5 = analogRead(m_4V5);
      V4v5 = (((V4v5 * 3.3)/1024)*11.00244498);
      //Serial.print("4.5V =");
      Serial.print(V4v5);
      Serial.print("\t");

      if (((23 <= V24) && (V24<= 25)) && ((4 <= V5) && (V5 <= 5)) && ((4 <= V4v5) && (V4v5 <= 5))){
        var = 5;
      }
      else{
        if(23 >= V24){
          // Serial.println("***24V low***");
        }
        if(V24>= 25){
          // Serial.println("***24V high***");
        }

        if(4 >= V5){
          // Serial.println("***5V low***");
        }
        if(V5 >= 6){
          // Serial.println("***5V high***");
        }

        if(4 >= V4v5){
          // Serial.println("***4,5V low***");
        }
        if(V4v5 >= 5){
          // Serial.println("***4,5V high***");
        }

        var = 5;
      }
      break;

    case 3:
      Serial.println("");
      Serial.println("***PASS***");
      greenled();
      var = 1;
      break;

    case 4:
      Serial.println("");
      Serial.println("***FAIL***");
      redled();
      var = 1;
      break;

    case 5:
      for(i=0; i<2; i++){
        digitalWrite(ledctl0, HIGH);
        digitalWrite(ledctl1, HIGH);
        digitalWrite(ledctl2, HIGH);
        digitalWrite(ledctl3, HIGH);
        delay(200);
        digitalWrite(ledctl0, LOW);
        digitalWrite(ledctl1, LOW);
        digitalWrite(ledctl2, LOW);
        digitalWrite(ledctl3, LOW);
        delay(200);
      }
      i = 0;
      var = 6;
    break;

    case 6:
        for(int i=0; i<2; i++){
          digitalWrite(v_ctl1, HIGH);
          digitalWrite(v_ctl2, HIGH);
          digitalWrite(v_ctl3, HIGH);
          digitalWrite(v_ctl4, HIGH);
          digitalWrite(v_ctl5, HIGH);
          digitalWrite(v_ctl6, HIGH);
          delay(200);
          digitalWrite(v_ctl1, LOW);
          digitalWrite(v_ctl2, LOW);
          digitalWrite(v_ctl3, LOW);
          digitalWrite(v_ctl4, LOW);
          digitalWrite(v_ctl5, LOW);
          digitalWrite(v_ctl6, LOW);
          delay(200);
        }
        //Serial.println("ULN test:");
        
        digitalWrite(v_ctl1, LOW);
        delay(100);
        if((digitalRead(ctl1) == HIGH)){
          portHIGH = 1;
        }
        else portHIGH = 0;
        digitalWrite(v_ctl1, HIGH);
        delay(100);
        if((digitalRead(ctl1) == LOW)){
          portLOW = 1;
        }
        else portLOW = 0;

        if((portHIGH == 1) && (portLOW == 1)){
          Serial.print("OK\t");
        }
        else{
          Serial.print("FAIL\t");
        }
        digitalWrite(v_ctl1, LOW);

        //#####################################

        digitalWrite(v_ctl2, LOW);
        delay(100);
        if((digitalRead(ctl2) == HIGH)){
          portHIGH = 1;
        }
        else portHIGH = 0;
        digitalWrite(v_ctl2, HIGH);
        delay(100);
        if((digitalRead(ctl2) == LOW)){
          portLOW = 1;
        }
        else portLOW = 0;

        if((portHIGH == 1) && (portLOW == 1)){
          Serial.print("OK\t");
        }
        else{
          Serial.print("FAIL\t");
        }
        digitalWrite(v_ctl2, LOW);


        digitalWrite(v_ctl3, LOW);
        delay(100);
        if((digitalRead(ctl3) == HIGH)){
          portHIGH = 1;
        }
        else portHIGH = 0;
        digitalWrite(v_ctl3, HIGH);
        delay(100);
        if((digitalRead(ctl3) == LOW)){
          portLOW = 1;
        }
        else portLOW = 0;

        if((portHIGH == 1) && (portLOW == 1)){
          Serial.print("OK\t");
        }
        else{
          Serial.print("FAIL\t");
        }
        digitalWrite(v_ctl3, LOW);


        digitalWrite(v_ctl4, LOW);
        delay(100);
        if((digitalRead(ctl4) == HIGH)){
          portHIGH = 1;
        }
        else portHIGH = 0;
        digitalWrite(v_ctl4, HIGH);
        delay(100);
        if((digitalRead(ctl4) == LOW)){
          portLOW = 1;
        }
        else portLOW = 0;

        if((portHIGH == 1) && (portLOW == 1)){
          Serial.print("OK\t");
        }
        else{
          Serial.print("FAIL\t");
        }
        digitalWrite(v_ctl4, LOW);


        digitalWrite(v_ctl5, LOW);
        delay(100);
        if((digitalRead(ctl5) == HIGH)){
          portHIGH = 1;
        }
        else portHIGH = 0;
        digitalWrite(v_ctl5, HIGH);
        delay(100);
        if((digitalRead(ctl5) == LOW)){
          portLOW = 1;
        }
        else portLOW = 0;

        if((portHIGH == 1) && (portLOW == 1)){
          Serial.print("OK\t");
        }
        else{
          Serial.print("FAIL\t");
        }
        digitalWrite(v_ctl5, LOW);


        digitalWrite(v_ctl6, LOW);
        delay(100);
        if((digitalRead(ctl6) == HIGH)){
          portHIGH = 1;
        }
        else portHIGH = 0;
        digitalWrite(v_ctl6, HIGH);
        delay(100);
        if((digitalRead(ctl6) == LOW)){
          portLOW = 1;
        }
        else portLOW = 0;

        if((portHIGH == 1) && (portLOW == 1)){
          Serial.print("OK\t");
        }
        else{
          Serial.print("FAIL\t");
        }
        digitalWrite(v_ctl6, LOW);

        
    

      var = 7;
    break;

    case 7:
      //Serial.println("INNA test:");
      // *marc makes no sense to read touchsens 4 times with delays... and not average or anything.
      delay(100);
      o_touch = analogRead(touchsens);
      o_touch = (((o_touch*3.3)/1024)*1000);
      //Serial.print("Touch =");
      Serial.print(o_touch);
      Serial.print("\t");

      if (((760 <= o_touch) && (o_touch<= 840))){
        var = 8;
      }
      else{
        if(760 > o_touch){
          Serial.println("***Touch low***");
        }
        if(o_touch> 840){
          Serial.println("***Touch high***");
        }
        var = 8;
      }
      break;
    
    case 8:
      //digitalWrite(fingerprint, HIGH);
      //digitalWrite(VACsens, HIGH);
      delay(100);
      //Serial.println("Sens:");
      Fingprint = analogRead(m_fingerprint);
      Fingprint = ((Fingprint*3.3)/1024);
      //Serial.print("Fingerprint=");
      Serial.print(Fingprint);
      Serial.print("\t");
      delay(1000);

      // * marc: makes no sense to read 5 times and only keep the last value.
      vacs = analogRead(m_VACsens);
      vacs = ((vacs*3.3)/1024);
      //Serial.print("vacsens=");
      Serial.print(vacs);
      Serial.print("\t");
      delay(1000);

      var = 3;
      break;

    default:
      break;
  }
}

void loop() {
  sw_case();
  String buffer;
  buffer = Serial.readString();
  if (buffer == "start\r\n"){
    var = 2;
    digitalWrite(green, LOW);
    digitalWrite(red, LOW);
  }

  if(analogRead(m_4V5) >= 100){
    tap_ok = 1;
  }
  else tap_ok = 0;

  if (tap_ok == tap_old)
  {
    tap_old = tap_ok;
  }
  else {
    if (tap_ok == 1)
    {
      if (var == 0) var = 2;
      Serial.println("Auto start");
      digitalWrite(green, LOW);
      digitalWrite(red, LOW);
    }
  }
  if(tap_ok == 1) tap_old = 1; 
  else tap_old = 0;
}