# signer
A deaf and dumb aid project. Speech to text and text to speech conversion

This was a team project which I completed with A.Mikela

  Items Required:
  Arduino Uno
  Python IDE(Anaconda, Spyder, Python(x,y))
  MPU 6050
  Push Buttons
  Flex Sensors
  Resistors
  Arduino USB cable type A/B

  Steps:
  
  1. Make connections between Arduino and MPU9150(SDA-A4 , SCL-A5 , Vcc-3.3V , GND-Ground , INT-Digital Pin 2)

  2. Install Python and the required libraries.

  3. Now burn the Arduino code in Arduino.

  4. Now for Python part there are two steps:
 
  
  Training : This Involves teaching the algorithm what kind of data it data it should expect. As of now each gesture is associated with   a character ( case sensitive ). This means that you can teach the algorithm a maximum of about 60 different gestures.
  
  Enter the following command in cmd to execute the python script. [port=your arduino com port, target= (gesture):(batch)]
                            
                            python start.py target=a:0 port=COM6
  
  Train the model: trainign the model lets you save gestures and be able to use them later.
                            
                            python learn.py
    
  Testing : Command for predictng a gesture and speech output
  
                            python start.py port=<YOUR_SERIAL_PORT> predict
  
