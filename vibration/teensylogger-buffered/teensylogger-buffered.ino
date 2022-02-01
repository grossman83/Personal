//#include <SD_t3.h>
#include <SD.h>
//#include "home/marc/arduino-1.8.19/hardware/teensy/avr/libraries/SD/src/SD.h"
#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>
#include <Wire.h>
#include <SPI.h>
#include <CircularBuffer.h>


// Reference Material
//https://github.com/rlogiacco/CircularBuffer

/*HOW TO USE
 * CHANGE FILENAME TO SOMETHING APPROPRIATE. THIS WILL APPEND TO LAST FILE
 * IF FILENAME IS NOT CHANGED.
 * 
 * IF CONNECTED TO A COMPUTER SET serialconn = 1 to see serial outputs
 * IF NOT CONNECTED TO A COMPUTER SET serialconn = 0
 * 
 * 50% pwm blinks 10 times when waiting for button press
 * hold button until LED goes solid
 * once solid it's recording data and you can release button
 * data recording is for a few seconds
 * led blinks lightly and somewhat intermittently when writing data
 * to SD card which occurs after recording.
 * 
 * you can remove SD card once the LED goes back to the 50% pwm slow (1s period)
 * blink.
 * 
 * you can re-insert SD card when in this mode as well to take additional data
 * 
 * 
 */



char filename[] = "1FEB2022 1042PDT.CSV";
const int btn = 23; //btn pin
int btnState = 1;

const bool serialconn = 0;

//macro for detection af rasing edge
#define RE(signal, state) (state=(state<<1)|(signal&1)&3)==1
#define FE(signal, state) (state=(state<<1)|(signal&1)&3)==2

//create bufferes for accelerations and time in micros()
CircularBuffer<float,10000> ax_buff;
CircularBuffer<float,10000> ay_buff;
CircularBuffer<float,10000> az_buff;
CircularBuffer<int, 10000> t_buff;

bool SD_log = true;
int led_pin = 13;


Adafruit_MPU6050 mpu;

void setup(void) {
  if (serialconn) {
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
  }

  pinMode(led_pin, OUTPUT);
  pinMode(btn, INPUT_PULLUP);
  if (!mpu.begin()){
    while(1){
      digitalWrite(led_pin, 0);
      delay(75);
      digitalWrite(led_pin, 1);
      delay(75);      
    }
  }
  mpu.setAccelerometerRange(MPU6050_RANGE_2_G);
  if (serialconn) {
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
  }
  mpu.setGyroRange(MPU6050_RANGE_500_DEG);
  if (serialconn) {
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
  }

  mpu.setFilterBandwidth(MPU6050_BAND_260_HZ);
  if (serialconn){
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
  }


  
}



void record_data(){

  //SD CARD STUFF
  delay(100);
  if (serialconn) {
    Serial.print("\nInitializing SD card...");
  }
  bool blah = SD.begin(BUILTIN_SDCARD);
  if (blah && (serialconn)) {
    Serial.println("SD Begin Success");
  }

  pinMode(led_pin, OUTPUT);
  pinMode(btn, INPUT_PULLUP);
  digitalWrite(led_pin, 0);
  int record = 1;
  File dataFile = SD.open(filename, FILE_WRITE);
  if (dataFile) {
    if (serialconn) {
      Serial.println("Data File Opened");
    }
    digitalWrite(led_pin, record);
    int count = 0;
    int t0 = 0;
    int ts = 0;
    while (record) {
      if (count == 0){
        t0 = micros();
      }
      sensors_event_t a, g, temp;
      mpu.getEvent(&a, &g, &temp);
      ts = micros() - t0;
      ax_buff.push(a.acceleration.x);
      ay_buff.push(a.acceleration.y);
      az_buff.push(a.acceleration.z);
      t_buff.push(ts);
      count ++;
      if (count >= 10000) {
        while (count > 0){
          dataFile.println(String(t_buff.shift()) + "," 
          + String(ax_buff.shift()) + "," 
          + String(ay_buff.shift()) + "," 
          + String(az_buff.shift()));
//          Serial.println(String(count));
          
          if (count % 20 > 5){
            digitalWrite(led_pin, 0);
            dataFile.flush();
          }
          else {
            digitalWrite(led_pin, 1);
          }
          count --;
        }
        
        dataFile.close();
        record = 0;
        if (serialconn) {
          Serial.println("Data File Closed");
        }
        digitalWrite(led_pin, 0);
        delay(100);
        break;
      }
    }
  }
  else {
    if (serialconn) {
      Serial.println("Unable to open SD card");
    }
  }
}




void loop() {
  delay(100);
  if (serialconn) {
    Serial.println("in loop");
  }
  if(!digitalRead(btn)){
    if (serialconn) {
      Serial.println("recording");
    }
    record_data();
  }
  for (int k = 0; k<10; k++){
    delay(500);
    digitalWrite(led_pin, 0);
    delay(500);
    digitalWrite(led_pin, 1);
  }
    
}
