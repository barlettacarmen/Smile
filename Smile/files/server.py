 #       ___
 #      /   /\
 #     /___/  \
 #     \___\  /_      \_\_\_
 #    /   /\\/ /|    \_
 #   /___/  \_/ |   \_\_\_    \_ \_   \_  \_     \_\_\_
 #   \   \  / \ |        \_  \_\_\_  \_  \_     \_\_
 #    \___\//\_\|  \_\_\_   \_   \_ \_  \_\_\_ \_\_\_
 #     /___/  \
 #     \   \  /
 #      \___\/
 #
 # Copyright 2017 Fabiola Casasopra, Carmen Barletta, Gabriele Iannone, Guido Lanfranchi, Francesco Maio
 #
 # Licensed under the Apache License, Version 2.0 (the "License");
 # you may not use this file except in compliance with the License.
 # You may obtain a copy of the License at
 #
 # 	http://www.apache.org/licenses/LICENSE-2.0
 #
 # Unless required by applicable law or agreed to in writing, software
 # distributed under the License is distributed on an "AS IS" BASIS,
 # WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 # See the License for the specific language governing permissions and
 # limitations under the License.



get_ipython().magic('matplotlib inline')

from pynq import Overlay
Overlay("base.bit").download()
from pynq.iop import Arduino_Analog
from pynq.iop import ARDUINO
from pynq.iop import ARDUINO_GROVE_A1, ARDUINO_GROVE_A2, ARDUINO_GROVE_A3, ARDUINO_GROVE_A4
from pynq.board import LED, RGBLED
import time
import socket
import numpy as np

import matplotlib.pyplot as plt


TEMP_BEFORE_SENDING = 20
#frequency with which sensors will take input from outside
FREQUENCY = 0.05
TIME_OF_EVENT = 60 # fixed as 60sec for the demo
# In final implementation it must be set with respect to the duration of the event

MAX_LEDS = 4
MAX_RGB_LEDS = 2
MAX_RGB_VALUE = 8
 
global flag_crowded
global ss


def Main():
    host = "10.79.3.204"
    port = 5001           
    mySocket = socket.socket()
    mySocket.bind((host,port))           
    mySocket.listen(1)
    conn, addr = mySocket.accept()
    print ("Connection from: " + str(addr))
    flag_crowded = 0
    
    
    data = conn.recv(1024).decode()
    while data !="ciao":
        time.sleep(0.1)
    
    while True:
        readSensorsInput()
        conn.send ("gente".encode())
        
        while not data:
            time.sleep(1)
        data = conn.recv(1024).decode()
        getNotice(str(data))
        flag_crowded = 0                                            
    conn.close()


