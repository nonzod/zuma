/**
 * Richiede una lettura via I2C a ZumaEyes
 */
byte requestDistance(int address) {
  byte dst;
  Wire.requestFrom(address, 1);

  while (Wire.available() == 0) { }
  dst = Wire.read();

  return dst;
}

/**
 * Aggiorna l'array con le distanze inviate da ZumaEyes
 */
void updateDistances() {
  size_t us_pos = 0;
  
  while (requestDistance(USONIC_ADDRESS) < 255) { } // Attendo che arrivi il primo byte di start "255"
  for (us_pos = 0; us_pos < 3; us_pos++) {
    distances[us_pos] = requestDistance(USONIC_ADDRESS);
  }
}

