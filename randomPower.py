from serial_communication import powerSupply
import random
import time

power = powerSupply('COM5')

while(True):
  power.setVoltage(40)
  power.setCurrent(round(random.uniform(1,10),1))
  time.sleep(5)