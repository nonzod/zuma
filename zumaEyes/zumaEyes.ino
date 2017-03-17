/*
   Zuma Array Sensors

  Questo sketch gira su ATtiny85 collegato ad Arduino Uno e gestisce 3 sensori a ultrasuoni.
  Le letture vengono effettuate quando viene fatte una richiesta da Arduino Uno.

  Nicola Tomassoni, 2017
*/

#include <TinyWireS.h>       // https://github.com/rambo/TinyWire
#include <NewPing.h>         // NewPing 1.8

#define I2C_SLAVE_ADDRESS 8 // the 7-bit address (remember to change this when adapting this example)
// The default buffer size, Can't recall the scope of defines right now
#ifndef TWI_RX_BUFFER_SIZE
#define TWI_RX_BUFFER_SIZE ( 16 )
#endif

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

// Tracks the current register pointer position
volatile byte reg_position;
const byte reg_size = 4;

/**
  Viene richiamata ad ogni richiesta di lettura.
  Per leggere tutti i sensori devono venir fatte 4 richieste start, left, center, right
*/
void transmit() {
  byte dst;
  
  switch (reg_position) {
    case 0:
      dst = 255; // Start byte
      break;
    case 1:
      dst = readDistance(1); // Invio lettura sensore Sinistra
      break;
    case 2:
      dst = readDistance(2); // Invio lettura sensore Centrale
      break;
    case 3:
      dst = readDistance(3);  // Invio lettura sensore Destra
      break;
  }
  
  TinyWireS.send(dst);
  reg_position++;
  if (reg_position >= reg_size) reg_position = 0;
}

/**
   Lettura distanze
   Ritorna la distanza rilevata dal sensore selezionato
   Ogni lettura ha un delay di 20ms
*/
int readDistance(int pos) {
  int distance;
  
  switch(pos) {
    case 1:
      distance = SensorLeft.ping_cm();
      break;
    case 2:
      distance = SensorMiddle.ping_cm();
      break;
    case 3:
      distance = SensorRight.ping_cm();
      break;
  }

  if (distance > 254 ) {
    distance = 254;
  }
  
  tws_delay(20);
  
  return distance;
}

void setup() {
  TinyWireS.begin(I2C_SLAVE_ADDRESS);
  TinyWireS.onRequest(transmit);
}

void loop() {
  /**
     This is the only way we can detect stop condition (http://www.avrfreaks.net/index.php?name=PNphpBB2&file=viewtopic&p=984716&sid=82e9dc7299a8243b86cf7969dd41b5b5#984716)
     it needs to be called in a very tight loop in order not to miss any (REMINDER: Do *not* use delay() anywhere, use tws_delay() instead).
     It will call the function registered via TinyWireS.onReceive(); if there is data in the buffer on stop.
  */
  TinyWireS_stop_check();
}
