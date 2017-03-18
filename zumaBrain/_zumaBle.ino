void bleHandleInput() {
  static byte ndx = 0;
  char rc;

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
    
//#ifdef LOG_SERIAL
//    Serial.print("Control: ");
//#endif

    /* Verifica il tipo di pacchetto

        10 SPEED_LEFT SPEED_RIGHT>
    */
    switch (control) {
      case 10:
        num_pk++;
//#ifdef LOG_SERIAL
//       Serial.println(control);
//#endif
        blePilot(data);
        break;
      default:
        num_errors++;
        setSpeeds(0, 0);
//#ifdef LOG_SERIAL
//       Serial.print(F("ERROR: "));
//        Serial.println(control);
//#endif
        break;
    }

    // Reset
    ble_is_new = false;
    control = 0;
    memset(ble_chars, 0, sizeof(ble_chars));
    delay(10);
  }
}

/**
 * Test con String
 */
void bleHandleInputS() {
  String packet;
  String left;
  String right;
  
  if (BleSerial.available() > 0) {
    packet = BleSerial.readStringUntil(EOP);
    String control = getValue(packet, ' ', 0);

    switch (control.toInt()) {
      case 10:
        left = getValue(packet, ' ', 1);
        right = getValue(packet, ' ', 2);
        setSpeeds(left.toInt(), right.toInt());
        break;
      default:
        Serial.println(control);
    }
  }
}

String getValue(String data, char separator, int index) {
  int found = 0;
  int strIndex[] = { 0, -1 };
  int maxIndex = data.length() - 1;

  for (int i = 0; i <= maxIndex && found <= index; i++) {
    if (data.charAt(i) == separator || i == maxIndex) {
      found++;
      strIndex[0] = strIndex[1] + 1;
      strIndex[1] = (i == maxIndex) ? i + 1 : i;
    }
  }
  return found > index ? data.substring(strIndex[0], strIndex[1]) : "";
}

/**
   Per ora invia solo le letture distanze
*/
void sendBleData() {
  BleSerial.print(F("US "));
  BleSerial.print(distances[SLEFT]);
  BleSerial.print(F(" "));
  BleSerial.print(distances[SMIDDLE]);
  BleSerial.print(F(" "));
  BleSerial.print(distances[SRIGHT]);
}

/**
  Motori comandati dagli input via Bluetooth
*/
void blePilot(int data[2]) {

//#ifdef LOG_SERIAL
//  Serial.print("Motors: ");
//  Serial.print(data[0]);
//  Serial.print(" : ");
//  Serial.println(data[1]);
//#endif

  setSpeeds(data[0], data[1]);
}
