/*********************************************************************
 This is an example for our nRF52 based Bluefruit LE modules

 Pick one up today in the adafruit shop!

 Adafruit invests time and resources providing this open source code,
 please support Adafruit and open-source hardware by purchasing
 products from Adafruit!

 MIT license, check LICENSE for more information
 All text above, and the splash screen below must be included in
 any redistribution
*********************************************************************/
#include <bluefruit.h>
#include <Adafruit_LittleFS.h>
#include <InternalFileSystem.h>
#include <LSM6DS3.h>
#include <Wire.h>
#include <avr/dtostrf.h>

#define LSM6DS3_ADDRESS 0x6A

LSM6DS3 myIMU(I2C_MODE, LSM6DS3_ADDRESS);    //I2C device address 0x6A

const int analogInPin = A0;  // Analog input pin that the potentiometer is attached to
const int LEDR = 11;
const int LEDG = 12;
const int LEDB = 13;

unsigned long micro_count = 0;

int sensorValue = 0;  // value read from the pot

float x = 0;
float y = 0;
float z = 0;

float g = 0;

char xvalstr[8];
char yvalstr[8];
char zvalstr[8];
char gvalstr[8];
char micros_str[10];
char text_str[16];

// BLE Service
BLEDfu  bledfu;  // OTA DFU service
BLEDis  bledis;  // device information
BLEUart bleuart; // uart over ble
BLEBas  blebas;  // battery

void setup()
{
  Serial.begin(115200);


  if (myIMU.begin() != 0) {
        Serial.println("Device error");
    } else {
        Serial.println("Device OK!");
    }

#if CFG_DEBUG
  // Blocking wait for connection when debug mode is enabled via IDE
  while ( !Serial ) yield();
#endif
  
  Serial.println("Bluefruit52 BLEUART Example");
  Serial.println("---------------------------\n");

  // Setup the BLE LED to be enabled on CONNECT
  // Note: This is actually the default behavior, but provided
  // here in case you want to control this LED manually via PIN 19
  Bluefruit.autoConnLed(true);

  // Config the peripheral connection with maximum bandwidth 
  // more SRAM required by SoftDevice
  // Note: All config***() function must be called before begin()
  Bluefruit.configPrphBandwidth(BANDWIDTH_MAX);

  Bluefruit.begin();
  Bluefruit.setTxPower(4);    // Check bluefruit.h for supported values
  //Bluefruit.setName(getMcuUniqueID()); // useful testing with multiple central connections
  Bluefruit.Periph.setConnectCallback(connect_callback);
  Bluefruit.Periph.setDisconnectCallback(disconnect_callback);

  // To be consistent OTA DFU should be added first if it exists
  bledfu.begin();

  // Configure and Start Device Information Service
  bledis.setManufacturer("Adafruit Industries");
  bledis.setModel("Bluefruit Feather52");
  bledis.begin();

  // Configure and Start BLE Uart Service
  bleuart.begin();

  // Start BLE Battery Service
  blebas.begin();
  blebas.write(100);

  // Set up and start advertising
  startAdv();

  Serial.println("Please use Adafruit's Bluefruit LE app to connect in UART mode");
  Serial.println("Once connected, enter character(s) that you wish to send");
}

void startAdv(void)
{
  // Advertising packet
  Bluefruit.Advertising.addFlags(BLE_GAP_ADV_FLAGS_LE_ONLY_GENERAL_DISC_MODE);
  Bluefruit.Advertising.addTxPower();

  // Include bleuart 128-bit uuid
  Bluefruit.Advertising.addService(bleuart);

  // Secondary Scan Response packet (optional)
  // Since there is no room for 'Name' in Advertising packet
  Bluefruit.ScanResponse.addName();
  
  /* Start Advertising
   * - Enable auto advertising if disconnected
   * - Interval:  fast mode = 20 ms, slow mode = 152.5 ms
   * - Timeout for fast mode is 30 seconds
   * - Start(timeout) with timeout = 0 will advertise forever (until connected)
   * 
   * For recommended advertising interval
   * https://developer.apple.com/library/content/qa/qa1931/_index.html   
   */
  Bluefruit.Advertising.restartOnDisconnect(true);
  Bluefruit.Advertising.setInterval(32, 244);    // in unit of 0.625 ms
  Bluefruit.Advertising.setFastTimeout(30);      // number of seconds in fast mode
  Bluefruit.Advertising.start(0);                // 0 = Don't stop advertising after n seconds  
}

void loop()
{
  //Forward data from HW Serial to BLEUART
  // while (Serial.available())
  // {
  //   // Delay to wait for enough input, since we have a limited transmission buffer
  //   delay(2);

  //   uint8_t buf[64];
  //   int count = Serial.readBytes(buf, sizeof(buf));
  //   bleuart.write( buf, count );

  //   sensorValue = analogRead(analogInPin);
  //   // int count = sizeof(sensorValue);
  //   // bleuart.write(sensorValue, count);
  // }

  while(1)
  {
    x = myIMU.readFloatAccelX();
    y = myIMU.readFloatAccelY();
    z = myIMU.readFloatAccelZ();

    g = sqrt(x*x + y*y + z*z);
    micro_count = micros();
    
    
    //working**********
    // bleuart.write("x: ");  
    // bleuart.write((uint8_t*)xvalstr, strlen(xvalstr));  // Send the string over BLE
    // bleuart.write("\n");
    // bleuart.write("y: ");
    // bleuart.write((uint8_t*)yvalstr, strlen(yvalstr));  // Send the string over BLE
    // bleuart.write("\n");
    // bleuart.write("z: ");
    // bleuart.write((uint8_t*)zvalstr, strlen(zvalstr));  // Send the string over BLE
    // bleuart.write("\n");
    //working***********
    ultoa(micro_count, micros_str, 10);
    dtostrf(g, 5, 2, gvalstr);

    // strcpy(text_str, micros_str); // Copy the first string to the target buffer
    // strcat(text_str, ", "); // Concatenate the second string to the target buffer
    strcat(text_str, gvalstr); // Concatenate the third string to the target buffer
    strcat(text_str, "\n"); // Concatenate the fourth string to the target buffer
    bleuart.write((uint8_t*)text_str, strlen(text_str));  // Send the string over BLE

    delay(10);

  }

}

// callback invoked when central connects
void connect_callback(uint16_t conn_handle)
{
  // Get the reference to current connection
  BLEConnection* connection = Bluefruit.Connection(conn_handle);

  char central_name[32] = { 0 };
  connection->getPeerName(central_name, sizeof(central_name));

  Serial.print("Connected to ");
  Serial.println(central_name);
}

/**
 * Callback invoked when a connection is dropped
 * @param conn_handle connection where this event happens
 * @param reason is a BLE_HCI_STATUS_CODE which can be found in ble_hci.h
 */
void disconnect_callback(uint16_t conn_handle, uint8_t reason)
{
  (void) conn_handle;
  (void) reason;

  Serial.println();
  Serial.print("Disconnected, reason = 0x"); Serial.println(reason, HEX);
}
