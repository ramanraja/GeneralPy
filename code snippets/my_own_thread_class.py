# How to derive a class from Thread

from time import sleep
import threading

class MyOwnThread (threading.Thread):

    def __init__ (self):
        threading.Thread.__init__(self)
        self.terminate = False 
        self.start_action = False
        self.counter = 0
                       
                            
    def run (self):
        while not self.terminate: 
            if (not self.start_action):
                sleep(0)     # equivalent to yield()
            try:
                self.counter += 1
                print ("Counter: {}".format(self.counter))
                sleep(2.0)
            except Exception as e:
                print(e)  
        print ('Worker thread exits.')
        
    
    def open(self):
        self.start_action = True
    
        
    def close(self):
        self.terminate = True
        
            
    def printStats(self):
        print ("Total messages printed {}".format(self.counter))
  
        
#----------------------------------------------------------------------------- 
# MAIN
#----------------------------------------------------------------------------- 

def main(): 
    
    mot = MyOwnThread ()
    mot.open()
    mot.start()
    
    print ("Press CTRL+C to quit...")
    while True:
        try : 
            print ('This is main thread !')
            sleep (10.0)
        except KeyboardInterrupt:
            print ("CTRL+C pressed.")
            break         
    
    mot.printStats()
    mot.close()
    sleep (1.0)
    print("Main thread exits.") 


if __name__ == "__main__":
    main()  
