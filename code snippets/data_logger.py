# logging, with periodic flushing

import time
import datetime
from random import randint

 
def init_log():
    global f
    f.write("time,device_id,temperature,humidity\n")
    
def write_log (jdata):  
    global f, record_count
    ts = datetime.datetime.now()
    f.write(ts.strftime("%Y-%m-%d %H:%M:%S")); f.write(",") 
    f.write(str(jdata['device_id'])); f.write(",")    
    f.write(str(jdata['temperature'])); f.write(",") 
    f.write(str(jdata['humidity'])); f.write("\n")                 
    record_count += 1
    if (record_count >= 10):  
        record_count = 0
        print("flushing...")
        f.flush()
        f.close()
        f = open(fname, "a+")

def close_log():   
    global f     
    f.flush()    
    f.close()
            
            
record_count = 0    
fname = "log_" + str(randint(1,100))+".csv"
print(fname)    
f = open (fname, "w")
init_log()
for i in range(100):
    json_data = {"device_id":i%20, "temperature":2*i, "humidity":3*i}
    write_log(json_data)
close_log()
