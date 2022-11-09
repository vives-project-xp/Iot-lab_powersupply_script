
import time # time voor sleeps
import serial # serial zorgt voor communicatie aan de hand van scpi commands
import random


class powerSupply:

  def __init__(self, serialPort): # maakt instantie van klasse aan met port gelijk aan de input
    self.conn = serial.Serial(port= serialPort, baudrate=115200, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE, 
    stopbits=serial.STOPBITS_ONE, timeout=1)

  def setVoltage(self, voltage): # set de voltage
    voltageMessage = 'VOLTage {}<LF>\n'.format(voltage)
    self.conn.write(voltageMessage.encode()) # write de message naar de voeding

  def setCurrent(self, current):
    voltageMessage = 'CURRent {}<LF>\n'.format(current)
    self.conn.write(voltageMessage.encode()) # write de message naar de voeding

  def getVoltage(self):
    message = 'MEASure:VOLTage?\n'
    self.conn.write(message.encode()) # write de message naar de voeding

  def getCurrent(self):
    message = 'MEASure:CURRent?\n'
    self.conn.write(message.encode()) # write de message naar de voeding

  def turnOff(self):
    message = b'OUTput OFF\r\n' # werkt niet met .encode, maar wel als binary string
    self.conn.write(message) # write de message naar de voeding

  def turnOn(self):
    message = b'OUTput ON\r\n' # werkt niet met .encode, maar wel als binary string
    self.conn.write(message) # write de message naar de voeding

  def setRandomCurrent(self): # zet de stroom van de voeding iedere 5 seconden op een random waarde
    self.setCurrent(round(random.uniform(1,10),1))
    time.sleep(5)

  def setRandomVoltage(self): # zet de spanning van de voeding iedere 5 seconden op een random waarde
    self.setVoltage(random.randint(22,45))
    time.sleep(5)
