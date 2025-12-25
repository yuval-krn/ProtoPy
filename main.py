import socket
import threading

PORT = 50007


def echo(conn: socket.socket, addr: socket._RetAddress) -> None:
    with conn:
        print("New connection:", addr)
        while True:
            data = conn.recv(2048)
            if not data:
                raise RuntimeError("Broken Connection")
            conn.sendall(data)


def make_client_thread(
    conn: socket.socket, addr: socket._RetAddress
) -> threading.Thread:
    t = threading.Thread(target=echo, args=(conn, addr))
    return t


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((socket.gethostname(), PORT))
        s.listen(5)
        print("Listening on port", PORT)
        while True:
            conn, addr = s.accept()
            ct = make_client_thread(conn, addr)
            ct.start()


if __name__ == "__main__":
    main()
