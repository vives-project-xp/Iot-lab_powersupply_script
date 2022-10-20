import random
import paho.mqtt.client as mqtt
from serial_communication import powerSupply
from threading import Thread
import time

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
      if(voltage.isnumeric()):
        print('voltage message received')
        power.setVoltage(voltage)
    elif(msg.topic == 'current'):
      current = msg.payload.decode().strip()
      # print("received current after decode:" + current)
      if(float(current)):
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
    

def printTest(client):
  while(True):
    while(randomCurrent | randomVoltage):
      if(randomCurrent):
        number = round(random.uniform(1,10),1)
        power.setCurrent(number)
        client.publish("current",number)
      if(randomVoltage):
        power.setRandomVoltage()
      time.sleep(10)

def startMqtt(client):
  client.loop_forever()

client = mqtt.Client("python_app") # client ID "mqtt-test"
client.on_connect = on_connect
client.on_message = on_message
client.username_pw_set("mqttuser", "lab1234")
client.connect('172.16.101.121', 1883)

# Start networking daemon
mqttThread = Thread(target=startMqtt,args=[client])
effectsThread = Thread(target=printTest, args=[client])
# client.loop_forever() # loops in this thread and blocks everything else ?
print("after starting mqtt")
mqttThread.start()
effectsThread.start()








