from random import random
import paho.mqtt.client as mqtt
from serial_communication import powerSupply
from threading import Thread

power = powerSupply('/dev/ttyUSB0')


def on_connect(client, userdata, flags, rc):
    # This will be called once the client connects
    print(f"Connected with result code {rc}")
    # Subscribe here!
    client.subscribe("voltage")
    client.subscribe("current")
    client.subscribe("state")
    client.subscribe("randomVoltage")


def on_message(client, userdata, msg):
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


client = mqtt.Client("python_app") # client ID "mqtt-test"
client.on_connect = on_connect
client.on_message = on_message
client.username_pw_set("mqttuser", "lab1234")
client.connect('172.16.100.243', 1883)

# Start networking daemon
mqttThread = Thread(client.loop_forever())
# client.loop_forever() # loops in this thread and blocks everything else ?
print("after starting mqtt")








