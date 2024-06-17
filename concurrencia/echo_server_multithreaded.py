import socket
from threading import Thread

SOCK_BUFFER = 1024

client_counter = 0

def client_handler(conn, client_address):
    global client_counter
    
    client_counter += 1
    print(f"Conexion de {client_address[0]}:{client_address[1]}, numero total de clientes conectados: {client_counter}")

    try:
        while True:
            dato = conn.recv(SOCK_BUFFER)
        
            if dato:
                print(f"Recibí: {dato}")
                conn.sendall(dato)
            else:
                print("No hay más datos")
                break
    except ConnectionResetError:
        print("El cliente cerró la conexión de manera abrupta")
    finally:
        print("Cerrando la conexión")
        client_counter -= 1
        conn.close()



if __name__ == '__main__':
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ("0.0.0.0", 5000)

    print(f"Levantando el servidor en {server_address[0]}, con puerto {server_address[1]}")

    sock.bind(server_address)

    sock.listen(5)

    while True:
        print("Esperando conexiones...")
        conn, client_address = sock.accept()
        
        t = Thread(target=client_handler, args=(conn, client_address))
        t.start()
