import paho.mqtt.client as paho
import os
import socket
import ssl
from time import sleep
import threading
import pickle
from Crypto.Cipher import AES

connflag = False
keyaccepted = 0
key = ""

while keyaccepted == 0:
    key = input("Enter a session key: ")
    if(len(key) == 16 or len(key) == 24 or len(key) == 32 ):
        keyaccepted = 1
    else:
        print("key must be 16, 24, or 32 characters exactly. Try again")

def on_connect(client, userdata, flags, rc):
    global connflag
    global msg
    print("Connected to broker")
    connflag = True
    print("Connection returned result: " + str(rc) )

def on_message(client, userdata, message):
    global puptop
    global msg
    if str(message.topic) != pubtop:
        obj2 = AES.new(str(key), AES.MODE_CFB, 's7a6sTM58ZBLiNpR')
        recvmsgEncrypted = message.payload
        m = obj2.decrypt(recvmsgEncrypted)
        f = str(m)
        print(str(message.topic), ": ", f, "\n> ", end = '')

def on_subscribe(client, userdata, mid, granted_qos):
    print("Subscribed:", str(mid), str(grant))

def on_unsubscribe(client, userdata, mid):
    print("Unsubscribed:", str(mid))

def on_disconnect(client, userdata, rc):
    if rc != 0:
        print("Unexpected Disconnection")

def pubThread():
    global pubtop
    while 1==1:
        if connflag == True:
            obj = AES.new(str(key), AES.MODE_CFB, 's7a6sTM58ZBLiNpR')
            m = input("> ")
            z = m
            ciphertext = obj.encrypt(z)
            client.publish(pubtop, ciphertext)
        else:
            print("waiting for connection...")

client = paho.Client()
client.on_connect = on_connect
client.on_message = on_message
client.on_subscribe = on_subscribe
client.on_unsubscribe = on_unsubscribe
client.on_disconnect = on_disconnect



broker = "broker.hivemq.com"
port = 1883
clientId = "alexpi"
thingName = "alexpi"

client.connect(broker, port) # connect to broker

sleep(1)

pubtop = "chat/" + thingName
subtop = "chat/#"


client.subscribe(subtop)

sleep(1)

iThread = threading.Thread(target = pubThread)
iThread.start()
client.loop_forever()
