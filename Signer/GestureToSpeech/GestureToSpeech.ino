
#include <Wire.h>
//#include <SoftwareSerial.h>

boolean isBluetoothEnabled = true;
// Pins connected to the HC-06 bluetooth module
int rxPin = 1;
int txPin = 0;
//SoftwareSerial bluetooth(rxPin, txPin);

// Pins used for I/O
int btnPin1 = 10;
//int btnPin2 = 7;
//int btnMode = 8;
int pin1 = A0;
int pin2 = A1;
int pin3 = A2;
int pin4 = A3;
int pin5 = A4;

// I2C address of the MPU-6050
const int MPU_addr=0x68;
// Variables that will store sensor data
int16_t AcX,AcY,AcZ,Tmp,GyX,GyY,GyZ;

// Status variables, used with buttons
int precBtn1 = HIGH;
//int precBtn2 = HIGH;
int redLedPin = LED_BUILTIN;
void setup(){
  
  pinMode(pin1,INPUT);
  pinMode(pin2,INPUT);
  pinMode(pin3,INPUT);
  pinMode(pin4,INPUT);
  pinMode(pin5,INPUT);

   // Set the pin mode of the LEDs
  pinMode(redLedPin, OUTPUT);
 
  // Start the comunication with the MPU-6050 sensor
  Wire.begin();
  Wire.beginTransmission(MPU_addr);
  Wire.write(0x6B);  // PWR_MGMT_1 register
  Wire.write(0);     // set to zero (wakes up the MPU-6050)
  Wire.endTransmission(true);

  // Start the serial communication
  Serial.begin(38400);
  //bluetooth.begin(38400);
}
void loop(){
  // Read the values of the buttons
  
  int resultBtn1 = digitalRead(btnPin1);
  //int resultBtn2 = digitalRead(btnPin2);
  //int resultMode = digitalRead(btnMode);
  // ON btn1 pressed, start the batch and light up the yellow LED
  if(precBtn1 == HIGH && resultBtn1 == LOW)
  {
    startBatch();
  }
  
  // ON btn2 pressed, toggle the communication channel ( Bluetooth/Serial )
  /*if (precBtn2 == HIGH && resultBtn2 == LOW)
  {
    isBluetoothEnabled=!isBluetoothEnabled;
  }
  
  // Controls the red LED based on the current communication channel
  if (isBluetoothEnabled)
  {
    digitalWrite(redLedPin, HIGH);
  }else{
    digitalWrite(redLedPin, LOW);
  }
  */
  // If the btn1 is pressed, reads the data from the sensor and sends it through the communication channel
  if (resultBtn1==LOW)
  {
    readSensors();
    //Serial.println("read2");  
  }

  // Closes the batch when the button is released
   
  if (precBtn1 == LOW && resultBtn1 == HIGH )
        {
           closeBatch();   
        }

          // Saves the button states
  precBtn1 = resultBtn1;
  //precBtn2 = resultBtn2; 
 }

void readSensors()
{
        // Start the transmission with the MPU-6050 sensor
    Wire.beginTransmission(MPU_addr);
    Wire.write(0x3B);  // starting with register 0x3B (ACCEL_XOUT_H)
    Wire.endTransmission(false);
    Wire.requestFrom(MPU_addr,14,true);  // request a total of 14 registers
    int val1 = analogRead(pin1);int val2 = analogRead(pin2);
    int val3 = analogRead(pin3);int val4 = analogRead(pin4);
    int val5 = analogRead(pin5);
    // Reads the data from the sensor
    AcX=Wire.read()<<8|Wire.read();  // 0x3B (ACCEL_XOUT_H) & 0x3C (ACCEL_XOUT_L)    
    AcY=Wire.read()<<8|Wire.read();  // 0x3D (ACCEL_YOUT_H) & 0x3E (ACCEL_YOUT_L)
    AcZ=Wire.read()<<8|Wire.read();  // 0x3F (ACCEL_ZOUT_H) & 0x40 (ACCEL_ZOUT_L)
    Tmp=Wire.read()<<8|Wire.read();  // 0x41 (TEMP_OUT_H) & 0x42 (TEMP_OUT_L)
    GyX=Wire.read()<<8|Wire.read();  // 0x43 (GYRO_XOUT_H) & 0x44 (GYRO_XOUT_L)
    GyY=Wire.read()<<8|Wire.read();  // 0x45 (GYRO_YOUT_H) & 0x46 (GYRO_YOUT_L)
    GyZ=Wire.read()<<8|Wire.read();  // 0x47 (GYRO_ZOUT_H) & 0x48 (GYRO_ZOUT_L)

    /*    if (isBluetoothEnabled)
    {
      bluetooth.print("START");
      bluetooth.print(" "); bluetooth.print(AcX);
      bluetooth.print(" "); bluetooth.print(AcY);
      bluetooth.print(" "); bluetooth.print(AcZ);
      bluetooth.print(" "); bluetooth.print(GyX);
      bluetooth.print(" "); bluetooth.print(GyY);
      bluetooth.print(" "); bluetooth.print(GyZ);
      bluetooth.print(" "); bluetooth.print(val1);
      bluetooth.print(" "); bluetooth.print(val2);
      bluetooth.print(" "); bluetooth.print(val3);
      bluetooth.print(" "); bluetooth.print(val4);
      bluetooth.print(" "); bluetooth.print(val5);
      bluetooth.println(" END");
    }else{
      */
    Serial.print("START");
    Serial.print(" "); Serial.print(AcX);
    Serial.print(" "); Serial.print(AcY);
    Serial.print(" "); Serial.print(AcZ);
    Serial.print(" "); Serial.print(GyX);
    Serial.print(" "); Serial.print(GyY);
    Serial.print(" "); Serial.print(GyZ);
    Serial.print(" "); Serial.print(val1);
    Serial.print(" "); Serial.print(val2);
    Serial.print(" "); Serial.print(val3);
    Serial.print(" "); Serial.print(val4);
    Serial.print(" "); Serial.print(val5);
    Serial.println(" END");
    //}
}

// Sends the started batch signal
void startBatch()
{
 /* if (isBluetoothEnabled)
  {
    bluetooth.println("STARTING BATCH");
  }else{
 */   Serial.println("STARTING BATCH");
  //}
}

// Sends the closed batch signal
void closeBatch()
{
/* if (isBluetoothEnabled)
  {
    bluetooth.println("CLOSING BATCH");
  }else{
    Serial.println("CLOSING BATCH");
  }*/
}
