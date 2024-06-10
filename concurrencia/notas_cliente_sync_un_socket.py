import json
import socket
import sys
import time

SOCK_BUFFER = 1024


if __name__ == '__main__':
    try:
        offset = int(sys.argv[1])
    except ValueError:
        offset = 0
    except IndexError:
        offset = 0

    codigo_base = 20240001
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_address = ("localhost", 5000)
    print(f"Conectandonos al servidor en {server_address[0]} en el puerto {server_address[1]}")

    sock.connect(server_address)

    notas_finales = list()

    for idx in range(10):
        msg = {"codigo": f"{codigo_base + offset + idx}", "modo": "servidor"}

        sock.sendall(json.dumps(msg).encode("utf-8"))
        dato = sock.recv(SOCK_BUFFER)
        print(f"Recibi del servidor: {dato}")
        dato_json = json.loads(dato)
        if dato_json["estado"] == "éxito" or dato_json["estado"] == "exito":
            notas_finales.append({"codigo": msg["codigo"], "nota": dato_json["nota"]})
        
        time.sleep(2)

    sock.close()

    for nota_final in notas_finales:
        print(f"Nota final de {nota_final['codigo']}: {nota_final['nota']}")
