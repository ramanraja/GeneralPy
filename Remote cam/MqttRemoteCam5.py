# capture camera stream in response to an MQTT message

from cameravideostream import CameraVideoStream 
from datetime import datetime
import paho.mqtt.client as mqtt
import imutils
import time
import sys
import cv2
 
# pip install paho-mqtt
# pip install imutils     

#-------------------------------------------------------------------------------
#                                   MQTT CLIENT
#-------------------------------------------------------------------------------                  
# server = 'broker.mqtt-dashboard.com'  # this also works
# server = 'm2m.eclipse.org'
# server = 'test.mosquitto.org'        
# server = 'localhost'                  # mosquitto -v

# globals  
server = 'broker.mqttdashboard.com'     # http://www.hivemq.com/demos/websocket-client/ 
port = 1883
client = None
topic1 = 'ind/che/vel/maa/407/command'
topic2 = 'ind/che/vel/maa/407/response'

#------------------------------ callbacks ---------------------------- 

def on_connect(client, userdata, flags, rc):
    print('Connected to MQTT server')
    client.subscribe (topic1, qos=0)  # on reconnection, automatically renew
 
def on_publish(client, userdata, mid):
    print("Published msg id: "+str(mid))

def on_subscribe(client, userdata, mid, granted_qos):
    print("Subscribed; mid="+str(mid)+", granted QOS="+str(granted_qos))
    
def on_message(client, userdata, msg):
    global recording, terminate 
    #print(msg.topic+" <- " +str(msg.payload)) 
    dmsg = msg.payload.decode() # decode('utf-8') is default
    print(msg.topic+" <- " + dmsg)
    dmsg = dmsg.lower()
    if (dmsg.startswith("exit")):
        print('Exit command received')
        client.publish(topic2, payload='EXIT', qos=0)
        terminate = True
        return
    if (not dmsg.startswith("toggle")):
        print('Unknown message: [may be OTA]')
        return
    print('Toggle recording command received')        
    recording = not recording
    response = "OFF"
    if recording: 
        response = "ON"    
    print("Now the RC is "+response)   
    client.publish(topic2, payload=response, qos=0)   

#-------------------------------------------------------------------------------
#                                   VIDEO RECORDER
#-------------------------------------------------------------------------------                  

def init_video_recorder (fps=30.0):   
    global writer
    video_file_name = make_video_file_name(False)
    print ("File name: %s"  %(video_file_name))
    (height, width, depth) = cam.get_image_size()    
    
    #width = cam.camera.get(cv2.CAP_PROP_FRAME_WIDTH)
    #height = cam.camera.get(cv2.CAP_PROP_FRAME_HEIGHT)
    
    print ("fps={}, width={}, height={}".format(fps, width, height))   
    #fcc = cv2.VideoWriter_fourcc(*'XVID')  # preferred
    #fcc = cv2.VideoWriter_fourcc(*'MJPG')  # larger file size
    fcc = cv2.VideoWriter_fourcc(*'DIVX')   # on Windows
    writer = cv2.VideoWriter(video_file_name, fcc, fps, (width,height), True)         

def make_video_file_name(static=True):
    fname = 'captured.avi'
    if not static:
        ts = time.time()
        fname = datetime.fromtimestamp(ts).strftime('video_%d-%b_%H.%M.%S.avi')              
    return fname

def stop_recording():
    global writer
    if (writer is not None):
        writer.release()   
#-------------------------------------------------------------------------------                  
#                                   MAIN
#-------------------------------------------------------------------------------       
# globals 
frame_delay = 20  # 1 #  30        # millisec between frames
frame_width = 640
resize_frame = False # True
show_frame =True  #  False  #
recording = False   
terminate = False  
  
print ('Connecting to WC..')
cam = CameraVideoStream () 

if not cam.start():
    print ('Unable to start the RC !')
    exit(0)
init_video_recorder ()   # this needs the camera object started 
  
  
client = mqtt.Client("raman_rajas_SUB_client_1963", clean_session=False)
# client.username_pw_set("User", "password")     
client.on_connect = on_connect
client.on_publish = on_publish
client.on_subscribe = on_subscribe
client.on_message = on_message
client.connect(server, port, keepalive=60)    # temporarily blocking 
####client.subscribe (topic1, qos=0)  # Not here: subscribe in on_connect() !

###client.loop_forever()    # blocking call
client.loop_start()         # start a background thread  
time.sleep(2)
   
cv2.namedWindow('RC',cv2.WINDOW_NORMAL)   

while not terminate:
    frame = cam.read() 
    if frame is None: # there may be a delay in first frame
        continue        
    if resize_frame:
        frame = imutils.resize(frame, width=frame_width) 
    if recording:
        writer.write(frame)    
    if show_frame: 
        cv2.resizeWindow('RC', 16,12)  # width,height
        cv2.moveWindow('RC', 1900,1270)    
        cv2.imshow('RC', frame) 
    key = cv2.waitKey(frame_delay) & 0xFF
    if key == 27: break
            
               
cam.stop()   
stop_recording()
client.loop_stop()   # kill the background thread   
time.sleep(1)    
cv2.destroyAllWindows()
print ('Bye !')        