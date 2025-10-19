int MOTOR_B_IN1 = 5;
int MOTOR_B_IN2 = 6;
int MOTOR_A_IN1 = 9;
int MOTOR_A_IN2 = 10;
int speedValue = 0;

void setup()
{
    Serial.begin(115200);
}

void loop()
{
    if (Serial.available())
    {
        String data = Serial.readStringUntil('\n');
        int comma = data.indexOf(',');
        int left = data.substring(0, comma).toInt();
        int right = data.substring(comma + 1).toInt();

        // TODO: replace with actual motor driver control
        Serial.print("Left: ");
        Serial.print(left);
        
        Serial.print(" Right: ");
        Serial.println(right);
    }
}
