void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(A0, INPUT);
  pinMode(A4, INPUT);
  pinMode(A8, INPUT);
}
int pins[] = {A0,A4,A8};
float output = 0;
void loop() {
  for(int pin = 0; pin < 3; pin++){
    for(int i = 0; i < 50; i++) {
      output += analogRead(pins[pin]);
      delay(100);
    }
  Serial.print(pins[pin]);
  Serial.print(",");
  Serial.println(output/50);
  output = 0;
  }
}
