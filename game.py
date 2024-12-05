import random

class Tablero:
    def __init__(self):
        self.casillas = ["normal"] * 68
        self.salidas = {1: 1, 2: 18, 3: 35, 4: 52}  # Casillas de salida por jugador
        self.llegadas = {1: 64, 2: 13, 3: 30, 4: 47}  # Casillas de llegada específicas
        self.casillas_de_llegada = ["seguro"] * 7
        self.definir_especiales()

    def definir_especiales(self):
        for i in [8, 13, 25, 30, 42, 47, 59, 64]:  # Casillas de seguro
            self.casillas[i] = "seguro"
        for salida in self.salidas.values():  # Salidas
            self.casillas[salida] = "salida"

    def tipo_de_casilla(self, posicion):
        if 0 <= posicion < len(self.casillas):
            return self.casillas[posicion]


class Jugador:
    def __init__(self, nombre, color, numero):
        self.nombre = nombre
        self.color = color
        self.numero = numero  # Número de jugador
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
        # El jugador ha ganado si todas sus fichas han llegado a la meta
        return all(ficha.en_meta for ficha in self.fichas)


class Ficha:
    def __init__(self, casilla_salida, casilla_llegada):
        self.en_carcel = True
        self.posicion = None  # Posición actual en el tablero (None si está en la cárcel)
        self.en_seguro = False
        self.en_llegada = False
        self.en_meta = False
        self.casilla_salida = casilla_salida
        self.casilla_llegada = casilla_llegada  # Casilla de llegada específica

    def sacar_de_carcel(self):
        if self.en_carcel:
            self.posicion = self.casilla_salida
            self.en_carcel = False
            self.en_seguro = True
            return True  # Indicamos que la ficha ha salido de la cárcel
        return False

    def mover(self, pasos):
        if self.en_carcel:
            raise Exception("No puedes mover una ficha que está en la cárcel.")
        if self.en_meta:
            raise Exception("No puedes mover una ficha que ya llegó a la meta.")

        if not self.en_llegada:
            # Movimiento en las casillas generales
            nueva_posicion = (self.posicion + pasos) % 68
            if nueva_posicion == self.casilla_llegada:
                self.en_llegada = True
                self.posicion = self.casilla_llegada  # Llegada específica del jugador
                self.en_seguro = True  # Todas las casillas de llegada empiezan como seguras
            else:
                self.posicion = nueva_posicion
                self.en_seguro = tablero.tipo_de_casilla(self.posicion) in ["seguro", "salida"]

        else:
            # Movimiento dentro de las casillas de llegada (avanzar 7 casillas)
            nueva_posicion = self.posicion + pasos
            # Verificamos que no se salga de las 7 casillas de la meta
            if self.posicion < self.casilla_llegada + 7:
                self.posicion = nueva_posicion
                if self.posicion >= self.casilla_llegada + 7:  # Llegar a la casilla final de la meta
                    self.en_meta = True
            else:
                raise Exception("Movimiento inválido: no puedes salir de las casillas de llegada.")

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

def inicio_del_juego():
    print("¡Bienvenido al juego de Parchís!")

    jugadores = []
    colores_usados = set()

    while True:
        print("\nOpciones:")
        print("1. Registrar un jugador")
        print("2. Iniciar el juego")

        opcion = input("Elige una opción (1 o 2): ").strip()

        if opcion == "1":
            # Registro de un nuevo jugador
            if len(jugadores) == 4:
                print("El juego solo admite hasta 4 jugadores.")
                continue

            nombre = input("Introduce el nombre del jugador: ").strip()
            while True:
                color = input("Introduce un color para el jugador: ").strip().capitalize()
                if color not in colores_usados:
                    colores_usados.add(color)
                    break
                print("Ese color ya está ocupado, elige otro.")

            numero = len(jugadores) + 1
            jugadores.append(Jugador(nombre, color, numero))
            print(f"Jugador {nombre} ({color}) registrado exitosamente.")

        elif opcion == "2":
            if len(jugadores) < 2:
                print("Necesitas al menos 2 jugadores para comenzar.")
            else:
                print("¡El juego está listo para comenzar!")
                break

        else:
            print("Opción no válida. Intenta de nuevo.")

    return jugadores


def mostrar_tablero(jugadores):
    print("\nEstado del tablero:")
    for jugador in jugadores:
        print(f"{jugador.nombre} ({jugador.color}):")
        for i, ficha in enumerate(jugador.fichas, 1):
            print(f"  Ficha {i}: Posición {ficha.posicion} - {'En cárcel' if ficha.en_carcel else 'En meta' if ficha.en_meta else 'En juego'}")


def turno_de_jugador(jugador):
    print(f"\nEs el turno de {jugador.nombre} ({jugador.color})")
    input("Presiona Enter para tirar los dados...")

    dado = Dado()
    tirada1 = dado.lanzar()
    tirada2 = dado.lanzar()
    print(f"{jugador.nombre} ha sacado {tirada1} y {tirada2} en los dados.")

    # Verificar si tiene fichas fuera de la cárcel
    fichas_fuera = [ficha for ficha in jugador.fichas if not ficha.en_carcel]

    # Siempre que salga un par, se deben sacar todas las fichas de la cárcel
    if tirada1 == tirada2:
        print("¡Has sacado un par! Todas las fichas de la cárcel saldrán ahora.")
        for i, ficha in enumerate(jugador.fichas, 1):
            if ficha.sacar_de_carcel():
                print(f"La ficha {i} ha salido de la cárcel.")

    if len(fichas_fuera) == 0:  # Si no tiene fichas fuera
        print("No tienes fichas fuera de la cárcel. Debes sacar un 5 o un par para sacar una ficha de la cárcel.")
        return False  # No se mueve ninguna ficha en este turno

    print("Fichas disponibles para mover:")
    for i, ficha in enumerate(fichas_fuera, 1):
        print(f"{i}. Ficha en la posición {ficha.posicion} (en seguro: {ficha.en_seguro}, en meta: {ficha.en_meta})")

    # Opción para elegir la ficha
    opcion_ficha = int(input(f"Elige qué ficha mover (1-{len(fichas_fuera)}): ").strip())
    ficha_elegida = fichas_fuera[opcion_ficha - 1]

    ficha_elegida.mover(tirada1 + tirada2)
    print(f"Has elegido la ficha {opcion_ficha} para mover {tirada1 + tirada2} pasos.")

    # Verificar si el jugador ha ganado
    if jugador.ha_ganado():
        print(f"¡{jugador.nombre} ha ganado el juego!")
        return True  # El jugador ha ganado, termina el juego

    return False  # El juego continúa


# Inicia el juego
jugadores = inicio_del_juego()

# Loop principal del juego
while True:
    for jugador in jugadores:
        if turno_de_jugador(jugador):
            break  # Termina el juego si algún jugador ha ganado
