import numpy as np
import scipy.stats as sc
import matplotlib.pyplot as plt
import matplotlib.ticker

BINARY_OUTPUT = "random.bin"

filein = open(BINARY_OUTPUT, 'rb')
#file_array = np.fromfile(flile, dtype=np.int32, count= 4, sep="")
file_array = filein.readlines()
file_array = np.uint32(file_array)
print(file_array)
file_array_float = file_array.astype(np.float32)/4294967295
print(file_array_float)
sums = list()
#print(len(file_array_float))
#for i in range(0, len(file_array_float)):
#  print(i)
#  sums.append(sum(file_array_float[i:len(file_array_float)]))
for i in range(0, 1000):
   #print(i)
   sums.append(sum(file_array_float[i:1000]))
plt.hist(sums, bins = 1000)
plt.show()  
print(sums[0:1000])