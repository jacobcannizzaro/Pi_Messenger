import paho.mqtt.client as paho
import os
import socket
import ssl
from time import sleep
import threading
import pickle
import tkinter as tk
from tkinter import *
from tkinter import messagebox
from Crypto.Cipher import AES

connflag = False
pubtop = ""
subtop = ""
client = paho.Client()

key = ""

# initialise main window
def init(win):
    win.title("SEPI Messenger")
    win.minsize(400,500)
   # frame1 = tk.Frame(master = win, width= 500, height = 100, bg="red")
    e.place(bordermode=INSIDE, height=25, width=425, x=0, y=475)
    btnSend.place(bordermode=INSIDE, height = 25, width = 75, x = 425, y = 475)
    btn2.place(bordermode=INSIDE, height=25, width=75, x=0, y=0)
    btn2.pack()
    messages.pack()
    
    
def popup():
	 input_user2 = StringVar()
	 popup = Toplevel()
	 popup.title("Enter session key")
	 popup.minsize(400,20)
	 win.withdraw()
	 l=Label(popup, text="Enter Session Key: ")
	 l.grid(row=2, column = 0)
	 e2 = Entry(popup, text=input_user2)
	 e2.grid(row = 2, column = 1)
	 b1 = Button(popup, text = "Submit", command = lambda: handleSessionKey(popup, e2))
	 b1.grid(row=2, column = 2)
	 
def handleSessionKey(window, entryField):
	 global key
	 key = str(entryField.get())
	 if(len(key) == 16 or len(key) == 24 or len(key) == 32):
	 	window.destroy()
	 	btn2.destroy()
	 	win.deiconify()
	 	subThread()
	 else:
	 	handleProblem(window)
	 
def handleProblem(window):
	window.withdraw()
	popup2 = Toplevel()
	popup2.title("Error!")
	popup2.minsize(400, 20)
	l2 = Label(popup2, text = "Please enter a key that is either 16, 24, or 32 characters in length.")
	l2.pack()
	b2 = Button(popup2, text = "Okay", command = lambda: handleErrorMessage(window, popup2))#popup2.destroy)
	b2.pack()
	
def handleErrorMessage(window1, window2):
	window1.deiconify()
	window2.destroy()
	
def enterPressed():
	 global client
	 sent = e.get()
	 input_user.set('')
	 if connflag == True:
	 	  obj = AES.new(str(key), AES.MODE_CFB, 's7a6sTM58ZBLiNpR')
	 	  ciphertext = obj.encrypt(sent)
	 	  client.publish(pubtop, ciphertext)
	 else:
	 	  messages.insert(INSERT, '%s\n' % sent)
	 messages.insert(INSERT, '%s\n' % sent)

# button callback     
def Enter_pressed(event):
    global client
    sent = e.get()
    input_user.set('')
    if connflag == True:
        obj = AES.new(str(key), AES.MODE_CFB, 's7a6sTM58ZBLiNpR')
        ciphertext = obj.encrypt(sent)
        client.publish(pubtop, ciphertext)        
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
        obj2 = AES.new(str(key), AES.MODE_CFB, 's7a6sTM58ZBLiNpR')
        # recvmsg = str(message.payload.decode("utf-8"))
        recvmsgEncrypted = message.payload
        m = obj2.decrypt(recvmsgEncrypted)
        sender_message = str(message.topic) + ": " + m.decode('utf-8') + "\n\n"
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
	 global key 
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
btnSend = Button(win, text="Send", command=enterPressed)
btn2 = Button(win, text="Connect", command=popup)
# initialise and start main loop
init(win)

# iThread = threading.Thread(target = subThread)
# iThread.start()

mainloop()




