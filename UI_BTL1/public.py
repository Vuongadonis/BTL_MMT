from tkinter import *
from tkinter import messagebox

window = Tk()

flagConnect = False


def hideOptions():
    public.config(bg="black")
    fetch.config(bg="black")


def handleConnect(btn):
    global flagConnect
    if flagConnect == True:
        return
    flagConnect = True
    btn.config(bg="green")


def handlePublic(path_val, file_val):
    path_val.delete(0, 'end')
    file_val.delete(0, 'end')
    messagebox.showinfo("", "send success")


def handleFetch(file_val):
    file_val.delete(0, 'end')
    messagebox.showinfo("", "send success")


def public_page():
    public_frame = Frame(main_frame)
    public_frame.pack(pady=20)

    path_frame = Frame(public_frame)
    path_frame.pack(pady=5)

    path_label = Label(path_frame, text="path name",
                       font="arial 15 bold", fg="green")
    path_label.pack()
    path_val = Entry(path_frame, font="arial 15", bg="white",
                     fg="black", bd=4, width=25)
    path_val.pack(pady=5)

    file_label = Label(path_frame, text="file name",
                       font="arial 15 bold", fg="green")
    file_label.pack()
    file_val = Entry(path_frame, font="arial 15", bg="white",
                     fg="black", bd=4, width=25)
    file_val.pack(pady=5)

    sendBtn = Button(public_frame, text="send", bg="black", fg="white",
                     font="arial 15", command=lambda: handlePublic(path_val, file_val))
    sendBtn.pack()


def fetch_page():
    fetch_frame = Frame(main_frame)

    file_label = Label(fetch_frame, text="file name",
                       font="arial 15 bold", fg="green")
    file_label.pack()
    file_val = Entry(fetch_frame, font="arial 15", bg="white",
                     fg="black", bd=4, width=25)
    file_val.pack(pady=5)

    fetch_frame.pack(pady=20)
    sendBtn = Button(fetch_frame, text="send", bg="black", fg="white",
                     font="arial 15", command=lambda: handleFetch(file_val))
    sendBtn.pack()


def deletePage():
    for frame in main_frame.winfo_children():
        frame.destroy()


def handleOptions(lb, page):
    hideOptions()
    lb.config(bg="green")
    deletePage()
    page()


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

btn_connect = Button(window, text="connect", bg="black", fg="white",
                     font="arial 15", command=lambda: handleConnect(btn_connect))
btn_connect.place(x=windowWidth-100, y=0)

options_frame = Frame(window, width=350, height=350, bg='#c3c3c3')
options_frame.place(x=10, y=50)

main_frame = Frame(window, width=350, height=350, bg='#c3c3c3',
                   highlightbackground="black", highlightthickness=2)
main_frame.place(x=10, y=90)

public = Button(window, text="Public", bg="black", fg="white",
                font="arial 15", command=lambda: handleOptions(public, public_page))
public.place(x=50, y=50)

fetch = Button(window, text="Fetch", bg="black", fg="white",
               font="arial 15", command=lambda: handleOptions(fetch, fetch_page))
fetch.place(x=200, y=50)

window.mainloop()
