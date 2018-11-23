# np array min, max, median
# running min-max and median

import numpy as np

x = np.array([20,40,50,30,10])
print (x)
print()

print (len(x))
print (min(x))
print (max(x))
print()

print (np.amin(x))
print (np.amax(x))
print (np.median(x))
print('------------------------------------')

arr = np.arange(100)
print(arr)
print()

N = 10  # run length

runmin = np.zeros(N)
runmax = np.zeros(N)
runmedian = np.zeros(N)

pointer = 0
for x in arr:
    runmin[pointer] = x
    runmax[pointer] = x
    runmedian[pointer] = x
    pointer = (pointer+1) % N 
    if (pointer==0):
        print("min: {},  max; {}, mexian: {}". format(np.amin(runmin), np.amax(runmax), np.median(runmedian)))

print('------------------------------------')

arr = np.random.randint(0,50,size=100)
print(arr)
print()

N = 10  # run length

runmin = np.zeros(N)
runmax = np.zeros(N)
runmedian = np.zeros(N)

pointer = 0
for x in arr:
    runmin[pointer] = x
    runmax[pointer] = x
    runmedian[pointer] = x
    pointer = (pointer+1) % N 
    if (pointer==0):
        print("min: {},  max; {}, mexian: {}". format(np.amin(runmin), np.amax(runmax), np.median(runmedian)))
 