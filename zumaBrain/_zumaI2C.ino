/**
   Richiede una lettura via I2C a ZumaEyes
*/
byte requestDistance(int address) {
  byte dst;
  Wire.requestFrom(address, 1);

  while (Wire.available() == 0) { }
  dst = Wire.read();

  return dst;
}

/**
   Aggiorna l'array con le distanze inviate da ZumaEyes
*/
void updateDistances() {
  size_t us_pos = 0;

//#ifdef LOG_SERIAL
//  Serial.print(F("Distances: "));
//#endif

  while (requestDistance(USONIC_ADDRESS) < 255) { // Attendo che arrivi il primo byte di start "255"
//#ifdef LOG_SERIAL
//    Serial.println(F("W"));
//#endif
  }
  
  for (us_pos = 0; us_pos < 3; us_pos++) {
    distances[us_pos] = requestDistance(USONIC_ADDRESS);

//#ifdef LOG_SERIAL
//   Serial.print(distances[us_pos]);
//    Serial.print(F(" "));
//#endif
  }

//#ifdef LOG_SERIAL
//  Serial.println(F(" "));
//#endif
}

