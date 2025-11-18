#include "motor.h"
#include <Arduino.h>

void motor_init() {
  pinMode(MOTOR_L_FORWARD, OUTPUT);
  pinMode(MOTOR_L_BACK, OUTPUT);
  pinMode(MOTOR_R_FORWARD, OUTPUT);
  pinMode(MOTOR_R_BACK, OUTPUT);

  pinMode(LED_R_PIN, OUTPUT);
  pinMode(LED_G_PIN, OUTPUT);
  pinMode(LED_B_PIN, OUTPUT);
}

void stopMotors() {
  analogWrite(MOTOR_L_FORWARD, 0);
  analogWrite(MOTOR_L_BACK, 0);
  analogWrite(MOTOR_R_FORWARD, 0);
  analogWrite(MOTOR_R_BACK, 0);
}

static void setMotorPair(int pinF, int pinB, int value) {
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
  analogWrite(LED_R_PIN, r);
  analogWrite(LED_G_PIN, g);
  digitalWrite(LED_B_PIN, (b > 127) ? HIGH : LOW);
}
