// Motor pins
int MOTOR_B_IN1 = 5;
int MOTOR_B_IN2 = 6;
int MOTOR_A_IN1 = 9;
int MOTOR_A_IN2 = 10;

int baseSpeed = 150; // Default speed

void setup()
{
    pinMode(MOTOR_B_IN1, OUTPUT);
    pinMode(MOTOR_B_IN2, OUTPUT);
    pinMode(MOTOR_A_IN1, OUTPUT);
    pinMode(MOTOR_A_IN2, OUTPUT);

    Serial.begin(115200);
    Serial.println("Arduino ready for joystick commands");
}

void loop()
{
    if (Serial.available() > 0)
    {
        String input = Serial.readStringUntil('\n');
        input.trim();

        if (input.startsWith("dir"))
        {
            // Example input: "dir 1 0" (Hat0X=1, Hat0Y=0)
            int space1 = input.indexOf(' ');
            int space2 = input.indexOf(' ', space1 + 1);
            int hatX = input.substring(space1 + 1, space2).toInt();
            int hatY = input.substring(space2 + 1).toInt();

            moveRobot(hatX, hatY);
        }
    }
}

void moveRobot(int hatX, int hatY)
{
    int spd = baseSpeed;

    if (hatX == 0 && hatY == 0)
    {
        stopMotors();
    }
    else if (hatX == 0 && hatY == -1)
    { // forward
        forward(spd);
    }
    else if (hatX == 0 && hatY == 1)
    { // backward
        backward(spd);
    }
    else if (hatX == -1 && hatY == 0)
    { // left
        turnLeft(spd);
    }
    else if (hatX == 1 && hatY == 0)
    { // right
        turnRight(spd);
    }
    else if (hatX == -1 && hatY == -1)
    { // forward-left
        motorAStop();
        motorBForward(spd);
    }
    else if (hatX == 1 && hatY == -1)
    { // forward-right
        motorAForward(spd);
        motorBStop();
    }
    else if (hatX == -1 && hatY == 1)
    { // backward-left
        motorAStop();
        motorBBackward(spd);
    }
    else if (hatX == 1 && hatY == 1)
    { // backward-right
        motorABackward(spd);
        motorBStop();
    }
}

void forward(int spd)
{
    motorAForward(spd);
    motorBForward(spd);
}

void backward(int spd)
{
    motorABackward(spd);
    motorBBackward(spd);
}

void turnLeft(int spd)
{
    motorABackward(spd);
    motorBForward(spd);
}

void turnRight(int spd)
{
    motorAForward(spd);
    motorBBackward(spd);
}

void stopMotors()
{
    motorAStop();
    motorBStop();
}

// --- Motor A ---
void motorAForward(int spd)
{
    analogWrite(MOTOR_A_IN1, spd);
    analogWrite(MOTOR_A_IN2, 0);
}
void motorABackward(int spd)
{
    analogWrite(MOTOR_A_IN1, 0);
    analogWrite(MOTOR_A_IN2, spd);
}
void motorAStop()
{
    analogWrite(MOTOR_A_IN1, 0);
    analogWrite(MOTOR_A_IN2, 0);
}

// --- Motor B ---
void motorBForward(int spd)
{
    analogWrite(MOTOR_B_IN1, spd);
    analogWrite(MOTOR_B_IN2, 0);
}
void motorBBackward(int spd)
{
    analogWrite(MOTOR_B_IN1, 0);
    analogWrite(MOTOR_B_IN2, spd);
}
void motorBStop()
{
    analogWrite(MOTOR_B_IN1, 0);
    analogWrite(MOTOR_B_IN2, 0);
}
