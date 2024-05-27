import socket

SOCK_BUFFER = 4


if __name__ == '__main__':
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_address = ("localhost", 5000)
    print(f"Conectandonos al servidor en {server_address[0]} en el puerto {server_address[1]}")

    sock.connect(server_address)

    msg = "hola mundo!"
    msg_bytes = msg.encode("utf-8")
    cantidad_esperada = len(msg_bytes)
    cantidad_recibida = 0
    msg_retorno_bytes = b''

    sock.sendall(msg_bytes)

    while cantidad_recibida < cantidad_esperada:
        dato = sock.recv(SOCK_BUFFER)
        print(f"Recibí: {dato}")
        msg_retorno_bytes += dato
        cantidad_recibida += len(dato)

    sock.close()
    print(f"Mensaje completo recibido {msg_retorno_bytes.decode('utf-8')}")
