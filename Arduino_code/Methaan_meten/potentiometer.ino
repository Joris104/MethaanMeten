#include <SPI.h>
const int spd = 20000000;
const SPISettings settings = new SPISettings(spd,MSBFIRST,SPI_MODE0);
void digitalPotWrite(slave, data){
  SPI.beginTransaction(settings);
  pinMode(slave,LOW);
  delay(100);
  //Data transfer
  pinMode(slave,HIGH);
  SPI.endTransaction();
}
