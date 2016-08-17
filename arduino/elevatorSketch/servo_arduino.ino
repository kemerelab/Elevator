// Use with servo_GUI.py to control servo motors

#include <Adafruit_PWMServoDriver.h>
#define SERVOAMIN  170
#define SERVOAMAX  556
#define SERVOA_0 260
#define SERVOA_90 495
#define SERVOBMIN  171
#define SERVOBMAX  558
#define SERVOB_0 247
#define SERVOB_90 475
#define SERVOCMIN  169
#define SERVOCMAX  553
#define SERVOC_0 254
#define SERVOC_90 482
#define SERVODMIN  169
#define SERVODMAX  553
#define SERVOD_0 250
#define SERVOD_90 481
#define SERVOEMIN  170
#define SERVOEMAX  557
#define SERVOE_0 246
#define SERVOE_90 477
#define SERVOFMIN  170
#define SERVOFMAX  556
#define SERVOF_0 249
#define SERVOF_90 477
#define SERVOGMIN  169
#define SERVOGMAX  552
#define SERVOG_0 268
#define SERVOG_90 496
#define SERVOHMIN  169
#define SERVOHMAX  553
#define SERVOH_0 279
#define SERVOH_90 510
#define SERVOIMIN  170
#define SERVOIMAX  556
#define SERVOI_0 255
#define SERVOI_90 482
#define SERVOJMIN  170
#define SERVOJMAX  557
#define SERVOJ_0 251
#define SERVOJ_90 475
#define SERVOKMIN  170
#define SERVOKMAX  556
#define SERVOK_0 255
#define SERVOK_90 492
#define SERVOLMIN  170
#define SERVOLMAX  556
#define SERVOL_0 233
#define SERVOL_90 468
#define SERVOMMIN  168
#define SERVOMMAX  551
#define SERVOM_0 250
#define SERVOM_90 480
#define SERVONMIN  171
#define SERVONMAX  559
#define SERVON_0 233
#define SERVON_90 466
#define SERVOOMIN  170
#define SERVOOMAX  556
#define SERVOO_0 226
#define SERVOO_90 456
#define SERVOPMIN  168
#define SERVOPMAX  551
#define SERVOP_0 236
#define SERVOP_90 465

Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver();

void setup() {
  Serial.begin(9600);
  pwm.begin();
  pwm.setPWMFreq(60);

  int servo_0[] = {SERVOA_0, SERVOB_0, SERVOC_0, SERVOD_0,
                   SERVOE_0, SERVOF_0, SERVOG_0, SERVOH_0,
                   SERVOI_0, SERVOJ_0, SERVOK_0, SERVOL_0,
                   SERVOM_0, SERVON_0, SERVOO_0, SERVOP_0};

  for(int x = 0; x < 16; x++){
    // replace servo_0[x] with starting position
    pwm.setPWM(x, 0, servo_0[x]);
    delay(50);
  }
}

void loop() {
  if(Serial.available()){
    String data = Serial.readString();
    int input_degree = data.substring(9).toInt();
    if(data.substring(0,1) == "2"){
      uint16_t pulselenA = map(input_degree, 0, 90, SERVOA_0, SERVOA_90);
      pwm.setPWM(0, 0, pulselenA);
      uint16_t pulselenB = map(input_degree, 0, 90, SERVOB_0, SERVOB_90);
      pwm.setPWM(1, 0, pulselenB);
      delay(50);
    }
    if(data.substring(1,2) == "2"){
      uint16_t pulselenC = map(input_degree, 0, 90, SERVOC_0, SERVOC_90);
      pwm.setPWM(2, 0, pulselenC);
      uint16_t pulselenD = map(input_degree, 0, 90, SERVOD_0, SERVOD_90);
      pwm.setPWM(3, 0, pulselenD);
      delay(50);
    }
    if(data.substring(2,3) == "2"){
      uint16_t pulselenE = map(input_degree, 0, 90, SERVOE_0, SERVOE_90);
      pwm.setPWM(4, 0, pulselenE);
      uint16_t pulselenF = map(input_degree, 0, 90, SERVOF_0, SERVOF_90);
      pwm.setPWM(5, 0, pulselenF);
      delay(50);
    }
    if(data.substring(3,4) == "2"){
      uint16_t pulselenG = map(input_degree, 0, 90, SERVOG_0, SERVOG_90);
      pwm.setPWM(6, 0, pulselenG);
      uint16_t pulselenH = map(input_degree, 0, 90, SERVOH_0, SERVOH_90);
      pwm.setPWM(7, 0, pulselenH);
      delay(50);
    }
    if(data.substring(4,5) == "2"){
      uint16_t pulselenI = map(input_degree, 0, 90, SERVOI_0, SERVOI_90);
      pwm.setPWM(8, 0, pulselenI);
      uint16_t pulselenJ = map(input_degree, 0, 90, SERVOJ_0, SERVOJ_90);
      pwm.setPWM(9, 0, pulselenJ);
      delay(50);
    }
    if(data.substring(5,6) == "2"){
      uint16_t pulselenK = map(input_degree, 0, 90, SERVOK_0, SERVOK_90);
      pwm.setPWM(10, 0, pulselenK);
      uint16_t pulselenL = map(input_degree, 0, 90, SERVOL_0, SERVOL_90);
      pwm.setPWM(11, 0, pulselenL);
      delay(50);
    }
    if(data.substring(6,7) == "2"){
      uint16_t pulselenM = map(input_degree, 0, 90, SERVOM_0, SERVOM_90);
      pwm.setPWM(12, 0, pulselenM);
      uint16_t pulselenN = map(input_degree, 0, 90, SERVON_0, SERVON_90);
      pwm.setPWM(13, 0, pulselenN);
      delay(50);
    }
    if(data.substring(7,8) == "2"){
      uint16_t pulselenO = map(input_degree, 0, 90, SERVOO_0, SERVOO_90);
      pwm.setPWM(14, 0, pulselenO);
      uint16_t pulselenP = map(input_degree, 0, 90, SERVOP_0, SERVOP_90);
      pwm.setPWM(15, 0, pulselenP);
      delay(50);
    }
  }
}
