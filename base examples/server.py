from socket import *
import threading
import time
server_port = 8828

lock = threading.Lock()

def handle_client(connection, client_number):
    global counter, data
    while counter<1000:
        sentence = connection.recv(1024).decode()
        # print("sentence = ", sentence)
        x = parse(sentence)
        if (x!=None): 
            with lock:  
                if (data[x[0]] == ''):
                    counter+=1
                    data[x[0]] = x[1]
                    # print(counter, time.time() - st) 
                    print(f"Client {client_number}: Counter = {counter}, Time = {time.time() - st}")
    connection.close()


serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.bind(('0.0.0.0',server_port))
serverSocket.listen(3)
print('Server is ready to receive')


counter = 0
data = ['' for x in range(1001)]
client_number = 1

def parse(s):
    l = s.split()
    try:
        x = int(l[0])
        if (x == -1):
            return None
        return x,l[1]
    except ValueError:
        return None


st = time.time()

# one connection is directly to server itself
# but if i use my slave then it is not optimal but ok

while True:
    connection, addr = serverSocket.accept()
    # print(addr)
    client_thread = threading.Thread(target=handle_client, args=(connection, client_number))
    client_thread.start()
    client_number += 1