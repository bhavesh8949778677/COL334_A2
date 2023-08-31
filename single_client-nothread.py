import socket


def validate_line(line):
    """Runs basic checks on the string received from the server"""

    # For incomplete packets, checking if it ends with \n
    # Line should also start with an integer.
    if len(line) < 2:
        return -2, None
    if (line[:2] == "-1" or line[0].isnumeric()) and line[-1] == "\n":
        line_list = line.split("\n")
        return int(line_list[0]), "\n".join(line_list[1:])
    return -2, None


def assemble_lines(data, entry, name):
    """Assembles the complete data in the format for submission to server"""
    pass


def record_time(func, args):
    """Prints the time taken to run"""
    pass


def send_request(client_socket, request):
    client_socket.send(request.encode("utf-8"))
    response = client_socket.recv(1000_000).decode("utf-8")
    return response


def connect_to_server(server_ip, server_port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, server_port))
    return client_socket


def collect_lines(client_socket):
    """Requests the server in a loop until all lines are collected"""

    line_count = 0
    data = [None] * 1000

    # try:
    # wait_tries = 0
    while True:
        result = validate_line(send_request(client_socket, "SENDLINE\n"))

        # Doing checks
        if result[0] == -2 or result[0] == -1 or data[result[0]]:
            continue

        data[result[0]] = result[1]
        line_count += 1

        print(f"lines received: {line_count}")

        if line_count == 1000:
            break
    print("all lines received\n\n")
    return data

    # except Exception as e:
    #     print("Error:", e)

    # finally:


server_ip = "vayu.iitd.ac.in"
server_port = 9801

socket = connect_to_server(server_ip, server_port)
print("Connected to the server.\n")

r = send_request(socket, "SESSION RESET\n")
print(r)

if r == "Ok\n":
    d = collect_lines(socket)

socket.close()
print("Connection closed.")
