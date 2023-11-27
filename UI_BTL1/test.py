import tkinter as tk


class ỨngDụng(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)

        self.trang_1 = Trang1(self)
        self.trang_2 = Trang2(self)

        self.trang_1.pack()

    def chuyển_trang_1(self):
        self.trang_1.pack()
        self.trang_2.pack_forget()

    def chuyển_trang_2(self):
        self.trang_2.pack()
        self.trang_1.pack_forget()


class Trang1(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        nút = tk.Button(self, text="Chuyển đến trang 2",
                        command=master.chuyển_trang_2)
        nút.pack()


class Trang2(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        nút = tk.Button(self, text="Chuyển đến trang 1",
                        command=master.chuyển_trang_1)
        nút.pack()


ứng_dụng = ỨngDụng()
ứng_dụng.mainloop()
