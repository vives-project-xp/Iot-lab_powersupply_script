import random
import paho.mqtt.client as mqtt
from serial_communication import powerSupply
from threading import Thread
import time
import math
import matplotlib.pyplot as plt

power = powerSupply('COM5')

randomCurrent = False
randomVoltage = False


def on_connect(client, userdata, flags, rc):
    # This will be called once the client connects
    print(f"Connected with result code {rc}")
    # Subscribe here!
    client.subscribe("voltage")
    client.subscribe("current")
    client.subscribe("state")
    client.subscribe("randomVoltage")
    client.subscribe("currentEffect")
    client.subscribe("voltageEffect")


def on_message(client, userdata, msg):
    global randomCurrent
    global randomVoltage
    print(f"Message received [{msg.topic}]: {msg.payload}")
    if(msg.topic == 'state'):
      if(msg.payload.decode().strip() == "off"):
        power.turnOff()
      elif(msg.payload.decode().strip() == "on"):
        power.turnOn()
    elif(msg.topic == 'voltage'):
      # voltage = msg.payload.decode().strip()
      # print("detected voltage " +voltage)
      # print(voltage.isnumeric())
      voltage = msg.payload.decode().strip()
      if(voltage.isnumeric() and (voltage <= 45 or voltage >= 22)):
        print('voltage message received')
        power.setVoltage(voltage)
    elif(msg.topic == 'current'):
      current = msg.payload.decode().strip()
      # print("received current after decode:" + current)
      if(float(current) and (current <= 10 or current >= 1)):
        print("current message received after float check")
        power.setCurrent(current)
    elif(msg.topic == 'currentEffect'):
      if(msg.payload.decode().strip() == "off"):
        print("turn off effect received")
        randomCurrent = False
      elif(msg.payload.decode().strip() == "on"):
        randomCurrent = True
        print("turn on effect received")
    elif(msg.topic == 'voltageEffect'):
      if(msg.payload.decode().strip() == "off"):
        print("turn off effect received")
        randomVoltage = False
      elif(msg.payload.decode().strip() == "on"):
        randomVoltage = True
        print("turn on effect received")
    
def calculateSine(input):
  return round((2.5*math.sin(input-7.9)) + 3.5,1)

def publishCurrentWave(client, currentWave):
  while(True):
    while(randomCurrent):
        for i in range (currentWave.length):
          time.sleep(5)
          number = currentWave[i]
          power.setCurrent(number)
          client.publish("current",number)

def startMqtt(client):
  client.loop_forever()

# Start by calculating the sine wave we want the current to follow
dayLength = (4*60)//5 # >> 300 seconds in 5 minutes and we want to update every 5 seconds
# print(dayLength)
nightLength = (1*60)//5
# print(length)

output = []
for i in range(dayLength):
  output.append(calculateSine(i/7.5))

for i in range(nightLength):
  output.append(1)

plt.plot(output, color="red")
plt.show()

client = mqtt.Client("python_app") # client ID "mqtt-test"
client.on_connect = on_connect
client.on_message = on_message
client.username_pw_set("mqttuser", "lab1234")
client.connect('172.16.101.121', 1883)

# Start networking daemon
mqttThread = Thread(target=startMqtt,args=[client])
effectsThread = Thread(target=publishCurrentWave, args=[client])
# client.loop_forever() # loops in this thread and blocks everything else ?
print("after starting mqtt")
mqttThread.start()
effectsThread.start()








