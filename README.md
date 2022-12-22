# Iot-lab_powersupply_script

## required modules

- pySerial
- paho-mqtt
- numpy
- matplotlib

to install the required modules run the following commands in the terminal. Gebruik op de pi echter wel pip3 in plaats van pip

```txt
pip install paho-mqtt
pip install pyserial
pip install numpy
pip install matplotlib
```

## hoe runnen

python ./mqtt.py op windows en python3 ./mqtt.py op de pi. MAAK VOOR HET RUNNEN ZEKER DAT HET IP ADDRESS VAN DE MQTT BROKER JUIST STAAT.

Het ip is aan te passen op lijn 100.

```py
client.connect('172.16.101.210', 1883)
```

Maak zeker dat je het script opnieuw opstart wanneer je de mqtt broker/home assistant opnieuw opstart.

## sineWave.py

Een script om de sinus die de dag simuleerd te controleren.

```python
def calculateSine(input):
  return round((2.5*math.sin(input-7.6)) + 3.5,1)
```
Berekend de output van de sinus met y waarde tussen 1 en 6 en met een minima ongeveer bij x = 0.

```python
dayLength = (9*60)//30
nightLength = (1*60)//30
```

berekend de benodigde elementen voor de dag en nacht.
9 minuten dag met een update van de stroom elke 30 seconden en 1 minuut nacht met ook een update elke 30 seconden.

```python
output = []
for i in range(dayLength):
  output.append(calculateSine(i/(dayLength/5)))
```

Er wordt per benodigd element een output berekend. We moeten echter i nog delen omdat we anders meerdere sinussen berekenen. Het is mogelijk om manueel te proberen waardoor je het beste deelt, maar in mijn testen blijkt delen door (dayLength/5) altijd goed te werken.

```python
for i in range(nightLength):
  output.append(1)
```

Voeg voor de lengte van de nacht gewoon 1 toe als output.

```python
plt.plot(output, color="red")
plt.show()
```

In SineWave.py wordt hiervan dan nog een plot gemaakt waarmee je kunt zien of de sinus is hoe je hem wilt.

![voorbeeld sinus](/img/example_sinus.png)

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
