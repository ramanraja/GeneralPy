# create a unique file name based on time stamp

def make_video_file_name(static=True):
    fname = 'captured.avi'
    if not static:
        ts = time.time()
        fname = datetime.fromtimestamp(ts).strftime('video_%d-%b_%H.%M.%S.avi')              
    return fname
    
video_file_name = make_video_file_name(False)
print ("File name: %s"  %(video_file_name))    

---------------------------------------------------

# create random file name

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
    if (record_count >= 1000):  
        record_count = 0
        print("flushing...")
        f.flush()
        f.close()
        f = open(fname, "a+")

def close_log():   
    global f         
    f.close()
            
            
record_count = 0    
fname = "log_" + str(randint(1,100))+".csv"
print(fname)    
f = open (fname, "w")
init_log()
for i in range(10000):
    json_data = {"device_id":i, "temperature":35, "humidity":88}
    write_log(json_data)
close_log()

---------------------------------------------------
