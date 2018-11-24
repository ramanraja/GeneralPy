# system camera / web camera
 
from threading import Thread
import numpy as np 
import imutils
import time
import cv2


# TODO: set the camera resolution at source itself
class CameraVideoStream:
	
    def __init__(self):
        self.frame = None
        self.terminate = False
        self.camera_present = True
        self.camera = cv2.VideoCapture(0)
        
        ### if this is not done, fourcc will use default resolution:
        self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, 800)  
        self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 600)        
        time.sleep(0.25)
        (grabbed, junk) = self.camera.read()
        if  not grabbed: 
            print ("No camera found !") 
            self.camera_present = False          


    def start (self):
        if not self.camera_present: 
            return False
        t = Thread(target=self.grab_frame, args=())
        t.daemon = True
        t.start()
        return True


    def stop(self):
        self.camera.release()
        self.terminate = True
        print ('Cam stopped.')
		
		
    def read(self):
        # return the frame most recently captured
        return self.frame
        		
        		
    def grab_frame(self):
        while not self.terminate:
            (grabbed, self.frame) = self.camera.read()    # TODO: will there be dirty reads ?
            if  not grabbed:     
                self.frame = None      
        print ('Frame grabber exits.')


    def get_image_size(self):
        # height, width, depth 
        if (self.frame is None):
            time.sleep(1.0)
            if (self.frame is None):            
                return None
        #width = self.camera.get(cv2.CAP_PROP_FRAME_WIDTH)
        #height = self.camera.get(cv2.CAP_PROP_FRAME_HEIGHT)                
        return (self.frame.shape)

    
    
    
    
    
