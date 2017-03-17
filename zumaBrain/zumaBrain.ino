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
#define BLE_RX 18 // BLE RX Pin
#define BLE_TX 17 // BLE TX Pin
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
long ble_interval = 200; // Intervallo di invio dati via Bluetooth
long ble_prev_ms = 0; // Tempo dell'ultimo invio via Bluetooth

/*Ultrasonic Globals
 * 
 * distances[SLEFT] Sinistra
 * distances[SMIDDLE] Centro
 * distances[SRIGHT] Destra
 */
byte distances[3]; // Letture delle distanze da ZumaEyes
long eye_interval = 20; // Intervallo di invio dati via Bluetooth
long eye_prev_ms = 0; // Tempo dell'ultimo invio via Bluetooth

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
  Serial.println("Zuma è pronto");
#endif
}

void loop() {
  unsigned long curr_ms = millis();
  
  // "Thread" invio dati Bluetooth
  if(curr_ms - ble_prev_ms > ble_interval) {
    ble_prev_ms = curr_ms;
    sendBleData();
  }

  // "Thread" letture da zumaEyes
  if(curr_ms - eye_prev_ms > eye_interval) {
    eye_prev_ms = curr_ms;
    updateDistances();
  }
  
  // Leggi le cose Bluetooth
  handleBleInput();
}
