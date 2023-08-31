import socket

server_ip = "vayu.iitd.ac.in"
server_port = 9801

"""
def validate_line(line):
    # Runs basic checks on the string received from the server
 
    # For incomplete packets, checking if it ends with \n
    # Line should also start with an integer.
    if (line[:2] == "-1" or line[0].isnumeric()) and line[-1] == "\n":
        line_list = line.split("\n")
        return int(line_list[0]), "\n".join(line_list[1:])
    return -2, None


def assemble_lines(data, entry, name):
    pass


def request_line(client_socket):
    # Returns [line number, line]
    request = "SENDLINE\n"
    client_socket.send(request.encode("utf-8"))
    line = client_socket.recv(1000_000).decode("utf-8")
    return validate_line(line)  
"""
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

    return received_data.decode("utf-8").strip()

def request_line(client_socket):
    # Returns [line number, line]
    request = "SENDLINE\n"
    client_socket.send(request.encode("utf-8"))
    line = receive_full_line(client_socket)
    return line

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

line_count = 0
data = [None] * 1000

# try:
client_socket.connect((server_ip, server_port))
print("Connected to the server.\n")
# wait_tries = 0
while True:
    result = request_line(client_socket)
    if result[0] == -2 or result[0] == -1 or data[result[0]]:
        continue

    data[result[0]] = result[1]
    line_count += 1

    print(f"lines received: {line_count}")

    if line_count == 1000:
        break
print("all lines received\n\n")


# except Exception as e:
#     print("Error:", e)

# finally:
client_socket.close()
print("Connection closed.")
