import random

class Tablero:
    def __init__(self):
        self.casillas = ["normal"] * 68
        self.salidas = {1: 1, 2: 18, 3: 35, 4: 52}  # casillas de salida por jugador
        self.llegadas = {1: 64, 2: 13, 3: 30, 4: 47}  # inicio de las casillas de llegada
        self.casillas_de_llegada = ["seguro"]* 7
        self.definir_especiales()

    def definir_especiales(self):
        for i in [8, 13, 25, 30, 42, 47, 59, 64]:  # seguros
            self.casillas[i] = "seguro"
        for salida in self.salidas.values():  # salidas
            self.casillas[salida] = "salida"
    
    def tipo_de_casilla(self, posicion):
        if 0 <= posicion < len(self.casillas):
            return self.casillas[posicion]



class Jugador:
    def __init__(self, nombre, color, numero):
        self.nombre = nombre
        self.color = color
        self.numero = numero  #numero de jugador 
        self.salida = tablero.salidas[self.numero]
        self.llegada = tablero.llegadas[self.numero]
        self.fichas = [Ficha(self.salida, self.llegada) for _ in range(4)]
        self.bloqueado = False  # inicialmente, todos los jugadores estan bloqueados
        self.turno = False 
        self.fichas_fuera = 0           
        self.fichas_meta = 0 
    
    def desbloquear(self):
        self.bloqueado = False

    def bloquear(self):
        self.bloqueado = True
        

class Ficha:
    def __init__(self, casilla_salida, casilla_llegada):
        self.en_carcel = True  
        self.posicion = None  # posición actual en el tablero (None si está en la cárcel)
        self.en_seguro = False 
        self.en_llegada = False 
        self.en_meta = False  
        self.casilla_salida = casilla_salida
        self.casilla_llegada = casilla_llegada  # Inicio de las casillas de llegada específicas
    
    def sacar_de_carcel(self):
        if self.en_carcel:
            self.posicion = self.casilla_salida
            self.en_carcel = False
            self.en_seguro = True  

    def mover(self, pasos):
        if self.en_carcel:
            raise Exception("No puedes mover una ficha que está en la cárcel.")
        if self.en_meta:
            raise Exception("No puedes mover una ficha que ya llegó a la meta.")

        if not self.en_llegada:
            # movimiento en las casillas generales
            nueva_posicion = (self.posicion + pasos) % 68
            if nueva_posicion == self.casilla_llegada:
                self.en_llegada = True
                self.posicion = 0  # primera casilla de llegada
                self.en_seguro = True  # todas las casillas de llegada empiezan como seguras
            else:
                self.posicion = nueva_posicion
                self.en_seguro = tablero.tipo_de_casilla(self.posicion) in ["seguro", "salida"]

        else:
            # movimiento en las casillas de llegada
            nueva_posicion = self.posicion + pasos
            if nueva_posicion < len(tablero.casillas_de_llegada):
                self.posicion = nueva_posicion
                if nueva_posicion == len(tablero.casillas_de_llegada) + 1: # justo despues de la septima casilla de llega es la meta
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
        self.valor = random.randint(1,6)
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

    return tablero, jugadores


def determinar_jugador_inicial(jugadores):
    print("Determinando quién comienza el juego...")
    dado = Dado()
    max_valor = -1
    jugador_inicial = None

    # Cada jugador lanza el dado
    for jugador in jugadores:
        valor = dado.lanzar()
        print(f"{jugador.nombre} lanzó el dado y obtuvo {valor}.")
        if valor > max_valor:
            max_valor = valor
            jugador_inicial = jugador
        

    print(f"{jugador_inicial.nombre} comienza el juego.")
    return jugador_inicial




