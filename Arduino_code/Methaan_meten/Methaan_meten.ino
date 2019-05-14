/* This script controls the Arduino
 * Two variables to be modified : 
 * pins controls which pins are read from
 * numMetingen controls over how many measurements we average
 * This needs to be over a multiple of 20ms
 * One measurement takes 112 microseconds
 */
#include <SPI.h>
int pins[] = {A0};
int slaveSelect = 46;
int numMetingen = 178; 

long ts_start, ts_meet;

void setup() {
  
  Serial.begin(9600);
  
  for(int i = 0; i < sizeof(pins)/sizeof(int);i++){
    pinMode(pins[i], INPUT);
  }

  // initialize SPI to communicate with potentiometer
  SPI.begin();

  //set constant resistor value of the potentiometer
  SPI.beginTransaction(SPISettings(10000000, MSBFIRST, SPI_MODE0));
  digitalWrite(slaveSelect, LOW);
  SPI.transfer16(256);
  digitalWrite(slaveSelect, HIGH);
  SPI.endTransaction();

  
  ts_start = millis();
}
void loop() {
  for(int i = 0; i < sizeof(pins)/sizeof(int);i++){
    float output = 0;
    for(int i = 0; i < numMetingen; i++){
      output += analogRead(pins[i]);
    }
    
    ts_meet = millis();
    long t =(ts_meet - ts_start);
    Serial.print(pins[i]);
    Serial.print(",");
    Serial.print(t);
    Serial.print(",");
    Serial.println(output/numMetingen);
    
    delay(10000);
  }
}
