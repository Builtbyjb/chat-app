import socket
import threading
import sys

FT = 'utf-8'

# Creates a server object
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

usage = "USAGE: python3 server.py HOST PORT"

# Stores a list of user sockets currently connected
clients = []

# Stores a list of usernamess currently connected
usernames = []


def main():
    if len(sys.argv) != 3:
        print(usage)
        sys.exit()
    else:
        # Calls the start server function
        start(sys.argv[1], sys.argv[2])


# Starts the server
def start(arg1, arg2):
    try:
        server.bind((arg1, int(arg2)))
        server.listen()
        print("Server is running")
    except Exception:
        print(arg1, arg2)
        print("Connection error! invalid HOST or PORT, check and try again")
        sys.exit()

    while True:
        # Acceots connections
        conn, addr = server.accept()
        clients.append(conn)  # Adds users to the users list.

        # Recievers username of thee user
        username = conn.recv(1024).decode(FT)
        usernames.append(username)

        print(f"{username} is connected")
        broadcast(f"{username} is connected".encode(FT))

        # Creates a daemon thread that recieves data
        # from the users and sends it to the other users
        recv_thread = threading.Thread(target=handle_recieve,
                                       daemon=True,
                                       args=(conn,))
        recv_thread.start()


# Handles recieving and broadcasting of user data
def handle_recieve(conn):
    index = clients.index(conn)
    while True:
        try:
            message = conn.recv(1024).decode(FT)
            if message:
                broadcast(f"{usernames[index]}: {message}".encode(FT))
            elif len(message) == 0:
                print(f"{usernames[index]} disconnected!!")
                broadcast(f"{usernames[index]} disconnected!!".encode(FT))
                break
        except Exception:
            clients.remove(conn)
            usernames.remove(usernames[index])
            conn.close()
            break


# Handles the sending of data to all the users
def broadcast(message):
    for c in clients:
        c.send(message)


if __name__ == "__main__":
    main()
