#include <LSM6DS3.h>
#include "Wire.h"
#include "CircularBuffer.hpp"

//low power sleep stuff
#include "Adafruit_SPIFlash.h"
#define DO_WORK_PIN   D2
#define SHUTDOWN_PIN  D3
#define wait2sleep_millis 300000


bool serial_enabled = false;

//test
//Display Stuff
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#define SCREEN_PIN D1
#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64
#define OLED_RESET    -1
#define D0 0
#define cursor_x 20
#define cursor_y 20



Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);
#define LSM6DS3_ADDRESS 0x6A
LSM6DS3 myIMU(I2C_MODE, LSM6DS3_ADDRESS);    //I2C device address 0x6A

// More sleep stuff
Adafruit_FlashTransport_QSPI flashTransport;
SemaphoreHandle_t xSemaphore;
// bool gotoSystemOffSleep = false;
int boot_millis = 0;

void QSPIF_sleep(void)
{
  flashTransport.begin();
  flashTransport.runCommand(0xB9);
  flashTransport.end();  
}


double x_val = 0.0;
double y_val = 0.0;
double z_val = 0.0;
double gs = 0.0;
uint8_t max_gs = 0;
int gs_int = 0;


#define fast_buf_length 500
CircularBuffer<uint8_t, fast_buf_length> fast_buffer;
CircularBuffer<int, fast_buf_length> millis_buffer;

void setup() {
    if(serial_enabled){
      Serial.begin(115200);
      // while (!Serial);
      //Call .begin() to configure the IMUs
      if (myIMU.begin() != 0) {
          Serial.println("Device error");
      } else {
          Serial.println("Device OK!");
      }
    }


    // myIMU.settings.accelFifoDecimation = 0x06;//decimation by a factor of 4
    myIMU.settings.accelSampleRate = 416;
    // myIMU.settings.accelSampleRate = 3300;
    myIMU.settings.accelBandWidth = 400;//50, 100, 200, 400
    myIMU.settings.accelRange = 16;
    myIMU.settings.gyroEnabled = 0;
    myIMU.settings.tempEnabled = 0;
    myIMU.begin(); //must call this to apply the settings.
    

    

    

    //########################DISPLAY##############################
    if(serial_enabled){
      if(!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) {
        Serial.println(F("SSD1306 allocation failed"));
        for(;;);
      }
    }
    //turn on the display
    pinMode(SCREEN_PIN, OUTPUT);
    digitalWrite(SCREEN_PIN, HIGH);
    delay(10);

    // initialize the display
    display.begin(SSD1306_SWITCHCAPVCC, 0x3C);
    display.clearDisplay();

    // Set text size, color, and position
    display.setTextSize(4); //4 seems to be the largest
    display.setTextColor(SSD1306_WHITE);
    display.setCursor(cursor_x, cursor_y);
    //########################DISPLAY##############################


    //D0 was used to measure timing with oscilloscope.
    //pinMode(D0, OUTPUT); // Set D0 as an output

    //basic LED stuff
    pinMode(LED_RED, OUTPUT);
    pinMode(LED_GREEN, OUTPUT);
    pinMode(LED_BLUE, OUTPUT);
    digitalWrite(LED_RED, HIGH);
    digitalWrite(LED_GREEN, HIGH);
    

    QSPIF_sleep();

    // I'm not using any waking or sleeping based on a pin.
    // pinMode(DO_WORK_PIN, INPUT_PULLUP_SENSE);
    // attachInterrupt(digitalPinToInterrupt(DO_WORK_PIN), doWorkISR, FALLING);
    // pinMode(SHUTDOWN_PIN, INPUT_PULLUP_SENSE);
    // attachInterrupt(digitalPinToInterrupt(SHUTDOWN_PIN), shutdownISR, FALLING);

    xSemaphore = xSemaphoreCreateBinary();

    // Flash green to see power on, reset, and wake from system_off
    digitalWrite(LED_GREEN, LOW);
    delay(1000);
    digitalWrite(LED_GREEN, HIGH);
    boot_millis = millis();
}

// void doWorkISR()
// {
//   xSemaphoreGive(xSemaphore);
// }

void shutdownISR()
{
  // gotoSystemOffSleep = true;
  xSemaphoreGive(xSemaphore);
}

uint8_t sample_fast(){
  digitalWrite(LED_BLUE, LOW);//turn on blue LED
  //digitalWrite(D0, HIGH);//for timing measurement with oscope
  for(int i=0; i<fast_buf_length; i++){
    x_val = myIMU.readFloatAccelX();
    y_val = myIMU.readFloatAccelY();
    z_val = myIMU.readFloatAccelZ();

    gs_int = (int)(10*sqrt(x_val*x_val + y_val*y_val + z_val*z_val));
    fast_buffer.push(gs_int);

    if(serial_enabled){
      millis_buffer.push(millis());
    }
  }
  //digitalWrite(D0, LOW);//for timing measurement with oscope
  digitalWrite(LED_BLUE, HIGH);//turn off blue LED

  uint8_t fast_max_gs = 0;
  for(int i=0; i<fast_buf_length; i++){
    if(fast_buffer[i] > fast_max_gs){
      fast_max_gs = fast_buffer[i];
    }
  }

  if(serial_enabled){
    for(int i=0; i<fast_buf_length; i++){
      Serial.print(millis_buffer[i]);
      Serial.print(", ");
      Serial.println(fast_buffer[i]/9.81);
    }
  }

  
  return fast_max_gs;
}


void loop() {
  // if(millis() - boot_millis > wait2sleep_millis){
  //   gotoSystemOffSleep = true;
  // }

  if (millis() - boot_millis > wait2sleep_millis){
    //Turn off the blue LED
    digitalWrite(LED_BLUE, HIGH);
    //Flash red to see we are going to system_off sleep mode
    digitalWrite(LED_RED, LOW);
    delay(1000);
    digitalWrite(LED_RED, HIGH);


    // turn off the IMU
    myIMU.settings.accelEnabled = 0;
    myIMU.begin();
    


    // tried commenting this out, but it does matter. If I don't turn off
    // the screen I use nearly 6 mA in sleep. I'm surprised that the pin
    // doesn't naturally go off in sleep mode.
    // the red LED goes off during sleep mode despite me not telling it to go high.
    digitalWrite(SCREEN_PIN, LOW);//turn off the screen

    NRF_POWER->SYSTEMOFF=1; // Execution should not go beyond this
  }
  
  
  gs_int = sample_fast(); //get the highest value from sample_fast
  if(gs_int > max_gs){
    max_gs = gs_int;
  }

  gs = (float)max_gs/10;
  char buffer[4];
  sprintf(buffer, "%.1f", gs);

  //write the data to the display
  display.clearDisplay();
  display.setTextSize(4);
  display.setTextColor(SSD1306_WHITE);
  display.setCursor(cursor_x, cursor_y);
  display.println(buffer);
  display.display();
  
  

  // if(serial_enabled){
  //   Serial.println(gs);
  // }
}
