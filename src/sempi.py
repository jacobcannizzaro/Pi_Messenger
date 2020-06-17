import paho.mqtt.client as paho
import os
import socket
import ssl
from time import sleep
import threading
import pickle
from tkinter import *
from tkinter import messagebox
from Crypto.Cipher import AES
#Above import is from PyCrypto library
#AES (Advanced Encryption Standard) is a symmetric block cipher standardized by NIST
"""
Below is an example call using this library that needs the most explanation:
obj = AES.new(str(key), AES.MODE_CFB, 's7a6sTM58ZBLiNpR')

*   This creates a new cipher object in obj.
*   The first argument is they key (gotten from the user) that can be 16, 24, 
    or 32 bytes (chars) long. This is the key to be used for the symmetric cipher.
    The second argument s
*   The second argument specifies the mode
*   Third argument specifies the initialization vector for encryption/decryption
    This must be 16 bytes long and the same for the decryption cipher object as
    the encryption cipher object. Therefore I randomly generated a 16 char string
    to serve as the iv and hardcoded it instead of computing it randomly as is
    often done.

read more: https://www.dlitz.net/software/pycrypto/api/current/
"""


#initialize global variables
connflag = False
clientRunning = False
pubtop = ""
subtop = ""
client = paho.Client()
e = ""
key = ""
input_user = ""

# initialise main window
def init(win):
    win.title("SEMPi")
    win.geometry("415x450")
    win.minsize(415,450)
    
#request session key    
def popup():
	 input_user2 = StringVar()
	 popup = Toplevel()
	 popup.geometry("+{}+{}".format(positionRight, positionDown))
	 popup.title("Enter session key")
	 popup.minsize(400,20)
	 win.withdraw()
	 l=Label(popup, text="Enter Session Key: ")
	 l.grid(row=2, column = 0)
	 e2 = Entry(popup, text=input_user2)
	 e2.grid(row = 2, column = 1)
	 b1 = Button(popup, text = "Submit", command = lambda: handleSessionKey(popup, e2))
	 b1.grid(row=2, column = 2)
	
#handle the user inputted session key 
def handleSessionKey(window, entryField):
	 global key
	 global e
	 global input_user
	 key = str(entryField.get())
	 if(len(key) == 16 or len(key) == 24 or len(key) == 32): #make sure key is of proper length
	 	window.destroy() #destroy key input window
	 	btn2.destroy() #destroy connect button
	 	win.deiconify() #show main window
	 	input_user = StringVar()
	 	e = Entry(win,text=input_user)
	 	e.bind("<Return>", Enter_pressed)
	 	e.place(bordermode=INSIDE, height=25, width=325, x=0, y=425) #place text entry field
	 	btnSend = Button(win, text="Send", command=enterPressed)
	 	btnSend.place(bordermode=INSIDE, height = 25, width = 75, x = 325, y = 425) #place send button
	 	messages.pack() #pack text field
	 	subThread()
	 else:
	 	handleProblem(window) #display error message

#if the user does not enter a proper key
def handleProblem(window):
	window.withdraw() #hide session key window
	popup2 = Toplevel()
	popup2.geometry("+{}+{}".format(positionRight, positionDown))
	popup2.title("Error!")
	popup2.minsize(400, 20)
	l2 = Label(popup2, text = "Please enter a key that is either 16, 24, or 32 characters in length.")
	l2.pack()
	b2 = Button(popup2, text = "Okay", command = lambda: handleErrorMessage(window, popup2)) #close window when clicked
	b2.pack()
	
#close error message, show session key window
def handleErrorMessage(window1, window2): 
	window1.deiconify()
	window2.destroy()

#button handler for send button
def enterPressed():
	 global client
	 global e
	 sent = e.get() #grab text from text input field
	 strippedString = sent.strip()
	 if not strippedString:
	 	  input_user.set('')
	 	  return
	 input_user.set('')
	 if connflag == True:
	 	  obj = AES.new(str(key), AES.MODE_CFB, 's7a6sTM58ZBLiNpR') #see under imports for explanation
	 	  ciphertext = obj.encrypt(sent) #encrypt msg -> ciphertext
	 	  client.publish(pubtop, ciphertext) #publish encrypted msg
	 	  messages.configure(state="normal")
	 	  messages.insert(INSERT, 'Me: %s\n\n' % sent)
	 	  messages.configure(state="disabled")  
	 	  messages.see("end")

# button callback     
def Enter_pressed(event):
    global client
    global e
    sent = e.get()
    strippedString = sent.strip()
    if not strippedString:
    	  input_user.set('')
    	  return
    input_user.set('')
    if connflag == True:
        obj = AES.new(str(key), AES.MODE_CFB, 's7a6sTM58ZBLiNpR') #see under imports for explanation
        ciphertext = obj.encrypt(sent)
        client.publish(pubtop, ciphertext) 
        messages.configure(state="normal")
        messages.insert(INSERT, 'Me: %s\n\n' % sent)   
        messages.configure(state="disabled")   
        messages.see("end") 

