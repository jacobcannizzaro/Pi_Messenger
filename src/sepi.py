import paho.mqtt.client as paho
import os
import socket
import ssl
from time import sleep
import threading
import pickle
from tkinter import *
from tkinter import messagebox

connflag = False
pubtop = ""
subtop = ""
client = paho.Client()

# initialise main window
def init(win):
    win.title("SEPI Messenger")
    win.minsize(400,500)
    e.place(bordermode=INSIDE, height=25, width=425, x=0, y=475)
    btn2.place(bordermode=INSIDE, height=25, width=50, x=350, y=450)
    messages.pack()


# button callback     
def Enter_pressed(event):
    global client
    sent = e.get()
    input_user.set('')
    if connflag == True:
            client.publish(pubtop, sent)        
    else:
        messages.insert(INSERT, '%s\n' % sent)

    
    #msg = Message(messages, text=sent, width=400)
    #msg.pack()
    messages.insert(INSERT, '%s\n' % sent)




def on_connect(client, userdata, flags, rc):
    global connflag
    global msg
    messages.insert(INSERT, "Connected to AWS\n")
    # msg2 = Message(win, text="Connected to AWS")
    # print("Connected to AWS")
    connflag = True
    # print("Connection returned result: " + str(rc) )

def on_message(client, userdata, message):
    # print("in on_message()")
    global puptop
    global msg
    if str(message.topic) != pubtop:
        recvmsg = str(message.payload.decode("utf-8"))
        sender_message = str(message.topic) + ": " + recvmsg + "\n\n"
        messages.insert(INSERT, '%s\n' % sender_message)
        # print(str(message.topic), ": ", recvmsg, "\n\n> ", end = '')
        

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
        if connflag == True:
            client.publish(pubtop, input("> "))
            print()
        else:
            print("waiting for connection...")


def connect_client():
    global pubtop
    global subtop
    global client
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_subscribe = on_subscribe
    client.on_unsubscribe = on_unsubscribe
    client.on_disconnect = on_disconnect

    credentials = pickle.load(open("connection.pkl", "rb"))

    awshost = credentials['endpoint']
    awsport = 8883                                              # Port no.
    clientId = credentials['thingname']                                   # Thing_Name
    thingName = credentials['thingname']                                    # Thing_Name
    caPath = credentials['pathname'] + "connect_device_package/root-CA.crt"                                      # Root_CA_Certificate_Name
    certPath = credentials['pathname'] + "connect_device_package/" + thingName + ".cert.pem"                            # <Thing_Name>.cert.pem
    keyPath = credentials['pathname'] + "connect_device_package/" + thingName + ".private.key"

    client.tls_set(caPath, certfile=certPath, keyfile=keyPath, cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)  # pass parameters

    client.connect(awshost, awsport, keepalive=60)               # connect to aws server
    sleep(1) #ensure correct order... maybe not needed
    pubtop = "chat/" + thingName
    subtop = "chat/#"

    client.subscribe(subtop)

    sleep(1)

    client.loop_forever()


def subThread():
    iThread = threading.Thread(target = connect_client)
    iThread.start()



win = Tk()
input_user = StringVar()
e = Entry(win,text=input_user)
e.bind("<Return>", Enter_pressed)
messages = Text(win) 
 
# Gets the requested values of the height and widht.
windowWidth = win.winfo_reqwidth()
windowHeight = win.winfo_reqheight()
 
# Gets both half the screen width/height and window width/height
positionRight = int(win.winfo_screenwidth()/2 - windowWidth/2)
positionDown = int(win.winfo_screenheight()/2 - windowHeight/2)
 
# Positions the window in the center of the page.
win.geometry("+{}+{}".format(positionRight, positionDown))
 
# create a button

btn2 = Button(win, text="Connect", command=subThread)
 
# initialise and start main loop
init(win)

# iThread = threading.Thread(target = subThread)
# iThread.start()

mainloop()




