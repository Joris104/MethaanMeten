int pins[] = {A0};
long ts_start;
long ts_meet[800];
int metingen[800];
void setup() {
  Serial.begin(9600);
  for(int i = 0; i < sizeof(pins)/sizeof(int);i++){
    pinMode(pins[i], INPUT);
  }
  
}

void loop() {
  // put your main code here, to run repeatedly:
  ts_start= millis();
  for(int i = 0; i < 800; i++)
  {
    metingen[i] = analogRead(A0); 
    ts_meet[i]=micros();
  }
  //ts_meet=millis();
  for(int i = 0; i < 800; i++)
  {
    Serial.print(pins[0]);
    Serial.print(',');
    Serial.print(ts_meet[i]);
    Serial.print(',');
    Serial.println(metingen[i]);
  }
}
