/* This script controls the Arduino
 * Two variables to be modified : 
 * pins controls which pins are read from
 * numMetingen controls over how many measurements we average
 * This needs to be over a multiple of 20ms
 * One measurement takes 112 microseconds
 */
int pins[] = {A0};

int numMetingen = 178; 

long ts_start, ts_meet;
void setup() {
  
  Serial.begin(9600);
  
  for(int i = 0; i < sizeof(pins)/sizeof(int);i++){
    pinMode(pins[i], INPUT);
  }
  
  ts_start = millis();
}
void loop() {
  for(int i = 0; i < sizeof(pins)/sizeof(int);i++){
    float output = 0;
    long ts_loop = millis();
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
    
    delay(60000);
  }
}
