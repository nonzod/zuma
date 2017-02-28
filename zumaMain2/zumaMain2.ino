#include <Wire.h>
#include <ZumoBuzzer.h>
#include <ZumoMotors.h>
#include <Pushbutton.h>
#include <LSM303.h>
//#include <L3G.h>

#define LOG_SERIAL true // Abilita l'output su monitor seriale
#define SLEFT 0 // Indice nell'array distances del sensore Sinistra
#define SRIGHT 2 // Indice nell'array distances del sensore Destra
#define SMIDDLE 1 // Indice nell'array distances del sensore Centrale
#define TD_LEFT 1 // Indica di girare a Sinistra
#define TD_RIGHT 2 // Indica di girare a Destra
#define FLIP_RIGHT 1 // Flip motore destro 1 = Si, 0 = No
#define FLIP_LEFT 0 // Flip motore sinistro 1 = Si, 0 = No
#define TURN_DURATION 600 // Deprecated
#define BAT_VOLTAGE A1 // Pin per controllo stato batterie
// Accelerometer Settings
#define RA_SIZE 3  // number of readings to include in running average of accelerometer readings
#define XY_ACCELERATION_THRESHOLD 2400  // for detection of contact (~16000 = magnitude of acceleration due to gravity)

const char sound_effect[] PROGMEM = "O4 T100 V10 L4 MS g12>c12>e12>G6>E12 ML>G2"; // Melodia di avvio - V < 10 Muto; v15 Volume al massimo
const int I2CUSonic = 8; // Indirizzo I2C dell'array di sensori a ultrasuoni.

ZumoMotors zMotors;
Pushbutton zButton(ZUMO_BUTTON); // pushbutton on pin 12
ZumoBuzzer zBuzzer;

int default_speed = 200; // Velocità di crocera
int slow_speed = 50; // Velocità lenta
int max_speed = 400; // Velocità massima
int usonic_pos; // Contatore per ciclare la lettura dei sensori
int distances[3]; // Array per registrare le distanze
bool slow_running = false; // Indicatore di andatura lenta

/**
   SETUP
*/
void setup() {
  zMotors.flipRightMotor(FLIP_RIGHT); // Il motore destro va flippato :)
  zMotors.flipLeftMotor(FLIP_LEFT); // Il motore destro va flippato :)
  motorsStop();

  Wire.begin(); // Comunicazione I2C

#ifdef LOG_SERIAL
  Serial.begin(115200);
  Serial.println("Zuma è pronto");
#endif

  waitForButtonAndGo(false);
}

/**
   LOOP
*/
void loop() {
  if (zButton.isPressed()) {
    // Se premo il bottone mi fermo e aspetto una nuova pressione per ripartire
    zMotors.setSpeeds(0, 0);
    zButton.waitForRelease();
    waitForButtonAndGo(true);
  }

  fillDistances();
  autoPilot();
}

/**
   Pilota automatico
*/
void autoPilot() {
  fillDistances(); // Aggiorna situazione distanze

  if (distances[SMIDDLE] < 15 && distances[SMIDDLE] > 0) {
    int turn_direction = chooseDirection();
    turn(turn_direction);
  } else if (distances[SLEFT] < 15 && distances[SLEFT] > 0) {
    turn(TD_RIGHT);
  } else if (distances[SRIGHT] < 15 && distances[SRIGHT] > 0) {
    turn(TD_LEFT);
  }

}

/**
    Decide da che parte girare in base alle letture dei sensori
*/
int chooseDirection() {
  if (distances[SLEFT] < distances[SRIGHT]) {
    return TD_RIGHT;
  }

  return TD_LEFT;
}

/**
    Effettua una curva
*/
void turn(int turn_direction) {

  int turn_speed = default_speed - int(default_speed / 2);

  if (turn_direction == TD_LEFT) {
    zMotors.setSpeeds(-default_speed, default_speed);
    while (distances[SRIGHT] < 15 || distances[SRIGHT] == 0) {
      fillDistances();
    }
  } else if (turn_direction == TD_RIGHT) {
    zMotors.setSpeeds(default_speed, -default_speed);
    while (distances[SLEFT] < 15 || distances[SLEFT] == 0) {
      fillDistances();
    }
  }

  motorsForward(default_speed);
}

/**
   Avanti dritto
*/
void motorsForward(int new_speed) {
  zMotors.setSpeeds(new_speed, new_speed);
  slow_running = false;
}

/**
   Rallenta
*/
void motorsDecelerate() {
  zMotors.setSpeeds(slow_speed, slow_speed);
  slow_running = true;
}

/**
   Motori fermi
*/
void motorsStop() {
  zMotors.setSpeeds(0, 0);
}

/**
    Gira di 180°
*/
void motorsReverse() {
  int rev_delay = TURN_DURATION * 2;
  zMotors.setSpeeds(default_speed, -default_speed);
  delay(rev_delay);
  motorsForward(default_speed);
  /*
    while(rotazione < 180°){
    // Qui mi sa che va letto prima il valore del compasso poi si inizia a girare
    // fino a quando la differenza tra la prima lettura e l'ultima è 180°
    rotazione = leggi compasso;
    };
    forward();*/
}

/**
    Aggiorna l'array con le distanze lette via I2C
*/
void fillDistances() {
  while (readUSonicArray(I2CUSonic) < 255) {
#ifdef LOG_SERIAL
    Serial.print("WT");  // Attende il primo byte
#endif
  }

  for (usonic_pos = 0; usonic_pos < 3; usonic_pos++) {
    distances[usonic_pos] = readUSonicArray(I2CUSonic);
  }

#ifdef LOG_SERIAL
  Serial.print(" L ");
  Serial.print(distances[SLEFT]);
  Serial.print(" - C ");
  Serial.print(distances[SMIDDLE]);
  Serial.print(" - R ");
  Serial.print(distances[SRIGHT]);
#endif

#ifdef LOG_SERIAL
  Serial.println();
#endif

  delay(25); // Era 200
}

/**
   Lettura Sensori a Ultrasuoni
*/
byte readUSonicArray(int address) {
  byte hh ;
  long entry = millis();
  Wire.requestFrom(address, 1); // The TinyWire library only allows for one byte to be requested at a time

  while (Wire.available() == 0 && (millis() - entry) < 100) {
#ifdef LOG_SERIAL
    Serial.print("W");
#endif
  }

  if (millis() - entry < 100) hh = Wire.read();

  return hh;
}

/**
   Azione alla pressione del pulsante start/stop
*/
void waitForButtonAndGo(bool restarting) {
  digitalWrite(LED_BUILTIN, HIGH);
  zButton.waitForButton();
  digitalWrite(LED_BUILTIN, LOW);

#ifdef LOG_SERIAL
  Serial.print(restarting ? "Riavvio il Countdown" : "Avvio il Countdown");
  Serial.println();
#endif

  zBuzzer.playFromProgramSpace(sound_effect);
  delay(1000);

  // reset loop variables
  // TODO
  if (restarting == false) {
    zMotors.setSpeeds(-50, -50);
    delay(1500);
    zMotors.setSpeeds(100, -100);
    delay(800);
  }
  motorsForward(default_speed);
}
