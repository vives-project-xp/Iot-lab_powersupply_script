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

### Wat zijn SCPI commands

SCPI-commando's zijn ASCII-strings, die via de physical layer naar het apparaat worden gestuurd, waardoor alle communicatie-interfaces worden ondersteund. Het gebruik van deze SCPI-commando's is de eenvoudigste manier om een voeding te programmeren, doordat ze onafhankelijk zijn van de driver en programmeertaal.

[Voor meer info en voorbeelden zie de volgende website](https://magna-power.com/assets/docs/html_ts/index-scpi.html#:~:text=SCPI%20commands%20are%20ASCII%20textual,driver%20and%20programming%20environment%20independent.)

Om deze SCPI commands in python te programmeren hebben we gebruik gemaakt van de pySerial library.

[Zie deze site voor de verschillende functies en hun argumenten](https://pyserial.readthedocs.io/en/latest/pyserial_api.html)

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

Wanneer een bericht ontvangen wordt met van currentEffect wordt het effect waarin de stroom een sinus volgt aan of uitgezet afhankelijk van het bericht.

### calculateSine

Een functie die de output van een sinus bepaald aan de hand van een output.

### publishCurrentWave

Wanneer randomCurrent True is zal om de 5 seconden de volgende waarde van de berekende sinus gepublished worden naar mqtt en zal de stroom van de voeding naar deze waarde gezet worden.

### Threads

In dit programma moeten we gebruik maken van threads omdat we voor onze mqtt client een oneindige loop starten. Als we hiernaast dus nog andere zaken willen doen zoals het stoppen en starten van het sinus current effect dan hebben we threads nodig.
Het starten van threads binnen python is niet moeilijk, hieronder een voorbeeld uit het powersupply script.

```python
from threading import Thread
mqttThread = Thread(target=startMqtt,args=[client]) # Een thread voor de oneindige loop van mqtt, aan target wordt de functie meegegeven die moet uitgevoerd worden en in args de argumenten die de functie nodig heeft
effectsThread = Thread(target=publishCurrentWave, args=[client])

mqttThread.start() # om de thread te starten wordt simpelweg op het object de functie start aangeropen
effectsThread.start()
```