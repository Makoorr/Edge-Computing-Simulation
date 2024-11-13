import time
import math
import random

Time = 0

def next_time_interval (l):
    n=random.random()*1.0 
    inter_event_time = -math.log(1.0 - n)/l 
    return (inter_event_time)

# lamda: lambda number of messages per second (poissonian arrival model)
def Generation_pub_messages_oneTopic(client, lamda, NbreMessages, data_set, topic):
    global Time
    i=0
    
    while i<NbreMessages:
        tt= next_time_interval(lamda)

        print("Publishing Time:",Time) 
        
        time.sleep(tt) # wait
        Time+=tt
        
        message = str(data_set[i])

        client.publish(topic,message) 

        i=i+1