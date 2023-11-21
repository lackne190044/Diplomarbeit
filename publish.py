import paho.mqtt.client as paho
from time import sleep
import random

broker="localhost"
port=1883

sensor_id = "test"
value = 20.0

def on_publish(client,userdata,result):             #create function for callback
#    print("data published \n")
    pass

client1= paho.Client("control1")                           #create client object
client1.on_publish = on_publish                          #assign function to callback
client1.connect(broker,port)                                 #establish connection

for _ in range(50):
    value = random.randrange(0, 50)
    ret= client1.publish(f"telegraf/sensors/test/1", value)                   #publish
    sleep(1)
