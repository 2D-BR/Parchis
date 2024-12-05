def mostrar_tablero(tablero):
    for fila in tablero:
        print(" ".join(fila))

def crear_tablero(filas, columnas):
    # Crear un tablero vacío de tamaño filas x columnas
    tablero = [[" " for _ in range(columnas)] for _ in range(filas)]
    return tablero

def agregar_parque(tablero, fila, columna):
    # Colocar un parque en la posición dada (si es válida)
    if 0 <= fila < len(tablero) and 0 <= columna < len(tablero[0]):
        tablero[fila][columna] = "P"

# Crear un tablero de 5x5
tablero = crear_tablero(5, 5)

# Agregar algunos parques
agregar_parque(tablero, 1, 1)
agregar_parque(tablero, 3, 3)
agregar_parque(tablero, 4, 0)

# Mostrar el tablero
mostrar_tablero(tablero)
