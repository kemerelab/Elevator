//Download from https://github.com/adafruit/Adafruit-PWM-Servo-Driver-Library
//I'd personally change this to quotes and put the .cpp and .h files within the
//same directory. Ask me if you need help/don't understand what this is doing or
//what this means. 
#include "Adafruit_PWMServoDriver.h"

Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver();

//Letters correspond to different servos...not useful in terms of a naming
//convention. I recommend front1/2, back1/2, right1/2, left1/2 (assuming two 
//servos per door)
//A
#define SERVOAMIN  170
#define SERVOAMAX  556
#define SERVOA_0 260
#define SERVOA_90 495
//B
#define SERVOBMIN  171
#define SERVOBMAX  558
#define SERVOB_0 235
//12 or 13 currently
#define SERVOB_90 440
//95
//C
#define SERVOCMIN  169
#define SERVOCMAX  553
#define SERVOC_0 254
#define SERVOC_90 482
//D
#define SERVODMIN  169
#define SERVODMAX  553
#define SERVOD_0 250
#define SERVOD_90 481
//E
#define SERVOEMIN  170
#define SERVOEMAX  557
#define SERVOE_0 246
#define SERVOE_90 477
//F
#define SERVOFMIN  170
#define SERVOFMAX  556
#define SERVOF_0 249
#define SERVOF_90 477
//G
#define SERVOGMIN  169
#define SERVOGMAX  552
#define SERVOG_0 268
#define SERVOG_90 496
//H
#define SERVOHMIN  169
#define SERVOHMAX  553
#define SERVOH_0 279
#define SERVOH_90 510
//I
#define SERVOIMIN  170
#define SERVOIMAX  556
#define SERVOI_0 255
#define SERVOI_90 482
//J
#define SERVOJMIN  170
#define SERVOJMAX  557
#define SERVOJ_0 240
#define SERVOJ_90 447
//K
#define SERVOKMIN  170
#define SERVOKMAX  556
#define SERVOK_0 255
#define SERVOK_90 492
//L
#define SERVOLMIN  170
#define SERVOLMAX  556
#define SERVOL_0 233
#define SERVOL_90 468
//M
#define SERVOMMIN  168
#define SERVOMMAX  551
#define SERVOM_0 250
#define SERVOM_90 480
//N
#define SERVONMIN  171
#define SERVONMAX  559
#define SERVON_0 233
#define SERVON_90 466
//O
#define SERVOOMIN  170
#define SERVOOMAX  556
#define SERVOO_0 226
#define SERVOO_90 456
//P
#define SERVOPMIN  168
#define SERVOPMAX  551
#define SERVOP_0 236
#define SERVOP_90 465

//This variable is useless
uint8_t servonum = 0;
//not sure why these are globals? there's no reason for this
uint16_t pulselenA;
uint16_t pulselenB;
uint16_t pulselenC;
uint16_t pulselenD;
uint16_t pulselenE;
uint16_t pulselenF;
uint16_t pulselenG;
uint16_t pulselenH;
uint16_t pulselenI;
uint16_t pulselenJ;
uint16_t pulselenK;
uint16_t pulselenL;
uint16_t pulselenM;
uint16_t pulselenN;
uint16_t pulselenO;
uint16_t pulselenP;

int state = 90;

void setup() {
  Serial.begin(9600);
  pwm.begin();
  pwm.setPWMFreq(60); //why?
}

