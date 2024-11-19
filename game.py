import random

class Jugador:
    def __init__(self, nombre, color, numero):
        self.nombre = nombre
        self.color = color
        self.numero = numero  #numero de jugador 
        self.fichas = [Ficha(casilla_salida=Tablero().salidas[self.numero]) for _ in range(4)]
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
        self.en_meta = False  
        self.casilla_salida = casilla_salida
        self.casilla_llegada = casilla_llegada  # Inicio de las casillas de llegada específicas
    
    def sacar_de_carcel(self):
        if self.en_carcel:
            self.posicion = self.casilla_salida
            self.en_carcel = False
            self.en_seguro = True  

    def mover(self, pasos, tablero):
        if self.en_carcel:
            raise Exception("No puedes mover una ficha que está en la cárcel.")
        if self.en_meta:
            raise Exception("No puedes mover una ficha que ya llegó a la meta.")

        if not self.en_llegada:
            # Movimiento en las casillas generales
            nueva_posicion = (self.posicion + pasos) % 68
            if nueva_posicion == self.casilla_llegada:
                self.en_llegada = True
                self.posicion = 0  # Primera casilla de llegada
                self.en_seguro = True  # Todas las casillas de llegada empiezan como seguras
            else:
                self.posicion = nueva_posicion
                self.en_seguro = tablero.tipo_de_casilla_general(self.posicion) == "seguro"

        else:
            # Movimiento en las casillas de llegada
            nueva_posicion = self.posicion + pasos
            if nueva_posicion < len(tablero.casillas_de_llegada):
                self.posicion = nueva_posicion
                if nueva_posicion == len(tablero.casillas_de_llegada) + 1: #justo despues de la septima casilla se llega a la meta
                    self.en_meta = True
            else:
                raise Exception("Movimiento inválido: no puedes salir de las casillas de llegada.")

    def enviar_a_carcel(self):
        if not self.en_seguro:
            self.posicion = None
            self.en_carcel = True
            self.en_seguro = False


class Tablero:
    def __init__(self):
        self.casillas = ["normal"] * 68
        self.salidas = {1: 1, 2: 18, 3: 35, 4: 52}  # casillas de salida por jugador
        self.llegadas = {1: 64, 2: 13, 3: 30, 4: 47}  # inicio de las casillas de llegada
        self.casillas_de_llegada = ["seguro"]* 6
        self.definir_especiales()

    def definir_especiales(self):
        for i in [8, 13, 25, 30, 42, 47, 59, 64]:  # seguros
            self.casillas[i] = "seguro"
        for salida in self.salidas.values():  # salidas
            self.casillas[salida] = "salida"
    
    def tipo_de_casilla(self, posicion):
        if 0 <= posicion < len(self.casillas):
            return self.casillas[posicion]

