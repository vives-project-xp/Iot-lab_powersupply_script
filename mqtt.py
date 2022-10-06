import paho.mqtt.client as mqtt
from serial_communication import powerSupply

power = powerSupply('COM5')

def on_connect(client, userdata, flags, rc):
    # This will be called once the client connects
    print(f"Connected with result code {rc}")
    # Subscribe here!
    client.subscribe("voltage")
    client.subscribe("current")
    client.subscribe("state")

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
      if(current.isnumeric()):
        print("current message received")
        
        power.setCurrent(current)

client = mqtt.Client("python_app") # client ID "mqtt-test"
client.on_connect = on_connect
client.on_message = on_message
client.username_pw_set("mqttuser", "lab1234")
client.connect('172.16.100.243', 1883)
client.loop_forever()  # Start networking daemon


# port = 1883
# topic = "python/mqtt"
# # generate client ID with pub prefix randomly
# client_id = f'python-mqtt-{random.randint(0, 100)}'
# username = 'mqtt-user'
# password = 'lab123'







