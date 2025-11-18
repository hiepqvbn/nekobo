#ifndef NEKOBO_ULTRASONIC_H
#define NEKOBO_ULTRASONIC_H

#include <Arduino.h>

class UltrasonicSensor {
public:
  UltrasonicSensor(uint8_t trigPin = 2, uint8_t echoPin = 3, unsigned long timeout_us = 30000UL);
  void begin();
  // returns distance in centimeters, or -1 on timeout/no-reading
  long read_cm();

private:
  uint8_t _trig;
  uint8_t _echo;
  unsigned long _timeout_us;
};

#endif // NEKOBO_ULTRASONIC_H
