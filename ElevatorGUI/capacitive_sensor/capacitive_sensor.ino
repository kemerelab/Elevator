#include <CapacitiveSensor.h>
#include <Wire.h> // Include the Arduino SPI library
/*
 * CapitiveSense Library Demo Sketch with s7s output
 * Paul Badger 2008; modified by Etienne Ackermann 2016
 * Uses a high value resistor e.g. 10M between send pin and receive pin
 * Resistor affects sensitivity, experiment with values, 50K - 50M. Larger resistor values yield larger sensor values.
 * Receive pin is the sensor pin - try different amounts of foil/metal on this pin
 */

CapacitiveSensor   cs_4_2 = CapacitiveSensor(4,2);        // 10M resistor between pins 4 & 2, pin 2 is sensor pin, add a wire and or foil if desired

const byte s7sAddress = 0x71;

//unsigned int counter = 9900;  // This variable will count up to 65k
char tempString[4];  // Will be used with sprintf to create strings
//int ct;
int resetpin = 8;

void setup()                    
{
   Wire.begin();
   clearDisplayI2C();
   setBrightnessI2C(255);  // High brightness
   delay(1000);
   clearDisplayI2C();
   //ct = 5;
   pinMode(resetpin, INPUT);
   //attachInterrupt(digitalPinToInterrupt(resetpin), resetCapSense, FALLING);
   cs_4_2.set_CS_AutocaL_Millis(0xFFFFFFFF);     // turn off autocalibrate on channel 1 - just as an example
   Serial.begin(115200);
}

void loop()                    
{
    if(!digitalRead(resetpin)){
      cs_4_2.reset_CS_AutoCal();
    }
    /*while(ct<5)
    {
        ct = 6;
        Serial.println(ct);
    }
    */
    long sensorValue =  cs_4_2.capacitiveSensor(30);
    //ct = 7;
    sprintf(tempString, "%4d", sensorValue);
    //Serial.println(ct);
    String omgplsworkpleeeaassseee = String(sensorValue);
    Serial.println(omgplsworkpleeeaassseee);
    // This will output the tempString to the s7s
    s7sSendStringI2C(tempString);
    delay(100);                             // arbitrary delay to limit data to serial port 
}

void resetCapSense(){
  cs_4_2.reset_CS_AutoCal();
  Serial.println("moo");
}

void s7sSendStringI2C(String toSend)
{
  Wire.beginTransmission(s7sAddress);
  for (int i=0; i<4; i++)
  {
    Wire.write(toSend[i]);
  }
  Wire.endTransmission();
}

// Send the clear display command (0x76)
//  This will clear the display and reset the cursor
void clearDisplayI2C()
{
  Wire.beginTransmission(s7sAddress);
  Wire.write(0x76);  // Clear display command
  Wire.endTransmission();
}

// Set the displays brightness. Should receive byte with the value
//  to set the brightness to
//  dimmest------------->brightest
//     0--------127--------255
void setBrightnessI2C(byte value)
{
  Wire.beginTransmission(s7sAddress);
  Wire.write(0x7A);  // Set brightness command byte
  Wire.write(value);  // brightness data byte
  Wire.endTransmission();
}
