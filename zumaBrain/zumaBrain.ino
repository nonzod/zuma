/**

   Il cervello di Zuma...

*/
#include <Wire.h>
#include <SoftwareSerial.h>
#include <ZumoBuzzer.h>
#include <ZumoMotors.h>
#include <Pushbutton.h>

// Voltage settings
#define BAT_VOLTAGE A1 // Pin per controllo stato batterie

// Motors settings
#define SLEFT 0 // Indice nell'array distances del sensore Sinistra
#define SMIDDLE 1 // Indice nell'array distances del sensore Centrale
#define SRIGHT 2 // Indice nell'array distances del sensore Destra
#define FLIP_RIGHT 1 // Flip motore destro 1 = Si, 0 = No
#define FLIP_LEFT 0 // Flip motore sinistro 1 = Si, 0 = No

// @TODO Accelerometer settings
#define RA_SIZE 3  // number of readings to include in running average of accelerometer readings
#define XY_ACCELERATION_THRESHOLD 2400  // for detection of contact (~16000 = magnitude of acceleration due to gravity)

// I2C settings
#define USONIC_ADDRESS 8

// Bluetooth settings
#define BLE_RX 17 // BLE RX Pin
#define BLE_TX 16 // BLE TX Pin
#define EOP '>' // Identifica la fine di un pacchetto via BLE

// Debug
#define LOG_SERIAL true // Abilita l'output su monitor seriale

ZumoMotors zMotors;
Pushbutton zButton(ZUMO_BUTTON); // default: pushbutton su pin 12
ZumoBuzzer zBuzzer;
SoftwareSerial BleSerial(BLE_RX, BLE_TX); // RX, TX

// BLE Globals
const byte ble_size = 24; // Dimensione pacchetto in arrivo via BLE
boolean ble_is_new = false; // E' un nuovo pacchetto BLE?
char ble_chars[ble_size]; // Contenuto del pacchetto via BLE
long ble_interval = 80; // Intervallo di invio dati via Bluetooth
long ble_prev_ms = 0; // Tempo dell'ultimo invio via Bluetooth

/*Ultrasonic Globals

   distances[SLEFT] Sinistra
   distances[SMIDDLE] Centro
   distances[SRIGHT] Destra
*/
byte distances[3]; // Letture delle distanze da ZumaEyes
long eye_interval = 160; // Intervallo letture delle distanze da ZumaEyes
long eye_prev_ms = 0; // Tempo ultima lettura delle distanze da ZumaEyes

long inp_interval = 40; // Intervallo di letture dati via Bluetooth
long inp_prev_ms = 0; // Tempo dell'ultima lettura via Bluetooth

long debug_interval = 1000;
long debug_prev_ms = 0;
long num_pk = 0;
long num_errors = 0;

void setup() {
  // Setup BLE
  pinMode(BLE_RX, INPUT);
  pinMode(BLE_TX, OUTPUT);
  BleSerial.begin(9600);

  // Setup motors
  zMotors.flipRightMotor(FLIP_RIGHT);
  zMotors.flipLeftMotor(FLIP_LEFT);
  motorsStop();

  // Setup I2C
  Wire.begin();

  // Setup serial monitor
#ifdef LOG_SERIAL
  Serial.begin(9600);
  Serial.println(F("Zuma ready"));
#endif
}

void loop() {
  unsigned long curr_ms = millis();

  if (curr_ms - eye_prev_ms > eye_interval) { // "Thread" letture da zumaEyes
    eye_prev_ms = curr_ms;
    updateDistances();
  }

  if (curr_ms - ble_prev_ms > ble_interval) { // "Thread" invio dati Bluetooth
    ble_prev_ms = curr_ms;
    sendBleData();
  }

  if (curr_ms - inp_prev_ms > inp_interval) { // "Thread" letture da Bluetooth
    bleHandleInput();
  }

  if (curr_ms - debug_prev_ms > debug_interval) { // "Thread" debug
    debug_prev_ms = curr_ms;
#ifdef LOG_SERIAL
    Serial.print(F("Num/Err: "));
    Serial.print(num_pk);
    Serial.print(F("/"));
    Serial.println(num_errors);
#endif
  }
}
