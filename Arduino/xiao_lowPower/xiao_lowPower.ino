#include "Adafruit_SPIFlash.h"

#define DO_WORK_PIN   D2
#define SHUTDOWN_PIN  D3

// working code came from here
//https://forum.seeedstudio.com/t/getting-lower-power-consumption-on-seeed-xiao-nrf52840/270129/3

Adafruit_FlashTransport_QSPI flashTransport;
SemaphoreHandle_t xSemaphore;
bool gotoSystemOffSleep = false;
int work_LED_status = HIGH;

void QSPIF_sleep(void)
{
  flashTransport.begin();
  flashTransport.runCommand(0xB9);
  flashTransport.end();  
}

void setup()
{
  pinMode(LED_RED, OUTPUT);
  pinMode(LED_GREEN, OUTPUT);
  pinMode(LED_BLUE, OUTPUT);
  
  digitalWrite(LED_RED, HIGH);
  digitalWrite(LED_GREEN, HIGH);
  digitalWrite(LED_BLUE, work_LED_status);

  QSPIF_sleep();

  pinMode(DO_WORK_PIN, INPUT_PULLUP_SENSE);
  attachInterrupt(digitalPinToInterrupt(DO_WORK_PIN), doWorkISR, FALLING);

  pinMode(SHUTDOWN_PIN, INPUT_PULLUP_SENSE);
  attachInterrupt(digitalPinToInterrupt(SHUTDOWN_PIN), shutdownISR, FALLING);

  xSemaphore = xSemaphoreCreateBinary();

  // Flash green to see power on, reset, and wake from system_off
  digitalWrite(LED_GREEN, LOW);
  delay(1000);
  digitalWrite(LED_GREEN, HIGH);
}

void doWorkISR()
{
  xSemaphoreGive(xSemaphore);
}

void shutdownISR()
{
  gotoSystemOffSleep = true;
  xSemaphoreGive(xSemaphore);
}

void loop()
{
  // FreeRTOS will automatically put the system in system_on sleep mode here
  xSemaphoreTake(xSemaphore, portMAX_DELAY);

  if (gotoSystemOffSleep)
  {
    //Flash red to see we are going to system_off sleep mode
    digitalWrite(LED_RED, LOW);
    delay(1000);
    digitalWrite(LED_RED, HIGH);

    NRF_POWER->SYSTEMOFF=1; // Execution should not go beyond this
    //sd_power_system_off() // Use this instead if using the soft device
  }

  // Not going to system off sleep mode, so do work
  work_LED_status = !work_LED_status;
  digitalWrite(LED_BLUE, work_LED_status);
}