import random
import socket
import pickle

class Tablero:
    def __init__(self):
        self.casillas = ["normal"] * 68
        self.salidas = {1: 1, 2: 18, 3: 35, 4: 52}
        self.llegadas = {1: 64, 2: 13, 3: 30, 4: 47}
        self.casillas_de_llegada = ["seguro"] * 7
        self.definir_especiales()

    def definir_especiales(self):
        for i in [8, 13, 25, 30, 42, 47, 59, 64]:
            self.casillas[i] = "seguro"
        for salida in self.salidas.values():
            self.casillas[salida] = "salida"

    def tipo_de_casilla(self, posicion):
        if 0 <= posicion < len(self.casillas):
            return self.casillas[posicion]

class Jugador:
    def __init__(self, nombre, color, numero, socket_cliente):
        self.nombre = nombre
        self.color = color
        self.numero = numero
        self.socket_cliente = socket_cliente
        self.salida = tablero.salidas[self.numero]
        self.llegada = tablero.llegadas[self.numero]
        self.fichas = [Ficha(self.salida, self.llegada) for _ in range(4)]
        self.turno = False
        self.fichas_fuera = []  # Lista de fichas fuera de la cárcel
        self.fichas_meta = 0  # Fichas que han llegado a la meta

    def desbloquear(self):
        self.bloqueado = False

    def bloquear(self):
        self.bloqueado = True

    def tiene_fichas_fuera(self):
        return len(self.fichas_fuera) > 0

    def ha_ganado(self):
        return all(ficha.en_meta for ficha in self.fichas)

class Ficha:
    def __init__(self, casilla_salida, casilla_llegada):
        self.en_carcel = True
        self.posicion = None
        self.en_seguro = False
        self.en_llegada = False
        self.en_meta = False
        self.casilla_salida = casilla_salida
        self.casilla_llegada = casilla_llegada

    def sacar_de_carcel(self):
        if self.en_carcel:
            self.posicion = self.casilla_salida
            self.en_carcel = False
            self.en_seguro = True
            return True
        return False

    def mover(self, pasos):
        if self.en_carcel:
            raise Exception("No puedes mover una ficha que está en la cárcel.")
        if self.en_meta:
            raise Exception("No puedes mover una ficha que ya llegó a la meta.")
        
        if not self.en_llegada:
            nueva_posicion = (self.posicion + pasos) % 68
            if nueva_posicion == self.casilla_llegada:
                self.en_llegada = True
                self.posicion = self.casilla_llegada
                self.en_seguro = True
            else:
                self.posicion = nueva_posicion
                self.en_seguro = tablero.tipo_de_casilla(self.posicion) in ["seguro", "salida"]
        else:
            nueva_posicion = self.posicion + pasos
            if self.posicion < self.casilla_llegada + 7:
                self.posicion = nueva_posicion
                if self.posicion >= self.casilla_llegada + 7:
                    self.en_meta = True
            else:
                raise Exception("Movimiento inválido.")

    def enviar_a_carcel(self):
        if not self.en_seguro:
            self.posicion = None
            self.en_carcel = True
            self.en_seguro = False

class Dado:
    def __init__(self):
        self.valor = 0

    def lanzar(self):
        self.valor = random.randint(1, 6)
        return self.valor

tablero = Tablero()

class GameServer:
    def __init__(self, host='localhost', port=12345):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((host, port))
        self.server_socket.listen(4)
        self.jugadores = []
        self.turno_actual = 0

    def aceptar_conexiones(self):
        print("Esperando conexiones de jugadores...")
        while len(self.jugadores) < 4:
            cliente_socket, cliente_address = self.server_socket.accept()
            print(f"Jugador conectado: {cliente_address}")
            cliente_socket.send(pickle.dumps("¡Conectado al servidor!"))
            nombre = cliente_socket.recv(1024).decode()
            color = cliente_socket.recv(1024).decode()
            jugador = Jugador(nombre, color, len(self.jugadores) + 1, cliente_socket)
            self.jugadores.append(jugador)

            if len(self.jugadores) > 1:
                mensaje = "Hay suficientes jugadores para comenzar el juego. ¿Deseas empezar? Responde 'sí' o 'no'."
                cliente_socket.send(pickle.dumps(mensaje))

        print("Todos los jugadores se han conectado.")

    def iniciar_juego(self):
        self.aceptar_conexiones()

        # Esperar respuestas de todos los jugadores
        respuestas = []
        for jugador in self.jugadores:
            respuesta = self.recibir_mensaje(jugador)
            respuestas.append(respuesta.lower() == "sí")

        # Si todos aceptan, iniciar el juego
        if all(respuestas):
            for jugador in self.jugadores:
                jugador.socket_cliente.send(pickle.dumps("El juego ha comenzado!"))
            self.manejar_turnos()
        else:
            for jugador in self.jugadores:
                jugador.socket_cliente.send(pickle.dumps("No todos han aceptado, el juego no comienza."))

    def recibir_mensaje(self, jugador):
        return pickle.loads(jugador.socket_cliente.recv(1024))

    def manejar_turnos(self):
        while True:
            jugador_actual = self.jugadores[self.turno_actual]
            jugador_actual.socket_cliente.send(pickle.dumps("Es tu turno. Lanza los dados."))
            dado = Dado()
            tirada1 = dado.lanzar()
            tirada2 = dado.lanzar()
            jugador_actual.socket_cliente.send(pickle.dumps((tirada1, tirada2)))
            print(f"{jugador_actual.nombre} ha sacado {tirada1} y {tirada2} en los dados.")
            
            self.turno_actual = (self.turno_actual + 1) % len(self.jugadores)

            if any(jugador.ha_ganado() for jugador in self.jugadores):
                ganador = next(jugador for jugador in self.jugadores if jugador.ha_ganado())
                for jugador in self.jugadores:
                    jugador.socket_cliente.send(pickle.dumps(f"¡{ganador.nombre} ha ganado!"))
                break

        self.server_socket.close()

# Ejecutar el servidor
if __name__ == "__main__":
    servidor = GameServer()
    servidor.iniciar_juego()
