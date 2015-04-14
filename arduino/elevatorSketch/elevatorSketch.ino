//Code that manually controls the door of the elevator
// include the atmel I2C libs
#include "mpr121.h"
#include "i2c.h"
#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>

// 11 max digits used
#define DIGITS 11 

// Match key inputs with electrode numbers
#define ONE 8
#define TWO 5
#define THREE 2
#define FOUR 7
#define FIVE 4
#define SIX 1
#define SEVEN 6
#define EIGHT 3
#define NINE 0

//extras (not used)
#define ELE9 9
#define ELE10 10
#define ELE11 11

// called this way, it uses the default address 0x40
Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver();
// you can also call it with a different address you want
//Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver(0x41);

// Depending on your servo make, the pulse width min and max may vary, you 
// want these to be as small/large as possible without hitting the hard stop
// for max range. You'll have to tweak them as necessary to match the servos you
// have!
#define SERVOMIN  120 // this is the 'minimum' pulse length count (out of 4096)
#define SERVOMAX  595 // this is the 'maximum' pulse length count (out of 4096)
#define SERVO_0 275
#define SERVO_90 497

// our servo # counter
uint8_t servonum=1;
uint16_t pulselen = (SERVOMIN + SERVOMAX)/2;

//interupt pin
int irqpin = 2;  // D2
volatile char number='0';
volatile bool newevent;
void setup()
{
  //make sure the interrupt pin is an input and pulled high
  pinMode(irqpin, INPUT);
  digitalWrite(irqpin, HIGH);
  
  //configure serial out
  Serial.begin(9600);
  
  
  //servo setup
  pwm.begin();
  pwm.setPWMFreq(60);  // Analog servos run at ~60 Hz updates
   
   //touch shield setup
  //output on ADC4 (PC4, SDA)
  DDRC |= 0b00010011;
  // Pull-ups on I2C Bus
  PORTC = 0b00110000; 
  // initalize I2C bus. Wiring lib not used. 
  i2cInit();
  
  delay(100);
  // initialize mpr121
  mpr121QuickConfig();
  
  // Create and interrupt to trigger when a button
  // is hit, the IRQ pin goes low, and the function getNumber is run. 
  attachInterrupt(0,getNumber,LOW);
  
  // prints 'Ready...' when you can start hitting numbers
  Serial.println("Ready...");

}
  
// you can use this function if you'd like to set the pulse length in seconds
// e.g. setServoPulse(0, 0.001) is a ~1 millisecond pulse width. its not precise!
void setServoPulse(uint8_t n, double pulse) {
  double pulselength;
  
  pulselength = 1000000;   // 1,000,000 us per second
  pulselength /= 60;   // 60 Hz
  Serial.print(pulselength); Serial.println(" us per period"); 
  pulselength /= 4096;  // 12 bits of resolution
  Serial.print(pulselength); Serial.println(" us per bit"); 
  pulse *= 1000;
  pulse /= pulselength;
  Serial.println(pulse);
  pwm.setPWM(n, 0, pulse);
}
 

void loop()
{
  uint8_t degrees;
  
  if ((number=='1')&&(newevent==true)){
    degrees = 20;
    pulselen = map(degrees, 0, 90, SERVO_0, SERVO_90);
    pwm.setPWM(servonum, 0, pulselen);
    newevent=false;
    Serial.println("open");
    delay(30);
  }
  else if ((number=='2')&&(newevent==true)){
    degrees = 70;
    pulselen = map(degrees, 0, 90, SERVO_0, SERVO_90);
    pwm.setPWM(servonum, 0, pulselen);
    newevent=false;
    Serial.println("close");
    delay(30);
  }
  /*
  if ((number=='1')&&(newevent==true)){
        pulselen --;
        pwm.setPWM(servonum, 0, pulselen);
        newevent=false;
        Serial.print("plen: ");
        Serial.println(pulselen);
        delay(30);
  }
  else if ((number=='3')&&(newevent==true)){
        pulselen ++;
        pwm.setPWM(servonum, 0, pulselen);
        newevent=false;
        Serial.print("plen: ");
        Serial.println(pulselen);
        delay(30);
  }
  */
  
  
}

void getNumber()
{
  int touchNumber = 0;
  uint16_t touchstatus;
  
  touchstatus = mpr121Read(0x01) << 8;
  touchstatus |= mpr121Read(0x00);
  
  for (int j=0; j<12; j++)  // Check how many electrodes were pressed
  {
    if ((touchstatus & (1<<j)))
      touchNumber++;
  }
  
  if (touchNumber == 1)
  {
    newevent=true;
    if (touchstatus & (1<<SEVEN))
      number = '7';
    else if (touchstatus & (1<<FOUR))
      number = '4';
    else if (touchstatus & (1<<ONE))
      number = '1';
    else if (touchstatus & (1<<EIGHT))
      number = '8';
    else if (touchstatus & (1<<FIVE))
      number = '5';
    else if (touchstatus & (1<<TWO))
      number = '2';
    else if (touchstatus & (1<<NINE))
      number = '9';
    else if (touchstatus & (1<<SIX))
      number = '6';
    else if (touchstatus & (1<<THREE))
      number = '3';
    //Serial.println(number);
  }
  //do nothing if more than one button is pressed
/*  else if (touchNumber == 0){
    ;}
  else{
    ;}
    */
}
