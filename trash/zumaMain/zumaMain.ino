#include <Wire.h>
#include <ZumoBuzzer.h>
#include <ZumoMotors.h>
#include <Pushbutton.h>
//#include <LSM303.h>
//#include <L3G.h>

#define LOG_SERIAL true

#define SLEFT 0 // Indice nell'array distances del sensore Sinistra
#define SRIGHT 2 // Indice nell'array distances del sensore Destra
#define SMIDDLE 1 // Indice nell'array distances del sensore Centrale

#define TD_LEFT 1 // Indica di girare a Sinistra
#define TD_RIGHT 2 // Indica di girare a Destra

#define FLIP_RIGHT 1 // Flip motore destro 1 = Si, 0 = No
#define FLIP_LEFT 0 // Flip motore sinistro 1 = Si, 0 = No

#define TURN_DURATION 600
#define IREYES A1

const char sound_effect[] PROGMEM = "O4 T100 V10 L4 MS g12>c12>e12>G6>E12 ML>G2"; // Melodia di avvio - V < 10 Muto; v15 Volume al massimo
const int I2CUSonic = 8; // Indirizzo I2C dell'array di sensori a ultrasuoni.

ZumoMotors zMotors;
Pushbutton zButton(ZUMO_BUTTON); // pushbutton on pin 12
ZumoBuzzer zBuzzer;

int default_speed = 150; // Velocità di crocera
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
  
  fillDistances(); // Aggiorna situazione distanze
  
  //autoPilot();
}

/**
   Pilota automatico
*/
void autoPilot() {
  if (distances[SMIDDLE] < 25 && distances[SMIDDLE] > 10) {
    

    int turn_direction = chooseDirection();

    if (turn_direction != 0) {
      turn(2, turn_direction);
    } else {
      motorsDecelerate();
    }
  } else if (distances[SMIDDLE] < 10  && distances[SMIDDLE] > 0) {
    motorsReverse();
  } else if (slow_running == true) {
    motorsForward(default_speed); // serve per accellerare dopo un decelerate()
  }
}

bool readIREyes() {
  float volts = analogRead(IREYES);
  //float front_distance = 65 * pow(volts, -1.10);
  
#ifdef LOG_SERIAL
  Serial.print("Front ");
  Serial.println(volts);
#endif

  return volts;
}

/**
    Decide da che parte girare in base alle letture dei sensori
*/
int chooseDirection() {
  // Se non c'è spazio per girare torna 0
  if ((distances[SLEFT] < 25 && distances[SLEFT] > 0) && (distances[SRIGHT] < 25 && distances[SRIGHT] > 0)) {
    return 0;
  }

  if (distances[SLEFT] < distances[SRIGHT]) {
    return TD_RIGHT;
  }

  return TD_LEFT;
}

/**
    Effettua una curva
*/
void turn(int turn_type, int turn_direction) {
  /*if(turn_type >=30) {
    turn_type = 3;
    } else {
    turn_type = 2;
    }*/
  int turn_speed = default_speed - int(default_speed / turn_type);

  if (turn_direction == TD_LEFT) {
    zMotors.setSpeeds(-default_speed, default_speed);
  } else if (turn_direction == TD_RIGHT) {
    zMotors.setSpeeds(default_speed, -default_speed);
  }

  delay(TURN_DURATION);
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

  delay(200); // Era 200
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

  motorsForward(default_speed);
}

