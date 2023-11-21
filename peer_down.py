import socket
from threading import Thread
import pickle
# import tqdm
# Đây là một thư viện trong Python cho phép thao tác với các chức năng hệ thống,
# trong trường hợp này, nó được sử dụng để lấy kích thước của tệp hình ảnh
import os

peerport = 25001
boss_port = 5000
# localhost = socket.gethostname()
# boss_host = "192.168.31.162"
localhost = socket.gethostname()
boss_host = socket.gethostname()
file_path = "C:/Users/Acer/Desktop/DHBK/HK5/MMT/lab/lab2/lab2protocol/file-sharing/"
file_path_save = "C:/Users/Acer/Desktop/DHBK/HK5/MMT/lab/lab2/lab2protocol/file-sharing/"


def new_connection(addr, conn):
    str_recv = addr.recv(16)
    str_recv = str(str_recv, "utf-8")
    print(str_recv)
    if os.path.exists(file_path + "image.png") == True:
        print("Tệp tồn tại trong hệ thống.")
    else:
        print("Tệp không tồn tại trong hệ thống.")
    # Dòng này mở tệp hình ảnh "image.png" trong chế độ đọc nhị phân (binary).
    file = open(file_path + "image.png", "rb")
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
    peer_socket.connect((info[0][0], info[0][1]))
    message = "hello from " + str(peerport)
    peer_socket.send(bytes(message, "utf-8"))
    print(info)
    # Dòng này nhận tên tệp từ máy khách, sau đó chuyển đổi từ dạng bytes sang dạng chuỗi (decode()).
    print(file_name)
    # Dòng này nhận kích thước tệp từ máy khách, sau đó chuyển đổi từ dạng bytes sang dạng chuỗi (decode()).
    file_size = peer_socket.recv(1024).decode()
    print(file_size)
    # Dòng này mở tệp với tên tệp đã nhận từ máy khách trong chế độ ghi nhị phân (binary).
    # wb = chế độ ghi nhị phân (ghi theo bytes), nếu không có file sẽ tự tạo file
    file = open(file_path_save + file_name + ".png", "wb")
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
            data = [localhost, peerport]
            data = pickle.dumps(data)
            client_socket.send(data)
            print("send port\n")
            # wait boss return succeed then send continue
            client_socket.recv(16)
        case "get":
            client_socket.send(bytes(mess, "utf-8"))
            client_socket.recv(16)
            local_list = pickle.loads(client_socket.recv(4096))
            print("local list: ", local_list)
            for lport in local_list:
                peer_socket = socket.socket()
                peer_socket.connect((lport[0], lport[1]))
                message = "hello from " + str(peerport)
                peer_socket.send(bytes(message, "utf-8"))
        case "fetch":
            fname = command[1]
            client_socket.send(bytes(command[0], "utf-8"))
            # wait boss return succeed then send continue
            client_socket.recv(16)
            # send file name want to download
            client_socket.send(bytes(command[1], "utf-8"))
            # wait boss return succeed then send continue
            client_socket.recv(16)
            # receive hostname and port of peer to download file
            info = pickle.loads(client_socket.recv(4096))

            peer_down_file(info, fname)
        case "public":
            client_socket.send(bytes(command[0], "utf-8"))
            # wait boss return succeed then send continue
            client_socket.recv(16)
            lname = command[1]
            fname = command[2]
            client_socket.send(bytes(command[2], "utf-8"))
            # wait boss return succeed then send continue
            client_socket.recv(16)
            print("public: ", lname, fname)


def thread_peer_client(host, port):
    client_socket = socket.socket()
    client_socket.connect((host, port))
    while True:
        val = peer_get_command()
        peer_handle_command(client_socket, val)


def server_program(host, port):
    # thread chay gui thong tin den cac peer
    nconn1 = Thread(target=peer_server_create, args=[localhost, peerport])
    nconn1.start()
    # thread ket noi den bigboss
    nconn2 = Thread(target=thread_peer_client, args=[boss_host, boss_port])
    nconn2.start()


if __name__ == '__main__':
    port = peerport
    server_program(boss_host, port)
