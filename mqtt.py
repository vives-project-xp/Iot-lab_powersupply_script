import random
import paho.mqtt.client as mqtt # paho mqtt om te publishen en te subscriben naar/op de mqtt broker
from serial_communication import powerSupply # om scpi commands naar de voeding te kunnen sturen
from threading import Thread # om threads te kunnen starten
import time
import math # voor de sinus te kunnen berekenen
import matplotlib.pyplot as plt # om de sinus te plotten



power = powerSupply('COM5') # object van de klasse powerSupply, met als poort COM5 (windows), op linux is dit iets zoals /dev/ttyUSB0

randomCurrent = False # om te controleren of het sinus effect mag blijven loopen

# wat te doen bij een connectie met een broker
def on_connect(client, userdata, flags, rc):
    # This will be called once the client connects
    print(f"Connected with result code {rc}")
    # Subscribe op de verschillende broker topics
    client.subscribe("voltage")
    client.subscribe("current")
    client.subscribe("state")
    client.subscribe("randomVoltage")
    client.subscribe("currentEffect")

# wat te doen wanneer een message binnenkomt
def on_message(client, userdata, msg):
    global randomCurrent # zorgt ervoor dat we aan de globale variabele kunnen binnen deze functie
    print(f"Message received [{msg.topic}]: {msg.payload}") # print van de message die binnengekomen is en de topic van deze message
    if(msg.topic == 'state'): # wat te doen als de topic state is
      if(msg.payload.decode().strip() == "off"):
        power.turnOff() # zet de voeding uit
      elif(msg.payload.decode().strip() == "on"):
        power.turnOn() # zet de voeding aan
    elif(msg.topic == 'voltage'):
      voltage = msg.payload.decode().strip()
      if(voltage.isnumeric() and (int(voltage) <= 45 or int(voltage) >= 22)): # houd de voltage waarde tussen 22 en 45 anders gebeurt er niets, ook controle of wel een getal ontvangen werd
        print('voltage message received') 
        power.setVoltage(voltage) # zet de voltage van de voeding op de ontvangen waarde
    elif(msg.topic == 'current'):
      current = msg.payload.decode().strip()
      if(float(current) and (float(current) <= 10 or float(current) >= 1)): # houd de voltage waarde tussen 1 en 10 anders gebeurt er niets, ook controle of wel een getal ontvangen werd
        print("current message received after float check")
        power.setCurrent(current) # zet de current van de voeding op de ontvangen waarde
    elif(msg.topic == 'currentEffect'):
      if(msg.payload.decode().strip() == "off"):
        print("turn off effect received")
        randomCurrent = False # stopt de loop van het sinus effect
      elif(msg.payload.decode().strip() == "on"):
        randomCurrent = True # start de loop van het sinus effect
        print("turn on effect received")
    
def calculateSine(input):
  return round((2.5*math.sin(input-7.9)) + 3.5,1) # berekent de sinus aan de hand van de gegeven input

def publishCurrentWave(client, currentWave): # publisht de huidige waarde van de sinus naar de broker en zet ook de current van de voeding naar deze waarde
  while(True):
    while(randomCurrent):
        for i in range (len(currentWave)):
          time.sleep(5) # update elke 5 seconden
          number = currentWave[i]
          print(number)
          if(number == 1.0):
            client.publish("daytime", "off")
            print("published daytime off to mqtt")
          else:
            client.publish("daytime", "on")
            print("published daytime on to mqtt")
          power.setCurrent(number)
          client.publish("current",number)
          if(not randomCurrent): # stopt deze loop wannneer randomCurrent false wordt
            break

def startMqtt(client): # functie om de mqtt loop te starten
  client.loop_forever()

# Start by calculating the sine wave we want the current to follow
dayLength = (4*60)//5 # >> 300 seconds in 5 minutes and we want to update every 5 seconds
# print(dayLength)
nightLength = (1*60)//5
# print(length)

output = []
for i in range(dayLength): # output gedurende de "dag"
  output.append(calculateSine(i/7.5))

for i in range(nightLength): # output gedurende de nacht = 1
  output.append(1)

# plt.plot(output, color="red") # plot van de sinus (inclusief nacht)
# plt.show()

client = mqtt.Client("python_app") # client ID "mqtt-test"
client.on_connect = on_connect
client.on_message = on_message
client.username_pw_set("mqttuser", "lab1234")
client.connect('172.16.101.210', 1883)

# alle settings voor de connectie met de mqtt broker

# Start networking daemon
mqttThread = Thread(target=startMqtt,args=[client]) # de mqtt thread
effectsThread = Thread(target=publishCurrentWave, args=[client, output]) # de sinus thread

mqttThread.start() # start de mqtt thread
effectsThread.start() # start de sinus thread








