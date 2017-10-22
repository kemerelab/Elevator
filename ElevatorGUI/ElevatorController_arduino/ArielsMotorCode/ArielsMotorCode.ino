#include <SPI.h>
#include "AMIS30543.h"

const uint8_t amisDirPin = 8;
const uint8_t amisStepPin = 9;
const uint8_t amisSlaveSelect = 10;

float input_speed;
float input_step;
int input_mode;
float input_torque;
float input_delay;

AMIS30543 stepper;

void setup()
{
  Serial.begin(9600);
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
  //Serial.println("moo");
  if(Serial.available()){
      String data = Serial.readString();
      
      // convert speed from RPM to milliseconds per step
      // 1 RPM = 200/60 steps/sec
      int indices[4];
      int j = 0;
      for (int i= 1; i < data.length(); ++i)
      {
        if (data.substring(i,i+1) == "x")
        {
           indices[j] = i;
           ++j;
        }
      }                             
      input_speed = data.substring(1, indices[0]).toFloat();
      input_step = data.substring(indices[0]+1, indices[1]).toInt();
      input_mode = data.substring(indices[1]+1, indices[2]).toInt();
      input_delay = data.substring(indices[2]+1, indices[3]).toFloat();
      if(data.substring(indices[3]+1, data.length()) == "Up")
        setDirection(0);
      if(data.substring(indices[3]+1, data.length()) == "Down")
        setDirection(1);
      
      Serial.println(input_speed);
      Serial.println(input_step);
      Serial.println(input_mode);
      Serial.println(input_delay);
      Serial.println(data.substring(indices[3]+1, data.length()));
      
      // valid step modes: 1, 2, 4, 8, 16, 32, 64, 128
      stepper.setStepMode(input_mode);
      
      for (int x = 0; x < input_step; x++)
      {
        //unsigned long t = micros();
        step(input_delay * 1000);
        //Serial.println(micros()-t);
        Serial.println(x);
      }
  }
}

// Sends a pulse on the NXT/STEP pin to tell the driver to take
// one step, and also delays to control the speed of the motor.
void step(float input_delay)
{
  // The NXT/STEP minimum high pulse width is 2 microseconds.
  digitalWrite(amisStepPin, HIGH);
  // delay = time each step takes, or
  // delay = ((60,000 msecs)/(200 steps)) * (1/RPM)
  delayMicroseconds(input_delay);
  digitalWrite(amisStepPin, LOW);
  delayMicroseconds(input_delay);
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

