#include "ultrasonic.h"

UltrasonicSensor::UltrasonicSensor(uint8_t trigPin, uint8_t echoPin, unsigned long timeout_us)
  : _trig(trigPin), _echo(echoPin), _timeout_us(timeout_us) {}

void UltrasonicSensor::begin() {
  pinMode(_trig, OUTPUT);
  pinMode(_echo, INPUT);
  digitalWrite(_trig, LOW);
}

long UltrasonicSensor::read_cm() {
  // Trigger pulse
  digitalWrite(_trig, LOW);
  delayMicroseconds(2);
  digitalWrite(_trig, HIGH);
  delayMicroseconds(10);
  digitalWrite(_trig, LOW);

  // Read echo pulse (timeout in microseconds)
  unsigned long duration = pulseIn(_echo, HIGH, _timeout_us);
  if (duration == 0) {
    return -1;
  }
  // Speed of sound ~343 m/s -> 29.1 us per cm for round trip (approx 58 us per cm round trip)
  long cm = duration / 58;
  return cm;
}
