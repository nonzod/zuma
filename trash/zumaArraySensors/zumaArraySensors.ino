/*
   Zuma Array Sensors

  Questo sketch gira su ATtiny85 collegato ad Arduino Uno e gestisce 3 sensori a ultrasuoni.
  Le letture vengono effettuate quando viene fatte una richiesta da Arduino Uno.

  Nicola Tomassoni, 2017
   sketch basato su un lavoro di Andreas Spiess https://github.com/SensorsIot/ThreeSensorsTiny/blob/master/ThreeSensors_Tiny/ThreeSensors_Tiny.ino
*/

#include <TinyWireS.h>       // Requires fork by Rambo with onRequest support
#include <NewPing.h>         // NewPing 1.8
#include <avr/wdt.h>         // Watchdog

#define SLEFT 0 // Indice nell'array distances del sensore Sinistra
#define SRIGHT 2 // Indice nell'array distances del sensore Destra
#define SMIDDLE 1 // Indice nell'array distances del sensore Centrale

#define LEFT_T PB3
#define LEFT_E PB3
#define MIDDLE_T PB1
#define MIDDLE_E PB1
#define RIGHT_T PB4
#define RIGHT_E PB4
#define MAX_DISTANCE 270 // Distanza massima da misurare (in centimetri). Il sensore legge massimo ~400-500cm.

NewPing SensorLeft (LEFT_T, LEFT_E, MAX_DISTANCE); // Sensore Sinistra
NewPing SensorMiddle (MIDDLE_T, MIDDLE_E, MAX_DISTANCE); // Sensore Centro
NewPing SensorRight (RIGHT_T, RIGHT_E, MAX_DISTANCE); // Sensore Destra

const int I2CSlaveAddress = 8; // Indirizzo I2C

int distance[3]; // Contiene le letture dai sensori (8 bit unsigned)
int place = 0;
unsigned long start;

void setup() {
  TinyWireS.begin(I2CSlaveAddress); // Inizializza la comunicazione I2C
  TinyWireS.onRequest(transmit);  // Quando viene richiesta una lettura chiama la funzione transmit()

  wdt_enable(WDTO_500MS); // Watchdog
}

void loop() {
  readDistance();
  wdt_reset();  // Feed the watchdog
}

/**
   Trasmissione delle letture
*/
void transmit() {
  byte hh;
  
  switch (place) {
    case 0:
      hh = 255; // Start byte
      break;
    case 1:
      hh = distance[SLEFT]; // Invio lettura sensore Sinistra
      break;
    case 2:
      hh = distance[SMIDDLE]; // Invio lettura sensore Centrale
      break;
    case 3:
      hh = distance[SRIGHT];  // Invio lettura sensore Destra
      break;
  }
  
  TinyWireS.send(hh);
  place = place + 1;
  if (place > 3) place = 0;
}

/**
   Lettura distanze
*/
void readDistance() {
  distance[SLEFT] = SensorLeft.ping_cm();
  if (distance[SLEFT] > 254 ) {
    distance[SLEFT] = 254;
  }
  delay(20);
  distance[SMIDDLE] = SensorMiddle.ping_cm();
  if (distance[SMIDDLE] > 254 ) {
    distance[SMIDDLE] = 254;
  }
  delay(20);
  distance[SRIGHT] = SensorRight.ping_cm();
  if (distance[SRIGHT] > 254 ) {
    distance[SRIGHT] = 254;
  }
  delay(20);
}

/**
   Converte le letture in base alla tabella:

  3 - Distanza > 30cm
  2 - Distanza tra 21 e 30 cm
  1 - Distranza tra 11 e 20 cm
  0 - Distranza tra 0 e 10 cm
*/
/*int parseDistance(int cm) {
  if (cm > 30) {
    return 3;
  } else if (cm > 20 && cm < 30) {
    return 2;
  } else if (cm > 10 && cm < 20) {
    return 1;
  } else {
    return 0;
  }
}*/

