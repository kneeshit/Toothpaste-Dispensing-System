#include <Servo.h>
#include <PID_v1.h>

const int servoPin = 9;           // Servo Pin
const int trigPin = 7;            // Trig Pin for HC-SR04
const int echoPin = 6;            // Echo Pin for HC-SR04

float Kp = 3;                   // Initial Proportional Gain
float Ki = 0;                     // Initial Integral Gain
float Kd = 0.5;                   // Initial Derivative Gain
double Setpoint, Input, Output, ServoOutput;

PID myPID(&Input, &Output, &Setpoint, Kp, Ki, Kd, DIRECT);  // Initialize PID

Servo myServo;  // Initialize Servo

void setup() {
  Serial.begin(9600);              // Begin Serial communication
  myServo.attach(servoPin);        // Attach Servo
  pinMode(trigPin, OUTPUT);        // Trig pin as output
  pinMode(echoPin, INPUT);         // Echo pin as input

  Input = readPosition();          // Calls function readPosition() to set ball position as input to the PID
  
  myPID.SetMode(AUTOMATIC);        // Set PID to AUTOMATIC mode
  myPID.SetOutputLimits(-40, 40);  // Set Output limits to -80 and 80 degrees
}

void loop() {
  Setpoint = 12;                  // Set the target position (15 cm in this case)
  Input = readPosition();         // Read current position
  
  myPID.Compute();                // Compute Output within the range of -80 to 80 degrees
  
  ServoOutput = 90 + Output;     // 102 degrees is your horizontal reference
  myServo.write(ServoOutput);     // Move the servo to the calculated position
}

float readPosition() {
  long duration;
  int cm;
  
  // Trigger the sensor by sending a 10us HIGH pulse to the Trig pin
  digitalWrite(trigPin, LOW);  
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10); 
  digitalWrite(trigPin, LOW);

  // Read the Echo pin. Duration will be the time (in microseconds) for the echo to return
  duration = pulseIn(echoPin, HIGH);

  // Calculate the distance in cm
  cm = duration / 24 / 2;
  
  // Limit the maximum value to 30 cm
  if (cm > 25) {
    cm = 25;
  }

  Serial.println(cm);  // Print the distance for debugging purposes

  return cm;           // Return the measured distance
}
