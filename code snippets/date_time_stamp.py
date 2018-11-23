# how to create temporary file names based on time stamp
# how to find time delta

import time
import datetime
from random import randint

t= datetime.datetime.now()
print(t)
tstr = t.strftime("%Y-%m-%d %H:%M:%S")
print(tstr)

ts = datetime.datetime.now()
file_name = ts.strftime("log_%Y-%m-%d_%H.%M.%S.csv")
print (file_name)

print ('\nPlease wait...')
ts1 = datetime.datetime.now()
time.sleep(5)
ts2 = datetime.datetime.now()
delta = ts2-ts1
print(type(delta))
print(delta)
print(delta.seconds) 
print('Bye !')
