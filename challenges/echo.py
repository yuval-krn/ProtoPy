import socket


def echo(conn: socket.socket, addr: socket._RetAddress) -> None:
    with conn:
        print("New connection:", addr)
        while True:
            data = conn.recv(2048)
            if not data:
                break
            conn.sendall(data)
