import socket


def parse_line(line_str):
    """Converts the line string to (line number, line) pair"""
    line_list = line_str.split("\n")
    return int(line_list[0]), "\n".join(line_list[1:])


def validate_line(line):
    """Runs basic checks on the string received from the server, and returns parsed line"""

    # For incomplete packets, checking if it ends with \n
    # Line should also start with an integer.
    if len(line) < 2:
        return -2, None
    if (line[:2] == "-1" or line[0].isnumeric()) and line[-1] == "\n":
        return parse_line(line)
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


def receive_full_line(client_socket):
    buffer_size = 1024
    received_data = b""

    while True:
        chunk = client_socket.recv(buffer_size)
        if not chunk:
            break
        received_data += chunk
        if b"\n" in received_data:
            break
    # I've removed the .strip() at the end to keep the final '\n'
    # so that we can verify later with validate_line() that this function gets the complete line
    return received_data.decode("utf-8")


def request_line(client_socket):
    # Returns [line number, line]
    request = "SENDLINE\n"
    client_socket.send(request.encode("utf-8"))
    line = receive_full_line(client_socket)
    return line


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
        # result = validate_line(send_request(client_socket, "SENDLINE\n"))
        response = request_line(client_socket)
        result = validate_line(response)
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
