import socket

server_ip = "vayu.iitd.ac.in"
server_port = 9801


def validate_line(line):
    """
    Runs basic checks on the string received from the server
    """
    # For incomplete packets, checking if it ends with \n
    # Line should also start with an integer.
    if (line[:2] == "-1" or line[0].isnumeric()) and line[-1] == "\n":
        line_list = line.split("\n")
        return int(line_list[0]), "\n".join(line_list[1:])
    return -2, None


def assemble_lines(data, entry, name):
    pass


def request_line(client_socket):
    """
    Returns [line number, line]
    """
    request = "SENDLINE\n"
    client_socket.send(request.encode("utf-8"))
    line = client_socket.recv(1000_000).decode("utf-8")
    return validate_line(line)


client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

line_count = 0
data = [None] * 1000

# try:
client_socket.connect((server_ip, server_port))
print("Connected to the server.\n")
# wait_tries = 0
while True:
    result = request_line(client_socket)

    # if result[0] == -2:
    #     print("incorrect packet. Retrying...\n")
    # continue
    # elif result[0] == -1:
    #     if wait_tries == 0:
    #         # First rate limit error, starts sending requests till wait over
    #         print("Rate limit exceeded. waiting...")
    #     wait_tries += 1
    # continue

    # if wait_tries != 0:
    #     # If condition means just before this request it was a rate limit error,
    #     # so now rate limit is over, resetting wait_tries
    #     print(f"wait over, after {wait_tries} tries\n")
    #     wait_tries = 0

    # if data[result[0]]:
    #     # print("already had. skipping\n")
    #     continue

    # Doing checks
    if result[0] == -2 or result[0] == -1 or data[result[0]]:
        continue

    # print(f"Received line {line[0]}:\n{line[1]}\n")
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
print("Connection closed.")
