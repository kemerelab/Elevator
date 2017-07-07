#include <SPI.h>
#include "AMIS30543.h"

const uint8_t amisDirPin = 8;
const uint8_t amisStepPin = 9;
const uint8_t amisSlaveSelect = 10;

float input_speed;
float input_step;
int input_mode;
float input_torque;

AMIS30543 stepper;

void setup()
{
  Serial.begin(115200);
  SPI.begin();
  stepper.init(amisSlaveSelect);

  // Drive the NXT/STEP and DIR pins low initially.
  pinMode(amisStepPin, OUTPUT);
  digitalWrite(amisStepPin, LOW);
  pinMode(amisDirPin, OUTPUT);
  digitalWrite(amisDirPin, LOW);

  // Give the driver some time to power up.
  delay(1);

  // Reset the driver to its default settings.
  stepper.resetSettings();

  // Set the current limit.  You should change the number here to
  // an appropriate value for your particular system.
  stepper.setCurrentMilliamps(1750);

  // Enable the motor outputs.
  stepper.enableDriver();
}

void loop()
{
  if(Serial.available()){
      String data = Serial.readString();
  
      // convert speed from RPM to milliseconds per step
      // 1 RPM = 200/60 steps/sec
      input_speed = 1/(data.substring(1,5).toInt()*float(200./60000));
   
      input_step = data.substring(6,14).toInt();
      input_mode = data.substring(15,18).toInt();
      input_torque = data.substring(19,20).toInt()/10.0;

      if(data.substring(21) == "Up")
        setDirection(0);
      if(data.substring(21) == "Down")
        setDirection(1);
  
      // valid step modes: 1, 2, 4, 8, 16, 32, 64, 128
      stepper.setStepMode(input_mode);

      for (int x = 0; x < input_step; x++)
      {
        step(input_speed, input_torque);
        Serial.println(x);
      }
  }
}

// Sends a pulse on the NXT/STEP pin to tell the driver to take
// one step, and also delays to control the speed of the motor.
void step(float input_speed)
{
  // The NXT/STEP minimum high pulse width is 2 microseconds.
  digitalWrite(amisStepPin, HIGH);
  // delay = time each step takes, or
  // delay = ((60,000 msecs)/(200 steps)) * (1/RPM)
  delay((60000/200) * (1/input_speed));
  digitalWrite(amisStepPin, LOW);
  delay((60000/200) * (1/input_speed));
}

// Writes a high or low value to the direction pin to specify
// what direction to turn the motor.
void setDirection(bool dir)
{
  // The NXT/STEP pin must not change for at least 0.5
  // microseconds before and after changing the DIR pin.
  delayMicroseconds(1);
  digitalWrite(amisDirPin, dir);
  delayMicroseconds(1);
}
