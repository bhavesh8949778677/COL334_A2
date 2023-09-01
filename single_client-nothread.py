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
        return -2, line
    if (line[:2] == "-1" or line[0].isnumeric()) and line[-1] == "\n":
        return parse_line(line)
    return -2, line


def assemble_lines(data, entry, name, line_no=1000):
    """Assembles the data in the format for submission to server"""
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
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, server_port))
    return client_socket


broken_lines = []


def collect_lines(client_socket, line_count_limit=1000):
    """Requests the server in a loop until all lines are collected"""

    line_count = 0
    data = [None] * 1000

    # try:
    # wait_tries = 0
    while True:
        # result = validate_line(send_request(client_socket, "SENDLINE\n"))
        response = request_line(client_socket)
        result = parse_line(response)

        # Doing checks
        if result[0] == -2:
            broken_lines.append(result)
        if result[0] == -2 or result[0] == -1 or data[result[0]]:
            continue

        data[result[0]] = result[1]
        line_count += 1
        print(f"lines received: {line_count}\n no.:{result[0]}")

        if line_count == line_count_limit:
            break
    print("all lines received\n\n")
    return data

    # except Exception as e:
    #     print("Error:", e)

    # finally:


try:
    server_ip = "vayu.iitd.ac.in"
    server_port = 9801

    socket = connect_to_server(server_ip, server_port)
    print("Connected to the server.\n")

    r = send_request(socket, "SESSION RESET\n")
    print(r)

    if r == "Ok\n":
        full_text = collect_lines(socket, 1000)
        submission = assemble_lines(full_text, "2021CS50609", "blank", 1000)
        with open("sub.txt", "w") as f:
            f.write(submission)
        submission_response = send_request(socket, submission)
        print(submission_response)

except:
    pass

socket.close()
print("Connection closed.")
