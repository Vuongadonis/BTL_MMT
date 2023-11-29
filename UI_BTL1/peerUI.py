from tkinter import *
from tkinter import messagebox
from threading import Thread
import socket
import pickle
import os
import threading
window = Tk()

flagConnect = False
mutex = threading.Lock()
condition_is_met = False

peerport = 25001
boss_port = 5000
# localhost = socket.gethostname()
# boss_host = "192.168.31.162"
localhost = "192.168.31.162"  # socket.gethostname()
boss_host = "192.168.31.217"  # socket.gethostname()
val = ""
file_list = []  # file_list[[path1, file_name1], [path2, filename2]]
# file_path = "C:/Users/Acer/Desktop/DHBK/HK5/MMT/lab/lab2/lab2protocol/file-sharing/"
file_path = ""
file_path_save = "C:/Users/Acer/Desktop/DHBK/HK5/MMT/lab/lab2/lab2protocol/file-sharing/"


def add_path(lname, fname):
    item = [lname, fname]
    file_list.append(item)
    print("add success", file_list)


def find_path(file_name):
    for item in file_list:
        if item[1] == file_name:
            file_path = item[0]
    print("path: ", file_path)
    return file_path


def new_connection(addr, conn):
    str_recv = addr.recv(16)
    str_recv = str(str_recv, "utf-8")
    print(str_recv)
    addr.send(bytes("receive success ", "utf-8"))
    # receive file name from peer want to down file
    file_name = str(addr.recv(16), "utf-8")
    # find the path of this file in the file_list
    file_path = find_path(file_name)
    # check if it còn tồn tại
    if os.path.exists(file_path + file_name) == True:
        print("Tệp tồn tại trong hệ thống.")
    else:
        print("Tệp không tồn tại trong hệ thống.")
    # Dòng này mở tệp hình ảnh "image.png" trong chế độ đọc nhị phân (binary).
    file = open(file_path + file_name, "rb")
    # Dòng này lấy kích thước của tệp hình ảnh "image.png" bằng cách sử dụng hàm os.path.getsize()
    file_size = os.path.getsize(file_path)
    # addr.send("received_image.png".encode())
    addr.send(str(file_size).encode())
    data = file.read(1024)
    i = 0
    while data:
        addr.send(data)
        # addr.recv(16)
        data = file.read(1024)
        # i = i + 1
        # print("send ", i)
    addr.send(b"<END>")
    addr.send(b"")
    print("send done")
    # file.close()


def peer_server_create(host, port):
    print("Ready to create peer \n")
    psocket = socket.socket()
    psocket.bind((host, port))

    psocket.listen(10)
    while True:
        # taccept = Thread(target=accept_connection, args=[serversocket])
        # taccept.start()
        addr, conn = psocket.accept()
        peer_conn = Thread(target=new_connection, args=[addr, conn])
        peer_conn.start()


def peer_down_file(info, file_name):
    # connect to peer have file
    peer_socket = socket.socket()
    peer_socket.connect((info[0], int(info[1])))
    message = "hello from " + str(peerport)
    peer_socket.send(bytes(message, "utf-8"))
    print(info)
    # Dòng này gửi file name qua cho peer kia
    peer_socket.recv(16)
    peer_socket.send(bytes(file_name, "utf-8"))
    print(file_name)
    # Dòng này nhận kích thước tệp từ máy khách, sau đó chuyển đổi từ dạng bytes sang dạng chuỗi (decode()).
    file_size = peer_socket.recv(1024).decode()
    print(file_size)
    # Dòng này mở tệp với tên tệp đã nhận từ máy khách trong chế độ ghi nhị phân (binary).
    # wb = chế độ ghi nhị phân (ghi theo bytes), nếu không có file sẽ tự tạo file
    file = open(file_path_save + file_name, "wb")
    # Dòng này khởi tạo một biến để lưu trữ dữ liệu của tệp.
    file_bytes = b""
    # Dòng này khởi tạo một biến để đánh dấu khi quá trình nhận tệp hoàn tất.
    done = False
    # Dòng này khởi tạo một đối tượng tqdm để hiển thị thanh tiến trình,
    # với đơn vị là Byte và tổng là kích thước tệp.
    # progress = tqdm.tqdm(unit="B", unit_scale=True, unit_divisor=1000,
    #                      total=int(file_size))

    while not done:
        # print("OK")
        # Dòng này nhận dữ liệu (chunks) từ máy khách với kích thước tối đa là 1024 byte.
        data = peer_socket.recv(1024)
        # print("data ", data)
        file_bytes += data
        # Dòng này kiểm tra nếu dữ liệu nhận được là chuỗi bytes "", tương ứng với kết thúc tệp.
        if file_bytes[-5:] == b"<END>":
            break
        # Dòng này cập nhật thanh tiến trình của tqdm với một khối dữ liệu có kích thước 1024 byte đã nhận.
        # progress.update(1024)

    # Dòng này ghi dữ liệu đã nhận vào tệp.
    # print("write")
    file.write(file_bytes)
    file.close()
    print("receive oke")


def peer_get_command():
    command = input()
    return command


