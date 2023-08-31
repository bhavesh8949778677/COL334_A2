from socket import *
import threading
import time

server = 'vayu.iitd.ac.in'
port = 9801
message = 'SENDLINE\n'

c = socket(AF_INET,SOCK_STREAM)
c.connect((server,port))
s = socket(AF_INET,SOCK_STREAM)
s.connect(('127.0.0.1',8828))


while True:
    try:
        c.send(message.encode())
        mess = c.recv(1024).decode()
        s.send(mess.encode())
        time.sleep(0.01)
    except (BrokenPipeError, ConnectionResetError):
        print("Server connection closed. Exiting...")
        break


c.close()
s.close()
