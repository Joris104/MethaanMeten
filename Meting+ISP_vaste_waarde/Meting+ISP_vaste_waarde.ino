//************************
//
//Digital pin 53 is the standard SS pin for SPI communication
//
//************************

// inslude the SPI library:
#include <SPI.h>

//input channels + number of channels
const int number_channels = 1;
int pins[number_channels] = {A0};

//number of measurements to take average over
int numMetingen = 178;

//variables
long ts_start, ts_meet;

void setup() {
  // set the selected channel pins as an input
  for(int i = 0; i < number_channels; i++){
    pinMode(pins[i], INPUT);                                  
  }

  //initialize Serial library to read data from arduino
  Serial.begin(9600);
  // initialize SPI to communicate with potentiometer
  SPI.begin();

  //set constant resistor value of the potentiometer
  SPI.beginTransaction(SPISettings(10000000, MSBFIRST, SPI_MODE0));
  digitalWrite(53, LOW);
  SPI.transfer16(31);
  digitalWrite(53, HIGH);
  SPI.endTransaction();
  
  //begin of the measurements
  ts_start = millis();
}

void loop() {
  for( int i = 0; i < number_channels; i++){
    float output = 0;                                         

    for( int j = 0; j < numMetingen; j++){
      output += analogRead(pins[i]);
    }

    ts_meet = millis();
    
    long t = (ts_meet - ts_start);
    Serial.print("Kanaal: ");
    Serial.print(pins[i]);
    Serial.print("     -     Tijd: ");
    Serial.print(t);
    Serial.print("     -     Meting(bits): ");
    Serial.print(output/numMetingen);
    Serial.print("     -     Meting(volt): ");
    Serial.println(output/numMetingen/1024*5);
  }

  delay(5000);  //delay 5 seconden
}
