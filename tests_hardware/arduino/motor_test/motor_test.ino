// Define motor control pins
int motor1FWD = 3; // Motor 1 Forward PWM
int motor1REV = 5;  // Motor 1 Reverse PWM

int motor2FWD = 9; // Motor 1 Forward PWM
int motor2REV = 10;  // Motor 1 Reverse PWM


void setup() {
  // Set all the motor control pins to outputs
  pinMode(motor1FWD, OUTPUT);
  pinMode(motor1REV, OUTPUT);

  pinMode(motor2FWD, OUTPUT);
  pinMode(motor2REV, OUTPUT);
}

void loop() {
  // Set Motor 1 forward
  analogWrite(motor1FWD, 50);
  analogWrite(motor1REV, 0);

  delay(1000); // Run motors for 2000 milliseconds

  // Set Motor 1 Stop
  analogWrite(motor1FWD, 0);
  analogWrite(motor1REV, 0);

  delay(1000); // Run motors for 2000 milliseconds

  // Set Motor 1 reverse
  analogWrite(motor1FWD, 0);
  analogWrite(motor1REV, 50);

  delay(1000); // Run motors for 2000 milliseconds

  // Set Motor 1 Stop
  analogWrite(motor1FWD, 0);
  analogWrite(motor1REV, 0);

  delay(2000); // Run motors for 2000 milliseconds
}
