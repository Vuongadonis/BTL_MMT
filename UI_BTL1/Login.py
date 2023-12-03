from tkinter import *
from tkinter import messagebox
import subprocess

list_account = ["giaqui", "hoangvuong", "trungkien", "anhkhoa"]

root = Tk()
root.title("Login")
root.geometry("925x500+300+200")
root.configure(bg='#fff')
root.resizable(False, False)


def sign_in():
    if (user.get() in list_account and password.get() == "12345"):
        root.destroy()
        subprocess.call(['python', 'peerUI.py'])
    elif (user.get() in list_account_bigboss and password.get() == "12345"):
        root.destroy()
        subprocess.call(['python', 'bigbossUI.py'])
    else:
        messagebox.showerror("Lỗi", "Tài khoản hoặc mặt khẩu không đúng!"
                             "\n\nVui lòng kiểm tra lại.")


img = PhotoImage(file='img.png')
Label(root, image=img, bg='white').place(x=50, y=50)

frame = Frame(root, width=350, height=350, bg='white')
frame.place(x=480, y=70)


heading = Label(frame, text='Đăng Nhập', fg='#57a1f8', bg='white',
                font=('Microsolf Yahei UI Light', 23, 'bold'))
heading.place(x=100, y=5)
# ===================== Tên đăng nhập ========================


def on_enter(e):
    user.delete(0, 'end')


def on_leave(e):
    name = user.get()
    if (name == ''):
        user.insert(0, 'Tên đăng nhập')


user = Entry(frame, width=25, fg='black', border=0,
             bg='white', font=('Microsolf Yahei UI Light', 11))
user.place(x=30, y=80)
user.insert(0, 'Tên đăng nhập')
user.bind('<FocusIn>', on_enter)
user.bind('<FocusOut>', on_leave)

Frame(frame, width=295, height=2, bg='black',).place(x=25, y=107)

# ==================== Mật  khẩu ================================


def on_enter(e):
    password.delete(0, 'end')


def on_leave(e):
    name = password.get()
    if (name == ''):
        password.insert(0, 'Mật khẩu')


password = Entry(frame, width=25, fg='black', border=0,
                 bg='white', font=('Microsolf Yahei UI Light', 11), show='*')
password.place(x=30, y=150)
password.insert(0, 'Mật khẩu')
password.bind('<FocusIn>', on_enter)
password.bind('<FocusOut>', on_leave)

Frame(frame, width=295, height=2, bg='black',).place(x=25, y=177)

# --------------------- Nút đăng nhập ----------------------------


Button(frame, width=39, pady=7, text="Đăng nhập", bg='#57a1f8',
       fg='white', border=0, command=sign_in).place(x=35, y=204)

root.mainloop()
