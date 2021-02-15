#include <SD_t3.h>
#include <SD.h>

// Basic demo for accelerometer readings from Adafruit MPU6050

#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>
#include <Wire.h>
#include <SPI.h>

const int btn = 14; //btn pin
int btnState;
//macro for detection af rasing edge
#define RE(signal, state) (state=(state<<1)|(signal&1)&3)==1


bool SD_log = true;
int led_pin = 13;


Adafruit_MPU6050 mpu;

void setup(void) {
  Serial.begin(115200);
  while (!Serial)
    delay(10); // will pause Zero, Leonardo, etc until serial console opens

  Serial.println("Adafruit MPU6050 test!");

  // Try to initialize!
  if (!mpu.begin()) {
    Serial.println("Failed to find MPU6050 chip");
    while (1) {
      delay(1000);
      Serial.println("Failed to find MPU6050 chip");
    }
  }
  Serial.println("MPU6050 Found!");

  mpu.setAccelerometerRange(MPU6050_RANGE_16_G);
  Serial.print("Accelerometer range set to: ");
  switch (mpu.getAccelerometerRange()) {
  case MPU6050_RANGE_2_G:
    Serial.println("+-2G");
    break;
  case MPU6050_RANGE_4_G:
    Serial.println("+-4G");
    break;
  case MPU6050_RANGE_8_G:
    Serial.println("+-8G");
    break;
  case MPU6050_RANGE_16_G:
    Serial.println("+-16G");
    break;
  }
  mpu.setGyroRange(MPU6050_RANGE_500_DEG);
  Serial.print("Gyro range set to: ");
  switch (mpu.getGyroRange()) {
  case MPU6050_RANGE_250_DEG:
    Serial.println("+- 250 deg/s");
    break;
  case MPU6050_RANGE_500_DEG:
    Serial.println("+- 500 deg/s");
    break;
  case MPU6050_RANGE_1000_DEG:
    Serial.println("+- 1000 deg/s");
    break;
  case MPU6050_RANGE_2000_DEG:
    Serial.println("+- 2000 deg/s");
    break;
  }

  mpu.setFilterBandwidth(MPU6050_BAND_260_HZ);
  Serial.print("Filter bandwidth set to: ");
  switch (mpu.getFilterBandwidth()) {
  case MPU6050_BAND_260_HZ:
    Serial.println("260 Hz");
    break;
  case MPU6050_BAND_184_HZ:
    Serial.println("184 Hz");
    break;
  case MPU6050_BAND_94_HZ:
    Serial.println("94 Hz");
    break;
  case MPU6050_BAND_44_HZ:
    Serial.println("44 Hz");
    break;
  case MPU6050_BAND_21_HZ:
    Serial.println("21 Hz");
    break;
  case MPU6050_BAND_10_HZ:
    Serial.println("10 Hz");
    break;
  case MPU6050_BAND_5_HZ:
    Serial.println("5 Hz");
    break;
  }


  //SD CARD STUFF
  delay(100);
  Serial.print("\nInitializing SD card...");
  bool blah = SD.begin(BUILTIN_SDCARD);
  if (blah) {
    Serial.println("SD Begin Success");
  }

  pinMode(led_pin, OUTPUT);
  pinMode(btn, INPUT_PULLUP);
}



void record_data(){
//  char filename = String("Data" + millis() + ".txt");
//  File dataFile = SD.open(filename, FILE_WRITE);
//  File dataFile = SD.open("data" + millis() + ".txt", FILE_WRITE);
File dataFile = SD.open("data12345.txt", FILE_WRITE);
  int record = 1;
  digitalWrite(led_pin, record);

  while(record) {
    sensors_event_t a, g, temp;
    mpu.getEvent(&a, &g, &temp);
    if (dataFile) {
      dataFile.println(String(millis()) + "," + String(a.acceleration.x) + "," + String(a.acceleration.y) + "," + String(a.acceleration.z));
      Serial.println(String(millis()) + "," + String(a.acceleration.x) + "," + String(a.acceleration.y) + "," + String(a.acceleration.z));
      
      if(RE(digitalRead(btn), btnState)){
        //close dataFile and exit
        dataFile.close();
        //Turn off the LED
        digitalWrite(led_pin, 0);
        delay(50);
        break;
      }
    }
  }
}




void loop() {
  if(RE(digitalRead(btn), btnState)){
    record_data();
    delay(50);
  }
}
