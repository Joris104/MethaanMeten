
int pins[] = {A0};
int numMetingen = 1000;
void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  for(int i = 0; i < sizeof(pins)/sizeof(int);i++){
    pinMode(A0, INPUT);
  }
}
void loop() {
  for(int i = 0; i < sizeof(pins)/sizeof(int);i++){
    float output[numMetingen];
    int ts_start = millis();
    for(int j = 0; j < numMetingen; j++){
      output[j] = analogRead(pins[i]);
    }
    int ts_end = millis();
    //Serial.println(ts_end - ts_start);
    for(int j = 0; j < numMetingen; j++){
      Serial.print(pins[i]);
      Serial.print(",");
    Serial.println(output[j]);
    }
    
  }
}
