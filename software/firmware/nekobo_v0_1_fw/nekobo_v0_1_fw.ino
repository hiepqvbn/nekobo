#include "protocol.h"
#include <stdlib.h>

// Motor pins (adjust to your hardware)
const int MOTOR_L_FORWARD = 5;
const int MOTOR_L_BACK = 6;
const int MOTOR_R_FORWARD = 9;
const int MOTOR_R_BACK = 10;

// LED pins (change if they conflict with motors)
const int LED_R = 3;   // PWM
const int LED_G = 11;  // PWM
const int LED_B = 13;  // digital fallback

// Sensor pin example (A0)
const int SENSOR_PIN = A0;

// Sensor report interval (ms)
const unsigned long SENSOR_INTERVAL_MS = 500;
// Heartbeat interval (ms) - firmware will send a heartbeat periodically
const unsigned long HEARTBEAT_INTERVAL_MS = 1000;

unsigned long lastSensorMillis = 0;
unsigned long lastHeartbeatMillis = 0;

// timing measurement
unsigned long firmwareStartMillis = 0;
unsigned long firmwareInitTimeMs = 0;
unsigned long lastLoopMillis = 0;
unsigned long lastLoopDurationMs = 0;

void setup() {
  unsigned long setupStart = millis();
  firmwareStartMillis = setupStart;
  Serial.begin(57600);

  pinMode(MOTOR_L_FORWARD, OUTPUT);
  pinMode(MOTOR_L_BACK, OUTPUT);
  pinMode(MOTOR_R_FORWARD, OUTPUT);
  pinMode(MOTOR_R_BACK, OUTPUT);

  pinMode(LED_R, OUTPUT);
  pinMode(LED_G, OUTPUT);
  pinMode(LED_B, OUTPUT);

  pinMode(SENSOR_PIN, INPUT);

  Serial.println("Nekobo firmware ready");
  // record init duration
  firmwareInitTimeMs = millis() - setupStart;
  lastLoopMillis = millis();
}

void stopMotors() {
  analogWrite(MOTOR_L_FORWARD, 0);
  analogWrite(MOTOR_L_BACK, 0);
  analogWrite(MOTOR_R_FORWARD, 0);
  analogWrite(MOTOR_R_BACK, 0);
}

void setMotorPair(int pinF, int pinB, int value) {
  // value: -255..255
  value = constrain(value, -255, 255);
  if (value >= 0) {
    analogWrite(pinF, value);
    analogWrite(pinB, 0);
  } else {
    analogWrite(pinF, 0);
    analogWrite(pinB, -value);
  }
}

void setDrive(int leftSpeed, int rightSpeed) {
  setMotorPair(MOTOR_L_FORWARD, MOTOR_L_BACK, leftSpeed);
  setMotorPair(MOTOR_R_FORWARD, MOTOR_R_BACK, rightSpeed);
}

void setLED(int r, int g, int b) {
  r = constrain(r, 0, 255);
  g = constrain(g, 0, 255);
  b = constrain(b, 0, 255);
  analogWrite(LED_R, r);
  analogWrite(LED_G, g);
  // LED_B may not be PWM-capable on all boards; use digital threshold fallback
  digitalWrite(LED_B, (b > 127) ? HIGH : LOW);
}

void sendACK(int id) {
  Serial.print("ACK ");
  Serial.print("0x");
  if (id < 16) Serial.print('0');
  Serial.print(id, HEX);
  Serial.println();
}

void sendNACK(int id, int err) {
  Serial.print("NACK ");
  Serial.print("0x");
  if (id < 16) Serial.print('0');
  Serial.print(id, HEX);
  Serial.print(' ');
  Serial.print("0x");
  Serial.println(err, HEX);
}

void sendSensorReport(int sensor_id, int value) {
  // print message id using macro so it stays in sync with protocol.h
  Serial.print("0x");
  if (MSG_SENSOR_REPORT < 16) Serial.print('0');
  Serial.print(MSG_SENSOR_REPORT, HEX);
  Serial.print(' ');
  Serial.print(sensor_id);
  Serial.print(' ');
  Serial.println(value);
}

void processLine(String line) {
  line.trim();
  if (line.length() == 0) return;

  // Convert to char buffer and tokenize for easier parsing
  char buf[128];
  line.toCharArray(buf, sizeof(buf));
  char *tok = strtok(buf, " \t\r\n");
  if (!tok) return;

  // parse id token, support hex (0xNN) or decimal
  int id = (int)strtol(tok, NULL, 0);

  if (id == 0x01) { // MOVE
    char *t1 = strtok(NULL, " \t\r\n");
    char *t2 = strtok(NULL, " \t\r\n");
    if (!t1 || !t2) {
      sendNACK(id, 0x01); // missing args
      return;
    }
    int left = atoi(t1);
    int right = atoi(t2);
    setDrive(left, right);
    sendACK(id);
  } else if (id == 0x02) { // STOP
    stopMotors();
    sendACK(id);
  } else if (id == 0x03) { // SET_LED
    // parse RGB args
    char *tr = strtok(NULL, " \t\r\n");
    char *tg = strtok(NULL, " \t\r\n");
    char *tb = strtok(NULL, " \t\r\n");
    if (!tr || !tg || !tb) {
      sendNACK(id, ERR_MISSING_ARGS);
      return;
    }
    int r = atoi(tr);
    int g = atoi(tg);
    int b = atoi(tb);
    setLED(r, g, b);
    sendACK(id);
  } else if (id == MSG_HEARTBEAT_REQ) {
    // Reply with heartbeat: init_time_ms and last loop duration (ms)
    sendHeartbeat();
    // ACK the request id
    sendACK(id);
  } else {
    // Unknown id: ignore or reply
    // echo error
    Serial.print("ERR Unknown ID ");
    Serial.println(id, HEX);
  }
}

void sendHeartbeat() {
  // send heartbeat response: id <MSG_HEARTBEAT_RESP> <init_ms> <loop_ms>
  Serial.print("0x");
  if (MSG_HEARTBEAT_RESP < 16) Serial.print('0');
  Serial.print(MSG_HEARTBEAT_RESP, HEX);
  Serial.print(' ');
  Serial.print(firmwareInitTimeMs);
  Serial.print(' ');
  Serial.println(lastLoopDurationMs);
  // toggle onboard LED to indicate heartbeat (D13)
  static bool ledState = false;
  ledState = !ledState;
  digitalWrite(LED_B, ledState ? HIGH : LOW);
}

void loop() {
  // handle incoming serial lines
  while (Serial.available()) {
    String line = Serial.readStringUntil('\n');
    processLine(line);
  }

  // periodic sensor reporting
  unsigned long now = millis();
  // compute loop duration
  lastLoopDurationMs = now - lastLoopMillis;
  lastLoopMillis = now;

  if (now - lastSensorMillis >= SENSOR_INTERVAL_MS) {
    lastSensorMillis = now;
    int val = analogRead(SENSOR_PIN);
    sendSensorReport(0, val); // sensor_id 0
  }

  // periodic heartbeat
  if (now - lastHeartbeatMillis >= HEARTBEAT_INTERVAL_MS) {
    lastHeartbeatMillis = now;
    sendHeartbeat();
  }
}
