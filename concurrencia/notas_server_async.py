import asyncio
import json
import socket


SOCKET_BUFFER = 1024


def busca_info(codigo: str) -> list[str]:
    with open("notas.csv", "r") as f:
        contenido = f.read()
    contenido = contenido.split("\n")

    print(f"longitud de contenido: {len(contenido)}")

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


def procesa_mensaje(dato: bytes) -> dict:
    try:
        msg_cliente = json.loads(dato)
        print(f"Mensaje del cliente: {msg_cliente}")
        if "codigo" in msg_cliente.keys() and "modo" in msg_cliente.keys():
            print("Codigo y modo existen")
            notas = busca_info(msg_cliente["codigo"])
            print(f"nota: {notas}")
            if len(notas) > 0:
                msg_respuesta = empaqueta_datos(notas, msg_cliente["modo"])
            else:
                msg_respuesta = {"estado": "error", "mensaje": "No existen registros para el codigo indicado"}
        else:
            msg_respuesta = {"estado": "error", "mensaje": "Solicitud enviada en formato incorrecto"}
    except json.decoder.JSONDecodeError:
        msg_respuesta = {"estado": "error", "mensaje": "No se pudo decodificar el mensaje de JSON"}

    print(f"respuesta: {msg_respuesta}")

    return msg_respuesta


async def handle_client(reader, writer):
    print("Cliente conectado")
    msg_bytes = await reader.read(SOCKET_BUFFER)
    print(f"Recibi {msg_bytes}")
    if msg_bytes:
        print("msg_bytes tiene data, procesando")
        msg_respuesta = procesa_mensaje(msg_bytes)
        print(f"Enviando respuesta: {msg_respuesta}")
        msg_respuesta_str = json.dumps(msg_respuesta)

        await writer.write(msg_respuesta_str.encode("utf-8"))
        await writer.drain()

    writer.close()
    await writer.wait_closed()
    print("conexion cerrada")

    
async def main():
    server_adddress = ("0.0.0.0", 5000)

    server = await asyncio.start_server(handle_client, server_adddress[0], server_adddress[1])

    async with server:
        print("Empezando servidor...")
        await server.serve_forever()

if __name__ == '__main__':
    asyncio.run(main())
