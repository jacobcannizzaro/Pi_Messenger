import paho.mqtt.client as paho
import os
import socket
import ssl
from time import sleep
import threading
import pickle

connflag = False

def on_connect(client, userdata, flags, rc):
    global connflag
    global msg
    print("Connected to AWS")
    connflag = True
    print("Connection returned result: " + str(rc) )

def on_message(client, userdata, message):
    # print("in on_message()")
    global puptop
    global msg
    if str(message.topic) != pubtop:
        recvmsg = str(message.payload.decode("utf-8"))
        print(str(message.topic), ": ", recvmsg, "\n\n> ", end = '')
        # if recvmsg == "STOP":
        #     print("client " + str(message.topic) + " has left")
        # chat = input("Enter Message: ")
        # client.publish(pubtop,msg)

    # print(msg.topic+" "+str(msg.payload))

def on_subscribe(client, userdata, mid, granted_qos):
    print("Subscribed:", str(mid), str(grant))

def on_unsubscribe(client, userdata, mid):
    print("Unsubscribed:", str(mid))

def on_disconnect(client, userdata, rc):
    if rc != 0:
        print("unexpected Disconnection")



def pubThread():
    global pubtop
    while 1==1:
        # sleep(5)
        if connflag == True:
            client.publish(pubtop, input("> "))
            print()
            # tempreading = uniform(20.0,25.0)                        # Generating Temperature Readings
            # mqttc.publish("temperature", tempreading, qos=1)        # topic: temperature # Publishing Temperature values
            # print("msg sent: temperature " + "%.2f" % tempreading ) # Print sent temperature msg on console
        else:
            print("waiting for connection...")

client = paho.Client()
client.on_connect = on_connect
client.on_message = on_message
client.on_subscribe = on_subscribe
client.on_unsubscribe = on_unsubscribe
client.on_disconnect = on_disconnect

# awshost = "a1wrobr8i9l833-ats.iot.us-east-1.amazonaws.com"      # Endpoint
# awsport = 8883                                              # Port no.
# clientId = "jakemacbook"                                     # Thing_Name
# thingName = "jakemacbook"                                    # Thing_Name
# caPath = "../connect_device_package/root-CA.crt"                                      # Root_CA_Certificate_Name
# certPath = "../connect_device_package/jakemacbook.cert.pem"                            # <Thing_Name>.cert.pem
# keyPath = "../connect_device_package/jakemacbook.private.key"                          # <Thing_Name>.private.key

credentials = pickle.load(open("connection.pkl", "rb"))
# print("username: " + username + "!")




awshost = credentials['endpoint']
# print("path" + credentials['thingname'])
awsport = 8883                                              # Port no.
clientId = credentials['thingname']                                   # Thing_Name
thingName = credentials['thingname']                                    # Thing_Name
caPath = credentials['pathname'] + "connect_device_package/root-CA.crt"                                      # Root_CA_Certificate_Name
certPath = credentials['pathname'] + "connect_device_package/" + thingName + ".cert.pem"                            # <Thing_Name>.cert.pem
keyPath = credentials['pathname'] + "connect_device_package/" + thingName + ".private.key"


# print("path: " + keyPath)

client.tls_set(caPath, certfile=certPath, keyfile=keyPath, cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)  # pass parameters

client.connect(awshost, awsport, keepalive=60)               # connect to aws server

sleep(1) #ensure correct order... maybe not needed

# global pubtop


#attempt to unpickle file

pubtop = "chat/" + thingName
subtop = "chat/#"

#FLAG = True

client.subscribe(subtop)
# client.loop_start()                                          # Start the loop


sleep(1)

iThread = threading.Thread(target = pubThread)
# iThread.daemon = True
iThread.start()

client.loop_forever()


# msg = input("Enter a message: ")
# client.publish(pubtop, msg)

# while True:
#     if !connflag or msg == "STOP":
#         break

# client.disconnect()
# client.loop_stop()
