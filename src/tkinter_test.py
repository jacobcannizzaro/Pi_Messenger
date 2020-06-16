from tkinter import *
from tkinter import messagebox
 
# initialise main window
def init(win):
    win.title("SEPI Messenger")
    win.minsize(400,500)
    e.place(bordermode=INSIDE, height=25, width=425, x=0, y=475)
    btn.place(bordermode=INSIDE, height=25, width=50, x=350, y=475)

# button callback     
def send():
    sent = e.get()
    msg = Message(win, text=sent)
    msg.pack()
    
# create top-level window
win = Tk()
e = Entry(win)
 
# Gets the requested values of the height and widht.
windowWidth = win.winfo_reqwidth()
windowHeight = win.winfo_reqheight()
 
# Gets both half the screen width/height and window width/height
positionRight = int(win.winfo_screenwidth()/2 - windowWidth/2)
positionDown = int(win.winfo_screenheight()/2 - windowHeight/2)
 
# Positions the window in the center of the page.
win.geometry("+{}+{}".format(positionRight, positionDown))
 
# create a button
btn = Button(win, text="Send", command=send)
 
# initialise and start main loop
init(win)
mainloop()