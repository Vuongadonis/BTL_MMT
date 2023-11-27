from tkinter import *
from tkinter import messagebox
import subprocess

root = Tk()
root.title("Login")
root.geometry("925x500+300+200")
root.configure(bg='#fff')
root.resizable(False,False)

def call_UI():
    root.destroy();
    subprocess.call(['python','UI_tkinter.py'])


# img = PhotoImage(file='./FileSharing.png')
# Label(root,image=img,bg='white').place(x=50,y=50)

frame = Frame(root,width=350,height=350,bg='white')
frame.place(x=480,y=70)



heading = Label(frame,text='Đăng Nhập',fg='#57a1f8',bg='white',font=('Microsolf Yahei UI Light',23,'bold'))
heading.place(x=100,y=5)
#===================== Tên đăng nhập ========================
user = Entry(frame,width=25,fg='black',border=0,bg='white',font=('Microsolf Yahei UI Light',11))
user.place(x=30,y=80)
user.insert(0,'Tên đăng nhập')

Frame(frame,width=295,height=2,bg='black',).place(x=25,y=107)

#==================== Mật  khẩu ================================

password = Entry(frame,width=25,fg='black',border=0,bg='white',font=('Microsolf Yahei UI Light',11),show='*')
password.place(x=30,y=150)
password.insert(0,'Mật khẩu')

Frame(frame,width=295,height=2,bg='black',).place(x=25,y=177)

#--------------------- Nút đăng nhập ----------------------------


Button(frame,width=39,pady=7,text="Đăng nhập",bg='#57a1f8',fg='white',border=0,command=call_UI).place(x=35,y=204)

root.mainloop()