#handler method waiting for connection to broker
def on_connect(client, userdata, flags, rc):
    global connflag
    global msg
    messages.configure(state="normal")
    messages.insert(INSERT, "Connected to AWS\n\n")
    messages.configure(state="disabled")
    connflag = True #update global connection flag

#handler method executes when client recieves a message from broker
def on_message(client, userdata, message):
    global puptop
    global msg
    if str(message.topic) != pubtop:
        obj2 = AES.new(str(key), AES.MODE_CFB, 's7a6sTM58ZBLiNpR') #see under imports for explanation
        recvmsgEncrypted = message.payload  #recieve message from broker
        m = obj2.decrypt(recvmsgEncrypted)  #decrypt ciphertext -> m
        gen_topic, sender = message.topic.split('/')       #grab the 'jakepi' from 'chat/jakepi' topic
        sender_message = sender + ": " + m.decode('utf-8') #decrypted text is in bytes format, have to decode
        messages.configure(state="normal")
        messages.insert(INSERT, '%s\n\n' % sender_message)
        messages.configure(state="disabled")
        messages.see("end")
        

#following 3 methods just used for debugging purposes --#
def on_subscribe(client, userdata, mid, granted_qos):
    print("Subscribed:", str(mid), str(grant))

def on_unsubscribe(client, userdata, mid):
    print("Unsubscribed:", str(mid))

def on_disconnect(client, userdata, rc):
    if rc != 0:
        print("unexpected Disconnection")
#-------------------------------------------------------#

def connect_client():
    global pubtop
    global subtop
    global client
    #point client object's functions to the functions implemented above
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_subscribe = on_subscribe
    client.on_unsubscribe = on_unsubscribe
    client.on_disconnect = on_disconnect
    #load pickled credential dictionary to grab AWS required connection credentials
    credentials = pickle.load(open("connection.pkl", "rb"))
    awshost = credentials['endpoint']
    awsport = 8883                          # Port no.
    clientId = credentials['thingname']     # Thing_Name
    thingName = credentials['thingname']    # Thing_Name
    caPath = credentials['pathname'] + "connect_device_package/root-CA.crt"                           # Root_CA_Certificate_Name
    certPath = credentials['pathname'] + "connect_device_package/" + thingName + ".cert.pem"          # <Thing_Name>.cert.pem
    keyPath = credentials['pathname'] + "connect_device_package/" + thingName + ".private.key"        # path to keys
    #set aws credentials for client
    client.tls_set(caPath, certfile=certPath, keyfile=keyPath, cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)  
    client.connect(awshost, awsport, keepalive=60)               # connect to aws server
    sleep(1) #ensure correct order... 

    pubtop = "chat/" + thingName #topic client publishes messages to
    subtop = "chat/#"            #topic client subscribes to (# is wildcard that allows subscribing to all chat/subtopics)
    client.subscribe(subtop)
    sleep(1)
    clientRunning = True
    client.loop_start()          #this thread is now just looping, waiting for subscribed topics being relayed from broker


#function is run after session key is entered to use this thread to connect and listen to the AWS broker
def subThread():
	 iThread = threading.Thread(target = connect_client) #target method is connect_client() - this is where iThread begins executing
	 iThread.start()

#window closing event handler
def on_closing():
    global clientRunning
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        if clientRunning == True: #if client is running stop the loop
            clientRunning = False
            client.loop_stop()
        win.destroy()             #quit program



win = Tk() #establish window
btn2 = Button(win, text="Connect", command=popup) #define connect button
btn2.place(bordermode=INSIDE, height=25, width=75, x=0, y=0) #place connect button on the window
btn2.pack() #pack the connect button
scrollbar=Scrollbar(win) #establish the scrollbar for main window
messages = Text(win, wrap = WORD, yscrollcommand = scrollbar.set) #establish textfield for sent and incoming messages
messages.see("end")
messages.insert(INSERT, "Click the Connect button to start chatting\n\n") #instruct the user
messages.configure(state="disabled") #disable editing the messages area
scrollbar.pack(side=RIGHT, fill = Y) #format scrollbar
scrollbar.config(command=messages.yview)
messages.pack() #pack the text field


 
# Gets the requested values of the height and width
windowWidth = win.winfo_reqwidth()
windowHeight = win.winfo_reqheight()
 
# Gets both half the screen width/height and window width/height
positionRight = int(win.winfo_screenwidth()/2 - windowWidth/2)
positionDown = int(win.winfo_screenheight()/2 - windowHeight/2)
 
# Positions the window in the center of the page.
win.geometry("+{}+{}".format(positionRight, positionDown))
win.protocol("WM_DELETE_WINDOW", on_closing) #execute method on closing

# initialise and start main loop
init(win)
mainloop()




