import math
import scipy.stats as sc
import numpy as np
import pickle
import struct
BINARY_OUTPUT = "binaryout.bin"

flile = open(BINARY_OUTPUT, 'r')
a = np.fromfile(flile, dtype=np.uint8)
binScr = list()
letters = list()
for item in a:
  binScr.append(np.binary_repr(item, 8))
#print(a[0])
#print(np.binary_repr(a[0], 32))
#print(binScr[0])
print(binScr[0:5])
for i in range(0,100000):
  counter = 0
  val = binScr[i]
  for j in range(0,8):
    if(val[j]=='1'): counter += 1
  if(counter <= 2): letters.append('A')
  elif(counter == 3): letters.append('B')
  elif(counter == 4): letters.append('C')
  elif(counter == 5): letters.append('D')
  elif(counter >= 6): letters.append('E')
print(letters[0:5])

words = list()

for i in range(0,20000):
  words.append("".join(letters[i*5:i*5+5]))
uniqueWords5, counterWords5 = np.unique(words, return_counts = True)
words.clear()

for i in range(0,20000):
  words.append("".join(letters[i*4:i*4+4]))
uniqueWords4, counterWords4 = np.unique(words, return_counts = True)

