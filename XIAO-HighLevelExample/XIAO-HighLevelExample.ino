#include <LSM6DS3.h>

// #include "/Users/marc/Documents/Arduino/libraries/Seeed_Arduino_LSM6DS3/LSM6DS3.h"
#include "Wire.h"


#define LSM6DS3_ADDRESS 0x6A

// TwoWire myWire = TwoWire(0);  // Use Wire1 for I2C communication
LSM6DS3 myIMU(I2C_MODE, LSM6DS3_ADDRESS);    //I2C device address 0x6A
// LSM6DS3 myIMU();    //I2C device address 0x6A

float x = 0;
float y = 0;
float z = 0;
int a = 0;

void setup() {
    // put your setup code here, to run once:
    Serial.begin(9600);
    while (!Serial);
    //Call .begin() to configure the IMUs
    if (myIMU.begin() != 0) {
        Serial.println("Device error");
    } else {
        Serial.println("Device OK!");
    }
}

void loop() {
    //Accelerometer
    x = myIMU.readFloatAccelX();
    Serial.print("\nAccelerometer:\n");
    Serial.print(" X1 = ");
    Serial.println(myIMU.readFloatAccelX(), 4);
    Serial.print(" Y1 = ");
    Serial.println(myIMU.readFloatAccelY(), 4);
    Serial.print(" Z1 = ");
    Serial.println(myIMU.readFloatAccelZ(), 4);

    //Gyroscope
    Serial.print("\nGyroscope:\n");
    Serial.print(" X1 = ");
    Serial.println(myIMU.readFloatGyroX(), 4);
    Serial.print(" Y1 = ");
    Serial.println(myIMU.readFloatGyroY(), 4);
    Serial.print(" Z1 = ");
    Serial.println(myIMU.readFloatGyroZ(), 4);

    //Thermometer
    Serial.print("\nThermometer:\n");
    Serial.print(" Degrees C1 = ");
    Serial.println(myIMU.readTempC(), 4);
    Serial.print(" Degrees F1 = ");
    Serial.println(myIMU.readTempF(), 4);

    delay(100);
}
