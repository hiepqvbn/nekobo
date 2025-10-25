int MOTOR_B_IN1 = 5;
int MOTOR_B_IN2 = 6;
int MOTOR_A_IN1 = 9;
int MOTOR_A_IN2 = 10;
int speedValue = 0;

void setup()
{
  pinMode(MOTOR_B_IN1, OUTPUT);
  pinMode(MOTOR_B_IN2, OUTPUT);
  pinMode(MOTOR_A_IN1, OUTPUT);
  pinMode(MOTOR_A_IN2, OUTPUT);
  Serial.begin(9600);
  Serial.println("Arduino ready");
}

void loop()
{
  if (Serial.available() > 0)
  {
    String input = Serial.readStringUntil('\n');
    input.trim();

    if (input.startsWith("forward"))
    {
      int spd = input.substring(7).toInt();
      analogWrite(MOTOR_A_IN1, spd);
      analogWrite(MOTOR_A_IN2, 0);
      Serial.println("Moving forward at " + String(spd));
    }
    else if (input.startsWith("backward"))
    {
      int spd = input.substring(8).toInt();
      analogWrite(MOTOR_A_IN1, 0);
      analogWrite(MOTOR_A_IN2, spd);
      Serial.println("Moving backward at " + String(spd));
    }
    else if (input == "stop")
    {
      analogWrite(MOTOR_A_IN1, 0);
      analogWrite(MOTOR_A_IN2, 0);
      Serial.println("Stopped");
    }
  }
}
