import json
import socket
from threading import Thread

SOCK_BUFFER = 1024


def busca_info(codigo: str) -> list[str]:
    with open("notas.csv", "r") as f:
        contenido = f.read()
    contenido = contenido.split("\n")

    for fila in contenido:
        if codigo in fila:
            return fila.split(",")
        
    return list()


def empaqueta_datos(notas: list[str], modo: str) -> dict:
    match modo:
        case"cliente":
            r_dict = dict()
            for idx in range(12):
                r_dict[f"lab{idx + 1}"] = int(notas[idx + 1])
            r_dict["e1"] = int(notas[13])
            r_dict["e2"] = int(notas[14] )
            r_dict["estado"] = "éxito"
        case "servidor":
            notas_lab = 0
            for idx in range(12):
                notas_lab += int(notas[idx + 1])
            notas_lab = notas_lab / 12

            nota = (notas_lab * 0.5) + (int(notas[13]) * 0.25) + (int(notas[14]) * 0.25)

            r_dict = {"estado": "éxito", "nota": nota}
        case _:
            r_dict = {"estado": "error", "mensaje": "modo seleccionado no es válido"}
    
    return r_dict


def client_handler(conn, client_address):
    print(f"Conexion de {client_address[0]}:{client_address[1]}")
    try:
        while True:
            dato = conn.recv(SOCK_BUFFER)
        
            if dato:
                print(f"Recibí: {dato}")
                d = json.loads(dato)
                if "codigo" in d.keys() and "modo" in d.keys():
                    notas = busca_info(d["codigo"])
                    if len(notas) > 0:
                        msg_dict = empaqueta_datos(notas, d["modo"])
                    else:
                        msg_dict = {"estado": "error", "mensaje": "No existen registros para el codigo indicado"}
                else:
                    msg_dict = {"estado": "error", "mensaje": "Solicitud enviada en formato incorrecto"}
                conn.sendall(json.dumps(msg_dict).encode("utf-8"))
            else:
                print("No hay más datos")
                break
    except ConnectionResetError:
        print("El cliente cerró la conexión de manera abrupta")
    finally:
        print("Cerrando la conexión")
        conn.close()


if __name__ == '__main__':
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ("0.0.0.0", 5000)

    print(f"Levantando el servidor en {server_address[0]}, con puerto {server_address[1]}")

    sock.bind(server_address)

    sock.listen(1)

    while True:
        print("Esperando conexiones...")
        conn, client_address = sock.accept()
        print(f"Conexion de {client_address[0]}:{client_address[1]}")

        t = Thread(target=client_handler, args=(conn, client_address))
        t.start()
