#include "protocol.h"
#include <stdlib.h>
#include "motor/motor.h"
#include "sensor/ultrasonic.h"
// Optional hardware watchdog. Define USE_HW_WATCHDOG at compile-time
// to enable AVR hardware watchdog (resets MCU when it locks). This is
// supported on Arduino UNO (AVR). When enabled the code will call
// wdt_reset() periodically while the system is healthy; if the watchdog
// is not reset the MCU will be reset by the hardware.
#if defined(__AVR__) && defined(USE_HW_WATCHDOG)
#include <avr/wdt.h>
#define HW_WATCHDOG_ENABLED 1
#else
#define HW_WATCHDOG_ENABLED 0
#endif

// Ultrasonic sensor pins (HC-SR04) - adjust to your wiring
#define FRONT_TRIG_PIN 7
#define FRONT_ECHO_PIN 8
#define REAR_TRIG_PIN 4
#define REAR_ECHO_PIN 2

// Sensor report interval (ms)
const unsigned long SENSOR_INTERVAL_MS = 500;
// Heartbeat interval (ms) - firmware will send a heartbeat periodically
const unsigned long HEARTBEAT_INTERVAL_MS = 1000;

// Safety distance (cm). If an obstacle is closer than this, MOVE commands
// that would cause motion toward that obstacle will be rejected.
const int SAFETY_DISTANCE_CM = 20;

unsigned long lastSensorMillis = 0;
unsigned long lastHeartbeatMillis = 0;
// Command watchdog: ensures we stop motors when commands stop arriving.
unsigned long lastCommandMillis = 0;
const unsigned long COMMAND_WATCHDOG_MS = 1500UL; // ms

// timing measurement
unsigned long firmwareStartMillis = 0;
unsigned long firmwareInitTimeMs = 0;
unsigned long lastLoopMillis = 0;
unsigned long lastLoopDurationMs = 0;

// Sensor objects
UltrasonicSensor frontSensor(FRONT_TRIG_PIN, FRONT_ECHO_PIN);
UltrasonicSensor rearSensor(REAR_TRIG_PIN, REAR_ECHO_PIN);

void setup() {
  unsigned long setupStart = millis();
  firmwareStartMillis = setupStart;
  Serial.begin(57600);

  // initialize motor and LEDs
  motor_init();

  // initialize ultrasonic sensors
  frontSensor.begin();
  rearSensor.begin();

  // Optionally enable the hardware watchdog (if compiled with -D USE_HW_WATCHDOG)
  if (HW_WATCHDOG_ENABLED) {
    // Enable with ~2s timeout; watchdog will reset MCU if not kicked.
    wdt_enable(WDTO_2S);
    wdt_reset();
    Serial.println("HW watchdog enabled (2s)");
  }

  Serial.println("Nekobo firmware ready");
  // record init duration
  firmwareInitTimeMs = millis() - setupStart;
  lastLoopMillis = millis();
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
    // Safety check: if motion would go forward, check front sensor; if
    // reversing, check rear sensor. If obstacle inside SAFETY_DISTANCE_CM,
    // reject the MOVE and keep motors stopped.
    long avg = (long(left) + long(right)) / 2L;
    if (avg > 0) {
      long d = frontSensor.read_cm();
      if (d >= 0 && d < SAFETY_DISTANCE_CM) {
        // obstacle in front
        stopMotors();
        sendNACK(id, 0x02);
        return;
      }
    } else if (avg < 0) {
      long d = rearSensor.read_cm();
      if (d >= 0 && d < SAFETY_DISTANCE_CM) {
        // obstacle in rear
        stopMotors();
        sendNACK(id, 0x02);
        return;
      }
    }
    // record last command time for watchdog
    lastCommandMillis = millis();
    setDrive(left, right);
    sendACK(id);
    // kick hardware watchdog if enabled
    if (HW_WATCHDOG_ENABLED) wdt_reset();
  } else if (id == 0x02) { // STOP
    lastCommandMillis = millis();
    stopMotors();
    sendACK(id);
    if (HW_WATCHDOG_ENABLED) wdt_reset();
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
    lastCommandMillis = millis();
    setLED(r, g, b);
    sendACK(id);
    if (HW_WATCHDOG_ENABLED) wdt_reset();
  } else if (id == MSG_HEARTBEAT_REQ) {
    // Reply with heartbeat: init_time_ms and last loop duration (ms)
    sendHeartbeat();
    // ACK the request id
    lastCommandMillis = millis();
    sendACK(id);
    if (HW_WATCHDOG_ENABLED) wdt_reset();
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
    long f = frontSensor.read_cm();
    long r = rearSensor.read_cm();
    // sensor_id 1 = front, 2 = rear
    sendSensorReport(1, (int)f);
    sendSensorReport(2, (int)r);
  }

  // periodic heartbeat
  if (now - lastHeartbeatMillis >= HEARTBEAT_INTERVAL_MS) {
    lastHeartbeatMillis = now;
    sendHeartbeat();
    if (HW_WATCHDOG_ENABLED) wdt_reset();
  }

  // command watchdog: if motors are non-zero and we haven't seen a command
  // recently, stop motors and emit a log. This prevents runaway motion when
  // the controller/host becomes unresponsive.
  static bool watchdog_tripped = false;
  if ((now - lastCommandMillis) > COMMAND_WATCHDOG_MS) {
    // If motors are active, stop them and report
    // We do a conservative check: always stop motors when watchdog expires.
    if (!watchdog_tripped) {
      stopMotors();
      Serial.println("WATCHDOG: no commands, motors stopped");
      watchdog_tripped = true;
    }
  } else {
    watchdog_tripped = false;
  }
}
