import socket
import pickle


class GameClient:
    def __init__(self, host='localhost', port=12345):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((host, port))

    def recibir_mensaje(self):
        return pickle.loads(self.client_socket.recv(1024))

    def jugar(self):
        print(self.recibir_mensaje())  # Mensaje de conexión

        # Registro del jugador
        nombre = input("Introduce tu nombre: ")
        color = input("Introduce tu color: ")

        self.client_socket.send(nombre.encode())
        self.client_socket.send(color.encode())

        # Esperar hasta que el servidor decida si iniciar el juego
        mensaje = self.recibir_mensaje()
        print(mensaje)

        # Responder si está listo para iniciar el juego
        respuesta = input("¿Deseas comenzar el juego? (sí/no): ").strip()
        self.client_socket.send(pickle.dumps(respuesta))

        # Esperar la confirmación del servidor de que el juego ha comenzado
        mensaje = self.recibir_mensaje()
        print(mensaje)

        # Aquí puede continuar con el flujo del juego, como tirar los dados, mover fichas, etc.


# Ejecutar el cliente
if __name__ == "__main__":
    cliente = GameClient()
    cliente.jugar()
