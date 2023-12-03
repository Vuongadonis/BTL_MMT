from tkinter import *
import socket
from threading import Thread
import pickle
import subprocess

window = Tk()

sockets_list = [
]
# socket_list[0][0] = ip(hostname) + port of first peer
# socket_list[0][1] = list_file of this hostname of first peer
# socket_list[1][0] = ip(hostname) + port of second peer
# socket_list[1][1] = list_file of this hostname of second peer

# serversocket = 0
# server_host = "192.168.72.183"
server_host = socket.gethostname()
server_port = 5000
flagConnect = False


def get_user_input(user_input, frame):
    # while True:
    # user_input = input()
    command = user_input.split(" ")
    if command[0] == "discover":
        print("List of hostname ", command[1], "is: ")
        # print list file of command[1] (hostname)
        y_val = 60
        for index1, i in enumerate(sockets_list):
            if isinstance(i, list):
                # item[ [ [host, port], [file] ] ]
                if i[0][0] != command[1]:
                    continue
                for index2, item in enumerate(i):
                    if isinstance(item, list):
                        print(item[0])
                        if item[0] == command[1]:
                            print("Yes")
                        else:
                            #     # print from item[1] -> end -> [file]
                            text = Text(frame)

                            for index, k in enumerate(item):
                                text.insert(END, f'file {index} : {str(k)} \n')
                                text.pack()
        print("Discover done")
    if command[0] == "ping":
        ping_process = subprocess.Popen(
            ["ping", "-n", "4", command[1]], stdout=subprocess.PIPE)
        ping_output = ping_process.communicate()[0]
        print(ping_output.decode('utf-8'))
        print("Ping done")

        canvas = Canvas(frame, bg="white", scrollregion=(0, 0, 200, 5000))
        canvas.place(x=0, y=60)
        canvas.bind('<MouseWheel>',
                    lambda event: canvas.yview_scroll(-int(event.delta/60), "units"))

        scrollbar = Scrollbar(frame, orient='vertical', command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.place(relx=1, rely=0.2, relheight=0.8, anchor="ne")
        ping_out_lbl = Label(frame, text=ping_output,
                             font="arial 10 bold", fg="green")
        canvas.create_window(10, 0, anchor='nw', window=ping_out_lbl)
    # if command[0].lower() == "exit":
        # break


def new_connection(addr, conn):
    status = ""
    while True:
        str_recv = addr.recv(16)
        # print("receive: \n", str)
        str_recv = str(str_recv, "utf-8")
        addr.send(bytes("receive success ", "utf-8"))

        match str_recv:
            case "add list":
                print("add list: ", end="")
                item = pickle.loads(addr.recv(4096))
                item_add = [item, []]
                sockets_list.append(item_add)
                addr.send(bytes("receive success ", "utf-8"))
                status = ""
                print("list: ", sockets_list)
            case "get list":

                print("get list: \n")
                status = ""
            case "fetch":
                print("fetch")
                # receive file name peer want to download
                file_name = str(addr.recv(16), "utf-8")
                addr.send(bytes("receive success ", "utf-8"))
                # send hostname and port have this file
                flag = True
                # sockets_list = [
                #     [[], ["1"]],
                #     [[], ["2"]]
                # ]
                print(file_name)
                for index1, client in enumerate(sockets_list):
                    if isinstance(client, list):
                        for index2, item in enumerate(client):
                            for index3, k in enumerate(item):
                                print("k: ", k)
                                if k == file_name:
                                    print(
                                        f"Index: {index1, index2, index3}, Value: {k, client[0]}")
                                    print(client[0])
                                    data = pickle.dumps(client[0])
                                    addr.send(data)
                                    flag = False

                if flag:
                    print("send error")
                    # addr.send(bytes("do not have this file", "utf-8"))
            case "public":
                ip_port = pickle.loads(addr.recv(4096))
                addr.send(bytes("receive success ", "utf-8"))

                file_name = str(addr.recv(16), "utf-8")
                addr.send(bytes("receive success ", "utf-8"))

                for client in sockets_list:
                    if client[0] == ip_port:
                        print("add success", client[1])
                        client[1].append(file_name)
                        break
                print(sockets_list)


def server_program(host, port):
    serversocket = socket.socket()
    serversocket.bind((host, port))
    print("server is ready\n")
    serversocket.listen(10)
    while True:
        # taccept = Thread(target=accept_connection, args=[serversocket])
        # taccept.start()
        addr, conn = serversocket.accept()
        # print("addr: ", addr, "\n")
        nconn = Thread(target=new_connection, args=[addr, conn])
        nconn.start()
        # nconn2 = Thread(target=get_user_input)
        # nconn2.start()


def handleDiscover(data, frame):
    get_user_input("discover " + data.get(), frame)


def handlePing(data, frame):
    get_user_input("ping " + data.get(), frame)


def handleOn(btn):
    global flagConnect
    if flagConnect == True:
        return
    flagConnect = True
    btn.config(text="On", bg="green")
    serverThread = Thread(target=server_program, args=[
                          server_host, server_port])
    serverThread.start()


def Discover_page():
    Discover_Frame = Frame(main_frame, width=346, height=346)
    Discover_Frame.place(x=0, y=0)

    discover_label = Label(Discover_Frame, text="IP Discover",
                           font="arial 15 bold", fg="green")
    discover_label.place(x=100, y=0)
    discover_val = Entry(Discover_Frame, font="arial 15", bg="white",
                         fg="black", bd=4, width=20)
    discover_val.place(x=30, y=30)

    sendBtn = Button(Discover_Frame, text="send", bg="black", fg="white",
                     font="arial 15", command=lambda: handleDiscover(discover_val, Discover_Frame))
    sendBtn.place(x=280, y=25)


def Ping_page():
    ping_frame = Frame(main_frame, width=346, height=346)
    ping_frame.place(x=0, y=0)
    ping_label = Label(ping_frame, text="IP Ping",
                       font="arial 15 bold", fg="green")
    ping_label.place(x=100, y=0)
    ping_val = Entry(ping_frame, font="arial 15", bg="white",
                     fg="black", bd=4, width=20)
    ping_val.place(x=30, y=30)

    sendBtn = Button(ping_frame, text="send", bg="black", fg="white",
                     font="arial 15", command=lambda: handlePing(ping_val, ping_frame))
    sendBtn.place(x=280, y=25)


def deletePage():
    for frame in main_frame.winfo_children():
        frame.destroy()


def hideOptions():
    Discover.config(bg="black")
    Ping.config(bg="black")


def handleOptions(lb, page):
    hideOptions()
    lb.config(bg="green")
    deletePage()
    page()


windowWidth = 400
windowHeight = 400

screenWidth = window.winfo_screenwidth()
screenHeight = window.winfo_screenheight()

newX = (screenWidth - windowWidth) // 2  # Tính toán vị trí mới theo trục X
newY = (screenHeight - windowHeight) // 2  # Tính toán vị trí mới theo trục Y

windowX = int(newX - windowWidth)
windowY = newY

windowInfo = str(windowWidth) + "x" + str(windowHeight) + \
    "+" + str(windowX) + "+" + str(windowY)

window.title("bigboss")
window.geometry(windowInfo)

lbl = Label(window, text="bigboss", font="arial 15 bold", fg="green")
# position in the middle of the window
lbl.place(x=0, y=0)

Onbtn = Button(window, text="OFF", bg="grey", fg="white",
               font="arial 15", command=lambda: handleOn(Onbtn))
Onbtn.place(x=300, y=0)

main_frame = Frame(window, width=350, height=350, bg='#c3c3c3',
                   highlightbackground="black", highlightthickness=2)
main_frame.place(x=25, y=90)

Discover = Button(window, text="Discover", bg="black", fg="white", width=10,
                  font="arial 15", command=lambda: handleOptions(Discover, Discover_page))
Discover.place(x=50, y=50)

Ping = Button(window, text="Ping", bg="black", fg="white", width=10,
              font="arial 15", command=lambda: handleOptions(Ping, Ping_page))
Ping.place(x=200, y=50)

window.mainloop()
