from tkinter import *

window = Tk()


def handleClick():
    data = entry.get()
    lbl.config(text="xin chao" + data)


window.title("bigboss")
window.geometry("400x400+100+200")

lbl = Label(window, text="bigboss", font="arial 15 bold", fg="green")
# position in the middle of the window
lbl.grid(row=0, column=0)

entry = Entry(window, font="arial 15", bg="white",
              fg="black", bd=4, width=25)
entry.grid(row=2, column=0)

btn = Button(window, text="send", bg="black", fg="white",
             font="arial 15", command=handleClick)
btn.grid(row=2, column=1)

window.mainloop()
