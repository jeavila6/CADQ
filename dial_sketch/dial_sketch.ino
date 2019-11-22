#define DIAL A0  // potentiometer

const int minValue = 0;
const int maxValue = 20;

void setup() {
  Serial.begin(9600);
}

void loop() {
  int potValue = analogRead(DIAL);
  int dialValue = map(potValue, 0, 1023, minValue, maxValue);
  Serial.println(dialValue);
}
