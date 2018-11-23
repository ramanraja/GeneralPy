# how to append to a fixed size array

import numpy as np

arr = np.array(100)
print (arr)

arr = np.zeros(100)
print (arr)
print()

for i in range(10):
    for j in range(10):
        arr[10*i + j] = 10*i + j
print (arr)        
print()

for i in range(10):
    row = np.zeros(10)
    for j in range(10):
        row[j] = 10*i + j
    arr[10*i : 10*(i+1)] = row
print (arr)  
print()

arr = np.zeros(100)
arr = arr.reshape(10,10)
for i in range(10):
    row = np.zeros(10)
    for j in range(10):
        row[j] = j + 10*i
    arr[i] = row
print (arr)  