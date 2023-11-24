from tkinter import *
from tkinter import messagebox

# Create window
window = Tk()


def handleClick():
    data = entry.get()
    lbl.config(text="xin chao" + data)
    # a = messagebox.showinfo(title="show info", message="day la info")
    # lbl.config(text=a)
    a = messagebox.showerror(title="show error", message="day la info")
    lbl.config(text=a)


def writeOutput():
    entry.insert(0, "output")


window.title("BTL1_MMT")
# change size and tọa độ of the window Widthxheight+x+y
window.geometry("400x400+100+200")
# Choose avater of window, just use ioc file
# window.iconbitmap("path of ioc file")
window.config(background="blue")
# disable change the size of the window
# window.resizable(False, False)

photo = PhotoImage(
    file="C:/Users/Acer/Desktop/DHBK/HK5/MMT/lab/lab2/lab2protocol/file-sharing/image.png")
# create label
lbl = Label(window, text="BTL1", font="arial 15 bold",
            background="black", fg="green", image=photo, compound='bottom')
# position in the middle of the window
lbl.pack()
# choose x and y position of label
# lbl.place(x=0, y=60)
# lbl.grid(row=0, column=0)
# create button
btn = Button(window, text="button", bg="black", fg="white",
             font="arial 15", command=handleClick)
btn.pack()
btn = Button(window, text="output", bg="black", fg="white",
             font="arial 15", command=writeOutput)
btn.pack()

# create entry
entry = Entry(window, font="arial 15", bg="white",
              fg="black", bd=4, width=25)
entry.pack()

window.mainloop()