def peer_handle_command(client_socket, mess):
    command = mess.split(" ")
    match(command[0]):
        case "add":
            client_socket.send(bytes(mess, "utf-8"))
            # wait boss return succeed then send continue
            client_socket.recv(16)
            # send information
            data = [localhost, str(peerport)]
            data = pickle.dumps(data)
            client_socket.send(data)
            print("send port\n")
            # wait boss return succeed then send continue
            client_socket.recv(16)
        case "get":
            client_socket.send(bytes(mess, "utf-8"))
            client_socket.recv(16)
            local_list = pickle.loads(client_socket.recv(8192))
            print("local list: ", local_list)
            for lport in local_list:
                peer_socket = socket.socket()
                peer_socket.connect((lport[0], lport[1]))
                message = "hello from " + str(peerport)
                peer_socket.send(bytes(message, "utf-8"))
        case "fetch":
            fname = command[1]
            client_socket.send(bytes(command[0], "utf-8"))
            client_socket.recv(16)
            # wait boss return succeed then send continue
            # send file name want to download
            client_socket.send(bytes(command[1], "utf-8"))
            # wait boss return succeed then send continue
            client_socket.recv(16)
            # receive hostname and port of peer to download file
            info = pickle.loads(client_socket.recv(4096))
            print("can receive", info)
            peer_down_file(info, fname)
        case "public":
            client_socket.send(bytes(command[0], "utf-8"))
            # wait boss return succeed then send continue
            client_socket.recv(16)

            data = [localhost, str(peerport)]
            data = pickle.dumps(data)
            client_socket.send(data)
            client_socket.recv(16)

            lname = command[1]
            fname = command[2]
            add_path(lname, fname)
            client_socket.send(bytes(command[2], "utf-8"))
            # wait boss return succeed then send continue
            client_socket.recv(16)
            print("public: ", lname, fname)


def thread_peer_client(host, port):
    client_socket = socket.socket()
    client_socket.connect((host, port))
    global condition_is_met
    while True:
        # Thực hiện các xử lý và kiểm tra điều kiện
        while not condition_is_met:
            continue
        condition_is_met = False
        # Đợi đến khi điều kiện được đáp ứng
        # Sau khi điều kiện được đáp ứng, tiếp tục thực hiện các công việc khác
        peer_handle_command(client_socket, val)


def server_program():
    # thread chay gui thong tin den cac peer
    nconn1 = Thread(target=peer_server_create, args=[localhost, peerport])
    nconn1.start()
    # thread ket noi den bigboss
    nconn2 = Thread(target=thread_peer_client, args=[boss_host, boss_port])
    nconn2.start()


def hideOptions():
    public.config(bg="black")
    fetch.config(bg="black")


def handleConnect(btn, btnAdd):
    global flagConnect
    if flagConnect == True:
        return
    flagConnect = True
    btn.config(bg="green")
    btnAdd.config(bg="black")

    server_program()


def getCommand(command):
    global condition_is_met
    global val
    mutex.acquire()
    try:
        condition_is_met = True
        val = command
    finally:
        mutex.release()


def handleAddlist(btn):
    getCommand("add list")
    messagebox.showinfo("", "add success")


def handlePublic(path_val, file_val):
    command = "public " + path_val.get() + " " + file_val.get()
    getCommand(command)
    path_val.delete(0, 'end')
    file_val.delete(0, 'end')
    messagebox.showinfo("", "send success")


def handleFetch(file_val):
    command = "fetch " + file_val.get()
    getCommand(command)
    file_val.delete(0, 'end')
    messagebox.showinfo("", "send success")


def handleLocal(local_val):
    global file_path_save
    val = local_val.get()
    file_path_save = val
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


def local_page():
    local_frame = Frame(main_frame)

    local_label = Label(local_frame, text="Local storage",
                        font="arial 15 bold", fg="green")
    local_label.pack()
    local_val = Entry(local_frame, font="arial 15", bg="white",
                      fg="black", bd=4, width=25)
    local_val.pack(pady=5)

    local_frame.pack(pady=20)
    sendBtn = Button(local_frame, text="send", bg="black", fg="white",
                     font="arial 15", command=lambda: handleLocal(local_val))
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

screenWidth = window.winfo_screenwidth()
screenHeight = window.winfo_screenheight()

newX = (screenWidth - windowWidth) // 2  # Tính toán vị trí mới theo trục X
newY = (screenHeight - windowHeight) // 2  # Tính toán vị trí mới theo trục Y

windowX = newX
windowY = newY
entryWidth = 20
windowInfo = str(windowWidth) + "x" + str(windowHeight) + \
    "+" + str(windowX) + "+" + str(windowY)

window.title("peer " + str(number))
window.geometry(windowInfo)
window.resizable(False, False)

lbl1 = Label(window, text="peer " + str(number),
             font="arial 15 bold", fg="green")
# position in the middle of the window
lbl1.place(x=0, y=0)

btn_addlist = Button(window, text="Add list", bg="gray", fg="white",
                     font="arial 15", command=lambda: handleAddlist(btn_addlist))
btn_addlist.place(x=windowWidth-100, y=0)

btn_connect = Button(window, text="connect", bg="black", fg="white",
                     font="arial 15", command=lambda: handleConnect(btn_connect, btn_addlist))
btn_connect.place(x=windowWidth-200, y=0)

options_frame = Frame(window, width=350, height=350, bg='#c3c3c3')
options_frame.place(x=25, y=50)

main_frame = Frame(window, width=300, height=350, bg='#c3c3c3',
                   highlightbackground="black", highlightthickness=2)
main_frame.place(x=50, y=90)

file_local = Button(window, text="Local", bg="black", fg="white",
                    font="arial 15", command=lambda: handleOptions(file_local, local_page))
file_local.place(x=50, y=50)

public = Button(window, text="Public", bg="black", fg="white",
                font="arial 15", command=lambda: handleOptions(public, public_page))
public.place(x=165, y=50)

fetch = Button(window, text="Fetch", bg="black", fg="white",
               font="arial 15", command=lambda: handleOptions(fetch, fetch_page))
fetch.place(x=400-25-25-fetch.winfo_reqwidth(), y=50)

window.mainloop()
