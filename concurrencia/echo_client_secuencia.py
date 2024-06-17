import socket
import time

SOCK_BUFFER = 1024


if __name__ == '__main__':
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_address = ("localhost", 5000)
    print(f"Conectandonos al servidor en {server_address[0]} en el puerto {server_address[1]}")

    sock.connect(server_address)

    for i in range(10):
        msg = f"hola mundo {i}!"

        sock.sendall(msg.encode("utf-8"))
        dato = sock.recv(SOCK_BUFFER)

        time.sleep(2)

    sock.close()

    print(f"Recibí: {dato}")
