#include "Arduino.h"
#include <Wire.h>
#include "registers.h"

#define I2C_ADDR 0x21

#define RESET 33
#define VSYNC 52 //PortB.21
#define PCLK  32 //PortD.10
#define XCLK   7 //PWML6

              //Pin from 51 to 44 are on PortC
#define D0 51 //12
#define D1 50 //13
#define D2 49 //14
#define D3 48 //15
#define D4 47 //16
#define D5 46 //17
#define D6 45 //18
#define D7 44 //19

#define WIDTH  320
#define HEIGHT 240

byte frame[HEIGHT][WIDTH];

void writeReg(byte regID, byte regVal){
  Wire.beginTransmission(I2C_ADDR);
  Wire.write(regID);
  Wire.write(regVal);
  if (Wire.endTransmission(true)) {
    SerialUSB.print(F("ERROR REG 0x"));
    SerialUSB.println(regID,HEX);
  }
  delay(20);
}

byte readReg(byte regID){
  byte regVal;
  Wire.beginTransmission(I2C_ADDR);
  Wire.write(regID);
  Wire.endTransmission(true);
  Wire.requestFrom(I2C_ADDR,1);
  while (Wire.available() == 0);
  regVal = Wire.read();
  delay(20);
  return regVal;
}



void setup() {

  pinMode(RESET,OUTPUT);
  digitalWrite(RESET,HIGH);
  digitalWrite(RESET,LOW);
  digitalWrite(RESET,HIGH);
  
  pinMode(D0, INPUT);
  pinMode(D1, INPUT);
  pinMode(D2, INPUT);
  pinMode(D3, INPUT);
  pinMode(D4, INPUT);
  pinMode(D5, INPUT);
  pinMode(D6, INPUT);
  pinMode(D7, INPUT);
  
  pinMode(VSYNC, INPUT);
  pinMode(PCLK, INPUT);

  int32_t PWM_pin = digitalPinToBitMask(XCLK);
  REG_PMC_PCER1 = 1 << 4;     // Enable peripheral ID 36 (PWM) in the peripheral clock enable register - see 28.15.23
  REG_PIOC_PDR |= PWM_pin;    // Allow peripheral control for PWM_pin
  REG_PIOC_ABSR |= PWM_pin;   // Select peripheral B
  REG_PWM_CPRD6 = 8;          // Period: 84 MHz / 8 = 10.5 MHz - see 38.6.2.2 of datasheet
  REG_PWM_CDTY6 = 4;          // Duty Cycle: 8 / 4  = 0.5
  REG_PWM_ENA = 1 << 6;       // Enable PWML6 (pin 7) - see 38.5.1 and 38.7.5 of datasheet for more info

  SerialUSB.begin(0);
  while(!SerialUSB);
  Wire.begin();

  setupDefault();
  setupQVGA();
  setupYUV422();
  
  writeReg(R_CLKRC,0x06);      //Use external clock
  
  SerialUSB.print(F("PID=0x"));
  SerialUSB.println(readReg(R_PID),HEX); //PID should be 0x76
  SerialUSB.print(F("VER=0x"));
  SerialUSB.println(readReg(R_VER),HEX); //VER should be 0x73

  SerialUSB.println(F("READY"));

}

void setupDefault() {
  writeReg(R_COM7, 0x80);      //Reset OV7670 registers
  
  writeReg(R_TSLB, 0x04);      //Line Buffer Test Option
  writeReg(R_COM10,1 << 5);    //PLCK does not toggle during horizontal blank

  writeReg(R_RSVD_35,0x84);    //Hue correction - undocumented
  writeReg(R_HSYST, 0x00);     //disable some delays
  writeReg(R_HSYEN, 0x00);
  writeReg(R_COM8, 0xC5);      //Enables auto gain, auto white balance and auto exposure
  writeReg(R_HAECC1, 0x78);    //Histogram-based AEC/AGC controls
  writeReg(R_HAECC2, 0x68); 
  writeReg(R_HAECC3, 0xD8); 
  writeReg(R_HAECC4, 0xD8);
  writeReg(R_HAECC5, 0xF0);
  writeReg(R_HAECC6, 0x90);
  writeReg(R_HAECC7, 0x94);
  writeReg(R_COM9, 0x18);      // 4x Gain
  
}

void setupQVGA() {
  //setup for QVGA
  writeReg(R_COM3,  0x04);
  writeReg(R_COM14, 0x19);
  writeReg(R_HSTART,0x16);
  writeReg(R_HSTOP, 0x04);
  writeReg(R_HREF,  0x24);
  writeReg(R_VSTRT, 0x02);     
  writeReg(R_VSTOP, 0x7A);
  writeReg(R_VREF,  0x0A);    
  writeReg(R_SCALING_DCWCTR, 0x11);
  writeReg(R_SCALING_PCLK_DIV, 0xF1);
}

void setupYUV422() {
  //setup for YUV422
  writeReg(R_COM15,0xC0);      //Data format, output range from [00] to [FF]
  writeReg(R_COM9, 0X6A);      //128x gain ceiling
  writeReg(R_MTX1, 0x80);      //Matrix coefficient
  writeReg(R_MTX2, 0x80);      //Matrix coefficient
  writeReg(R_MTX3, 0x00);      //Matrix coefficient
  writeReg(R_MTX4, 0x22);      //Matrix coefficient
  writeReg(R_MTX5, 0x5E);      //Matrix coefficient
  writeReg(R_MTX6, 0x80);      //Matrix coefficient
  writeReg(R_COM13,0x40);      //UV Saturation auto-adjust
}

void loop() {
  char buffer_USB[3];
  if(SerialUSB.available() > 0) {
    SerialUSB.readBytes(buffer_USB,3);
    if(buffer_USB[0] != 0xD0 && buffer_USB[1] == 0xD0) {

      SerialUSB.println(readReg(buffer_USB[0]));
    } else if (buffer_USB[0] != 0xD0 && buffer_USB[1] !=0xD0) {

      writeReg(buffer_USB[0],buffer_USB[1]);
    } else {

      captureImg(WIDTH,HEIGHT,0);
      if (buffer_USB[2] == 0x01) {
        captureImg(WIDTH,HEIGHT,1);
      }
    }
  }
}

void captureImg(uint16_t width, uint16_t height, bool chroma){
  uint16_t x,y;
  noInterrupts();
  
  while(!(REG_PIOB_PDSR & (1 << 21)));  //wait VSYNC high - pin 52 = bit 21 on PortB
  while((REG_PIOB_PDSR & (1 << 21)));   //wait VSYNC low
  y = height;
  while (y--) {
    x = width;
    while (x--){

      while ((REG_PIOD_PDSR & (1 << 10)));                    //wait PCLK low - pin 32 = bit 10 on PortD
      
      if (!chroma) {frame[y][x] = (REG_PIOC_PDSR & 0xFF000) >> 12;}    //read Y 
      while (!(REG_PIOD_PDSR & (1 << 10)));                   //wait PCLK high
      
      while ((REG_PIOD_PDSR & (1 << 10)));                    //wait PCLK low
      
      if (chroma) {frame[y][x] = (REG_PIOC_PDSR & 0xFF000) >> 12;}    //read Cb or Cr
      while (!(REG_PIOD_PDSR & (1 << 10)));                   //wait PCLK high
    }
  }

  for(y = 0;y < height;y++){
    for(x = 0; x < width;x++){
       SerialUSB.write(frame[y][x]);
    }
  }
  interrupts();

}
