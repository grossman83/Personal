#include <LSM6DS3.h>
// #include "/Users/marc/Documents/Arduino/libraries/Seeed_Arduino_LSM6DS3/LSM6DS3.h"
#include "Wire.h"

#include "CircularBuffer.hpp"

//Display Stuff
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64
#define OLED_RESET    -1
#define D0 0
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);



#define LSM6DS3_ADDRESS 0x6A

LSM6DS3 myIMU(I2C_MODE, LSM6DS3_ADDRESS);    //I2C device address 0x6A


int LEDR = 11;
int LEDB = 12;
int LEDG = 13;


// const int analogInPin = A0;  // Analog input pin that the potentiometer is attached to
int sensorValue = 0;  // value read from the pot


double x_val = 0.0;
double y_val = 0.0;
double z_val = 0.0;
double gs = 0.0;
int gs_int = 0;


#define slow_buf_length 10
#define fast_buf_length 500
CircularBuffer<uint8_t, fast_buf_length> fast_buffer;
CircularBuffer<uint8_t, slow_buf_length> slow_buffer;

void setup() {
    // put your setup code here, to run once:


    //########################Serial is for debugging only#############
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
    //########################Serial is for debugging only#############

    // myIMU.settings.accelFifoDecimation = 0x06;//decimation by a factor of 4
    myIMU.settings.accelSampleRate = 416;
    myIMU.settings.accelBandWidth = 400;
    myIMU.settings.accelRange = 16;
    myIMU.settings.gyroEnabled = 0;

    myIMU.begin();
    

    display.begin(SSD1306_SWITCHCAPVCC, 0x3C);

    

    //########################DISPLAY##############################
    // Initialize display
    /*
    if(!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) {
      Serial.println(F("SSD1306 allocation failed"));
      for(;;);
    }
    */

    // Clear the buffer
    display.clearDisplay();

    // Set text size, color, and position
    display.setTextSize(12);
    display.setTextColor(SSD1306_WHITE);
    display.setCursor(0, 0);
    //########################DISPLAY##############################


    pinMode(LEDR, OUTPUT);
    pinMode(LEDG, OUTPUT);
    pinMode(LEDB, OUTPUT);
    pinMode(LED_BUILTIN, OUTPUT);

    // set the resolution of the analog read to 12 bits. 
    // analogReadResolution(12);


    pinMode(D0, OUTPUT); // Set D0 as an output
}

uint8_t sample_fast(){
  analogWrite(LEDB, 0);//turn on blue LED
  digitalWrite(D0, HIGH);
  for(int i=0; i<fast_buf_length; i++){
    x_val = myIMU.readFloatAccelX();
    y_val = myIMU.readFloatAccelY();
    z_val = myIMU.readFloatAccelZ();

    gs_int = (int)(10*sqrt(x_val*x_val + y_val*y_val + z_val*z_val));
    fast_buffer.push(gs_int);
  }
  digitalWrite(D0, LOW);
  analogWrite(LEDB, 255);//turn off blue LED

  uint8_t max_gs = 0;
  for(int i=0; i<fast_buf_length; i++){
    if(fast_buffer[i] > max_gs){
      max_gs = fast_buffer[i];
    }
  }

  
  return max_gs;
}


void loop() {    
    gs_int = sample_fast();
    slow_buffer.push(gs_int);

    uint8_t max_gs = 0;
    for(int i=0; i<slow_buf_length; i++){
      if(slow_buffer[i] > max_gs){
        max_gs = slow_buffer[i];
      }
    }

    gs = (float)max_gs/10;
    char buffer[4];
    sprintf(buffer, "%.1f", gs);

    //write the data to the display
    display.clearDisplay();
    display.setTextSize(4);
    display.setTextColor(SSD1306_WHITE);
    display.setCursor(0, 0);
    display.println(buffer);
    display.display();
    
    

    //########################Serial is for debugging only#############
    // Serial.println(gs);
    //########################Serial is for debugging only#############

    // analogWrite(LEDG, 255);// turn off green LED
    // delay(100);
    // analogWrite(LEDG, 0);
}
