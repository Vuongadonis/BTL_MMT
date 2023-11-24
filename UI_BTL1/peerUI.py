from tkinter import *

window = Tk()

flagConnect = False


def handleConnect():
    global flagConnect
    if flagConnect == True:
        return
    flagConnect = True
    btn1.config(bg="green")
    data = entry.get()
    lbl1.config(text="xin chao" + data)


def handleSend():
    data = entry.get()
    lbl1.config(text="xin chao" + data)


number = 1
windowWidth = 400
windowHeight = 400
windowX = 100
windowY = 200
entryWidth = 20
windowInfo = str(windowWidth) + "x" + str(windowHeight) + \
    "+" + str(windowX) + "+" + str(windowY)

window.title("peer " + str(number))
window.geometry(windowInfo)

lbl1 = Label(window, text="peer " + str(number),
             font="arial 15 bold", fg="green")
# position in the middle of the window
lbl1.place(x=0, y=0)

btn1 = Button(window, text="connect", bg="black", fg="white",
              font="arial 15", command=handleConnect)
btn1.place(x=10, y=50)

lbl2 = Label(window, text="Nhap input:", font="arial 10", fg="black")
# position in the middle of the window
lbl2.place(x=10, y=100)

entry = Entry(window, font="arial 15", bg="white",
              fg="black", bd=4, width=entryWidth)
entry.place(x=10, y=120)

btn2 = Button(window, text="send", bg="black", fg="white",
              font="arial 15", command=handleSend)
btn2.place(x=300, y=120)

window.mainloop()