void loop() {
  /*
  Austin's Rendition:
  Input degree is expected to be passed in to the COMPORT
  If there is an input degree available in the port
  Then change the direction of the servo accordingly.

  Few things modified from this logic/added (to both this and ElevatorGUI.py):
  (1) Delays are useless this I think was just for visual feedback
  (2) Input should be Elevator Door ID (front, back, right, left) along with 
      associated state change (0 to 90 degrees). So, two servos per door (?) 
      are being triggered (rename from A, B, C, etc. to front1, front2, back1, 
      back2, etc.)
  (3) With regards to (2), I think the input to these should still be between
      0 and 90 but the ElevatorGUI.py file that'll be interfacing with this 
      code (similar to the other stepper motor) will handle send the exact 
      number to the COMPORT. To do this we need to figure out which servos 
      Etienne accidentally destroyed and which ones are still operational. We
      may need to recalibrate the servos.
  (4) ElevatorGUI.py should have a another number entry box (this is not the
      technical name) added to it along with another use presets checkbox and
      an execution button to close the door (aka trigger the servos). The box
      will be to enter in the degree of the angle if the user wants to do that 
      and the presets checkbox will be to go ahead and trigger all the way to
      90 degrees (all the way open/close). This means that we will need to keep
      track of each door as well as state of door (open/closed). I recommend 
      doing this within the .py file as opposed to here.
  (5) (4) should be repeated for each of the four doors of the elevator.
  */
  if(Serial.available()){
    int input_degree = Serial.readString().toInt();

    /*
    pulselenA = map(input_degree, 0, 90, SERVOA_0, SERVOA_90);
    pwm.setPWM(0, 0, pulselenA);
    */

    
    //*********
    //Opening and Closing slowly
    //Closing!
    int cow = input_degree;
      while(state > input_degree){
        pulselenB = map(90 - state, 0, 90, SERVOB_0, SERVOB_90);
        pulselenJ = map(state, 0, 90, SERVOJ_0, SERVOJ_90);
        pwm.setPWM(1, 0, pulselenB);
        pwm.setPWM(9, 0, pulselenJ);
        delay(25);
        state -= 1;
      }
    //*****
    //Opening!
      while(state < input_degree){
        pulselenB = map(90 - state, 0, 90, SERVOB_0, SERVOB_90);
        pulselenJ = map(state, 0, 90, SERVOJ_0, SERVOJ_90);
        pwm.setPWM(1, 0, pulselenB);
        pwm.setPWM(9, 0, pulselenJ);
        delay(25);
        state += 1;
      }

    //quiet at 71 and 29 degrees
    
    //***** ORiginal StuFF
    //pulselenB = map(90 - input_degree, 0, 90, SERVOB_0, SERVOB_90);
    //pwm.setPWM(1, 0, pulselenB);

    /*
    delay(500);

    
    pulselenC = map(input_degree, 0, 90, SERVOC_0, SERVOC_90);
    pwm.setPWM(2, 0, pulselenC);
    pulselenD = map(input_degree, 0, 90, SERVOD_0, SERVOD_90);
    pwm.setPWM(3, 0, pulselenD);
    

    delay(500);

    pulselenE = map(input_degree, 0, 90, SERVOE_0, SERVOE_90);
    pwm.setPWM(4, 0, pulselenE);
    pulselenF = map(input_degree, 0, 90, SERVOF_0, SERVOF_90);
    pwm.setPWM(5, 0, pulselenF);

    delay(500);

    pulselenG = map(input_degree, 0, 90, SERVOG_0, SERVOG_90);
    pwm.setPWM(6, 0, pulselenG);
    pulselenH = map(input_degree, 0, 90, SERVOH_0, SERVOH_90);
    pwm.setPWM(7, 0, pulselenH);

    delay(500);

    pulselenI = map(input_degree, 0, 90, SERVOI_0, SERVOI_90);
    pwm.setPWM(8, 0, pulselenI);
    */
    
    //***** ORiginal StuFF
    //pulselenJ = map(input_degree, 0, 90, SERVOJ_0, SERVOJ_90);
    //pwm.setPWM(9, 0, pulselenJ);

    /*
    delay(500);

    pulselenK = map(input_degree, 0, 90, SERVOK_0, SERVOK_90);
    pwm.setPWM(10, 0, pulselenK);
    pulselenL = map(input_degree, 0, 90, SERVOL_0, SERVOL_90);
    pwm.setPWM(11, 0, pulselenL);

    delay(500);

    pulselenM = map(input_degree, 0, 90, SERVOM_0, SERVOM_90);
    pwm.setPWM(12, 0, pulselenM);
    pulselenN = map(input_degree, 0, 90, SERVON_0, SERVON_90);
    pwm.setPWM(13, 0, pulselenN);

    delay(500);

    pulselenO = map(input_degree, 0, 90, SERVOO_0, SERVOO_90);
    pwm.setPWM(14, 0, pulselenO);
    pulselenP = map(input_degree, 0, 90, SERVOP_0, SERVOP_90);
    pwm.setPWM(15, 0, pulselenP);

    delay(500);
    */
  }
}

