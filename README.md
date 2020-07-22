# signer
A deaf and dumb aid project. Speech to text and text to speech conversion

This was a team project which I completed with A.Mikela as part of our final year project in Electronics and Computer Engineering

  Items Required:
  Arduino nano (Microcontroller)
  Python IDE & Android IDE
  MPU 6050
  Flex Sensors
  Resistors, Push buttons, LEDs
  Bluetooth module (HC-05)
  Android phone

  The project uses the flex sensors and gyro mounted on a glove to translate hand motions into audio enabling the deaf communicate with the hearing.
  And android application translates spoken word to text
  Steps:
  
  1. Burn the Arduino code in Arduino nano from the arduino IDE.

  2. Make the right connections as indicated in the schematic 

  3. Train the model:
   
  Training : This Involves teaching the algorithm what kind of data it should expect.
  
  Enter the following command in cmd to execute the python script. [port=your arduino com port, target= (gesture):(batch)]
                            
                            python main.py target=a:0 port=COM6
  
  NB: Bluetooth and USB use different serial ports so be sure to specify in code or cmd arguments... Also try different baudrates for better results.
  Train the model: trainign the model lets you save gestures and be able to use them later.
                            
                            python learn.py
    
  4. Run the program:
  
  Testing : Command for predictng a gesture and speech output
  
                            python start.py port=<YOUR_SERIAL_PORT> predict
  
