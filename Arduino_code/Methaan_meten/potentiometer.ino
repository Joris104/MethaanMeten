#include <SPI.h>
const int spd = 20000000;

void digitalPotWrite (int slave, int data){
  SPI.beginTransaction(SPISettings(spd,MSBFIRST,SPI_MODE0));
  pinMode(slave,LOW);
  delay(100);
  //Data transfer
  pinMode(slave,HIGH);
  SPI.endTransaction();
}
