import socket
from threading import Thread
import pickle
import subprocess

sockets_list = [
    [[], []],
    []
]
# socket_list[0][0] = ip(hostname) + port of first peer
# socket_list[0][1] = list_file of this hostname of first peer
# socket_list[1][0] = ip(hostname) + port of second peer
# socket_list[1][1] = list_file of this hostname of second peer

# serversocket = 0
server_host = "192.168.31.162"
server_port = 5000


def get_user_input():
    while True:
        user_input = input()
        command = user_input.split(" ")
        if command[0] == "discover":
            print("List of hostname ", command[1], "is: ")
            # print list file of command[1] (hostname)
            for index1, i in enumerate(sockets_list):
                if isinstance(i, list):
                    # item[ [ [host, port], [file] ] ]
                    for index2, item in enumerate(i):
                        if isinstance(item, list):
                            if item[0][0] == command[1]:
                                print("Yes")
                            else:
                                # print from item[1] -> end -> [file]
                                for index, k in enumerate(item):
                                    print("file", index, "is:", k)
            print("Discover done")
        if command[0] == "ping":
            # print ping
            ping_process = subprocess.Popen(
                ["ping", "-n", "4", command[1]], stdout=subprocess.PIPE)
            ping_output = ping_process.communicate()[0]
            print(ping_output.decode('utf-8'))
            print("Ping done")
        if command[0].lower() == "exit":
            break


def new_connection(addr, conn):
    status = ""
    while True:
        str_recv = addr.recv(16)
        # print("receive: \n", str)
        str_recv = str(str_recv, "utf-8")
        addr.send(bytes("receive success", "utf-8"))

        match str_recv:
            case "add list":
                print("add list: ")
                item = pickle.loads(addr.recv(4096))
                sockets_list[0][0].append(item)
                print(item)
                addr.send(bytes("receive success", "utf-8"))
                status = ""
                print("list: ", sockets_list)
            case "get list":

                print("get list: \n")
                status = ""
            case "fetch":
                print("fetch")
                # receive file name peer want to download
                str_recv = str(addr.recv(16), "utf-8")
                addr.send(bytes("receive success", "utf-8"))
                # send hostname and port have this file
                flag = True
                for index1, i in enumerate(sockets_list):
                    if isinstance(i, list):
                        for index2, item in enumerate(i):
                            for index3, k in enumerate(item):
                                if k == str_recv:
                                    print(
                                        f"Index: {index1, index2, index3}, Value: {k, i[0]}")
                                    data = pickle.dumps(i[0])
                                    addr.send(data)
                                    flag = False
                if flag:
                    addr.send(bytes("do not have this file", "utf-8"))
            case "public":
                str_recv = addr.recv(16)
                sockets_list[0][1].append(str(str_recv, "utf-8"))
                addr.send(bytes("receive success", "utf-8"))
                print(str_recv)


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
        nconn2 = Thread(target=get_user_input)
        nconn2.start()


if __name__ == '__main__':
    host = socket.gethostname()
    # host = "192.168.31.162"
    port = 5000
    server_program(host, port)
    # print("local + port: ", sockets_list[0][0])
    # print("file name: ", sockets_list[1])
