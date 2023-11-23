from tkinter import *

# Create window
window = Tk()
window.title("BTL1_MMT")
# change size and tọa độ of the window Widthxheight+x+y
window.geometry("400x400+100+200")
# Choose avater of window, just use ioc file
# window.iconbitmap("path of ioc file")
window.config(background="blue")
# disable change the size of the window
window.resizable(False, False)
window.mainloop()
