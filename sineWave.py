from turtle import color
import numpy as np
import math
import matplotlib.pyplot as plt

# x = (2.5*math.sin(-7.9)) + 3.5 # sine wave from 1 to 6
# print(round(x,1))

def calculateSine(input):
  return round((2.5*math.sin(input-7.9)) + 3.5,1)

# print(calculateSine(0))
dayLength = (9*60)//30 # >> 300 seconds in 5 minutes and we want to update every 5 seconds
# print(dayLength)
nightLength = (1*60)//30
print(dayLength + nightLength)

output = []
for i in range(dayLength):
  output.append(calculateSine(i/3)) # change 3 depending on how many values in sine wave

# maxIndex = output.index(4.7)
# for i in range(14):
#   output[maxIndex+i] = 6


for i in range(nightLength):
  output.append(1)

print(output)

plt.plot(output, color="red")
plt.show()
