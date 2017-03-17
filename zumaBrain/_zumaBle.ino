void handleBleInput() {
  static byte ndx = 0;
  char rc;

#ifdef LOG_SERIAL
  if (Serial.available() > 0) {
    Serial.println("incoming");
  }
#endif

  while (BleSerial.available() > 0 && ble_is_new == false) {
    rc = BleSerial.read();

    if (rc != EOP) {
      ble_chars[ndx] = rc;
      ndx++;
      if (ndx >= ble_size) {
        ndx = ble_size - 1;
      }
    } else {
      ndx = 0;
      ble_is_new = true;
    }
  }

  if (ble_is_new == true) {
    size_t control;
    int data[2];
    char *token = strtok(ble_chars, " ");

    for (size_t i = 0; i < 3; i++) {
      if (token) {
        if (i == 0) {
          control = atoi(token);
        } else {
          data[i - 1] = atoi(token);
        }
        token = strtok(NULL, " ");
      }
    }

#ifdef LOG_SERIAL
      Serial.println(control);
#endif

    /* Verifica il tipo di pacchetto
     *  
     *  10 SPEED_LEFT SPEED_RIGHT>
     */
    switch(control) {
      case 10:
        blePilot(data);
        break;
    }
    
    // Reset
    ble_is_new = false;
    memset(ble_chars, 0, sizeof(ble_chars));
  }
}

/**
 * Per ora invia solo le letture distanze
 */
void sendBleData() {
  BleSerial.print(distances[SLEFT]);
  BleSerial.print(distances[SMIDDLE]);
  BleSerial.print(distances[SRIGHT]);
}

/**
  Motori comandati dagli input via Bluetooth
*/
void blePilot(int data[2]) {
  
#ifdef LOG_SERIAL
    Serial.println(data[0]);
    Serial.println(data[1]);
#endif

    setSpeeds(data[0], data[1]);    
}
