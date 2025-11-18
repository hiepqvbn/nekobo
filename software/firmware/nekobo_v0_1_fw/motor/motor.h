#ifndef NEKOBO_MOTOR_H
#define NEKOBO_MOTOR_H

// Motor pins (adjust to your hardware)
#define MOTOR_L_FORWARD 5
#define MOTOR_L_BACK 6
#define MOTOR_R_FORWARD 9
#define MOTOR_R_BACK 10

// LED pins (change if they conflict with motors)
#define LED_R_PIN 3
#define LED_G_PIN 11
#define LED_B_PIN 13

void motor_init();
void stopMotors();
void setDrive(int leftSpeed, int rightSpeed);
void setLED(int r, int g, int b);

#endif // NEKOBO_MOTOR_H
