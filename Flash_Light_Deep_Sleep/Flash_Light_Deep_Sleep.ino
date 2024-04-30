//----------------------------------------------------------------------------------------------
// BSP : Seeed nRF52 Borads 1.1.1
// Board : Seeed nRF52 Borads / Seeed XIAO nRF52840 Sense 
//----------------------------------------------------------------------------------------------
// 2023/08/11

#include <bluefruit.h>          // /Arduino15/packages/Seeeduino/hardware/nrf52/1.1.1/libraries/Bluefruit52Lib/src
#include <Adafruit_SPIFlash.h>  // Need to be deleted /Documents/Arduino/libraries/SdFat
#include <LowPower.h>

#define WAKEUP_PIN 4  // Change this to the pin you want to use for wake-up


const int LEDR = 11;
const int LEDB = 12;
const int LEDG = 13;


// Built from the P25Q16H datasheet.
// https://gitlab.com/arduino5184213/seeed_xiao_nrf52840/flash_speedtest/-/tree/master
SPIFlash_Device_t const P25Q16H {
  .total_size = (1UL << 21), // 2MiB
  .start_up_time_us = 10000, // Don't know where to find that value
  
  .manufacturer_id = 0x85,
  .memory_type = 0x60,
  .capacity = 0x15,

  .max_clock_speed_mhz = 55,
  .quad_enable_bit_mask = 0x02, // Datasheet p. 27
  .has_sector_protection = 1,   // Datasheet p. 27
  .supports_fast_read = 1,      // Datasheet p. 29
  .supports_qspi = 1,           // Obviously
  .supports_qspi_writes = 1,    // Datasheet p. 41
  .write_status_register_split = 1, // Datasheet p. 28
  .single_status_byte = 0,      // 2 bytes
  .is_fram = 0,                 // Flash Memory
};
Adafruit_FlashTransport_QSPI flashTransport;
Adafruit_SPIFlash flash(&flashTransport);

void setup()
{
  // Enable DC-DC converter Mode
  NRF_POWER->DCDCEN = 1;            // Enable DC/DC converter for REG1 stage

  delay(1000);


  // marc sleep stuff
  pinMode(WAKEUP_PIN, INPUT_PULLUP);
  // marc sleep stuff

  //LEDs
  pinMode(LEDR, OUTPUT);
  pinMode(LEDG, OUTPUT);
  pinMode(LEDB, OUTPUT);


  // on board Flash enter to Deep Power-Down Mode
  flashTransport.begin();
  flashTransport.runCommand(0xB9);  // enter deep power-down mode
  delayMicroseconds(5);             // tDP=3uS
  flashTransport.end();

  // Light Sleep Mode (RTOS delay function)
  delay(1000);

  // Deep Sleep Mode
  NRF_POWER->SYSTEMOFF = 1;

  // Even after entering deep sleep mode, 
  // 3.3V LOD's "quiescent current 2.5uA" remains. 
}

void loop()
{
  analogWrite(LEDG, 0);
  // Enter sleep mode
  // Wait for wake-up event
  LowPower.attachInterruptWakeup(WAKEUP_PIN, NULL, CHANGE);
  LowPower.sleep();
}


void wakeup()
{
  // Wake-up routine
  analogWrite(LEDB, 0);


  delay(3000);
  LowPower.attachInterruptWakeup(WAKEUP_PIN, NULL, CHANGE);
  LowPower.sleep();

}
