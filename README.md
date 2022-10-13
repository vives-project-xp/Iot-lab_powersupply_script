# Iot-lab_powersupply_script

## required modules

- pySerial
- paho-mqtt

to install the required modules run the following two commands in the terminal

```txt
pip install paho-mqtt
pip install pyserial
```

## serial_communication.py

The serial_communication.py file contains the powerSupply class which has methods that can be used to control the owon SPE series 1 CH DC power supply using scpi commands over USB.

### __init__

creates the serial object that will be used. Here the port to which the powerSupply is connected needs to be specified.
Use device manager on windows to find the correct port.

To find the port on linux run the devicesCheck file.
If you cant run it use the following command.

```txt
chmod u+x ./devicesCheck
```

### setVoltage

Use this method to set the voltage. It excepts the voltage to be in the following format '{number}'.

### setCurrent

This method works the same as the previous method but sets the current.

### getVoltage

Retrieves the current voltage.

### getCurrent

Retrieves the current current.

### turnOff

Turns off the power supply.

### turnOn

Turns on the power supply.

## mqtt.py

This script subscribes to voltage, current and state topics on a specified mqtt broker. If needed the names for these topics can be changed. Do make sure you then change them everywhere in the code.
First make sure to change the specified port for the powerSupply object if needed on line 4.

### on_connect

A function that subscribes to the three afformentioned topics when a connection to the broker is made.

### on_message

A function that handles the messages that are received from the broker.
When a message with the topic state is received the power supply will turn on or off depending on the content of the message.
The expected messages here are 'off' or 'on'. Any other message will do nothing

When a message with the topic voltage is received the voltage of the power supply will be changed unless the message is not numeric.

When a message with the topic current is received the same thing will happen but for the current of the power supply.