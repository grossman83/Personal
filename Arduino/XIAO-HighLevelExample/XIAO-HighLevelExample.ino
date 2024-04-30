#include <LSM6DS3.h>
// #include "/Users/marc/Documents/Arduino/libraries/Seeed_Arduino_LSM6DS3/LSM6DS3.h"
#include "Wire.h"


#define LSM6DS3_ADDRESS 0x6A

LSM6DS3 myIMU(I2C_MODE, LSM6DS3_ADDRESS);    //I2C device address 0x6A

// float x = 0;
// float y = 0;
// float z = 0;
// int a = 0;


int LEDR = 11;
int LEDG = 12;
int LEDB = 13;


// const int analogInPin = A0;  // Analog input pin that the potentiometer is attached to
int sensorValue = 0;  // value read from the pot

void setup() {
    // put your setup code here, to run once:
    /*
    Serial.begin(115200);
    while (!Serial);
    //Call .begin() to configure the IMUs
    if (myIMU.begin() != 0) {
        Serial.println("Device error");
    } else {
        Serial.println("Device OK!");
    }
    */

    pinMode(LEDR, OUTPUT);
    pinMode(LEDG, OUTPUT);
    pinMode(LEDB, OUTPUT);
    pinMode(LED_BUILTIN, OUTPUT);

    // set the resolution of the analog read to 12 bits. 
    analogReadResolution(12);
}

void loop() {
    //Accelerometer
    /*
    Serial.print("\nAccelerometer:\n");
    Serial.print(" X1 = ");
    Serial.println(myIMU.readFloatAccelX(), 4);
    Serial.print(" Y1 = ");
    Serial.println(myIMU.readFloatAccelY(), 4);
    Serial.print(" Z1 = ");
    Serial.println(myIMU.readFloatAccelZ(), 4);
    */
    
    
    // sensorValue = analogRead(A0);
    // Serial.println(sensorValue);

    // Gyroscope
    /*
    Serial.print("\nGyroscope:\n");
    Serial.print(" X1 = ");
    Serial.println(myIMU.readFloatGyroX(), 4);
    Serial.print(" Y1 = ");
    Serial.println(myIMU.readFloatGyroY(), 4);
    Serial.print(" Z1 = ");
    Serial.println(myIMU.readFloatGyroZ(), 4);

    // Thermometer
    Serial.print("\nThermometer:\n");
    Serial.print(" Degrees C1 = ");
    Serial.println(myIMU.readTempC(), 4);
    Serial.print(" Degrees F1 = ");
    Serial.println(myIMU.readTempF(), 4);
    */

    // delay(100);
    // analogWrite(LED_BUILTIN, 0);
    // delay(100);
    // analogWrite(LED_BUILTIN, 0);

    for(int i=0; i<25; i++){
      analogWrite(LEDR, i*10);
      delay(10);
    }
    analogWrite(LEDR, 0);
    delay(100);

    for(int i=0; i<25; i++){
      analogWrite(LEDG, i*10);
      delay(10);
    }
    analogWrite(LEDG, 0);
    delay(100);

    for(int i=0; i<25; i++){
      analogWrite(LEDB, i*10);
      delay(10);
    }
    analogWrite(LEDB, 0);
    delay(100);



    // Serial.print(LED_BUILTIN);
}
