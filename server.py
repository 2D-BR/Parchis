import select
import socket
import pickle

conexiones = []
usuarios = []
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
turno = 1
parques = None
jugando = False
juego_finalizado = False
colores_disponibles = {
    1: "ROJO",
    2: "AMARILLO",
    3: "AZUL",
    4: "VERDE"
}

def enviar_mensaje_a_todos(message):
    print('\nse inicia el envio de datos.')
    for _socket in conexiones:
        if _socket != server_socket:
            try:
                _socket.send(message)
                print("datos enviados a: ", _socket)
            except:
                _socket.close()
                conexiones.remove(_socket)
                print("error enviando datos a: ", _socket)
    print('envio de datos terminado.\n')


def nuevo_jugador(cliente):
    mensaje = "Bienvenido\n" \
              "A continuación ingrese: nombre de usuario y color " \
              "en ese orden y separado por comas.\n" \
              "Ingrese el número del color en base a la siguiente lista:\n" \
              "Colores disponibles:\n" + str(colores_disponibles)

    cliente.send(bytes(mensaje, 'utf-8'))  # Envía el mensaje inicial en bytes
    datos = cliente.recv(1024).decode('utf-8').split(",")

    if len(datos) != 2:
        cliente.send(bytes("Datos con formato incorrecto. Intente de nuevo.", 'utf-8'))  # Codifica el mensaje a bytes
        return False

    if int(datos[1]) not in colores_disponibles.keys():
        cliente.send(bytes("Color incorrecto. Intente de nuevo.", 'utf-8'))  # Codifica el mensaje a bytes
        return False
    cliente.send(bytes("Ok, todo bien, todo bonito.", 'utf-8'))  # Codifica el mensaje a bytes
    pos = len(usuarios) + 1
    nombre = datos[0]
    color = int(datos[1])
    jugador = (nombre, color, pos)
    usuarios.append(jugador)
    del(colores_disponibles[color])
    return True





if __name__ == '__main__':

    server_socket.bind(("localhost", 5000))
    server_socket.listen(4)
    conexiones.append(server_socket)

    while not juego_finalizado:
        print('SERVIDOR DE PARQUES EN SERVICIO')
        read_sockets, write_sockets, error_sockets = select.select(conexiones, [], [])

        for _socket in read_sockets:

            # Nueva conexion
            if _socket == server_socket:

                nuevo_socket, addr = server_socket.accept()
                print('atendiendo conexion entrante.')
                if len(conexiones) > 5:
                    nuevo_socket.send("El juego esta lleno, intenta mas tarde.")
                    break
                if jugando:
                    nuevo_socket.send("\nya se esta jugando una partida. intente mas tarde\n")
                    break

                resultado = nuevo_jugador(nuevo_socket)
                if resultado:
                    enviar_mensaje_a_todos("se unio un nuevo jugador")
                    conexiones.append(nuevo_socket)
                    # if len(usuarios) >= 2:
                    #     resultado = preguntar_iniciar()
                    #     if resultado:
                    #         iniciar_juego()
                    #     else:
                    #         enviar_mensaje_a_todos("juego no iniciado, un integrante quiere esperar.")
            # Datos recibidos de un cliente
            else:
                try:
                    data = _socket.recv(4096)
                    procesar_datos(data)
                    if juego_finalizado:
                        break
                except:
                    print("Un cliente desconectado")
                    conexiones.remove(_socket)
                    _socket.close()
                    continue
    server_socket.close()
