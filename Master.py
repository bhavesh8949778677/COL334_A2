from socket import *
import sys
import threading
import time
from dotenv import load_dotenv, find_dotenv
import os


# Global Variables

# Default server
server_ip = "10.17.7.134"
server_port = 9801

client_number = 1  # Increments when other clients join
serverSocket = 0
connection_list = []  # list of all connections made

data = [None] * 1000
line_count = 0

stop_event = threading.Event()  # To Terminate All Threads and close the code
skt = 0
submitted = 0

def parse_line(line_str):
    """Converts the line string to (line number, line) pair"""
    line_list = line_str.split("\n")
    try:
        s = int(line_list[0]), "\n".join(line_list[1:])
        return s
    except:
        pass


def validate_line(line):
    """Runs basic checks on the string received from the server, and returns parsed line"""

    # For incomplete packets, checking if it ends with \n
    # Line should also start with an integer.
    if len(line) < 2:
        return -2, line
    if (line[:2] == "-1" or line[0].isnumeric()) and line[-1] == "\n":
        return parse_line(line)
    return -2, line


def assemble_lines(data, entry, name, line_no=1000):
    """Assembles the data in the format for submission to server"""
    # entry = os.environ.get("ENTRY_NO")
    submission = f"SUBMIT\n{entry}@{name}\n{line_no}\n"
    for i in range(len(data)):
        if data[i] != None:
            submission += f"{i}\n{data[i]}"
    return submission


def record_time(func, args):
    """Prints the time taken to run"""
    pass


def send_request(client_socket, request):
    """WITHOUT USING receive_full_line()"""
    client_socket.send(request.encode("utf-8"))
    response = client_socket.recv(1000_000).decode("utf-8")
    return response


def receive_full_line(client_socket):
    """Keeps retrying recv() till we get empty response,
    to ensure that all the data is received.
    """
    buffer_size = 1024
    received_data = b""

    while True:
        chunk = client_socket.recv(buffer_size)
        if not chunk:
            break
        received_data += chunk
        if received_data[-1:] == b"\n":
            break
    return received_data.decode("utf-8")


def request_line(client_socket):
    request = "SENDLINE\n"
    client_socket.send(request.encode("utf-8"))
    response = receive_full_line(client_socket)
    return response


def connect_to_server(server_ip, server_port):
    client_socket = socket(AF_INET, SOCK_STREAM)
    client_socket.connect((server_ip, server_port))
    return client_socket


broken_lines = []


broadcast_lock = threading.Lock()


def broadcast(result):
    global connection_list
    # print(connection_list)
    with broadcast_lock:
        message = str(result[0]) + "\n" + result[1]
        for connection in connection_list:
            connection.send(message.encode())
        # time.sleep(1)
    # with concurrent.futures.ThreadPoolExecutor() as executor:
    #     executor.map(lambda conn: conn.send(message.encode()), connection_list)


def collect_lines(client_socket, line_count_limit=1000):
    """Requests the server in a loop until all lines are collected"""
    # try:
    # wait_tries = 0
    global line_count, data
    while True:
        response = request_line(client_socket)
        result = parse_line(response)

        # Doing checks
        if result == None:
            break
        if result[0] == -2:
            broken_lines.append(result)
        if result[0] == -2 or result[0] == -1 or data[result[0]]:
            continue

        data[result[0]] = result[1]
        line_count += 1
        # broadcast(result)
        print(f"lines received: {line_count}\n no.:{result[0]}")

        if line_count == line_count_limit:
            break
    print("all lines received\n\n")
    return data


def connect_server(server_ip=server_ip, server_port=server_port):
    strt = time.time()
    global skt,submitted,connection_list
    skt = connect_to_server(server_ip, server_port)
    print("Connected to the server.\n")

    r = send_request(skt, "SESSION RESET\n")
    print(r)

    if r == "Ok\n":
        full_text = collect_lines(skt, 1000)
        if (submitted == 0):
            submission = assemble_lines(full_text, "2021CS50609", "blank", 1000)
            with open("sub.txt", "w") as f:
                f.write(submission)
            submission_response = send_request(skt, submission)
            print(submission_response)
    skt.close()
    print("Connection closed")
    if (submitted == 0):
        submitted = 1
        print("Every Thing is done")
        print("Time Taken : ", time.time() - strt)
        print("Broadcasting all lines")
        for i in range(line_count):
            broadcast([i, data[i]])
            time.sleep(0.001)
        print("all lines broadcasted")
    return


def handle_client(connection, client_number):
    global line_count, data, submitted
    strt = 0
    flag = 0
    while True:
        response = receive_full_line(connection)
        if flag == 0:
            strt = time.time()
            flag = 1
        result = parse_line(response)
        if result == None:
            break
        if result[0] == -2:
            broken_lines.append(result)
        if result[0] == -2 or result[0] == -1 or data[result[0]]:
            continue

        data[result[0]] = result[1]
        line_count += 1
        print(f"Data from {client_number} Client")
        print(f"lines received: {line_count}\n no.:{result[0]}")
        if line_count >= 1000:
            break
    print("all lines received\n\n")
    print("Last Line is received from some client")
    if (submitted == 0):
        submission = assemble_lines(data, "2021CS50594", "blank", 1000)
        with open("sub.txt", "w") as f:
            f.write(submission)
        submission_response = send_request(skt, submission)
        print(submission_response)
        print("Connection closed")
        submitted = 1
        print("Every Thing is done")
        print("Time Taken : ", time.time() - strt)
        print("Broadcasting all lines")
        for i in range(line_count):
            broadcast([i, data[i]])
            time.sleep(0.001)
        print("all lines broadcasted")
    return



def act_server():
    global serverSocket, client_number
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.bind(("0.0.0.0", 8828))
    serverSocket.listen(5)
    print("Server is ready to receive")

    while True:
        if stop_event.is_set():
            for connection in connection_list:
                connection.close()
            break
        connection, addr = serverSocket.accept()
        print(f"Succesful Connection with a client with addr = {addr}")
        print(connection)
        connection_list.append(connection)
        print(connection_list)
        client_thread = threading.Thread(
            target=handle_client, args=(connection, client_number)
        )
        client_thread.start()
        # client_thread.join()
        client_number += 1


def main():
    print("Program Starts")
    threads = []
    while True:
        s = input("Input : ")
        print("Parsing the inputs")
        l = s.split(" ")
        if l[0].lower() == "connect_server":
            print(
                "This command will connect vayu and start taking the inputs from vayu"
            )
            if len(l) < 2:
                print(
                    f"Connecting to default Server : {server_ip} at port {server_port}"
                )
                t = threading.Thread(
                    target=connect_server, args=(server_ip, server_port)
                )
                t.start()
                threads.append(t)
            else:
                print(f"Connecting to server : {l[1]} at port {l[2]}")
                t = threading.Thread(target=connect_server, args=(l[1], l[2]))
                t.start()
                threads.append(t)

        elif l[0].lower() == "act_server":
            print(f"Starting the server for all")
            t = threading.Thread(target=act_server, args=())
            t.start()
        elif s.lower() == "exit":
            print("Exitting the Program")
            stop_event.set()  # Turn off all threads
            for thread in threads:
                thread.join()
            sys.exit(0)
        else:
            print("Could not parse the input")


if __name__ == "__main__":
    main()
