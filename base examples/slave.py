from socket import *
import threading
import time

server = 'vayu.iitd.ac.in'
port = 9801
message = 'SENDLINE\n'

c = socket(AF_INET,SOCK_STREAM)
c.connect((server,port))
s = socket(AF_INET,SOCK_STREAM)
s.connect(('10.184.54.81',8828)) # my IP address


while True:
    try:
        print("Hi")
        # c.send(message.encode())
        # mess = c.recv(1024).decode()
        # print(mess)
        # s.send(mess.encode())
        time.sleep(0.01)
    except (BrokenPipeError, ConnectionResetError):
        print("Server connection closed. Exiting...")
        break


# c.close()