def readSensorsInput():

    #inizialize readers pins
    proximityPresence1= Arduino_Analog(ARDUINO,ARDUINO_GROVE_A4)
    proximityPresence2= Arduino_Analog(ARDUINO,ARDUINO_GROVE_A3)
    proximitySound= Arduino_Analog(ARDUINO,ARDUINO_GROVE_A2)
    proximityLight= Arduino_Analog(ARDUINO,ARDUINO_GROVE_A1)

    crowdLevel = 0
    ss = 0 #start state
    
    valuesPresence1 = np.zeros(TEMP_BEFORE_SENDING)
    valuesPresence2 = np.zeros(TEMP_BEFORE_SENDING)
    valuesSound = np.zeros(TEMP_BEFORE_SENDING)
    valuesLight = np.zeros(TEMP_BEFORE_SENDING)
    
    #calibration
    
    for i in range(0,TEMP_BEFORE_SENDING):
            valuesPresence1[i] = proximityPresence1.read()[1]
            valuesPresence2[i] = proximityPresence2.read()[1]
            #valuesSound.append(proximitySound.read()[1])
            #valuesLight.append(proximityLight.read()[1])
            time.sleep(FREQUENCY)
    
    cal1 = np.mean(valuesPresence1)
    cal2 = np.mean(valuesPresence2)

    
    while True:
        #inizialize lists for values
        valuesPresence1 = np.zeros(TEMP_BEFORE_SENDING)
        valuesPresence2 = np.zeros(TEMP_BEFORE_SENDING)
        #valuesSound = list()
        #valuesLight = list()
        valuesSound = np.zeros(TEMP_BEFORE_SENDING)
        valuesLight = np.zeros(TEMP_BEFORE_SENDING)
    
        #plt.axis([0,TEMP_BEFORE_SENDING,0,3])
        #plt.ion()
    
        #read input from sensors
        for i in range(0,TEMP_BEFORE_SENDING):
            valuesPresence1[i] = proximityPresence1.read()[1]
            valuesPresence2[i] = proximityPresence2.read()[1]
            valuesSound[i] = proximitySound.read()[0]
            valuesLight[i] = proximityLight.read()[0]
            #valueSound.append(proximitySound.read()[1])
            #valueLight.append(proximityLight.read()[1])
            time.sleep(FREQUENCY)
            #y = valuesSound[i]
            #plt.plot(i,y)
            #plt.show()
            
        #debug 
        #print (len(valuesPresence1))
        #print (valuesPresence1)
        #print (valuesPresence2)
        #print (valueSound)
        #print (valueLight)
    
        #processInput (valuesPresence1, valuesPresence2, valueSound)
        
        avg1 = np.mean(valuesPresence1)
        avg2 = np.mean(valuesPresence2)
        
        #implemento una macchina a stati. 
        # 0 ENTRAMBI SENSORI BASSI
        # 1 PRIMO ALTO SECONDO BASSO MA CI ARRIVO DA 0
        # 2 PRIMO BASSO SECONDO ALTO MA CI ARRIVO DA 0
        # 3 ENTRAMBI ALTI
        # 4 PRIMO BASSO SECONDO ALTO MA CI ARRIVO DA 1
        # 5 PRIMO ALTO SECONDO BASSO MA CI ARRIVO DA 2
        
        if ss == 0:
            print("sono nello stato 0")
            if avg1 > 1.2*cal1 and avg2 < 1.2*cal2:
                ss = 1
            
            elif avg1 < 1.2*cal1 and avg2 > 1.2*cal2:
                ss = 2
                
            elif avg1 > 1.2*cal1 and avg2 > 1.2*cal2:
                ss = 3
                
            elif avg1 < 1.2*cal1 and avg2 < 1.2*cal2:
                ss = 0
                
        elif ss == 1:
            print("sono nello stato 1")
            if avg1 > 1.2*cal1 and avg2 < 1.2*cal2:
                ss = 1
            
            elif avg1 < 1.2*cal1 and avg2 > 1.2*cal2:
                ss = 4
                
            elif avg1 > 1.2*cal1 and avg2 > 1.2*cal2:
                ss = 3
                
            elif avg1 < 1.2*cal1 and avg2 < 1.2*cal2:
                ss = 0
            
        elif ss == 2:
            print("sono nello stato 2")
            if avg1 > 1.2*cal1 and avg2 < 1.2*cal2:
                ss = 5
            
            elif avg1 < 1.2*cal1 and avg2 > 1.2*cal2:
                ss = 2
                
            elif avg1 > 1.2*cal1 and avg2 > 1.2*cal2:
                ss = 3
                
            elif avg1 < 1.2*cal1 and avg2 < 1.2*cal2:
                ss = 0       
        
        elif ss == 3:
            print("sono nello stato 3")
            print("c e qualcuno fermo")
            ss = 0
        
        elif ss == 4:
            print("sono nello stato 4")
            flag_crowded = 1
            ss = 0
            break
        
        elif ss == 5:
            print("sono nello stato 5")
            flag_crowded = 0
            print("uscito qualcuno")
            ss = 0
        



def getNotice(s):
    
    proximityLight= Arduino_Analog(ARDUINO,ARDUINO_GROVE_A1)

    valuesLight = np.zeros(TEMP_BEFORE_SENDING)
    
    #read input from sensors
    for i in range(0,TEMP_BEFORE_SENDING):
        valuesLight[i] = proximityLight.read()[0]
        time.sleep(FREQUENCY)
        
    avgLight = sum(valuesLight)/TEMP_BEFORE_SENDING
    print(avgLight)
    
    threshold = 1
    accesi = 0
    
    if avgLight > threshold:
        accesi = 2
    else:
        accesi = 1
        
    rgb_leds = [RGBLED(i+MAX_LEDS) for i in range (MAX_RGB_LEDS)]
    
    for i in range(MAX_RGB_LEDS):
        rgb_leds[i].off()

    if s == "focus":
        for i in range (accesi):
            rgb_leds[i].on(3) #light blue

    elif s == "party":
        for i in range (accesi):
            rgb_leds[i].on(4) #red

    elif s == "dinner":
        rgb_leds[0].on(4) #red
        rgb_leds[1].on(6) #yellow

    elif s == "sleep":
        for i in range (accesi):
            rgb_leds[i].on(5) #purple

    elif s == "workout":
        for i in range (accesi):
            rgb_leds[i].on(2) #green

    elif s == "chill":
        for i in range (accesi):
            rgb_leds[i].on(1) #blue

    elif s == "travel":
        for i in range (accesi):
            rgb_leds[i].on(6) #yellow

    elif s == "nomatch":
        for i in range (accesi):
            rgb_leds[i].on(7) #white

    elif s == "noevent":
        for i in range (accesi):
            rgb_leds[i].off() # shut down everything

    else:
        print("Error in data transmission from Calendar!")

    time.sleep(TIME_OF_EVENT)

    for i in range (MAX_RGB_LEDS):
        rgb_leds[i].off() # shut down everything
     
         
if __name__ == '__main__':
                Main()






