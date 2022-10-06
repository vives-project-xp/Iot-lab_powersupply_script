
import time
import serial

class powerSupply:

  def __init__(self, serialPort):
    self.conn = serial.Serial(port= serialPort, baudrate=115200, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE, 
    stopbits=serial.STOPBITS_ONE, timeout=1)

  def setVoltage(self, voltage):
    voltageMessage = 'VOLTage {}<LF>\n'.format(voltage)
    self.conn.write(voltageMessage.encode())

  def setCurrent(self, current):
    voltageMessage = 'CURRent {}<LF>\n'.format(current)
    self.conn.write(voltageMessage.encode())

  def getVoltage(self):
    message = 'MEASure:VOLTage?\n'
    self.conn.write(message.encode())

  def getCurrent(self):
    message = 'MEASure:CURRent?\n'
    self.conn.write(message.encode())

  def turnOff(self):
    message = b'OUTput OFF\r\n'
    self.conn.write(message)

  def turnOn(self):
    message = b'OUTput ON\r\n'
    self.conn.write(message)
