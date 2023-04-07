#include <Arduino.h>

int red = 23;
int green = 22;

float m_24V = A0; // pin to measure 24V
float m_5V = A1; // pin to measure 5V
float m_4V5 = A2; // measure 4.5V
float V24 = 0; // measured value
float V5 = 0; // measured value
float V4v5 = 0; // measured value

float touchsens = A3;
float o_touch = 0;

int var = 1;
int i = 0;

int ledctl0 = 5;
int ledctl1 = 4;
int ledctl2 = 7;
int ledctl3 = 6;


int ULN1 = 9;
int ULN2 = 8;
int ULN3 = 11;
int ULN4 = 10;
int ULN5 = 13;
int ULN6 = 12;

// bools for making sure various parts of circuit are ok
bool V24_ok = false;
bool V5_ok = false;
bool V4v5_ok = false;
bool ULN_ON_OK = false;
bool ULN_OFF_OK = false;
bool touch_ok = false;

int v1 = 14;
int v2 = 15;
int v3 = 16;
int v4 = 17;
int v5 = 18;
int v6 = 19;

bool ULN1_LOW = false;
bool ULN2_LOW = false;
bool ULN3_LOW = false;
bool ULN4_LOW = false;
bool ULN5_LOW = false;
bool ULN6_LOW = false;


//declare and initialize valve state variables
int vs1 = LOW;
int vs2 = LOW;
int vs3 = LOW;
int vs4 = LOW;
int vs5 = LOW;
int vs6 = LOW;



int fingpin = A4;
int fingvalue = 0;
//*marc appropriate range TBD


int vacpin = A5;
int vacvalue = 0;
//*marc appropriate range TBD


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


  pinMode(fingpin, INPUT);
  pinMode(vacpin, INPUT);


  pinMode(ledctl0, OUTPUT);
  pinMode(ledctl1, OUTPUT);
  pinMode(ledctl2, OUTPUT);
  pinMode(ledctl3, OUTPUT);

  pinMode(ULN1, OUTPUT);
  pinMode(ULN2, OUTPUT);
  pinMode(ULN3, OUTPUT);
  pinMode(ULN4, OUTPUT);
  pinMode(ULN5, OUTPUT);
  pinMode(ULN6, OUTPUT);

  pinMode(v1, INPUT);
  pinMode(v2, INPUT);
  pinMode(v3, INPUT);
  pinMode(v4, INPUT);
  pinMode(v5, INPUT);
  pinMode(v6, INPUT);

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

    case 2://start testing
      Serial.println("Test results:");
      Serial.println("24V\t5V\t4.5V\tULN1\tULN2\tULN3\tULN4\tULN5\tULN6\tINA\tFP\tVAC\tCAN\t");
      V24 = analogRead(m_24V);
      V24 = (((V24*3.3)/1024)*11.00244498);
      Serial.print(V24);
      Serial.print("\t");
      if(V24 > 23 && V24<25){
        V24_ok = true;
      }
      else{
        V24_ok = false;
      }
      
      V5 = analogRead(m_5V);
      V5 = (((V5 * 3.3)/1024)*11.00244498);
      Serial.print(V5);
      Serial.print("\t");
      if(V5 > 4.5 && V5<5.5){
        V5_ok = true;
      }
      else{
        V5_ok = false;
      }
    
    
      V4v5 = analogRead(m_4V5);
      V4v5 = (((V4v5 * 3.3)/1024)*11.00244498);
      Serial.print(V4v5);
      Serial.print("\t");
      if(V4v5 > 4.0 && V4v5<5.0){
        V4v5_ok = true;
      }
      else{
        V4v5_ok = false;
      }

      //blink all four leds on the gophr board
      //Touch
      //Vac
      //Finger
      //Green (maybe power)
      for(i=0; i<5; i++){
        digitalWrite(ledctl0, HIGH); //led off
        digitalWrite(ledctl1, HIGH);
        digitalWrite(ledctl2, HIGH);
        digitalWrite(ledctl3, HIGH);
        delay(200);
        digitalWrite(ledctl0, LOW); //led on
        digitalWrite(ledctl1, LOW);
        digitalWrite(ledctl2, LOW);
        digitalWrite(ledctl3, LOW);
        delay(200);
      }

      //Serial.println("ULN test:");
      // pull all ULN channels low
      digitalWrite(ULN1, LOW);
      digitalWrite(ULN2, LOW);
      digitalWrite(ULN3, LOW);
      digitalWrite(ULN4, LOW);
      digitalWrite(ULN5, LOW);
      digitalWrite(ULN6, LOW);
      delay(50);

      // confirm all ULN channels are low by making
      // sure that the measured vs (valve state) is high. (NPN)
      vs1 = digitalRead(v1);
      vs2 = digitalRead(v2);
      vs3 = digitalRead(v3);
      vs4 = digitalRead(v4);
      vs5 = digitalRead(v5);
      vs6 = digitalRead(v6);
      if(vs1 && vs2 && vs3 && vs4 && vs5 && vs6){
        //ulns are not stuck on
        ULN_OFF_OK = true;
      }
      else{
        Serial.print("One or more ULN channel stuck on");
        ULN_OFF_OK = false;
      }

      //turn all ULN channels high to turn on ULN pulling valves low
      digitalWrite(ULN1, HIGH);
      digitalWrite(ULN2, HIGH);
      digitalWrite(ULN3, HIGH);
      digitalWrite(ULN4, HIGH);
      digitalWrite(ULN5, HIGH);
      digitalWrite(ULN6, HIGH);
      delay(50);

      //confirm all valves have been pulled low by ULN
      vs1 = digitalRead(v1);
      vs2 = digitalRead(v2);
      vs3 = digitalRead(v3);
      vs4 = digitalRead(v4);
      vs5 = digitalRead(v5);
      vs6 = digitalRead(v6);

      if(!(vs1 || vs2 || vs3 || vs4 || vs5 || vs6)){
        //ulns are able to turn on
        ULN_ON_OK = true;
      }
      else{
        Serial.print("One or more ULN channel unable to turn off");
        ULN_ON_OK = false;
      }

      // turn off all ULN channels by setting output low
      digitalWrite(ULN1, LOW);
      digitalWrite(ULN2, LOW);
      digitalWrite(ULN3, LOW);
      digitalWrite(ULN4, LOW);
      digitalWrite(ULN5, LOW);
      digitalWrite(ULN6, LOW);

      if (ULN_ON_OK && ULN_OFF_OK){
        Serial.print("ULN OK");        
      }
      else{Serial.print("ULN FAIL");}


      // touch sensor testing.
      // o_touch between 760 and 840
      delay(100);
      o_touch = analogRead(touchsens);
      o_touch = analogRead(touchsens);
      o_touch = (((o_touch*3.3)/1024)*1000);
      //Serial.print("Touch =");
      Serial.print(o_touch);
      Serial.print("\t");

      if (((760 <= o_touch) && (o_touch<= 840))){
        touch_ok = true;
      }
      else{
        touch_ok = false;
      }


      //Finger Testing
      fingvalue = analogRead(fingpin);
      fingvalue = analogRead(fingpin);
      // fingsense = ((fingsense*3.3)/1024);
      //Serial.print("Fingerprint=");
      Serial.print(fingvalue);
      Serial.print("\t");
      delay(1000);


      //Vacuum sense testing
      vacvalue = analogRead(vacpin);
      vacvalue = analogRead(vacpin);
      // vacs = ((vacs*3.3)/1024);
      //Serial.print("vacsens=");
      Serial.print(vacvalue);
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