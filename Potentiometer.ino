int poti = A0; //analoger pin für potentiometer
int button = 2; //Button mit dem der gewählte emoji gesendet werden soll

void setup() 
  {
  pinMode(poti, INPUT);
  pinMode(button, INPUT);
  Serial.begin(115200);      //Einstellung der Baudrate
  }

void loop() 
  {
    int value = analogRead(poti);
    int pushed = digitalRead(button);
    if(value < 350 && pushed == HIGH){
      Serial.println("happy");
      delay(200);
      } else if(value < 690 && pushed == HIGH) {
        Serial.println("sad");
        delay(200);
        } else if(value > 690 && pushed == HIGH){
          Serial.println("angry");
          delay(200);
          }
    delay(100);
  }
