#include <SoftwareSerial.h>

//Define the pins used for receiving
//and transmitting information via Bluetooth
const int rxpin = 10;
const int txpin = 11;

int motorA1 = 5; // Pin  2 of L293
int motorA2 = 6; // Pin  7 of L293
int motorB1 = 3; // Pin 10 of L293
int motorB2 = 9; // Pin 14 of L293
int vel = 255; // Speed Of Motors (0-255)
int state = '0'; // Initialise Motors


//Variable to store input value
//initialized with arbitrary value
char k = 'A';
//Connect the Bluetooth module
SoftwareSerial bluetooth(rxpin, txpin);

//Define the pin to control the light
int lightbulb = 13;

void setup()
{
  //Set the lightbulb pin to put power out
  pinMode(lightbulb, OUTPUT);
 pinMode(motorA1, OUTPUT);
pinMode(motorA2, OUTPUT);
pinMode(motorB1, OUTPUT);
pinMode(motorB2, OUTPUT);
  //Initialize Serial for debugging purposes
  Serial.begin(115200);
  Serial.println("Serial ready");
  //Initialize the bluetooth
  bluetooth.begin(115200);
  bluetooth.println("Bluetooth ready");
}

void loop()
{
  //Check for new data
  if(bluetooth.available()){
    //Remember new data
    k = bluetooth.read();
    //Print the data for debugging purposes
    Serial.println(k);
  }
  //Turn on the light if transmitted data is H
  if( k == '0' ){//STOP
     analogWrite(motorA1, 0); 
analogWrite(motorA2, 0); 
analogWrite(motorB1, 0); 
analogWrite(motorB2, 0); 
  }
  //Turn off the light if transmitted data is L
  else if( k == '1') {//FORWARD
    analogWrite(motorA1, vel); 
analogWrite(motorA2, 0); 
analogWrite(motorB1, vel); 
analogWrite(motorB2, 0); 
  }
  else if( k == '4') {//back-change
    analogWrite(motorA1, vel); 
analogWrite(motorA2, 0); 
analogWrite(motorB1, 0); 
analogWrite(motorB2, vel); 
  }
  else if( k == '2') {//RIGHT
   analogWrite(motorA1, vel); 
analogWrite(motorA2, 0); 
analogWrite(motorB1, 0); 
analogWrite(motorB2, vel); 
  }
  else if( k == '3') {//LEFT
    analogWrite(motorA1, 0); 
analogWrite(motorA2, vel);
analogWrite(motorB1, vel);
analogWrite(motorB2, 0); 
  }
  //Wait ten milliseconds to decrease unnecessary hardware strain
   delay(10);
}
